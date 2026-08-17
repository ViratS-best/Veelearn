"""Deep Geometry curriculum builders — Units 5–8."""
from __future__ import annotations

from curriculum_kit import lesson_figure, svg_plane, svg_circle, svg_triangle, svg_rect

from hs_curriculum import (
    concept_block, solved, mq, xy_graph, sample_curve, number_line,
    labeled_right_triangle, unit_circle_svg, parallel_lines_transversal,
    tangent_curve_svg, practice_slots, unit_shell, fill_qs, page_break,
)
from .common import AUDIENCE, STRETCH_LABEL
from .units_1_4 import _pack, _prop_svg


def _para_svg():
    return (
        '<svg viewBox="0 0 280 150" width="100%" style="max-width:280px" role="img">'
        '<polygon points="50,120 210,120 240,40 80,40" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<line x1="50" y1="120" x2="240" y2="40" stroke="#94a3b8" stroke-dasharray="4 3"/>'
        '<line x1="210" y1="120" x2="80" y2="40" stroke="#94a3b8" stroke-dasharray="4 3"/>'
        '<text x="40" y="132">A</text><text x="214" y="136">B</text>'
        '<text x="246" y="38">C</text><text x="68" y="36">D</text>'
        "</svg>"
    )


def _trap_svg():
    return (
        '<svg viewBox="0 0 280 140" width="100%" style="max-width:280px" role="img">'
        '<polygon points="40,110 240,110 190,40 90,40" fill="#fef3c7" stroke="#92400e" stroke-width="2"/>'
        '<line x1="40" y1="110" x2="240" y2="110" stroke="#b91c1c" stroke-width="3"/>'
        '<line x1="90" y1="40" x2="190" y2="40" stroke="#b91c1c" stroke-width="3"/>'
        '<text x="140" y="128" text-anchor="middle" font-size="12">bases</text>'
        "</svg>"
    )


def _kite_svg():
    return (
        '<svg viewBox="0 0 220 200" width="100%" style="max-width:220px" role="img">'
        '<polygon points="110,20 180,90 110,180 40,90" fill="#dcfce7" stroke="#166534" stroke-width="2"/>'
        '<line x1="110" y1="20" x2="110" y2="180" stroke="#b91c1c" stroke-width="2"/>'
        '<line x1="40" y1="90" x2="180" y2="90" stroke="#2563eb" stroke-width="2"/>'
        '<text x="118" y="16" font-size="12">A</text>'
        "</svg>"
    )


def _elev_svg():
    return (
        '<svg viewBox="0 0 300 170" width="100%" style="max-width:300px" role="img">'
        '<line x1="20" y1="140" x2="280" y2="140" stroke="#0f172a" stroke-width="2"/>'
        '<rect x="40" y="118" width="16" height="22" fill="#1d4ed8"/>'
        '<line x1="48" y1="118" x2="240" y2="40" stroke="#b91c1c" stroke-width="2"/>'
        '<rect x="228" y="40" width="18" height="100" fill="#64748b"/>'
        '<path d="M 70 118 A 28 28 0 0 0 62 100" fill="none" stroke="#d97706" stroke-width="2"/>'
        '<text x="78" y="108" font-size="12" fill="#b45309">θ elev.</text>'
        "</svg>"
    )


def _inscribed_svg():
    # Center (120,110), r=80. A and B at 150°/30°; inscribed vertex C at the bottom of the circle.
    return (
        '<svg viewBox="0 0 240 230" width="100%" style="max-width:240px" role="img">'
        '<circle cx="120" cy="110" r="80" fill="#eef2ff" stroke="#312e81" stroke-width="2"/>'
        '<line x1="120" y1="110" x2="50.7" y2="70" stroke="#94a3b8"/>'
        '<line x1="120" y1="110" x2="189.3" y2="70" stroke="#94a3b8"/>'
        '<polygon points="50.7,70 189.3,70 120,190" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        '<circle cx="120" cy="110" r="4" fill="#111"/>'
        '<circle cx="120" cy="190" r="4" fill="#b91c1c"/>'
        '<text x="124" y="104" font-size="12">O</text>'
        '<text x="112" y="214" font-size="12" fill="#b91c1c">C (on circle)</text>'
        "</svg>"
    )


def _tangent_circ_svg():
    # O(110,110), r=70, P=(166,68) is 56 right and 42 up on the circle (4-3-5×14).
    # OP=(56,-42); a perpendicular direction is (42,56). Tangent through P.
    return (
        '<svg viewBox="0 0 260 200" width="100%" style="max-width:260px" role="img">'
        '<circle cx="110" cy="110" r="70" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>'
        '<line x1="118" y1="4" x2="214" y2="132" stroke="#b91c1c" stroke-width="2.4"/>'
        '<line x1="110" y1="110" x2="166" y2="68" stroke="#1d4ed8" stroke-width="2"/>'
        '<circle cx="166" cy="68" r="5" fill="#b91c1c"/>'
        '<rect x="160" y="62" width="12" height="12" fill="none" stroke="#0f172a" transform="rotate(-37 166 68)"/>'
        '<text x="176" y="62" font-size="12">P</text>'
        '<text x="96" y="108" font-size="12">O</text>'
        '<text x="200" y="108" font-size="12" fill="#b91c1c">tangent</text>'
        "</svg>"
    )


def _chord_svg():
    return (
        '<svg viewBox="0 0 240 220" width="100%" style="max-width:240px" role="img">'
        '<circle cx="120" cy="110" r="80" fill="#eef2ff" stroke="#312e81" stroke-width="2"/>'
        '<line x1="50.7" y1="150" x2="189.3" y2="150" stroke="#b91c1c" stroke-width="2.6"/>'
        '<line x1="120" y1="110" x2="120" y2="150" stroke="#1d4ed8" stroke-width="2" stroke-dasharray="4 3"/>'
        '<line x1="120" y1="110" x2="189.3" y2="150" stroke="#64748b" stroke-width="1.6"/>'
        '<rect x="120" y="138" width="12" height="12" fill="none" stroke="#0f172a"/>'
        '<circle cx="120" cy="110" r="4" fill="#111"/>'
        '<circle cx="120" cy="150" r="4" fill="#1d4ed8"/>'
        '<text x="126" y="104" font-size="12">O</text>'
        '<text x="126" y="168" font-size="12" fill="#1d4ed8">M</text>'
        '<text x="108" y="196" font-size="12" fill="#b91c1c">chord AB</text>'
        "</svg>"
    )


def _sector_svg():
    return (
        '<svg viewBox="0 0 220 200" width="100%" style="max-width:220px" role="img">'
        '<circle cx="110" cy="110" r="70" fill="#f8fafc" stroke="#0f172a" stroke-width="2"/>'
        '<path d="M 110 110 L 180 110 A 70 70 0 0 0 145 48 Z" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>'
        '<text x="150" y="88" font-size="12">60°</text>'
        '<text x="140" y="118" font-size="12" fill="#b91c1c">r</text>'
        "</svg>"
    )


def _prism_svg(lab="ℓ=5, w=3, h=4"):
    return (
        '<svg viewBox="0 0 200 160" width="100%" style="max-width:200px" role="img">'
        '<polygon points="40,70 130,70 160,40 70,40" fill="#c7d2fe" stroke="#312e81"/>'
        '<polygon points="40,70 40,130 130,130 130,70" fill="#a5b4fc" stroke="#312e81"/>'
        '<polygon points="130,70 160,40 160,100 130,130" fill="#818cf8" stroke="#312e81"/>'
        f'<text x="100" y="154" text-anchor="middle" font-size="12">{lab}</text></svg>'
    )


def _cyl_svg():
    return (
        '<svg viewBox="0 0 180 170" width="100%" style="max-width:180px" role="img">'
        '<ellipse cx="90" cy="40" rx="50" ry="16" fill="#bfdbfe" stroke="#1e3a8a"/>'
        '<line x1="40" y1="40" x2="40" y2="120" stroke="#1e3a8a" stroke-width="2"/>'
        '<line x1="140" y1="40" x2="140" y2="120" stroke="#1e3a8a" stroke-width="2"/>'
        '<ellipse cx="90" cy="120" rx="50" ry="16" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="90" y="88" text-anchor="middle" font-size="12">h</text>'
        '<text x="90" y="36" text-anchor="middle" font-size="12">r</text>'
        "</svg>"
    )


def _cone_svg():
    return (
        '<svg viewBox="0 0 180 170" width="100%" style="max-width:180px" role="img">'
        '<polygon points="90,20 30,130 150,130" fill="#fde68a" stroke="#92400e" stroke-width="2"/>'
        '<ellipse cx="90" cy="130" rx="60" ry="16" fill="#fcd34d" stroke="#92400e"/>'
        '<line x1="90" y1="20" x2="90" y2="130" stroke="#b91c1c" stroke-dasharray="4 3"/>'
        '<text x="100" y="80" font-size="12" fill="#b91c1c">h</text>'
        "</svg>"
    )


def _sphere_svg():
    return (
        '<svg viewBox="0 0 180 180" width="100%" style="max-width:180px" role="img">'
        '<circle cx="90" cy="90" r="70" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>'
        '<ellipse cx="90" cy="90" rx="70" ry="24" fill="none" stroke="#64748b"/>'
        '<line x1="90" y1="90" x2="160" y2="90" stroke="#b91c1c" stroke-width="2"/>'
        '<text x="118" y="84" font-size="12" fill="#b91c1c">r</text>'
        "</svg>"
    )


def _coord_poly_svg():
    return (
        svg_plane(points=[(0, 0, "A"), (6, 0, "B"), (6, 4, "C"), (0, 4, "D")], lim=7,
                  line=(0, 0, 6, 0))
    )


# ===========================================================================
# UNIT 5
# ===========================================================================

def _u5_questions():
    rows = [
        ("In a right triangle with legs 6 and 8, the hypotenuse is…",
         10, "6²+8²=36+64=100, hypotenuse 10. A scaled 3-4-5.",
         [14, 7, 48]),
        ("A triangle has sides 5, 12, and 13. It is…",
         "right", "5²+12²=25+144=169=13², so the converse of Pythagoras says it is right.",
         ["acute", "obtuse", "equilateral"]),
        ("Sides 6, 8, and 11 form a triangle that is…",
         "obtuse", "6²+8²=100, 11²=121>100, so the angle opposite 11 is obtuse.",
         ["right", "acute", "impossible"]),
        ("A right triangle has legs 9 and 12. The hypotenuse is…",
         15, "Another 3-4-5 scale (×3).",
         [21, 13, 108]),
        ("If a²+b²=c² for the longest side c, the triangle is…",
         "right with hypotenuse c", "That is the converse of the Pythagorean theorem.",
         ["acute", "obtuse", "equilateral"]),
        ("In a 45-45-90 triangle the legs are equal and the hypotenuse is a leg times…",
         "√2", "Isosceles right triangle: legs x, hypotenuse x√2.",
         ["√3", 2, "1/2"]),
        ("A 45-45-90 triangle has a leg of 7. The hypotenuse is…",
         "7√2", "Multiply the leg by √2.",
         [7, "7√3", 14]),
        ("A 45-45-90 triangle has hypotenuse 10√2. Each leg is…",
         10, "Divide the hypotenuse by √2: 10√2/√2=10.",
         ["10√2", 5, "10√3"]),
        ("The area of a 45-45-90 triangle with hypotenuse 8√2 is…",
         32, "Legs are 8, area=(1/2)·8·8=32.",
         [16, 64, "32√2"]),
        ("A square with side 5 has diagonal…",
         "5√2", "The diagonal is the hypotenuse of a 45-45-90 triangle with leg 5.",
         [10, "5√3", 25]),
        ("In a 30-60-90 triangle the sides are in the ratio…",
         "1 : √3 : 2", "Short leg opposite 30°, long leg opposite 60° is √3 times the short, hypotenuse twice the short.",
         ["1 : 1 : √2", "3 : 4 : 5", "1 : 2 : √3"]),
        ("A 30-60-90 triangle has short leg 5. The hypotenuse is…",
         10, "Hypotenuse = 2 × short leg.",
         ["5√3", 15, "5√2"]),
        ("A 30-60-90 triangle has short leg 5. The long leg is…",
         "5√3", "Long leg = short × √3.",
         [10, "5√2", 15]),
        ("A 30-60-90 triangle has hypotenuse 14. The short leg is…",
         7, "Short = hypotenuse/2.",
         ["7√3", 14, 28]),
        ("An equilateral triangle with side 8 has height…",
         "4√3", "The height splits it into two 30-60-90 triangles with short leg 4, so height 4√3.",
         [8, 4, "8√3"]),
        ("In a right triangle, sin θ equals…",
         "opposite / hypotenuse", "SOH: sine is opposite over hypotenuse.",
         ["adjacent / hypotenuse", "opposite / adjacent", "hypotenuse / opposite"]),
        ("cos θ equals…",
         "adjacent / hypotenuse", "CAH: cosine is adjacent over hypotenuse.",
         ["opposite / hypotenuse", "opposite / adjacent", "adjacent / opposite"]),
        ("tan θ equals…",
         "opposite / adjacent", "TOA: tangent is opposite over adjacent.",
         ["opposite / hypotenuse", "adjacent / hypotenuse", "adjacent / opposite"]),
        ("In a 3-4-5 right triangle, sin of the angle opposite 3 is…",
         "3/5", "Opposite 3, hypotenuse 5.",
         ["4/5", "3/4", "4/3"]),
        ("In a 3-4-5 right triangle, tan of the angle adjacent to 3 (so opposite 4) is…",
         "4/3", "Opposite 4, adjacent 3.",
         ["3/4", "3/5", "4/5"]),
        ("A right triangle has an acute angle 30° and hypotenuse 12. The side opposite 30° is…",
         6, "sin 30°=1/2=opp/12, opp=6. Also the 30-60-90 short leg.",
         ["6√3", 12, 4]),
        ("A right triangle has an acute angle θ with opposite 8 and hypotenuse 17. sin θ =…",
         "8/17", "Definition: opposite over hypotenuse.",
         ["15/17", "8/15", "17/8"]),
        ("If tan θ=5/12 in a right triangle, a possible hypotenuse is…",
         13, "Legs 5 and 12 give hypotenuse 13.",
         [17, 7, 10]),
        ("An acute angle with sin θ=3/5 has cos θ (in a right triangle) equal to…",
         "4/5", "The other leg is 4 in a 3-4-5 triangle.",
         ["3/5", "3/4", "5/4"]),
        ("To solve a right triangle given one acute angle and the hypotenuse, you use…",
         "sine and cosine of that angle", "opp=hyp·sin, adj=hyp·cos. Then the third angle is 90 minus the given acute.",
         ["only Pythagoras, never trig", "the law of sines for obtuse triangles", "SSS congruence"]),
        ("An angle of elevation is measured from…",
         "the horizontal up to the line of sight", "Elevation looks up; depression looks down from the horizontal.",
         ["the vertical down to the ground", "the hypotenuse to a leg", "north to east"]),
        ("An angle of depression from a cliff to a boat equals the angle of elevation from the boat to the cliff because they are…",
         "alternate interior angles (horizontals parallel)",
         "The two horizontals are parallel, so the alternate interiors are congruent.",
         ["vertical angles only", "complements", "always 45°"]),
        ("From 50 m away, the angle of elevation to a building top is 45°. The building’s height is…",
         50, "tan 45°=1=h/50, so h=50.",
         [25, "50√3", 100]),
        ("A kite string 20 m long makes a 30° angle with the ground. The kite’s height is…",
         10, "sin 30°=1/2=h/20, h=10.",
         ["10√3", 20, 15]),
        ("A ramp rises 3 m over a 9 m horizontal run. tan of the inclination is…",
         "1/3", "opposite 3, adjacent 9.",
         ["3/9√10", "3", "√10/9"]),
        ("Legs 7 and 24. Hypotenuse?",
         25, "7-24-25 triple.",
         [31, 26, 13]),
        ("A 45-45-90 triangle has hypotenuse 6. Each leg is…",
         "3√2", "6/√2=3√2 after rationalizing.",
         [6, "6√2", 3]),
        ("A 30-60-90 triangle has long leg 9√3. The short leg is…",
         9, "Long = short × √3, so short = 9.",
         ["9√3", 18, "3√3"]),
        ("cos of the angle adjacent to 8 in a 8-15-17 triangle is…",
         "8/17", "Adjacent 8, hypotenuse 17.",
         ["15/17", "8/15", "15/8"]),
        ("The third angle of a right triangle with an acute angle 22° is…",
         68, "90−22=68.",
         [22, 158, 45]),
        ("A depression angle of 30° from a 40 m lighthouse to a boat means the boat is how far from the base?",
         "40√3", "tan 30°=40/d=1/√3, so d=40√3.",
         [40, 20, "40/√3"]),
        ("A 20-ft ladder leans against a wall with foot 12 ft from the wall. How high up the wall does it reach?",
         16, "12-16-20 is a scaled 3-4-5 (×4).",
         [8, 32, 15]),
        ("If sin θ=8/17, then the adjacent leg of a right triangle could be…",
         15, "8-15-17 triple.",
         [17, 9, 8]),
        ("A 45-45-90 triangle with leg 4√2 has hypotenuse…",
         8, "4√2 · √2=8.",
         ["4√2", "8√2", 4]),
        ("In a 30-60-90 triangle the side opposite 60° is 6. The hypotenuse is…",
         "4√3", "Opposite 60° is x√3=6, so x=6/√3=2√3, hypotenuse 4√3.",
         [12, 6, "6√3"]),
        ("A right triangle has legs 2 and 3. The hypotenuse is…",
         "√13", "4+9=13.",
         [5, "√6", 13]),
        ("The complement of a 37° acute angle in a right triangle is…",
         53, "90−37=53.",
         [37, 143, 45]),
        ("tan of the larger acute angle in a 5-12-13 triangle is…",
         "12/5", "The larger acute angle is opposite 12.",
         ["5/12", "12/13", "5/13"]),
        ("A support cable 25 m long meets the ground at 45°. The attachment height is…",
         "25√2/2", "sin 45°=h/25=√2/2, h=25√2/2.",
         [25, "25√2", 12.5]),
        ("Pythagorean converse: sides 2, 3, 4. The triangle is…",
         "obtuse", "4+9=13 < 16, so obtuse opposite the side of length 4.",
         ["right", "acute", "not a triangle"]),
        ("A square inscribed in a circle of diameter 10 has side…",
         "5√2", "Diagonal of the square is the diameter 10, so side 5√2.",
         [10, 5, "10√2"]),
        ("SAT Stretch: Sides 9, 40, x form a right triangle with hypotenuse x. x=…",
         41, "9-40-41 triple: 81+1600=1681=41².",
         [49, 31, 40]),
        ("SAT Stretch: A 45-45-90 triangle is one half of a square whose perimeter is 48. The triangle’s hypotenuse is…",
         "12√2", "The square’s side is 48/4=12, so that side is a leg of the 45-45-90 triangle and the hypotenuse is 12√2.",
         ["12", "24√2", 24]),
        ("SAT Stretch: A regular hexagon is assembled from six equilateral triangles of side 8, then one of those triangles is removed. The remaining area is…",
         "80√3", "One equilateral of side 8 has area (√3/4)·64=16√3. Six of them make 96√3; removing one leaves 80√3.",
         ["96√3", "16√3", "64√3"]),
        ("SAT Stretch: A 20 m cliff has an angle of depression of 45° to a boat, then later 30° to the same boat. How far did the boat travel away from the cliff?",
         "20√3-20", "First ground distance 20/tan 45°=20. Later 20/tan 30°=20√3. The boat moved 20√3−20 m.",
         ["20√3", 20, "20√3+20"]),
        ("SAT Stretch: From a lighthouse 50 m above the water, the angle of depression to a ship is 60°, then later 30°. How far did the ship travel between those sights?",
         "100√3/3", "First ground distance 50/tan 60°=50/√3=50√3/3. Later 50/tan 30°=50√3. Difference 50√3−50√3/3=100√3/3.",
         ["50√3", "50√3/3", 50]),
        ("SAT Stretch: In right △ABC with right angle at C, AC=8 and hypotenuse AB=17. The tangent of ∠A is…",
         "15/8", "The remaining leg BC=15 by 8-15-17. For ∠A, opposite is BC and adjacent is AC, so tan A=15/8.",
         ["8/17", "15/17", "8/15"]),
        ("SAT Stretch: A square sits in the right angle of a 12-16-20 triangle, with two sides along the legs and the opposite vertex on the hypotenuse. The side of the square is…",
         "48/7", "If the side is s, then s/12+s/16=1, so s(4+3)/48=1 and s=48/7.",
         [8, 6, 10]),
        ("SAT Stretch: Elevation 30° from 40 m away reaches a window. Elevation 45° from the same point reaches the roof. The wall height between window and roof is…",
         "40-40√3/3", "Window: tan 30°=h/40 so h=40/√3=40√3/3. Roof: tan 45°=H/40 so H=40. Difference 40−40√3/3.",
         [40, "40√3/3", 20]),
        ("SAT Stretch: A 30-60-90 triangle has perimeter 18+6√3. The hypotenuse is…",
         12, "Sides x, x√3, 2x. Sum 3x+x√3=18+6√3, so x=6 and 2x=12.",
         [6, "6√3", 18]),
    ]
    return _pack(rows)


