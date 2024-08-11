import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Database connection
def connect_db():
    conn = sqlite3.connect('billing.db')
    return conn

# Database setup
def setup_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        description TEXT,
                        price REAL NOT NULL,
                        stock INTEGER NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
                        customer_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        contact TEXT,
                        address TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Transactions (
                        transaction_id INTEGER PRIMARY KEY,
                        customer_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        total REAL NOT NULL,
                        FOREIGN KEY(customer_id) REFERENCES Customers(customer_id),
                        FOREIGN KEY(product_id) REFERENCES Products(product_id))''')
    conn.commit()
    conn.close()

# Functions for product management
def add_product(name, description, price, stock):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (name, description, price, stock) VALUES (?, ?, ?, ?)", (name, description, price, stock))
    conn.commit()
    conn.close()

def get_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE product_id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

# Functions for customer management
def add_customer(name, contact, address):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Customers (name, contact, address) VALUES (?, ?, ?)", (name, contact, address))
    conn.commit()
    conn.close()

def get_customers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customers")
    customers = cursor.fetchall()
    conn.close()
    return customers

# Functions for transaction management
def add_transaction(customer_id, product_id, quantity, date, total):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Transactions (customer_id, product_id, quantity, date, total) VALUES (?, ?, ?, ?, ?)",
                   (customer_id, product_id, quantity, date, total))
    conn.commit()
    conn.close()

def generate_invoice(transaction_id, customer_name, products, total_amount):
    c = canvas.Canvas(f"invoice_{transaction_id}.pdf", pagesize=A4)
    width, height = A4
    c.drawString(100, height - 100, f"Invoice #{transaction_id}")
    c.drawString(100, height - 120, f"Customer: {customer_name}")
    y = height - 160
    for product, qty, price in products:
        c.drawString(100, y, f"{product}: {qty} x {price}")
        y -= 20
    c.drawString(100, y, f"Total: {total_amount}")
    c.save()

# GUI setup
class BillingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Billing Software")
        self.geometry("800x600")

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, expand=True)

        # Product Management Tab
        self.products_frame = ttk.Frame(self.notebook, width=800, height=400)
        self.products_frame.pack(fill='both', expand=True)
        self.notebook.add(self.products_frame, text='Products')
        self.setup_products_tab()

        # Customer Management Tab
        self.customers_frame = ttk.Frame(self.notebook, width=800, height=400)
        self.customers_frame.pack(fill='both', expand=True)
        self.notebook.add(self.customers_frame, text='Customers')
        self.setup_customers_tab()

        # Sales Tab
        self.sales_frame = ttk.Frame(self.notebook, width=800, height=400)
        self.sales_frame.pack(fill='both', expand=True)
        self.notebook.add(self.sales_frame, text='Sales')
        self.setup_sales_tab()

        # Invoice Tab
        self.invoice_frame = ttk.Frame(self.notebook, width=800, height=400)
        self.invoice_frame.pack(fill='both', expand=True)
        self.notebook.add(self.invoice_frame, text='Invoice')
        self.setup_invoice_tab()

    def setup_products_tab(self):
        # Entry fields
        self.prod_name_var = tk.StringVar()
        self.prod_desc_var = tk.StringVar()
        self.prod_price_var = tk.StringVar()
        self.prod_stock_var = tk.StringVar()

        tk.Label(self.products_frame, text="Product Name").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.products_frame, textvariable=self.prod_name_var).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self.products_frame, text="Description").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.products_frame, textvariable=self.prod_desc_var).grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self.products_frame, text="Price").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.products_frame, textvariable=self.prod_price_var).grid(row=2, column=1, padx=10, pady=10)
        
        tk.Label(self.products_frame, text="Stock").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.products_frame, textvariable=self.prod_stock_var).grid(row=3, column=1, padx=10, pady=10)

        # Add product button
        tk.Button(self.products_frame, text="Add Product", command=self.add_product).grid(row=4, column=1, padx=10, pady=10)

        # Display product list
        self.product_list = tk.Listbox(self.products_frame, width=50, height=10)
        self.product_list.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.refresh_product_list()

    def setup_customers_tab(self):
        # Entry fields
        self.cust_name_var = tk.StringVar()
        self.cust_contact_var = tk.StringVar()
        self.cust_address_var = tk.StringVar()

        tk.Label(self.customers_frame, text="Customer Name").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.customers_frame, textvariable=self.cust_name_var).grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self.customers_frame, text="Contact").grid(row=1, column=0, padx=10, pady=10)
        tk.Entry(self.customers_frame, textvariable=self.cust_contact_var).grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self.customers_frame, text="Address").grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.customers_frame, textvariable=self.cust_address_var).grid(row=2, column=1, padx=10, pady=10)

        # Add customer button
        tk.Button(self.customers_frame, text="Add Customer", command=self.add_customer).grid(row=3, column=1, padx=10, pady=10)

        # Display customer list
        self.customer_list = tk.Listbox(self.customers_frame, width=50, height=10)
        self.customer_list.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.refresh_customer_list()

    def setup_sales_tab(self):
        # Select customer
        tk.Label(self.sales_frame, text="Select Customer").grid(row=0, column=0, padx=10, pady=10)
        self.customer_var = tk.StringVar()
        self.customer_dropdown = ttk.Combobox(self.sales_frame, textvariable=self.customer_var)
        self.customer_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.refresh_customer_dropdown()

        # Select product
        tk.Label(self.sales_frame, text="Select Product").grid(row=1, column=0, padx=10, pady=10)
        self.product_var = tk.StringVar()
        self.product_dropdown = ttk.Combobox(self.sales_frame, textvariable=self.product_var)
        self.product_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.refresh_product_dropdown()

        # Enter quantity
        tk.Label(self.sales_frame, text="Quantity").grid(row=2, column=0, padx=10, pady=10)
        self.quantity_var = tk.StringVar()
        tk.Entry(self.sales_frame, textvariable=self.quantity_var).grid(row=2, column=1, padx=10, pady=10)

        # Add to transaction button
        tk.Button(self.sales_frame, text="Add to Transaction", command=self.add_to_transaction).grid(row=3, column=1, padx=10, pady=10)

        # Display transaction summary
        self.transaction_list = tk.Listbox(self.sales_frame, width=50, height=10)
        self.transaction_list.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.transaction_items = []

    def setup_invoice_tab(self):
        tk.Label(self.invoice_frame, text="Transaction Summary").pack(pady=10)
        self.invoice_text = tk.Text(self.invoice_frame, width=70, height=15)
        self.invoice_text.pack(pady=10)

        # Generate invoice button
        tk.Button(self.invoice_frame, text="Generate Invoice", command=self.generate_invoice).pack(pady=10)

    def add_product(self):
        name = self.prod_name_var.get()
        description = self.prod_desc_var.get()
        price = float(self.prod_price_var.get())
        stock = int(self.prod_stock_var.get())
        add_product(name, description, price, stock)
        self.refresh_product_list()

    def refresh_product_list(self):
        self.product_list.delete(0, tk.END)
        products = get_products()
        for product in products:
            self.product_list.insert(tk.END, f"{product[0]} - {product[1]} - {product[2]} - {product[3]} - {product[4]}")

    def add_customer(self):
        name = self.cust_name_var.get()
        contact = self.cust_contact_var.get()
        address = self.cust_address_var.get()
        add_customer(name, contact, address)
        self.refresh_customer_list()
        self.refresh_customer_dropdown()

    def refresh_customer_list(self):
        self.customer_list.delete(0, tk.END)
        customers = get_customers()
        for customer in customers:
            self.customer_list.insert(tk.END, f"{customer[0]} - {customer[1]} - {customer[2]} - {customer[3]}")

    def refresh_customer_dropdown(self):
        customers = get_customers()
        self.customer_dropdown['values'] = [f"{customer[1]}" for customer in customers]

    def refresh_product_dropdown(self):
        products = get_products()
        self.product_dropdown['values'] = [f"{product[1]}" for product in products]

    def add_to_transaction(self):
        customer_name = self.customer_var.get()
        product_name = self.product_var.get()
        quantity = int(self.quantity_var.get())
        
        product = next((p for p in get_products() if p[1] == product_name), None)
        if product:
            price = product[3]
            self.transaction_items.append((product_name, quantity, price))
            self.transaction_list.insert(tk.END, f"{product_name} - {quantity} x {price}")

    def generate_invoice(self):
        customer_name = self.customer_var.get()
        total_amount = sum([qty * price for _, qty, price in self.transaction_items])
        transaction_id = len(self.transaction_items) + 1  # Simplified transaction ID logic
        generate_invoice(transaction_id, customer_name, self.transaction_items, total_amount)
        self.invoice_text.insert(tk.END, f"Invoice #{transaction_id}\nCustomer: {customer_name}\n")
        for item in self.transaction_items:
            self.invoice_text.insert(tk.END, f"{item[0]}: {item[1]} x {item[2]}\n")
        self.invoice_text.insert(tk.END, f"Total: {total_amount}\n")

# Run the application
if __name__ == "__main__":
    #setup_db()   Set up the database
    app = BillingApp()
    app.mainloop()
