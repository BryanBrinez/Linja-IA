import tkinter as tk
from tkinter import messagebox, ttk
from linja import LinjaGame  # Importa la clase LinjaGame
from PIL import Image, ImageTk
from tkinter import filedialog
from minimax_ai import MinimaxAI
import copy

class LinjaGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.selected_piece = None
        self.square_size = 50  # Tamaño de cada cuadrado del tablero
        self.margins = 100    # Márgenes en píxeles

         # Cargar y colocar la imagen de fondo
        
        self.root.geometry("800x600")

        self.load_background_image()


        self.highlighted_squares = []

        self.load_images()     # Cargar las imágenes
        # Crea una instancia de MinimaxAI
        self.ai = MinimaxAI(game)

        # Etiqueta para mostrar el turno actual del jugador (en la parte superior)
        self.turn_label = ttk.Label(root, text=f"Turno actual: {self.game.current_player}", font=("Helvetica", 16))
        self.turn_label.pack()
        self.steps_label = ttk.Label(root, text="Pasos disponibles para el segundo movimiento: 0", font=("Helvetica", 12))
        self.steps_label.pack()

        # Botón para cargar la matriz desde un archivo (en la parte superior)
        self.load_matrix_button = ttk.Button(root, text="Cargar Matriz", command=self.load_matrix_from_file_dialog)
        self.load_matrix_button.pack()

        # Crear un contenedor para el tablero con márgenes
        self.board_frame = tk.Frame(root)
        self.board_frame.pack(expand=True, fill="both", padx=self.margins, pady=self.margins)

        self.create_board()
        self.is_first_move = True
        self.selected_square = None
        
        

    def reset_game(self):
        self.selected_piece = None
        self.selected_square = None
        self.is_first_move = True
        self.game.current_player = "Red"  # o el jugador que comienza el juego
        self.ai.game = self.game
        self.update_board()
        self.turn_label.config(text=f"Turno actual: {self.game.current_player}")
        self.steps_label.config(text="Pasos disponibles para el segundo movimiento: 0")
        self.game.display_board()





    def load_matrix_from_file_dialog(self):
        # Abre el explorador de archivos para seleccionar un archivo de matriz
        filename = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if filename:
            self.load_matrix_from_file(filename)
    

    def load_matrix_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                matrix = [line.strip().split() for line in lines]
                if len(matrix) == 8 and all(len(row) == 8 for row in matrix):
                    self.game.board = matrix
                    self.ai.game = self.game  # Asegurarse de que la IA también use el nuevo juego
                    self.reset_game()  # Reiniciar el juego con la nueva matriz
                else:
                    messagebox.showerror("Error", "El archivo de matriz no tiene el formato correcto (8x8).")
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo de matriz no se encontró.")




    def load_images(self):
        red_img = Image.open("../img/red.png")  # Asegúrate de que la ruta sea correcta
        black_img = Image.open("../img/black.png")

        # Redimensionar las imágenes para que encajen en los cuadrados del tablero
        red_img = red_img.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)
        black_img = black_img.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)

        self.red_piece = ImageTk.PhotoImage(red_img)
        self.black_piece = ImageTk.PhotoImage(black_img)

    def create_board(self):
        self.canvas = tk.Canvas(self.board_frame, width=self.square_size*8, height=self.square_size*6)
        self.canvas.pack()

        for i in range(6):  # Ahora el tablero tiene 6 filas
            for j in range(8):  # El tablero tiene 8 columnas
                x1 = j * self.square_size
                y1 = i * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                self.draw_piece(i, j, x1, y1)

        self.canvas.bind("<Button-1>", self.on_canvas_click)




    def draw_piece(self, row, col, x1, y1):
        # Primero, determina el color de fondo de la casilla
        if (row, col) == self.selected_piece:
            # Resalta la casilla seleccionada en verde
            self.canvas.create_rectangle(x1, y1, x1 + self.square_size, y1 + self.square_size, fill="green", outline="red")
        elif (row, col) in self.highlighted_squares:
            # Resalta las casillas destino en azul
            self.canvas.create_rectangle(x1, y1, x1 + self.square_size, y1 + self.square_size, fill="blue", outline="red")
        else:
            # Casillas normales en blanco
            self.canvas.create_rectangle(x1, y1, x1 + self.square_size, y1 + self.square_size, fill="white", outline="black")

        # Luego, dibuja la pieza si hay una en esta casilla
        piece = self.game.board[row][col]
        if piece == "Red":
            image = self.red_piece  # Imagen de la pieza roja
            self.canvas.create_image(x1 + self.square_size // 2, y1 + self.square_size // 2, image=image, anchor='center')
        elif piece == "Black":
            image = self.black_piece  # Imagen de la pieza negra
            self.canvas.create_image(x1 + self.square_size // 2, y1 + self.square_size // 2, image=image, anchor='center')
        # No se hace nada si la casilla está vacía ('Free')


    
    
    def on_canvas_click(self, event):
        col = event.x // self.square_size
        row = event.y // self.square_size
        

        if self.game.current_player == "Red":
                # Obtener todos los posibles primeros movimientos
            if self.is_first_move:
                all_possible_moves = self.game.find_all_possible_first_moves()
                filtered_moves = [move for move in all_possible_moves if move[0] == row and move[1] == col]
                # Filtrar para obtener solo los movimientos que comienzan en la fila y columna seleccionadas
                self.highlighted_squares = [(move[2], move[3]) for move in filtered_moves]
                self.update_board()
            else: 
                all_possible_moves = self.game.find_all_possible_second_moves()
                filtered_moves = [move for move in all_possible_moves if move[0] == row and move[1] == col]
                # Filtrar para obtener solo los movimientos que comienzan en la fila y columna seleccionadas
                self.highlighted_squares = [(move[2], move[3]) for move in filtered_moves]
                self.update_board()



            if self.selected_piece:
                
                start_row, start_col = self.selected_piece
                if self.is_first_move:
                    moved = self.game.make_move(start_row, start_col, row, col)
                    if moved:
                        self.is_first_move = False  # Prepararse para el segundo movimiento
                        self.selected_piece = None  # Deseleccionar la ficha después de un movimiento válido
                        steps_available = self.game.second_move_distance
                        self.steps_label.config(text=f"Pasos disponibles para el segundo movimiento: {steps_available}")
                        
                        if steps_available == 0:
                            self.is_first_move = True
                            self.selected_piece = None
                            self.perform_black_move()
                            self.game.change_turn()
                        self.update_board()
                    else:
                        messagebox.showerror("Error", "Movimiento no válido")
                        self.update_board()
                        self.highlighted_squares = []
                        
                        self.update_board()
                        self.selected_piece = None  # Reiniciar la selección de ficha en caso de movimiento ilegal
                        self.update_board()  # Deseleccionar la casilla al mostrar el error
                else:

                    if not self.is_first_move:
                        print("sisaaaaaa")

                    moved = self.game.make_second_move(start_row, start_col, row, col)
                    
                    if moved:
                        self.is_first_move = True  # Resetear para el siguiente jugador
                        self.selected_piece = None  # Deseleccionar la ficha
                        self.steps_label.config(text="Pasos disponibles para el segundo movimiento: 0")
                        
                        # Actualizar el tablero inmediatamente después del segundo movimiento
                        self.update_board()

                        # Forzar la actualización de la interfaz gráfica
                        self.root.update_idletasks()

                        # Después de actualizar la interfaz gráfica, realizar el movimiento de la IA
                        self.game.change_turn()
                        self.perform_black_move()
                        self.game.change_turn()

                    else:
                        messagebox.showerror("Error", "Movimiento no válido")
                        self.selected_piece = None  # Reiniciar la selección de ficha en caso de movimiento ilegal
                        self.update_board()  # Deseleccionar la casilla al mostrar el error
            else:
                if self.game.board[row][col] != 'Free':
                    if self.is_first_move or self.game.current_player == self.game.board[row][col]:
                        self.selected_piece = (row, col)
                        self.update_board() 
                    

    def perform_black_move(self):
        best_move = self.ai.get_best_move(self.game, self.ai.depth)
        if best_move:
            print("el best",best_move)
            self.ai.apply_move(self.game, best_move)
            self.update_board()
            #self.game.change_turn()
            self.turn_label.config(text=f"Turno actual: {self.game.current_player}")
        else:
            messagebox.showinfo("Fin del juego", "No hay movimientos posibles para el jugador negro.")


    
        
    def load_background_image(self):
        # Carga la imagen de fondo
        bg_img = Image.open("../img/fondo.png")  # Asegúrate de que la ruta sea correcta
        # Redimensionar la imagen al tamaño de la ventana
        bg_img = bg_img.resize((800, 600), Image.Resampling.LANCZOS)  # Ajusta el tamaño según tus necesidades
        self.bg_image = ImageTk.PhotoImage(bg_img)

        # Crear y colocar el Label con la imagen de fondo
        self.background_label = tk.Label(self.root, image=self.bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def update_board(self):
        self.canvas.delete("all")  # Borra todo del canvas

        # Redibuja el tablero y las piezas
        for i in range(6):  # Ajustar para 6 filas
            for j in range(8):  # Mantener 8 columnas
                x1 = j * self.square_size
                y1 = i * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                self.draw_piece(i, j, x1, y1)

            self.turn_label.config(text=f"Turno actual: {self.game.current_player}")  # Actualiza el texto de la etiqueta
        

        if not self.game.find_all_possible_first_moves():
            self.game.change_turn()
            if self.game.current_player == "Black":
                self.is_first_move = True
                self.selected_piece = None
                self.perform_black_move()
                self.game.change_turn()
        # Verificar si hay un ganador
        winner_info = self.game.check_winner()
        if winner_info[0] is not None:  # Asegurarse de que hay un ganador
            winner, red_score, black_score = winner_info
            messagebox.showinfo("Fin del juego", f"¡Juego terminado! {winner} gana con {red_score if winner == 'Red' else black_score} puntos.")

# Creando la instancia del juego y la interfaz
game = LinjaGame()
root = tk.Tk()
app = LinjaGUI(root, game)
root.mainloop()
