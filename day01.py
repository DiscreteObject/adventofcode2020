"""
Specifically, they need you to find the two entries that sum to 2020 and then multiply those two numbers together.

For example, suppose your expense report contained the following:

1721
979
366
299
675
1456

In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them together produces 1721 * 299 = 514579, so the correct answer is 514579.

Of course, your expense report is much larger. Find the two entries that sum to 2020; what do you get if you multiply them together?
"""

MAGIC_TOTAL = 2020

def find_answer(numbers):
    numbers_by_remainder = {}
    for position, number in enumerate(numbers):
        numbers_by_remainder[MAGIC_TOTAL - number] = position

    for remainder, position in numbers_by_remainder.items():
        if (MAGIC_TOTAL - remainder) in numbers_by_remainder.keys():
            print('%r * %r' % (numbers[position], remainder))
            return (numbers[position] * remainder)

    return None

"""
The Elves in accounting are thankful for your help; one of them even offers you a starfish coin they had left over from a past vacation. They offer you a second one if you can find three numbers in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?
"""

def find_triplet(numbers):
    numbers_by_remainder = {}
    numbers_positions = {}
    for position, number in enumerate(numbers):
        numbers_by_remainder[MAGIC_TOTAL - number] = position
        numbers_positions[number] = position

    for remainder, position_1 in numbers_by_remainder.items():
        for term_2, position_2 in numbers_positions.items():
            if position_1 == position_2:
                continue

            term_3 = remainder - term_2

            if numbers_positions.get(term_3):
                print('pos_1=%r numbers[position_1]=%r remainder=%r' % (position_1, numbers[position_1], remainder))
                print('-- pos_2=%r term_2=%r term_3=%r in numbers?=%r' % (position_2, term_2, term_3, (numbers_positions.get(term_3))))
                print('---- %r + %r + %r' % (numbers[position_1], term_2, term_3))
                return numbers[position_1] * term_2 * term_3

    return None


def main():
    with open('day01.txt') as f:
        numbers = [int(num.strip()) for num in f.readlines()]

    print(find_triplet(numbers))

if __name__ == '__main__':
    main()
