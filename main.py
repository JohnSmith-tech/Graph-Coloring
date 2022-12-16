import random
from typing import List
from methods_for_crypro.methods import *
from sympy import isprime, randprime


def generate_c_number(f: int) -> int:
    c = 0
    while euclid_algorithm(c, f)[0] != 1:
        c = random.randrange(2, f)
    return c


def eval_d_number(c: int, f: int) -> int:
    return exp_mod(euclid_algorithm(c, f)[1], 1, f)


def generate_p_q(v: int) -> List[list]:
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


def eval_n(p: list, q: list) -> list:
    n = []
    for i in range(len(p)):
        n.append(p[i] + q[i])
    return n


def eval_f(p: list, q: list):
    f = []
    for i in range(len(p)):
        f.append((p[i]-1)*(q[i]-1))
    return f


def recolor_vertices(col: list, color: list):
    return True


def main() -> None:
    v = 10  # v - кол-во вершин
    color = [1, 2, 3]
    col = [1, 2, 3, 1, 2, 3, 1, 2, 1, 2]

    p_array, q_array = generate_p_q(v)
    n = eval_n(p_array, q_array)
    f = eval_f(p_array, q_array)

    keys_c = [generate_c_number(f[i]) for i in range(v)]
    keys_d = [eval_d_number(keys_c[i], f[i]) for i in range(v)]

    random.shuffle(color)

    print(color)

    r = [int(str(random.randint(2, 2**24)) + str(col[i])) % n[i]
         for i in range(v)]
    z = [exp_mod(r[i], keys_d[i], n[i]) for i in range(v)]


main()
