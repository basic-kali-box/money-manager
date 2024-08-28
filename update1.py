import sqlite3

def update_expense():
    """Update an expense record in the database."""
    # Get user inputs
    rowid = int(input("Enter the row ID to update: "))
    
    new_amount_input = input("Enter the new amount (Leave it blank if you don't want any changes): ")
    new_amount = float(new_amount_input) if new_amount_input else None
    
    new_spent_input = input("Enter the new spent (Leave it blank if you don't want any changes): ")
    new_spent = float(new_spent_input) if new_spent_input else None
    
    new_description = input("Enter the new description (Leave it blank if you don't want any changes): ")
    
    # Connect to the SQLite database
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    # Build the update query dynamically based on provided parameters
    update_query = 'UPDATE expenses SET '
    update_params = []
    
    if new_amount is not None:
        update_query += 'amount = ?, '
        update_params.append(new_amount)
    elif new_amount is None and new_spent is not None:
        # Fetch the amount from the previous row to adjust
        cursor.execute('SELECT amount FROM expenses WHERE rowid = ?', (rowid - 1,))
        amounts = cursor.fetchone()
        if amounts:
            previous_amount = amounts[0]
            new_amount = previous_amount - new_spent
            update_query += 'amount = ?, '
            update_params.append(new_amount)
    
    if new_spent is not None:
        update_query += 'spent = ?, '
        update_params.append(new_spent)
    
    if new_description:
        update_query += 'description = ? '
        update_params.append(new_description)
    
    # Check if any updates were made
    if not update_params:
        print("No changes were made.")
        conn.close()
        return False
    
    # Remove trailing comma and space if necessary
    if update_query.endswith(', '):
        update_query = update_query[:-2]
    
    # Add the WHERE clause to the query
    update_query += ' WHERE rowid = ?'
    update_params.append(rowid)
    
    # Execute the update query
    cursor.execute(update_query, update_params)

    # Commit the changes
    conn.commit()
    
    # Print confirmation
    print(f"Updated record with rowid {rowid} successfully!")
    
    # Close the connection
    conn.close()
