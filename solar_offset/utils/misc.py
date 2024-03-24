
from collections.abc import Iterable
from math import floor, isclose, log10

# Find the nth percentile by interpolating between the given data points
def calculate_percentile(finite_iter:Iterable[int|float], percentile:float):
    ranked_list = sorted(finite_iter)
    rank_ix = (percentile * (len(ranked_list) + 1)) - 1

    if rank_ix >= len(ranked_list)-1:
        return ranked_list[-1]
    elif rank_ix <= 0:
        return ranked_list[0]
    elif isclose(rank_ix, int(rank_ix)):
        # The rank is a whole number, just return the value
        return ranked_list[rank_ix]
    else:
        # Interpolated between values
        rank_ix_int = int(rank_ix)
        rank_ix_remainder = rank_ix % 1
        r1 = ranked_list[rank_ix_int]
        r2 = ranked_list[rank_ix_int+1]
        return min(r1, r2) + abs( (r2-r1) * rank_ix_remainder )


## Code taken from https://stackoverflow.com/a/3411435
##   Comment authored by user Roy Hyunjin Han (https://stackoverflow.com/users/192092/roy-hyunjin-han)
def round_to_n_sig_figs(num:int|float, significant_figures):
    round_ix = - int( floor(log10(num)) ) + (significant_figures - 1)
    return round(num, round_ix)