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

