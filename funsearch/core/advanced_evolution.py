"""Advanced Evolutionary Architecture for FunSearch.

Implements next-generation evolutionary operators:
1. MAP-Elites Quality-Diversity Archive (behavioral phenotypic niches).
2. Diagnostic Trace-Guided Mutation ("Evolution of Thought").
3. Semantic Multi-Parent Crossover.
4. Continuous Ring-Topology Island Migration.
5. AdvancedProgramsDatabase coordinating Quality-Diversity and Islands.
"""
from __future__ import annotations

import ast
import copy
import dataclasses
import json
import math
import random
import re
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Callable

import numpy as np

from funsearch.core import code_manipulation
from funsearch.core import config as config_lib
from funsearch.core.programs_database import (
    Cluster,
    Island,
    ProgramsDatabase,
    Prompt,
    ScoresPerTest,
    Signature,
    _get_signature,
    _reduce_score,
    _softmax,
)


# ---------------------------------------------------------------------------
# 1. Phenotypic Feature Extractor
# ---------------------------------------------------------------------------
class BehavioralFeatureExtractor:
    """Extracts behavioral and structural phenotypic dimensions from code and scores."""

    @staticmethod
    def extract_ast_complexity(body_code: str) -> float:
        """Measures AST complexity (normalized node count, branching, loops)."""
        try:
            tree = ast.parse("def temp():\n" + body_code)
            node_count = sum(1 for _ in ast.walk(tree))
            branch_count = sum(
                1 for n in ast.walk(tree) if isinstance(n, (ast.If, ast.For, ast.While, ast.comprehension))
            )
            complexity = float(node_count + 3 * branch_count)
            return min(max(complexity, 10.0), 100.0)
        except Exception:
            return 30.0

    @staticmethod
    def extract_aggression_ratio(body_code: str) -> float:
        """Estimates offensive aggression vs defensive weighting from constants and heuristics."""
        try:
            weight_pattern = re.findall(r'(\d+\.?\d*)\s*\*\*\s*m_cnt', body_code)
            base = float(weight_pattern[0]) if weight_pattern else 8.0
            has_fork = (
                1.5
                if any(kw in body_code.lower() for kw in ["fork", "high_threat", "overlap", "active_count"])
                else 1.0
            )
            aggression = math.log10(max(base, 2.0)) * has_fork
            return float(min(max(aggression, 0.5), 3.5))
        except Exception:
            return 1.5

    @staticmethod
    def extract_scale_generalization(scores_per_test: ScoresPerTest) -> float:
        """Measures performance ratio between hardest scale and base scale."""
        if not scores_per_test or len(scores_per_test) < 2:
            return 1.0
        keys = sorted(scores_per_test.keys())
        base_score = max(scores_per_test[keys[0]], 1.0)
        hard_score = max(scores_per_test[keys[-1]], 1.0)
        ratio = float(hard_score / base_score)
        return float(min(max(ratio, 0.1), 10.0))


# ---------------------------------------------------------------------------
# 2. MAP-Elites Quality-Diversity Archive
# ---------------------------------------------------------------------------
@dataclasses.dataclass
class EliteRecord:
    """An individual stored within a MAP-Elites behavioral niche cell."""
    program: code_manipulation.Function
    score: float
    scores_per_test: ScoresPerTest
    features: tuple[float, float, float]
    feature_bins: tuple[int, int, int]
    diagnostic_trace: str
    discovered_at: float
    iteration: int = 0


