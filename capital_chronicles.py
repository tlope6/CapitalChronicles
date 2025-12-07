import tkinter as tk
from tkinter import messagebox
import hashlib
import json
import os

# -------------------------------------------------------
#  ACCOUNT SYSTEM (password hashing + JSON persistence)
# -------------------------------------------------------
ACCOUNT_FILE = "accounts.json"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def load_accounts():
    if not os.path.exists(ACCOUNT_FILE):
        return {}
    try:
        with open(ACCOUNT_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_accounts(accounts):
    with open(ACCOUNT_FILE, "w") as f:
        json.dump(accounts, f, indent=2)


# -------------------------------------------------------
#  MAIN APP CONTROLLER
# -------------------------------------------------------
class CapitalChroniclesApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("CapitalChronicles - Financial Adventure")
        self.geometry("900x650")
        self.resizable(False, False)

        # 🎨 HYBRID GRADIENT BACKGROUND
        self.gradient_canvas = tk.Canvas(self, width=900, height=650, highlightthickness=0)
        self.gradient_canvas.pack(fill="both", expand=True)
        self.draw_gradient("#f4f7ff", "#d9e4ff")  # Soft white → soft blue

        # Store user data
        self.accounts = load_accounts()
        self.current_user = None
        self.user_data = {}

        # Create a container for pages
        self.container = tk.Frame(self.gradient_canvas, bg="", highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Register frames
        self.frames = {}
        for F in (IntroFrame, AuthFrame, MenuFrame, AdventureFrame, GoalsFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("IntroFrame")

    def draw_gradient(self, color1, color2):
        """Draws a vertical gradient background."""
        for i in range(650):
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            ratio = i / 650
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.gradient_canvas.create_line(0, i, 900, i, fill=color)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    # ------------------- LOGIN / SIGN UP -------------------
    def login(self, username, password):
        if username not in self.accounts:
            messagebox.showerror("Login Failed", "User not found.")
            return

        if self.accounts[username]["password_hash"] != hash_password(password):
            messagebox.showerror("Login Failed", "Incorrect password.")
            return

        self.current_user = username
        self.user_data = self.accounts[username].get("data", {})
        self.show_frame("MenuFrame")

    def sign_up(self, username, password):
        if username in self.accounts:
            messagebox.showerror("Error", "Username already taken.")
            return

        self.accounts[username] = {
            "password_hash": hash_password(password),
            "data": {}
        }
        save_accounts(self.accounts)
        messagebox.showinfo("Success", "Account created! Please log in.")

    def save_user_data(self):
        if not self.current_user:
            return
        self.accounts[self.current_user]["data"] = self.user_data
        save_accounts(self.accounts)


# -------------------------------------------------------
#  HELPER: WHITE "CARD" CONTAINER FOR ALL PAGES
# -------------------------------------------------------
class CardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg="white",
            bd=0,
            relief="groove",
            highlightbackground="#e6e9f5",
            highlightthickness=2
        )
        self.configure(width=650, height=480)
        self.pack_propagate(False)


# -------------------------------------------------------
#  INTRO SCREEN
# -------------------------------------------------------
class IntroFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="")
        self.controller = controller

        self.card = CardFrame(self)
        self.card.pack(pady=20)

        self.title_label = tk.Label(
            self.card, text="", font=("Montserrat", 34, "bold"),
            fg="#1F3A93", bg="white"
        )
        self.title_label.pack(pady=40)

        subtitle = tk.Label(
            self.card,
            text="Scripting Your Financial Epic Adventure",
            font=("Montserrat", 14),
            fg="#1976D2",
            bg="white"
        )
        subtitle.pack(pady=10)

        start_btn = tk.Button(
            self.card,
            text="Begin Your Journey",
            font=("Montserrat", 14, "bold"),
            bg="#1976D2",
            fg="white",
            padx=20, pady=10,
            command=lambda: controller.show_frame("AuthFrame")
        )
        start_btn.pack(pady=30)

        # typewriter animation
        self.full_text = "CapitalChronicles"
        self.index = 0

    def on_show(self):
        self.title_label.config(text="")
        self.index = 0
        self.type_animation()

    def type_animation(self):
        if self.index <= len(self.full_text):
            self.title_label.config(text=self.full_text[:self.index])
            self.index += 1
            self.after(70, self.type_animation)


# -------------------------------------------------------
#  LOGIN / SIGNUP SCREEN
# -------------------------------------------------------
class AuthFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="")
        self.controller = controller

        self.card = CardFrame(self)
        self.card.pack()

        tk.Label(
            self.card,
            text="Welcome Back, Traveler",
            font=("Montserrat", 20, "bold"),
            fg="#283593",
            bg="white"
        ).pack(pady=20)

        form = tk.Frame(self.card, bg="white")
        form.pack()

        tk.Label(form, text="Username:", font=("Montserrat", 12), bg="white").grid(row=0, column=0, pady=5)
        tk.Label(form, text="Password:", font=("Montserrat", 12), bg="white").grid(row=1, column=0, pady=5)

        self.username_e = tk.Entry(form, font=("Montserrat", 12))
        self.password_e = tk.Entry(form, font=("Montserrat", 12), show="*")

        self.username_e.grid(row=0, column=1, padx=10, pady=5)
        self.password_e.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(
            self.card, text="Log In", font=("Montserrat", 12, "bold"),
            bg="#1976D2", fg="white", padx=20,
            command=self.login_user
        ).pack(pady=10)

        tk.Button(
            self.card, text="Sign Up", font=("Montserrat", 12, "bold"),
            bg="#64B5F6", fg="white", padx=20,
            command=self.sign_up_user
        ).pack()

    def login_user(self):
        self.controller.login(self.username_e.get(), self.password_e.get())

    def sign_up_user(self):
        self.controller.sign_up(self.username_e.get(), self.password_e.get())


