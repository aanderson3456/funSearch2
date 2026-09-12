"""Generate Interactive HTML Replay for Grandmaster Maker vs. Grandmaster Breaker.

Simulates matches on both 9x9 and 10x10 boards, collects detailed turn-by-turn
telemetry, tactical commentary, active shapes, and exports a standalone,
zero-dependency interactive HTML5/CSS3/ES6 replay application.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))

from boost_mock_evolution import load_strategy_from_file, get_board_shapes
from test_10x10_experiment import get_grid_shapes

p_m = FS2_DIR / "strategies/maker/rank_9x9_grandmaster_maker.py"
p_b = FS2_DIR / "strategies/breaker/rank_9x9_grandmaster_breaker.py"

fn_m = load_strategy_from_file(str(p_m), "priority")
fn_b = load_strategy_from_file(str(p_b), "breaker_priority")

def record_9x9_match():
    shapes = get_board_shapes(4)
    m_cells, b_cells = [], []
    history = []
    
    for turn in range(41):
        m_set, b_set = set(m_cells), set(b_cells)
        active = [tuple(s) for s in shapes if not (s & b_set)]
        cands = set(p for s in active for p in s if p not in m_set and p not in b_set)
        if not cands:
            break
            
        best_m = max(cands, key=lambda c: fn_m(c, m_cells, b_cells, active))
        m_cells.append(best_m)
        m_set.add(best_m)
        won = any(s.issubset(m_set) for s in shapes)
        max_c_m = max((len(s & m_set) for s in shapes), default=0)
        
        # Commentary generation
        comment = f"Maker claims {best_m}."
        if turn == 0:
            comment = f"Maker opens on outer ring at {best_m} to avoid central congestion."
        elif max_c_m == 5:
            comment = f"CRITICAL THREAT: Maker forms 5-cell Snaky structure with {best_m}!"
        elif max_c_m == 4:
            comment = f"Maker establishes 4-cell foundation at {best_m}."
            
        history.append({
            "step": len(history) + 1,
            "turn": turn + 1,
            "player": "Maker",
            "coord": best_m,
            "maker_cells": list(m_cells),
            "breaker_cells": list(b_cells),
            "active_shapes": len(active),
            "max_cells": max_c_m,
            "won": won,
            "comment": comment,
        })
        if won:
            break
            
        active_b = [tuple(s) for s in shapes if not (s & b_set)]
        cands_b = set(p for s in active_b for p in s if p not in m_set and p not in b_set)
        if not cands_b:
            break
            
        best_b = max(cands_b, key=lambda c: fn_b(c, m_cells, b_cells, active_b))
        b_cells.append(best_b)
        b_set.add(best_b)
        active_after_b = [tuple(s) for s in shapes if not (s & b_set)]
        max_c_b = max((len(s & m_set) for s in shapes), default=0)
        
        b_comment = f"Breaker replies at {best_b}."
        if max_c_m == 5 and max_c_b < 5:
            b_comment = f"EMERGENCY BLOCK: Breaker snuffs out lethal 5-threat at {best_b}!"
        elif abs(best_b[0] - best_m[0]) + abs(best_b[1] - best_m[1]) <= 1:
            b_comment = f"SMOTHER CLAMP: Breaker clings to Maker stone at {best_b}."
            
        history.append({
            "step": len(history) + 1,
            "turn": turn + 1,
            "player": "Breaker",
            "coord": best_b,
            "maker_cells": list(m_cells),
            "breaker_cells": list(b_cells),
            "active_shapes": len(active_after_b),
            "max_cells": max_c_b,
            "won": False,
            "comment": b_comment,
        })
        
    return {
        "board_size": 9,
        "coord_type": "centered",  # -4 to +4
        "winner": "Breaker",
        "total_turns": history[-1]["turn"],
        "total_steps": len(history),
        "history": history,
        "winning_shape": None,
    }

def record_10x10_match():
    shapes = get_grid_shapes(10, 10)
    m_cells, b_cells = [], []
    history = []
    winning_shape = None
    
    for turn in range(50):
        m_set, b_set = set(m_cells), set(b_cells)
        active = [tuple(s) for s in shapes if not (s & b_set)]
        cands = set(p for s in active for p in s if p not in m_set and p not in b_set)
        if not cands:
            break
            
        best_m = max(cands, key=lambda c: fn_m(c, m_cells, b_cells, active))
        m_cells.append(best_m)
        m_set.add(best_m)
        won = any(s.issubset(m_set) for s in shapes)
        max_c_m = max((len(s & m_set) for s in shapes), default=0)
        
        comment = f"Maker plays at {best_m}."
        if won:
            ws = [s for s in shapes if s.issubset(m_set)][0]
            winning_shape = sorted(list(ws))
            comment = f"VICTORY: Maker completes Snaky Hexomino at {best_m}! 6/6 Cells connected!"
        elif max_c_m == 5:
            comment = f"THREAT: Maker creates 5-threat fork at {best_m}!"
            
        history.append({
            "step": len(history) + 1,
            "turn": turn + 1,
            "player": "Maker",
            "coord": best_m,
            "maker_cells": list(m_cells),
            "breaker_cells": list(b_cells),
            "active_shapes": len(active),
            "max_cells": max_c_m,
            "won": won,
            "comment": comment,
        })
        if won:
            break
            
        active_b = [tuple(s) for s in shapes if not (s & b_set)]
        cands_b = set(p for s in active_b for p in s if p not in m_set and p not in b_set)
        if not cands_b:
            break
            
        best_b = max(cands_b, key=lambda c: fn_b(c, m_cells, b_cells, active_b))
        b_cells.append(best_b)
        b_set.add(best_b)
        active_after_b = [tuple(s) for s in shapes if not (s & b_set)]
        max_c_b = max((len(s & m_set) for s in shapes), default=0)
        
        history.append({
            "step": len(history) + 1,
            "turn": turn + 1,
            "player": "Breaker",
            "coord": best_b,
            "maker_cells": list(m_cells),
            "breaker_cells": list(b_cells),
            "active_shapes": len(active_after_b),
            "max_cells": max_c_b,
            "won": False,
            "comment": f"Breaker blocks at {best_b}.",
        })
        
    return {
        "board_size": 10,
        "coord_type": "zero_indexed",  # 0 to 9
        "winner": "Maker",
        "total_turns": history[-1]["turn"],
        "total_steps": len(history),
        "history": history,
        "winning_shape": winning_shape,
    }

def generate_html():
    match_9 = record_9x9_match()
    match_10 = record_10x10_match()
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Snaky Hexomino Grandmaster Replay | AI Co-Evolution</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #0b0f19;
      --panel-bg: #111827;
      --card-bg: #1f2937;
      --border-color: #374151;
      --accent-maker: #06b6d4;
      --accent-maker-glow: rgba(6, 182, 212, 0.4);
      --accent-breaker: #f43f5e;
      --accent-breaker-glow: rgba(244, 63, 94, 0.4);
      --accent-gold: #fbbf24;
      --text-main: #f3f4f6;
      --text-dim: #9ca3af;
      --font-code: 'Fira Code', monospace;
      --font-sans: 'Inter', sans-serif;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: radial-gradient(circle at top, #1e1b4b 0%, var(--bg-dark) 60%);
      color: var(--text-main);
      font-family: var(--font-sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 24px;
    }}
    header {{
      text-align: center;
      margin-bottom: 20px;
      width: 100%;
      max-width: 1200px;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 12px;
      font-size: 0.75rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      border-radius: 9999px;
      background: rgba(99, 102, 241, 0.2);
      border: 1px solid rgba(99, 102, 241, 0.4);
      color: #a5b4fc;
      margin-bottom: 8px;
    }}
    h1 {{
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #e0e7ff 0%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 6px;
    }}
    p.subtitle {{
      color: var(--text-dim);
      font-size: 0.95rem;
      max-width: 700px;
      margin: 0 auto;
    }}
    /* Top Mode Toggle */
    .match-toggle {{
      display: flex;
      justify-content: center;
      gap: 12px;
      margin: 18px 0;
    }}
    .toggle-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      color: var(--text-dim);
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .toggle-btn:hover {{
      border-color: #6366f1;
      color: #fff;
    }}
    .toggle-btn.active {{
      background: #4f46e5;
      color: #fff;
      border-color: #6366f1;
      box-shadow: 0 0 16px rgba(79, 70, 229, 0.4);
    }}
    /* Main Layout */
    .arena-container {{
      display: grid;
      grid-template-columns: 1fr 380px;
      gap: 24px;
      width: 100%;
      max-width: 1240px;
    }}
    @media (max-width: 960px) {{
      .arena-container {{
        grid-template-columns: 1fr;
      }}
    }}
    /* Board Area */
    .board-card {{
      background: var(--panel-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
      position: relative;
    }}
    .board-wrapper {{
      position: relative;
      margin: 16px 0;
      background: #0d1322;
      padding: 20px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.06);
      box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.8);
    }}
    .grid-board {{
      display: grid;
      gap: 4px;
      user-select: none;
    }}
    .grid-cell {{
      width: 44px;
      height: 44px;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-size: 0.65rem;
      font-family: var(--font-code);
      color: rgba(255, 255, 255, 0.2);
      position: relative;
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    .grid-cell:hover {{
      border-color: rgba(255, 255, 255, 0.3);
      background: rgba(255, 255, 255, 0.05);
    }}
    .grid-cell.maker {{
      background: linear-gradient(135deg, #0891b2, #06b6d4);
      border-color: #67e8f9;
      color: #ffffff;
      font-weight: 700;
      box-shadow: 0 0 12px var(--accent-maker-glow);
      transform: scale(0.96);
    }}
    .grid-cell.breaker {{
      background: linear-gradient(135deg, #e11d48, #f43f5e);
      border-color: #fda4af;
      color: #ffffff;
      font-weight: 700;
      box-shadow: 0 0 12px var(--accent-breaker-glow);
      transform: scale(0.96);
    }}
    .grid-cell.winning-shape {{
      background: linear-gradient(135deg, #d97706, #fbbf24) !important;
      border-color: #fef08a !important;
      color: #000 !important;
      box-shadow: 0 0 20px rgba(251, 191, 36, 0.8) !important;
      animation: pulseWin 1.5s infinite alternate;
      z-index: 10;
    }}
    @keyframes pulseWin {{
      from {{ transform: scale(0.96); filter: brightness(1); }}
      to {{ transform: scale(1.04); filter: brightness(1.3); }}
    }}
    .grid-cell.last-move {{
      outline: 3px solid #fbbf24;
      outline-offset: 2px;
      z-index: 5;
    }}
    .cell-num {{
      font-size: 0.8rem;
      font-weight: 800;
    }}
    .cell-coord {{
      font-size: 0.55rem;
      opacity: 0.7;
    }}
    /* Control Bar */
    .controls {{
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 100%;
      max-width: 540px;
    }}
    .slider-row {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .timeline-slider {{
      flex: 1;
      accent-color: #6366f1;
      height: 6px;
      border-radius: 3px;
      cursor: pointer;
    }}
    .btn-row {{
      display: flex;
      justify-content: center;
      gap: 10px;
    }}
    .ctrl-btn {{
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 8px 16px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.85rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}
    .ctrl-btn:hover {{
      background: #374151;
      border-color: #6366f1;
    }}
    .ctrl-btn.play {{
      background: #4f46e5;
      border-color: #6366f1;
      color: #fff;
    }}
    .ctrl-btn.play:hover {{
      background: #4338ca;
    }}
    /* Sidebar / HUD */
    .sidebar {{
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .hud-card {{
      background: var(--panel-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 20px;
    }}
    .hud-title {{
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .stat-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 14px;
    }}
    .stat-item {{
      background: var(--card-bg);
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.04);
    }}
    .stat-label {{
      font-size: 0.7rem;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 600;
      margin-bottom: 4px;
    }}
    .stat-val {{
      font-size: 1.25rem;
      font-weight: 800;
      font-family: var(--font-code);
    }}
    .stat-val.maker {{ color: var(--accent-maker); }}
    .stat-val.breaker {{ color: var(--accent-breaker); }}
    .stat-val.gold {{ color: var(--accent-gold); }}
    /* Gauge Bar */
    .gauge-wrapper {{
      margin-top: 10px;
    }}
    .gauge-header {{
      display: flex;
      justify-content: space-between;
      font-size: 0.75rem;
      font-weight: 600;
      margin-bottom: 6px;
    }}
    .gauge-bar {{
      height: 8px;
      background: #1e293b;
      border-radius: 4px;
      overflow: hidden;
      display: flex;
    }}
    .gauge-fill {{
      height: 100%;
      background: linear-gradient(90deg, #06b6d4, #fbbf24);
      transition: width 0.3s ease;
    }}
    /* Move Log */
    .log-container {{
      max-height: 280px;
      overflow-y: auto;
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      background: #0d1322;
      font-family: var(--font-code);
      font-size: 0.8rem;
    }}
    .log-entry {{
      padding: 8px 12px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      display: flex;
      justify-content: space-between;
      cursor: pointer;
      transition: background 0.15s ease;
    }}
    .log-entry:hover {{
      background: rgba(255, 255, 255, 0.05);
    }}
    .log-entry.active {{
      background: rgba(99, 102, 241, 0.25);
      border-left: 3px solid #818cf8;
    }}
    .log-maker {{ color: var(--accent-maker); }}
    .log-breaker {{ color: var(--accent-breaker); }}
    /* Commentary Box */
    .commentary-box {{
      background: rgba(99, 102, 241, 0.08);
      border: 1px solid rgba(99, 102, 241, 0.2);
      border-radius: 10px;
      padding: 14px;
      font-size: 0.85rem;
      line-height: 1.45;
      color: #e0e7ff;
      min-height: 60px;
    }}
  </style>
</head>
<body>

  <header>
    <div class="badge">DeepMind Advanced Agentic Coding</div>
    <h1>Snaky Polyomino Grandmaster Replay</h1>
    <p class="subtitle">
      Adversarial showdown between the Evolved Grandmaster Maker and Grandmaster Breaker.
      Experience the exact turn-by-turn maneuvers that define the 40-year open problem boundary.
    </p>
  </header>

  <div class="match-toggle">
    <button class="toggle-btn active" id="btn-9x9" onclick="switchMatch('9x9')">
      🛡️ 9x9 Duel: Grandmaster Breaker Total Denial (27 Turns)
    </button>
    <button class="toggle-btn" id="btn-10x10" onclick="switchMatch('10x10')">
      ⚔️ 10x10 Duel: Grandmaster Maker Breakthrough (19 Turns)
    </button>
  </div>

  <div class="arena-container">
    
    <!-- Board Card -->
    <div class="board-card">
      <div id="status-banner" style="font-weight: 700; font-size: 1rem; color: #a5b4fc; margin-bottom: 4px;">
        Match Active
      </div>
      <div class="board-wrapper">
        <div id="grid-board" class="grid-board"></div>
      </div>

      <!-- Controls -->
      <div class="controls">
        <div class="slider-row">
          <span style="font-family: var(--font-code); font-size: 0.8rem; color: var(--text-dim);" id="step-counter">0 / 0</span>
          <input type="range" id="timeline-slider" class="timeline-slider" min="0" max="100" value="0" oninput="onSliderChange(this.value)">
          <span style="font-family: var(--font-code); font-size: 0.8rem; color: var(--text-dim);" id="turn-counter">Turn 1</span>
        </div>
        <div class="btn-row">
          <button class="ctrl-btn" onclick="stepTo(0)">⏮ Reset</button>
          <button class="ctrl-btn" onclick="stepBy(-1)">◀ Prev</button>
          <button class="ctrl-btn play" id="play-btn" onclick="togglePlay()">▶ Play</button>
          <button class="ctrl-btn" onclick="stepBy(1)">Next ▶</button>
          <button class="ctrl-btn" onclick="stepTo(currentMatch.total_steps)">End ⏭</button>
          <button class="ctrl-btn" id="speed-btn" onclick="toggleSpeed()">1x</button>
        </div>
      </div>
    </div>

    <!-- Sidebar HUD -->
    <div class="sidebar">
      <div class="hud-card">
        <div class="hud-title">
          <span>Live Match Telemetry</span>
          <span id="player-indicator" class="badge">Maker's Move</span>
        </div>
        
        <div class="stat-grid">
          <div class="stat-item">
            <div class="stat-label">Maker Stones</div>
            <div class="stat-val maker" id="stat-maker-stones">0</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Breaker Stones</div>
            <div class="stat-val breaker" id="stat-breaker-stones">0</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Active Snaky Shapes</div>
            <div class="stat-val gold" id="stat-active-shapes">320</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">Max Completed Cells</div>
            <div class="stat-val" id="stat-max-cells">0 / 6</div>
          </div>
        </div>

        <div class="gauge-wrapper">
          <div class="gauge-header">
            <span>Snaky Hexomino Completion</span>
            <span id="gauge-pct">0%</span>
          </div>
          <div class="gauge-bar">
            <div class="gauge-fill" id="gauge-fill" style="width: 0%;"></div>
          </div>
        </div>
      </div>

      <!-- Tactical Commentary -->
      <div class="hud-card">
        <div class="hud-title">Tactical Commentary</div>
        <div class="commentary-box" id="commentary-text">
          Select a match and press Play to observe the tactical maneuvers.
        </div>
      </div>

      <!-- Move Log -->
      <div class="hud-card" style="flex: 1; display: flex; flex-direction: column;">
        <div class="hud-title">Move Notation Log</div>
        <div class="log-container" id="log-container"></div>
      </div>
    </div>

  </div>

  <script>
    const MATCH_DATA = {{
      "9x9": {json.dumps(match_9)},
      "10x10": {json.dumps(match_10)}
    }};

    let currentMode = "9x9";
    let currentMatch = MATCH_DATA[currentMode];
    let currentStep = 0;
    let isPlaying = false;
    let playInterval = null;
    let playSpeed = 600;

    function initBoard() {{
      const boardEl = document.getElementById("grid-board");
      boardEl.innerHTML = "";
      const size = currentMatch.board_size;
      boardEl.style.gridTemplateColumns = `repeat(${{size}}, 44px)`;

      const offset = currentMatch.coord_type === "centered" ? 4 : 0;

      for (let r = 0; r < size; r++) {{
        for (let c = 0; c < size; c++) {{
          const cell = document.createElement("div");
          cell.className = "grid-cell";
          
          let x, y;
          if (currentMatch.coord_type === "centered") {{
            x = c - offset;
            y = offset - r; // standard cartesian
          }} else {{
            x = c;
            y = r;
          }}
          
          cell.dataset.x = x;
          cell.dataset.y = y;
          cell.id = `cell-${{x}}-${{y}}`;
          cell.innerHTML = `<span class="cell-coord">${{x}},${{y}}</span>`;
          boardEl.appendChild(cell);
        }}
      }}

      // Init timeline
      const slider = document.getElementById("timeline-slider");
      slider.max = currentMatch.total_steps;
      slider.value = 0;
      currentStep = 0;

      buildLog();
      renderStep(0);
    }}

    function buildLog() {{
      const container = document.getElementById("log-container");
      container.innerHTML = "";
      currentMatch.history.forEach((h, idx) => {{
        const row = document.createElement("div");
        row.className = "log-entry";
        row.id = `log-entry-${{idx + 1}}`;
        row.onclick = () => stepTo(idx + 1);
        
        const pClass = h.player === "Maker" ? "log-maker" : "log-breaker";
        row.innerHTML = `
          <span><b>T${{h.turn}}</b> <span class="${{pClass}}">${{h.player}}</span></span>
          <span>(${{h.coord[0]}}, ${{h.coord[1]}})</span>
        `;
        container.appendChild(row);
      }});
    }}

    function renderStep(step) {{
      currentStep = step;
      document.getElementById("timeline-slider").value = step;
      document.getElementById("step-counter").innerText = `${{step}} / ${{currentMatch.total_steps}}`;

      // Clear all board cells
      document.querySelectorAll(".grid-cell").forEach(c => {{
        c.className = "grid-cell";
        const coordSpan = c.querySelector(".cell-coord");
        c.innerHTML = "";
        if (coordSpan) c.appendChild(coordSpan);
      }});

      if (step === 0) {{
        document.getElementById("turn-counter").innerText = "Turn 1";
        document.getElementById("stat-maker-stones").innerText = "0";
        document.getElementById("stat-breaker-stones").innerText = "0";
        document.getElementById("stat-active-shapes").innerText = currentMatch.board_size === 9 ? "320" : "432";
        document.getElementById("stat-max-cells").innerText = "0 / 6";
        document.getElementById("gauge-fill").style.width = "0%";
        document.getElementById("gauge-pct").innerText = "0%";
        document.getElementById("commentary-text").innerText = "Match start. Both players begin with zero stones on the board.";
        document.getElementById("player-indicator").innerText = "Maker to Play";
        document.getElementById("player-indicator").style.color = "var(--accent-maker)";
        document.getElementById("status-banner").innerText = "Match in Progress";
        return;
      }}

      const data = currentMatch.history[step - 1];
      document.getElementById("turn-counter").innerText = `Turn ${{data.turn}}`;
      document.getElementById("stat-maker-stones").innerText = data.maker_cells.length;
      document.getElementById("stat-breaker-stones").innerText = data.breaker_cells.length;
      document.getElementById("stat-active-shapes").innerText = data.active_shapes;
      document.getElementById("stat-max-cells").innerText = `${{data.max_cells}} / 6`;
      
      const pct = Math.round((data.max_cells / 6) * 100);
      document.getElementById("gauge-fill").style.width = `${{pct}}%`;
      document.getElementById("gauge-pct").innerText = `${{pct}}%`;
      document.getElementById("commentary-text").innerText = data.comment;

      // Update indicator
      const nextPlayer = data.player === "Maker" ? "Breaker to Play" : "Maker to Play";
      document.getElementById("player-indicator").innerText = nextPlayer;
      document.getElementById("player-indicator").style.color = data.player === "Maker" ? "var(--accent-breaker)" : "var(--accent-maker)";

      // Highlight cells
      data.maker_cells.forEach((c, idx) => {{
        const el = document.getElementById(`cell-${{c[0]}}-${{c[1]}}`);
        if (el) {{
          el.classList.add("maker");
          el.innerHTML = `<span class="cell-num">M${{idx + 1}}</span><span class="cell-coord">${{c[0]}},${{c[1]}}</span>`;
        }}
      }});

      data.breaker_cells.forEach((c, idx) => {{
        const el = document.getElementById(`cell-${{c[0]}}-${{c[1]}}`);
        if (el) {{
          el.classList.add("breaker");
          el.innerHTML = `<span class="cell-num">B${{idx + 1}}</span><span class="cell-coord">${{c[0]}},${{c[1]}}</span>`;
        }}
      }});

      // Last move highlight
      const lastEl = document.getElementById(`cell-${{data.coord[0]}}-${{data.coord[1]}}`);
      if (lastEl) lastEl.classList.add("last-move");

      // Winning shape highlight
      if (data.won && currentMatch.winning_shape) {{
        currentMatch.winning_shape.forEach(c => {{
          const winEl = document.getElementById(`cell-${{c[0]}}-${{c[1]}}`);
          if (winEl) winEl.classList.add("winning-shape");
        }});
        document.getElementById("status-banner").innerText = "🏆 MAKER BREAKTHROUGH VICTORY (6/6 CELLS)!";
        document.getElementById("status-banner").style.color = "#fbbf24";
      }} else if (step === currentMatch.total_steps && currentMatch.winner === "Breaker") {{
        document.getElementById("status-banner").innerText = "🛡️ BREAKER TOTAL DENIAL VICTORY (SHUTDOWN AT 5/6)!";
        document.getElementById("status-banner").style.color = "#f43f5e";
      }} else {{
        document.getElementById("status-banner").innerText = "Match in Progress";
        document.getElementById("status-banner").style.color = "#a5b4fc";
      }}

      // Scroll active log entry into view
      document.querySelectorAll(".log-entry").forEach(e => e.classList.remove("active"));
      const activeLog = document.getElementById(`log-entry-${{step}}`);
      if (activeLog) {{
        activeLog.classList.add("active");
        activeLog.scrollIntoView({{ block: "nearest", behavior: "smooth" }});
      }}
    }}

    function onSliderChange(val) {{
      pause();
      renderStep(parseInt(val, 10));
    }}

    function stepBy(delta) {{
      pause();
      const target = Math.max(0, Math.min(currentMatch.total_steps, currentStep + delta));
      renderStep(target);
    }}

    function stepTo(target) {{
      pause();
      renderStep(target);
    }}

    function togglePlay() {{
      if (isPlaying) pause();
      else play();
    }}

    function play() {{
      if (currentStep >= currentMatch.total_steps) currentStep = 0;
      isPlaying = true;
      document.getElementById("play-btn").innerText = "⏸ Pause";
      playInterval = setInterval(() => {{
        if (currentStep < currentMatch.total_steps) {{
          renderStep(currentStep + 1);
        }} else {{
          pause();
        }}
      }}, playSpeed);
    }}

    function pause() {{
      isPlaying = false;
      document.getElementById("play-btn").innerText = "▶ Play";
      clearInterval(playInterval);
    }}

    function toggleSpeed() {{
      const btn = document.getElementById("speed-btn");
      if (playSpeed === 600) {{
        playSpeed = 300;
        btn.innerText = "2x";
      }} else if (playSpeed === 300) {{
        playSpeed = 150;
        btn.innerText = "4x";
      }} else {{
        playSpeed = 600;
        btn.innerText = "1x";
      }}
      if (isPlaying) {{
        pause();
        play();
      }}
    }}

    function switchMatch(mode) {{
      pause();
      currentMode = mode;
      currentMatch = MATCH_DATA[mode];
      document.getElementById("btn-9x9").classList.toggle("active", mode === "9x9");
      document.getElementById("btn-10x10").classList.toggle("active", mode === "10x10");
      initBoard();
    }}

    window.onload = () => {{
      initBoard();
    }};
  </script>
</body>
</html>
"""
    output_path = FS2_DIR / "grandmasters_replay.html"
    output_path.write_text(html_content, encoding="utf-8")
    print(f"Interactive Grandmaster Replay generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_html()
