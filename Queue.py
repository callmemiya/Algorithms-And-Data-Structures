import sys
import os

class Queue:
    def __init__(self, size):
        self.size = size
        self.array = [0 for i in range(size)]
        self.delete = 0
        self.safe = 0
        self.vol = 0

    def push(self, line, file):
        if self.vol == self.size:
            file.write('overflow\n')
        else:
            self.array[self.safe] = line
            self.vol += 1
            self.safe = (self.safe + 1) % self.size
        return

    def pop(self, file):
        if self.vol == 0:
            file.write('underflow\n')
        else:
            file.write(str(self.array[self.delete]) + '\n')
            self.array[self.delete] = 0
            self.delete = (self.delete + 1) % self.size
            self.vol -= 1

    def print(self, file):
        if self.vol == 0:
            file.write('empty\n')
        else:
            if self.delete >= self.safe:
                if self.safe == 0:
                    for i in range(self.delete, self.size - 1):
                        file.write(str(self.array[i]) + ' ')
                    file.write(str(self.array[self.size - 1]) + '\n')
                else:
                    for i in range(self.delete, self.size):
                        file.write(str(self.array[i]) + ' ')
                    for j in range(self.safe - 1):
                        file.write(str(self.array[j]) + ' ')
                    file.write(str(self.array[self.safe - 1]) + '\n')
            else:
                for i in range(self.delete, self.safe - 1):
                    file.write(str(self.array[i]) + ' ')
                file.write(str(self.array[self.safe - 1]) + '\n')

inputf = open(sys.argv[1], 'r')
outputf = open(sys.argv[2], 'w')
if os.stat(inputf.name).st_size == 0:
    inputf.close()
    outputf.close()
    sys.exit()
for line in inputf:
    try:
        if line == '\n':
            continue
        elif line[: 9] == 'set_size ' and line[9:-1].isdigit():
            break
        else:
            outputf.write('error\n')
    except EOFError:
        inputf.close()
        sys.exit()
try:
    size = int(line[9:])
except:
    outputf.close()
    sys.exit()
Qu = Queue(size)
for line in inputf:
    try:
        if line == '\n':
            continue
        elif line[:5] == 'push ' and ' ' not in line[5:]:
            Qu.push(line[5: -1], outputf)
        elif line == "pop\n" or line == 'pop':
            Qu.pop(outputf)
        elif line == 'print\n' or line == 'print':
            Qu.print(outputf)
        else:
            outputf.write('error\n')
    except EOFError:
        inputf.close()
        outputf.close()
        sys.exit()
