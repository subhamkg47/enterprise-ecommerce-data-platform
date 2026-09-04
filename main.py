from src.pipeline.context import create_pipeline_context
from src.pipeline.result import StageResult
from src.pipeline.stages import (
    run_ingestion,
    run_validation,
    run_transformation,
    run_database_loading,
    run_analytics,
)


def stage_failed(result):
    return result.status == "failed"


def run_pipeline():
    context = create_pipeline_context()

    orders, ingestion_result = run_ingestion(context)

    if stage_failed(ingestion_result):
        valid_orders = []
        validation_result = StageResult.failure(
            "validation",
            RuntimeError("Skipped because ingestion failed"),
        )
    else:
        valid_orders, validation_result = run_validation(orders)

    transformed_orders, transformation_result = run_transformation(
        valid_orders,
        context,
    )

    database_result = run_database_loading(
        valid_orders,
        context,
    )

    analytics_result = run_analytics(context)

    results = [
        ingestion_result,
        validation_result,
        transformation_result,
        database_result,
        analytics_result,
    ]

    print("\nPIPELINE SUMMARY")
    print("================")

    for result in results:
        print(
            f"{result.stage_name}: "
            f"{result.status} | "
            f"processed={result.records_processed} | "
            f"rejected={result.records_rejected}"
        )

    if all(result.status == "success" for result in results):
        print("\nData pipeline completed successfully.")
    else:
        print("\nData pipeline completed with failures.")

if __name__ == "__main__":
    run_pipeline()
