"""
All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.

Floor (.) never changes; seats don't move, and nobody sits on the floor.

Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
"""
from enum import Enum

class CellType(Enum):
    FLOOR = 1
    SEAT = 2

class CellState(Enum):
    EMPTY = 1
    OCCUPIED = 2

class Cell:
    FLOOR = '.'
    EMPTY = 'L'
    OCCUPIED = '#'

    INPUT_TO_CELL_TYPE_KEY = {
        FLOOR: CellType.FLOOR,
        EMPTY: CellType.SEAT,
        OCCUPIED: CellType.SEAT,
    }

    INPUT_TO_CELL_STATE_KEY = {
        FLOOR: None,
        EMPTY: CellState.EMPTY,
        OCCUPIED: CellState.OCCUPIED,
    }

    FORMAT_STR_KEY = {
        CellState.EMPTY: EMPTY,
        CellState.OCCUPIED: OCCUPIED,
    }

    def __init__(self, type_, state):
        self.type = type_
        self.state = state

    @classmethod
    def from_input_char(cls, input_char):
        return cls(
            type_=cls.INPUT_TO_CELL_TYPE_KEY[input_char],
            state=cls.INPUT_TO_CELL_STATE_KEY[input_char],
        )

    @classmethod
    def init_empty(cls):
        return cls(
            type_=CellType.SEAT,
            state=CellState.EMPTY,
        )

    @classmethod
    def init_occupied(cls):
        return cls(
            type_=CellType.SEAT,
            state=CellState.OCCUPIED,
        )

    def __str__(self):
        if self.type == CellType.FLOOR:
            return Cell.FLOOR
        else:
            return self.FORMAT_STR_KEY[self.state]

    @property
    def is_occupied(self):
        return self.state == CellState.OCCUPIED
    

    def matches_cell(self, other_cell):
        return self.type == other_cell.type and self.state == other_cell.state


class Grid:
    def __init__(self, cell_rows):
        self.cell_rows = cell_rows
        self.width = len(cell_rows[0])
        self.height = len(cell_rows)

    @classmethod
    def from_input_lines(cls, lines):
        cell_rows = []
        for line in lines:
            cell_rows.append([Cell.from_input_char(cell) for cell in list(line)])
        return cls(cell_rows=cell_rows)

    def __str__(self):
        joined_cells = []
        for cell_row in self.cell_rows:
            joined_cells.append('|'.join([str(cell) for cell in cell_row]))
        return '\n'.join(joined_cells)

    def cell_at(self, row_col_tuple):
        row, col = row_col_tuple
        return self.cell_rows[row][col]

    def adjacent_cell_coords_from_position(self, row_col_tuple):
        row, col = row_col_tuple
        adjacent_cell_tuples = []
        upper_bound = 0 if row == 0 else row - 1
        lower_bound = self.height - 1 if row == self.height - 1 else row + 1
        left_bound = 0 if col == 0 else col - 1
        right_bound = self.width - 1 if col == self.width - 1 else col + 1

        for row in list(range(upper_bound, lower_bound + 1)):
            for col in list(range(left_bound, right_bound + 1)):
                if (row, col) != row_col_tuple:
                    adjacent_cell_tuples.append((row, col))

        return adjacent_cell_tuples

    def adjacent_cells_from_position(self, row_col_tuple):
        adjacent_cell_tuples = self.adjacent_cell_coords_from_position(row_col_tuple)

        cells = []
        for adjacent_cell_tuple in adjacent_cell_tuples:
            row, col = adjacent_cell_tuple
            cells.append(self.cell_rows[row][col])
        return cells

    def num_occupied_adjacent_cells_from_position(self, row_col_tuple):
        adjacent_cells = self.adjacent_cells_from_position(row_col_tuple)

        occupied_fn = lambda cell: cell.type == CellType.SEAT and cell.state == CellState.OCCUPIED
        filtered_cells = list(filter(occupied_fn, adjacent_cells))
        return len(filtered_cells)

    def next_cell_iteration_for_cell_at(self, row_col_tuple):
        row, col = row_col_tuple
        current_cell = self.cell_rows[row][col]

        if current_cell.type == CellType.FLOOR:
            return current_cell

        num_occupied_adjacent_cells = self.num_occupied_adjacent_cells_from_position(row_col_tuple)

        if current_cell.state == CellState.EMPTY and num_occupied_adjacent_cells == 0:
            return Cell.init_occupied()

        if current_cell.state == CellState.OCCUPIED and num_occupied_adjacent_cells >= 4:
            return Cell.init_empty()

        return current_cell

    @classmethod
    def from_previous_grid(cls, previous_grid):
        new_cell_rows = []
        for i, row in enumerate(previous_grid.cell_rows):
            new_row = []
            for j, cell in enumerate(row):
                new_row.append(previous_grid.next_cell_iteration_for_cell_at((i, j)))
            new_cell_rows.append(new_row)

        return cls(cell_rows=new_cell_rows)

    def changed_from_other_state(self, other_grid):
        for i, row in enumerate(self.cell_rows):
            for j, cell in enumerate(row):
                if not cell.matches_cell(other_grid.cell_at((i, j))):
                    return True

        return False

    def num_occupied_seats(self):
        return sum([sum([1 for cell in row if cell.is_occupied]) for row in self.cell_rows])

def advance_grid(lines):
    previous_grid = Grid.from_input_lines(lines)

    next_grid = Grid.from_previous_grid(previous_grid)

    count = 0
    while next_grid.changed_from_other_state(previous_grid):
        count += 1
        previous_grid = next_grid
        next_grid = Grid.from_previous_grid(previous_grid)

    print('found equilibrium at %r iterations' % count)
    return next_grid.num_occupied_seats()


def main():
    with open('day11.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    result = advance_grid(lines)
    print(result)

if __name__ == '__main__':
    main()
