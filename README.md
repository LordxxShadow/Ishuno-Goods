
# Ishuno Goods — Inventory and Sales Management System

## Project Description

Ishuno Goods is a Python application designed to help a small retail business manage products, track inventory, and record sales transactions. The application uses a graphical user interface built with Tkinter.

## Features

- Add, update, remove, and search for products.
- View product details, prices, quantities, and stock status.
- Record sales and calculate transaction totals.
- Automatically update inventory quantities after sales.
- Display receipts and maintain a sales history.
- Prevent sales when there is insufficient stock.

## Technologies Used

- Python 3
- Tkinter
- Object-oriented programming
- Lists, tuples, and dictionaries

## Main Classes

- **Product:** Stores product information and provides product details.
- **Inventory:** Manages the collection of products.
- **Sale:** Calculates transaction totals and generates receipts.
- **StoreSystem:** Coordinates inventory operations and records sales.
- **IshunoGoodsApp:** Provides the graphical user interface.

## How to Run

1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   `python main.py`

Tkinter is included with many standard Python installations.

## Testing

The application was launched successfully and tested with a sample product.

The tests confirmed that:
- A product can be added to inventory.
- A sale of two T-shirts priced at $24.99 each produces a total of $49.98.
- Inventory decreases from 10 units to 8 after the sale.
- The transaction appears in sales history.
- A sale exceeding available stock is rejected.

## Project Documentation

The project proposal and UML class diagram were prepared during the earlier project milestones. These documents should be included with the final submission as supporting documentation.
