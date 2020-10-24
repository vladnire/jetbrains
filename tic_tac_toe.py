class TicTacToe:
    """Basic TicTacToe game where
    players input coordinates"""

    def __init__(self):
        """Initialize and set empty field"""
        self.field = [['_', '_', '_'],
                      ['_', '_', '_'],
                      ['_', '_', '_']]
        self.size = len(self.field)

    def play_game(self):
        """Play the game"""
        self.print_cells()
        turns = 1
        value = 'X'

        while turns < 10:
            coords = self.get_coordinates()

            # Set player input value in matrix
            self.field[coords[0]][coords[1]] = value
            self.print_cells()

            # Check if someone wins or if out of turns
            if self.check_win(value):
                print(f"{value} wins")
                break
            elif turns == 9:
                print('Draw')
                break

            if value == 'X':
                value = 'O'
            else:
                value = 'X'

            turns += 1

    def print_cells(self):
        """Print result in the required format"""
        print("---------")
        for row in self.field:
            print('| ' + row[0] + ' ' + row[1] + ' ' + row[2] + ' |')
        print("---------")

    def get_coordinates(self):
        """Check if provided coordinates are ok
        and return the matrix coordinates"""
        coord_flag = False
        while not coord_flag:
            coord = str(input("Enter the coordinates: "))
            coord = coord.split(' ')

            if len(coord) != 2:
                print("You should enter two coordinates!")
                continue

            if not coord[0].isdigit() or not coord[1].isdigit():
                print("You should enter numbers!")
                continue

            coord = [int(e) for e in coord]
            if coord[0] not in [1, 2, 3] or coord[1] not in [1, 2, 3]:
                print("Coordinates should be from 1 to 3!")
                continue

            # Transpose coordinates to matrix format
            x_coord = 3 - coord[1]
            y_coord = coord[0] - 1

            # Check to see if position is occupied
            if self.field[x_coord][y_coord] == "_":
                coord_flag = True
            else:
                print("This cell is occupied! Choose another one!")

            matrix_coords = [x_coord, y_coord]

        return matrix_coords

    def check_win(self, mark):
        """Check to see if we have a winner"""
        lst_check = [mark, mark, mark]

        # Check rows and columns
        transposed_matrix = map(list, zip(*self.field))
        if lst_check in self.field or lst_check in transposed_matrix:
            return True

        # Check main diagonal
        if lst_check == [self.field[i][i] for i in range(self.size)]:
            return True

        # Check secondary diagonal
        if lst_check == [self.field[i][~i] for i in range(self.size)]:
            return True

        return False


game = TicTacToe()
game.play_game()
