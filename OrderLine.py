from itertools import product

from product import Product
class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("Product must be a valid Product instance.")
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")
        if quantity > product.get_stock():
            raise ValueError(f"Insufficient stock for {product.get_name()} (available: {product.get_stock()}).")
        
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.__product.get_price() * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.get_name()} x {self.__quantity} = ${self.calculate_subtotal():.2f}")
