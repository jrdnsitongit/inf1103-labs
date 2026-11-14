from supplier import Supplier
from product import Product
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from inventory import Inventory
from order import Order

#2.2) for predicting whether product is there if supplier is deleted
print("--- Association test: del supplier ---")

supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")

laptop = PhysicalProduct("T1", "Laptop", 1200.00, 15, supplier, 2.0)
editor = DigitalProduct("T2", "Photo Editor", 59.00, 100, supplier, 850)

print("\nBefore del supplier:")
laptop.display_supplier()
editor.display_supplier()

del supplier
print("\nAfter del supplier:")
laptop.display_supplier()
editor.display_supplier()

#3.2) prediction where inventory object is there even product is deleted
print("\n--- Aggregation test: Inventory and Product ---")

supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")

laptop = PhysicalProduct("T1", "Laptop", 1200.00, 15, supplier, 2.0)
print("\nProduct created before any inventory:")
laptop.display_information()

inventory_a = Inventory()
inventory_b = Inventory()

print("\nAdded to Inventory A:", inventory_a.add_product(laptop))
inventory_a.display_all()

print("\nRemoved from Inventory A:", inventory_a.remove_product("T1"))
inventory_a.display_all()

print("\nProduct after removal from Inventory A:")
laptop.display_information()
laptop.update_stock(5)
print("Stock after update_stock(5):", laptop.get_stock())

print("\nAdded to Inventory B:", inventory_b.add_product(laptop))
inventory_b.display_all()
print("Same object in Inventory B?", inventory_b.find_product("T1") is laptop)

inventory_b.remove_product("T1")
print("\nInventory B emptied:")
inventory_b.display_all()
print("Product still exists:", laptop.get_name(), "| stock:", laptop.get_stock())

#4.3) prediction where add the same Product to two different Orders, how many OrderLine objects and how many Product objects are created

print("\n--- Composition test: Order and OrderLine ---")

supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
laptop = PhysicalProduct("T1", "Laptop", 1200.00, 15, supplier, 2.0)
mouse = PhysicalProduct("T2", "Mouse", 25.50, 40, supplier, 0.1)
editor = DigitalProduct("T3", "Photo Editor", 59.00, 100, supplier, 850)

inventory = Inventory()
inventory.add_product(laptop)          

order1 = Order("O001")
order1.add_order_line(laptop, 1)
order1.add_order_line(mouse, 2)
order1.add_order_line(editor, 1)

print()
order1.display_information()

order2 = Order("O002")
order2.add_order_line(laptop, 3)

print()
order2.display_information()

line_a = order1.get_order_lines()[0]
line_b = order2.get_order_lines()[0]
print("\nSame OrderLine object in both orders?", line_a is line_b)
print("Same Product object in both lines?   ", line_a.get_product() is line_b.get_product())
print("Product is also still in the inventory?", inventory.find_product("T1") is laptop)

print("\nRemoved Mouse line from order 1:", order1.remove_order_line("T2"))
order1.display_information()
print("Mouse still exists:", mouse.get_name(), "| stock:", mouse.get_stock())

del order1
print("\nAfter deleting order1, laptop still works:")
laptop.display_information()
print("Order 2 unaffected, total:", order2.calculate_total())
 
#6.2 test substitutablity of Product, PhysicalProduct, DigitalProduct
print("\n--- LSP test: substitutability of Product ---")
def show_product_details(product: Product) -> None:
        product.display_information()
        print(product.get_fulfilment_info())

supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
laptop = PhysicalProduct("T1", "Laptop", 1200.00, 15, supplier, 2.0)
editor = DigitalProduct("T2", "Photo Editor", 59.00, 100, supplier, 850)

show_product_details(laptop)
show_product_details(editor)    
#6.3 test update_stock on both types
print("\n--- LSP test: update_stock on both types ---")
products: list[Product] = [laptop, editor]
for p in products:
    p.update_stock(10)
    print(p.get_name(), "after +10:", p.get_stock())
    p.update_stock(-1000)
    print(p.get_name(), "after -1000:", p.get_stock())

#7.2 polymorphism test
print("\n--- Polymorphism test: one loop over Product ---")
supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
laptop = PhysicalProduct("T1", "Laptop", 1200.00, 15, supplier, 2.0)
editor = DigitalProduct("T2", "Photo Editor", 59.00, 100, supplier, 850)

inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(editor)

for product in inventory.get_products():
    product.display_information()
    print(product.get_fulfilment_info())