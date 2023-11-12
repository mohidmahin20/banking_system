class User:
    account_number_counter = 1

    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = User.account_number_counter
        self.transaction_history = []
        self.loan_count = 1
        User.account_number_counter += 1

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f'Deposited: {amount}')
            return f'Deposited {amount}. Current balance {self.balance}'
        else:
            return 'Invalid deposit amount.'

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transaction_history.append(f'Withdrawn: {amount}')
            return f'Withdrawn: {amount}. Current balance {self.balance}'
        else:
            return 'Withdrawal amount exceeded or insufficient balance'

    def check_balance(self):
        return f'Current balance: {self.balance}'

    def get_transaction_history(self):
        return self.transaction_history

    def take_loan(self, amount):
        if self.loan_count <= 2:
            if amount > 0:
                self.balance += amount
                self.loan_count += 1
                self.transaction_history.append(f'Took a loan of amount {amount}')
                return f'Took a loan of amount {amount}. Current balance {self.balance}'
            else:
                return 'Invalid loan amount'
        else:
            return 'Cannot take more than two loans.'

    def transfer(self, recipient, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            self.transaction_history.append(f'Transferred {amount} to account {recipient.account_number}')
            recipient.transaction_history.append(f'Received {amount} from account {self.account_number}')
            return f'Transferred {amount} to account number {recipient.account_number}. Current balance {self.balance}'
        else:
            return 'Invalid transfer amount or insufficient balance'

    def is_bankrupt(self):
        if self.balance < 0:
            return 'The bank is bankrupt.'
        else:
            return False

    def view_transaction_history(self):
        print(f"Transaction history for Account Number {self.account_number}:")
        for transaction in self.transaction_history:
            print(transaction)

    @classmethod
    def create_account(cls):
        name = input("Enter name: ")
        email = input("Enter email: ")
        address = input("Enter address: ")
        account_type = input("Enter account type (Savings or Current): ")

        return cls(name, email, address, account_type)


class Admin:
    admin_created = False

    def __init__(self):
        if not Admin.admin_created:
            Admin.admin_created = True
            self.admin_name = None
            self.admin_email = None
            self.admin_password = None
        else:
            raise Exception("Admin account already exists.")

        self.users = []
        self.loan_feature_enabled = True

    def create_account(self, user):
        self.users.append(user)
        return f'Account created. Account number {user.account_number}'

    def create_admin_account(self):
        if not self.admin_name:
            self.admin_name = input("Enter admin name: ")
            self.admin_email = input("Enter admin email: ")
            self.admin_password = input("Enter admin password: ")  # You may want to implement proper password handling
            print(f'Admin account created. Welcome, {self.admin_name}!')
        else:
            print("Admin account already exists.")

    def admin_login(self):
        entered_name = input("Enter admin name: ")
        entered_password = input("Enter admin password: ")  # You may want to implement proper password handling

        if entered_name == self.admin_name and entered_password == self.admin_password:
            print(f'Logged in as admin: {self.admin_name}')
            return self
        else:
            print('Invalid admin credentials. Please try again.')
            return None

    def delete_account(self, account_number):
        for user in self.users:
            if user.account_number == account_number:
                self.users.remove(user)
                return f'Account {account_number} deleted'
        return f'Account {account_number} not found.'

    def view_user_accounts(self):
        user_list = '\n'.join([f'Account number: {user.account_number}, Name: {user.name}, Balance: {user.balance}' for user in self.users])
        return f'All user accounts:\n{user_list}'

    def total_available_balance(self):
        total_balance = sum(user.balance for user in self.users)
        return f"Total Available Balance in the Bank: ${total_balance}"

    def total_loan_amount(self):
        total_loan = sum(user.balance for user in self.users if user.balance < 0)
        return f"Total Loan Amount in the Bank: ${-total_loan}"

    def toggle_loan_feature(self):
        self.loan_feature_enabled = not self.loan_feature_enabled
        status = "enabled" if self.loan_feature_enabled else "disabled"
        return f"Loan Feature is now {status}"


def user_menu(admin):
    while True:
        print("\nUser Options:")
        print("1: Create User Account")
        print("2: Deposit")
        print("3: Withdraw")
        print("4: Check Balance")
        print("5: View Transaction History")
        print("6: Take Loan")
        print("7: Transfer Money")
        print("8: Exit")

        option = input("Select an option: ")

        if option.isdigit():
            option = int(option)

            if option == 1:
                new_user = User.create_account()
                print(admin.create_account(new_user))
            elif admin.users and option == 2:
                for user in admin.users:
                    amount = float(input(f"Enter the deposit amount for {user.name}: "))
                    print(user.deposit(amount))
            elif admin.users and option == 3:
                for user in admin.users:
                    amount = float(input(f"Enter the withdrawal amount for {user.name}: "))
                    print(user.withdraw(amount))
            elif admin.users and option == 4:
                for user in admin.users:
                    print(user.check_balance())
            elif admin.users and option == 5:
                for user in admin.users:
                    user.view_transaction_history()
            elif admin.users and option == 6:
                for user in admin.users:
                    amount = float(input(f"Enter the loan amount for {user.name}: "))
                    print(user.take_loan(amount))
            elif admin.users and option == 7:
                sender_account_number = int(input("Enter your account number: "))
                sender = None
                for user in admin.users:
                    if user.account_number == sender_account_number:
                        sender = user
                        break
                if sender:
                    others_account_number = int(input("Enter the recipient's account number: "))
                    amount = float(input("Enter the transfer amount: "))
                    recipient = None
                    for user in admin.users:
                        if user.account_number == others_account_number:
                            recipient = user
                            break
                    if recipient:
                        print(sender.transfer(recipient, amount))
                    else:
                        print("Recipient's account does not exist.")
                else:
                    print("Your account does not exist.")
            elif admin.users and option == 8:
                print("Exiting user menu...")
                break
            else:
                print("Invalid option. Please try again.")
        else:
            print("Invalid option. Please enter a numeric value.")

def admin_menu(admin):
    while True:
        print("\nAdmin Options:")
       
        print("1: Create Admin Account")
        print("2: Delete User Account")
        print("3: View User Accounts")
        print("4: Total Available Balance")
        print("5: Total Loan Amount")
        print("6: Toggle Loan Feature")
        print("7: Exit")

        admin_option = input("Select an option: ")

        if admin_option.isdigit():
            admin_option = int(admin_option)
            
            if admin_option == 1:
                admin.create_admin_account()
            elif admin_option == 2:
                account_number = int(input("Enter the account number to delete: "))
                print(admin.delete_account(account_number))
            elif admin_option == 3:
                print(admin.view_user_accounts())
            elif admin_option == 4:
                print(admin.total_available_balance())
            elif admin_option == 5:
                print(admin.total_loan_amount())
            elif admin_option == 6:
                print(admin.toggle_loan_feature())
            elif admin_option == 7:
                print("Exiting admin menu...")
                break
            else:
                print("Invalid option. Please try again.")
        else:
            print("Invalid option. Please enter a numeric value.")

def main():
    admin = Admin()

    print("----Welcome to the Banking Management System----")

    while True:
        print("\nOptions:")
        print("1: User Menu")
        print("2: Admin Menu")
        print("3: Exit")

        choice = input("Select an option: ")

        if choice == "1":
            user_menu(admin)
        elif choice == "2":
            if not admin.admin_name:
                admin.create_admin_account()

            admin_instance = admin.admin_login()
            if admin_instance:
                admin_menu(admin_instance)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
