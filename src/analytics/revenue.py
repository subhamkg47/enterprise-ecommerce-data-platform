import sqlite3


def get_customer_revenue(database_file):
    connection = sqlite3.connect(database_file)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            c.customer_id,
            c.first_name || ' ' || c.last_name AS customer_name,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(o.total_amount) AS total_spent
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        GROUP BY
            c.customer_id,
            c.first_name,
            c.last_name
        ORDER BY total_spent DESC
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results

