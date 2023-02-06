import argparse
from utils import read_system_from_xyz

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

atomic_system = read_system_from_xyz(input_file_path, cell_vector)
for direction in directions:
    atomic_system = atomic_system.multiple_in_direction(direction, times)

with open(output_file_name, 'w') as output_file:
    output_file.write(str(atomic_system))
