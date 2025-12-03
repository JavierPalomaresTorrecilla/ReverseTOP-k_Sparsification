from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from helper.telemetry import TelemetryStats


@dataclass
class _ClientRTkSState:
    """Internal per-client RTkS state.

    For now this only tracks the current sparsity level and when it last changed.
    Additional smoothed telemetry statistics can be added later.
    """

    level_index: int
    last_change_round: int


class RTkSController:
    """Reverse Top-k sparsification controller (skeleton).

    This class will eventually map per-client telemetry into a sparsity level
    chosen from a geometric ladder. At this stage, it implements a stable
    no-op policy that always picks the densest level.
    """

    def __init__(self, p_levels: List[float]) -> None:
        """Initialize the controller with a sparsity ladder.

        Args:
            p_levels: List of sparsity fractions in (0, 1], ordered from
                densest (typically 1.0) to sparsest (e.g., 0.05).
        """
        if not p_levels:
            raise ValueError("p_levels must be a non-empty list of sparsity levels")
        # We expect p_levels[0] to correspond to the densest level.
        self._p_levels: List[float] = list(p_levels)
        self._client_state: Dict[int, _ClientRTkSState] = {}

    @property
    def levels(self) -> List[float]:
        """Return the configured sparsity ladder (densest to sparsest)."""
        return self._p_levels

    def _get_or_create_state(self, client_id: int, round_index: int) -> _ClientRTkSState:
        """Return the per-client state, creating a default one if needed."""
        state = self._client_state.get(client_id)
        if state is None:
            # Default to the densest level at the first observed round.
            state = _ClientRTkSState(level_index=0, last_change_round=round_index)
            self._client_state[client_id] = state
        return state

    def choose_level(self, client_id: int, telemetry: TelemetryStats) -> int:
        """Choose a sparsity level index for a client.

        For now, this implements a no-op policy that always returns the current
        level index stored for the client. The default is 0 (densest).

        Args:
            client_id: Integer client identifier.
            telemetry: TelemetryStats for this client and round.

        Returns:
            Index into `self.levels` (0-based).
        """
        state = self._get_or_create_state(client_id, telemetry.round_index)
        # Future versions will update `state.level_index` based on telemetry.
        return state.level_index

    def apply_envelope(
        self,
        client_id: int,
        base_level_index: int,
        envelope_bytes: int,
        estimated_bytes_per_level: List[int],
    ) -> int:
        """Adjust the chosen level to respect a byte envelope (placeholder).

        This method will eventually enforce per-round byte or time envelopes by
        potentially moving the client to a sparser level. For now, it simply
        returns `base_level_index` without modification.

        Args:
            client_id: Integer client identifier.
            base_level_index: Index originally chosen by `choose_level`.
            envelope_bytes: Maximum allowed bytes for this client's update in
                the current round.
            estimated_bytes_per_level: Estimated bytes per level, same length
                as `self.levels`.

        Returns:
            A possibly adjusted level index. Currently returns `base_level_index`.
        """
        # Placeholder: we do not yet enforce the envelope here.
        _ = client_id, envelope_bytes, estimated_bytes_per_level
        return base_level_index
