from product import Product

class Database:
    def __init__(self):
        self.products = {}
        self._last_product_key = 0

    def add_product(self, product):
        self._last_product_key += 1
        self.products[self._last_product_key] = product
        return self._last_product_key

    def update_product(self, product_key, product):
        self.products[product_key] = product

    def delete_product(self, product_key):
        if product_key in self.products:
            del self.products[product_key]

    def get_product(self, product_key):
        product = self.products.get(product_key)
        if product is None:
            return None
        product_ = Product(product.name, situation=product.situation, description=product.description)
        return product_

    def get_products(self):
        products = []
        for product_key, product in self.products.items():
            product_ = Product(product.name, situation=product.situation, description=product.description)
            products.append((product_key,product_ ))
        return products