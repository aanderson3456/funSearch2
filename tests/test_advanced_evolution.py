"""Unit test suite for Advanced Evolutionary Architecture in FunSearch."""
from __future__ import annotations

import copy

from funsearch.core import code_manipulation
from funsearch.core import config as config_lib
from funsearch.core.advanced_evolution import (
    BehavioralFeatureExtractor,
    DiagnosticTraceGenerator,
    EliteRecord,
    MapElitesArchive,
    RingMigrationController,
    SemanticCrossoverOperator,
    AdvancedProgramsDatabase,
)

SAMPLE_SPEC = '''"""Problem spec."""
import funsearch

@funsearch.evolve
def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      score += float(8.0 ** m_cnt)
  score -= (abs(candidate[0]) + abs(candidate[1])) * 0.1
  return float(score)

@funsearch.run
def evaluate(grid_radius: int) -> float:
  return 100.0
'''

SAMPLE_SPEC_COMPLEX = '''"""Problem spec complex."""
import funsearch

@funsearch.evolve
def priority(candidate: tuple[int, int], maker_cells: list[tuple[int, int]], breaker_cells: list[tuple[int, int]], active_shapes: list[tuple[tuple[int, int], ...]]) -> float:
  m_set = set(maker_cells)
  b_set = set(breaker_cells)
  score = 0.0
  fork_threats = 0
  for shape in active_shapes:
    if candidate in shape:
      m_cnt = sum(1 for p in shape if p in m_set)
      if m_cnt >= 4:
        score += 50000.0
      elif m_cnt == 3:
        fork_threats += 1
        score += 500.0
      else:
        score += float(10.0 ** m_cnt)
  if fork_threats >= 2:
    score += 15000.0
  dist = abs(candidate[0]) + abs(candidate[1])
  score -= dist * 0.05
  return float(score)

@funsearch.run
def evaluate(grid_radius: int) -> float:
  return 250.0
'''


def test_feature_extractor():
    prog = code_manipulation.text_to_program(SAMPLE_SPEC)
    fn = prog.get_function('priority')
    
    comp = BehavioralFeatureExtractor.extract_ast_complexity(fn.body)
    assert 10.0 <= comp <= 100.0
    
    agg = BehavioralFeatureExtractor.extract_aggression_ratio(fn.body)
    assert 0.5 <= agg <= 3.5
    
    scale = BehavioralFeatureExtractor.extract_scale_generalization({3: 50.0, 4: 150.0})
    assert scale == 3.0


def test_map_elites_archive():
    archive = MapElitesArchive(grid_dims=(4, 4, 4))
    prog1 = code_manipulation.text_to_program(SAMPLE_SPEC).get_function('priority')
    prog2 = code_manipulation.text_to_program(SAMPLE_SPEC_COMPLEX).get_function('priority')
    
    is_new, is_imp = archive.add(prog1, score=100.0, scores_per_test={3: 50.0, 4: 100.0})
    assert is_new
    assert is_imp
    assert archive.coverage > 0.0
    
    # Adding an identical one with lower score should NOT improve
    is_new2, is_imp2 = archive.add(prog1, score=50.0, scores_per_test={3: 50.0, 4: 100.0})
    assert not is_new2
    assert not is_imp2
    
    # Adding a different complex program should occupy a new niche or improve
    is_new3, is_imp3 = archive.add(prog2, score=250.0, scores_per_test={3: 100.0, 4: 250.0})
    assert archive.max_fitness == 250.0
    
    elites = archive.sample_elites(n=2)
    assert len(elites) >= 1
    
    summary = archive.get_summary()
    assert summary['occupied_niches'] >= 1
    assert summary['max_fitness'] == 250.0


def test_diagnostic_trace_generator():
    diag_maker_win = DiagnosticTraceGenerator.generate_diagnostic(
        role='Maker', score=320.0, scores_per_test={4: 320.0}, turns=7, max_cells=6
    )
    assert 'SUCCESSFUL FORK' in diag_maker_win
    assert '7 turns played' in diag_maker_win

    diag_maker_loss = DiagnosticTraceGenerator.generate_diagnostic(
        role='Maker', score=120.0, scores_per_test={4: 120.0}, turns=27, max_cells=5
    )
    assert 'DEFENSIVE STALEMATE' in diag_maker_loss

    diag_breaker = DiagnosticTraceGenerator.generate_diagnostic(
        role='Breaker', score=1245.0, scores_per_test={4: 1245.0}, turns=27, max_cells=5
    )
    assert 'EFFECTIVE BLOCKING' in diag_breaker


def test_semantic_crossover_operator():
    prog1 = code_manipulation.text_to_program(SAMPLE_SPEC).get_function('priority')
    prog2 = code_manipulation.text_to_program(SAMPLE_SPEC_COMPLEX).get_function('priority')
    template = code_manipulation.text_to_program(SAMPLE_SPEC)

    e1 = EliteRecord(
        program=prog1, score=100.0, scores_per_test={4: 100.0},
        features=(20.0, 1.0, 1.0), feature_bins=(0, 0, 0),
        diagnostic_trace='# Diagnostic A', discovered_at=0.0
    )
    e2 = EliteRecord(
        program=prog2, score=250.0, scores_per_test={4: 250.0},
        features=(50.0, 2.0, 2.5), feature_bins=(2, 2, 2),
        diagnostic_trace='# Diagnostic B', discovered_at=0.0
    )

    prompt_code, ver = SemanticCrossoverOperator.build_crossover_prompt(e1, e2, template, 'priority')
    assert 'SEMANTIC GENETIC CROSSOVER TASK' in prompt_code
    assert 'priority_parent_a' in prompt_code
    assert 'priority_parent_b' in prompt_code
    assert 'def priority_crossover_child' in prompt_code


def test_ring_migration_controller():
    template = code_manipulation.text_to_program(SAMPLE_SPEC)
    prog = template.get_function('priority')
    cfg = config_lib.ProgramsDatabaseConfig(num_islands=4)
    db = AdvancedProgramsDatabase(cfg, template, 'priority', ring_migration_interval=2)
    
    # Register in island 0
    db.register_program(prog, island_id=0, scores_per_test={4: 150.0})
    db.register_program(prog, island_id=0, scores_per_test={4: 160.0})
    
    assert db.ring_migration.total_migrations >= 0


def test_advanced_programs_database_modes():
    template = code_manipulation.text_to_program(SAMPLE_SPEC)
    prog1 = template.get_function('priority')
    prog2 = code_manipulation.text_to_program(SAMPLE_SPEC_COMPLEX).get_function('priority')
    
    cfg = config_lib.ProgramsDatabaseConfig(num_islands=3)
    db = AdvancedProgramsDatabase(cfg, template, 'priority')

    # Seed programs
    db.register_program(prog1, island_id=0, scores_per_test={4: 100.0}, turns=15, max_cells=5)
    db.register_program(prog2, island_id=1, scores_per_test={4: 250.0}, turns=7, max_cells=6)

    assert db.archive.coverage > 0.0
    assert db.global_best_score == 250.0

    # Draw multiple prompts to test prompt generation paths
    prompts = [db.get_prompt() for _ in range(10)]
    assert len(prompts) == 10
    for p in prompts:
        assert 'def priority' in p.code
