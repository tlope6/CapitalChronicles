import turtle
import hashlib  # To hash passwords securely

# Constants
SCREENSIZE = 500
ACCOUNT_FILE = "accounts.txt"  # File to store user account details

# Global variables
age = 0
salary = 0
expenses = 0
savings = 0
maxval = 0; 
minval = 0;



# Hash Passwords for Security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Setup Turtle and Screen
def setup_screen():
    global t, s
    t = turtle.Turtle()
    t.hideturtle()
    s = turtle.Screen()
    s.screensize(SCREENSIZE, SCREENSIZE)
    s.bgcolor("white")


# Display Initial Logo and Intro
def display_intro():
    turtle.addshape("ChroniclesLogo.gif")
    logo = turtle.Turtle()
    logo.penup()
    logo.goto(0, 150)
    logo.shape("ChroniclesLogo.gif")
    
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.write("CapitalChronicles", align="center", font=("Times New Roman", 21, "bold"))
    t.penup()
    t.goto(0, -25)
    t.pendown()
    t.write("Scripting Your Financial Epic Adventure", align="center", font=("Times New Roman", 15, "bold"))
    
    # Button Setup
    turtle.addshape("button_gif.gif")
    button = turtle.Turtle()
    button.penup()
    button.goto(0, -150)
    button.shape("button_gif.gif")
    button.onclick(display_account_screen)


# Display Account Screen (Sign Up / Log In)
def display_account_screen(x=None, y=None):
    # global minval, maxval
    t.clear()
    choice = s.numinput("Account", "1: Sign Up\n2: Log In\nEnter your choice:", minval=1, maxval=2)
    if choice == 1:
        create_account()
    elif choice == 2:
        login()


# Account Creation
def create_account():
    t.clear()
    t.penup()
    t.goto(0, 150)
    t.pendown()
    t.write("Create Account", align="center", font=("Times New Roman", 25, "bold"))
    
    username = s.textinput("Sign Up", "Enter a username:")
    password = s.textinput("Sign Up", "Enter a password:")
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Save account to file
    with open(ACCOUNT_FILE, "a") as file:
        file.write(f"{username},{hashed_password}\n")
    
    t.penup()
    t.goto(0, 50)
    t.pendown()
    t.write("Account created successfully!", align="center", font=("Times New Roman", 15, "bold"))
    
    display_account_screen()


