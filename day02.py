"""
Part 1
To try to debug the problem, they have created a list (your puzzle input) of passwords (according to the corrupted database) and the corporate policy when that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc

Each line gives the password policy and then the password. The password policy indicates the lowest and highest number of times a given letter must appear for the password to be valid. For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is not; it contains no instances of b, but needs at least 1. The first and third passwords are valid: they contain one a or nine c, both within the limits of their respective policies.

"""

import re
from collections import namedtuple

PasswordCheck = namedtuple('PasswordCheck', ['min', 'max', 'check_char', 'password'])

PASSWORD_POLICY_RE = re.compile('(\d+)-(\d+)\s+(\w):\s+(\w+)')

def parse_line(line):
    match = PASSWORD_POLICY_RE.match(line)
    if match:
        min_, max_, check_char, password = match.groups()
        return PasswordCheck(min=int(min_), max=int(max_), check_char=check_char, password=password)
    else:
        return None

def validate_password_check(check):
    if not check:
        return False

    matching_chars = sum([char == check.check_char for char in check.password])

    return matching_chars >= check.min and matching_chars <= check.max

def find_valid_passwords_1(lines):
    return sum([int(validate_password_check(parse_line(line))) for line in lines])

"""
Part 2

Each policy actually describes two positions in the password, where 1 means the first character, 2 means the second character, and so on. (Be careful; Toboggan Corporate Policies have no concept of "index zero"!) Exactly one of these positions must contain the given letter. Other occurrences of the letter are irrelevant for the purposes of policy enforcement.

Given the same example list from above:

    1-3 a: abcde is valid: position 1 contains a and position 3 does not.
    1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
    2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

"""

def find_valid_passwords_2(lines):
    pass

def main():
    with open('day02.txt') as f:
        lines = f.readlines()

    print(find_valid_passwords_1(lines))
    print(find_valid_passwords_2(lines))

if __name__ == '__main__':
    main()
