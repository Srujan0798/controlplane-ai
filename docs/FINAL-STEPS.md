# Final steps to complete (ControlPlane)

## Already done
- Core gate + console + policies + tests green
- Proposal FINAL + PDF, pitch R2S5 + PPTX
- Waves 6–8 shipped in code
- Repo cleaned: agent shards deleted; scaffolding removed
- Unique research → `PHASE2-FROM-RESEARCH.md` only

## You do now (stand)
1. `bash orchestrator/scripts/preflight-lite.sh`
2. Start console (`make run` or Docker) — refund Edit+Escalate, flip Edit→Pass
3. Walk `JUDGE_RUNBOOK.md` + top of `HOSTILE_QA_DRILL.md`
4. Tag when happy:
   ```bash
   git tag -a v0.2.0-round2 -m "Round 2 prize-day known-good"
   ```
5. Submit: Proposal PDF + Pitch PPTX + live/demo per organizer rules

## Do not
- Re-import Adaptoid Lite copies
- Re-create stage-shards
- Rewrite the frozen matrix
- Claim Lane-2 / FNR % you do not have
