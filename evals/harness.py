"""Backward-compatible entrypoint. `make eval` uses ``evals.run``.

``python -m evals.harness`` is the same honest report: action-level FNR/FPR
with Wilson CIs, per-route binding distribution (not precision), self-authored
corpus, production FNR unknown. No single accuracy number.
"""
from evals.run import (  # noqa: F401
    LAST_RUN,
    ROOT,
    build_report,
    main,
    run_case,
)

if __name__ == "__main__":
    raise SystemExit(main())
