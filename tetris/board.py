class Board():
    def __init__(self, rows, cols, cell_size) -> None:
        if cell_size < 20:
            raise ValueError("Cell size too small, must be at least 20px")
        if rows < 8 or cols < 6:
            raise ValueError("Board too small, must be at least 6x8")
        self.cell_size = cell_size
        self.rows = rows
        self.cols = cols
        self.board = [[{} for i in range(cols)] for j in range(rows)]

        for i in range(rows):
            for j in range(cols):
                self.board[i][j] = {
                    # calculate where to draw the cell on the canvas
                    "topLeft": (cell_size*j, cell_size*i),
                    "btmRight": ((cell_size * j + cell_size), (cell_size * i + cell_size)),
                    "row": i,
                    "col": j,
                    "empty": True,
                    "colour": "",
                    "piece_id": -1
                }