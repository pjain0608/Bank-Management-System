import hashlib
import sqlite3

class BankManagementSystem:
    def __init__(self):
        self.db_connection = sqlite3.connect('bank_management_system.db')
        self.db_cursor = self.db_connection.cursor()
        self.create_database()

    def create_database(self):
        self.db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            balance REAL NOT NULL,
            pin TEXT
        )
        ''')
        self.db_connection.commit()

    def encrypt_pin(self, pin):
        # Encrypt PIN using a custom mapping
        mapping = {str(i): chr(97 + i) for i in range(10)} 
        encrypted_pin = ''.join(mapping[digit] for digit in pin)
        return encrypted_pin

    def create_account(self):
        try:
            name = input("Enter Name: ")
            mobile = input("Enter Mobile Number: ")
            email = input("Enter Email ID: ")
            opening_balance = float(5000)

            self.db_cursor.execute("SELECT MAX(CAST(account_number AS INTEGER)) FROM accounts")
            result = self.db_cursor.fetchone()

            if result and result[0]:
                next_number = f"{int(result[0]) + 1:012}"
            else:
                next_number = "100000000001"  # Starting 12-digit account number

            self.db_cursor.execute('''
            INSERT INTO accounts (account_number, name, mobile, email, balance, pin) 
            VALUES (?, ?, ?, ?, ?, NULL)
            ''', (next_number, name, mobile, email, opening_balance))
            self.db_connection.commit()

            print(f"Account created successfully. Your account number is {next_number}")
            self.generate_pin(next_number)
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def generate_pin(self, account_number):
        try:
            pin = input("Enter a 4-digit PIN: ")
            encrypted_pin = self.encrypt_pin(pin)
            self.db_cursor.execute("UPDATE accounts SET pin = ? WHERE account_number = ?", (encrypted_pin, account_number))
            self.db_connection.commit()
            print("PIN set successfully!")
        except Exception as e:
            print(f"Error setting PIN: {e}")

    def check_balance(self):
        try:
            print("1) Using Account Number")
            print("2) Using Mobile Number")
            print("3) Using Email ID")
            choice = int(input("Choose an option: "))

            if choice == 1:
                account_number = input("Enter Account Number: ")
                self.db_cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
            elif choice == 2:
                mobile = input("Enter Mobile Number: ")
                self.db_cursor.execute("SELECT balance FROM accounts WHERE mobile = ?", (mobile,))
            elif choice == 3:
                email = input("Enter Email ID: ")
                self.db_cursor.execute("SELECT balance FROM accounts WHERE email = ?", (email,))
            else:
                print("Invalid choice.")
                return

            result = self.db_cursor.fetchone()
            if result:
                print(f"Balance: {result[0]}")
            else:
                print("No matching account found.")
        except Exception as e:
            print(f"Error checking balance: {e}")

    def validate_account(self, account_number, pin):
        try:
            self.db_cursor.execute("SELECT pin FROM accounts WHERE account_number = ?", (account_number,))
            result = self.db_cursor.fetchone()
            if result:
                encrypted_pin = self.encrypt_pin(pin)
                if result[0] == encrypted_pin:
                    return True
                else:
                    print("Invalid PIN.")
            else:
                print("Invalid account number.")
        except Exception as e:
            print(f"Validation error: {e}")
        return False

    def withdraw(self):
        try:
            account_number = input("Enter Account Number: ")
            pin = input("Enter PIN: ")

            if self.validate_account(account_number, pin):
                amount = float(input("Enter amount to withdraw: "))
                self.db_cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
                balance = self.db_cursor.fetchone()

                if balance and balance[0] >= amount:
                    new_balance = balance[0] - amount
                    self.db_cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
                    self.db_connection.commit()
                    print(f"Withdrawal successful. New balance: {new_balance}")
                else:
                    print("Insufficient balance or invalid account.")
        except Exception as e:
            print(f"Error during withdrawal: {e}")

    def deposit(self):
        try:
            account_number = input("Enter Account Number: ")
            pin = input("Enter PIN: ")

            if self.validate_account(account_number, pin):
                amount = float(input("Enter amount to deposit: "))
                self.db_cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
                balance = self.db_cursor.fetchone()

                if balance:
                    new_balance = balance[0] + amount
                    self.db_cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_number))
                    self.db_connection.commit()
                    print(f"Deposit successful. New balance: {new_balance}")
        except Exception as e:
            print(f"Error during deposit: {e}")

    def transfer(self):
        try:
            print("1) To Account Number")
            print("2) To Mobile Number")
            choice = int(input("Choose an option: "))

            sender_account_number = input("Enter Your Account Number: ")
            pin = input("Enter PIN: ")

            if not self.validate_account(sender_account_number, pin):
                return

            amount = float(input("Enter amount to transfer: "))

            self.db_cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (sender_account_number,))
            sender_balance = self.db_cursor.fetchone()
            if not sender_balance or sender_balance[0] < amount:
                print("Insufficient balance or invalid account.")
                return

            if choice == 1:
                receiver_account_number = input("Enter Receiver Account Number: ")
                self.db_cursor.execute("SELECT account_number FROM accounts WHERE account_number = ?", (receiver_account_number,))
                receiver = self.db_cursor.fetchone()

                if receiver:
                    self.db_cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_number = ?", (amount, sender_account_number))
                    self.db_cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_number = ?", (amount, receiver_account_number))
                    self.db_connection.commit()
                    print("Transfer successful.")
                else:
                    print("Invalid receiver account number.")

            elif choice == 2:
                receiver_mobile = input("Enter Receiver Mobile Number: ")
                self.db_cursor.execute("SELECT account_number FROM accounts WHERE mobile = ?", (receiver_mobile,))
                receiver = self.db_cursor.fetchone()

                if receiver:
                    receiver_account_number = receiver[0]
                    self.db_cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_number = ?", (amount, sender_account_number))
                    self.db_cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_number = ?", (amount, receiver_account_number))
                    self.db_connection.commit()
                    print("Transfer successful.✔️")
                else:
                    print("Invalid receiver mobile number.❗")
        except Exception as e:
            print(f"Error during transfer: {e}")

    def run(self):
        while True:
            try:
                print("\n**********Bank Management System**********")
                print("1. Open Account")
                print("2. Check Balance")
                print("3. Withdraw")
                print("4. Deposit")
                print("5. Account Transfer")
                print("6. Exit")

                choice = int(input("Choose an option: "))

                if choice == 1:
                    self.create_account()
                elif choice == 2:
                    self.check_balance()
                elif choice == 3:
                    self.withdraw()
                elif choice == 4:
                    self.deposit()
                elif choice == 5:
                    self.transfer()
                elif choice == 6:
                    print("Thank you for using the Bank Management System.")
                    self.db_connection.close()
                    break
                else:
                    print("Invalid choice. Please try again.😥")
            except ValueError:
                print("Please enter a valid number.😊")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    system = BankManagementSystem()
    system.run()