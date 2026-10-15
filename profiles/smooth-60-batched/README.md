# Experimental CPU yield batching profile

Based on smooth-60 with one change: `[perf] hotfunc_yield_every = 16` instead of 1. Graphics, tick-rate patches, and frame limit remain identical for comparison.

The upstream `src/core/hotfunc/hotfunc_yield.h` batches SwitchToThread calls in the hot guest yield override. This may reduce scheduling overhead on multicore PCs, but no gameplay frame-time improvement has been measured yet. It can change thread scheduling and should be checked for audio, loading, and physics regressions.

Close the game and copy these three TOML files beside fable_2.exe to apply. To revert, copy the original profiles/smooth-60 files instead. Keep shader caches between comparison runs. Compare the same route and camera movements after visiting the area once.

For a lightweight main-loop rate log, launch with the process environment variable FABLE2_FPS_METER=1. This reports a five-second average, not individual frame times or displayed FPS; it cannot establish that brief hitches are eliminated.
