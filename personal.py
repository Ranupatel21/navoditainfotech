# Create a project directory and set up a virtual environment.
mkdir finance_manager
cd finance_manager
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
# Create a file named finance_manager.py.
# finance_manager.py

import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt

class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.data = pd.DataFrame(columns=["Type", "Category", "Amount"])
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Type:").grid(row=0, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar(value="Expense")
        tk.OptionMenu(self.frame, self.type_var, "Expense", "Income").grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(self.frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(self.frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.frame, text="Add Entry", command=self.add_entry)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.summary_button = tk.Button(self.frame, text="View Summary", command=self.view_summary)
        self.summary_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.visualize_button = tk.Button(self.frame, text="Visualize Data", command=self.visualize_data)
        self.visualize_button.grid(row=5, column=0, columnspan=2, pady=10)

    def add_entry(self):
        entry_type = self.type_var.get()
        category = self.category_entry.get()
        try:
            amount = float(self.amount_entry.get())
            new_entry = {"Type": entry_type, "Category": category, "Amount": amount}
            self.data = self.data.append(new_entry, ignore_index=True)
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Entry added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered. Please enter a numeric value.")

    def view_summary(self):
        income = self.data[self.data["Type"] == "Income"]["Amount"].sum()
        expenses = self.data[self.data["Type"] == "Expense"]["Amount"].sum()
        summary = f"Total Income: ${income:.2f}\nTotal Expenses: ${expenses:.2f}\nNet Savings: ${income - expenses:.2f}"
        messagebox.showinfo("Summary", summary)

    def visualize_data(self):
        if self.data.empty:
            messagebox.showinfo("No Data", "No data available to visualize.")
            return

        fig, axs = plt.subplots(2, 1, figsize=(10, 8))
        
        # Pie chart for income and expenses
        type_data = self.data.groupby("Type")["Amount"].sum()
        axs[0].pie(type_data, labels=type_data.index, autopct='%1.1f%%', startangle=140)
        axs[0].set_title("Income vs Expenses")

        # Bar chart for category-wise distribution
        category_data = self.data.groupby(["Type", "Category"])["Amount"].sum().unstack().fillna(0)
        category_data.plot(kind='bar', stacked=True, ax=axs[1])
        axs[1].set_title("Category-wise Distribution")
        axs[1].set_ylabel("Amount")

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManager(root)
    root.mainloop()
python finance_manager.py

