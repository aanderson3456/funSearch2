import json

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🐍 Snaky 13x13 Arena (Colab Edition)\n",
                "This notebook automatically mounts your Google Drive, finds your latest trained model, fixes any PyTorch saving issues, and runs the Arena!"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Cell 1: Mount Google Drive & Setup Repository\n",
                "import os\n",
                "from google.colab import drive\n",
                "\n",
                "print(\"Mounting Google Drive...\")\n",
                "drive.mount('/content/drive')\n",
                "\n",
                "print(\"\\nDownloading latest FunSizzy code from GitHub...\")\n",
                "# Remove old nested folders if they exist\n",
                "!rm -rf /content/funSearch2-main\n",
                "!rm -rf /content/main.zip\n",
                "\n",
                "!wget -q https://github.com/aanderson3456/funSearch2/archive/refs/heads/main.zip\n",
                "!unzip -q main.zip\n",
                "print(\"Repository downloaded and extracted to /content/funSearch2-main\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Cell 2: Find the Model, Copy it, and Fix it (if needed)\n",
                "import os, sys, glob\n",
                "import shutil\n",
                "import torch\n",
                "\n",
                "# 1. First, search for the model in Google Drive\n",
                "print(\"Searching for snaky_large_model_it*.pt in Google Drive...\")\n",
                "drive_models = glob.glob(\"/content/drive/MyDrive/**/snaky_large_model_it*.pt\", recursive=True)\n",
                "root_models = glob.glob(\"/content/snaky_large_model_it*.pt\") # In case you uploaded manually to the sidebar\n",
                "\n",
                "all_models = drive_models + root_models\n",
                "\n",
                "if not all_models:\n",
                "    print(\"❌ ERROR: Could not find any snaky_large_model_it*.pt files in Google Drive!\")\n",
                "    print(\"Please upload the file to your Google Drive and run this cell again.\")\n",
                "else:\n",
                "    # Sort by modification time to get the most recently added one\n",
                "    all_models.sort(key=os.path.getmtime, reverse=True)\n",
                "    latest_model_path = all_models[0]\n",
                "    \n",
                "    print(f\"✅ Found latest model at: {latest_model_path}\")\n",
                "    \n",
                "    # 2. Add big_nn to sys.path so torch.load can find resnet if it's a full model\n",
                "    sys.path.append(\"/content/funSearch2-main/big_nn\")\n",
                "    \n",
                "    # 3. Load it and check if it's a full model or state_dict\n",
                "    print(\"Inspecting the model file...\")\n",
                "    try:\n",
                "        # Load ignoring security flags temporarily in case it's a full model\n",
                "        loaded = torch.load(latest_model_path, weights_only=False, map_location='cpu')\n",
                "        \n",
                "        target_path = f\"/content/funSearch2-main/{os.path.basename(latest_model_path)}\"\n",
                "        \n",
                "        if isinstance(loaded, dict):\n",
                "            print(\"Model is already a clean state_dict! Copying it over...\")\n",
                "            shutil.copy2(latest_model_path, target_path)\n",
                "        else:\n",
                "            print(\"Model is a full object! Extracting state_dict and saving it cleanly...\")\n",
                "            torch.save(loaded.state_dict(), target_path)\n",
                "            \n",
                "        print(f\"🎉 Model is perfectly set up at: {target_path}\")\n",
                "        \n",
                "    except Exception as e:\n",
                "        print(f\"❌ ERROR processing model: {e}\")"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Cell 3: Run the 13x13 Arena\n",
                "import os\n",
                "os.chdir(\"/content/funSearch2-main\")\n",
                "\n",
                "print(\"Starting the Arena! (This will take a minute or two...)\")\n",
                "!python arena_13x13.py"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Cell 4: View the Replay\n",
                "import IPython\n",
                "IPython.display.HTML(filename='/content/funSearch2-main/snakey_replay.html')"
            ]
        }
    ],
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "T4",
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open("colab_arena.ipynb", "w") as f:
    json.dump(notebook, f, indent=2)
print("Notebook generated!")
