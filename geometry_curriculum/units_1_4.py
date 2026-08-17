"""Deep Geometry curriculum builders — Units 1–4."""
from __future__ import annotations

from curriculum_kit import lesson_figure, svg_plane, svg_circle, svg_triangle, svg_rect

from hs_curriculum import (
    concept_block, solved, mq, xy_graph, sample_curve, number_line,
    labeled_right_triangle, unit_circle_svg, parallel_lines_transversal,
    tangent_curve_svg, practice_slots, unit_shell, fill_qs, page_break,
)
from .common import AUDIENCE, STRETCH_LABEL


def _pack(rows):
    return [mq(t, a, e, i, distractors=list(d)) for i, (t, a, e, d) in enumerate(rows, 1)]


def _planes_svg():
    return (
        '<svg viewBox="0 0 340 210" width="100%" style="max-width:340px" role="img">'
        '<polygon points="18,86 188,48 268,96 98,134" fill="#dbeafe" stroke="#1e3a8a" '
        'stroke-width="2" opacity="0.88"/>'
        '<polygon points="72,28 248,72 214,186 38,142" fill="#fde68a" stroke="#92400e" '
        'stroke-width="2" opacity="0.62"/>'
        '<line x1="86" y1="68" x2="196" y2="152" stroke="#b91c1c" stroke-width="3"/>'
        '<circle cx="118" cy="92" r="4.5" fill="#111827"/>'
        '<text x="126" y="88" font-size="13">A</text>'
        '<text x="22" y="72" font-size="13">P</text>'
        '<text x="252" y="48" font-size="13">Q</text>'
        '<text x="204" y="168" font-size="13" fill="#b91c1c">ℓ</text>'
        "</svg>"
    )


def _seg_svg(a="A", b="B", c="C", ab="5", bc="8", ac="13"):
    return (
        '<svg viewBox="0 0 360 90" width="100%" style="max-width:360px" role="img">'
        '<line x1="28" y1="42" x2="332" y2="42" stroke="#0f172a" stroke-width="3"/>'
        '<circle cx="40" cy="42" r="5" fill="#1d4ed8"/>'
        '<circle cx="150" cy="42" r="5" fill="#b91c1c"/>'
        '<circle cx="320" cy="42" r="5" fill="#1d4ed8"/>'
        f'<text x="40" y="72" text-anchor="middle" font-size="13">{a}</text>'
        f'<text x="150" y="72" text-anchor="middle" font-size="13">{b}</text>'
        f'<text x="320" y="72" text-anchor="middle" font-size="13">{c}</text>'
        f'<text x="95" y="28" text-anchor="middle" font-size="12">{ab}</text>'
        f'<text x="235" y="28" text-anchor="middle" font-size="12">{bc}</text>'
        f'<text x="180" y="88" text-anchor="middle" font-size="12">AC={ac}</text>'
        "</svg>"
    )


def _ang_pair_svg():
    return (
        '<svg viewBox="0 0 320 180" width="100%" style="max-width:320px" role="img">'
        '<line x1="20" y1="90" x2="300" y2="90" stroke="#0f172a" stroke-width="2.4"/>'
        '<line x1="160" y1="20" x2="160" y2="160" stroke="#0f172a" stroke-width="2.4"/>'
        '<path d="M 190 90 A 30 30 0 0 1 160 60" fill="none" stroke="#d97706" stroke-width="2.4"/>'
        '<path d="M 130 90 A 30 30 0 0 0 160 60" fill="none" stroke="#2563eb" stroke-width="2.4"/>'
        '<text x="186" y="68" font-size="13" fill="#b45309">1</text>'
        '<text x="118" y="68" font-size="13" fill="#1d4ed8">2</text>'
        '<text x="186" y="128" font-size="13" fill="#1d4ed8">3</text>'
        '<text x="118" y="128" font-size="13" fill="#b45309">4</text>'
        '<text x="168" y="18" font-size="12">C</text>'
        '<text x="304" y="86" font-size="12">B</text>'
        "</svg>"
    )


def _construct_svg():
    return (
        '<svg viewBox="0 0 320 200" width="100%" style="max-width:320px" role="img">'
        '<line x1="40" y1="150" x2="280" y2="150" stroke="#0f172a" stroke-width="2.4"/>'
        '<circle cx="80" cy="150" r="5" fill="#1d4ed8"/>'
        '<circle cx="240" cy="150" r="5" fill="#1d4ed8"/>'
        '<path d="M 40 150 A 90 90 0 0 1 160 70" fill="none" stroke="#7c3aed" stroke-width="1.8" '
        'stroke-dasharray="4 3"/>'
        '<path d="M 280 150 A 90 90 0 0 0 160 70" fill="none" stroke="#7c3aed" stroke-width="1.8" '
        'stroke-dasharray="4 3"/>'
        '<line x1="160" y1="36" x2="160" y2="170" stroke="#b91c1c" stroke-width="2.2"/>'
        '<text x="80" y="178" text-anchor="middle" font-size="13">A</text>'
        '<text x="240" y="178" text-anchor="middle" font-size="13">B</text>'
        '<text x="172" y="48" font-size="13" fill="#b91c1c">M</text>'
        '<text x="96" y="28" font-size="12" fill="#6d28d9">compass arcs</text>'
        "</svg>"
    )


def _ticks(x1, y1, x2, y2, n=1, color="#0f172a"):
    bits = []
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = (dx * dx + dy * dy) ** 0.5 or 1
    px, py = -dy / L * 7, dx / L * 7
    for i in range(n):
        off = (i - (n - 1) / 2) * 6
        sx, sy = mx + dx / L * off, my + dy / L * off
        bits.append(
            f'<line x1="{sx + px:.1f}" y1="{sy + py:.1f}" x2="{sx - px:.1f}" y2="{sy - py:.1f}" '
            f'stroke="{color}" stroke-width="2"/>'
        )
    return "".join(bits)


def _two_tri_svg(kind="sss"):
    """Two triangles with only the marks that match the named shortcut."""
    # Left △ABC: A(40,150), B(140,150), C(80,50). Right copy shifted +140.
    ticks = ""
    extra = ""
    if kind == "sss":
        ticks = (
            _ticks(40, 150, 140, 150, 1)
            + _ticks(180, 150, 280, 150, 1)
            + _ticks(40, 150, 80, 50, 2)
            + _ticks(180, 150, 220, 50, 2)
            + _ticks(140, 150, 80, 50, 3)
            + _ticks(280, 150, 220, 50, 3)
        )
    elif kind == "sas":
        # Sides AB and AC with included ∠A; matching copy on △DEF.
        ticks = (
            _ticks(40, 150, 140, 150, 1)
            + _ticks(180, 150, 280, 150, 1)
            + _ticks(40, 150, 80, 50, 2)
            + _ticks(180, 150, 220, 50, 2)
        )
        extra = (
            '<path d="M 62 150 A 20 20 0 0 0 50 132" fill="none" stroke="#d97706" stroke-width="2.2"/>'
            '<path d="M 202 150 A 20 20 0 0 0 190 132" fill="none" stroke="#d97706" stroke-width="2.2"/>'
        )
    elif kind == "asa":
        # ∠A, included side AB, ∠B.
        ticks = _ticks(40, 150, 140, 150, 1) + _ticks(180, 150, 280, 150, 1)
        extra = (
            '<path d="M 62 150 A 20 20 0 0 0 50 132" fill="none" stroke="#d97706" stroke-width="2.2"/>'
            '<path d="M 118 150 A 20 20 0 0 1 130 132" fill="none" stroke="#2563eb" stroke-width="2.2"/>'
            '<path d="M 202 150 A 20 20 0 0 0 190 132" fill="none" stroke="#d97706" stroke-width="2.2"/>'
            '<path d="M 258 150 A 20 20 0 0 1 270 132" fill="none" stroke="#2563eb" stroke-width="2.2"/>'
        )
    else:
        # AAS: ∠A and ∠C with non-included side AB.
        ticks = _ticks(40, 150, 140, 150, 1) + _ticks(180, 150, 280, 150, 1)
        extra = (
            '<path d="M 62 150 A 20 20 0 0 0 50 132" fill="none" stroke="#d97706" stroke-width="2.2"/>'
            '<path d="M 70 62 A 18 18 0 0 1 90 62" fill="none" stroke="#2563eb" stroke-width="2.2"/>'
            '<path d="M 202 150 A 20 20 0 0 0 190 132" fill="none" stroke="#d97706" stroke-width="2.2"/>'
            '<path d="M 210 62 A 18 18 0 0 1 230 62" fill="none" stroke="#2563eb" stroke-width="2.2"/>'
        )
    return (
        '<svg viewBox="0 0 320 180" width="100%" style="max-width:320px" role="img">'
        '<polygon points="40,150 140,150 80,50" fill="#eef2ff" stroke="#312e81" stroke-width="2"/>'
        '<polygon points="180,150 280,150 220,50" fill="#fef3c7" stroke="#92400e" stroke-width="2"/>'
        + ticks
        + extra
        + '<text x="90" y="172" text-anchor="middle" font-size="12">△ABC</text>'
        '<text x="230" y="172" text-anchor="middle" font-size="12">△DEF</text>'
        "</svg>"
    )


def _overlap_svg():
    return (
        '<svg viewBox="0 0 300 190" width="100%" style="max-width:300px" role="img">'
        '<polygon points="40,160 260,160 150,30" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>'
        '<line x1="40" y1="160" x2="220" y2="70" stroke="#b91c1c" stroke-width="2"/>'
        '<circle cx="40" cy="160" r="4" fill="#111"/>'
        '<circle cx="260" cy="160" r="4" fill="#111"/>'
        '<circle cx="150" cy="30" r="4" fill="#111"/>'
        '<circle cx="220" cy="70" r="4" fill="#b91c1c"/>'
        '<text x="28" y="178" font-size="13">A</text>'
        '<text x="262" y="178" font-size="13">B</text>'
        '<text x="154" y="22" font-size="13">C</text>'
        '<text x="228" y="68" font-size="13" fill="#b91c1c">D</text>'
        "</svg>"
    )


def _similar_svg():
    return (
        '<svg viewBox="0 0 340 190" width="100%" style="max-width:340px" role="img">'
        '<polygon points="30,160 130,160 30,70" fill="#dbeafe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="170,160 320,160 170,40" fill="#fef3c7" stroke="#92400e" stroke-width="2"/>'
        '<rect x="30" y="144" width="14" height="14" fill="none" stroke="#1e3a8a"/>'
        '<rect x="170" y="144" width="14" height="14" fill="none" stroke="#92400e"/>'
        + _ticks(30, 160, 130, 160, 1)
        + _ticks(170, 160, 320, 160, 1)
        + '<text x="80" y="178" text-anchor="middle" font-size="12">small (k=1)</text>'
        '<text x="245" y="178" text-anchor="middle" font-size="12">image (k=1.5)</text>'
        "</svg>"
    )


def _dilate_svg():
    return (
        '<svg viewBox="0 0 300 220" width="100%" style="max-width:300px" role="img">'
        '<line x1="20" y1="200" x2="280" y2="200" stroke="#0f172a"/>'
        '<line x1="40" y1="20" x2="40" y2="210" stroke="#0f172a"/>'
        '<polygon points="40,200 100,200 100,140" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<polygon points="40,200 160,200 160,80" fill="none" stroke="#b91c1c" stroke-width="2" '
        'stroke-dasharray="6 4"/>'
        '<circle cx="40" cy="200" r="4" fill="#111"/>'
        '<text x="48" y="214" font-size="12">O</text>'
        '<text x="108" y="168" font-size="12">P</text>'
        '<text x="168" y="92" font-size="12" fill="#b91c1c">P′ (k=2)</text>'
        "</svg>"
    )


def _proof_seg_svg():
    return (
        '<svg viewBox="0 0 320 100" width="100%" style="max-width:320px" role="img">'
        '<line x1="30" y1="50" x2="290" y2="50" stroke="#0f172a" stroke-width="3"/>'
        '<circle cx="40" cy="50" r="5" fill="#1d4ed8"/>'
        '<circle cx="160" cy="50" r="5" fill="#b91c1c"/>'
        '<circle cx="280" cy="50" r="5" fill="#1d4ed8"/>'
        '<text x="40" y="78" text-anchor="middle">A</text>'
        '<text x="160" y="78" text-anchor="middle">B</text>'
        '<text x="280" y="78" text-anchor="middle">C</text>'
        '<text x="100" y="32" text-anchor="middle" font-size="12">x</text>'
        '<text x="220" y="32" text-anchor="middle" font-size="12">x</text>'
        "</svg>"
    )


def _tri_sum_svg():
    return (
        '<svg viewBox="0 0 280 170" width="100%" style="max-width:280px" role="img">'
        '<polygon points="40,140 240,140 120,30" fill="#fef3c7" stroke="#0f172a" stroke-width="2"/>'
        '<path d="M 64 140 A 24 24 0 0 0 52 122" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        '<path d="M 216 140 A 24 24 0 0 1 228 122" fill="none" stroke="#2563eb" stroke-width="2"/>'
        '<path d="M 108 48 A 22 22 0 0 1 132 48" fill="none" stroke="#059669" stroke-width="2"/>'
        '<text x="72" y="128" font-size="12" fill="#b91c1c">α</text>'
        '<text x="198" y="128" font-size="12" fill="#1d4ed8">β</text>'
        '<text x="128" y="58" font-size="12" fill="#047857">γ</text>'
        '<text x="140" y="162" text-anchor="middle" font-size="12">α+β+γ=180°</text>'
        "</svg>"
    )


def _perp_svg():
    return (
        '<svg viewBox="0 0 280 160" width="100%" style="max-width:280px" role="img">'
        '<line x1="20" y1="120" x2="260" y2="120" stroke="#1e3a8a" stroke-width="3"/>'
        '<line x1="140" y1="20" x2="140" y2="140" stroke="#b91c1c" stroke-width="2.6"/>'
        '<rect x="140" y="104" width="16" height="16" fill="none" stroke="#0f172a"/>'
        '<text x="248" y="112" font-size="12">ℓ</text>'
        '<text x="148" y="18" font-size="12" fill="#b91c1c">n</text>'
        '<text x="160" y="96" font-size="12">90°</text>'
        "</svg>"
    )


def _prop_svg():
    return (
        '<svg viewBox="0 0 280 170" width="100%" style="max-width:280px" role="img">'
        '<polygon points="140,30 40,150 240,150" fill="#eef2ff" stroke="#312e81" stroke-width="2"/>'
        '<line x1="90" y1="90" x2="190" y2="90" stroke="#b91c1c" stroke-width="2.4"/>'
        '<text x="140" y="82" text-anchor="middle" font-size="12" fill="#b91c1c">DE ∥ BC</text>'
        '<text x="144" y="22">A</text><text x="28" y="166">B</text><text x="244" y="166">C</text>'
        '<text x="74" y="84">D</text><text x="196" y="84">E</text>'
        "</svg>"
    )


def _iso_svg():
    return (
        '<svg viewBox="0 0 260 170" width="100%" style="max-width:260px" role="img">'
        '<polygon points="40,150 220,150 130,30" fill="#dcfce7" stroke="#166534" stroke-width="2"/>'
        + _ticks(40, 150, 130, 30, 1)
        + _ticks(220, 150, 130, 30, 1)
        + '<path d="M 58 150 A 20 20 0 0 0 50 134" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        '<path d="M 202 150 A 20 20 0 0 1 210 134" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        '<text x="130" y="166" text-anchor="middle" font-size="12">base</text>'
        '<text x="64" y="128" font-size="12" fill="#b91c1c">=</text>'
        "</svg>"
    )


# ===========================================================================
# UNIT 1
# ===========================================================================

