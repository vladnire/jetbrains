import random
import sys
import sqlite3


class BankingSystem:
    def __init__(self):
        self.card_number = None
        self.pin = None
        self.logged_in = False
        self.balance = 0
        self._create_database()

        while True:
            self._menu()

    def _create_database(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute("DROP table IF EXISTS card")
        self.cur.execute("CREATE TABLE IF NOT EXISTS card ("
                         "id INTEGER,"
                         "number TEXT,"
                         "pin TEXT,"
                         "balance INTEGER DEFAULT 0)")
        self.conn.commit()

    def _menu(self):
        if not self.logged_in:
            choice = input("1. Create an account\n"
                           "2. Log into account\n"
                           "0. Exit\n")
            if choice == "1":
                self._generate_credit_card()
            elif choice == "2":
                self._log_in()
            elif choice == "0":
                self.conn.close()
                sys.exit("Bye!")
        else:
            choice = input("1. Balance\n"
                           "2. Add income\n"
                           "3. Do transfer\n"
                           "4. Close account\n"
                           "5. Log out\n"
                           "0. Exit\n")
            if choice == "1":
                balance = self._check_balance()
                print(f"Balance: {balance}")
            elif choice == "2":
                self._add_income()
            elif choice == "3":
                self._do_transfer()
            elif choice == "4":
                self._close_account()
            elif choice == "5":
                self._log_out()
            elif choice == "0":
                self.conn.close()
                sys.exit("Bye!")

    def _generate_credit_card(self):
        self.card_number = self._luhn_algorithm()
        self.pin = self._generate_credit_card_pin()
        print(
            "Your card has been created",
            "Your card number:",
            self.card_number,
            "Your card PIN:",
            self.pin,
            sep="\n",
        )
        self._add_card_to_database()

    def _add_card_to_database(self):
        self.id = 0
        self.cur.execute("INSERT INTO card VALUES (?, ?, ?, ?)",
                         (self.id, self.card_number, self.pin, self.balance))
        self.conn.commit()
        self.id += 1

    def _log_in(self):
        card_number = input("Enter your card number:\n")
        pin = input("Enter your PIN:\n")
        if self._check_card_exists(card_number):
            self.card_number = card_number
            self.cur.execute("SELECT * FROM card WHERE number = ?", [self.card_number])
            self.pin = self.cur.fetchone()[2]
            if self.pin == pin:
                print("\nYou have successfully logged in!")
                self.logged_in = True
            else:
                print("\nWrong card number or PIN!")
        else:
            print("\nWrong card number or PIN!")

    def _check_card_exists(self, card):
        self.cur.execute("SELECT * FROM card WHERE number = ?", [card])
        if self.cur.fetchone():
            return True
        return False

    def _check_balance(self):
        self.cur.execute("SELECT * FROM card WHERE number = ?", [self.card_number])
        return self.cur.fetchone()[-1]

    def _add_income(self):
        income = int(input("Enter income:\n"))
        self.balance += income
        self.cur.execute("UPDATE card SET balance = ? WHERE number = ?", [self.balance, self.card_number])
        self.conn.commit()
        print("Income was added!")

    def _do_transfer(self):
        self.transfer_card = str(input("Enter card number:\n"))

        if self.transfer_card[-1] != self._get_luhn_checksum(self.transfer_card[:-1]):
            print("Probably you made mistake in card number. Please try again!")

        if not self._check_card_exists(self.transfer_card):
            print("Such a card does not exist.")

        elif self.transfer_card == self.card_number:
            print("You can't transfer money to the same account!")

        else:
            self.transfer_money = int(input("Enter how much money you want to transfer:\n"))
            if self.transfer_money > self.balance:
                print("Not enough money!")
            else:
                # Update sender card balance
                self._update_balance(self.card_number, -self.transfer_money)
                # Update receiver card balance
                self._update_balance(self.transfer_card, self.transfer_money)
                print("Success!")

    def _update_balance(self, card, transfer_money):
        self.cur.execute("SELECT * FROM card WHERE number = ?", [card])
        card_balance = self.cur.fetchone()[-1]
        card_balance += transfer_money
        self.cur.execute("UPDATE card SET balance = ? WHERE number = ?", [card_balance, card])
        self.conn.commit()

    def _close_account(self):
        self.cur.execute("DELETE FROM card WHERE number = ?", [self.card_number])
        self.conn.commit()
        print("The account has been closed!")

    def _log_out(self):
        self.logged_in = False
        print("You have successfully logged out!")

    def _generate_credit_card_number(self):
        return "".join(["400000", f"{random.randint(0,999999999):09d}"])

    def _generate_credit_card_pin(self):
        return f"{random.randint(0,9999):04d}"

    def _get_luhn_checksum(self, card):

        card_nr_list = [int(e) for e in card]

        # Multiply odd index digits by 2
        for i in range(0, len(card_nr_list), 2):
            card_nr_list[i] *= 2

        # Subtract 9 from numbers over 9
        for i in range(len(card_nr_list)):
            if card_nr_list[i] > 9:
                card_nr_list[i] -= 9

        # Add all numbers
        card_sum = sum(card_nr_list)

        if card_sum % 10 == 0:
            checksum = 0
        else:
            checksum = 10 - card_sum % 10

        return checksum

    def _luhn_algorithm(self):
        luhn_card = self._generate_credit_card_number()
        checksum = self._get_luhn_checksum(luhn_card)
        return luhn_card + str(checksum)


def main():
    BankingSystem()


if __name__ == "__main__":
    main()
