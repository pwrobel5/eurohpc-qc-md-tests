This directory contains some scripts used for preparation of geometries.

Input files for NAMD (.psf and .pdb files) were prepared using [PSF/PDB builder](https://github.com/pwrobel5/psf-pdb-builder-python).

## standarize_cell.py 

Script for standarizing cell, i.e. setting the origin of coordinate system at the position of given atom, and setting the x axis direction along a chosen interatomic distance.

Usage:
```
python3 standarize_cell.py input [parameters]
```

Available parameters:
* `-c index` or `--center-index index` - index of the atom at which the origin of the coordinate system is set, default 0
* `-p index1 index2` or `--pair-indices index1 index2` - indices of two atoms which will set the direction of x axis, default 0, 1
* `-o name` or `--output-name name` - name of the output file, default output.xyz

## extend_cell.py

Script for extendion of given system along a specified axis.

Usage:
```
python3 extend_cell.py input [parameters]
```

Available parameters:
* `-d [xyz]+` or `--directions [xyz]+` - directions along which the cell should be multiplied, default xyz
* `-c vectors+` or `--cell vectors+` - cell vector(s), for cubic cell only one value is necessary
* `-n number` or `--times number` - how many times the cell should be extended, default 1
* `-o name` or `--output-name name` - name of the output file, default output.xyz

## xyz2gen.py

Script for conversion of .xyz file to .gen file used in DFTB+.

Usage:
```
python3 xyz2gen.py input [parameters]
```

Available parameters:
* `-c vectors+` or `--cell-vectors vectors+` - length(s) of the cell vector(s), if not set, the system is treated as non-periodic (default value)
* `-o name` or `--output-name name` - name of the output name, default output.gen