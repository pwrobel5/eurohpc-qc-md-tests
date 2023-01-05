from __future__ import annotations

import numpy as np
import numpy.typing as npt


class Atom:
    def __init__(self, symbol: str, coordinates: npt.ArrayLike) -> Atom:
        self._symbol = symbol
        self._coordinates = coordinates
    
    def move_by_vector(self, move_vector: npt.ArrayLike) -> Atom:
        new_coordinates = self._coordinates + move_vector
        moved_atom = Atom(self._symbol, new_coordinates)
        return moved_atom
    
    def __str__(self) -> str:
        return '{} {} {} {}'.format(self._symbol, *self._coordinates)