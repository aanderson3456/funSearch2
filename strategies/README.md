# Snakey Top Discovered Strategies

This directory preserves the top 8 evolved Python heuristics for both **Maker** and **Breaker** playing the Snakey (Step Snaky Hexomino) Achievement Game in `funSearch2`.

Full massive evolutionary experiment runs and raw traces remain ignored in `.gitignore` (`outputs/`).

---

## 1. Snakey Maker Strategies (`strategies/maker/`)

Maker seeks to construct any D8 isometric copy of the 6-cell Snakey Hexomino:
`[(0,0), (1,0), (2,0), (3,0), (3,1), (4,1)]`

| Rank | File | Score | Strategy Profile |
| :--- | :--- | :--- | :--- |
| 1 | `rank_1_score_280.00.py` | 280.00 | Multi-level exponential weight map, active shape density scaling (`**1.3`), Manhattan distance penalty |
| 2 | `rank_2_score_270.00.py` | 270.00 | Aggressive fork acceleration with calibrated threat-3 branching |
| 3 | `rank_3_score_270.00.py` | 270.00 | Heavy center-mass development with high density multiplier |
| 4 | `rank_4_score_270.00.py` | 270.00 | Mid-tier threat clustering with compact territorial control |
| 5 | `rank_5_score_270.00.py` | 270.00 | High-weight step-head completion bias |
| 6 | `rank_6_score_270.00.py` | 270.00 | Multi-axis expansion with density clustering |
| 7 | `rank_7_score_270.00.py` | 270.00 | Rapid 4-cell backbone prioritization |
| 8 | `rank_8_score_270.00.py` | 270.00 | Balanced backbone and head advancement |

---

## 2. Snakey Breaker Strategies (`strategies/breaker/`)

Breaker seeks to block Maker from completing any Snakey Hexomino within 25 turns. Scores $>1000$ indicate Breaker completely neutralized Maker.

| Rank | File | Score | Strategy Profile |
| :--- | :--- | :--- | :--- |
| 1 | `rank_1_score_1010.00.py` | 1010.00 | Instant 1-threat & 2-threat neutralization with exponential overlap destruction |
| 2 | `rank_2_score_1010.00.py` | 1010.00 | Superlinear shape intersection defense (`overlap ** 1.5`) |
| 3 | `rank_3_score_1010.00.py` | 1010.00 | High-order fork extinction with threat-3 dampening |
| 4 | `rank_4_score_1010.00.py` | 1010.00 | Tight dual-threat interceptor with amplified overlap penalty |
| 5 | `rank_5_score_1010.00.py` | 1010.00 | Balanced multi-threat blocking with high 4-cell defense |
| 6 | `rank_6_score_1010.00.py` | 1010.00 | Early territorial parity denial |
| 7 | `rank_7_score_1010.00.py` | 1010.00 | Backbone termination prioritizing intersection cells |
| 8 | `rank_8_score_1010.00.py` | 1010.00 | Perimeter and center junction defense |
