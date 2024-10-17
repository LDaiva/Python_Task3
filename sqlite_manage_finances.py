import sqlite3

# Connect to SQLite database
connect = sqlite3.connect('manage_finances.db')
c = connect.cursor()

# Create the finances table
# Nespėjau pataisyti duomenų tipo category int -> text ir amount int -> flout
query_table = ('''
create table if not exists finances (
    id integer primary key,
    type text,
    amount int,
    category int
)
''')
with connect:
    c.execute(query_table)
    print(f'Table created successfully')


def enter_amount(choice, amount, category):
    if choice == 1:
        query_insert = '''
            insert into finances (type, amount, category) 
            values ("income", ?, ? )
        '''
        print(f"Income {amount} EUR for category {category} added successfully")
    if choice == 2:
        query_insert = '''
            insert into finances (type, amount, category) 
            values ("expense", ?, ? )
        '''
        print(f"Expense {amount} EUR for category {category} added successfully")
    with connect:
        c.execute(query_insert, (amount, category))


# Function to take user input for amount (income or expense)
def user_input(choice):
    amount = int(input("Enter amount: "))
    category = input("Enter category: ")
    enter_amount(choice, amount, category)


def get_balance():
    query_income_sum = '''
        select sum(amount) from finances 
        where type='income'
    '''

    query_expense_sum = '''
            select sum(amount) from finances 
            where type='expense'
        '''
    with connect:
        c.execute(query_income_sum)
        record_income = c.fetchone()[0]
        c.execute(query_expense_sum)
        record_execute = c.fetchone()[0]
        balance = record_income - record_execute
    print(f'Income sum: {record_income},'
          f' Execute sum: {record_execute},'
          f' Balance: {balance}')


def get_incomes():
    query_all_incomes = '''
        select * from finances 
        where type='income'
    '''
    print("Incomes:")
    with connect:
        c.execute(query_all_incomes)
        incomes = c.fetchall()
        for income in incomes:
            print(income)


def get_expenses():
    query_all_expense = '''
        select * from finances 
        where type='expense'
    '''
    print("Expenses:")
    with connect:
        c.execute(query_all_expense)
        expenses = c.fetchall()
        for expense in expenses:
            print(expense)


def delete_record():
    rec_id = int(input("Enter the record ID you want to delete: "))
    query_select_delete = '''
        select * from finances 
        where id = ?
    '''
    query_delete = '''
        delete from finances 
        where id = ?
    '''
    with connect:
        c.execute(query_select_delete, (rec_id,))
        record_deleted = c.fetchone()
        c.execute(query_delete, (rec_id,))
        print(f'Deleted record ID {rec_id}, sum {record_deleted[2]}, type {record_deleted[1]}')


def update_record():
    rec_id = int(input("Enter the record ID you want to update: "))
    new_type = input("Enter new type (income/expense): ")
    new_amount = int(input("Enter new amount: "))
    new_category = int(input("Enter new category: "))

    query_select_update = "select * from finances where id = ?"
    query_update = "update finances set type=?, amount=?, category=? where id=?"

    with connect:
        c.execute(query_select_update, (rec_id,))
        record_updated = c.fetchone()
        c.execute(query_update, (new_type, new_amount, new_category, rec_id))
        print(f'Updated record ID {record_updated[0]},'
              f' type {record_updated[1]},'
              f' sum {record_updated[2]},'
              f' category {record_updated[3]}')


def main():
    while True:
        print("\nPersonal Finance Manager")
        print("1. Enter Income")
        print("2. Enter Expense")
        print("3. Get Balance")
        print("4. Get All Incomes")
        print("5. Get All Expenses")
        print("6. Delete Income/Expense")
        print("7. Update Income/Expense")
        print("8. Exit")

        choice = int(input("Choose an option: "))

        if choice == 1 or choice == 2:
            user_input(choice)
        elif choice == 3:
            get_balance()
        elif choice == 4:
            get_incomes()
        elif choice == 5:
            get_expenses()
        elif choice == 6:
            delete_record()
        elif choice == 7:
            update_record()
        elif choice == 8:
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the main program
if __name__ == "__main__":
    main()
