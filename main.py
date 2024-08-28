import sqlite3
import update1
from art import text2art
from rich import print

def print_ascii_art(text):
    # Generate ASCII art text
    ascii_art = text2art(text)
    
    # Print the ASCII art text
    print(ascii_art)
    print("This project is dedicated to [red]Hiba[/red], whose inspiration and love guide every aspect of its creation") 
# Example usage
print_ascii_art("        Money     Manager")



def create_table():
    """Create the expenses table if it doesn't exist."""
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (amount REAL, spent REAL, description TEXT)''')
    conn.commit()
    conn.close()

def print_all_data():
    """Fetch and print all data from the expenses table."""
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT rowid, * FROM expenses")
    
    rows = c.fetchall()
    conn.close()
    # Print each row in a readable format
    for row in rows:
        print(f"\nNumber: {row[0]}, Amount: {row[1]}, Spent: {row[2]}, Description: {row[3]}\n")

def get_last_amount():
    """Retrieve the last amount from the database."""
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT amount FROM expenses ORDER BY rowid DESC LIMIT 1")
    last_amount = c.fetchone()
    conn.close()
    return last_amount[0] if last_amount else None

def add_expense(amount, spent, description):
    """Add a new expense to the database and update the amount."""
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()

    # If there are existing records, get the latest amount
    last_amount = get_last_amount()
    if last_amount is not None:
        new_amount = last_amount - spent
    else:
        new_amount = amount - spent

    # Insert the new record
    c.execute("INSERT INTO expenses (amount, spent, description) VALUES (?, ?, ?)", 
              (new_amount, spent, description))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    return new_amount

def delete_last_row():
    # Connect to your SQLite database
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM expenses
        WHERE rowid = (SELECT MAX(rowid) FROM expenses);
    ''')
    row = cursor.fetchone()
    print(f"\nDeleted  [ spent : {row[1]}, description : {row[2]} ] [green]Succesfully !![/green]")

    # Delete the last row from the 'expenses' table
    cursor.execute('''
        SELECT amount FROM expenses
        WHERE rowid = (SELECT MAX(rowid) FROM expenses);
    ''')
    amounts = cursor.fetchone()
    amount = amounts[0]
    cursor.execute('''
        SELECT spent FROM expenses
        WHERE rowid = (SELECT MAX(rowid) FROM expenses);
    ''')
    spents = cursor.fetchone()
    spent = spents[0]
    new_amount = spent + amount
    cursor.execute('''
        UPDATE expenses
        SET amount = ?
        WHERE rowid = (SELECT MAX(rowid) - 1 FROM expenses);
    ''',(new_amount,))

    cursor.execute('''
        DELETE FROM expenses
        WHERE rowid = (SELECT MAX(rowid) FROM expenses);
    ''')
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def handle_choice(choice):
    if choice == 'a':
        main()
    elif choice == 'b':
        print_all_data()
    elif choice == 'c':
        delete_last_row()
    elif choice == 'e':
        print_all_data()
        update1.update_expense()
    elif choice == 'd':
        print("Quitting...")
        return False
    else:
        print("Invalid choice. Please select a valid option.")
    return True

def main():
    create_table()  # Ensure the table is created

    # Get the last amount or set it to None if no record exists
    last_amount = get_last_amount()
    if last_amount is None:
        last_amount = float(input("Enter the initial amount: "))
    else:
        print(f"Here's your last amount: {last_amount}")
    while True:
        try:
            spent = float(input("Enter how much you spent: "))
            description = input("Enter what you spent on: ")
            break
        except ValueError:
            print("Enter a valid input")
    new_amount = add_expense(last_amount, spent, description)
    print(f"\nNew balance: {new_amount}\n")

while True:
    print("\na - Enter New Payment")
    print("b - Check History")
    print("c - Delete Last payment")
    print("e - Update an Expense")
    print("[red]d - QUIT[/red]\n")
    choice = input("Choose what you want: ").strip().lower()  # Use input as string and strip unwanted whitespace
    if not handle_choice(choice):
        break

