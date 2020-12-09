import re
"""
Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags. 

These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.

How many bag colors can eventually contain at least one shiny gold bag? 
"""
LINE_RE = re.compile("(.+) bags contain (.+).")
BAG_CHILDREN_RE = re.compile("(\d+) (.+) bags?")

def parse_line(line):
    match = LINE_RE.match(line)
    if not match:
        raise("Error parsing line %s" % line)

    container = match.group(1)
    children_strs = match.group(2).split(", ")
    children = []
    for child in children_strs:
        if BAG_CHILDREN_RE.match(child):
            children.append(BAG_CHILDREN_RE.match(child).groups())
        elif 'no other bags' in child:
            children.append(None)

    return (container, children)

def get_varieties_by_container(lines):
    varieties_by_container = {}
    for line in lines:
        container, children = parse_line(line)
        for child in children:
            if child is None:
                continue

            num, variety = child
            if variety not in varieties_by_container:
                varieties_by_container[variety] = [(container, num)]
            else:
                varieties_by_container[variety].append((container, num))

    return varieties_by_container

def get_num_containing_bags(lines, variety):
    varieties_by_children = get_varieties_by_container(lines)
    print(varieties_by_children)
    if variety not in varieties_by_children.keys():
        return 0

    varieties_to_check = []
    varieties_to_check += varieties_by_children[variety]
    print(varieties_to_check)
    containing_bags = set()
    containing_bags.update([var[0] for var in varieties_by_children[variety]])

    while len(varieties_to_check) > 0:
        variety = varieties_to_check.pop()[0]
        # print('popped', variety)
        if variety not in varieties_by_children.keys():
            continue
        print('** adding ', varieties_by_children[variety], ' to ' , containing_bags)
        containing_bags.update([var[0] for var in varieties_by_children[variety]])
        varieties_to_check += varieties_by_children[variety]

    return(containing_bags)

def main():
    with open('day07.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    variety = "shiny gold"

    result = get_num_containing_bags(lines, variety)
    print(len(result))

if __name__ == '__main__':
    main()
