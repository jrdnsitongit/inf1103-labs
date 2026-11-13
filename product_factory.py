from product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from supplier import Supplier

class ProductFactory:
    @staticmethod
    def create_product(product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, extra: float | None = None) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, extra if extra is not None else 1.0)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, extra if extra is not None else 1.0)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
