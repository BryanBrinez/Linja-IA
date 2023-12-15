from linja import LinjaGame
import copy
class MinimaxAI:
    def __init__(self, juego, depth=2):
        self.juego = juego
        self.depth = depth

    def heuristica(self,game_state):
        red_score, black_score = game_state.calculate_scores()
        return red_score - black_score

    def apply_move(self, game_state, move):
        """
        Aplica un movimiento al estado del juego.

        :param game_state: El estado actual del juego.
        :param move: Una tupla que representa el movimiento (primer movimiento, segundo movimiento).
        """
        first_move, second_move = move

        # Aplicar el primer movimiento
        game_state.make_move(*first_move)
        # Aplicar el segundo movimiento
        game_state.make_second_move(*second_move)

    def generate_moves_and_evaluate(self):
        """
        Genera y aplica todos los posibles movimientos, evaluando el estado del juego después de cada uno.
        """
        possible_moves = self.juego.generate_possible_moves()
        evaluations = []

        for move in possible_moves:
            game_state_copy = copy.deepcopy(self.juego)
            self.apply_move(game_state_copy, move)
            board_value = self.heuristica(game_state_copy)
            evaluations.append((move, board_value))

        return evaluations

    

    def minimax(self, game_state, depth, maximizing_player):
        if depth == 0 or game_state.game_over():
            return self.heuristica(game_state)

        if maximizing_player:
            max_eval = float('-inf')
            for move in game_state.generate_possible_moves():
                game_state_copy = copy.deepcopy(game_state)
                self.apply_move(game_state_copy, move)
                eval = self.minimax(game_state_copy, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in game_state.generate_possible_moves():
                game_state_copy = copy.deepcopy(game_state)
                self.apply_move(game_state_copy, move)
                eval = self.minimax(game_state_copy, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
        
    def get_best_move(self, game_state, depth):
        best_eval = float('-inf')
        best_move = None

        for move in game_state.generate_possible_moves():
            game_state_copy = copy.deepcopy(game_state)
            self.apply_move(game_state_copy, move)
            eval = self.minimax(game_state_copy, depth - 1, False)  # False para el jugador oponente
            if eval > best_eval:
                best_eval = eval
                best_move = move

        return best_move






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