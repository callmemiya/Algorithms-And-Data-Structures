import fileinput
import sys

class TreeNode:

    def __init__(self):
        self._children = {}
        self._endhere = False

class Trie:

    def __init__(self):
        self.__root = TreeNode()

    '''
    Сложность алгоритма O(n), где n - длина слова, которое вставляем в словарь,
    т.к. для каждой буквы слова необходимо проверить, есть ли такая буква в конкретной
    ветви дерева - словаря. Сложность по памяти также O(n), т.к. для каждой буквы
    создается узел дерева.
    '''
    def insert(self, word):
        parent = self.__root
        for i, char in enumerate(word):
            if char not in parent._children:
                parent._children[char] = TreeNode()
            parent = parent._children[char]
            if i == len(word) - 1:
                parent._endhere = True

    '''
    Сложность алгоритма O(n), где n - длина проверяемого слова, т.к. для каждой буквы слова
    нужно проверить, есть ли она в конкретной части дерева-словаря. Сложность по памяти O(1),
    т.к. для проверки не требуется выделения дополнительной памяти.
    '''
    def same(self, word):
        current = self.__root
        for letter in word:
            if letter not in current._children:
                return False
            else:
                current = current._children[letter]
        return current._endhere

    @staticmethod
    def searching(start, word, path, letter, similar, line_2, line_1):
        if start is None:
            return

        line = [line_1[0] + 1]
        for j in range(1, len(word) + 1):
            if word[j - 1] != letter:
                cost = 1
            else:
                cost = 0
            line.append(min(line_1[j] + 1,                    # удаление
                            line[j - 1] + 1,                  # вставка
                            line_1[j - 1] + cost))            # замена буквы

            if len(path) > 1 and j > 1 and letter == word[j - 2] and path[-2] == word[j - 1] and letter != word[j - 1]:
                line[j] = min(line[j], line_2[j - 2] + 1)     # транспозиция

        if line[-1] == 1 and start._endhere:
            similar.append(path)

        if min(line) <= 1:
            for letter, child in start._children.items():
                Trie.searching(child, word, path + letter, letter, similar, line_1, line)

    '''
    Для поиска похожих слов запускатся рекурсивная функция searching. Для проверки каждой
    буквы создается массив, длина которого n + 1, где n - длина входного слова.
    То есть сложность O(m * n), где m - количество узлов в дереве.
    В худшем случае массив будет создаваться для каждого узла дерева, это O(max * m),
    где max - максимальная длина слова в словаре, а m - количество узлов в дереве.
    Сложность по памяти:
    Массив длиной n + 1 для каждой буквы O(n*m), в худшем случае O(max*m). Также создаётся массив для
    хранения подходящих слов, в лучшем случае - похожих слов не найдено, массив пустой O(1),
    в худшем случае массив будет состоять из всех слов словаря(например, если дано слово
    'случал', а словарь состоит из слов 'случай', 'случаи', 'случае', 'случая'), а это
    O(N*n), где N - количество слов в словаре, а n - длина слова.
    При выполнении необходима память для 3 строк длины n, то есть O(n), где n - длина слова
    '''
    def sim(self, word):
        similar = []
        line_1 = [i for i in range(len(word) + 1)]
        for letter, current in self.__root._children.items():
            self.searching(current, word, letter, letter, similar, None, line_1)
        return sorted(similar)

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
    size = int(line)
except:
    sys.exit()
Tree = Trie()

for i in range(size):
    word = input().lower()
    Tree.insert(word)
l = 0
for line in fileinput.input():
    if line == '\n':
        continue
    line = line[:-1]
    if l > 0:
        print(file=out)
    l += 1

    if Tree.same(line.lower()):
        print(line, '- ok', end='', file=out)
    else:
        simi = Tree.sim(line.lower())
        if simi:
            print(line, '-> ', end="", file=out)
            for i in range(len(simi) - 1):
                print(simi[i], end=", ", file=out)
            print(simi[len(simi) - 1], end='', file=out)
        else:
            print(line, '-?', end='', file=out)
