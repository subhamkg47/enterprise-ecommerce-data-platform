from src.config.settings import REVENUE_REPORT_FILE
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


def get_product_revenue(database_file):
    connection = sqlite3.connect(database_file)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            p.product_id,
            p.product_name,
            SUM(oi.quantity) AS units_sold,
            SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY
            p.product_id,
            p.product_name
        ORDER BY total_revenue DESC
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results



def get_revenue_summary(database_file):
    connection = sqlite3.connect(database_file)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_orders,
            COALESCE(SUM(total_amount), 0) AS total_revenue,
            COALESCE(AVG(total_amount), 0) AS average_order_value
        FROM orders
        """
    )

    result = cursor.fetchone()

    connection.close()

    return result


def generate_revenue_report(database_file, output_file):
    customer_revenue = get_customer_revenue(database_file)
    product_revenue = get_product_revenue(database_file)
    revenue_summary = get_revenue_summary(database_file)

    total_orders, total_revenue, average_order_value = revenue_summary

    with open(output_file, "w") as file:
        file.write("E-COMMERCE REVENUE REPORT\n")
        file.write("=========================\n\n")

        file.write("SUMMARY\n")
        file.write("-------\n")
        file.write(f"Total Orders: {total_orders}\n")
        file.write(f"Total Revenue: {total_revenue:.2f}\n")
        file.write(f"Average Order Value: {average_order_value:.2f}\n\n")

        file.write("CUSTOMER REVENUE\n")
        file.write("----------------\n")

        for customer_id, customer_name, total_orders, total_spent in customer_revenue:
            file.write(
                f"{customer_id} | {customer_name} | "
                f"Orders: {total_orders} | "
                f"Spent: {total_spent:.2f}\n"
            )

        file.write("\nPRODUCT REVENUE\n")
        file.write("----------------\n")

        for product_id, product_name, units_sold, total_revenue in product_revenue:
            file.write(
                f"{product_id} | {product_name} | "
                f"Units Sold: {units_sold} | "
                f"Revenue: {total_revenue:.2f}\n"
            )

def generate_default_revenue_report(database_file):
    generate_revenue_report(
        database_file,
        str(REVENUE_REPORT_FILE),
    )
