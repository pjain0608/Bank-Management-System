# Bank-Management-System

This project is a Python-based Bank Management System that allows users to manage basic banking operations such as account creation, balance checks, deposits, withdrawals, and transfers. The application uses SQLite for database management, ensuring data persistence.

## Features
1)  **Account Management**
-  Create new accounts with a 12-digit unique account number.
-  Set and encrypt a 4-digit PIN for secure account access.

2) **Banking Operations**
-  **Check Balance**: View account balance using account number, mobile number, or email ID.
-  **Deposit Money**: Add funds to an account securely.
-  **Withdraw Money**: Safely withdraw funds from an account.
-  **Transfer Money**: Transfer funds to other accounts using account numbers or mobile numbers.

3) **Security**
-  PIN encryption using a custom character mapping for added security.
-  Validation checks for secure account access.

4) **Database Integration**
-  Data is stored in an SQLite database (bank_management_system.db) for persistent and reliable storage.

5) **User-Friendly Interface**
-  Simple text-based menu for interaction.
-  Clear prompts and error handling for ease of use.

# How it works

1) **Open Account**:
-  Enter personal details (Name, Mobile, Email).
-  A 12-digit account number is generated automatically.
-  Set a 4-digit PIN for your account.

2) **Check Balance**:
-  Choose to check your balance using account number, mobile number, or email ID.

3) **Deposit & Withdraw**:
-  Deposit funds or withdraw money securely by providing the account number and PIN.

4) **Transfer Funds**:
-  Transfer money to another account using the recipient's account number or mobile number.


