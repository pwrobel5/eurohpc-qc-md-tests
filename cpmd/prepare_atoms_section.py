import collections
import sys

class PseudopotentialInfo():
    def __init__(self, file_name, l_max):
        self._file_name = file_name
        self._l_max = l_max
    
    def __str__(self):
        return ' *{}\n  LMAX={}\n'.format(self._file_name, self._l_max)

ATOM_PSEUDOPOTENTIALS = {
    'H':  PseudopotentialInfo('H-GTH-BLYP.psp', 'S'),
    'Li': PseudopotentialInfo('Li-GTH-BLYP.psp', 'S'),
    'C':  PseudopotentialInfo('C-GTH-BLYP.psp', 'P'),
    'O':  PseudopotentialInfo('O-GTH-BLYP.psp', 'P'),
    'Na': PseudopotentialInfo('Na-GTH-BLYP.psp', 'S')
}

if len(sys.argv) != 2:
    print('Incorrect number of initial arguments!')
    exit(1)

input_file_name = sys.argv[1]
input_file = open(input_file_name, 'r')
atom_coordinates = collections.defaultdict(list)

atoms_number = int(input_file.readline())
input_file.readline()  # omit commentary line

for line in input_file:
    splitted = line.strip().split()
    atom_symbol = splitted[0]
    coordinates = list(map(float, splitted[1:]))
    atom_coordinates[atom_symbol].append(coordinates)

input_file.close()

output_file = open('{}_atoms_section.txt'.format(input_file_name.split('.')[0]), 'w')
output_file.write('&ATOMS\n')

for atom, coordinates_list in atom_coordinates.items():
    pseudopotential = ATOM_PSEUDOPOTENTIALS[atom]
    output_file.write(str(pseudopotential))
    output_file.write('  {}\n'.format(len(coordinates_list)))

    for position in coordinates_list:
        output_file.write('  {:15.10f} {:15.10f} {:15.10f}\n'.format(position[0], position[1], position[2]))

    output_file.write('\n')

output_file.write('&END')
output_file.close()