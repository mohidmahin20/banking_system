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
        self.loan_count = 0
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

    def transfer(self, other_user, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            other_user.balance += amount
            self.transaction_history.append(f'Transferred {amount} to account {other_user.account_number}')
            other_user.transaction_history.append(f'Received {amount} from account {self.account_number}')
            return f'Transferred {amount} to account number {other_user.account_number}. Current balance {self.balance}'
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


class Admin:
    def __init__(self):
        self.users = []
        self.loan_feature_enabled = True

    def create_account(self, user):
        self.users.append(user)
        return f'Account created. Account number {user.account_number}'

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

def main():
    admin = Admin()
    
    print("----Welcome to the Banking Management System----")

    while True:
        if not admin.users:
            print("No user accounts available. Please create an account (Option 7).")

        print("\nOptions for User:")
        print("1: Create Account")
        print("2: Deposit")
        print("3: Withdraw")
        print("4: Check Balance")
        print("5: View Transaction History")
        print("6: Take Loan")
        print("7: Transfer Money")
        
        print("8: Delete User Account")
        print("9: View User Accounts")
        print("10: Total Available Balance")
        print("11: Total Loan Amount")
        print("12: Toggle Loan Feature")
        print("13: Exit")

        option = input("Select an option: ")
        if option == "1":
            user = User(
                input("Enter name: "),
                input("Enter email: "),
                input("Enter address: "),
                input("Enter account type (Savings or Current): ")
            )
            print(admin.create_account(user))
        
        elif admin.users and option == "2":
            for user in admin.users:
                amount = float(input(f"Enter the deposit amount for {user.name}: "))
                print(user.deposit(amount))
        
        elif admin.users and option == "3":
            for user in admin.users:
                amount = float(input(f"Enter the withdrawal amount for {user.name}: "))
                print(user.withdraw(amount))
        
        elif admin.users and option == "4":
            for user in admin.users:
                print(user.check_balance())
        
        elif admin.users and option == "5":
            for user in admin.users:
                user.view_transaction_history()
        
        elif admin.users and option == "6":
            for user in admin.users:
                amount = float(input(f"Enter the loan amount for {user.name}: "))
                print(user.take_loan(amount))
        
        elif admin.users and option == "7":
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
        
        elif option == "8":
            account_number = int(input("Enter the account number to delete: "))
            print(admin.delete_account(account_number))
        
        elif option == "9":
            print(admin.view_user_accounts())
        
        elif option == "10":
            print(admin.total_available_balance())
        
        elif option == "11":
            print(admin.total_loan_amount())
        
        elif option == "12":
            print(admin.toggle_loan_feature())
        
        elif option == "13":
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
