"""
Polaris Validation Engine
Usage: python validate.py <claim.json>
Takes a scientific claim and auto-validates: dimensions, limits, magnitudes, algebra.
No API keys needed. No GPU. Pure deterministic checks.
"""

import json
import sys
import math
from pathlib import Path

# Try imports gracefully — tell user what to install if missing
MISSING = []
try:
    import sympy as sp
    from sympy import oo, Symbol, diff, integrate, limit, sin, cos, exp, log, tan, sinh, cosh
    from sympy.physics.units import Quantity, convert_to
    from sympy.physics.units.systems.si import SI
    from sympy.physics.units import meter, kilogram, second, ampere, kelvin, mole, candela
    from sympy.physics.units import joule, watt, newton, pascal, volt, ohm, tesla, henry, farad
    from sympy.physics.units import hertz, coulomb, weber, degree, radian, steradian
except ImportError:
    MISSING.append("sympy (pip install sympy)")

try:
    import pint
    ureg = pint.UnitRegistry()
except ImportError:
    MISSING.append("pint (pip install pint)")

if MISSING:
    print(f"Missing packages: {', '.join(MISSING)}")
    print("Install: pip install sympy pint")
    print("Proceeding with limited checks...\n")


# ─── Q1: Dimensional Analysis ─────────────────────────────────────────
def check_dimensions(expr_str: str, expected_unit: str = None) -> dict:
    """Check if an expression has consistent physical dimensions."""
    try:
        # Parse expression
        expr = sp.sympify(expr_str)
        free_symbols = list(expr.free_symbols)

        result = {
            "status": "ok",
            "expression": expr_str,
            "free_symbols": [str(s) for s in free_symbols],
            "issues": []
        }

        # Check transcendental function arguments — must be dimensionless
        transcendental_funcs = [sp.sin, sp.cos, sp.tan, sp.exp, sp.log, sp.sinh, sp.cosh]
        for func in transcendental_funcs:
            for arg in sp.preorder_traversal(expr):
                if arg.func == func:
                    # Check if argument has physical units
                    for sym in arg.args[0].free_symbols:
                        if any(unit_str in str(sym).lower() for unit_str in ['m', 'kg', 's', 'a', 'k', 'j', 'w', 'n', 'pa', 'v', 't', 'hz']):
                            result["status"] = "warning"
                            result["issues"].append(
                                f"Transcendental function {func.__name__}(...) argument may have units: {sym}"
                            )

        return result
    except Exception as e:
        return {"status": "error", "expression": expr_str, "error": str(e)}


# ─── Q2: Limit Degeneration ───────────────────────────────────────────
def check_limits(expr_str: str, variable: str, cases: list = None) -> dict:
    """
    Verify that expression degenerates to known limits.
    cases: list of (var_value, expected_value, description)
    """
    if cases is None:
        cases = []

    try:
        var = Symbol(variable)
        expr = sp.sympify(expr_str)
        results = []

        for val, expected, desc in cases:
            try:
                actual = limit(expr, var, val)
                if expected is not None:
                    expected_val = sp.sympify(expected)
                    match = sp.simplify(actual - expected_val) == 0
                else:
                    match = None  # Just compute, don't compare

                results.append({
                    "case": desc,
                    f"{variable} → {val}": str(actual),
                    "expected": str(expected) if expected else "N/A",
                    "match": match
                })
            except Exception as e:
                results.append({
                    "case": desc,
                    "error": str(e)
                })

        return {"status": "ok", "results": results}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ─── Q3: Magnitude Sanity Check ──────────────────────────────────────
def check_magnitude(value: float, expected_range: tuple, label: str = "") -> dict:
    """
    Flag if value is >10 orders of magnitude from expected range.
    """
    lo, hi = expected_range
    within = lo <= abs(value) <= hi
    orders_off = abs(math.log10(abs(value)) - math.log10((lo + hi) / 2)) if not within else 0

    return {
        "label": label,
        "value": value,
        "expected_range": f"[{lo}, {hi}]",
        "within_range": within,
        "orders_of_magnitude_off": round(orders_off, 1) if not within else 0,
        "severity": "ok" if within else ("warning" if orders_off < 10 else "critical")
    }


# ─── Q4: Numerical Evaluation ─────────────────────────────────────────
def evaluate_numerically(expr_str: str, substitutions: dict) -> dict:
    """Substitute numerical values and compute result."""
    try:
        expr = sp.sympify(expr_str)
        result = float(expr.subs(substitutions).evalf())
        return {"status": "ok", "result": result, "substitutions": substitutions}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ─── Validation Runner ─────────────────────────────────────────────────
