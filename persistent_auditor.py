# Part 1: Load saved data from inventory.txt
def load_inventory():
    """
    Reads inventory.txt if it exists.
    Returns the total inventory count and the list of past transaction amounts.
    If the file does not exist, returns 0 and an empty list.
    """
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()
            if not lines:
                return 0, []
            
            # Read total from line 1, and history from remaining lines
            saved_total = int(lines[0].strip())
            saved_history = []
            next_product_id = 1001
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue

                if "|" in line or line.count(",") >= 2:
                    separator = "|" if "|" in line else ","
                    fields = [field.strip() for field in line.split(separator)]
                    if len(fields) == 3:
                        product_id, product_name, quantity = fields
                        product_id = int(product_id)
                        saved_history.append((product_id, product_name, int(quantity)))
                        next_product_id = max(next_product_id, product_id + 1)
                    elif len(fields) == 2:
                        product_name, quantity = fields
                        saved_history.append((next_product_id, product_name, int(quantity)))
                        next_product_id += 1
                else:
                    if line.startswith("(") and line.endswith(")"):
                        product_name, quantity = line[1:-1].split(",", 1)
                        product_name = product_name.strip().strip("'\"")
                        quantity = int(quantity.strip())
                    else:
                        product_name = "Unknown"
                        quantity = int(line)

                    saved_history.append((next_product_id, product_name, quantity))
                    next_product_id += 1

            return saved_total, saved_history

    except FileNotFoundError:
        # File doesn't exist yet (first time running), return defaults safely
        return 0, []
    except ValueError:
        # File is corrupted or empty, fallback to defaults
        return 0, []

# Part 2: Save total and history back to inventory.txt
def save_inventory(total, history):
    """
    Saves the total inventory to the first line, 
    followed by each individual transaction amount on a new line.
    """
    with open("inventory.txt", "w") as file:
        file.write(f"{total}\n")
        for product_id, product_name, quantity in history:
            file.write(f"{product_id}, {product_name}, {quantity}\n")


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