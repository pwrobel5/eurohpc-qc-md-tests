from __future__ import annotations
from .atom import Atom

import numpy as np
import numpy.typing as npt

DIRECTION_TO_INDEX = {
    'x': 0,
    'y': 1,
    'z': 2
}


class System:
    def __init__(self, cell_vectors: npt.ArrayLike, atoms: list[Atom]) -> System:
        length = cell_vectors.shape[0]
        if length == 1:
            self._cell_vectors = np.array([cell_vectors[0], cell_vectors[0], cell_vectors[0]])
        elif length == 2:
            self._cell_vectors = np.array([*cell_vectors, 0.0])
        else:
            self._cell_vectors = cell_vectors
        self._atoms = atoms
    
    def multiple_in_direction(self, direction: str, times: int) -> System:
        index = DIRECTION_TO_INDEX[direction]
        moving_vector = np.zeros((3,))
        cell_period = self._cell_vectors[index]
        added_vector = np.zeros((3,))
        added_vector[index] = cell_period

        moved_atoms = []
        for _ in range(times):
            moving_vector += added_vector
            moved_atoms.extend([x.move_by_vector(moving_vector) for x in self._atoms])
        
        new_cell_vector = self._cell_vectors + moving_vector

        new_system = System(new_cell_vector, self._atoms + moved_atoms)
        return new_system
    
    def __str__(self) -> str:
        lines = []
        lines.append('{}'.format(len(self._atoms)))
        lines.append('cell {:6.3f} {:6.3f} {:6.3f}'.format(self._cell_vectors[0], self._cell_vectors[1], self._cell_vectors[2]))
        lines.extend([str(x) for x in self._atoms])
        return '\n'.join(lines)