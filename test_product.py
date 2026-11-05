""" from inventory_manager import Product, PhysicalProduct, DigitalProduct, CanBeShipped

print("--- 1. Abstract class cannot be instantiated ---")
try:
    Product("X", "Test", 1, 1)
except TypeError as e:
    print("TypeError:", e)

guitar = PhysicalProduct("T1", "Guitar", 500, 2, 3.5)
piano = PhysicalProduct("T2", "Piano", 3000, 1, 120)
editor = DigitalProduct("T3", "Photo Editor", 59, 100, 850)

print("\n--- 2. Display (common info + type-specific info) ---")
guitar.display_information()
editor.display_information()

print("\n--- 3. get_fulfilment_info() ---")
print("Physical:", guitar.get_fulfilment_info())
print("Digital:", editor.get_fulfilment_info())

print("\n--- 4. Shipping cost (physical only) ---")
print("Guitar (3.5 kg):", guitar.calculate_shipping_cost())
print("Piano (120 kg):", piano.calculate_shipping_cost())
print("Physical is CanBeShipped?", isinstance(guitar, CanBeShipped))
print("Digital is CanBeShipped?", isinstance(editor, CanBeShipped))
print("Digital has shipping method?", hasattr(editor, "calculate_shipping_cost"))

print("\n--- 5. to_dict() includes type and extra field ---")
print(guitar.to_dict())
print(editor.to_dict())
"""
#for predicting whether product is there if supplier is deleted
"""  
from inventory_manager import Supplier, PhysicalProduct, DigitalProduct

print("--- Association test: del supplier ---")

# 1. Create the supplier independently
supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")

# 2. Create one physical and one digital product using that supplier
laptop = PhysicalProduct("T1", "Laptop", 1200.00, 15, supplier, 2.0)
editor = DigitalProduct("T2", "Photo Editor", 59.00, 100, supplier, 850)

# 3. Display the supplier through each product
print("\nBefore del supplier:")
laptop.display_supplier()
editor.display_supplier()

# 4. Delete the variable, then try again
del supplier

print("\nAfter del supplier:")
laptop.display_supplier()
editor.display_supplier()
"""
"""
#prediction where inventory object is there even product is deleted
from inventory_manager import Supplier, PhysicalProduct, Inventory

print("\n--- Aggregation test: Inventory and Product ---")

supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")

# 1. Create the Product BEFORE any Inventory exists
laptop = PhysicalProduct("T1", "Laptop", 1200.00, 15, supplier, 2.0)
print("\nProduct created before any inventory:")
laptop.display_information()

inventory_a = Inventory()
inventory_b = Inventory()

# 2. Add it to Inventory A
print("\nAdded to Inventory A:", inventory_a.add_product(laptop))
inventory_a.display_all()

# 3. Remove it from Inventory A, then check the Product still works
print("\nRemoved from Inventory A:", inventory_a.remove_product("T1"))
inventory_a.display_all()

print("\nProduct after removal from Inventory A:")
laptop.display_information()
laptop.update_stock(5)
print("Stock after update_stock(5):", laptop.get_stock())

# 4. Add the SAME object to Inventory B
print("\nAdded to Inventory B:", inventory_b.add_product(laptop))
inventory_b.display_all()
print("Same object in Inventory B?", inventory_b.find_product("T1") is laptop)

# 5. Empty Inventory B, the Product should still exist
inventory_b.remove_product("T1")
print("\nInventory B emptied:")
inventory_b.display_all()
print("Product still exists:", laptop.get_name(), "| stock:", laptop.get_stock())
  """
#prediction where add the same Product to two different Orders, how many OrderLine objects and how many Product objects are created
from inventory_manager import Supplier, PhysicalProduct, DigitalProduct, Inventory, Order

print("\n--- Composition test: Order and OrderLine ---")

supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
laptop = PhysicalProduct("T1", "Laptop", 1200.00, 15, supplier, 2.0)
mouse = PhysicalProduct("T2", "Mouse", 25.50, 40, supplier, 0.1)
editor = DigitalProduct("T3", "Photo Editor", 59.00, 100, supplier, 850)

inventory = Inventory()
inventory.add_product(laptop)           # the laptop also sits in an inventory

# 1. Create an order and add several products
order1 = Order("O001")
order1.add_order_line(laptop, 1)
order1.add_order_line(mouse, 2)
order1.add_order_line(editor, 1)

print()
order1.display_information()

# 2. Add the SAME product to a different order
order2 = Order("O002")
order2.add_order_line(laptop, 3)

print()
order2.display_information()

# 3. Compare the objects
line_a = order1.get_order_lines()[0]
line_b = order2.get_order_lines()[0]
print("\nSame OrderLine object in both orders?", line_a is line_b)
print("Same Product object in both lines?   ", line_a.get_product() is line_b.get_product())
print("Product is also still in the inventory?", inventory.find_product("T1") is laptop)

# 4. Remove a line through the Order
print("\nRemoved Mouse line from order 1:", order1.remove_order_line("T2"))
order1.display_information()
print("Mouse still exists:", mouse.get_name(), "| stock:", mouse.get_stock())

# 5. Remove the whole order from the scenario
del order1
print("\nAfter deleting order1, laptop still works:")
laptop.display_information()
print("Order 2 unaffected, total:", order2.calculate_total())