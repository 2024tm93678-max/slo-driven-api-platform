products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 75000
    },
    {
        "id": 2,
        "name": "Keyboard",
        "price": 2500
    },
    {
        "id": 3,
        "name": "Mouse",
        "price": 1200
    }
]


def get_products():
    return products


def create_product(name: str, price: float):
    new_product = {
        "id": len(products) + 1,
        "name": name,
        "price": price
    }

    products.append(new_product)

    return new_product