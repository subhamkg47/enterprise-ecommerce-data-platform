from src.config.settings import (
    DATABASE_FILE,
    ORDERS_RAW_FILE,
    ORDERS_PROCESSED_FILE,
    REVENUE_REPORT_FILE,
)
from src.ingestion.validate_orders import validate_orders
from src.transformation.transform_orders import transform_orders
import sqlite3
from src.loading.load_to_database import (
    load_orders_to_database,
    count_order_items,
)
from src.analytics.revenue import (
    get_customer_revenue,
    get_product_revenue,
    get_revenue_summary,
    generate_revenue_report,
)
from pathlib import Path

from src.pipeline.context import (
    PipelineContext,
    create_pipeline_context,
)
from src.pipeline.stages import (
    run_ingestion,
    run_validation,
    run_transformation,
)
from src.pipeline.result import StageResult


def test_validate_orders_removes_invalid_quantity():
    orders = [
        {
            "order_id": 1,
            "customer_id": 1,
            "product_id": 101,
            "quantity": 2,
        },
        {
            "order_id": 2,
            "customer_id": 1,
            "product_id": 101,
            "quantity": -1,
        },
    ]

    valid_orders = validate_orders(orders)

    assert len(valid_orders) == 1
    assert valid_orders[0]["order_id"] == 1



def test_transform_orders_calculates_line_amount():
    orders = [
        {
            "order_id": 1,
            "customer_id": 1,
            "product_id": 101,
            "quantity": 2,
        }
    ]

    transformed_orders = transform_orders(orders)

    assert transformed_orders[0]["unit_price"] == 499.00
    assert transformed_orders[0]["line_amount"] == 998.00


