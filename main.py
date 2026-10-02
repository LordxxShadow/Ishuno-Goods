# Ishuno Goods - Inventory and Sales Management System
# Author: Marvelours Ojeyemi
# Description: Main program file for the Ishuno Goods system.


class Product:
    def __init__(self, product_id, name, price, quantity, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def update_product(self, name, price, quantity, category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def get_details(self):
        return {
            "Product ID": self.product_id,
            "Name": self.name,
            "Price": self.price,
            "Quantity": self.quantity,
            "Category": self.category
        }

    def is_in_stock(self):
        return self.quantity > 0


# Test Product class
product = Product(
    1,
    "Ishuno T-Shirt",
    24.99,
    10,
    "Clothing"
)

print("Welcome to Ishuno Goods!")
print()
print("Product Information")
print("-------------------")

details = product.get_details()

for key, value in details.items():
    print(f"{key}: {value}")

print("In Stock:", product.is_in_stock())
