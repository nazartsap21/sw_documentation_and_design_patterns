import argparse
import csv
import random

OUTPUT_FILE = "financial_data.csv"
DEFAULT_ROWS = 1000

DEPARTMENTS = [
    "Sales", "Marketing", "Production", "Logistics",
    "IT", "HR", "Finances", "R&D", "Support", "Administration",
]

QUARTERS = ["Q1", "Q2", "Q3", "Q4"]
YEARS = list(range(2018, 2025))


def generate_row(row_id: int) -> dict:
    year = random.choice(YEARS)
    quarter = random.choice(QUARTERS)
    period = f"{year}-{quarter}"

    department = random.choice(DEPARTMENTS)
    revenue = round(random.uniform(50_000, 5_000_000), 2)
    expenses = round(revenue * random.uniform(0.40, 0.95), 2)

    return {
        "id": row_id,
        "period": period,
        "department": department,
        "revenue": revenue,
        "expenses": expenses,
    }


def generate_csv(rows: int = DEFAULT_ROWS, output: str = OUTPUT_FILE) -> None:
    fieldnames = ["id", "period", "department", "revenue", "expenses"]

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, rows + 1):
            writer.writerow(generate_row(i))

    print(f"Generated {rows} rows → {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator for CSV with financial data")
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    parser.add_argument("--output", type=str, default=OUTPUT_FILE)
    args = parser.parse_args()
    generate_csv(rows=args.rows, output=args.output)
