---
name: funsearch-snakey-search
description: >-
  Runs and monitors live LLM-driven FunSearch evolutionary discovery on the Snakey Polyomino
  Achievement Game, generating Maker strategies against adversarial Breakers and exporting
  proof certificates to Lean 4.
---

# FunSearch Snakey Evolutionary Strategy Search

This skill guides running, monitoring, and exporting results from the **FunSearch** evolutionary program search engine for the **Snaky Hexomino Polyomino Achievement Game**.

---

## 1. Secret API Key Configuration

To keep your Google Gemini API key secure without exposing it in terminal logs, git history, or process tables:

### Option A: Shell Environment Variable (Recommended for interactive sessions)
Set the variable in your current terminal session (or add to `~/.zshrc` / `~/.zshenv`):
```bash
export GEMINI_API_KEY="<your-api-key>"
```

### Option B: Local `.env` File (Ignored by Git)
Create a `.env` file in the project root:
```bash
echo 'GEMINI_API_KEY="<your-api-key>"' > /Users/austinanderson/GitHub/FunSearchScratch/.env
chmod 600 /Users/austinanderson/GitHub/FunSearchScratch/.env
```
*(Note: `.env` is listed in `.gitignore` so it will never be committed).*

### Option C: macOS Keychain (Maximum Security)
Store the key in the system keychain:
```bash
security add-generic-password -s "GEMINI_API_KEY" -a "$USER" -w "<your-api-key>" -U
```
Then load it into your shell on-demand:
```bash
export GEMINI_API_KEY=$(security find-generic-password -s "GEMINI_API_KEY" -w)
```

---

## 2. Launching Live Evolutionary Search

### Recommended Command (Gemini 3.6 Flash / Gemini 3.7 Flash)
```bash
cd /Users/austinanderson/GitHub/FunSearchScratch
source .venv/bin/activate

# Ensure your key is exported
export GEMINI_API_KEY="${GEMINI_API_KEY:-$(security find-generic-password -s "GEMINI_API_KEY" -w 2>/dev/null)}"

# Launch FunSearch on Snakey
python -m funsearch.cli \
  --problem snakey \
  --model gemini-3.6-flash \
  --iterations 50 \
  --samples-per-prompt 2 \
  --islands 5
```

### Command Flags Reference
| Flag | Description | Default | Recommended |
|---|---|---|---|
| `--problem` | Problem specification (`snakey`, `cap_set`, `bin_packing`) | required | `snakey` |
| `--model` | LLM model (`gemini-3.6-flash`, `gemini-3.7-flash`, `mock`) | `gemini-3.6-flash` | `gemini-3.6-flash` |
| `--iterations` | Total evolutionary iterations to run | `50` | `50`–`150` |
| `--samples-per-prompt` | Number of candidate programs sampled per step | `2` | `2`–`4` |
| `--islands` | Number of independent evolutionary populations | `5` | `5`–`10` |
| `--temperature` | LLM sampling temperature | `0.7` | `0.7` |
| `--no-live` | Disable rich terminal dashboard (useful for headless background tasks) | `False` | Omit for live UI |

---

## 3. Fast Zero-Cost Offline Testing (Mock Sampler)
To verify changes to problem specifications or sandbox execution without consuming API quota:
```bash
cd /Users/austinanderson/GitHub/FunSearchScratch
source .venv/bin/activate
python -m funsearch.cli --problem snakey --model mock --iterations 20 --islands 3
```

---

## 4. Exporting Discovered Strategies to Lean 4

When a winning Maker strategy is evolved, FunSearch saves the checkpoint in `outputs/snakey_<timestamp>/best_program.py`.

To transpile the Python strategy tree into a verified Lean 4 `StrategyTree` theorem:
```bash
python -m funsearch.problems.snakey_lean_transpiler \
  --output /Users/austinanderson/GitHub/MyLean4Code/SnakeyLean/Snakey/SnakeyProof.lean
```

To build and formally verify with the Lean 4 compiler:
```bash
cd /Users/austinanderson/GitHub/MyLean4Code/SnakeyLean
lake build
```
