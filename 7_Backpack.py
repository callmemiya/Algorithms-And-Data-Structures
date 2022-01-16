import sys
import math
import fileinput

class Subject:

    def __init__(self, weight, cost):
        self.weight = weight
        self.cost = cost

class Backpack:

    def __init__(self):
        self.__subjects = dict()
        self.__decision = []
        self.__weight = 0
        self.__cost = 0

    def add(self, weight, cost):
        number = len(self.__subjects)
        self.__subjects[number] = Subject(weight, cost)

    def __get_weight_and_cost(self, nod):
        weight = [int(self.__subjects[item].weight/nod) for item in self.__subjects]
        cost = [self.__subjects[item].cost for item in self.__subjects]
        return weight, cost

    def __get_gcd(self, max_weight):
        if len(self.__subjects) == 1:
            return math.gcd(self.__subjects[0].weight, max_weight)
        nod = math.gcd(self.__subjects[0].weight, max_weight)
        for i in range(1, len(self.__subjects)):
            nod = math.gcd(nod, self.__subjects[i].weight)
        return nod

    def __search(self, max_weight):
        nod = self.__get_gcd(max_weight)
        weight, cost = self.__get_weight_and_cost(nod)
        max_weight = int(max_weight / nod)
        n = len(self.__subjects)
        matrix = [[0 for w in range(max_weight + 1)] for i in range(n + 1)]
        for i in range(n + 1):
            for w in range(max_weight + 1):
                if i == 0:
                    matrix[i][w] = 0
                elif weight[i - 1] <= w:
                    matrix[i][w] = max(cost[i - 1] + matrix[i - 1][w - weight[i - 1]], matrix[i - 1][w])
                else:
                    matrix[i][w] = matrix[i - 1][w]
        result_list = []
        max_cost = matrix[n][max_weight]
        max_weigh = 0
        for i in range(n, 0, -1):
            if max_cost <= 0:
                break
            if max_cost == matrix[i - 1][max_weight]:
                continue
            else:
                result_list.append(i - 1)
                max_cost -= cost[i - 1]
                max_weight -= weight[i - 1]
        for i in result_list:
            max_weigh += self.__subjects[i].weight
        return max_weigh, matrix[-1][-1], sorted(result_list)

    def decision(self, max_weight):
        if len(self.__subjects) == 0:
            return
        self.__weight, self.__cost, self.__decision = self.__search(max_weight)

    def print(self, out):
        if len(self.__subjects) == 0:
            return
        print(self.__weight, self.__cost, file=out)
        for i in self.__decision:
            print(i + 1, file=out)


def isdigit_(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def main():
    backpack = Backpack()
    out = sys.stdout
    while True:
        try:
            line = input()
            if line == '':
                continue
            elif line.isdigit():
                break
            else:
                print('error', file=out)
        except EOFError:
            break
    try:
        max_weight = int(line)
    except:
        sys.exit()

    for line in fileinput.input():
        try:
            if line == '\n':
                continue
            line = line[:-1]
            line = line.split()
            success = True
            if isdigit_(line[0]) and isdigit_(line[1]) and int(line[0]) >= 0 and int(line[1]) >= 0:
                backpack.add(int(line[0]), int(line[1]))
            else:
                success = False
            if success is False:
                print('error', file=out)
        except IndexError:
            print('error', file=out)
    backpack.decision(max_weight)
    backpack.print(out)


if __name__ == '__main__':
    main()