class MapElitesArchive:
    """Multi-dimensional Quality-Diversity Archive for code heuristics."""

    def __init__(
        self,
        grid_dims: tuple[int, int, int] = (5, 5, 5),
        feature_ranges: tuple[tuple[float, float], tuple[float, float], tuple[float, float]] = (
            (10.0, 80.0),   # AST Complexity
            (0.5, 3.0),     # Aggression Ratio
            (0.5, 4.0),     # Scale Generalization
        ),
    ):
        self.grid_dims = grid_dims
        self.feature_ranges = feature_ranges
        self.cells: dict[tuple[int, int, int], EliteRecord] = {}
        self.total_evaluations: int = 0
        self.improvements_count: int = 0

    def get_bin_index(self, val: float, dim: int) -> int:
        low, high = self.feature_ranges[dim]
        clamped = max(low, min(high, val))
        norm = (clamped - low) / (high - low + 1e-9)
        idx = int(norm * self.grid_dims[dim])
        return min(idx, self.grid_dims[dim] - 1)

    def compute_bins(self, features: tuple[float, float, float]) -> tuple[int, int, int]:
        return (
            self.get_bin_index(features[0], 0),
            self.get_bin_index(features[1], 1),
            self.get_bin_index(features[2], 2),
        )

    def add(
        self,
        program: code_manipulation.Function,
        score: float,
        scores_per_test: ScoresPerTest,
        diagnostic_trace: str = "",
        iteration: int = 0,
    ) -> tuple[bool, bool]:
        """Adds a candidate program to the MAP-Elites grid."""
        self.total_evaluations += 1
        f1 = BehavioralFeatureExtractor.extract_ast_complexity(program.body)
        f2 = BehavioralFeatureExtractor.extract_aggression_ratio(program.body)
        f3 = BehavioralFeatureExtractor.extract_scale_generalization(scores_per_test)
        features = (f1, f2, f3)
        bins = self.compute_bins(features)

        is_new_niche = bins not in self.cells
        is_improvement = False

        if is_new_niche or score > self.cells[bins].score:
            self.cells[bins] = EliteRecord(
                program=program,
                score=score,
                scores_per_test=scores_per_test,
                features=features,
                feature_bins=bins,
                diagnostic_trace=diagnostic_trace,
                discovered_at=time.time(),
                iteration=iteration,
            )
            self.improvements_count += 1
            is_improvement = True

        return is_new_niche, is_improvement

    def sample_elites(self, n: int = 2) -> list[EliteRecord]:
        """Samples n distinct elites from occupied niches uniformly at random."""
        if not self.cells:
            return []
        keys = list(self.cells.keys())
        chosen_keys = np.random.choice(len(keys), size=min(n, len(keys)), replace=False)
        return [self.cells[keys[k]] for k in chosen_keys]

    @property
    def coverage(self) -> float:
        """Percentage of behavioral grid niches occupied."""
        total_niches = self.grid_dims[0] * self.grid_dims[1] * self.grid_dims[2]
        return len(self.cells) / total_niches

    @property
    def max_fitness(self) -> float:
        return max((e.score for e in self.cells.values()), default=-float("inf"))

    def get_summary(self) -> dict[str, Any]:
        return {
            "occupied_niches": len(self.cells),
            "total_niches": self.grid_dims[0] * self.grid_dims[1] * self.grid_dims[2],
            "coverage_pct": round(self.coverage * 100.0, 2),
            "max_fitness": self.max_fitness,
            "total_evaluations": self.total_evaluations,
            "improvements_count": self.improvements_count,
        }


# ---------------------------------------------------------------------------
# 3. Diagnostic Trace Generator ("Evolution of Thought")
# ---------------------------------------------------------------------------
class DiagnosticTraceGenerator:
    """Synthesizes actionable game-physics feedback from evaluation execution traces."""

    @staticmethod
    def generate_diagnostic(
        role: str,
        score: float,
        scores_per_test: ScoresPerTest,
        turns: int | None = None,
        max_cells: int | None = None,
        opponent_name: str = "Ensemble",
    ) -> str:
        """Produces structured diagnostic guidance tailored for LLM prompt context."""
        lines = ["# --- Diagnostic Telemetry & Turn Trace ---"]
        if turns is not None:
            lines.append(f"# Game Resolution: {turns} turns played against {opponent_name}.")
        if max_cells is not None:
            lines.append(f"# Peak Shape Alignment: {max_cells}/6 cells placed.")

        if role.lower() == "maker":
            if score >= 300.0:
                lines.append("# Tactical Verdict: SUCCESSFUL FORK. Discovered unblockable geometric split.")
                lines.append("# Next Objective: Compress moves-to-win while maintaining dual-threat branches.")
            elif max_cells is not None and max_cells == 5:
                lines.append("# Tactical Verdict: DEFENSIVE STALEMATE. Reached 5 cells but was promptly blocked.")
                lines.append("# Recommendation: Transition from single-line extension to multi-threat branching (C4 >= 2).")
            else:
                lines.append("# Tactical Verdict: EARLY CONTAINMENT. Breaker severed critical polyomino orientations.")
                lines.append("# Recommendation: Prioritize cells with high active_count and spatial centrality.")
        else:  # Breaker
            if score >= 1000.0:
                lines.append("# Tactical Verdict: EFFECTIVE BLOCKING. Successfully stonewalled Maker attacks.")
                lines.append("# Next Objective: Identify and neutralize fork candidates before Maker reaches 4 cells.")
            else:
                lines.append("# Tactical Verdict: PENETRATION LEAK. Maker completed an unblocked 6-cell Snakey.")
                lines.append("# Recommendation: Increase weight on overlap cells and 3-threat anti-fork defense.")

        lines.append("# ----------------------------------------")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# 4. Semantic Multi-Parent Crossover Operator
