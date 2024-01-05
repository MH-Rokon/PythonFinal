import random

class Bank:
    def __init__(self):
        self.users = []
        self.bank_balance = 0
        self.bankrupt = False
        self.loan_feature_enabled = True

    def generate_account_number(self):
        return random.randint(100, 999)

class User:
    def __init__(self, name, email, address, account_type, bank):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = bank.generate_account_number()
        self.balance = 0
        self.transaction_history = []
        self.loan_taken = 0
        self.bank = bank

    def deposit(self, amount):
        if not self.bank.bankrupt:
            self.balance += amount
            self.bank.bank_balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
        else:
            print("Bank is bankrupt. Unable to deposit.")

    def withdraw(self, amount):
        if not self.bank.bankrupt:
            if amount <= self.balance:
                self.balance -= amount
                self.bank.bank_balance -= amount
                self.transaction_history.append(f"Withdrew ${amount}")
            else:
                print("Withdrawal amount exceeded")
        else:
            print("Bank is bankrupt. Unable to withdraw.")

    def check_balance(self):
        return self.balance

    def check_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if not self.bank.bankrupt:
            if self.loan_taken < 2 and self.bank.loan_feature_enabled:
                self.balance += amount
                self.bank.bank_balance += amount
                self.loan_taken += 1
                self.transaction_history.append(f"Took a loan of ${amount}")
            else:
                print("Cannot take more loans or loan feature is disabled")
        else:
            print("Bank is bankrupt. Unable to take a loan.")

    def transfer(self, recipient, amount):
        if not self.bank.bankrupt:
            if recipient in self.bank.users:
                if amount <= self.balance:
                    self.balance -= amount
                    recipient.balance += amount
                    self.transaction_history.append(f"Transferred ${amount} to {recipient.name}")
                else:
                    print("Insufficient funds for transfer")
            else:
                print("Recipient account does not exist")
        else:
            print("Bank is bankrupt. Unable to transfer funds.")

    def show_info(self):
        print(f"Name: {self.name}\nEmail: {self.email}\nAddress: {self.address}\nAccount Type: {self.account_type}\n"
              f"Account Number: {self.account_number}\nBalance: ${self.balance}")

class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, email, address, account_type):
        user = User(name, email, address, account_type, self.bank)
        self.bank.users.append(user)
        return user

    def delete_account(self, user):
        if user in self.bank.users:
            self.bank.users.remove(user)
            print(f"Account of {user.name} deleted")
        else:
            print("User not found")

    def see_all_accounts(self):
        for user in self.bank.users:
            user.show_info()
            print("------------")

    def check_total_balance(self):
        return self.bank.bank_balance

    def check_total_loan_amount(self):
        total_loan = sum(user.loan_taken for user in self.bank.users)
        return total_loan

    def toggle_loan_feature(self):
        self.bank.loan_feature_enabled = not self.bank.loan_feature_enabled
        status = "enabled" if self.bank.loan_feature_enabled else "disabled"
        print(f"Loan feature is now {status}")

# Menu for user operations
def user_menu(user):
    while True:
        print("\nUser Menu:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Take Loan")
        print("6. Transfer Money")
        print("7. Logout")

        choice = input("Enter choice (1-7): ")
        if choice == '1':
            amount = float(input("Enter deposit amount: "))
            user.deposit(amount)
        elif choice == '2':
            amount = float(input("Enter withdrawal amount: "))
            user.withdraw(amount)
        elif choice == '3':
            print(f"Current Balance: ${user.check_balance()}")
        elif choice == '4':
            print("Transaction History:")
            for transaction in user.check_transaction_history():
                print(transaction)
        elif choice == '5':
            amount = float(input("Enter loan amount: "))
            user.take_loan(amount)
        elif choice == '6':
            recipient_name = input("Enter recipient's name: ")
            recipient = next((u for u in bank.users if u.name == recipient_name), None)
            if recipient:
                amount = float(input("Enter transfer amount: "))
                user.transfer(recipient, amount)
            else:
                print("Recipient not found.")
        elif choice == '7':
            print("Logout successful.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# Menu for admin operations
def admin_menu(admin):
    while True:
        print("\nAdmin Menu:")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. See All Accounts")
        print("4. Check Total Balance")
        print("5. Check Total Loan Amount")
        print("6. Toggle Loan Feature")
        print("7. Logout")

        choice = input("Enter choice (1-7): ")
        if choice == '1':
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            address = input("Enter user address: ")
            account_type = input("Enter account type (Savings/Current): ")
            admin.create_account(name, email, address, account_type)
        elif choice == '2':
            account_number = int(input("Enter account number to delete: "))
            user_to_delete = next((u for u in bank.users if u.account_number == account_number), None)
            if user_to_delete:
                admin.delete_account(user_to_delete)
            else:
                print("User not found.")
        elif choice == '3':
            admin.see_all_accounts()
        elif choice == '4':
            print(f"Total Bank Balance: ${admin.check_total_balance()}")
        elif choice == '5':
            print(f"Total Loan Amount: ${admin.check_total_loan_amount()}")
        elif choice == '6':
            admin.toggle_loan_feature()
        elif choice == '7':
            print("Logout successful.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

bank = Bank()

while True:
    print("\nWelcome to the Banking Management System:")
    print("1. User Login")
    print("2. Admin Login")
    print("3. Create Account")
    print("4. Exit")

    login_choice = input("Enter choice (1-4): ")

    if login_choice == '1':
        user_name = input("Enter your name: ")
        user = next((u for u in bank.users if u.name == user_name), None)
        if user:
            user_menu(user)
        else:
            create_account_option = input("User not found. Do you want to create an account? (yes/no): ")
            if create_account_option.lower() == 'yes':
                name = input("Enter user name: ")
                email = input("Enter user email: ")
                address = input("Enter user address: ")
                account_type = input("Enter account type (Savings/Current): ")
                user = Admin(bank).create_account(name, email, address, account_type)
                user_menu(user)
            else:
                print("Returning to the main menu.")

    elif login_choice == '2':
        admin_password = input("Enter admin password: ")
        if admin_password == "admin123":
            admin_menu(Admin(bank))
        else:
            print("Incorrect admin password.")

    elif login_choice == '3':
        create_account_option = input("Do you want to create a new account? (yes/no): ")
        if create_account_option.lower() == 'yes':
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            address = input("Enter user address: ")
            account_type = input("Enter account type (Savings/Current): ")
            user = Admin(bank).create_account(name, email, address, account_type)
            print("Account created successfully.")
            user_menu(user)
        else:
            print("Returning to the main menu.")

    elif login_choice == '4':
        print("Thank you for using the Banking Management System. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
