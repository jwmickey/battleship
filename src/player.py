from src.utils import Attack
from src.grid import Grid
from src.utils import Attack


class Player():
    def __init__(self, grid: Grid):
        self.grid = grid

    def reset(self):
        pass

    def get_attack_pos(self) -> int:
        raise NotImplementedError

    def handle_attack_result(self, pos: int, result: Attack):
        raise NotImplementedError
