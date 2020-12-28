"""
XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one such pair.

The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?

"""

def compute_sums_for_subarray(subarray, memoized_sums = {}):
    sums = set()
    for i in range(0, len(subarray) - 1):
        j = i + 1

        while j < len(subarray):
            memo_key = (subarray[i], subarray[j])
            if memo_key in memoized_sums:
                sums.add(memoized_sums[memo_key])
                j += 1
                continue
            sums.add(subarray[i] + subarray[j])
            memoized_sums[memo_key] = subarray[i] + subarray[j]
            j += 1

    return (sums, memoized_sums)

def find_first_violation(lines, preamble_length):
    check_pos = preamble_length
    memoized_sums = {}

    while check_pos < len(lines):
        start = check_pos - preamble_length
        subarray = lines[start:check_pos]
        sums, memoized_sums = compute_sums_for_subarray(subarray, memoized_sums)
        if lines[check_pos] not in sums:
            print('!! found violation %r at pos %r' % (lines[check_pos], check_pos))
            return (lines[check_pos], check_pos)
        check_pos += 1


"""
The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.

To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example, these are 15 and 47, producing 62.
"""

def find_range_for_violation(lines, violation_result, violation_pos):
    range_end_pos = violation_pos
    
    while range_end_pos > 0:
        range_end_pos -= 1
        current_sum = 0
        range_start_pos = range_end_pos
        # print('on range_end_pos=%r current_sum=%r range_start_pos=%r' % (range_end_pos, current_sum, range_start_pos))

        while current_sum < violation_result:
            # print('-- adding %r + %r = %r' % (lines[range_start_pos], current_sum, current_sum + lines[range_start_pos]))
            current_sum += lines[range_start_pos]
            range_start_pos -= 1

        if current_sum == violation_result:
            return (range_start_pos + 1, range_end_pos)


def main():
    with open('day09.txt') as f:
        lines = [int(line.strip()) for line in f.readlines()]

    preamble_length = 25
    violation_result, violation_pos = find_first_violation(lines, preamble_length)
    print(violation_result, violation_pos)
    result_range = find_range_for_violation(lines, violation_result, violation_pos)
    print(result_range)

    subrange = lines[result_range[0]:result_range[1] + 1]
    print(subrange)
    least, greatest = min(subrange), max(subrange)

    print(least + greatest)


if __name__ == '__main__':
    main()
