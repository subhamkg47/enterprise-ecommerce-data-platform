from src.pipeline.context import PipelineContext
from src.pipeline.result import StageResult

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


def run_ingestion(context: PipelineContext):
    try:
        orders = load_orders(str(context.raw_orders_file))

        print(f"Loaded orders: {len(orders)}")

        return orders, StageResult(
            stage_name="ingestion",
            status="success",
            records_processed=len(orders),
        )

    except Exception as error:
        return [], StageResult.failure("ingestion", error)

def run_validation(orders):
    try:
        valid_orders = validate_orders(orders)

        rejected_orders = len(orders) - len(valid_orders)

        print(f"Valid orders: {len(valid_orders)}")

        return valid_orders, StageResult(
            stage_name="validation",
            status="success",
            records_processed=len(valid_orders),
            records_rejected=rejected_orders,
        )

    except Exception as error:
        return [], StageResult.failure("validation", error)

def run_transformation(
    valid_orders,
    context: PipelineContext,
):
    try:
        transformed_orders = transform_orders(valid_orders)

        print(f"Transformed orders: {len(transformed_orders)}")

        save_orders(
            transformed_orders,
            str(context.processed_orders_file),
        )

        print("Processed data saved successfully.")

        return transformed_orders, StageResult(
            stage_name="transformation",
            status="success",
            records_processed=len(transformed_orders),
        )

    except Exception as error:
        return [], StageResult.failure("transformation", error)

def run_database_loading(
    valid_orders,
    context: PipelineContext,
):
    try:
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

        return StageResult(
            stage_name="database_loading",
            status="success",
            records_processed=database_count,
        )

    except Exception as error:
        return StageResult.failure("database_loading", error)

def run_analytics(context: PipelineContext):
    try:
        generate_revenue_report(
            str(context.database_file),
            str(context.revenue_report_file),
        )

        print("Revenue report generated successfully.")

        return StageResult(
            stage_name="analytics",
            status="success",
            records_processed=1,
            metadata={
                "report_file": str(context.revenue_report_file),
            },
        )

    except Exception as error:
        return StageResult.failure("analytics", error)