# ---------------------------------------------------------------------------
class SemanticCrossoverOperator:
    """Constructs recombination prompts blending complementary traits of two distinct parents."""

    @staticmethod
    def build_crossover_prompt(
        parent_a: EliteRecord,
        parent_b: EliteRecord,
        template: code_manipulation.Program,
        function_to_evolve: str,
    ) -> tuple[str, int]:
        """Builds a crossover prompt instructing the LLM to synthesize Parent A and Parent B."""
        prompt_prog = copy.deepcopy(template)
        target_fn = prompt_prog.get_function(function_to_evolve)
        fn_idx = prompt_prog.find_function_index(function_to_evolve)

        # Build versioned functions for Parent A and Parent B
        v0 = copy.deepcopy(parent_a.program)
        v0.name = f"{function_to_evolve}_parent_a"
        v1 = copy.deepcopy(parent_b.program)
        v1.name = f"{function_to_evolve}_parent_b"

        # Synthesis child target
        target = copy.deepcopy(target_fn)
        target.name = f"{function_to_evolve}_crossover_child"
        target.body = ""

        # Diagnostic header
        commentary = (
            f"# ==========================================================================\n"
            f"# SEMANTIC GENETIC CROSSOVER TASK\n"
            f"# Parent A (Fitness: {parent_a.score:.2f}, Niche: {parent_a.feature_bins})\n"
            f"{parent_a.diagnostic_trace}\n"
            f"# Parent B (Fitness: {parent_b.score:.2f}, Niche: {parent_b.feature_bins})\n"
            f"{parent_b.diagnostic_trace}\n"
            f"# INSTRUCTION: Synthesize Parent A's high-threat logic with Parent B's spatial efficiency.\n"
            f"# Do not blindly copy; produce an integrated child combining both advantages.\n"
            f"# =========================================================================="
        )

        prompt_prog.functions = (
            prompt_prog.functions[:fn_idx]
            + [v0, v1, target]
            + prompt_prog.functions[fn_idx + 1 :]
        )

        prompt_str = str(prompt_prog)
        target_header = f"def {function_to_evolve}_crossover_child"
        cutoff = prompt_str.find(target_header)
        if cutoff != -1:
            end_of_header = prompt_str.find(":\n", cutoff)
            if end_of_header != -1:
                prompt_str = prompt_str[: end_of_header + 2]

        full_prompt = commentary + "\n\n" + prompt_str
        return full_prompt, 2


# ---------------------------------------------------------------------------
# 5. Continuous Ring-Topology Migration Controller
# ---------------------------------------------------------------------------
class RingMigrationController:
    """Maintains continuous, directed gene flow between islands in a ring topology."""

    def __init__(self, num_islands: int, migration_interval: int = 20):
        self.num_islands = num_islands
        self.migration_interval = migration_interval
        self.evaluations_since_migration: int = 0
        self.total_migrations: int = 0
        self.migration_log: list[dict[str, Any]] = []

    def should_migrate(self) -> bool:
        return self.evaluations_since_migration >= self.migration_interval

    def execute_ring_migration(
        self,
        islands: list[Island],
        best_program_per_island: list[code_manipulation.Function | None],
        best_score_per_island: list[float],
        best_scores_per_test_per_island: list[ScoresPerTest | None],
    ) -> list[dict[str, Any]]:
        """Migrates elite champions along a directed ring: Island i -> Island (i+1) % K."""
        events = []
        n = len(islands)
        if n <= 1:
            return events

        for src_idx in range(n):
            dst_idx = (src_idx + 1) % n
            donor_prog = best_program_per_island[src_idx]
            donor_score = best_score_per_island[src_idx]
            donor_scores_per_test = best_scores_per_test_per_island[src_idx]

            if donor_prog and donor_scores_per_test:
                islands[dst_idx].register_program(donor_prog, donor_scores_per_test)
                ev = {
                    "timestamp": time.time(),
                    "src_island": src_idx,
                    "dst_island": dst_idx,
                    "migrant_score": donor_score,
                }
                events.append(ev)
                self.migration_log.append(ev)

        self.evaluations_since_migration = 0
        self.total_migrations += len(events)
        return events


