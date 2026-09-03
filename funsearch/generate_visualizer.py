import json
import os
from funsearch.problems import snakey_interactive
from funsearch.interactive_evaluator import simulate_game

def load_func(filepath, func_name):
    with open(filepath, 'r') as f:
        code = f.read()
    namespace = {}
    exec(code, namespace)
    return namespace[func_name]

def main():
    print("Running simulation...")
    maker_func = load_func("outputs/snakey_1788406504/best_program.py", "priority")
    breaker_func = load_func("outputs/snakey_breaker_1788405958/best_program.py", "breaker_priority")
    
    # Capture trace
    all_shapes = snakey_interactive._get_board_shapes(radius=6)
    m_cells, b_cells = [], []
    maker_won = False
    
    trace = []
    
    winning_shape = None
    for turn in range(25):
        m_set, b_set = set(m_cells), set(b_cells)
        for s in all_shapes:
            if s.issubset(m_set):
                maker_won = True
                winning_shape = list(s)
                break
        if maker_won:
            break
            
        active = [s for s in all_shapes if not (s & b_set)]
        if not active:
            break
            
        candidates = set()
        for s in active:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates.add(p)
        if not candidates:
            break
            
        best_m_move = max(candidates, key=lambda c: maker_func(c, m_cells, b_cells, active))
        m_cells.append(best_m_move)
        trace.append({'turn': turn + 1, 'player': 'maker', 'move': list(best_m_move)})
        
        m_set = set(m_cells)
        active_for_breaker = [s for s in all_shapes if not (s & b_set)]
        candidates_b = set()
        for s in active_for_breaker:
            for p in s:
                if p not in m_set and p not in b_set:
                    candidates_b.add(p)
                    
        if not candidates_b:
            break
            
        b_move = max(candidates_b, key=lambda c: breaker_func(c, m_cells, b_cells, active_for_breaker))
        b_cells.append(b_move)
        trace.append({'turn': turn + 1, 'player': 'breaker', 'move': list(b_move)})
        
    print(f"Simulation done. Maker won: {maker_won}. Turns: {len(m_cells)}. Traces: {len(trace)}")
    
    # Generate HTML
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>MathGod - Snakey Arena Replay</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700;800&family=Inter:wght@400;600;800&display=swap');
    
    :root {{
      --bg-color: #f8fafc;
      --card-bg: #ffffff;
      --text-primary: #1e293b;
      --text-secondary: #475569;
      --maker-color: #38bdf8;
      --breaker-color: #fb7185;
      --accent-color: #8b5cf6;
      --grid-line: #cbd5e1;
      --grid-hover: #e2e8f0;
    }}
    body {{
      font-family: 'Inter', sans-serif;
      background-color: var(--bg-color);
      color: var(--text-primary);
      margin: 0;
      padding: 2rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-height: 100vh;
    }}
    h1 {{
      font-size: 2.5rem;
      font-weight: 800;
      background: linear-gradient(to right, var(--maker-color), var(--accent-color));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 0.5rem;
    }}
    .subtitle {{
      color: var(--text-secondary);
      margin-bottom: 2rem;
    }}
    .game-container {{
      background-color: var(--card-bg);
      padding: 2rem;
      border-radius: 1rem;
      box-shadow: 0 20px 50px -12px #0000001a;
      border: 1px solid rgba(0,0,0,0.05);
      display: flex;
      flex-direction: column;
      align-items: center;
      max-width: 800px;
      width: 100%;
    }}
    .controls {{
      display: flex;
      gap: 1rem;
      margin-bottom: 2rem;
      width: 100%;
      justify-content: center;
    }}
    button {{
      padding: 0.75rem 1.5rem;
      border-radius: 0.5rem;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
    }}
    button.primary {{
      background-color: var(--accent-color);
      color: white;
    }}
    button.primary:hover {{
      background-color: #7c3aed;
      transform: translateY(-1px);
    }}
    button:disabled {{
      opacity: 0.5;
      cursor: not-allowed;
    }}
    .status-card {{
      background-color: #0000000d;
      padding: 1rem 2rem;
      border-radius: 0.5rem;
      text-align: center;
      margin-bottom: 2rem;
      min-width: 200px;
    }}
    .status-label {{ font-size: 0.8rem; color: var(--text-secondary); }}
    .status-value {{ font-size: 1.2rem; font-weight: 700; margin-top: 0.25rem; }}
    .turn-maker {{ color: var(--maker-color); }}
    .turn-breaker {{ color: var(--breaker-color); }}
    
    svg {{
      width: 100%;
      max-width: 600px;
      height: auto;
    }}
    .cell {{
      stroke: var(--grid-line);
      stroke-width: 1;
      fill: transparent;
      transition: fill 0.3s;
    }}
    .maker-piece {{
      fill: var(--maker-color);
      filter: drop-shadow(0 0 10px var(--maker-color));
    }}
    .breaker-piece {{
      fill: var(--breaker-color);
      filter: drop-shadow(0 0 10px var(--breaker-color));
    }}
    .winning-cell {{
      stroke: var(--accent-color) !important;
      stroke-width: 4 !important;
      filter: drop-shadow(0 0 15px var(--accent-color));
      animation: pulse 1s infinite alternate;
    }}
    @keyframes pulse {{
      from {{ transform: scale(1); transform-origin: center; }}
      to {{ transform: scale(1.05); transform-origin: center; }}
    }}
    .victory-banner {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(255, 255, 255, 0.95);
      border: 4px solid var(--accent-color);
      padding: 2rem 4rem;
      border-radius: 1rem;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0,0,0,0.3);
      display: none;
      z-index: 100;
    }}
    .victory-banner h2 {{
      margin: 0;
      font-size: 3rem;
      font-weight: 800;
      color: var(--accent-color);
      text-transform: uppercase;
    }}
    .grid-wrapper {{
      position: relative;
      width: 100%;
      max-width: 600px;
      display: flex;
      justify-content: center;
    }}
  </style>
