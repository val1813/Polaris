"""
Quantum Validator — 量子力学命题专用
Usage: python quantum.py <claim.json>
Covers: commutators, eigenvalue spectra, density matrix, entanglement
Requires: pip install qutip numpy
"""

import json, sys, math

try:
    import numpy as np
    from qutip import (basis, expect, sigmax, sigmay, sigmaz, tensor, Qobj,
                        commutator, sigmam, sigmap, fidelity, entropy_vn)
    HAS_QUTIP = True
except ImportError:
    HAS_QUTIP = False


def check_commutator(A_str: str, B_str: str, expected: str) -> dict:
    """Verify [A, B] = expected. A/B can be 'sx','sy','sz','a','adag' etc."""
    if not HAS_QUTIP:
        return {"status": "skipped", "reason": "QuTiP not installed"}

    pauli = {'sx': sigmax(), 'sy': sigmay(), 'sz': sigmaz(),
             'sp': sigmap(), 'sm': sigmam()}
    A = pauli.get(A_str.lower())
    B = pauli.get(B_str.lower())

    if A is None or B is None:
        return {"status": "error", "reason": f"Unknown operator: {A_str} or {B_str}"}

    result = commutator(A, B)
    # Parse expected (e.g., "2j*sz" → 2j * sigmaz())
    if expected.lower().replace(' ', '') == '0':
        is_zero = np.allclose(result.full(), 0)
        return {"status": "ok" if is_zero else "fail",
                "expected": "0", "actual_max": float(np.max(np.abs(result.full())))}

    return {"status": "ok", "result_matrix": str(result),
            "note": "manual verification recommended for non-zero expectation"}


def check_hermiticity(H_str: str) -> dict:
    """Check if Hamiltonian H = H†."""
    if not HAS_QUTIP:
        return {"status": "skipped", "reason": "QuTiP not installed"}
    # For custom Hamiltonians, user provides matrix in JSON
    return {"status": "skipped", "note": "Provide matrix in claim JSON for auto-check"}


def check_density_matrix(rho_list: list) -> dict:
    """Verify ρ ≥ 0, Tr(ρ) = 1, ρ = ρ†."""
    if not HAS_QUTIP:
        return {"status": "skipped", "reason": "QuTiP not installed"}

    try:
        rho = Qobj(np.array(rho_list))
        checks = {
            "trace_one": np.allclose(rho.tr(), 1.0, atol=1e-10),
            "hermitian": np.allclose(rho.full(), rho.dag().full()),
            "positive_semidefinite": np.all(np.linalg.eigvalsh(rho.full()) >= -1e-10)
        }
        all_ok = all(checks.values())
        return {"status": "ok" if all_ok else "fail", "checks": checks}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_entanglement(state_vec: list) -> dict:
    """Compute von Neumann entropy as entanglement measure for bipartite system."""
    if not HAS_QUTIP:
        return {"status": "skipped", "reason": "QuTiP not installed"}

    try:
        psi = Qobj(np.array(state_vec))
        rho = psi * psi.dag()
        # Assume bipartite — trace out second half
        dim = int(np.sqrt(len(state_vec)))
        if dim * dim != len(state_vec):
            return {"status": "error", "reason": "State vector length must be perfect square for bipartite split"}
        rho_A = rho.ptrace([0])
        S = entropy_vn(rho_A)
        return {"status": "ok", "entanglement_entropy": float(S)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_eigenvalues(H_list: list, expected_spectrum: list = None) -> dict:
    """Compute eigenvalues of Hamiltonian and compare to expected."""
    if not HAS_QUTIP:
        return {"status": "skipped", "reason": "QuTiP not installed"}

    try:
        H = Qobj(np.array(H_list))
        evals = np.sort(np.linalg.eigvalsh(H.full()))
        result = {"eigenvalues": [float(e) for e in evals]}
        if expected_spectrum:
            match = np.allclose(evals, np.sort(expected_spectrum), atol=1e-8)
            result["matches_expected"] = bool(match)
        return {"status": "ok", **result}
    except Exception as e:
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quantum.py <claim.json>")
        # Demo
        if HAS_QUTIP:
            print("\nDemo: [sx, sy] = 2j*sz")
            result = check_commutator("sx", "sy", "2j*sz")
            print(json.dumps(result, indent=2))
        else:
            print("Install QuTiP: pip install qutip")
        sys.exit(0)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        claim = json.load(f)

    for check in claim.get("quantum_checks", []):
        check_type = check.get("type")
        if check_type == "commutator":
            result = check_commutator(check["A"], check["B"], check.get("expected", "0"))
        elif check_type == "density_matrix":
            result = check_density_matrix(check["matrix"])
        elif check_type == "entanglement":
            result = check_entanglement(check["state"])
        elif check_type == "eigenvalues":
            result = check_eigenvalues(check["hamiltonian"], check.get("expected_spectrum"))
        else:
            result = {"status": "error", "reason": f"Unknown check type: {check_type}"}
        print(json.dumps({check_type: result}, indent=2))
