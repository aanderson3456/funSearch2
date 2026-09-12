import json
from pathlib import Path

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# SnakyNet v4 AlphaZero Self-Play Runner (Git Auto-Sync)\n",
                "This notebook automatically clones and executes the latest `train_colab_NNv4.py` directly from GitHub.\n",
                "- **Zero Notebook Maintenance**: You never need to upload or edit this `.ipynb` file again.\n",
                "- **Auto-Sync**: Automatically pulls the newest FunSearch Grandmaster champions, A100 AMP optimizations, and threat detectors from GitHub on every run.\n",
                "- **Checkpoint Continuity**: Automatically resumes from the latest checkpoint on Google Drive (`/content/drive/MyDrive/SnakyNet_v4_Checkpoints`)."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from google.colab import drive\n",
                "drive.mount('/content/drive')\n",
                "import os\n",
                "os.makedirs('/content/drive/MyDrive/SnakyNet_v4_Checkpoints', exist_ok=True)\n",
                "print('Mounted Google Drive and verified SnakyNet_v4_Checkpoints directory!')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "!rm -rf /content/funSearch2\n",
                "!git clone https://github.com/aanderson3456/funSearch2.git /content/funSearch2\n",
                "%cd /content/funSearch2/FS2\n",
                "!git pull origin main 2>/dev/null || true\n",
                "print('Cloned latest repository with newest FunSearch Grandmaster models!')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "!python train_colab_NNv4.py"
            ]
        }
    ],
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "A100",
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

for path_str in [
    "colab_runner.ipynb",
    "colab_training_NNv4_v1.ipynb",
    "/Users/austinanderson/Library/CloudStorage/GoogleDrive-pianowater@gmail.com/My Drive/Colab Notebooks/colab_training_NNv4_v1.ipynb",
]:
    p = Path(path_str)
    if p.parent.exists():
        with open(p, "w") as f:
            json.dump(notebook, f, indent=2)
        print(f"Updated {p}")
