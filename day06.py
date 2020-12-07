from collections import defaultdict
"""
The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.

abcx
abcy
abcz

In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the same question don't count extra; each question counts at most once.)

For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
"""

def get_question_group_sets(lines):
    groups = []
    current_group_set = set()
    for line in lines:
        if line == '':
            groups.append(current_group_set)
            current_group_set = set()
        else:
            current_group_set.update(list(line))

    groups.append(current_group_set)
    return groups

def get_total_num_questions(lines):
    groups = get_question_group_sets(lines)
    return sum(len(group) for group in groups)

"""
You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!

This list represents answers from five groups:

    In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
    In the second group, there is no question to which everyone answered "yes".
    In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
    In the fourth group, everyone answered yes to only 1 question, a.
    In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.

In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.
"""
def get_question_counts_for_group(group):
    counts = defaultdict(int)
    for member_questions in group:
        for question in member_questions:
            counts[question] += 1
    return counts

def get_question_groups(lines):
    groups = []
    current_group = []
    for line in lines:
        if line == '':
            groups.append(current_group)
            current_group = []
        else:
            current_group.append(line)

    groups.append(current_group)
    return groups

def get_everyone_answered_questions(lines):
    groups = get_question_groups(lines)

    all_groups_answer_counts = []
    for group in groups:
        counts = get_question_counts_for_group(group)
        all_questions_answered_count = sum(1 for q, count in counts.items() if count == len(group))
        all_groups_answer_counts.append(all_questions_answered_count)

    return all_groups_answer_counts

def get_sum_all_answered_questions(lines):
    return sum(get_everyone_answered_questions(lines))

def main():
    with open('day06.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    print(get_total_num_questions(lines))
    print(get_sum_all_answered_questions(lines))

if __name__ == '__main__':
    main()
