import sqlite3
from tabulate import tabulate

conn = sqlite3.connect("database_01.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_data_01(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
name VARCHAR(15),
email VARCHAR(18),
user_name VARCHAR(15)
)
""")
conn.commit()


def add_user(name, email, user_name):
    cursor.execute(
        "INSERT INTO user_data_01 (name,email,user_name) VALUES (?,?,?)",
        (name, email, user_name)
    )
    conn.commit()
    print(f"User '{name}' added successfully")


def show_users_data():
    cursor.execute("SELECT * FROM user_data_01")
    rows = cursor.fetchall()

    if not rows:
        print("⚠ No users found.")
        return

    headers = ["ID", "Name", "Email", "Username"]

    print("\n" + tabulate(rows, headers=headers, tablefmt="grid"))


def search_user(user_name):
    cursor.execute(
        "SELECT * FROM user_data_01 WHERE LOWER(user_name) = LOWER(?)",
        (user_name,)
    )
    rows = cursor.fetchall()

    if not rows:
        print("No user found.")
        return

    headers = ["ID", "Name", "Email", "Username"]

    print("\t\t\t  Search Result:\n")
    print(tabulate(rows, headers=headers, tablefmt="grid"))


while True:
    command = input("Command: ").lower()

    if command == "add user":
        name = input("Enter name: ")
        email = input("Enter email: ")
        user_name = input("Enter username: ")
        add_user(name, email, user_name)

    elif command == "see user":
        show_users_data()

    elif command == "search user":
        user = input("Enter username: ")
        search_user(user)

    elif command == "exit":
        print("Exiting program...")
        break

    else:
        print("Invalid command")
