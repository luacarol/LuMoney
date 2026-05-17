"""
LuMoney — Fake Financial Data Generator
Generates a realistic Excel spreadsheet with income and expense transactions.
"""

import random
from datetime import date, timedelta

import pandas as pd

# --- Configuration ---
START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)
OUTPUT_FILE = "transactions.xlsx"

# --- Categories ---
EXPENSE_CATEGORIES = {
    "Food & Groceries": [
        "Supermarket", "Bakery", "Ifood delivery", "Rappi delivery",
        "Restaurant lunch", "Coffee shop", "Snacks",
    ],
    "Transport": [
        "Uber ride", "99 ride", "Gas station", "Bus fare", "Parking",
    ],
    "Housing": [
        "Rent", "Electricity bill", "Water bill", "Internet bill", "Condo fee",
    ],
    "Health": [
        "Pharmacy", "Doctor appointment", "Gym membership", "Lab exam",
    ],
    "Entertainment": [
        "Netflix", "Spotify", "Cinema ticket", "Concert ticket", "Books",
    ],
    "Shopping": [
        "Clothing store", "Amazon purchase", "Electronics", "Shoes",
    ],
    "Education": [
        "Online course", "English class", "Technical book", "Workshop",
    ],
    "Personal Care": [
        "Haircut", "Manicure", "Skincare products",
    ],
}

INCOME_CATEGORIES = {
    "Salary": ["Monthly salary", "Salary advance"],
    "Freelance": ["Freelance project", "Consulting", "Design work"],
    "Investment": ["Dividend payment", "Interest income", "Fund redemption"],
    "Other Income": ["Birthday gift", "Refund", "Cashback reward"],
}

# --- Price ranges per category (BRL) ---
EXPENSE_RANGES = {
    "Food & Groceries": (15, 350),
    "Transport": (8, 120),
    "Housing": (80, 1800),
    "Health": (30, 400),
    "Entertainment": (12, 200),
    "Shopping": (50, 800),
    "Education": (40, 600),
    "Personal Care": (20, 150),
}

INCOME_RANGES = {
    "Salary": (4500, 7000),
    "Freelance": (300, 2500),
    "Investment": (50, 800),
    "Other Income": (20, 500),
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "Pix", "Cash", "Bank Transfer"]


def random_date(start: date, end: date) -> date:
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def generate_transactions(n_expenses: int = 250, n_incomes: int = 40) -> pd.DataFrame:
    rows = []

    # --- Expenses ---
    for _ in range(n_expenses):
        category = random.choice(list(EXPENSE_CATEGORIES.keys()))
        description = random.choice(EXPENSE_CATEGORIES[category])
        low, high = EXPENSE_RANGES[category]
        amount = round(random.uniform(low, high), 2)
        rows.append(
            {
                "date": random_date(START_DATE, END_DATE),
                "description": description,
                "category": category,
                "type": "Expense",
                "amount": -amount,  # negative = money out
                "payment_method": random.choice(PAYMENT_METHODS),
            }
        )

    # --- Income ---
    for _ in range(n_incomes):
        category = random.choice(list(INCOME_CATEGORIES.keys()))
        description = random.choice(INCOME_CATEGORIES[category])
        low, high = INCOME_RANGES[category]
        amount = round(random.uniform(low, high), 2)
        rows.append(
            {
                "date": random_date(START_DATE, END_DATE),
                "description": description,
                "category": category,
                "type": "Income",
                "amount": amount,  # positive = money in
                "payment_method": random.choice(PAYMENT_METHODS),
            }
        )

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1  # row IDs starting at 1
    df.index.name = "id"
    return df


def save_to_excel(df: pd.DataFrame, filepath: str) -> None:
    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Transactions", index=True)

        # --- Summary sheet ---
        summary_data = {
            "Metric": [
                "Total Income (BRL)",
                "Total Expenses (BRL)",
                "Net Balance (BRL)",
                "# Transactions",
                "# Income records",
                "# Expense records",
            ],
            "Value": [
                round(df[df["type"] == "Income"]["amount"].sum(), 2),
                round(df[df["type"] == "Expense"]["amount"].sum(), 2),
                round(df["amount"].sum(), 2),
                len(df),
                len(df[df["type"] == "Income"]),
                len(df[df["type"] == "Expense"]),
            ],
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)

        # --- Monthly breakdown sheet ---
        df["month"] = df["date"].dt.to_period("M").astype(str)
        monthly = (
            df.groupby(["month", "type"])["amount"]
            .sum()
            .unstack(fill_value=0)
            .reset_index()
        )
        monthly.to_excel(writer, sheet_name="Monthly Breakdown", index=False)

    print(f"✅ File saved: {filepath}")
    print(f"   {len(df)} transactions generated ({START_DATE} → {END_DATE})")


if __name__ == "__main__":
    df = generate_transactions(n_expenses=250, n_incomes=40)
    save_to_excel(df, OUTPUT_FILE)