def _u1_questions():
    rows = [
        ("In Euclidean geometry, which of these is treated as an undefined term rather than a defined object?",
         "point", "A point, a line, and a plane are the three undefined terms; we describe them, but we do not define them from simpler objects.",
         ["rectangle", "midpoint", "volume"]),
        ("Two distinct planes that are not parallel must meet. Their intersection is always a…",
         "line", "If two distinct planes intersect, they share infinitely many points that form a straight line.",
         ["single point", "ray", "segment"]),
        ("How many noncollinear points are required to determine a unique plane?",
         3, "One point is not enough, two points determine a line, and three noncollinear points lock down exactly one plane.",
         [1, 2, 4]),
        ("If two distinct lines in a plane intersect, their intersection consists of…",
         "exactly one point", "Distinct lines cannot share two points; two shared points would force the lines to be the same line.",
         ["a segment", "two points", "a plane"]),
        ("Collinear points are points that…",
         "lie on one common line", "Collinear means “on the same line.” Coplanar means “in the same plane.”",
         ["lie in one plane only", "form a triangle", "have equal coordinates"]),
        ("Point B lies between A and C on a segment. If AB=7 and BC=11, what is AC?",
         18, "Segment Addition: AC=AB+BC=7+11=18.",
         [4, 11, 77]),
        ("M is the midpoint of RS. RM=4x−2 and MS=x+10. What is the length of RS?",
         28, "Midpoint means RM=MS, so 4x−2=x+10, 3x=12, x=4. Then RM=14 and RS=28.",
         [14, 12, 16]),
        ("Collinear points D, E, F in that order have DE=9 and DF=21. Find EF.",
         12, "E is between D and F, so DF=DE+EF and EF=21−9=12.",
         [30, 9, 15]),
        ("On a number line, J is at −3 and K is at 13. The midpoint of JK is located at…",
         5, "Midpoint is the average: (−3+13)/2=10/2=5.",
         [8, 16, -8]),
        ("Segment AB has endpoint A at 2 and midpoint M at 8. Where is endpoint B?",
         14, "M is the average of A and B: 8=(2+B)/2, so 16=2+B and B=14.",
         [5, 10, 6]),
        ("Two complementary angles measure 3x° and (2x+10)°. What is the measure of the larger angle?",
         48, "Complements sum to 90: 3x+2x+10=90, 5x=80, x=16. The angles are 48° and 42°.",
         [42, 90, 32]),
        ("Adjacent angles on a straight line measure (4x−5)° and (3x+17)°. What is the smaller angle?",
         89, "A linear pair sums to 180: 7x+12=180, 7x=168, x=24. The angles are 91° and 89°.",
         [91, 95, 85]),
        ("Vertical angles formed by two intersecting lines are always…",
         "congruent", "Vertical angles share a vertex and are opposite each other, so they have equal measure.",
         ["complementary", "adjacent", "obtuse"]),
        ("An angle measures 38°. What is the measure of its supplement?",
         142, "Supplementary angles sum to 180, so 180−38=142.",
         [52, 71, 218]),
        ("Ray BD bisects ∠ABC. If m∠ABD=2x+6 and m∠DBC=4x−10, find m∠ABC.",
         44, "A bisector splits an angle into two congruent pieces: 2x+6=4x−10, x=8. Each piece is 22°, so the whole angle is 44°.",
         [22, 16, 52]),
        ("The perpendicular bisector of a segment is the set of all points that are…",
         "equidistant from the two endpoints", "By construction, every point on the perpendicular bisector of AB satisfies PA=PB.",
         ["equidistant from the midpoint only", "on the segment AB", "closer to A than to B"]),
        ("To copy a segment AB with compass and unmarked straightedge, the first compass move is to…",
         "open the compass to length AB", "The compass stores the length. You then swing that radius from the new endpoint.",
         ["measure AB with a ruler", "draw a 90° mark", "estimate AB by eye"]),
        ("A classical angle-bisector construction produces two angles that are…",
         "congruent", "The construction copies equal arcs so the two new angles have the same measure.",
         ["complementary", "supplementary", "vertical"]),
        ("After you construct the perpendicular bisector of AB, that line meets AB at…",
         "the midpoint of AB", "The perpendicular bisector is perpendicular to AB and cuts it in half, so the intersection is the midpoint.",
         ["an endpoint of AB", "a random interior point", "a point not on AB"]),
        ("Which tool is not part of classical Euclidean constructions?",
         "a protractor", "Euclid’s tools are an unmarked straightedge and a collapsing compass. A protractor measures degrees; it does not construct.",
         ["a compass", "an unmarked straightedge", "a pencil"]),
        ("On a number line, what is the distance from −5 to 9?",
         14, "Distance is the absolute difference: |9−(−5)|=|14|=14.",
         [4, -14, 45]),
        ("Points P=−8 and Q=3 sit on a number line. The length PQ equals…",
         11, "|3−(−8)|=11.",
         [5, -5, 24]),
        ("If |x−4|=6, which pair lists both possible locations of x?",
         "-2 and 10", "Absolute value splits: x−4=6 or x−4=−6, so x=10 or x=−2.",
         ["4 and 6", "2 and 10", "-6 and 6"]),
        ("A trail marker reads 2 at the start and 19 at the finish. How many miles of trail lie between them?",
         17, "Distance = |19−2|=17.",
         [21, 10, 8]),
        ("The distance between 7 and −7 on the real line is…",
         14, "|7−(−7)|=14. Opposite numbers are twice as far apart as each is from 0.",
         [0, 7, -14]),
        ("What is the distance from (0,0) to (6,8) in the coordinate plane?",
         10, "d=√(6²+8²)=√(36+64)=√100=10. This is a 6-8-10 scaling of 3-4-5.",
         [14, 48, 7]),
        ("Find the distance from (1,2) to (4,6).",
         5, "Δx=3, Δy=4, so d=√(9+16)=5.",
         [7, 25, 3]),
        ("The distance from (−3,1) to (1,4) is…",
         5, "Δx=4, Δy=3, so d=√(16+9)=5.",
         [7, 4, 25]),
        ("Which point is 5 units from the origin and lies on the positive y-axis?",
         "(0,5)", "On the positive y-axis, x=0 and y>0. Distance from the origin is |y|, so y=5.",
         ["(5,0)", "(0,-5)", "(5,5)"]),
        ("Find the distance between (2,−1) and (2,8).",
         9, "The x-coordinates match, so this is a vertical segment of length |8−(−1)|=9.",
         [7, 10, 6]),
        ("A unique line is determined by how many distinct points (the minimum number)?",
         2, "Two distinct points determine exactly one line. One point does not; three might be collinear or not.",
         [1, 3, 4]),
        ("Noncollinear points A, B, and C lie in plane N. How many distinct planes contain all three of A, B, and C?",
         1, "Three noncollinear points determine exactly one plane.",
         [0, 2, 3]),
        ("B is between A and C with AB=x+5, BC=2x, and AC=20. What is x?",
         5, "Segment Addition: x+5+2x=20, 3x=15, x=5.",
         [15, 4, 10]),
        ("What is the midpoint of the segment with endpoints (−2,6) and (8,0)?",
         "(3,3)", "Average the coordinates: ((−2+8)/2, (6+0)/2)=(3,3).",
         ["(5,3)", "(3,6)", "(-2,0)"]),
        ("Two supplementary angles are in the ratio 2:7. The smaller angle measures…",
         40, "2k+7k=180, 9k=180, k=20. The smaller is 40°.",
         [20, 70, 80]),
        ("Vertical angles measure (5x−12)° and (3x+20)°. Find the measure of either angle.",
         68, "Vertical angles are congruent: 5x−12=3x+20, 2x=32, x=16. Then 5(16)−12=68.",
         [32, 16, 52]),
        ("Two complementary angles have measures in the ratio 1:2. The smaller angle is…",
         30, "x+2x=90, 3x=90, x=30.",
         [45, 60, 90]),
        ("The locus of points equidistant from two given points A and B is…",
         "the perpendicular bisector of AB", "That is the definition used in the perpendicular-bisector construction and theorem.",
         ["the circle with diameter AB", "the midpoint of AB only", "line AB itself"]),
        ("A runner goes from marker −12 to marker 5, then from 5 to 1. Total distance traveled?",
         21, "|5−(−12)|+|1−5|=17+4=21. Distance traveled is not net displacement.",
         [17, 13, 18]),
        ("A right triangle has vertices (0,0), (3,0), and (0,4). The hypotenuse length is…",
         5, "Legs 3 and 4 give hypotenuse 5 by the distance formula (or 3-4-5).",
         [7, 12, 4]),
        ("C is between A and B. AC=3x−1, CB=x+5, and AB=28. Find AC.",
         17, "3x−1+x+5=28, 4x+4=28, 4x=24, x=6. Then AC=17.",
         [11, 28, 6]),
        ("Ray BD is interior to ∠ABC. If m∠ABC=110° and m∠ABD=40°, then m∠DBC equals…",
         70, "Angle Addition: 40+m∠DBC=110, so m∠DBC=70.",
         [150, 40, 55]),
        ("Compute the distance from (−1,−2) to (5,6).",
         10, "Δx=6, Δy=8, d=√(36+64)=10.",
         [14, 2, 48]),
        ("Which statement is always true in Euclidean geometry?",
         "Two distinct points determine a unique line", "This is a postulates-level fact. Three points need not be collinear, and two planes need not be parallel.",
         ["Three points determine a unique line", "Two planes determine a unique point", "A line contains exactly two points"]),
        ("The midpoint of a segment is (4,−1) and one endpoint is (1,3). The other endpoint is…",
         "(7,−5)", "4=(1+x)/2 ⇒ x=7. −1=(3+y)/2 ⇒ y=−5.",
         ["(3,2)", "(5,1)", "(2.5,1)"]),
        ("Interpreted as distance, |3−(−9)| equals…",
         12, "|3+9|=12.",
         [6, -6, 27]),
        ("SAT Stretch: M is the midpoint of AB with AM=2x+7 and MB=5x−8. What is AB?",
         34, "Midpoint forces AM=MB: 2x+7=5x−8, 15=3x, x=5. Then AM=17 and AB=34.",
         [17, 15, 21]),
        ("SAT Stretch: Triangle ABC has A(−2,3), B(4,3), C(4,−1). Its perimeter is…",
         "10+2√13", "AB=6, BC=4, AC=√(6²+4²)=√52=2√13. Perimeter=10+2√13.",
         ["10", "2√13", "24"]),
        ("SAT Stretch: P is at 0 and Q is at 18 on a number line. Point R partitions PQ so that PR:RQ=1:2. The coordinate of R is…",
         6, "R is one-third of the way from 0 to 18, so R=6.",
         [9, 12, 8]),
        ("SAT Stretch: Complementary angles measure (4x+10)° and (2x+20)°. After solving, the difference of the two angles is…",
         10, "6x+30=90, 6x=60, x=10. The angles are 50° and 40°, so the difference is 10°.",
         [30, 90, 20]),
        ("SAT Stretch: The distance from (a,0) to (0,a) is 10√2, with a>0. Then a equals…",
         10, "√(a²+a²)=|a|√2=10√2, so a=10.",
         ["10√2", 5, 20]),
        ("SAT Stretch: A is at 1 and C is at 13. B is between them with AB=2·BC. The coordinate of B is…",
         9, "AB+BC=12 and AB=2·BC, so 3·BC=12, BC=4, B=13−4=9.",
         [7, 5, 10]),
        ("SAT Stretch: Ray BD is interior to ∠ABC=75°. If m∠ABD=x+15 and m∠DBC=2x, the larger of the two pieces measures…",
         40, "x+15+2x=75, 3x=60, x=20. The pieces are 35° and 40°.",
         [35, 20, 55]),
        ("SAT Stretch: Endpoints (2t,−4) and (8,6) have midpoint (5,1). What is t?",
         1, "x-midpoint: (2t+8)/2=5 ⇒ 2t+8=10 ⇒ t=1. y-midpoint checks: (−4+6)/2=1.",
         [2, 5, 3]),
        ("SAT Stretch: Point P lies on the perpendicular bisector of AB with AB=10, and P is not on AB. Triangle PAB is always…",
         "isosceles with PA=PB", "Every point on the perpendicular bisector is equidistant from A and B, so PA=PB.",
         ["equilateral", "right with hypotenuse AB", "scalene"]),
    ]
    return _pack(rows)


