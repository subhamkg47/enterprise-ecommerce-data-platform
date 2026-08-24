from src.config.settings import (
    DATABASE_FILE,
    ORDERS_RAW_FILE,
    ORDERS_PROCESSED_FILE,
    REVENUE_REPORT_FILE,
)

from src.ingestion.load_orders import load_orders
from src.ingestion.validate_orders import validate_orders
from src.transformation.transform_orders import transform_orders, save_orders
from src.loading.load_to_database import (
    load_orders_to_database,
    load_orders_table,
    count_order_items,
)
from src.analytics.revenue import generate_revenue_report


def run_pipeline():
    orders = load_orders(str(ORDERS_RAW_FILE))
    print(f"Loaded orders: {len(orders)}")

    valid_orders = validate_orders(orders)
    print(f"Valid orders: {len(valid_orders)}")

    transformed_orders = transform_orders(valid_orders)
    print(f"Transformed orders: {len(transformed_orders)}")

    save_orders(
        transformed_orders,
        str(ORDERS_PROCESSED_FILE),
    )
    print("Processed data saved successfully.")

    load_orders_to_database(
        str(ORDERS_PROCESSED_FILE),
        str(DATABASE_FILE),
    )

    database_count = count_order_items(str(DATABASE_FILE))
    print(f"Database order items: {database_count}")

    load_orders_table(
        valid_orders,
        str(DATABASE_FILE),
    )

    generate_revenue_report(
        str(DATABASE_FILE),
        str(REVENUE_REPORT_FILE),
    )
    print("Revenue report generated successfully.")

    print("Data loaded into SQLite successfully.")


if __name__ == "__main__":
    run_pipeline()
