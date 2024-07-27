import tkinter as tk
from tkinter import ttk, messagebox
import requests

def get_exchange_rates():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    data = response.json()
    return data['rates']

def convert_currency(amount, rate):
    return amount * rate

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USD Currency Converter")

        self.amount_label = tk.Label(root, text="Amount in USD:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10)

        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_button.grid(row=0, column=2, padx=10, pady=10)

        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.currency_label = tk.Label(root, text="Select Currency:")
        self.currency_label.grid(row=2, column=0, padx=10, pady=10)

        self.currency_combobox = ttk.Combobox(root)
        self.currency_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.rates = get_exchange_rates()
        self.currency_combobox['values'] = list(self.rates.keys())

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            currency = self.currency_combobox.get()
            if currency:
                rate = self.rates[currency]
                converted_amount = convert_currency(amount, rate)
                self.result_label.config(text=f"{amount} USD = {converted_amount:.2f} {currency}")
            else:
                messagebox.showwarning("Input Error", "Please select a currency.")
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid amount.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
