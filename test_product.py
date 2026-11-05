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