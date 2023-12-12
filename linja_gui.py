import tkinter as tk
from tkinter import messagebox
from linja import LinjaGame  # Importa la clase LinjaGame
from PIL import Image, ImageTk

class LinjaGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.selected_piece = None
        self.square_size = 50  # Tamaño de cada cuadrado del tablero
        self.load_images()     # Cargar las imágenes
        self.create_board()
        self.is_first_move = True
        


    
    def load_images(self):
        red_img = Image.open("img/red.png")  # Asegúrate de que la ruta sea correcta
        black_img = Image.open("img/black.png")

        # Redimensionar las imágenes para que encajen en los cuadrados del tablero
        red_img = red_img.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)
        black_img = black_img.resize((self.square_size, self.square_size), Image.Resampling.LANCZOS)

        self.red_piece = ImageTk.PhotoImage(red_img)
        self.black_piece = ImageTk.PhotoImage(black_img)

    def create_board(self):
        self.canvas = tk.Canvas(self.root, width=self.square_size*8, height=self.square_size*8)
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
        if piece == "Red":
            self.canvas.create_image(x1 + self.square_size // 2, y1 + self.square_size // 2, image=self.red_piece, anchor='center')
        elif piece == "Black":
            self.canvas.create_image(x1 + self.square_size // 2, y1 + self.square_size // 2, image=self.black_piece, anchor='center')

    def on_canvas_click(self, event):
        col = event.x // self.square_size
        row = event.y // self.square_size

        if self.selected_piece:
            start_row, start_col = self.selected_piece
            if self.is_first_move:
                moved = self.game.make_move(start_row, start_col, row, col)
                if moved:
                    self.is_first_move = False  # Prepararse para el segundo movimiento
            else:
                moved = self.game.make_second_move(start_row, start_col, row, col)
                if moved:
                    self.is_first_move = True  # Resetear para el siguiente jugador
                    #self.game.change_turn()  # Cambiar el turno

            if not moved:
                messagebox.showerror("Error", "Movimiento no válido")
            else:
                self.update_board()
                if self.game.game_over():
                    winner = self.game.check_winner()
                    messagebox.showinfo("Game Over", winner)
            self.selected_piece = None
        else:
            if self.game.board[row][col] != 'Free':
                if self.is_first_move or self.game.current_player == self.game.board[row][col]:
                    self.selected_piece = (row, col)

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

        self.root.title(f"Linja Game - Current Player: {self.game.current_player}")

# Creando la instancia del juego y la interfaz
game = LinjaGame()
root = tk.Tk()
app = LinjaGUI(root, game)
root.mainloop()
