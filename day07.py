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
    if variety not in varieties_by_children.keys():
        return []

    varieties_to_check = []
    varieties_to_check += varieties_by_children[variety]
    containing_bags = set()
    containing_bags.update([var[0] for var in varieties_by_children[variety]])

    while len(varieties_to_check) > 0:
        variety = varieties_to_check.pop()[0]
        if variety not in varieties_by_children.keys():
            continue
        containing_bags.update([var[0] for var in varieties_by_children[variety]])
        varieties_to_check += varieties_by_children[variety]

    return len(containing_bags)

"""
How many individual bags are required inside your single shiny gold bag?
"""

def total_containing_bags(bag_content_counts, num_parent_bags, variety):
    # print('-- count %rx %s' % (num_parent_bags, variety))
    if len(bag_content_counts[variety]) == 0:
        # print('---- no children, returning 1')
        return 1

    # print('-- children=%r' % (bag_content_counts[variety],))
    first_sum = 0
    for child_bag in bag_content_counts[variety]:
        num_bags, child_variety = child_bag
        sum_child_bags = total_containing_bags(bag_content_counts, 1, child_variety)
        # print('---- %s sum_child_bags=%r' % (child_variety, sum_child_bags))
        first_sum += num_bags * sum_child_bags

    # print('---- variety=%s num_parent_bags=%s, new sum = %s' % (variety, num_parent_bags, first_sum))
    return num_parent_bags + first_sum

def get_num_contained_bags(lines, variety):
    bag_content_counts = get_bag_content_counts(lines)
    # for var, children in bag_content_counts.items():
    #     print(var, children)

    num_parent_bags = 0
    total = total_containing_bags(bag_content_counts, num_parent_bags, variety)

    return total

def get_bag_content_counts(lines):
    bag_content_counts = {}
    for line in lines:
        container, children = parse_line(line)
        new_tuples = [(int(child[0]), child[1]) for child in children if child]
        bag_content_counts[container] = new_tuples
    return bag_content_counts

def main():
    with open('day07.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    variety = "shiny gold"

    result = get_num_containing_bags(lines, variety)
    print(result)

    result = get_num_contained_bags(lines, variety)
    print(result)

if __name__ == '__main__':
    main()