def test_load_orders_to_database(tmp_path):
    database_file = tmp_path / "test.db"

    connection = sqlite3.connect(database_file)

    connection.execute(
        """
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()

    csv_file = tmp_path / "orders.csv"

    csv_file.write_text(
        "order_item_id,order_id,customer_id,product_id,quantity,order_date,unit_price,line_amount\n"
        "1,1001,1,102,1,2026-08-20 11:00:00,2499.0,2499.0\n"
    )

    load_orders_to_database(
        str(csv_file),
        str(database_file),
    )

    assert count_order_items(str(database_file)) == 1



def test_get_customer_revenue(tmp_path):
    database_file = tmp_path / "test.db"

    connection = sqlite3.connect(database_file)

    connection.execute(
        """
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL
        )
        """
    )

    connection.execute(
        "INSERT INTO customers VALUES (1, 'Test', 'User')"
    )

    connection.execute(
        "INSERT INTO orders VALUES (1001, 1, 1000.0)"
    )

    connection.execute(
        "INSERT INTO orders VALUES (1002, 1, 500.0)"
    )

    connection.commit()
    connection.close()

    results = get_customer_revenue(str(database_file))

    assert len(results) == 1
    assert results[0][0] == 1
    assert results[0][1] == "Test User"
    assert results[0][2] == 2
    assert results[0][3] == 1500.0



def test_get_product_revenue(tmp_path):
    database_file = tmp_path / "test.db"

    connection = sqlite3.connect(database_file)

    connection.execute(
        """
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL
        )
        """
    )

    connection.execute(
        "INSERT INTO products VALUES (101, 'Test Product')"
    )

    connection.execute(
        "INSERT INTO order_items VALUES (1, 1001, 101, 2, 500.0)"
    )

    connection.execute(
        "INSERT INTO order_items VALUES (2, 1002, 101, 1, 500.0)"
    )

    connection.commit()
    connection.close()

    results = get_product_revenue(str(database_file))

    assert len(results) == 1
    assert results[0][0] == 101
    assert results[0][1] == "Test Product"
    assert results[0][2] == 3
    assert results[0][3] == 1500.0



def test_get_revenue_summary(tmp_path):
    database_file = tmp_path / "test.db"

    connection = sqlite3.connect(database_file)

    connection.execute(
        """
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            total_amount DECIMAL(10, 2) NOT NULL
        )
        """
    )

    connection.execute(
        "INSERT INTO orders VALUES (1001, 1000.0)"
    )

    connection.execute(
        "INSERT INTO orders VALUES (1002, 500.0)"
    )

    connection.execute(
        "INSERT INTO orders VALUES (1003, 1500.0)"
    )

    connection.commit()
    connection.close()

    results = get_revenue_summary(str(database_file))

    assert results[0] == 3
    assert results[1] == 3000.0
    assert results[2] == 1000.0


def test_generate_revenue_report(tmp_path):
    database_file = tmp_path / "test.db"
    report_file = tmp_path / "revenue_report.txt"

    connection = sqlite3.connect(database_file)

    connection.execute(
        """
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL
        )
        """
    )

    connection.execute(
        "INSERT INTO customers VALUES (1, 'Test', 'User')"
    )

    connection.execute(
        "INSERT INTO orders VALUES (1001, 1, 1000.0)"
    )

    connection.execute(
        "INSERT INTO products VALUES (101, 'Test Product')"
    )

    connection.execute(
        "INSERT INTO order_items VALUES (1, 1001, 101, 2, 500.0)"
    )

    connection.commit()
    connection.close()

    generate_revenue_report(
        str(database_file),
        str(report_file),
    )

    report = report_file.read_text()

    assert "E-COMMERCE REVENUE REPORT" in report
    assert "Total Orders: 1" in report
    assert "Total Revenue: 1000.00" in report
    assert "Average Order Value: 1000.00" in report
    assert "Test User" in report
    assert "Test Product" in report


def test_configuration_paths():
    assert DATABASE_FILE.suffix == ".db"
    assert ORDERS_RAW_FILE.name == "orders.csv"
    assert ORDERS_PROCESSED_FILE.name == "orders_processed.csv"
    assert REVENUE_REPORT_FILE.name == "revenue_report.txt"

    assert DATABASE_FILE.parent.name == "data"
    assert ORDERS_RAW_FILE.parent.name == "raw"
    assert ORDERS_PROCESSED_FILE.parent.name == "processed"
    assert REVENUE_REPORT_FILE.parent.name == "reports"



def test_pipeline_context():
    context = PipelineContext(
        raw_orders_file=Path("data/raw/orders.csv"),
        processed_orders_file=Path("data/processed/orders_processed.csv"),
        database_file=Path("data/ecommerce.db"),
        revenue_report_file=Path("reports/revenue_report.txt"),
    )

    assert context.raw_orders_file == Path("data/raw/orders.csv")
    assert context.processed_orders_file == Path(
        "data/processed/orders_processed.csv"
    )
    assert context.database_file == Path("data/ecommerce.db")
    assert context.revenue_report_file == Path(
        "reports/revenue_report.txt"
    )


def test_create_pipeline_context():
    context = create_pipeline_context()

    assert context.raw_orders_file.exists()
    assert context.processed_orders_file.parent.exists()
    assert context.database_file.parent.exists()
    assert context.revenue_report_file.parent.exists()



def test_run_ingestion():
    context = create_pipeline_context()

    orders, result = run_ingestion(context)

    assert len(orders) == 5
    assert result.status == "success"
    assert result.records_processed == 5
    assert all("order_id" in order for order in orders)


def test_run_validation():
    orders = [
        {
            "order_id": 1,
            "customer_id": 1,
            "product_id": 101,
            "quantity": 2,
        },
        {
            "order_id": 2,
            "customer_id": 1,
            "product_id": 101,
            "quantity": -1,
        },
    ]

    valid_orders, result = run_validation(orders)

    assert len(valid_orders) == 1
    assert result.status == "success"
    assert result.records_processed == 1
    assert result.records_rejected == 1
    assert valid_orders[0]["order_id"] == 1


def test_run_transformation(tmp_path):
    context = PipelineContext(
        raw_orders_file=Path("data/raw/orders.csv"),
        processed_orders_file=tmp_path / "orders_processed.csv",
        database_file=Path("data/ecommerce.db"),
        revenue_report_file=Path("reports/revenue_report.txt"),
    )

    orders = [
        {
            "order_id": 1,
            "customer_id": 1,
            "product_id": 101,
            "quantity": 2,
        }
    ]
    transformed_orders, result = run_transformation(
        orders,
        context,
    )

    assert len(transformed_orders) == 1
    assert result.status == "success"
    assert result.records_processed == 1

    assert transformed_orders[0]["line_amount"] == 998.00
    assert context.processed_orders_file.exists()


def test_stage_result():
    result = StageResult(
        stage_name="validation",
        status="success",
        records_processed=5,
        records_rejected=1,
    )

    assert result.stage_name == "validation"
    assert result.status == "success"
    assert result.records_processed == 5
    assert result.records_rejected == 1
    assert result.error == ""
