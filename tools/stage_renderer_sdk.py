"""Stage matched fork headers/runtime/plugin with an official codegen package.

Usage: python tools/stage_renderer_sdk.py OFFICIAL_SDK SDK_SOURCE BUILD_DIR OUTPUT
       [--configuration Release|Debug]
The native application must be rebuilt against OUTPUT. Codegen continues using
OFFICIAL_SDK/bin/rexglue.exe with its original runtime, not OUTPUT/bin/rexglue.exe.
Only SDK files are copied; game dumps and saves are never packaged.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("official", "source", "build", "output"):
        parser.add_argument(name, type=Path)
    parser.add_argument("--configuration", choices=("Release", "Debug"), default="Release")
    args = parser.parse_args()
    official, source, build, output = (getattr(args, name).resolve()
        for name in ("official", "source", "build", "output"))
    if any(output == path or path.is_relative_to(output) or output.is_relative_to(path)
           for path in (official, source, build)):
        raise SystemExit("Output must be separate from every input tree")
    native = source / "out/win-amd64"
    suffix = "d" if args.configuration == "Debug" else ""
    runtime = f"rexruntime{suffix}"
    plugin = f"rexgpu-xenos{suffix}"
    required = [native / f"{runtime}.dll", native / f"{plugin}.dll",
                native / f"{runtime}.lib", native / f"{plugin}.lib", build / "include/rex/version.h",
                official / "bin/rexglue.exe"]
    for path in required:
        if not path.is_file():
            raise SystemExit(f"Missing build input: {path}")
    shutil.copytree(official, output, dirs_exist_ok=True)
    shutil.copytree(source / "include/rex", output / "include/rex", dirs_exist_ok=True)
    shutil.copy2(build / "include/rex/version.h", output / "include/rex/version.h")
    shutil.copytree(source / "thirdparty/sdl3/include/SDL3", output / "include/SDL3", dirs_exist_ok=True)
    for path in native.glob("*.lib"):
        shutil.copy2(path, output / "lib" / path.name)
    for name in (f"{runtime}.dll", f"{plugin}.dll"):
        shutil.copy2(native / name, output / "bin" / name)
    # Carry the PDBs (when present) so the host build can stage them next to
    # the exe for debugger/profiler symbolization.
    for name in (f"{runtime}.pdb", f"{plugin}.pdb"):
        if (native / name).is_file():
            shutil.copy2(native / name, output / "bin" / name)
    for name in ("rex_app.cpp", "windowed_app_main_sdl.cpp"):
        shutil.copy2(source / "src/ui" / name, output / "share/rexglue" / name)
    revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    provenance = {
        "configuration": args.configuration,
        "sdk_commit": revision,
        "codegen_tool": str(official / "bin/rexglue.exe"),
        "note": "Native headers, integration sources and DLLs must stay matched. Official tool uses its own runtime.",
        "runtime_sha256": hashlib.sha256((native / f"{runtime}.dll").read_bytes()).hexdigest(),
        "plugin_sha256": hashlib.sha256((native / f"{plugin}.dll").read_bytes()).hexdigest(),
    }
    (output / "renderer-sdk-provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print(f"Matched native SDK staged at {output}")
    print(f"Configure host with -DFABLE2_CODEGEN_TOOL={official / 'bin/rexglue.exe'}")


if __name__ == "__main__":
    main()
