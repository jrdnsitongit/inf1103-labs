from abc import ABC, abstractmethod
from ast import While
import json
import os
from supplier import Supplier
from product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from inventory import Inventory
from OrderLine import OrderLine
from order import Order
from product_factory import ProductFactory

def get_non_empty_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_valid_email(prompt: str) -> str:
    while True:
        email = input(prompt).strip()
        if not email:
            print("Email cannot be empty. Please try again.")
            continue
        if " " not in email and "@" in email:
            local_part, _, domain_part = email.partition("@")
            if local_part and "." in domain_part and not domain_part.startswith(".") and not domain_part.endswith("."):
                return email
        print("Invalid email format (e.g., name@example.com). Please try again.")


def get_non_negative_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if value < 0:
                print("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid number format. Please enter a valid decimal number.")


def get_non_negative_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if value < 0:
                print("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid integer format. Please enter a whole number.")


def get_valid_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Invalid quantity format. Please enter a whole number.")

def create_product_from_dict(item: dict) -> Product:
    product_id = item.get("product_id", item.get("id"))
    product_type = item.get("type", "physical")
    name = item["name"]
    price = float(item["price"])
    stock = int(item["stock"])

    if not product_id or not name:
        raise ValueError("Product ID and name must not be empty.")
    if price < 0 or stock < 0:
        raise ValueError("Price and stock cannot be negative.")

    s = item["supplier"]
    if not s.get("supplier_id") or not s.get("name") or not s.get("contact_email"):
        raise ValueError("Incomplete supplier details.")
    supplier = Supplier(s["supplier_id"], s["name"], s["contact_email"])

    extra = item.get("weight") if product_type == "physical" else item.get("download_size")
    if extra is None or float(extra) < 0:
        raise ValueError("Invalid weight or download size.")

    return ProductFactory.create_product(product_type, product_id, name, price, stock, supplier, float(extra))

INVENTORY_FILE = "inventory.json"

def build_default_inventory() -> Inventory:
    inventory = Inventory()
    for p in get_default_products():
        inventory.add_product(p)
    return inventory


def load_inventory() -> Inventory:
    """
    Loads inventory.json. If the file does not exist, creates it
    from the default products and returns that inventory.
    """
    if not os.path.exists(INVENTORY_FILE):
        print("inventory.json not found.")
        print("Creating inventory.json with the default products.")
        inventory = build_default_inventory()
        save_inventory(inventory)
        print()
        return inventory

    try:
        inventory = Inventory()
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
        for item in data:
            inventory.add_product(create_product_from_dict(item))
        print("inventory.json found.")
        print("Inventory loaded successfully.\n")
        return inventory
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError, ValueError):
        print("inventory.json could not be read (invalid or old format).")
        print("Starting with the default inventory. The file is not overwritten until you save.\n")
        return build_default_inventory()

def get_default_products() -> list[Product]:
    tech_supply = Supplier("S001", "TechSupply", "sales@techsupply.com")
    soft_house = Supplier("S002", "SoftHouse", "support@softhouse.com")
    return [
        ProductFactory.create_product("physical", "P001", "Laptop", 1200.00, 15, tech_supply, 2.5),
        ProductFactory.create_product("physical", "P002", "Mouse", 25.50, 40, tech_supply, 0.1),
        ProductFactory.create_product("digital", "P003", "Photo Editor", 59.00, 100, soft_house, 100.0),
    ]
# Part 2: Save inventory list to inventory.json
def save_inventory(inventory: Inventory) -> None:
    print("\nSaving inventory...")
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory.to_list(), file, indent=4)
    print("Inventory saved successfully to inventory.json.")

#json functionalties
def add_product_menu(inventory: Inventory) -> None:
    print("\nAdd New Product")

    while True:
        product_id = get_non_empty_input("Product ID: ")
        if inventory.find_product(product_id) is not None:
                    print("A product with that ID already exists. Please enter a unique Product ID.")
                    continue
        break
    name = get_non_empty_input("Product Name: ")

    print("Product type: 1. Physical  2. Digital")
    while True:
        ptype = input("Choose type: ").strip()
        if ptype in ("1", "2"):
            break
        print("Invalid product type. Please enter 1 or 2.")

    print("\nSupplier details")
    supplier_id = get_non_empty_input("Supplier ID: ")
    supplier_name = get_non_empty_input("Supplier Name: ")
    contact_email = get_non_empty_input("Supplier Email: ")
    supplier = Supplier(supplier_id, supplier_name, contact_email)
    price = get_non_negative_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    if ptype == "1":
        extra = get_non_negative_float("Weight (kg): ")
        product = ProductFactory.create_product("physical", product_id, name, price, stock, supplier, extra)
    else:
        extra = get_non_negative_float("Download size (MB): ")
        product = ProductFactory.create_product("digital", product_id, name, price, stock, supplier, extra)

    if inventory.add_product(product):
        print("\nProduct added successfully!")
    else:
        print("\nA product with that ID already exists. Product creation canceled.")

#update stock function
def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = get_non_empty_input("Enter Product ID: ").strip()
 
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
 
    print("\nProduct Found:")
    product.display_information()
 
    while True:
            quantity = get_valid_int("Enter stock quantity to add (use negative to subtract): ")
            if hasattr(product, "stock") and product.stock + quantity < 0:
                print(f"Insufficient stock (current stock: {product.stock}). Please enter a valid quantity.")
                continue
            try:
                product.update_stock(quantity)
                break
            except ValueError as e:
                print(f"Invalid stock update: {e}")
    
    print("\nStock updated successfully!")
    print("Updated Details:")
    product.display_information()
#search product function
def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    keyword = get_non_empty_input("Enter Product ID or Name: ").strip()

    product = inventory.search_product(keyword) if keyword else None
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("--------------------------------------------------")
    product.display_information()
    print("--------------------------------------------------")

# Main Menu Application Loop
if __name__ == "__main__":
    print("==========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("==========================================\n")

    inventory = load_inventory()

    while True:
        print("--------- MENU ---------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("------------------------")

        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product_menu(inventory)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")