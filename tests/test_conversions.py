import json
import math
import subprocess
import sys

import pytest

from egsa87.egsa87wgs84 import egsa87wgs84
from egsa87.wgs84egsa87 import wgs84egsa87

# Sample points spread across Greece, including Athens city centre and the
# Morosini Fountain in Heraklion (the reference point used by the C test).
SAMPLE_POINTS = [
    (41.007, 20.513),  # near Kastoria
    (40.640, 22.944),  # Thessaloniki
    (39.074, 21.824),  # central Greece
    (37.976, 23.734),  # Athens (Syntagma)
    (36.891, 27.288),  # Kos
    (35.3391370, 25.1331727),  # Heraklion (Morosini Fountain)
]

# HGRS87/EGSA87 corresponds to EPSG:2100 (GGRS87 / Greek Grid). The two
# implementations use slightly different datum models (a simple 3-parameter
# geocentric translation vs PROJ's more refined handling), so ~1 m
# differences are expected. Round-trip consistency is far tighter.


def test_roundtrip_wgs84_egsa87_wgs84():
    for lat, lon in SAMPLE_POINTS:
        phi, lam = math.radians(lat), math.radians(lon)
        x, y = wgs84egsa87(phi, lam)
        phi2, lam2 = egsa87wgs84(x, y)
        assert abs(phi2 - phi) < 1e-8
        assert abs(lam2 - lam) < 1e-8


def test_roundtrip_egsa87_wgs84_egsa87():
    for lat, lon in SAMPLE_POINTS:
        x, y = wgs84egsa87(math.radians(lat), math.radians(lon))
        x2, y2 = wgs84egsa87(*egsa87wgs84(x, y))
        assert abs(x2 - x) < 0.05
        assert abs(y2 - y) < 0.05


def test_forward_against_epsg2100():
    pyproj = pytest.importorskip("pyproj")
    transformer = pyproj.Transformer.from_crs(
        "EPSG:4326", "EPSG:2100", always_xy=True
    )
    for lat, lon in SAMPLE_POINTS:
        x, y = wgs84egsa87(math.radians(lat), math.radians(lon))
        expected_x, expected_y = transformer.transform(lon, lat)
        assert math.hypot(x - expected_x, y - expected_y) < 2.0


def test_inverse_against_epsg2100():
    pyproj = pytest.importorskip("pyproj")
    transformer = pyproj.Transformer.from_crs("EPSG:2100", "EPSG:4326", always_xy=True)
    geod = pyproj.Geod(ellps="WGS84")
    for lat, lon in SAMPLE_POINTS:
        x, y = wgs84egsa87(math.radians(lat), math.radians(lon))
        phi, lam = egsa87wgs84(x, y)
        ref_lon, ref_lat = transformer.transform(x, y)
        _, _, dist = geod.inv(ref_lon, ref_lat, math.degrees(lam), math.degrees(phi))
        assert dist < 2.0


def _run_cli(*argv):
    return subprocess.run(
        [sys.executable, "-m", "egsa87", *argv],
        capture_output=True,
        text=True,
        check=True,
    )


def test_cli_to_egsa87_matches_library():
    out = _run_cli("to-egsa87", "--lat", "38.5", "--lon", "23.5").stdout
    x, y = (float(v) for v in out.split())
    xi, yi = wgs84egsa87(math.radians(38.5), math.radians(23.5))
    assert abs(x - xi) < 1e-3
    assert abs(y - yi) < 1e-3


def test_cli_json_roundtrip():
    data = json.loads(_run_cli("to-egsa87", "--lat", "38.5", "--lon", "23.5", "--json").stdout)
    out = _run_cli("to-wgs84", "--x", str(data["x"]), "--y", str(data["y"]), "--json").stdout
    back = json.loads(out)
    assert abs(back["latitude"] - 38.5) < 1e-6
    assert abs(back["longitude"] - 23.5) < 1e-6
