"""Command-line interface for running FunSearch experiments."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

from rich.console import Console
from rich.panel import Panel

from funsearch.core.config import Config, ProgramsDatabaseConfig
from funsearch.engine import FunSearchEngine
from funsearch.llm.gemini import GeminiLLM
from funsearch.llm.mock import MockLLM
from funsearch.llm.openai_client import OpenAILLM
from funsearch.problems import PROBLEMS


def _load_dotenv_if_present() -> None:
  """Loads variables from local .env into os.environ if not already set."""
  for env_path in [Path.cwd() / ".env", Path(__file__).resolve().parent.parent / ".env"]:
    if env_path.is_file():
      try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
          line = line.strip()
          if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip("'\"")
            if k and k not in os.environ:
              os.environ[k] = v
      except Exception:
        pass


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
      description="FunSearch: Discover mathematical algorithms & heuristics using LLMs."
  )
  parser.add_argument(
      "--problem",
      type=str,
      default="cap_set",
      help="Target problem (cap_set, bin_packing, admissible_set) or path to custom python spec.",
  )
  parser.add_argument(
      "--model",
      type=str,
      default="gemini-3.7-flash",
      help="LLM model (e.g. gemini-3.7-flash, gemini-3.7-pro, gemini-2.5-flash, gpt-4o, mock).",
  )
  parser.add_argument(
      "--api-key",
      type=str,
      default=None,
      help="LLM API key (if not set via GEMINI_API_KEY / OPENAI_API_KEY).",
  )
  parser.add_argument(
      "--iterations",
      type=int,
      default=50,
      help="Number of iterations to run.",
  )
  parser.add_argument(
      "--samples-per-prompt",
      type=int,
      default=2,
      help="Number of samples to draw per prompt.",
  )
  parser.add_argument(
      "--islands",
      type=int,
      default=10,
      help="Number of evolutionary islands in database.",
  )
  parser.add_argument(
      "--temperature",
      type=float,
      default=0.7,
      help="Sampling temperature for LLM.",
  )
  parser.add_argument(
      "--timeout",
      type=int,
      default=30,
      help="Sandbox execution timeout in seconds per test.",
  )
  parser.add_argument(
      "--output-dir",
      type=str,
      default="outputs",
      help="Directory to save experiment logs and checkpoints.",
  )
  parser.add_argument(
      "--no-live",
      action="store_true",
      help="Disable live Rich dashboard UI.",
  )
  return parser


def main() -> None:
  _load_dotenv_if_present()
  parser = build_parser()
  args = parser.parse_args()
  console = Console()

  # Load Problem Specification
  problem_name = args.problem
  if args.problem in PROBLEMS:
    prob_mod = PROBLEMS[args.problem]
    specification = prob_mod.SPECIFICATION
    inputs = prob_mod.INPUTS
  else:
    spec_path = Path(args.problem)
    if not spec_path.exists():
      console.print(f"[bold red]Error:[/bold red] Problem spec file '{args.problem}' not found.")
      sys.exit(1)
    specification = spec_path.read_text(encoding="utf-8")
    inputs = [1]  # Default input
    problem_name = spec_path.stem

  # Configure Database & Engine
  db_config = ProgramsDatabaseConfig(
      num_islands=args.islands,
      functions_per_prompt=2,
  )
  config = Config(
      programs_database=db_config,
      samples_per_prompt=args.samples_per_prompt,
      sandbox_timeout=args.timeout,
      max_iterations=args.iterations,
      model_name=args.model,
      temperature=args.temperature,
      output_dir=args.output_dir,
  )

  # Initialize LLM Sampler
  model_lower = args.model.lower()
  if "mock" in model_lower:
    llm = MockLLM(samples_per_prompt=args.samples_per_prompt, temperature=args.temperature)
  elif "gemini" in model_lower:
    llm = GeminiLLM(
        model_name=args.model,
        api_key=args.api_key,
        samples_per_prompt=args.samples_per_prompt,
        temperature=args.temperature,
    )
  elif "gpt" in model_lower or "claude" in model_lower or "ollama" in model_lower:
    llm = OpenAILLM(
        model_name=args.model,
        api_key=args.api_key,
        samples_per_prompt=args.samples_per_prompt,
        temperature=args.temperature,
    )
  else:
    # Default to Gemini
    llm = GeminiLLM(
        model_name=args.model,
        api_key=args.api_key,
        samples_per_prompt=args.samples_per_prompt,
        temperature=args.temperature,
    )

  engine = FunSearchEngine(
      specification=specification,
      inputs=inputs,
      config=config,
      llm=llm,
      problem_name=problem_name,
      enable_live_ui=not args.no_live,
  )

  best_program, best_score = engine.run()

  # Final Summary Display
  console.print("\n")
  console.print(
      Panel(
          f"[bold green]Search Complete![/bold green]\n"
          f"Problem: [bold cyan]{problem_name}[/bold cyan]\n"
          f"Best Score: [bold yellow]{best_score:.2f}[/bold yellow]\n"
          f"Discovered Program saved to: [bold white]{engine.logger.best_program_file}[/bold white]",
          title="🎉 FunSearch Results",
          border_style="green",
      )
  )
  if best_program:
    console.print("\n[bold]Best Discovered Function Body:[/bold]")
    console.print(str(best_program))


if __name__ == "__main__":
  main()
