import random

PIECE_TYPES = ["I", "O", "T", "J", "L", "S", "Z"]
COLOURS = {
    "I": "cyan",
    "O": "yellow",
    "T": "purple",
    "J": "blue",
    "L": "orange",
    "S": "green",
    "Z": "red"
}

ROTATIONS = {
    "I": [
        [[1], [1], [1], [1]],
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]],
        [[1, 1, 1, 1]]
    ],
    "O": [
        [[1, 1], [1, 1]],
        [[1, 1], [1, 1]], 
        [[1, 1], [1, 1]],
        [[1, 1], [1, 1]]
    ],
    "T": [
        [[1, 1, 1], [0, 1, 0]],
        [[0, 1], [1, 1], [0, 1]],
        [[0, 1, 0], [1, 1, 1]],
        [[1, 0], [1, 1], [1, 0]]
    ],
    "J": [
        [[0, 1], [0, 1], [1, 1]],
        [[1, 0, 0], [1, 1, 1]],
        [[1, 1], [1, 0], [1, 0]],
        [[1, 1, 1], [0, 0, 1]],
    ],
    "L": [
        [[1, 0], [1, 0], [1, 1]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1], [0, 1], [0, 1]],
        [[0, 0, 1], [1, 1, 1]]
    ],
    "S": [
        [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 1], [0, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 1], [0, 1]],
    ],
    "Z": [
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1], [1, 1], [1, 0]],
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1], [1, 1], [1, 0]],
    ]
}

class Piece():
    def __init__(self, piece_type="") -> None:
        self.piece_type = piece_type
        if self.piece_type not in PIECE_TYPES and self.piece_type != "":
            raise ValueError("Invalid piece type specified")
        if self.piece_type == "":
            self.piece_type = random.choice(PIECE_TYPES)
        
        self.colour = COLOURS[self.piece_type]
        self._piece_cells = ROTATIONS[self.piece_type][0]
        self.rotation = 0
        self.height = len(self._piece_cells)
        self.width = len(self._piece_cells[0])
    
    def __str__(self):
        piece_str = ""
        for i in range(len(self._piece_cells)):
            for j in range(len(self._piece_cells[0])):
                if self._piece_cells[i][j] == 1:
                    piece_str += "*"
                else:
                    piece_str += " "
            piece_str += "\n"
        return piece_str

    def get_piece(self):
        return self._piece_cells
    
    def rotate(self):
        """ Rotate the shape 90 degrees clockwise and return the new shape """
        self.rotation += 1
        self._piece_cells = ROTATIONS[self.piece_type][self.rotation % 4]
        # rotating may change the dimensions of the shape
        self.height = len(self._piece_cells)
        self.width = len(self._piece_cells[0])
        return self._piece_cells