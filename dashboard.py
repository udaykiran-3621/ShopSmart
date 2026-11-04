import customtkinter as ctk
from tkinter import messagebox
import json
import os

from storage import (
    load_products,
    total_products,
    total_amount,
    save_products
)

from product import open_add_product, show_products
from budget import open_budget_tracker
from report import open_reports
from price_comparison import open_price_comparison


class Dashboard:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("ShopSmart Dashboard")
        self.app.geometry("1200x700")
        self.app.resizable(False, False)

        # ==========================
        # Sidebar
        # ==========================

        sidebar = ctk.CTkFrame(
            self.app,
            width=220,
            corner_radius=0
        )

        sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            sidebar,
            text="🛒 ShopSmart",
            font=("Arial", 26, "bold")
        ).pack(pady=25)

        # Dashboard Button

        ctk.CTkButton(
            sidebar,
            text="🏠 Dashboard",
            command=self.show_dashboard
        ).pack(pady=8, padx=20, fill="x")

        # Add Product

        ctk.CTkButton(
            sidebar,
            text="➕ Add Product",
            command=open_add_product
        ).pack(pady=8, padx=20, fill="x")

        # View Products

        ctk.CTkButton(
            sidebar,
            text="📦 View Products",
            command=lambda: show_products(self.content)
        ).pack(pady=8, padx=20, fill="x")

        # Budget Tracker

        ctk.CTkButton(
            sidebar,
            text="💰 Budget Tracker",
            command=open_budget_tracker
        ).pack(pady=8, padx=20, fill="x")

        # Price Comparison

        ctk.CTkButton(
            sidebar,
            text="💲 Price Comparison",
            command=open_price_comparison
        ).pack(pady=8, padx=20, fill="x")

        # Reports

        ctk.CTkButton(
            sidebar,
            text="📊 Reports",
            command=open_reports
        ).pack(pady=8, padx=20, fill="x")

        # Settings

        ctk.CTkButton(
            sidebar,
            text="⚙ Settings",
            command=self.open_settings
        ).pack(pady=8, padx=20, fill="x")

        # Exit

        ctk.CTkButton(
            sidebar,
            text="❌ Exit",
            fg_color="red",
            hover_color="darkred",
            command=self.app.destroy
        ).pack(
            side="bottom",
            pady=20,
            padx=20,
            fill="x"
        )

        # ==========================
        # Main Content
        # ==========================

        self.content = ctk.CTkFrame(self.app)

        self.content.pack(
            side="right",
            expand=True,
            fill="both",
            padx=20,
            pady=20
        )

        self.show_dashboard()

    # ==========================
    # Dashboard Screen
    # ==========================

    def show_dashboard(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        # Load Product Data

        product_count = total_products()
        spending = total_amount()

        # Load Monthly Budget

        budget = 0

        if os.path.exists("budget.json"):

            try:

                with open("budget.json", "r") as file:

                    data = json.load(file)

                    budget = float(
                        data.get("budget", 0)
                    )

            except (ValueError, TypeError, OSError):

                budget = 0

        remaining = budget - spending

        # Dashboard Heading

        ctk.CTkLabel(
            self.content,
            text="Welcome to ShopSmart",
            font=("Arial", 30, "bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self.content,
            text="Smart Purchase Optimizer",
            font=("Arial", 18)
        ).pack()

        # Dashboard Cards

        cards = ctk.CTkFrame(self.content)

        cards.pack(pady=30)

        self.create_card(
            cards,
            "📦 Total Products",
            str(product_count),
            0,
            0
        )

        self.create_card(
            cards,
            "💰 Total Cost",
            f"₹{spending:.2f}",
            0,
            1
        )

        self.create_card(
            cards,
            "📈 Monthly Budget",
            f"₹{budget:.2f}",
            1,
            0
        )

        self.create_card(
            cards,
            "💵 Remaining Budget",
            f"₹{remaining:.2f}",
            1,
            1
        )

    # ==========================
    # Dashboard Cards
    # ==========================

    def create_card(
        self,
        parent,
        title,
        value,
        row,
        column
    ):

        frame = ctk.CTkFrame(
            parent,
            width=250,
            height=140
        )

        frame.grid(
            row=row,
            column=column,
            padx=20,
            pady=20
        )

        frame.grid_propagate(False)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 16, "bold")
        ).pack(pady=15)

        ctk.CTkLabel(
            frame,
            text=value,
            font=("Arial", 28)
        ).pack()

    # ==========================
    # Settings Window
    # ==========================

    def open_settings(self):

        window = ctk.CTkToplevel(self.app)

        window.title("ShopSmart Settings")
        window.geometry("500x500")
        window.resizable(False, False)

        ctk.CTkLabel(
            window,
            text="SETTINGS",
            font=("Arial", 28, "bold")
        ).pack(pady=25)

        # Appearance Mode

        ctk.CTkLabel(
            window,
            text="Appearance Mode",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        appearance = ctk.CTkOptionMenu(
            window,
            values=["Dark", "Light", "System"],
            command=ctk.set_appearance_mode
        )

        appearance.set(
            ctk.get_appearance_mode()
        )

        appearance.pack(pady=10)

        # About ShopSmart

        def about():

            messagebox.showinfo(
                "About ShopSmart",

                "ShopSmart - Smart Purchase Optimizer\n\n"

                "A smart shopping management application.\n\n"

                "Features:\n"

                "1. Product Management\n"
                "2. Budget Tracking\n"
                "3. Price Comparison\n"
                "4. Purchase Reports\n\n"

                "Developed using Python and CustomTkinter.",

                parent=window
            )

        ctk.CTkButton(
            window,
            text="About ShopSmart",
            width=220,
            command=about
        ).pack(pady=20)

        # Reset Application Data

        def reset_data():

            confirm = messagebox.askyesno(
                "Confirm Reset",

                "Are you sure you want to delete all products "
                "and reset your monthly budget?",

                parent=window
            )

            if confirm:

                try:

                    # Clear Products

                    save_products([])

                    # Reset Budget

                    with open("budget.json", "w") as file:

                        json.dump(
                            {"budget": 0},
                            file,
                            indent=4
                        )

                    messagebox.showinfo(
                        "Success",
                        "All application data reset successfully.",
                        parent=window
                    )

                    self.show_dashboard()

                except OSError as error:

                    messagebox.showerror(
                        "Error",
                        f"Unable to reset data:\n{error}",
                        parent=window
                    )

        ctk.CTkButton(
            window,
            text="Reset All Data",
            width=220,
            fg_color="red",
            hover_color="darkred",
            command=reset_data
        ).pack(pady=15)

        # Close Button

        ctk.CTkButton(
            window,
            text="Close",
            width=220,
            command=window.destroy
        ).pack(pady=15)

    # ==========================
    # Run Dashboard
    # ==========================

    def run(self):

        self.app.mainloop()


# ==========================
# Run Directly
# ==========================

if __name__ == "__main__":

    Dashboard().run()