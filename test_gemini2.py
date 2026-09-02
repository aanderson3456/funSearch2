import os
from pathlib import Path
from funsearch.llm.gemini import GeminiLLM

if "GEMINI_API_KEY" not in os.environ:
    for line in Path(".env").read_text().splitlines():
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip("'\"")

llm = GeminiLLM(model_name="gemini-3.6-flash", samples_per_prompt=1)
prompt = """
def priority_v0(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  return 0.0

def priority_v1(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
"""
print("Running GeminiLLM...")
res = llm.draw_sample(prompt)
print("LENGTH:", len(res))
print(res)
