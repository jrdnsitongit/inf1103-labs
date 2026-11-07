from abc import ABC, abstractmethod
import json
import os
from supplier import Supplier
from product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from inventory import Inventory
from OrderLine import OrderLine
from order import Order







def create_product_from_dict(item: dict) -> Product:
    product_id = item.get("product_id", item.get("id"))
    product_type = item.get("type", "physical")

    s = item["supplier"]
    supplier = Supplier(s["supplier_id"], s["name"], s["contact_email"])

    if product_type == "physical":
        return PhysicalProduct(product_id, item["name"], item["price"],
                               item["stock"], supplier, item.get("weight", 1.0))
    elif product_type == "digital":
        return DigitalProduct(product_id, item["name"], item["price"],
                              item["stock"], supplier, item["download_size"])
    else:
        raise ValueError(f"Unknown product type: {product_type}")


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
        PhysicalProduct("P001", "Laptop", 1200.00, 15, tech_supply, 2.0),
        PhysicalProduct("P002", "Mouse", 25.50, 40, tech_supply, 0.1),
        DigitalProduct("P003", "Photo Editor", 59.00, 100, soft_house, 850),
    ]
# Part 2: Save inventory list to inventory.json
def save_inventory(inventory: Inventory) -> None:
    print("\nSaving inventory...")
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory.to_list(), file, indent=4)
    print("Inventory saved successfully to inventory.json.")


# Part 3: Function to get and validate user input
def get_valid_input():
    global failed_entries
    while True:
        product_name = input("Enter product name (or type 'quit' to exit): ").strip()

        # Check if user wants to quit
        if product_name.lower() == "quit":
            return "quit"

        if not product_name:
            print("Product name cannot be empty. Please try again.")
            failed_entries += 1
            continue

        if not product_name.replace(" ", "").isalpha():
            print("Product name must contain letters and spaces only. Please try again.")
            failed_entries += 1
            continue

        user_input = input("Enter quantity (or type 'quit' to exit): ").strip()

        if user_input.lower() == "quit":
            return "quit"

        if not user_input.isdigit():
            print("Invalid input. Please enter a valid number.")
            failed_entries += 1
            continue

        quantity = int(user_input)

        # Reject quantities outside the allowed range
        if quantity < 0 or quantity > 500:
            print("Quantity must be between 1 and 500. Please try again.")
            failed_entries += 1
            continue

        return product_name, quantity

    # Part 4: Process a valid delivery
def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

# Part 5: Calculate 10% tax for the delivery
def calculate_tax(amount):
    tax = amount * 0.10
    return tax

# Part 6: Generate the final report
def generate_report(total_units, failed_attempts, history):
    print("\n--- Inventory Report ---")
    print(f"Total Transactions Recorded: {len(history)}")
    print(f"Total Units Processed: {total_units}")
    """"
    print("Transaction History:")
    if history:
        for product_id, product_name, quantity in history:
            print(f"{product_id}, {product_name}, {quantity}")
    else:
        print("No previous orders found")
    """
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

#json functionalties
def add_product_menu(inventory: Inventory) -> None:
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()

    if not product_id or not name:
        print("Product ID and name cannot be empty. Product creation canceled.")
        return

    print("Product type: 1. Physical  2. Digital")
    ptype = input("Choose type: ").strip()
    if ptype not in ("1", "2"):
        print("Invalid product type. Product creation canceled.")
        return

    print("\nSupplier details")
    supplier_id = input("Supplier ID: ").strip()
    supplier_name = input("Supplier Name: ").strip()
    contact_email = input("Supplier Email: ").strip()

    if not supplier_id or not supplier_name or not contact_email:
        print("Supplier details cannot be empty. Product creation canceled.")
        return

    supplier = Supplier(supplier_id, supplier_name, contact_email)

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if ptype == "1":
            extra = float(input("Weight (kg): "))
        else:
            extra = float(input("Download size (MB): "))
    except ValueError:
        print("Invalid number format. Product creation canceled.")
        return

    if price < 0 or stock < 0 or extra < 0:
        print("Price, stock and weight/download size cannot be negative. Product creation canceled.")
        return

    if ptype == "1":
        product = PhysicalProduct(product_id, name, price, stock, supplier, extra)
    else:
        product = DigitalProduct(product_id, name, price, stock, supplier, extra)

    if inventory.add_product(product):
        print("\nProduct added successfully!")
    else:
        print("\nA product with that ID already exists. Product creation canceled.")

#update stock function
def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
 
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
 
    print("\nProduct Found:")
    product.display_information()
 
    try:
        quantity = int(input("Enter stock quantity to add (use negative to subtract): "))
    except ValueError:
        print("Invalid quantity format. Stock update canceled.")
        return
 
    product.update_stock(quantity)
    print("\nStock updated successfully!")
    print("Updated Details:")
    product.display_information()
#search product function
def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    keyword = input("Enter Product ID or Name: ").strip()

    product = inventory.search_product(keyword) if keyword else None
    if product is None:
        print("\nProduct not found.")
        return

    print("\nProduct Found")
    print("--------------------------------------------------")
    product.display_information()
    print("--------------------------------------------------")
#display all products function
def display_all(inventory):
    print("\nCurrent Inventory")
    print("--------------------------------------------------")
    if not inventory:
        print("No products currently in inventory.")
    else:
        for p in inventory:
            print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print("--------------------------------------------------")
  # Main program
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
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")