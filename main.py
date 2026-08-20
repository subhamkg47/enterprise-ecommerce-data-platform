from src.ingestion.load_orders import load_orders
from src.ingestion.validate_orders import validate_orders
from src.transformation.transform_orders import (
    transform_orders,
    save_orders,
)


def run_pipeline():
    orders = load_orders("data/raw/orders.csv")

    valid_orders = validate_orders(orders)

    transformed_orders = transform_orders(valid_orders)

    save_orders(
        transformed_orders,
        "data/processed/orders_processed.csv"
    )

    print(f"Loaded orders: {len(orders)}")
    print(f"Valid orders: {len(valid_orders)}")
    print(f"Transformed orders: {len(transformed_orders)}")
    print("Processed data saved successfully.")


if __name__ == "__main__":
    run_pipeline()