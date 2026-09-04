import sys

with open("arena_13x13.py", "r") as f:
    code = f.read()

# Add a print statement in the turn loop
code = code.replace(
    'for turn in range(85): # Max ~84 moves per player on 13x13',
    'for turn in range(85): # Max ~84 moves per player on 13x13\n        print(f"\\rMatch turn {turn+1}...", end="", flush=True)'
)

with open("arena_13x13.py", "w") as f:
    f.write(code)
