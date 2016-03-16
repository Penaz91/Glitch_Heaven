import pstats
pstats.Stats('binary_profile').strip_dirs().sort_stats("cumulative").print_stats()