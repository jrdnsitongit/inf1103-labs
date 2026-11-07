
from product import Product
class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def find_product(self, product_id: str)-> Product | None:
        for p in self.__products:
            if p.get_product_id().lower() == product_id.lower():
                return p
        return None

    def search_product(self, keyword: str)-> Product | None:
        for p in self.__products:
            if p.matches(keyword):
                return p
        return None

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("--------------------------------------------------")
        if not self.__products:
            print("No products currently in inventory.")
        else:
            for p in self.__products:
                p.display_information()
        print("--------------------------------------------------")

    def to_list(self) -> list[dict]:
        return [p.to_dict() for p in self.__products]

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
           return False
        self.__products.remove(product)
        return True
    def get_products(self) -> list[Product]:
        return self.__products