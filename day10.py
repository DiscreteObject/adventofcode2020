"""
Each of your joltage adapters is rated for a specific output joltage (your puzzle input). Any given adapter can take an input 1, 2, or 3 jolts lower than its rating and still produce its rated output joltage.

In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the highest-rated adapter in your bag. (If your adapter list were 3, 9, and 6, your device's built-in adapter would be rated for 12 jolts.)

Treat the charging outlet near your seat as having an effective joltage rating of 0.

If you use every adapter in your bag at once, what is the distribution of joltage differences between the charging outlet, the adapters, and your device?

Find a chain that uses all of your adapters to connect the charging outlet to your device's built-in adapter and count the joltage differences between the charging outlet, the adapters, and your device. What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
"""

def find_differences(lines):
    sorted_lines = [0] + sorted(lines)
    diffs = {1: 0, 3: 0}

    current_pos = 0
    while current_pos < len(sorted_lines) - 1:
        current_pos += 1
        # print('on %r = %r' % (current_pos, sorted_lines[current_pos]))
        diff = sorted_lines[current_pos] - sorted_lines[current_pos - 1]
        diffs[diff] += 1
        # print('-- added diff of %r' % (diff))

    # Add device built-in adapter
    diffs[3] += 1
    return diffs

"""
To completely determine whether you have enough adapters, you'll need to figure out how many different ways they can be arranged. Every arrangement needs to connect the charging outlet to your device. The previous rules about when adapters can successfully connect still apply.

What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?
"""

def find_contiguous_subarrays(lines):
    sorted_lines = [0] + sorted(lines)
    current_pos = -1
    contiguous_subarrays = []

    while current_pos < len(sorted_lines) - 1:
        current_pos += 1
        subarray = [sorted_lines[current_pos]]
        # print('on pos[%r]= %r' % (current_pos, sorted_lines[current_pos]))
        while current_pos < len(sorted_lines) - 1 and sorted_lines[current_pos + 1] - sorted_lines[current_pos] == 1:
            # print('-- 1 apart, adding %r' % sorted_lines[current_pos + 1])
            subarray.append(sorted_lines[current_pos + 1])
            current_pos += 1
        # print('---- subarray %r' % subarray)
        contiguous_subarrays.append(subarray)

    return contiguous_subarrays

def find_num_paths_in_subarray(subarray):
    if len(subarray) == 1:
        return 1
    if len(subarray) == 2:
        return 1
    if len(subarray) == 3:
        return 2
    if len(subarray) == 4:
        return 4
    if len(subarray) == 5:
        return 7

def find_num_paths(lines):
    subarrays = find_contiguous_subarrays(lines)
    product = 1
    for subarray in subarrays:
        product *= find_num_paths_in_subarray(subarray)
    return product

def main():
    with open('day10.txt') as f:
        lines = [int(line.strip()) for line in f.readlines()]

    diffs = find_differences(lines)
    print(diffs)
    print(diffs[1] * diffs[3])

    result = find_num_paths(lines)
    print(result)

if __name__ == '__main__':
    main()
