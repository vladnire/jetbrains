import sys


class CoffeeMachine:
    """Coffee Machine"""

    def __init__(self, water, milk, beans, cups, money):
        """Create CoffeeMachine with starting ingredients and money"""
        self.money = money
        self.water = water
        self.milk = milk
        self.beans = beans
        self.cups = cups

        while True:
            action = str(input("\nWrite action (buy, fill, take, remaining, exit):\n"))
            if action == "exit":
                sys.exit()
            elif action == "buy":
                self.buy()
            elif action == "take":
                self.take()
            elif action == "fill":
                self.fill()
            elif action == "remaining":
                self.print_state()

    def print_state(self):
        """Print CoffeeMachine state"""
        print("The coffee machine has:")
        print(f"{self.water} of water")
        print(f"{self.milk} of milk")
        print(f"{self.beans} of coffee beans")
        print(f"{self.cups} of disposable cups")
        print(f"${self.money} of money")

    def buy(self):
        """Buy a type of coffee or go back to menu"""
        buy_request = str(input("\nWhat do you want to buy? "
                                "1 - espresso, "
                                "2 - latte, "
                                "3 - cappuccino:, "
                                "back - to main menu:\n"))

        if buy_request == '1':
            self.espresso()
        elif buy_request == '2':
            self.latte()
        elif buy_request == '3':
            self.cappuccino()
        elif buy_request == "back":
            pass

    def take(self):
        """Take money from machine"""
        print(f"I gave you ${self.money}\n")
        self.money = 0

    def fill(self):
        """Fill the machine"""
        water = int(input("Write how many ml of water do you want to add:\n"))
        milk = int(input("Write how many ml of milk do you want to add:\n"))
        beans = int(input("Write how many grams of coffee beans do you want to add:\n"))
        cups = int(input("Write how many disposable cups of coffee do you want to add:\n"))
        self.update_machine(water, milk, beans, 0, cups)

    def espresso(self):
        """Buy an espresso
        250 water 16 beans 4$"""
        self.check_resources(250, 0, 16, 4)

    def latte(self):
        """Buy a latte
        350 water 75 milk 20 beans 7$"""
        self.check_resources(350, 75, 20, 7)

    def cappuccino(self):
        """Buy a cappuccino
        200 water 100 milk 12 beans 6$"""
        self.check_resources(200, 100, 12, 6)

    def update_machine(self, water, milk, beans, price, cups):
        """Update machine ingredients and money"""
        self.water += water
        self.milk += milk
        self.beans += beans
        self.money += price
        self.cups += cups

    def check_resources(self, water, milk, beans, price):
        """Check to see if there are enough resources
        If not, print what is missing"""
        if self.water < water:
            print("Sorry, not enough water!")
        elif self.milk < milk:
            print("Sorry, not enough milk!")
        elif self.beans < beans:
            print("Sorry, not enough coffee beans!")
        elif self.cups < 1:
            print("Sorry, not enough cups!")
        else:
            print("I have enough resources, making you a coffee!")
            self.update_machine(-water, -milk, -beans, price, -1)


if __name__ == '__main__':
    # create coffee machine with starting ingredients
    CoffeeMachine(400, 540, 120, 9, 550)
