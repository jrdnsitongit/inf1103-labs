from supplier import Supplier
from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if not isinstance(supplier, Supplier):
            raise TypeError("Supplier must be a valid Supplier instance.")

        price_val = float(price)
        stock_val = int(stock)
        if price_val < 0:
            raise ValueError("Price cannot be negative.")
        if stock_val < 0:
            raise ValueError("Stock cannot be negative.")
        
        self.__product_id:str = product_id.strip()
        self.__name: str = name.strip()
        self.__price: float = price_val
        self.__stock: int = stock_val
        self.__supplier :Supplier = supplier
    
    def update_stock(self, quantity: int) -> None:
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise TypeError("Quantity must be an integer.")
        if quantity == 0:
            raise ValueError("Quantity cannot be zero.")
        if self.__stock == 0 and quantity < 0:
            raise ValueError("No stock available (current stock: 0).")
        if self.__stock + quantity < 0:
            raise ValueError("Insufficient stock available.")
        self.__stock += quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def matches(self, keyword: str) -> bool:
        if not isinstance(keyword, str) or not keyword.strip():
            return False
        cleaned = keyword.strip().lower()
        return (self.__product_id.lower() == cleaned
                or cleaned in self.__name.lower())
    
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock
    
    def to_dict(self) -> dict:
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict()
        }
    def get_supplier(self) -> Supplier:
        return self.__supplier
    
    def display_supplier(self) -> None:
       self.__supplier.display_information()