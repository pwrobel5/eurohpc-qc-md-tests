from __future__ import annotations
import argparse


DIRECTION_TO_INDEX = {
    'x': 0,
    'y': 1,
    'z': 2
}

class Atom:
    def __init__(self, symbol: str, coordinates: list[float]) -> Atom:
        self._symbol = symbol
        self._coordinates = coordinates
    
    def move_by_vector(self, direction: str, value: float) -> Atom:
        index = DIRECTION_TO_INDEX[direction]
        new_coordinates = self._coordinates.copy()
        new_coordinates[index] += value
        moved_atom = Atom(self._symbol, new_coordinates)
        return moved_atom
    
    def __str__(self) -> str:
        return '{} {} {} {}'.format(self._symbol, *self._coordinates)


class System:
    def __init__(self, cell_vectors: list[float], atoms: list[Atom]) -> System:
        if len(cell_vectors) == 1:
            self._cell_vectors = 3 * cell_vectors
        elif len(cell_vectors) == 2:
            self._cell_vectors = cell_vectors + [0.0]
        else:
            self._cell_vectors = cell_vectors
        self._atoms = atoms
    
    def multiple_in_direction(self, direction: str, times: int) -> System:
        index = DIRECTION_TO_INDEX[direction]
        moving_vector = [0.0, 0.0, 0.0]
        cell_vector = self._cell_vectors[index]
        moved_atoms = []
        for _ in range(times):
            moving_vector[index] += cell_vector
            moved_atoms.extend([x.move_by_vector(direction, cell_vector) for x in self._atoms])
        
        modified_cell_vector = cell_vector * (times + 1)
        new_cell_vectors = self._cell_vectors.copy()
        new_cell_vectors[index] = modified_cell_vector

        new_system = System(new_cell_vectors, self._atoms + moved_atoms)
        return new_system
    
    def __str__(self) -> str:
        lines = []
        lines.append('{}'.format(len(self._atoms)))
        lines.append('cell {} {} {}'.format(self._cell_vectors[0], self._cell_vectors[1], self._cell_vectors[2]))
        lines.extend([str(x) for x in self._atoms])
        return '\n'.join(lines)

parser = argparse.ArgumentParser(description='Create .xyz file with extended cell along chosen vectors from basic .xyz file')

parser.add_argument('input', metavar='input', type=str, help='Path to input .xyz file')
parser.add_argument('-d', '--directions', type=str, default='xyz', help='Directions in which cell has to be extended (default xyz)')
parser.add_argument('-c', '--cell', type=float, nargs='+', default=[20.0], help='Cell vector(s) (default 20.0)')
parser.add_argument('-n', '--times', type=int, default=1, help='Times by which system should be extended (default 1)')
parser.add_argument('-o', '--output-name', type=str, default='output.xyz', help='Name of the output file (default output.xyz)')

args = parser.parse_args()
input_file_path = args.input
directions = list(args.directions)
cell_vector = args.cell
times = args.times
output_file_name = args.output_name

with open(input_file_path, 'r') as input_file:
    atoms_number = int(input_file.readline())
    input_file.readline()
    atoms_list = []
    for _ in range(atoms_number):
        line = input_file.readline().split()
        current_atom = Atom(line[0], [float(line[1]), float(line[2]), float(line[3])])
        atoms_list.append(current_atom)

atomic_system = System(cell_vector, atoms_list)
for direction in directions:
    atomic_system = atomic_system.multiple_in_direction(direction, times)

with open(output_file_name, 'w') as output_file:
    output_file.write(str(atomic_system))
