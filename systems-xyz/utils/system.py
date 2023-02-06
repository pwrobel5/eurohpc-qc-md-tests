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
    def __init__(self, cell_vectors: npt.ArrayLike, atoms: list[Atom], commentary: str='') -> System:
        length = cell_vectors.shape[0]
        if length == 1:
            self._cell_vectors = np.array([cell_vectors[0], cell_vectors[0], cell_vectors[0]])
        elif length == 2:
            self._cell_vectors = np.array([*cell_vectors, 0.0])
        else:
            self._cell_vectors = cell_vectors
        self._atoms = atoms
        self._commentary = commentary.strip()
    
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
    
    def center_at_position(self, center_index: int) -> System:
        center_position = self._atoms[center_index].coordinates
        moving_vector = -1.0 * center_position
        centered_atoms = [x.move_by_vector(moving_vector) for x in self._atoms]
        return System(self._cell_vectors, centered_atoms, self._commentary)
    
    def place_atoms_at_x_axis(self, pair_indices: list[int]) -> System:
        new_x_vector = self._atoms[pair_indices[1]].coordinates - self._atoms[pair_indices[0]].coordinates
        angle = np.arctan2(new_x_vector[1], new_x_vector[0])  # using atan2 to obtain the correct orientation
        rotated_atoms = [x.rotate_by_angle(angle) for x in self._atoms]
        return System(self._cell_vectors, rotated_atoms, self._commentary)
    
    def __str__(self) -> str:
        lines = []
        lines.append('{}'.format(len(self._atoms)))
        if len(self._commentary) > 0:
            lines.append(self._commentary)
        else:
            lines.append('cell {:6.3f} {:6.3f} {:6.3f}'.format(self._cell_vectors[0], self._cell_vectors[1], self._cell_vectors[2]))
        lines.extend([str(x) for x in self._atoms])
        return '\n'.join(lines)
    
    @property
    def cell_vectors(self) -> npt.ArrayLike:
        return self._cell_vectors

    @property
    def periodic(self) -> bool:
        return self._cell_vectors.size != 0
    
    @property
    def atoms_number(self) -> int:
        return len(self._atoms)
    
    @property
    def atoms(self) -> list[Atom]:
        return self._atoms
    
    @property
    def commentary(self) -> str:
        return self._commentary
    
    @property
    def atom_unique_types(self) -> list[str]:
        types_set = set()
        for atom in self._atoms:
            types_set.add(atom.symbol)
        
        return list(types_set)
