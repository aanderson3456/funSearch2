# FunSizzy / FS2 Project Handover Document

**Date**: September 10, 2026  
**Workspace**: `/Users/austinanderson/GitHub/FunSizzy/FS2`  
**Google Drive Mount**: `/Users/austinanderson/Library/CloudStorage/GoogleDrive-pianowater@gmail.com/My Drive/`  

---

## 1. Executive Summary & Current State

This project investigates the **Snakey Polyomino Achievement Game** (Maker vs. Breaker on a $13 \times 13$ board) across three converging methodologies:
1. **AlphaZero-Style Deep Reinforcement Learning** (NNv1, NNv2, NNv3, NNv4).
2. **FunSearch Evolutionary Program Discovery** (LLM-driven heuristic search with multi-island genetic algorithms).
3. **Formal Mathematical Verification** (Lean 4 formal certificates for infinite-board paving losers).

---

## 2. Google Drive & Colab Integration

- **Desktop Auto-Sync**: The Mac has Google Drive for Desktop active. Any file written to `/Users/austinanderson/Library/CloudStorage/GoogleDrive-pianowater@gmail.com/My Drive/` immediately syncs to Google Drive cloud in real time.
- **Colab Notebooks Folder**:
  `/Users/austinanderson/Library/CloudStorage/GoogleDrive-pianowater@gmail.com/My Drive/Colab Notebooks/`
- **Checkpoints Storage**:
  - NNv3: `.../My Drive/SnakyNet_v3_Checkpoints/` (contains `snaky_large_model_it0.pt` through `it73.pt`, and `loss_history.json`).
  - NNv4: `.../My Drive/SnakyNet_v4_Checkpoints/` (created for NNv4 training outputs).

---

## 3. NNv3 Status & Findings

- **Latest Run**: Iteration 73 completed on Colab (A100 GPU) with loss `2.987`.
- **Local Checkpoints Synced**:
  - `snaky_v3_model_it72.pt` and `snaky_v3_model_it73.pt` in `FS2/`.
  - `loss_history_v3.json` in `FS2/`.
- **Key Self-Play Observation**: Median game length reached **169.0 moves** (full $13 \times 13$ board saturation). Breaker's 6th-channel threat-blocking completely stonewalls naive Maker attacks, creating a "defensive collapse" where Maker never learns multi-threat branching forks in pure self-play.

---

## 4. Round Robin Tournament Results

A full 12-match round robin was run pitting all best versions against each other (both as Maker and Breaker). Recorded in `elo_results.json` with 12 interactive HTML replay viewers (`elo_match_1_replay.html` through `elo_match_12_replay.html`):

| Rank | Competitor | Elo Rating | Record | Maker W-L | Breaker W-L | Avg Turns | Dynamics |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 🥇 **1** | **FunSearch** | **1085.6** | **6 – 0 (100%)** | 3 – 0 | 3 – 0 | 28.0 | Undefeated. Wins in 6–8 moves as Maker via unblockable geometric forks. |
| 🥈 **2** | **NNv3 (`it72`)** | **1025.8** | **4 – 2 (66.7%)** | 2 – 1 | 2 – 1 | 42.2 | Swept NNv1 & NNv2 4–0. Defended as Breaker for 62 and 59 turns. Held FunSearch for 7 turns. |
| 🥉 **3** | **NNv2 (`it450`)** | **946.1** | **1 – 5 (16.7%)** | 1 – 2 | 0 – 3 | 31.5 | 0% win rate as Breaker. Won only when moving first against NNv1. |
| **4** | **NNv1 (`it850`)** | **942.5** | **1 – 5 (16.7%)** | 1 – 2 | 0 – 3 | 34.0 | 0% win rate as Breaker. Won only when moving first against NNv2. |

---

## 5. Mathematical & Lean 4 Frontier on $n$

