from src.ingestion.validate_orders import validate_orders
from src.transformation.transform_orders import transform_orders
import sqlite3
from src.loading.load_to_database import (
    load_orders_to_database,
    count_order_items,
)

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
