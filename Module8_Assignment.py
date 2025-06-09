import logging
import csv
import os

# Setup logger
logging.basicConfig(filename='atm_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
MAX_ATTEMPTS = 3
CORRECT_PIN = "1234"
STATE_FILE = 'atm_state.csv'

class ATM:
    def __init__(self):
        self.state = "Idle"
        self.attempts = 0
        self.balance = 1000.0  # Default balance if no file exists
        self.session_active = True
        self.load_state()

    def load_state(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    self.balance = float(row[0])
                    self.attempts = int(row[1])
                    logging.info(f"Loaded previous state: Balance=${self.balance}, Attempts={self.attempts}")
        else:
            logging.info("No previous ATM state found. Starting fresh.")

    def save_state(self):
        with open(STATE_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.balance, self.attempts])
            logging.info(f"Saved current state: Balance=${self.balance}, Attempts={self.attempts}")

    def log_state(self, event, guard, action):
        logging.info(f"STATE: {self.state} | EVENT: {event} [{guard}] / ACTION: {action}")

    def authenticate(self):
        self.state = "Authenticate"
        while self.attempts < MAX_ATTEMPTS:
            pin = input("Enter your 4-digit PIN: ")
            if pin == CORRECT_PIN:
                self.log_state("EnterPIN", "correct", "goToAuthenticated")
                print("PIN accepted. Authentication successful.")
                return True
            else:
                self.attempts += 1
                self.log_state("EnterPIN", "incorrect", "incrementCounter")
                print(f"Incorrect PIN. Attempt {self.attempts} of {MAX_ATTEMPTS}.")

        self.state = "Rejected"
        self.log_state("MaxAttemptsReached", "failed", "rejectUser")
        print("Too many incorrect attempts. Access denied.")
        return False

    def withdraw_funds(self):
        self.state = "Withdraw Funds"
        try:
            amount = float(input("Enter withdrawal amount: "))
            if amount <= 0:
                raise ValueError
        except ValueError:
            self.log_state("Withdraw", "invalid input", "abortTransaction")
            print("Invalid amount. Transaction aborted.")
            return

        if amount > self.balance:
            self.state = "Verify Balance"
            self.log_state("Withdraw", "balance < amount", "insufficientFunds")
            print("Insufficient funds.")
        else:
            self.balance -= amount
            self.state = "Dispense Cash"
            self.log_state("Withdraw", "balance >= amount", "dispenseCash")
            print(f"${amount:.2f} dispensed. Remaining balance: ${self.balance:.2f}")
            if self.balance == 0:
                self.state = "Close Session"
                self.log_state("BalanceCheck", "balance == 0", "closeAccount")
                print("Your account is now empty and will be closed.")

    def run(self):
        self.state = "Idle"
        print("Welcome to the ATM.")
        self.log_state("Start", "N/A", "goToAuthenticate")

        if not self.authenticate():
            self.save_state()
            return

        self.state = "Authenticated"
        while self.session_active:
            print("\nSelect an option:")
            print("1. Withdraw Funds")
            print("2. Check Balance")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.withdraw_funds()
            elif choice == "2":
                self.state = "Verify Balance"
                self.log_state("CheckBalance", "N/A", "displayBalance")
                print(f"Current balance: ${self.balance:.2f}")
            elif choice == "3":
                self.state = "Close Session"
                self.log_state("Exit", "N/A", "endSession")
                print("Thank you for using the ATM. Goodbye.")
                self.session_active = False
                self.save_state()
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    atm_machine = ATM()
    atm_machine.run()