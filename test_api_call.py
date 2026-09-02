import os
import sys
from pathlib import Path
from funsearch.llm.gemini import GeminiLLM
from funsearch.core import code_manipulation

def main():
    if "GEMINI_API_KEY" not in os.environ:
        try:
            for line in Path(".env").read_text().splitlines():
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")
        except:
            pass

    # Setup LLM
    llm = GeminiLLM(model_name="gemini-3.6-flash", temperature=0.7)
    
    # Read Snakey spec
    spec = Path("funsearch/problems/snakey.py").read_text()
    
    # Get the evolve function code
    template, function_to_evolve = next(code_manipulation.yield_decorated(spec, 'funsearch', 'evolve'))
    evolve_fn = template.get_function(function_to_evolve)
    
    # Generate prompt like Sampler does
    prompt = f'"""\nComplete the following function.\n"""\n{str(evolve_fn)}'
    
    print("====== SENDING PROMPT ======")
    print(prompt)
    print("====== GENERATING (gemini-3.6-flash) ======")
    
    sample = llm.draw_sample(prompt)
    print("====== RAW OUTPUT ======")
    print(sample)
    print("========================")
    
    # Trim logic
    from funsearch.sandbox.base import trim_function_body
    body = trim_function_body(sample)
    print("====== PARSED BODY ======")
    print(body)
    print("========================")

if __name__ == "__main__":
    main()
