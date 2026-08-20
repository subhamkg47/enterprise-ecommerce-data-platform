def validate_orders(orders):
    valid_orders = []

    for order in orders:
        if order["quantity"] <= 0:
            continue

        if order["customer_id"] <= 0:
            continue

        if order["product_id"] <= 0:
            continue

        valid_orders.append(order)

    return valid_orders