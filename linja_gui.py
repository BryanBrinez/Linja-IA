import tkinter as tk
from tkinter import messagebox, ttk
from linja import LinjaGame  # Importa la clase LinjaGame
from PIL import Image, ImageTk
from tkinter import filedialog

class LinjaGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.selected_piece = None
        self.square_size = 50  # Tamaño de cada cuadrado del tablero
        self.margins = 100    # Márgenes en píxeles

        self.load_images()     # Cargar las imágenes

        # Etiqueta para mostrar el turno actual del jugador (en la parte superior)
        self.turn_label = ttk.Label(root, text=f"Turno actual: {self.game.current_player}", font=("Helvetica", 16))
        self.turn_label.pack()

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
        self.game = LinjaGame()
        self.selected_piece = None
        self.selected_square = None
        self.is_first_move = True
        self.update_board()
        self.turn_label.config(text=f"Turno actual: {self.game.current_player}")


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
                    self.reset_game()  # Llama al método de reinicio
                else:
                    messagebox.showerror("Error", "El archivo de matriz no tiene el formato correcto (8x8).")
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo de matriz no se encontró.")



    def load_images(self):
        red_img = Image.open("img/red.png")  # Asegúrate de que la ruta sea correcta
        black_img = Image.open("img/black.png")

        # Redimensionar las imágenes para que encajen en los cuadrados del tablero
        red_img = red_img.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)
        black_img = black_img.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)

        self.red_piece = ImageTk.PhotoImage(red_img)
        self.black_piece = ImageTk.PhotoImage(black_img)

    def create_board(self):
        self.canvas = tk.Canvas(self.board_frame, width=self.square_size*8, height=self.square_size*8)
        self.canvas.pack()

        for i in range(8):
            for j in range(8):
                x1 = j * self.square_size
                y1 = i * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                
                # Dibujar las imágenes desde el inicio
                self.draw_piece(i, j, x1, y1)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_piece(self, row, col, x1, y1):
        piece = self.game.board[row][col]

        if (row, col) == self.selected_piece:
            self.canvas.create_rectangle(x1, y1, x1 + self.square_size, y1 + self.square_size, fill="blue", outline="red")

        if piece == "Red":
            image = self.red_piece
        elif piece == "Black":
            image = self.black_piece
        else:
            return

        self.canvas.create_image(x1 + self.square_size // 2, y1 + self.square_size // 2, image=image, anchor='center')
    
    def on_canvas_click(self, event):
        col = event.x // self.square_size
        row = event.y // self.square_size

        if self.selected_piece:
            start_row, start_col = self.selected_piece
            if self.is_first_move:
                moved = self.game.make_move(start_row, start_col, row, col)
                if moved:
                    self.is_first_move = False  # Prepararse para el segundo movimiento
                    self.selected_piece = None  # Deseleccionar la ficha después de un movimiento válido
                    self.update_board()
                else:
                    messagebox.showerror("Error", "Movimiento no válido")
                    self.selected_piece = None  # Reiniciar la selección de ficha en caso de movimiento ilegal
                    self.update_board()  # Deseleccionar la casilla al mostrar el error
            else:
                moved = self.game.make_second_move(start_row, start_col, row, col)
                if moved:
                    self.is_first_move = True  # Resetear para el siguiente jugador
                    self.selected_piece = None  # Deseleccionar la ficha después de un movimiento válido
                    self.update_board()
                else:
                    messagebox.showerror("Error", "Movimiento no válido")
                    self.selected_piece = None  # Reiniciar la selección de ficha en caso de movimiento ilegal
                    self.update_board()  # Deseleccionar la casilla al mostrar el error
        else:
            if self.game.board[row][col] != 'Free':
                if self.is_first_move or self.game.current_player == self.game.board[row][col]:
                    self.selected_piece = (row, col)
                    self.update_board()  # Actualiza el tablero después de seleccionar una ficha

    def update_board(self):
        self.canvas.delete("all")  # Borra todo del canvas

        # Redibuja el tablero y las piezas
        for i in range(8):
            for j in range(8):
                x1 = j * self.square_size
                y1 = i * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

                # Dibujar las imágenes actualizadas
                self.draw_piece(i, j, x1, y1)

        self.turn_label.config(text=f"Turno actual: {self.game.current_player}")  # Actualiza el texto de la etiqueta


# Creando la instancia del juego y la interfaz
game = LinjaGame()
root = tk.Tk()
app = LinjaGUI(root, game)
root.mainloop()