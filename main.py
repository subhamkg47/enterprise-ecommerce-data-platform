from src.ingestion.load_orders import load_orders
from src.ingestion.validate_orders import validate_orders
from src.transformation.transform_orders import (
    transform_orders,
    save_orders,
)
from src.loading.load_to_database import (
    load_orders_to_database,
    load_orders_table,
    count_order_items,
)
from src.analytics.revenue import generate_revenue_report


def run_pipeline():
    orders = load_orders("data/raw/orders.csv")

    valid_orders = validate_orders(orders)

    transformed_orders = transform_orders(valid_orders)

    save_orders(
        transformed_orders,
        "data/processed/orders_processed.csv"
    )

   
    load_orders_to_database(
      "data/processed/orders_processed.csv",
      "data/ecommerce.db"
    )

    load_orders_table(
    valid_orders,
    "data/ecommerce.db"
    )

    generate_revenue_report(
    "data/ecommerce.db",
    "reports/revenue_report.txt"
    )

    print("Revenue report generated successfully.")

    database_count = count_order_items("data/ecommerce.db")
    print(f"Database order items: {database_count}")

    print(f"Loaded orders: {len(orders)}")
    print(f"Valid orders: {len(valid_orders)}")
    print(f"Transformed orders: {len(transformed_orders)}")
    print("Processed data saved successfully.")
    print("Data loaded into SQLite successfully.")



if __name__ == "__main__":
    run_pipeline()
