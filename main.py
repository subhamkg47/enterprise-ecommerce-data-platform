from src.pipeline.context import create_pipeline_context
from src.pipeline.stages import (
    run_ingestion,
    run_validation,
    run_transformation,
    run_database_loading,
    run_analytics,
)


def run_pipeline():
    context = create_pipeline_context()

    orders = run_ingestion(context)

    valid_orders = run_validation(orders)

    run_transformation(
        valid_orders,
        context,
    )

    run_database_loading(
        valid_orders,
        context,
    )

    run_analytics(context)

    print("Data pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
