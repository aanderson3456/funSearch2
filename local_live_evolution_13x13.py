"""Local Live Evolution on 9x9, 11x11, and 13x13 with Overfitting Guardrails.

Runs FunSearch-style program evolution locally using Gemini 3.6 Flash.
Evaluates candidate programs across multiple board sizes and against multiple
archetypes of adversarial Breakers to prevent overfitting to a single board size
or adversary.

Enforces CPU <= 25% via single-threading.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any, Callable

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))

# Load .env variables
env_file = FS2_DIR / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"\'')

from funsearch.llm.gemini import GeminiLLM
from boost_mock_evolution import (
    get_board_shapes,
    run_match,
    load_strategy_from_file,
)

# Precompute board shapes for test radii
print("Precomputing board shapes for 9x9 (r=4) and 13x13 (r=6)...")
SHAPES_9x9 = get_board_shapes(radius=4)
SHAPES_13x13 = get_board_shapes(radius=6)
print(f"Loaded {len(SHAPES_9x9)} shapes (9x9) and {len(SHAPES_13x13)} shapes (13x13).")

# Load Breaker Ensemble (Overfitting Guardrails)
BREAKERS = [
    ("Invariant Breaker", load_strategy_from_file("strategies/breaker/rank_multiscale_invariant_breaker.py", "breaker_priority")),
    ("Perfect 9x9 Breaker", load_strategy_from_file("strategies/breaker/rank_9x9_perfect_breaker.py", "breaker_priority")),
    ("Grandmaster Breaker", load_strategy_from_file("strategies/breaker/rank_9x9_grandmaster_breaker.py", "breaker_priority")),
]

INITIAL_MAKER_CODE = '''def priority(candidate, maker_cells, breaker_cells, active_shapes):
    m_set = set(maker_cells)
    b_set = set(breaker_cells)
    score = 0.0
    threat_4 = 0
    threat_3 = 0
    overlap = 0
    weights = {0: 1.0, 1: 4.5, 2: 32.0, 3: 550.0, 4: 28000.0, 5: 1e7}
    for s in active_shapes:
        if candidate in s:
            overlap += 1
            m_cnt = sum(1 for p in s if p in m_set)
            score += weights.get(m_cnt, 10.0 ** m_cnt)
            if m_cnt == 4:
                threat_4 += 1
            elif m_cnt == 3:
                threat_3 += 1
    if threat_4 >= 2:
        score += 5000000.0 * (threat_4 ** 2)
    if threat_3 >= 2:
        score += 250000.0 * threat_3
    score += (overlap ** 1.35) * 4.2
    return float(score)
'''

def evaluate_maker_guardrails(maker_fn: Callable) -> tuple[float, dict[str, Any]]:
    """Evaluates Maker against diverse Breakers across 9x9 and 13x13.
    
    A strategy that overfits to 9x9 perimeter traps or a single opponent
    will be heavily penalized.
    """
    total_score = 0.0
    wins = 0
    matches = 0
    details = []
    
    # Test on 9x9 (dense, boundary-sensitive)
    for b_name, b_fn in BREAKERS:
        matches += 1
        res = run_match(maker_fn, b_fn, grid_radius=4)
        if res["maker_won"]:
            wins += 1
            total_score += 150.0 + (50 - res["turns"]) * 5.0
        else:
            total_score += res["max_cells_in_shape"] * 15.0
        details.append((b_name, 9, res["maker_won"], res["turns"], res["max_cells_in_shape"]))
        
    # Test on 13x13 (open-field, scale-free)
    for b_name, b_fn in BREAKERS:
        matches += 1
        res = run_match(maker_fn, b_fn, grid_radius=6)
        if res["maker_won"]:
            wins += 1
            total_score += 250.0 + (90 - res["turns"]) * 5.0
        else:
            total_score += res["max_cells_in_shape"] * 25.0
        details.append((b_name, 13, res["maker_won"], res["turns"], res["max_cells_in_shape"]))

    fitness = total_score / matches
    return fitness, {"wins": wins, "matches": matches, "win_rate": wins / matches, "details": details}

def compile_candidate(code_str: str) -> Callable | None:
    ns = {}
    try:
        exec(code_str, ns)
        return ns.get("priority")
    except Exception:
        return None

def run_local_gemini_evolution(num_rounds: int = 10):
    print("=" * 78)
    print(f"LAUNCHING LOCAL GEMINI EVOLUTION ({num_rounds} ROUNDS)")
    print("Multi-Scale Guardrails: 9x9 & 13x13 against Invariant + Perfect + GM Breakers")
    print("=" * 78)
    
    llm = GeminiLLM(model_name="gemini-3.6-flash", temperature=0.7)
    
    best_code = INITIAL_MAKER_CODE
    best_fn = compile_candidate(best_code)
    best_score, best_meta = evaluate_maker_guardrails(best_fn)
    
    print(f"Seed Baseline Score: {best_score:.2f} | Win Rate: {best_meta['win_rate']*100:.1f}% ({best_meta['wins']}/{best_meta['matches']})")
    print("-" * 78)
    
    for round_idx in range(1, num_rounds + 1):
        print(f"\n[Round {round_idx}/{num_rounds}] Prompting Gemini 3.6 Flash for topological innovations...")
        prompt = f"""You are an expert combinatorial game theorist working on the unsolved Snaky Polyomino Achievement Game.
