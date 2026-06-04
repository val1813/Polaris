"""
Extract INSPECTOR_CHECK blocks from derivation files → claim.json
Usage: python extract.py <derivation.md> > claim.json
INSPECTOR uses this to convert A/B outputs into validate.py input.
"""

import sys, re, json
from pathlib import Path


def extract_checks(filepath: str) -> list:
    """Parse --- INSPECTOR_CHECK --- blocks from markdown."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by INSPECTOR_CHECK markers
    blocks = re.split(r'---\s*INSPECTOR_CHECK\s*---', content)

    checks = []
    for i, block in enumerate(blocks[1:], 1):  # skip pre-first-marker
        check = {"index": i}

        # Extract fields
        formula = re.search(r'\[公式\]\s*(.+?)(?:\n\[|\Z)', block, re.DOTALL)
        direction = re.search(r'\[方向\]\s*(.+?)(?:\n\[|\Z)', block, re.DOTALL)
        data_src = re.search(r'\[数据\]\s*(.+?)(?:\n\[|\Z)', block, re.DOTALL)
        assumption = re.search(r'\[假设\]\s*(.+?)(?:\n\[|\Z)', block, re.DOTALL)

        if formula:
            check["formula_text"] = formula.group(1).strip()
            # Try to extract LaTeX expression
            latex = re.findall(r'\$([^$]+)\$', formula.group(1))
            if latex:
                check["expression"] = latex[0].strip()
                # Remove LaTeX commands for sympy
                clean = latex[0].replace('\\', '').replace('{', '').replace('}', '')
                check["expression_clean"] = clean

        if direction:
            check["direction"] = direction.group(1).strip()
        if data_src:
            check["data_source"] = data_src.group(1).strip()
        if assumption:
            check["assumptions"] = assumption.group(1).strip()

        checks.append(check)

    return checks


def build_claim_json(checks: list, claim_id: str = "AUTO") -> dict:
    """Convert extracted checks into validate.py-compatible claim JSON."""
    equations = []
    for c in checks:
        eq = {"label": f"EQ-{c['index']}", "description": c.get("formula_text", "")}
        if "expression_clean" in c:
            eq["expression"] = c["expression_clean"]
        if "direction" in c:
            eq["direction_claim"] = c["direction"]
        equations.append(eq)

    return {
        "id": claim_id,
        "claim": f"Extracted from {len(checks)} INSPECTOR_CHECK blocks",
        "equations": equations
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract.py <derivation.md> [--json]")
        print("  Converts INSPECTOR_CHECK blocks to claim.json format")
        print("  --json: output claim.json for validate.py")
        sys.exit(1)

    filepath = sys.argv[1]
    checks = extract_checks(filepath)

    if "--json" in sys.argv:
        claim = build_claim_json(checks, claim_id=Path(filepath).stem)
        print(json.dumps(claim, indent=2, ensure_ascii=False))
    else:
        print(f"Found {len(checks)} INSPECTOR_CHECK blocks:")
        for c in checks:
            print(f"\n  [{c['index']}] {c.get('formula_text', '?')[:80]}")
            if "expression_clean" in c:
                print(f"      expr: {c['expression_clean'][:60]}")
