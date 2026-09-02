"""Rich interactive console dashboard for real-time FunSearch monitoring."""
from __future__ import annotations

import collections
import datetime
import time
from typing import Any

from rich.console import Console, Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from funsearch.core.programs_database import ProgramsDatabase


class LiveDashboard:
  """Renders a real-time Rich terminal UI showing evolutionary search progress."""

  def __init__(
      self,
      problem_name: str,
      model_name: str,
      database: ProgramsDatabase,
      max_iterations: int | None = None,
  ) -> None:
    self.problem_name = problem_name
    self.model_name = model_name
    self.database = database
    self.max_iterations = max_iterations

    self.console = Console()
    self.start_time = time.time()
    self.iteration = 0
    self.total_evaluations = 0
    self.valid_evaluations = 0
    self.syntax_errors = 0
    self.exec_errors = 0

    self.event_log: collections.deque[tuple[str, str, str]] = collections.deque(maxlen=6)
    self.score_history: list[tuple[float, float]] = []  # (timestamp, score)
    self._live: Live | None = None

  def start(self) -> None:
    """Starts the rich Live context."""
    self.start_time = time.time()
    self._live = Live(
        self.render(),
        console=self.console,
        refresh_per_second=4,
        transient=False,
    )
    self._live.start()

  def stop(self) -> None:
    """Stops the rich Live context and prints summary."""
    if self._live:
      self._live.update(self.render(), refresh=True)
      self._live.stop()
      self._live = None

  def log_event(self, text: str, style: str = "white", emoji: str = "ℹ️") -> None:
    """Appends an event to the recent activity log."""
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    self.event_log.append((now_str, f"{emoji} {text}", style))

  def on_evaluation(self, event: dict[str, Any]) -> None:
    """Callback triggered on each evaluation."""
    self.total_evaluations += 1
    status = event.get("status")

    if status == "success":
      self.valid_evaluations += 1
      score = event.get("score")
      is_new_best = event.get("is_new_best", False)
      island_id = event.get("island_id")

      if score is not None:
        self.score_history.append((time.time() - self.start_time, score))

      if is_new_best:
        self.log_event(
            f"NEW GLOBAL RECORD: score = {score:.2f} (Island {island_id})",
            style="bold green",
            emoji="🌟",
        )
      else:
        self.log_event(
            f"Program evaluated: score = {score:.2f} (Island {island_id})",
            style="cyan",
            emoji="✓",
        )
    elif status == "syntax_error":
      self.syntax_errors += 1
      self.log_event("Syntax parsing error in candidate", style="dim red", emoji="✗")
    elif status == "exec_error":
      self.exec_errors += 1
      self.log_event("Execution / runtime error in candidate", style="yellow", emoji="⚠️")

    self.update()

  def step(self, iteration: int) -> None:
    """Updates the current iteration count and refreshes."""
    self.iteration = iteration
    self.update()

  def update(self) -> None:
    """Refreshes the live display."""
    if self._live:
      self._live.update(self.render())

  def _build_header(self) -> Panel:
    elapsed = time.time() - self.start_time
    mins, secs = divmod(int(elapsed), 60)
    hours, mins = divmod(mins, 60)
    time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"

    rate = self.total_evaluations / max(elapsed, 0.001)
    iter_str = (
        f"{self.iteration}/{self.max_iterations}"
        if self.max_iterations
        else f"{self.iteration}"
    )

    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="center", ratio=1)
    grid.add_column(justify="right", ratio=1)

    grid.add_row(
        Text.from_markup(f"[bold cyan]FunSearch[/bold cyan] 🧬 [bold white]{self.problem_name}[/bold white]"),
        Text.from_markup(f"Model: [bold magenta]{self.model_name}[/bold magenta] | Time: [bold yellow]{time_str}[/bold yellow]"),
        Text.from_markup(f"Iter: [bold green]{iter_str}[/bold green] | Speed: [bold blue]{rate:.2f} eval/s[/bold blue]"),
    )
    return Panel(grid, style="bold blue", padding=(0, 1))

  def _build_islands_table(self) -> Table:
    table = Table(title="🏝️ Islands Population", expand=True, show_edge=True, header_style="bold magenta")
    table.add_column("Island", justify="center", style="cyan", width=6)
    table.add_column("Programs", justify="right", style="white", width=9)
    table.add_column("Clusters", justify="right", style="blue", width=9)
    table.add_column("Temp", justify="right", style="yellow", width=7)
    table.add_column("Best Score", justify="right", style="bold green")

    for i, island in enumerate(self.database.islands):
      best_score = self.database.best_score_per_island[i]
      score_str = f"{best_score:.2f}" if best_score != -float("inf") else "—"
      is_global_best = (best_score == self.database.global_best_score and best_score != -float("inf"))

      row_style = "bold white on dark_green" if is_global_best else None
      table.add_row(
          f"#{i}",
          str(island.num_programs),
          str(island.num_clusters),
          f"{island.temperature:.3f}",
          score_str,
          style=row_style,
      )
    return table

  def _build_best_program_panel(self) -> Panel:
    best_prog = self.database.global_best_program
    best_score = self.database.global_best_score

    if best_prog and best_score != -float("inf"):
      title = f"🏆 Global Best Heuristic (Score: {best_score:.2f})"
      code_snippet = str(best_prog).strip()
      # If snippet is very long, truncate lines for display
      lines = code_snippet.splitlines()
      if len(lines) > 16:
        code_snippet = "\n".join(lines[:14] + ["  # ... (truncated for display)"] + lines[-2:])
      syntax = Syntax(code_snippet, "python", theme="monokai", line_numbers=True)
      return Panel(syntax, title=title, border_style="bold green", expand=True)
    else:
      return Panel(
          Text("No successful program evaluated yet...\nWaiting for first candidate.", justify="center", style="dim italic"),
          title="🏆 Global Best Heuristic",
          border_style="dim",
          expand=True,
      )

  def _build_activity_log(self) -> Panel:
    log_text = Text()
    if not self.event_log:
      log_text.append("Initializing search pipeline...", style="dim")
    else:
      for ts, msg, style in self.event_log:
        log_text.append(f"[{ts}] ", style="dim")
        log_text.append(f"{msg}\n", style=style)

    valid_rate = (self.valid_evaluations / max(self.total_evaluations, 1)) * 100
    footer = f"Total Evals: {self.total_evaluations} | Valid: {self.valid_evaluations} ({valid_rate:.1f}%) | Syntax Err: {self.syntax_errors} | Runtime Err: {self.exec_errors}"
    return Panel(log_text, title=f"⚡ Live Event Feed  ({footer})", border_style="cyan", height=8)

  def render(self) -> Layout:
    """Constructs the full UI layout."""
    layout = Layout()
    layout.split_column(
        Layout(self._build_header(), size=3),
        Layout(name="middle", ratio=1),
        Layout(self._build_activity_log(), size=8),
    )

    layout["middle"].split_row(
        Layout(self._build_islands_table(), ratio=1),
        Layout(self._build_best_program_panel(), ratio=2),
    )
    return layout