# Login
def login():
    t.clear()
    t.penup()
    t.goto(0, 150)
    t.pendown()
    t.write("Log In", align="center", font=("Times New Roman", 25, "bold"))
    
    username = s.textinput("Login", "Enter your username:")
    password = s.textinput("Login", "Enter your password:")
    
    # Validate credentials
    hashed_password = hash_password(password)
    valid = False
    
    # Check accounts file for matching username and hashed password
    try:
        with open(ACCOUNT_FILE, "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if username == stored_username and hashed_password == stored_password:
                    valid = True
                    break
    except FileNotFoundError:
        t.penup()
        t.goto(0, 50)
        t.pendown()
        t.write("No accounts found. Please sign up first.", align="center", font=("Times New Roman", 15, "bold"))
        display_account_screen()
        return
    
    if valid:
        t.penup()
        t.goto(0, 50)
        t.pendown()
        t.write("Login successful!", align="center", font=("Times New Roman", 15, "bold"))
        display_menu()
    else:
        t.penup()
        t.goto(0, 50)
        t.pendown()
        t.write("Invalid credentials. Try again.", align="center", font=("Times New Roman", 15, "bold"))
        display_account_screen()


# Display Main Menu
def display_menu():
    t.clear()
    t.penup()
    t.goto(0, 150)
    t.pendown()
    t.write("Which CapitalChronicle Mission Will You Choose?", align="center", font=("Times New Roman", 20, "bold"))
    
    t.penup()
    t.goto(0, 50)
    t.pendown()
    t.write("1. Enter Your Way Through Your Financial Adventure", align="center", font=("Times New Roman", 15, "bold"))
    
    t.penup()
    t.goto(0, -25)
    t.pendown()
    t.write("2. Seek Your Scripted Goals", align="center", font=("Times New Roman", 15, "bold"))
    
    t.penup()
    t.goto(0, -150)
    t.pendown()
    t.write("3. Exit", align="center", font=("Times New Roman", 15, "bold"))
    
    choice = s.numinput("Menu", "Enter your choice (1-3):", minval=1, maxval=3)
    handle_menu_choice(int(choice))


# Handle User's Menu Choice
def handle_menu_choice(choice):
    if choice == 1:
        enter_financial_adventure()
    elif choice == 2:
        scripted_goals()
    elif choice == 3:
        exit_app()

# Function to Adjust Necessities Costs
def calculate_necessities():
    global expenses
    t.clear()
    necessities = s.numinput("Necessities", "Enter your monthly living costs (e.g., rent, food, etc.):", minval=0)
    expenses += necessities
    with open("Necessities.txt", "a") as file:
        file.write(f"Monthly Necessities: ${necessities:.2f}\n")
    t.penup()
    t.goto(0, 70)
    t.pendown()
    t.write(f"Necessities: ${necessities:.2f}", align="center", font=("Times New Roman", 15, "bold"))

# Function to Calculate Taxes
def calculate_taxes(income):
    tax_rate = 0.15  # Example: 15% tax rate
    taxes = income * tax_rate
    adjusted_income = income - taxes
    with open("Taxes.txt", "a") as file:
        file.write(f"Income: ${income:.2f}, Taxes: ${taxes:.2f}, After Tax: ${adjusted_income:.2f}\n")
    return taxes, adjusted_income

# Handle Job/Income Details
def handle_job():
    global salary, expenses
    has_job = s.textinput("Job Status", "Do you have a job? (yes/no):").lower()
    if has_job == "yes":
        salary = s.numinput("Salary", "Enter your monthly salary ($):", minval=0)
        t.penup()
        t.goto(0, -50)
        t.pendown()
        t.write(f"Salary: ${salary:.2f}", align="center", font=("Times New Roman", 15, "bold"))
        calculate_necessities()
        taxes, net_income = calculate_taxes(salary)
        expenses += taxes
        t.penup()
        t.goto(0, -70)
        t.pendown()
        t.write(f"Taxes: ${taxes:.2f}, Net Income: ${net_income:.2f}", align="center", font=("Times New Roman", 15, "bold"))
        return net_income
    else:
        stipend = s.numinput("Stipend", "Enter your monthly stipend ($):", minval=0)
        t.penup()
        t.goto(0, -50)
        t.pendown()
        t.write(f"Stipend: ${stipend:.2f}", align="center", font=("Times New Roman", 15, "bold"))
        calculate_necessities()
        return stipend

# Adjust Financial Adventure
def enter_financial_adventure():
    global age, salary, expenses
    t.clear()
    t.penup()
    t.goto(0, 150)
    t.pendown()
    t.write("Financial Adventure", align="center", font=("Times New Roman", 25, "bold"))

    age = int(s.numinput("Financial Adventure", "Enter your age:", minval=0))
    t.penup()
    t.goto(0, 100)
    t.pendown()
    t.write(f"Age: {age}", align="center", font=("Times New Roman", 15, "bold"))
    
    if age < 18:
        t.penup()
        t.goto(0, 70)
        t.pendown()
        t.write("Status: Child", align="center", font=("Times New Roman", 15, "bold"))
        allowance = s.numinput("Allowance", "Enter your monthly allowance ($):", minval=0)
        expenses = allowance * 0.5
        with open("Child.txt", "a") as file:
            file.write(f"Age: {age}, Allowance: ${allowance:.2f}, Expenses: ${expenses:.2f}\n")
    elif 18 <= age <= 22:
        t.penup()
        t.goto(0, 70)
        t.pendown()
        t.write("Status: Student", align="center", font=("Times New Roman", 15, "bold"))
        salary = handle_job()
    else:
        t.penup()
        t.goto(0, 70)
        t.pendown()
        t.write("Status: Working Adult", align="center", font=("Times New Roman", 15, "bold"))
        salary = handle_job()

    t.penup()
    t.goto(0, -150)
    t.pendown()
    t.write(f"Total Monthly Expenses: ${expenses:.2f}", align="center", font=("Times New Roman", 15, "bold"))
# Rest of the Financial Functionality (Same as Before)


# Exit Application
def exit_app():
    t.clear()
    t.penup()
    t.goto(0, 0)
    t.pendown()
    t.write("Thanks for using CapitalChronicles!", align="center", font=("Times New Roman", 20, "bold"))
    t.penup()
    t.goto(0, -50)
    t.pendown()
    t.write("Goodbye!", align="center", font=("Times New Roman", 15, "bold"))
    turtle.done()


# Main Program Execution
setup_screen()
display_intro()
turtle.mainloop()
