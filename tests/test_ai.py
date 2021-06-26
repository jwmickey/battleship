from src.utils import Attack, Direction, Orientation
from src.ai import Ai
from src.grid import Grid


def test_init():
    assert isinstance(Ai(grid=Grid()), Ai)


def test_get_attack_pos():
    ai = Ai(grid=Grid())
    ai.last_hit = 0
    assert ai.get_attack_pos() is not None


def test_set_orientation():
    ai = Ai(grid=Grid())

    ai.direction = Direction.DOWN
    ai.set_ship_orientation()
    assert ai.ship_orientation == Orientation.VERTICAL

    ai.direction = Direction.UP
    ai.set_ship_orientation()
    assert ai.ship_orientation == Orientation.VERTICAL

    ai.direction = Direction.LEFT
    ai.set_ship_orientation()
    assert ai.ship_orientation == Orientation.HORIZONTAL

    ai.direction = Direction.RIGHT
    ai.set_ship_orientation()
    assert ai.ship_orientation == Orientation.HORIZONTAL


def test_finished_on_win():
    ai = Ai(grid=Grid())
    ai.handle_attack_result(0, Attack.WIN)
    assert ai.finished == True


def test_last_hit():
    ai = Ai(grid=Grid())
    ai.handle_attack_result(0, Attack.HIT)
    assert ai.last_hit == 0


def test_last_hit_miss():
    ai = Ai(grid=Grid())
    ai.handle_attack_result(0, Attack.MISS)
    assert ai.last_hit == None


def test_last_hit_origin():
    ai = Ai(grid=Grid())
    ai.handle_attack_result(0, Attack.HIT)
    assert ai.last_hit == 0
    assert ai.last_hit_origin == 0
    ai.handle_attack_result(1, Attack.HIT)
    assert ai.last_hit == 1
    ai.handle_attack_result(2, Attack.MISS)
    assert ai.last_hit == 0


def test_last_hit_sink():
    ai = Ai(grid=Grid())
    ai.handle_attack_result(0, Attack.HIT)
    ai.handle_attack_result(1, Attack.HIT)
    ai.direction = Direction.RIGHT
    ai.set_ship_orientation()
    assert ai.last_hit is not None
    assert ai.last_hit_origin is not None
    assert ai.ship_orientation is not None
    ai.handle_attack_result(2, Attack.SINK)
    assert ai.last_hit is None
    assert ai.last_hit_origin is None
    assert ai.ship_orientation is None


def test_valid_moves_from():
    grid = Grid()
    ai = Ai(grid=grid)

    assert [Direction.DOWN, Direction.RIGHT] == [
        x[0] for x in ai.valid_moves_from(0)]

    grid.mark(1, Attack.MISS)
    assert [Direction.DOWN] == [
        x[0] for x in ai.valid_moves_from(0)]

    assert [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT] == [
        x[0] for x in ai.valid_moves_from(55)]


def test_reverse_direction():
    ai = Ai(grid=Grid())
    ai.ship_orientation = Orientation.HORIZONTAL
    ai.direction = Direction.LEFT
    ai.reverse_direction()
    assert ai.direction == Direction.RIGHT
    ai.reverse_direction()
    assert ai.direction == Direction.LEFT

    ai.ship_orientation = Orientation.VERTICAL
    ai.direction = Direction.DOWN
    ai.reverse_direction()
    assert ai.direction == Direction.UP
    ai.reverse_direction()
    assert ai.direction == Direction.DOWN


def test_next_best_direction():
    ai = Ai(grid=Grid())

    assert ai.next_best_direction(10) == Direction.RIGHT
    assert ai.next_best_direction(99) == Direction.LEFT
    assert ai.next_best_direction(40) == Direction.DOWN
    assert ai.next_best_direction(94) == Direction.RIGHT
    assert ai.next_best_direction(55) == None


def test_next_in_direction():
    grid = Grid()
    ai = Ai(grid=grid)
    grid.mark(2, Attack.MISS)
    grid.mark(3, Attack.HIT)
    grid.mark(4, Attack.HIT)
    grid.mark(6, Attack.MISS)
    assert ai.next_in_direction() == None
    ai.ship_orientation = Orientation.HORIZONTAL
    ai.direction = Direction.LEFT
    ai.last_hit = 3
    ai.last_hit_origin = 4
    assert ai.next_in_direction() == 5
    assert ai.direction == Direction.RIGHT
    assert ai.has_reversed == True
    ai.last_hit = 5
    assert ai.next_in_direction() == None


def test_next_target():
    grid = Grid()
    ai = Ai(grid=grid)

    assert ai.next_target() == None

    grid.mark(5, Attack.HIT)
    ai.last_hit = 5
    ai.direction = Direction.RIGHT
    assert ai.next_target() == 6

    ai.direction = None
    grid.mark(4, Attack.MISS)
    grid.mark(6, Attack.MISS)
    grid.mark(15, Attack.MISS)
    assert ai.next_target() == None

    grid.mark(55, Attack.HIT)
    ai.last_hit = 55
    ai.direction = None
    grid.mark(54, Attack.MISS)
    grid.mark(56, Attack.MISS)
    assert ai.next_target() in (45, 65)

def test_has_open_neighbors():
    grid = Grid()
    ai = Ai(grid=grid)
    assert ai.has_open_neighbors(0) == True

    grid.mark(1, Attack.MISS)
    grid.mark(10, Attack.MISS)
    assert ai.has_open_neighbors(0) == False

    grid.mark(49, Attack.HIT)
    grid.mark(51, Attack.MISS)
    grid.mark(40, Attack.MISS)
    grid.mark(60, Attack.MISS)
    assert ai.has_open_neighbors(50) == False
