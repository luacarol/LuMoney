# LuMoney

> AI-powered personal finance dashboard for analyzing expenses, tracking spending habits, and generating smart financial insights.

## About

LuMoney is a personal finance intelligence platform that transforms transaction data into smart insights and interactive dashboards.

## Features (planned)

- Upload and parse financial transaction data (CSV/Excel)
- Automatic expense categorization
- Monthly spending analysis and trends
- AI-generated financial insights
- Interactive dashboard with charts and visualizations

## Tech Stack (planned)

- **Frontend:** React
- **Backend:** Django (Python)
- **AI/ML:** OpenAI API / custom models
- **Data:** Pandas, openpyxl

## Project Structure

```
LuMoney/
├── mock-data/
│   ├── generate_transactions.py   # Fake financial data generator
│   └── transactions.xlsx          # Generated output (git-ignored)
├── .venv/                         # Python virtual environment (git-ignored)
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

**Requirements:** Python 3.x

```bash
# Clone and enter the project
git clone https://github.com/your-user/LuMoney.git
cd LuMoney

# Create and activate the virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Mock Data

Generates a realistic Excel file with one year of personal finance transactions in BRL.

```bash
cd mock-data
python generate_transactions.py
# Output: mock-data/transactions.xlsx
```

The generated file contains three sheets:

| Sheet | Description |
|---|---|
| `Transactions` | Full row-level data (250 expenses + 40 incomes by default) |
| `Summary` | Total income, total expenses, net balance, record counts |
| `Monthly Breakdown` | Income vs. expenses grouped by month |

Each transaction has: `date`, `description`, `category`, `type` (Income/Expense), `amount` (negative = expense), `payment_method`.

To change the volume or date range, edit the constants at the top of `generate_transactions.py`:

```python
START_DATE = date(2025, 1, 1)
END_DATE   = date(2025, 12, 31)
```

## Status

🚧 Under development — MVP in progress.

