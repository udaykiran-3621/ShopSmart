import customtkinter as ctk
from tkinter import messagebox
import json
import os
from storage import load_products

BUDGET_FILE = "budget.json"


class BudgetTracker:

    def __init__(self):

        self.window = ctk.CTkToplevel()
        self.window.title("Budget Tracker")
        self.window.geometry("700x500")
        self.window.resizable(False, False)

        self.total_budget = 0

        self.create_file()
        self.load_budget()

        self.build_ui()

    def create_file(self):

        if not os.path.exists(BUDGET_FILE):

            with open(BUDGET_FILE, "w") as file:

                json.dump(
                    {
                        "budget": 0
                    },
                    file,
                    indent=4
                )

    def load_budget(self):

        with open(BUDGET_FILE, "r") as file:

            data = json.load(file)

            self.total_budget = float(data.get("budget", 0))

    def save_budget(self):

        with open(BUDGET_FILE, "w") as file:

            json.dump(
                {
                    "budget": self.total_budget
                },
                file,
                indent=4
            )

    def total_spent(self):

        products = load_products()

        total = 0

        for product in products:

            try:

                price = float(product["price"])
                qty = int(product["quantity"])

                total += price * qty

            except (ValueError, KeyError):
                pass

        return total

    def remaining_budget(self):

        return self.total_budget - self.total_spent()

    def build_ui(self):

        title = ctk.CTkLabel(
            self.window,
            text="Monthly Budget Tracker",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=20)

        self.budget_entry = ctk.CTkEntry(
            self.window,
            width=250,
            placeholder_text="Enter Monthly Budget"
        )
        self.budget_entry.pack(pady=10)

        if self.total_budget > 0:
            self.budget_entry.insert(
                0,
                str(self.total_budget)
            )

        save_btn = ctk.CTkButton(
            self.window,
            text="Save Budget",
            width=200,
            command=self.update_budget
        )
        save_btn.pack(pady=10)

        refresh_btn = ctk.CTkButton(
            self.window,
            text="Refresh",
            width=200,
            command=self.refresh
        )
        refresh_btn.pack(pady=5)

        self.spent_label = ctk.CTkLabel(
            self.window,
            text="",
            font=("Arial", 18)
        )
        self.spent_label.pack(pady=10)

        self.remaining_label = ctk.CTkLabel(
            self.window,
            text="",
            font=("Arial", 18)
        )
        self.remaining_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self.window,
            text="",
            font=("Arial", 18, "bold")
        )
        self.status_label.pack(pady=10)

        self.progress = ctk.CTkProgressBar(
            self.window,
            width=450
        )
        self.progress.pack(pady=20)

        self.progress.set(0)

        self.refresh()

    def update_budget(self):

        try:

            self.total_budget = float(
                self.budget_entry.get()
            )

            self.save_budget()

            messagebox.showinfo(
                "Success",
                "Budget Saved Successfully"
            )

            self.refresh()

        except ValueError:

            messagebox.showerror(
                "Error",
                "Please enter a valid budget amount."
            )

    def refresh(self):

        spent = self.total_spent()
        remaining = self.remaining_budget()

        self.spent_label.configure(
            text=f"Total Spent : ₹{spent:.2f}"
        )

        self.remaining_label.configure(
            text=f"Remaining Budget : ₹{remaining:.2f}"
        )

        if self.total_budget <= 0:

            self.progress.set(0)

            self.status_label.configure(
                text="Set your monthly budget.",
                text_color="yellow"
            )

            return

        percent = min(spent / self.total_budget, 1)

        self.progress.set(percent)

        if remaining < 0:

            self.status_label.configure(
                text="Budget Exceeded!",
                text_color="red"
            )

        elif remaining <= self.total_budget * 0.2:

            self.status_label.configure(
                text="Warning: Budget Almost Finished",
                text_color="orange"
            )

        else:

            self.status_label.configure(
                text="Within Budget",
                text_color="green"
            )


# -----------------------------
# Open Budget Window
# -----------------------------
def open_budget_tracker():
    tracker = BudgetTracker()
    return tracker


# -----------------------------
# Run File Directly
# -----------------------------
if __name__ == "__main__":

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.withdraw()

    BudgetTracker()

    root.mainloop()