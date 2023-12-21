# Actualizando la función para contar piezas en la columna de destino del movimiento

import copy
# Actualizando la clase LinjaGame con la lógica corregida para el conteo de piezas
class LinjaGame:
    def __init__(self):
        #Tablero default
        self.board = [
            ["Red", "Black", "Black", "Black", "Black", "Black", "Black", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Free", "Free", "Free", "Free", "Free", "Free", "Black"],
            ["Red", "Red", "Red", "Red", "Red", "Red", "Red", "Black"]
            
        ]
        self.current_player = "Red"  
        
        self.second_move_distance = 0

    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        print("\n")

    def contar_diferentes_a_free_en_columna(self, columna):
        #Cuenta cuantos black o red hay en una columna
        contador = 0
        for fila in self.board:
            if fila[columna] != "Free":
                contador += 1
        return contador

    def make_move(self, start_row, start_col, end_row, end_col):
        if self.is_move_legal(start_row, start_col, end_row, end_col):
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = "Free"

            # Establecer la distancia inicial para el segundo movimiento, se le resta 1, ya que es la ficha recien movida
            self.second_move_distance = self.contar_diferentes_a_free_en_columna(end_col) - 1

            

            if self.second_move_distance == 0: 
                self.change_turn()
                return True
                
            



            # Ajustar la distancia del segundo movimiento si no hay movimientos legales disponibles
            while self.second_move_distance > 0 and not self.any_legal_second_move():
                self.second_move_distance -= 1

            return self.second_move_distance
        else:
            print("Illegal move")
            return False
        


    def find_all_possible_first_moves(self):
        #busca todas las primeros movimientos 
        possible_moves = []
        for start_row in range(len(self.board)):
            for start_col in range(len(self.board[start_row])):
                if self.board[start_row][start_col] == self.current_player:
                    for end_row in range(len(self.board)):
                        for end_col in range(len(self.board[end_row])):
                            if self.is_move_legal(start_row, start_col, end_row, end_col):
                                possible_moves.append((start_row, start_col, end_row, end_col))
        return possible_moves


    def find_all_possible_second_moves(self):
        #busca todas los segundos movimientos 
        possible_moves = []
        for start_row in range(len(self.board)):
            for start_col in range(len(self.board[start_row])):
                if self.board[start_row][start_col] == self.current_player:
                    for end_row in range(len(self.board)):
                        for end_col in range(len(self.board[end_row])):
                            if self.is_second_move_legal(start_row, start_col, end_row, end_col):
                                possible_moves.append((start_row, start_col, end_row, end_col))
        return possible_moves

    def any_legal_second_move(self):
        # Verificar si hay algún segundo movimiento legal con la distancia actual
        for start_row in range(len(self.board)):
            for start_col in range(len(self.board[start_row])):
                if self.board[start_row][start_col] == self.current_player:
                    for end_row in range(len(self.board)):
                        for end_col in range(len(self.board[end_row])):
                            if self.is_second_move_legal(start_row, start_col, end_row, end_col):
                                return True
        return False
    
    def make_second_move(self, start_row, start_col, end_row, end_col):
        print(self.second_move_distance)
        if self.is_second_move_legal(start_row, start_col, end_row, end_col):
            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = "Free"
            #self.change_turn()
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

        # permitir diagonal
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

        # Verificar que el movimiento no sea en la misma columna
        if start_col == end_col:
            return False

        # Movimientos diagonales: la distancia en filas y columnas debe ser igual y igual a second_move_distance
        if row_distance == col_distance and row_distance == self.second_move_distance:
            pass
        # Movimientos rectos horizontales: distancia en filas es 0 y distancia en columnas igual a second_move_distance
        elif row_distance == 0 and col_distance == self.second_move_distance:
            pass
        else:
            return False

        # Verificar la dirección del movimiento
        if self.current_player == "Red":
            # "Red" solo puede moverse hacia la derecha
            if end_col <= start_col:
                return False
        elif self.current_player == "Black":
            # "Black" solo puede moverse hacia la izquierda
            if end_col >= start_col:
                return False

        return True

    def check_winner(self):
        if not self.game_over():
            return None, None, None  # Juego no ha terminado aún

        #si termina calcula el puntaje
        red_score, black_score = self.calculate_scores()
        
        if red_score > black_score:
            return 'Red', red_score, black_score
        elif black_score > red_score:
            return 'Black', red_score, black_score
        else:
            return 'Tie', red_score, black_score

    def game_over(self):
        # Contar las fichas rojas en las columnas 4, 5, 6, 7
        reds_on_right_side = sum(row[col] == "Red" for row in self.board for col in range(4, 8))
        print("las red", reds_on_right_side)
        
        # Contar las fichas negras en las columnas 0, 1, 2, 3
        blacks_on_left_side = sum(row[col] == "Black" for row in self.board for col in range(4))

        print("las blac", blacks_on_left_side)
        
        # Asegurarse de que no hay fichas rojas en las columnas 0, 1, 2, 3
        no_reds_on_left_side = all(row[col] != "Red" for row in self.board for col in range(4))
        print("las no red", no_reds_on_left_side)
        # Asegurarse de que no hay fichas negras en las columnas 4, 5, 6, 7
        no_blacks_on_right_side = all(row[col] != "Black" for row in self.board for col in range(4, 8))
        print("las no black", no_blacks_on_right_side)

        # Verificar si todas las fichas están en sus respectivas columnas
        return reds_on_right_side == 12 and blacks_on_left_side == 12 and no_reds_on_left_side and no_blacks_on_right_side


    

    def count_colors_and_columns(self):
        count = {"Red": {}, "Black": {}}
        for i, row in enumerate(self.board):
            for j, color in enumerate(row):
                if color in ["Red", "Black"]:
                    if j in count[color]:
                        count[color][j] += 1
                    else:
                        count[color][j] = 1
        return count

    def calculate_score_with_multipliers(self, count, multipliers):
        return sum(count.get(col, 0) * multiplier for col, multiplier in multipliers.items())

    def calculate_scores(self):
        color_counts = self.count_colors_and_columns()

        red_multipliers = {7: 5, 6: 3, 5: 2, 4: 1}
        black_multipliers = {0: 5, 1: 3, 2: 2, 3: 1}

        red_score = self.calculate_score_with_multipliers(color_counts["Red"], red_multipliers)
        black_score = self.calculate_score_with_multipliers(color_counts["Black"], black_multipliers)

        return red_score, black_score


    def change_turn(self):
        self.current_player = "Black" if self.current_player == "Red" else "Red"

    def generate_possible_moves(self, player):
        possible_moves = []
        for start_row in range(len(self.board)):
            for start_col in range(len(self.board[start_row])):
                if self.board[start_row][start_col] == player:
                    for end_row in range(len(self.board)):
                        for end_col in range(len(self.board[end_row])):
                            # Crear una copia del estado del juego para probar el movimiento
                            game_state_copy = copy.deepcopy(self)
                            if game_state_copy.make_move(start_row, start_col, end_row, end_col):
                                # Probar todos los posibles segundos movimientos
                                for second_start_row in range(len(game_state_copy.board)):
                                    for second_start_col in range(len(game_state_copy.board[second_start_row])):
                                        if game_state_copy.board[second_start_row][second_start_col] == player:
                                            for second_end_row in range(len(game_state_copy.board)):
                                                for second_end_col in range(len(game_state_copy.board[second_end_row])):
                                                    if game_state_copy.make_second_move(second_start_row, second_start_col, second_end_row, second_end_col):
                                                        # Agregar ambos movimientos a la lista de posibles movimientos
                                                        possible_moves.append(((start_row, start_col, end_row, end_col), (second_start_row, second_start_col, second_end_row, second_end_col)))
                                                        # Restaurar el tablero después de probar el segundo movimiento
                                                        game_state_copy.board = copy.deepcopy(self.board)

        return possible_moves
    
    

        
        

            


        
# Crear una instancia del juego y realizar el primer movimiento
#game = LinjaGame()
#pieces_to_move = game.make_move(1, 0, 1, 1)  # Mover de (1,0) a (1,1)
#print(pieces_to_move)  
#game.display_board()
#movimientos = game.generar_movimientos()
#print(movimientos) 


#game.make_second_move(3,0, 3,2)
#game.display_board()

#winner  = game.check_winner()
#print(winner)
#game.make_second_move(7,2, 5,3)
#game.display_board()


#winner  = game.check_winner()
#print(winner)

# Ahora debería dar 2 según la descripción proporcionada
#game.display_board()
#pieces_to_move = game.make_move(2, 0, 2, 1) 
#print(pieces_to_move)
#game.display_board()
#pieces_to_move = game.make_move(7, 2, 6, 3) 
#print(pieces_to_move)
#game.display_board()