import csv


PRODUCT_PRICES = {
    101: 499.00,
    102: 2499.00,
    103: 299.00,
}


def transform_orders(orders):
    transformed_orders = []

    for order in orders:
        product_id = order["product_id"]
        quantity = order["quantity"]

        unit_price = PRODUCT_PRICES[product_id]
        line_amount = quantity * unit_price

        transformed_order = {
            **order,
            "unit_price": unit_price,
            "line_amount": line_amount,
        }

        transformed_orders.append(transformed_order)

    return transformed_orders


def save_orders(orders, file_path):
    fieldnames = [
        "order_id",
        "customer_id",
        "product_id",
        "quantity",
        "order_date",
        "unit_price",
        "line_amount",
    ]

    with open(file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)
