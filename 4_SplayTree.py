from collections import deque
import fileinput
import sys


class Node:
    def __init__(self, key, value, parent):
        self._key = key
        self._value = value
        self._left = None
        self._right = None
        self._parent = parent


class SpTree:
    def __init__(self):
        self.__root = None

    def insert(self, key, value):
        if self.__root is None:
            self.__root = Node(key, value, None)
            return True
        current = self.__root
        while current is not None:
            if current._key > key:
                if current._left is None:
                    current._left = Node(key, value, current)
                    current._left._parent = current
                    self.__splay(current._left)
                    break
                else:
                    current = current._left
            elif current._key < key:
                if current._right is None:
                    current._right = Node(key, value, current)
                    current._right._parent = current
                    self.__splay(current._right)
                    break
                else:
                    current = current._right
            else:
                self.__splay(current)
                return False
        return True

    def delete(self, key):
        node = self.__root
        while node is not None:
            if node._key > key:
                if node._left is None:
                    self.__splay(node)
                    return False
                node = node._left
            elif node._key < key:
                if node._right is None:
                    self.__splay(node)
                    return False
                node = node._right
            elif node._key == key:
                self.__splay(node)
                break
        if node is None:
            return False
        if node._left is not None:
            leftsubtree = node._left
            leftsubtree._parent = None
        else:
            leftsubtree = None
        if node._right is not None:
            rightsubtree = node._right
            rightsubtree._parent = None
        else:
            rightsubtree = None

        if leftsubtree is None:
            self.__root = rightsubtree
        elif rightsubtree is None:
            self.__root = leftsubtree
        else:
            self.__root = leftsubtree
            node = leftsubtree
            while node._right is not None:
                node = node._right
            self.__splay(node)
            node._right = rightsubtree
            rightsubtree._parent = node
        return True

    def __Zig(self, vertex):
        if vertex._parent._left == vertex:
            vertex._parent._left = vertex._right
            if vertex._right is not None:
                vertex._right._parent = vertex._parent
            vertex._right = vertex._parent

        if vertex._parent._right == vertex:
            vertex._parent._right = vertex._left
            if vertex._left is not None:
                vertex._left._parent = vertex._parent
            vertex._left = vertex._parent

        grparent = vertex._parent._parent
        if grparent is not None and grparent._right == vertex._parent:
            grparent._right = vertex
        elif grparent is not None and grparent._left == vertex._parent:
            grparent._left = vertex
        else:
            self.__root = vertex
        vertex._parent._parent = vertex
        vertex._parent = grparent

    def __ZigZig(self, node):
        self.__Zig(node._parent)
        self.__Zig(node)

    def __ZigZag(self, node):
        self.__Zig(node)
        self.__Zig(node)

    def __splay(self, node):
        while node != self.__root:
            if node._parent == self.__root:
                self.__Zig(node)
            else:
                if node == node._parent._left and node._parent == node._parent._parent._left:
                    self.__ZigZig(node)
                elif node == node._parent._right and node._parent == node._parent._parent._right:
                    self.__ZigZig(node)
                else:
                    self.__ZigZag(node)

    def set(self, key, value):
        if self.__root is None:
            return False
        current = self.__root
        while current is not None:
            if current._key > key:
                if current._left is None:
                    self.__splay(current)
                    return False
                current = current._left
            elif current._key < key:
                if current._right is None:
                    self.__splay(current)
                    return False
                current = current._right
            elif current._key == key:
                current._value = value
                self.__splay(current)
                return True

    def min(self):
        if self.__root is None:
            return None, None
        node = self.__root
        while node._left is not None:
            node = node._left
        self.__splay(node)
        return node._key, node._value

    def max(self):
        if self.__root is None:
            return None, None
        node = self.__root
        while node._right is not None:
            node = node._right
        self.__splay(node)
        return node._key, node._value

    def search(self, key):
        if self.__root is None:
            return None
        node = self.__root
        while node is not None:
            if node._key > key:
                if node._left is None:
                    self.__splay(node)
                    return None
                node = node._left
            elif node._key < key:
                if node._right is None:
                    self.__splay(node)
                    return None
                node = node._right
            elif node._key == key:
                self.__splay(node)
                return node._value

    def __maxDepth(self, node):
        if node:
            return 1 + max(self.__maxDepth(node._left), self.__maxDepth(node._right))
        return 0

    def __maxd(self):
        return self.__maxDepth(self.__root)

    def print_(self, out):
        if self.__root is None:
            print('_', file=out)
            return
        print('[{} {}]'.format(self.__root._key, self.__root._value), file=out)
        if self.__root._right is None and self.__root._left is None:
            return
        Queue = deque()
        if self.__root._left is not None:
            Queue.append(self.__root._left)
        else:
            Queue.append(1)
        if self.__root._right is not None:
            Queue.append(self.__root._right)
        else:
            Queue.append(1)
        curlevel = 1                         # текущий уровень, не считая уровня вершины
        nodesintree = 2 ** self.__maxd() - 1   # общее количество узлов в дереве
        nodesinqueue = 2                     # счетчик количества узлов, побывавших в очереди
        n = 2                                # количество вершин на уровне
        line = ''
        while len(Queue) != 0:
            node = Queue.popleft()
            if type(node) != int:
                line += '[{} {} {}] '.format(node._key, node._value, node._parent._key)
                n -= 1
            else:
                n -= node
                for x in range(node):
                    line += '_ '
            if n == 0:
                if line[-1] == ' ':
                    line = line[:-1]
                print(line, file=out)
                line = ''
                curlevel += 1
                n = 2 ** curlevel
            if type(node) != int:
                if nodesinqueue < nodesintree:
                    if node._left is not None:
                        Queue.append(node._left)
                    else:
                        Queue.append(1)
                    if node._right is not None:
                        Queue.append(node._right)
                    else:
                        Queue.append(1)
                    nodesinqueue += 2
            else:
                if nodesinqueue < nodesintree:
                    Queue.append(node * 2)
                    nodesinqueue += node * 2

def isdigit(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

SplayTree = SpTree()
out = sys.stdout
for line in fileinput.input():
    if line == '\n':
        continue
    line = line[:-1]
    line = line.split()
    success = True
    if line[0] == 'add' and isdigit(line[1]):
        success = SplayTree.insert(int(line[1]), line[2])
    elif line[0] == 'set' and isdigit(line[1]):
        success = SplayTree.set(int(line[1]), line[2])
    elif line[0] == 'delete' and isdigit(line[1]):
        success = SplayTree.delete(int(line[1]))
    elif line[0] == 'search' and isdigit(line[1]):
        value = SplayTree.search(int(line[1]))
        if value is None:
            print(0, file=out)
        else:
            print(1, value, file=out)
    elif line[0] == 'min':
        key, value = SplayTree.min()
        if key is not None and value is not None:
            print(key, value, file=out)
        else:
            success = False
    elif line[0] == 'max':
        key, value = SplayTree.max()
        if key is not None and value is not None:
            print(key, value, file=out)
        else:
            success = False
    elif line[0] == 'print':
        SplayTree.print_(out)
    else:
        success = False
    if success is False:
        print('error', file=out)
