from methods_for_crypro.methods import *
import random
from sympy import isprime
from typing import List
from file import *
from functools import reduce
from ciphers.rsa import RsaSystem


class RsaGraphColoring(RsaSystem):
    def generate_c_number(self, f: int) -> int:
        c = 0
        while euclid_algorithm(c, f)[0] != 1:
            c = random.randrange(2, f)
        return c

    def eval_d_number(self, c: int, f: int) -> int:
        return exp_mod(euclid_algorithm(c, f)[1], 1, f)

    def generate_p_q(self) -> list:
        p = 0
        q = 0
        while p == q:
            while not isprime(p):
                p = random.getrandbits(1024)
            while not isprime(q):
                q = random.getrandbits(1024)

        return [p, q]

    def geneterate_arrays_p_q(self, v: int) -> List[list]:
        p_array = []
        q_array = []
        for _ in range(v):
            temp_p, temp_q = self.generate_p_q()
            p_array.append(temp_p)
            q_array.append(temp_q)
        return [p_array, q_array]

    def eval_n(self, p: int, q: int) -> int:
        return p * q

    def eval_f(self, p: int, q: int) -> int:
        return (p-1)*(q-1)


class GraphColoring(RsaGraphColoring):

    def __init__(self, fileNameGraph: str, fileNameColors: str) -> None:
        super().__init__()
        self.__fileGraph = ReaderGraph(fileNameGraph)
        self.__fileGraph.read_file()
        self.__fileColor = ReaderColor(fileNameColors)
        self.__fileColor.read_file()
        self._encode_colors = {'R': '00', 'B': '01', 'Y': '10'}

    def coloring(self, alpha: int) -> bool:
        for _ in range(alpha * self.__fileGraph.e):
            self.p_array, self.q_array = self.geneterate_arrays_p_q(
                self.__fileGraph.v)
            self.n = [self.eval_n(self.p_array[i], self.q_array[i])
                      for i in range(self.__fileGraph.v)]
            self.f = [self.eval_f(self.p_array[i], self.q_array[i])
                      for i in range(self.__fileGraph.v)]
            self.__keys_c = [self.generate_c_number(self.f[i])
                             for i in range(self.__fileGraph.v)]
            self.keys_d = [self.eval_d_number(self.__keys_c[i], self.f[i])
                           for i in range(self.__fileGraph.v)]

            self.__permutation()

            self.r = [int(str(random.getrandbits(512)) + str(self._encode_colors[self.__fileColor._colors[key]]))
                      for key in self.__fileColor._colors]

            self.z = [exp_mod(self.r[i], self.keys_d[i], self.n[i])
                      for i in range(self.__fileGraph.v)]

            bob = Bob(edges=self.__fileGraph.edges,
                      n=self.n, keys_d=self.keys_d, z=self.z)
            random_edge = bob.random_egde()

            c_key1, c_key2 = self.__get_two_key_c(random_edge)
            if bob.check(c_key1=c_key1, c_key2=c_key2) is False:
                return False
        return True

    def __get_two_key_c(self, edge: list) -> List[list]:
        return [self.__keys_c[int(edge[0])-1], self.__keys_c[int(edge[1])-1]]

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


class Bob:
    def __init__(self, edges: List[list], n: list, keys_d: list, z: list) -> None:
        self.edges = edges
        self.n = n
        self.d = keys_d
        self.z = z
        self.curr_edge = None

    def random_egde(self) -> list:
        index_random_edge = random.randint(
            0, len(self.edges)-1)
        self.curr_edge = self.edges[index_random_edge]
        return self.edges[index_random_edge]

    def __get_z_two_vertex(self, edge: list) -> List[list]:
        return [self.z[int(edge[0])-1], self.z[int(edge[1])-1]]

    def __get_n_two_vertex(self, edge: list) -> List[list]:
        return [self.n[int(edge[0])-1], self.n[int(edge[1])-1]]

    def check(self, c_key1: int, c_key2: int) -> bool:
        z1, z2 = self.__get_z_two_vertex(self.curr_edge)
        n1, n2 = self.__get_n_two_vertex(self.curr_edge)
        a = exp_mod(z1, c_key1, n1)
        b = exp_mod(z2, c_key2, n2)
        if str(a)[-2:] == str(b)[-2:]:
            return False
        return True
