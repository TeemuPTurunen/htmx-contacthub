# game_state.py
from enum import Enum, auto
from threading import Lock

class TileState(Enum):
    HIDDEN_EMPTY = auto()
    HIDDEN_MINE = auto()
    FLAGGED_EMPTY = auto()
    FLAGGED_MINE = auto()
    OPEN_EMPTY = auto()
    OPEN_1 = auto()
    OPEN_2 = auto()
    OPEN_3 = auto()
    OPEN_4 = auto()
    OPEN_5 = auto()
    OPEN_6 = auto()
    OPEN_7 = auto()
    OPEN_8 = auto()
    EXPLODED_MINE = auto()

# Shared global board

board_x = 22
board_y = 22
board_mines = 33

board = [
    [{"state": TileState.HIDDEN_EMPTY.name, "hovered_by": None, "highlight": False} for _ in range(board_x)]
    for _ in range(board_y)
]


clients = []
clients_lock = Lock()
