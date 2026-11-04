import json
import os

FILE_NAME = "products.json"


def load_products():
    """
    Load all products from products.json
    """

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as file:
            json.dump([], file)

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []


def save_products(products):
    """
    Save products to products.json
    """

    with open(FILE_NAME, "w") as file:
        json.dump(products, file, indent=4)


def add_product(product):
    """
    Add a new product
    """

    products = load_products()
    products.append(product)
    save_products(products)


def delete_product(index):
    """
    Delete a product using index
    """

    products = load_products()

    if 0 <= index < len(products):
        products.pop(index)
        save_products(products)


def update_product(index, product):
    """
    Update an existing product
    """

    products = load_products()

    if 0 <= index < len(products):
        products[index] = product
        save_products(products)


def search_product(keyword):
    """
    Search products by name
    """

    keyword = keyword.lower()

    products = load_products()

    result = []

    for product in products:

        if keyword in product["name"].lower():
            result.append(product)

    return result


def total_products():
    """
    Return total number of products
    """

    return len(load_products())


def total_amount():
    """
    Return total shopping amount
    """

    total = 0

    for product in load_products():

        try:
            total += float(product["price"]) * float(product["quantity"])
        except:
            pass

    return total