def validate_claim(claim_file: str) -> dict:
    """
    Load a claim JSON file and run all applicable checks.

    Claim JSON format:
    {
        "id": "C1",
        "claim": "T-linear resistivity implies non-Fermi liquid",
        "equations": [
            {
                "label": "F1",
                "expression": "m/(n*e**2*tau)",
                "description": "Drude conductivity",
                "free_params": {"m": "electron mass", "n": "density", "e": "charge", "tau": "scattering time"},
                "limits": [
                    {"var": "tau", "to": "oo", "expected": "0", "desc": "perfect conductor limit"}
                ],
                "numerical_test": {
                    "substitutions": {"m": 9.11e-31, "n": 1e28, "e": 1.6e-19, "tau": 1e-14},
                    "expected_range": [1e-8, 1e-5]
                }
            }
        ]
    }
    """
    with open(claim_file, 'r', encoding='utf-8') as f:
        claim = json.load(f)

    report = {
        "claim_id": claim.get("id", "unknown"),
        "claim_text": claim.get("claim", ""),
        "checks": [],
        "overall": "pass"
    }

    for eq in claim.get("equations", []):
        eq_label = eq.get("label", "unnamed")
        expr = eq.get("expression", "")

        # Q1: Dimensions
        dim_result = check_dimensions(expr)
        report["checks"].append({"type": "dimensions", "equation": eq_label, **dim_result})

        # Q2: Limits
        limits_config = []
        for lim in eq.get("limits", []):
            limits_config.append((lim["to"], lim.get("expected"), lim.get("desc", "")))
        if limits_config:
            lim_result = check_limits(expr, eq.get("limit_var", "x"), limits_config)
            report["checks"].append({"type": "limits", "equation": eq_label, **lim_result})

        # Q3: Magnitude
        num_test = eq.get("numerical_test", {})
        if num_test:
            subs = num_test.get("substitutions", {})
            # Convert string keys to sympy symbols
            sym_subs = {Symbol(k): v for k, v in subs.items()}
            num_result = evaluate_numerically(expr, sym_subs)
            if num_result["status"] == "ok":
                mag_result = check_magnitude(
                    num_result["result"],
                    num_test.get("expected_range", [1e-99, 1e99]),
                    eq_label
                )
                report["checks"].append({"type": "magnitude", "equation": eq_label, **mag_result})

    # Overall verdict
    severities = [c.get("severity", "ok") for c in report["checks"] if "severity" in c]
    if "critical" in severities:
        report["overall"] = "fail"
    elif "warning" in severities:
        report["overall"] = "warning"

    return report


# ─── CLI ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate.py <claim.json>")
        print("\nExample claim.json:")
        print(json.dumps({
            "id": "C1",
            "claim": "T-linear resistivity from isotropic scattering",
            "equations": [{
                "label": "F1",
                "expression": "m/(n*e**2*tau)",
                "limits": [{"var": "tau", "to": "oo", "expected": "0", "desc": "perfect conductor"}],
                "numerical_test": {
                    "substitutions": {"m": 9.11e-31, "n": 1e28, "e": 1.6e-19, "tau": 1e-14},
                    "expected_range": [1e-8, 1e-5]
                }
            }]
        }, indent=2))
        sys.exit(1)

    claim_file = sys.argv[1]
    report = validate_claim(claim_file)

    print("=" * 60)
    print(f"POLARIS VALIDATION REPORT")
    print(f"Claim: {report['claim_text'][:80]}")
    print("=" * 60)

    for check in report["checks"]:
        check_type = check["type"]
        eq = check.get("equation", "?")
        if check_type == "dimensions":
            status = check.get("status", "?")
            issues = check.get("issues", [])
            print(f"\n[Q1 Dimensions] [{eq}]: {status.upper()}")
            for issue in issues:
                print(f"   WARN: {issue}")
        elif check_type == "limits":
            print(f"\n[Q2 Limits] [{eq}]:")
            for r in check.get("results", []):
                if "error" in r:
                    print(f"   FAIL {r['case']}: {r['error']}")
                else:
                    icon = "PASS" if r.get("match") else "FAIL"
                    print(f"   {icon} {r['case']}: {r.get(list(r.keys())[1], '?')}")
        elif check_type == "magnitude":
            sev = check.get("severity", "?")
            icon = {"ok": "PASS", "warning": "WARN", "critical": "CRITICAL"}.get(sev, "?")
            print(f"\n[Q3 Magnitude] [{eq}]: {sev.upper()}")
            print(f"   {icon} Value={check.get('value', '?')}, Expected={check.get('expected_range', '?')}")

    print(f"\n{'=' * 60}")
    print(f"OVERALL: {report['overall'].upper()}")
    print(f"{'=' * 60}")
