from .atom import *
from .system import *


def read_system_from_xyz(input_file_path: str, cell_vector: list=[], include_commentary: bool=False) -> System:
    with open(input_file_path, 'r') as input_file:
        atoms_number = int(input_file.readline())
        commentary = input_file.readline()
        if not include_commentary:
            commentary = ''
        atoms_list = []
        for _ in range(atoms_number):
            line = input_file.readline().split()
            current_atom = Atom(line[0], np.array([float(line[1]), float(line[2]), float(line[3])]))
            atoms_list.append(current_atom)

    return System(np.array(cell_vector), atoms_list, commentary)