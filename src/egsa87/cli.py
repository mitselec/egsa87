"""Command-line interface for the egsa87 package.

Examples:
    egsa87 to-egsa87 --lat 38.5 --lon 23.5
    egsa87 to-egsa87 --lat 0.671952 --lon 0.410152 --radians --json
    egsa87 to-wgs84 --x 500000 --y 4000000
"""

import argparse
import json
import math
import sys

from .egsa87wgs84 import egsa87wgs84
from .wgs84egsa87 import wgs84egsa87


def _to_egsa87(args):
    """Convert WGS84 geodetic coordinates to EGSA87 planar coordinates."""
    phi, lambd = (
        (args.lat, args.lon)
        if args.radians
        else (math.radians(args.lat), math.radians(args.lon))
    )
    x, y = wgs84egsa87(phi, lambd)
    if args.json:
        print(json.dumps({"x": x, "y": y}))
    else:
        print(f"{x:.3f} {y:.3f}")


def _to_wgs84(args):
    """Convert EGSA87 planar coordinates to WGS84 geodetic coordinates."""
    phi, lambd = egsa87wgs84(args.x, args.y)
    if args.json:
        if args.radians:
            print(json.dumps({"latitude": phi, "longitude": lambd}))
        else:
            print(
                json.dumps(
                    {"latitude": math.degrees(phi), "longitude": math.degrees(lambd)}
                )
            )
    elif args.radians:
        print(f"{phi:.9f} {lambd:.9f}")
    else:
        print(f"{math.degrees(phi):.9f} {math.degrees(lambd):.9f}")


def build_parser():
    parser = argparse.ArgumentParser(
        prog="egsa87",
        description=(
            "Convert geodetic coordinates between WGS84 and the HGRS87 "
            "(EGSA87/ΕΓΣΑ87) Greek geodetic system."
        ),
        epilog=(
            "examples:\n"
            "  egsa87 to-egsa87 --lat 38.5 --lon 23.5\n"
            "  egsa87 to-wgs84 --x 500000 --y 4000000\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_forward = subparsers.add_parser(
        "to-egsa87", help="convert WGS84 latitude/longitude to EGSA87 x/y"
    )
    p_forward.add_argument("--lat", required=True, type=float, help="WGS84 latitude")
    p_forward.add_argument("--lon", required=True, type=float, help="WGS84 longitude")
    p_forward.add_argument(
        "--radians",
        action="store_true",
        help="interpret latitude/longitude as radians instead of degrees",
    )
    p_forward.add_argument(
        "--json", action="store_true", help="print output as a JSON object"
    )
    p_forward.set_defaults(func=_to_egsa87)

    p_inverse = subparsers.add_parser(
        "to-wgs84", help="convert EGSA87 x/y to WGS84 latitude/longitude"
    )
    p_inverse.add_argument("--x", required=True, type=float, help="EGSA87 x (meters)")
    p_inverse.add_argument("--y", required=True, type=float, help="EGSA87 y (meters)")
    p_inverse.add_argument(
        "--radians",
        action="store_true",
        help="print latitude/longitude in radians instead of degrees",
    )
    p_inverse.add_argument(
        "--json", action="store_true", help="print output as a JSON object"
    )
    p_inverse.set_defaults(func=_to_wgs84)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
