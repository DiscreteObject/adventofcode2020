import re
"""
The expected fields are as follows:

    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)

Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?
"""

REQUIRED_FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def valid_passport(passport):
    included_fields = [term.split(':')[0] for term in passport.split(' ')]

    return all([field in included_fields for field in REQUIRED_FIELDS])

def parse_passports(lines):
    passports = []
    current_passport = []
    for line in lines:
        if line == '':
            passports.append(' '.join(current_passport))
            current_passport = []
        else:
            current_passport.append(line)

    passports.append(' '.join(current_passport))
    return passports

def find_number_passports_1(lines):
    passports = parse_passports(lines)
    return sum([valid_passport(passport) for passport in passports])

"""
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

    Your job is to count the passports where all required fields are both present and valid according to the above rules. Here are some example values:
"""

HCL_RE = re.compile('\A#[0-9a-f]{6}\Z')
PID_RE = re.compile('\A\d{9}\Z')

def valid_byr(value):
    return int(value) >= 1920 and int(value) <= 2002

def valid_iyr(value):
    return int(value) >= 2010 and int(value) <= 2020

def valid_eyr(value):
    return int(value) >= 2020 and int(value) <= 2030

def valid_hgt(value):
    if value.endswith('cm'):
        num = int(value[:-2])
        return num >= 150 and num <= 193
    elif value.endswith('in'):
        num = int(value[:-2])
        return num >= 59 and num <= 76
    return False

def valid_hcl(value):
    return HCL_RE.match(value)

def valid_ecl(value):
    return value in 'amb blu brn gry grn hzl oth'.split()

def valid_pid(value):
    return PID_RE.match(value)

def vaildate_field(field, value):
    if field == 'byr':
        return valid_byr(value)
    elif field == 'iyr':
        return valid_iyr(value)
    elif field == 'eyr':
        return valid_eyr(value)
    elif field == 'hgt':
        return valid_hgt(value)
    elif field == 'hcl':
        return valid_hcl(value)
    elif field == 'ecl':
        return valid_ecl(value)
    elif field == 'pid':
        return valid_pid(value)
    elif field == 'cid':
        return True

def valid_passport_2(passport):
    passport_fields = { term.split(':')[0]: term.split(':')[1] for term in passport.split(' ')}

    if not all([field in passport_fields.keys() for field in REQUIRED_FIELDS]):
        return False

    for field, value in passport_fields.items():
        if not vaildate_field(field, value):
            return False

    return True

def find_number_passports_2(lines):
    passports = parse_passports(lines)
    return sum([valid_passport_2(passport) for passport in passports])

def main():
    with open('day04.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    print(find_number_passports_1(lines))
    print(find_number_passports_2(lines))

if __name__ == '__main__':
    main()