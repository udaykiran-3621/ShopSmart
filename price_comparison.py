import customtkinter as ctk
from storage import load_products


def open_price_comparison():

    window = ctk.CTkToplevel()
    window.title("ShopSmart - Price Comparison")
    window.geometry("850x600")
    window.resizable(False, False)

    products = load_products()

    ctk.CTkLabel(
        window,
        text="PRICE COMPARISON",
        font=("Arial", 28, "bold")
    ).pack(pady=20)

    # Search field
    search_entry = ctk.CTkEntry(
        window,
        width=350,
        placeholder_text="Enter Product Name"
    )
    search_entry.pack(pady=10)

    result_frame = ctk.CTkScrollableFrame(
        window,
        width=750,
        height=300
    )
    result_frame.pack(padx=20, pady=15, fill="both", expand=True)

    result_label = ctk.CTkLabel(
        window,
        text="Search for a product to compare prices.",
        font=("Arial", 17, "bold")
    )
    result_label.pack(pady=15)

    def compare():

        for widget in result_frame.winfo_children():
            widget.destroy()

        keyword = search_entry.get().strip().lower()

        if not keyword:
            result_label.configure(
                text="Please enter a product name."
            )
            return

        matches = []

        for p in products:

            if keyword in p.get("name", "").lower():

                try:
                    price = float(p["price"])

                    matches.append({
                        "name": p["name"],
                        "store": p["store"],
                        "price": price
                    })

                except (ValueError, TypeError, KeyError):
                    continue

        if not matches:

            result_label.configure(
                text="No matching products found."
            )
            return

        matches.sort(key=lambda x: x["price"])

        ctk.CTkLabel(
            result_frame,
            text="PRODUCT       STORE       PRICE",
            font=("Arial", 17, "bold")
        ).pack(pady=10)

        for p in matches:

            ctk.CTkLabel(
                result_frame,
                text=f"{p['name']}       {p['store']}       ₹{p['price']:.2f}",
                font=("Arial", 15)
            ).pack(pady=8)

        cheapest = matches[0]
        highest = matches[-1]

        savings = highest["price"] - cheapest["price"]

        if len(matches) == 1:

            result_label.configure(
                text=f"Lowest recorded price: ₹{cheapest['price']:.2f} at {cheapest['store']}. Add the same product from another store to compare."
            )

        else:

            result_label.configure(
                text=(
                    f"🏆 Best Price: {cheapest['store']} "
                    f"– ₹{cheapest['price']:.2f}\n"
                    f"💰 Potential Savings: ₹{savings:.2f}"
                ),
                text_color="#D4AF37"
            )

    ctk.CTkButton(
        window,
        text="Compare Prices",
        width=200,
        command=compare
    ).pack(pady=10)