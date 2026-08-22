import csv
import sqlite3


def load_orders_to_database(csv_file, database_file):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    with open(csv_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cursor.execute(
                """
                INSERT OR REPLACE INTO order_items
                (order_item_id, order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    int(row["order_item_id"]),
                    int(row["order_id"]),
                    int(row["product_id"]),
                    int(row["quantity"]),
                    float(row["unit_price"]),
                ),
            )

    connection.commit()
    connection.close()


def load_orders_table(orders, database_file):
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    unique_orders = {}

    for order in orders:
        order_id = int(order["order_id"])

        if order_id not in unique_orders:
            unique_orders[order_id] = order

    for order in unique_orders.values():
        order_id = int(order["order_id"])

        cursor.execute(
            """
            SELECT
                COALESCE(SUM(quantity * unit_price), 0)
            FROM order_items
            WHERE order_id = ?
            """,
            (order_id,),
        )

        total_amount = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT OR REPLACE INTO orders
            (order_id, customer_id, order_date, order_status, total_amount)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                order_id,
                int(order["customer_id"]),
                order["order_date"].strftime("%Y-%m-%d %H:%M:%S"),
                "completed",
                total_amount,
            ),
        )

    connection.commit()
    connection.close()


def count_order_items(database_file):
    connection = sqlite3.connect(database_file)

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM order_items")

    count = cursor.fetchone()[0]

    connection.close()

    return count
