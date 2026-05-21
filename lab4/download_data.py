import argparse
import gzip
import os
import re
import shutil

import requests

INDEX_URL = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
DEFAULT_OUTPUT = os.path.join(os.path.dirname(__file__), "data", "storm_events.csv")


def get_details_url(year: int) -> str:
    """Fetch the directory index and find the latest details file for the given year."""
    print(f"[INFO] Fetching file index from {INDEX_URL} ...")
    resp = requests.get(INDEX_URL, timeout=120)
    resp.raise_for_status()

    pattern = rf"StormEvents_details-ftp_v1\.0_d{year}_c\d+\.csv\.gz"
    matches = re.findall(pattern, resp.text)
    if not matches:
        raise ValueError(f"No storm events details file found for year {year}.")

    filename = sorted(matches)[-1]   # latest update version
    url = INDEX_URL + filename
    print(f"[INFO] Found: {filename}")
    return url


def download(url: str, output_path: str) -> None:
    gz_path = output_path + ".gz"

    print(f"[INFO] Downloading {url} ...")
    with requests.get(url, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        total = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        with open(gz_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    pct = downloaded * 100 // total
                    print(f"\r  {pct}% ({downloaded}/{total} bytes)", end="", flush=True)
    print()

    print(f"[INFO] Extracting to {output_path} ...")
    with gzip.open(gz_path, "rb") as gz_in, open(output_path, "wb") as csv_out:
        shutil.copyfileobj(gz_in, csv_out)
    os.remove(gz_path)

    size_kb = os.path.getsize(output_path) // 1024
    print(f"[INFO] Done. Saved {output_path} ({size_kb} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download NCDC Storm Events dataset")
    parser.add_argument("--year", type=int, default=2025, help="Dataset year (default: 2025)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output CSV path")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    url = get_details_url(args.year)
    download(url, args.output)


if __name__ == "__main__":
    main()
