import argparse
from utils import System, Atom

import numpy as np

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
        current_atom = Atom(line[0], np.array([float(line[1]), float(line[2]), float(line[3])]))
        atoms_list.append(current_atom)

atomic_system = System(np.array(cell_vector), atoms_list)
for direction in directions:
    atomic_system = atomic_system.multiple_in_direction(direction, times)

with open(output_file_name, 'w') as output_file:
    output_file.write(str(atomic_system))
