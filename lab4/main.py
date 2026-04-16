import argparse
import os
import yaml

from app.reader import read_csv
from app.factory import create_strategy


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main() -> None:
    parser = argparse.ArgumentParser(description="Storm Events data pipeline (Strategy pattern)")
    parser.add_argument(
        "--config",
        default=os.path.join(os.path.dirname(__file__), "config/app.yml"),
        help="Path to YAML config file",
    )
    args = parser.parse_args()

    config = load_config(args.config)

    file_path = config["data"]["file_path"]
    max_rows = config["data"].get("max_rows")

    if not os.path.exists(file_path):
        print(f"[ERROR] Data file not found: '{file_path}'")
        print("Run 'python download_data.py' first to download the dataset.")
        return

    strategy = create_strategy(config)
    strategy_name = config["output"]["strategy"]
    print(f"[INFO] Using output strategy: {strategy_name}")
    print(f"[INFO] Reading from: {file_path}" + (f" (max {max_rows} rows)" if max_rows else ""))

    count = 0
    try:
        for row in read_csv(file_path, max_rows=max_rows):
            strategy.output(row)
            count += 1
    finally:
        strategy.close()

    print(f"[INFO] Done. Processed {count} row(s).")


if __name__ == "__main__":
    main()
