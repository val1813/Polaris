"""
Polaris-Bench Generator
Takes a template contradiction + domain → generates new benchmark with known answer.
Usage: python benchmarks/generate.py --template B01 --domain "cosmology" --count 3
"""

import json, sys, argparse
from pathlib import Path

BENCH_DIR = Path(__file__).parent

TEMPLATES = {
    "experiment_vs_theory": {
        "pattern": "实验观测X与理论预测Y存在≥3σ偏离",
        "generator_prompt": """
Given a physics domain, generate a historically RESOLVED contradiction where:
1. An experimental measurement disagreed with the best theory at the time (≥3 sigma)
2. The resolution required a fundamental change in assumptions (not just better measurements)
3. The resolution is now textbook knowledge

Output as JSON with: id, title, domain, contradiction (proposition_A/B/why_not_both),
ground_truth (resolution/key_insight/theory/landmark_paper), references.
"""
    },
    "hidden_assumption": {
        "pattern": "所有人默认的前提H从未被检验，¬H未被考虑",
        "generator_prompt": """
Given a physics domain, identify a hidden assumption that:
1. Was universally accepted in that domain before a certain date
2. Was later proven false by experiment or theory
3. Its negation led to a major breakthrough (textbook knowledge today)

Output the hidden assumption, what replaced it, and the landmark paper.
"""
    },
    "two_theories_clash": {
        "pattern": "两个成熟理论在边界处给出相反预言",
        "generator_prompt": """
Find a historically resolved case where two well-established theories made contradictory
predictions about the same observable in the same parameter regime. The resolution
required a third, deeper theory that contained both as limiting cases.
"""
    }
}


def generate_from_template(template_name: str, domain: str, count: int = 1) -> list:
    """
    Generate benchmark entries by asking an AI to fill in a template.
    This script prints the prompt — the actual generation is done by Claude/LLM.
    """
    template = TEMPLATES.get(template_name)
    if not template:
        print(f"Unknown template: {template_name}")
        print(f"Available: {list(TEMPLATES.keys())}")
        return []

    prompts = []
    for i in range(count):
        prompts.append({
            "template": template_name,
            "domain": domain,
            "prompt": template["generator_prompt"] + f"\n\nDomain: {domain}\nGenerate benchmark entry #{i+1}."
        })

    return prompts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Polaris-Bench Generator")
    parser.add_argument("--template", default="hidden_assumption",
                       choices=list(TEMPLATES.keys()))
    parser.add_argument("--domain", default="condensed matter",
                       help="Physics domain to generate for")
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    prompts = generate_from_template(args.template, args.domain, args.count)
    for p in prompts:
        print(f"\n{'='*60}")
        print(f"Template: {p['template']} | Domain: {p['domain']}")
        print(f"{'='*60}")
        print(f"\nGive this to Claude:\n")
        print(p['prompt'])
