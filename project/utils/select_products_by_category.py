from models.product import Product


def select_products_by_category(products: list[Product], category: str) -> list[Product]:
    return [product for product in products if product.category == category]
