from src.grid import Grid


class TestGrid:
    def test_init(self):
        g = Grid()
        assert isinstance(g, Grid)

    def test_custom_size(self):
        g = Grid(size=20)
        assert g.get_size() == 20

    def test_custom_initial_char(self):
        g = Grid(size=20, inital_char="?")
        assert g.get_initial_char() == "?"

    def test_val(self):
        g = Grid(size=10)
        assert g.val(0) == '.'

    def test_invalid_val(self):
        g = Grid(size=10)
        assert g.val(200) == None

    def test_mark(self):
        g = Grid(size=10)
        g.mark(0, 'X')
        assert g.val(0) == 'X'

    def test_coords(self):
        size = 10
        g = Grid(size=size)
        assert g.coords(0) == (0, 0)
        assert g.coords(size) == (0, 1)
        assert g.coords(size + 1) == (1, 1)
        assert g.coords(size ** 2 - 1) == (size - 1, size - 1)
        assert g.coords(size - 1) == (size - 1, 0)

    def test_pos(self):
        size = 10
        g = Grid(size=size)
        assert g.pos(0, 0) == 0
        assert g.pos(size - 1, size - 1) == size ** 2 - 1

    def test_val(self):
        size = 10
        g = Grid(size=size)
        g.mark(42, 'X')
        assert g.val(42) == 'X'

    def test_val_by_coords(self):
        size = 10
        g = Grid(size=size)
        g.mark(42, 'X')
        coords = g.coords(42)
        assert g.val_by_coords(coords[0], coords[1]) == 'X'

    def test_reset(self):
        size = 10
        g = Grid(size=size)
        g.mark(42, 'X')
        assert g.val(42) == 'X'
        g.reset()
        assert g.val(42) == '.'

    def test_render(self):
        size = 10
        g = Grid(size=size, inital_char='_')
        g.mark(42, 'X')
        g.mark(43, 'X')
        g.mark(44, 'O')
        s = g.render()
        expected = (("\n_ _ _ _ _ _ _ _ _ _" * 4) +
                    "\n_ _ X X O _ _ _ _ _" + ("\n_ _ _ _ _ _ _ _ _ _") * 5)[1:]
        assert s == expected

    def test_neighbors(self):
        size = 10
        g = Grid(size=size)

        # top left corner
        neighbors = g.neighbors(0)
        assert neighbors.UP == None
        assert neighbors.LEFT == None
        assert neighbors.RIGHT == 1
        assert neighbors.DOWN == size

        # x = 0, y = 1
        neighbors = g.neighbors(size)
        assert neighbors.UP == 0
        assert neighbors.LEFT == None
        assert neighbors.RIGHT == size + 1
        assert neighbors.DOWN == size * 2

        # top right corner
        pos = size - 1
        neighbors = g.neighbors(pos)
        assert neighbors.UP == None
        assert neighbors.LEFT == pos - 1
        assert neighbors.RIGHT == None
        assert neighbors.DOWN == pos + size

        # bottom left corner
        pos = size ** 2 - size
        neighbors = g.neighbors(pos)
        assert neighbors.UP == size ** 2 - size * 2
        assert neighbors.LEFT == None
        assert neighbors.RIGHT == pos + 1
        assert neighbors.DOWN == None

        # bottom right corner
        pos = size ** 2 - 1
        neighbors = g.neighbors(pos)
        assert neighbors.UP == pos - size
        assert neighbors.LEFT == pos - 1
        assert neighbors.RIGHT == None
        assert neighbors.DOWN == None

        # middle of grid
        pos = 42
        neighbors = g.neighbors(pos)
        assert neighbors.UP == pos - size
        assert neighbors.LEFT == pos - 1
        assert neighbors.RIGHT == pos + 1
        assert neighbors.DOWN == pos + size

    def test_empty_positions(self):
        g = Grid()
        g.mark(0, 'X')
        g.mark(99, 'X')
        assert g.empty_positions() == list(range(1, 99))
