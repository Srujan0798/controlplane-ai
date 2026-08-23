#!/usr/bin/env python3
"""Sequential refund-demo latency bench (Lane-1 gate path).

Default: in-process FastAPI TestClient via create_app().
Optional: CONTROLPLANE_BENCH_URL=http://127.0.0.1:8787 for a live server.

Writes submission/latency_bench.json and prints p50/p95/p99 for:
  - latency_ms from each response JSON (gate-internal)
  - wall time per HTTP call (client-observed)
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
OUT = ROOT / "submission" / "latency_bench.json"
DEFAULT_N = 200
ENDPOINT = "/v1/controlplane/demo/refund?mode=enforce"


def _percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def _summarize(vals: list[float]) -> dict[str, float]:
    ordered = sorted(vals)
    return {
        "n": len(vals),
        "min": round(ordered[0], 3) if ordered else 0.0,
        "mean": round(statistics.fmean(vals), 3) if vals else 0.0,
        "p50": round(_percentile(ordered, 50), 3),
        "p95": round(_percentile(ordered, 95), 3),
        "p99": round(_percentile(ordered, 99), 3),
        "max": round(ordered[-1], 3) if ordered else 0.0,
    }


def _client(url: str | None):
    if url:
        import httpx

        base = url.rstrip("/")

        class Live:
            def post(self, path: str):
                return httpx.post(f"{base}{path}", timeout=30.0)

        return Live(), "live"

    from fastapi.testclient import TestClient

    from controlplane.server.app import create_app

    return TestClient(create_app()), "testclient"


def run(n: int, url: str | None) -> dict:
    client, mode = _client(url)
    gate_ms: list[float] = []
    wall_ms: list[float] = []

    # Warm one call so import / policy load does not dominate the first sample.
    warm = client.post(ENDPOINT)
    if warm.status_code != 200:
        raise SystemExit(f"warm-up failed: {warm.status_code} {warm.text}")

    for _ in range(n):
        t0 = time.perf_counter()
        resp = client.post(ENDPOINT)
        wall = (time.perf_counter() - t0) * 1000.0
        if resp.status_code != 200:
            raise SystemExit(f"bench call failed: {resp.status_code} {resp.text}")
        body = resp.json()
        if "latency_ms" not in body:
            raise SystemExit("response missing latency_ms")
        gate_ms.append(float(body["latency_ms"]))
        wall_ms.append(wall)

    gate_summary = _summarize(gate_ms)
    wall_summary = _summarize(wall_ms)
    payload = {
        "n": n,
        "endpoint": ENDPOINT,
        "client": mode,
        "url": url,
        "units": "milliseconds",
        "gate_latency_ms": gate_summary,
        "wall_latency_ms": wall_summary,
        "note": (
            "gate_latency_ms is ControlPlaneGate internal timing from response JSON. "
            "wall_latency_ms is client-observed HTTP round-trip. "
            "Targets remain ≤40ms p50 / ≤200ms p95 on R0/R1 — never quote 40ms as p95."
        ),
        "samples_gate_ms_head": [round(x, 3) for x in gate_ms[:5]],
        "samples_wall_ms_head": [round(x, 3) for x in wall_ms[:5]],
    }
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", type=int, default=DEFAULT_N, help="sequential calls (default 200)")
    parser.add_argument(
        "--url",
        default=os.environ.get("CONTROLPLANE_BENCH_URL"),
        help="live base URL; default uses in-process TestClient",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT,
        help=f"output JSON path (default {OUT})",
    )
    args = parser.parse_args(argv)

    result = run(args.n, args.url)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    g, w = result["gate_latency_ms"], result["wall_latency_ms"]
    print(f"client={result['client']} n={result['n']} → {args.out}")
    print(
        f"gate  latency_ms  p50={g['p50']}  p95={g['p95']}  p99={g['p99']}  "
        f"mean={g['mean']}  max={g['max']}"
    )
    print(
        f"wall  latency_ms  p50={w['p50']}  p95={w['p95']}  p99={w['p99']}  "
        f"mean={w['mean']}  max={w['max']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
