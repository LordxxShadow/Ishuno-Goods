
# Ishuno Goods - Inventory and Sales Management System
# Author: Marvelours Ojeyemi
# Description: A GUI application for managing products, inventory, and sales.

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# --------------------------------------------------
# Product Class
# --------------------------------------------------

class Product:
    def __init__(self, product_id, name, price, quantity, category):
        self.product_id = str(product_id).strip()
        self.name = name.strip()
        self.price = float(price)
        self.quantity = int(quantity)
        self.category = category.strip()

    def update_product(self, name, price, quantity, category):
        self.name = name.strip()
        self.price = float(price)
        self.quantity = int(quantity)
        self.category = category.strip()

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


# --------------------------------------------------
# Inventory Class
# --------------------------------------------------

class Inventory:
    def __init__(self):
        # Dictionary: product ID -> Product object
        self.products = {}

    def add_product(self, product):
        if product.product_id in self.products:
            raise ValueError("A product with this ID already exists.")
        self.products[product.product_id] = product

    def remove_product(self, product_id):
        product_id = str(product_id).strip()
        if product_id not in self.products:
            raise ValueError("Product not found.")
        del self.products[product_id]

    def update_product(self, product_id, name, price, quantity, category):
        product_id = str(product_id).strip()
        if product_id not in self.products:
            raise ValueError("Product not found.")

        self.products[product_id].update_product(
            name, price, quantity, category
        )

    def search_product(self, search_term):
        search_term = str(search_term).strip().lower()

        return [
            product for product in self.products.values()
            if search_term in product.product_id.lower()
            or search_term in product.name.lower()
            or search_term in product.category.lower()
        ]

    def check_stock(self, product_id):
        product_id = str(product_id).strip()
        if product_id not in self.products:
            raise ValueError("Product not found.")
        return self.products[product_id].quantity

    def get_all_products(self):
        return list(self.products.values())


# --------------------------------------------------
# Sale Class
# --------------------------------------------------

class Sale:
    def __init__(self):
        # List of tuples: (Product object, quantity sold)
        self.items = []
        self.date = datetime.now()
        self.total = 0.0

    def add_item(self, product, quantity):
        quantity = int(quantity)

        if quantity <= 0:
            raise ValueError("Sale quantity must be greater than zero.")

        if product.quantity < quantity:
            raise ValueError("There is not enough stock for this sale.")

        self.items.append((product, quantity))
        self.calculate_total()

    def calculate_total(self):
        self.total = sum(
            product.price * quantity
            for product, quantity in self.items
        )
        return self.total

    def complete_sale(self):
        if not self.items:
            raise ValueError("A sale must contain at least one item.")

        for product, quantity in self.items:
            if product.quantity < quantity:
                raise ValueError(
                    f"Not enough stock for {product.name}."
                )

        for product, quantity in self.items:
            product.quantity -= quantity

        self.calculate_total()
        return self.get_receipt()

    def get_receipt(self):
        receipt = [
            f"Sale Date: {self.date.strftime('%Y-%m-%d %H:%M:%S')}",
            "-" * 40
        ]

        for product, quantity in self.items:
            subtotal = product.price * quantity
            receipt.append(
                f"{product.name} x {quantity} = ${subtotal:.2f}"
            )

        receipt.append("-" * 40)
        receipt.append(f"Total: ${self.calculate_total():.2f}")

        return "\n".join(receipt)


# --------------------------------------------------
# StoreSystem Class
# --------------------------------------------------

class StoreSystem:
    def __init__(self):
        self.inventory = Inventory()
        self.sales = []

    def add_product(self, product):
        self.inventory.add_product(product)

    def remove_product(self, product_id):
        # Prevent deleting a product referenced by sale history.
        product_id = str(product_id).strip()

        for sale in self.sales:
            for product, quantity in sale.items:
                if product.product_id == product_id:
                    raise ValueError(
                        "This product has sales history and cannot be removed."
                    )

        self.inventory.remove_product(product_id)

    def update_product(self, product_id, name, price, quantity, category):
        self.inventory.update_product(
            product_id, name, price, quantity, category
        )

    def search_product(self, search_term):
        return self.inventory.search_product(search_term)

    def record_sale(self, product_id, quantity):
        product_id = str(product_id).strip()

        if product_id not in self.inventory.products:
            raise ValueError("Product not found.")

        product = self.inventory.products[product_id]
        quantity = int(quantity)

        sale = Sale()
        sale.add_item(product, quantity)
        receipt = sale.complete_sale()
        self.sales.append(sale)

        return receipt

    def get_sales(self):
        return list(self.sales)


# --------------------------------------------------
# Tkinter Graphical User Interface
# --------------------------------------------------

class IshunoGoodsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ishuno Goods - Inventory and Sales")
        self.root.geometry("1000x680")
        self.root.minsize(800, 550)

        self.store = StoreSystem()

        self.create_widgets()
        self.refresh_inventory()
        self.refresh_sales()

    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="Ishuno Goods",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(12, 2))

        subtitle = ttk.Label(
            self.root,
            text="Inventory and Sales Management System"
        )
        subtitle.pack(pady=(0, 12))

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(
            fill="both", expand=True, padx=12, pady=8
        )

        self.inventory_tab = ttk.Frame(self.notebook, padding=12)
        self.sale_tab = ttk.Frame(self.notebook, padding=12)
        self.history_tab = ttk.Frame(self.notebook, padding=12)

        self.notebook.add(self.inventory_tab, text="Inventory")
        self.notebook.add(self.sale_tab, text="Record Sale")
        self.notebook.add(self.history_tab, text="Sales History")

        self.create_inventory_tab()
        self.create_sale_tab()
        self.create_history_tab()

    def create_inventory_tab(self):
        form = ttk.LabelFrame(
            self.inventory_tab, text="Product Information", padding=10
        )
        form.pack(fill="x", pady=(0, 10))

        self.product_fields = {}
        field_names = [
            ("Product ID", "id"),
            ("Product Name", "name"),
            ("Price", "price"),
            ("Quantity", "quantity"),
            ("Category", "category")
        ]

        for index, (label_text, key) in enumerate(field_names):
            row = index // 3
            column = (index % 3) * 2

            ttk.Label(form, text=label_text).grid(
                row=row, column=column, padx=5, pady=6, sticky="w"
            )

            entry = ttk.Entry(form, width=22)
            entry.grid(
                row=row, column=column + 1, padx=5, pady=6, sticky="ew"
            )
            self.product_fields[key] = entry

        for column in range(6):
            form.columnconfigure(column, weight=1)

        buttons = ttk.Frame(form)
        buttons.grid(
            row=2, column=0, columnspan=6, sticky="w", pady=(8, 0)
        )

        ttk.Button(
            buttons, text="Add Product", command=self.add_product
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Update Selected", command=self.update_product
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Remove Selected", command=self.remove_product
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Clear Fields", command=self.clear_product_fields
        ).pack(side="left", padx=4)

        search_frame = ttk.Frame(self.inventory_tab)
        search_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(search_frame, text="Search products:").pack(side="left")

        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=8)
        self.search_entry.bind(
            "<Return>", lambda event: self.search_products()
        )

        ttk.Button(
            search_frame, text="Search", command=self.search_products
        ).pack(side="left", padx=3)

        ttk.Button(
            search_frame, text="Show All", command=self.refresh_inventory
        ).pack(side="left", padx=3)

        columns = ("id", "name", "price", "quantity", "category", "stock")
        self.inventory_tree = ttk.Treeview(
            self.inventory_tab,
            columns=columns,
            show="headings",
            height=12
        )

        headings = {
            "id": "Product ID",
            "name": "Product Name",
            "price": "Price",
            "quantity": "Quantity",
            "category": "Category",
            "stock": "In Stock"
        }

        widths = {
            "id": 100,
            "name": 200,
            "price": 100,
            "quantity": 100,
            "category": 150,
            "stock": 100
        }

        for column in columns:
            self.inventory_tree.heading(
                column, text=headings[column]
            )
            self.inventory_tree.column(
                column, width=widths[column], anchor="center"
            )

        self.inventory_tree.pack(fill="both", expand=True)
        self.inventory_tree.bind(
            "<<TreeviewSelect>>", self.select_product
        )

    def create_sale_tab(self):
        form = ttk.LabelFrame(
            self.sale_tab, text="New Sale", padding=15
        )
        form.pack(fill="x", pady=10)

        ttk.Label(form, text="Product ID:").grid(
            row=0, column=0, padx=8, pady=8, sticky="w"
        )
        self.sale_product_id = ttk.Entry(form, width=25)
        self.sale_product_id.grid(
            row=0, column=1, padx=8, pady=8
        )

        ttk.Label(form, text="Quantity to sell:").grid(
            row=1, column=0, padx=8, pady=8, sticky="w"
        )
        self.sale_quantity = ttk.Entry(form, width=25)
        self.sale_quantity.grid(
            row=1, column=1, padx=8, pady=8
        )

        ttk.Button(
            form, text="Complete Sale", command=self.record_sale
        ).grid(row=2, column=0, columnspan=2, pady=12)

        ttk.Label(
            self.sale_tab,
            text="Enter an existing Product ID and the quantity to sell."
        ).pack(anchor="w", pady=8)

        self.receipt_text = tk.Text(
            self.sale_tab, height=15, wrap="word", state="disabled"
        )
        self.receipt_text.pack(fill="both", expand=True, pady=8)

    def create_history_tab(self):
        columns = ("number", "date", "items", "total")

        self.sales_tree = ttk.Treeview(
            self.history_tab,
            columns=columns,
            show="headings",
            height=16
        )

        headings = {
            "number": "Sale #",
            "date": "Date and Time",
            "items": "Items Sold",
            "total": "Total"
        }

        for column in columns:
            self.sales_tree.heading(column, text=headings[column])
            self.sales_tree.column(column, anchor="center")

        self.sales_tree.column("number", width=80)
        self.sales_tree.column("date", width=200)
        self.sales_tree.column("items", width=400)
        self.sales_tree.column("total", width=120)

        self.sales_tree.pack(fill="both", expand=True)

        ttk.Button(
            self.history_tab,
            text="Refresh Sales History",
            command=self.refresh_sales
        ).pack(anchor="w", pady=10)

    def get_product_form(self):
        values = {
            key: entry.get().strip()
            for key, entry in self.product_fields.items()
        }

        if any(not value for value in values.values()):
            raise ValueError("Please fill in all product fields.")

        try:
            price = float(values["price"])
            quantity = int(values["quantity"])
        except ValueError:
            raise ValueError(
                "Price must be a number and quantity must be a whole number."
            )

        if price < 0:
            raise ValueError("Price cannot be negative.")

        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        return values, price, quantity

    def add_product(self):
        try:
            values, price, quantity = self.get_product_form()

            product = Product(
                values["id"],
                values["name"],
                price,
                quantity,
                values["category"]
            )

            self.store.add_product(product)
            self.refresh_inventory()
            self.clear_product_fields()

            messagebox.showinfo(
                "Success", "Product added successfully."
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror("Cannot Add Product", str(error))

    def update_product(self):
        selected = self.inventory_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Product", "Select a product to update."
            )
            return

        try:
            values, price, quantity = self.get_product_form()
            product_id = self.inventory_tree.item(
                selected[0], "values"
            )[0]

            if values["id"] != product_id:
                raise ValueError(
                    "The Product ID cannot be changed during an update."
                )

            self.store.update_product(
                product_id,
                values["name"],
                price,
                quantity,
                values["category"]
            )

            self.refresh_inventory()
            self.clear_product_fields()

            messagebox.showinfo(
                "Success", "Product updated successfully."
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror("Cannot Update Product", str(error))

    def remove_product(self):
        selected = self.inventory_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Product", "Select a product to remove."
            )
            return

        product_id = self.inventory_tree.item(
            selected[0], "values"
        )[0]

        confirmed = messagebox.askyesno(
            "Confirm Removal",
            f"Remove product {product_id}?"
        )

        if not confirmed:
            return

        try:
            self.store.remove_product(product_id)
            self.refresh_inventory()
            self.clear_product_fields()

            messagebox.showinfo(
                "Success", "Product removed successfully."
            )

        except ValueError as error:
            messagebox.showerror("Cannot Remove Product", str(error))

    def select_product(self, event=None):
        selected = self.inventory_tree.selection()

        if not selected:
            return

        values = self.inventory_tree.item(
            selected[0], "values"
        )

        field_values = {
            "id": values[0],
            "name": values[1],
            "price": values[2].replace("$", ""),
            "quantity": values[3],
            "category": values[4]
        }

        for key, value in field_values.items():
            entry = self.product_fields[key]
            entry.delete(0, tk.END)
            entry.insert(0, value)

    def clear_product_fields(self):
        for entry in self.product_fields.values():
            entry.delete(0, tk.END)

        for item in self.inventory_tree.selection():
            self.inventory_tree.selection_remove(item)

    def refresh_inventory(self, products=None):
        if products is None:
            products = self.store.inventory.get_all_products()

        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        for product in products:
            self.inventory_tree.insert(
                "",
                tk.END,
                values=(
                    product.product_id,
                    product.name,
                    f"${product.price:.2f}",
                    product.quantity,
                    product.category,
                    "Yes" if product.is_in_stock() else "No"
                )
            )

    def search_products(self):
        search_term = self.search_entry.get().strip()

        if not search_term:
            self.refresh_inventory()
            return

        results = self.store.search_product(search_term)
        self.refresh_inventory(results)

    def record_sale(self):
        product_id = self.sale_product_id.get().strip()
        quantity_text = self.sale_quantity.get().strip()

        try:
            if not product_id or not quantity_text:
                raise ValueError(
                    "Enter both a Product ID and a quantity."
                )

            quantity = int(quantity_text)
            receipt = self.store.record_sale(product_id, quantity)

            self.receipt_text.config(state="normal")
            self.receipt_text.delete("1.0", tk.END)
            self.receipt_text.insert(tk.END, receipt)
            self.receipt_text.config(state="disabled")

            self.sale_product_id.delete(0, tk.END)
            self.sale_quantity.delete(0, tk.END)

            self.refresh_inventory()
            self.refresh_sales()

            messagebox.showinfo(
                "Sale Complete", "The sale was recorded successfully."
            )

        except (ValueError, TypeError) as error:
            messagebox.showerror("Sale Failed", str(error))

    def refresh_sales(self):
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)

        for number, sale in enumerate(self.store.get_sales(), start=1):
            item_summary = ", ".join(
                f"{product.name} x {quantity}"
                for product, quantity in sale.items
            )

            self.sales_tree.insert(
                "",
                tk.END,
                values=(
                    number,
                    sale.date.strftime("%Y-%m-%d %H:%M:%S"),
                    item_summary,
                    f"${sale.calculate_total():.2f}"
                )
            )


# --------------------------------------------------
# Start Application
# --------------------------------------------------

def main():
    root = tk.Tk()
    IshunoGoodsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
