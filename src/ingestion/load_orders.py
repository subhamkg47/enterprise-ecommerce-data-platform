import csv
from datetime import datetime


def load_orders(file_path):
    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        orders = list(reader)

    for order in orders:
        order["order_id"] = int(order["order_id"])
        order["customer_id"] = int(order["customer_id"])
        order["product_id"] = int(order["product_id"])
        order["quantity"] = int(order["quantity"])


        order["order_date"] = datetime.strptime(
            order["order_date"],
            "%Y-%m-%d %H:%M:%S"
        )

    return orders
