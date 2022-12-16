from methods_for_crypro.methods import *
import random
from sympy import isprime, randprime
from typing import List
from file import *
from abc import abstractmethod, ABC
from functools import reduce


class RsaSystem(ABC):

    @abstractmethod
    def generate_c_number(self, f: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def eval_d_number(self, c: int, f: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def generate_p_q(self, v: int) -> List[list]:
        raise NotImplementedError

    @abstractmethod
    def eval_n(self, p: list, q: list) -> list:
        raise NotImplementedError

    @abstractmethod
    def eval_f(self, p: list, q: list):
        raise NotImplementedError


class RsaGraphColoring(RsaSystem):
    def generate_c_number(self, f: int) -> int:
        c = 0
        while euclid_algorithm(c, f)[0] != 1:
            c = random.randrange(2, f)
        return c

    def eval_d_number(self, c: int, f: int) -> int:
        return exp_mod(euclid_algorithm(c, f)[1], 1, f)

    def generate_p_q(self, v: int) -> List[list]:
        p_array = []
        q_array = []

        for _ in range(v):
            p = 0
            q = 0
            while p == q:
                while not isprime(p):
                    p = randprime(2, 2**24)
                while not isprime(q):
                    q = randprime(2, 2**24)

            p_array.append(p)
            q_array.append(q)
        return [p_array, q_array]

    def eval_n(self, p: list, q: list) -> list:
        n = []
        for i in range(len(p)):
            n.append(p[i] + q[i])
        return n
    
    def eval_f(self, p: list, q: list):
        f = []
        for i in range(len(p)):
            f.append((p[i]-1)*(q[i]-1))
        return f


class GraphColoring(RsaGraphColoring):

    def __init__(self, fileNameGraph, fileNameColors) -> None:
        super().__init__()
        self.__fileGraph = ReaderGraph(fileNameGraph)
        self.__fileGraph.read_file()
        self.__fileColor = ReaderColor(fileNameColors)
        self.__fileColor.read_file()
        self._encode_colors = {'R': '00', 'B': '01', 'Y': '10'}

    def coloring(self):
        self.p_array, self.q_array = self.generate_p_q(self.__fileGraph.v)
        self.n = self.eval_n(self.p_array, self.q_array)
        self.f = self.eval_f(self.p_array, self.q_array)

        self.keys_c = [self.generate_c_number(self.f[i])
                       for i in range(self.__fileGraph.v)]
        self.keys_d = [self.eval_d_number(self.keys_c[i], self.f[i])
                       for i in range(self.__fileGraph.v)]

        self.__permutation()

        r = [int(str(random.randint(2, 2**24)) + str(self._encode_colors[self.__fileColor._colors[key]]))
             for key in self.__fileColor._colors]

        z = [exp_mod(r[i], self.keys_d[i], self.n[i])
             for i in range(self.__fileGraph.v)]

    def __get_unique_colors(self) -> list:
        unique = []
        for key in self.__fileColor._colors:
            if self.__fileColor._colors[key] in unique:
                continue
            else:
                unique.append(self.__fileColor._colors[key])
        return unique

    def __permutation(self):
        unique_colors = self.__get_unique_colors()
        shuffle_colors = unique_colors.copy()
        while reduce(lambda x, y: x and y, map(lambda p, q: p == q, unique_colors, shuffle_colors), True):
            random.shuffle(shuffle_colors)

        dict_for_perm = {}
        for i in range(len(unique_colors)):
            dict_for_perm[unique_colors[i]] = shuffle_colors[i]

        for key in self.__fileColor._colors:
            self.__fileColor._colors[key] = dict_for_perm[self.__fileColor._colors[key]]


a = GraphColoring(fileNameGraph='./resources/data.txt',
                  fileNameColors='./resources/vertexColor.txt')
a.coloring()
