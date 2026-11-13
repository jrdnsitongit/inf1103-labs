from product import Product
from supplier import Supplier
class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if isinstance(download_size, bool):
            raise TypeError("Download size must be a number.")
        size_val = float(download_size)
        if size_val <= 0:
            raise ValueError("Download size must be greater than 0 MB.")
        self.__download_size = size_val 

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Download size: {self.__download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via download link."

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data