import json

INVENTORY_FILE = "inventory.json"

# Part 1: Load saved data from inventory.json
def load_inventory():
    """
    Reads inventory.json if it exists.
    Returns the loaded list of product dictionaries.
    If the file does not exist, returns initial default inventory list.
    """
    try:
        with open(INVENTORY_FILE, "r") as file:
            inventory = json.load(file)
            print("inventory.json found.")
            print("Inventory loaded successfully.\n")
            return inventory
    except (FileNotFoundError, json.JSONDecodeError):
        print("inventory.json not found.")
        print("Starting with initial inventory.\n")
        return get_default_inventory()

def get_default_inventory():
    """Default inventory items matching the lab requirements."""
    return [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
    ]
# Part 2: Save inventory list to inventory.json
def save_inventory(inventory):
    """Saves current inventory list to inventory.json."""
    print("\nSaving inventory...")
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)
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
def add_product(inventory):
    """Adds a new product dictionary using exact prompts."""
    print("\nAdd New Product")
    prod_id = input("Product ID: ").strip()
    name = input("Product Name: ").strip()
    
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid number format. Product creation canceled.")
        return

    new_item = {
        "id": prod_id,
        "name": name,
        "price": price,
        "stock": stock
    }
    
    inventory.append(new_item)
    print("\nProduct added successfully!")
#update stock function
def update_stock(inventory):
    """Updates product stock and displays current product details beforehand."""
    print("\nUpdate Stock")
    prod_id = input("Enter Product ID: ").strip()

    for p in inventory:
        if p["id"].lower() == prod_id.lower():
            print("\nProduct Found:")
            print(f"Name: {p['name']}")
            print(f"Current Stock: {p['stock']}\n")
            
            try:
                new_stock = int(input("New Stock Quantity: "))
                p["stock"] = new_stock
                print("\nStock updated successfully!")
                return
            except ValueError:
                print("Invalid stock quantity.")
                return

    print("\nProduct not found.")
#search product function
def search_product(inventory):
    """Searches for a product by ID or name and prints multiline output."""
    print("\nSearch Product")
    prod_id = input("Enter Product ID: ").strip()

    for p in inventory:
        if p["id"].lower() == prod_id.lower() or prod_id.lower() in p["name"].lower():
            print("\nProduct Found")
            print("--------------------------------------------------")
            print(f"ID: {p['id']}")
            print(f"Name: {p['name']}")
            print(f"Price: ${p['price']:.2f}")
            print(f"Stock: {p['stock']}")
            print("--------------------------------------------------")
            return

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
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            print("\nSaving inventory before exit...")
            with open(INVENTORY_FILE, "w") as file:
                json.dump(inventory, file, indent=4)
            print("Inventory saved successfully.\n")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")