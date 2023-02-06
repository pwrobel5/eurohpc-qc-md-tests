import argparse

from utils import read_system_from_xyz

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

atom_system = read_system_from_xyz(input_file_path, include_commentary=True)
centered_system = atom_system.center_at_position(center_index)
rotated_system = centered_system.place_atoms_at_x_axis(pair_indices)

with open(output_file_name, 'w') as output_file:
    output_file.write(str(rotated_system))
