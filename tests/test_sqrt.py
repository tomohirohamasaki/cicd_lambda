from pytest import approx
from math import sqrt
from my_package.math import newton_sqrt


def test_newton_sqrt():
    assert newton_sqrt(42) == approx(sqrt(42), abs=1e-6)
