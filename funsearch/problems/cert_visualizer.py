import json
import argparse
import os
from collections import Counter

HTML_HEAD = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Strategy Explorer</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 20px; line-height: 1.5; color: #333; background: #fafafa; }
  h1 { border-bottom: 2px solid #eaecef; padding-bottom: 10px; }
  .node { margin-left: 20px; border-left: 2px solid #dfe2e5; padding-left: 15px; margin-top: 10px; margin-bottom: 10px; }
  .tabs { display: flex; gap: 5px; margin-bottom: 5px; margin-top: 5px; }
  .tab-btn { cursor: pointer; padding: 4px 10px; border: 1px solid #d1d5da; border-radius: 4px; background: #f6f8fa; font-size: 12px; font-weight: 600; color: #24292e; }
  .tab-btn:hover { background: #e1e4e8; }
  .tab-btn.active { background: #0366d6; color: white; border-color: #0366d6; }
  .tab-content { display: none; padding: 10px; background: #fff; border: 1px solid #dfe2e5; border-radius: 4px; font-size: 14px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .tab-content.active { display: block; }
  .code-content { font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; white-space: pre-wrap; background: #f6f8fa; border: none; }
  details { margin-top: 5px; }
  summary { font-weight: 600; cursor: pointer; padding: 5px 0; outline: none; }
  summary:hover { color: #0366d6; }
  .breaker-response { margin-top: 10px; padding: 5px 10px; background: #fffbdd; border-left: 3px solid #e3c500; border-radius: 3px; font-weight: bold; }
  .winner-node { color: #28a745; font-weight: bold; padding: 5px 0; }
  .polyomino-grid { font-family: monospace; line-height: 1; margin: 10px 0; background: #fff; padding: 10px; border: 1px solid #ddd; display: inline-block;}
  .nav-bar { background: #24292e; color: white; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 6px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
  .nav-bar a { color: white; text-decoration: none; padding: 5px 10px; border-radius: 4px; transition: background 0.2s; }
  .nav-bar a:hover { background: #444c56; }
  .nav-bar a.active { background: #0366d6; font-weight: bold; }
</style>
<script>
function switchTab(nodeId, tabName) {
    document.querySelectorAll('#content-' + nodeId + ' > .tab-content').forEach(el => el.classList.remove('active'));
    document.getElementById('content-' + nodeId + '-' + tabName).classList.add('active');
    
    document.querySelectorAll('#tabs-' + nodeId + ' > .tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById('btn-' + nodeId + '-' + tabName).classList.add('active');
}
</script>
</head>
<body>
"""

HTML_FOOT = """
</body>
</html>
"""

def draw_shape(shape):
    if not shape: return ""
    max_x = max(p[0] for p in shape)
    max_y = max(p[1] for p in shape)
    grid = []
    for y in range(max_y, -1, -1):
        row = []
        for x in range(max_x + 1):
            if [x, y] in shape or (x, y) in shape:
                row.append("██")
            else:
                row.append("  ")
        grid.append("".join(row))
    return "\n".join(grid)

def generate_nav(base_name, active_tab):
    def cls(t): return "class='active'" if active_tab == t else ""
    return f"""
<div class="nav-bar">
  <strong style="font-size: 18px;">🧩 Strategy Explorer</strong>
  <div style="display: flex; gap: 10px;">
    <a href="viewer_{base_name}.html" {cls('viewer')}>🌲 Tree View</a>
    <a href="ride_mode_{base_name}.html" {cls('ride')}>🛹 Ride Mode</a>
    <a href="metadata_{base_name}.html" {cls('meta')}>📊 Metadata</a>
  </div>
</div>
"""

class Visualizer:
    def __init__(self, cert):
        self.cert = cert
        self.node_counter = 0

    def generate_all(self, out_dir, base_name):
        self.generate_viewer(out_dir, base_name)
        self.generate_metadata(out_dir, base_name)
        self.generate_ride_mode(out_dir, base_name)

    def generate_viewer(self, out_dir, base_name):
        html = [HTML_HEAD, generate_nav(base_name, "viewer")]
        html.append(f"<p><strong>Grid Radius:</strong> {self.cert.get('grid_radius', 4)} | <strong>Max Depth:</strong> {self.cert.get('max_depth', 8)}</p>")
        html.append("<div style='display: flex; gap: 30px; align-items: stretch; margin-bottom: 20px; flex-wrap: wrap;'>")
        html.append("<div style='flex: 0 0 auto;'>")
        html.append("<h3 style='margin-top: 0;'>Target Shape</h3>")
        html.append("<div class='polyomino-grid' style='font-size: 24px; line-height: 1.1; margin: 0;'>")
        html.append(draw_shape(self.cert.get('polyomino_base', [])).replace(" ", "&nbsp;").replace("\n", "<br>"))
        html.append("</div></div>")
        
        poly_size = len(self.cert.get('polyomino_base', []))
        poly_name = {4: "tetromino", 5: "pentomino", 6: "hexomino"}.get(poly_size, f"{poly_size}-omino")
        html.append("<div style='flex: 1; min-width: 400px; background: #eef7ff; border-left: 4px solid #0366d6; padding: 15px; border-radius: 4px; font-size: 14px;'>")
        html.append("<h4 style='margin-top: 0; margin-bottom: 10px; color: #0366d6;'>🧩 How to Read This Proof</h4>")
        html.append(f"<p style='margin-top: 0;'>To force a win for this {poly_name}, Maker must navigate Breaker's defenses.</p>")
        html.append("<p><strong>What is a \"Critical\" response?</strong><br>When Maker claims a cell, they actively threaten to complete specific alignments. A <strong>critical response</strong> occurs when Breaker plays directly into one of those actively threatened alignments. Otherwise, it's a wasted turn, and Maker proceeds down the <strong>Default path</strong>.</p>")
        html.append("</div></div>")
        
        html.append("<h2>Strategy Tree</h2>")
        self.node_counter = 0
        html.append(self.render_node(self.cert['strategy_tree']))
        html.append(HTML_FOOT)
        
        with open(os.path.join(out_dir, f"viewer_{base_name}.html"), "w") as f:
            f.write("\n".join(html))

    def render_node(self, tree, is_root=True, current_depth=0):
        if not tree: return "<div class='node'>None</div>"
        if self.node_counter > 5000:
            return "<div class='node' style='color: #d73a49; font-weight: bold;'>⚠️ Tree truncated: Over 5000 nodes reached.</div>"
        if tree[0] == "win":
            return "<div class='node winner-node'>🎯 Maker Wins! (Shape completed)</div>"
            
        if tree[0] == "move":
            self.node_counter += 1
            nid = self.node_counter
            maker_move = tree[1]
            branches = tree[2]
            default_tree = tree[3]
            num_critical = len(branches)
            
            summary_text = f"Maker plays {maker_move}."
            if num_critical > 0: summary_text += f" ({num_critical} critical threat responses)"
            
            narrative_text = f"Maker claims cell <strong>{maker_move}</strong>. "
            if num_critical == 0:
                narrative_text += "Breaker has no critical threats to block, so Maker can proceed along the default winning path."
            else:
                narrative_text += f"Breaker must respond to immediate threats. There are {num_critical} critical response(s): "
                narrative_text += ", ".join([f"<strong>{b[0]}</strong>" for b in branches]) + ". "
                
            code_obj = ["move", maker_move, [], "default_tree..."]
            if num_critical > 0: code_obj[2] = [[b[0], "...sub_tree..."] for b in branches]
            
            html = [f"<div class='node'><details {'open' if is_root else ''}><summary>Maker {maker_move}</summary>"]
            html.append(f"<div class='tabs' id='tabs-{nid}'>")
            html.append(f"<button class='tab-btn active' id='btn-{nid}-top' onclick='switchTab({nid}, \"top\")'>Top</button>")
            html.append(f"<button class='tab-btn' id='btn-{nid}-nat' onclick='switchTab({nid}, \"nat\")'>Natural Language</button>")
            html.append(f"<button class='tab-btn' id='btn-{nid}-code' onclick='switchTab({nid}, \"code\")'>Code</button></div>")
            html.append(f"<div id='content-{nid}'>")
            html.append(f"<div class='tab-content active' id='content-{nid}-top'>{summary_text}</div>")
            html.append(f"<div class='tab-content' id='content-{nid}-nat'>{narrative_text}</div>")
            html.append(f"<div class='tab-content code-content' id='content-{nid}-code'>{json.dumps(code_obj, indent=2)}</div></div>")
            
            for b in branches:
                html.append(f"<div class='breaker-response'>🛡️ If Breaker plays {b[0]}:</div>")
                html.append(self.render_node(b[1], is_root=False, current_depth=current_depth+1))
                
            html.append(f"<div class='breaker-response'>➡️ Default path (Breaker plays anything else):</div>")
            html.append(self.render_node(default_tree, is_root=False, current_depth=current_depth+1))
            html.append("</details></div>")
            return "\n".join(html)

    def generate_metadata(self, out_dir, base_name):
        html = [HTML_HEAD, generate_nav(base_name, "meta")]
        
        counts = Counter()
        def analyze(t):
            if not t or t[0] == 'win': return
            if t[0] == 'move':
                counts[len(t[2])] += 1
                for b in t[2]: analyze(b[1])
                analyze(t[3])
                
        analyze(self.cert['strategy_tree'])
        total_moves = sum(counts.values())
        
        html.append("<h2>Computational Metadata & Limitations</h2>")
        html.append("<div style='background: #fff; padding: 20px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); max-width: 800px;'>")
        html.append(f"<h3>Branching Factor Analysis</h3>")
        html.append(f"<p>Total Maker Moves (Nodes): <strong>{total_moves}</strong></p>")
        html.append("<table style='width: 100%; border-collapse: collapse; text-align: left;'>")
        html.append("<tr style='border-bottom: 2px solid #ddd;'><th>Critical Responses</th><th>Frequency</th><th>Percentage</th></tr>")
        for k in sorted(counts.keys()):
            perc = (counts[k] / total_moves) * 100 if total_moves else 0
            html.append(f"<tr style='border-bottom: 1px solid #eee;'><td>{k} responses</td><td>{counts[k]}</td><td>{perc:.1f}%</td></tr>")
        html.append("</table>")
        
        html.append("<h3 style='margin-top: 30px;'>Computational Limits Explained</h3>")
        html.append("<p><strong>Why bounded grids?</strong> Mathgod uses unbounded infinite grids, but explicit AI search trees must be capped to a Grid Radius (e.g., 4) to prevent combinatorial explosion.</p>")
        html.append("<p><strong>The 6x6 Wall:</strong> While 4-omino shapes are solved quickly, higher-order shapes like the Hexomino explode exponentially. A 6x6 board's explicit tree would require Petabytes of storage, making brute-force enumeration impossible and requiring topological formalizations in Lean 4.</p>")
        html.append("</div>")
        html.append(HTML_FOOT)
        
        with open(os.path.join(out_dir, f"metadata_{base_name}.html"), "w") as f:
            f.write("\n".join(html))

    def generate_ride_mode(self, out_dir, base_name):
        html = [HTML_HEAD, generate_nav(base_name, "ride")]
        
        radius = self.cert.get('grid_radius', 4)
        grid_size = radius * 2 + 1
        js_cert = json.dumps(self.cert)
        
        # We use a simple script injection to avoid f-string escaping hell.
        html.append("""
<div style="display: flex; gap: 40px; margin-top: 20px;">
  <!-- Board -->
  <div style="flex: 0 0 auto;">
    <svg id="game-board" width="500" height="500" style="background: #fff; border: 2px solid #333; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></svg>
  </div>
  
  <!-- Controls -->
  <div style="flex: 1; max-width: 500px;">
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
        <h3 style="margin-top: 0; color: #0366d6;">Step-by-Step Playback</h3>
        <p id="narrative-text" style="font-size: 16px; min-height: 80px;"></p>
        
        <div id="choices-container" style="display: flex; flex-direction: column; gap: 10px; margin-top: 20px;">
            <!-- Buttons injected here -->
        </div>
        
        <div style="margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
            <button id="btn-back" style="padding: 8px 16px; background: #e1e4e8; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">⬅️ Back (Undo)</button>
            <button id="btn-reset" style="padding: 8px 16px; background: #ffeef0; color: #d73a49; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; margin-left: 10px;">🔄 Reset to Start</button>
        </div>
    </div>
  </div>
</div>

<script>
""")
        html.append(f"const certData = {js_cert};")
        html.append(f"const R = {radius};")
        html.append(f"const SIZE = {grid_size};")
        html.append("""
const CELL_W = 500 / SIZE;

const svg = document.getElementById('game-board');
const narrative = document.getElementById('narrative-text');
const choices = document.getElementById('choices-container');

// State
let pathHistory = []; 
let currentTree = certData.strategy_tree;
let makerMoves = [];
let breakerMoves = [];

function coordToSVG(x, y) {
    const px = (x + R) * CELL_W;
    const py = (R - y) * CELL_W;
    return { px, py };
}

function drawBoard(ghostResponses) {
    svg.innerHTML = '';
    
    // Grid lines
    for(let i=0; i<=SIZE; i++) {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", i*CELL_W); line.setAttribute("y1", 0);
        line.setAttribute("x2", i*CELL_W); line.setAttribute("y2", 500);
        line.setAttribute("stroke", "#eee");
        svg.appendChild(line);
        
        const lineH = document.createElementNS("http://www.w3.org/2000/svg", "line");
        lineH.setAttribute("x1", 0); lineH.setAttribute("y1", i*CELL_W);
        lineH.setAttribute("x2", 500); lineH.setAttribute("y2", i*CELL_W);
        lineH.setAttribute("stroke", "#eee");
        svg.appendChild(lineH);
    }
    
    // Origin axes
    const axisX = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axisX.setAttribute("x1", 0); axisX.setAttribute("y1", 250);
    axisX.setAttribute("x2", 500); axisX.setAttribute("y2", 250);
    axisX.setAttribute("stroke", "#ccc"); axisX.setAttribute("stroke-width", "2");
    svg.appendChild(axisX);
    
    const axisY = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axisY.setAttribute("x1", 250); axisY.setAttribute("y1", 0);
    axisY.setAttribute("x2", 250); axisY.setAttribute("y2", 500);
    axisY.setAttribute("stroke", "#ccc"); axisY.setAttribute("stroke-width", "2");
    svg.appendChild(axisY);

    // Breaker moves (Red squares)
    breakerMoves.forEach(m => {
        const pos = coordToSVG(m[0], m[1]);
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", pos.px + 2); rect.setAttribute("y", pos.py + 2);
        rect.setAttribute("width", CELL_W - 4); rect.setAttribute("height", CELL_W - 4);
        rect.setAttribute("fill", "#d73a49");
        svg.appendChild(rect);
    });
    
    // Maker moves (Blue circles)
    makerMoves.forEach((m, idx) => {
        const pos = coordToSVG(m[0], m[1]);
        const circ = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circ.setAttribute("cx", pos.px + CELL_W/2); circ.setAttribute("cy", pos.py + CELL_W/2);
        circ.setAttribute("r", CELL_W/2 - 4);
        circ.setAttribute("fill", idx === makerMoves.length - 1 ? "#0366d6" : "#79b8ff"); 
        svg.appendChild(circ);
    });
    
    // Ghost dots (Critical Breaker responses)
    if(ghostResponses) {
        ghostResponses.forEach(m => {
            const pos = coordToSVG(m[0], m[1]);
            const circ = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            circ.setAttribute("cx", pos.px + CELL_W/2); circ.setAttribute("cy", pos.py + CELL_W/2);
            circ.setAttribute("r", CELL_W/4);
            circ.setAttribute("fill", "rgba(215, 58, 73, 0.5)"); 
            circ.setAttribute("stroke", "#d73a49");
            circ.setAttribute("stroke-width", "2");
            svg.appendChild(circ);
        });
    }
}

function renderState() {
    choices.innerHTML = '';
    
    if (!currentTree) {
        narrative.innerHTML = "<strong>Error:</strong> Reached empty tree node.";
        drawBoard([]);
        return;
    }
    
    if (currentTree[0] === 'win') {
        narrative.innerHTML = "<span style='color:#28a745; font-weight:bold; font-size:24px;'>🎯 MAKER WINS!</span><br>The shape is complete!";
        drawBoard([]);
        return;
    }
    
    if (currentTree[0] === 'move') {
        const makerMove = currentTree[1];
        const branches = currentTree[2];
        const defaultTree = currentTree[3];
        
        makerMoves.push(makerMove);
        const numCritical = branches.length;
        
        if(numCritical === 0) {
            narrative.innerHTML = `Maker claims <strong>[${makerMove}]</strong>.<br><br>There are no critical threats to block, so Breaker can play anywhere (Default path).`;
        } else {
            narrative.innerHTML = `Maker claims <strong>[${makerMove}]</strong>.<br><br>Breaker is forced to respond. The red ghost dots show Breaker's <strong>${numCritical} critical response options</strong>.`;
        }
        
        const ghosts = branches.map(b => b[0]);
        drawBoard(ghosts);
        
        branches.forEach(b => {
            const btn = document.createElement('button');
            btn.innerHTML = `🛡️ If Breaker plays <strong>[${b[0]}]</strong>`;
            btn.style.cssText = "padding: 10px; background: #fffbdd; border: 1px solid #e3c500; text-align: left; cursor: pointer; border-radius: 4px;";
            btn.onclick = () => advance(b[1], makerMove, b[0]);
            choices.appendChild(btn);
        });
        
        const defBtn = document.createElement('button');
        defBtn.innerHTML = `➡️ Default path (Breaker plays elsewhere)`;
        defBtn.style.cssText = "padding: 10px; background: #f6f8fa; border: 1px solid #ddd; text-align: left; cursor: pointer; border-radius: 4px;";
        defBtn.onclick = () => advance(defaultTree, makerMove, null);
        choices.appendChild(defBtn);
        
        makerMoves.pop();
    }
}

function advance(nextTree, mMove, bMove) {
    pathHistory.push({ tree: currentTree, mMove, bMove });
    currentTree = nextTree;
    makerMoves.push(mMove);
    if(bMove) breakerMoves.push(bMove);
    renderState();
}

document.getElementById('btn-back').onclick = () => {
    if(pathHistory.length === 0) return;
    const last = pathHistory.pop();
    currentTree = last.tree;
    makerMoves.pop();
    if(last.bMove) breakerMoves.pop();
    renderState();
};

document.getElementById('btn-reset').onclick = () => {
    pathHistory = [];
    makerMoves = [];
    breakerMoves = [];
    currentTree = certData.strategy_tree;
    renderState();
};

renderState();
</script>
""")
        html.append(HTML_FOOT)
        
        with open(os.path.join(out_dir, f"ride_mode_{base_name}.html"), "w") as f:
            f.write("\n".join(html))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cert', type=str, required=True, help="Path to input JSON certificate")
    parser.add_argument('--outdir', type=str, required=True, help="Output directory")
    parser.add_argument('--basename', type=str, required=True, help="Base name (e.g. 4_5)")
    args = parser.parse_args()
    
    with open(args.cert, 'r') as f:
        cert_data = json.load(f)
        
    viz = Visualizer(cert_data)
    viz.generate_all(args.outdir, args.basename)
    print(f"Generated all explorer HTML files in {args.outdir}")
