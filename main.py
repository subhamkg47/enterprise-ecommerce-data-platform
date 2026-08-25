from src.pipeline.context import (
    PipelineContext,
    create_pipeline_context,
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


def run_pipeline(context: PipelineContext):
    orders = load_orders(str(context.raw_orders_file))
    print(f"Loaded orders: {len(orders)}")

    valid_orders = validate_orders(orders)
    print(f"Valid orders: {len(valid_orders)}")

    transformed_orders = transform_orders(valid_orders)
    print(f"Transformed orders: {len(transformed_orders)}")

    save_orders(
        transformed_orders,
        str(context.processed_orders_file),
    )
    print("Processed data saved successfully.")

    load_orders_to_database(
        str(context.processed_orders_file),
        str(context.database_file),
    )

    database_count = count_order_items(
        str(context.database_file)
    )
    print(f"Database order items: {database_count}")

    load_orders_table(
        valid_orders,
        str(context.database_file),
    )

    generate_revenue_report(
        str(context.database_file),
        str(context.revenue_report_file),
    )
    print("Revenue report generated successfully.")

    print("Data loaded into SQLite successfully.")


if __name__ == "__main__":
    context = create_pipeline_context()
    run_pipeline(context)
