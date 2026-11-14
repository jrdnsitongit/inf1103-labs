#for week 11 lab 10 testing 
import sys
import os
import builtins
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


""" for 2.3 testing the discount strategy classes """
from supplier import Supplier
from PhysicalProduct import PhysicalProduct
from DigitalProduct import DigitalProduct
from order import Order
from inventory import Inventory
from OrderLine import OrderLine
from inventory_manager import get_positive_float, load_products
from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from product_factory import ProductFactory

print("--- Section 2: Strategy Pattern ---")
supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
item = PhysicalProduct("T1", "Widget", 50.00, 20, supplier, 1.0)

order = Order("O001", BulkDiscount(200, 20))
order.add_order_line(item, 5)
print("Bulk:", order.calculate_total())
assert order.calculate_total() == 230.0
order.set_discount(PercentageDiscount(10))
print("Percentage:", order.calculate_total())
assert order.calculate_total() == 225.0
default_order = Order("O002")
default_order.add_order_line(item, 5)
print("Default (no discount):", default_order.calculate_total())
assert default_order.calculate_total() == 250.0

#additional test for student discount
student_order = Order("O003", StudentDiscount())
student_order.add_order_line(item, 5)
print("Student Discount:", student_order.calculate_total())

print("--- Section 3.2: Product Factory ---")
phys = ProductFactory.create_product("physical", "P001", "Laptop", 1200.00, 15, supplier, 2.5)
dig = ProductFactory.create_product("digital", "P003", "Photo Editor", 59.00, 100, supplier, 100.0)
print("Created:", type(phys).__name__, "and", type(dig).__name__)
assert isinstance(phys, PhysicalProduct)
assert isinstance(dig, DigitalProduct)
#3.2 test whether product factory can take in 'service'
try:
    ProductFactory.create_product("service", "S1", "Installation", 30.0, 5, supplier, 1.0)
    assert False, "Expected ValueError for unknown product type"
except ValueError as e:
    print("Caught expected ValueError:", e)

# 4a. Price must be greater than zero
print("\n--- Section 4: Validation ---")
for bad_price in (0, -15.00):
    try:
        ProductFactory.create_product("physical", "P999", "Bad Price", bad_price, 5, supplier, 1.0)
        assert False, f"Expected ValueError for price={bad_price}"
    except ValueError as e:
        print(f"Rejected price {bad_price}:", e)
# 4b. Stock quantity cannot be negative
try:
    ProductFactory.create_product("physical", "P998", "Bad Stock", 25.00, -3, supplier, 1.0)
    assert False, "Expected ValueError for negative initial stock"
except ValueError as e:
    print("Rejected negative initial stock:", e)

try:
    item.update_stock(-999)
    assert False, "Expected ValueError when reducing stock below zero"
except ValueError as e:
    print("Rejected stock deduction below 0:", e)

# 4c. OrderLine quantity must be greater than zero
for bad_qty in (0, -2):
    try:
        OrderLine(item, bad_qty)
        assert False, f"Expected ValueError for OrderLine quantity={bad_qty}"
    except ValueError as e:
        print(f"Rejected OrderLine quantity {bad_qty}:", e)

#5.1 testing user input validation for get_positive_float
print("\n--- Section 5.1: get_positive_float ---")
simulated_inputs = iter(["abc", "-5", "12.50"])
original_input = builtins.input
try:
    builtins.input = lambda prompt="": next(simulated_inputs)
    price_result = get_positive_float("Price: ")
    print("Returned valid float:", price_result)
    assert price_result == 12.50
finally:
    builtins.input = original_input

#5.2 testing load_products from CSV
print("\n--- Section 5.2: load_products (Valid + Bad Rows) ---")
test_csv = "test_products.csv"
with open(test_csv, "w", encoding="utf-8") as f:
    f.write(
        "product_type,product_id,name, price,stock_quantity\n"
        "physical, P001, Desk Lamp, 25.00,10\n"
        "digital, D001, Photo Editor, 49.90,100\n"
        "service, S001, Installation, 30.00,5\n"
        "physical, P002, Office Chair, abc,3\n"
        "physical, P003, Monitor Stand, 39.50,7\n"
    )

try:
    inv = Inventory()
    load_products(test_csv, inv, supplier)
    assert inv.find_product("P001") is not None
    assert inv.find_product("D001") is not None
    assert inv.find_product("P003") is not None
    assert inv.find_product("S001") is None
    assert inv.find_product("P002") is None
finally:
    if os.path.exists(test_csv):
        os.remove(test_csv)

print("\n--- Section 5.2: load_products (Missing File) ---")
load_products("non_existent_products.csv", Inventory(), supplier)

print("\nAll Lab 9 test cases passed!")
