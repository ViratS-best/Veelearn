import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manimlib import *

from lesson import LessonScene
from units_1_2 import U1, U2
from units_3_4 import U3, U4
from units_5_6 import U5, U6
from units_7_8 import U7, U8


def bind(meta, class_name):
    class Bound(LessonScene):
        unit_num = meta["num"]
        unit_title = meta["title"]
        subtitle = meta["subtitle"]
        parts = meta["parts"]
    Bound.__name__ = class_name
    Bound.__qualname__ = class_name
    return Bound


Unit1Exponents = bind(U1, "Unit1Exponents")
Unit2Equations = bind(U2, "Unit2Equations")
Unit3Slope = bind(U3, "Unit3Slope")
Unit4Functions = bind(U4, "Unit4Functions")
Unit5Substitution = bind(U5, "Unit5Substitution")
Unit6Elimination = bind(U6, "Unit6Elimination")
Unit7Pythagoras = bind(U7, "Unit7Pythagoras")
Unit8Data = bind(U8, "Unit8Data")

SCENES = [
    (Unit1Exponents, U1["file"]),
    (Unit2Equations, U2["file"]),
    (Unit3Slope, U3["file"]),
    (Unit4Functions, U4["file"]),
    (Unit5Substitution, U5["file"]),
    (Unit6Elimination, U6["file"]),
    (Unit7Pythagoras, U7["file"]),
    (Unit8Data, U8["file"]),
]
