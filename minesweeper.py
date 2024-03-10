import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        count = 0

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) == cell:
                    continue

                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        a = set()

        if self.count == len(self.cells):
            return self.cells
        elif self.count == 0:
            return a
        else:
            return a

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.

        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:

            self.cells.discard(cell)
            self.count = self.count - 1

            return
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            try:
                self.cells.discard(cell)
                return
            except:

                return
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function has the main algorithm
        """

        self.moves_made.add(cell)
        self.safes.add(cell)
        neighbours = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.width and 0 <= j < self.height and ((i, j)) not in self.mines and ((i, j)) not in self.safes:
                    neighbours.add((i, j))

                elif 0 <= i < self.width and 0 <= j < self.height and ((i, j)) in self.mines:
                    count = count - 1
                    self.mines.add((i, j))

        if Sentence(neighbours, count) not in self.knowledge:
            self.knowledge.append(Sentence(neighbours, count))

        recheck = 1
        while recheck == 1:
            list_knowledge = copy.deepcopy(self.knowledge)
            for i in list_knowledge:
                if i.count == 0 and len(i.cells) > 0:
                    for f in i.cells:
                        if f not in self.safes and f not in self.moves_made and f not in self.mines:
                            self.mark_safe(f)

                elif i.count == len(i.cells) and i.count > 0:
                    for f in i.cells:
                        if f not in self.mines and f not in self.moves_made and f not in self.safes:
                            self.mark_mine(f)

            for i in list_knowledge:
                for j in list_knowledge:
                    if i != j and i in self.knowledge and j in self.knowledge:
                        if i.cells in j.cells:
                            a = j.cells - i.cells
                            b = j.count - i.count
                            self.knowledge.append(Sentence(a, b))

                        elif j.cells in i.cells:
                            a = i.cells - j.cells
                            b = i.count - j.count
                            self.knowledge.append(Sentence(a, b))

            if list_knowledge == self.knowledge:
                recheck = None
        return

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        """
        for x in range(self.height):
            for y in range(self.width):
                if ((x, y) not in self.moves_made and (x, y) in self.safes and (x, y) not in self.mines):
                    return (x, y)
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        """
        for x in range(self.width):
            for y in range(self.height):
                if ((x, y) not in self.moves_made and (x, y) not in self.mines):
                    return (x, y)
        return None
