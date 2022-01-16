from math import log2, log
import sys
import fileinput


class Bitarray:
    def __init__(self, size):
        self.__size = size // 16 if size % 16 == 0 else size // 16 + 1
        self.__array = [0 for i in range(self.__size)]

    def add(self, idx):
        self.__array[idx // 16] = self.__array[idx // 16] | (1 << (15 - idx % 16))

    def get_bit(self, idx):
        return self.__array[idx // 16] & (1 << (15 - idx % 16)) != 0

    def result(self, size):
        result = []
        for i in range(len(self.__array)):
            byte = str(bin(self.__array[i]))[2:]
            if i == len(self.__array) - 1:
                if byte != '0':
                    result.append('0' * (16 - len(byte)))
                    if size % 16 != 0:
                        result.append(byte[:(size % 16 - (16 - len(byte)))])
                    else:
                        result.append(byte)
                else:
                    if size % 16 != 0:
                        result.append('0' * (size % 16))
                    else:
                        result.append('0' * 16)
            else:
                if len(byte) < 16:
                    result.append('0' * (16 - len(byte)))
                result.append(byte)
        return result


class BloomFilter:
    def __init__(self, size, p):
        self.__size = round(-size * log2(p)/log(2))
        self.__bit_array = Bitarray(self.__size)
        self.__primes = self.__prime(p)

    def get_sizes(self):
        return self.__size, len(self.__primes)

    def __prime(self, p):
        k = round(-log2(p))
        primes = [2]
        if k == 1:
            return primes
        n = 3
        while len(primes) < k:
            s = True
            for i in primes:
                if n % i == 0:
                    s = False
                    break
            if s:
                primes.append(n)
            n += 1
        return primes

    def add(self, k):
        for i in range(len(self.__primes)):
            h = (((i + 1) * k + self.__primes[i]) % (2 ** 31 - 1)) % self.__size
            self.__bit_array.add(h)

    def search(self, k):
        s = True
        for i in range(len(self.__primes)):
            h = (((i + 1) * k + self.__primes[i]) % (2 ** 31 - 1)) % self.__size
            if not self.__bit_array.get_bit(h):
                s = False
                return s
        return s

    def print(self, out):
        result = self.__bit_array.result(self.__size)
        for i in range(len(result)):
            if i == len(result) - 1:
                print(result[i], file=out)
            else:
                print(result[i], end='', file=out)


def pretender(line):
    if len(line) == 3 and line[0] == 'set':
        if line[1].isdigit() and int(line[1]) >= 1 and float(line[2]) < 1 and float(line[2]) > 0:
            if round(-int(line[1]) * log2(float(line[2])) / log(2)) >= 1 and round(-log2(float(line[2]))) >= 1:
                return True
    return False


def main():
    out = sys.stdout
    while True:
        try:
            line = input()
            if line == '':
                continue
            line = line.split()
            if pretender(line):
                break
            else:
                print('error', file=out)
                continue
        except EOFError:
            sys.exit()

    size = int(line[1])
    p = float(line[2])
    bloom_filter = BloomFilter(size, p)
    size_bit, n = bloom_filter.get_sizes()
    print(size_bit, n, file=out)

    for line in fileinput.input():
        try:
            if line == '\n':
                continue
            line = line.split()
            if line[0] == 'add' and line[1].isdigit():
                bloom_filter.add(int(line[1]))
            elif line[0] == 'search' and line[1].isdigit():
                s = bloom_filter.search(int(line[1]))
                if s:
                    print('1', file=out)
                else:
                    print('0', file=out)
            elif line[0] == 'print':
                bloom_filter.print(out)
            else:
                print('error', file=out)
        except IndexError:
            print('error', file=out)


if __name__ == '__main__':
    main()
