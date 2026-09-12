"""Evolved 13x13 Breakthrough Breaker Champion (Denials: 2/3)"""
from typing import List, Tuple

def breaker_priority(candidate: Tuple[int, int], maker_cells: List[Tuple[int, int]], breaker_cells: List[Tuple[int, int]], active_shapes: List[List[Tuple[int, int]]]) -> float:
    m_set = set(maker_cells)
    for s in active_shapes:
        if candidate in s and sum(1 for p in s if p in m_set) == 5:
            return 1e16

    score = 0.0
    threat_4 = 0
    threat_3 = 0
    overlap = 0
    weights = {0: 1.293, 1: 3.387, 2: 36.116, 3: 1882.153, 4: 110388.888}
    for s in active_shapes:
        if candidate in s:
            overlap += 1
            m_cnt = sum(1 for p in s if p in m_set)
            score += weights.get(m_cnt, 10.0 ** (m_cnt + 1))
            if m_cnt == 4:
                threat_4 += 1
            elif m_cnt == 3:
                threat_3 += 1

    if threat_4 >= 2:
        score += 91621970.3 * (threat_4 ** 2.0)
    elif threat_4 == 1:
        score += 916219.7

    if threat_3 >= 2:
        score += 326293.0 * (threat_3 ** 1.5)

    if threat_4 == 0:
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                if ((candidate[0] + dx, candidate[1]) in m_set and 
                    (candidate[0], candidate[1] + dy) in m_set and 
                    (candidate[0] + dx, candidate[1] + dy) in m_set):
                    score += 916698.4
                    break

    if (((candidate[0] - 1, candidate[1]) in m_set and (candidate[0] - 2, candidate[1]) in m_set) or
        ((candidate[0] + 1, candidate[1]) in m_set and (candidate[0] + 2, candidate[1]) in m_set) or
        ((candidate[0], candidate[1] - 1) in m_set and (candidate[0], candidate[1] - 2) in m_set) or
        ((candidate[0], candidate[1] + 1) in m_set and (candidate[0], candidate[1] + 2) in m_set)):
        score += 75968.8

    if maker_cells:
        min_dist = min(abs(candidate[0] - m[0]) + abs(candidate[1] - m[1]) for m in maker_cells)
        if min_dist <= 1:
            score += 7812.8
        elif min_dist == 2:
            score += 3368.9
        elif min_dist >= 5:
            score -= 11520.3

    score += (overlap ** 1.31) * 6.93
    return float(score)
