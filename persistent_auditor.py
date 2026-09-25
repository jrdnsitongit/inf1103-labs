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
            saved_history = [int(line.strip()) for line in lines[1:] if line.strip()]
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
        for amount in history:
            file.write(f"{amount}\n")


# Part 3: Function to get and validate user input
def get_valid_input():
    global failed_entries
    while True:
        user_input = input("Enter stock quantity (or type 'quit' to exit): ")

        # Check if user wants to quit
        if user_input.lower() == "quit":
            return "quit"

        # Check if input is a valid integer
        if not user_input.lstrip("-").isdigit():
            print("Invalid input. Please enter a valid number.")
            
            failed_entries += 1
            continue

        quantity = int(user_input)

        # Reject negative numbers
        if quantity < 0:
            print("Quantity cannot be negative. Please try again.")
            failed_entries += 1
            continue

        return quantity

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
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Transaction History: {history}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

  # Main program
if __name__ == "__main__":
    # 1. Load existing data or start fresh
    inventory, transaction_history = load_inventory()
    failed_entries = 0

    print(f"Starting inventory total loaded from file: {inventory}")
    print(f"Previous history loaded: {transaction_history}\n")

    # 2. Continuous Input Loop
    while True:
        result = get_valid_input()

        if result == "quit":
            break

        # Process valid entry
        inventory = process_delivery(inventory, result)
        transaction_history.append(result)  # Track transaction history in Python list

        tax = calculate_tax(result)

        print(f"Added {result} to inventory. Total inventory: {inventory}")
        print(f"Tax for this delivery: {tax:.2f}\n")

    # 3. Save data upon quitting
    save_inventory(inventory, transaction_history)
    print("\nData successfully saved to inventory.txt.")

    # 4. Final summary report
    generate_report(inventory, failed_entries, transaction_history)