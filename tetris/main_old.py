import tkinter as tk
import random

SQUARE = ([[1, 1], [1, 1]], "yellow")
LINE = ([[1], [1], [1], [1]], "cyan")
S = ([[0, 1, 1], [1, 1, 0]], "green")
Z = ([[1, 1, 0], [0, 1, 1]], "red")
T = ([[1, 1, 1], [0, 1, 0]], "purple")
L = ([[0, 1], [0, 1], [1, 1]], "orange")
L_2 = ([[1, 0], [1, 0], [1, 1]], "blue")

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # game settings
        self.ROWS = 20
        self.COLS = 10
        self.CELL_SIZE = 40

        # configure window properties
        self.title("Tetris!")
        self.geometry("600x800")

        self._ticks_elapsed = 0

        self._board = [[{} for i in range(self.COLS)] for j in range(self.ROWS)]
        self._piece = random.choice([SQUARE, LINE, S, Z, T, L, L_2])
        self.create_game_board()
        self.draw_piece(0, 0, self._piece)
        self._canvas = tk.Canvas(width=400, height=800, bg="white", highlightthickness=0, borderwidth=0)
        self.draw_game_board()
        self._canvas.pack()
        # update the state of the board and pieces
        self._canvas.after(1000, self.update)
    
    def create_game_board(self):
        size = self.CELL_SIZE
        for i in range(self.ROWS):
            for j in range(self.COLS):
                self._board[i][j] = {
                    "corner1": (size*j, size*i),
                    "corner2": ((size*j + size), (size*i + size)),
                    "row": j,
                    "col": i,
                    "filled": False,
                    "colour": "black"}

    def draw_game_board(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                cell = self._board[i][j]
                self._canvas.create_rectangle(
                    cell["corner1"],
                    cell["corner2"],
                    outline="black",
                    fill=(cell["colour"] if cell["filled"] else None)
                )
    
        self._canvas.create_line(
            (self.COLS*self.CELL_SIZE,0),
            (self.COLS*self.CELL_SIZE, self.ROWS*self.CELL_SIZE),
            fill="black")
    
    def draw_piece(self, row, col, piece):
        piece_height = len(piece[0])
        piece_width = len(piece[0][0])
        if row + piece_height >= self.ROWS or row < 0:
            print("Piece out of bounds")
            return False
        if col + piece_width >= self.COLS or col < 0:
            print("Piece out of bounds")
            return False
        for i in range(len(piece[0])):
            for j in range(len(piece[0][0])):
                self._board[i + row][j + col]["filled"] = True if piece[0][i][j] == 1 else False
                self._board[i + row][j + col]["colour"] = piece[1]

    def update_shape_pos(self):
        # check shape can be moved
        bottom_row = self._piece[0][-1]
        print(bottom_row)

    def clear_full_rows(self):
        pass

    def update(self):
        self.clear_full_rows()
        self.update_shape_pos()
        self.draw_game_board()
        print("Board Redrawn")
        self._ticks_elapsed += 1
        self._canvas.after(1000, self.update)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()