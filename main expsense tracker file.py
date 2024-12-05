#Matthew Onwulata, Tecumasy Morris, Lukas Agrio-O'Reilly Final project 

import sqlite3
import datetime
conn = sqlite3.connect("expenses.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Date TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
)
""")
conn.commit()

while True:
    print("\nSelect an option:")
    print("1. Enter a new expense")
    print("2. View expenses summary")
    print("3. Exit")

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        continue

    if choice == 1:
        date = input("Enter the date of the expense (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")
            continue

        description = input("Enter the description of the expense: ")
        cur.execute("SELECT DISTINCT category FROM expenses")
        categories = cur.fetchall()

        print("Select a category by number:")
        for idx, category in enumerate(categories):
            print(f"{idx + 1}. {category[0]}")
        print(f"{len(categories) + 1}. Create new category")

        try:
            category_choice = int(input())
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if category_choice == len(categories) + 1:
            category = input("Enter the new category name: ")
        elif 1 <= category_choice <= len(categories):
            category = categories[category_choice - 1][0]
        else:
            print("Invalid category choice!")
            continue

        try:
            price = float(input("Enter the price of the expense: "))
        except ValueError:
            print("Invalid price! Please enter a number.")
            continue

        # Insert the expense into the database
        cur.execute(
            "INSERT INTO expenses (Date, description, category, price) VALUES (?, ?, ?, ?)",
            (date, description, category, price),
        )
        conn.commit()
        print("Expense added successfully!")

    elif choice == 2:
        print("\nSelect an option:")
        print("1. View all expenses")
        print("2. View monthly expenses by category")

        try:
            view_choice = int(input())
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if view_choice == 1:
            cur.execute("SELECT * FROM expenses ORDER BY Date")
            expenses = cur.fetchall()
            if not expenses:
                print("No expenses found.")
            else:
                for expense in expenses:
                    print(expense)
        elif view_choice == 2:
            month = input("Enter the month (MM): ")
            year = input("Enter the year (YYYY): ")
            if not (month.isdigit() and year.isdigit() and 1 <= int(month) <= 12):
                print("Invalid month or year!")
                continue

            cur.execute(
                """
                SELECT category, SUM(price) FROM expenses 
                WHERE strftime('%m', Date) = ? AND strftime('%Y', Date) = ?
                GROUP BY category
                """,
                (month.zfill(2), year),
            )
            expenses = cur.fetchall()
            if not expenses:
                print("No expenses found for the given month and year.")
            else:
                for expense in expenses:
                    print(f"Category: {expense[0]}, Total: {expense[1]}")
        else:
            print("Invalid choice!")
    elif choice == 3:
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice!")

conn.close()








        

