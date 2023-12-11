# Actualizando la función para contar piezas en la columna de destino del movimiento
def contar_diferentes_a_free_en_columna(matriz, columna):
    contador = 0
    for fila in matriz:
        if fila[columna] != "Free":
            contador += 1
    return contador

# Actualizando la clase LinjaGame con la lógica corregida para el conteo de piezas
class LinjaGame:
    def __init__(self):
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
        self.current_player = "Red"
        self.second_move_distance = 0

    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        print("\n")

    def make_move(self, start_row, start_col, end_row, end_col):
        if self.is_move_legal(start_row, start_col, end_row, end_col):
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = "Free"
            
            # Contar piezas en la columna de destino, excluyendo la pieza movida
            self.second_move_distance = contar_diferentes_a_free_en_columna(self.board, end_col) - 1
            return self.second_move_distance
        else:
            print("Illegal move")
            return False

    
    def make_second_move(self, start_row, start_col, end_row, end_col):
        if self.is_second_move_legal(start_row, start_col, end_row, end_col):
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = "Free"
            self.current_player = "Black" if self.current_player == "Red" else "Red"
            self.second_move_distance = 0  # Resetear la distancia para el segundo movimiento
            return True
        else:
            print("Illegal second move")
            return False


    def is_move_legal(self, start_row, start_col, end_row, end_col):
        if self.board[end_row][end_col] != "Free":
            return False

        if self.current_player == "Red" and self.board[start_row][start_col] != "Red":
            return False
        if self.current_player == "Black" and self.board[start_row][start_col] != "Black":
            return False

        move_direction = 1 if self.current_player == "Red" else -1

        # Allow diagonal and straight moves
        if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
            if (self.current_player == "Red" and end_col > start_col) or (self.current_player == "Black" and end_col < start_col):
                return True

        if start_col + move_direction == end_col and start_row == end_row:
            return True

        return False


    def is_second_move_legal(self, start_row, start_col, end_row, end_col):
        # Comprobar si el destino está vacío
        if self.board[end_row][end_col] != "Free":
            return False

        # Calcular la distancia del movimiento
        row_distance = abs(end_row - start_row)
        col_distance = abs(end_col - start_col)

        # Verificar la distancia para movimientos rectos y diagonales
        if row_distance == 0 or col_distance == 0:  # Movimiento recto
            if row_distance + col_distance != self.second_move_distance:
                return False
        else:  # Movimiento diagonal
            if max(row_distance, col_distance) != self.second_move_distance:
                return False

        # Verificar la dirección del movimiento
        if self.current_player == "Red":
            if col_distance > 0 and end_col <= start_col:
                return False
        elif self.current_player == "Black":
            if col_distance > 0 and end_col >= start_col:
                return False

        return True

# Crear una instancia del juego y realizar el primer movimiento
game = LinjaGame()
pieces_to_move = game.make_move(1, 0, 1, 1)  # Mover de (1,0) a (1,1)
print(pieces_to_move)  

game.display_board()


game.make_second_move(3,0, 3,2)
game.display_board()

# Ahora debería dar 2 según la descripción proporcionada
#game.display_board()
#pieces_to_move = game.make_move(2, 0, 2, 1) 
#print(pieces_to_move)
#game.display_board()
#pieces_to_move = game.make_move(7, 2, 6, 3) 
#print(pieces_to_move)
#game.display_board()