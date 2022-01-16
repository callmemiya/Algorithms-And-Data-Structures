import fileinput
import sys


def decision(value):
    res = []
    while value != 0:
        if value == 1 or value == 3:
            res.append('inc')
            value -= 1
        elif value % 2 == 0:
            res.append('dbl')
            value /= 2
        elif value % 2 == 1:
            value1 = value - 1
            value2 = value + 1
            count1 = 0
            count2 = 0
            while value1 % 2 == 0:
                count1 += 1
                value1 /= 2
            while value2 % 2 == 0:
                count2 += 1
                value2 /= 2
            if count1 < count2:
                res.append('dec')
                value += 1
            else:
                res.append('inc')
                value -= 1
    return reversed(res)


def print_(res, out):
    for i in res:
        print(i, file=out)


def isdigit_(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


def main():
    out = sys.stdout
    for line in fileinput.input():
        if line == '\n':
            continue
        line = line.split()
        if len(line) == 1 and isdigit_(line[0]) and int(line[0]) >= 0:
            print_(decision(int(line[0])), out)
        else:
            print('error', file=out)


if __name__ == '__main__':
    main()
