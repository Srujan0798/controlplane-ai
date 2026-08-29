"""Wilson score confidence interval for a binomial proportion."""
from __future__ import annotations

import math


def wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float, float]:
    """Return (point, low, high). If n==0 return (0.0, 0.0, 0.0)."""
    if n <= 0:
        return 0.0, 0.0, 0.0
    p = successes / n
    z2 = z * z
    denom = 1.0 + z2 / n
    centre = p + z2 / (2 * n)
    margin = z * math.sqrt((p * (1 - p) + z2 / (4 * n)) / n)
    low = max(0.0, (centre - margin) / denom)
    high = min(1.0, (centre + margin) / denom)
    return p, low, high
