import customtkinter as ctk
from tkinter import messagebox
from dashboard import Dashboard


class LoginWindow:

    def __init__(self):

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()
        self.window.title("ShopSmart Login")
        self.window.geometry("500x450")
        self.window.resizable(False, False)

        ctk.CTkLabel(
            self.window,
            text="🛒 ShopSmart",
            font=("Arial", 30, "bold")
        ).pack(pady=25)

        ctk.CTkLabel(
            self.window,
            text="Smart Purchase Optimizer",
            font=("Arial", 18)
        ).pack()

        self.username = ctk.CTkEntry(
            self.window,
            width=280,
            placeholder_text="Username"
        )
        self.username.pack(pady=20)

        self.password = ctk.CTkEntry(
            self.window,
            width=280,
            placeholder_text="Password",
            show="*"
        )
        self.password.pack()

        self.show_password = ctk.CTkCheckBox(
            self.window,
            text="Show Password",
            command=self.toggle_password
        )
        self.show_password.pack(pady=10)

        ctk.CTkButton(
            self.window,
            text="Login",
            width=280,
            command=self.login
        ).pack(pady=15)

        ctk.CTkButton(
            self.window,
            text="Exit",
            width=280,
            fg_color="red",
            hover_color="darkred",
            command=self.window.destroy
        ).pack()

    def toggle_password(self):

        if self.show_password.get() == 1:
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    def login(self):

        username = self.username.get().strip()
        password = self.password.get().strip()

        if username == "" or password == "":
            messagebox.showerror(
                "Error",
                "Please enter Username and Password."
            )
            return

        if username == "admin" and password == "admin123":

            self.window.destroy()

            dashboard = Dashboard()
            dashboard.run()

        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password."
            )

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    LoginWindow().run()