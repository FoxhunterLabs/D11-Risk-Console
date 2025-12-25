import random

def _u32(x: int) -> int:
    return x & 0xFFFFFFFF

def tick_rng(seed: int, tick: int, salt: int = 0) -> random.Random:
    mixed = _u32(seed ^ _u32(tick * 0x9E3779B9) ^ _u32(salt * 0x85EBCA6B))
    return random.Random(mixed)