# ---------------------------------------------------------------------------
# 6. Advanced Programs Database
# ---------------------------------------------------------------------------
class AdvancedProgramsDatabase(ProgramsDatabase):
    """Drop-in enhanced ProgramsDatabase fusing MAP-Elites, Ring Migration, & Diagnostics."""

    def __init__(
        self,
        config: config_lib.ProgramsDatabaseConfig,
        template: code_manipulation.Program,
        function_to_evolve: str,
        map_elites_dims: tuple[int, int, int] = (5, 5, 5),
        ring_migration_interval: int = 25,
        crossover_rate: float = 0.20,
        map_elites_rate: float = 0.25,
    ):
        super().__init__(config, template, function_to_evolve)
        self.archive = MapElitesArchive(grid_dims=map_elites_dims)
        self.ring_migration = RingMigrationController(
            num_islands=config.num_islands, migration_interval=ring_migration_interval
        )
        self.crossover_rate = crossover_rate
        self.map_elites_rate = map_elites_rate
        self.latest_diagnostics: dict[str, str] = {}

    def register_program(
        self,
        program: code_manipulation.Function,
        island_id: int | None,
        scores_per_test: ScoresPerTest,
        turns: int | None = None,
        max_cells: int | None = None,
    ) -> bool:
        """Registers a program into Islands, MAP-Elites archive, and triggers Ring Migration."""
        score = _reduce_score(scores_per_test)
        role = "Maker" if "breaker" not in self._function_to_evolve.lower() else "Breaker"
        diag = DiagnosticTraceGenerator.generate_diagnostic(
            role=role,
            score=score,
            scores_per_test=scores_per_test,
            turns=turns,
            max_cells=max_cells,
        )

        # 1. Add to MAP-Elites Archive
        is_new_niche, is_improvement = self.archive.add(
            program=program,
            score=score,
            scores_per_test=scores_per_test,
            diagnostic_trace=diag,
            iteration=self._total_programs_registered,
        )

        # 2. Register into Island(s)
        is_new_global_best = super().register_program(program, island_id, scores_per_test)

        # 3. Continuous Ring Migration check
        self.ring_migration.evaluations_since_migration += 1
        if self.ring_migration.should_migrate():
            self.ring_migration.execute_ring_migration(
                self._islands,
                self._best_program_per_island,
                self._best_score_per_island,
                self._best_scores_per_test_per_island,
            )

        return is_new_global_best

    def get_prompt(self) -> Prompt:
        """Tri-modal sampling: Island Exploitation (55%), MAP-Elites Exploration (25%), Crossover (20%)."""
        mode = np.random.choice(["island", "map_elites", "crossover"], p=[0.55, 0.25, 0.20])

        # A. Semantic Crossover Mode
        if mode == "crossover" and len(self.archive.cells) >= 2:
            parents = self.archive.sample_elites(n=2)
            if len(parents) == 2:
                prompt_code, ver = SemanticCrossoverOperator.build_crossover_prompt(
                    parents[0], parents[1], self._template, self._function_to_evolve
                )
                return Prompt(code=prompt_code, version_generated=ver, island_id=-1)

        # B. MAP-Elites Exploration Mode
        if mode == "map_elites" and len(self.archive.cells) >= 1:
            elites = self.archive.sample_elites(n=min(self._config.functions_per_prompt, len(self.archive.cells)))
            if elites:
                # Build prompt from diverse niche elites with diagnostics
                programs = [e.program for e in elites]
                diag_header = "\n".join(e.diagnostic_trace for e in elites)
                base_prompt, ver = self._islands[0]._build_prompt(programs, len(programs)), len(programs)
                full_code = diag_header + "\n\n" + base_prompt
                return Prompt(code=full_code, version_generated=ver, island_id=-2)

        # C. Default Island Softmax Exploitation
        prompt = super().get_prompt()
        # Prepend latest diagnostic if available
        if self.archive.cells:
            top_elite = max(self.archive.cells.values(), key=lambda e: e.score)
            enriched_code = top_elite.diagnostic_trace + "\n\n" + prompt.code
            return Prompt(code=enriched_code, version_generated=prompt.version_generated, island_id=prompt.island_id)

        return prompt
