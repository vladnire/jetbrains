import sys
import random


class CoordinateError(Exception):
    pass


class CellOccupyError(Exception):
    pass


class TicTacToe:
    """Basic TicTacToe game where
    players input coordinates"""

    def __init__(self):
        """Initialize and set empty field"""
        self.game_board = [' '] * 9
        self.size = len(self.game_board)
        self.move = 'X'
        self.player1 = None
        self.player2 = None
        self.current_player = None
        self.board_coords = {
                        (1, 3): 0, (2, 3): 1, (3, 3): 2,
                        (1, 2): 3, (2, 2): 4, (3, 2): 5,
                        (1, 1): 6, (2, 1): 7, (3, 1): 8
                        }

        self.winning_cases = [
                            (0, 1, 2), (3, 4, 5), (6, 7, 8),
                            (0, 3, 6), (1, 4, 7), (2, 5, 8),
                            (0, 4, 8), (2, 4, 6)
                            ]

    def game_menu(self):
        """Game menu"""
        while True:
            user_input = str(input("Input command: "))
            if user_input == 'exit':
                sys.exit('Bye!')
            try:
                start, player1, player2 = user_input.split()
                if start != 'start':
                    raise ValueError

                self.player1 = player1
                self.player2 = player2

                self.play_game()
            except ValueError:
                print("Bad parameters!")

    def play_game(self):
        """Play the game"""
        for i in range(1, 10):

            if i % 2 == 0:
                self.current_player = self.player2
            else:
                self.current_player = self.player1

            self.move = self.get_current_move()

            if self.current_player == 'user':
                self.user_move()
            else:
                self.ai_move()

            # Check if someone wins
            if self.check_win(self.game_board, self.move):
                print(f"{self.move} wins")
                self.restart_board()
                break
            # If there is not a winner and we are out of turns, we have a draw
            elif not self.check_for_empty():
                print("Draw")
                self.restart_board()
                break

    def restart_board(self):
        self.game_board = [' '] * 9
        self.move = 'X'

    def get_next_move(self):
        """Get the next move"""
        if self.move == 'X':
            return 'O'
        return 'X'

    def get_current_move(self):
        """Get current move based on field values count"""
        x_count = self.game_board.count('X')
        o_count = self.game_board.count('O')
        if x_count <= o_count:
            return 'X'
        return 'O'

    def check_for_empty(self):
        """Check to see if there is an empty cell"""
        return ' ' in self.game_board

    @staticmethod
    def get_empty_cells(board):
        """Return a list with empty cells indexes"""
        empty_cells = [idx for idx, e in enumerate(board) if e == ' ']
        return empty_cells

    def user_move(self):
        """User move implementation"""
        user_move_idx = self.get_user_move()
        # Set player input value in matrix
        self.game_board[user_move_idx] = self.move
        self.display_board()

    def random_move(self):
        """Implement random move for AI"""
        available_idx = self.get_empty_cells(self.game_board)
        return random.choice(available_idx)

    def ai_move(self):
        """Computer move"""
        if self.current_player == 'easy':
            easy_move = self.random_move()
            self.game_board[easy_move] = self.move
            print(f'Making move level {self.current_player}')
        elif self.current_player == 'medium':
            # Ai can win
            # Other player can win
            medium_move = self.ai_medium()
            self.game_board[medium_move] = self.move
            print(f'Making move level {self.current_player}')
        elif self.current_player == 'hard':
            hard_move = self.ai_hard()
            self.game_board[hard_move] = self.move
            print(f'Making move level {self.current_player}')
        self.display_board()

    def ai_medium(self):
        """Medium difficulty AI"""

        # If it already has two in a row and can win with one further move,
        # it does so.
        my_next_winning_move = self.search_next_win(self.move)
        if my_next_winning_move is not None:
            return my_next_winning_move

        # If its opponent can win with one move, it plays the move necessary
        # to block this.
        my_next_losing_move = self.search_next_win(self.get_next_move())
        if my_next_losing_move is not None:
            return my_next_losing_move

        # Otherwise, it makes a random move.
        return self.random_move()

    def search_next_win(self, player):
        """Search every combination of winning positions and get the
        empty position from that combination"""
        for i, j, k in self.winning_cases:
            if self.game_board[i] == player and \
               self.game_board[j] == player and \
               self.game_board[k] == ' ':
                return k
            elif self.game_board[j] == player and \
                 self.game_board[k] == player and \
                 self.game_board[i] == ' ':
                return i
            elif self.game_board[i] == player and \
                 self.game_board[k] == player and \
                 self.game_board[j] == ' ':
                return j
        return None

    def ai_hard(self):
        """Medium difficulty AI"""
        return self.minimax(self.game_board, self.move)['index']

    def minimax(self, board, player):
        """Min max function to get best hard ai move"""
        avail_spots = self.get_empty_cells(board)

        # If opponent wins return -10
        if self.check_win(board, self.get_next_move()):
            return {'score': -10}
        # If current ai wins, return 10, this is the wanted scenario
        elif self.check_win(board, self.move):
            return {'score': 10}
        elif len(avail_spots) == 0:
            return {'score': 0}
        else:
            moves = []
            for i in avail_spots:
                move = {'index': i}
                board[i] = player

                if player == self.move:
                    result = self.minimax(board, self.get_next_move())
                else:
                    result = self.minimax(board, self.move)

                # Update current move score and moves list
                move.update({'score': result['score']})
                moves.append(move)

                # Reset current board
                board[i] = ' '

            # Choose move with highest score
            if player == self.move:
                best_score = -20
                for move in moves:
                    if move['score'] > best_score:
                        best_score = move['score']
                        best_move = move
            # Choose move with lowest score
            else:
                best_score = 20
                for move in moves:
                    if move['score'] < best_score:
                        best_score = move['score']
                        best_move = move

        return best_move

    def display_board(self):
        """Print result in the required format"""
        print("-" * 9)
        for i in range(0, len(self.game_board), 3):
            row = self.game_board[i:i + 3]
            print('|', *row, '|', sep=' ')
        print('-' * 9)

    def get_user_move(self):
        """Get user index move based on input coordinates"""
        while True:
            user_input = input("Enter the coordinates: > ")
            try:
                col, row = map(int, user_input.split())
                if col not in [1, 2, 3] or row not in [1, 2, 3]:
                    raise CoordinateError
                idx = self.board_coords[(col, row)]
                if self.game_board[idx] != ' ':
                    raise CellOccupyError
                return idx
            except ValueError:
                print("You should enter numbers!")
            except CoordinateError:
                print("Coordinates should be from 1 to 3!")
            except CellOccupyError:
                print('This cell is occupied! Choose another one!')

    def check_win(self, board, move):
        """Check to see if we have a winner"""
        for i, j, k in self.winning_cases:
            if board[i] == move and board[j] == move and board[k] == move:
                return True
        return False


if __name__ == "__main__":
    game = TicTacToe()
    game.game_menu()
