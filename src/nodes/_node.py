from abc import ABC
from typing import List

class Node(ABC):

    def __init__(self, required_keys: List[str] = None, max_iterations: int = 5) -> None:

        self._required_keys = required_keys

        self._num_iterations = 0
        self._max_iterations = max_iterations

    def _increment_iteration(self):
        self._num_iterations += 1