def build_unit1():
    title = "Geometry Unit 1: Points, Lines, Planes & Angles"
    description = (
        "Undefined terms, segment addition and midpoints, angle pairs, classical constructions, "
        "distance on a number line, and the coordinate distance formula — with matching diagrams "
        "and a hard SAT-style stretch set."
    )
    concepts = [
        "Undefined terms and notation",
        "Segment addition and midpoint",
        "Angle addition and pairs",
        "Constructions overview",
        "Distance on a number line",
        "Coordinate distance intro",
    ]
    c1 = concept_block(
        "1. Undefined terms and notation",
        [
            "Euclidean geometry begins with three undefined terms: point, line, and plane. We do not define them "
            "from simpler objects; we describe how they behave and then build every later definition on top of them.",
            "A point names a location with no size. We write a capital letter, such as $A$. A line is straight, "
            "extends forever in two directions, and is named by two of its points, as in line $AB$ or $\\overleftrightarrow{AB}$.",
            "A plane is a flat surface that extends forever. Three noncollinear points determine exactly one plane. "
            "Two distinct planes are either parallel or they intersect in a line.",
            "Collinear points lie on one common line. Coplanar points lie in one common plane. Four points in space "
            "need not be coplanar — think of a pyramid’s four vertices.",
            "Notation matters on quizzes. $\\overline{AB}$ is a segment (finite length), $\\overrightarrow{AB}$ is a ray "
            "starting at $A$ and passing through $B$, and $AB$ with no mark often means the length of that segment.",
            "These primitive objects are the vocabulary of every later unit: congruence talks about segments and angles, "
            "parallel lines live in a plane, and coordinate geometry simply puts numbers on the same points and lines.",
        ],
        "If you mix up “three points determine a plane” with “any three points are collinear,” later proofs about "
        "triangles, coplanar lines, and intersecting planes collapse. The undefined-term language is the grammar of Geometry.",
        "When a question says “determine,” ask: how many of this object are forced to exist, and is that number one? "
        "Two points force one line. Three noncollinear points force one plane. Two distinct intersecting lines force one point.",
        lesson_figure(
            _planes_svg(),
            "Planes $P$ and $Q$ intersecting in line $\\ell$",
            "Point $A$ lies on the line of intersection, so $A$ is in both planes.",
        )
        + solved(1, "Name the intersection of two distinct planes $P$ and $Q$ that are not parallel.",
                 ["Distinct planes that are not parallel must meet.",
                  "Their shared points cannot be a single point or a segment; they continue forever.",
                  "The intersection is a line."],
                 "a line", "", "Easy")
        + solved(2, "Points $A$, $B$, and $C$ are noncollinear. How many planes contain all three?",
                 ["Two points $A$ and $B$ already determine a unique line.",
                  "A third point $C$ off that line cannot sit on that same line.",
                  "There is exactly one plane containing a given line and a point not on the line, so exactly one plane contains $A$, $B$, and $C$."],
                 "1", "If the three points were collinear, infinitely many planes could contain them.", "Medium")
        + solved(3, "Line $\\ell$ lies in plane $P$. Point $Q$ is not in $P$. How many planes contain both $\\ell$ and $Q$?",
                 ["A line and a point not on the line determine a unique plane.",
                  "That plane is different from $P$, because $Q$ is not in $P$.",
                  "So there is exactly one such plane."],
                 "1", "", "Hard"),
        ("Calling a segment a line",
         "A line has no endpoints and infinite length. A segment $\\overline{AB}$ has two endpoints and a finite length $AB$. "
         "Naming the line $AB$ when the picture is clearly a segment is a notation error that later confuses midpoint and distance problems."),
        ("Translate each mark before you argue",
         "Rewrite the picture in words: “points $A,B$ on line $\\ell$, point $C$ off the line.” Then apply one postulate. "
         "Do not skip from the picture to an answer without naming whether you used two-points-determine-a-line or three-points-determine-a-plane."),
        [
            "I can name points, lines, rays, segments, and planes with correct notation.",
            "I can tell collinear from coplanar.",
            "I can state how many lines or planes are determined by a given set of points.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Segment addition and midpoint",
        [
            "If $B$ is between $A$ and $C$ on a line, the Segment Addition Postulate says $AC=AB+BC$. Betweenness is "
            "the geometric meaning of “the lengths add.”",
            "The midpoint $M$ of $\\overline{AB}$ is the point on the segment that splits it into two congruent pieces: "
            "$AM=MB$. On a number line, $M$ is the average of the two endpoint coordinates.",
            "In the coordinate plane the midpoint formula is $M=\\bigl(\\dfrac{x_1+x_2}{2},\\dfrac{y_1+y_2}{2}\\bigr)$. "
            "You average $x$ and $y$ separately; you do not average the distances.",
            "Algebra enters immediately: if $AM=3x-1$ and $MB=x+7$ and $M$ is a midpoint, set the expressions equal, "
            "solve for $x$, then substitute back to get a length. The equation uses congruence of pieces, not their sum.",
            "A common mix-up is to add the two half-expressions and call that the midpoint. Midpoint is a location "
            "(or an equal-split condition). Segment addition is a sum of lengths. Keep those jobs separate.",
            "Segment addition and midpoints are the first proof tools of the course: they justify the algebra you write "
            "in a two-column proof and they feed the distance formula in the last lesson of this unit.",
        ],
        "Almost every later length problem — triangle inequality, similar-triangle proportions, circle chords — starts "
        "by splitting a segment at a between-point or a midpoint. If Segment Addition is shaky, those chapters feel like new languages.",
        "Draw the three letters in order on a line, mark the given lengths, and write either “add the pieces” or "
        "“set the halves equal” before you touch $x$. The picture chooses the equation.",
        lesson_figure(
            _seg_svg("A", "B", "C", "5", "8", "13"),
            "B between A and C",
            "Segment Addition: $AC=AB+BC=5+8=13$.",
        )
        + solved(4, "B is between A and C, AB=5, BC=8. Find AC.",
                 ["Sketch A-B-C in that order.",
                  "Apply Segment Addition: $AC=AB+BC$.",
                  "Compute $5+8=13$."],
                 "$13$", "", "Easy")
        + solved(5, "M is the midpoint of PQ. PM=3x-1 and MQ=x+7. Find PQ.",
                 ["Midpoint means the two halves are congruent: $3x-1=x+7$.",
                  "Solve: $2x=8$, so $x=4$.",
                  "Then $PM=3(4)-1=11$, and $PQ=2\\cdot11=22$."],
                 "$22$", "After solving for $x$, always substitute to get the length the question asked for.", "Medium")
        + solved(6, "Endpoint A is at 2 and midpoint M is at 8 on a number line. Find B.",
                 ["The midpoint is the average of the endpoints: $8=\\dfrac{2+B}{2}$.",
                  "Multiply both sides by 2: $16=2+B$.",
                  "So $B=14$."],
                 "$14$", "A shortcut: B is as far beyond M as A is before M. From 2 to 8 is +6, so 8+6=14.", "Hard"),
        ("Adding halves instead of equating them",
         "If M is a midpoint and the halves are $3x-1$ and $x+7$, students sometimes write $(3x-1)+(x+7)$ and stop. "
         "That sum is the whole segment only after you know $x$. The defining equation of a midpoint is equality of the two halves."),
        ("Write the three letters in order",
         "Before algebra, write $A$-$B$-$C$ or $P$-$M$-$Q$ in the order they sit. Then either add (betweenness) or "
         "set equal (midpoint). The order on the paper prevents using the wrong postulate."),
        [
            "I can apply Segment Addition when a point is between two others.",
            "I can use the midpoint as equal halves or as an average of coordinates.",
            "I can solve for $x$ and then find the length the question asked for.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Angle addition and pairs",
        [
            "An angle is formed by two rays that share an endpoint, the vertex. We write $\\angle ABC$ with the vertex "
            "letter in the middle. The measure $m\\angle ABC$ is a number of degrees between $0$ and $180$ for the angles in this unit.",
            "If ray $BD$ lies in the interior of $\\angle ABC$, Angle Addition says $m\\angle ABC=m\\angle ABD+m\\angle DBC$. "
            "This is the angle version of Segment Addition.",
            "Complementary angles sum to $90^\\circ$. Supplementary angles sum to $180^\\circ$. A linear pair is a pair of "
            "adjacent angles whose nonshared rays form a straight line; a linear pair is always supplementary.",
            "Vertical angles are the opposite angles formed when two lines cross. Vertical angles are congruent. Adjacent "
            "angles in that picture form linear pairs, so they are supplementary, not congruent (unless each is $90^\\circ$).",
            "An angle bisector is a ray that splits an angle into two congruent angles. That gives an equation of measures, "
            "just as a midpoint gives an equation of lengths.",
            "Angle pairs are the engine of the parallel-line unit that comes next: corresponding angles, alternate interiors, "
            "and the triangle-sum theorem are all linear-pair and vertical-angle arguments in a new costume.",
        ],
        "SAT geometry items love a diagram of two crossing lines with an algebraic expression on one angle. If you instantly "
        "know “vertical ⇒ congruent” and “linear pair ⇒ supplementary,” you skip the trap of adding or subtracting 90 by habit.",
        "Name the pair first in words: complementary, supplementary, vertical, or adjacent-with-bisector. Then write the "
        "matching equation. Only after the equation is correct should you solve for $x$.",
        lesson_figure(
            _ang_pair_svg(),
            "Two lines forming vertical angles 1 and 4",
            "Angles 1 and 4 are vertical (congruent). Angles 1 and 2 are a linear pair (supplementary).",
        )
        + solved(7, "An angle measures 38°. Find its complement and its supplement.",
                 ["Complementary angles sum to $90^\\circ$, so the complement is $90-38=52$.",
                  "Supplementary angles sum to $180^\\circ$, so the supplement is $180-38=142$.",
                  "Report both: complement $52^\\circ$, supplement $142^\\circ$."],
                 "complement $52^\\circ$, supplement $142^\\circ$", "", "Easy")
        + solved(8, "Two complementary angles measure $3x^\\circ$ and $(2x+10)^\\circ$. Find the larger angle.",
                 ["Complements sum to $90$: $3x+(2x+10)=90$.",
                  "Combine: $5x+10=90$, so $5x=80$ and $x=16$.",
                  "The angles are $3(16)=48$ and $2(16)+10=42$. The larger is $48^\\circ$."],
                 "$48^\\circ$", "", "Medium")
        + solved(9, "Ray BD bisects ∠ABC. m∠ABD=2x+6 and m∠DBC=4x-10. Find m∠ABC.",
                 ["A bisector splits an angle into two congruent pieces, so set $2x+6=4x-10$.",
                  "Then $16=2x$, so $x=8$.",
                  "Each piece is $2(8)+6=22$, and Angle Addition gives $m\\angle ABC=44^\\circ$."],
                 "$44^\\circ$", "If you add $2x+6$ and $4x-10$ before equating, you are using Angle Addition without the bisector condition.", "Hard"),
        ("Treating vertical angles as supplementary",
         "When two lines cross, the adjacent pair is the linear pair (sums to 180). The opposite pair is vertical (equal measures). "
         "Using 180 on vertical angles, or setting adjacent angles equal, is the most common angle-pair error on quizzes."),
        ("Label the pair before the algebra",
         "Write “vertical ⇒ set equal” or “linear pair ⇒ sum to 180” as a short note next to the diagram. That one sentence "
         "prevents solving the wrong equation with perfect arithmetic."),
        [
            "I can use Angle Addition when a ray is in the interior.",
            "I can identify complementary, supplementary, linear-pair, and vertical angles.",
            "I can solve algebraic angle-pair equations and then report the measure asked for.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Constructions overview",
        [
            "Classical constructions use only an unmarked straightedge and a compass. The compass copies a radius; the "
            "straightedge draws the unique line through two points. A protractor and a marked ruler are not allowed in this game.",
            "Copying a segment means opening the compass to length $AB$ and swinging that same radius from a new endpoint. "
            "You have transferred a length without measuring it in inches or centimeters.",
            "The perpendicular bisector of $\\overline{AB}$ is constructed by swinging equal arcs from $A$ and from $B$ and "
            "connecting the two intersection points of those arcs. The new line is perpendicular to $AB$ and cuts it at its midpoint.",
            "That construction is also a theorem: the perpendicular bisector is exactly the set of points equidistant from "
            "$A$ and $B$. Later, that fact proves that a point on the bisector of a segment forms an isosceles triangle.",
            "An angle bisector is constructed by swinging an arc through both rays, then from those two intersection points "
            "swinging equal arcs and drawing the ray through the new intersection. The two smaller angles are congruent.",
            "You will not be asked to film a compass on a computer quiz, but you will be asked what a construction produces "
            "and why: midpoint, right angle, equal distances, or congruent angles. Those are the properties to memorize.",
        ],
        "Constructions are how Geometry earns its theorems without coordinates. The perpendicular-bisector theorem, the "
        "angle-bisector theorem, and later the circumcenter of a triangle all grow from these four compass moves.",
        "For each named construction, memorize the output property, not the hand motion: copy-a-segment ⇒ equal lengths; "
        "perpendicular bisector ⇒ midpoint and $90^\\circ$ and equal distances; angle bisector ⇒ two congruent angles.",
        lesson_figure(
            _construct_svg(),
            "Perpendicular bisector of $AB$",
            "Equal compass arcs from $A$ and $B$ meet; the line through those intersections hits $AB$ at its midpoint $M$.",
        )
        + solved(10, "What point do you obtain where the perpendicular bisector of AB meets AB?",
                 ["The perpendicular bisector is perpendicular to AB.",
                  "By construction it also cuts AB in half.",
                  "The intersection is the midpoint of AB."],
                 "the midpoint of AB", "", "Easy")
        + solved(11, "A point P lies on the perpendicular bisector of AB. What can you conclude about PA and PB?",
                 ["The perpendicular bisector is the locus of points equidistant from A and B.",
                  "Therefore $PA=PB$."],
                 "$PA=PB$", "Triangle PAB is isosceles with vertex P.", "Medium")
        + solved(12, "Why is a protractor not a Euclidean construction tool?",
                 ["Euclid’s postulates allow a straightedge (no marks) and a compass (copy a radius).",
                  "A protractor measures a number of degrees; it does not create a congruent angle from equal radii.",
                  "So a protractor is a measuring device, not a construction tool."],
                 "It measures degrees instead of copying equal radii.", "", "Hard"),
        ("Thinking “close enough” is a construction",
         "Sketching a right angle by eye, or copying a length with a ruler’s numbers, is not a construction. The compass "
         "must transfer a radius, and the straightedge must connect existing points. Estimation is a drawing, not a proof."),
        ("Name the property the construction guarantees",
         "After you picture the arcs, write the guaranteed property in one line: “equal distances,” “90° at the midpoint,” "
         "or “two congruent angles.” Questions almost always ask for that property, not for the sequence of hand moves."),
        [
            "I can name the tools of classical constructions.",
            "I can state what the perpendicular-bisector construction produces.",
            "I can connect a construction to the property it guarantees (equal lengths or equal angles).",
        ],
        16,
    )
    c5 = concept_block(
        "5. Distance on a number line",
        [
            "On a number line, the distance between points with coordinates $a$ and $b$ is $|a-b|$. Absolute value turns "
            "a subtraction into a length, which cannot be negative.",
            "Order does not matter: $|7-(-2)|=|-2-7|=9$. Distance is symmetric. Directed travel (left versus right) is "
            "signed; length is not.",
            "The equation $|x-c|=d$ means $x$ is $d$ units from $c$, so $x=c+d$ or $x=c-d$. Geometrically those are two "
            "points on the line at equal distance from the center $c$.",
            "A midpoint on a number line is the average of the two coordinates, which is also the point halfway in distance. "
            "Both views agree because distance is $|a-b|$ and halfway is adding half that length with the correct sign.",
            "When a path visits several markers, total distance traveled is the sum of the absolute hops, not the absolute "
            "value of the net change. Going from 2 to 9 and back to 4 travels $7+5=12$, even though the net change is only $2$.",
            "Number-line distance is the one-dimensional case of the coordinate distance formula in the next lesson: "
            "$\\sqrt{(x_2-x_1)^2}$ is exactly $|x_2-x_1|$.",
        ],
        "Absolute value as distance is the bridge from Algebra 1 into Geometry’s coordinate plane. Every later “how far” "
        "question is this idea, just in more dimensions.",
        "Translate every number-line sentence into $|\\text{end}-\\text{start}|$. If the problem is a two-location equation "
        "like $|x-4|=6$, split into two ordinary equations immediately.",
        lesson_figure(
            number_line(-6, 10, closed=[(-5, "A"), (9, "B")], shade=("between", -5, 9)),
            "Distance from $A=-5$ to $B=9$",
            "The shaded gap has length $|9-(-5)|=14$.",
        )
        + solved(13, "Find the distance from -5 to 9 on a number line.",
                 ["Distance is the absolute difference: $|9-(-5)|$.",
                  "Simplify: $|14|=14$."],
                 "$14$", "", "Easy")
        + solved(14, "Solve |x-4|=6 for both locations of x.",
                 ["Split: $x-4=6$ or $x-4=-6$.",
                  "So $x=10$ or $x=-2$."],
                 "$x=-2$ or $x=10$", "Both points sit 6 units from 4.", "Medium")
        + solved(15, "A runner goes from marker -12 to 5, then to 1. Find the total distance traveled.",
                 ["First hop: $|5-(-12)|=17$.",
                  "Second hop: $|1-5|=4$.",
                  "Total distance: $17+4=21$."],
                 "$21$", "Net change is $|1-(-12)|=13$, which is not the distance traveled.", "Hard"),
        ("Dropping the absolute value",
         "Computing $2-9=-7$ and reporting $-7$ as a length is the classic error. Length is $|2-9|=7$. If a multiple-choice "
         "option is negative, it is almost never a distance."),
        ("Split absolute-value equations into two signed cases",
         "Write both $x-c=d$ and $x-c=-d$ every time. Checking both on the number line (dots on each side of $c$) catches "
         "the case you would otherwise forget."),
        [
            "I can compute $|a-b|$ as a length.",
            "I can solve $|x-c|=d$ as two points.",
            "I can add hops to get distance traveled, not just net change.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Coordinate distance intro",
        [
            "In the coordinate plane, the distance between $A(x_1,y_1)$ and $B(x_2,y_2)$ is "
            "$d=\\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$. This is the Pythagorean theorem on the right triangle whose legs are "
            "the horizontal and vertical changes.",
            "The differences $x_2-x_1$ and $y_2-y_1$ may be negative, but they are squared, so the sign disappears. "
            "You may subtract in either order.",
            "When the points share an $x$-coordinate, the segment is vertical and $d=|y_2-y_1|$. When they share a "
            "$y$-coordinate, the segment is horizontal and $d=|x_2-x_1|$. The full formula still works; it just has a zero in one square.",
            "A 3-4-5 triangle is the most common SAT distance in disguise: $(0,0)$ to $(6,8)$ is $10$, because both legs "
            "were doubled. Recognizing multiples of 3-4-5 or 5-12-13 saves a radical.",
            "The midpoint formula from earlier still applies in two dimensions: average $x$, average $y$. Distance and "
            "midpoint answer different questions — how long versus where is the middle.",
            "This formula returns in Unit 3 (to compare sides for SSS), Unit 6 (coordinate proofs of parallelograms), "
            "Unit 7 (equations of circles), and Unit 8 (polygon area by coordinates). Learn it as a right-triangle picture, not as a string of letters.",
        ],
        "Coordinate geometry is Geometry with a grid. Once distance is automatic, you can prove congruence, compute "
        "perimeters, and write circle equations without a compass.",
        "Sketch a tiny right triangle using the two legs $\\Delta x$ and $\\Delta y$, then apply Pythagoras. If you see "
        "3 and 4, or 5 and 12, name the hypotenuse from memory and then confirm with the formula.",
        lesson_figure(
            svg_plane(points=[(0, 0, "A(0,0)"), (6, 8, "B(6,8)")], lim=9, line=(0, 0, 6, 8)),
            "Distance from $A(0,0)$ to $B(6,8)$",
            "Legs $6$ and $8$ give hypotenuse $10$.",
        )
        + solved(16, "Find the distance from (0,0) to (6,8).",
                 ["$\\Delta x=6$, $\\Delta y=8$.",
                  "$d=\\sqrt{6^2+8^2}=\\sqrt{36+64}=\\sqrt{100}=10$."],
                 "$10$", "A scaled 3-4-5 triangle.", "Easy")
        + solved(17, "Find the distance from (1,2) to (4,6).",
                 ["$\\Delta x=3$, $\\Delta y=4$.",
                  "$d=\\sqrt{9+16}=\\sqrt{25}=5$."],
                 "$5$", "", "Medium")
        + solved(18, "Find the distance from (2,-1) to (2,8).",
                 ["The $x$-coordinates are equal, so the segment is vertical.",
                  "$d=|8-(-1)|=9$.",
                  "The full formula gives $\\sqrt{0^2+9^2}=9$ as well."],
                 "$9$", "", "Hard"),
        ("Adding the legs instead of using Pythagoras",
         "From $(0,0)$ to $(6,8)$, adding $6+8=14$ is the taxicab path along the axes, not the straight-line (Euclidean) "
         "distance. Straight-line distance squares, adds, and takes a square root."),
        ("Build the right triangle on the grid",
         "Plot both points, drop a vertical and a horizontal, and label the legs before you write the formula. Seeing "
         "the 3-4-5 (or 6-8-10) picture prevents arithmetic slips inside the radical."),
        [
            "I can use $d=\\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$.",
            "I can simplify vertical and horizontal cases as absolute differences.",
            "I can recognize 3-4-5 and 5-12-13 distances on the grid.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2
# ===========================================================================

def _u2_questions():
    rows = [
        ("The converse of “If a figure is a square, then it is a rectangle” is…",
         "If a figure is a rectangle, then it is a square",
         "The converse swaps hypothesis and conclusion. It is false, because a non-square rectangle exists.",
         ["If a figure is not a square, then it is not a rectangle",
          "If a figure is not a rectangle, then it is not a square",
          "A figure is a square if and only if it is a rectangle"]),
        ("The inverse of “If it rains, then the game is delayed” is…",
         "If it does not rain, then the game is not delayed",
         "The inverse negates both parts. It is not logically equivalent to the original.",
         ["If the game is delayed, then it rains",
          "If the game is not delayed, then it does not rain",
          "The game is delayed if and only if it rains"]),
        ("Which statement is logically equivalent to a given conditional?",
         "its contrapositive",
         "A conditional and its contrapositive are always both true or both false. Converse and inverse are equivalent to each other, not to the original.",
         ["its converse", "its inverse", "its negation"]),
        ("A counterexample to “If a quadrilateral has four right angles, then it is a square” is a…",
         "nonsquare rectangle",
         "A rectangle that is not a square has four right angles but is not a square, so it kills the conditional.",
         ["rhombus that is not a square", "trapezoid", "circle"]),
        ("The hypothesis of “If two angles are vertical, then they are congruent” is…",
         "two angles are vertical",
         "The hypothesis is the “if” clause. The conclusion is “they are congruent.”",
         ["they are congruent", "the angles are adjacent", "the lines are parallel"]),
        ("Given 3x+5=20, the next justified step toward x=5 is…",
         "subtract 5 from both sides",
         "Subtraction Property of Equality: 3x=15, then Division Property gives x=5.",
         ["divide both sides by 5 first", "add 5 to both sides", "subtract 20"]),
        ("In a two-column proof, the right column lists…",
         "reasons (definitions, postulates, theorems, properties)",
         "The left column is statements. Each statement needs a reason.",
         ["only the given facts", "the picture labels", "guesses"]),
        ("If AB=CD and CD=EF, then AB=EF by which property of equality?",
         "Transitive",
         "Transitive: if a=b and b=c then a=c. Substitution would also be accepted in some books, but the named property here is Transitive.",
         ["Reflexive", "Symmetric", "Distributive"]),
        ("AB=AB is justified by the…",
         "Reflexive Property",
         "Every quantity equals itself. Reflexive is the usual first step in overlapping-triangle proofs.",
         ["Symmetric Property", "Transitive Property", "Segment Addition"]),
        ("If m∠1=m∠2, then m∠2=m∠1 by the…",
         "Symmetric Property",
         "Symmetric: if a=b then b=a. Order of an equality can be flipped.",
         ["Reflexive Property", "Addition Property", "Angle Addition"]),
        ("Two parallel lines are cut by a transversal. A pair of corresponding angles measures 70° and (3x+10)°. Find x.",
         20, "Corresponding angles are congruent, so 3x+10=70, 3x=60, x=20.",
         [30, "80/3", 10]),
        ("Lines ℓ ∥ m, transversal t. If an interior angle on the same side of t is 110°, the other same-side interior is…",
         70, "Same-side interior angles are supplementary: 180−110=70.",
         [110, 20, 250]),
        ("If two lines are cut by a transversal so that a pair of alternate interior angles is congruent, then the lines are…",
         "parallel",
         "This is the converse of the alternate-interior theorem, a standard way to prove lines parallel.",
         ["perpendicular", "skew", "intersecting"]),
        ("In the parallel-lines diagram, corresponding angles 1 and 2 are marked. If m∠1=65°, then m∠2=…",
         65, "Corresponding angles formed by parallel lines and a transversal are congruent.",
         [115, 25, 90]),
        ("A transversal crosses parallel lines. One acute angle is 40°. An angle adjacent to it on the straight line is…",
         140, "Adjacent angles on a straight line form a linear pair: 180−40=140.",
         [40, 50, 90]),
        ("Corresponding angles are in the same relative position at each intersection. If ℓ ∥ m and a corresponding pair is 2x-4 and 50, then x=…",
         27, "2x−4=50, 2x=54, x=27.",
         [23, 54, 46]),
        ("Alternate interior angles lie between the parallel lines on opposite sides of the transversal. If one is 3x+6 and the other is 54, then x=…",
         16, "They are congruent: 3x+6=54, 3x=48, x=16.",
         [18, 20, 12]),
        ("Same-side interior angles are supplementary. If they measure 2x and 4x+30, then the smaller is…",
         50, "2x+(4x+30)=180, 6x=150, x=25. The angles are 50° and 130°.",
         [100, 30, 75]),
        ("If corresponding angles are 5x-8 and 3x+20, and the lines are parallel, x equals…",
         14, "5x−8=3x+20, 2x=28, x=14.",
         [6, 28, 12]),
        ("A pair of alternate exterior angles formed by parallel lines measures 80°. The other alternate exterior angle is…",
         80, "Alternate exterior angles are congruent when lines are parallel.",
         [100, 10, 160]),
        ("Two lines that intersect to form a right angle are…",
         "perpendicular",
         "Definition of perpendicular lines: they meet at 90°.",
         ["parallel", "skew", "corresponding"]),
        ("If n ⊥ ℓ and n ⊥ m, with ℓ and m coplanar, then ℓ and m are…",
         "parallel",
         "Two lines in a plane that are both perpendicular to the same line are parallel to each other.",
         ["perpendicular to each other", "skew", "the same line"]),
        ("The slopes of two perpendicular (nonvertical) lines in the coordinate plane are…",
         "negative reciprocals",
         "If one slope is 2, the other is −1/2. The product of the slopes is −1.",
         ["equal", "reciprocals with the same sign", "always 0 and undefined"]),
        ("A right angle measures…",
         90, "By definition, a right angle measures 90°.",
         [45, 180, 60]),
        ("If two adjacent angles formed by intersecting lines are congruent, each measures…",
         90, "The adjacent pair is a linear pair, so 2x=180, x=90. The lines are perpendicular.",
         [45, 60, 180]),
        ("The sum of the interior angles of any triangle is…",
         180, "Triangle Angle Sum Theorem: the three interior angles add to 180°.",
         [90, 360, 270]),
        ("A triangle has angles 50° and 60°. The third angle is…",
         70, "180−50−60=70.",
         [80, 110, 10]),
        ("An exterior angle of a triangle equals the sum of the two remote interior angles. If those interiors are 40° and 65°, the exterior is…",
         105, "Exterior Angle Theorem: 40+65=105.",
         [25, 75, 155]),
        ("In right triangle ABC with right angle at C, if A=35°, then B=…",
         55, "The acute angles of a right triangle are complementary: 90−35=55.",
         [35, 145, 45]),
        ("A triangle has two angles of 50° each. It must be…",
         "isosceles",
         "Base angles equal ⇒ the sides opposite them are equal, so the triangle is isosceles. It is not equilateral unless all three angles are 60°.",
         ["equilateral", "right", "obtuse"]),
        ("Which pair of statements is equivalent?",
         "a conditional and its contrapositive",
         "They always share a truth value. The converse is not equivalent to the original.",
         ["a conditional and its converse", "a converse and a negation", "an inverse and a given fact"]),
        ("If 2(x+4)=18, a correct next statement in an algebraic proof is…",
         "x+4=9",
         "Division Property (or Distributive then Subtraction). Dividing both sides by 2 yields x+4=9.",
         ["2x+4=18", "x+4=18", "x=18"]),
        ("Parallel lines, transversal: corresponding angles (x+12)° and 3x°. Find the measure of each.",
         18, "x+12=3x, 12=2x, x=6. Each corresponding angle measures 18°.",
         [6, 12, 24]),
        ("ℓ ∥ m. Same-side interior angles are 2x+10 and 3x. The larger of those two angles is…",
         102, "5x+10=180, 5x=170, x=34. The angles are 78° and 102°.",
         [78, 34, 90]),
        ("To prove ℓ ∥ m, it is enough to show that a pair of alternate interior angles is…",
         "congruent",
         "The converse of the alternate-interior theorem is a parallel-line test.",
         ["supplementary", "complementary", "adjacent"]),
        ("Two lines with slopes 3/4 and −4/3 in the coordinate plane are…",
         "perpendicular",
         "(3/4)·(−4/3)=−1, so the slopes are negative reciprocals.",
         ["parallel", "neither parallel nor perpendicular", "the same line"]),
        ("A triangle has angles (2x)°, (3x)°, and (4x)°. The largest angle measures…",
         80, "9x=180, x=20. The angles are 40°, 60°, and 80°.",
         [20, 60, 90]),
        ("An exterior angle is 120° and one remote interior is 50°. The other remote interior is…",
         70, "120=50+other, so the other is 70°.",
         [170, 50, 30]),
        ("If a transversal is perpendicular to one of two parallel lines, it is perpendicular to…",
         "the other parallel line as well",
         "Corresponding (or alternate interior) angles would both be 90°.",
         ["neither line", "a third unrelated line", "only the first line"]),
        ("The contrapositive of “If two lines are parallel, then corresponding angles are congruent” is…",
         "If corresponding angles are not congruent, then the two lines are not parallel",
         "Negate both parts and swap them.",
         ["If corresponding angles are congruent, then the lines are parallel",
          "If the lines are not parallel, then corresponding angles are not congruent",
          "If the lines are parallel, then corresponding angles are not congruent"]),
        ("In an algebraic proof, 5x−7=18 followed by 5x=25 uses the…",
         "Addition Property of Equality",
         "Adding 7 to both sides is the Addition Property.",
         ["Multiplication Property", "Distributive Property", "Reflexive Property"]),
        ("Parallel lines cut by a transversal form eight angles. If one is 50°, how many of the eight measure 50°?",
         4, "The four acute angles are 50° and the four obtuse angles are 130°.",
         [2, 1, 8]),
        ("A right triangle has acute angles in the ratio 1:2. The smallest angle is…",
         30, "x+2x=90, 3x=90, x=30.",
         [45, 60, 90]),
        ("If m∠A=m∠B and m∠B=m∠C in triangle ABC, the triangle is…",
         "equilateral",
         "All three angles equal 60°, so all three sides are equal.",
         ["scalene", "right", "obtuse"]),
        ("Same-side interior angles of 3x-5 and x+25 are formed by parallel lines. Find x.",
         40, "3x−5+x+25=180, 4x+20=180, 4x=160, x=40.",
         [45, 20, 32]),
        ("A triangle has a 90° angle and a 90° angle. This is…",
         "impossible",
         "Angle sum would already be 180° with no room for a third positive angle.",
         ["a right isosceles triangle", "a straight line", "an equilateral triangle"]),
        ("SAT Stretch: “If a triangle is equilateral, then it is isosceles.” A true related statement that is equivalent is…",
         "If a triangle is not isosceles, then it is not equilateral",
         "That is the contrapositive. The converse (“if isosceles then equilateral”) is false.",
         ["If a triangle is isosceles, then it is equilateral",
          "If a triangle is not equilateral, then it is not isosceles",
          "Every isosceles triangle is equilateral"]),
        ("SAT Stretch: ℓ ∥ m. Same-side interiors measure (5x−20)° and (3x+40)°. The acute corresponding copy of the smaller interior is…",
         80, "5x−20+3x+40=180, 8x=160, x=20. The interiors are 80° and 100°. Every angle corresponding to the 80° interior is also 80°.",
         [70, 100, 60]),
        ("SAT Stretch: An exterior angle of a triangle is (2x+20)° and the remote interiors are 50° and x°. The interior angle adjacent to that exterior angle measures…",
         100, "Exterior Angle Theorem: 50+x=2x+20, so x=30. The exterior is 80°, and the adjacent interior is 180−80=100.",
         [80, 30, 50]),
        ("SAT Stretch: Nonvertical lines are perpendicular, and one slope is 2/5. The other slope must be…",
         "-5/2", "Negative reciprocals: flip 2/5 and change the sign to get −5/2.",
         ["5/2", "-2/5", "2/5"]),
        ("SAT Stretch: ℓ ∥ m with corresponding angles (7x−4)° and (5x+12)°. The linear-pair partner of those corresponding angles measures…",
         128, "7x−4=5x+12, 2x=16, x=8. Each corresponding angle is 52°, so a linear-pair partner is 128°.",
         [52, 8, 64]),
        ("SAT Stretch: In a two-column proof whose last reason is the Corresponding Angles Converse, the last statement must conclude that…",
         "the two lines are parallel",
         "The converse of “parallel ⇒ corresponding angles congruent” is the test that corresponding angles congruent ⇒ the lines are parallel.",
         ["the angles are supplementary", "the transversal is perpendicular", "the angles are vertical"]),
        ("SAT Stretch: A right triangle has acute angles x° and 2x°. The smallest angle measures…",
         30, "The acute angles of a right triangle are complementary: x+2x=90, x=30.",
         [45, 60, 90]),
        ("SAT Stretch: A transversal cuts two lines so same-side interiors are (2x+10)° and (4x−10)°. For the lines to be parallel, x must equal…",
         30, "Converse of same-side interiors: 2x+10+4x−10=180, 6x=180, x=30.",
         [20, 36, 15]),
        ("SAT Stretch: All three of n, ℓ, and m are coplanar. If n ⊥ ℓ and ℓ ∥ m, then n and m…",
         "are perpendicular",
         "A line perpendicular to one of two parallels is perpendicular to the other. So n ⊥ m.",
         ["are parallel", "must coincide", "cannot be compared"]),
    ]
    return _pack(rows)


def build_unit2():
    title = "Geometry Unit 2: Reasoning, Proof & Parallel Lines"
    description = (
        "Conditionals and logic, algebraic and geometric proofs, parallel lines with a transversal, "
        "corresponding and alternate angles, perpendicular lines, and the triangle angle-sum theorem."
    )
    concepts = [
        "Conditional statements",
        "Algebraic and geometric proofs",
        "Parallel lines and transversals",
        "Corresponding and alternate angles",
        "Perpendicular lines",
        "Triangle angle sum",
    ]
    c1 = concept_block(
        "1. Conditional statements",
        [
            "A conditional statement has the form “If $p$, then $q$.” The hypothesis is $p$ (the “if” part) and the "
            "conclusion is $q$ (the “then” part). Geometry theorems are almost all conditionals.",
            "The converse swaps $p$ and $q$: “If $q$, then $p$.” The converse of a true theorem can be false. “If a figure "
            "is a square, then it is a rectangle” is true; the converse is not.",
            "The inverse negates both parts: “If not $p$, then not $q$.” The contrapositive swaps and negates: “If not $q$, "
            "then not $p$.” A conditional and its contrapositive are logically equivalent — always true together or false together.",
            "A biconditional, “$p$ if and only if $q$,” means both the conditional and the converse are true. Definitions "
            "in Geometry are written as biconditionals: a triangle is equilateral if and only if all three sides are congruent.",
            "A counterexample is a single specific case where the hypothesis is true and the conclusion is false. One "
            "nonsquare rectangle kills “four right angles ⇒ square.”",
            "You will use this language in every proof: the Givens are a hypothesis, the Prove statement is a conclusion, "
            "and the converse of a parallel-line theorem is how you prove lines are parallel.",
        ],
        "SAT and honors proofs often ask which statement is equivalent to a given theorem. If you grab the converse by "
        "habit, you prove the wrong direction. Contrapositive is the safe twin of the original.",
        "For any “if-then,” write four one-line versions: original, converse, inverse, contrapositive. Mark which two "
        "are equivalent. Then hunt for a counterexample to the converse if the problem asks whether it is true.",
        lesson_figure(
            _ang_pair_svg(),
            "A picture that supports “If two angles are vertical, then they are congruent”",
            "Angles 1 and 4 are vertical. The converse would claim that congruent angles must be vertical — which is false.",
        )
        + solved(19, "Write the converse of “If two angles are vertical, then they are congruent.”",
                 ["Hypothesis $p$: two angles are vertical. Conclusion $q$: they are congruent.",
                  "Converse: If two angles are congruent, then they are vertical.",
                  "That converse is false (two 40° angles in different triangles need not be vertical)."],
                 "If two angles are congruent, then they are vertical.", "", "Easy")
        + solved(20, "Which statement is equivalent to “If it is a square, then it is a rectangle”?",
                 ["The equivalent partner is the contrapositive.",
                  "Contrapositive: If it is not a rectangle, then it is not a square.",
                  "The converse (“if rectangle then square”) is false."],
                 "If it is not a rectangle, then it is not a square.", "", "Medium")
        + solved(21, "Give a counterexample to “If a quadrilateral has four right angles, then it is a square.”",
                 ["The hypothesis requires four right angles.",
                  "A rectangle that is not a square has four right angles but unequal adjacent sides.",
                  "That rectangle is a counterexample."],
                 "any nonsquare rectangle", "", "Hard"),
        ("Treating the converse as automatically true",
         "Theorems do not come with free converses. Parallel lines ⇒ congruent corresponding angles is true; the converse "
         "is a different theorem that must be quoted separately when you want to prove lines parallel."),
        ("Write all four forms before you choose",
         "On a matching question, scribble original / converse / inverse / contrapositive in a tiny table. Equivalence "
         "is always original with contrapositive, and converse with inverse."),
        [
            "I can identify hypothesis and conclusion.",
            "I can write converse, inverse, and contrapositive.",
            "I can give a counterexample to a false conditional.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Algebraic and geometric proofs",
        [
            "A proof is a sequence of statements, each justified by a definition, postulate, theorem, or property of "
            "equality or congruence. Geometry uses the same equality properties you used in Algebra 1.",
            "The Addition, Subtraction, Multiplication, and Division Properties of Equality let you do the same operation "
            "to both sides. The Distributive Property expands $a(b+c)$. Reflexive, Symmetric, and Transitive Properties "
            "handle $a=a$, swapping, and chaining.",
            "A two-column proof puts statements on the left and reasons on the right. The first statements are usually "
            "Given. The last statement is the Prove goal. Every line except the givens needs a reason that names a real rule.",
            "A geometric proof about segments or angles often starts with Reflexive ($AB=AB$ or $\\angle 1\\cong\\angle 1$) "
            "when a side or angle is shared. Shared parts are the quiet heroes of overlapping-triangle proofs in Unit 3.",
            "Substitution lets you replace a quantity with an equal quantity. Transitive says if $a=b$ and $b=c$ then $a=c$. "
            "In many classrooms those two reasons are used almost interchangeably for numbers; follow your teacher’s preference, but know both names.",
            "The point of practicing algebraic proofs first is to make the later geometric proofs feel like the same sport: "
            "one legal move per line, no unexplained jumps, and a clear last sentence that matches the Prove box.",
        ],
        "When a test says “Complete the proof,” the missing reason is almost always a named property (Reflexive, Vertical "
        "Angles, Linear Pair, Corresponding Angles) rather than a new calculation. Knowing the names is the whole skill.",
        "Read the Prove line first, then the picture, then the Givens. Work backwards one step: “What would let me say "
        "that last line?” Fill that reason, then repeat. Forward writing comes after the backwards plan.",
        lesson_figure(
            _proof_seg_svg(),
            "A segment diagram for an algebraic length proof",
            "If $AB=BC=x$ and $AC=12$, Segment Addition plus algebra gives $x=6$.",
        )
        + solved(22, "Justify the step from 3x+5=20 to 3x=15.",
                 ["Subtract 5 from both sides.",
                  "That is the Subtraction Property of Equality."],
                 "Subtraction Property of Equality", "", "Easy")
        + solved(23, "If AB=CD and CD=EF, why is AB=EF?",
                 ["The two givens chain through the common length CD.",
                  "Transitive Property of Equality: if $a=b$ and $b=c$ then $a=c$."],
                 "Transitive Property", "", "Medium")
        + solved(24, "In a proof that two overlapping segments are congruent, why might the first geometric reason after the givens be Reflexive?",
                 ["The overlap is a shared segment, say $\\overline{BC}$.",
                  "Every segment is congruent to itself: $BC=BC$.",
                  "Reflexive supplies that shared piece so SSS or SAS can finish later."],
                 "the shared segment is congruent to itself", "", "Hard"),
        ("Writing “because it looks true” as a reason",
         "A picture can suggest a statement, but the reason column needs a name: Given, Definition of midpoint, Vertical "
         "Angles Congruent, Corresponding Angles Postulate. “Obvious” is not a reason."),
        ("Plan the last line first",
         "Circle the Prove statement. Ask what theorem would produce it. Then ask what you still need in order to use "
         "that theorem. That reverse list becomes the forward proof."),
        [
            "I can name the properties of equality used in algebraic proofs.",
            "I can structure a two-column proof with statements and reasons.",
            "I can use Reflexive on a shared side or shared angle.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Parallel lines and transversals",
        [
            "Parallel lines are coplanar lines that never meet. We write $\\ell\\parallel m$. A transversal is a line that "
            "intersects two or more coplanar lines at different points.",
            "A transversal creates eight angles. The region between the two lines is the interior; outside is the exterior. "
            "Pairs get names: corresponding, alternate interior, alternate exterior, and same-side (consecutive) interior.",
            "When the two lines are parallel, corresponding angles are congruent, alternate interior angles are congruent, "
            "alternate exterior angles are congruent, and same-side interior angles are supplementary.",
            "Those four facts are the workhorses of this unit. You prove them from a linear pair plus corresponding angles, "
            "or you take corresponding angles as a postulate, depending on your textbook’s order.",
            "The converses are how you prove lines parallel: if a transversal makes a pair of corresponding angles congruent "
            "(or alternate interiors congruent, or same-side interiors supplementary), then the two lines are parallel.",
            "Skew lines are noncoplanar and never meet; they are not parallel, because parallel requires a shared plane. "
            "That distinction matters in space, not in the usual two-line textbook diagram.",
        ],
        "A huge fraction of high-school geometry items is this one picture: two parallels and a transversal with an "
        "algebraic expression. If you can name the pair, you can write the equation in five seconds.",
        "Trace the transversal in red. Mark the two interiors with a tiny “in.” Then decide: same corner (corresponding), "
        "opposite interiors (alternate interior), or interiors on the same side (supplementary).",
        lesson_figure(
            parallel_lines_transversal(),
            "Parallel lines $\\ell$ and $m$ cut by a transversal",
            "The marked angles 1 and 2 are corresponding (same relative corner at each intersection).",
        )
        + solved(25, "ℓ ∥ m. A corresponding pair measures 70° and (3x+10)°. Find x.",
                 ["Corresponding angles are congruent when the lines are parallel.",
                  "Set $3x+10=70$.",
                  "Then $3x=60$ and $x=20$."],
                 "$20$", "", "Easy")
        + solved(26, "ℓ ∥ m. A same-side interior angle is 110°. Find its partner.",
                 ["Same-side interior angles are supplementary when the lines are parallel.",
                  "The partner is $180-110=70$.",
                  "So the other same-side interior angle measures $70^\\circ$."],
                 "$70^\\circ$", "", "Medium")
        + solved(27, "A transversal makes alternate interior angles congruent. What can you conclude about the two lines?",
                 ["The alternate-interior theorem says parallel lines make those angles congruent.",
                  "The converse runs the other way: congruent alternate interiors force the lines to be parallel.",
                  "Conclude that the two lines are parallel."],
                 "the lines are parallel", "Congruent alternate interiors are a parallel test, not a consequence you still need to prove.", "Hard"),
        ("Using 180° on corresponding angles",
         "Corresponding angles are congruent (equal), not supplementary. Supplementary is for a linear pair or for same-side "
         "interiors. Mixing those two numbers —  equal versus 180 − — is the standard trap.",
        ),
        ("Name the pair out loud",
         "Before algebra, write “corresponding ⇒ congruent” or “same-side interior ⇒ supplementary” on the paper. The "
         "equation is then automatic, and you will not subtract from 180 on a pair that should be set equal."),
        [
            "I can identify a transversal and the eight angles it creates.",
            "I can use the parallel-line angle theorems in both directions.",
            "I can prove lines parallel with a converse test.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Corresponding and alternate angles",
        [
            "Corresponding angles sit in the same relative position at each intersection: both upper-right, both lower-left, "
            "and so on. If the lines are parallel, corresponding angles are congruent.",
            "Alternate interior angles are between the two lines, on opposite sides of the transversal. Alternate exterior "
            "angles are outside the two lines, on opposite sides of the transversal. Both pairs are congruent when the lines are parallel.",
            "Same-side interior angles (also called consecutive interior angles) are between the two lines on the same side "
            "of the transversal. They are supplementary when the lines are parallel.",
            "All eight angles are determined by a single number. If one acute angle is $40^\\circ$, then four angles are "
            "$40^\\circ$ and four are $140^\\circ$. You never need eight separate computations.",
            "Algebraic versions just replace the number with an expression: set corresponding or alternate pairs equal, "
            "or add same-side interiors to $180$, then solve. Always substitute back to report the angle measure if that is what was asked.",
            "These pair names return in triangle proofs (a midsegment creates parallel lines) and in similar-triangle proofs "
            "(corresponding angles from parallels give AA similarity).",
        ],
        "Once you can classify the pair, the rest of high-school geometry’s parallel-line algebra is one of two equations: "
        "$= $ or $+ =180$. That binary choice is the whole chapter.",
        "Mark the four acute angles with one tick and the four obtuse angles with another. Then the pair names are just "
        "a way of saying “same tick” (congruent) or “different ticks that make a straight line” (supplementary).",
        lesson_figure(
            parallel_lines_transversal(),
            "Corresponding angles marked 1 and 2",
            "Same relative corner at each parallel. If $\\ell\\parallel m$, then $\\angle1\\cong\\angle2$.",
        )
        + solved(28, "ℓ ∥ m. Corresponding angles are 2x-4 and 50. Find x.",
                 ["Corresponding angles are congruent, so set the expressions equal.",
                  "$2x-4=50$, then $2x=54$.",
                  "So $x=27$."],
                 "$27$", "", "Easy")
        + solved(29, "ℓ ∥ m. Alternate interior angles are 3x+6 and 54. Find x.",
                 ["Alternate interior angles are congruent when the lines are parallel.",
                  "Set $3x+6=54$, then $3x=48$.",
                  "So $x=16$."],
                 "$16$", "", "Medium")
        + solved(30, "ℓ ∥ m. Same-side interiors are 2x and 4x+30. Find the smaller angle.",
                 ["Same-side interiors are supplementary: $2x+(4x+30)=180$.",
                  "Then $6x+30=180$, so $6x=150$ and $x=25$.",
                  "The angles are $2(25)=50^\\circ$ and $4(25)+30=130^\\circ$. The smaller is $50^\\circ$."],
                 "$50^\\circ$", "", "Hard"),
        ("Setting same-side interiors equal",
         "Same-side interiors look “alike” because they are both inside, but they are the supplementary pair. Setting them "
         "equal produces an $x$ that fails a linear-pair check at either intersection."),
        ("Find one angle, then clone it",
         "Compute a single angle completely. Then walk around the diagram cloning that measure to every corresponding and "
         "alternate copy, and taking $180$ minus that measure for every linear pair. This beats solving eight equations."),
        [
            "I can distinguish corresponding, alternate interior, alternate exterior, and same-side interior pairs.",
            "I can write the correct equation for each pair when lines are parallel.",
            "I can recover the eight-angle pattern from one given angle.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Perpendicular lines",
        [
            "Perpendicular lines intersect to form a right angle. We write $n\\perp\\ell$. All four angles at that "
            "intersection are $90^\\circ$, because adjacent angles on a straight line would be $90$ and $90$.",
            "In a plane, if two lines are both perpendicular to the same third line, then those two lines are parallel. "
            "This is a standard way to prove parallels without mentioning a transversal’s corresponding angles by name.",
            "If a transversal is perpendicular to one of two parallel lines, it is perpendicular to the other as well. "
            "The corresponding angles are both $90^\\circ$.",
            "In the coordinate plane, two nonvertical lines are perpendicular when their slopes $m_1$ and $m_2$ satisfy "
            "$m_1m_2=-1$ (negative reciprocals). A vertical line is perpendicular to a horizontal line.",
            "The shortest distance from a point to a line is along the perpendicular segment. That fact is used in area "
            "(height of a triangle or parallelogram) and later in coordinate geometry.",
            "Right triangles, altitude constructions, and the coordinate proofs of Unit 6 all depend on a clean definition "
            "of perpendicular: a $90^\\circ$ angle, not merely “they look steep.”",
        ],
        "Height in every area formula is a perpendicular, not a slanted side. Mixing those up is how students compute "
        "parallelogram area using a side instead of the height.",
        "In a diagram, look for the tiny square at the intersection. In a coordinate problem, multiply the slopes and "
        "check for $-1$. In a proof, quote the definition: “perpendicular ⇒ right angle.”",
        lesson_figure(
            _perp_svg(),
            "Line $n$ perpendicular to line $\\ell$",
            "The box marks a right angle, so $n\\perp\\ell$.",
        )
        + solved(31, "Two lines intersect to form a right angle. What word describes the lines?",
                 ["The definition of perpendicular lines is that they intersect at 90°.",
                  "The lines are perpendicular."],
                 "perpendicular", "", "Easy")
        + solved(32, "Lines with slopes 3/4 and -4/3 are drawn in the plane. How are they related?",
                 ["Compute the product: $(3/4)\\cdot(-4/3)=-1$.",
                  "Negative-reciprocal slopes mean the lines are perpendicular."],
                 "perpendicular", "", "Medium")
        + solved(33, "n ⊥ ℓ and n ⊥ m, with ℓ and m coplanar and distinct. Why is ℓ ∥ m?",
                 ["Each of ℓ and m is perpendicular to the same line n.",
                  "Two lines in a plane perpendicular to the same line are parallel.",
                  "Therefore $\\ell\\parallel m$."],
                 "$\\ell\\parallel m$", "", "Hard"),
        ("Calling any steep intersection perpendicular",
         "Perpendicular is exactly $90^\\circ$, not “fairly upright.” On a graph, slopes $2$ and $-2$ are not perpendicular "
         "because $2\\cdot(-2)=-4\\neq-1$. The negative reciprocal of $2$ is $-1/2$."),
        ("Check slope product, not opposite sign alone",
         "Opposite signs are necessary for nonvertical perpendiculars, but not sufficient. Multiply. You need $-1$ exactly, "
         "which is the negative-reciprocal test."),
        [
            "I can define perpendicular lines using a right angle.",
            "I can use perpendicularity to prove lines parallel.",
            "I can apply the negative-reciprocal slope test.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Triangle angle sum",
        [
            "The Triangle Angle Sum Theorem says the three interior angles of any triangle add to $180^\\circ$. The usual "
            "proof draws a line through one vertex parallel to the opposite side and then uses alternate interior angles.",
            "If two angles are known, the third is $180$ minus their sum. In a right triangle the two acute angles are "
            "complementary, because $90$ plus those two acute angles is already $180$.",
            "An exterior angle of a triangle is formed by extending one side. The Exterior Angle Theorem says that exterior "
            "angle equals the sum of the two remote interior angles. It also equals $180$ minus the adjacent interior angle.",
            "Equilateral triangles are equiangular: each angle is $60^\\circ$. Isosceles triangles have two congruent base "
            "angles; if the vertex angle is known, the base angles are $(180-\\text{vertex})/2$.",
            "A triangle cannot have two right angles, or two obtuse angles, because the sum would already meet or exceed "
            "$180$ before the third angle. This is a quick classification check.",
            "Triangle sum is the reason AA similarity works (two angles force the third) and the reason the acute angles "
            "of a right triangle are complementary in the trig unit. It is the most reused $180$ in the course.",
        ],
        "On a contest problem with a messy diagram, hunt for a triangle, write $180$ on it, and peel off the known angles. "
        "That one move unlocks exterior angles, isosceles base angles, and parallel-line chains.",
        "Mark every triangle’s angles with expressions, then write one $180$ equation per triangle. If an exterior angle "
        "is given, use remote interiors instead of inventing a new $180$ on a straight line — both work, but remote interiors is faster.",
        lesson_figure(
            _tri_sum_svg(),
            "Interior angles $\\alpha,\\beta,\\gamma$",
            "Always $\\alpha+\\beta+\\gamma=180^\\circ$.",
        )
        + solved(34, "A triangle has angles 50° and 60°. Find the third angle.",
                 ["Angle sum is 180°.",
                  "$180-50-60=70$."],
                 "$70^\\circ$", "", "Easy")
        + solved(35, "An exterior angle is 105° and one remote interior is 40°. Find the other remote interior.",
                 ["Exterior Angle Theorem: exterior = sum of remote interiors.",
                  "$105=40+x$, so $x=65$."],
                 "$65^\\circ$", "", "Medium")
        + solved(36, "A triangle has angles 2x, 3x, and 4x. Find the largest angle.",
                 ["$2x+3x+4x=180$, $9x=180$, $x=20$.",
                  "The angles are $40^\\circ$, $60^\\circ$, and $80^\\circ$.",
                  "The largest is $80^\\circ$."],
                 "$80^\\circ$", "", "Hard"),
        ("Using 360° for a triangle",
         "A full turn around a point is $360^\\circ$, and a quadrilateral sums to $360^\\circ$, but a triangle sums to "
         "$180^\\circ$. Using 360 on a triangle doubles every answer."),
        ("Write 180 on the triangle before algebra",
         "Literally write a small “180” inside the triangle. Then subtract known pieces. For an exterior angle, mark the "
         "two remote interiors and add them. The annotation prevents using the adjacent interior by mistake."),
        [
            "I can find a missing interior angle using 180°.",
            "I can apply the Exterior Angle Theorem.",
            "I can handle algebraic angle-sum equations in a triangle.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3
# ===========================================================================

def _u3_questions():
    rows = [
        ("SSS congruence requires three pairs of congruent…",
         "sides", "SSS is side-side-side: three pairs of corresponding sides congruent imply the triangles are congruent.",
         ["angles", "altitudes", "medians"]),
        ("SAS congruence uses two sides and the…",
         "included angle", "The angle must be the one formed by those two sides, not a remote angle (that would be SSA, which is not a shortcut).",
         ["opposite angle", "exterior angle", "remote interior angle"]),
        ("Which of the following is not a valid triangle-congruence shortcut?",
         "SSA", "SSA is the ambiguous case; it does not always determine a unique triangle. HL is the right-triangle exception that looks like SSA.",
         ["SSS", "SAS", "HL"]),
        ("In △ABC and △DEF, AB=DE, BC=EF, and AC=DF. The triangles are congruent by…",
         "SSS", "Three pairs of sides match, so SSS applies.",
         ["SAS", "ASA", "AAA"]),
        ("In △ABC and △DEF, AB=DE, ∠B=∠E, and BC=EF. The triangles are congruent by…",
         "SAS", "∠B is included between sides AB and BC; ∠E is included between DE and EF.",
         ["ASA", "SSS", "AAA"]),
        ("ASA congruence uses two angles and the…",
         "included side", "The side must be the one between those two angles.",
         ["opposite side", "hypotenuse", "median"]),
        ("AAS is valid because two angles determine the third, which turns AAS into…",
         "ASA", "Angle sum gives the third angle, so AAS reduces to a known ASA configuration.",
         ["SSA", "AAA", "HL"]),
        ("AAA is not a congruence shortcut because it only proves the triangles are…",
         "similar", "Equal angles give the same shape, not the same size.",
         ["congruent", "right", "isosceles"]),
        ("In △ABC and △XYZ, ∠A=∠X, AB=XY, and ∠B=∠Y. The triangles are congruent by…",
         "ASA", "Side AB is included between ∠A and ∠B.",
         ["SAS", "SSS", "HL"]),
        ("In △PQR and △STU, ∠P=∠S, ∠R=∠U, and QR=TU. The triangles are congruent by…",
         "AAS", "Two angles and a non-included side (opposite R and U) match.",
         ["SAS", "SSS", "HL"]),
        ("HL congruence applies only to…",
         "right triangles", "Hypotenuse-leg requires a right angle in each triangle plus a congruent hypotenuse and one congruent leg.",
         ["all triangles", "isosceles triangles only", "obtuse triangles"]),
        ("In right triangles ABC and DEF with right angles at C and F, AB=DE and AC=DF. Congruence is by…",
         "HL", "AB and DE are hypotenuses; AC and DF are legs.",
         ["SAS", "ASA", "AAA"]),
        ("Why is HL allowed even though it resembles SSA?",
         "the right angle makes the triangle rigid",
         "A right triangle with given hypotenuse and a leg is unique; the ambiguous SSA case cannot occur.",
         ["SSA is always valid", "the acute angles must be 45°", "the legs must be equal to each other"]),
        ("If two right triangles share a hypotenuse of 13 and a leg of 5, they are…",
         "congruent by HL", "Same hypotenuse and same leg force congruence of right triangles.",
         ["only similar", "congruent by AAA", "not comparable"]),
        ("To use HL you must first establish that each triangle has a…",
         "right angle", "Without a right angle, “hypotenuse” is not defined.",
         ["60° angle", "pair of congruent acute angles", "median to the base"]),
        ("CPCTC stands for Corresponding Parts of Congruent Triangles are…",
         "Congruent", "After triangles are congruent, every pair of corresponding sides and angles is congruent.",
         ["Complementary", "Similar", "Parallel"]),
        ("You may apply CPCTC only after you have already proved the triangles are…",
         "congruent", "CPCTC is a consequence, not a method for proving the triangles congruent in the first place.",
         ["similar", "right", "isosceles"]),
        ("△ABC ≅ △DEF. Then ∠B corresponds to…",
         "∠E", "Vertices are listed in corresponding order: A↔D, B↔E, C↔F.",
         ["∠D", "∠F", "∠A"]),
        ("△ABC ≅ △DEF. Side AC corresponds to…",
         "DF", "First and third vertices: A↔D and C↔F, so AC↔DF.",
         ["DE", "EF", "FE"]),
        ("A proof uses SAS, then concludes a pair of angles congruent. The reason for that last step is…",
         "CPCTC", "SAS proved the triangles congruent; the angles are corresponding parts.",
         ["ASA", "Vertical angles", "AAA"]),
        ("In isosceles △ABC with AB=AC, the base angles are…",
         "∠B and ∠C", "The base angles sit at the base, opposite the congruent sides.",
         ["∠A and ∠B", "∠A and ∠C", "only ∠A"]),
        ("If the base angles of a triangle are congruent, the triangle is…",
         "isosceles", "Converse of the isosceles triangle theorem: equal base angles ⇒ equal opposite sides.",
         ["right", "obtuse", "scalene"]),
        ("An equilateral triangle is also…",
         "equiangular, with each angle 60°", "All sides equal ⇒ all angles equal, and 180/3=60.",
         ["right", "obtuse", "scalene"]),
        ("The vertex angle of an isosceles triangle is 40°. Each base angle measures…",
         70, "(180−40)/2=70.",
         [40, 80, 140]),
        ("The altitude from the vertex of an isosceles triangle to the base is also a…",
         "median and angle bisector", "That altitude is a median, an angle bisector, and a perpendicular bisector of the base.",
         ["only a median, never a bisector", "hypotenuse", "third congruent side"]),
        ("Overlapping triangles often share a side that is congruent to itself by the…",
         "Reflexive Property", "The shared segment is the usual first corresponding pair in an overlapping SAS or SSS proof.",
         ["Symmetric Property", "Vertical Angle Theorem", "CPCTC first"]),
        ("Two triangles overlap so that they share ∠C. That shared angle is a corresponding pair by…",
         "Reflexive Property", "An angle is congruent to itself, just as a side is.",
         ["CPCTC", "AAS immediately without other parts", "AAA"]),
        ("In overlapping △ABD and △CBD that share BD, a likely first congruence pair is…",
         "BD ≅ BD", "Name the shared side before hunting for SAS or SSS.",
         ["AB ≅ CD always", "∠A ≅ ∠C always", "AD ≅ BC always"]),
        ("Vertical angles in an overlapping X-shaped figure give a congruent-angle pair that is often used for…",
         "ASA or AAS", "The vertical pair supplies an angle; you still need a side and another angle or side.",
         ["SSS only", "HL only", "CPCTC before congruence"]),
        ("A common overlapping-triangle trap is to use CPCTC…",
         "before the triangles have been proved congruent", "CPCTC is illegal until a congruence shortcut has already been applied.",
         ["after SSS", "after SAS", "after HL"]),
        ("Which additional pair would complete SAS if AB=DE and BC=EF?",
         "∠B ≅ ∠E", "The included angles at B and E sit between those sides.",
         ["∠A ≅ ∠D", "∠C ≅ ∠F", "AC = DF"]),
        ("Which additional pair would complete ASA if ∠A=∠D and ∠B=∠E?",
         "AB ≅ DE", "AB is the side included between ∠A and ∠B.",
         ["BC ≅ EF", "AC ≅ DF", "∠C ≅ ∠F"]),
        ("Two triangles have all three pairs of angles congruent. They must be…",
         "similar, but not necessarily congruent", "AAA is similarity. Size can still differ.",
         ["congruent by AAA", "right triangles", "equilateral"]),
        ("Right triangles with hypotenuses 10 and 10 and one pair of legs 6 and 6 are congruent by…",
         "HL", "Hypotenuse and a leg match.",
         ["AAA", "AAS only", "SSA"]),
        ("△ABC ≅ △CBA would indicate that the triangle is…",
         "isosceles with AB=CB", "The mapping swaps A and C, so AB maps to CB.",
         ["scalene", "equilateral only", "impossible"]),
        ("Given AB=DE, ∠A=∠D, and AC=DF. Congruence of △ABC and △DEF is by…",
         "SAS", "∠A is included between AB and AC.",
         ["ASA", "AAS", "HL"]),
        ("An isosceles triangle has vertex angle 80° and congruent legs. Each base angle is…",
         50, "(180−80)/2=50.",
         [80, 40, 100]),
        ("SSA with an acute angle opposite a shorter side can produce…",
         "zero, one, or two triangles", "That is the ambiguous case; it is why SSA is not a congruence shortcut.",
         ["always exactly one triangle", "always two congruent triangles", "always a right triangle"]),
        ("If △ABC ≅ △FED, then ∠C corresponds to…",
         "∠D", "Order ABC ↔ FED means C↔D.",
         ["∠F", "∠E", "∠A"]),
        ("A proof lists vertical angles, then a shared side, then another pair of sides from the vertex. The shortcut is…",
         "SAS", "Angle (vertical) included between the shared side and the other sides.",
         ["SSS", "HL", "AAA"]),
        ("Equilateral △ABC has side 6. A second triangle congruent to it must have perimeter…",
         18, "Congruent triangles have the same side lengths, so the perimeter is 18.",
         [12, 6, 36]),
        ("The included side for ∠B and ∠C in △ABC is…",
         "BC", "BC is the side whose endpoints are B and C.",
         ["AB", "AC", "the altitude from A"]),
        ("After proving △ABM ≅ △CBM by SSS, BM is a median if M is on AC because…",
         "CPCTC gives AM=CM", "Corresponding sides AM and CM are congruent, so M is the midpoint of AC.",
         ["AAA", "the triangles are similar only", "BM is a hypotenuse"]),
        ("Two right triangles share the hypotenuse AB and have a pair of congruent acute angles at A. They are congruent by…",
         "AAS (or HA)", "Right angles match, the acute angles at A match, and hypotenuse AB is a non-included side; AAS applies. (Some books call this HA.)",
         ["SSS", "SSA", "AAA"]),
        ("If AB=AC and BD and CD are altitudes to the legs, a symmetry argument often uses…",
         "two pairs of right triangles from the vertex", "The isosceles vertex altitude creates two congruent right triangles.",
         ["AAA on the original triangle alone", "SSA on the base", "CPCTC with no prior congruence"]),
        ("A kite’s diagonal between the vertex angles splits the kite into two triangles congruent by…",
         "SSS or SAS, depending on the marked sides", "The diagonal is reflexive; the two pairs of adjacent equal sides give SSS or SAS.",
         ["AAA", "HL only", "AAS only"]),
        ("SAT Stretch: △ABC and △ADC share AC. AB=AD, CB=CD. The triangles are congruent by…",
         "SSS", "AB=AD, CB=CD, and AC=AC (reflexive), so SSS.",
         ["AAA", "HL", "SSA"]),
        ("SAT Stretch: In overlapping △ABE and △CBD, AE and CD cross at X, with AX=CX and BX=DX. Vertical angles at X plus those sides give…",
         "SAS",
         "AX=CX, vertical ∠AXB≅∠CXD, and BX=DX, so the vertical angle is included: SAS at X.",
         ["SSS with no extra work", "HL", "CPCTC first"]),
        ("SAT Stretch: Isosceles △ABC with AB=AC, vertex angle x°, and each base angle 2x°. The vertex angle measures…",
         36, "x+2x+2x=180, 5x=180, x=36.",
         [72, 54, 90]),
        ("SAT Stretch: Right △ABC and right △DEF have hypotenuses 17 and 17 and legs 8 and 8. They are congruent by…",
         "HL", "Matching hypotenuse and matching leg in right triangles is HL.",
         ["SSA", "AAA", "AAS only"]),
        ("SAT Stretch: △PQR ≅ △RPQ. Which side must equal QR?",
         "PQ", "Order PQR ↔ RPQ sends Q→P and R→Q, so QR↔PQ.",
         ["PR", "QR itself only", "none; the mapping is impossible"]),
        ("SAT Stretch: AB and CD bisect each other at M. △AMC and △BMD are congruent by…",
         "SAS", "AM=BM, vertical angles at M, and CM=DM, so SAS. (The vertical angle is included.)",
         ["AAA", "HL", "SSA"]),
        ("SAT Stretch: Isosceles △ABC with AB=AC has base angles (2x+10)° and (3x−5)°. The vertex angle measures…",
         100, "Base angles equal: 2x+10=3x−5, x=15. Each base is 40°, so the vertex is 100°.",
         [40, 80, 65]),
        ("SAT Stretch: You are given AB=DE, ∠A=∠D, and BC=EF. That listing is SSA. Which extra pair would produce SAS?",
         "AC ≅ DF", "SAS needs two sides and the included angle. Adding AC=DF puts ∠A between AB and AC.",
         ["∠C ≅ ∠F only", "AAA", "a pair of hypotenuses with no right angle"]),
        ("SAT Stretch: Right triangles ABD and ABC are both right at B and share leg AB. If hypotenuses AD=AC, the triangles are congruent by…",
         "HL", "Shared leg AB and matching hypotenuses in two right triangles is HL. Then CPCTC would give BD=BC.",
         ["SSA", "AAA", "SSS without using the right angles"]),
    ]
    return _pack(rows)


def build_unit3():
    title = "Geometry Unit 3: Triangle Congruence"
    description = (
        "SSS and SAS, ASA and AAS, HL for right triangles, CPCTC, isosceles triangle theorems, "
        "and overlapping-triangle proofs — with matching tick-mark diagrams and SAT-hard stretch items."
    )
    concepts = [
        "SSS and SAS",
        "ASA and AAS",
        "HL for right triangles",
        "CPCTC",
        "Isosceles triangle theorems",
        "Overlapping triangles",
    ]
    c1 = concept_block(
        "1. SSS and SAS",
        [
            "Two triangles are congruent if one can be placed on the other so that all corresponding sides and all "
            "corresponding angles match. Congruence shortcuts let you prove that from only three carefully chosen pairs.",
            "SSS (Side-Side-Side) says that three pairs of corresponding congruent sides force the triangles to be congruent. "
            "The triangle is a rigid object once its three side lengths are fixed.",
            "SAS (Side-Angle-Side) uses two sides and the included angle — the angle whose vertex is the shared endpoint "
            "of those two sides. If the included angles match and the bordering sides match, the triangles match.",
            "SSA is not on the list. Two sides and a non-included angle can produce zero, one, or two triangles (the ambiguous "
            "case). That is why a quiz that shows an angle opposite a side is a trap unless the triangles are right (see HL).",
            "Correspondence of vertices matters as much as the shortcut. $\\triangle ABC\\cong\\triangle DEF$ means $A\\leftrightarrow D$, "
            "$B\\leftrightarrow E$, $C\\leftrightarrow F$, so $AB$ matches $DE$, not $DF$.",
            "Tick marks on a diagram are a visual SSS or SAS. One tick on two sides means those sides are a corresponding pair. "
            "Read the ticks before you name a shortcut, and check that an angle marked for SAS really sits between the two sides.",
        ],
        "Almost every later proof in this course — parallelograms, similar-triangle proportions after a congruence, circle "
        "chords — starts by locking two triangles together with SSS or SAS. If the included-angle test is fuzzy, those proofs stall.",
        "On a diagram, highlight the two sides and then ask: is the marked angle the one between them? If yes, SAS. If you "
        "have three sides and no needed angle, SSS. If the angle is opposite a side, you do not have a shortcut yet.",
        lesson_figure(
            _two_tri_svg("sas"),
            "Two triangles marked for SAS",
            "Matching ticks on two sides and a matching arc on the included angle.",
        )
        + solved(1, "AB=DE, BC=EF, and AC=DF. Why are △ABC and △DEF congruent?",
                 ["Three pairs of corresponding sides are congruent.",
                  "SSS applies."],
                 "SSS", "", "Easy")
        + solved(2, "AB=DE, ∠B=∠E, and BC=EF. Why are the triangles congruent?",
                 ["∠B is formed by sides AB and BC.",
                  "∠E is formed by sides DE and EF.",
                  "Two sides and the included angle match, so SAS applies."],
                 "SAS", "If the congruent angles had been ∠A and ∠D, this listing would have been SSA, which is not a shortcut.", "Medium")
        + solved(3, "A diagram shows AB=DE, AC=DF, and ∠C=∠F. Can you conclude congruence?",
                 ["The congruent angles are at C and F, opposite the sides AB and DE rather than included between AB, AC.",
                  "This is SSA, which is not a valid congruence shortcut.",
                  "You cannot conclude congruence from this listing alone."],
                 "no; the listing is SSA", "", "Hard"),
        ("Using SSA as if it were SAS",
         "Students see two sides and an angle and write SAS without checking that the angle is included. SAS is a sandwich: "
         "the angle is the filling between the two sides. An angle on the end is SSA."),
        ("Mark the included vertex with a finger",
         "Touch the vertex of the candidate angle. The two sides you need for SAS must both start at that vertex. If one of "
         "the given sides is across the triangle from that vertex, you do not have SAS."),
        [
            "I can apply SSS from three pairs of sides.",
            "I can apply SAS only when the angle is included.",
            "I can reject SSA as a congruence shortcut.",
        ],
        1,
    )
    c2 = concept_block(
        "2. ASA and AAS",
        [
            "ASA (Angle-Side-Angle) uses two angles and the included side — the side whose endpoints are the vertices of "
            "those two angles. Two angles and the wall between them lock the triangle.",
            "AAS (Angle-Angle-Side) uses two angles and a non-included side. It is valid because the Triangle Angle Sum "
            "Theorem produces the third angle, after which you have ASA (or a corresponding AAS configuration that is equally rigid).",
            "AAA is not congruence. Three pairs of congruent angles prove the triangles are similar — same shape — but they "
            "may be different sizes. A small 40-60-80 triangle is similar to a large 40-60-80 triangle, not congruent to it.",
            "Order still matters. If $\\angle A=\\angle D$ and $\\angle B=\\angle E$, the included side for ASA is $AB$ matching $DE$, "
            "not $BC$ matching $EF$. Choosing the wrong side is how ASA quietly becomes AAS or a non-corresponding mess.",
            "AAS often appears when a pair of angles is vertical or corresponding (from parallels) and a side not between them "
            "is given. Name the two angles first, then name the side and check whether it is included.",
            "ASA and AAS are the angle-heavy twins of SSS and SAS. Together with HL they are the complete high-school list "
            "of congruence shortcuts you are allowed to quote in a proof.",
        ],
        "AA similarity in the next unit is ASA/AAS without caring about size. Learning which side is included now prevents "
        "you from claiming congruence when the problem only gave angles.",
        "Write the three letters of each triangle in corresponding order, then underline the given parts. If the underlined "
        "pattern is angle-side-angle in a row, it is ASA. If it is angle-angle-side, it is AAS.",
        lesson_figure(
            _two_tri_svg("asa"),
            "Two triangles marked for ASA",
            "Matching arcs at two angles and a tick only on the included side between those angles.",
        )
        + lesson_figure(
            _two_tri_svg("aas"),
            "Two triangles marked for AAS",
            "Matching arcs at two angles and a tick on a non-included side (not the wall between those angles).",
        )
        + solved(4, "∠A=∠X, AB=XY, and ∠B=∠Y. Name the congruence shortcut.",
                 ["AB is the side between ∠A and ∠B.",
                  "XY is the side between ∠X and ∠Y.",
                  "This is ASA."],
                 "ASA", "", "Easy")
        + solved(5, "∠P=∠S, ∠R=∠U, and QR=TU. Name the shortcut.",
                 ["QR is opposite ∠P, not between ∠P and ∠R.",
                  "Two angles and a non-included side match.",
                  "This is AAS."],
                 "AAS", "", "Medium")
        + solved(6, "All three pairs of angles match, but no sides are given. Why is that not congruence?",
                 ["AAA determines shape only.",
                  "The triangles are similar, but one could be a scaled copy of the other.",
                  "Without a size match, they need not be congruent."],
                 "AAA proves similarity, not congruence", "", "Hard"),
        ("Picking a non-included side and calling it ASA",
         "ASA requires the side between the two angles. If the given side is across from one of the angles, the name is AAS, "
         "which is still valid — but only if you identify it correctly. Misnaming in a proof can cost the reason column."),
        ("List parts in vertex order",
         "Write $A$-$B$-$C$ and $D$-$E$-$F$ with checkmarks on given parts. A check-blank-check pattern on three consecutive "
         "vertices is ASA. Two checks on angles plus a check on a far side is AAS."),
        [
            "I can apply ASA when the side is included.",
            "I can apply AAS and explain why it works.",
            "I can reject AAA as a congruence shortcut.",
        ],
        6,
    )
    c3 = concept_block(
        "3. HL for right triangles",
        [
            "HL (Hypotenuse-Leg) is a congruence shortcut that applies only to right triangles. You need a right angle in "
            "each triangle, congruent hypotenuses, and one pair of congruent legs.",
            "The hypotenuse is the side opposite the right angle, always the longest side. A “leg” is either of the two "
            "sides that form the right angle. HL does not use an acute angle; it uses two sides of a right triangle.",
            "HL looks like SSA, and SSA is illegal in general. The right angle removes the ambiguity: a right triangle with "
            "a given hypotenuse and a given leg is rigid, so only one such triangle exists up to congruence.",
            "Before you write HL you must know the triangles are right. A square in the diagram, a statement that two lines "
            "are perpendicular, or an altitude to a side can supply that right angle.",
            "If you have a right angle, a leg, and the adjacent acute angle, that is ASA (or AAS), not HL. HL is specifically "
            "hypotenuse plus a leg. Using the wrong name is a reason-column error even when the triangles really are congruent.",
            "HL shows up in isosceles altitudes (two right triangles sharing a height), in kites, and in coordinate proofs "
            "where a vertical and a horizontal meet. It is the only extra shortcut beyond SSS, SAS, ASA, and AAS.",
        ],
        "Contest problems love a right triangle with the hypotenuse and a leg marked, hoping you will write SSA and freeze. "
        "If you see a right angle, HL is the name that legalizes that pair of sides.",
        "Circle the right angles first. Then identify the hypotenuse in each triangle (opposite the box). If those hypotenuses "
        "match and one pair of legs matches, write HL. If an acute angle is matching instead, look for AAS.",
        lesson_figure(
            labeled_right_triangle(5, 12, 13, a_lab="5", b_lab="12", c_lab="13", angle_lab=""),
            "A right triangle with hypotenuse 13 and a leg 5",
            "HL would match this triangle to any other right triangle with hypotenuse 13 and a leg 5.",
        )
        + solved(7, "Right triangles ABC and DEF, right at C and F, have AB=DE and AC=DF. Name the shortcut.",
                 ["AB and DE are the hypotenuses (opposite the right angles).",
                  "AC and DF are legs.",
                  "HL applies."],
                 "HL", "", "Easy")
        + solved(8, "Why is HL allowed when SSA is not?",
                 ["SSA can produce two different triangles in the acute case.",
                  "A right triangle with a fixed hypotenuse and a fixed leg cannot flip into a second copy.",
                  "The right angle makes the figure unique, so HL is safe."],
                 "the right angle removes the SSA ambiguity", "", "Medium")
        + solved(9, "Two right triangles share hypotenuse AB and have ∠A congruent. Which shortcut applies?",
                 ["Right angles are congruent.",
                  "∠A is a second pair of angles, and AB is a non-included side (the hypotenuse).",
                  "This is AAS (sometimes called HA), not HL, because a leg is not the second given side."],
                 "AAS (HA)", "HL would require a matching leg, not a matching acute angle.", "Hard"),
        ("Writing SSA on a right triangle and stopping",
         "The data may be legal as HL, but SSA is still not a reason you can quote. Translate “hypotenuse and leg” into the "
         "name HL. Do not leave SSA in the reason column."),
        ("Find the hypotenuse before you name a leg",
         "The hypotenuse is opposite the right angle. If you accidentally treat a leg as the hypotenuse, you will write HL "
         "when you only have two legs (which would be SAS if you also use the right angle as the included angle)."),
        [
            "I can state the hypotheses of HL.",
            "I can distinguish HL from SAS that uses the right angle.",
            "I can explain why HL does not contradict the ban on SSA.",
        ],
        11,
    )
    c4 = concept_block(
        "4. CPCTC",
        [
            "CPCTC means Corresponding Parts of Congruent Triangles are Congruent. Once two triangles are congruent, every "
            "pair of corresponding sides and every pair of corresponding angles is congruent.",
            "CPCTC is a consequence, not a shortcut. You may not use it to prove the triangles congruent. You prove congruence "
            "with SSS, SAS, ASA, AAS, or HL, and only then may you harvest extra matching parts with CPCTC.",
            "Correspondence comes from the congruence statement. $\\triangle ABC\\cong\\triangle DEF$ tells you $A\\leftrightarrow D$, "
            "$B\\leftrightarrow E$, $C\\leftrightarrow F$. Then $\\angle B\\cong\\angle E$ and $\\overline{AC}\\cong\\overline{DF}$ by CPCTC.",
            "A typical proof goal is “prove two segments congruent” when those segments are not part of the original shortcut. "
            "You build two triangles, prove them congruent, then name the desired segments as corresponding parts.",
            "Writing the congruence statement with vertices in the wrong order makes CPCTC name the wrong parts. If you proved "
            "$\\triangle ABC\\cong\\triangle FED$ but wanted $AC$ matching $FD$, check the order: $A\\leftrightarrow F$ would be wrong.",
            "Medians, angle bisectors, and parallelogram proofs in later units are CPCTC machines: prove two triangles congruent, "
            "then the leftover corresponding sides or angles finish the definition you wanted.",
        ],
        "The whole point of triangle congruence is to get parts you were not given. CPCTC is how those parts become legal. "
        "Without it, a congruence proof has nowhere to go after the shortcut.",
        "Circle the two triangles, write a congruence statement with vertices in matching order, tick the three pairs used "
        "in the shortcut, then point to the leftover pair the question asked for and write CPCTC.",
        lesson_figure(
            _two_tri_svg("sss"),
            "After SSS, leftover corresponding angles match by CPCTC",
            "The three pairs of ticks prove congruence; any matching angle pair is then CPCTC.",
        )
        + solved(10, "△ABC ≅ △DEF. Which angle corresponds to ∠B?",
                 ["The vertex order is A↔D, B↔E, C↔F.",
                  "So ∠B corresponds to ∠E."],
                 "∠E", "", "Easy")
        + solved(11, "A proof uses SAS, then concludes ∠C ≅ ∠F. What is the reason for that conclusion?",
                 ["SAS already established △ABC ≅ △DEF.",
                  "∠C and ∠F are corresponding angles.",
                  "The reason is CPCTC."],
                 "CPCTC", "", "Medium")
        + solved(12, "After △ABM ≅ △CBM by SSS with M on AC, why is BM a median?",
                 ["SSS used AB, BM, AM matching CB, BM, CM, or a similar listing.",
                  "CPCTC gives AM=CM (the leftover corresponding sides on AC).",
                  "M is the midpoint of AC, so BM is a median."],
                 "CPCTC yields AM=CM, so M is a midpoint", "", "Hard"),
        ("Using CPCTC as the congruence shortcut",
         "CPCTC cannot be the first triangle reason. If the triangles are not yet congruent, corresponding parts are not "
         "yet known. A proof that starts with CPCTC is circular."),
        ("Write the congruence statement before CPCTC",
         "Force yourself to write $\\triangle\\_\\_\\_\\cong\\triangle\\_\\_\\_$ with three letters each. Then the corresponding "
         "parts are whatever occupies the same slot. This prevents matching $AC$ to $EF$ by accident."),
        [
            "I can decode a congruence statement into corresponding parts.",
            "I use CPCTC only after a congruence shortcut.",
            "I can finish a proof whose goal is a leftover side or angle.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Isosceles triangle theorems",
        [
            "An isosceles triangle has at least two congruent sides, called the legs. The third side is the base. The angles "
            "at the base are the base angles; the angle between the legs is the vertex angle.",
            "The Isosceles Triangle Theorem says the base angles are congruent. If $AB=AC$, then $\\angle B\\cong\\angle C$. "
            "The converse is also true: if two angles of a triangle are congruent, the sides opposite them are congruent.",
            "An equilateral triangle is isosceles in three ways. It is also equiangular, with each angle $60^\\circ$. Those "
            "facts are the cleanest angle-chasing tools in the course.",
            "The altitude from the vertex to the base of an isosceles triangle is also a median and an angle bisector, and it "
            "is the perpendicular bisector of the base. One segment does four jobs. Proofs usually split the isosceles triangle "
            "into two congruent right triangles.",
            "Algebra with isosceles triangles is angle sum plus equal base angles. If the vertex is $40^\\circ$, each base "
            "angle is $70^\\circ$. If the base angles are $2x$ and $3x-10$, set them equal first, then find the vertex.",
            "Isosceles theorems combine with congruence: you may get $AB=AC$ from the converse, then use SAS with the vertex "
            "angle, or you may use HL on the two right triangles created by the altitude.",
        ],
        "SAT figures hide an isosceles triangle with two equal tick marks and then ask for an angle that looks unrelated. "
        "Equal sides ⇒ equal base angles is the fastest angle-chase in Geometry.",
        "Mark the two equal sides, then immediately mark the two base angles with the same arc. If the vertex angle is the "
        "unknown, subtract twice a base angle from 180. If a base angle is unknown, set the two base-angle expressions equal.",
        lesson_figure(
            _iso_svg(),
            "Isosceles triangle with congruent legs and congruent base angles",
            "Equal ticks on the legs force equal arcs on the base angles.",
        )
        + solved(13, "Isosceles △ABC with AB=AC has vertex angle 40°. Find a base angle.",
                 ["The base angles are equal.",
                  "They share the remaining $180-40=140$.",
                  "Each base angle is $70^\\circ$."],
                 "$70^\\circ$", "", "Easy")
        + solved(14, "A triangle has two angles of 50°. What kind of triangle is it, and why?",
                 ["Two angles equal ⇒ the sides opposite them are equal (converse of the isosceles theorem).",
                  "The triangle is isosceles.",
                  "The third angle is $80^\\circ$, so it is not equilateral."],
                 "isosceles (not equilateral)", "", "Medium")
        + solved(15, "Isosceles △ABC with AB=AC has base angles (2x+10)° and (3x-5)°. Find the vertex angle.",
                 ["Set the base angles equal: $2x+10=3x-5$.",
                  "$15=x$, so each base angle is $40^\\circ$.",
                  "The vertex is $180-80=100^\\circ$."],
                 "$100^\\circ$", "", "Hard"),
        ("Calling the vertex angle a base angle",
         "The vertex angle sits between the two congruent sides. The base angles sit on the base. Using  the vertex as if it "
         "matched a base angle produces a $90$ or $40$ that the picture cannot support."),
        ("Set the two base-angle expressions equal first",
         "When both base angles have algebra, do not add them to 180 until they are the same number. Equality of base angles "
         "is the isosceles fact; 180 is the second fact."),
        [
            "I can use equal sides to get equal base angles, and conversely.",
            "I can compute missing isosceles angles with 180°.",
            "I can name the extra jobs of the vertex altitude.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Overlapping triangles",
        [
            "Overlapping triangles share a side or an angle. The shared piece is congruent to itself by the Reflexive "
            "Property, and that pair is often the first line of the proof after the givens.",
            "A common picture is two triangles that share a side, like $\\triangle ABD$ and $\\triangle CBD$ sharing $BD$. "
            "Another is an X, where two segments cross and the vertical angles at the intersection are a congruent pair.",
            "The strategy is always the same: name the two triangles, list three pairs (including reflexive or vertical), "
            "choose SSS, SAS, ASA, AAS, or HL, write a congruence statement in matching order, then use CPCTC if needed.",
            "The danger is using a part that belongs to both triangles as if it were two different given lengths, or using "
            "CPCTC on a pair you have not yet earned. Shared does not mean “given twice”; it means reflexive once.",
            "Coloring helps. Shade one triangle lightly and outline the other. Then the overlapping region is the shared "
            "side or angle you will mark reflexive.",
            "Overlapping proofs are the SAT Stretch of this unit: two triangles that do not sit side by side, a vertical "
            "angle, a midpoint, and a request for a leftover side. The method does not change — only the picture gets busier.",
        ],
        "Real exam figures almost never show two separate triangles. They overlap on purpose. If you can pull two triangles "
        "out of a messy sketch and name a shortcut, you can do the hard items at the end of this unit.",
        "Redraw the two triangles separately, copying every tick and arc, and include the shared side in both sketches. "
        "If the separated sketches make SAS obvious, the original picture will too.",
        lesson_figure(
            _overlap_svg(),
            "Overlapping △ABC and △ADC sharing AC, or △ABD inside △ABC",
            "Shared segments and interior points create two triangles that must be named carefully.",
        )
        + solved(16, "△ABD and △CBD share BD. What congruence pair can you write immediately?",
                 ["BD is in both triangles.",
                  "Reflexive Property: $BD\\cong BD$."],
                 "$BD\\cong BD$", "", "Easy")
        + solved(17, "AB and CD bisect each other at M. Why is △AMC ≅ △BMD?",
                 ["A midpoint (bisect) gives AM=BM and CM=DM.",
                  "Vertical angles at M are congruent.",
                  "Two sides and the included vertical angle give SAS."],
                 "SAS", "", "Medium")
        + solved(18, "△ABC and △ADC share AC, with AB=AD and CB=CD. Prove the triangles congruent and then that ∠BAC ≅ ∠DAC.",
                 ["AB=AD, CB=CD, and AC=AC (reflexive) so SSS.",
                  "Write △ABC ≅ △ADC (or △CBA ≅ △CDA) with matching order.",
                  "∠BAC and ∠DAC are corresponding angles, so they are congruent by CPCTC. Ray AC is an angle bisector of ∠BAD."],
                 "SSS, then CPCTC", "This is the standard kite or isosceles-on-both-sides argument.", "Hard"),
        ("Using a shared side as two different given lengths",
         "Writing $BD=5$ from one triangle and $BD=5$ from the other as if they were independent measurements is clutter. "
         "State Reflexive once. Extra copies of the same fact do not make SSS out of two sides."),
        ("Separate the triangles on scrap paper",
         "A 20-second redraw of each triangle, with the shared side copied into both, turns an overlapping mess into an "
         "ordinary SAS question. Do that redraw on every overlapping item in the stretch set."),
        [
            "I can find a reflexive shared side or angle.",
            "I can use vertical angles in an X-shaped overlap.",
            "I can finish overlapping proofs with a named shortcut and CPCTC.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4
# ===========================================================================

def _u4_questions():
    rows = [
        ("Similar polygons have congruent corresponding angles and corresponding sides that are…",
         "proportional", "Similarity is same shape, possibly different size. Sides match in a constant ratio, the scale factor.",
         ["equal in length always", "perpendicular", "parallel only"]),
        ("If ABCD ~ EFGH, then ∠B corresponds to…",
         "∠F", "Vertex order names the correspondence: A↔E, B↔F, C↔G, D↔H.",
         ["∠E", "∠G", "∠H"]),
        ("A pentagon similar to one with sides 3,3,4,5,6 has shortest side 6. Its longest side is…",
         12, "Scale factor 6/3=2, so the longest side 6 becomes 12.",
         [9, 18, 8]),
        ("The ratio of perimeters of similar polygons equals…",
         "the scale factor", "Perimeter scales with length, so it uses the same ratio as corresponding sides.",
         ["the square of the scale factor", "the cube of the scale factor", "always 1"]),
        ("Two rectangles are similar if and only if…",
         "their side ratios length:width match", "All angles are already 90°, so similarity reduces to a single side-ratio match.",
         ["they have the same area", "they have the same perimeter", "one pair of sides is equal"]),
        ("AA similarity requires…",
         "two pairs of congruent corresponding angles", "Two angles force the third, so the triangles have the same angle set.",
         ["two pairs of congruent sides", "three pairs of congruent sides", "a right angle in each"]),
        ("SAS similarity uses two pairs of proportional sides and the…",
         "included angle congruent", "The included angles must match; the sides forming them must be in the same ratio.",
         ["opposite angle congruent", "third side congruent", "hypotenuses equal"]),
        ("SSS similarity requires three pairs of corresponding sides that are…",
         "proportional (same scale factor)", "Unlike SSS congruence, the sides need not be equal — only in proportion.",
         ["equal", "perpendicular", "parallel"]),
        ("A triangle with angles 40° and 70° is similar to a triangle with angles 70° and 40° by…",
         "AA", "Both have angles 40°, 70°, and 70°? 180-40-70=70, so 40-70-70. The other also 40-70-70. AA applies.",
         ["SSS congruence", "HL", "SSA"]),
        ("Vertical angles at an intersection of two lines can supply AA when…",
         "each triangle also has another pair of congruent angles (often from parallels)",
         "Vertical angles give one pair; you still need a second pair for AA.",
         ["vertical angles alone always prove congruence", "vertical angles prove SSS", "you never need a second pair"]),
        ("A midsegment of a triangle is parallel to the third side and is…",
         "half as long", "Triangle Midsegment Theorem: the midsegment is 1/2 of the third side and parallel to it.",
         ["twice as long", "the same length", "one-third as long"]),
        ("A line parallel to one side of a triangle intersecting the other two sides divides those sides…",
         "proportionally", "Triangle Proportionality Theorem (Thales): AM/MB = AN/NC if MN ∥ BC.",
         ["into congruent pieces always", "randomly", "into equal areas always"]),
        ("In △ABC with DE ∥ BC and D on AB, E on AC, if AD=4, DB=6, and AE=6, then EC=…",
         9, "4/6=6/EC, so 4·EC=36, EC=9.",
         [6, 4, 10]),
        ("If a parallel line cuts two sides of a triangle into segments 3 and 5 on one side, the other side’s pieces are in the ratio…",
         "3:5", "Corresponding segments are proportional, so the other side splits in the same 3:5 ratio.",
         ["5:3 always, reversed", "3:8", "1:1"]),
        ("An angle bisector in a triangle divides the opposite side in the ratio of…",
         "the adjacent sides", "Angle Bisector Theorem: BD/DC = AB/AC if BD bisects ∠A.",
         ["the altitudes", "the medians", "1:1 always"]),
        ("A 6-ft pole casts an 8-ft shadow. A tree casts a 20-ft shadow at the same time. The tree’s height is…",
         15, "Similar right triangles: 6/8=h/20, h=15.",
         [12, 18, 24]),
        ("A person 5 ft tall standing 12 ft from a lamppost 15 ft high has a shadow of length…",
         6, "Similar triangles: 15/(12+s)=5/s, 15s=5(12+s), 15s=60+5s, 10s=60, s=6.",
         [4, 8, 10]),
        ("To find a river’s width with a mirror on the ground, you use…",
         "similar right triangles (equal angles of incidence)",
         "The mirror makes two right triangles with a shared acute angle, so AA similarity applies.",
         ["SSS congruence only", "circle theorems", "coordinate midpoints only"]),
        ("A map scale of 1:20000 means 3 cm on the map represents how many meters on the ground?",
         600, "3×20000=60000 cm=600 m.",
         [60, 6000, 20]),
        ("Indirect measurement works because the triangles are similar, so corresponding sides are…",
         "proportional", "You set up a proportion, not a congruence of lengths.",
         ["equal", "supplementary", "perpendicular"]),
        ("A dilation with center O and scale factor k=2 sends P to P′ with OP′=…",
         "2·OP", "Every ray from the center is scaled by k. Distances from O multiply by |k|.",
         ["OP/2", "OP+2", "OP"]),
        ("A dilation with k=1/2 is a…",
         "contraction toward the center", "0<k<1 shrinks figures toward the center. k>1 enlarges.",
         ["translation", "reflection", "rotation of 180°"]),
        ("Under a dilation about the origin with k=3, the image of (2,−1) is…",
         "(6,−3)", "Multiply both coordinates by 3.",
         ["(5,2)", "(2,−3)", "(3,−1)"]),
        ("Dilations preserve…",
         "angle measures (and shape)", "A dilation is a similarity transformation. Angles stay the same; lengths scale.",
         ["all lengths", "orientation only if k<0? they preserve angles regardless", "area"]),
        ("If k=−2 about the origin, (3,1) maps to…",
         "(−6,−2)", "A negative scale factor scales and rotates 180° about the center (through the origin here).",
         ["(6,2)", "(−3,−1)", "(3,−2)"]),
        ("If similar figures have scale factor 3, the ratio of their areas is…",
         "9:1", "Area scales by k². 3²=9.",
         ["3:1", "27:1", "6:1"]),
        ("If similar solids have scale factor 2, the ratio of their volumes is…",
         "8:1", "Volume scales by k³. 2³=8.",
         ["2:1", "4:1", "6:1"]),
        ("Two similar triangles have area ratio 16:25. The scale factor (smaller to larger) is…",
         "4:5", "Scale factor is the square root of the area ratio.",
         ["16:25", "8:10.5", "2:5"]),
        ("Corresponding sides 6 and 9 belong to similar triangles. The ratio of their areas is…",
         "4:9", "Scale factor 6/9=2/3, area ratio (2/3)²=4/9, or 4:9 comparing small to large.",
         ["2:3", "6:9", "8:27"]),
        ("A photo is enlarged with k=2. If the original area is 20 cm², the enlargement’s area is…",
         80, "Area multiplies by 2²=4, so 80.",
         [40, 60, 100]),
        ("ABCD ~ WXYZ with AB=8, WX=12, and BC=10. Find XY.",
         15, "8/12=10/XY, XY=15.",
         [6, 12, 20]),
        ("Two similar triangles have perimeters 18 and 30. A side of 6 on the smaller corresponds to…",
         10, "Scale factor 18/30=3/5, so 6 corresponds to 10.",
         [8, 12, 15]),
        ("DE ∥ BC in △ABC, AD=3, AB=12. If AC=16, then AE=…",
         4, "AD/AB=AE/AC, 3/12=AE/16, AE=4.",
         [12, 8, 6]),
        ("A 4-m stick 6 m from a building lines up with the top. From the same spot the building’s top is 18 m along the ray. Building height?",
         12, "Similar triangles: 4/6=h/18, h=12.",
         [9, 16, 8]),
        ("Dilation about (0,0) with k=1/2 sends (8,−6) to…",
         "(4,−3)", "Halve each coordinate.",
         ["(16,−12)", "(8,−3)", "(4,−6)"]),
        ("AA is enough for triangles (not general polygons) because…",
         "the third angles then match automatically", "Angle sum forces the third pair. Quadrilaterals need more than two angles.",
         ["triangles have no sides", "AA is actually SSS", "all triangles are congruent"]),
        ("A line parallel to the bases of a trapezoid (midsegment) has length equal to…",
         "the average of the two bases", "Trapezoid midsegment = (b1+b2)/2. (Triangle midsegment is the special case b2=0.)",
         ["the longer base", "the difference of the bases", "the product of the bases"]),
        ("If k=4 for similar polygons, a 5-cm side corresponds to…",
         20, "Lengths multiply by 4.",
         [9, 16, 25]),
        ("Scale factor from large to small is 2/5. The small perimeter is 40. The large perimeter is…",
         100, "Small/large=2/5=40/P, P=100.",
         [16, 80, 50]),
        ("In △ABC, a bisector of ∠A meets BC at D with AB=8, AC=12, BD=6. Then DC=…",
         9, "Angle Bisector Theorem: 6/DC=8/12=2/3, so DC=9.",
         [6, 8, 4]),
        ("Two similar right triangles have hypotenuses 5 and 15. A leg of 3 on the small one corresponds to…",
         9, "Scale factor 3, so 3×3=9.",
         [5, 12, 6]),
        ("A dilation with k=1 is…",
         "the identity (every point stays put)", "Scale factor 1 leaves distances from the center unchanged.",
         ["a point reflection", "undefined", "a translation by 1"]),
        ("Area ratio 9:4 means the linear scale factor (large to small) is…",
         "3:2", "√9:√4 = 3:2.",
         ["9:4", "81:16", "6:2"]),
        ("If MN ∥ BC with AM=2, MB=5, the ratio AN:NC equals…",
         "2:5", "Proportionality theorem: the other side splits in the same ratio as AD:DB, here 2:5.",
         ["5:2", "2:7", "1:1"]),
        ("Similar triangles with scale 5:2 have area ratio…",
         "25:4", "Square the scale factor.",
         ["5:2", "10:4", "125:8"]),
        ("A 2-by-3 rectangle dilated by k=4 has area…",
         96, "Original area 6, times 16, is 96. Or 8-by-12 rectangle.",
         [24, 48, 12]),
        ("SAT Stretch: Nested similar triangles share ∠A. The small has sides 4,5,6 and the large has side 10 opposite the same angle as the 5. The large perimeter is…",
         30, "Correspondence: 5 corresponds to 10, so k=2. Large sides 8,10,12; perimeter 30.",
         [20, 24, 15]),
        ("SAT Stretch: DE ∥ BC, AD=x, DB=x+3, AE=4, EC=6. Then x=…",
         6, "x/(x+3)=4/6=2/3, 3x=2x+6, x=6.",
         [4, 3, 9]),
        ("SAT Stretch: A 1.8 m student 3.6 m from a mirror on the ground sees a flagpole top. The mirror is 12 m from the pole. Flagpole height?",
         6, "Similar right triangles: 1.8/3.6=h/12, h=6.",
         [4.8, 9, 7.2]),
        ("SAT Stretch: △ABC ~ △ACB would force the triangle to be…",
         "isosceles with AB=AC",
         "The correspondence swaps B and C, so AB corresponds to AC, forcing AB=AC.",
         ["scalene", "equilateral only", "right always"]),
        ("SAT Stretch: Dilate △(0,0),(4,0),(0,6) about the origin with k=1/2, then the image’s area is…",
         3, "Original area (1/2)·4·6=12. Area scales by (1/2)²=1/4, so 3.",
         [6, 12, 1.5]),
        ("SAT Stretch: Two similar triangles have sides 6 and x corresponding, and 9 and 15 corresponding. x=…",
         10, "6/x=9/15=3/5, so x=10.",
         [8, 12, 4]),
        ("SAT Stretch: A parallel to the base cuts a triangle’s sides in ratio 2:3 (top:bottom). If the large area is 25, the small top triangle’s area is…",
         4, "Linear ratio of small to large is 2/(2+3)=2/5. Area ratio 4/25. Small area=4.",
         [10, 8, 16]),
        ("SAT Stretch: Angle bisector from A splits BC into 4 and 10. If AB=6, then AC=…",
         15, "4/10=6/AC, AC=15.",
         [12, 8, 24]),
        ("SAT Stretch: Similar polygons have perimeters 20 and 45 and the smaller area is 48. The larger area is…",
         243, "Scale 20:45=4:9. Area scale 16:81. 48/A=16/81, A=48·81/16=243.",
         [108, 162, 192]),
    ]
    return _pack(rows)


def build_unit4():
    title = "Geometry Unit 4: Similarity & Proportion"
    description = (
        "Similar polygons, AA/SAS/SSS similarity, triangle proportionality, indirect measurement, "
        "dilations, and how scale factor compares to area — with matching diagrams and SAT Stretch items."
    )
    concepts = [
        "Similar polygons",
        "AA, SAS, SSS similarity",
        "Triangle proportionality",
        "Indirect measurement",
        "Dilation on the plane",
        "Scale factor and area",
    ]
    c1 = concept_block(
        "1. Similar polygons",
        [
            "Similar polygons have the same shape. Corresponding angles are congruent, and corresponding sides are "
            "proportional — they sit in a single scale factor $k$. We write $ABCD\\sim EFGH$ with vertices in matching order.",
            "The scale factor is a ratio of corresponding lengths: $k=\\dfrac{\\text{image length}}{\\text{original length}}$. "
            "If $k>1$ the image is larger; if $0<k<1$ it is smaller. Congruence is the special case $k=1$.",
            "Perimeters of similar polygons scale by $k$, because perimeter is a sum of lengths. Areas scale by $k^2$, which "
            "is the last lesson of this unit. Do not mix those two ratios.",
            "Correspondence is still everything. $ABCD\\sim CDAB$ would rotate the labeling; $AB$ would match $CD$, not $CD$’s "
            "neighbor. Read the vertex order the way you read a congruence statement.",
            "Rectangles are similar when their length-to-width ratios match, because all angles are already $90^\\circ$. "
            "Two squares are always similar. Two rhombuses need not be (their angles can differ).",
            "Similarity is the language of maps, scale models, shadows, and later trigonometry. This lesson names the "
            "parts; the next lessons give triangle tests that prove two polygons are similar.",
        ],
        "If you treat similar as “pretty close” instead of “proportional sides plus congruent angles,” every SAT proportion "
        "in this unit will be set up with the wrong correspondence.",
        "Write the vertex order, then write one fraction $\\dfrac{\\text{small}}{\\text{large}}$ and keep that order for every "
        "pair of sides. Mixing $\\dfrac{\\text{small}}{\\text{large}}$ with $\\dfrac{\\text{large}}{\\text{small}}$ in the same proportion is the classic error.",
        lesson_figure(
            _similar_svg(),
            "Similar right triangles with scale factor $1.5$",
            "Angles match; each side of the image is $1.5$ times the corresponding side of the original.",
        )
        + solved(1, "ABCD ~ EFGH with AB=6, EF=9, and BC=10. Find FG.",
                 ["Corresponding sides: AB↔EF and BC↔FG.",
                  "$\\dfrac{6}{9}=\\dfrac{10}{FG}$.",
                  "$FG=15$."],
                 "$15$", "", "Easy")
        + solved(2, "Similar pentagons have corresponding sides 3 and 6. The smaller perimeter is 21. Find the larger perimeter.",
                 ["Scale factor $6/3=2$.",
                  "Perimeters scale by the same factor.",
                  "Larger perimeter $=42$."],
                 "$42$", "", "Medium")
        + solved(3, "Why are two rectangles 2-by-4 and 3-by-6 similar, while 2-by-4 and 3-by-5 are not?",
                 ["All rectangle angles are 90°, so only the side ratios matter.",
                  "$2/4=1/2$ and $3/6=1/2$, so the first pair is similar.",
                  "$3/5\\neq 1/2$, so 3-by-5 is a different shape."],
                 "side ratios must match", "", "Hard"),
        ("Matching sides that are not corresponding",
         "The longest side of one polygon must match the longest side of the other. Pairing a short side with a long side "
         "because they “look close” breaks the scale factor."),
        ("Lock one fraction and reuse it",
         "Write $k=\\dfrac{6}{9}$ at the top of the page and use that same $k$ for every other pair. This prevents flipping "
         "one ratio in a four-term proportion."),
        [
            "I can use vertex order to name corresponding parts.",
            "I can compute a missing side from a scale factor.",
            "I can scale a perimeter by $k$, not by $k^2$.",
        ],
        1,
    )
    c2 = concept_block(
        "2. AA, SAS, and SSS similarity",
        [
            "For triangles, AA (Angle-Angle) is enough: two pairs of congruent corresponding angles imply the third pair "
            "matches as well, so the triangles are similar. This is the workhorse of the unit.",
            "SAS similarity is not SAS congruence. You need two pairs of sides proportional and the included angles congruent. "
            "The sides that form the angle must be the ones in the ratio.",
            "SSS similarity needs three pairs of corresponding sides in the same ratio. The triangles need not be the same "
            "size, so this is weaker than SSS congruence and stronger than “three random sides.”",
            "A pair of vertical angles, or a pair of corresponding angles from parallel lines, often supplies one of the "
            "two angles for AA. Shared angles in overlapping similar triangles supply the other.",
            "AAA is similarity, not congruence — that is the Unit 3 warning in reverse. Here AAA (or AA) is exactly what "
            "you want. Do not over-prove by hunting for a side you do not need.",
            "Once similar, corresponding sides are proportional and corresponding angles are congruent. That proportion is "
            "how you compute a missing length in every remaining lesson of the unit.",
        ],
        "AA from a shared angle plus a pair of parallels is the standard SAT similar-triangle setup. If you can spot it, "
        "the algebra is a single proportion.",
        "Mark every congruent-angle pair first (vertical, corresponding, shared). If you already have two, write AA and "
        "stop hunting. Then set up one proportion of corresponding sides.",
        lesson_figure(
            _similar_svg(),
            "AA similarity of two right triangles",
            "A shared (or matching) acute angle plus the right angles gives AA.",
        )
        + solved(4, "A triangle has angles 40° and 70°. Another has angles 70° and 40°. Why are they similar?",
                 ["Each has a 40° and a 70° angle.",
                  "The third angles are both 70° as well (isosceles), but two matches already suffice.",
                  "AA similarity applies."],
                 "AA", "", "Easy")
        + solved(5, "Two triangles have sides 3,4,5 and 6,8,10. Why are they similar?",
                 ["$6/3=8/4=10/5=2$.",
                  "Three pairs of sides are proportional.",
                  "SSS similarity applies (they are also congruent-scaled 3-4-5 triangles)."],
                 "SSS similarity with $k=2$", "", "Medium")
        + solved(6, "In △ABC and △DEF, AB/DE=AC/DF and ∠A=∠D. Why similar?",
                 ["AB and AC form ∠A; DE and DF form ∠D.",
                  "Two sides proportional and the included angles congruent.",
                  "SAS similarity applies."],
                 "SAS similarity", "If the congruent angles were not included, this would not be a similarity shortcut.", "Hard"),
        ("Using SAS congruence numbers on a similarity problem",
         "SAS congruence needs equal sides, not proportional sides. If the sides are 3,4 versus 6,8, you want SAS similarity, "
         "not SAS congruence. The included-angle picture is the same; the side requirement is not."),
        ("Mark AA before you write a proportion",
         "If you cannot name two congruent-angle pairs, you are not ready to set corresponding sides in a ratio. Prove "
         "similarity first, then compute."),
        [
            "I can apply AA from two pairs of angles.",
            "I can apply SAS and SSS similarity with a scale factor.",
            "I can distinguish similarity shortcuts from congruence shortcuts.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Triangle proportionality",
        [
            "If a line parallel to one side of a triangle intersects the other two sides, it divides those sides "
            "proportionally. That is the Triangle Proportionality Theorem (sometimes called Thales’ theorem).",
            "In symbols: if $DE\\parallel BC$ with $D$ on $AB$ and $E$ on $AC$, then $\\dfrac{AD}{DB}=\\dfrac{AE}{EC}$. "
            "You may also use $\\dfrac{AD}{AB}=\\dfrac{AE}{AC}$, which compares each piece to the whole side.",
            "The converse is a parallel test: if a line divides two sides of a triangle proportionally, then it is parallel "
            "to the third side. This is how some proofs establish $DE\\parallel BC$ without angle chasing.",
            "A midsegment joins the midpoints of two sides. It is parallel to the third side and half as long. That is "
            "proportionality with ratio $1:1$ on the two split sides, so $k=1/2$ toward the third side.",
            "The Angle Bisector Theorem is a cousin: an angle bisector divides the opposite side in the ratio of the "
            "adjacent sides, $\\dfrac{BD}{DC}=\\dfrac{AB}{AC}$. It is still a proportion, but the parallel is not required.",
            "These theorems are the algebraic engine of nested similar triangles. The small triangle on top is similar to "
            "the original, and the parallel line is what created the AA match.",
        ],
        "A parallel inside a triangle is the most common SAT geometry proportion. If you mix $AD/DB$ with $AD/AB$ in the "
        "same equation, the algebra will still look pretty and the answer will be wrong.",
        "Decide first: pieces-to-pieces ($AD/DB=AE/EC$) or pieces-to-wholes ($AD/AB=AE/AC$). Draw both segments, label the "
        "numbers, and pick one style. Do not mix them.",
        lesson_figure(
            _prop_svg(),
            "$DE\\parallel BC$ inside $\\triangle ABC$",
            "The parallel creates a small triangle similar to the original and splits $AB$ and $AC$ proportionally.",
        )
        + solved(7, "DE ∥ BC, AD=4, DB=6, AE=6. Find EC.",
                 ["Because $DE\\parallel BC$, corresponding side pieces are proportional: $AD/DB=AE/EC$.",
                  "Write $4/6=6/EC$.",
                  "Cross-multiply: $4\\cdot EC=36$, so $EC=9$."],
                 "$9$", "", "Easy")
        + solved(8, "DE ∥ BC, AD=3, AB=12, AC=16. Find AE.",
                 ["This time the given lengths are a piece and a whole side, so use $AD/AB=AE/AC$.",
                  "Write $3/12=AE/16$.",
                  "Then $AE=16\\cdot 1/4=4$."],
                 "$4$", "AB is the whole side, not the bottom piece DB.", "Medium")
        + solved(9, "An angle bisector from A meets BC at D with AB=8, AC=12, BD=6. Find DC.",
                 ["The Angle Bisector Theorem says $BD/DC=AB/AC$.",
                  "So $6/DC=8/12=2/3$.",
                  "Then $2\\cdot DC=18$ and $DC=9$."],
                 "$9$", "", "Hard"),
        ("Mixing part/part with part/whole",
         "Writing $AD/DB=AE/AC$ pairs a part-to-part ratio with a part-to-whole ratio. The two sides of the equation are "
         "not the same kind of fraction. Pick one theorem form and stay with it."),
        ("Label the parallel first",
         "If the problem says $DE\\parallel BC$, mark arrows on those segments before placing numbers. The parallel is what "
         "justifies the proportion; without it you would need another reason (midpoints, a bisector, or AA)."),
        [
            "I can write a correct proportion from a parallel in a triangle.",
            "I can use a midsegment as half the third side.",
            "I can apply the Angle Bisector Theorem.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Indirect measurement",
        [
            "Indirect measurement uses similar triangles to find a length you cannot reach with a ruler: a tree, a building, "
            "a river width. Shadows, mirrors, and sight lines are the usual physical setups.",
            "At the same time of day, a pole and a tree cast shadows that form similar right triangles with the sun’s rays. "
            "The acute sun angle is the same for both, so AA applies. Then $\\dfrac{\\text{pole}}{\\text{pole shadow}}=\\dfrac{\\text{tree}}{\\text{tree shadow}}$.",
            "A mirror on the ground uses the fact that the angle of incidence equals the angle of reflection, creating two "
            "similar right triangles that share that acute angle. The person’s height over distance-to-mirror matches the "
            "object’s height over distance-from-mirror-to-object.",
        "Sight-line problems (a stick lining up with a building) are nested similar triangles. The small triangle from "
            "eye to stick is similar to the large triangle from eye to building.",
            "Map scales are similarity in disguise: $1:20000$ means every length on the map is multiplied by $20000$ to "
            "get the ground length. Convert units at the end (cm to m, for example).",
            "The algebra is always one proportion of corresponding sides. The geometry work is confirming AA (same sun "
            "angle, shared angle, or equal reflection angles) so the proportion is legal.",
        ],
        "Word problems on SAT Math that mention shadows or flagpoles are this lesson. If you set height/height equal to "
        "shadow/height, you have mixed corresponding parts and the answer will be a distractor.",
        "Sketch two separate similar triangles, even if the word problem did not. Label the two heights and the two "
        "shadows in corresponding positions, then write one fraction equals another.",
        lesson_figure(
            _similar_svg(),
            "A pole and a tree as similar right triangles",
            "Matching acute sun angles give AA; heights over shadows are proportional.",
        )
        + solved(10, "A 6-ft pole casts an 8-ft shadow. A tree casts a 20-ft shadow. Find the tree’s height.",
                 ["AA from the equal sun angles.",
                  "$6/8=h/20$.",
                  "$h=15$."],
                 "$15$ ft", "", "Easy")
        + solved(11, "A 1.8 m student stands 3.6 m from a mirror and sees a flagpole 12 m beyond the mirror. Find the flagpole height.",
                 ["Similar right triangles from equal reflection angles.",
                  "$1.8/3.6=h/12$.",
                  "$h=6$."],
                 "$6$ m", "", "Medium")
        + solved(12, "A person 5 ft tall stands 12 ft from a 15-ft lamppost. Find the shadow length s.",
                 ["Large triangle: lamppost over (12+s). Small triangle: person over s.",
                  "$15/(12+s)=5/s$.",
                  "$15s=5(12+s)$, $15s=60+5s$, $10s=60$, $s=6$."],
                 "$6$ ft", "The small triangle is not 5 over 12; 12 is the gap from person to post, not the shadow.", "Hard"),
        ("Pairing a height with the wrong shadow",
         "Corresponding sides are height-with-height and shadow-with-shadow, or height-over-shadow for each object. Mixing "
         "the pole’s height with the tree’s shadow in a single fraction breaks AA correspondence."),
        ("Draw both triangles before the proportion",
         "A 15-second sketch with two right triangles and the shared sun angle prevents using adjacent-side lengths from "
         "the physical layout that are not corresponding sides."),
        [
            "I can set up a shadow proportion from AA.",
            "I can handle a mirror or sight-line similar-triangle model.",
            "I can convert a map scale into a real length.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Dilation on the plane",
        [
            "A dilation with center $O$ and scale factor $k$ sends each point $P$ to a point $P'$ on ray $\\overrightarrow{OP}$ "
            "with $OP'=|k|\\cdot OP$. If $k<0$, the image is on the opposite ray (a $180^\\circ$ turn through the center as well as a scale).",
            "In coordinates, a dilation about the origin is $(x,y)\\mapsto(kx,ky)$. About a general center $C$, you subtract "
            "$C$, multiply by $k$, and add $C$ back.",
            "Dilations preserve angle measure and send lines to parallel lines (unless the line through the center stays "
            "on itself). They do not preserve length unless $|k|=1$. That is why a dilation is a similarity transformation.",
            "The image of a polygon is a similar polygon with scale factor $|k|$. Orientation reverses when $k<0$, but "
            "angles are still congruent.",
            "$0<k<1$ shrinks toward the center (a contraction). $k>1$ enlarges. $k=1$ is the identity. $k=0$ crushes "
            "everything to the center, which is not useful as a similarity of a figure with size.",
            "Dilations explain why nested similar triangles pointing the same way appear in a triangle with a parallel: "
            "the small triangle is a dilation of the large one about the shared vertex.",
        ],
        "Coordinate questions that say “dilate by 3 about the origin” are this lesson in one line: multiply. About another "
        "center, they are a three-step translation-scale-translation, which is a frequent SAT miss.",
        "If the center is the origin, multiply. If not, write a tiny table: original, minus center, times $k$, plus center. "
        "Skipping the minus-center step scales about the origin by accident.",
        lesson_figure(
            _dilate_svg(),
            "Dilation about $O$ with $k=2$",
            "Each image point lies on the ray from $O$ through the original point, twice as far out.",
        )
        + solved(13, "Dilate (2,−1) about the origin by k=3.",
                 ["A dilation about the origin multiplies each coordinate by $k$.",
                  "Compute $3\\cdot 2=6$ and $3\\cdot(-1)=-3$.",
                  "The image is $(6,-3)$."],
                 "$(6,-3)$", "", "Easy")
        + solved(14, "Dilate (8,−6) about the origin by k=1/2.",
                 ["Here $k=1/2$, so each coordinate is halved.",
                  "$8\\cdot\\dfrac{1}{2}=4$ and $-6\\cdot\\dfrac{1}{2}=-3$.",
                  "The image is $(4,-3)$."],
                 "$(4,-3)$", "", "Medium")
        + solved(15, "Dilate (3,1) about the origin by k=−2.",
                 ["Multiply by $k=-2$: $(-6,-2)$.",
                  "A negative scale factor also rotates the point $180^\\circ$ about the origin.",
                  "The distance from the origin is doubled, and the image lies on the opposite ray."],
                 "$(-6,-2)$", "", "Hard"),
        ("Scaling about the origin when the center is another point",
         "If the center is $(1,0)$ and you simply multiply coordinates by $k$, you dilated about $(0,0)$ instead. Always "
         "subtract the center first."),
        ("Plot the ray from the center",
         "Even in a coordinate problem, sketch $O$, $P$, and the ray. The image must sit on that ray. A point off the ray "
         "cannot be the dilation image."),
        [
            "I can dilate a point about the origin by multiplying.",
            "I can interpret $k<0$ as a scale plus a $180^\\circ$ turn.",
            "I can connect a dilation to a similar image polygon.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Scale factor versus area",
        [
            "If corresponding lengths of similar figures are in the ratio $k$, then corresponding areas are in the ratio "
            "$k^2$ and corresponding volumes (for similar solids) are in the ratio $k^3$. Length, area, and volume do not share a ratio.",
            "This is because area is built from two length factors. A rectangle $3$ by $4$ scaled by $2$ becomes $6$ by $8$, "
            "and $6\\cdot8=48=4\\cdot(3\\cdot4)$. The extra factor of $4$ is $2^2$.",
            "Going backwards: if the area ratio is $16:25$, the linear scale factor is $4:5$, the positive square root of "
            "the area ratio. If the volume ratio is $8:27$, the linear scale factor is $2:3$.",
            "A parallel that cuts a triangle, creating a small triangle on top similar to the original, is the usual exam "
            "setting. If the small triangle’s sides are $2/5$ of the large, the small area is $4/25$ of the large area.",
            "Perimeters still use $k$, not $k^2$. A question that gives two perimeters and one area is asking you to find "
            "$k$ from the perimeters, square it, and scale the area.",
            "This is the last similarity idea of the course and one of the most missed: students square a perimeter ratio "
            "they already squared, or they forget to square a side ratio. Name whether the given numbers are lengths or areas before you compute.",
        ],
        "SAT Stretch items in this unit almost always hide $k^2$. If the problem mentions area after talking about similar "
        "triangles, square the scale factor. If it mentions a missing side after talking about areas, take a square root.",
        "Write three labels in a column: length $k$, area $k^2$, volume $k^3$. Circle which row the given numbers belong "
        "to, then move to the row the question asks for.",
        lesson_figure(
            _similar_svg(),
            "Linear scale $1.5$ means area scale $2.25$",
            "Each length is $3/2$ of the original; the area is $(3/2)^2=9/4$ of the original.",
        )
        + solved(16, "Similar figures have scale factor 3. Find the ratio of their areas.",
                 ["Corresponding lengths scale by $k$, but areas scale by $k^2$.",
                  "Here $k=3$, so the area factor is $3^2=9$.",
                  "The larger-to-smaller area ratio is therefore $9:1$."],
                 "$9:1$", "", "Easy")
        + solved(17, "Similar triangles have area ratio 16:25. Find the scale factor of corresponding sides (small to large).",
                 ["The area ratio is $k^2$, so the side scale factor $k$ is the square root of the area ratio.",
                  "Take square roots of both parts: $\\sqrt{16}:\\sqrt{25}=4:5$.",
                  "Check: $4^2:5^2=16:25$, which matches the given area ratio, so the side scale is $4:5$."],
                 "$4:5$", "", "Medium")
        + solved(18, "Similar polygons have perimeters 20 and 45. The smaller area is 48. Find the larger area.",
                 ["Length ratio $20:45=4:9$.",
                  "Area ratio $16:81$.",
                  "$48/A=16/81$, so $A=48\\cdot 81/16=243$."],
                 "$243$", "", "Hard"),
        ("Using k for area",
         "A scale factor of 3 does not triple the area. It multiplies area by 9. Using 3 on an area is the most common "
         "similarity arithmetic error in the course."),
        ("Name the dimension before the arithmetic",
         "Ask “is this a length, an area, or a volume?” out loud. Then choose $k$, $k^2$, or $k^3$. That one-word check "
         "is the whole lesson."),
        [
            "I can scale area by $k^2$ and volume by $k^3$.",
            "I can recover $k$ from an area ratio by taking square roots.",
            "I can combine a perimeter ratio with an area in a two-step problem.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
