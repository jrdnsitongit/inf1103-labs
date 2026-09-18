# Part 1: Function to get and validate user input
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

    # Part 2: Process a valid delivery
def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

# Part 3: Calculate 10% tax for the delivery
def calculate_tax(amount):
    tax = amount * 0.10
    return tax

# Part 4: Generate the final report
def generate_report(total_units, failed_attempts):
    print("\n--- Inventory Report ---")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

 # Main program
inventory = 0
failed_entries = 0

while True:

    # Get validated input
    result = get_valid_input()

    # Exit if user types quit
    if result == "quit":
        break

    # Process the delivery
    inventory = process_delivery(inventory, result)

    # Calculate tax for this delivery
    tax = calculate_tax(result)

    print(f"Added {result} to inventory. Total inventory: {inventory}")
    print(f"Tax for this delivery: {tax:.2f}")

# Generate final report after user quits
generate_report(inventory, failed_entries)