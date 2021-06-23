from src.utils import Neighbors


class Grid:
    def __init__(self, size=10, inital_char=".") -> None:
        self.size = size
        self.initial_char = inital_char
        self.reset()

    def get_size(self):
        """Gets the size of the grid

        Returns:
            int
        """
        return self.size

    def get_initial_char(self):
        """Gets the initial/empty char

        Returns:
            string
        """
        return self.initial_char

    def reset(self) -> None:
        """Resets all values to the initial value"""
        self.grid = [self.initial_char] * (self.size ** 2)

    def coords(self, p) -> tuple:
        """Gets x,y coordiates from a position int

        Args:
            p: zero-based position integer

        Returns:
            A tuple of (x, y)
        """
        [y, x] = divmod(p, self.size)
        return (x, y)

    def pos(self, x, y):
        """Gets position integer from an (x, y) coordinate tuple

        Args:
            x: zero-based x coordinate
            y: zero-based y coordinate

        Returns:
            A zero-based position
        """
        return y * self.size + x

    def val(self, p):
        """Gets value stored at position p

        Returns:
            A string
        """
        return self.grid[p] if p < self.size ** 2 and p >= 0 else None

    def val_by_coords(self, x, y):
        """Gets value stored at coordinates (x, y)

        Args:
            x: zero-based x coordinate
            y: zero-based y coordinate

        Returns:
            A string
        """
        return self.grid[self.pos(x, y)]

    def neighbors(self, p) -> Neighbors:
        """Gets positions of valid neighbors (excluding diagonal neighbors).  
           If the position is on an edge or corner, the neighbors that are outside the grid 
           boundary are None

        Args:
            p: zero-based position 

        Returns:
            Neighbors tuple
        """
        up = down = left = right = None

        if p >= self.size:
            up = p - self.size
        if p < self.size ** 2 - self.size:
            down = p + self.size
        if p % self.size > 0:
            left = p - 1
        if p % self.size < self.size - 1:
            right = p + 1

        return Neighbors(up, down, left, right)

    def empty_positions(self):
        """Get a list of all positions that are set to the initial value

        Returns:
            List of positions
        """
        return [x for x in range(len(self.grid)) if self.grid[x] == self.initial_char]

    def mark(self, p, val):
        """Set the value at position p

        Args:
            p: position
            val: value to set
        """
        self.grid[p] = val

    def render(self):
        """Renders the grid

        Returns:
            A string representation of the grid in size x size
        """
        s = ""
        for i in range(self.size):
            offset = i * self.size
            chars = self.grid[offset:offset + self.size]
            s += "\n" + "".join(["{} ".format(c) for c in chars])[:-1]
        return s[1:]
