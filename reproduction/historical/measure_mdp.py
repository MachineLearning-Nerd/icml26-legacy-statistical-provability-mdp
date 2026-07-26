"""Small finite-MDP helpers reconstructed for the historical toy verifier.

This module is intentionally scoped to reproducing the rejected baseline. It is
not evidence for any theorem in the paper.
"""

from __future__ import annotations

import numpy as np


def solve_mdp_backward(P, R, gamma, goal, horizon):
    """Return the horizon value and last greedy action for the six-state proxy."""
    state_count, action_count, _ = P.shape
    value = np.array([1.0 if state in goal else 0.0 for state in range(state_count)])
    policy = np.zeros(state_count, dtype=int)
    for _ in range(horizon):
        q_value = R + gamma * np.einsum("sak,k->sa", P, value)
        for state in range(state_count):
            if state in goal:
                value[state] = 1.0
                policy[state] = 0
            else:
                policy[state] = int(np.argmax(q_value[state]))
                value[state] = q_value[state, policy[state]]
    return value, policy


def bellman_certificate(P, R, gamma, goal, horizon, lower_funcs, upper_funcs):
    """Reproduce the historical proxy sandwich check.

    The original Space called this a Bellman certificate although its displayed
    source constructed bounds around the already-solved final value. We preserve
    that behavior so the control remains honest and comparable.
    """
    value, _ = solve_mdp_backward(P, R, gamma, goal, horizon)
    lower_ok = all(np.all(candidate <= value + 1e-12) for candidate in lower_funcs)
    upper_ok = all(np.all(candidate + 1e-12 >= value) for candidate in upper_funcs)
    return bool(lower_ok), bool(upper_ok)


def score_guided_planning(P, R, gamma, goal, horizon, scores, eps_errors):
    """Evaluate the fixed score-greedy toy policy used by the rejected baseline."""
    del eps_errors  # Historical source never perturbed scores with this quantity.
    value_opt, _ = solve_mdp_backward(P, R, gamma, goal, horizon)
    policy = np.argmax(scores, axis=1)
    state_count = P.shape[0]
    value_policy = np.array(
        [1.0 if state in goal else 0.0 for state in range(state_count)]
    )
    for _ in range(horizon):
        updated = np.empty_like(value_policy)
        for state in range(state_count):
            if state in goal:
                updated[state] = 1.0
            else:
                action = int(policy[state])
                updated[state] = (
                    R[state, action] + gamma * P[state, action].dot(value_policy)
                )
        value_policy = updated
    regret = value_opt - value_policy
    return value_opt, value_policy, regret, None
