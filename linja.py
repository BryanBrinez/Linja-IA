class LinjaGame:
    def __init__(self):
        # Initialize the game board as an 8x8 matrix with "Free" for empty spaces
        self.board = [
            ["Free", "Black", "Black", "Black", "Black", "Black", "Black", "Free"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Free", "Red", "Red", "Red", "Red", "Red", "Red", "Free"]
        ]
        self.current_player = "Red"  # Red starts the game

    def display_board(self):
        # Display the game board
        for row in self.board:
            print(" ".join(row))
        print("\n")

    def make_move(self, start_row, start_col, end_row, end_col):
        # Move a piece from start position to end position if the move is legal
        if self.is_move_legal(start_row, start_col, end_row, end_col):
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = "Free"
            return True
        else:
            print("Illegal move")
            return False

    def is_move_legal(self, start_row, start_col, end_row, end_col):
        # Check if the end position is free
        if self.board[end_row][end_col] != "Free":
            return False

        # Check if the starting position matches the current player's piece
        if self.current_player == "Red" and self.board[start_row][start_col] != "Red":
            return False
        if self.current_player == "Black" and self.board[start_row][start_col] != "Black":
            return False

        # Calculate the allowed move direction based on the current player
        move_direction = 1 if self.current_player == "Red" else -1

        # Check if the move is diagonal and in the allowed direction
        if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
            if (self.current_player == "Red" and end_col > start_col) or (self.current_player == "Black" and end_col < start_col):
                return True

        # Check if the move is a standard move in the allowed direction
        if start_col + move_direction == end_col and start_row == end_row:
            return True

        return False

# Create an instance of the game
game = LinjaGame()
game.display_board()

# Let's test moving a piece
#game.make_move(7, 2, 6, 3)  # Attempt to move a Red piece diagonally to the right
#game.make_move(0, 3, 1, 2)
#game.make_move(1, 7, 1, 6)
game.make_move(1, 0, 1, 1)
game.display_board()

# Now let's test a straight move to the right for Red
#game.make_move(0, 1, 1, 1)  # Attempt to move a Red piece straight to the right
#game.display_board()
