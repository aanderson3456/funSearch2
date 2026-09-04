import json

def make_html(trace_file, out_file, title):
    with open(trace_file, "r") as f:
        data = json.load(f)
    trace = data["trace"]
    winning_shape = data["winningShape"]
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background-color: #1a1a1a; color: white; }}
            #board {{ display: grid; grid-template-columns: repeat(13, 30px); gap: 2px; margin-top: 20px; padding: 10px; background-color: #333; border-radius: 8px; }}
            .cell {{ width: 30px; height: 30px; background-color: #444; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 12px; transition: background-color 0.3s; }}
            .maker {{ background-color: #3b82f6; }}
            .breaker {{ background-color: #ef4444; }}
            .winning {{ background-color: #22c55e !important; box-shadow: 0 0 10px #22c55e; z-index: 10; }}
            #controls {{ margin-top: 20px; display: flex; gap: 10px; align-items: center; }}
            button {{ padding: 8px 16px; background-color: #4f46e5; color: white; border: none; border-radius: 4px; cursor: pointer; }}
            button:hover {{ background-color: #4338ca; }}
            #turn-info {{ font-size: 1.2rem; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h2>{title}</h2>
        <div id="turn-info">Turn: 0</div>
        <div id="board"></div>
        <div id="controls">
            <button onclick="prevTurn()">Previous</button>
            <button onclick="togglePlay()" id="playBtn">Play</button>
            <button onclick="nextTurn()">Next</button>
        </div>

        <script>
            const trace = {json.dumps(trace)};
            const winningShape = {json.dumps(winning_shape)};
            let currentTurn = 0;
            let isPlaying = false;
            let playInterval;

            const board = document.getElementById('board');
            for(let y=-6; y<=6; y++) {{
                for(let x=-6; x<=6; x++) {{
                    const cell = document.createElement('div');
                    cell.className = 'cell';
                    cell.id = `cell-${{x}}-${{y}}`;
                    board.appendChild(cell);
                }}
            }}

            function updateBoard() {{
                document.querySelectorAll('.cell').forEach(c => c.className = 'cell');
                for(let i=0; i<currentTurn; i++) {{
                    const move = trace[i];
                    const cell = document.getElementById(`cell-${{move.move[0]}}-${{move.move[1]}}`);
                    if(cell) {{
                        cell.classList.add(move.player);
                        cell.textContent = i+1;
                    }}
                }}
                
                if(currentTurn === trace.length && winningShape) {{
                    winningShape.forEach(p => {{
                        const cell = document.getElementById(`cell-${{p[0]}}-${{p[1]}}`);
                        if(cell) cell.classList.add('winning');
                    }});
                }}
                document.getElementById('turn-info').textContent = `Turn: ${{currentTurn}} / ${{trace.length}}`;
            }}

            function nextTurn() {{
                if(currentTurn < trace.length) {{ currentTurn++; updateBoard(); }}
                else pause();
            }}

            function prevTurn() {{
                if(currentTurn > 0) {{ currentTurn--; updateBoard(); }}
            }}

            function togglePlay() {{
                if(isPlaying) pause();
                else play();
            }}

            function play() {{
                isPlaying = true;
                document.getElementById('playBtn').textContent = 'Pause';
                if(currentTurn === trace.length) currentTurn = 0;
                playInterval = setInterval(nextTurn, 500);
            }}

            function pause() {{
                isPlaying = false;
                document.getElementById('playBtn').textContent = 'Play';
                clearInterval(playInterval);
            }}
            
            updateBoard();
        </script>
    </body>
    </html>
    """
    with open(out_file, "w") as f:
        f.write(html)

make_html("arena_13x13_trace.json", "arena_match_1_replay.html", "Match 1: Heuristic Maker vs NN Breaker")
make_html("arena_13x13_trace_2.json", "arena_match_2_replay.html", "Match 2: NN Maker vs Heuristic Breaker")
make_html("arena_13x13_trace_3.json", "arena_match_3_replay.html", "Match 3: NN Maker vs NN Breaker")