# -------------------------------------------------------
#  MENU SCREEN
# -------------------------------------------------------
class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.card = CardFrame(self)
        self.card.pack()

        self.welcome_label = tk.Label(
            self.card,
            text="",
            font=("Montserrat", 20, "bold"),
            fg="#1E3A8A",
            bg="white"
        )
        self.welcome_label.pack(pady=20)

        tk.Button(
            self.card,
            text="Financial Adventure",
            font=("Montserrat", 13),
            bg="#1976D2", fg="white", padx=20, pady=10,
            command=lambda: controller.show_frame("AdventureFrame")
        ).pack(pady=10)

        tk.Button(
            self.card,
            text="Scripted Goals",
            font=("Montserrat", 13),
            bg="#64B5F6", fg="white", padx=20, pady=10,
            command=lambda: controller.show_frame("GoalsFrame")
        ).pack(pady=10)

        tk.Button(
            self.card,
            text="Exit",
            font=("Montserrat", 13),
            bg="#F44336", fg="white",
            padx=20, pady=10,
            command=controller.destroy
        ).pack(pady=20)

    def on_show(self):
        name = self.controller.current_user
        self.welcome_label.config(text=f"Welcome, {name}!")


# -------------------------------------------------------
#  FINANCIAL ADVENTURE SCREEN
# -------------------------------------------------------
class AdventureFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.card = CardFrame(self)
        self.card.pack()

        tk.Label(
            self.card, text="Your Financial Chapter",
            font=("Montserrat", 20, "bold"),
            fg="#283593", bg="white"
        ).pack(pady=20)

        form = tk.Frame(self.card, bg="white")
        form.pack()

        labels = ["Age:", "Job? (yes/no):", "Monthly Income ($):", "Necessities ($):"]
        self.entries = []

        for i, label in enumerate(labels):
            tk.Label(form, text=label, font=("Montserrat", 12), bg="white").grid(row=i, column=0, pady=5)
            entry = tk.Entry(form, font=("Montserrat", 12))
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries.append(entry)

        tk.Button(
            self.card,
            text="Calculate",
            font=("Montserrat", 12, "bold"),
            bg="#1976D2", fg="white", padx=20,
            command=self.calculate
        ).pack(pady=20)

        self.result = tk.Label(
            self.card, text="",
            bg="white", fg="#1E3A8A",
            font=("Montserrat", 12),
            wraplength=500
        )
        self.result.pack()

    def calculate(self):
        age = int(self.entries[0].get())
        job = self.entries[1].get().lower()
        income = float(self.entries[2].get())
        nec = float(self.entries[3].get())

        has_job = (job == "yes")
        taxes = income * 0.15 if has_job else 0
        net = income - taxes
        leftover = net - nec

        if age < 18:
            status = "Child"
        elif age <= 22:
            status = "Student"
        else:
            status = "Working Adult"

        msg = (
            f"Status: {status}\n"
            f"Income after tax: ${net:.2f}\n"
            f"Necessities: ${nec:.2f}\n"
            f"Leftover: ${leftover:.2f}\n"
        )

        self.result.config(text=msg)


# -------------------------------------------------------
#  GOALS SCREEN (placeholder)
# -------------------------------------------------------
class GoalsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.card = CardFrame(self)
        self.card.pack()

        tk.Label(
            self.card, text="Scripted Goals",
            font=("Montserrat", 20, "bold"), fg="#283593", bg="white"
        ).pack(pady=20)

        tk.Label(
            self.card,
            text="Goal system coming soon.",
            font=("Montserrat", 12),
            fg="#1E3A8A",
            bg="white"
        ).pack()

