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
    
    def rotate_by_angle(self, angle: float) -> Atom:
        # rotation of coordination system is made counter-clockwise by a given angle
        # thus rotation of vector coordinates is clockwise
        rotation_matrix = np.array([[ np.cos(angle), np.sin(angle), 0.0],
                                    [-np.sin(angle), np.cos(angle), 0.0],
                                    [           0.0,           0.0, 1.0]])
        new_coordinates = rotation_matrix @ self._coordinates
        return Atom(self._symbol, new_coordinates)
    
    @property
    def coordinates(self) -> npt.ArrayLike:
        return np.copy(self._coordinates)
    
    @property
    def symbol(self) -> str:
        return self._symbol
    
    def __str__(self) -> str:
        return '{} {:12.8f} {:12.8f} {:12.8f}'.format(self._symbol, *self._coordinates)