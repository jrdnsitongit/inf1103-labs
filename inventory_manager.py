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

  # Main program
if __name__ == "__main__":
    # 1. Load existing data or start fresh
    inventory, transaction_history = load_inventory()
    failed_entries = 0
    next_product_id = max(
        (product_id for product_id, _, _ in transaction_history),
        default=1000,
    ) + 1

    if not transaction_history:
        print(f"Current Orders:")
        print("No previous orders found")
    else:
        print(f"Current Inventory: ")
        for product_id, product_name, quantity in transaction_history:
            print(f"{product_id}, {product_name}, {quantity}")
        print()

    # 2. Continuous Input Loop
    while True:
        result = get_valid_input()

        if result == "quit":
            break

        # Process valid entry
        product_name, quantity = result
        inventory = process_delivery(inventory, quantity)
        product_id = next_product_id
        transaction_history.append((product_id, product_name, quantity))
        next_product_id += 1

        tax = calculate_tax(quantity)

        print("New Order Added")
        print(f"{product_id}, {product_name}, {quantity}")
        print(f"Tax: {tax:.2f} | Total Inventory: {inventory}\n")

    # 3. Save data upon quitting
    save_inventory(inventory, transaction_history)
    print("Inventory successfully saved to inventory.txt.")

    # 4. Final summary report
    generate_report(inventory, failed_entries, transaction_history)