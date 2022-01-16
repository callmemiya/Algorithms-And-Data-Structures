import fileinput
import sys


class Stack:
    def __init__(self, size):
        self.size = size
        self.array = [0 for i in range(size)]
        self.number = 0

    def push(self, line):
        if self.number == self.size:
            print('overflow')
        else:
            self.array[self.number] = line
            self.number += 1
        return

    def pop(self):
        if self.number == 0:
            print('underflow')
        else:
            print(self.array[self.number - 1])
            self.number -= 1
            self.array[self.number] = 0
        return

    def pr(self):
        if self.number == 0:
            print('empty')
        else:
            for i in range(self.number - 1):
                print(self.array[i], end=" ")
            print(self.array[self.number - 1])


while True:
    try:
        line = input()
        if line == '':
            continue
        elif line[: 9] == 'set_size ' and line[9:].isdigit():
            break
        else:
            print('error')
    except EOFError:
        break
try:
    size = int(line[9:])
except:
    sys.exit()
St = Stack(size)

for line in fileinput.input():
    if line == '\n':
        continue
    elif line[:5] == 'push ' and ' ' not in line[5:]:
        St.push(line[5: -1])
    elif line == "pop\n":
        St.pop()
    elif line == 'print\n':
        St.pr()
    else:
        print('error')

