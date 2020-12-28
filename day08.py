"""
The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).

    acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0. After an acc instruction, the instruction immediately below it is executed next.
    jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction, jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
    nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?

"""
import copy
from collections import OrderedDict

def run_program_and_return_acc_before_loop(lines):
    acc = 0
    current_line_num = 0
    lines_executed = OrderedDict()
    while current_line_num not in lines_executed.keys():
        if current_line_num >= len(lines):
            return (lines_executed, acc, True)
        cmd, arg = lines[current_line_num].split()
        lines_executed[current_line_num] = True
        # print('current=%s instruction = %s %s' % (current_line_num, cmd, arg))
        if cmd == 'nop':
            current_line_num += 1
        elif cmd == 'acc':
            op, amount = arg[0], int(arg[1:])
            current_line_num += 1
            # print('-- setting acc: %r %s %r' % (acc, op, amount))
            if op == '+':
                acc += amount
            elif op == '-':
                acc -= amount
        elif cmd == 'jmp':
            op, amount = arg[0], int(arg[1:])
            # print('-- jumping %s' % arg)
            if op == '+':
                current_line_num += amount
            elif op == '-':
                current_line_num -= amount

    return (lines_executed, acc, False)

"""
Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
"""

def find_acc_after_corrected_program(lines, lines_executed):
    lines_reversal_checked = OrderedDict()
    for line_num in lines_executed.keys():
        if lines[line_num].startswith('acc'):
            continue
        lines_reversal_checked[line_num] = True
        # print('checking reversal %r: %r' % (line_num, lines[line_num]))
        new_lines = copy.deepcopy(lines)
        cmd, arg = new_lines[line_num].split()
        if cmd == 'jmp':
            new_cmd = 'nop'
        elif cmd == 'nop':
            new_cmd = 'jmp'
        new_lines[line_num] = ' '.join([new_cmd, arg])

        new_lines_executed, acc, program_terminated = run_program_and_return_acc_before_loop(new_lines)

        if program_terminated:
            print('!! Terminated acc=%r' % acc)
            return acc

    return None

def main():
    with open('day08.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    lines_executed, acc, result = run_program_and_return_acc_before_loop(lines)
    print(acc)

    acc = find_acc_after_corrected_program(lines, lines_executed)
    print(acc)


if __name__ == '__main__':
    main()
