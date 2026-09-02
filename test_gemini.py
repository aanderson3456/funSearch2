import os
from pathlib import Path
from google import genai
from google.genai import types

if "GEMINI_API_KEY" not in os.environ:
    for line in Path(".env").read_text().splitlines():
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip("'\"")

prompt = """
def priority_v0(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  return 0.0

def priority_v1(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
"""

client = genai.Client()
config = types.GenerateContentConfig(temperature=0.7, max_output_tokens=2048)
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=config
)
print("LENGTH:", len(response.text))
print(response.text)