def build_unit5():
    title = "Geometry Unit 5: Right Triangles & Intro Trig"
    description = (
        "The Pythagorean theorem and its converse, 45-45-90 and 30-60-90 triangles, sine cosine "
        "and tangent, solving right triangles, and angles of elevation and depression."
    )
    concepts = [
        "Pythagorean theorem and converse",
        "Special right triangles 45-45-90",
        "Special 30-60-90",
        "Sine cosine tangent",
        "Solving a right triangle",
        "Angles of elevation and depression",
    ]
    c1 = concept_block(
        "1. Pythagorean theorem and converse",
        [
            "In a right triangle with legs $a$ and $b$ and hypotenuse $c$, $a^2+b^2=c^2$. The hypotenuse is opposite "
            "the right angle and is the longest side.",
            "The converse is a classification tool: if $a$, $b$, and $c$ (with $c$ longest) satisfy $a^2+b^2=c^2$, the "
            "triangle is right. If $a^2+b^2>c^2$ it is acute; if $a^2+b^2<c^2$ it is obtuse.",
            "Memorize the common primitive triples: $3$-$4$-$5$, $5$-$12$-$13$, $7$-$24$-$25$, $8$-$15$-$17$, and $9$-$40$-$41$, "
            "plus their multiples ($6$-$8$-$10$, $9$-$12$-$15$, $10$-$24$-$26$).",
            "A ladder, a TV screen diagonal, and a coordinate distance are all Pythagorean problems. Sketch the right "
            "triangle, name the hypotenuse, then square, add, and take a square root.",
            "If you know two sides, the third is determined. If you know three sides, the converse tells you the type. "
            "Do not assume a triangle is right just because a picture looks steep.",
            "The rest of this unit is Pythagoras in costumes: special right triangles are triples with $\\sqrt{2}$ or "
            "$\\sqrt{3}$, and trigonometry is the same right triangle with a named acute angle.",
        ],
        "Coordinate distance in Unit 1 was already $a^2+b^2=c^2$. This lesson names it, classifies triangles with the "
        "converse, and prepares every trig ratio that follows.",
        "Circle the right angle, label the opposite side as hypotenuse, then write $a^2+b^2=c^2$ with $c$ in that slot. "
        "For classification, compare $a^2+b^2$ to the square of the longest side.",
        lesson_figure(
            labeled_right_triangle(3, 4, 5, a_lab="3", b_lab="4", c_lab="5", angle_lab=""),
            "The 3-4-5 right triangle",
            "$3^2+4^2=9+16=25=5^2$. The square marks $90^\\circ$; the vertical leg is $3$.",
        )
        + solved(1, "Legs 6 and 8. Find the hypotenuse.",
                 ["The hypotenuse is the side opposite the right angle, so it is $c$ in $a^2+b^2=c^2$.",
                  "Compute $6^2+8^2=36+64=100$.",
                  "Then $c=\\sqrt{100}=10$.",
                  "This is a $3$-$4$-$5$ triangle scaled by $2$."],
                 "$10$", "A $3$-$4$-$5$ triangle scaled by $2$.", "Easy")
        + solved(2, "Sides 5, 12, 13. Classify the triangle.",
                 ["The longest side is $13$, so that is the candidate hypotenuse.",
                  "Compare $5^2+12^2=25+144=169$ with $13^2=169$.",
                  "Because $a^2+b^2=c^2$, the converse of Pythagoras says the triangle is right."],
                 "right", "", "Medium")
        + solved(3, "Sides 6, 8, 11. Classify the triangle.",
                 ["The longest side is $11$.",
                  "Compute $6^2+8^2=36+64=100$ and $11^2=121$.",
                  "Since $100<121$, the angle opposite $11$ is obtuse.",
                  "The triangle is obtuse (and still a legal triangle because $6+8>11$)."],
                 "obtuse", "", "Hard"),
        ("Adding the legs instead of squaring",
         "A $6$-$8$ right triangle does not have hypotenuse $14$. That is the path around the corner. Straight-line "
         "hypotenuse squares first."),
        ("Always put the longest side in the $c$ slot for the converse",
         "If you test $6^2+11^2$ against $8^2$ you will misclassify. The candidate hypotenuse is the longest side."),
        [
            "I can find a missing side with $a^2+b^2=c^2$.",
            "I can classify a triangle with the converse.",
            "I can recognize common triples and their multiples.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Special right triangles 45-45-90",
        [
            "A $45$-$45$-$90$ triangle is an isosceles right triangle. The two legs are congruent, the acute angles are "
            "both $45^\\circ$, and the hypotenuse is a leg times $\\sqrt{2}$.",
            "If a leg is $x$, the hypotenuse is $x\\sqrt{2}$. If the hypotenuse is given, divide by $\\sqrt{2}$ (and "
            "rationalize: $c/\\sqrt{2}=c\\sqrt{2}/2$).",
            "A square cut along a diagonal produces two $45$-$45$-$90$ triangles. The square’s diagonal is $s\\sqrt{2}$.",
            "Area of a $45$-$45$-$90$ triangle is $\\dfrac{1}{2}x^2$. If the area is given, solve for the leg, then the hypotenuse.",
            "These exact values appear constantly: $\\sin 45^\\circ=\\cos 45^\\circ=\\dfrac{\\sqrt{2}}{2}$ and "
            "$\\tan 45^\\circ=1$, which is the next lesson’s language for the same picture.",
            "Do not mix this pattern with $30$-$60$-$90$. A hypotenuse of $x\\sqrt{2}$ is the $45$ family; a hypotenuse "
            "of $2x$ with a $\\sqrt{3}$ leg is the $30$-$60$ family.",
        ],
        "A square’s diagonal and an isosceles right triangle are the same object. If you remember one picture, you remember "
        "both SAT favorites.",
        "Write $x$, $x$, $x\\sqrt{2}$ on the three sides as soon as you see two $45$s or a square diagonal. Then substitute "
        "the given number for whichever of those three expressions it matches.",
        lesson_figure(
            labeled_right_triangle(1, 1, 1.41, a_lab="x", b_lab="x", c_lab="x√2", angle_lab="45°"),
            "The $45$-$45$-$90$ pattern",
            "Equal legs $x$; hypotenuse $x\\sqrt{2}$. The $45^\\circ$ label sits at an acute vertex; the square is $90^\\circ$.",
        )
        + solved(4, "A 45-45-90 triangle has a leg of 7. Find the hypotenuse.",
                 ["In a $45$-$45$-$90$ triangle the legs are equal and the hypotenuse is a leg times $\\sqrt{2}$.",
                  "The given leg is $x=7$.",
                  "Hypotenuse $=x\\sqrt{2}=7\\sqrt{2}$."],
                 "$7\\sqrt{2}$", "", "Easy")
        + solved(5, "A 45-45-90 triangle has hypotenuse $10\\sqrt{2}$. Find a leg.",
                 ["The pattern is hypotenuse $=x\\sqrt{2}$.",
                  "Set $x\\sqrt{2}=10\\sqrt{2}$.",
                  "Divide both sides by $\\sqrt{2}$ to get $x=10$."],
                 "$10$", "", "Medium")
        + solved(6, "A 45-45-90 triangle has area 18. Find a leg.",
                 ["Area of an isosceles right triangle is $\\dfrac{1}{2}x^2$.",
                  "Solve $\\dfrac{1}{2}x^2=18$, so $x^2=36$ and $x=6$ (length, so positive).",
                  "The hypotenuse would then be $6\\sqrt{2}$, but the question asked for a leg."],
                 "leg $6$", "", "Hard"),
        ("Using $\\sqrt{3}$ on a 45-45-90 triangle",
         "$\\sqrt{3}$ belongs to $30$-$60$-$90$. The $45$ family only introduces $\\sqrt{2}$."),
        ("Rationalize a hypotenuse division",
         "If $x\\sqrt{2}=6$, then $x=6/\\sqrt{2}=3\\sqrt{2}$, not $3$. Multiply numerator and denominator by $\\sqrt{2}$."),
        [
            "I can go from leg to hypotenuse with $\\sqrt{2}$.",
            "I can go from hypotenuse back to a leg.",
            "I can connect a square’s diagonal to this pattern.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Special 30-60-90",
        [
            "A $30$-$60$-$90$ triangle has sides in the ratio $1:\\sqrt{3}:2$. The short leg (opposite $30^\\circ$) is $x$, "
            "the long leg (opposite $60^\\circ$) is $x\\sqrt{3}$, and the hypotenuse is $2x$.",
            "An equilateral triangle of side $2x$ split by an altitude is two $30$-$60$-$90$ triangles. That is why the "
            "height of an equilateral triangle of side $s$ is $\\dfrac{s\\sqrt{3}}{2}$.",
            "Given any one side, you can find $x$ and then the other two. If the hypotenuse is $14$, then $x=7$. If the "
            "long leg is $9\\sqrt{3}$, then $x=9$.",
            "Exact values: $\\sin 30^\\circ=1/2$, $\\cos 30^\\circ=\\sqrt{3}/2$, $\\sin 60^\\circ=\\sqrt{3}/2$, "
            "$\\cos 60^\\circ=1/2$, $\\tan 30^\\circ=1/\\sqrt{3}$, $\\tan 60^\\circ=\\sqrt{3}$.",
            "Mixing the short and long legs is the usual error: opposite $30^\\circ$ is the smaller leg, not the $\\sqrt{3}$ "
            "leg. Sketch the triangle and write $30$ and $60$ at the correct vertices before you assign $x$ and $x\\sqrt{3}$.",
            "Together with $45$-$45$-$90$, these two families give every exact trig value you need in high-school Geometry.",
        ],
        "Equilateral height, hexagonal radii, and elevation problems at $30^\\circ$ or $60^\\circ$ all collapse to this "
        "one ratio. It is worth memorizing cold.",
        "Write short $=x$, long $=x\\sqrt{3}$, hyp $=2x$ in a tiny table. Match the given side to one row, solve for $x$, "
        "then fill the other rows.",
        lesson_figure(
            labeled_right_triangle(1, 1.73, 2, a_lab="x", b_lab="x√3", c_lab="2x", angle_lab="30°"),
            "The $30$-$60$-$90$ pattern",
            "Short vertical leg $x$ opposite $30^\\circ$ at the bottom-right vertex; long leg $x\\sqrt{3}$; hypotenuse $2x$.",
        )
        + solved(7, "A 30-60-90 triangle has short leg 5. Find the hypotenuse and the long leg.",
                 ["The short leg (opposite $30^\\circ$) is $x$, so $x=5$.",
                  "The hypotenuse is $2x=10$.",
                  "The long leg (opposite $60^\\circ$) is $x\\sqrt{3}=5\\sqrt{3}$."],
                 "$10$ and $5\\sqrt{3}$", "", "Easy")
        + solved(8, "A 30-60-90 triangle has hypotenuse 14. Find the short leg.",
                 ["The hypotenuse is $2x$.",
                  "Set $2x=14$.",
                  "Then $x=7$, which is the short leg opposite $30^\\circ$."],
                 "$7$", "", "Medium")
        + solved(9, "An equilateral triangle has side 8. Find its height.",
                 ["An altitude of an equilateral triangle splits it into two $30$-$60$-$90$ triangles.",
                  "The hypotenuse of one of those is the side $8$, so the short leg is $x=4$.",
                  "The height is the long leg: $4\\sqrt{3}$."],
                 "$4\\sqrt{3}$", "", "Hard"),
        ("Putting $\\sqrt{3}$ on the hypotenuse",
         "The hypotenuse is $2x$, a rational multiple of the short leg. $\\sqrt{3}$ lives on the long leg, opposite $60^\\circ$."),
        ("Label 30 and 60 before assigning $x$",
         "The short leg is opposite $30^\\circ$, not “whichever number is given first.” Mark the angles, then mark $x$."),
        [
            "I can use $x:x\\sqrt{3}:2x$ in either direction.",
            "I can find the height of an equilateral triangle.",
            "I can connect this triangle to the exact values of $30^\\circ$ and $60^\\circ$.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Sine, cosine, and tangent",
        [
            "For an acute angle $\\theta$ in a right triangle, $\\sin\\theta=\\dfrac{\\text{opposite}}{\\text{hypotenuse}}$, "
            "$\\cos\\theta=\\dfrac{\\text{adjacent}}{\\text{hypotenuse}}$, and $\\tan\\theta=\\dfrac{\\text{opposite}}{\\text{adjacent}}$. "
            "The mnemonic is SOH-CAH-TOA.",
            "Opposite means the side across from $\\theta$. Adjacent means the leg that touches $\\theta$ but is not the "
            "hypotenuse. The hypotenuse never changes when you switch which acute angle you are looking at; opposite and adjacent swap.",
            "The cofunction identities $\\sin(90^\\circ-\\theta)=\\cos\\theta$ are visible in the picture: the opposite of one "
            "acute angle is the adjacent of the other.",
            "A $3$-$4$-$5$ triangle gives immediate ratios: the angle opposite $3$ has $\\sin=3/5$, $\\cos=4/5$, $\\tan=3/4$. "
            "You do not need a calculator for those.",
            "Sine and cosine of an acute angle are always less than $1$, because a leg is shorter than the hypotenuse. "
            "Tangent can be larger than $1$ when the opposite is the longer leg.",
            "These three ratios are how you solve a right triangle in the next lesson and how you model elevation in the last.",
        ],
        "Every later trig course still starts here. If opposite and adjacent are mixed, every ratio in the unit is inverted.",
        "Circle $\\theta$, star the opposite side, underline the adjacent leg, and leave the hypotenuse as the unmarked long "
        "side. Then write the ratio the question named.",
        lesson_figure(
            labeled_right_triangle(3, 4, 5, a_lab="opp 3", b_lab="adj 4", c_lab="hyp 5", angle_lab="θ"),
            "SOH-CAH-TOA on a 3-4-5 triangle",
            "$\\theta$ is at the acute vertex opposite the vertical leg $3$. Then $\\sin\\theta=3/5$, $\\cos\\theta=4/5$, $\\tan\\theta=3/4$.",
        )
        + solved(10, "In a 3-4-5 triangle, find sin of the angle opposite 3.",
                 ["Sine is opposite over hypotenuse (SOH).",
                  "The opposite side is $3$ and the hypotenuse is $5$.",
                  "So $\\sin\\theta=3/5$."],
                 "$3/5$", "", "Easy")
        + solved(11, "In a 3-4-5 triangle, find tan of the angle opposite 4.",
                 ["Tangent is opposite over adjacent (TOA).",
                  "For the angle opposite $4$, the opposite is $4$ and the remaining leg (adjacent) is $3$.",
                  "So $\\tan=4/3$."],
                 "$4/3$", "", "Medium")
        + solved(12, "If sin θ=5/13 in a right triangle, find tan θ.",
                 ["$\\sin\\theta=5/13$ means opposite $5$ and hypotenuse $13$.",
                  "The remaining leg is $\\sqrt{13^2-5^2}=12$, a $5$-$12$-$13$ triangle.",
                  "Then $\\tan\\theta=\\text{opp}/\\text{adj}=5/12$."],
                 "$5/12$", "", "Hard"),
        ("Using the wrong angle’s opposite",
         "Each acute angle has its own opposite. If $\\theta$ is at the left, the opposite is the right-hand leg, not "
         "“the height in the picture” unless that height is truly across from $\\theta$."),
        ("Star opposite, underline adjacent",
         "A five-second annotation prevents swapping sine and cosine. Do it on every item, even the easy ones."),
        [
            "I can write SOH-CAH-TOA from a labeled triangle.",
            "I can find a ratio from a triple.",
            "I know sine and cosine of an acute angle are less than $1$.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Solving a right triangle",
        [
            "To solve a right triangle means to find all three sides and both acute angles. You always already have the "
            "$90^\\circ$ angle. The acute angles are complementary.",
            "Typical givens: one acute angle and one side, or two sides. If you have two sides, Pythagoras gives the third "
            "and a trig ratio (or an inverse trig function) gives an acute angle.",
            "If you have an acute angle $\\theta$ and the hypotenuse, the opposite is $c\\sin\\theta$ and the adjacent is "
            "$c\\cos\\theta$. If you have $\\theta$ and a leg, use sine, cosine, or tangent depending on which leg it is.",
            "Keep exact values when the angle is $30$, $45$, or $60$. Use a calculator (degree mode) for other angles, and "
            "round only at the end.",
            "Check: the hypotenuse must be the longest side, the larger acute angle must sit opposite the longer leg, and "
            "the two acute angles must sum to $90^\\circ$.",
            "Solving the triangle is the computational heart of elevation problems: find one missing length, then the rest "
            "follow.",
        ],
        "A “solve the triangle” item is several short questions glued together. If you stay organized — angles first or "
        "sides first, then the other — you will not drop a piece.",
        "Make a three-side, three-angle table. Fill what is given. Use $90$ minus an acute angle immediately. Then one "
        "trig ratio or Pythagoras per blank.",
        lesson_figure(
            labeled_right_triangle(6, 8, 10, a_lab="6", b_lab="8", c_lab="10", angle_lab="θ"),
            "A solved 6-8-10 triangle",
            "$\\theta$ sits at the acute vertex opposite the vertical leg $6$ (the scaled $3$ of a $3$-$4$-$5$).",
        )
        + solved(13, "A right triangle has an acute angle 30° and hypotenuse 12. Find the side opposite 30°.",
                 ["Sine uses opposite and hypotenuse: $\\sin 30^\\circ=\\text{opp}/12$.",
                  "Use the exact value $\\sin 30^\\circ=1/2$.",
                  "Then $\\text{opp}=12\\cdot\\dfrac{1}{2}=6$."],
                 "$6$", "", "Easy")
        + solved(14, "A right triangle has opposite 8 and hypotenuse 17 relative to θ. Find sin θ and the third side.",
                 ["$\\sin\\theta=\\text{opp}/\\text{hyp}=8/17$.",
                  "The remaining leg is $\\sqrt{17^2-8^2}=\\sqrt{289-64}=15$.",
                  "This is an $8$-$15$-$17$ triangle, so the third side is $15$."],
                 "$\\sin\\theta=8/17$, other leg $15$", "", "Medium")
        + solved(15, "tan θ=5/12. Find the hypotenuse of that right triangle.",
                 ["$\\tan\\theta=5/12$ means the legs are $5$ (opposite) and $12$ (adjacent).",
                  "The hypotenuse is $\\sqrt{5^2+12^2}=\\sqrt{25+144}=13$.",
                  "Check: $5$-$12$-$13$ is a primitive Pythagorean triple."],
                 "$13$", "", "Hard"),
        ("Leaving an acute angle unfound",
         "Solving the triangle includes both acute angles. After you have one, subtract from $90$ for the other. Forgetting "
         "that step leaves the answer incomplete."),
        ("Match the ratio to the given side",
         "If the hypotenuse is given, sine or cosine is easier than tangent. If both given sides are legs, tangent (or "
         "Pythagoras first) is natural. Choose the ratio that uses the known side."),
        [
            "I can find a missing side from an angle and a side.",
            "I can find a missing acute angle as $90$ minus the other.",
            "I can check that the hypotenuse is longest.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Angles of elevation and depression",
        [
            "An angle of elevation is measured upward from the horizontal to a line of sight. An angle of depression is "
            "measured downward from the horizontal to a line of sight.",
            "The two horizontals (ground and eye-level, or sea and cliff-top) are parallel, so the angle of depression "
            "from the top equals the angle of elevation from the bottom: they are alternate interior angles.",
            "The model is a right triangle: the vertical is a height, the horizontal is a distance along the ground, and "
            "the hypotenuse is a line of sight (a ladder, a cable, or a kite string).",
            "Choose sine, cosine, or tangent from which two of those three lengths are involved. Height and ground distance "
            "are tangent. Height and line of sight are sine. Ground and line of sight are cosine.",
            "Two-angle problems (elevation to the top and to a window) produce two right triangles that share the same "
            "ground distance. Subtract the two heights if the question asks for the distance between window and roof.",
            "Always sketch: a horizontal, a vertical, and a diagonal, with $\\theta$ marked at the correct place — up from "
            "the ground or down from the top horizontal, never floating in the middle of the diagonal without a vertex.",
        ],
        "SAT word problems about lighthouses, kites, and ramps are this lesson. The trig is easy; placing $\\theta$ on the "
        "correct vertex is the whole game.",
        "Draw the horizontal first, then the object, then the sight line. Mark elevation at the observer on the ground or "
        "depression at the observer on the cliff. Then name opposite and adjacent from that vertex.",
        lesson_figure(
            _elev_svg(),
            "Angle of elevation from an observer to a building",
            "$\\tan\\theta=\\dfrac{\\text{height}}{\\text{ground distance}}$.",
        )
        + solved(16, "From 50 m away, the angle of elevation to a building is 45°. Find the height.",
                 ["Sketch a right triangle: ground $50$, height $h$, elevation $45^\\circ$ at the observer.",
                  "Tangent uses opposite over adjacent: $\\tan 45^\\circ=h/50$.",
                  "Since $\\tan 45^\\circ=1$, $h=50$ m."],
                 "$50$ m", "", "Easy")
        + solved(17, "A kite string 20 m long makes a 30° angle with the ground. Find the kite’s height.",
                 ["The string is the hypotenuse and the height is opposite the $30^\\circ$ angle.",
                  "Sine is the matching ratio: $\\sin 30^\\circ=h/20$.",
                  "$\\sin 30^\\circ=1/2$, so $h=10$ m."],
                 "$10$ m", "", "Medium")
        + solved(18, "From 30 m away, elevation to a tower top is 60° and to a window is 30°. Find the window’s height.",
                 ["Both angles share the same ground distance $30$ m.",
                  "For the window, $\\tan 30^\\circ=h/30=1/\\sqrt{3}$, so $h=10\\sqrt{3}$ m.",
                  "As a check, the top is $30\\tan 60^\\circ=30\\sqrt{3}$ m, which is taller, as it should be."],
                 "$10\\sqrt{3}$ m", "", "Hard"),
        ("Putting depression at the ground",
         "Depression is at the upper observer, measured down from that person’s horizontal. The congruent elevation sits "
         "at the lower object. Swapping them still gives the same angle measure, but a messy sketch leads to using cosine "
         "on the wrong pair of sides."),
        ("Identify opposite vs adjacent from the observer",
         "Stand (in your mind) at the vertex of $\\theta$. The height is usually opposite; the walk-along-the-ground is "
         "usually adjacent. Then pick tan if you have those two."),
        [
            "I can define elevation and depression from the horizontal.",
            "I can use alternate interiors to equate them.",
            "I can choose the correct trig ratio in a sight-line triangle.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6
# ===========================================================================

def _u6_questions():
    rows = [
        ("In a parallelogram, opposite sides are…",
         "congruent and parallel", "That is the definition-plus-theorem package: both pairs of opposite sides parallel and congruent.",
         ["perpendicular", "unequal", "only parallel, never congruent"]),
        ("Consecutive angles of a parallelogram are…",
         "supplementary", "They are same-side interiors of parallel lines.",
         ["congruent always", "complementary", "vertical"]),
        ("The diagonals of a parallelogram…",
         "bisect each other", "They share a midpoint. They are not necessarily congruent (that is a rectangle).",
         ["are always congruent", "are always perpendicular", "bisect the vertex angles always"]),
        ("In parallelogram ABCD, AB=3x-1 and CD=x+7. AB=…",
         11, "Opposite sides: 3x−1=x+7, 2x=8, x=4, AB=11.",
         [7, 8, 15]),
        ("In parallelogram ABCD, ∠A=70°. Then ∠B=…",
         110, "Consecutive angles supplementary: 180−70=110. Opposite ∠C=70°.",
         [70, 20, 140]),
        ("A rectangle is a parallelogram with…",
         "four right angles", "Equivalently, a parallelogram with one right angle, or with congruent diagonals.",
         ["four congruent sides only", "exactly one right angle and no more", "perpendicular diagonals only"]),
        ("A rhombus is a parallelogram with…",
         "all sides congruent", "Its diagonals are perpendicular and bisect the vertex angles.",
         ["four right angles only", "exactly one pair of parallel sides", "congruent diagonals only"]),
        ("A square is…",
         "a rectangle and a rhombus", "All sides equal and all angles 90°. Diagonals congruent, perpendicular, and bisecting.",
         ["only a rhombus, never a rectangle", "a kite that is not a parallelogram", "a trapezoid with no parallel sides"]),
        ("The diagonals of a rhombus are…",
         "perpendicular bisectors of each other", "They are not necessarily congruent unless the rhombus is a square.",
         ["always congruent", "never perpendicular", "parallel"]),
        ("A parallelogram with congruent diagonals must be a…",
         "rectangle", "That is a rectangle test. A rhombus need not have congruent diagonals.",
         ["rhombus", "kite", "trapezoid"]),
        ("A trapezoid (exclusive definition) has…",
         "exactly one pair of parallel sides", "The parallel sides are the bases. The nonparallel sides are the legs.",
         ["two pairs of parallel sides", "no parallel sides", "four congruent sides"]),
        ("The base angles of an isosceles trapezoid are…",
         "congruent", "Legs congruent ⇒ base angles congruent. Diagonals are also congruent.",
         ["complementary", "vertical", "always 90°"]),
        ("A kite has two pairs of consecutive congruent sides. Its diagonals are…",
         "perpendicular, and one of them is a symmetry diagonal",
         "The diagonal between the equal-side vertices bisects the other diagonal and the vertex angles.",
         ["congruent always", "parallel", "never perpendicular"]),
        ("An isosceles trapezoid has bases 8 and 14 and legs 5. The height is…",
         4, "The overhang is 3 on each side; 3-4-5 gives height 4.",
         [5, 3, 6]),
        ("The midsegment of a trapezoid with bases 8 and 14 has length…",
         11, "Average of the bases: (8+14)/2=11.",
         [22, 6, 8]),
        ("The interior angle sum of an n-gon is…",
         "(n-2)·180°", "Divide into n−2 triangles from one vertex.",
         ["n·180°", "(n-1)·180°", "360° always"]),
        ("A regular octagon has each interior angle…",
         135, "(8−2)·180=1080, 1080/8=135.",
         [45, 180, 108]),
        ("The sum of the exterior angles of any convex polygon, one at each vertex, is…",
         360, "Always 360°, independent of n.",
         [180, "(n-2)·180", 720]),
        ("A regular polygon with each exterior angle 30° has how many sides?",
         12, "360/30=12.",
         [6, 8, 15]),
        ("A pentagon’s interior sum is…",
         540, "(5−2)·180=540.",
         [360, 720, 108]),
        ("To prove a quadrilateral is a parallelogram on the coordinate plane, it is enough to show…",
         "both pairs of opposite sides have equal slope (or equal length)",
         "Parallel slopes, or congruent opposite sides, or diagonals bisecting (shared midpoint).",
         ["one pair of sides equal", "one right angle", "the area is positive"]),
        ("A(0,0), B(6,0), C(8,3), D(2,3). ABCD is a…",
         "parallelogram", "AB and DC both slope 0; AD and BC both slope 3/2.",
         ["rhombus only", "rectangle", "kite that is not a parallelogram"]),
        ("The midpoint of AC and of BD for A(0,0), B(4,0), C(5,2), D(1,2) is…",
         "(2.5,1) for both", "Diagonals share a midpoint, confirming a parallelogram.",
         ["(0,0)", "(4,2)", "different midpoints"]),
        ("A(0,0), B(0,4), C(3,4), D(3,0) is a…",
         "rectangle (actually a rectangle that is not a square)",
         "Sides vertical/horizontal so angles 90°. Sides 4 and 3, not a square.",
         ["rhombus that is not a rectangle", "square", "non-rectangular parallelogram"]),
        ("Distance AB=distance AD=distance CB=distance CD with perpendicular diagonals suggests a…",
         "rhombus (or square)", "All sides equal is a rhombus. Check a right angle or diagonal congruence for a square.",
         ["trapezoid with no equal sides", "scalene kite", "circle"]),
        ("A triangle midsegment joins midpoints of two sides. It is parallel to the third side and…",
         "half as long", "Triangle Midsegment Theorem.",
         ["twice as long", "the same length", "one-third as long"]),
        ("In △ABC, M and N are midpoints of AB and AC. If BC=18, then MN=…",
         9, "Midsegment is half of BC.",
         [18, 36, 12]),
        ("The midsegment of a trapezoid with bases 10 and 22 is…",
         16, "(10+22)/2=16.",
         [32, 12, 6]),
        ("Three midsegments of a triangle split it into…",
         "four small triangles of equal area",
         "The three midsegments form the medial triangle; each of the four small triangles has area one-fourth of the original.",
         ["two similar triangles only", "a hexagon", "six right triangles always"]),
        ("If E and F are midpoints of AB and CB in △ABC, then EF ∥ AC and EF=…",
         "AC/2", "Midsegment pairing the midpoints of AB and CB is parallel to AC.",
         ["2·AC", "AB/2", "BC"]),
        ("In parallelogram PQRS, ∠P=3x and ∠R=x+80. Then x=…",
         40, "Opposite angles congruent: 3x=x+80, 2x=80, x=40.",
         [80, 20, 60]),
        ("A rhombus has side 10 and an angle 60°. Its area is…",
         "50√3", "Area = side² sin 60° = 100·√3/2 = 50√3.",
         [100, 60, "100√3"]),
        ("A rectangle’s diagonals are 10 and 10. A side is 6. The other side is…",
         8, "6²+b²=10², b=8.",
         [4, 16, 12]),
        ("A kite has diagonals 6 and 10. Its area is…",
         30, "Kite area = (1/2)d1 d2 = 30.",
         [60, 16, 8]),
        ("A regular hexagon has each interior angle…",
         120, "(6−2)·180/6=120.",
         [60, 135, 108]),
        ("n-gon interior sum 1800°. n=…",
         12, "(n-2)·180=1800, n-2=10, n=12.",
         [10, 8, 14]),
        ("A(1,1), B(4,1), C(5,3), D(2,3) has both pairs of opposite sides parallel, so it is a parallelogram. The vector AB is…",
         "(3,0)", "B−A=(3,0). DC should match.",
         ["(1,0)", "(0,3)", "(3,2)"]),
        ("Triangle midpoints D,E,F. The medial triangle DEF has perimeter how compared to ABC if ABC has perimeter 24?",
         12, "Each midsegment is half a side; the three midsegments total 12.",
         [24, 8, 18]),
        ("Isosceles trapezoid bases 6 and 16, legs 13. Height?",
         12, "Overhang 5 each side; 5-12-13.",
         [13, 5, 8]),
        ("A square with diagonal 8 has area…",
         32, "d=s√2=8, s=4√2, area=32. Or area=d²/2=32.",
         [16, 64, "16√2"]),
        ("Parallelogram consecutive angles (2x+10)° and (4x−40)°. The smaller measures…",
         80, "6x−30=180, x=35. The angles are 80° and 100°.",
         [70, 100, 90]),
        ("A rhombus has diagonals 8 and 6. Its side length is…",
         5, "Half-diagonals 4 and 3 form a 3-4-5 right triangle.",
         [7, 10, 14]),
        ("Each exterior angle of a regular polygon is 24°. The interior angle is…",
         156, "Interior = 180−24=156. Also n=360/24=15.",
         [24, 148, 168]),
        ("SAT Stretch: Parallelogram ABCD has A(0,0), B(6,0), D(2,4). Point C is…",
         "(8,4)", "C=B+D−A=(6,0)+(2,4)=(8,4).",
         ["(4,4)", "(6,4)", "(2,0)"]),
        ("SAT Stretch: A rhombus has diagonals 10 and 24. Its perimeter is…",
         52, "Half-diagonals 5 and 12 give side 13; 4×13=52.",
         [34, 48, 26]),
        ("SAT Stretch: Isosceles trapezoid bases 8 and 20, legs 10. The area is…",
         112, "Overhang 6 each side; height 8 from 6-8-10. Area=(8+20)/2·8=112.",
         [140, 80, 96]),
        ("SAT Stretch: In parallelogram ABCD, ∠A=(4x+8)° and opposite ∠C=(2x+40)°. Consecutive ∠B measures…",
         108, "Opposite angles are congruent: 4x+8=2x+40, x=16, so ∠A=72°. Consecutive angles are supplementary, so ∠B=108°.",
         [72, 80, 90]),
        ("SAT Stretch: Parallelogram ABCD has AB=5x-4, CD=2x+11, AD=3x+1, and BC=2x+6. Its perimeter is…",
         74, "Opposite sides: 5x-4=2x+11 so x=5 and AB=21; 3x+1=2x+6 so AD=16. Perimeter 2(21+16)=74.",
         [42, 58, 80]),
        ("SAT Stretch: An isosceles trapezoid has bases 2x and 4x+6 and midsegment 15. Each leg is 25. The area is…",
         360, "The midsegment averages the bases: (6x+6)/2=15, so x=4. Bases 8 and 22. Each overhang is 7. Then 7²+h²=25², h=24. Area=15·24=360.",
         [300, 240, 187]),
        ("SAT Stretch: An isosceles trapezoid has bases 10 and 26 and legs 17. Its area is…",
         270, "Overhang 8 on each side. Then 8²+h²=17², h=15. Area=(10+26)/2·15=270.",
         [221, 180, 136]),
        ("SAT Stretch: Opposite vertices of a square are A(0,0) and C(6,8). The side length is…",
         "5√2", "Diagonal AC=10, and a square’s diagonal is s√2, so s=10/√2=5√2.",
         ["10", "5", "6√2"]),
        ("SAT Stretch: A parallelogram has consecutive angles (5x)° and (4x+9)°. The obtuse angle measures…",
         95, "Supplementary: 9x+9=180, x=19. The angles are 95° and 85°.",
         [85, 90, 171]),
        ("SAT Stretch: Rectangle PQRS has opposite vertices P(0,0) and R(a,b). If PR=15 and the perimeter is 42, the area is…",
         108, "a²+b²=225 and 2(a+b)=42 so a+b=21. Then (a+b)²=441=a²+2ab+b², so 2ab=216 and ab=108.",
         [63, 90, 126]),
        ("SAT Stretch: A rhombus has side 13 and one diagonal 10. The other diagonal is…",
         24, "Half of 10 is 5. Then (d/2)²+25=169, so d/2=12 and d=24.",
         [26, 13, 10]),
        ("SAT Stretch: In rhombus ABCD, ∠A=(2x+10)° and ∠B=(4x-40)°. Diagonal AC is drawn. Each of the two angles formed at A measures…",
         40, "Consecutive angles supplementary: 6x-30=180, x=35, so ∠A=80°. A rhombus diagonal bisects the vertex angle, so each piece is 40°.",
         [80, 35, 50]),
    ]
    return _pack(rows)


def _unit_body(title, concepts, blocks):
    return unit_shell(
        title, AUDIENCE, concepts, "".join(blocks),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )


def build_unit6():
    title = "Geometry Unit 6: Quadrilaterals & Polygons"
    description = (
        "Parallelograms, rectangles rhombi and squares, trapezoids and kites, interior and exterior "
        "angle sums, coordinate proofs, and midsegments."
    )
    concepts = [
        "Parallelogram properties",
        "Rectangles rhombi squares",
        "Trapezoids and kites",
        "Interior/exterior angle sums",
        "Coordinate proofs",
        "Midsegment",
    ]
    c1 = concept_block(
        "1. Parallelogram properties",
        [
            "A parallelogram is a quadrilateral with both pairs of opposite sides parallel. Opposite sides are congruent, "
            "opposite angles are congruent, consecutive angles are supplementary, and the diagonals bisect each other.",
            "Consecutive angles are same-side interiors of a pair of parallels, so they sum to $180^\\circ$. Opposite "
            "angles are congruent because each is supplementary to the same neighbor.",
            "If the diagonals of a quadrilateral bisect each other, the quadrilateral is a parallelogram. Other tests: "
            "both pairs of opposite sides congruent, or one pair of opposite sides both congruent and parallel.",
            "Algebra on a parallelogram is usually opposite sides equal or consecutive angles supplementary. Set expressions "
            "equal or add them to $180$, then substitute back.",
            "The missing fourth vertex given $A,B,D$ is $C=B+D-A$. That vector formula is the coordinate version of "
            "parallelogram completion.",
            "Rectangles, rhombi, and squares inherit every parallelogram property and then add extras in the next lesson.",
        ],
        "The diagonal-bisect midpoint check is the fastest parallelogram test on a grid and the reason coordinate proofs work.",
        "Mark opposite sides with matching arrows, then decide: set equal (opposite) or add to $180$ (consecutive).",
        lesson_figure(
            _para_svg(),
            "Parallelogram $ABCD$ with diagonals",
            "Opposite sides parallel and congruent; diagonals bisect each other.",
        )
        + solved(1, "In parallelogram ABCD, ∠A=70°. Find ∠B and ∠C.",
                 ["Consecutive angles of a parallelogram are supplementary, so $\\angle B=180^\\circ-70^\\circ=110^\\circ$.",
                  "Opposite angles are congruent, so $\\angle C=\\angle A=70^\\circ$.",
                  "As a check, $\\angle D$ would also be $110^\\circ$, consecutive with $\\angle A$."],
                 "$\\angle B=110^\\circ$, $\\angle C=70^\\circ$", "", "Easy")
        + solved(2, "In parallelogram ABCD, AB=3x-1 and CD=x+7. Find AB.",
                 ["Opposite sides of a parallelogram are congruent, so $AB=CD$.",
                  "Set $3x-1=x+7$, then $2x=8$ and $x=4$.",
                  "Substitute: $AB=3(4)-1=11$."],
                 "$11$", "", "Medium")
        + solved(3, "In parallelogram PQRS, ∠P=3x and ∠R=x+80. Find x.",
                 ["$P$ and $R$ are opposite vertices, so the angles are congruent.",
                  "Set $3x=x+80$, then $2x=80$.",
                  "So $x=40$. (Then each opposite angle measures $120^\\circ$.)"],
                 "$40$", "", "Hard"),
        ("Setting consecutive angles equal",
         "Consecutive angles are supplementary unless the figure is a rectangle. Equal consecutive angles force $90^\\circ$."),
        ("Name opposite versus consecutive first",
         "Opposite: set equal. Consecutive: add to $180$. That one word chooses the equation."),
        ["I can use opposite sides and angles.", "I can use consecutive angles.", "I can use the diagonal-bisect test."],
        1,
    )
    c2 = concept_block(
        "2. Rectangles, rhombi, and squares",
        [
            "A rectangle is a parallelogram with four right angles; its diagonals are congruent. A rhombus is a parallelogram "
            "with all sides congruent; its diagonals are perpendicular and bisect the vertex angles.",
            "A square is both: four right angles and four congruent sides. Its diagonals are congruent, perpendicular, and "
            "angle-bisecting.",
            "Every square is a rectangle and a rhombus. A non-square rectangle is not a rhombus. A non-square rhombus is "
            "not a rectangle.",
            "Rhombus (and kite) area is $\\dfrac{1}{2}d_1 d_2$. A rhombus with side $s$ and included angle $\\theta$ has "
            "area $s^2\\sin\\theta$.",
            "Half-diagonals of a rhombus form right triangles. Diagonals $8$ and $6$ give legs $4$ and $3$ and side $5$.",
            "On a grid, equal side lengths make a rhombus; perpendicular adjacent sides make a rectangle; both make a square.",
        ],
        "Always-sometimes-never classification is this family tree. Square sits inside rectangle and rhombus; both sit inside parallelogram.",
        "When a property is named, ask which extra it adds to a parallelogram: rectangle, rhombus, or both (square).",
        lesson_figure(
            svg_rect(8, 5, True),
            "A rectangle that is not a square",
            "Right angles and congruent diagonals; adjacent sides need not be equal.",
        )
        + solved(4, "A parallelogram has congruent diagonals. What special name must it have?",
                 ["A generic parallelogram has diagonals that bisect each other, but they need not be congruent.",
                  "Congruent diagonals is the extra property that forces a rectangle.",
                  "So the parallelogram must be a rectangle (and might also be a square, but rectangle is the name the test guarantees)."],
                 "rectangle", "", "Easy")
        + solved(5, "A rhombus has diagonals 8 and 6. Find a side.",
                 ["Rhombus diagonals are perpendicular bisectors of each other.",
                  "Half-diagonals $4$ and $3$ form a right triangle with the side as hypotenuse.",
                  "Then $3^2+4^2=25$, so a side is $5$."],
                 "$5$", "", "Medium")
        + solved(6, "A rhombus has side 10 and a $60^\\circ$ angle. Find its area.",
                 ["Area of a parallelogram (hence a rhombus) is $s^2\\sin\\theta$.",
                  "Here $s=10$ and $\\theta=60^\\circ$, so $\\sin 60^\\circ=\\sqrt{3}/2$.",
                  "Area $=100\\cdot\\sqrt{3}/2=50\\sqrt{3}$."],
                 "$50\\sqrt{3}$", "", "Hard"),
        ("Calling every rhombus a square",
         "A rhombus can lean. Without a right angle or congruent diagonals, it is not a square."),
        ("Draw the half-diagonals",
         "Rhombus and kite computations become Pythagorean triples at the crossing of the diagonals."),
        ["I can place rectangle, rhombus, and square in the family.", "I can use diagonal tests.", "I can compute rhombus area."],
        6,
    )
    c3 = concept_block(
        "3. Trapezoids and kites",
        [
            "A trapezoid has exactly one pair of parallel sides (the bases). An isosceles trapezoid has congruent legs, "
            "congruent base angles, and congruent diagonals.",
            "The trapezoid midsegment averages the bases: $\\dfrac{b_1+b_2}{2}$. Area is that midsegment times height.",
            "A kite has two pairs of consecutive congruent sides. Diagonals are perpendicular; one is a symmetry line.",
            "Kite area is $\\dfrac{1}{2}d_1 d_2$. Isosceles-trapezoid height comes from right triangles on the overhangs "
            "$\\dfrac{b_{\\text{long}}-b_{\\text{short}}}{2}$.",
            "Drop perpendiculars from the short base to the long base to see a rectangle plus two right triangles.",
            "Kites and isosceles trapezoids share some, but not both, of a parallelogram’s pairing properties.",
        ],
        "SAT trapezoid area almost always hides a $3$-$4$-$5$ overhang. Split the extra base length in half before Pythagoras.",
        "For a kite, draw both diagonals and use $\\dfrac{1}{2}d_1 d_2$. For a trapezoid, average the parallel sides, then multiply by height.",
        lesson_figure(
            _trap_svg(),
            "A trapezoid with two bases marked",
            "Exactly one pair of parallel sides. The midsegment averages those bases.",
        )
        + solved(7, "Trapezoid bases 8 and 14. Find the midsegment.",
                 ["The midsegment of a trapezoid averages the two bases.",
                  "Compute $(8+14)/2=22/2=11$.",
                  "That midsegment is parallel to both bases."],
                 "$11$", "", "Easy")
        + solved(8, "Isosceles trapezoid bases 8 and 14, legs 5. Find the height.",
                 ["The extra base length is $14-8=6$, so each overhang is $3$.",
                  "Drop perpendiculars: each side triangle has leg $3$ and hypotenuse $5$.",
                  "Then $3$-$4$-$5$ gives height $4$."],
                 "$4$", "", "Medium")
        + solved(9, "A kite has diagonals 6 and 10. Find its area.",
                 ["Kite diagonals are perpendicular, so area is $\\dfrac{1}{2}d_1 d_2$.",
                  "Substitute $d_1=6$ and $d_2=10$.",
                  "Area $=\\dfrac{1}{2}\\cdot 6\\cdot 10=30$."],
                 "$30$", "", "Hard"),
        ("Using both legs as bases",
         "Only the parallel pair are bases. Average those two lengths, not all four sides."),
        ("Drop two heights on an isosceles trapezoid",
         "The middle rectangle has width equal to the short base. The triangles absorb the extra length equally."),
        ["I can use trapezoid midsegment and area.", "I can find isosceles height from overhangs.", "I can compute kite area."],
        11,
    )
    c4 = concept_block(
        "4. Interior and exterior angle sums",
        [
            "Interior sum of a convex $n$-gon is $(n-2)\\cdot 180^\\circ$, because one vertex splits the polygon into $n-2$ triangles.",
            "A regular $n$-gon has each interior $\\dfrac{(n-2)\\cdot 180}{n}$. Exterior sum, one per vertex, is always $360^\\circ$.",
            "Each regular exterior is $360/n$, and interior $+$ exterior $=180$. If each interior is $150$, the exterior is $30$ and $n=12$.",
            "Pentagon interiors $540$, hexagon $720$, octagon $1080$. The formula covers every other $n$.",
            "Do not use $360$ as an interior sum except for a quadrilateral. $360$ is the exterior-sum constant.",
            "When $n$ is unknown, convert an interior to an exterior first, then divide $360$ by that exterior.",
        ],
        "Regular-polygon SAT items are fastest if you go exterior-first: subtract from $180$, then $360$ divided by that number is $n$.",
        "If the problem gives an interior, subtract from $180$ to get the exterior, then $n=360/\\text{exterior}$.",
        lesson_figure(
            svg_rect(5, 5, False),
            "A square: interiors $90^\\circ$, exteriors $90^\\circ$",
            "Four exteriors sum to $360^\\circ$. Four interiors sum to $360^\\circ$ as well, because $n=4$.",
        )
        + solved(10, "Find the interior sum of a pentagon.",
                 ["Interior sum of a convex $n$-gon is $(n-2)\\cdot 180^\\circ$.",
                  "A pentagon has $n=5$, so $n-2=3$.",
                  "Then $3\\cdot 180=540$."],
                 "$540^\\circ$", "", "Easy")
        + solved(11, "Each exterior of a regular polygon is $30^\\circ$. Find $n$.",
                 ["One exterior at each vertex, and the exteriors of any convex polygon sum to $360^\\circ$.",
                  "For a regular polygon they are equal, so $n=360/30$.",
                  "Thus $n=12$."],
                 "$12$", "", "Medium")
        + solved(12, "A regular polygon has interior $150^\\circ$. Find $n$.",
                 ["Interior and exterior at a vertex are a linear pair, so the exterior is $180-150=30^\\circ$.",
                  "Then $n=360/30=12$.",
                  "Check: $(12-2)\\cdot 180/12=150$, which matches the given interior."],
                 "$12$", "", "Hard"),
        ("Using $360^\\circ$ as a pentagon’s interior sum",
         "A pentagon interiors sum to $540^\\circ$. $360$ is exteriors for any $n$, or interiors of a quadrilateral."),
        ("Convert interior to exterior before finding $n$",
         "Do not divide $360$ by an interior angle."),
        ["I can compute $(n-2)\\cdot 180$.", "I can use $360/n$ for exteriors.", "I can recover $n$ from an angle."],
        16,
    )
    c5 = concept_block(
        "5. Coordinate proofs",
        [
            "Place a figure on the grid and use slope, distance, and midpoint. Equal slopes mean parallel; product $-1$ means "
            "perpendicular; equal distances mean congruent segments; equal midpoints mean bisected diagonals.",
            "To prove a parallelogram, show both pairs of opposite sides parallel, or show the diagonals share a midpoint.",
            "A convenient placement is $A(0,0)$, $B(a,0)$, $D(b,c)$, $C(a+b,c)$. The fourth vertex given $A,B,D$ is $C=B+D-A$.",
            "A rectangle on the axes is $(0,0)$, $(a,0)$, $(a,b)$, $(0,b)$. A rhombus needs four equal side lengths.",
            "After you have a parallelogram, check extra properties only if the question asks for rectangle, rhombus, or square.",
            "These same three tools — slope, distance, midpoint — return in Unit 8 for polygon area and segment partitions.",
        ],
        "A grid turns “prove $ABCD$ is a parallelogram” into four slope computations. Write the slopes; do not guess from the sketch.",
        "Compute slopes or midpoints first, name the parallelogram, then test extras (equal sides or right angles) only if asked.",
        lesson_figure(
            svg_plane(points=[(0, 0, "A"), (6, 0, "B"), (8, 3, "C"), (2, 3, "D")], lim=9, line=(0, 0, 6, 0)),
            "A parallelogram on the coordinate plane",
            "Horizontal sides slope $0$; the other pair both slope $3/2$.",
        )
        + solved(13, "A(0,0), B(6,0), C(8,3), D(2,3). Why is ABCD a parallelogram?",
                 ["Slope of $AB=(0-0)/(6-0)=0$ and slope of $DC=(3-3)/(2-8)=0$, so $AB\\parallel DC$.",
                  "Slope of $AD=3/2$ and slope of $BC=(3-0)/(8-6)=3/2$, so $AD\\parallel BC$.",
                  "Both pairs of opposite sides are parallel, so $ABCD$ is a parallelogram."],
                 "both pairs of opposite sides parallel", "", "Easy")
        + solved(14, "A(0,0), B(6,0), D(2,4). Find C so ABCD is a parallelogram.",
                 ["Vector $AB=(6,0)$ and vector $AD=(2,4)$.",
                  "The fourth vertex is $C=A+AB+AD=B+D-A$.",
                  "So $C=(6,0)+(2,4)=(8,4)$."],
                 "$(8,4)$", "", "Medium")
        + solved(15, "A(0,0), B(0,4), C(3,4), D(3,0). Classify as specifically as possible.",
                 ["Adjacent sides are vertical and horizontal, so every angle is $90^\\circ$: a rectangle.",
                  "Side lengths are $4$ and $3$, which are not equal, so it is not a rhombus or a square.",
                  "The most specific name is rectangle (that is not a square)."],
                 "rectangle (not a square)", "", "Hard"),
        ("Using only one pair of parallel sides",
         "One pair of parallels is a trapezoid. A parallelogram needs both pairs or an equivalent test."),
        ("Place a vertex at the origin when you choose the coordinates",
         "A smart placement eliminates extra constants. If the figure is already plotted, compute it as given."),
        ["I can prove a parallelogram with slopes or midpoints.", "I can find a missing vertex.", "I can classify on a grid."],
        21,
    )
    c6 = concept_block(
        "6. Midsegment",
        [
            "A triangle midsegment joins the midpoints of two sides, is parallel to the third side, and is half as long.",
            "The three midsegments split a triangle into four small triangles of equal area. Their total perimeter is half "
            "the original perimeter.",
            "A trapezoid midsegment joins the midpoints of the legs, is parallel to the bases, and averages the bases. "
            "Do not use “half the third side” on a trapezoid.",
            "Varignon’s theorem: the quadrilateral formed by joining the midpoints of any quadrilateral is a parallelogram.",
            "On coordinates, a midsegment is two midpoint formulas plus a slope or distance check.",
            "Midsegments are similarity with $k=1/2$ plus a parallel, which is why they sit at the end of the quadrilateral unit.",
        ],
        "A sentence that names two midpoints of sides is this theorem. A median is a vertex-to-midpoint segment and is a different object.",
        "Name the third side first — the side whose endpoints were not used as midpoints. The midsegment copies that side at half length.",
        lesson_figure(
            _prop_svg(),
            "A midsegment is the $k=1/2$ parallel case",
            "When $D$ and $E$ are midpoints, $DE$ is parallel to the third side and half as long.",
        )
        + solved(16, "M and N midpoints of AB and AC, BC=18. Find MN.",
                 ["$MN$ joins the midpoints of two sides of $\\triangle ABC$, so it is a midsegment.",
                  "A midsegment is parallel to the third side and half as long.",
                  "The third side is $BC=18$, so $MN=9$."],
                 "$9$", "", "Easy")
        + solved(17, "Trapezoid bases 10 and 22. Find the midsegment.",
                 ["A trapezoid midsegment averages the two bases; it is not half of one side.",
                  "Compute $(10+22)/2=16$.",
                  "That segment is parallel to both bases."],
                 "$16$", "", "Medium")
        + solved(18, "ABC has perimeter 24. The three-midsegment triangle has perimeter…",
                 ["Each midsegment is half of one side of $\\triangle ABC$.",
                  "The three midsegments therefore total half the original perimeter.",
                  "Half of $24$ is $12$."],
                 "$12$", "", "Hard"),
        ("Using the triangle formula on a trapezoid",
         "A trapezoid midsegment averages two bases. Half of one side is the triangle version only."),
        ("Identify the third side",
         "The third side is the one whose endpoints are not the two midpoints you joined."),
        ["I can apply the triangle midsegment theorem.", "I can apply the trapezoid midsegment theorem.", "I can use midpoints on a grid."],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7
# ===========================================================================

def _u7_questions():
    rows = [
        ("A central angle intercepting a 80° arc measures…",
         80, "A central angle equals its intercepted arc.",
         [40, 160, 100]),
        ("An inscribed angle intercepting a 80° arc measures…",
         40, "An inscribed angle is half its intercepted arc.",
         [80, 160, 20]),
        ("A central angle of 50° intercepts an arc of…",
         50, "Central angle and arc have the same measure.",
         [25, 100, 130]),
        ("An inscribed angle of 35° intercepts an arc of…",
         70, "Arc = 2 × inscribed angle.",
         [35, 17.5, 145]),
        ("An angle inscribed in a semicircle measures…",
         90, "It intercepts a 180° arc, so it is 90°. (Thales’ theorem.)",
         [45, 180, 60]),
        ("Arc length of a 60° arc in a circle of radius 6, in terms of π, is…",
         "2π", "60/360 · 2π·6 = π·2 = 2π.",
         ["6π", "π", "12π"]),
        ("Sector area for r=6 and 60°, in terms of π, is…",
         "6π", "60/360 · π·36 = 6π.",
         ["36π", "12π", "2π"]),
        ("A full circle of radius 4 has circumference…",
         "8π", "C=2πr=8π.",
         ["16π", "4π", 8]),
        ("A 90° arc in a circle of radius 8 has length…",
         "4π", "90/360 · 16π = 4π.",
         ["8π", "2π", "16π"]),
        ("A 90° sector of a circle of radius 8 has area…",
         "16π", "90/360 · 64π = 16π.",
         ["64π", "8π", "32π"]),
        ("A radius perpendicular to a chord…",
         "bisects the chord", "The perpendicular from the center to a chord hits the midpoint.",
         ["is parallel to the chord", "equals the chord", "bisects a tangent automatically"]),
        ("A diameter is a chord that…",
         "passes through the center (longest chord)", "Every diameter is a chord; not every chord is a diameter.",
         ["is shorter than every other chord", "never contains the center", "equals the radius"]),
        ("If a chord is 8 and the perpendicular from the center to it is 3, the radius is…",
         5, "Half-chord 4, so 3-4-5.",
         [8, 11, 7]),
        ("Congruent chords in the same circle are…",
         "equidistant from the center", "Equal chords sit at equal distances from the center.",
         ["always diameters", "never parallel", "always tangent"]),
        ("A diameter that bisects a chord (that is not a diameter) is…",
         "perpendicular to the chord", "The converse of the perpendicular-bisector fact for chords.",
         ["parallel to the chord", "tangent to the circle", "shorter than the chord"]),
        ("A tangent is perpendicular to the radius at the…",
         "point of tangency", "Radius ⊥ tangent at the contact point.",
         ["center only", "a random chord", "the far end of a diameter"]),
        ("Two tangent segments from a common external point are…",
         "congruent", "The two tangents from an outside point to a circle have equal length.",
         ["perpendicular to each other always", "parallel", "unequal"]),
        ("A radius of 5 meets a tangent. A point on the tangent is 12 from the external endpoint of a 13-path. The tangent segment from that external point is…",
         12, "Radius 5, hypotenuse 13 to the external point, tangent 12 (5-12-13).",
         [5, 13, 7]),
        ("If a tangent and a radius form an angle of x at the contact point, then x=…",
         90, "By the tangent-radius theorem, the angle is 90°.",
         [45, 180, 60]),
        ("A circumscribed polygon has sides that are…",
         "tangent to the circle", "Each side touches the circle once. Opposite to an inscribed polygon, whose vertices lie on the circle.",
         ["chords of the circle", "diameters", "secants only"]),
        ("An inscribed angle intercepting the same arc as a 100° central angle measures…",
         50, "Inscribed is half the central that intercepts the same arc.",
         [100, 200, 80]),
        ("Opposite angles of a cyclic quadrilateral are…",
         "supplementary", "Each intercepts the arc that the other does not; they add to 180°.",
         ["congruent", "complementary", "right always"]),
        ("An inscribed angle intercepting a diameter measures…",
         90, "The intercepted arc is a semicircle.",
         [45, 60, 180]),
        ("If two inscribed angles intercept the same arc, they are…",
         "congruent", "Both equal half of that same arc.",
         ["supplementary", "central", "vertical"]),
        ("A cyclic quadrilateral has angles 80°, 100°, 70°, and…",
         110, "Opposite to 70 is 110 because 70+110=180.",
         [80, 90, 20]),
        ("The equation of a circle with center (0,0) and radius 5 is…",
         "x²+y²=25", "x²+y²=r².",
         ["x²+y²=5", "(x-5)²+(y-5)²=0", "x+y=5"]),
        ("Center (3,−2), radius 4. The equation is…",
         "(x-3)²+(y+2)²=16", "r²=16; y−(−2)=y+2.",
         ["(x+3)²+(y-2)²=16", "(x-3)²+(y+2)²=4", "x²+y²=16"]),
        ("x²+y²−6x=0 completes to a circle of radius…",
         3, "(x-3)²+y²=9, r=3.",
         [6, 9, 0]),
        ("The point (3,4) lies on x²+y²=r². Then r=…",
         5, "9+16=25, r=5.",
         [7, 12, 25]),
        ("A circle with diameter from (−1,2) to (5,2) has center…",
         "(2,2)", "Midpoint of the diameter.",
         ["(5,2)", "(−1,2)", "(2,0)"]),
        ("A central angle is 120° and r=9. Arc length in terms of π?",
         "6π", "120/360·18π=6π.",
         ["9π", "3π", "18π"]),
        ("Inscribed angle 18° intercepts an arc of…",
         36, "Double the inscribed angle.",
         [18, 9, 162]),
        ("Chord 10, distance from center 12. Radius?",
         13, "Half-chord 5; 5-12-13.",
         [11, 22, 2]),
        ("Two tangents from a point are 7 and 3x-2. Then x=…",
         3, "Congruent tangents: 3x-2=7, 3x=9, x=3.",
         [7, 2, 5]),
        ("Cyclic quadrilateral angles 95° and the opposite angle is…",
         85, "Supplementary: 180−95=85.",
         [95, 5, 265]),
        ("(x+1)²+(y-4)²=49 has center and radius…",
         "(-1,4), r=7", "h=−1, k=4, r=7.",
         ["(1,-4), r=7", "(-1,4), r=49", "(0,0), r=7"]),
        ("A 270° arc with r=4 has length…",
         "6π", "270/360·8π=6π.",
         ["8π", "4π", "12π"]),
        ("Sector 40° with r=9. Area in terms of π?",
         "9π", "40/360·81π=9π.",
         ["81π", "18π", "4π"]),
        ("A tangent from (0,0) to a circle centered at (0,5) with r=3. The tangent length is…",
         4, "Distance to center 5, r=3, tangent √(25-9)=4.",
         [5, 3, 8]),
        ("An inscribed angle and a central angle intercept the same 48° arc. The inscribed angle is…",
         24, "Half of 48.",
         [48, 96, 12]),
        ("Diameter 16. A perpendicular from the center to a chord is 6. The chord length is…",
         "4√7", "Radius 8. Half the chord is √(64−36)=√28=2√7, so the full chord is 4√7.",
         [8, 6, "2√7"]),
        ("A 120° sector with r=3 has area…",
         "3π", "120/360·9π=3π.",
         ["9π", "6π", "π"]),
        ("Inscribed angle 22° and a central angle intercepting the same arc. The central angle is…",
         44, "The central angle is twice the inscribed angle when they share an arc.",
         [22, 11, 158]),
        ("The circle (x-2)²+(y+5)²=36 passes through which of these points?",
         "(2,1)", "Center (2,−5), r=6. Distance from center to (2,1) is 6.",
         ["(2,-5)", "(8,-5)", "(0,0)"]),
        ("A tangent and a secant from an external point: the tangent is 6 and the external secant piece is 4. The entire secant is…",
         9, "Power of a point: 6²=4·s, so s=9.",
         [12, 6, 8]),
        ("Two circles of radii 5 and 3 are tangent externally. The distance between centers is…",
         8, "External tangency: d=r1+r2=8.",
         [2, 15, 4]),
        ("SAT Stretch: Inscribed ∠ABC=2x+8 and inscribed ∠ADC intercept the same arc AC. If ∠ADC=3x−4, then arc AC measures…",
         64, "Angles intercepting the same arc are congruent: 2x+8=3x−4, x=12. Each inscribed angle is 32°, so the arc is 64°.",
         [32, 48, 96]),
        ("SAT Stretch: An arc of 120° has length 8π. A 90° sector of the same circle has area…",
         "36π", "120/360·2πr=8π ⇒ (1/3)·2r=8 ⇒ r=12. Then 90/360·π·144=36π.",
         ["16π", "24π", "144π"]),
        ("SAT Stretch: A diameter is 26 and a chord of length 10 is parallel to that diameter. The distance from the diameter to the chord is…",
         12, "Radius 13. Half the chord is 5, so the distance from the center is √(169−25)=12. The diameter runs through the center, so that is also the distance to the chord.",
         [5, 13, 8]),
        ("SAT Stretch: Two tangents from P touch a circle at A and B, and ∠APB=40°. Minor arc AB measures…",
         140, "Quadrilateral OAPB has angles 90, 90, 40, and the central angle. 360−220=140° for the minor arc.",
         [40, 80, 220]),
        ("SAT Stretch: x²+y²+8x-6y=0. The radius is…",
         5, "(x+4)²+(y-3)²=25, r=5.",
         [4, 3, 25]),
        ("SAT Stretch: A cyclic quadrilateral has opposite angles 2x+10 and 4x-10. Then x=…",
         30, "Opposites supplementary: 6x=180, x=30. The angles are 70° and 110°.",
         [20, 45, 15]),
        ("SAT Stretch: Circle center (1,−2) through (4,2). The radius is…",
         5, "Δx=3, Δy=4, r=5. Equation (x-1)²+(y+2)²=25.",
         [7, 25, 4]),
        ("SAT Stretch: A 72° inscribed angle intercepts a minor arc. The major arc measures…",
         216, "The intercepted minor arc is 144°, so the major arc is 360−144=216°.",
         [144, 72, 288]),
        ("SAT Stretch: Intersecting chords split one chord into 3 and 8 and the other into 4 and x. Then x=…",
         6, "Power of a point: 3·8=4x, so x=6.",
         [12, 24, 5]),
    ]
    return _pack(rows)


def build_unit7():
    title = "Geometry Unit 7: Circles"
    description = (
        "Central and inscribed angles, arc length and sector area, chords and diameters, tangent "
        "theorems, the inscribed-angle theorem, and equations of circles."
    )
    concepts = [
        "Central and inscribed angles",
        "Arc length and sector area",
        "Chords and diameters",
        "Tangent theorems",
        "Inscribed angle theorem",
        "Equations of circles",
    ]
    c1 = concept_block(
        "1. Central and inscribed angles",
        [
            "A central angle has its vertex at the center of the circle. Its measure equals the measure of its intercepted arc.",
            "An inscribed angle has its vertex on the circle and sides that are chords. Its measure is half the intercepted arc.",
            "Consequently, a central angle is twice an inscribed angle that intercepts the same arc. An angle inscribed in a "
            "semicircle is $90^\\circ$ because it intercepts a $180^\\circ$ arc.",
            "Two inscribed angles that intercept the same arc are congruent. That is a quick way to mark equal angles in a circle diagram.",
            "Arc measure is in degrees (like a central angle). Arc length is a distance, computed in the next lesson from that degree measure.",
            "Naming the intercepted arc is the whole skill: the arc that lies in the interior of the angle, between the two sides.",
        ],
        "SAT circle items almost always hide “inscribed = half the arc.” If you use the central-angle number on an inscribed angle, every answer is doubled.",
        "Point to the vertex: on the center $\\Rightarrow$ copy the arc; on the circle $\\Rightarrow$ take half the arc.",
        lesson_figure(
            _inscribed_svg(),
            "A central angle at $O$ and an inscribed angle on the same arc",
            "The inscribed angle is half the central angle that intercepts the same arc.",
        )
        + solved(1, "A central angle intercepts an 80° arc. Find the central angle and an inscribed angle on that arc.",
                 ["A central angle equals its intercepted arc, so the central angle is $80^\\circ$.",
                  "An inscribed angle intercepting the same arc is half of that arc.",
                  "The inscribed angle is $40^\\circ$."],
                 "$80^\\circ$ and $40^\\circ$", "", "Easy")
        + solved(2, "An inscribed angle measures 35°. Find the intercepted arc.",
                 ["An inscribed angle is half its intercepted arc, so the arc is twice the angle.",
                  "Compute $2\\times 35=70$.",
                  "The intercepted arc measures $70^\\circ$."],
                 "$70^\\circ$", "", "Medium")
        + solved(3, "Why is an angle inscribed in a semicircle a right angle?",
                 ["An angle inscribed in a semicircle intercepts a diameter, whose arc is $180^\\circ$.",
                  "The inscribed-angle theorem says the angle is half that arc.",
                  "Half of $180$ is $90$, which is Thales’ theorem."],
                 "$90^\\circ$ (Thales’ theorem)", "", "Hard"),
        ("Using the full arc on an inscribed angle",
         "Inscribed angles take half of the intercepted arc, not the whole circle minus something unless the problem says so."),
        ("Mark the intercepted arc with a highlighter",
         "The intercepted arc is the one the two chords cut off, interior to the angle. Half of that number is the angle."),
        ["I can equate a central angle to its arc.", "I can take half an arc for an inscribed angle.", "I can use the semicircle right-angle theorem."],
        1,
    )
    c2 = concept_block(
        "2. Arc length and sector area",
        [
            "Arc length is the fraction of the circumference: $\\dfrac{\\theta}{360}\\cdot 2\\pi r$, with $\\theta$ in degrees. "
            "In radians it is $s=r\\theta$, but this course stays in degrees unless a later class switches.",
            "Sector area is the same fraction of the disk: $\\dfrac{\\theta}{360}\\cdot\\pi r^2$. A $60^\\circ$ sector is one-sixth of the circle.",
            "A $90^\\circ$ arc of radius $8$ has length $4\\pi$. The matching sector has area $16\\pi$. Length uses $2\\pi r$; area uses $\\pi r^2$.",
            "A common mix-up is to use the area formula for a length question. Check the units: length answers look like $k\\pi$; area answers look like $k\\pi$ too, so you must know which formula you used.",
            "A segment of a circle (area between a chord and its arc) is sector minus triangle. That is a stretch skill still on this lesson.",
            "Leave answers in terms of $\\pi$ unless the problem asks for a decimal. Exact form is the Geometry standard.",
        ],
        "If you remember one picture — a pizza slice — you remember both formulas: the crust is arc length, the cheese is sector area, and both use $\\theta/360$.",
        "Write the fraction $\\theta/360$ first, then multiply by $2\\pi r$ or $\\pi r^2$ depending on whether the question said length or area.",
        lesson_figure(
            _sector_svg(),
            "A $60^\\circ$ sector of radius $r$",
            "The slice is $\\dfrac{1}{6}$ of the circle: arc $\\dfrac{1}{6}\\cdot 2\\pi r$, area $\\dfrac{1}{6}\\pi r^2$.",
        )
        + solved(4, "r=6, θ=60°. Find the arc length in terms of π.",
                 ["Arc length is the fraction $\\theta/360$ of the circumference $2\\pi r$.",
                  "Here $\\theta/360=60/360=1/6$ and $2\\pi r=12\\pi$.",
                  "So the arc length is $\\dfrac{1}{6}\\cdot 12\\pi=2\\pi$."],
                 "$2\\pi$", "", "Easy")
        + solved(5, "Same circle. Find the sector area in terms of π.",
                 ["Sector area is the same fraction of the disk $\\pi r^2$.",
                  "With $r=6$, $\\pi r^2=36\\pi$, and $60/360=1/6$.",
                  "Sector area $=\\dfrac{1}{6}\\cdot 36\\pi=6\\pi$."],
                 "$6\\pi$", "", "Medium")
        + solved(6, "r=12, θ=150°. Find the arc length in terms of π.",
                 ["Write the fraction first: $150/360=5/12$.",
                  "Circumference is $2\\pi\\cdot 12=24\\pi$.",
                  "Arc length $=\\dfrac{5}{12}\\cdot 24\\pi=10\\pi$."],
                 "$10\\pi$", "", "Hard"),
        ("Using πr² when the question asked for arc length",
         "Arc length is a piece of the circumference $2\\pi r$, not of the area. A $60^\\circ$ arc of radius $6$ is $2\\pi$, not $6\\pi$."),
        ("Write θ/360 before multiplying",
         "That fraction is the same for length and area. Choosing $2\\pi r$ versus $\\pi r^2$ is the only extra decision."),
        ["I can compute arc length from a degree measure.", "I can compute sector area.", "I can leave answers in terms of π."],
        6,
    )
    c3 = concept_block(
        "3. Chords and diameters",
        [
            "A chord joins two points on the circle. A diameter is a chord through the center and is the longest chord.",
            "A radius perpendicular to a chord bisects the chord. Conversely, a diameter that bisects a chord is perpendicular to it.",
            "The right triangle formed by a radius, the perpendicular to the chord, and a half-chord is a Pythagorean factory: "
            "$r^2 = d^2 + (\\text{half-chord})^2$.",
            "Congruent chords are equidistant from the center. Nearer chords are longer; the diameter is the nearest (distance $0$ from the center along the chord’s perpendicular would mean the chord is a diameter).",
            "Two chords intersecting inside a circle satisfy the power relation $ae=ce$ of the pieces, which is a stretch fact still on chords.",
            "Always drop the perpendicular from the center to the chord before you compute. That right triangle is the whole lesson.",
        ],
        "A chord-length SAT item is a $6$-$8$-$10$ triangle in disguise. Half the chord, the distance from the center, and the radius are the three sides.",
        "Draw the radius to an endpoint of the chord and the perpendicular to the midpoint, then label $r$, $d$, and half the chord.",
        lesson_figure(
            _chord_svg(),
            "A chord with the perpendicular from the center",
            "Radius $OM$ is perpendicular to chord $AB$ at its midpoint $M$. Half the chord, $OM$, and a radius to an endpoint form a right triangle.",
        )
        + solved(7, "A chord is 8 and the perpendicular from the center is 3. Find the radius.",
                 ["A radius perpendicular to a chord bisects the chord, so each half is $4$.",
                  "The right triangle has legs $3$ and $4$ and hypotenuse $r$.",
                  "Then $3^2+4^2=25$, so $r=5$."],
                 "$5$", "", "Easy")
        + solved(8, "Chord 16, radius 10, distance from center 6. Why is this consistent?",
                 ["Half the chord is $8$.",
                  "The three lengths $6$, $8$, and $10$ should satisfy Pythagoras.",
                  "Check: $6^2+8^2=36+64=100=10^2$, so the perpendicular, half-chord, and radius form a $6$-$8$-$10$ right triangle."],
                 "6-8-10 right triangle", "", "Medium")
        + solved(9, "Diameter 16, perpendicular from center to a chord is 6. Find the chord.",
                 ["The radius is half the diameter: $r=8$.",
                  "Half the chord is $\\sqrt{8^2-6^2}=\\sqrt{64-36}=\\sqrt{28}=2\\sqrt{7}$.",
                  "The full chord is twice that: $4\\sqrt{7}$."],
                 "$4\\sqrt{7}$", "", "Hard"),
        ("Forgetting to halve the chord",
         "The right triangle uses half the chord, not the whole chord. Using $8$ instead of $4$ as a leg doubles the error."),
        ("Draw the perpendicular first",
         "The picture of $r$, $d$, and half-chord prevents plugging the diameter in as a leg."),
        ["I can bisect a chord with a perpendicular from the center.", "I can find r from a half-chord right triangle.", "I can compare chord lengths by distance from the center."],
        11,
    )
    c4 = concept_block(
        "4. Tangent theorems",
        [
            "A tangent line touches the circle at exactly one point. The radius to that point is perpendicular to the tangent.",
            "Two tangent segments from a common external point are congruent. The line from the center to that external point bisects the angle between the tangents.",
            "The right triangle formed by the radius, the tangent segment, and the line from the center to the external point is another Pythagorean triple: $r^2 + t^2 = d^2$.",
            "A circumscribed polygon has sides tangent to an incircle. An inscribed polygon has vertices on a circumcircle. The words are easy to swap — inscribed vertices sit on the circle.",
            "A tangent-secant power relation from an external point says $t^2 = \\text{external}\\cdot\\text{whole secant}$. That is the stretch version of this lesson.",
            "Look for the little square where a radius meets a tangent. That $90^\\circ$ is the given that makes HL or Pythagoras legal.",
        ],
        "A ladder leaning against a circular tank, or two tangents from a point, is this theorem. The equal-tangents fact is as useful as isosceles base angles.",
        "Mark the radius perpendicular to the tangent, then look for a $3$-$4$-$5$ or $5$-$12$-$13$ with the external point.",
        lesson_figure(
            _tangent_circ_svg(),
            "A tangent at $P$ perpendicular to radius $OP$",
            "The radius is perpendicular to the tangent at the point of contact.",
        )
        + solved(10, "A radius meets a tangent. What is the angle at the contact point?",
                 ["A tangent touches the circle at exactly one point.",
                  "The radius to that point of contact is perpendicular to the tangent.",
                  "So the angle is $90^\\circ$."],
                 "$90^\\circ$", "", "Easy")
        + solved(11, "Two tangents from a point are 7 and 3x-2. Find x.",
                 ["Two tangent segments from the same external point are congruent.",
                  "Set $3x-2=7$.",
                  "Then $3x=9$ and $x=3$."],
                 "$3$", "", "Medium")
        + solved(12, "External point is 13 from the center; radius 5. Find the tangent length.",
                 ["The radius is perpendicular to the tangent, so the triangle is right with legs $r=5$ and $t$, hypotenuse $13$.",
                  "Then $t^2+5^2=13^2$.",
                  "$t^2=169-25=144$, so $t=12$."],
                 "$12$", "", "Hard"),
        ("Treating a secant as a tangent",
         "A secant cuts the circle twice. A tangent cuts it once. Equal-tangent theorems do not apply to a secant unless you use power of a point."),
        ("Mark the right angle at the contact point",
         "That square is the whole theorem. Without it you will use an acute angle as if it were $90^\\circ$."),
        ["I can use radius ⊥ tangent.", "I can set two tangents from a point equal.", "I can find a tangent length with Pythagoras."],
        16,
    )
    c5 = concept_block(
        "5. Inscribed angle theorem",
        [
            "The inscribed-angle theorem is the half-arc rule, now used in more crowded figures: cyclic quadrilaterals, angles that intercept the same arc, and angles that intercept a diameter.",
            "Opposite angles of a cyclic quadrilateral are supplementary, because they intercept arcs that together make the whole circle.",
            "If two inscribed angles intercept the same arc, they are congruent. If they intercept a diameter, they are right angles.",
            "An inscribed angle and a central angle on the same arc still satisfy inscribed $= \\dfrac{1}{2}$ central.",
            "A quadrilateral can be inscribed in a circle if and only if a pair of opposite angles is supplementary (and then the other pair is too).",
            "Stretch items combine this with algebra: an inscribed angle $x+20$ intercepting arc $4x+10$ gives $2(x+20)=4x+10$.",
        ],
        "Cyclic quadrilateral supplementary opposites is one of the most-tested circle facts after “inscribed is half.” Mark the cyclic quad as soon as four vertices sit on the circle.",
        "Name the intercepted arc of each inscribed angle before you write an equation. Same arc $\\Rightarrow$ equal angles; opposite arcs in a cyclic quad $\\Rightarrow$ supplementary.",
        lesson_figure(
            _inscribed_svg(),
            "An inscribed angle intercepting an arc",
            "The angle is half the arc between its sides. Opposite angles in a cyclic quad would add to $180^\\circ$.",
        )
        + solved(13, "A central angle of 100° and an inscribed angle intercept the same arc. Find the inscribed angle.",
                 ["The inscribed angle is half the central angle that intercepts the same arc.",
                  "Compute $\\dfrac{1}{2}\\cdot 100=50$.",
                  "The inscribed angle is $50^\\circ$."],
                 "$50^\\circ$", "", "Easy")
        + solved(14, "A cyclic quadrilateral has an angle 80°. Find the opposite angle.",
                 ["Opposite angles of a cyclic quadrilateral are supplementary.",
                  "Compute $180-80=100$.",
                  "The opposite angle is $100^\\circ$."],
                 "$100^\\circ$", "", "Medium")
        + solved(15, "An inscribed angle is x+20 and intercepts arc 4x+10. Find x.",
                 ["Inscribed angle $=\\dfrac{1}{2}$ intercepted arc, so $2(x+20)=4x+10$.",
                  "Expand: $2x+40=4x+10$, then $30=2x$.",
                  "So $x=15$. (The angle is $35^\\circ$ and the arc is $70^\\circ$.)"],
                 "$15$", "", "Hard"),
        ("Using 360° on opposite angles of a cyclic quad",
         "Opposite angles sum to $180$, not $360$. All four interiors of the quadrilateral sum to $360$; each opposite pair takes half of that in a balanced way, but the theorem is $180$ per pair."),
        ("Same-arc inscribed angles get the same mark",
         "If two angles “see” the same arc, they are equal even if they sit on opposite sides of the circle."),
        ["I can use inscribed = half arc in crowded figures.", "I can use cyclic-quadrilateral opposites.", "I can set up algebraic inscribed-arc equations."],
        21,
    )
    c6 = concept_block(
        "6. Equations of circles",
        [
            "The standard equation of a circle with center $(h,k)$ and radius $r$ is $(x-h)^2+(y-k)^2=r^2$. This is the distance formula set equal to $r$.",
            "Center $(0,0)$ and radius $5$ is $x^2+y^2=25$. Center $(3,-2)$ and radius $4$ is $(x-3)^2+(y+2)^2=16$. Watch the sign inside the $y$ parentheses.",
            "Completing the square turns the general form $x^2+y^2+Dx+Ey+F=0$ into standard form. $x^2+y^2-6x=0$ becomes $(x-3)^2+y^2=9$.",
            "A diameter’s endpoints determine the circle: the center is the midpoint, and the radius is half the diameter (or the distance from center to an endpoint).",
            "A point $(x,y)$ lies on the circle if plugging it in makes the equation true. It lies inside if the left side is less than $r^2$.",
            "This is Unit 1’s distance formula wearing a circle. Completing the square is the only extra algebraic move.",
        ],
        "Completing the square on $x^2+y^2+Dx+Ey$ is a standard SAT circle question. If you forget to add $(D/2)^2$ to both sides, the radius comes out wrong.",
        "Read off $(h,k)$ from the parentheses with opposite signs, then take the square root of the right side for $r$. For general form, complete the square first.",
        lesson_figure(
            svg_plane(points=[(3, -2, "C"), (7, -2, "P")], lim=8, line=(3, -2, 7, -2)),
            "Center $(3,-2)$ and a point on the circle $4$ units right",
            "Radius $4$ gives $(x-3)^2+(y+2)^2=16$.",
        )
        + solved(16, "Write the equation of a circle center (0,0), radius 5.",
                 ["The standard form is $(x-h)^2+(y-k)^2=r^2$.",
                  "Here $(h,k)=(0,0)$ and $r=5$, so $r^2=25$.",
                  "The equation is $x^2+y^2=25$."],
                 "$x^2+y^2=25$", "", "Easy")
        + solved(17, "Center (3,−2), radius 4. Write the equation.",
                 ["Plug $(h,k)=(3,-2)$ into $(x-h)^2+(y-k)^2=r^2$.",
                  "Then $(x-3)^2+(y-(-2))^2=16$.",
                  "Simplify the $y$ piece: $(x-3)^2+(y+2)^2=16$."],
                 "$(x-3)^2+(y+2)^2=16$", "", "Medium")
        + solved(18, "Rewrite x²+y²+8x−6y=0 in standard form and find r.",
                 ["Complete the square: $x^2+8x$ needs $+16$, and $y^2-6y$ needs $+9$.",
                  "Add $16+9$ to both sides: $(x+4)^2+(y-3)^2=25$.",
                  "So the center is $(-4,3)$ and $r=5$."],
                 "$r=5$, center $(-4,3)$", "", "Hard"),
        ("Dropping the sign inside (y−k)",
         "Center $(3,-2)$ produces $(y-(-2))=(y+2)$, not $(y-2)$. The sign in the parentheses is the opposite of the center’s coordinate."),
        ("Complete the square on both x and y",
         "Add $(D/2)^2$ and $(E/2)^2$ to both sides. Forgetting to add them to the right side shrinks $r^2$."),
        ["I can write $(x-h)^2+(y-k)^2=r^2$.", "I can complete the square to find the center and radius.", "I can test whether a point lies on the circle."],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8
# ===========================================================================

def _u8_questions():
    rows = [
        ("A triangle with base 10 and height 6 has area…",
         30, "(1/2)·10·6=30.",
         [60, 16, 36]),
        ("A parallelogram with base 9 and height 4 has area…",
         36, "bh=36. Do not use a slanted side as height.",
         [13, 18, 26]),
        ("A trapezoid with bases 8 and 14 and height 4 has area…",
         44, "(8+14)/2·4=44.",
         [56, 32, 22]),
        ("A rhombus with diagonals 8 and 10 has area…",
         40, "(1/2)·8·10=40.",
         [80, 18, 9]),
        ("A regular hexagon with side 4 has area…",
         "24√3", "Six equilateral triangles of side 4: 6·(√3/4)·16=24√3.",
         ["16√3", 24, "8√3"]),
        ("A circle of radius 7 has area (in terms of π)…",
         "49π", "πr²=49π.",
         ["14π", "7π", "21π"]),
        ("A circle of diameter 10 has area…",
         "25π", "r=5, π·25.",
         ["10π", "100π", "50π"]),
        ("A circle of radius 6 has circumference…",
         "12π", "2πr=12π.",
         ["36π", "6π", 12]),
        ("A semicircle of radius 4 has area…",
         "8π", "(1/2)π·16=8π.",
         ["16π", "4π", "8"]),
        ("If a circle’s area is 36π, its radius is…",
         6, "r²=36, r=6.",
         [36, 18, 12]),
        ("A rectangular prism 4×3×5 has volume…",
         60, "lwh=60.",
         [12, 47, 24]),
        ("A cube of edge 5 has volume…",
         125, "5³=125.",
         [25, 15, 75]),
        ("A cylinder of radius 3 and height 4 has volume…",
         "36π", "πr²h=9π·4=36π.",
         ["12π", "24π", "36"]),
        ("A prism with triangular base area 10 and height 7 has volume…",
         70, "Bh=70.",
         [17, 35, 140]),
        ("A cube of edge 4 has surface area…",
         96, "6s²=96.",
         [64, 24, 16]),
        ("A pyramid with base area 18 and height 5 has volume…",
         30, "(1/3)Bh=30.",
         [90, 45, 15]),
        ("A cone with radius 3 and height 4 has volume…",
         "12π", "(1/3)πr²h=(1/3)π·9·4=12π.",
         ["36π", "24π", "12"]),
        ("A square pyramid with base side 6 and height 4 has volume…",
         48, "Base 36, (1/3)·36·4=48.",
         [144, 72, 24]),
        ("A cone with radius 6 and height 3 has volume…",
         "36π", "(1/3)π·36·3=36π.",
         ["108π", "18π", "36"]),
        ("Forgetting the 1/3 on a pyramid of B=12, h=6 would incorrectly give…",
         72, "Bh=72, but the true volume is 24.",
         [24, 36, 12]),
        ("A sphere of radius 3 has volume…",
         "36π", "(4/3)πr³=(4/3)π·27=36π.",
         ["12π", "108π", "9π"]),
        ("A sphere of radius 3 has surface area…",
         "36π", "4πr²=36π. Same number as volume in π units for r=3, but different dimensions.",
         ["12π", "9π", "4π"]),
        ("A sphere of diameter 4 has volume…",
         "32π/3", "r=2, (4/3)π·8=32π/3.",
         ["16π", "64π/3", "8π"]),
        ("If a sphere’s volume is 36π, then r³=27 so r=…",
         3, "(4/3)πr³=36π ⇒ r³=27.",
         [6, 9, 4]),
        ("A hemisphere of radius 3 has volume…",
         "18π", "Half of 36π.",
         ["36π", "12π", "9π"]),
        ("Vertices (0,0), (6,0), (6,4), (0,4). The polygon’s area is…",
         24, "A 6-by-4 rectangle.",
         [10, 20, 12]),
        ("Vertices (0,0), (8,0), (0,6). The triangle’s area is…",
         24, "(1/2)·8·6=24.",
         [48, 14, 10]),
        ("A segment from (0,0) to (9,6) is partitioned in the ratio 1:2 from (0,0). The point is…",
         "(3,2)", "One-third of the way: (3,2).",
         ["(6,4)", "(4.5,3)", "(9,6)"]),
        ("The midpoint of (2,−4) and (8,6) is…",
         "(5,1)", "Average: (5,1).",
         ["(10,2)", "(6,1)", "(3,5)"]),
        ("Shoelace on (0,0), (4,0), (4,3), (0,3) gives area…",
         12, "A 4-by-3 rectangle.",
         [7, 14, 6]),
        ("A kite with diagonals 12 and 9 has area…",
         54, "(1/2)·12·9=54.",
         [108, 21, 27]),
        ("An annulus between r=5 and r=3 has area…",
         "16π", "25π−9π=16π.",
         ["8π", "15π", "34π"]),
        ("A cylinder r=2, h=10. Volume?",
         "40π", "π·4·10=40π.",
         ["20π", "100π", "40"]),
        ("A cone r=4, h=9. Volume?",
         "48π", "(1/3)π·16·9=48π.",
         ["144π", "36π", "48"]),
        ("A prism 2×3×10. Volume?",
         60, "60.",
         [15, 30, 50]),
        ("A sphere r=6. Surface area?",
         "144π", "4π·36=144π.",
         ["36π", "288π", "24π"]),
        ("Triangle (0,0), (10,0), (0,8). Area?",
         40, "(1/2)·10·8=40.",
         [80, 18, 24]),
        ("Partition (0,0) to (12,9) in ratio 2:1 from the first point. The point is…",
         "(8,6)", "Two-thirds of the way: (8,6).",
         ["(4,3)", "(6,4.5)", "(12,9)"]),
        ("A cube edge 6. Volume?",
         216, "6³=216.",
         [36, 108, 72]),
        ("A pyramid B=20, h=9. Volume?",
         60, "(1/3)·20·9=60.",
         [180, 90, 30]),
        ("A trapezoid bases 5 and 11, height 4. Area?",
         32, "(16/2)·4=32.",
         [44, 16, 20]),
        ("Circle area 81π. Circumference?",
         "18π", "r=9, 2πr=18π.",
         ["9π", "81π", "162π"]),
        ("Cylinder r=5, h=2. Volume?",
         "50π", "25π·2=50π.",
         ["10π", "20π", "50"]),
        ("Sphere r=1. Volume?",
         "4π/3", "(4/3)π.",
         ["4π", "π", "2π"]),
        ("Points (1,1), (6,1), (6,4). Triangle area?",
         "7.5", "(1/2)·5·3=7.5.",
         [15, 8, 4]),
        ("A rectangular prism 3×4×12. Space diagonal?",
         13, "√(9+16+144)=√169=13.",
         [19, 12, 7]),
        ("SAT Stretch: A cone and a cylinder share r=3 and h=4. The ratio of cone volume to cylinder volume is…",
         "1:3", "Cone is one-third of the cylinder with the same r and h.",
         ["1:2", "3:1", "1:1"]),
        ("SAT Stretch: A sphere is inscribed in a cube of edge 6. The sphere’s volume is…",
         "36π", "Diameter 6, r=3, (4/3)π·27=36π.",
         ["216", "288π", "12π"]),
        ("SAT Stretch: Polygon (0,0), (6,0), (8,4), (2,4). Area?",
         24, "Vectors (6,0) and (2,4) give a parallelogram of area |6·4−0·2|=24.",
         [32, 16, 20]),
        ("SAT Stretch: A segment from A(0,0) to B(12,9) is partitioned 1:3 starting at A. The point is…",
         "(3,2.25)", "One-fourth of the way: (3, 9/4).",
         ["(4,3)", "(9,6.75)", "(6,4.5)"]),
        ("SAT Stretch: A pyramid of volume 80 has B=16. Its height is…",
         15, "(1/3)·16·h=80, 16h=240, h=15.",
         [5, 80, 20]),
        ("SAT Stretch: A cylinder’s lateral area is 48π and r=4. Then h=…",
         6, "2πrh=48π, 8h=48, h=6. Volume would then be 96π.",
         [12, 4, 8]),
        ("SAT Stretch: Composite: a hemisphere of r=3 on top of a cylinder r=3, h=4. Total volume?",
         "54π", "Cylinder 36π plus hemisphere 18π = 54π.",
         ["36π", "72π", "54"]),
        ("SAT Stretch: Shoelace (0,0), (5,0), (7,3), (2,3). Area?",
         15, "Trapezoid bases 5 and 5, height 3? Points form a parallelogram base 5 height 3, area 15.",
         [21, 10, 12]),
        ("SAT Stretch: A cube’s space diagonal is 6√3. Its volume is…",
         216, "Space diagonal s√3=6√3, s=6, volume 216.",
         ["36√3", 108, 72]),
    ]
    return _pack(rows)


def build_unit8():
    title = "Geometry Unit 8: Area, Volume & Coordinate Geometry"
    description = (
        "Polygon area, circle area, prisms and cylinders, pyramids and cones, spheres, and "
        "coordinate area with partitions."
    )
    concepts = [
        "Area of polygons",
        "Circles area review",
        "Prisms and cylinders",
        "Pyramids and cones",
        "Spheres",
        "Coordinate area and partitions",
    ]
    c1 = concept_block(
        "1. Area of polygons",
        [
            "Triangle area is $\\dfrac{1}{2}bh$, with $h$ the perpendicular height to that base — never a slanted side. "
            "Parallelogram area is $bh$ with the same warning.",
            "Trapezoid area is $\\dfrac{b_1+b_2}{2}\\cdot h$, the midsegment times height. Rhombus and kite area is "
            "$\\dfrac{1}{2}d_1 d_2$ from perpendicular diagonals.",
            "A regular hexagon of side $s$ is six equilateral triangles: area $\\dfrac{3\\sqrt{3}}{2}s^2$, or $6\\cdot\\dfrac{\\sqrt{3}}{4}s^2$.",
            "Heron’s formula and $\\dfrac{1}{2}ab\\sin C$ are optional extras; perpendicular height is the Geometry default.",
            "Always sketch the height as a dashed perpendicular. If the diagram only shows a slanted side, drop an altitude before you multiply.",
            "These plane areas become bases $B$ for the prism and pyramid volumes in the next lessons.",
        ],
        "Using a slanted side as height is the error that follows students from Grade 6 through SAT Math. Height is perpendicular, every time.",
        "Mark the right-angle box on the height, then write the matching formula. For a rhombus or kite, switch to diagonals instead of $b$ and $h$.",
        lesson_figure(
            svg_rect(10, 6, True),
            "A rectangle as the simplest polygon-area case",
            "Area $=10\\times 6=60$. A parallelogram with the same base and height has the same area.",
        )
        + solved(1, "Triangle base 10, height 6. Find the area.",
                 ["Triangle area is $\\dfrac{1}{2}bh$ with $h$ perpendicular to the chosen base.",
                  "Substitute $b=10$ and $h=6$.",
                  "Area $=\\dfrac{1}{2}\\cdot 10\\cdot 6=30$."],
                 "$30$", "", "Easy")
        + solved(2, "Trapezoid bases 8 and 14, height 4. Find the area.",
                 ["Trapezoid area is the average of the bases times the height.",
                  "The average of $8$ and $14$ is $11$.",
                  "Then $11\\cdot 4=44$."],
                 "$44$", "", "Medium")
        + solved(3, "Regular hexagon of side 4. Find the area.",
                 ["A regular hexagon is six equilateral triangles of the same side.",
                  "One equilateral triangle of side $4$ has area $\\dfrac{\\sqrt{3}}{4}\\cdot 16=4\\sqrt{3}$.",
                  "Six of them give $24\\sqrt{3}$."],
                 "$24\\sqrt{3}$", "", "Hard"),
        ("Using a slanted side as height",
         "A parallelogram’s side is not the height unless the figure is a rectangle. Drop a perpendicular."),
        ("Name the formula before the numbers",
         "Triangle half-base-height, trapezoid average-bases times height, rhombus half-diagonals. Saying the name prevents mixing them."),
        ["I can find triangle, parallelogram, and trapezoid area.", "I can use rhombus/kite diagonal area.", "I can find a regular hexagon’s area."],
        1,
    )
    c2 = concept_block(
        "2. Circles area review",
        [
            "Circle area is $\\pi r^2$. Circumference is $2\\pi r$. Diameter $d$ means $r=d/2$; do not plug the diameter into $r^2$ by accident.",
            "A semicircle has area $\\dfrac{1}{2}\\pi r^2$ and curved length $\\pi r$ (plus the diameter if you want the full perimeter).",
            "An annulus (ring) between radii $R$ and $r$ has area $\\pi(R^2-r^2)$. Factor as $\\pi(R-r)(R+r)$ if that helps.",
            "If the area is $36\\pi$, then $r^2=36$ and $r=6$. If the circumference is $10\\pi$, then $2r=10$ and $r=5$.",
            "Leave answers in terms of $\\pi$ unless a decimal is requested. Exact $\\pi$ is the course standard.",
            "Sectors were Unit 7; here the full disk is the base of cylinders and cones in the next lessons.",
        ],
        "Plugging the diameter into $\\pi r^2$ quadruples the area. Halve the diameter first, every time.",
        "Write $r=$ in the margin before you square. If you were given a diameter, that line is $r=d/2$.",
        lesson_figure(
            svg_circle(7, True),
            "A circle of radius $7$",
            "Area $49\\pi$, circumference $14\\pi$.",
        )
        + solved(4, "Radius 7. Find the area in terms of π.",
                 ["Circle area is $\\pi r^2$.",
                  "Here $r=7$, so $r^2=49$.",
                  "Area $=49\\pi$."],
                 "$49\\pi$", "", "Easy")
        + solved(5, "Diameter 10. Find the area in terms of π.",
                 ["The radius is half the diameter: $r=5$.",
                  "Then area $=\\pi r^2=\\pi\\cdot 25$.",
                  "So the area is $25\\pi$."],
                 "$25\\pi$", "", "Medium")
        + solved(6, "Area 36π. Find the circumference in terms of π.",
                 ["From $\\pi r^2=36\\pi$, cancel $\\pi$ to get $r^2=36$, so $r=6$.",
                  "Circumference is $2\\pi r$.",
                  "Then $2\\pi\\cdot 6=12\\pi$."],
                 "$12\\pi$", "", "Hard"),
        ("Using the diameter as r",
         "Diameter $10$ is not $r=10$. Area would incorrectly become $100\\pi$ instead of $25\\pi$."),
        ("Solve for r before finding the other measurement",
         "Area $\\to r^2 \\to r \\to$ circumference. Circumference $\\to r \\to$ area. Do not mix the formulas in one step."),
        ["I can compute πr² and 2πr.", "I can convert between area and circumference.", "I can handle semicircles and annuli."],
        6,
    )
    c3 = concept_block(
        "3. Prisms and cylinders",
        [
            "A prism has two congruent parallel bases. Volume is $Bh$, where $B$ is the base area and $h$ is the perpendicular height between bases.",
            "A rectangular prism is $lwh$. A cube is $s^3$. Surface area of a cube is $6s^2$; of a rectangular prism, $2(lw+lh+wh)$.",
            "A cylinder is a circular prism: $B=\\pi r^2$, so volume $\\pi r^2 h$. Lateral area is $2\\pi r h$ (the unrolled rectangle).",
            "The height is perpendicular to the bases. A slanted edge is not $h$. For an oblique prism the volume is still $Bh$ with perpendicular $h$.",
            "A net of a cylinder is two circles and a rectangle of width $2\\pi r$ and height $h$. That net is how lateral area is remembered.",
            "Prisms and cylinders use the full base $B$. Pyramids and cones in the next lesson take one-third of that product.",
        ],
        "Volume of a box is length times width times height only when the base is a rectangle. For a triangular prism, $B$ is the triangle first, then times $h$.",
        "Compute $B$ as a plane-area problem from lesson 1, then multiply by the 3-D height. Keep those two steps separate.",
        lesson_figure(
            _prism_svg("ℓ=5, w=3, h=4"),
            "A rectangular prism",
            "Volume $5\\cdot 3\\cdot 4=60$. This is a 2-D sketch of a 3-D box, not a coordinate plane.",
        )
        + solved(7, "Rectangular prism 4×3×5. Find the volume.",
                 ["Volume of a rectangular prism is length times width times height.",
                  "Compute $4\\cdot 3\\cdot 5$.",
                  "The volume is $60$."],
                 "$60$", "", "Easy")
        + solved(8, "Cylinder r=3, h=4. Find the volume in terms of π.",
                 ["Cylinder volume is $\\pi r^2 h$, the circular base area times height.",
                  "Base area $=\\pi\\cdot 9=9\\pi$.",
                  "Then $9\\pi\\cdot 4=36\\pi$."],
                 "$36\\pi$", "", "Medium")
        + solved(9, "Cube edge 4. Find the surface area.",
                 ["A cube has six square faces, each of area $s^2$.",
                  "Here $s=4$, so one face is $16$.",
                  "Surface area $=6\\cdot 16=96$."],
                 "$96$", "", "Hard"),
        ("Using a slanted edge as height",
         "Height is the perpendicular distance between bases. A space diagonal or a lateral edge is a different length."),
        ("Find B first, then multiply by h",
         "Especially for a triangular prism: area of the triangular base, then times the length of the prism."),
        ["I can compute prism volume Bh.", "I can compute cylinder volume πr²h.", "I can find cube and prism surface area."],
        11,
    )
    c4 = concept_block(
        "4. Pyramids and cones",
        [
            "A pyramid has a polygonal base and triangular lateral faces meeting at an apex. Volume is $\\dfrac{1}{3}Bh$. "
            "The $\\dfrac{1}{3}$ is the difference from a prism with the same base and height.",
            "A cone is a circular pyramid: volume $\\dfrac{1}{3}\\pi r^2 h$. Lateral area is $\\pi r\\ell$ where $\\ell$ is the slant height.",
            "Slant height $\\ell$ is the distance from the apex to a point on the base circumference along a generator. "
            "It is not $h$. Pythagoras relates $r$, $h$, and $\\ell$.",
            "Forgetting $\\dfrac{1}{3}$ triples every pyramid and cone volume. That is the most common 3-D error in the course.",
            "A square pyramid with base side $6$ and height $4$ has $B=36$ and volume $48$. A cone with $r=3$, $h=4$ has volume $12\\pi$.",
            "Cavalieri’s principle says that matching cross-sectional areas at every height give matching volumes, which is why the $\\dfrac{1}{3}$ is the same for every cone and pyramid.",
        ],
        "If a cylinder and a cone share $r$ and $h$, the cone is exactly one-third of the cylinder. That comparison is the fastest check on a multiple-choice volume item.",
        "Write the $\\dfrac{1}{3}$ before you plug in numbers. Then compute $B$, then multiply by $h$. Three written factors, not two.",
        lesson_figure(
            _cone_svg(),
            "A cone with height $h$ marked as a dashed perpendicular",
            "Volume $\\dfrac{1}{3}\\pi r^2 h$. The slanted edge is not $h$.",
        )
        + solved(10, "Pyramid B=18, h=5. Find the volume.",
                 ["Pyramid volume is $\\dfrac{1}{3}Bh$, one-third of the prism with the same base and height.",
                  "Write $\\dfrac{1}{3}\\cdot 18\\cdot 5$.",
                  "That product is $30$."],
                 "$30$", "", "Easy")
        + solved(11, "Cone r=3, h=4. Find the volume in terms of π.",
                 ["Cone volume is $\\dfrac{1}{3}\\pi r^2 h$.",
                  "First $r^2=9$, so $\\pi r^2 h=36\\pi$.",
                  "Then take one-third: $12\\pi$."],
                 "$12\\pi$", "", "Medium")
        + solved(12, "Square pyramid base side 6, height 4. Find the volume.",
                 ["The base is a square of side $6$, so $B=36$.",
                  "Volume $=\\dfrac{1}{3}Bh=\\dfrac{1}{3}\\cdot 36\\cdot 4$.",
                  "That is $48$."],
                 "$48$", "", "Hard"),
        ("Dropping the 1/3",
         "A pyramid is not a prism. Using $Bh$ instead of $\\dfrac{1}{3}Bh$ triples the volume."),
        ("Distinguish h from slant height",
         "Volume uses the perpendicular height. Lateral area of a cone uses the slant height $\\ell$."),
        ["I can compute pyramid volume (1/3)Bh.", "I can compute cone volume (1/3)πr²h.", "I can compare a cone to a cylinder with the same r and h."],
        16,
    )
    c5 = concept_block(
        "5. Spheres",
        [
            "A sphere of radius $r$ has volume $\\dfrac{4}{3}\\pi r^3$ and surface area $4\\pi r^2$. Diameter $d$ means $r=d/2$ before you cube.",
            "A hemisphere has volume $\\dfrac{2}{3}\\pi r^3$ (half the sphere) and curved surface $2\\pi r^2$. Including the circular base adds another $\\pi r^2$.",
            "For $r=3$, volume is $36\\pi$ and surface area is also $36\\pi$ numerically in $\\pi$ units — different dimensions, coincidentally the same coefficient. Do not assume that coincidence for other $r$.",
            "A sphere inscribed in a cube of edge $s$ has diameter $s$, so $r=s/2$. A sphere circumscribed about a cube has diameter equal to the cube’s space diagonal $s\\sqrt{3}$.",
            "Solving $\\dfrac{4}{3}\\pi r^3 = 36\\pi$ gives $r^3=27$, $r=3$. Cancel $\\pi$ first, then undo the $\\dfrac{4}{3}$.",
            "Composite solids (hemisphere on a cylinder) add volumes; if a piece is hollow, subtract. Name each piece before you add.",
        ],
        "Inscribed-sphere problems are diameter-from-the-cube-edge. If you use the space diagonal as the diameter of an inscribed sphere, you have described a circumscribed sphere instead.",
        "Write $r=$ from the picture (half an edge, or half a diameter) before touching $\\dfrac{4}{3}\\pi r^3$. Cubing the diameter is the usual disaster.",
        lesson_figure(
            _sphere_svg(),
            "A sphere with radius marked",
            "Volume $\\dfrac{4}{3}\\pi r^3$, surface $4\\pi r^2$.",
        )
        + solved(13, "Sphere r=3. Find the volume in terms of π.",
                 ["Sphere volume is $\\dfrac{4}{3}\\pi r^3$.",
                  "Here $r^3=27$, so $\\dfrac{4}{3}\\pi\\cdot 27$.",
                  "That simplifies to $36\\pi$."],
                 "$36\\pi$", "", "Easy")
        + solved(14, "Sphere r=3. Find the surface area in terms of π.",
                 ["Sphere surface area is $4\\pi r^2$.",
                  "Here $r^2=9$, so $4\\pi\\cdot 9$.",
                  "Surface area $=36\\pi$."],
                 "$36\\pi$", "", "Medium")
        + solved(15, "A sphere is inscribed in a cube of edge 6. Find the sphere’s volume.",
                 ["An inscribed sphere touches all six faces, so its diameter equals the cube’s edge $6$.",
                  "Then $r=3$.",
                  "Volume $=\\dfrac{4}{3}\\pi\\cdot 27=36\\pi$."],
                 "$36\\pi$", "", "Hard"),
        ("Cubing the diameter",
         "Volume uses $r^3$. Diameter $4$ means $r=2$ and $\\dfrac{4}{3}\\pi\\cdot 8=\\dfrac{32\\pi}{3}$, not $\\dfrac{4}{3}\\pi\\cdot 64$."),
        ("Cancel π, then undo 4/3",
         "From $\\dfrac{4}{3}\\pi r^3=36\\pi$, drop $\\pi$, multiply by $\\dfrac{3}{4}$, then take a cube root."),
        ["I can compute sphere volume and surface area.", "I can handle a hemisphere.", "I can inscribe a sphere in a cube."],
        21,
    )
    c6 = concept_block(
        "6. Coordinate area and partitions",
        [
            "On a grid, a rectangle or right triangle has area from base and height along the axes. A parallelogram with base $b$ along an axis and height $h$ still uses $bh$.",
            "The shoelace formula for a polygon with vertices $(x_i,y_i)$ in order (and back to the first) is "
            "$\\dfrac{1}{2}\\bigl|\\sum x_i y_{i+1}-\\sum y_i x_{i+1}\\bigr|$. It is the coordinate version of combining triangles.",
            "A point that partitions segment $AB$ in the ratio $m:n$ starting at $A$ is $\\dfrac{n\\cdot A+m\\cdot B}{m+n}$. "
            "The ratio $1:2$ from $A$ is one-third of the way to $B$.",
            "The midpoint is the $1:1$ partition. Section formula and midpoint are the same idea; midpoint is the one you already know from Unit 1.",
            "A space diagonal of a rectangular prism $a\\times b\\times c$ is $\\sqrt{a^2+b^2+c^2}$. That is Pythagoras twice: first a face diagonal, then the space diagonal.",
            "Coordinate area closes the course: every length tool (distance, midpoint, partition) and every area tool (triangle, trapezoid, shoelace) sit on one grid.",
        ],
        "Partition ratios are easy to reverse: $1:2$ from $A$ is not the midpoint. The midpoint is $1:1$. Drawing the segment and marking two hops versus one hop prevents the swap.",
        "List vertices in order around the polygon (counterclockwise) before shoelace. Repeating the first point at the end of the list is the usual reminder.",
        lesson_figure(
            svg_plane(points=[(0, 0, "A"), (6, 0, "B"), (6, 4, "C"), (0, 4, "D")], lim=7, line=(0, 0, 6, 0)),
            "A 6-by-4 rectangle on the coordinate plane",
            "Area $24$. A partition of $AB$ in the ratio $1:2$ from $A$ would sit at $(2,0)$.",
        )
        + solved(16, "Vertices (0,0), (6,0), (6,4), (0,4). Find the area.",
                 ["The four points are the corners of a rectangle aligned with the axes.",
                  "Width $6$ and height $4$.",
                  "Area $=6\\times 4=24$."],
                 "$24$", "", "Easy")
        + solved(17, "Partition (0,0) to (9,6) in the ratio 1:2 from the origin. Find the point.",
                 ["The ratio $1:2$ from $A$ means the point is $1/(1+2)=1/3$ of the way from $A$ to $B$.",
                  "One-third of the displacement $(9,6)$ is $(3,2)$.",
                  "Starting at the origin, the point is $(3,2)$."],
                 "$(3,2)$", "", "Medium")
        + solved(18, "Rectangular prism 3×4×12. Find the space diagonal.",
                 ["The space diagonal is $\\sqrt{a^2+b^2+c^2}$.",
                  "Compute $9+16+144=169$.",
                  "Then $\\sqrt{169}=13$."],
                 "$13$", "", "Hard"),
        ("Treating 1:2 as the midpoint",
         "The midpoint is $1:1$. A $1:2$ split from $A$ is closer to $A$ (one part toward $A$, two parts toward $B$)."),
        ("Walk vertices in order for shoelace",
         "Skipping around the polygon, or listing clockwise mixed with counterclockwise, flips or wrecks the signed area. Go around the fence once."),
        ["I can find polygon area on a grid.", "I can partition a segment in a given ratio.", "I can find a rectangular-prism space diagonal."],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Points, Lines, Planes & Angles', ['Undefined terms and notation', 'Segment addition and midpoint', 'Angle addition and pairs', 'Constructions overview', 'Distance on a number line', 'Coordinate distance intro']), ('Reasoning, Proof & Parallel Lines', ['Conditional statements', 'Algebraic and geometric proofs', 'Parallel lines and transversals', 'Corresponding and alternate angles', 'Perpendicular lines', 'Triangle angle sum']), ('Triangle Congruence', ['SSS and SAS', 'ASA and AAS', 'HL for right triangles', 'CPCTC', 'Isosceles triangle theorems', 'Overlapping triangles']), ('Similarity & Proportion', ['Similar polygons', 'AA, SAS, SSS similarity', 'Triangle proportionality', 'Indirect measurement', 'Dilation on the plane', 'Scale factor and area']), ('Right Triangles & Intro Trig', ['Pythagorean theorem and converse', 'Special right triangles 45-45-90', 'Special 30-60-90', 'Sine cosine tangent', 'Solving a right triangle', 'Angles of elevation and depression']), ('Quadrilaterals & Polygons', ['Parallelogram properties', 'Rectangles rhombi squares', 'Trapezoids and kites', 'Interior/exterior angle sums', 'Coordinate proofs', 'Midsegment']), ('Circles', ['Central and inscribed angles', 'Arc length and sector area', 'Chords and diameters', 'Tangent theorems', 'Inscribed angle theorem', 'Equations of circles']), ('Area, Volume & Coordinate Geometry', ['Area of polygons', 'Circles area review', 'Prisms and cylinders', 'Pyramids and cones', 'Spheres', 'Coordinate area and partitions'])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>Geometry Complete</h1>"
        f"<p><strong>For:</strong> <strong>High school Geometry</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
