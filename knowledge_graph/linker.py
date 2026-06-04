"""
Knowledge Graph Linker — 把分散的 JSON 织成统一图谱
Usage: python knowledge_graph/linker.py [--search "keyword"] [--graph]
Scans all JSONs in knowledge_graph/ and builds cross-project connections.
"""

import json, sys, argparse
from pathlib import Path
from collections import defaultdict

KG_DIR = Path(__file__).parent


def load_all() -> list:
    """Load all knowledge graph JSONs."""
    entries = []
    for f in sorted(KG_DIR.glob("*.json")):
        if f.name in ("index.json", "graph.json"):
            continue
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                entry = json.load(fp)
                entry["_file"] = f.name
                entries.append(entry)
        except Exception as e:
            print(f"  SKIP {f.name}: {e}")
    return entries


def index_by_field(entries: list, field_path: str) -> dict:
    """Index entries by a dot-separated field path."""
    index = defaultdict(list)
    for e in entries:
        val = e
        for key in field_path.split("."):
            if isinstance(val, dict):
                val = val.get(key, None)
            elif isinstance(val, list):
                # For list fields, index each item
                if key == "[]":
                    for item in val:
                        if isinstance(item, dict):
                            for k, v in item.items():
                                if k != "description" and k != "statement":
                                    index[str(v)].append(e["_file"])
                    val = None
                    break
                else:
                    val = [item.get(key) for item in val if isinstance(item, dict)]
            else:
                val = None
                break
        if val:
            if isinstance(val, list):
                for v in val:
                    if v:
                        index[str(v)].append(e["_file"])
            else:
                index[str(val)].append(e["_file"])
    return dict(index)


def build_links(entries: list) -> list:
    """Build cross-project links based on shared fields."""
    links = []

    # Link by math_objects (new format) or nodes (legacy format)
    math_index = defaultdict(list)
    for e in entries:
        # New format: claims[].math_objects
        for claim in e.get("claims", []):
            for mo in claim.get("math_objects", []):
                math_index[mo.lower()].append(e["_file"])
        # Legacy format: nodes[].label
        for node in e.get("nodes", []):
            lbl = node.get("label", "")
            if lbl:
                math_index[lbl.lower()[:60]].append(e["_file"])

    for mo, files in math_index.items():
        if len(files) >= 2:
            links.append({
                "type": "shared_math_object",
                "math_object": mo,
                "projects": files,
                "strength": "strong"
            })

    # Link by shared references (DOI)
    doi_index = defaultdict(list)
    for e in entries:
        for ref in e.get("references", []):
            doi = ref.get("doi", "")
            if doi:
                doi_index[doi].append(e["_file"])

    for doi, files in doi_index.items():
        if len(files) >= 2:
            label = ""
            for e in entries:
                for ref in e.get("references", []):
                    if ref.get("doi") == doi:
                        label = ref.get("label", doi)
                        break
            links.append({
                "type": "shared_reference",
                "reference": label,
                "doi": doi,
                "projects": files,
                "strength": "medium"
            })

    # Link by domain
    domain_index = defaultdict(list)
    for e in entries:
        proj = e.get("project", {})
        domain = proj.get("domain", "") if isinstance(proj, dict) else ""
        if domain:
            domain_index[domain].append(e["_file"])

    for domain, files in domain_index.items():
        if len(files) >= 2:
            links.append({
                "type": "shared_domain",
                "domain": domain,
                "projects": files,
                "strength": "weak"
            })

    # Link by selector_strategy
    strategy_index = defaultdict(list)
    for e in entries:
        proj = e.get("project", {})
        strat = proj.get("selector_strategy", "") if isinstance(proj, dict) else ""
        if strat:
            strategy_index[strat].append(e["_file"])

    for strat, files in strategy_index.items():
        if len(files) >= 2:
            links.append({
                "type": "shared_strategy",
                "strategy": strat,
                "projects": files,
                "strength": "weak"
            })

    return links


def search(entries: list, query: str) -> list:
    """Full-text search across all fields."""
    results = []
    q = query.lower()
    for e in entries:
        # Flatten to string for search
        flat = json.dumps(e, ensure_ascii=False).lower()
        if q in flat:
            proj = e.get("project", {})
            if isinstance(proj, str):
                proj = {"id": proj, "title": "", "domain": "", "status": e.get("status", "")}
            verdict = proj.get("verdict", "") if isinstance(proj, dict) else e.get("primary_contribution", "")
            results.append({
                "file": e["_file"],
                "project_id": proj.get("id", "?") if isinstance(proj, dict) else proj,
                "title": (proj.get("title", "") if isinstance(proj, dict) else "")[:80],
                "domain": (proj.get("domain", "") if isinstance(proj, dict) else ""),
                "status": (proj.get("status", "") if isinstance(proj, dict) else e.get("status", "")),
                "verdict": verdict[:120] if isinstance(verdict, str) else str(verdict)[:120]
            })
    return results


