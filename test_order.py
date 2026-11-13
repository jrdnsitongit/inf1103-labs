#for week 11 lab 10 testing 
""" for 2.3 testing the discount strategy classes """
from supplier import Supplier
from PhysicalProduct import PhysicalProduct
from order import Order
from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount

supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
item = PhysicalProduct("T1", "Widget", 50.00, 20, supplier, 1.0)

order = Order("O001", BulkDiscount(200, 20))
order.add_order_line(item, 5)
print("Bulk:", order.calculate_total())

order.set_discount(PercentageDiscount(10))
print("Percentage:", order.calculate_total())

default_order = Order("O002")
default_order.add_order_line(item, 5)
print("Default (no discount):", default_order.calculate_total())

#additional test for student discount
student_order = Order("O003", StudentDiscount())
student_order.add_order_line(item, 5)
print("Student Discount:", student_order.calculate_total())