</head>
<body>
  <h1>ARENA REPLAY</h1>
  <p class="subtitle">Agent-in-the-Loop Latest Generation</p>
  
  <div class="game-container">
    <div class="controls">
      <button id="btn-prev" class="primary" onclick="step(-1)" disabled>Prev Move</button>
      <button id="btn-auto" class="primary" onclick="toggleAuto()">Autoplay</button>
      <div class="status-card">
        <div class="status-label">Turn Status</div>
        <div id="status-display" class="status-value">Start</div>
      </div>
      <button id="btn-next" class="primary" onclick="step(1)">Next Move</button>
    </div>
    
    <div class="grid-wrapper">
        <svg id="grid-svg" viewBox="0 0 650 650">
          <!-- Grid drawn by JS -->
        </svg>
        <div id="victory-banner" class="victory-banner">
            <h2>MAKER WINS!</h2>
            <p>6-Cell Shape Completed</p>
        </div>
    </div>
  </div>

  <script>
    const trace = {json.dumps(trace)};
    const winningShape = {json.dumps(winning_shape)};
    let currentStep = 0;
    let autoInterval = null;
    
    // Draw Grid (13x13 grid, radius 6)
    const svg = document.getElementById('grid-svg');
    const cellSize = 50;
    for (let x = -6; x <= 6; x++) {{
      for (let y = -6; y <= 6; y++) {{
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", (x + 6) * cellSize);
        rect.setAttribute("y", (y + 6) * cellSize);
        rect.setAttribute("width", cellSize);
        rect.setAttribute("height", cellSize);
        rect.setAttribute("class", "cell");
        rect.setAttribute("id", `cell-${{x}}-${{y}}`);
        svg.appendChild(rect);
      }}
    }}
    
    function updateBoard() {{
      // Reset all
      document.querySelectorAll('.cell').forEach(el => {{
          el.setAttribute("class", "cell");
          el.style.transformOrigin = "center";
          el.style.transformBox = "fill-box";
      }});
      document.getElementById('victory-banner').style.display = 'none';
      
      // Apply trace up to currentStep
      for(let i=0; i<currentStep; i++) {{
        const move = trace[i];
        const cell = document.getElementById(`cell-${{move.move[0]}}-${{move.move[1]}}`);
        if(cell) {{
           cell.setAttribute("class", `cell ${{move.player}}-piece`);
        }}
      }}
      
      // Check for win
      if (currentStep === trace.length && winningShape) {{
          document.getElementById('victory-banner').style.display = 'block';
          winningShape.forEach(p => {{
              const c = document.getElementById(`cell-${{p[0]}}-${{p[1]}}`);
              if(c) c.setAttribute("class", "cell maker-piece winning-cell");
          }});
      }}
      
      // Update UI
      document.getElementById('btn-prev').disabled = currentStep === 0;
      document.getElementById('btn-next').disabled = currentStep === trace.length;
      
      const statusDiv = document.getElementById('status-display');
      if (currentStep === 0) {{
        statusDiv.innerText = "Start";
        statusDiv.className = "status-value";
      }} else {{
        const lastMove = trace[currentStep-1];
        statusDiv.innerText = `Turn ${{lastMove.turn}}: ${{lastMove.player.toUpperCase()}}`;
        statusDiv.className = `status-value turn-${{lastMove.player}}`;
      }}
      
      if (currentStep === trace.length && autoInterval) {{
          toggleAuto();
      }}
    }}
    
    function step(delta) {{
      currentStep += delta;
      if (currentStep < 0) currentStep = 0;
      if (currentStep > trace.length) currentStep = trace.length;
      updateBoard();
    }}
    
    function toggleAuto() {{
        const btn = document.getElementById('btn-auto');
        if (autoInterval) {{
            clearInterval(autoInterval);
            autoInterval = null;
            btn.innerText = "Autoplay";
            btn.style.backgroundColor = "var(--accent-color)";
        }} else {{
            if (currentStep === trace.length) {{
                currentStep = 0;
                updateBoard();
            }}
            autoInterval = setInterval(() => step(1), 1000);
            btn.innerText = "Stop";
            btn.style.backgroundColor = "var(--breaker-color)";
        }}
    }}
    
    updateBoard();
  </script>
</body>
</html>
"""
    
    from pathlib import Path
    out_path = Path(os.environ.get("SNAKEY_REPLAY_HTML", "snakey_replay.html"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Generated visualizer at: {out_path.resolve()}")

if __name__ == '__main__':
    main()
