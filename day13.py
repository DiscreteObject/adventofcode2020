"""
The time this loop takes a particular bus is also its ID number: the bus with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11 departs at 0, 11, 22, 33, and so on. If you are there when the bus departs, you can ride that bus to the airport!

Your notes (your puzzle input) consist of two lines. The first line is your estimate of the earliest timestamp you could depart on a bus. The second line lists the bus IDs that are in service according to the shuttle company; entries that show x must be out of service, so you decide to ignore them.

To save time once you arrive, your goal is to figure out the earliest bus you can take to the airport. (There will be exactly one such bus.)

What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?
"""

from math import floor, inf

def find_first_bus(lines):
    start_time = int(lines[0])
    busses = lines[1].split(',')
    print(start_time, busses)

    lowest_wait_time_for_bus = (None, inf)
    for bus in busses:
        if bus == 'x':
            continue
        bus = int(bus)

        wait_time_for_next_bus = (floor(start_time / bus) * bus + bus) % start_time
        if wait_time_for_next_bus < lowest_wait_time_for_bus[1]:
            lowest_wait_time_for_bus = (bus, wait_time_for_next_bus)


    return lowest_wait_time_for_bus

"""
The shuttle company is running a contest: one gold coin for anyone that can find the earliest timestamp such that the first bus ID departs at that time and each subsequent listed bus ID departs at that subsequent minute. (The first line in your input is no longer relevant.)

An x in the schedule means there are no constraints on what bus IDs must depart at that time.

What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list?
"""

def find_first_timestamp_matching_offsets(lines):
    busses = lines[1].split(',')
    bus_0 = int(busses[0])
    multiplier = 1

    timestamp_0 = floor(100000000000000 / bus_0) * bus_0
    while True:
        multiplier += 1
        timestamp = timestamp_0 + bus_0 * multiplier
        # print('multiplier=%r on t=%r' % (multiplier, timestamp))
        busses_matched = 0

        for i, bus in enumerate(busses):
            if bus == 'x' or i == 0:
                busses_matched += 1
                continue

            bus = int(bus)
            if (timestamp + i) % bus != 0:
                continue
            # print('-- time=%r on i=%r bus=%r matches' % (timestamp + i, i, bus))
            busses_matched += 1

        if busses_matched == len(busses):
            return timestamp

def main():
    with open('day13.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    result = find_first_bus(lines)
    print(result[0] * result[1])

    result = find_first_timestamp_matching_offsets(lines)
    print(result)

if __name__ == '__main__':
    main()
