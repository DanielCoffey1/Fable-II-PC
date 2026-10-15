# Development notes

## Provenance

Upstream: https://github.com/himdo/Fable-2-Recomp
Starting release: 1.5.0
Starting commit: e12f40d7faa30c6c816008135e67fcd94f055824
The upstream README below the personal introduction remains the build reference.

## Local layout

Source checkout: Documents\Fable 2\Fable-II-PC
Playable release: Documents\Fable 2\Recompiled\Fable 2 1.5.0
Keep source and the playable installation separate. This checkout has not been compiled locally yet.

## Building

Follow the upstream toolchain requirements in README.md and build.cmd: LLVM/Clang, Ninja, CMake, compatible MSVC build tools/Windows SDK, and the ReXGlue SDK. The launcher build needs the .NET SDK.

Initialize dependencies with `git submodule update --init --recursive`.
Supply supported `default.xex` and `data/` locally, as documented upstream. They are ignored by Git. Then use `build.cmd -release fable_2` for the native game, or `build.cmd launcher` for the launcher. These commands are documented starting points, not verified local builds.

## Continuing work

1. Establish a reproducible local Release build before changing engine code.
2. Compare the same gameplay route with a warm shader cache and record frame times.
3. Keep both tick-rate patches paired; check cloth physics, audio, and save/load behavior.
4. Track upstream fixes through the `upstream` remote and review changes before merging.
5. Keep future trilogy launcher work separate from each game's porting work.

Do not commit disc images, game assets, extracted executables, saves, credentials, or generated binaries. Keep the upstream license and attribution when sharing code.

## Experimental stutter investigation

A separate `profiles/smooth-60-batched` variant changes only hotfunc_yield_every from 1 to 16. It uses the existing upstream runtime option, without rebuilding engine code. The original smooth-60 profile remains available for rollback. Existing logs do not prove shader compilation is responsible for individual hitches; present-gate suppression counts are not FPS measurements. Validate this variant in gameplay before adopting it as the default.

## Progression hitches and diagnostic correction

The yield-batching experiment did not resolve the reported stutters and the playable installation was returned to the smooth-60 baseline (`hotfunc_yield_every = 1`). The experimental profile is retained for reference only.

The upstream FPS meter contained `if (n == 1 || elapsed >= 5 seconds)` and reset its sample counter inside that block. Consequently every next frame had n == 1 and flushed a log line, contrary to its intended five-second window. Removed that condition and seeded the initial time window before computing elapsed time. This source correction has not been compiled into the installed upstream release. FPS logging is disabled for normal play by launching without FABLE2_FPS_METER.

Upstream docs/RUNTIME_FIXES.md explains that async pipeline waiting can stall the first use of a shader pipeline. Keep that correctness behavior enabled and preserve caches; do not claim that every reported hitch is shader compilation without a correlated trace. Compare a newly visited route with the same route after revisiting or reloading. Repeated warm-route stalls need per-frame CPU/GPU and storage profiling rather than more unmeasured settings changes.