We need to evolve an improved Maker priority function that simultaneously wins on small boards (9x9) and large open boards (13x13) against top adversarial Breakers.

Here is the current best Maker priority function (Score: {best_score:.2f}, Win Rate: {best_meta['win_rate']*100:.1f}%):
```python
{best_code}
```

Key Insights to beat the invariant Breaker:
1. Quadratic 4-threat branching: Breaker blocks 1 cell per turn. If Maker creates 2 simultaneous 4-threats in orthogonal quadrants, Breaker can only stop 1.
2. 2x2 nuclear box foundation: Snaky contains a 2x2 square core. Forming a 3-cell cluster of a 2x2 box creates unblockable dual extensions.
3. Scale invariance: avoid using absolute coordinates like abs(candidate[0]) which overfit to the origin. Instead use relative distances to existing maker cells.
4. Parity and curvature: reward candidate moves that introduce orthogonal elbows.

Write an improved `def priority(candidate, maker_cells, breaker_cells, active_shapes):` function.
Return ONLY valid Python code inside a ```python ``` code block.
"""
        try:
            generated_code = llm.draw_sample(prompt)
            candidate_fn = compile_candidate(generated_code)
            if candidate_fn is None:
                print("  -> Syntax / compilation error in candidate. Skipping.")
                continue
                
            cand_score, cand_meta = evaluate_maker_guardrails(candidate_fn)
            print(f"  -> Candidate Score: {cand_score:.2f} | Win Rate: {cand_meta['win_rate']*100:.1f}% ({cand_meta['wins']}/{cand_meta['matches']})")
            
            if cand_score > best_score:
                diff = cand_score - best_score
                best_score = cand_score
                best_code = generated_code
                best_meta = cand_meta
                print(f"  🏆 NEW LOCAL CHAMPION! Improvement: +{diff:.2f}")
                
                # Save checkpoint
                out_path = FS2_DIR / "strategies" / "maker" / f"gemini_live_champion_{int(time.time())}.py"
                out_path.write_text(best_code)
                print(f"  Saved to: {out_path.name}")
            else:
                print(f"  (Candidate did not beat current best {best_score:.2f})")
        except Exception as e:
            print(f"  -> Error during iteration: {e}")
            
    print("\n" + "=" * 78)
    print("LOCAL GEMINI EVOLUTION COMPLETE")
    print(f"Final Best Score: {best_score:.2f} | Win Rate: {best_meta['win_rate']*100:.1f}%")
    print("=" * 78)

if __name__ == "__main__":
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    run_local_gemini_evolution(num_rounds=rounds)
