
from collections.abc import Iterable
from math import isclose

# Find the nth percentile by interpolating between the given data points
def calculate_percentile(finite_iter:Iterable[int|float], percentile:float):
    ranked_list = sorted(finite_iter)
    rank_ix = (percentile * (len(ranked_list) + 1)) - 1

    if isclose(rank_ix, int(rank_ix)):
        # The rank is a whole number, just return the value
        return ranked_list[rank_ix]
    else:
        # Interpolated between values
        rank_ix_int = int(rank_ix)
        rank_ix_remainder = rank_ix % 1
        r1 = ranked_list[rank_ix_int]
        r2 = ranked_list[rank_ix_int+1]
        return min(r1, r2) + abs( (r2-r1) * rank_ix_remainder )