import pytest

from egsa87 import gui

# Morosini Fountain, Heraklion - the reference point used by the C test.
MOROSINI = (35.3391370, 25.1331727)
MOROSINI_XY = (602829.163609, 3910953.455740)


def test_convert_forward():
    x, y = gui.convert(gui.MODES[0], *MOROSINI)
    assert abs(x - MOROSINI_XY[0]) < 1e-2
    assert abs(y - MOROSINI_XY[1]) < 1e-2


def test_convert_inverse_roundtrip():
    x, y = gui.convert(gui.MODES[0], *MOROSINI)
    lat, lon = gui.convert(gui.MODES[1], x, y)
    assert abs(lat - MOROSINI[0]) < 1e-6
    assert abs(lon - MOROSINI[1]) < 1e-6


def test_convert_accepts_decimal_comma():
    x_dot, y_dot = gui.convert(gui.MODES[0], "35.3391370", "25.1331727")
    x_comma, y_comma = gui.convert(gui.MODES[0], "35,3391370", "25,1331727")
    assert abs(x_dot - x_comma) < 1e-9
    assert abs(y_dot - y_comma) < 1e-9


def test_convert_rejects_non_numeric():
    with pytest.raises(ValueError):
        gui.convert(gui.MODES[0], "abc", "23.5")
    with pytest.raises(ValueError):
        gui.convert(gui.MODES[1], "", "")


def test_gui_app_builds_and_converts():
    tkinter = pytest.importorskip("tkinter")
    try:
        root = tkinter.Tk()
    except tkinter.TclError:  # headless environment (e.g. CI without X)
        pytest.skip("no display available")
    root.withdraw()

    try:
        _root, app = gui.build_app(root)
        app.first_var.set("38.5")
        app.second_var.set("23.5")
        app._on_convert()
        assert app.result_var.get().startswith("X =")
        assert app._last_result is not None
    finally:
        root.destroy()
