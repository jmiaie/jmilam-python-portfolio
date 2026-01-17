import json
import os

# --- Configuration ---
DATA_FILE = "expenses.json"

def load_expenses():
    """Loads expenses from the JSON file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def save_expenses(expenses):
    """Saves the current list of expenses to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(expenses, file, indent=4)
        print("✓ Data saved successfully.")
    except IOError as e:
        print(f"Error saving data: {e}")

def add_expense(expenses):
    """Prompts user for details and adds a new expense."""
    print("\n--- Add New Expense ---")
    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        
        category = input("Enter category (e.g., Food, Travel): ").strip()
        if not category:
            category = "Uncategorized"

        expenses.append({"amount": amount, "category": category})
        save_expenses(expenses)
        print(f"Added: ${amount:.2f} to {category}")
        
    except ValueError:
        print("Invalid input! Please enter a numeric value for the amount.")

def view_expenses(expenses):
    """Prints all expenses in a tabulated format."""
    print("\n--- Expense List ---")
    if not expenses:
        print("No expenses recorded yet.")
    else:
        print(f"{'ID':<5} | {'Category':<15} | {'Amount':>10}")
        print("-" * 36)
        for index, item in enumerate(expenses, start=1):
            print(f"{index:<5} | {item['category']:<15} | ${item['amount']:>9.2f}")

def show_total(expenses):
    """Calculates and prints the total sum of expenses."""
    total = sum(item["amount"] for item in expenses)
    print(f"\nTotal Spent: ${total:.2f}")

def main():
    """Main program loop."""
    expenses = load_expenses()
    
    while True:
        print("\n=== EXPENSE TRACKER MENU ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Show Total")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            view_expenses(expenses)
        elif choice == '3':
            show_total(expenses)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()