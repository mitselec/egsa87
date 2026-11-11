# egsa87

[![CI](https://github.com/mitselec/egsa87/actions/workflows/ci.yml/badge.svg)](https://github.com/mitselec/egsa87/actions/workflows/ci.yml)
[![License: GPL v2](https://img.shields.io/badge/License-GPLv2-blue.svg)](LICENSE)

Functions to convert geodetic coordinates from the [World Geodetic System](https://en.wikipedia.org/wiki/World_Geodetic_System) 1984 (**WGS84**) to the [Hellenic Geodetic Reference System 1987](https://en.wikipedia.org/wiki/Hellenic_Geodetic_Reference_System_1987) (**HGRS87/EGSA87**) Greek geodetic system and vice versa.

Implementations are provided in three languages: Python (installable package with CLI and GUI), C (C99 port), and Matlab (the original implementation).

## Project layout

```
.
├── src/egsa87/          # Python package (see note below)
│   ├── wgs84egsa87.py   #   WGS84 -> EGSA87 conversion function
│   ├── egsa87wgs84.py   #   EGSA87 -> WGS84 conversion function
│   ├── cli.py           #   egsa87 command-line tool
│   ├── gui.py           #   egsa87-gui Tkinter desktop GUI
│   └── __init__.py      #   public API: from egsa87 import ...
├── tests/               # Python test suite (pytest)
├── C/                   # C99 port of the Matlab routines + test program
├── Matlab/              # original Matlab implementation
├── pyproject.toml       # Python packaging metadata (pip install .)
├── Makefile             # C build: make build / test-c / clean
├── CMakeLists.txt       # alternative CMake build for the C port
└── .github/workflows/   # CI: runs the Python tests and builds the C port
```

A note on the `src/` directory: it follows the modern Python *src layout* convention. `src/` itself contains no code — the package is `src/egsa87/`, and after `pip install .` you simply `import egsa87`. The indirection keeps the importable package from being picked up accidentally from the working directory, so tests always exercise the installed code. All other directories are named after the language they contain.

This repository is the maintained continuation of the original [mlourakis/egsa87](https://github.com/mlourakis/egsa87) project. The Python port was contributed by [Dimitrios Dimopoulos](https://github.com/mitselec) in [upstream PR #1](https://github.com/mlourakis/egsa87/pull/1), who also maintains this fork.

Code is based on the [icoordstrans](https://github.com/skozan/icoordstrans) library.
For an overview of spatial referencing, see [this.](https://unstats.un.org/Unsd/geoinfo/UNGEGN/docs/_data_ICAcourses/_HtmlModules/_Documents/D06/documents/D06-03_KnippersPPTeaching.pdf)

## Python

### Installation

```sh
pip install .
```

This installs the `egsa87` package and the `egsa87` command-line tool.

### Command-line usage

By default, geodetic coordinates are given in degrees and returned in degrees:

```sh
$ egsa87 to-egsa87 --lat 38.5 --lon 23.5
475859.572 4261163.141

$ egsa87 to-wgs84 --x 475859.572 --y 4261163.141
38.500000000 23.500000000
```

Use `--radians` to work in radians (matching the library API) and `--json` for machine-readable output. The module can also be run directly with `python -m egsa87`.

### GUI

A minimal desktop GUI built with Tkinter is included. After installing the package, run:

```sh
egsa87-gui
```

or equivalently `python -m egsa87.gui`. Pick the conversion direction, enter the two values (a decimal comma is accepted as well as a decimal point), press **Convert**, and copy the result if needed. On Linux, tkinter requires the `python3-tk` package (`sudo apt install python3-tk`); on Windows and macOS it ships with Python.

### Library usage

Both functions expect/return angles in radians and planar coordinates in meters:

```python
import math
from egsa87 import wgs84egsa87, egsa87wgs84

x, y = wgs84egsa87(math.radians(38.5), math.radians(23.5))   # WGS84 -> EGSA87
phi, lam = egsa87wgs84(x, y)                                 # EGSA87 -> WGS84
```

## C

```sh
make build          # builds build/egsa87_test
make test-c         # runs the test program
```

or with CMake:

```sh
cmake -S . -B build-cmake
cmake --build build-cmake
./build-cmake/egsa87_test
```

or directly:

```sh
gcc -O2 -Wall -std=c99 -o egsa87_test C/egsa87.c C/egsa87_test.c -lm && ./egsa87_test
```

To use in your own program, include `C/egsa87.h` and compile `C/egsa87.c` with it:

```c
double philam[2] = { phi_rad, lambda_rad };   // WGS84 geodetic coordinates
double xy[2];
wgs84egsa87(philam, xy);                     // EGSA87 planar coordinates (meters)

double philam2[2];
egsa87wgs84(xy, philam2);                    // back to WGS84 geodetic coordinates
```

## Matlab

Copy the `Matlab/` files to your path and call:

```matlab
[x, y] = wgs84egsa87(phi, lambda);   % WGS84 -> EGSA87
[phi, lambda] = egsa87wgs84(x, y);   % EGSA87 -> WGS84
```

## Testing

```sh
pip install -e ".[dev]"
pytest            # Python tests (validated against EPSG:2100 via pyproj when available)
make test-c       # C test program
```

The Python round-trip tests verify conversions to well under a centimeter; cross-checks against the official EPSG:2100 (GGRS87/Greek Grid) definition agree to within ~1 m due to slightly different datum shift models.

## Disclaimer

Use these conversion functions at your own risk. No warranties are made regarding the accuracy and reliability of the provided code.

## License

This project is licensed under the [GNU General Public License v2.0](LICENSE).

### Funding

_Development has received funding from the European Union’s Horizon 2020 Research and Innovation program under grant agreement No 826506 -- [sustAGE](https://www.sustage.eu/)._
