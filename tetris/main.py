import tkinter as tk
from board import Board
from piece import Piece

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.ROWS = 20
        self.COLS = 10
        self.CELL_SIZE = 40
        self.TICK_LENGTH = 100

        self.title("Tetris!")
        self.geometry("400x800")
        self.ticks_elapsed = 0
        # key binds
        self.bind("<Down>", self.handle_hard_drop)
        self.bind("<Left>", self.left_shift)
        self.bind("<Right>", self.right_shift)
        self.bind("<Up>", self.rotate)
        self.shift = False
        
        self.game_board = Board(self.ROWS, self.COLS, self.CELL_SIZE)
        self.active_piece = None
        self.active_piece_coords = (0, 0)
        self.active_piece_id = 0
        
        self.canvas = tk.Canvas(width=400, height=800, bg="white")
        self.canvas.after(self.TICK_LENGTH, self.update)
        self.canvas.after(1000, self.active_piece_update)

        self.draw_board()
        self.canvas.pack()
    
    def create_active_piece(self):
        self.active_piece = Piece()
        self.active_piece_id += 1
        col = int(self.COLS / 2) - 1
        self.active_piece_coords = (0, col)
        if not self.add_piece(0, col):
            # if no more pieces can be created, the game ends
            print("Game Over")
        
    def add_piece(self, row, col) -> bool:
        piece = self.active_piece
        # check the piece does not go out of bounds
        if row < 0 or col < 0:
            return False
        if row + piece.height >= self.ROWS:
            return False
        if col + piece.width > self.COLS:
            return False

        # check the space is unoccupied
        unoccupied = True
        for i in range(piece.height):
            for j in range(piece.width):
                if piece.get_piece()[i][j] == 0:
                    continue

                cell = self.game_board.board[row + i][col + j]
                if not cell["empty"]:
                    unoccupied = False
        # add the piece to the board
        if unoccupied:
            for i in range(piece.height):
                for j in range(piece.width):
                    if piece.get_piece()[i][j] == 0:
                        continue
                    cell = self.game_board.board[row + i][col + j]
                    cell["empty"] = False
                    cell["colour"] = piece.colour
                    cell["piece_id"] = self.active_piece_id
        else:
            return False
        return True
    
    def clear_full_rows(self):
        row_cleared = True
        while row_cleared:
            row_cleared = False
            for i in range(len(self.game_board.board)-1, -1, -1):
                row = self.game_board.board[i]
                if not row_cleared:
                    full = True
                    for col in row:
                        if col["empty"]:
                            full = False
                # if the row is full, clear and move down the row above
                if full:
                    for col in row:
                        col["empty"] = True
                    row_cleared = True
                
                if not row_cleared:
                    continue

                # move the row down
                if i == 0:
                    continue
                for j in range(len(row)):
                    self.game_board.board[i][j] = self.game_board.board[i-1][j]
            


    def col_shift(self, shift):
        if self.active_piece == None:
            return
        # check we don't go out of bounds
        if self.active_piece_coords[1] + shift < 0:
            return False
        if self.active_piece_coords[1] + abs(shift) > self.COLS:
            return False
        # remove the piece and attempt to replace it in the shifted position
        self.remove_active_piece()
        if self.add_piece(
            self.active_piece_coords[0],
            self.active_piece_coords[1] + shift
        ):
            self.active_piece_coords = (
                self.active_piece_coords[0],
                self.active_piece_coords[1] + shift)
            return True
        else:
            # put the piece back in its' original place if we can't move it
            self.add_piece(
                self.active_piece_coords[0],
                self.active_piece_coords[1]
            )
            return False
    
    def remove_active_piece(self):
        piece = self.active_piece.get_piece()
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                coords = (i + self.active_piece_coords[0],
                          j + self.active_piece_coords[1])
                cell = self.game_board.board[coords[0]][coords[1]]
                if cell["piece_id"] == self.active_piece_id:
                    cell["empty"] = True

    def handle_hard_drop(self, event):
        if self.active_piece == None:
            return
        else:
            self.row_shift(1)
            self.draw_board()
    
    def left_shift(self, event):
        if self.active_piece == None:
            return
        else:
            self.col_shift(-1)
            self.draw_board()

    def right_shift(self, event):
        if self.active_piece == None:
            return
        else:
            self.col_shift(1)
            self.draw_board()
    
    def rotate(self, event):
        if self.active_piece == None:
            return
        else:
            self.rotate_piece()
    
    def rotate_piece(self):
        self.remove_active_piece()
        self.active_piece.rotate()
        if not self.add_piece(self.active_piece_coords[0], self.active_piece_coords[1]):
            self.active_piece.rotate()
            self.active_piece.rotate()
            self.active_piece.rotate()
            self.add_piece(self.active_piece_coords[0], self.active_piece_coords[1])

    def row_shift(self, shift):
        # check we don't go out of bounds
        if self.active_piece_coords[0] + shift >= self.ROWS:
            return False
        # remove the piece and try placing it in the shifted position
        self.remove_active_piece()

        if self.add_piece(
            self.active_piece_coords[0] + shift,
            self.active_piece_coords[1]
        ):
            self.active_piece_coords = (
                self.active_piece_coords[0] + shift,
                self.active_piece_coords[1])
            return True
        else:
            # add the piece back to its' original place if it can't be moved
            self.add_piece(
                self.active_piece_coords[0],
                self.active_piece_coords[1]
            )
            return False



    def update_active_piece(self):
        # if the piece is at the bottom, create a new piece next tick
        bottom_row = self.active_piece_coords[0] + self.active_piece.height
        if bottom_row >= self.ROWS - 1:
            self.active_piece_coords = (0, 0)
            self.active_piece = None
            self.active_piece_update(False)
            return
        if not self.row_shift(1):
            self.active_piece_coords = (0, 0)
            self.active_piece = None

    def draw_board(self):
        for i in range(self.ROWS):
            for j in range(self.COLS):
                grid_cell = self.game_board.board[i][j]
                self.canvas.create_rectangle(
                    grid_cell["topLeft"],
                    grid_cell["btmRight"],
                    outline="black",
                    fill = "white" if grid_cell["empty"] else grid_cell["colour"]
                )
    def active_piece_update(self, repeat=True):
        if self.active_piece == None:
            self.clear_full_rows()
            self.create_active_piece()
        else:
            self.update_active_piece()
        if repeat:
            self.canvas.after(1000, self.active_piece_update)

    def update(self):
        # redraw the board to display any updates
        if self.shift:
            self.shift = False
            self.draw_board()
            return

        self.draw_board()
        self.canvas.after(self.TICK_LENGTH, self.update)

if __name__ == "__main__":
    app = App()
    app.mainloop()