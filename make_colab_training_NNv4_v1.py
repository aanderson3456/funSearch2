import json
import shutil
import os

with open('train_colab_NNv4.py', 'r') as f:
    train_code = f.read()

cells = [
    {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '# SnakyNet Massive 13x13 Self-Play Training on Colab Pro (NNv4_v1)\n',
            'This notebook trains the 13x13 AlphaGo-style ResNet for the Snakey game using Google Colab A100 GPUs.\n',
            '\n',
            '### Major Innovations in NNv4:\n',
            '1. **7-Channel Input Representation:**\n',
            '   - Channels 0-1: Maker & Breaker stone bitmasks\n',
            '   - Channel 2: Current player turn plane\n',
            '   - Channels 3-4: Checkerboard parity & Centrality gradient\n',
            '   - Channel 5: Single-threat heatmap (immediate 1-move win threats: 5/6 stones)\n',
            '   - **Channel 6: Dual-Threat / Fork Potential Heatmap:** Vectorized real-time identification of fork vertices (cells intersecting multiple active shapes with 4 or 3 Maker stones, plus existing unblockable 5-stone dual threats).\n',
            '2. **Curriculum / Hybrid Self-Play:**\n',
            '   - Injects Champion FunSearch Maker () into 25% of self-play games.\n',
            '   - Network learns directly from master-level geometric forks (via policy and value targets) AND learns how to defend against them as Breaker.\n',
            '   - 75% pure self-play games allow the network to internalize and transcend the heuristic.\n',
            '3. **Asymmetric Opening Exploration:**\n',
            '   - Moves 1–6: Maker explores diverse fork geometries using elevated Dirichlet noise (, ) and temperature $\\tau=1.25$.\n',
            '   - Breaker maintains disciplined defense (, $\\tau=1.0$).\n',
            '   - Moves > 6: Symmetrical exploration ($\\tau=1.0$, ), tapering to $\\tau=0.5$ in midgame and $\\tau=0.2$ in endgame.\n',
            '4. **Vectorized Fast Engine:**\n',
            '   - Dual threat and FunSearch calculations are fully vectorized in NumPy (<0.3 ms per state), ensuring training runs blazingly fast on A100 GPUs without wasting GPU hours.'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            'from google.colab import drive\n',
            'drive.mount("/content/drive")\n',
            'import os\n',
            'os.makedirs("/content/drive/MyDrive/SnakyNet_v4_Checkpoints", exist_ok=True)\n',
            'print("Mounted Google Drive and verified SnakyNet_v4_Checkpoints directory!")'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            '!rm -rf /content/funSearch2-main\n',
            '!rm -rf /content/main.zip\n',
            '!wget -q https://github.com/aanderson3456/funSearch2/archive/refs/heads/main.zip\n',
            '!unzip -q main.zip\n',
            'import sys\n',
            'sys.path.append("/content/funSearch2-main")\n',
            'sys.path.append("/content/funSearch2-main/big_nn")\n',
            'print("Repository cloned and paths added to sys.path!")'
        ]
    },
    {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            line + '\n' for line in train_code.splitlines()
        ]
    }
]

notebook = {
    'cells': cells,
    'metadata': {
        'accelerator': 'GPU',
        'colab': {
            'gpuType': 'A100',
            'provenance': []
        },
        'kernelspec': {
            'display_name': 'Python 3',
            'name': 'python3'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 0
}

target_ipynb = 'colab_training_NNv4_v1.ipynb'
with open(target_ipynb, 'w') as f:
    json.dump(notebook, f, indent=2)
print(f'Successfully generated {target_ipynb}!')

gdrive_path = '/Users/austinanderson/Library/CloudStorage/GoogleDrive-pianowater@gmail.com/My Drive/Colab Notebooks/colab_training_NNv4_v1.ipynb'
if os.path.exists(os.path.dirname(gdrive_path)):
    shutil.copyfile(target_ipynb, gdrive_path)
    print(f'Successfully synced {target_ipynb} to Google Drive at: {gdrive_path}!')
else:
    print(f'Warning: Google Drive directory not found at {os.path.dirname(gdrive_path)}')
