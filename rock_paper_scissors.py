import random


def get_score():
    """Enter name, read score file
    Return the score if in file or 0 if not"""
    player_name = str(input("Enter your name: "))

    print(f"Hello, {player_name}")

    scores_list = []
    with open('rating.txt', 'r') as f:
        scores_list = f.read().splitlines()

    for line in scores_list:
        if player_name in line:
            return int(line.split(' ')[1])

    return 0


def get_options():
    """Get game options"""
    options = str(input())

    if options:
        options = options.split(',')
    else:
        options = ["scissors", "paper", "rock"]

    print("Okay, let's start")

    return options


def user_input(options):
    """Get user input and check if it's valid"""

    player_choice = str(input())
    valid_choices = options[::]
    valid_choices.append('!exit')
    valid_choices.append('!rating')

    if player_choice not in valid_choices:
        return "Invalid input"

    return player_choice


def check_result(player, options):
    """Choose an option for computer and return number of points"""
    default_options = ["scissors", "paper", "rock"]
    computer = random.choice(options)

    if options == default_options:
        loose = {
            "rock": "paper",
            "scissors": "rock",
            "paper": "scissors"
        }
    else:
        loose = {}
        for n, i in enumerate(options):
            loose[i] = (options[n + 1:] + options[:n])[:(len(options) // 2) + 1]

    if player == computer:
        print(f"There is a draw ({player})")
        points = 50
    elif player in loose[computer]:
        print(f"Well done. The computer chose {computer} and failed")
        points = 100
    else:
        print(f"Sorry, but the computer chose {computer}")
        points = 0

    return points


if __name__ == "__main__":

    score = get_score()
    game_options = get_options()

    while True:
        user = user_input(game_options)
        if user == "Invalid input":
            print(user)
        elif user == '!exit':
            break
        elif user == "!rating":
            print(f"Your rating: {score}")
        else:
            score += check_result(user, game_options)

    print("Bye!")
