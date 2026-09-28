"""A disposable Redis cache for a pure calculation, never for approvals or memory."""

from __future__ import annotations

import os

def cached_annual_roi(annual_benefit: float, annual_cost: float) -> float:
    # Validate before reading a cached value: invalid inputs may never be bypassed.
    from workshop.tools import calculate_annual_roi

    value = calculate_annual_roi(annual_benefit, annual_cost)
    url = os.getenv("WORKSHOP_REDIS_URL", "").strip()
    if not url:
        return value
    import redis

    key = f"workshop:roi:v1:{annual_benefit:.2f}:{annual_cost:.2f}"
    try:
        client = redis.Redis.from_url(url, socket_connect_timeout=1, socket_timeout=1)
        cached = client.get(key)
        if cached is not None:
            return float(cached)
        client.setex(key, 3600, repr(value))
    except redis.RedisError:
        # Cache loss must not change a deterministic business result.
        pass
    return value
