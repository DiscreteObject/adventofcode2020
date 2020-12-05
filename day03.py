"""
You start on the open square (.) in the top-left corner and need to reach the bottom (below the bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper model that prefers rational numbers); start by counting all the trees you would encounter for the slope right 3, down 1:

From your starting position at the top-left, check the position that is right 3 and down 1. Then, check the position that is right 3 and down 1 from there, and so on until you go past the bottom of the map.

Starting at the top-left corner of your map and following a slope of right 3 and down 1, how many trees would you encounter?
"""

TREE = '#'

def find_number_trees(lines, right_step, down_step):
    # print('0 1 2 3 4 5 6 7 8 9 0 1 2 3')
    # for line in lines:
    #     print(' '.join([c for c in line]))
    row, col = 0, 0
    num_trees = 0
    while row < len(lines):
        if lines[row][col] == TREE:
            num_trees += 1
        # print('%r, %r char=%r' % (row, col, lines[row][col]))
        col = (col + right_step) % len(lines[row])
        row += down_step

    return num_trees

def find_number_trees_1(lines):
    return find_number_trees(lines, right_step=3, down_step=1)

"""
Determine the number of trees you would encounter if, for each of the following slopes, you start at the top-left corner and traverse the map all the way to the bottom:

    Right 1, down 1.
    Right 3, down 1. (This is the slope you already checked.)
    Right 5, down 1.
    Right 7, down 1.
    Right 1, down 2.
"""

def find_number_trees_2(lines):
    slopes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2)
    ]
    product = 1
    for slope in slopes:
        product *= find_number_trees(lines, right_step=slope[0], down_step=slope[1])

    return product

def main():
    with open('day03.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    # Part 1
    print(find_number_trees_1(lines))

    # Part 2
    print(find_number_trees_2(lines))


if __name__ == '__main__':
    main()
