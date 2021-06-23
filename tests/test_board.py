from src.board import Board
from src.grid import Grid
from src.utils import Attack, Fleet, Ship, Orientation


class TestBoard:
    def test_init(self):
        b = Board(grid=Grid())
        assert isinstance(b, Board)

    def test_reset(self):
        grid = Grid(size=10)
        grid.mark(0, 'A')
        b = Board(grid=grid)
        b.reset()
        assert len(grid.empty_positions()) == 100

    def test_ship_placement(self):
        b = Board(grid=Grid())

        # ship=4 in top left corner, horizontal
        [valid, positions] = b.ship_placement(
            0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert valid == True
        assert positions == [0, 1, 2, 3]

        # ship=4 in top left corner, vertical
        [valid, positions] = b.ship_placement(
            0, Fleet.BATTLESHIP.value, Orientation.VERTICAL)
        assert valid == True
        assert positions == [0, 10, 20, 30]

        # ship=4 in top right corner, horizontal (off grid)
        [valid, positions] = b.ship_placement(
            9, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert valid == False
        assert positions == []

        # ship=4 in top right corner, vertical
        [valid, positions] = b.ship_placement(
            9, Fleet.BATTLESHIP.value, Orientation.VERTICAL)
        assert valid == True
        assert positions == [9, 19, 29, 39]

        # ship=4 in bottom left corner, horizontal
        [valid, positions] = b.ship_placement(
            90, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert valid == True
        assert positions == [90, 91, 92, 93]

        # ship=4 in bottom left corner, vertical (off grid)
        [valid, positions] = b.ship_placement(
            90, Fleet.BATTLESHIP.value, Orientation.VERTICAL)
        assert valid == False
        assert positions == []

        # ship=4 in bottom right corner, horizontal (off grid)
        [valid, positions] = b.ship_placement(
            99, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert valid == False
        assert positions == []

        # ship=4 in bottom right corner, vertical (off grid)
        [valid, positions] = b.ship_placement(
            99, Fleet.BATTLESHIP.value, Orientation.VERTICAL)
        assert valid == False
        assert positions == []

        # ship=4 placed in bottom right, horizontal (offset from edge)
        [valid, positions] = b.ship_placement(
            96, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert valid == True
        assert positions == [96, 97, 98, 99]

    def test_ship_placement_with_collisions(self):
        g = Grid()
        for x in range(0, Fleet.BATTLESHIP.value.size):
            g.mark(x, 'B')
        b = Board(grid=g)

        assert b.ship_placement(
            0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL).valid == False

    def test_place_ship(self):
        b = Board(grid=Grid())
        assert b.place_ship(0, Fleet.BATTLESHIP.value,
                            Orientation.HORIZONTAL) == True

    def test_place_ship_invalid(self):
        g = Grid()
        for x in range(0, Fleet.BATTLESHIP.value.size):
            g.mark(x, Fleet.BATTLESHIP.value.id)
        b = Board(grid=g)

        assert b.place_ship(0, Fleet.BATTLESHIP.value,
                            Orientation.HORIZONTAL) == False
        assert b.total_fleet_size == 0

    def test_total_fleet_size(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        b.place_ship(20, Fleet.CARRIER.value, Orientation.HORIZONTAL)
        assert b.total_fleet_size == Fleet.BATTLESHIP.value.size + Fleet.CARRIER.value.size

    def test_ship_hits(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        b.hits = [1, 2]
        assert b.ship_hits(Fleet.BATTLESHIP.value) == 2

    def test_ship_at_pos(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert b.ship_at_pos(0) == Fleet.BATTLESHIP.value

    def test_ship_is_sunk(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)

        b.hits = [1, 2]
        assert b.ship_is_sunk(Fleet.BATTLESHIP.value) == False

        b.hits = [0, 1, 2, 3]
        assert b.ship_is_sunk(Fleet.BATTLESHIP.value) == True

    def test_receive_attack_miss(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert b.receive_attack(20) == Attack.MISS

    def test_receive_attack_hit(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert b.receive_attack(1) == Attack.HIT

    def test_receive_attack_win(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        assert b.receive_attack(0) == Attack.HIT
        assert b.receive_attack(1) == Attack.HIT
        assert b.receive_attack(2) == Attack.HIT
        assert b.receive_attack(3) == Attack.WIN

    def test_receive_attack_sink(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        b.place_ship(20, Fleet.CARRIER.value, Orientation.HORIZONTAL)
        assert b.receive_attack(0) == Attack.HIT
        assert b.receive_attack(1) == Attack.HIT
        assert b.receive_attack(2) == Attack.HIT
        assert b.receive_attack(3) == Attack.SINK

    def test_place_fleet_randomly(self):
        b = Board(grid=Grid())
        b.place_fleet_randomly()
        fleet_size = sum([x.value.size for x in Fleet.__members__.values()])
        assert b.grid.size ** 2 - len(b.grid.empty_positions()) == fleet_size

    def test_render_fleet(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        s = b.render()
        assert len(s) == b.grid.get_size() ** 2 * 2 - 1
        assert len([c for c in s if c ==
                   Fleet.BATTLESHIP.value.id]) == Fleet.BATTLESHIP.value.size

    def test_render_hit(self):
        b = Board(grid=Grid())
        b.place_ship(0, Fleet.BATTLESHIP.value, Orientation.HORIZONTAL)
        b.receive_attack(0)
        s = b.render()
        assert len([c for c in s if c ==
                   Fleet.BATTLESHIP.value.id]) == Fleet.BATTLESHIP.value.size - 1
        assert s[0] == Attack.HIT.value
