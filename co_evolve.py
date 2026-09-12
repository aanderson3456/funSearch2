"""Snakey Maker & Breaker Co-Evolution Runner (100 Generations).

Executes alternating Maker and Breaker multi-island evolutionary discovery
with move count logging, baseline normies included, and capped at <=25% CPU.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add FS2 to path
FS2_DIR = Path(__file__).resolve().parent
if str(FS2_DIR) not in sys.path:
    sys.path.insert(0, str(FS2_DIR))

from boost_mock_evolution import main

if __name__ == "__main__":
    main()

