import os
from pathlib import Path
from funsearch.llm.gemini import GeminiLLM

if "GEMINI_API_KEY" not in os.environ:
    for line in Path(".env").read_text().splitlines():
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip("'\"")

prompt = Path("funsearch_prompt_dump.txt").read_text()
llm = GeminiLLM(model_name="gemini-3.6-flash", samples_per_prompt=1)
print("Running GeminiLLM...")
res = llm.draw_sample(prompt)
print("LENGTH:", len(res))
print(res)
