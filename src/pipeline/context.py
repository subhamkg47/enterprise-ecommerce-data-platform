from dataclasses import dataclass
from pathlib import Path

from src.config.settings import (
    DATABASE_FILE,
    ORDERS_RAW_FILE,
    ORDERS_PROCESSED_FILE,
    REVENUE_REPORT_FILE,
)


@dataclass(frozen=True)
class PipelineContext:
    raw_orders_file: Path
    processed_orders_file: Path
    database_file: Path
    revenue_report_file: Path


def create_pipeline_context():
    return PipelineContext(
        raw_orders_file=Path(ORDERS_RAW_FILE),
        processed_orders_file=Path(ORDERS_PROCESSED_FILE),
        database_file=Path(DATABASE_FILE),
        revenue_report_file=Path(REVENUE_REPORT_FILE),
    )
