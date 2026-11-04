import customtkinter as ctk
from storage import load_products


def open_reports():

    window = ctk.CTkToplevel()
    window.title("ShopSmart - Reports")
    window.geometry("750x600")
    window.resizable(False, False)

    products = load_products()

    # Calculate statistics
    total_products = len(products)
    total_spending = 0
    total_quantity = 0
    categories = {}

    for p in products:

        try:
            price = float(p.get("price", 0))
            quantity = int(p.get("quantity", 0))

            amount = price * quantity

            total_spending += amount
            total_quantity += quantity

            category = p.get("category", "Others")

            categories[category] = (
                categories.get(category, 0) + amount
            )

        except (ValueError, TypeError):
            continue

    # Title
    ctk.CTkLabel(
        window,
        text="SHOPSMART REPORTS",
        font=("Arial", 28, "bold")
    ).pack(pady=25)

    # Summary
    summary = ctk.CTkFrame(window)
    summary.pack(fill="x", padx=30, pady=15)

    details = [
        ("Total Products", total_products),
        ("Total Quantity", total_quantity),
        ("Total Spending", f"₹{total_spending:.2f}"),
        ("Total Categories", len(categories))
    ]

    for title, value in details:

        card = ctk.CTkFrame(summary)
        card.pack(fill="x", padx=15, pady=8)

        ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=20, pady=12)

        ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 18, "bold"),
            text_color="#D4AF37"
        ).pack(side="right", padx=20)

    # Category Report
    ctk.CTkLabel(
        window,
        text="Category-wise Spending",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    textbox = ctk.CTkTextbox(
        window,
        width=650,
        height=150
    )
    textbox.pack(padx=20, pady=10)

    if categories:

        for category, amount in categories.items():

            textbox.insert(
                "end",
                f"{category} : ₹{amount:.2f}\n"
            )

    else:
        textbox.insert("end", "No purchase data available.")

    textbox.configure(state="disabled")

    # Close Button
    ctk.CTkButton(
        window,
        text="Close",
        command=window.destroy,
        width=150
    ).pack(pady=15)