import subprocess
import os

def generate_fingerprint(file_path):
    result = subprocess.run(
        ["fpcalc", file_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"[fpcalc ERROR] {file_path}")
        print(result.stderr.strip())
        return None, None

    fingerprint = None
    duration = None

    for line in result.stdout.splitlines():
        if line.startswith("FINGERPRINT="):
            fingerprint = line.split("=", 1)[1]
        elif line.startswith("DURATION="):
            duration = int(float(line.split("=", 1)[1]))

    if not fingerprint or not duration:
        print(f"[fpcalc FAILED] No data for: {file_path}")
        return None, None

    return fingerprint, duration