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

    @property
    def is_seat(self):
        return self.type == CellType.SEAT

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

        for row in range(upper_bound, lower_bound + 1):
            for col in range(left_bound, right_bound + 1):
                if (row, col) != row_col_tuple:
                    adjacent_cell_tuples.append((row, col))

        return adjacent_cell_tuples

    def adjacent_cells_from_position(self, row_col_tuple):
        adjacent_cell_tuples = self.adjacent_cell_coords_from_position(row_col_tuple)

        return [self.cell_at(adjacent_cell_tuple) for adjacent_cell_tuple in adjacent_cell_tuples]

    def num_occupied_cells_from_cells(self, cells):
        occupied_fn = lambda cell: cell.type == CellType.SEAT and cell.state == CellState.OCCUPIED
        filtered_cells = list(filter(occupied_fn, cells))
        return len(filtered_cells)

    def next_cell_iteration_for_cell_at_adjacent(self, row_col_tuple):
        current_cell = self.cell_at(row_col_tuple)

        if current_cell.type == CellType.FLOOR:
            return current_cell

        adjacent_cells = self.adjacent_cells_from_position(row_col_tuple)

        num_occupied_adjacent_cells = self.num_occupied_cells_from_cells(adjacent_cells)

        if current_cell.state == CellState.EMPTY and num_occupied_adjacent_cells == 0:
            return Cell.init_occupied()

        if current_cell.state == CellState.OCCUPIED and num_occupied_adjacent_cells >= 4:
            return Cell.init_empty()

        return current_cell

    def visible_cell_coords_from_position(self, row_col_tuple):
        visible_cell_tuples = []

        # up left
        row, col = row_col_tuple
        while row > 0 and col > 0:
            row -= 1
            col -= 1
            cell = self.cell_at((row, col))
            if cell.is_seat:
                visible_cell_tuples.append((row, col))
                break

        # up
        row, col = row_col_tuple
        while row > 0:
            row -= 1
            cell = self.cell_at((row, col))
            if cell.is_seat:
                visible_cell_tuples.append((row, col))
                break

        # up right
        row, col = row_col_tuple
        while row > 0 and col < self.width - 1:
            row -= 1
            col += 1
            cell = self.cell_at((row, col))
            if cell.is_seat:
                visible_cell_tuples.append((row, col))
                break

        # left
        row, col = row_col_tuple
        while col > 0:
            col -= 1
            cell = self.cell_at((row, col))
            if cell.is_seat:
                visible_cell_tuples.append((row, col))
                break

        # right
        row, col = row_col_tuple
        while col < self.width - 1:
            col += 1
            cell = self.cell_at((row, col))
            if cell.is_seat:
                visible_cell_tuples.append((row, col))
                break

        # down left
        row, col = row_col_tuple
        while row < self.height - 1 and col > 0:
            row += 1
            col -= 1
            cell = self.cell_at((row, col))
            if cell.is_seat:
                visible_cell_tuples.append((row, col))
                break

        # down
        row, col = row_col_tuple
        while row < self.height - 1:
            row += 1
            cell = self.cell_at((row, col))
            if cell.is_seat:
                visible_cell_tuples.append((row, col))
                break

        # down right
        row, col = row_col_tuple
        while row < self.height - 1 and col < self.width - 1:
            row += 1
            col += 1
            cell = self.cell_at((row, col))
            if cell.is_seat:
                visible_cell_tuples.append((row, col))
                break

        return visible_cell_tuples

    def visible_cells_from_position(self, row_col_tuple):
        visible_cell_tuples = self.visible_cell_coords_from_position(row_col_tuple)
        return [self.cell_at(visible_cell_tuple) for visible_cell_tuple in visible_cell_tuples]

    def num_occupied_visible_seats(self, row_col_tuple):
        visible_cells = self.visible_cells_from_position(row_col_tuple)
        num_occupied_visible_cells = self.num_occupied_cells_from_cells(visible_cells)
        return num_occupied_visible_cells

    def next_cell_iteration_for_cell_at_visible(self, row_col_tuple):
        current_cell = self.cell_at(row_col_tuple)

        if current_cell.type == CellType.FLOOR:
            return current_cell

        num_occupied_visible_seats = self.num_occupied_visible_seats(row_col_tuple)

        if current_cell.state == CellState.EMPTY and num_occupied_visible_seats == 0:
            return Cell.init_occupied()

        if current_cell.state == CellState.OCCUPIED and num_occupied_visible_seats >= 5:
            return Cell.init_empty()

        return current_cell

    def next_cell_iteration_for_cell_at(self, row_col_tuple, lookup_version):
        if lookup_version == 'ADJACENT':
            return self.next_cell_iteration_for_cell_at_adjacent(row_col_tuple)
        else:
            return self.next_cell_iteration_for_cell_at_visible(row_col_tuple)

    @classmethod
    def from_previous_grid(cls, previous_grid, lookup_version):
        new_cell_rows = []
        for i in range(previous_grid.height):
            new_row = []
            for j in range(previous_grid.width):
                new_row.append(previous_grid.next_cell_iteration_for_cell_at((i, j), lookup_version))
            new_cell_rows.append(new_row)

        return cls(cell_rows=new_cell_rows)

    def changed_from_previous_state(self, previous_grid):
        for i in range(self.height):
            for j in range(self.width):
                if not self.cell_at((i, j)).matches_cell(previous_grid.cell_at((i, j))):
                    return True

        return False

    def num_occupied_seats(self):
        return sum([sum([1 for cell in row if cell.is_occupied]) for row in self.cell_rows])

def find_occupied_seats_at_equilibrium(lines, lookup_version):
    previous_grid = Grid.from_input_lines(lines)
    next_grid = Grid.from_previous_grid(previous_grid, lookup_version)
    count = 0
    while next_grid.changed_from_previous_state(previous_grid):
        count += 1
        previous_grid = next_grid
        next_grid = Grid.from_previous_grid(previous_grid, lookup_version)

    print('found equilibrium at %r iterations' % count)
    return next_grid.num_occupied_seats()


def main():
    with open('day11.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    lookup_version = 'ADJACENT'
    result = find_occupied_seats_at_equilibrium(lines, lookup_version)
    print(result)

    lookup_version = 'VISIBLE'
    result = find_occupied_seats_at_equilibrium(lines, lookup_version)
    print(result)


if __name__ == '__main__':
    main()
