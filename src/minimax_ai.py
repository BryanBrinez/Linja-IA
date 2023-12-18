from linja import LinjaGame
import copy
class MinimaxAI:
    def __init__(self, juego, depth=1):
        self.juego = juego
        self.depth = depth

    def heuristic(self, game_state):
        # Calcular las puntuaciones desde la perspectiva de 'Black'
        red_score, black_score = game_state.calculate_scores()
        red_distance_penalty = self.calculate_average_distance_penalty(game_state, "Red")
        black_distance_penalty = self.calculate_average_distance_penalty(game_state, "Black")
        
        # Evaluar los movimientos de 'Red' (el oponente de 'Black')
        red_moves = self.count_opponent_moves(game_state, "Red")


        #[((0,1,0,2),(2,2,3,4))]
        
        # Ajustar la puntuación tomando en cuenta los movimientos del oponente
        # Una mayor puntuación para 'Black' y un menor número de movimientos para 'Red' es mejor
        return black_score - black_distance_penalty - (red_score - red_distance_penalty) - red_moves


    def count_opponent_moves(self, game_state, player):
        # Contar el número de movimientos posibles para el jugador indicado
        return len(game_state.generate_possible_moves(player))
    


    def calculate_average_distance_penalty(self, game_state, color):

        #Distancia entre las fichas
        positions = []
        for i, row in enumerate(game_state.board):
            for j, piece in enumerate(row):
                if piece == color:
                    positions.append((i, j))

        if len(positions) < 2:
            return 0

        total_distance = 0
        for pos1 in positions:
            for pos2 in positions:
                if pos1 != pos2:
                    total_distance += self.calculate_distance(pos1, pos2)

        average_distance = total_distance / (len(positions) * (len(positions) - 1))
        return average_distance

    def calculate_distance(self, pos1, pos2):
        
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def apply_move(self, game_state, move):
       
        first_move, second_move = move

        # Aplicar el primer movimiento
        game_state.make_move(*first_move)
        # Aplicar el segundo movimiento
        game_state.make_second_move(*second_move)

    

    def minimax(self, game_state, depth, maximizing_player):
        # Chequear la condición de terminación: profundidad cero o juego terminado.
        if depth == 0 or game_state.game_over():
            return self.heuristic(game_state)  # Evaluar el estado del juego usando la función heurística.

        if maximizing_player:
            # Inicializar el valor máximo para un jugador que maximiza (IA o jugador actual).
            max_eval = float('-inf')
            for move in game_state.generate_possible_moves(self.juego.current_player):
                # Crear una copia del estado del juego para probar cada posible movimiento.
                game_state_copy = copy.deepcopy(game_state)
                self.apply_move(game_state_copy, move)  # Aplicar el movimiento a la copia.
                # Llamar recursivamente a minimax, disminuyendo la profundidad y cambiando al jugador minimizador.
                eval = self.minimax(game_state_copy, depth - 1, False)
                max_eval = max(max_eval, eval)  # Actualizar el valor máximo si se encuentra una mejor evaluación.
            return max_eval  # Devolver la mejor evaluación para los movimientos del jugador maximizador.
        else:
            # Similar al caso anterior, pero para un jugador que minimiza (generalmente el oponente).
            min_eval = float('inf')
            for move in game_state.generate_possible_moves(self.juego.current_player):
                game_state_copy = copy.deepcopy(game_state)
                self.apply_move(game_state_copy, move)
                eval = self.minimax(game_state_copy, depth - 1, True)
                min_eval = min(min_eval, eval)  # Actualizar el valor mínimo si se encuentra una evaluación más baja.
            return min_eval  # Devolver la mejor evaluación para los movimientos del jugador minimizador.

    def get_best_move(self, game_state, depth):
        # Inicializar la mejor evaluación y el mejor movimiento.
        best_eval = float('-inf')
        best_move = None

        # Iterar sobre todos los posibles movimientos del jugador actual.
        for move in game_state.generate_possible_moves(self.juego.current_player):
            game_state_copy = copy.deepcopy(game_state)  # Crear una copia del estado actual del juego.
            self.apply_move(game_state_copy, move)  # Aplicar el movimiento a la copia.
            # Evaluar el movimiento usando la función minimax.
            eval = self.minimax(game_state_copy, depth - 1, False)  # False indica que el siguiente turno es del oponente.
            if eval > best_eval:
                best_eval = eval  # Actualizar la mejor evaluación si se encuentra un mejor movimiento.
                best_move = move  # Actualizar el mejor movimiento.

        return best_move  # Devolver el mejor movimiento encontrado.





game = LinjaGame()
ai = MinimaxAI(game)

#game.display_board()
#mov = game.generate_possible_moves()
#print(mov)

#generated_boards = ai.generate_moves_and_evaluate()


# Imprimir los tableros generados

#game.make_move(1,0,1,1)
#game.make_second_move(2,0,2,2)


#game.make_move(1,7,1,6)
#turn = game.current_player

#print(turn)

#game.display_board()

#       
#mov = game.generate_possible_moves()
#print(mov)

#


#game.display_board()
#mov = game.generar_movimientos()
#print(mov)