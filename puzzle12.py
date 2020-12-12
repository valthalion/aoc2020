from math import cos, radians, sin


def read_input():
    with open('puzzle12.in', 'r') as f:
        yield from ((cmd[0], int(cmd[1:])) for cmd in f)


def part_1():
    cmds = read_input()
    pos = [0, 0]
    heading = 0
    # print(pos, heading)
    for cmd, arg in cmds:
        if cmd == 'N':
            pos[1] += arg
        elif cmd == 'S':
            pos[1] -= arg
        elif cmd == 'E':
            pos[0] += arg
        elif cmd == 'W':
            pos[0] -= arg
        elif cmd == 'F':
            pos[0] += arg * cos(radians(heading))
            pos[1] += arg * sin(radians(heading))
        elif cmd == 'L':
            heading = (heading + arg) % 360
        elif cmd == 'R':
            heading = (heading - arg) % 360
        else:
            raise ValueError('Ivalid command', cmd)
        # print(cmd, arg, '->', pos, heading)
    return round(sum(abs(x) for x in pos))


def part_2():
    cmds = read_input()
    pos = complex(0)
    waypoint = complex(10, 1)
    for cmd, arg in cmds:
        if cmd == 'N':
            waypoint += complex(0, arg)
        elif cmd == 'S':
            waypoint -= complex(0, arg)
        elif cmd == 'E':
            waypoint += arg
        elif cmd == 'W':
            waypoint -= arg
        elif cmd == 'F':
            pos += arg * waypoint
        elif cmd == 'L':
            angle = radians(arg)
            waypoint *= complex(cos(angle), sin(angle))
        elif cmd == 'R':
            angle = - radians(arg)
            waypoint *= complex(cos(angle), sin(angle))
        else:
            raise ValueError('Ivalid command', cmd)
    return round(abs(pos.real) + abs(pos.imag))
