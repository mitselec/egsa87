"""egsa87 - Convert geodetic coordinates between WGS84 and the HGRS87 (EGSA87/ΕΓΣΑ87) Greek geodetic system.

The two conversion functions work with radians (matching the original Matlab
implementation):

    from egsa87 import wgs84egsa87, egsa87wgs84

    x, y = wgs84egsa87(phi, lambda)      # WGS84 -> EGSA87 (meters)
    phi, lambda = egsa87wgs84(x, y)      # EGSA87 -> WGS84 (radians)

A command-line interface accepting degrees is also provided:

    egsa87 to-egsa87 --lat 38.5 --lon 23.5
    egsa87 to-wgs84 --x 500000 --y 4000000

See https://en.wikipedia.org/wiki/Hellenic_Geodetic_Reference_System_1987
"""

from .egsa87wgs84 import egsa87wgs84
from .wgs84egsa87 import wgs84egsa87

__all__ = ["wgs84egsa87", "egsa87wgs84"]
__version__ = "1.2.0"
