def distance_min_2d(pos_1: tuple[int, int], pos_2: tuple[int, int]) -> int:
    return min(abs(pos_1[0] - pos_2[0]), abs(pos_1[1] - pos_2[1]))
