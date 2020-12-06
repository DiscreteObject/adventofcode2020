import math

"""
Instead of zones or groups, this airline uses binary space partitioning to seat people. A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane (numbered 0 through 127). Each letter tells you which half of a region the given seat is in. Start with the whole list of rows; the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127). The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps. L means to keep the lower half, while R means to keep the upper half.

Every seat also has a unique seat ID: multiply the row by 8, then add the column. In this example, the seat has ID 44 * 8 + 5 = 357.

As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?
"""

def binary_partition(instructions, left_bound, right_bound, left_step, right_step):
    for inst in instructions:
        if inst == left_step:
            right_bound = left_bound + math.floor((right_bound - left_bound) / 2)
        elif inst == right_step:
            left_bound = left_bound + math.ceil((right_bound - left_bound) / 2)
        else:
            raise('!! Unknown instruction %r in %r' % (inst, instructions))

    return left_bound

def parse_row(row_part):
    instr = list(row_part)
    left_bound, right_bound = 0, 127
    return binary_partition(instr, left_bound, right_bound, left_step='F', right_step='B')

def parse_col(col_part):
    instr = list(col_part)
    left_bound, right_bound = 0, 8
    return binary_partition(instr, left_bound, right_bound, left_step='L', right_step='R')

def calculate_seat_id(row, col):
    return row * 8 + col

def parse_seat_id(line):
    row_num = parse_row(line[:7])
    col_num = parse_col(line[7:])
    return calculate_seat_id(row_num, col_num)

def get_sorted_seat_ids(lines):
    return sorted([parse_seat_id(line) for line in lines])

def find_missing_seat(sorted_seat_ids, lowest_seat_id, highest_seat_id):
    for i, elem in enumerate(sorted_seat_ids):
        if sorted_seat_ids[i + 1] != elem + 1:
            return elem + 1
    return None

def main():
    with open('day05.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    print(parse_seat_id('FBFBBFFRLR') == 357)
    print(parse_seat_id('BFFFBBFRRR') == 567)
    print(parse_seat_id('FFFBBBFRRR') == 119)
    print(parse_seat_id('BBFFBBFRLL') == 820)

    sorted_seat_ids = get_sorted_seat_ids(lines)

    lowest_seat_id, highest_seat_id = sorted_seat_ids[0], sorted_seat_ids[-1]
    print(lowest_seat_id, highest_seat_id)
    print(find_missing_seat(sorted_seat_ids, lowest_seat_id, highest_seat_id))

if __name__ == '__main__':
    main()