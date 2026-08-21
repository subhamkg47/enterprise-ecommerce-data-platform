import csv
import sqlite3


def load_orders_to_database(csv_file, database_file):
    connection = sqlite3.connect(database_file)

    cursor = connection.cursor()

    with open(csv_file, "r") as file:
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
def count_order_items(database_file):
    connection = sqlite3.connect(database_file)

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM order_items")

    count = cursor.fetchone()[0]

    connection.close()

    return count
