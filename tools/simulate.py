"""Run the self-checking FIFO test with a separately installed Icarus Verilog."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(command, timeout=60, echo=True):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                            errors="replace", timeout=timeout)
    output = result.stdout + result.stderr
    if echo:
        print(output, end="")
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {command[0]}")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iverilog", default="iverilog")
    parser.add_argument("--vvp", default="vvp")
    args = parser.parse_args()
    ivl, vvp = shutil.which(args.iverilog), shutil.which(args.vvp)
    if not ivl or not vvp:
        parser.error("Install Icarus Verilog and vvp or provide their executable paths.")
    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    binary = build / "fifo.vvp"
    try:
        version = run([ivl, "-V"], echo=False)
        print(version.splitlines()[0])
        run([ivl, "-g2012", "-s", "tb_fifo", "-o", str(binary),
             "examples/rtl/sync_fifo.sv", "examples/tb/tb_fifo.sv"])
        output = run([vvp, str(binary)])
        if "PASS ALL FIFO CASES" not in output or output.count("PASS FIFO W=") != 3:
            raise RuntimeError("Simulator did not report all expected successful cases")
        (build / "simulation.json").write_text(json.dumps({
            "tool_version": version.splitlines()[0], "passed": True,
            "output": output,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 0
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        (build / "simulation.json").write_text(json.dumps({
            "passed": False, "error": str(exc)
        }, indent=2) + "\n", encoding="utf-8")
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
