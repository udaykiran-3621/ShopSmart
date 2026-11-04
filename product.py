import customtkinter as ctk
from tkinter import messagebox
from storage import load_products, save_products


def open_add_product():

    window = ctk.CTkToplevel()
    window.title("Add Product")
    window.geometry("450x500")

    ctk.CTkLabel(
        window,
        text="Add New Product",
        font=("Arial", 22, "bold")
    ).pack(pady=15)

    name = ctk.CTkEntry(window, placeholder_text="Product Name")
    name.pack(pady=8)

    category = ctk.CTkEntry(window, placeholder_text="Category")
    category.pack(pady=8)

    store = ctk.CTkEntry(window, placeholder_text="Store Name")
    store.pack(pady=8)

    price = ctk.CTkEntry(window, placeholder_text="Price")
    price.pack(pady=8)

    quantity = ctk.CTkEntry(window, placeholder_text="Quantity")
    quantity.pack(pady=8)

    def save():

        if name.get() == "":
            messagebox.showerror("Error", "Enter Product Name")
            return

        product = {
            "name": name.get(),
            "category": category.get(),
            "store": store.get(),
            "price": price.get(),
            "quantity": quantity.get()
        }

        products = load_products()
        products.append(product)
        save_products(products)

        messagebox.showinfo("Success", "Product Saved Successfully")
        window.destroy()

    ctk.CTkButton(
        window,
        text="Save Product",
        command=save
    ).pack(pady=20)


def open_view_products():

    window = ctk.CTkToplevel()
    window.title("View Products")
    window.geometry("700x500")

    ctk.CTkLabel(
        window,
        text="Saved Products",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    products = load_products()

    if len(products) == 0:
        ctk.CTkLabel(
            window,
            text="No Products Found"
        ).pack(pady=20)
        return

    textbox = ctk.CTkTextbox(window, width=650, height=350)
    textbox.pack(pady=10)

    textbox.insert("end",
        "Name\tCategory\tStore\tPrice\tQty\n")
    textbox.insert("end",
        "-" * 70 + "\n")

    for p in products:

        textbox.insert(
            "end",
            f"{p['name']}\t{p['category']}\t{p['store']}\t₹{p['price']}\t{p['quantity']}\n"
        )

    textbox.configure(state="disabled")

def show_products(parent):

    # Clear previous widgets
    for widget in parent.winfo_children():
        widget.destroy()

    ctk.CTkLabel(
        parent,
        text="Saved Products",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    products = load_products()

    if not products:
        ctk.CTkLabel(
            parent,
            text="No Products Found",
            font=("Arial", 16)
        ).pack(pady=20)
        return

    frame = ctk.CTkScrollableFrame(parent)
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    header = ctk.CTkLabel(
        frame,
        text=f"{'Name':20}{'Category':15}{'Store':15}{'Price':10}{'Qty':8}",
        font=("Arial", 16, "bold"),
        anchor="w"
    )
    header.pack(fill="x", pady=5)

    for p in products:

        text = (
            f"{p['name'][:18]:20}"
            f"{p['category'][:13]:15}"
            f"{p['store'][:13]:15}"
            f"₹{p['price']:8}"
            f"{p['quantity']:>6}"
        )

        ctk.CTkLabel(
            frame,
            text=text,
            font=("Consolas", 13),
            anchor="w"
        ).pack(fill="x", pady=2)