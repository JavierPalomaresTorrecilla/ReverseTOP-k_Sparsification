from dataclasses import dataclass
from typing import Optional


@dataclass
class TelemetryStats:
    """Per-client telemetry for the ReverseTOP-k_Sparsification controller."""

    round_index: int
    client_id: int
    duration: float  # total time cost for this client in this round
    local_compute_time: float  # placeholder mapping to duration for now
    upload_time: float  # placeholder for measured upload latency
    bytes_uploaded: int  # total bytes in the model delta this round
    speed_per_sample: float  # seconds per sample, parsed from learner speed
    num_samples: int  # number of samples processed in this round
    delay_inflation: float = 0.0
    delivery_rate: float = 0.0
    loss_pulse: int = 0

    """delay_inflation, delivery_rate, and loss_pulse are placeholders for
    endpoint-network telemetry that the ReverseTOP-k_Sparsification logic will
    populate when RTkS transport hooks are integrated."""
