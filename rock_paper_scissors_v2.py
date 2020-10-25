import random


class RockPaperScissors:
    """Rock-Paper-Scissors game or the more complex version
    rock,gun,lightning,devil,dragon,water,air,paper,sponge,wolf,
    tree,human,snake,scissors,fire"""


    def __init__(self):
        print("!!!Welcome to rock-paper-scissors!!!")
        self.player_score = 0
        self.computer_score = 0
        self.set_game_type()
        self.set_loosing_conditions()
        self.start_game()

    def set_game_type(self):
        """Choose what type of game you want to play"""
        valid_options = ["classic", "extended"]
        
        # Set a valid game type
        while True:
            type = str(input("Enter game type (classic or extended): > "))
            if type in valid_options:
                break
            else:
                print(f"Invalid game option, please choose one of: {valid_options}")           
        
        # Set game options
        if type == "classic":
            options = ["scissors", "paper", "rock"]
        else:
            options = ['rock', 'gun', 'lightning', 'devil', 
                'dragon', 'water', 'air', 'paper', 'sponge', 'wolf', 
                'tree', 'human', 'snake', 'scissors', 'fire']
            
        self.game_type = type
        self.game_options = options

        print(f"Valid choices: {options}")   
        print("Enter !score to show scores")
        print("Enter !exit to stop playing")
        print("Enter !rules to see loosing conditions")
        
    def set_loosing_conditions(self):
        """Set loosing conditions"""
        
        if self.game_type == "classic":
            self.loose = {
                "rock": "paper",
                "scissors": "rock",
                "paper": "scissors"
            }
            
        else:
            self.loose = {}
            for n, i in enumerate(self.game_options):
                self.loose[i] = (self.game_options[n + 1:] + 
                self.game_options[:n])[:(len(self.game_options) // 2) + 1]
        
    def user_input(self):
        """Get user input and check if it's valid"""
        player_choice = str(input("> "))
        valid_choices = self.game_options[::]
        for e in ['!exit', '!score', '!rules']:
            valid_choices.append(e)

        if player_choice not in valid_choices:
            self.user_choice = "Invalid input"
        else:
            self.user_choice = player_choice
    
    def check_result(self):
        """Choose an option for computer and return number of points"""
                
        computer = random.choice(self.game_options)

        # Check current result
        if self.user_choice == computer:
            print(f"There is a draw ({self.user_choice})")
            self.player_score += 50
            self.computer_score += 50
        elif self.user_choice in self.loose[computer]:
            print(f"Well done. The computer chose {computer} and failed")
            self.player_score += 100
        else:
            print(f"Sorry, but the computer chose {computer}")
            self.computer_score += 100
        
    def start_game(self):    
        """Start game, play until user exits"""
        
        while True:
            self.user_input()
            if self.user_choice == "Invalid input":
                print(self.user_choice)
            elif self.user_choice == '!exit':
                break
            elif self.user_choice == "!score":
                print(f"Your score: {self.player_score}")
                print(f"Computer score {self.computer_score}")
            elif self.user_choice == "!rules":
                for key, value in self.loose.items():
                    print(f"  {key} is beaten by {value}")                 
            else:
                self.check_result()
                
        if self.player_score > self.computer_score:
            print(f"Player wins {self.player_score} > {self.computer_score}")
        elif self.player_score < self.computer_score:
            print(f"Computer wins {self.computer_score} > {self.player_score}")
        else:
            print("There was a Draw!")
            
        print("Bye!")


RockPaperScissors()
