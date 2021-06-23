from src.utils import Attack, Direction, KeyPad
from src.human import Human
from src.grid import Grid


def test_init():
    h = Human(grid=Grid(), get_input=lambda: None, redraw=lambda: None)
    assert isinstance(h, Human)
    assert h.covered_val == h.grid.initial_char
    assert h.pos == 0


def test_move():
    h = Human(grid=Grid(size=10), get_input=lambda: None, redraw=lambda: None)
    h.move(Direction.LEFT)
    assert h.pos == 0
    h.move(Direction.RIGHT)
    assert h.pos == 1
    h.move(Direction.UP)
    assert h.pos == 1
    h.move(Direction.DOWN)
    assert h.pos == 11
    h.move(Direction.LEFT)
    assert h.pos == 10
    h.move(Direction.UP)
    assert h.pos == 0


def test_move_over_known_pegs():
    h = Human(grid=Grid(size=10), get_input=lambda: None, redraw=lambda: None)
    h.grid.mark(1, Attack.MISS)
    h.grid.mark(2, Attack.MISS)
    assert h.pos == 0
    h.move(Direction.RIGHT)
    assert h.pos == 3


def test_handle_attack_miss():
    h = Human(grid=Grid(size=10), get_input=lambda: None, redraw=lambda: None)
    h.pos = 5
    h.handle_attack_result(5, Attack.MISS)
    assert h.covered_val == Attack.MISS.value
    assert h.grid.val(5) == Attack.MISS.value


def test_handle_attack_hit():
    h = Human(grid=Grid(size=10), get_input=lambda: None, redraw=lambda: None)
    h.pos = 5
    h.handle_attack_result(5, Attack.HIT)
    assert h.covered_val == Attack.HIT.value
    assert h.grid.val(5) == Attack.HIT.value


def test_handle_attack_sink():
    h = Human(grid=Grid(size=10), get_input=lambda: None, redraw=lambda: None)
    h.pos = 5
    h.handle_attack_result(5, Attack.SINK)
    assert h.covered_val == Attack.HIT.value
    assert h.grid.val(5) == Attack.HIT.value


def test_get_attack_pos():
    vals = [KeyPad.RIGHT, KeyPad.RIGHT, KeyPad.DOWN, KeyPad.DOWN, KeyPad.ENTER]

    def get_input():
        return vals.pop(0).value if len(vals) else None

    h = Human(grid=Grid(size=10), get_input=get_input, redraw=lambda: None)
    pos = h.get_attack_pos()
    assert pos == 22
