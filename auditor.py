#part 1 initialize inventory and failed entries
inventory = 0
failed_entries = 0

#part 2 run loop asking user for stock input until they enter 'quit'
while True:

    #continuously asking user for stock input
    stock = input("Enter stock item (or type 'quit' to exit): ")

    # Step 3: Check if the user wants to quit
    if stock.lower() == "quit":
        break
