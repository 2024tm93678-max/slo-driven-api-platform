orders = []


def create_order(product_id: int, quantity: int):
    new_order = {
        "id": len(orders) + 1,
        "product_id": product_id,
        "quantity": quantity,
        "status": "created"
    }

    orders.append(new_order)

    return new_order


def get_orders():
    return orders