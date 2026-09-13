# FunSizzy / FS2 Project Handover Document

**Last Updated**: September 12, 2026 (14:10 HST)  
**Workspace**: `/Users/austinanderson/GitHub/FunSizzy/FS2`  
**GCP Project**: `gen-lang-client-0887909657` (`pianowater@gmail.com`)  
**Upstream Git**: `https://github.com/aanderson3456/funSearch2.git` (branch `main`)

---

## 1. Cloud Run Overnight FunSearch (10,000 Iterations)

- **Job Name**: `funsearch-snakey-10k`
- **Active Execution**: `funsearch-snakey-10k-wnl78`
- **Region**: `us-central1`
- **Specs**: 2 vCPUs, 4.0 GiB RAM, `timeout = 24h` (86,400 seconds)
- **Status**: **ACTIVE & RUNNING** in Google Cloud.
  - Restarting your local machine **does NOT affect this job**. It runs completely serverless in Google Cloud.
  - LLM: `gemini-3.6-flash` sampling 2 programs per step across 10 MAP-Elites island demes.
  - Overfitting guardrails: Evaluates across radii 3 and 4 ($7 \times 7$ and $9 \times 9$) against 4 diverse Breakers (heuristic greedy, checkerboard parity, 5-threat blocker, and $3 \times 3$ higher topological paving).
- **Check Cloud Progress Anytime**:
  ```bash
  gcloud logging read 'resource.type="cloud_run_job" AND resource.labels.job_name="funsearch-snakey-10k"' --project gen-lang-client-0887909657 --limit 15 --format "value(textPayload)"
  ```
  Or visit: [Cloud Run Console](https://console.cloud.google.com/run/jobs/executions/details/us-central1/funsearch-snakey-10k-wnl78?project=532027507834)

---

## 2. Research Frontier: Finite Boards vs. Asymptotic Open Field

### The Mathematical Dilemma & MathGold Core
- **Erdős-Selfridge Degree Deficit**: Snaky's maximum cell degree on $\mathbb{Z}^2$ is $D_{\max} = 48$. For $k=6$, the theoretical Breaker safety threshold is $D_{\text{crit}} = 2^{k-1} = 32$. Because $48 > 32$, Breaker has no guaranteed strategy-stealing or pairing win.
- **Academic Paper**: Pushed to GitHub in `paper/snaky_erdos_selfridge.tex` and `paper/snaky_erdos_selfridge.md`.
- **Finite vs. Infinite Paradox**:
  - On $8 \times 8$ and $9 \times 9$: Breaker wins or achieves 100% denial because perimeter boundaries act as uncrossable artificial walls.
  - On $13 \times 13$: Maker wins 75%–100% of matches because open space allows quadratic 4-threat branching across multiple quadrants.
  - If proving Maker win requires scaling beyond $n = 20$, the combinatorial state space ($> 10^{60}$) makes exhaustive game-tree search intractable for humans. This is the exact complex topological domain that **MathGold** is designed to conquer.

---

## 3. Latest Local Strategy Discoveries (Sept 12)

1. **13x13 Breakthrough Breaker Champion**:
   - File: `strategies/breaker/rank_13x13_breakthrough_breaker.py`
   - Evolved defense on $13 \times 13$: boosted quadratic fork multiplier (`fork4_mult = 7.8e7`) and tightened smother kernel.
   - Denied both `Rank 0 Maker` and `15-Turn Fork Maker` at 5/6 cells after 60 turns!
   - Only `Grandmaster Maker` broke through (12 turns).
2. **Perfect 9x9 Breaker Champion**:
   - File: `strategies/breaker/rank_9x9_perfect_breaker.py`
   - Achieves 100% denial across all 10 Maker archetypes on $9 \times 9$.
3. **Multi-Scale Invariant Breaker**:
   - File: `strategies/breaker/rank_multiscale_invariant_breaker.py`
   - 100% denial on $11 \times 11$, 75% denial on $13 \times 13$.

---

## 4. Immediate Instructions For The Agent Upon Restart

When the user reopens the session after computer restart:

1. **Step 1: Check Cloud Run Status**:
   ```bash
   gcloud run jobs executions describe funsearch-snakey-10k-wnl78 --region us-central1 --project gen-lang-client-0887909657
   ```
   Confirm it is still executing and inspect recent iteration scores.

2. **Step 2: Run Mock Mode FunSearch Locally**:
   Run offline FunSearch mock mode for a spell as requested:
   ```bash
   /Users/austinanderson/GitHub/FunSizzy/FS2/.venv/bin/python -m funsearch.cli \
     --problem snakey \
     --model mock \
     --iterations 50 \
     --islands 5 \
     --in-process \
     --no-live
   ```

3. **Step 3: Continue Co-Evolution on 9x9 and 13x13**:
   Run adversarial co-evolution testing Maker counter-adaptations against `rank_13x13_breakthrough_breaker.py`:
   ```bash
   /Users/austinanderson/GitHub/FunSizzy/FS2/.venv/bin/python co_evolve_13x13_breakthrough.py
   ```
   Evaluate if Maker can evolve a dual-quadrant opening that reliably defeats the new 66.7% denial Breaker.

4. **Step 4: Keep CPU $\le 25\%$**:
   Ensure all local scripts enforce single-threaded OpenMP/BLAS:
   `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`.

---
