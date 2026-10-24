import json

class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int ):
        self.__product_id= product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def update_stock(self, quantity: int) -> None:
        """Updates the stock using the given quantity integer."""
        self.__stock += quantity
        if self.__stock < 0:
            self.__stock = 0

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | Price: ${self.__price:.2f} | Stock: {self.__stock}")

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
            "stock": self.__stock
        }

class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product: Product) -> bool:
        """Adds a Product. Returns False if the ID already exists."""
        if self.find_by_id(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def find_by_id(self, product_id: str):
        """Returns the Product with this exact ID (case-insensitive), or None."""
        for p in self.__products:
            if p.get_product_id().lower() == product_id.lower():
                return p
        return None

    def search_product(self, keyword: str):
        """Returns the first Product whose ID or name matches keyword, or None."""
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

    def to_list(self) -> list:
        """Returns the products as a list of dictionaries (for saving to JSON)."""
        return [p.to_dict() for p in self.__products]



INVENTORY_FILE = "inventory.json"

def load_inventory() -> Inventory:
    """
    Reads inventory.json if it exists.
    Returns the loaded list of product dictionaries.
    If the file does not exist, returns initial default inventory list.
    """
    inventory = Inventory()
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
        for item in data:
            # accept both "product_id" (new) and "id" (Week 5 format)
            product_id = item.get("product_id", item.get("id"))
            inventory.add_product(
                Product(product_id, item["name"], item["price"], item["stock"])
            )
        print("inventory.json found.")
        print("Inventory loaded successfully.\n")
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, AttributeError):
        print("inventory.json not found.")
        print("Starting with initial inventory.\n")
        inventory = Inventory()
        for p in get_default_products():
            inventory.add_product(p)
    return inventory

def get_default_products() -> list:
    """Default inventory items matching the lab requirements."""
    return [
        Product("P001", "Laptop", 1200.00, 15),
        Product("P002", "Mouse", 25.50, 40),
        Product("P003", "Keyboard", 45.00, 25),
    ]
# Part 2: Save inventory list to inventory.json
def save_inventory(inventory):
    """Saves current inventory list to inventory.json."""
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
    """Adds a new product dictionary using exact prompts."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()

    if not product_id or not name:
        print("Product ID and name cannot be empty. Product creation canceled.")
        return
    
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid number format. Product creation canceled.")
        return
 
    if price < 0 or stock < 0:
        print("Price and stock cannot be negative. Product creation canceled.")
        return
 
    if inventory.add_product(Product(product_id, name, price, stock)):
        print("\nProduct added successfully!")
    else:
        print("\nA product with that ID already exists. Product creation canceled.")
#update stock function
def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
 
    product = inventory.find_by_id(product_id)
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
    print(f"ID: {product.get_product_id()}")
    print(f"Name: {product.get_name()}")
    print(f"Price: ${product.get_price():.2f}")
    print(f"Stock: {product.get_stock()}")
    print("--------------------------------------------------")

    print("\nProduct not found.")
#display all products function
def display_all(inventory):
    """Prints all products formatted in line with the sample outputs."""
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