from abc import abstractmethod, ABC
from typing import List


class RsaSystem(ABC):

    @abstractmethod
    def generate_c_number(self, f: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def eval_d_number(self, c: int, f: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def generate_p_q(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def eval_n(self, p: int, q: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def eval_f(self, p: int, q: int) -> int:
        raise NotImplementedError
