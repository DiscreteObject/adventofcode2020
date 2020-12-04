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
    found_matching = 0
    for char in check.password:
        if char == check.check_char:
            found_matching += 1
    
    return found_matching >= check.min and found_matching <= check.max

def find_valid_passwords(lines):
    num_passed = 0
    for line in lines:
        check = parse_line(line)
        if check is None:
            continue
        if validate_password_check(check):
            num_passed += 1

    return num_passed

def main():
    with open('day02.txt') as f:
        lines = f.readlines()

    print(find_valid_passwords(lines))

if __name__ == '__main__':
    main()
