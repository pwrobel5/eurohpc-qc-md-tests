import argparse

from utils import read_system_from_xyz

parser = argparse.ArgumentParser(description='Convert xyz file to gen format used by DFTB+')

parser.add_argument('input', metavar='input', type=str, help='Path to input .xyz file')
parser.add_argument('-o', '--output-name', type=str, default='output.xyz', help='Name of the output file (default output.xyz)')
parser.add_argument('-c', '--cell-vectors', type=float, nargs='+', default=[], help='Cell vector(s) (default empty - non-periodic system)')

args = parser.parse_args()
input_file_path = args.input
output_file_name = args.output_name
cell_vectors = args.cell_vectors

xyz_system = read_system_from_xyz(input_file_path, cell_vector=cell_vectors, include_commentary=True)
is_periodic = xyz_system.periodic

with open(output_file_name, 'w') as output_file:
    output_file.write('{} '.format(xyz_system.atoms_number))
    if len(xyz_system.commentary) > 0:
        output_file.write('# {}\n'.format(xyz_system.commentary))
        
    if is_periodic:
        output_file.write('S\n')
    else:
        output_file.write('C\n')
    
    atom_types = xyz_system.atom_unique_types
    print(atom_types)
    output_file.write('{}\n'.format(' '.join(atom_types).strip()))
    
    atoms = xyz_system.atoms
    for index, atom in enumerate(atoms):
        atom_type_index = atom_types.index(atom.symbol) + 1  # as in .gen format the lowest index is 1 not 0
        coordinates_string = '{:12.8f} {:12.8f} {:12.8f}'.format(*atom.coordinates)
        output_file.write('{} {} {}\n'.format(index + 1, atom_type_index, coordinates_string))  # with index goes the same as above

    if is_periodic:
        cell_vectors = xyz_system.cell_vectors
        cell_centre_str = '{:12.8f} {:12.8f} {:12.8f}\n'.format(0.0, 0.0, 0.0)
        cell_vectors_format = 3 * '{:12.8f} {:12.8f} {:12.8f}\n'
        cell_vectors_str = cell_vectors_format.format(cell_vectors[0], 0.0, 0.0,
                                                      0.0, cell_vectors[1], 0.0,
                                                      0.0, 0.0, cell_vectors[2])
        output_file.write(cell_centre_str)
        output_file.write(cell_vectors_str)
