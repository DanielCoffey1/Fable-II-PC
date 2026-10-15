# Smooth 60 FPS profile

Copy these three TOML files next to a compatible v1.5.0 `fable_2.exe`, backing up any existing files first. Close the game before changing configuration. These are configuration templates only.

- Target: 60 FPS; legacy `guest_vblank_pacing` disabled.
- Both `high_tick_rate` and `higher_hf_tick_rate` enabled together.
- VSync enabled; borderless display; 2560 x 1440 presentation.
- Internal resolution scale 1; upstream texture fixes preserved.

Tested informally on an RTX 5090 / Ryzen 9 9950X3D. Gameplay was reported much smoother; occasional hitches were not measured or diagnosed. Preserve shader caches between sessions. Adjust display size using the launcher for other monitors.
