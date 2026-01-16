import os
import subprocess
import requests

def get_fingerprint(file_path):
    """Run fpcalc and extract fingerprint + duration"""
    result = subprocess.run(
        ["fpcalc", file_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"fpcalc error: {result.stderr}")

    lines = result.stdout.splitlines()

    duration = None
    fingerprint = None

    for line in lines:
        if line.startswith("DURATION="):
            duration = line.split("=")[1]
        elif line.startswith("FINGERPRINT="):
            fingerprint = line.split("=")[1]

    if not duration or not fingerprint:
        raise Exception("Could not parse fpcalc output")

    return duration, fingerprint


def lookup_song(file_path):
    """Send fingerprint to AcoustID server"""
    api_key = os.getenv("ACOUSTID_API_KEY")

    if not api_key:
        raise Exception("ACOUSTID_API_KEY not set in environment!")

    duration, fingerprint = get_fingerprint(file_path)

    url = "https://api.acoustid.org/v2/lookup"

    params = {
        "client": api_key,
        "meta": "recordings+releasegroups+compress",
        "duration": duration,
        "fingerprint": fingerprint
    }

    response = requests.post(url, data=params)
    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    file_path = r"D:\sou.mp3"
    result = lookup_song(file_path)
    print(result)
