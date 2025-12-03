from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class ClientUtility:
    """Container mirroring the utility signals that Oort consumes."""

    client_id: str
    statistical_utility: float
    gradient_utility: float
    duration: float  # wall clock or simulated round duration
    data_diversity_score: Optional[float] = None
    combined_utility: float = 0.0

    @property
    def oort_reward(self) -> float:
        """Return the reward fed into Oort's selector (statistical utility)."""

        return self.statistical_utility


def build_client_utility(
    client_id: str,
    loss_value: float,
    trained_size: int,
    gradient_l2_norm: float,
    duration: float,
    data_diversity_score: Optional[float] = None,
) -> ClientUtility:
    """Replicate the reward / gradient utilities computed in ``param_server.run``."""

    # Same formulation as in param_server.run: sqrt(loss) scaled by sampled size.
    loss_value = max(loss_value, 0.0)
    gradient_l2_norm = max(gradient_l2_norm, 0.0)

    statistical_utility = math.sqrt(loss_value) * trained_size
    gradient_utility = (
        math.sqrt(gradient_l2_norm) * trained_size / 100.0 if trained_size > 0 else 0.0
    )
    combined_utility = statistical_utility

    return ClientUtility(
        client_id=client_id,
        statistical_utility=statistical_utility,
        gradient_utility=gradient_utility,
        duration=duration,
        data_diversity_score=data_diversity_score,
        combined_utility=combined_utility,
    )


def estimate_simple_cost(util: ClientUtility) -> float:
    """Return a simple scalar cost estimate from a ClientUtility.

    For now, define cost as util.duration. This is a placeholder that we will
    refine later to include bytes, penalties, and optional diversity hooks.
    """

    return util.duration