### Polyomino Order ($n$-omino):
- **$n = 7$ (Heptominoes)**: Largest order formally certified in Lean 4 (`LeanProofs/FunSizzy/Losers.lean`). 107 out of 108 heptominoes are mechanically verified as Breaker wins on $\mathbb{Z}^2$.
- **$n = 6$ (Hexominoes & Snakey)**: 32 of 35 are certified Breaker wins. **Snakey is one of only 3 survivors** that resists all 6 periodic domino pavings (`print_survivors.py`).
- **Straightominoes ($I_n$)**: $I_4$ ($n=4$) is certified Maker win (finite strategy tree of 2,684 nodes). All $n \ge 5$ are formally proven Breaker wins via checkerboard paving in Lean 4.

### Board Size ($n \times n$):
- **$n = \infty$ ($\mathbb{Z}^2$)**: Certified in Lean 4 for 148 polyominoes across 16 shift domains of 4-periodic pavings (`Core.lean`).
- **$n \le 8$ ($8 \times 8$)**: Snakey is a mathematically proven Breaker win in published game theory (Harary 1982, Sieben 2008).
- **$n = 13$ ($13 \times 13$)**: Active computational arena (`arena_13x13.py`, `run_elo_tournament.py`). FunSearch Maker forces wins in 6–8 moves against neural network Breakers.

---

## 6. NNv4: Architecture, Training Pipeline, & Colab Setup

To overcome the defensive self-play deadlock and conquer FunSearch, **NNv4** was designed, implemented, locally tested, and deployed:

### Innovations:
1. **7-Channel Input Tensor**:
   - Channel 5: Single-threat heatmap (5/6 pieces placed).
   - **Channel 6: Dual-Threat / Fork Potential Heatmap**: Real-time geometric detector identifying cells that create $\ge 2$ simultaneous winning threats ($C_4 \ge 2$).
2. **Curriculum Self-Play (25% FunSearch Injection)**:
   - 25% of self-play games use Champion FunSearch as Maker, seeding the replay buffer with expert fork demonstrations.
3. **Asymmetric Opening Exploration**:
   - Moves 1–6 use higher Maker temperature ($\tau = 1.25$) and boosted Dirichlet noise (`frac = 0.35`) so Maker explores diverse fork branches.
4. **Vectorized Fast Engine**:
   - 0.16 ms per state encoding; ResNet batch forward pass in 15.4 ms on CPU.

### Files Created & Verified:
- `big_nn/resnet.py`: Updated `SnakyNet(in_channels=7)`.
- `train_colab_NNv4.py`: Full training loop with 7-channel encoder and curriculum self-play.
- `test_nnv4.py`: 5-part verification test suite (100% passing).
- `make_colab_training_NNv4_v1.py`: Generator script.
- `colab_training_NNv4_v1.ipynb`: Generated notebook, **auto-synced to Google Drive** at:
  `/Users/austinanderson/Library/CloudStorage/GoogleDrive-pianowater@gmail.com/My Drive/Colab Notebooks/colab_training_NNv4_v1.ipynb`
- **Bug Fix Applied**: Fixed `__file__` NameError so the notebook runs cleanly in Colab.

### Running NNv4 in Colab:
1. Open `Colab Notebooks/colab_training_NNv4_v1.ipynb` in Colab.
2. Select A100 GPU runtime.
3. Click **Runtime $\rightarrow$ Run all**. Checkpoints save to `/MyDrive/SnakyNet_v4_Checkpoints/`.
4. Expected timeline to beat FunSearch: **~15–20 hours (approx. 20–25 iterations)** in a single Colab Pro run.

---

## 7. Ongoing / Next Tasks for the New Chat

1. **Monitor NNv4 Training**:
   - Watch `/Users/austinanderson/Library/CloudStorage/GoogleDrive-pianowater@gmail.com/My Drive/SnakyNet_v4_Checkpoints/` as checkpoints land every ~35–40 minutes.
2. **Co-Evolution Run**:
   - Alternating Maker then Breaker co-evolution for 100 generations with move count logging and baseline normies included, capped at 25% CPU.
3. **Post-Training Benchmark**:
   - Once `snaky_v4_model_it20.pt` or higher lands, update `run_elo_tournament.py` and benchmark NNv4 against FunSearch.
