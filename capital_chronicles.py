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

        # Background gradient canvas
        self.gradient_canvas = tk.Canvas(self, width=900, height=650, highlightthickness=0)
        self.gradient_canvas.pack(fill="both", expand=True)
        self.draw_gradient("#f4f7ff", "#d9e4ff")

        # Store user data
        self.accounts = load_accounts()
        self.current_user = None
        self.user_data = {}

        # Frame container for pages
        self.container = tk.Frame(self.gradient_canvas, bg="", highlightthickness=0)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Register app screens
        self.frames = {}
        for F in (IntroFrame, AuthFrame, MenuFrame, AdventureFrame, GoalsFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("IntroFrame")

    def draw_gradient(self, color1, color2):
        for i in range(650):
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            ratio = i / 650
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            self.gradient_canvas.create_line(0, i, 900, i, fill=f"#{r:02x}{g:02x}{b:02x}")

    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    # Login system ---------------------------------------------------
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
# Shared Card Frame (white box)
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
# Intro Screen
# -------------------------------------------------------
class IntroFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.card = CardFrame(self)
        self.card.pack(pady=40)

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

        tk.Button(
            self.card,
            text="Begin Your Journey",
            font=("Montserrat", 14, "bold"),
            bg="#1976D2",
            fg="white",
            padx=20, pady=10,
            command=lambda: controller.show_frame("AuthFrame")
        ).pack(pady=30)

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
# Login / Signup Screen
# -------------------------------------------------------
class AuthFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.card = CardFrame(self)
        self.card.pack(pady=40)

        tk.Label(
            self.card,
            text="Welcome Back, Traveler",
            font=("Montserrat", 20, "bold"),
            fg="#283593", bg="white"
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
# Menu Screen
# -------------------------------------------------------
class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.card = CardFrame(self)
        self.card.pack(pady=40)

        self.welcome_label = tk.Label(
            self.card,
            text="", font=("Montserrat", 20, "bold"),
            fg="#1E3A8A", bg="white"
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
# Adventure Calculator
# -------------------------------------------------------
class AdventureFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.card = CardFrame(self)
        self.card.pack(pady=40)

        tk.Label(
            self.card, text="Your Financial Chapter",
            font=("Montserrat", 20, "bold"), fg="#283593", bg="white"
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

        tk.Button(
            self.card,
            text="Back",
            font=("Montserrat", 12, "bold"),
            bg="#F44336", fg="white",
            padx=20, pady=5,
            command=lambda: controller.show_frame("MenuFrame")
        ).pack(pady=10)

        self.result = tk.Label(
            self.card, text="", bg="white", fg="#1E3A8A",
            font=("Montserrat", 12), wraplength=500
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

        status = (
            "Child" if age < 18 else
            "Student" if age <= 22 else
            "Working Adult"
        )

        msg = (
            f"Status: {status}\n"
            f"Income after tax: ${net:.2f}\n"
            f"Necessities: ${nec:.2f}\n"
            f"Leftover: ${leftover:.2f}\n"
        )

        self.result.config(text=msg)


# -------------------------------------------------------
# Goals / Quest System
# -------------------------------------------------------
class GoalsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Card starts lower for animation
        self.card = CardFrame(self)
        self.card.pack(pady=40)

        tk.Label(
            self.card, text="Scripted Quests",
            font=("Montserrat", 20, "bold"), fg="#283593", bg="white"
        ).pack(pady=10)

        tk.Label(
            self.card,
            text="Track your financial quests and mark them as completed.",
            font=("Montserrat", 11),
            fg="#1E3A8A", bg="white",
            wraplength=520, justify="center"
        ).pack(pady=5)

        #quest lists
        self.quests_frame = tk.Frame(self.card, bg="white")
        self.quests_frame.pack(pady=10)

        #adding in the list
        add_frame = tk.Frame(self.card, bg="white")
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Add your own quest:",
                 font=("Montserrat", 11), bg="white", fg="#283593").grid(row=0, column=0)

        self.new_quest_entry = tk.Entry(add_frame, font=("Montserrat", 11), width=32)
        self.new_quest_entry.grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            add_frame, text="Add Quest",
            font=("Montserrat", 10, "bold"), bg="#1976D2", fg="white",
            command=self.add_custom_quest
        ).grid(row=1, column=1, padx=5)


        #savings button
        tk.Button(
            self.card,
            text="View Savings Report",
            font=("Montserrat", 11, "bold"),
            bg="#64B5F6", fg="white",
            padx=16, pady=6,
            command=self.show_savings
        ).pack(pady=5)


        #back button
        tk.Button(
            self.card, text="Back to Menu",
            font=("Montserrat", 11, "bold"),
            bg="#F44336", fg="white",
            command=lambda: controller.show_frame("MenuFrame")
        ).pack(pady=10)


        #internal state
        self.quests = []
        self.quest_vars = []

    def on_show(self):
        # Start animation
        self.anim_pady = 200
        self.target_pady = 40
        self.animate_slide_in()

        data = self.controller.user_data
        # self.quests = data.get("goals", self.default_quests())
        self.render_quests()

    def animate_slide_in(self):
        if self.anim_pady > self.target_pady:
            self.anim_pady -= 10
            self.card.pack_configure(pady=self.anim_pady)
            self.after(15, self.animate_slide_in)

    # def default_quests(self):
    #     return [
    #         {"title": "Build an emergency fund of $500", "completed": False, "type": "Main Quest"},
    #         {"title": "Track all expenses for one month", "completed": False, "type": "Side Quest"},
    #         {"title": "Pay at least $50 toward debt this month", "completed": False, "type": "Side Quest"},
    #         {"title": "Save 10% of your income this month", "completed": False, "type": "Main Quest"},
    #     ]

    def render_quests(self):
        # Clear old UI
        for widget in self.quests_frame.winfo_children():
            widget.destroy()
        self.quest_vars.clear()

        for index, quest in enumerate(self.quests):
            row = tk.Frame(self.quests_frame, bg="white")
            row.pack(anchor="w", pady=4, fill="x")

            var = tk.BooleanVar(value=quest.get("completed", False))

            # Checkbox
            cb = tk.Checkbutton(
                row,
                variable=var,
                command=lambda v=var, q=quest: self.toggle_quest(v, q),
                bg="white",
                activebackground="white"
            )
            cb.pack(side="left")

            # Title
            label = tk.Label(
                row,
                text=quest["title"],
                font=("Montserrat", 11),
                bg="white",
                fg="#1E3A8A" if not quest["completed"] else "#9E9E9E",
                wraplength=500,
            )
            label.pack(side="left", padx=5)

            # DELETE BUTTON
            delete_btn = tk.Button(
                row,
                text="✖",
                font=("Montserrat", 10, "bold"),
                fg="white",
                bg="#F44336",
                width=2,
                command=lambda i=index: self.delete_quest(i)
            )
            delete_btn.pack(side="right", padx=5)

            self.quest_vars.append((var, quest, label))


    # ---------- UPDATE QUEST ----------
    def toggle_quest(self, var, quest):
        quest["completed"] = bool(var.get())
        self.controller.user_data["goals"] = self.quests
        self.controller.save_user_data()

    # ---------- DELETE QUEST ----------
    def delete_quest(self, index):
        del self.quests[index]
        self.controller.user_data["goals"] = self.quests
        self.controller.save_user_data()
        self.render_quests()

    # ---------- ADD QUEST ----------
    def add_custom_quest(self):
        title = self.new_quest_entry.get().strip()
        if not title:
            messagebox.showerror("Oops!", "Please enter a quest name.")
            return

        self.quests.append({"title": title, "completed": False})
        self.new_quest_entry.delete(0, tk.END)

        self.controller.user_data["goals"] = self.quests
        self.controller.save_user_data()
        self.render_quests()

    # ---------- SAVINGS VIEW ----------
    def show_savings(self):
        savings = self.controller.user_data.get("savings", 0)

        messagebox.showinfo(
            "Savings Report",
            f"💰 Current Savings: ${savings:.2f}\n\n"
            "More analytics coming soon!"
        )

# -------------------------------------------------------
# Run Application
# -------------------------------------------------------
if __name__ == "__main__":
    app = CapitalChroniclesApp()
    app.mainloop()