def build_index(entries: list) -> dict:
    """Build a searchable index file."""
    return {
        "total_entries": len(entries),
        "by_domain": dict(index_by_field(entries, "project.domain")),
        "by_strategy": dict(index_by_field(entries, "project.selector_strategy")),
        "by_status": dict(index_by_field(entries, "project.status")),
        "by_math_object": dict(index_by_field(entries, "claims[].math_objects")),
        "shared_references": dict(index_by_field(entries, "references[].doi")),
        "all_files": [e["_file"] for e in entries]
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Knowledge Graph Linker")
    parser.add_argument("--search", help="Search query across all entries")
    parser.add_argument("--contributor", help="Search by ORCID or GitHub username")
    parser.add_argument("--graph", action="store_true", help="Show cross-project connections")
    parser.add_argument("--index", action="store_true", help="Build and save searchable index")
    parser.add_argument("--stats", action="store_true", help="Show collection statistics")
    args = parser.parse_args()

    entries = load_all()
    if not entries:
        print("No knowledge graph entries found in", KG_DIR)
        print("Submit your first: run a Polaris课题 → GATE 7 → drop JSON here")
        sys.exit(0)

    if args.contributor:
        q = args.contributor.lower()
        results = []
        for e in entries:
            proj = e.get("project", {})
            contrib = proj.get("contributor", {}) if isinstance(proj, dict) else {}
            orcid = contrib.get("orcid", "").lower()
            github = contrib.get("github", "").lower()
            name = contrib.get("name", "").lower()
            if q in orcid or q in github or q in name:
                results.append(e)
        print(f"\nContributor '{args.contributor}' → {len(results)} entries\n")
        for e in results:
            proj = e.get("project", {})
            contrib = proj.get("contributor", {}) if isinstance(proj, dict) else {}
            print(f"  [{proj.get('id', '?')}] {proj.get('title', '')[:70]}")
            print(f"       ORCID={contrib.get('orcid','?')}  GitHub={contrib.get('github','?')}  name={contrib.get('name','?')}")

    elif args.search:
        results = search(entries, args.search)
        print(f"\nSearch: '{args.search}' → {len(results)} hits\n")
        for r in results:
            print(f"  [{r['project_id']}] {r['title']}")
            print(f"       domain={r['domain']}  status={r['status']}")
            print(f"       {r['verdict']}\n")

    elif args.graph:
        links = build_links(entries)
        print(f"\nCross-Project Links ({len(links)} found):\n")
        for link in sorted(links, key=lambda l: l["strength"], reverse=True):
            icon = {"strong": "🔴", "medium": "🟡", "weak": "⚪"}.get(link["strength"], "?")
            print(f"  {icon} [{link['type']}] {link.get(list(link.keys())[1], '')}")
            for proj in link["projects"]:
                print(f"       <- {proj}")

    elif args.index:
        index = build_index(entries)
        index_path = KG_DIR / "index.json"
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        print(f"Index saved to {index_path}")
        print(f"  {index['total_entries']} entries indexed")
        print(f"  Domains: {list(index['by_domain'].keys())}")
        print(f"  Strategies: {list(index['by_strategy'].keys())}")

    elif args.stats:
        print(f"\nKnowledge Graph Stats:")
        print(f"  Total entries: {len(entries)}")
        domains = set()
        for e in entries:
            proj = e.get("project", {})
            d = proj.get("domain", "unknown") if isinstance(proj, dict) else "unknown"
            domains.add(d)
        print(f"  Domains covered: {list(domains)}")
        links = build_links(entries)
        print(f"  Cross-project links: {len(links)}")
        print(f"  Strong links (shared math): {sum(1 for l in links if l['strength']=='strong')}")
        print(f"  Medium links (shared refs): {sum(1 for l in links if l['strength']=='medium')}")
        print(f"  Weak links (shared domain): {sum(1 for l in links if l['strength']=='weak')}")

    else:
        # Default: show summary
        print(f"\nKnowledge Graph: {len(entries)} entries\n")
        for e in entries:
            proj = e.get("project", {})
            if isinstance(proj, str):
                # Legacy format
                print(f"  [{proj}] {e.get('primary_contribution', '')[:70]}")
                print(f"       nodes={len(e.get('nodes',[]))}  status={e.get('status','?')}")
                print(f"       survived claims: {len(e.get('surviving_claims',[]))}")
            else:
                claims = e.get("claims", [])
                survived = [c for c in claims if c.get("status") == "survived"]
                print(f"  [{proj.get('id', '?')}] {proj.get('title', '')[:70]}")
                print(f"       domain={proj.get('domain','')}  rounds={proj.get('rounds','?')}  status={proj.get('status','')}")
                print(f"       survived claims: {len(survived)}  lessons: {len(e.get('lessons',[]))}")
        print(f"\n  --graph   show cross-project connections")
        print(f"  --search  full-text search")
        print(f"  --index   build searchable index")
        print(f"  --stats   collection statistics")
