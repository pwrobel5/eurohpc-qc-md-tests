import numpy as np
import argparse

from utils import Atom

parser = argparse.ArgumentParser(description='Center coordinates at the position of given atom, rotate to have X axis at desired direction')

parser.add_argument('input', metavar='input', type=str, help='Path to input .xyz file')
parser.add_argument('-c', '--center-index', type=int, default=0, help='index of atom which has to be at the (0, 0, 0) point (default 0)')
parser.add_argument('-p', '--pair-indices', type=int, nargs=2, default=[0, 1], help='Indices of atoms which should lay on the x axis (default 0, 1)')
parser.add_argument('-o', '--output-name', type=str, default='output.xyz', help='Name of the output file (default output.xyz)')

args = parser.parse_args()
input_file_path = args.input
center_index = args.center_index
pair_indices = args.pair_indices
output_file_name = args.output_name

atoms_list = []
with open(input_file_path, 'r') as input_file:
    atoms_number = int(input_file.readline())
    commentary = input_file.readline()
    
    for _ in range(atoms_number):
        line = input_file.readline().split()
        atoms_list.append(Atom(line[0], np.array([float(line[1]), float(line[2]), float(line[3])])))

center_position = atoms_list[center_index].coordinates
moving_vector = -1.0 * center_position
centered_atoms = [x.move_by_vector(moving_vector) for x in atoms_list]

current_x_vector = np.array([1.0, 0.0, 0.0])
new_x_vector = centered_atoms[pair_indices[1]].coordinates - centered_atoms[pair_indices[0]].coordinates
new_x_vector[-1] = 0.0  # make the z coordinate equal 0, as here only rotation in xy plane is considered
vector_product = current_x_vector @ new_x_vector
angle = np.arccos(vector_product / np.linalg.norm(new_x_vector))  # divide only by norm of the second vector as the first is equal 1
rotated_atoms = [x.rotate_by_angle(angle) for x in centered_atoms]

with open(output_file_name, 'w') as output_file:
    output_file.write('{}\n'.format(atoms_number))
    output_file.write(commentary)
    output_file.writelines('\n'.join([str(a) for a in rotated_atoms]))
