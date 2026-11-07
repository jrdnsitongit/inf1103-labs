from supplier import Supplier
from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self.__product_id:str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier :Supplier = supplier

    def update_stock(self, quantity: int) -> None:
        self.__stock += quantity
        if self.__stock < 0:
            self.__stock = 0

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def matches(self, keyword: str) -> bool:
        keyword = keyword.lower()
        return (self.__product_id.lower() == keyword
                or keyword in self.__name.lower())
    
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