"""
The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:

    Action N means to move north by the given value.
    Action S means to move south by the given value.
    Action E means to move east by the given value.
    Action W means to move west by the given value.
    Action L means to turn left the given number of degrees.
    Action R means to turn right the given number of degrees.
    Action F means to move forward by the given value in the direction the ship is currently facing.

Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
"""
from collections import namedtuple
from enum import Enum, auto

class Heading(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

Position = namedtuple('Position', ['x', 'y'])

class InstructionType(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()
    LEFT = auto()
    RIGHT = auto()
    FORWARD = auto()

class InputParser:
    INPUT_KEY = {
        'N': InstructionType.NORTH,
        'E': InstructionType.EAST,
        'S': InstructionType.SOUTH,
        'W': InstructionType.WEST,
        'L': InstructionType.LEFT,
        'R': InstructionType.RIGHT,
        'F': InstructionType.FORWARD,
    }

    @classmethod
    def input_to_instruction_type(cls, input_char):
        return cls.INPUT_KEY[input_char]

class Instruction:
    def __init__(self, type_, num_units):
        self.type = type_
        self.num_units = num_units

    @classmethod
    def from_input_line(cls, input_line):
        instr_char, num_units = input_line[0], int(input_line[1:])
        type_ = InputParser.input_to_instruction_type(instr_char)
        return cls(type_=type_, num_units=num_units)

    def __str__(self):
        return "<Instruction type={} num_units={}>".format(self.type, self.num_units)


class Ship:
    def __init__(self, heading):
        self.heading = heading
        self.position = Position(x=0, y=0)

    def __str__(self):
        return "<Ship pos=({}) heading={} >".format(self.position, self.heading)

    def run_instructions(self, instructions):
        for instr in instructions:
            self.update(instr)

    def move_north(self, num_units):
        self.position = self.position._replace(y=self.position.y - num_units)

    def move_east(self, num_units):
        self.position = self.position._replace(x=self.position.x + num_units)

    def move_south(self, num_units):
        self.position = self.position._replace(y=self.position.y + num_units)

    def move_west(self, num_units):
        self.position = self.position._replace(x=self.position.x - num_units)

    def rotate_left(self, num_units):
        rotation_units = int(num_units / 90)
        self.heading = Heading((self.heading.value - rotation_units) % len(Heading))

    def rotate_right(self, num_units):
        rotation_units = int(num_units / 90)
        self.heading = Heading((self.heading.value + rotation_units) % len(Heading))

    def move_by_heading(self, num_units):
        if self.heading == Heading.NORTH:
            self.move_north(num_units)
        elif self.heading == Heading.EAST:
            self.move_east(num_units)
        elif self.heading == Heading.SOUTH:
            self.move_south(num_units)
        elif self.heading == Heading.WEST:
            self.move_west(num_units)

    def update(self, instruction):
        if instruction.type == InstructionType.NORTH:
            self.move_north(instruction.num_units)
        elif instruction.type == InstructionType.EAST:
            self.move_east(instruction.num_units)
        elif instruction.type == InstructionType.SOUTH:
            self.move_south(instruction.num_units)
        elif instruction.type == InstructionType.WEST:
            self.move_west(instruction.num_units)
        elif instruction.type == InstructionType.FORWARD:
            self.move_by_heading(instruction.num_units)
        elif instruction.type == InstructionType.LEFT:
            self.rotate_left(instruction.num_units)
        elif instruction.type == InstructionType.RIGHT:
            self.rotate_right(instruction.num_units)

    def manhattan_distance_from_origin(self):
        return abs(self.position.x) + abs(self.position.y)

def process_instructions(lines):
    ship = Ship(heading=Heading.EAST)
    instructions = [Instruction.from_input_line(line) for line in lines]
    ship.run_instructions(instructions)
    return ship.manhattan_distance_from_origin()

"""

Action N means to move the waypoint north by the given value.
Action S means to move the waypoint south by the given value.
Action E means to move the waypoint east by the given value.
Action W means to move the waypoint west by the given value.
Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
Action F means to move forward to the waypoint a number of times equal to the given value.

The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.

Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?
"""

class MovableObject:
    def __init__(self, position):
        self.position = position

    def move_north(self, num_units):
        self.position = self.position._replace(y=self.position.y + num_units)

    def move_east(self, num_units):
        self.position = self.position._replace(x=self.position.x + num_units)

    def move_south(self, num_units):
        self.position = self.position._replace(y=self.position.y - num_units)

    def move_west(self, num_units):
        self.position = self.position._replace(x=self.position.x - num_units)

    def update_position(self, x, y):
        self.position = self.position._replace(x=x, y=y)


class Waypoint(MovableObject):
    def __str__(self):
        return "waypoint={}".format(self.position)

    def rotate_right(self, num_units):
        rotation_units = int(num_units / 90)
        if rotation_units == 1:
            new_pos_x = self.position.y
            new_pos_y = -self.position.x
        elif rotation_units == 2:
            new_pos_x = -self.position.x
            new_pos_y = -self.position.y
        elif rotation_units == 3:
            new_pos_x = -self.position.y
            new_pos_y = self.position.x

        self.update_position(x=new_pos_x, y=new_pos_y)

    def rotate_left(self, num_units):
        self.rotate_right(abs(num_units - 360))


class Ship2(MovableObject):
    def __init__(self, position, waypoint_origin):
        super().__init__(position=position)
        self.waypoint = Waypoint(position=waypoint_origin)

    def __str__(self):
        return "<Ship pos=({}) waypoint={}>".format(self.position, self.waypoint)

    def run_instructions(self, instructions):
        for instr in instructions:
            self.update(instr)

    def move_to_waypoint(self, num_units):
        new_pos_x = self.position.x + self.waypoint.position.x * num_units
        new_pos_y = self.position.y + self.waypoint.position.y * num_units
        self.update_position(x=new_pos_x, y=new_pos_y)

    def update(self, instruction):
        if instruction.type == InstructionType.NORTH:
            self.waypoint.move_north(instruction.num_units)
        elif instruction.type == InstructionType.EAST:
            self.waypoint.move_east(instruction.num_units)
        elif instruction.type == InstructionType.SOUTH:
            self.waypoint.move_south(instruction.num_units)
        elif instruction.type == InstructionType.WEST:
            self.waypoint.move_west(instruction.num_units)
        elif instruction.type == InstructionType.FORWARD:
            self.move_to_waypoint(instruction.num_units)
        elif instruction.type == InstructionType.LEFT:
            self.waypoint.rotate_left(instruction.num_units)
        elif instruction.type == InstructionType.RIGHT:
            self.waypoint.rotate_right(instruction.num_units)

    def manhattan_distance_from_origin(self):
        return abs(self.position.x) + abs(self.position.y)


def process_instructions_2(lines):
    origin = Position(x=0, y=0)
    waypoint_origin = Position(x=10, y=1)
    ship = Ship2(position=origin, waypoint_origin=waypoint_origin)

    instructions = [Instruction.from_input_line(line) for line in lines]
    ship.run_instructions(instructions)
    return ship.manhattan_distance_from_origin()

def main():
    with open('day12.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    result = process_instructions(lines)
    print(result)

    result = process_instructions_2(lines)
    print(result)

if __name__ == '__main__':
    main()
