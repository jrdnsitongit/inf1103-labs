#part 1 initialize inventory and failed entries
inventory = 0
failed_entries = 0

#part 2 run loop asking user for stock input until they enter 'quit'
while True:

    #continuously asking user for stock input
    stock = input("Enter stock item (or type 'quit' to exit): ")

    #part 3: Check if the user wants to quit
    if stock.lower() == "quit":
        break

    #part 4: Validate that the input is a number
    if not stock.isdigit():
        print("Error: Invalid input. Please enter a number.")
        failed_entries += 1
        continue

    # Convert the valid input from a string to an integer
    stock = int(stock)

     #part 5: Reject negative numbers
    if stock < 0:
        print("Error: Stock quantity cannot be negative.")
        failed_entries += 1
        continue

    #part 6: Add the stock to the running inventory total
    inventory += stock

    print("Stock accepted.")
    print("Current inventory:", inventory)

    #part 7: Check if inventory exceeds 500 units
    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        break