from src.ingestion.validate_orders import validate_orders
from src.transformation.transform_orders import transform_orders

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
