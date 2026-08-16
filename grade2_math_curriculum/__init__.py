"""Second Grade Math master course (grade 2)."""
from curriculum_kit import polish_unit

from .units_1_4 import build_unit1, build_unit2, build_unit3, build_unit4
from .units_5_8 import build_unit5, build_unit6, build_unit7, build_unit8, build_master


def all_units():
    return [polish_unit(*u) for u in (
        build_unit1(),
        build_unit2(),
        build_unit3(),
        build_unit4(),
        build_unit5(),
        build_unit6(),
        build_unit7(),
        build_unit8(),
    )]
