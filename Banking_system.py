class User:
    account_number_counter=0


    def __init__(self,name,email,address,account_type) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.account_number = User.account_number_counter
        self.transaction_history = []
        self.loan_count = 0

        User.account_number_counter+=1


    def deposit(self,amount):
        if amount>0:
            self.balance += amount
            self.transaction_history.append(f'Deposited: {amount}')
            return f'defosited {amount}. current balance {self.balance}'
        
        else: 
            return 'invalid deposit amount.'

    def withdraw(self,amount):
        if amount > 0:
            self.balance -=amount
            self.transaction_history.append(f'withdrawn{amount}')
            return f'withdrwan{amount}. current balance {self.balance}'
        else : 
            return 'withdrawal amount exceeded'

    def check_balance(self):
        return f'current balance: {self.balance}'
        
    def get_transaction_history(self):
        return self.transaction_history
        
    def take_loan (self,amount):
        if self.loan_count<=2:
            if amount>0:
                self.balance+=amount
                self.loan_count+=1
                self.transaction_history.append(f'took loan of amount {amount}')
                return f'took loan of amount {amount}. current balance {self.balance}'
            else : 
                return 'invalid loan amount'
        else :
            return ' cannot take more than two loans.'
            
    def transfer(self,other_user,amount):
        if amount>0:
            if self.balance>=amount:
                if other_user:
                    self.balance-=amount
                    other_user.balance +=amount
                    self.transaction_history.append(f'transfered {amount} to account {other_user.account_number}')
                    other_user.transaction_history.append(f'recieved {amount} from  account {self.account_number}')
                    return f'transfered {amount} to account num {other_user.account_number} . current balance {self.balance}'
                else:
                    return 'account does not exist'
            else:
                return 'insufficient balance'
            
        else :
            return 'invalid transfer amount'
        
    def is_bankrupt(self):
        if self.balance<0:
            return 'the bank is bankrupt.'
        else:
            return False
    def view_transaction_history(self):
        print(f"Transaction history for Account Number {self.account_number}:")
        for transaction in self.transaction_history:
            print(transaction)
        

class Admin:
    def __init__(self) -> None:
        self.users=[]
        self.loan_feature_enabled=True

    def create_account(self,user):
        self.users.append(user)
        return  f'account created. account number {user.account_number}'
    
    def delete_account(self,account_number):
        for user in self.users:
            if user.account_number== account_number:
                self.users.remove(user)
                return f'account {account_number} deleted'
        return f' account {account_number} not found.'
    def view_user_accounts(self):
        user_list = '\n'.join([f'account number : {user.account_number}, name:{user.name} , balance: {user.balance}' for user in self.users])
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
    user1 = User("karim", "karim@example.com", "dhaka", "Savings")
    user2 = User("Rahim", "rahim@example.com", "mym", "Current")

    print("----Welcome to the Banking Management System----")

    while True:
        print("\nOptions for User:")
        print("1: Deposit")
        print("2: Withdraw")
        print("3: Check Balance")
        print("4: View Transaction History")
        print("5: Take Loan")
        print("6: Transfer Money")
        print("\nOptions for Admin:")
        print("7: Create User Account")
        print("8: Delete User Account")
        print("9: View User Accounts")
        print("10: Total Available Balance")
        print("11: Total Loan Amount")
        print("12: Toggle Loan Feature")
        print("13: Exit")

        option = input("Select an option: ")

        if option == "1":
            amount = float(input("Enter the deposit amount: "))
            print(user1.deposit(amount))
        elif option == "2":
            amount = float(input("Enter the withdrawal amount: "))
            print(user1.withdraw(amount))
        elif option == "3":
            print(user1.check_balance())
        elif option == "4":
            print(user1.view_transaction_history())
        elif option == "5":
            amount = float(input("Enter the loan amount: "))
            print(user1.take_loan(amount))
        elif option == "6":
            
            others_account_number = int(input("Enter the others's account number: "))
            amount = float(input("Enter the transfer amount: "))
            others = None
            for u in admin.users:
                if u.account_number == others_account_number:
                    others = u
                    break
            if others:
                print(user1.transfer(others, amount))
            else:
                print("others account does not exist.")
        elif option == "7":
            user = User(
                input("Enter name: "),
                input("Enter email: "),
                input("Enter address: "),
                input("Enter account type (Savings or Current): ")
            )
            print(admin.create_account(user))
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
       
