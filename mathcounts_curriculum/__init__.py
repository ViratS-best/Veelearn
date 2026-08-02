"""MathCounts / AMC deep curriculum package."""

from .units_deep import build_unit1, build_master
from .units_rest import build_unit2
from .units_more import (
    build_unit3,
    build_unit4,
    build_unit5,
    build_unit6,
    build_unit7,
    build_unit8,
)


def all_units():
    return [
        build_unit1(),
        build_unit2(),
        build_unit3(),
        build_unit4(),
        build_unit5(),
        build_unit6(),
        build_unit7(),
        build_unit8(),
    ]
