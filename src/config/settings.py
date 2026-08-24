import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"

DATABASE_FILE = Path(
    os.getenv(
        "ECOMMERCE_DATABASE",
        DATA_DIR / "ecommerce.db",
    )
)

ORDERS_RAW_FILE = Path(
    os.getenv(
        "ORDERS_RAW_FILE",
        RAW_DATA_DIR / "orders.csv",
    )
)

ORDERS_PROCESSED_FILE = Path(
    os.getenv(
        "ORDERS_PROCESSED_FILE",
        PROCESSED_DATA_DIR / "orders_processed.csv",
    )
)

REVENUE_REPORT_FILE = Path(
    os.getenv(
        "REVENUE_REPORT_FILE",
        REPORTS_DIR / "revenue_report.txt",
    )
)
