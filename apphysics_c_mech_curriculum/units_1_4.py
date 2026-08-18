"""AP Physics C: Mechanics units 1–4 (calculus-based kinematics through momentum)."""
from __future__ import annotations

import math

from curriculum_kit import lesson_figure, svg_circle, svg_rect

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, mq,
    xy_graph, sample_curve,
    fbd_box, energy_bars_svg, incline_svg, energy_diagram_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _ican(items):
    return (
        "<p><strong>I can:</strong></p><ul>"
        + "".join(f"<li>{x}</li>" for x in items)
        + "</ul>"
    )


def _pulley_svg():
    return (
        '<svg viewBox="0 0 260 200" width="100%" style="max-width:260px" role="img">'
        '<circle cx="130" cy="48" r="26" fill="#e2e8f0" stroke="#334155" stroke-width="3"/>'
        '<line x1="104" y1="48" x2="104" y2="145" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="156" y1="48" x2="156" y2="112" stroke="#0f172a" stroke-width="2"/>'
        '<rect x="86" y="145" width="36" height="30" fill="#c7d2fe" stroke="#312e81"/>'
        '<rect x="138" y="112" width="36" height="30" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="90" y="165" font-size="11">m1</text>'
        '<text x="142" y="132" font-size="11">m2</text>'
        '<text x="148" y="28" font-size="11">pulley</text>'
        "</svg>"
    )


def _rocket_svg():
    return (
        '<svg viewBox="0 0 240 200" width="100%" style="max-width:240px" role="img">'
        '<polygon points="120,18 148,78 92,78" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<rect x="100" y="78" width="40" height="52" fill="#bfdbfe" stroke="#1e3a8a"/>'
        '<polygon points="100,130 78,168 100,130" fill="#fdba74"/>'
        '<polygon points="140,130 162,168 140,130" fill="#fdba74"/>'
        '<polygon points="108,130 120,182 132,130" fill="#f97316"/>'
        '<text x="156" y="48" font-size="11">exhaust v_ex</text>'
        '<text x="152" y="104" font-size="11">m(t)</text>'
        "</svg>"
    )


def _river_svg():
    return (
        '<svg viewBox="0 0 300 170" width="100%" style="max-width:300px" role="img">'
        '<rect x="10" y="40" width="280" height="90" fill="#dbeafe" stroke="#1e3a8a"/>'
        '<line x1="40" y1="85" x2="140" y2="85" stroke="#b91c1c" stroke-width="3"/>'
        '<polygon points="138,80 152,85 138,90" fill="#b91c1c"/>'
        '<line x1="40" y1="85" x2="40" y2="30" stroke="#15803d" stroke-width="3"/>'
        '<polygon points="35,32 40,18 45,32" fill="#15803d"/>'
        '<text x="90" y="78" font-size="11" fill="#b91c1c">v_current</text>'
        '<text x="48" y="28" font-size="11" fill="#15803d">v_boat/water</text>'
        '<text x="170" y="130" font-size="11">river bank</text>'
        "</svg>"
    )


def _add(qs, rows):
    for text, ans, expl, dist in rows:
        qs.append(mq(text, ans, expl, len(qs) + 1, distractors=dist))
    return qs


# ===========================================================================
# UNIT 1: Kinematics with Calculus
# ===========================================================================

def _u1_questions():
    qs = []
    _add(qs, [
        ("If $x=3t^2$ (meters, $t$ in seconds), what is $v$ at $t=2\\,\\mathrm{s}$? Velocity is $v=dx/dt$.",
         "12 m/s", "Power rule: $v=6t$. At $t=2$, $v=12\\,\\mathrm{m/s}$.",
         ["6 m/s", "3 m/s", "24 m/s"]),
        ("A cart follows $x=4t^3-2t$. What is its velocity at $t=1\\,\\mathrm{s}$?",
         "10 m/s", "$v=12t^2-2$. At $t=1$, $v=12-2=10\\,\\mathrm{m/s}$.",
         ["2 m/s", "12 m/s", "4 m/s"]),
        ("If velocity is $v=6t$, what is the acceleration $a=dv/dt$?",
         "6 m/s^2", "The derivative of $6t$ is the constant $6$.",
         ["6t m/s^2", "3t^2 m/s^2", "0"]),
        ("Position is $x=5t^2+3t$. What is $a$ (a second derivative)?",
         "10 m/s^2", "$v=10t+3$, then $a=10\\,\\mathrm{m/s}^2$.",
         ["5 m/s^2", "3 m/s^2", "10t m/s^2"]),
        ("For $x=t^3$, the acceleration at $t=2\\,\\mathrm{s}$ is",
         "12 m/s^2", "$v=3t^2$, $a=6t$. At $t=2$, $a=12\\,\\mathrm{m/s}^2$.",
         ["6 m/s^2", "8 m/s^2", "3 m/s^2"]),
        ("Velocity is $v=6t$ with $x(0)=0$. Integrate to find $x$ at $t=2\\,\\mathrm{s}$.",
         "12 m", "$x=\\int_0^2 6t\\,dt=3t^2\\big|_0^2=12\\,\\mathrm{m}$.",
         ["6 m", "24 m", "3 m"]),
        ("Constant $a=4\\,\\mathrm{m/s}^2$ and $v(0)=0$. What is $v$ at $t=3\\,\\mathrm{s}$?",
         "12 m/s", "$v=\\int_0^3 4\\,dt=12\\,\\mathrm{m/s}$.",
         ["4 m/s", "7 m/s", "36 m/s"]),
        ("If $v=2t$ and $x(0)=5\\,\\mathrm{m}$, find $x$ at $t=4\\,\\mathrm{s}$.",
         "21 m", "$x=t^2+5$. At $t=4$, $x=16+5=21\\,\\mathrm{m}$.",
         ["8 m", "16 m", "13 m"]),
        ("Acceleration is $a=6t$ with $v(0)=0$. What is $v$ at $t=2\\,\\mathrm{s}$?",
         "12 m/s", "$v=3t^2$. At $t=2$, $v=12\\,\\mathrm{m/s}$.",
         ["6 m/s", "24 m/s", "3 m/s"]),
        ("A particle has $v=4$ (constant). The displacement from $t=0$ to $t=3\\,\\mathrm{s}$ is",
         "12 m", "$\\Delta x=\\int_0^3 4\\,dt=12\\,\\mathrm{m}$.",
         ["4 m", "7 m", "0"]),
        ("Acceleration depends on time: $a=8t$. If $v(0)=2\\,\\mathrm{m/s}$, $v$ at $t=1\\,\\mathrm{s}$ is",
         "6 m/s", "$v=4t^2+2$. At $t=1$, $v=6\\,\\mathrm{m/s}$.",
         ["8 m/s", "10 m/s", "2 m/s"]),
        ("Using $a=v\\,dv/dx$: if $a=6x$ and $v=0$ at $x=0$, then at $x=2$, $v^2$ equals",
         "24", "$v\\,dv=6x\\,dx$. Integrate: $\\tfrac12 v^2=3x^2$, so $v^2=6x^2=24$ at $x=2$.",
         ["12", "6", "36"]),
        ("A force-free particle has $a=-4$ (slowing). Starting from $v=10$ at $t=0$, $v$ at $t=2\\,\\mathrm{s}$ is",
         "2 m/s", "$v=10-4t$. At $t=2$, $v=2\\,\\mathrm{m/s}$.",
         ["6 m/s", "8 m/s", "-4 m/s"]),
        ("If $a=2t$ and $v(0)=3$, the velocity function is",
         "t^2+3", "Antiderivative of $2t$ is $t^2$, plus the initial $3$.",
         ["2t+3", "t^2", "2t^2+3"]),
        ("Given $a=10-2t$ and $v(0)=0$, find $v$ at $t=5\\,\\mathrm{s}$.",
         "25 m/s", "$v=10t-t^2$. At $t=5$, $v=50-25=25\\,\\mathrm{m/s}$.",
         ["50 m/s", "10 m/s", "0"]),
        ("Position is $\\vec r=(t^2)\\,\\hat{\\imath}+(4t)\\,\\hat{\\jmath}$. Speed at $t=1\\,\\mathrm{s}$ is",
         "2\\sqrt{5} m/s", "$\\vec v=(2t,4)$. At $t=1$, $\\vec v=(2,4)$, speed $\\sqrt{4+16}=\\sqrt{20}=2\\sqrt{5}$.",
         ["6 m/s", "4 m/s", "\\sqrt{5} m/s"]),
        ("For $\\vec r=(3t)\\,\\hat{\\imath}+(t^2)\\,\\hat{\\jmath}$, the $y$-acceleration is",
         "2 m/s^2", "$v_y=2t$, so $a_y=2$ (constant).",
         ["0", "t m/s^2", "3 m/s^2"]),
        ("Projectile: $a_x=0$, $a_y=-10\\,\\mathrm{m/s}^2$, $v_{0x}=6$, $v_{0y}=8$. $v_y$ at $t=0.4\\,\\mathrm{s}$ is",
         "4 m/s", "$v_y=8-10(0.4)=4\\,\\mathrm{m/s}$.",
         ["8 m/s", "6 m/s", "-4 m/s"]),
        ("If $x=2t$ and $y=t^2$, the velocity vector at $t=3\\,\\mathrm{s}$ is",
         "(2, 6) m/s", "$v_x=2$, $v_y=2t=6$.",
         ["(2, 9) m/s", "(2t, 2t) m/s", "(6, 2) m/s"]),
        ("A 2D path has $v_x=4t$ and $v_y=3$. Displacement in $x$ from $t=0$ to $1\\,\\mathrm{s}$ is",
         "2 m", "$\\Delta x=\\int_0^1 4t\\,dt=2t^2\\big|_0^1=2\\,\\mathrm{m}$.",
         ["4 m", "3 m", "1 m"]),
        ("Boat velocity relative to water is $8\\,\\mathrm{m/s}$ north. Current is $6\\,\\mathrm{m/s}$ east. Ground speed is",
         "10 m/s", "$|\\vec v|=\\sqrt{8^2+6^2}=10\\,\\mathrm{m/s}$.",
         ["14 m/s", "2 m/s", "8 m/s"]),
        ("Car A has $v_A=20\\,\\mathrm{m/s}$ east. Car B has $v_B=12\\,\\mathrm{m/s}$ east. Velocity of A relative to B is",
         "8 m/s east", "$\\vec v_{AB}=\\vec v_A-\\vec v_B=8\\,\\mathrm{m/s}$ east.",
         ["32 m/s east", "8 m/s west", "12 m/s east"]),
        ("Rain falls at $5\\,\\mathrm{m/s}$ down. A cart moves $12\\,\\mathrm{m/s}$ right. Rain's speed relative to the cart is",
         "13 m/s", "$\\sqrt{5^2+12^2}=13\\,\\mathrm{m/s}$.",
         ["17 m/s", "7 m/s", "12 m/s"]),
        ("If $\\vec v_{P/G}=(3,0)$ and $\\vec v_{Q/G}=(0,4)$, then $\\vec v_{P/Q}$ is",
         "(3, -4) m/s", "$\\vec v_{P/Q}=\\vec v_P-\\vec v_Q=(3,-4)$.",
         ["(3, 4) m/s", "(0, 4) m/s", "(-3, 4) m/s"]),
        ("A walker $1.5\\,\\mathrm{m/s}$ on a walkway $1.0\\,\\mathrm{m/s}$ (same direction) has ground speed",
         "2.5 m/s", "Relative addition when directions match: $1.5+1.0=2.5$.",
         ["0.5 m/s", "1.5 m/s", "1.0 m/s"]),
        ("The slope of an $x(t)$ graph at an instant is",
         "instantaneous velocity", "By definition $v=dx/dt$, which is the slope of $x$ versus $t$.",
         ["displacement", "average speed", "jerk"]),
        ("The signed area under a $v(t)$ graph from $t_1$ to $t_2$ equals",
         "displacement Δx", "$\\Delta x=\\int_{t_1}^{t_2} v\\,dt$.",
         ["average acceleration", "speed", "jerk"]),
        ("A $v(t)$ graph is a straight line through $(0,0)$ and $(4,12)$. Acceleration is",
         "3 m/s^2", "Slope $=12/4=3\\,\\mathrm{m/s}^2=a$.",
         ["12 m/s^2", "4 m/s^2", "0"]),
        ("$v(t)$ is a triangle of height $8\\,\\mathrm{m/s}$ and base $4\\,\\mathrm{s}$. Displacement is",
         "16 m", "Area $=\\tfrac12(4)(8)=16\\,\\mathrm{m}$.",
         ["32 m", "8 m", "4 m"]),
        ("If $x(t)$ has a horizontal tangent at $t=3\\,\\mathrm{s}$, then at that instant",
         "v=0", "A zero slope of $x(t)$ means $v=dx/dt=0$.",
         ["a=0 always", "x=0", "speed is maximum"]),
        ("A particle has $x=t^2-4t$. The time when $v=0$ is",
         "t=2 s", "$v=2t-4=0$ gives $t=2\\,\\mathrm{s}$.",
         ["t=4 s", "t=0", "t=1 s"]),
        ("Given $v=3t^2$ and $x(1)=4$, the position at $t=2\\,\\mathrm{s}$ is",
         "11 m", "$x=t^3+C$. From $t=1$: $1+C=4$ so $C=3$. Then $x(2)=8+3=11$.",
         ["8 m", "7 m", "12 m"]),
        ("Two particles: $x_A=2t$ and $x_B=8-2t$. They meet when",
         "t=2 s", "$2t=8-2t$ so $4t=8$, $t=2\\,\\mathrm{s}$.",
         ["t=4 s", "t=8 s", "t=1 s"]),
        ("If $a=6$ (constant) and $x(0)=0$, $v(0)=0$, then $x(t)$ is",
         "3t^2", "Integrate twice: $v=6t$, $x=3t^2$.",
         ["6t^2", "6t", "t^2"]),
        ("Speed is the magnitude of velocity. If $\\vec v=(-3,4)\\,\\mathrm{m/s}$, speed is",
         "5 m/s", "$\\sqrt{9+16}=5$.",
         ["1 m/s", "7 m/s", "-3 m/s"]),
        ("A $v(t)$ graph stays at $+6\\,\\mathrm{m/s}$ for $2\\,\\mathrm{s}$, then $0$ for $3\\,\\mathrm{s}$. $\\Delta x$ is",
         "12 m", "Only the first interval contributes: $6\\times 2=12\\,\\mathrm{m}$.",
         ["30 m", "18 m", "6 m"]),
        ("Chain-rule form $a=v\\,dv/dx$ is most useful when $a$ is given as a function of",
         "position x", "Then $v\\,dv=a(x)\\,dx$ separates variables in $v$ and $x$.",
         ["time only", "mass", "temperature"]),
        ("If $x=\\cos(2t)$, then $v$ at $t=0$ is",
         "0", "$v=-2\\sin(2t)$. At $t=0$, $\\sin 0=0$.",
         ["-2", "2", "1"]),
        ("Average velocity from $t=0$ to $2\\,\\mathrm{s}$ if $x=t^3$ is",
         "4 m/s", "$\\Delta x=8-0=8$, $\\Delta t=2$, $v_\\mathrm{avg}=4\\,\\mathrm{m/s}$. Instantaneous $v(2)=12$.",
         ["12 m/s", "8 m/s", "2 m/s"]),
        ("A 2D velocity is $\\vec v=(6t, 2)$. The acceleration vector is",
         "(6, 0) m/s^2", "Differentiate each component: $a_x=6$, $a_y=0$.",
         ["(6t, 2)", "(6, 2)", "(0, 2)"]),
        ("Relative velocity in one dimension: if B sees A approaching at $9\\,\\mathrm{m/s}$ and B moves $4\\,\\mathrm{m/s}$ right, A's ground velocity (right positive, approach means A is to the right of B going left) needs a diagram. Simpler: $v_A=5$ right, $v_B=-4$ (left). $v_{A/B}$ is",
         "9 m/s", "$5-(-4)=9$.",
         ["1 m/s", "-9 m/s", "4 m/s"]),
        ("The jerk $j=da/dt$ for $a=6t$ is",
         "6 m/s^3", "Derivative of $6t$ is $6$.",
         ["0", "6t", "3t^2"]),
        ("If a $v(t)$ curve is above the axis then below, displacement can be smaller than distance because",
         "negative area subtracts", "Signed area is $\\Delta x$; distance uses absolute area.",
         ["slope is speed", "acceleration is always negative", "time reverses"]),
        ("Projectile launched with $v_{0x}=10$, $v_{0y}=0$ from $y=20\\,\\mathrm{m}$, $g=10$. Time to ground from $y=\\tfrac12 a t^2$ with $a=-10$ is",
         "2 s", "$20=\\tfrac12(10)t^2$ so $t^2=4$, $t=2\\,\\mathrm{s}$ (downward).",
         ["4 s", "1 s", "\\sqrt{2} s"]),
        ("An $a(t)$ graph is a rectangle of height $5\\,\\mathrm{m/s}^2$ and width $3\\,\\mathrm{s}$. $\\Delta v$ is",
         "15 m/s", "Area under $a(t)$ is $\\Delta v=15\\,\\mathrm{m/s}$.",
         ["5 m/s", "3 m/s", "8 m/s"]),
        ("If $x=e^{2t}$, velocity is $v=2e^{2t}$. At $t=0$, $v$ equals",
         "2 m/s", "$2e^0=2$.",
         ["e^2", "0", "1 m/s"]),
        ("AP Stretch: $a=8x$ with $v=0$ at $x=2\\,\\mathrm{m}$. Using $v\\,dv=a\\,dx$, $v^2$ at $x=4\\,\\mathrm{m}$ is",
         "96", "$\\tfrac12 v^2=4x^2+C$. At $(2,0)$: $0=16+C$, $C=-16$. Then $v^2=8x^2-32$; at $x=4$, $v^2=128-32=96$.",
         ["64", "128", "32"]),
        ("AP Stretch: $x=2t^3-6t$ (SI). The times when the particle is instantaneously at rest in $t>0$ satisfy $t^2=$",
         "1", "$v=6t^2-6=0$ so $t^2=1$.",
         ["3", "2", "6"]),
        ("AP Stretch: $\\vec r=(t^3, 2t^2)$. The speed at $t=2\\,\\mathrm{s}$ is",
         "4√13 m/s", "$\\vec v=(3t^2, 4t)=(12,8)$ at $t=2$, speed $\\sqrt{144+64}=\\sqrt{208}=4\\sqrt{13}$.",
         ["20 m/s", "√13 m/s", "8 m/s"]),
        ("AP Stretch: $a=-4v$ (drag-like) with $v(0)=8$. Separate $dv/v=-4\\,dt$. $v$ at $t=(\\ln 2)/4$ is",
         "4 m/s", "$\\ln(v/8)=-4t$. At $t=(\\ln 2)/4$, $\\ln(v/8)=-\\ln 2$ so $v/8=1/2$, $v=4$.",
         ["8 m/s", "2 m/s", "0"]),
        ("AP Stretch: $v=12t-3t^2$ from $t=0$ to $t=4$. Net displacement $\\int v\\,dt$ equals",
         "32 m", "$\\int_0^4(12t-3t^2)\\,dt=6t^2-t^3\\big|_0^4=96-64=32\\,\\mathrm{m}$. Also $v=0$ at both endpoints, so distance equals $32\\,\\mathrm{m}$ too.",
         ["96 m", "64 m", "16 m"]),
        ("AP Stretch: $a=3x^2$ and $v=0$ at $x=2$. Then $\\tfrac12 v^2$ at $x=4$ is (use $v\\,dv=a\\,dx$)",
         "56", "$\\int_0^v u\\,du=\\int_2^4 3x^2\\,dx=x^3\\big|_2^4=64-8=56$. So $\\tfrac12 v^2=56$.",
         ["56-8=48", "64", "8"]),
        ("AP Stretch: A river is $60\\,\\mathrm{m}$ wide. Boat $3.0\\,\\mathrm{m/s}$ relative to water, aimed straight across; current $2.0\\,\\mathrm{m/s}$ downriver. Downstream drift when the boat lands is",
         "40 m", "Crossing time $t=60/3=20\\,\\mathrm{s}$. Drift $=v_\\mathrm{current}t=2.0\\times 20=40\\,\\mathrm{m}$.",
         ["20 m", "60 m", "90 m"]),
        ("AP Stretch: $x=4t-t^2$. The maximum $x$ occurs where $v=0$. That maximum position is",
         "4 m", "$v=4-2t=0$ at $t=2$. $x(2)=8-4=4\\,\\mathrm{m}$.",
         ["8 m", "2 m", "0"]),
        ("AP Stretch: $\\vec a=(0,-6)$ and $\\vec v_0=(9,12)$. The speed at the highest point is",
         "9 m/s", "$v_y=12-6t=0$ at $t=2\\,\\mathrm{s}$. Then $v_x$ is still $9$, so speed $=9\\,\\mathrm{m/s}$.",
         ["12 m/s", "15 m/s", "0"]),
    ])
    return qs


def build_unit1():
    title = "AP Physics C Mechanics Unit 1: Kinematics with Calculus"
    description = (
        "Kinematics with calculus: derivatives and integrals of motion, variable acceleration, "
        "2D calculus, relative velocity, and motion graphs."
    )
    c1 = concept_block(
        "1. Velocity as dx/dt and acceleration as dv/dt",
        [
            "Position $x(t)$ is a function that tells you the coordinate of a particle at each clock time. "
            "Velocity is the derivative of position: $v=dx/dt$. That sentence is the whole definition. "
            "If $x=3t^2$ with $x$ in meters and $t$ in seconds, the power rule gives $v=6t$. At $t=2\\,\\mathrm{s}$, "
            "$v=12\\,\\mathrm{m/s}$. The units work because the $t^2$ brought down a factor of seconds in the denominator.",
            "Acceleration is the derivative of velocity: $a=dv/dt$. You can also write $a=d^2x/dt^2$, the second "
            "derivative of position. For $x=3t^2$, $v=6t$ and $a=6\\,\\mathrm{m/s}^2$, a constant. If instead "
            "$x=4t^3$, then $v=12t^2$ and $a=24t$, which grows with time. Calculus is what lets acceleration "
            "be a changing function, not only the constant $g$ from Algebra-based Physics 1.",
            "Instantaneous velocity is the slope of the $x(t)$ curve at one instant. Average velocity "
            "$\\Delta x/\\Delta t$ is a chord. Those two numbers match only for straight $x(t)$ lines "
            "(constant $v$). For $x=t^3$ from $t=0$ to $t=2$, $\\Delta x=8$ so $v_\\mathrm{avg}=4\\,\\mathrm{m/s}$, "
            "while $v(2)=3(2)^2=12\\,\\mathrm{m/s}$. Do not mix the two.",
            "Signs matter. If $x$ is decreasing, $dx/dt$ is negative, so $v$ is negative even if the speed "
            "$|v|$ is large. Speed is never the derivative by itself; speed is $|v|$. A particle with "
            "$v=-5\\,\\mathrm{m/s}$ is moving in the negative direction at $5\\,\\mathrm{m/s}$.",
            "On the AP Physics C Mechanics exam you will be given $x(t)$ or $v(t)$ as a polynomial, sine, or "
            "exponential and asked for $v$ or $a$ at a stated time. Differentiate term by term. "
            "Example: $x=5t^2+3t$ gives $v=10t+3$ and $a=10$. Plug in the time last, after differentiating.",
            "The next move in this unit is the reverse: if you know $v(t)$, you recover $x(t)$ by integrating. "
            "Keep the derivative picture in mind so the integral has a meaning — it undoes $d/dt$.",
        ],
        "Every later Mechanics idea that mentions $v$ or $a$ — Newton's second law as $F=dp/dt$, work as a "
        "line integral, SHM as a differential equation — assumes you can pass between $x$, $v$, and $a$ with "
        "calculus, not only with the three constant-acceleration formulas.",
        "Write the function you were given. Circle whether you need a first derivative ($v$ from $x$, or $a$ from $v$) "
        "or a second derivative ($a$ from $x$). Apply the power rule one term at a time, then substitute the time.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: 3 * t * t, 0, 3))],
                points=[(1, 3, "(1 s, 3 m)"), (2, 12, "(2 s, 12 m)")],
                xlim=(0, 3.2), ylim=(-2, 30), xlab="t (s)", ylab="x (m)",
            ),
            "$x=3t^2$ from $t=0$ to $t=3\\,\\mathrm{s}$",
            "The slope of this parabola at each $t$ is $v=6t$. At $t=2\\,\\mathrm{s}$ the slope is $12\\,\\mathrm{m/s}$.",
        )
        + solved(
            1, "Given $x=3t^2$ (SI units), find $v$ and $a$ at $t=2\\,\\mathrm{s}$.",
            [
                "Velocity is the derivative: $v=dx/dt=6t$.",
                "At $t=2\\,\\mathrm{s}$, $v=12\\,\\mathrm{m/s}$.",
                "Acceleration is $a=dv/dt=6\\,\\mathrm{m/s}^2$, already constant, so the same at $t=2\\,\\mathrm{s}$.",
            ],
            "$v=12\\,\\mathrm{m/s}$, $a=6\\,\\mathrm{m/s}^2$",
            "The $12$ is not $3\\times 2^2$; that would be position. Differentiate first.",
            "Easy",
        )
        + solved(
            2, "A bead moves on a wire with $x=4t^3-2t$. Find $v(1)$ and $a(1)$.",
            [
                "Differentiate: $v=12t^2-2$.",
                "At $t=1$, $v=12-2=10\\,\\mathrm{m/s}$.",
                "Differentiate again: $a=24t$. At $t=1$, $a=24\\,\\mathrm{m/s}^2$.",
            ],
            "$v=10\\,\\mathrm{m/s}$, $a=24\\,\\mathrm{m/s}^2$",
            "",
            "Medium",
        )
        + solved(
            3, "Position is $x=t^3-6t^2+9t$. Find all times when the particle is instantaneously at rest, and the acceleration at the earliest such $t>0$.",
            [
                "$v=3t^2-12t+9$. Set $v=0$: divide by $3$ to get $t^2-4t+3=0$.",
                "Factor: $(t-1)(t-3)=0$, so $t=1\\,\\mathrm{s}$ or $t=3\\,\\mathrm{s}$.",
                "$a=6t-12$. At $t=1\\,\\mathrm{s}$, $a=-6\\,\\mathrm{m/s}^2$.",
            ],
            "$t=1\\,\\mathrm{s}$ and $t=3\\,\\mathrm{s}$; $a(1)=-6\\,\\mathrm{m/s}^2$",
            "Rest means $v=0$, not $x=0$ and not $a=0$.",
            "Hard",
        )
        + _ican([
            "I can obtain $v$ from $x(t)$ and $a$ from $v(t)$ using derivatives.",
            "I can tell average velocity apart from instantaneous velocity on a numeric example.",
            "I can interpret the sign of $v$ as direction along the $x$-axis.",
        ]),
        ("Differentiating after plugging in the time",
         "If $x=3t^2$ and you first compute $x(2)=12$, then try to “take a derivative of $12$,” you get $0$, which is nonsense. "
         "Keep $t$ as a symbol, differentiate the function, and only then substitute the number."),
        ("Name the derivative you need before you compute",
         "On FRQs, write “$v=dx/dt$” or “$a=dv/dt$” in words and symbols, then show the derivative. That one line "
         "earns the kinematics justification point even if the algebra later slips."),
        [
            "I can obtain $v$ from $x(t)$ and $a$ from $v(t)$ using derivatives.",
            "I can tell average velocity apart from instantaneous velocity on a numeric example.",
            "I can interpret the sign of $v$ as direction along the $x$-axis.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Integrating to recover motion",
        [
            "Integration undoes differentiation. If $v=dx/dt$, then $x(t)=x(t_0)+\\int_{t_0}^{t} v(\\tau)\\,d\\tau$. "
            "The definite integral of velocity is the change in position. If $v=6t$ and $x(0)=0$, then "
            "$x=\\int_0^{t} 6u\\,du=3t^2$. At $t=2\\,\\mathrm{s}$, $x=12\\,\\mathrm{m}$.",
            "The same idea one level down: $v(t)=v(t_0)+\\int_{t_0}^{t} a(\\tau)\\,d\\tau$. Constant $a=4\\,\\mathrm{m/s}^2$ "
            "and $v(0)=0$ give $v=4t$. That is the familiar $v=at$ from Physics 1, now seen as an integral.",
            "Indefinite integrals produce a family of functions plus a constant $C$. You pin $C$ down with an "
            "initial condition. Example: $v=2t$ and $x(0)=5\\,\\mathrm{m}$ give $x=t^2+C$; then $C=5$, so "
            "$x=t^2+5$. At $t=4\\,\\mathrm{s}$, $x=21\\,\\mathrm{m}$. Forgetting $C$ is the most common error.",
            "Geometrically, $\\int v\\,dt$ is the signed area under the $v(t)$ graph. A rectangle of height "
            "$4\\,\\mathrm{m/s}$ and width $3\\,\\mathrm{s}$ has area $12\\,\\mathrm{m}$ of displacement. "
            "A triangle of base $4\\,\\mathrm{s}$ and height $8\\,\\mathrm{m/s}$ has area $16\\,\\mathrm{m}$.",
            "You can integrate piecewise if $v(t)$ is given in pieces (constant, then linear). Split the integral "
            "at the kinks. Signed area below the time axis is negative displacement: the particle moved backward.",
            "Later, when force is a known function of time, $a=F/m$ and this same integral recovers $v(t)$. "
            "The kinematics skill is the engine; Newton's laws will only supply $a(t)$.",
        ],
        "Work, impulse, and variable-force problems all ask you to accumulate a rate. Recovering $x$ from $v$ "
        "is the cleanest version of that habit, so the course starts here.",
        "Write $x=x_0+\\int v\\,dt$ or $v=v_0+\\int a\\,dt$, antiderive the polynomial, then apply the initial "
        "condition to fix $C$ before you evaluate at the requested time.",
        lesson_figure(
            xy_graph(
                curves=[("#059669", sample_curve(lambda t: 6 * t, 0, 3))],
                points=[(2, 12, "v(2)=12 m/s")],
                xlim=(0, 3.2), ylim=(-2, 22), xlab="t (s)", ylab="v (m/s)",
            ),
            "$v=6t$, whose area from $0$ to $2\\,\\mathrm{s}$ is $x=12\\,\\mathrm{m}$",
            "The triangular area under this line is $\\tfrac12(2)(12)=12\\,\\mathrm{m}$, matching $\\int_0^2 6t\\,dt$.",
        )
        + solved(
            6, "Velocity is $v=6t$ with $x(0)=0$. Find $x$ at $t=2\\,\\mathrm{s}$.",
            [
                "Integrate: $x=\\int_0^2 6t\\,dt=3t^2\\big|_0^2$.",
                "Evaluate: $3(4)-0=12$.",
                "Units: $\\mathrm{m/s}\\times\\mathrm{s}=\\mathrm{m}$, so $x=12\\,\\mathrm{m}$.",
            ],
            "$12\\,\\mathrm{m}$",
            "",
            "Easy",
        )
        + solved(
            7, "$a=6t$ with $v(0)=0$ and $x(0)=4\\,\\mathrm{m}$. Find $x$ at $t=2\\,\\mathrm{s}$.",
            [
                "First $v=\\int_0^t 6u\\,du=3t^2$.",
                "Then $x=4+\\int_0^2 3t^2\\,dt=4+t^3\\big|_0^2=4+8=12\\,\\mathrm{m}$.",
                "Check: $v(2)=12\\,\\mathrm{m/s}$ is consistent with $v=3t^2$.",
            ],
            "$12\\,\\mathrm{m}$",
            "Two integrations, two constants — here both constants were given at $t=0$.",
            "Medium",
        )
        + solved(
            8, "$v=3t^2$ and $x(1)=4\\,\\mathrm{m}$. Find $x(2)$.",
            [
                "Antiderivative: $x=t^3+C$.",
                "Use $t=1$: $1+C=4$ so $C=3$.",
                "Then $x(2)=8+3=11\\,\\mathrm{m}$.",
            ],
            "$11\\,\\mathrm{m}$",
            "The initial time is not zero. Always plug the given $(t,x)$ pair into $x=t^3+C$.",
            "Hard",
        )
        + _ican([
            "I can recover $x(t)$ from $v(t)$ with a definite integral and an initial position.",
            "I can recover $v(t)$ from $a(t)$ the same way.",
            "I can read displacement as signed area under a $v(t)$ graph.",
        ]),
        ("Dropping the constant of integration",
         "The antiderivative of $2t$ is $t^2+C$, not $t^2$. If $x(0)=5$, that $C$ is $5$ meters of actual location. "
         "A missing $C$ shifts the whole trajectory."),
        ("Set limits that match the story",
         "If motion is asked from $t=1$ to $t=2$, use $\\int_1^2$, not $\\int_0^2$. Write the times on the integral "
         "before you antiderive."),
        [
            "I can recover $x(t)$ from $v(t)$ with a definite integral and an initial position.",
            "I can recover $v(t)$ from $a(t)$ the same way.",
            "I can read displacement as signed area under a $v(t)$ graph.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Variable acceleration, including a(x)",
        [
            "When $a$ is not constant, the three SUVAT formulas from Physics 1 are illegal. You must integrate "
            "the actual $a$. If $a$ is a function of time, $a(t)$, use $dv=a\\,dt$. If $a=8t$ and $v(0)=2$, then "
            "$v=4t^2+2$. At $t=1\\,\\mathrm{s}$, $v=6\\,\\mathrm{m/s}$.",
            "Often $a$ is given as a function of position, $a(x)$, because a spring or a spatially varying force "
            "does that. Then the chain rule identity $a=dv/dt=(dv/dx)(dx/dt)=v\\,dv/dx$ is the move. "
            "Rearrange: $v\\,dv=a(x)\\,dx$. Integrate both sides between matching pairs $(x_i,v_i)$ and $(x_f,v_f)$.",
            "Numeric example: $a=6x$ with $v=0$ at $x=0$. Then $\\int_0^{v} u\\,du=\\int_0^{x} 6s\\,ds$, so "
            "$\\tfrac12 v^2=3x^2$, or $v^2=6x^2$. At $x=2\\,\\mathrm{m}$, $v^2=24$. The particle is speeding up "
            "as $|x|$ grows, which matches $a$ pointing the same way as $x$ here.",
            "If $a=-kx/m$ (a spring), the same identity produces $\\tfrac12 mv^2+\\tfrac12 kx^2=$ constant, which "
            "you will later call mechanical energy. Variable-acceleration kinematics is already energy in disguise.",
            "If $a$ depends on $v$, as with linear drag $a=-bv/m$, separate $dv/a(v)=dt$. You will meet that "
            "fully in Unit 2. The skill here is choosing the matching differential: $dt$, $dx$, or $dv$ as the "
            "independent piece.",
            "AP FRQs love to hand you $a=c-bt$ (a rocket that burns out) and ask for $v(t)$ and $x(t)$. Integrate "
            "twice and apply two initial conditions. Do not reach for $v^2=v_0^2+2a\\Delta x$ unless $a$ is constant.",
        ],
        "Springs, gravity that varies with height, and drag all produce non-constant $a$. Physics C is the course "
        "that can actually solve those motions.",
        "Ask: is $a$ given versus $t$, versus $x$, or versus $v$? Then pick $dv=a\\,dt$, $v\\,dv=a\\,dx$, or "
        "$dv/a(v)=dt$ and integrate between the two states in the problem.",
        lesson_figure(
            xy_graph(
                curves=[("#b45309", sample_curve(lambda t: 4 * t * t + 2, 0, 2))],
                points=[(0, 2, "v(0)=2"), (1, 6, "v(1)=6")],
                xlim=(0, 2.2), ylim=(0, 20), xlab="t (s)", ylab="v (m/s)",
            ),
            "$v=4t^2+2$ from $a=8t$ and $v(0)=2\\,\\mathrm{m/s}$",
            "Variable $a(t)$ makes a curved $v(t)$. The slope of this curve is $a=8t$, which is not constant.",
        )
        + solved(
            11, "$a=8t$ and $v(0)=2\\,\\mathrm{m/s}$. Find $v$ at $t=1\\,\\mathrm{s}$.",
            [
                "Integrate: $v=4t^2+C$.",
                "$v(0)=2$ gives $C=2$, so $v=4t^2+2$.",
                "At $t=1$, $v=6\\,\\mathrm{m/s}$.",
            ],
            "$6\\,\\mathrm{m/s}$",
            "",
            "Easy",
        )
        + solved(
            12, "$a=6x$ with $v=0$ at $x=0$. Find $v^2$ at $x=2\\,\\mathrm{m}$.",
            [
                "Use $v\\,dv=a\\,dx=6x\\,dx$.",
                "Integrate: $\\tfrac12 v^2=3x^2$ (both limits start at zero).",
                "At $x=2$, $v^2=6(4)=24$.",
            ],
            "$v^2=24$",
            "",
            "Medium",
        )
        + solved(
            13,
            "$a=6x^2$ with $v=2\\,\\mathrm{m/s}$ at $x=1\\,\\mathrm{m}$. Find $\\tfrac12 v^2$ at $x=2\\,\\mathrm{m}$.",
            [
                "Separate: $v\\,dv=6x^2\\,dx$.",
                "Integrate from the initial state: $\\int_2^{v} u\\,du=\\int_1^2 6x^2\\,dx$.",
                "Right side: $2x^3\\big|_1^2=16-2=14$. Left side: $\\tfrac12 v^2-2$.",
                "So $\\tfrac12 v^2=16$.",
            ],
            "$\\tfrac12 v^2=16$",
            "The integral $\\int_1^2 6x^2\\,dx=14$ is a standard check. Limits must match the two positions.",
            "Hard",
        )
        + _ican([
            "I can integrate $a(t)$ to get $v(t)$ when acceleration depends on time.",
            "I can use $v\\,dv=a(x)\\,dx$ when acceleration depends on position.",
            "I can refuse constant-acceleration formulas when $a$ is not constant.",
        ]),
        ("Using $v^2=v_0^2+2a\\Delta x$ with a variable $a$",
         "That formula assumes a single number $a$. If $a=6x$, there is no single $a$ to plug in. Use the "
         "integral $v\\,dv=a\\,dx$ instead."),
        ("Match the limits on both sides",
         "Left side runs from $v_i$ to $v_f$. Right side runs from $x_i$ to $x_f$. Mixing $v_f$ with $x_i$ "
         "is a classic FRQ loss."),
        [
            "I can integrate $a(t)$ to get $v(t)$ when acceleration depends on time.",
            "I can use $v\\,dv=a(x)\\,dx$ when acceleration depends on position.",
            "I can refuse constant-acceleration formulas when $a$ is not constant.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Two-dimensional motion with calculus",
        [
            "In a plane, position is a vector $\\vec r=x\\,\\hat{\\imath}+y\\,\\hat{\\jmath}$. Velocity is the "
            "derivative of each component: $\\vec v=(dx/dt)\\,\\hat{\\imath}+(dy/dt)\\,\\hat{\\jmath}$. "
            "If $\\vec r=(t^2, 4t)$, then $\\vec v=(2t, 4)$. At $t=1\\,\\mathrm{s}$, $\\vec v=(2,4)\\,\\mathrm{m/s}$ "
            "and the speed is $\\sqrt{4+16}=\\sqrt{20}=2\\sqrt{5}\\,\\mathrm{m/s}$.",
            "Acceleration is $\\vec a=d\\vec v/dt$. Components do not mix: $a_x$ uses only $v_x$. For "
            "$\\vec r=(3t, t^2)$, $a_x=0$ and $a_y=2\\,\\mathrm{m/s}^2$. A projectile near Earth is the special "
            "case $a_x=0$, $a_y=-g$.",
            "Speed is $|\\vec v|$, not a component. Direction of motion is the direction of $\\vec v$, which "
            "is tangent to the path. The acceleration vector can point off the path (changing direction) even "
            "if speed is constant, as in uniform circular motion $a=v^2/r$ inward.",
            "To recover coordinates, integrate each component separately. $v_x=4t$ from $t=0$ to $1$ gives "
            "$\\Delta x=\\int_0^1 4t\\,dt=2\\,\\mathrm{m}$, independent of whatever $v_y$ is doing.",
            "Projectile example with $g=10\\,\\mathrm{m/s}^2$: $v_{0x}=6$, $v_{0y}=8$. Then $v_y=8-10t$. "
            "At $t=0.4\\,\\mathrm{s}$, $v_y=4\\,\\mathrm{m/s}$. Peak occurs when $v_y=0$, here $t=0.8\\,\\mathrm{s}$.",
            "On FRQs, write $\\vec r(t)$, then $\\vec v=d\\vec r/dt$, then $|\\vec v|$ if speed is asked. "
            "Do not average the $x$ and $y$ speeds.",
        ],
        "Circular orbits, pendulums, and rolling objects all live in 2D or 3D. Component calculus is how "
        "Mechanics keeps Newton's laws honest in more than one direction.",
        "Split into $x$ and $y$. Differentiate or integrate each. Recombine with Pythagoras only when a "
        "magnitude (speed or $|\\vec a|$) is asked.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: 2 * math.sqrt(max(x, 0)), 0, 9))],
                points=[(1, 2, "t=1"), (4, 4, "t=2"), (9, 6, "t=3")],
                xlim=(-0.5, 10), ylim=(-0.5, 8), xlab="x (m)", ylab="y (m)",
            ),
            "Path $x=t^2$, $y=4t$ so $y=4\\sqrt{x}$",
            "The path in space is a sideways parabola. Velocity is tangent to this curve, not along the axes.",
        )
        + solved(
            16, "$\\vec r=(t^2)\\,\\hat{\\imath}+(4t)\\,\\hat{\\jmath}$. Find the speed at $t=1\\,\\mathrm{s}$.",
            [
                "$\\vec v=(2t, 4)$.",
                "At $t=1$, $\\vec v=(2,4)\\,\\mathrm{m/s}$.",
                "Speed $=\\sqrt{2^2+4^2}=\\sqrt{20}=2\\sqrt{5}\\,\\mathrm{m/s}$.",
            ],
            "$2\\sqrt{5}\\,\\mathrm{m/s}$",
            "",
            "Easy",
        )
        + solved(
            17, "Projectile: $a_x=0$, $a_y=-10\\,\\mathrm{m/s}^2$, $\\vec v_0=(6,8)\\,\\mathrm{m/s}$. Find $v_y$ at $t=0.4\\,\\mathrm{s}$.",
            [
                "$v_x$ stays $6\\,\\mathrm{m/s}$.",
                "$v_y=8-10t$.",
                "At $t=0.4$, $v_y=8-4=4\\,\\mathrm{m/s}$.",
            ],
            "$4\\,\\mathrm{m/s}$",
            "",
            "Medium",
        )
        + solved(
            18, "$\\vec r=(t^2, t^3)$. Find the speed at $t=1\\,\\mathrm{s}$ and the acceleration vector there.",
            [
                "$\\vec v=(2t, 3t^2)$, so at $t=1$, $\\vec v=(2,3)$ and speed $\\sqrt{13}\\,\\mathrm{m/s}$.",
                "$\\vec a=(2, 6t)$. At $t=1$, $\\vec a=(2,6)\\,\\mathrm{m/s}^2$.",
                "Note $|\\vec a|=\\sqrt{4+36}=\\sqrt{40}$, which is not needed unless asked.",
            ],
            "speed $\\sqrt{13}\\,\\mathrm{m/s}$, $\\vec a=(2,6)\\,\\mathrm{m/s}^2$",
            "",
            "Hard",
        )
        + _ican([
            "I can differentiate vector components separately to get $\\vec v$ and $\\vec a$.",
            "I can compute speed as $|\\vec v|$.",
            "I can integrate each component of $\\vec a$ or $\\vec v$ independently.",
        ]),
        ("Treating speed as $v_x+v_y$",
         "Speed is $\\sqrt{v_x^2+v_y^2}$. Adding components is not a magnitude. For $(2,4)$ the speed is "
         "$2\\sqrt{5}$, not $6$."),
        ("Keep $x$ and $y$ in two columns",
         "On paper, a two-column table ($x$ kinematics | $y$ kinematics) prevents using $v_y$ in an $x$ integral."),
        [
            "I can differentiate vector components separately to get $\\vec v$ and $\\vec a$.",
            "I can compute speed as $|\\vec v|$.",
            "I can integrate each component of $\\vec a$ or $\\vec v$ independently.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Relative velocity",
        [
            "The velocity of object A as seen by observer B is $\\vec v_{A/B}=\\vec v_A-\\vec v_B$, where both "
            "$\\vec v_A$ and $\\vec v_B$ are measured in the same inertial frame (usually the ground). "
            "If car A goes $20\\,\\mathrm{m/s}$ east and car B goes $12\\,\\mathrm{m/s}$ east, A relative to B "
            "is $8\\,\\mathrm{m/s}$ east.",
            "In two dimensions, subtract components. A boat's velocity relative to water plus the water's "
            "velocity relative to ground equals the boat's velocity relative to ground: "
            "$\\vec v_{B/G}=\\vec v_{B/W}+\\vec v_{W/G}$. If the boat goes $8\\,\\mathrm{m/s}$ north relative to "
            "water and the current is $6\\,\\mathrm{m/s}$ east, the ground speed is $\\sqrt{8^2+6^2}=10\\,\\mathrm{m/s}$.",
            "To cross a river in the shortest time, maximize the component perpendicular to the banks. Aiming "
            "straight at the opposite bank (so $\\vec v_{B/W}$ is perpendicular) does that. The current then "
            "carries you downstream, but it does not change the crossing time. An $80\\,\\mathrm{m}$ river with "
            "$2.0\\,\\mathrm{m/s}$ perpendicular component takes $40\\,\\mathrm{s}$.",
            "To land straight across, you must aim upstream so that the downstream components cancel. That "
            "makes the perpendicular component smaller than $|\\vec v_{B/W}|$, so the crossing takes longer.",
            "Relative acceleration is $\\vec a_{A/B}=\\vec a_A-\\vec a_B$. In a single inertial frame with "
            "constant velocities, relative acceleration is zero. Inside an accelerating train the story changes "
            "(Unit 2: inertial frames).",
            "Rain streaks on a side window give the rain's velocity relative to the car, not relative to the "
            "ground. If rain falls at $5\\,\\mathrm{m/s}$ down and the car moves $12\\,\\mathrm{m/s}$ right, "
            "the relative speed is $13\\,\\mathrm{m/s}$ along a slant.",
        ],
        "Atwood constraints, collisions, and center-of-mass frames all compare two velocities. Relative velocity "
        "is the language for “as seen by.”",
        "Draw both velocity arrows in the ground frame, then subtract tip-to-tail: $\\vec v_{A/B}=\\vec v_A-\\vec v_B$. "
        "For boats, write the vector addition $\\vec v_{B/G}=\\vec v_{B/W}+\\vec v_{W/G}$ before you take magnitudes.",
        lesson_figure(
            _river_svg(),
            "Boat velocity relative to water plus current equals ground velocity",
            "The red arrow is the river current. The green arrow is the boat relative to the water. The ground "
            "velocity is their vector sum.",
        )
        + solved(
            21, "Boat $8\\,\\mathrm{m/s}$ north relative to water, current $6\\,\\mathrm{m/s}$ east. Ground speed?",
            [
                "Add perpendicular components: $\\vec v_{B/G}=(6,8)\\,\\mathrm{m/s}$.",
                "Speed $=\\sqrt{36+64}=10\\,\\mathrm{m/s}$.",
                "Direction is $\\tan^{-1}(8/6)$ north of east, if asked.",
            ],
            "$10\\,\\mathrm{m/s}$",
            "",
            "Easy",
        )
        + solved(
            22, "River $80\\,\\mathrm{m}$ wide. Boat $2.0\\,\\mathrm{m/s}$ relative to water, aimed straight across. Crossing time?",
            [
                "The perpendicular component is the full $2.0\\,\\mathrm{m/s}$.",
                "$t=d/v_\\perp=80/2=40\\,\\mathrm{s}$.",
                "Any parallel current changes landing point, not this time.",
            ],
            "$40\\,\\mathrm{s}$",
            "",
            "Medium",
        )
        + solved(
            23,
            "$\\vec v_P=(3,0)\\,\\mathrm{m/s}$ and $\\vec v_Q=(0,4)\\,\\mathrm{m/s}$ in the ground frame. Find $\\vec v_{P/Q}$ and its magnitude.",
            [
                "$\\vec v_{P/Q}=\\vec v_P-\\vec v_Q=(3,-4)\\,\\mathrm{m/s}$.",
                "Magnitude $\\sqrt{9+16}=5\\,\\mathrm{m/s}$.",
                "Q sees P moving $3\\,\\mathrm{m/s}$ east and $4\\,\\mathrm{m/s}$ south.",
            ],
            "$(3,-4)\\,\\mathrm{m/s}$, speed $5\\,\\mathrm{m/s}$",
            "",
            "Hard",
        )
        + _ican([
            "I can subtract ground-frame velocities to get a relative velocity.",
            "I can add boat-relative-to-water and current to get ground velocity.",
            "I can choose aiming straight across when the goal is minimum crossing time.",
        ]),
        ("Adding speeds as scalars when directions differ",
         "An $8\\,\\mathrm{m/s}$ north boat and a $6\\,\\mathrm{m/s}$ east current do not make $14\\,\\mathrm{m/s}$. "
         "They are perpendicular, so Pythagoras gives $10\\,\\mathrm{m/s}$."),
        ("Label every velocity with two subscripts",
         "Write $v_{\\mathrm{boat/water}}$, $v_{\\mathrm{water/ground}}$, $v_{\\mathrm{boat/ground}}$. "
         "The middle letters should cancel like a telescope: $(B/W)+(W/G)=(B/G)$."),
        [
            "I can subtract ground-frame velocities to get a relative velocity.",
            "I can add boat-relative-to-water and current to get ground velocity.",
            "I can choose aiming straight across when the goal is minimum crossing time.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Graphical calculus of motion",
        [
            "A graph of $x$ versus $t$ has slope $v$ and curvature related to $a$. A graph of $v$ versus $t$ has "
            "slope $a$ and signed area $\\Delta x$. A graph of $a$ versus $t$ has signed area $\\Delta v$. "
            "Those three sentences are the entire graphical calculus of 1D motion.",
            "Example: a $v(t)$ line through $(0,0)$ and $(4\\,\\mathrm{s},\\,12\\,\\mathrm{m/s})$ has slope "
            "$a=3\\,\\mathrm{m/s}^2$. The area from $0$ to $4$ is a triangle of area $24\\,\\mathrm{m}$, which is $\\Delta x$.",
            "If $v(t)$ is a triangle of height $8\\,\\mathrm{m/s}$ and base $4\\,\\mathrm{s}$, displacement is "
            "$\\tfrac12(4)(8)=16\\,\\mathrm{m}$. If the triangle dips below the axis, that portion subtracts.",
            "A horizontal tangent on $x(t)$ means $v=0$ at that instant. An inflection of $x(t)$ (concavity change) "
            "means $a$ changes sign. Turning points of $v(t)$ are zeros of $a$.",
            "Distance traveled is the total variation of $x$, equal to the area using absolute value of $v$. "
            "Displacement is net signed area. AP items often ask both, hoping you confuse them.",
            "When an FRQ gives a graph instead of a formula, you still “integrate” by counting squares or using "
            "geometry (triangles, trapezoids). When it gives a formula, you may still sketch $v(t)$ to sanity-check "
            "the sign of $\\Delta x$.",
        ],
        "Many AP Physics C multiple-choice items are graphs with no equation. If slope and area are fluent, "
        "those items are fast points.",
        "For any graph, ask two questions: what is the slope (one derivative down) and what is the area "
        "(one integral up)? Label the axes first so you know which pair you have.",
        lesson_figure(
            xy_graph(
                curves=[("#dc2626", [(0, 0), (2, 8), (4, 0)])],
                points=[(2, 8, "peak v=8")],
                xlim=(-0.3, 4.5), ylim=(-1, 10), xlab="t (s)", ylab="v (m/s)",
            ),
            "$v(t)$ triangle: height $8\\,\\mathrm{m/s}$, base $4\\,\\mathrm{s}$",
            "Displacement equals the triangular area $16\\,\\mathrm{m}$. Slope on the way up is $a=+4\\,\\mathrm{m/s}^2$.",
        )
        + solved(
            26, "A $v(t)$ graph is a straight line from $(0,0)$ to $(4\\,\\mathrm{s},\\,12\\,\\mathrm{m/s})$. Find $a$ and $\\Delta x$.",
            [
                "Slope $a=12/4=3\\,\\mathrm{m/s}^2$.",
                "Area of the triangle $\\Delta x=\\tfrac12(4)(12)=24\\,\\mathrm{m}$.",
                "Both match $v=3t$, $x=\\tfrac32 t^2$ at $t=4$.",
            ],
            "$a=3\\,\\mathrm{m/s}^2$, $\\Delta x=24\\,\\mathrm{m}$",
            "",
            "Easy",
        )
        + solved(
            27, "$v(t)$ is a triangle of height $8\\,\\mathrm{m/s}$ and base $4\\,\\mathrm{s}$. Find displacement.",
            [
                "Area $=\\tfrac12\\times\\mathrm{base}\\times\\mathrm{height}$.",
                "$\\Delta x=\\tfrac12(4)(8)=16\\,\\mathrm{m}$.",
                "If this $v$ never goes negative, distance equals this same $16\\,\\mathrm{m}$.",
            ],
            "$16\\,\\mathrm{m}$",
            "",
            "Medium",
        )
        + solved(
            28,
            "$v=6t-t^2$ from $t=0$ to $t=6\\,\\mathrm{s}$. Find net displacement by integrating.",
            [
                "$\\Delta x=\\int_0^6(6t-t^2)\\,dt=3t^2-t^3/3\\big|_0^6$.",
                "At $6$: $3(36)-216/3=108-72=36\\,\\mathrm{m}$.",
                "Note $v=0$ at $t=0$ and $t=6$, and $v>0$ in between, so distance equals $36\\,\\mathrm{m}$ too.",
            ],
            "$36\\,\\mathrm{m}$",
            "",
            "Hard",
        )
        + _ican([
            "I can read $v$ as the slope of $x(t)$ and $a$ as the slope of $v(t)$.",
            "I can read $\\Delta x$ as signed area under $v(t)$.",
            "I can tell displacement apart from distance on a graph that crosses the time axis.",
        ]),
        ("Calling the value of $v$ the acceleration",
         "At the peak of a $v(t)$ triangle the velocity is large, but the slope is zero, so $a=0$ there. "
         "Height is $v$; slope is $a$."),
        ("Mark + and − regions before computing area",
         "Shade above-axis and below-axis regions in different colors. Net $\\Delta x$ is plus minus, not the "
         "sum of absolute areas, unless the question asked for distance."),
        [
            "I can read $v$ as the slope of $x(t)$ and $a$ as the slope of $v(t)$.",
            "I can read $\\Delta x$ as signed area under $v(t)$.",
            "I can tell displacement apart from distance on a graph that crosses the time axis.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        [
            "Obtain $v=dx/dt$ and $a=dv/dt$ from position functions",
            "Integrate $v$ and $a$ to recover motion, including initial conditions",
            "Handle variable $a(t)$ and $a(x)$ with the matching differential",
            "Differentiate and integrate 2D vector components",
            "Subtract velocities to get relative motion, including river boats",
            "Use slope and area on $x(t)$, $v(t)$, and $a(t)$ graphs",
        ],
        c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Newton's Laws
# ===========================================================================

def _u2_questions():
    qs = []
    _add(qs, [
        ("An inertial frame is one in which a free particle (net force zero) has",
         "constant velocity", "Newton's first law: $a=0$ when $F_\\mathrm{net}=0$, so $v$ is constant (including zero).",
         ["constant position only", "constant acceleration g", "zero mass"]),
        ("A cart at rest on Earth is approximately inertial for classroom times because",
         "Earth's acceleration is tiny here", "We treat the ground as inertial unless the problem involves rotating frames or accelerating elevators as the observer.",
         ["Earth does not move", "gravity is not a force", "mass is infinite"]),
        ("In a bus that speeds up, a hanging pendulum tilts backward. In the bus frame that tilt is blamed on",
         "a fictitious force", "The bus is not inertial. In the ground frame the pendulum's mass lags because $a$ needs a horizontal force.",
         ["a loss of gravity", "negative mass", "air becoming a force from behind"]),
        ("If $F_\\mathrm{net}=0$ in an inertial frame, which quantity is definitely constant?",
         "velocity", "First law: $a=0$ so $\\vec v$ does not change. Position can still change at a steady rate.",
         ["position", "only speed in circular motion", "mass"]),
        ("Two frames move at $5\\,\\mathrm{m/s}$ relative to each other with zero relative acceleration. Both are",
         "inertial if one is", "Constant relative velocity preserves the inertial property.",
         ["non-inertial", "rotating", "unable to use F=ma"]),
        ("Newton's second law in Physics C is $F_\\mathrm{net}=dp/dt$, where $p$ is",
         "momentum mv", "Linear momentum is $\\vec p=m\\vec v$. For constant $m$, $dp/dt=ma$.",
         ["power", "pressure", "potential energy"]),
        ("A $2\\,\\mathrm{kg}$ object has $v=4t$. The net force is",
         "8 N", "$p=8t$, $dp/dt=8\\,\\mathrm{N}$. Also $a=4$, so $F=ma=8\\,\\mathrm{N}$.",
         ["4 N", "2 N", "8t N"]),
        ("If $p=6t^2$ (SI), $F_\\mathrm{net}$ at $t=2\\,\\mathrm{s}$ is",
         "24 N", "$F=dp/dt=12t$. At $t=2$, $F=24\\,\\mathrm{N}$.",
         ["6 N", "12 N", "48 N"]),
        ("Constant $m=3\\,\\mathrm{kg}$ and $F_\\mathrm{net}=12\\,\\mathrm{N}$. Acceleration is",
         "4 m/s^2", "$a=F/m=4\\,\\mathrm{m/s}^2$.",
         ["36 m/s^2", "12 m/s^2", "3 m/s^2"]),
        ("A particle's momentum changes from $4\\,\\mathrm{kg\\,m/s}$ to $10\\,\\mathrm{kg\\,m/s}$ in $2\\,\\mathrm{s}$ at a steady rate. Average $F_\\mathrm{net}$ is",
         "3 N", "$\\Delta p=6$, $F_\\mathrm{avg}=\\Delta p/\\Delta t=3\\,\\mathrm{N}$.",
         ["6 N", "2 N", "14 N"]),
        ("Kinetic friction on a sliding block is often modeled as",
         "μ_k N", "$f_k=\\mu_k N$, opposite velocity, with $N$ the normal force.",
         ["μ_k mg even on a wall", "μ_s N while sliding", "zero whenever speed is constant"]),
        ("Static friction can take any value up to",
         "μ_s N", "$f_s\\le\\mu_s N$. Equality is impending slip.",
         ["μ_k N only", "mg", "zero"]),
        ("A $5\\,\\mathrm{kg}$ block, $N=50\\,\\mathrm{N}$, $\\mu_k=0.20$. Kinetic friction magnitude is",
         "10 N", "$f_k=0.20\\times 50=10\\,\\mathrm{N}$.",
         ["50 N", "2 N", "5 N"]),
        ("On a level floor, $N$ usually equals",
         "mg if no other vertical forces", "Vertical equilibrium: $N=mg$ when $a_y=0$ and no extra vertical push.",
         ["always μ mg", "zero", "mv"]),
        ("A block on a $30^\\circ$ frictionless incline has $a$ down the ramp equal to",
         "g/2", "$a=g\\sin 30^\\circ=g/2$.",
         ["g", "g\\sqrt{3}/2", "0"]),
        ("Linear drag is modeled as $F_d=-bv$. Terminal speed for a falling object of mass $m$ is",
         "mg/b", "At terminal, $mg=bv_t$, so $v_t=mg/b$.",
         ["b/mg", "mgb", "g/b"]),
        ("If $v_t=20\\,\\mathrm{m/s}$, $m=2\\,\\mathrm{kg}$, $g=10$, then $b$ is",
         "1 kg/s", "$b=mg/v_t=20/20=1\\,\\mathrm{kg/s}$.",
         ["2 kg/s", "10 kg/s", "0.5 kg/s"]),
        ("The SI unit of the linear-drag coefficient $b$ in $F=-bv$ is",
         "kg/s", "$[b]=[F]/[v]=\\mathrm{N/(m/s)}=\\mathrm{kg/s}$.",
         ["kg m/s", "N", "s/kg"]),
        ("For $m\\,dv/dt=mg-bv$ with $v(0)=0$, $v(t)$ approaches $v_t$ as",
         "1-e^{-(b/m)t}", "$v=v_t(1-e^{-(b/m)t})$.",
         ["e^{-(b/m)t}", "bt/m", "constant g t"]),
        ("At $t=0$ in linear drag fall from rest, the initial acceleration is",
         "g", "Initially $v=0$ so drag is $0$, hence $a=g$.",
         ["0", "g/2", "v_t"]),
        ("Two masses on a light string over a light frictionless pulley have constraint",
         "a1 = -a2", "String length fixed: $x_1+x_2=$ constant, so accelerations are opposite.",
         ["a1=a2 in the same direction", "v1=0", "T=0"]),
        ("A bead on a straight frictionless wire can only accelerate",
         "along the wire", "The constraint force (normal from the wire) kills perpendicular acceleration.",
         ["only vertically", "in a circle always", "not at all"]),
        ("For an Atwood machine with $m_1=5\\,\\mathrm{kg}$, $m_2=3\\,\\mathrm{kg}$, $g=10$, light pulley, $a$ is",
         "2.5 m/s^2", "$a=(m_1-m_2)g/(m_1+m_2)=20/8=2.5\\,\\mathrm{m/s}^2$.",
         ["10 m/s^2", "4 m/s^2", "2 m/s^2"]),
        ("Tension in that Atwood ($m_1=5$, $m_2=3$, $g=10$) is",
         "37.5 N", "$T=2m_1 m_2 g/(m_1+m_2)=300/8=37.5\\,\\mathrm{N}$.",
         ["50 N", "30 N", "80 N"]),
        ("A block sliding in a circular bowl has a normal force that",
         "does no work if the bowl is rigid", "The displacement is tangent; $N$ is perpendicular, so $N\\cdot dr=0$.",
         ["equals mg always", "is zero at the bottom", "points along velocity"]),
        ("A conveyor hopper drops sand onto a belt. If horizontal speed must rise, the belt must supply",
         "a forward force", "Incoming sand had less $p_x$; $F=dp/dt$ requires a force to raise the horizontal momentum.",
         ["no force because sand is slow", "only gravity", "a backward force to conserve mass"]),
        ("Rocket thrust (no external force) has magnitude $v_\\mathrm{ex}\\,dm/dt$ where $v_\\mathrm{ex}$ is",
         "exhaust speed relative to the rocket", "Thrust $=v_\\mathrm{rel}\\,(dm/dt)$ with $dm/dt$ the ejecta mass rate.",
         ["ground speed of the rocket", "speed of sound", "escape speed"]),
        ("If a rocket burns $2\\,\\mathrm{kg/s}$ of fuel at $v_\\mathrm{ex}=400\\,\\mathrm{m/s}$, thrust is",
         "800 N", "$F=400\\times 2=800\\,\\mathrm{N}$.",
         ["200 N", "400 N", "80 N"]),
        ("In $F_\\mathrm{ext}+v_\\mathrm{rel}(dm/dt)=m\\,dv/dt$, $m$ is",
         "the rocket's instantaneous mass", "Mass is a function of time as fuel leaves.",
         ["the exhaust mass only", "Earth's mass", "a constant 1 kg"]),
        ("A leaky hopper car rolling without friction slows if sand leaks",
         "false if sand drops with the car's horizontal v", "If sand leaves with the car's $v_x$, $p_x$ of what remains is unchanged and $v$ stays the same.",
         ["always true", "true only on inclines", "true because mass drops so v must drop"]),
        ("A $4\\,\\mathrm{kg}$ block pulled right by $20\\,\\mathrm{N}$ on a frictionless floor has $a=$",
         "5 m/s^2", "$a=20/4=5$.",
         ["20 m/s^2", "4 m/s^2", "80 m/s^2"]),
        ("If $p=3t^3$ (SI), $F$ at $t=1\\,\\mathrm{s}$ is",
         "9 N", "$F=9t^2$. At $t=1$, $F=9\\,\\mathrm{N}$.",
         ["3 N", "1 N", "27 N"]),
        ("Static friction on a $10\\,\\mathrm{N}$ object with $\\mu_s=0.40$ and $N=10\\,\\mathrm{N}$ cannot exceed",
         "4 N", "$\\mu_s N=4\\,\\mathrm{N}$.",
         ["10 N", "0.4 N", "40 N"]),
        ("A $2\\,\\mathrm{kg}$ brick, $g=10$, on a $30^\\circ$ rough incline with $\\mu_k=0.10$. $N$ is",
         "10\\sqrt{3} N", "$N=mg\\cos 30^\\circ=20(\\sqrt{3}/2)=10\\sqrt{3}\\,\\mathrm{N}$.",
         ["20 N", "10 N", "20\\sqrt{3} N"]),
        ("Terminal velocity doubles if $b$ is halved and $m$ is fixed because",
         "v_t=mg/b", "Halving $b$ doubles $mg/b$.",
         ["v_t=b/mg", "drag becomes zero", "g doubles"]),
        ("Constraint: a string of length $L$ with one end fixed and a mass at the other (vertical circle) has speed related to radius by",
         "the radius staying L", "The string forces the path to be a circle of radius $L$.",
         ["radius growing with v", "radius = v t", "no centripetal need"]),
        ("Light pulley Atwood: doubling both masses (same ratio) does what to $a$?",
         "a unchanged", "$a=\\dfrac{m_1-m_2}{m_1+m_2}g$ depends only on the ratio.",
         ["a doubles", "a halves", "a becomes g"]),
        ("A person in an elevator with $a=2\\,\\mathrm{m/s}^2$ up, $g=10$, $m=50\\,\\mathrm{kg}$. Scale reading is",
         "600 N", "$N-mg=ma$ so $N=m(g+a)=50\\times 12=600\\,\\mathrm{N}$.",
         ["500 N", "400 N", "100 N"]),
        ("Same elevator accelerating down at $2\\,\\mathrm{m/s}^2$. Scale reading is",
         "400 N", "$N=m(g-a)=50\\times 8=400\\,\\mathrm{N}$.",
         ["600 N", "500 N", "100 N"]),
        ("$F=6t$ (newtons) on $m=3\\,\\mathrm{kg}$ from rest. $v$ at $t=2\\,\\mathrm{s}$ from $a=F/m=2t$ is",
         "4 m/s", "$v=t^2$. At $t=2$, $v=4\\,\\mathrm{m/s}$.",
         ["12 m/s", "6 m/s", "2 m/s"]),
        ("Friction does negative work on a sliding box because",
         "f opposes displacement", "$\\vec f\\cdot d\\vec r<0$ when force and displacement are opposite.",
         ["friction is not a force", "N is negative", "mass decreases"]),
        ("A free-body diagram should include",
         "only forces on that one object", "Do not draw forces the object exerts on others (that's Newton's third law pair on the other body).",
         ["every force in the universe", "velocity arrows as forces", "mass as a force"]),
        ("If $F_\\mathrm{net}=0$ but the object moves, it must move with",
         "constant velocity", "First law. Uniform motion is allowed.",
         ["increasing speed", "zero velocity only", "centripetal acceleration"]),
        ("Linear drag: time constant $m/b$ has units of",
         "seconds", "$(kg)/(kg/s)=s$.",
         ["newtons", "meters", "kg"]),
        ("A block pressed against a vertical wall with horizontal $F$, $\\mu_s$ large enough to hold. Then $f_s$ equals",
         "mg", "Vertical equilibrium: static friction balances weight.",
         ["F", "μ_s F always even if smaller would do", "0"]),
        ("Newton's third law pair to Earth's gravity on a book is",
         "the book's gravity on Earth", "Action-reaction: same type, on the other object.",
         ["the table's normal on the book", "friction", "the book's weight as a second force on the book"]),
        ("AP Stretch: $m=2\\,\\mathrm{kg}$, $F=8x^3$ along $x$. Using $a=v\\,dv/dx=F/m$, if $v=0$ at $x=1$, then $v^2$ at $x=2$ is",
         "30", "$a=4x^3$, so $v\\,dv=4x^3\\,dx$. $\\tfrac12 v^2=x^4\\big|_1^2=16-1=15$, hence $v^2=30$.",
         ["15", "16", "8"]),
        ("AP Stretch: $dv/dt=g-bv/m$ with $v_t=mg/b$. The time to reach $v=v_t/2$ from rest is",
         "(m/b) ln 2", "$v=v_t(1-e^{-(b/m)t})=v_t/2$ gives $e^{-(b/m)t}=1/2$, so $t=(m/b)\\ln 2$.",
         ["(b/m) ln 2", "m/b", "2m/b"]),
        ("AP Stretch: Sand falls vertically onto a freight car of mass $M$ moving at constant $v$ (external engine). To keep $v$ constant while mass grows at $\\lambda\\,\\mathrm{kg/s}$, the engine force is",
         "λ v", "Horizontal $dp/dt=v\\,dm/dt=\\lambda v$ because $v$ is held fixed.",
         ["0", "λ g", "Mv"]),
        ("AP Stretch: Hanging $6\\,\\mathrm{kg}$ connected over a light pulley to $4\\,\\mathrm{kg}$ on a frictionless table, $g=10$. Find $a$, then the string tension $T$.",
         "24 N", "$a=60/10=6\\,\\mathrm{m/s}^2$. Table: $T=m_2 a=24\\,\\mathrm{N}$.",
         ["60 N", "36 N", "10 N"]),
        ("AP Stretch: $F=12-3t$ (newtons) on $m=3\\,\\mathrm{kg}$ from rest. Integrate $a=F/m$ to find $v$ at $t=2\\,\\mathrm{s}$.",
         "6 m/s", "$a=4-t$. $v=4t-t^2/2$. At $t=2$, $v=8-2=6\\,\\mathrm{m/s}$.",
         ["8 m/s", "4 m/s", "12 m/s"]),
        ("AP Stretch: Linear drag $m=4\\,\\mathrm{kg}$, $b=2\\,\\mathrm{kg/s}$, $v(0)=6\\,\\mathrm{m/s}$, no other horizontal force. $v$ at $t=2\\ln 2$ seconds is",
         "3 m/s", "$v=6e^{-(b/m)t}=6e^{-t/2}$. At $t=2\\ln 2$, exponent is $-\\ln 2$, so $v=3\\,\\mathrm{m/s}$.",
         ["6 m/s", "1.5 m/s", "0"]),
        ("AP Stretch: A rocket of instantaneous mass $200\\,\\mathrm{kg}$ ejects $5\\,\\mathrm{kg/s}$ at $v_\\mathrm{ex}=800\\,\\mathrm{m/s}$. Magnitude of $a$ (no gravity) is",
         "20 m/s^2", "Thrust $=4000\\,\\mathrm{N}$, $a=4000/200=20\\,\\mathrm{m/s}^2$.",
         ["4 m/s^2", "800 m/s^2", "5 m/s^2"]),
        ("AP Stretch: $F=-8x$ on $m=2\\,\\mathrm{kg}$ with $v=4$ at $x=0$. Using $v\\,dv=(F/m)\\,dx$, $v^2$ at $x=1$ is",
         "12", "$v\\,dv=-4x\\,dx$. $\\int_4^v u\\,du=\\int_0^1 -4x\\,dx=-2$, so $\\tfrac12 v^2-8=-2$, hence $\\tfrac12 v^2=6$ and $v^2=12$.",
         ["8", "16", "4"]),
        ("AP Stretch: A $4\\,\\mathrm{kg}$ block sits on an $8\\,\\mathrm{kg}$ block. The lower block is pulled by $F=6t$ (newtons) on a frictionless floor; they move together from rest. Their common $v$ at $t=4\\,\\mathrm{s}$ is",
         "4 m/s", "Impulse $J=\\int_0^4 6t\\,dt=3t^2\\big|_0^4=48\\,\\mathrm{N\\cdot s}$. Total mass $12\\,\\mathrm{kg}$, so $v=J/M=4\\,\\mathrm{m/s}$.",
         ["24 m/s", "8 m/s", "2 m/s"]),
    ])
    return qs


def build_unit2():
    title = "AP Physics C Mechanics Unit 2: Newton's Laws"
    description = (
        "Inertial frames, F_net = dp/dt, friction, linear drag, constraints, and variable-mass introductions."
    )
    c1 = concept_block(
        "1. Inertial frames",
        [
            "An inertial frame is a viewpoint in which a particle with zero net force moves at constant velocity "
            "(Newton's first law). The ground in a classroom is treated as inertial. A car that is speeding up "
            "is not: a hanging mass “leans back” even though, in the ground frame, the string simply has not yet "
            "given the mass the same horizontal $a$ as the car.",
            "If frame B moves at constant velocity relative to inertial frame A, then B is also inertial. "
            "Relative acceleration between frames is what destroys the first law. Two trains passing at steady "
            "$30\\,\\mathrm{m/s}$ can both use $\\vec F=m\\vec a$ with the same $a$ for a given object.",
            "In a non-inertial frame people invent a fictitious force $-m\\vec a_\\mathrm{frame}$ to keep using "
            "$\\sum F=ma$ as a bookkeeping device. Physics C wants you to recognize that this force is not from "
            "a physical agent (no third-law partner on another object). Prefer analyzing in an inertial frame.",
            "Elevators are a daily example. If the elevator accelerates up at $2\\,\\mathrm{m/s}^2$ and $g=10$, "
            "a $50\\,\\mathrm{kg}$ person has scale reading $N=m(g+a)=600\\,\\mathrm{N}$. The scale is not “creating "
            "extra gravity”; it must supply a larger normal force so that $N-mg=ma$.",
            "Rotating frames (Earth, a merry-go-round) are non-inertial. Coriolis effects exist but are not an "
            "AP Physics C Mechanics emphasis. You do need to know that uniform circular motion in an inertial "
            "frame still has a real centripetal force $mv^2/r$ pointing toward the center — no centrifugal agent.",
            "Exam move: if a problem says “a crate in the back of a truck that speeds up,” draw the FBD in the "
            "ground frame (static friction forward on the crate) rather than a mysterious backward force.",
        ],
        "Every later $F=ma$ or $F=dp/dt$ statement is true in inertial frames. Naming the frame is part of "
        "justifying a law on an FRQ.",
        "Ask: is my observer accelerating? If yes, either switch to the ground or include a fictitious force "
        "and say so. If two frames have constant relative velocity, $a$ of an object is the same in both.",
        lesson_figure(
            fbd_box(labels=("mg", "N", "f_s")),
            "Crate in a truck that speeds up, drawn in the ground (inertial) frame",
            "Static friction points forward — that is the real force giving the crate its acceleration. There is "
            "no backward “force of inertia” in this frame.",
        )
        + solved(
            1, "A $50\\,\\mathrm{kg}$ person stands in an elevator accelerating upward at $2\\,\\mathrm{m/s}^2$. Take $g=10\\,\\mathrm{m/s}^2$. What does the scale read?",
            [
                "Inertial (ground) analysis: $N-mg=ma$.",
                "$N=m(g+a)=50(12)=600\\,\\mathrm{N}$.",
                "The scale reading is the normal force $N$.",
            ],
            "$600\\,\\mathrm{N}$",
            "",
            "Easy",
        )
        + solved(
            2, "The same person, elevator accelerating downward at $2\\,\\mathrm{m/s}^2$. Scale reading?",
            [
                "$mg-N=ma$ when down is the positive $a$ direction, or $N-mg=m(-2)$.",
                "$N=m(g-a)=50\\times 8=400\\,\\mathrm{N}$.",
                "Apparent weight dropped; the frame of the elevator is not inertial.",
            ],
            "$400\\,\\mathrm{N}$",
            "",
            "Medium",
        )
        + solved(
            3,
            "A pendulum hangs in a bus. While the bus has constant velocity the string is vertical. The bus then speeds up. Explain the lean using an inertial frame, not a fictitious force.",
            [
                "Before, $v$ is constant, so $a=0$ and the string's tension balances $mg$ vertically.",
                "When the bus gains speed, the support (ceiling) accelerates forward.",
                "The bob's inertia means it does not instantly match that $a$; the string tilts so that a horizontal component of tension can provide $ma$ forward.",
                "In the ground frame there is no extra backward force — only $T$ and $mg$.",
            ],
            "String tilts so $T_x=ma$ forward; no fictitious force needed in the ground frame.",
            "",
            "Hard",
        )
        + _ican([
            "I can define an inertial frame using Newton's first law.",
            "I can compute apparent weight in an accelerating elevator.",
            "I can analyze a crate in an accelerating truck using real forces in the ground frame.",
        ]),
        ("Drawing a backward “force of inertia” in the ground frame",
         "Inertia is not a force. In the ground frame, friction or tension points the way the acceleration points. "
         "Save fictitious forces for an explicit non-inertial analysis, and label them as such."),
        ("State the frame in one sentence",
         "FRQ stem: “Using Newton's second law in an inertial frame…” Then your FBD only has physical forces."),
        [
            "I can define an inertial frame using Newton's first law.",
            "I can compute apparent weight in an accelerating elevator.",
            "I can analyze a crate in an accelerating truck using real forces in the ground frame.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Net force as the derivative of momentum",
        [
            "Linear momentum is $\\vec p=m\\vec v$ — mass times velocity, a vector. Newton's second law in its "
            "general Mechanics form is $\\vec F_\\mathrm{net}=d\\vec p/dt$. If mass is constant, this collapses "
            "to $\\vec F=m\\vec a$, because $d(mv)/dt=m\\,dv/dt$.",
            "Example: $m=2\\,\\mathrm{kg}$ and $v=4t$ give $p=8t$, so $F=dp/dt=8\\,\\mathrm{N}$. You could also "
            "say $a=4\\,\\mathrm{m/s}^2$ and $F=ma=8\\,\\mathrm{N}$. Same number, two languages.",
            "If $p=6t^2$ (SI units), then $F=12t$. At $t=2\\,\\mathrm{s}$, $F=24\\,\\mathrm{N}$. Momentum can be "
            "a curved function of time; force is its slope.",
            "Average force over a short interval is $\\Delta p/\\Delta t$. If $p$ goes from $4$ to $10\\,\\mathrm{kg\\,m/s}$ "
            "in $2\\,\\mathrm{s}$, $F_\\mathrm{avg}=3\\,\\mathrm{N}$. That is already the impulse idea of Unit 4.",
            "When mass changes (sand, rockets), $d(mv)/dt=m\\,dv/dt+v\\,dm/dt$. You must be careful which $v$ "
            "is whose — that is the last concept in this unit. For constant $m$, never invent an extra $v\\,dm/dt$ term.",
            "AP translation: if a graph of $p(t)$ is given, $F_\\mathrm{net}$ is the slope. If $F(t)$ is given, "
            "$\\Delta p=\\int F\\,dt$. Those are calculus twins of $a=dv/dt$ and $\\Delta v=\\int a\\,dt$.",
        ],
        "Impulse, collisions, and variable mass all start from $F=dp/dt$. Treating $F=ma$ as the only form "
        "fails as soon as $m$ is not constant.",
        "Write $\\vec p=m\\vec v$, then $\\vec F=d\\vec p/dt$. If $m$ is constant, replace with $m\\vec a$. "
        "If $p(t)$ is given, differentiate. If $F(t)$ is given, integrate to get $\\Delta p$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: 6 * t * t, 0, 3))],
                points=[(2, 24, "p(2)=24")],
                xlim=(0, 3.2), ylim=(-2, 60), xlab="t (s)", ylab="p (kg m/s)",
            ),
            "$p=6t^2$, so $F=dp/dt=12t$",
            "At $t=2\\,\\mathrm{s}$ the slope of this parabola is $24\\,\\mathrm{N}$, matching $F=12t$.",
        )
        + solved(
            6, "A $2\\,\\mathrm{kg}$ object has $v=4t$. Find $F_\\mathrm{net}$.",
            [
                "$p=mv=8t$.",
                "$F=dp/dt=8\\,\\mathrm{N}$ (constant).",
                "Check: $a=4$, $ma=8\\,\\mathrm{N}$.",
            ],
            "$8\\,\\mathrm{N}$",
            "",
            "Easy",
        )
        + solved(
            7, "$p=6t^2$ in SI units. Find $F$ at $t=2\\,\\mathrm{s}$.",
            [
                "$F=dp/dt=12t$.",
                "At $t=2$, $F=24\\,\\mathrm{N}$.",
                "Direction of $F$ is the direction of increasing $p$.",
            ],
            "$24\\,\\mathrm{N}$",
            "",
            "Medium",
        )
        + solved(
            8, "$F=6t$ newtons acts on $m=3\\,\\mathrm{kg}$ from rest. Find $v$ at $t=2\\,\\mathrm{s}$.",
            [
                "$a=F/m=2t$.",
                "$v=\\int_0^2 2t\\,dt=t^2\\big|_0^2=4\\,\\mathrm{m/s}$.",
                "Equivalently $\\Delta p=\\int F\\,dt=\\int_0^2 6t\\,dt=12$, so $v=\\Delta p/m=4\\,\\mathrm{m/s}$.",
            ],
            "$4\\,\\mathrm{m/s}$",
            "",
            "Hard",
        )
        + _ican([
            "I can state $F_\\mathrm{net}=dp/dt$ and reduce it to $F=ma$ when $m$ is constant.",
            "I can differentiate a given $p(t)$ to find force.",
            "I can integrate $F(t)$ to find $\\Delta p$ and then $v$.",
        ]),
        ("Writing $F=mv$ or $F=p$",
         "Force is the derivative of momentum, not momentum itself. Units: $\\mathrm{N}=\\mathrm{kg\\,m/s}^2$, "
         "while $p$ is $\\mathrm{kg\\,m/s}$."),
        ("If $p(t)$ is graphed, use slope not height",
         "A large momentum with zero slope means $F_\\mathrm{net}=0$ right then — uniform motion."),
        [
            "I can state $F_\\mathrm{net}=dp/dt$ and reduce it to $F=ma$ when $m$ is constant.",
            "I can differentiate a given $p(t)$ to find force.",
            "I can integrate $F(t)$ to find $\\Delta p$ and then $v$.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Friction models",
        [
            "Kinetic friction (object sliding) is modeled as $f_k=\\mu_k N$, opposite the velocity, where $N$ is "
            "the normal force, not always $mg$. On level ground with no extra vertical forces, $N=mg$. "
            "A $5\\,\\mathrm{kg}$ block with $N=50\\,\\mathrm{N}$ and $\\mu_k=0.20$ has $f_k=10\\,\\mathrm{N}$.",
            "Static friction (object not sliding) is not a single value. It adjusts up to a maximum "
            "$f_s\\le\\mu_s N$. Equality is impending slip. If a $10\\,\\mathrm{N}$ object has $\\mu_s=0.40$ and "
            "$N=10\\,\\mathrm{N}$, static friction cannot exceed $4\\,\\mathrm{N}$. A $3\\,\\mathrm{N}$ horizontal "
            "push is balanced by $f_s=3\\,\\mathrm{N}$, not by $4\\,\\mathrm{N}$.",
            "On an incline, resolve $mg$ into $mg\\sin\\theta$ down the ramp and $mg\\cos\\theta$ into the ramp. "
            "Then $N=mg\\cos\\theta$ (if no other perpendicular forces). Friction is $\\mu N=\\mu mg\\cos\\theta$, "
            "parallel to the surface. Frictionless $30^\\circ$ gives $a=g\\sin 30^\\circ=g/2$.",
            "A $2\\,\\mathrm{kg}$ brick, $g=10$, on a $30^\\circ$ ramp has $N=20\\cos 30^\\circ=10\\sqrt{3}\\,\\mathrm{N}$. "
            "If $\\mu_k=0.10$, $f_k=\\sqrt{3}\\,\\mathrm{N}$. Net force down the ramp is $mg\\sin\\theta-f_k$.",
            "Friction is a contact force from the surface, parallel to the surface. It is not $\\mu mg$ as a reflex "
            "on a vertical wall: there $N$ is the horizontal push, and static friction can equal $mg$ to hold the block.",
            "Rolling with friction without slipping is subtle: static friction can accelerate or decelerate rotation "
            "(Unit 5). Sliding means kinetic friction and energy loss to thermal energy.",
        ],
        "Inclines, stacked blocks, and rolling all need a friction model. Using $\\mu mg$ blindly when $N\\ne mg$ "
        "is one of the highest-frequency Mechanics errors.",
        "Find $N$ from the perpendicular equation first. Then write $f_k=\\mu_k N$ or $f_s\\le\\mu_s N$. Point "
        "kinetic friction against velocity; point static friction against the attempted slip.",
        lesson_figure(
            incline_svg(angle="30°"),
            "Block on an incline: weight $F_g$, surface normal, and (if rough) friction up the ramp when sliding down",
            "Always resolve $mg$ into components parallel and perpendicular to the surface before writing $N$ and $f$.",
        )
        + solved(
            11, "A $5\\,\\mathrm{kg}$ block has $N=50\\,\\mathrm{N}$ and $\\mu_k=0.20$. Find $f_k$.",
            [
                "$f_k=\\mu_k N=0.20\\times 50$.",
                "$f_k=10\\,\\mathrm{N}$.",
                "Direction: opposite the sliding velocity.",
            ],
            "$10\\,\\mathrm{N}$",
            "",
            "Easy",
        )
        + solved(
            12, "Frictionless incline at $30^\\circ$. Find $a$ down the ramp in terms of $g$.",
            [
                "Net force down the ramp is $mg\\sin 30^\\circ$.",
                "$\\sin 30^\\circ=1/2$, so $F_\\mathrm{net}=mg/2$.",
                "$a=g/2$.",
            ],
            "$g/2$",
            "",
            "Medium",
        )
        + solved(
            13,
            "A $2\\,\\mathrm{kg}$ brick on a $30^\\circ$ incline, $g=10$, $\\mu_k=0.10$, sliding down. Find $N$ and $a$.",
            [
                "$N=mg\\cos 30^\\circ=20\\times\\sqrt{3}/2=10\\sqrt{3}\\,\\mathrm{N}$.",
                "$f_k=0.10\\times 10\\sqrt{3}=\\sqrt{3}\\,\\mathrm{N}$.",
                "$mg\\sin 30^\\circ=10\\,\\mathrm{N}$. Then $a=(10-\\sqrt{3})/2\\,\\mathrm{m/s}^2$.",
            ],
            "$N=10\\sqrt{3}\\,\\mathrm{N}$, $a=(10-\\sqrt{3})/2\\,\\mathrm{m/s}^2$",
            "",
            "Hard",
        )
        + _ican([
            "I can write $f_k=\\mu_k N$ and $f_s\\le\\mu_s N$ with the correct $N$.",
            "I can resolve weight on an incline and find $a$.",
            "I can use $N$ as a horizontal push on a vertical wall problem.",
        ]),
        ("Setting $N=mg$ on an incline",
         "Perpendicular to the ramp, $N=mg\\cos\\theta$, which is less than $mg$. Using $mg$ for $N$ overstates friction."),
        ("Compute $N$ before $\\mu N$",
         "One perpendicular FBD equation, solve $N$, then write friction. Never start with $f=\\mu mg$ as a reflex."),
        [
            "I can write $f_k=\\mu_k N$ and $f_s\\le\\mu_s N$ with the correct $N$.",
            "I can resolve weight on an incline and find $a$.",
            "I can use $N$ as a horizontal push on a vertical wall problem.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Drag proportional to velocity",
        [
            "A common Physics C model of air or fluid resistance is linear drag $\\vec F_d=-b\\vec v$, opposite "
            "velocity, with $b>0$ a coefficient whose SI unit is $\\mathrm{kg/s}$. For a falling object, "
            "$m\\,dv/dt=mg-bv$ if down is positive.",
            "Terminal speed is the steady $v$ where net force is zero: $mg=bv_t$, so $v_t=mg/b$. If $m=2\\,\\mathrm{kg}$, "
            "$g=10$, and $v_t=20\\,\\mathrm{m/s}$, then $b=1\\,\\mathrm{kg/s}$. At the first instant of drop, $v=0$ "
            "so drag is $0$ and $a=g$. As $v$ grows, $a$ shrinks toward $0$.",
            "The differential equation $dv/dt=g-(b/m)v$ is first-order linear. With $v(0)=0$ the solution is "
            "$v(t)=v_t\\bigl(1-e^{-(b/m)t}\\bigr)$. The combination $m/b$ is a time in seconds. When $t=(m/b)\\ln 2$, "
            "$v$ has reached $v_t/2$.",
            "You do not need to memorize every solution if you can separate variables: $dv/(g-bv/m)=dt$ and integrate. "
            "The exponential approach to $v_t$ is the qualitative graph AP wants you to recognize.",
            "Quadratic drag $F=-cv^2$ is also used for high-speed motion; terminal then satisfies $mg=cv_t^2$. "
            "This unit's stretch items stay with linear $b v$ unless a problem states otherwise.",
            "Horizontal sliding with $F_d=-bv$ and no other horizontal force gives $m\\,dv/dt=-bv$, so "
            "$v=v_0 e^{-(b/m)t}$. Speed decays exponentially. Displacement $x=(mv_0/b)(1-e^{-(b/m)t})$ approaches "
            "a finite limit $mv_0/b$.",
        ],
        "Real objects do not fall with constant $g$ forever. Linear drag is the first solvable model that "
        "produces a terminal speed and an exponential $v(t)$.",
        "Write $m\\,dv/dt=mg-bv$ (or $-bv$ only). Identify $v_t=mg/b$. Either quote $v=v_t(1-e^{-t/\\tau})$ with "
        "$\\tau=m/b$, or separate variables and integrate between the two times in the problem.",
        lesson_figure(
            xy_graph(
                curves=[("#059669", sample_curve(lambda t: 20 * (1 - math.exp(-t / 2)), 0, 10))],
                points=[(0, 0, "v=0"), (1.386, 10, "v=v_t/2")],
                dashes=[("h", 20, "v_t=20")],
                xlim=(0, 10), ylim=(-1, 24), xlab="t (s)", ylab="v (m/s)",
            ),
            "$v=v_t(1-e^{-(b/m)t})$ approaching $20\\,\\mathrm{m/s}$",
            "The curve starts with slope $g$ and flattens toward the dashed terminal speed. It never quite reaches $v_t$ in finite time.",
        )
        + solved(
            16, "$m=2\\,\\mathrm{kg}$, $g=10$, $v_t=20\\,\\mathrm{m/s}$. Find $b$.",
            [
                "$v_t=mg/b$.",
                "$b=mg/v_t=20/20=1\\,\\mathrm{kg/s}$.",
                "Units: $\\mathrm{N/(m/s)}=\\mathrm{kg/s}$.",
            ],
            "$1\\,\\mathrm{kg/s}$",
            "",
            "Easy",
        )
        + solved(
            17, "From rest under linear drag, what is $a$ at $t=0$? What is $a$ as $t\\to\\infty$?",
            [
                "At $t=0$, $v=0$, so $F_d=0$ and $a=g$.",
                "As $t\\to\\infty$, $v\\to v_t$ and $F_\\mathrm{net}\\to 0$, so $a\\to 0$.",
                "In between, $a=g-(b/m)v$, shrinking as $v$ grows.",
            ],
            "$a(0)=g$, $a(\\infty)=0$",
            "",
            "Medium",
        )
        + solved(
            18, "Show that $v=v_t/2$ occurs at $t=(m/b)\\ln 2$ if $v(0)=0$.",
            [
                "$v=v_t(1-e^{-(b/m)t})$.",
                "Set $v=v_t/2$: $1-e^{-(b/m)t}=1/2$, so $e^{-(b/m)t}=1/2$.",
                "Thus $(b/m)t=\\ln 2$, hence $t=(m/b)\\ln 2$.",
            ],
            "$t=(m/b)\\ln 2$",
            "",
            "Hard",
        )
        + _ican([
            "I can write $F_d=-bv$ and find $v_t=mg/b$.",
            "I can explain why $a=g$ at the first instant of a drop from rest.",
            "I can use $v=v_t(1-e^{-(b/m)t})$ to find a time or a speed.",
        ]),
        ("Saying drag is $\\mu N$ for a falling skydiver",
         "Air drag is not dry friction. Linear drag is $-bv$; quadratic is $-cv^2$. There is no normal force from air in that model."),
        ("Check $t=0$ and $t\\to\\infty$ on any proposed $v(t)$",
         "A legal falling-from-rest solution must start at $0$ and approach $v_t$, never pass it."),
        [
            "I can write $F_d=-bv$ and find $v_t=mg/b$.",
            "I can explain why $a=g$ at the first instant of a drop from rest.",
            "I can use $v=v_t(1-e^{-(b/m)t})$ to find a time or a speed.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Constrained motion",
        [
            "A constraint is a geometric rule the motion must obey: a string of fixed length, a bead on a wire, "
            "a block sliding on a table attached to a hanging mass. Constraints produce constraint forces "
            "(tension, normal) that do no work if the allowed displacement is perpendicular to them.",
            "The classic Atwood machine: two masses $m_1$ and $m_2$ on a light inextensible string over a light "
            "frictionless pulley. The constraint is $x_1+x_2=$ constant, so $a_1=-a_2$ in magnitude along the string. "
            "Then $a=(m_1-m_2)g/(m_1+m_2)$. For $m_1=5\\,\\mathrm{kg}$, $m_2=3\\,\\mathrm{kg}$, $g=10$, $a=2.5\\,\\mathrm{m/s}^2$.",
            "Tension is $T=2m_1 m_2 g/(m_1+m_2)$. For those numbers, $T=37.5\\,\\mathrm{N}$, which is between the "
            "two weights $50\\,\\mathrm{N}$ and $30\\,\\mathrm{N}$, as it must be.",
            "Table-and-hanger: hanging $m_1$, table mass $m_2$, frictionless. Only $m_1 g$ is the unbalanced force; "
            "both masses accelerate. $a=m_1 g/(m_1+m_2)$. For $m_1=4$, $m_2=2$, $g=10$, $a=20/3\\,\\mathrm{m/s}^2$.",
            "A bead on a frictionless wire can accelerate only along the wire. The wire's normal force kills the "
            "perpendicular component of net force. You resolve gravity along the tangent.",
            "In Unit 6 the pulley will have mass and moment of inertia. The string constraint stays the same; "
            "the rotational equation $\\tau=I\\alpha$ with $\\alpha=a/R$ joins the two FBDs.",
        ],
        "Connected objects are how AP tests whether you can write more than one FBD and still have one $a$. "
        "The constraint is the missing equation that ties the accelerations together.",
        "Write a length constraint in symbols ($x_1+x_2=L$), differentiate twice to get $a_1=-a_2$, then write "
        "Newton 2 for each mass and add or substitute to eliminate $T$.",
        lesson_figure(
            _pulley_svg(),
            "Atwood constraint: the string length is fixed, so the masses accelerate at equal magnitude",
            "If $m_1$ goes down $2\\,\\mathrm{cm}$, $m_2$ goes up $2\\,\\mathrm{cm}$. Same $|a|$, opposite along the string.",
        )
        + solved(
            21, "Atwood $m_1=5\\,\\mathrm{kg}$, $m_2=3\\,\\mathrm{kg}$, $g=10$, light pulley. Find $a$.",
            [
                "$a=(m_1-m_2)g/(m_1+m_2)$.",
                "$a=20/8=2.5\\,\\mathrm{m/s}^2$.",
                "The $5\\,\\mathrm{kg}$ mass accelerates downward.",
            ],
            "$2.5\\,\\mathrm{m/s}^2$",
            "",
            "Easy",
        )
        + solved(
            22, "For the same Atwood, find tension $T$.",
            [
                "Use $m_2$: $T-m_2 g=m_2 a$ if $m_2$ accelerates up.",
                "$T=3(10+2.5)=37.5\\,\\mathrm{N}$.",
                "Check with $m_1$: $50-T=5\\times 2.5=12.5$ so $T=37.5\\,\\mathrm{N}$.",
            ],
            "$37.5\\,\\mathrm{N}$",
            "",
            "Medium",
        )
        + solved(
            23,
            "Hanging $4\\,\\mathrm{kg}$, table $2\\,\\mathrm{kg}$, frictionless, $g=10$. Find $a$ of the system.",
            [
                "Net force is the hanging weight $40\\,\\mathrm{N}$.",
                "Inertia of the system is $6\\,\\mathrm{kg}$.",
                "$a=40/6=20/3\\,\\mathrm{m/s}^2$.",
            ],
            "$20/3\\,\\mathrm{m/s}^2$",
            "Do not use the two-hanging Atwood formula here; one mass has $N$ canceling $mg$.",
            "Hard",
        )
        + _ican([
            "I can translate a fixed string length into $a_1=-a_2$.",
            "I can solve a light-pulley Atwood for $a$ and $T$.",
            "I can handle a hanger-and-table connected pair.",
        ]),
        ("Giving both masses acceleration $g$",
         "They are not in free fall. Tension is not zero. The lighter mass can even accelerate upward."),
        ("Add the two Newton-2 equations to kill $T$",
         "For Atwood, adding $m_1g-T=m_1 a$ and $T-m_2g=m_2 a$ yields $(m_1-m_2)g=(m_1+m_2)a$ in one line."),
        [
            "I can translate a fixed string length into $a_1=-a_2$.",
            "I can solve a light-pulley Atwood for $a$ and $T$.",
            "I can handle a hanger-and-table connected pair.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Non-constant mass, introduced",
        [
            "If mass changes, $F_\\mathrm{net}=d(mv)/dt$ is not automatically $ma$. Expanding the product gives "
            "$m\\,dv/dt+v\\,dm/dt$, but the $v\\,dm/dt$ term is subtle: you must use the relative velocity of the "
            "mass that is entering or leaving. The careful rocket equation (no external force) is "
            "$m\\,dv/dt=v_\\mathrm{ex}\\,dm/dt$ in magnitude, with $v_\\mathrm{ex}$ the exhaust speed relative to the rocket.",
            "Thrust has magnitude $v_\\mathrm{ex}\\,(dm/dt)$ where $dm/dt$ is the rate at which mass is ejected. "
            "Burning $2\\,\\mathrm{kg/s}$ at $v_\\mathrm{ex}=400\\,\\mathrm{m/s}$ produces $800\\,\\mathrm{N}$ of thrust. "
            "The rocket's remaining mass $m(t)$ is what multiplies $a$.",
            "Sand falling vertically onto a freight car that an engine keeps at constant $v$ requires a horizontal "
            "force $F=\\lambda v$, where $\\lambda=dm/dt$ is the loading rate. Why: each $\\Delta m$ must be brought "
            "from $p_x=0$ up to $v\\,\\Delta m$, so $dp/dt=\\lambda v$.",
            "If sand leaks from a hopper car and drops with the car's horizontal velocity, the remaining car does "
            "not change speed (no horizontal force, and the leaving sand carries away its share of $p_x$). "
            "“Mass dropped so $v$ must rise” is false in that case.",
            "Conveyor belts and chains being picked up are the same $dp/dt$ bookkeeping. Draw a system boundary. "
            "Ask what momentum crosses the boundary per second. That rate is a force.",
            "You are not required to derive the logarithmic rocket equation $v=v_\\mathrm{ex}\\ln(m_0/m)$ in every "
            "item, but you should recognize it as the integral of $m\\,dv=-v_\\mathrm{ex}\\,dm$ when $v_\\mathrm{ex}$ "
            "is constant. Qualitatively: throw mass backward, the remaining mass speeds forward.",
        ],
        "Rockets and loading cars show why Physics C writes $F=dp/dt$ instead of only $F=ma$. Unit 4 returns "
        "to this with impulse integrals.",
        "Identify whether mass is entering or leaving, and with what velocity relative to the object. Then "
        "write $F_\\mathrm{ext}+v_\\mathrm{rel}(dm/dt)=m\\,dv/dt$ with a consistent sign convention.",
        lesson_figure(
            _rocket_svg(),
            "Rocket: exhaust leaves backward at $v_\\mathrm{ex}$ relative to the ship; remaining mass is $m(t)$",
            "Thrust is $v_\\mathrm{ex}$ times the ejecta mass rate. The ship's acceleration is thrust divided by the current $m(t)$.",
        )
        + solved(
            26, "A rocket ejects $2\\,\\mathrm{kg/s}$ at $v_\\mathrm{ex}=400\\,\\mathrm{m/s}$. Find thrust.",
            [
                "Thrust $=v_\\mathrm{ex}\\,dm/dt$.",
                "$400\\times 2=800$.",
                "Units: $(\\mathrm{m/s})(\\mathrm{kg/s})=\\mathrm{N}$.",
            ],
            "$800\\,\\mathrm{N}$",
            "",
            "Easy",
        )
        + solved(
            27, "Sand loads at $\\lambda=5\\,\\mathrm{kg/s}$ onto a car held at $v=4\\,\\mathrm{m/s}$. Engine force to keep $v$ constant (ignore friction)?",
            [
                "Incoming sand has $p_x=0$; it must be sped to $4\\,\\mathrm{m/s}$.",
                "$F=dp/dt=v\\,\\lambda=20\\,\\mathrm{N}$.",
                "If $v$ were allowed to fall, no engine would be needed and the car would slow.",
            ],
            "$20\\,\\mathrm{N}$",
            "",
            "Medium",
        )
        + solved(
            28,
            "A hopper car rolls without friction. Sand leaks out and falls with the car's instantaneous horizontal velocity. Does the car speed up, slow down, or keep $v$?",
            [
                "No external horizontal force, so total $p_x$ of car-plus-remaining-sand-plus-just-leaving-sand is conserved in the horizontal.",
                "The leaving sand has the same $v_x$ as the car, so it carries away $v\\,\\Delta m$.",
                "The remaining mass times the same $v$ is what is left — $v$ does not change.",
            ],
            "Speed stays the same.",
            "Contrast with a rocket, where exhaust has a different velocity from the ship.",
            "Hard",
        )
        + _ican([
            "I can compute rocket thrust as $v_\\mathrm{ex}\\,dm/dt$.",
            "I can find the force needed to keep $v$ constant while loading mass.",
            "I can explain why leaking sand at the car's $v_x$ does not speed the car.",
        ]),
        ("Using $F=ma$ with the original full mass after fuel has left",
         "Acceleration at each instant is (net force including thrust) divided by the mass still on board. "
         "Using yesterday's mass understates $a$."),
        ("Draw a system and list what momentum enters or leaves per second",
         "That rate is a force. Signs: exhaust going backward means a forward thrust on the ship."),
        [
            "I can compute rocket thrust as $v_\\mathrm{ex}\\,dm/dt$.",
            "I can find the force needed to keep $v$ constant while loading mass.",
            "I can explain why leaking sand at the car's $v_x$ does not speed the car.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        [
            "Identify inertial frames and analyze accelerating elevators and trucks",
            "Use $F_\\mathrm{net}=dp/dt$, reducing to $ma$ when mass is constant",
            "Model static and kinetic friction with the correct normal force",
            "Solve linear-drag fall to a terminal speed",
            "Apply string and wire constraints, including Atwood",
            "Treat rockets and loading cars with variable mass qualitatively",
        ],
        c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Work, Energy, and Power
# ===========================================================================

def _u3_questions():
    qs = []
    _add(qs, [
        ("Work along a straight line is $W=\\int F_x\\,dx$. If $F=6x^2$ (newtons, $x$ in meters) from $x=1$ to $x=2$, $W$ is",
         "14 J", "$\\int_1^2 6x^2\\,dx=2x^3\\big|_1^2=16-2=14\\,\\mathrm{J}$.",
         ["12 J", "8 J", "6 J"]),
        ("If $\\vec F$ is perpendicular to $d\\vec r$ at every point, the line integral for work is",
         "0", "$\\vec F\\cdot d\\vec r=0$ when the force is perpendicular to the displacement.",
         ["equal to F times path length", "mgh", "always positive"]),
        ("A constant $12\\,\\mathrm{N}$ force along a $3\\,\\mathrm{m}$ displacement in the same direction does work",
         "36 J", "$W=F\\Delta x=36\\,\\mathrm{J}$, which is also $\\int 12\\,dx$.",
         ["4 J", "15 J", "0"]),
        ("The SI unit of the line integral $\\int \\vec F\\cdot d\\vec r$ is",
         "joule", "A joule is a newton-meter, the unit of work and energy.",
         ["watt", "newton", "kg m/s"]),
        ("If $F=4x$ from $x=0$ to $x=3$, $W$ equals",
         "18 J", "$\\int_0^3 4x\\,dx=2x^2\\big|_0^3=18\\,\\mathrm{J}$.",
         ["12 J", "4 J", "9 J"]),
        ("The work–energy theorem says $W_\\mathrm{net}$ equals",
         "ΔK", "Net work by all forces equals the change in kinetic energy.",
         ["ΔU only", "power", "impulse"]),
        ("A $2\\,\\mathrm{kg}$ object speeds from $3$ to $5\\,\\mathrm{m/s}$. $\\Delta K$ is",
         "16 J", "$K_i=9$, $K_f=25$, $\\Delta K=16\\,\\mathrm{J}$.",
         ["8 J", "4 J", "2 J"]),
        ("Variable $F=6x$ from $x=1$ to $2$ on a particle that starts at rest. Final $K$ is",
         "9 J", "$W=\\int_1^2 6x\\,dx=3x^2\\big|_1^2=12-3=9\\,\\mathrm{J}=K_f$.",
         ["6 J", "12 J", "3 J"]),
        ("If $W_\\mathrm{net}=0$ during an interval, kinetic energy",
         "does not change", "$\\Delta K=0$. Speed can reverse only if $K$ stayed the same and direction flipped by a constraint.",
         ["must be zero", "must increase", "becomes potential"]),
        ("A spring does $W=\\int -kx\\,dx$ from $x=0$ to $A$. That work equals",
         "-½ k A^2", "$\\int_0^A -kx\\,dx=-\\tfrac12 k A^2$. The spring force opposes the stretch.",
         ["½ k A^2", "k A", "0"]),
        ("A conservative force satisfies $F_x=-dU/dx$. If $U=3x^2$, then $F_x$ is",
         "-6x", "Differentiate: $-d(3x^2)/dx=-6x$.",
         ["6x", "3x^2", "0"]),
        ("Near Earth, taking $U=0$ at ground, $U$ at height $h$ is",
         "mgh", "Constant $g$ gives $U=mgy$ if $y=0$ is the reference.",
         ["-mgh", "½ mv^2", "0 always"]),
        ("A spring with $k=200\\,\\mathrm{N/m}$ stretched $0.10\\,\\mathrm{m}$ stores",
         "1 J", "$U=\\tfrac12 k x^2=\\tfrac12(200)(0.01)=1\\,\\mathrm{J}$.",
         ["20 J", "2 J", "0.1 J"]),
        ("If $U=-6/x$ (SI), the force $F_x=-dU/dx$ is",
         "-6/x^2", "$dU/dx=6/x^2$, so $F=-6/x^2$ (attractive toward the origin for $x>0$).",
         ["6/x^2", "-6/x", "6x"]),
        ("Changing the zero of $U$ by a constant $C$",
         "does not change forces", "Forces use $dU/dx$; a constant disappears. Only $\\Delta U$ is physical.",
         ["doubles every force", "cancels kinetic energy", "violates Newton 2"]),
        ("Friction is nonconservative because",
         "work depends on the path", "A longer scrape dumps more thermal energy. $W_\\mathrm{closed}\\ne 0$ in general.",
         ["it has no magnitude", "μ is imaginary", "N is conservative"]),
        ("For a closed loop, work by a conservative force is",
         "0", "You return to the same $U$, so $W_\\mathrm{cons}=-\\Delta U=0$.",
         ["equal to 2π r F", "mgh", "always positive"]),
        ("$W_\\mathrm{nc}=\\Delta E_\\mathrm{mech}$ in the sign convention where $E_\\mathrm{mech}=K+U$ and $W_\\mathrm{nc}$ is work by nonconservative forces. Sliding friction typically makes $W_\\mathrm{nc}$",
         "negative", "Friction opposes $d\\vec r$, so it removes mechanical energy.",
         ["positive always", "zero always", "equal to N"]),
        ("Gravity (constant $g$) is conservative. A round trip up $h$ and back down has gravitational work",
         "0", "$-mgh+mgh=0$.",
         ["2mgh", "-2mgh", "mgh"]),
        ("If only conservative forces do work, $K+U$ is",
         "constant", "Mechanical energy is conserved.",
         ["zero", "equal to impulse", "increasing"]),
        ("Instantaneous power is $P=\\vec F\\cdot\\vec v$. If $F=12\\,\\mathrm{N}$ and $v=3\\,\\mathrm{m/s}$ parallel, $P$ is",
         "36 W", "$P=Fv=36\\,\\mathrm{W}$.",
         ["4 W", "15 W", "0"]),
        ("If $\\vec F$ is perpendicular to $\\vec v$, power is",
         "0", "The force does not change speed; $P=Fv\\cos 90^\\circ=0$.",
         ["Fv", "infinite", "mgh"]),
        ("Power is also $P=dW/dt$. If $W=4t^2$ joules, $P$ at $t=3\\,\\mathrm{s}$ is",
         "24 W", "$P=8t$. At $t=3$, $P=24\\,\\mathrm{W}$.",
         ["4 W", "36 W", "12 W"]),
        ("A $20\\,\\mathrm{N}$ force at $60^\\circ$ to $\\vec v=4\\,\\mathrm{m/s}$ has $P=$",
         "40 W", "$P=Fv\\cos 60^\\circ=80\\times 1/2=40\\,\\mathrm{W}$.",
         ["80 W", "20 W", "0"]),
        ("Average power for $W=100\\,\\mathrm{J}$ in $5\\,\\mathrm{s}$ is",
         "20 W", "$P_\\mathrm{avg}=W/\\Delta t=20\\,\\mathrm{W}$.",
         ["500 W", "5 W", "100 W"]),
        ("On a $U(x)$ diagram, turning points are where",
         "E = U", "KE would be $E-U=0$, so $v=0$ and the particle reverses if a wall of $U$ is there.",
         ["U=0", "E=0", "F=0 always — F=0 is equilibrium, not always a turning point"]),
        ("Where $U(x)$ has a local minimum, a small displacement meets a restoring force. That equilibrium is",
         "stable", "$F=-dU/dx$ points toward the well.",
         ["unstable", "neutral only", "forbidden"]),
        ("A local maximum of $U$ is",
         "unstable equilibrium", "The force pushes away from the peak.",
         ["stable", "a turning point for all E", "where KE is maximum for all E"]),
        ("If $E$ lies above $U$ in a region, the particle can be there with $K=$",
         "E-U", "Always $E=K+U$ when only $U$ and $K$ are mechanical.",
         ["U-E", "U", "0 always"]),
        ("For $U=\\tfrac12 kx^2$ and total $E=\\tfrac12 kA^2$, speed is maximum at",
         "x=0", "All energy is kinetic at the bottom of the well.",
         ["x=A", "x=-A only", "everywhere"]),
        ("$F=8x$ from $x=0$ to $2$. Work is",
         "16 J", "$\\int_0^2 8x\\,dx=4x^2\\big|_0^2=16\\,\\mathrm{J}$.",
         ["8 J", "32 J", "4 J"]),
        ("A $3\\,\\mathrm{kg}$ object, $v_i=4\\,\\mathrm{m/s}$, $v_f=0$. Net work is",
         "-24 J", "$\\Delta K=0-24=-24\\,\\mathrm{J}$.",
         ["24 J", "12 J", "0"]),
        ("$U=2x^3$. Force $F_x$ at $x=1$ is",
         "-6 N", "$F=-6x^2$. At $x=1$, $F=-6\\,\\mathrm{N}$.",
         ["6 N", "2 N", "-2 N"]),
        ("Path independence of work is the test for a",
         "conservative force", "If two paths between the same points give different $W$, the force is not conservative.",
         ["constraint force", "impulse", "fictitious force"]),
        ("A $50\\,\\mathrm{W}$ motor runs for $4\\,\\mathrm{s}$. Energy delivered is",
         "200 J", "$W=P t=200\\,\\mathrm{J}$.",
         ["12.5 J", "50 J", "4 J"]),
        ("Drop of $m=2\\,\\mathrm{kg}$ by $5\\,\\mathrm{m}$, $g=10$, no drag. $\\Delta U$ is",
         "-100 J", "$\\Delta U=mg\\Delta y=20\\times(-5)=-100\\,\\mathrm{J}$.",
         ["100 J", "10 J", "0"]),
        ("That drop, starting from rest, ends with $K=$",
         "100 J", "Energy conservation: $-\\Delta U=\\Delta K$.",
         ["0", "20 J", "50 J"]),
        ("$P=Fv$ with $F=mx$ and $v=dx/dt$. Then $P=$",
         "m x v", "Dot product along a line: $P=F v=m x v$.",
         ["m v", "mx", "0"]),
        ("Work by tension in an inextensible string over a fixed pulley on one mass is not the system work of the string pair because",
         "the other mass has opposite T·dr", "Internal tensions cancel in the two-mass system if the pulley is fixed and the string is ideal.",
         ["tension is not a force", "T is conservative", "strings store U=½kx^2 always"]),
        ("If $F=(2y, 2x)$ in the plane, work from $(0,0)$ to $(1,1)$ along $y=x$ is $\\int_0^1 (2x,2x)\\cdot(dx,dx)=$",
         "2 J", "$(2x+2x)\\,dx=4x\\,dx$, $\\int_0^1 4x\\,dx=2\\,\\mathrm{J}$.",
         ["1 J", "4 J", "0"]),
        ("A hill of $U$ higher than $E$ is",
         "classically forbidden", "KE would be negative, which is not allowed in this course.",
         ["a stable well", "where v is maximum", "where F=0"]),
        ("$k=100\\,\\mathrm{N/m}$, $x=0.20\\,\\mathrm{m}$. Spring $U$ is",
         "2 J", "$\\tfrac12(100)(0.04)=2\\,\\mathrm{J}$.",
         ["20 J", "10 J", "0.2 J"]),
        ("Net work $40\\,\\mathrm{J}$ on $m=5\\,\\mathrm{kg}$ from rest gives $v=$",
         "4 m/s", "$\\tfrac12 m v^2=40$, $v^2=16$, $v=4$.",
         ["8 m/s", "40 m/s", "2 m/s"]),
        ("Power of a $10\\,\\mathrm{N}$ lift at constant $v=2\\,\\mathrm{m/s}$ upward is",
         "20 W", "$P=Fv=20\\,\\mathrm{W}$ (force balances weight at constant $v$).",
         ["5 W", "12 W", "0"]),
        ("$W=\\int_0^3 (6t)\\,dt$ if $F\\cdot v=6t$. That integral is energy of",
         "27 J", "$3t^2\\big|_0^3=27\\,\\mathrm{J}$. Here the integrand is already power.",
         ["18 J", "6 J", "9 J"]),
        ("Force $F=3$ from $x=2$ to $x=5$. Work is",
         "9 J", "$3\\times 3=9\\,\\mathrm{J}$.",
         ["15 J", "6 J", "3 J"]),
        ("AP Stretch: $F=4x^3$ from $x=1$ to $x=3$. Confirm $W=\\int F\\,dx$ and the matching $\\Delta K$ if $K_i=0$. $K_f=$",
         "80 J", "$\\int_1^3 4x^3\\,dx=x^4\\big|_1^3=81-1=80\\,\\mathrm{J}=K_f$.",
         ["64 J", "12 J", "16 J"]),
        ("AP Stretch: $U=2x^3-24x$ (SI). Equilibrium points satisfy $F=0$, i.e. $x=$",
         "±2", "$F=-6x^2+24=0$ so $x^2=4$, $x=\\pm 2$.",
         ["0", "±1", "±4"]),
        ("AP Stretch: At $x=2$ for $U=2x^3-24x$, the equilibrium is",
         "stable", "$U''=12x$. At $x=2$, $U''=24>0$, a local minimum, so the equilibrium is stable.",
         ["unstable", "neutral", "not an equilibrium"]),
        ("AP Stretch: $F=5x^4$ from $x=0$ to $x=2$. The work $\\int F\\,dx$ is",
         "32 J", "$\\int_0^2 5x^4\\,dx=x^5\\big|_0^2=32\\,\\mathrm{J}$.",
         ["16 J", "40 J", "10 J"]),
        ("AP Stretch: $U=x^3/3-4x$ (SI). Find $F=-dU/dx$, then the stable equilibrium, then $U$ there.",
         "-16/3 J", "$F=-x^2+4$. Equilibria at $x=\\pm 2$. $U''=2x$, so $x=2$ is stable. $U(2)=8/3-8=-16/3\\,\\mathrm{J}$.",
         ["8/3 J", "-8 J", "0"]),
        ("AP Stretch: $P=Fv$ with $F=6t$ and $v=2t$ (SI). Energy transferred from $t=0$ to $t=2$ is $\\int P\\,dt=$",
         "32 J", "$P=12t^2$. $\\int_0^2 12t^2\\,dt=4t^3\\big|_0^2=32\\,\\mathrm{J}$.",
         ["12 J", "16 J", "24 J"]),
        ("AP Stretch: $U=4x^2$ and a conservative force. $F_x$ at $x=3$ is",
         "-24 N", "$F=-dU/dx=-8x$. At $x=3$, $F=-24\\,\\mathrm{N}$.",
         ["24 N", "-8 N", "4 N"]),
        ("AP Stretch: Friction does $-12\\,\\mathrm{J}$ while $\\Delta U=-20\\,\\mathrm{J}$. If $K_i=5\\,\\mathrm{J}$, then $K_f$ from $W_\\mathrm{nc}=\\Delta K+\\Delta U$ is",
         "13 J", "$-12=\\Delta K-20$ so $\\Delta K=8$ and $K_f=13\\,\\mathrm{J}$.",
         ["5 J", "17 J", "8 J"]),
        ("AP Stretch: $W=\\int_{(0,0)}^{(2,0)} (3x^2, 0)\\cdot d\\vec r$ along the $x$-axis equals",
         "8 J", "Along $y=0$, $dy=0$, so $W=\\int_0^2 3x^2\\,dx=x^3\\big|_0^2=8\\,\\mathrm{J}$.",
         ["12 J", "6 J", "4 J"]),
    ])
    return qs


def build_unit3():
    title = "AP Physics C Mechanics Unit 3: Work, Energy, and Power"
    description = (
        "Work as a line integral, work-energy with variable force, potential functions, "
        "conservative tests, power as F·v, and mechanical energy diagrams."
    )
    c1 = concept_block(
        "1. Work as a line integral",
        [
            "Work is not “force times distance” once the force changes along the path. The Physics C definition is "
            "the line integral $W=\\int \\vec F\\cdot d\\vec r$. In one dimension that is $W=\\int_{x_i}^{x_f} F_x\\,dx$. "
            "If $F=6x^2$ newtons from $x=1\\,\\mathrm{m}$ to $x=2\\,\\mathrm{m}$, then "
            "$W=\\int_1^2 6x^2\\,dx=2x^3\\big|_1^2=16-2=14\\,\\mathrm{J}$.",
            "The dot product is why a force perpendicular to the motion does zero work. A centripetal force on a "
            "circle, or a static normal force on a bead that slides along a rigid wire, contributes $0$ to $W$ "
            "because $\\vec F\\cdot d\\vec r=0$ at every step.",
            "A constant force recovers the Physics 1 formula: $W=F\\Delta x$ when $F$ and $\\Delta x$ share a line "
            "and a sign. $12\\,\\mathrm{N}$ through $3\\,\\mathrm{m}$ is $36\\,\\mathrm{J}$. Calculus is what you "
            "need when $F$ is $4x$ or $6x^2$.",
            "If you reverse the path, $d\\vec r$ flips sign, so the work by the same $\\vec F$ flips sign. Going "
            "out against a spring stores energy; coming back, the spring does positive work on you.",
            "In the plane, parametrize the path: $d\\vec r=(dx,dy)$. Example: $\\vec F=(2y,2x)$ along $y=x$ from "
            "$(0,0)$ to $(1,1)$ gives $\\int_0^1 4x\\,dx=2\\,\\mathrm{J}$. A different path between the same points "
            "might give a different number — that is the conservative test later in this unit.",
            "Units: the integral of newtons with respect to meters is joules. Write the integral with limits before "
            "you antiderive, exactly as in Unit 1's $\\int v\\,dt$.",
        ],
        "Variable forces (springs, $1/r^2$ gravity, $F(x)$ from a graph) are graded with this integral. "
        "$W=Fd$ is only the constant-$F$ special case.",
        "Write $W=\\int F_x\\,dx$ or $\\int\\vec F\\cdot d\\vec r$, substitute the given $F$, antiderive, and evaluate "
        "the two endpoints. If $F\\perp dr$, the integrand is zero.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", sample_curve(lambda x: 6 * x * x, 0.5, 2.4))],
                points=[(1, 6, "F(1)=6 N"), (2, 24, "F(2)=24 N")],
                xlim=(0, 2.6), ylim=(-2, 32), xlab="x (m)", ylab="F (N)",
            ),
            "$F=6x^2$; work from $x=1$ to $2$ is the area $14\\,\\mathrm{J}$",
            "The area under $F(x)$ from $1$ to $2$ is $\\int 6x^2\\,dx=14\\,\\mathrm{J}$, not a rectangle of height $24$.",
        )
        + solved(
            1, "$F=6x^2$ from $x=1\\,\\mathrm{m}$ to $x=2\\,\\mathrm{m}$. Find $W$.",
            [
                "$W=\\int_1^2 6x^2\\,dx=2x^3\\big|_1^2$.",
                "$2(8)-2(1)=16-2=14$.",
                "Units: $\\mathrm{N}\\cdot\\mathrm{m}=\\mathrm{J}$.",
            ],
            "$14\\,\\mathrm{J}$",
            "",
            "Easy",
        )
        + solved(
            2, "$F=4x$ from $x=0$ to $x=3\\,\\mathrm{m}$. Find $W$.",
            [
                "$W=\\int_0^3 4x\\,dx=2x^2\\big|_0^3$.",
                "$2(9)=18\\,\\mathrm{J}$.",
                "A Physics 1 “average force $6\\,\\mathrm{N}$ times $3\\,\\mathrm{m}$” also gives $18\\,\\mathrm{J}$.",
            ],
            "$18\\,\\mathrm{J}$",
            "",
            "Medium",
        )
        + solved(
            3, "$\\vec F=(2y,2x)$ along the line $y=x$ from $(0,0)$ to $(1,1)$. Find $W$.",
            [
                "On the path, $\\vec F=(2x,2x)$ and $d\\vec r=(dx,dx)$.",
                "$\\vec F\\cdot d\\vec r=4x\\,dx$.",
                "$W=\\int_0^1 4x\\,dx=2\\,\\mathrm{J}$.",
            ],
            "$2\\,\\mathrm{J}$",
            "",
            "Hard",
        )
        + _ican([
            "I can compute $W=\\int F_x\\,dx$ for a polynomial force.",
            "I can explain why a perpendicular force does zero work.",
            "I can set up $\\vec F\\cdot d\\vec r$ on a specified plane path.",
        ]),
        ("Using $W=F(x_f)\\,\\Delta x$ for a changing force",
         "The force at the end of the interval is not the force throughout. You must integrate, or equivalently "
         "use the area under $F(x)$, not a single height times width."),
        ("Write limits on the integral before antideriving",
         "The $14$ in $\\int_1^2 6x^2\\,dx$ comes from $16-2$. Swapping limits would flip the sign of work."),
        [
            "I can compute $W=\\int F_x\\,dx$ for a polynomial force.",
            "I can explain why a perpendicular force does zero work.",
            "I can set up $\\vec F\\cdot d\\vec r$ on a specified plane path.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Work–energy with a variable force",
        [
            "The work–energy theorem is $W_\\mathrm{net}=\\Delta K=\\tfrac12 mv_f^2-\\tfrac12 mv_i^2$. It remains true "
            "when $F$ varies, because $W_\\mathrm{net}$ is the line integral of the net force. If a particle starts "
            "at rest and $W=14\\,\\mathrm{J}$, then $K_f=14\\,\\mathrm{J}$.",
            "Example: $F=6x$ from $x=1$ to $2$, starting at rest. $W=\\int_1^2 6x\\,dx=3x^2\\big|_1^2=9\\,\\mathrm{J}$, "
            "so $K_f=9\\,\\mathrm{J}$. For $m=2\\,\\mathrm{kg}$, $v_f=3\\,\\mathrm{m/s}$.",
            "A $2\\,\\mathrm{kg}$ object going from $3$ to $5\\,\\mathrm{m/s}$ has $\\Delta K=25-9=16\\,\\mathrm{J}$, "
            "so some net work of $16\\,\\mathrm{J}$ was done, whatever mix of forces produced it.",
            "If $W_\\mathrm{net}=0$, $K$ is unchanged. That can still include a round trip on a conservative force, "
            "or a constraint force that never does work.",
            "A spring stretched slowly from $0$ to $A$ has the spring force $-kx$ on the mass if $x$ is the stretch "
            "beyond equilibrium. Work by the spring is $-\\tfrac12 kA^2$. An external agent who stretches it slowly "
            "does $+\\tfrac12 kA^2$.",
            "You can also combine: $W_\\mathrm{nc}=\\Delta E_\\mathrm{mech}=\\Delta K+\\Delta U$ when $U$ accounts for "
            "the conservative pieces. That bookkeeping is the next two concepts.",
        ],
        "This theorem is how you convert a nasty $F(x)$ into a speed without solving the full $x(t)$ differential "
        "equation. AP FRQs expect $\\Delta K=\\int F\\,dx$ rather than $v=at$.",
        "Compute $W$ with the integral, set it equal to $\\Delta K$, and solve for the unknown speed or mass. "
        "Include every force that has a component along the displacement, or use $U$ for the conservative ones.",
        lesson_figure(
            energy_bars_svg(ke=0, pe=4, thermal=0),
            "Before: energy stored as $U$ (or not yet converted). After a net positive work, $K$ bars grow.",
            "Bar charts make $\\Delta K=W_\\mathrm{net}$ visible: kinetic bars rise by the same amount as the net work.",
        )
        + solved(
            6, "A $2\\,\\mathrm{kg}$ object goes from $3\\,\\mathrm{m/s}$ to $5\\,\\mathrm{m/s}$. Find $\\Delta K$.",
            [
                "$K_i=\\tfrac12(2)(9)=9\\,\\mathrm{J}$.",
                "$K_f=\\tfrac12(2)(25)=25\\,\\mathrm{J}$.",
                "$\\Delta K=16\\,\\mathrm{J}=W_\\mathrm{net}$.",
            ],
            "$16\\,\\mathrm{J}$",
            "",
            "Easy",
        )
        + solved(
            7, "$F=6x$ from $x=1$ to $2$, starting at rest. Find $K_f$.",
            [
                "$W=\\int_1^2 6x\\,dx=3x^2\\big|_1^2=12-3=9\\,\\mathrm{J}$.",
                "$K_i=0$, so $K_f=9\\,\\mathrm{J}$.",
                "If $m=2\\,\\mathrm{kg}$, then $v_f=3\\,\\mathrm{m/s}$.",
            ],
            "$9\\,\\mathrm{J}$",
            "",
            "Medium",
        )
        + solved(
            8, "Net work $40\\,\\mathrm{J}$ on $m=5\\,\\mathrm{kg}$ from rest. Find $v_f$.",
            [
                "$\\tfrac12(5)v^2=40$.",
                "$v^2=16$.",
                "$v=4\\,\\mathrm{m/s}$ (speed is nonnegative).",
            ],
            "$4\\,\\mathrm{m/s}$",
            "",
            "Hard",
        )
        + _ican([
            "I can apply $W_\\mathrm{net}=\\Delta K$ with a computed line integral.",
            "I can find a final speed from net work and mass.",
            "I can compute $\\Delta K$ from two speeds.",
        ]),
        ("Setting $W=Fd$ and also using $v^2=v_0^2+2a\\Delta x$ with a changing $F$",
         "Both shortcuts assume constant $F$ (hence constant $a$). Variable $F$ needs the integral for $W$, then $\\Delta K$."),
        ("List forces that do work vs forces that do not",
         "Normals on a rigid surface and ideal centripetal tensions drop out of $W_\\mathrm{net}$. Springs and gravity do not — unless you move them into $U$."),
        [
            "I can apply $W_\\mathrm{net}=\\Delta K$ with a computed line integral.",
            "I can find a final speed from net work and mass.",
            "I can compute $\\Delta K$ from two speeds.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Potential energy functions",
        [
            "A potential energy $U$ is a scalar function whose negative slope is the conservative force: "
            "$F_x=-dU/dx$ in one dimension, or $\\vec F=-\\nabla U$ in space. If $U=3x^2$, then $F_x=-6x$. "
            "You recover $U$ by integrating: $U(x)=-\\int F_x\\,dx+C$.",
            "The constant $C$ is a choice of zero. Forces never notice $C$ because derivatives kill constants. "
            "Only changes $\\Delta U$ enter energy bookkeeping.",
            "Standard catalog: near-Earth gravity $U=mgy$ if $y$ increases upward and $U=0$ at $y=0$. "
            "A spring $U=\\tfrac12 kx^2$ with $x$ the displacement from the unstretched length (ideal Hooke). "
            "A $k=200\\,\\mathrm{N/m}$ spring at $x=0.10\\,\\mathrm{m}$ stores $1\\,\\mathrm{J}$.",
            "If $U=-6/x$ for $x>0$, then $F_x=-dU/dx=-6/x^2$, toward the origin. That is the same shape as "
            "Newton gravity's $U=-GMm/r$ you will meet in Unit 8.",
            "If $U=2x^3$, $F=-6x^2$. At $x=1$, $F=-6\\,\\mathrm{N}$. The force is not constant even though you "
            "have a tidy $U$.",
            "On an FRQ, “find $U(x)$ given $F(x)$” means integrate $-F$ and apply a stated $U$ at one point to fix $C$.",
        ],
        "Energy methods beat $F=ma$ when you care about speeds at two positions, not the time in between. "
        "You cannot write $U$ unless the force is conservative.",
        "If you are given $F$, integrate $U=-\\int F\\,dx$. If you are given $U$, differentiate $F=-dU/dx$. "
        "State where $U=0$.",
        lesson_figure(
            xy_graph(
                curves=[("#059669", sample_curve(lambda x: 0.5 * 2 * x * x, -3, 3))],
                points=[(0, 0, "U=0"), (2, 4, "x=2")],
                xlim=(-3.2, 3.2), ylim=(-0.5, 10), xlab="x", ylab="U(x)",
            ),
            "Spring well $U=\\tfrac12 kx^2$ with $k=2$ (so $U=x^2$)",
            "The slope is zero at $x=0$ (equilibrium). Steeper walls mean a stronger restoring force $|F|=|dU/dx|$.",
        )
        + solved(
            11, "$U=3x^2$. Find $F_x$.",
            [
                "$F_x=-dU/dx$.",
                "$dU/dx=6x$.",
                "$F_x=-6x$.",
            ],
            "$F_x=-6x$",
            "",
            "Easy",
        )
        + solved(
            12, "$k=200\\,\\mathrm{N/m}$, $x=0.10\\,\\mathrm{m}$. Find spring $U$.",
            [
                "$U=\\tfrac12 kx^2$.",
                "$x^2=0.01$.",
                "$U=\\tfrac12(200)(0.01)=1\\,\\mathrm{J}$.",
            ],
            "$1\\,\\mathrm{J}$",
            "",
            "Medium",
        )
        + solved(
            13, "$U=-6/x$ ($x>0$). Find $F_x$ and its direction for $x>0$.",
            [
                "$dU/dx=6/x^2$.",
                "$F_x=-6/x^2$, which is negative.",
                "For $x>0$, negative $F_x$ points toward decreasing $x$, i.e. toward the origin.",
            ],
            "$F_x=-6/x^2$, attractive toward $x=0$",
            "",
            "Hard",
        )
        + _ican([
            "I can get $F$ from $U$ by differentiating.",
            "I can get $U$ from a conservative $F$ by integrating.",
            "I can evaluate spring and $mgy$ potentials with a stated zero.",
        ]),
        ("Writing $U=mgh$ with $h$ as a path length along a ramp",
         "Gravitational $U$ uses vertical height, not distance along the board. A $5\\,\\mathrm{m}$ ramp at $30^\\circ$ "
         "changes $y$ by $2.5\\,\\mathrm{m}$."),
        ("Fix $C$ with the point they give you",
         "If $U(1)=4$, plug $x=1$ into your antiderivative and solve for $C$ before evaluating anywhere else."),
        [
            "I can get $F$ from $U$ by differentiating.",
            "I can get $U$ from a conservative $F$ by integrating.",
            "I can evaluate spring and $mgy$ potentials with a stated zero.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Conservative versus nonconservative forces",
        [
            "A force is conservative if the work between two points does not depend on the path, equivalently if "
            "work around every closed loop is zero, equivalently if $\\vec F=-\\nabla U$ for some $U$. Gravity and "
            "ideal springs are conservative. Kinetic friction is not: a longer scrape means more negative work.",
            "Round trip up height $h$ and back: gravity does $-mgh$ going up and $+mgh$ coming down, net $0$. "
            "Friction on the same round trip does $-f$ times the total distance, which is not zero.",
            "When only conservative forces do work, $K+U$ is constant. When friction or drag does work, "
            "$W_\\mathrm{nc}=\\Delta E_\\mathrm{mech}=\\Delta(K+U)$, and $W_\\mathrm{nc}$ is typically negative.",
            "Constraint forces (ideal string, rigid normal) can be neither “energy-storing” nor dissipative: "
            "they do zero work if $\\vec v$ is perpendicular to them, so they drop out of $E_\\mathrm{mech}$ bookkeeping.",
            "Path independence is a test you can compute: evaluate $\\int\\vec F\\cdot d\\vec r$ on two different "
            "paths. If the numbers differ, you may not define a $U$ for that $\\vec F$.",
            "Exam language: “Justify that mechanical energy is conserved.” You must say which forces do work and "
            "why each is conservative or does zero work — not merely “no friction.”",
        ],
        "Choosing energy versus Newton 2 on an FRQ starts with this classification. Using $U$ for friction is a "
        "fatal category error.",
        "List every force that does work. For each, ask: path-independent? If yes, fold it into $U$. If no, put "
        "its work on the $W_\\mathrm{nc}$ side. If $W=0$ by perpendicularity, omit it.",
        lesson_figure(
            energy_bars_svg(ke=2, pe=1, thermal=2),
            "After sliding with friction: some mechanical energy has become thermal $E_\\mathrm{th}$",
            "The thermal bar is the footprint of nonconservative work. Conservative motion would keep $K+U$ bars adding to a fixed height.",
        )
        + solved(
            16, "A closed loop in a gravitational field (constant $g$). Work by gravity?",
            [
                "Gravity is conservative.",
                "You return to the same $U$.",
                "$W_\\mathrm{grav}=-\\Delta U=0$.",
            ],
            "$0$",
            "",
            "Easy",
        )
        + solved(
            17, "Why is sliding friction nonconservative?",
            [
                "Work by friction is $-f_k$ times the path length (if $f_k$ is constant).",
                "Two paths between the same points can have different lengths.",
                "Therefore $W$ depends on the path, so no single $U_\\mathrm{friction}$ exists.",
            ],
            "Path-dependent work; no potential for kinetic friction.",
            "",
            "Medium",
        )
        + solved(
            18,
            "A block slides down a rough ramp, dropping $5\\,\\mathrm{m}$ vertically, $m=2\\,\\mathrm{kg}$, $g=10$, "
            "and friction does $-30\\,\\mathrm{J}$ of work. Find $K$ at the bottom if it started at rest.",
            [
                "$\\Delta U=mg\\Delta y=20\\times(-5)=-100\\,\\mathrm{J}$.",
                "$W_\\mathrm{nc}=\\Delta K+\\Delta U$ so $-30=\\Delta K-100$.",
                "$\\Delta K=70\\,\\mathrm{J}=K_f$.",
            ],
            "$70\\,\\mathrm{J}$",
            "",
            "Hard",
        )
        + _ican([
            "I can test path independence as the definition of a conservative force.",
            "I can justify mechanical-energy conservation force by force.",
            "I can include $W_\\mathrm{nc}$ when friction does work.",
        ]),
        ("Putting friction into a potential $U_f=\\mu N x$",
         "That expression happens to match $W$ on one straight scrape, but it fails as soon as the path changes. "
         "Friction has no potential energy in this course."),
        ("Name the forces before you write $K_i+U_i=K_f+U_f$",
         "One sentence: “Gravity is conservative; the normal does no work; friction is absent.” Then conservation is justified."),
        [
            "I can test path independence as the definition of a conservative force.",
            "I can justify mechanical-energy conservation force by force.",
            "I can include $W_\\mathrm{nc}$ when friction does work.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Power as F dot v",
        [
            "Power is the rate of doing work: $P=dW/dt$. Because $dW=\\vec F\\cdot d\\vec r$, it follows that "
            "$P=\\vec F\\cdot\\vec v$. If a $12\\,\\mathrm{N}$ force is parallel to $v=3\\,\\mathrm{m/s}$, $P=36\\,\\mathrm{W}$.",
            "If $\\vec F\\perp\\vec v$, power is zero even though a force is present. Uniform circular motion has "
            "a centripetal force and a changing direction, but constant speed, so the centripetal power is $0$.",
            "If $W=4t^2$ joules, $P=8t$. At $t=3\\,\\mathrm{s}$, $P=24\\,\\mathrm{W}$. Differentiating work with "
            "respect to time is the other doorway into the same quantity.",
            "A force at $60^\\circ$ to $\\vec v$: $P=Fv\\cos\\theta$. For $F=20\\,\\mathrm{N}$ and $v=4\\,\\mathrm{m/s}$, "
            "$P=80\\times 1/2=40\\,\\mathrm{W}$.",
            "Average power over an interval is $W/\\Delta t$. Delivering $100\\,\\mathrm{J}$ in $5\\,\\mathrm{s}$ is $20\\,\\mathrm{W}$. "
            "A $50\\,\\mathrm{W}$ motor running $4\\,\\mathrm{s}$ transfers $200\\,\\mathrm{J}$.",
            "Lifting at constant speed, $F=mg$ upward and $P=mgv$. Speeding an object up requires extra force and extra power.",
        ],
        "Motors, towing, and “which engine is stronger” items are power, not energy. Energy can be large with tiny "
        "power if you have a long time.",
        "Write $P=\\vec F\\cdot\\vec v$ or $P=dW/dt$. Check the angle. Watts are joules per second.",
        lesson_figure(
            xy_graph(
                curves=[("#7c3aed", sample_curve(lambda t: 8 * t, 0, 4))],
                points=[(3, 24, "P(3)=24 W")],
                xlim=(0, 4.2), ylim=(-2, 36), xlab="t (s)", ylab="P (W)",
            ),
            "$P=8t$ from $W=4t^2$",
            "The slope of $W(t)$ is power. Here $W$ is a parabola, so $P$ is a straight line through the origin.",
        )
        + solved(
            21, "$F=12\\,\\mathrm{N}$ parallel to $v=3\\,\\mathrm{m/s}$. Find $P$.",
            [
                "$P=Fv$ when the angle is zero.",
                "$P=36\\,\\mathrm{W}$.",
                "In $2\\,\\mathrm{s}$ that would transfer $72\\,\\mathrm{J}$ if $P$ stayed constant.",
            ],
            "$36\\,\\mathrm{W}$",
            "",
            "Easy",
        )
        + solved(
            22, "$W=4t^2$ joules. Find $P$ at $t=3\\,\\mathrm{s}$.",
            [
                "$P=dW/dt=8t$.",
                "At $t=3$, $P=24\\,\\mathrm{W}$.",
                "Check units: $\\mathrm{J/s}=\\mathrm{W}$.",
            ],
            "$24\\,\\mathrm{W}$",
            "",
            "Medium",
        )
        + solved(
            23, "$F=20\\,\\mathrm{N}$ at $60^\\circ$ to $v=4\\,\\mathrm{m/s}$. Find $P$.",
            [
                "$P=Fv\\cos 60^\\circ$.",
                "$\\cos 60^\\circ=1/2$.",
                "$P=80\\times 1/2=40\\,\\mathrm{W}$.",
            ],
            "$40\\,\\mathrm{W}$",
            "",
            "Hard",
        )
        + _ican([
            "I can compute $P=\\vec F\\cdot\\vec v$ including an angle.",
            "I can differentiate $W(t)$ to get $P(t)$.",
            "I can convert between energy, time, and average power.",
        ]),
        ("Calling $P=Fv$ when $\\vec F$ and $\\vec v$ are not aligned",
         "You need the cosine. A $90^\\circ$ force contributes zero power even if $F$ and $v$ are both large."),
        ("Keep watts and joules in different columns",
         "If the question asks for energy, multiply power by time. If it asks for power, divide energy by time or use $F v$."),
        [
            "I can compute $P=\\vec F\\cdot\\vec v$ including an angle.",
            "I can differentiate $W(t)$ to get $P(t)$.",
            "I can convert between energy, time, and average power.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Mechanical energy diagrams",
        [
            "An energy diagram plots $U(x)$ and a horizontal line at the total mechanical energy $E$. At each $x$, "
            "the kinetic energy is the vertical gap $K=E-U(x)$, provided $E\\ge U$. Where $E=U$, $v=0$: a turning point.",
            "A local minimum of $U$ is stable equilibrium: $F=-dU/dx$ pushes back into the well. A local maximum is "
            "unstable: a tiny nudge and the force pushes away. $F=0$ wherever the slope of $U$ is zero.",
            "For a spring, $U=\\tfrac12 kx^2$ is a parabola. If $E=\\tfrac12 kA^2$, the motion is trapped between "
            "$x=\\pm A$, and speed is largest at $x=0$ where $U$ is smallest.",
            "If $E$ is below a hill of $U$, the particle cannot classically cross that hill (KE would be negative). "
            "That is how energy diagrams explain “bound” versus “unbound” motion without solving $x(t)$.",
            "Example: $U=x^3-3x$. Then $F=-3x^2+3$, so equilibria at $x=\\pm 1$. Second derivative $U''=6x$: "
            "$x=1$ is a local minimum (stable), $x=-1$ is a local maximum (unstable).",
            "On FRQs, sketch $U$, draw $E$, mark turning points, and state where $K$ is max. That sketch often "
            "earns points even before any algebra.",
        ],
        "SHM, gravity wells, and “will it make it over the loop” are all energy-diagram stories. Reading $U(x)$ "
        "is faster than integrating $a=F/m$ twice.",
        "Draw $U(x)$. Draw $E$. Allowed regions are where $U\\le E$. Turning points are intersections. "
        "Stability is the curvature of $U$ at $F=0$.",
        lesson_figure(
            xy_graph(
                curves=[("#b45309", sample_curve(lambda x: (x ** 3) / 3 - x, -2.2, 2.2))],
                points=[(-1, 2 / 3, "unstable"), (1, -2 / 3, "stable")],
                dashes=[("h", 0.5, "sample E")],
                xlim=(-2.4, 2.4), ylim=(-2.5, 2.5), xlab="x", ylab="U(x)",
            ),
            "$U=x^3/3-x$ with a sample energy line",
            "The right-hand well can trap a particle if $E$ is below the left peak. Intersections with $E$ are turning points.",
        )
        + solved(
            26, "For $U=\\tfrac12 kx^2$ and $E=\\tfrac12 kA^2$, where is speed maximum?",
            [
                "$K=E-U$ is largest where $U$ is smallest.",
                "$U$ is smallest at $x=0$.",
                "So $|v|$ is maximum at the equilibrium point.",
            ],
            "$x=0$",
            "",
            "Easy",
        )
        + solved(
            27, "What is a turning point on a $U(x)$ diagram?",
            [
                "It is an $x$ where $E=U(x)$.",
                "Then $K=0$, so $v=0$.",
                "If $U$ rises on both sides, the particle reverses.",
            ],
            "A position where $E=U$, hence $v=0$",
            "",
            "Medium",
        )
        + solved(
            28, "$U=x^3-3x$. Classify equilibria at $x=\\pm 1$.",
            [
                "$U'=3x^2-3=0$ at $x=\\pm 1$, so $F=0$ there.",
                "$U''=6x$. At $x=1$, $U''>0$: local minimum, stable.",
                "At $x=-1$, $U''<0$: local maximum, unstable.",
            ],
            "$x=1$ stable, $x=-1$ unstable",
            "",
            "Hard",
        )
        + _ican([
            "I can read turning points as $E=U$ intersections.",
            "I can classify stable vs unstable equilibria from the shape of $U$.",
            "I can find $K=E-U$ as a gap on the diagram.",
        ]),
        ("Calling every $F=0$ point stable",
         "A hilltop has $F=0$ and is unstable. Stability is a second-derivative (or “well vs peak”) test, not the first-derivative test alone."),
        ("Sketch $E$ as a horizontal line, not as another copy of $U$",
         "Total energy is a number for a given motion, constant if $W_\\mathrm{nc}=0$. It is not a function of $x$."),
        [
            "I can read turning points as $E=U$ intersections.",
            "I can classify stable vs unstable equilibria from the shape of $U$.",
            "I can find $K=E-U$ as a gap on the diagram.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        [
            "Compute work as $\\int \\vec F\\cdot d\\vec r$",
            "Use $W_\\mathrm{net}=\\Delta K$ with variable forces",
            "Build $U(x)$ from $F$ and recover $F=-dU/dx$",
            "Sort conservative vs nonconservative forces",
            "Compute power as $\\vec F\\cdot\\vec v$ and as $dW/dt$",
            "Read turning points and stability on energy diagrams",
        ],
        c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Systems of Particles and Momentum
# ===========================================================================

def _cm_svg():
    return (
        '<svg viewBox="0 0 320 120" width="100%" style="max-width:320px" role="img">'
        '<line x1="20" y1="70" x2="300" y2="70" stroke="#0f172a" stroke-width="2"/>'
        '<circle cx="70" cy="70" r="18" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<circle cx="220" cy="70" r="28" fill="#fecaca" stroke="#991b1b"/>'
        '<line x1="160" y1="30" x2="160" y2="100" stroke="#059669" stroke-dasharray="4 3"/>'
        '<text x="58" y="74" font-size="11">m</text>'
        '<text x="206" y="74" font-size="11">2m</text>'
        '<text x="148" y="24" font-size="11">CM</text>'
        "</svg>"
    )


def _u4_questions():
    qs = []
    _add(qs, [
        ("Center of mass of two point masses on a line is $x_\\mathrm{cm}=(m_1 x_1+m_2 x_2)/(m_1+m_2)$. For $m$ at $x=0$ and $2m$ at $x=3$, $x_\\mathrm{cm}$ is",
         "2", "$(0+6)/3=2$.",
         ["1.5", "3", "0"]),
        ("A uniform rod from $x=0$ to $x=L$ has $x_\\mathrm{cm}=$",
         "L/2", "$x_\\mathrm{cm}=(1/M)\\int_0^L x\\,(M/L)\\,dx=L/2$.",
         ["L", "L/3", "0"]),
        ("If linear density $\\lambda=cx$ on $0\\le x\\le L$, then $M=\\int\\lambda\\,dx=$",
         "c L^2 / 2", "$\\int_0^L cx\\,dx=c L^2/2$.",
         ["c L", "c L^2", "c L^3 / 3"]),
        ("For that $\\lambda=cx$ rod, $x_\\mathrm{cm}=$",
         "2L/3", "$x_\\mathrm{cm}=(1/M)\\int_0^L x(cx)\\,dx=(c/M)L^3/3=(2/3)L$.",
         ["L/2", "L/3", "L"]),
        ("The CM of a system of particles moves as if",
         "all mass sat at the CM with F_net^ext = M a_cm", "Newton 2 for the system: $M\\vec a_\\mathrm{cm}=\\vec F_\\mathrm{ext}$.",
         ["internal forces always accelerate the CM", "the heaviest particle is the CM", "CM cannot move"]),
        ("Impulse is $J=\\int F\\,dt$ and equals",
         "Δp", "By $F=dp/dt$, integrating both sides gives $\\Delta p=\\int F\\,dt$.",
         ["ΔK", "power", "ΔU"]),
        ("$F=6\\,\\mathrm{N}$ constant for $2\\,\\mathrm{s}$. Impulse is",
         "12 N·s", "$J=6\\times 2=12\\,\\mathrm{N\\cdot s}$.",
         ["3 N·s", "8 N·s", "6 N·s"]),
        ("$F=6t$ from $t=0$ to $2\\,\\mathrm{s}$. $J=\\int F\\,dt$ is",
         "12 N·s", "$\\int_0^2 6t\\,dt=3t^2\\big|_0^2=12\\,\\mathrm{N\\cdot s}$.",
         ["6 N·s", "24 N·s", "3 N·s"]),
        ("That impulse on $m=3\\,\\mathrm{kg}$ initially at rest gives $v=$",
         "4 m/s", "$\\Delta p=12=mv$, $v=4\\,\\mathrm{m/s}$.",
         ["12 m/s", "3 m/s", "36 m/s"]),
        ("A $p(t)$ graph's change from $t_1$ to $t_2$ equals the area under",
         "F(t)", "Because $J=\\int F\\,dt=\\Delta p$.",
         ["x(t)", "U(x)", "a(x) only"]),
        ("If $\\vec F_\\mathrm{ext}=0$ on a system, total $\\vec P$ is",
         "constant", "Conservation of linear momentum.",
         ["zero always", "increasing", "equal to KE"]),
        ("$3\\,\\mathrm{kg}$ at $4\\,\\mathrm{m/s}$ hits and sticks to $1\\,\\mathrm{kg}$ at rest. Final $v$ is",
         "3 m/s", "$12=(4)v$, $v=3\\,\\mathrm{m/s}$. Perfectly inelastic.",
         ["4 m/s", "1 m/s", "12 m/s"]),
        ("Two equal masses, opposite $5\\,\\mathrm{m/s}$, collide and stick. Final $v$ is",
         "0", "Total $P=0$ remains $0$.",
         ["5 m/s", "10 m/s", "2.5 m/s"]),
        ("Internal forces in a collision (large, brief) typically cancel in the system $P$ because",
         "Newton 3 pairs", "Action-reaction impulses are opposite if they act for the same time.",
         ["energy is always conserved", "mass is zero", "gravity shuts off"]),
        ("A $2\\,\\mathrm{kg}$ cart at $6\\,\\mathrm{m/s}$ catches a $2\\,\\mathrm{kg}$ cart at rest (stick). $v_f=$",
         "3 m/s", "$12=4v$, $v=3$.",
         ["6 m/s", "0", "12 m/s"]),
        ("Rocket thrust (qualitative) comes from",
         "exhaust carrying backward momentum", "The ship gains forward $p$ as exhaust gains backward $p$.",
         ["pushing on air in space as the only option", "burning mass into energy only", "gravity assist inside the engine"]),
        ("If exhaust leaves faster (larger $v_\\mathrm{ex}$) at the same $dm/dt$, thrust",
         "increases", "Thrust $=v_\\mathrm{ex}\\,dm/dt$.",
         ["decreases", "is unchanged", "becomes gravity"]),
        ("In empty space a rocket can still speed up because",
         "momentum is conserved for ship plus exhaust", "No external $F$ is required; the pair's total $P$ stays constant.",
         ["space contains a hidden wall", "mass increase speeds it", "Newton 1 forbids it"]),
        ("Loading sand that had $p_x=0$ onto a moving car tends to",
         "slow the car unless an engine compensates", "The car must share $p_x$ with new mass.",
         ["always speed the car", "leave v unchanged in every model", "reverse the car"]),
        ("Thrust $800\\,\\mathrm{N}$ on $m=200\\,\\mathrm{kg}$ (ignore $g$) gives $a=$",
         "4 m/s^2", "$a=800/200=4\\,\\mathrm{m/s}^2$.",
         ["800 m/s^2", "200 m/s^2", "0"]),
        ("1D elastic collision of equal masses: the velocities",
         "exchange", "Each takes the other's incoming velocity (in 1D, head-on).",
         ["both stop", "add", "halve and keep direction always"]),
        ("$m$ at $v$ hits identical $m$ at rest, elastic, 1D. Recoiling first mass has speed",
         "0", "It stops; the target takes $v$.",
         ["v", "v/2", "2v"]),
        ("Perfectly inelastic means the objects",
         "stick (one common v)", "Maximum KE is lost, consistent with $P$ conservation.",
         ["bounce with no KE loss", "explode", "pass through"]),
        ("A $4\\,\\mathrm{kg}$ object at $3\\,\\mathrm{m/s}$ hits $2\\,\\mathrm{kg}$ at rest and they stick. $v_f=$",
         "2 m/s", "$12=6v$, $v=2$.",
         ["3 m/s", "1 m/s", "6 m/s"]),
        ("In 2D, conservation of $P$ is two equations:",
         "P_x and P_y separately", "Components do not mix.",
         ["only the speed", "only the angle", "only KE"]),
        ("The CM frame is the frame where total $P$ is",
         "0", "It moves at $\\vec V_\\mathrm{cm}=\\vec P_\\mathrm{tot}/M$ relative to the lab.",
         ["maximum", "equal to M g t", "undefined"]),
        ("Lab velocities $v_1=5$, $v_2=-1$, equal masses. $V_\\mathrm{cm}=$",
         "2 m/s", "$(5-1)/2=2\\,\\mathrm{m/s}$.",
         ["4 m/s", "6 m/s", "0"]),
        ("In the CM frame of an equal-mass 1D elastic collision, the particles",
         "approach and recede at equal-and-opposite speeds", "Total $P=0$ stays $0$; elasticity preserves the relative speed.",
         ["both stop forever", "stick", "both go right"]),
        ("KE is least (for a given $P_\\mathrm{tot}$) in the",
         "CM frame", "Lab KE $=KE_\\mathrm{cm}+\\tfrac12 M V_\\mathrm{cm}^2$. The extra term is CM motion.",
         ["lab frame always", "photon frame", "Earth's surface always"]),
        ("A $1\\,\\mathrm{kg}$ and $3\\,\\mathrm{kg}$ at rest explode apart. If the $1\\,\\mathrm{kg}$ goes $6\\,\\mathrm{m/s}$ left, the $3\\,\\mathrm{kg}$ goes",
         "2 m/s right", "$-6+3v=0$, $v=2\\,\\mathrm{m/s}$ right.",
         ["6 m/s right", "2 m/s left", "18 m/s"]),
        ("Uniform rod $0$ to $6\\,\\mathrm{m}$. $x_\\mathrm{cm}=$",
         "3 m", "Midpoint of a uniform rod.",
         ["6 m", "2 m", "0"]),
        ("$F=4t$ from $0$ to $3\\,\\mathrm{s}$. Impulse is",
         "18 N·s", "$\\int_0^3 4t\\,dt=2t^2\\big|_0^3=18$.",
         ["12 N·s", "4 N·s", "36 N·s"]),
        ("$m=2\\,\\mathrm{kg}$, $v_i=5$, $v_f=-3$. Impulse on the object is",
         "-16 N·s", "$\\Delta p=2(-3-5)=-16\\,\\mathrm{N\\cdot s}$.",
         ["16 N·s", "-8 N·s", "2 N·s"]),
        ("Two skaters push off. Total $P$ of the pair (ice frictionless) stays",
         "0 if they started at rest", "Internal impulses cancel.",
         ["equal to their KE", "mg t", "infinite"]),
        ("Elastic vs inelastic is about",
         "whether KE of the system is conserved", "Both conserve $P$ if $F_\\mathrm{ext}=0$. Elastic also conserves KE.",
         ["whether mass is conserved", "whether they touch", "whether time is short"]),
        ("A bullet $0.02\\,\\mathrm{kg}$ at $400\\,\\mathrm{m/s}$ embeds in $1.98\\,\\mathrm{kg}$ block at rest. $v_f=$",
         "4 m/s", "$8=2v$, $v=4\\,\\mathrm{m/s}$.",
         ["400 m/s", "8 m/s", "200 m/s"]),
        ("2D: $p_x$ before $=8$, after one fragment has $p_x=3$. The other has $p_x=$",
         "5", "Component conservation: $8=3+p_x$.",
         ["8", "11", "0"]),
        ("$V_\\mathrm{cm}$ for $2\\,\\mathrm{kg}$ at $6\\,\\mathrm{m/s}$ and $4\\,\\mathrm{kg}$ at $0$ is",
         "2 m/s", "$P=12$, $M=6$, $V_\\mathrm{cm}=2$.",
         ["6 m/s", "3 m/s", "0"]),
        ("In CM frame that pair has velocities",
         "4 m/s and -2 m/s", "$6-2=4$, $0-2=-2$. Total $P=8-8=0$.",
         ["6 and 0", "2 and 2", "3 and -1"]),
        ("Area under an $F(t)$ spike of height $20\\,\\mathrm{N}$ and width $0.10\\,\\mathrm{s}$ (triangle) is impulse",
         "1 N·s", "$\\tfrac12(0.10)(20)=1\\,\\mathrm{N\\cdot s}$.",
         ["2 N·s", "20 N·s", "0.1 N·s"]),
        ("A firework at rest in space bursts. The vector sum of fragment momenta is",
         "0", "No external impulse, $P_\\mathrm{tot}$ stays $0$.",
         ["the chemical energy", "mg", "infinite"]),
        ("Catching a medicine ball increases your mass and, if you were moving and the ball was slower,",
         "tends to decrease your speed", "Inelastic capture shares momentum.",
         ["must increase your speed", "violates Newton 3", "creates energy"]),
        ("$\\lambda=2x$ on $0\\le x\\le 2$. Mass $M=$",
         "4", "$\\int_0^2 2x\\,dx=x^2\\big|_0^2=4$.",
         ["2", "8", "1"]),
        ("For that rod, $x_\\mathrm{cm}=(1/4)\\int_0^2 x(2x)\\,dx=$",
         "4/3", "$(1/4)(2/3)x^3\\big|_0^2=(1/6)\\times 8=4/3$.",
         ["1", "2", "1/2"]),
        ("If $F_\\mathrm{ext}\\ne 0$, $P_\\mathrm{tot}$",
         "changes at rate F_ext", "$dP/dt=F_\\mathrm{ext}$.",
         ["is still constant", "is always zero", "equals K"]),
        ("Equal-mass elastic 1D: incoming $v$ and $0$ become",
         "0 and v", "Velocity exchange.",
         ["v/2 and v/2", "v and v", "-v and 0"]),
        ("AP Stretch: $\\lambda=4x$ on $0\\le x\\le 2$. Compute $M=\\int\\lambda\\,dx$, then $x_\\mathrm{cm}=(1/M)\\int x\\lambda\\,dx$.",
         "4/3", "$M=2x^2\\big|_0^2=8$. $\\int_0^2 4x^2\\,dx=(4/3)x^3\\big|_0^2=32/3$. Then $x_\\mathrm{cm}=(32/3)/8=4/3$.",
         ["1", "2", "8/3"]),
        ("AP Stretch: $\\lambda=6-2x$ on $0\\le x\\le 3$. Compute $M$ and then $x_\\mathrm{cm}$.",
         "1", "$M=6x-x^2\\big|_0^3=9$. $\\int_0^3(6x-2x^2)\\,dx=3x^2-(2/3)x^3\\big|_0^3=9$. Then $x_\\mathrm{cm}=9/9=1$.",
         ["1.5", "3", "9"]),
        ("AP Stretch: $F=9t^2$ from $t=0$ to $t=2$ on $m=3\\,\\mathrm{kg}$ from rest. Impulse $\\int F\\,dt$ then $v_f=$",
         "8 m/s", "$J=\\int_0^2 9t^2\\,dt=3t^3\\big|_0^2=24\\,\\mathrm{N\\cdot s}$. Then $\\Delta p=mv=24$ so $v=8\\,\\mathrm{m/s}$.",
         ["24 m/s", "6 m/s", "16 m/s"]),
        ("AP Stretch: $m_1=3$ at $5\\,\\mathrm{m/s}$ elastic 1D into $m_2=3$ at $-1\\,\\mathrm{m/s}$. Afterward $v_1=$",
         "-1 m/s", "Equal-mass 1D elastic: velocities exchange, so $v_1$ becomes $-1\\,\\mathrm{m/s}$.",
         ["5 m/s", "2 m/s", "4 m/s"]),
        ("AP Stretch: $3\\,\\mathrm{kg}$ at $8\\,\\mathrm{m/s}$ and $6\\,\\mathrm{kg}$ at $-1\\,\\mathrm{m/s}$. Find $V_\\mathrm{cm}$, then the two CM-frame velocities.",
         "6 and -3 m/s", "$P=24-6=18$, $M=9$, $V_\\mathrm{cm}=2\\,\\mathrm{m/s}$. CM velocities: $8-2=6$ and $-1-2=-3\\,\\mathrm{m/s}$.",
         ["8 and -1 m/s", "2 and -2 m/s", "4 and -4 m/s"]),
        ("AP Stretch: A $3\\,\\mathrm{kg}$ object at $4\\,\\mathrm{m/s}$ explodes into $1\\,\\mathrm{kg}$ at $10\\,\\mathrm{m/s}$ (same direction) and $2\\,\\mathrm{kg}$. The $2\\,\\mathrm{kg}$ speed is",
         "1 m/s", "$12=10+2v$, $2 v=2$, $v=1\\,\\mathrm{m/s}$.",
         ["4 m/s", "6 m/s", "5 m/s"]),
        ("AP Stretch: 2D, before $P=(12,-4)$. After, one piece has $P=(5,3)$. The other piece has $P=$",
         "(7, -7)", "$(12,-4)-(5,3)=(7,-7)$.",
         ["(7, 7)", "(17, -1)", "(5, -7)"]),
        ("AP Stretch: $J=\\int_0^2 (12-6t)\\,dt$. The impulse equals",
         "12 N·s", "$12t-3t^2\\big|_0^2=24-12=12\\,\\mathrm{N\\cdot s}$.",
         ["24 N·s", "6 N·s", "0"]),
        ("AP Stretch: A rocket equation $m\\,dv=-v_\\mathrm{ex}\\,dm$ with constant $v_\\mathrm{ex}$. Integrating from $m_0$ to $m$ gives $\\Delta v=$",
         "v_ex ln(m0/m)", "$\\int dv=-v_\\mathrm{ex}\\int_{m_0}^{m} dm/m=v_\\mathrm{ex}\\ln(m_0/m)$.",
         ["v_ex (m0-m)", "v_ex m/m0", "v_ex ln(m/m0)"]),
    ])
    return qs


def build_unit4():
    title = "AP Physics C Mechanics Unit 4: Systems of Particles and Momentum"
    description = (
        "Center of mass by integration, impulse as ∫F dt, conservation of p, rockets, "
        "collisions in 1D and 2D, and the CM frame."
    )
    c1 = concept_block(
        "1. Center of mass by integral",
        [
            "The center of mass is the mass-weighted average position. For points, "
            "$x_\\mathrm{cm}=(\\sum m_i x_i)/M$. For a continuous object, replace the sum by an integral: "
            "$x_\\mathrm{cm}=(1/M)\\int x\\,dm$, with $M=\\int dm$. If $m$ is at $x=0$ and $2m$ at $x=3$, "
            "$x_\\mathrm{cm}=2$.",
            "A uniform rod from $x=0$ to $x=L$ has constant linear density $\\lambda=M/L$, so $dm=\\lambda\\,dx$. "
            "Then $x_\\mathrm{cm}=(1/M)\\int_0^L x\\lambda\\,dx=L/2$, the midpoint, as symmetry demands.",
            "If density varies, symmetry can fail. For $\\lambda=cx$ on $0\\le x\\le L$, first $M=\\int_0^L cx\\,dx=cL^2/2$. "
            "Then $x_\\mathrm{cm}=(1/M)\\int_0^L x(cx)\\,dx=(c/M)(L^3/3)=(2/3)L$. The CM sits toward the heavy end.",
            "In 2D, $x_\\mathrm{cm}=(1/M)\\int x\\,dm$ and $y_\\mathrm{cm}=(1/M)\\int y\\,dm$ separately. A uniform "
            "triangle's CM is at the centroid, one-third of the altitude from a side.",
            "The CM of a system moves as a single particle of mass $M$ acted on only by external forces: "
            "$M\\vec a_\\mathrm{cm}=\\vec F_\\mathrm{ext}$. Internal forces cancel by Newton's third law "
            "(for central forces, the usual AP assumption).",
            "On FRQs, write $dm=\\lambda\\,dx$ or $\\sigma\\,dA$, state the limits, compute $M$ first, then the "
            "moment $\\int x\\,dm$. Do not assume $L/2$ if $\\lambda$ is not constant.",
        ],
        "Rotation (Units 5–6) places axes through the CM whenever possible. Collisions in this unit use "
        "$V_\\mathrm{cm}=P_\\mathrm{tot}/M$. You cannot skip the definition.",
        "Write $M=\\int dm$ first. Then $x_\\mathrm{cm}=(1/M)\\int x\\,dm$. Use symmetry when $\\lambda$ is uniform; "
        "integrate when it is not.",
        lesson_figure(
            _cm_svg(),
            "Two point masses $m$ and $2m$: the CM lies closer to the heavier mass",
            "The dashed line is not the midpoint. With $m$ at $0$ and $2m$ at $3$, $x_\\mathrm{cm}=2$.",
        )
        + solved(
            1, "$m$ at $x=0$ and $2m$ at $x=3$. Find $x_\\mathrm{cm}$.",
            [
                "$x_\\mathrm{cm}=(m\\cdot 0+2m\\cdot 3)/(3m)$.",
                "$=6m/(3m)=2$.",
                "The CM is closer to $2m$, as expected.",
            ],
            "$x_\\mathrm{cm}=2$",
            "",
            "Easy",
        )
        + solved(
            2, "Uniform rod $0$ to $L$. Show $x_\\mathrm{cm}=L/2$ by integral.",
            [
                "$\\lambda=M/L$, $dm=\\lambda\\,dx$.",
                "$x_\\mathrm{cm}=(1/M)\\int_0^L x\\lambda\\,dx=(\\lambda/M)(L^2/2)$.",
                "But $\\lambda/M=1/L$, so $x_\\mathrm{cm}=L/2$.",
            ],
            "$L/2$",
            "",
            "Medium",
        )
        + solved(
            3, "$\\lambda=cx$ on $0\\le x\\le L$. Find $x_\\mathrm{cm}$.",
            [
                "$M=\\int_0^L cx\\,dx=cL^2/2$.",
                "$\\int x\\,dm=\\int_0^L x(cx)\\,dx=cL^3/3$.",
                "$x_\\mathrm{cm}=(cL^3/3)/(cL^2/2)=2L/3$.",
            ],
            "$2L/3$",
            "",
            "Hard",
        )
        + _ican([
            "I can locate the CM of two point masses.",
            "I can integrate $x_\\mathrm{cm}=(1/M)\\int x\\,dm$ for a rod.",
            "I can handle a linear density that varies with $x$.",
        ]),
        ("Assuming the CM is always the geometric center",
         "That is true for uniform density and symmetric shape. A density $\\lambda=cx$ pulls the CM toward larger $x$."),
        ("Compute $M$ as its own integral before the moment",
         "Many students write $(1/L)\\int x\\lambda\\,dx$ mixing $M$ with length. Keep $M=\\int\\lambda\\,dx$ on its own line."),
        [
            "I can locate the CM of two point masses.",
            "I can integrate $x_\\mathrm{cm}=(1/M)\\int x\\,dm$ for a rod.",
            "I can handle a linear density that varies with $x$.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Impulse as the integral of force",
        [
            "Impulse is $\\vec J=\\int_{t_i}^{t_f}\\vec F\\,dt$. Because $\\vec F=d\\vec p/dt$, it follows that "
            "$\\vec J=\\Delta\\vec p$. A constant $6\\,\\mathrm{N}$ for $2\\,\\mathrm{s}$ delivers $12\\,\\mathrm{N\\cdot s}$. "
            "If $F=6t$ from $0$ to $2$, $J=\\int_0^2 6t\\,dt=12\\,\\mathrm{N\\cdot s}$ as well.",
            "On $m=3\\,\\mathrm{kg}$ at rest, that $12\\,\\mathrm{N\\cdot s}$ produces $v=4\\,\\mathrm{m/s}$. "
            "You never needed $a(t)$ as an intermediate if you only want $\\Delta p$.",
            "A kick or a collision is a tall, narrow $F(t)$ spike. The area still equals $\\Delta p$. A triangle of "
            "height $20\\,\\mathrm{N}$ and width $0.10\\,\\mathrm{s}$ has area $1\\,\\mathrm{N\\cdot s}$.",
            "If velocity changes from $+5$ to $-3\\,\\mathrm{m/s}$ for $m=2\\,\\mathrm{kg}$, $\\Delta p=2(-8)=-16\\,\\mathrm{N\\cdot s}$. "
            "The impulse on the object is negative: the force pointed opposite the original motion.",
            "Average force is $J/\\Delta t$. The same $\\Delta p$ in less time means a larger average force "
            "(airbags increase $\\Delta t$).",
            "Graphically, $\\Delta p$ is the area under $F(t)$. Conversely, $F$ is the slope of $p(t)$. "
            "Those are the same calculus pair as $a$ and $v$ in Unit 1.",
        ],
        "Collisions last milliseconds. You almost never know $F(t)$ in detail, but you can still use $J=\\Delta p$ "
        "from the velocities. That is the doorway into conservation of $P$.",
        "Write $J=\\int F\\,dt=\\Delta p$. If $F(t)$ is given, integrate. If two speeds are given, compute $m\\Delta v$. "
        "Watch the sign of $\\Delta v$.",
        lesson_figure(
            xy_graph(
                curves=[("#dc2626", [(0, 0), (1, 12), (2, 0)])],
                points=[(1, 12, "F_peak")],
                xlim=(-0.2, 2.4), ylim=(-1, 14), xlab="t (s)", ylab="F (N)",
            ),
            "A triangular $F(t)$ pulse: impulse is the area",
            "Area $=\\tfrac12(2)(12)=12\\,\\mathrm{N\\cdot s}=\\Delta p$, regardless of the peak value alone.",
        )
        + solved(
            6, "$F=6t$ from $t=0$ to $2\\,\\mathrm{s}$. Find $J$.",
            [
                "$J=\\int_0^2 6t\\,dt=3t^2\\big|_0^2$.",
                "$J=12\\,\\mathrm{N\\cdot s}$.",
                "On $m=3\\,\\mathrm{kg}$ at rest, $v=4\\,\\mathrm{m/s}$.",
            ],
            "$12\\,\\mathrm{N\\cdot s}$",
            "",
            "Easy",
        )
        + solved(
            7, "$m=2\\,\\mathrm{kg}$, $v_i=5\\,\\mathrm{m/s}$, $v_f=-3\\,\\mathrm{m/s}$. Find impulse on the object.",
            [
                "$\\Delta p=m(v_f-v_i)=2(-3-5)$.",
                "$\\Delta p=-16\\,\\mathrm{kg\\,m/s}$.",
                "Impulse is $-16\\,\\mathrm{N\\cdot s}$ (same units).",
            ],
            "$-16\\,\\mathrm{N\\cdot s}$",
            "",
            "Medium",
        )
        + solved(
            8, "$F=6t^2$ from $t=1$ to $t=2$. Find $J$.",
            [
                "$J=\\int_1^2 6t^2\\,dt=2t^3\\big|_1^2$.",
                "$16-2=14\\,\\mathrm{N\\cdot s}$.",
                "Same arithmetic as $\\int_1^2 6x^2\\,dx=14$ in Unit 3, now with time as the variable.",
            ],
            "$14\\,\\mathrm{N\\cdot s}$",
            "",
            "Hard",
        )
        + _ican([
            "I can compute $J=\\int F\\,dt$ for a polynomial $F(t)$.",
            "I can convert impulse into $\\Delta v$ using mass.",
            "I can read impulse as area under an $F(t)$ graph.",
        ]),
        ("Setting impulse equal to $F$ or to $p$",
         "Impulse is the integral of force, or the change in momentum — not the force and not the momentum itself. "
         "Units $\\mathrm{N\\cdot s}=\\mathrm{kg\\,m/s}$."),
        ("If $F(t)$ is a graph, count area; if it is a formula, antiderive",
         "Do not plug the peak force into $J=F\\Delta t$ unless $F$ is actually constant."),
        [
            "I can compute $J=\\int F\\,dt$ for a polynomial $F(t)$.",
            "I can convert impulse into $\\Delta v$ using mass.",
            "I can read impulse as area under an $F(t)$ graph.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Conservation of linear momentum",
        [
            "If the net external impulse on a system is zero, $\\Delta\\vec P_\\mathrm{tot}=0$: total linear momentum "
            "is conserved. Isolated explosions, ice-skater push-offs, and collisions on a frictionless track "
            "are the standard settings.",
            "A $3\\,\\mathrm{kg}$ object at $4\\,\\mathrm{m/s}$ sticks to $1\\,\\mathrm{kg}$ at rest: $12=4v$ so "
            "$v=3\\,\\mathrm{m/s}$. Perfectly inelastic, but $P$ is still conserved. KE is not.",
            "Two equal masses approaching at $5\\,\\mathrm{m/s}$ from opposite ways and sticking end at rest: "
            "total $P$ was already zero.",
            "Internal collision forces are Newton-3 pairs. Their impulses cancel in the system's $\\Delta P$, "
            "provided we include both objects. Gravity during a $2\\,\\mathrm{ms}$ collision is often negligible "
            "compared with the huge contact force (impulse argument).",
            "A $1\\,\\mathrm{kg}$ fragment going $6\\,\\mathrm{m/s}$ left from a $4\\,\\mathrm{kg}$ rest explosion "
            "forces the $3\\,\\mathrm{kg}$ remainder to go $2\\,\\mathrm{m/s}$ right so that $-6+3v=0$.",
            "Write a system, argue $F_\\mathrm{ext}\\approx 0$ (or no external impulse in the direction of interest), "
            "then $P_i=P_f$. One dimension: algebraic signs. Two dimensions: two component equations.",
        ],
        "This conservation law is why you can solve collisions without knowing the contact force. It is the "
        "impulse theorem plus $J_\\mathrm{ext}=0$.",
        "Define the system. Check external impulses. Write $P_{ix}=P_{fx}$ (and $y$ if needed). Solve, then "
        "check KE only if the problem claims elastic.",
        lesson_figure(
            fbd_box(labels=("none on system", "internal", "pair")),
            "For two colliding carts as one system, the huge contact forces are internal",
            "External impulses (friction, a hand) would change total $P$. Isolated carts keep $P_1+P_2$ constant.",
        )
        + solved(
            11, "$3\\,\\mathrm{kg}$ at $4\\,\\mathrm{m/s}$ sticks to $1\\,\\mathrm{kg}$ at rest. Find $v_f$.",
            [
                "$P_i=12\\,\\mathrm{kg\\,m/s}$.",
                "$P_f=4v$.",
                "$v=3\\,\\mathrm{m/s}$ together.",
            ],
            "$3\\,\\mathrm{m/s}$",
            "",
            "Easy",
        )
        + solved(
            12, "$1\\,\\mathrm{kg}$ at $6\\,\\mathrm{m/s}$ left, $3\\,\\mathrm{kg}$ recoils from rest explosion. Find the $3\\,\\mathrm{kg}$ velocity.",
            [
                "$P_i=0$.",
                "$-6+3v=0$.",
                "$v=2\\,\\mathrm{m/s}$ right.",
            ],
            "$2\\,\\mathrm{m/s}$ right",
            "",
            "Medium",
        )
        + solved(
            13, "Bullet $0.02\\,\\mathrm{kg}$ at $400\\,\\mathrm{m/s}$ embeds in $1.98\\,\\mathrm{kg}$ block at rest. Find $v_f$.",
            [
                "$P_i=0.02\\times 400=8\\,\\mathrm{kg\\,m/s}$.",
                "Total mass $2.00\\,\\mathrm{kg}$.",
                "$v_f=8/2=4\\,\\mathrm{m/s}$.",
            ],
            "$4\\,\\mathrm{m/s}$",
            "KE is not conserved in an embedding (perfectly inelastic) collision.",
            "Hard",
        )
        + _ican([
            "I can state when total $P$ is conserved.",
            "I can solve 1D inelastic (sticking) collisions.",
            "I can handle a rest-explosion with two fragments.",
        ]),
        ("Conserving KE in a sticking collision",
         "Sticking is perfectly inelastic: $P$ is conserved, $K$ is not. The missing $K$ became thermal and deformation energy."),
        ("Include every piece of the isolated system",
         "If you omit the target, $P$ of the bullet alone is not conserved — the target exerts an external impulse on it."),
        [
            "I can state when total $P$ is conserved.",
            "I can solve 1D inelastic (sticking) collisions.",
            "I can handle a rest-explosion with two fragments.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Variable-mass rockets, qualitative",
        [
            "A rocket speeds up by throwing mass backward. Ship plus exhaust together can have $F_\\mathrm{ext}=0$ "
            "in space, so total $P$ is conserved, but the ship's mass is decreasing, so the ship's $v$ can rise. "
            "Thrust has magnitude $v_\\mathrm{ex}\\,dm/dt$.",
            "Larger exhaust speed at the same burn rate means larger thrust. Thrust $800\\,\\mathrm{N}$ on "
            "$m=200\\,\\mathrm{kg}$ (ignore gravity) gives $a=4\\,\\mathrm{m/s}^2$ at that instant. A second later "
            "$m$ is smaller, so $a$ is larger for the same thrust.",
            "The differential statement $m\\,dv=-v_\\mathrm{ex}\\,dm$ (positive $v_\\mathrm{ex}$, $dm$ of the ship negative "
            "in some texts — be consistent) integrates to $\\Delta v=v_\\mathrm{ex}\\ln(m_0/m)$ when $v_\\mathrm{ex}$ "
            "is constant: the rocket equation. You should recognize the logarithm, not fear it.",
            "Loading sand with $p_x=0$ onto a moving hopper is the opposite story: new mass must be brought up to "
            "speed, which slows the car unless an engine supplies $\\lambda v$.",
            "“Rockets need air to push on” is false. They push on their own exhaust. Air is a complication, not the engine.",
            "Keep this qualitative plus the two formulas (thrust and the log $\\Delta v$). Detailed multi-stage "
            "design is not the AP emphasis; justifying $P$ conservation of ship-plus-fuel is.",
        ],
        "This is the flagship example of $F=dp/dt$ when $m$ is not constant. It also previews why the CM of "
        "ship-plus-exhaust still drifts at constant velocity if $F_\\mathrm{ext}=0$.",
        "Draw ship and exhaust as one system for $P_\\mathrm{tot}$. For the ship alone, include thrust as $v_\\mathrm{ex}\\,dm/dt$. "
        "Use the current mass in $a=F/m$.",
        lesson_figure(
            _rocket_svg(),
            "Exhaust carries backward momentum; the remaining ship gains forward momentum",
            "Total $P$ of ship plus exhaust can stay zero while the ship's speed grows and its mass falls.",
        )
        + solved(
            16, "Thrust $800\\,\\mathrm{N}$, $m=200\\,\\mathrm{kg}$, ignore $g$. Find $a$.",
            [
                "$a=F/m$ using current mass.",
                "$a=800/200=4\\,\\mathrm{m/s}^2$.",
                "As fuel leaves, this $a$ would increase if thrust stayed the same.",
            ],
            "$4\\,\\mathrm{m/s}^2$",
            "",
            "Easy",
        )
        + solved(
            17, "Why can a rocket accelerate in empty space?",
            [
                "The system is ship plus exhaust.",
                "No external force is required for that system's $P$ to stay constant.",
                "The ship’s $p$ rises because the exhaust’s $p$ is opposite.",
            ],
            "Momentum conservation of ship plus exhaust; thrust is not a push on outside air.",
            "",
            "Medium",
        )
        + solved(
            18, "Integrate $m\\,dv=-v_\\mathrm{ex}\\,dm$ for constant $v_\\mathrm{ex}$ from $m_0$ to $m$. Find $\\Delta v$.",
            [
                "$\\int_{v_0}^{v} dv=-v_\\mathrm{ex}\\int_{m_0}^{m} dm/m$.",
                "$\\Delta v=-v_\\mathrm{ex}\\ln(m/m_0)=v_\\mathrm{ex}\\ln(m_0/m)$.",
                "Larger mass ratio $m_0/m$ means a larger speed change.",
            ],
            "$\\Delta v=v_\\mathrm{ex}\\ln(m_0/m)$",
            "",
            "Hard",
        )
        + _ican([
            "I can compute instantaneous rocket $a$ from thrust and current mass.",
            "I can justify rocket acceleration using ship-plus-exhaust momentum.",
            "I can recognize $\\Delta v=v_\\mathrm{ex}\\ln(m_0/m)$.",
        ]),
        ("Claiming a rocket cannot work in vacuum",
         "The exhaust is the other part of the Newton-3 pair. Vacuum is where rockets work most cleanly."),
        ("Use the mass at the moment you want $a$",
         "Do not divide thrust by the launch mass after most of the fuel is gone."),
        [
            "I can compute instantaneous rocket $a$ from thrust and current mass.",
            "I can justify rocket acceleration using ship-plus-exhaust momentum.",
            "I can recognize $\\Delta v=v_\\mathrm{ex}\\ln(m_0/m)$.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Collisions in one and two dimensions",
        [
            "Classify first: elastic means system KE is conserved (as well as $P$). Perfectly inelastic means "
            "the objects stick and share one $v$. “Inelastic” in between conserves $P$ but not KE.",
            "One-dimensional elastic collision of equal masses: the velocities exchange. A mass with $v$ hitting "
            "an identical rest mass stops; the target leaves with $v$. If they come in at $6$ and $-2$, they leave "
            "at $-2$ and $6$.",
            "Unequal masses, 1D elastic, have a standard pair of formulas, but you can also solve "
            "$m_1 v_1+m_2 v_2=m_1 v_1'+m_2 v_2'$ together with relative-speed reversal "
            "$v_1-v_2=-(v_1'-v_2')$ (coefficient of restitution $1$).",
            "A $4\\,\\mathrm{kg}$ object at $3\\,\\mathrm{m/s}$ sticking to $2\\,\\mathrm{kg}$ at rest: $v_f=2\\,\\mathrm{m/s}$. "
            "KE drops from $18\\,\\mathrm{J}$ to $12\\,\\mathrm{J}$.",
            "Two dimensions: conserve $P_x$ and $P_y$ separately. If before $P=(8,0)$ and one fragment after has "
            "$(3,4)$, the other has $(5,-4)$. Angles appear through components, not through a single “momentum magnitude” equation.",
            "Glancing elastic collisions of equal masses in 2D have a geometric property (depart at $90^\\circ$) "
            "that AP may mention; the reliable method is still components plus KE if elastic.",
        ],
        "This is the highest-frequency “system” topic on Mechanics. Mixing up elastic and inelastic is the "
        "fastest way to lose an FRQ.",
        "Write $P$ conservation (1 or 2 components). Add KE conservation only if the problem says elastic. "
        "If they stick, one unknown velocity.",
        lesson_figure(
            xy_graph(
                points=[(0, 0, "before"), (4, 0, "p1"), (1, 3, "p1'"), (3, -3, "p2'")],
                xlim=(-1, 6), ylim=(-4, 4), xlab="p_x", ylab="p_y",
            ),
            "Momentum vectors in 2D: the vector sum before equals the vector sum after",
            "Here $(4,0)$ splits into $(1,3)$ and $(3,-3)$. Check: $(1+3,\\,3-3)=(4,0)$.",
        )
        + solved(
            21, "Equal masses, 1D elastic, $v$ hits $0$. Find the outgoing speeds.",
            [
                "Velocities exchange.",
                "The striker stops.",
                "The target leaves with $v$.",
            ],
            "$0$ and $v$",
            "",
            "Easy",
        )
        + solved(
            22, "$4\\,\\mathrm{kg}$ at $3\\,\\mathrm{m/s}$ sticks to $2\\,\\mathrm{kg}$ at rest. Find $v_f$ and comment on KE.",
            [
                "$12=6v$ so $v=2\\,\\mathrm{m/s}$.",
                "$K_i=18\\,\\mathrm{J}$, $K_f=12\\,\\mathrm{J}$.",
                "KE dropped; the collision is perfectly inelastic.",
            ],
            "$2\\,\\mathrm{m/s}$; KE not conserved",
            "",
            "Medium",
        )
        + solved(
            23, "Before $P=(8,0)$. After, one piece has $(3,4)$. Find the other piece's $P$.",
            [
                "$(P_{2x},P_{2y})=(8,0)-(3,4)$.",
                "$P_2=(5,-4)$.",
                "Check magnitudes only if asked; conservation is vectorial.",
            ],
            "$(5,-4)$",
            "",
            "Hard",
        )
        + _ican([
            "I can exchange velocities in equal-mass 1D elastic collisions.",
            "I can solve sticking collisions with one common $v$.",
            "I can conserve $P_x$ and $P_y$ in two dimensions.",
        ]),
        ("Using one speed equation instead of two components in 2D",
         "Momentum is a vector. Conserving $|P|$ is not a law. Write $x$ and $y$ separately."),
        ("Label elastic vs perfectly inelastic before choosing equations",
         "Sticking: one unknown. Elastic: two unknowns, so you need KE or relative-speed reversal as the second equation."),
        [
            "I can exchange velocities in equal-mass 1D elastic collisions.",
            "I can solve sticking collisions with one common $v$.",
            "I can conserve $P_x$ and $P_y$ in two dimensions.",
        ],
        21,
    )

    c6 = concept_block(
        "6. The center-of-mass frame",
        [
            "The CM frame is the inertial frame that rides along with the center of mass, so $\\vec P_\\mathrm{tot}=0$ "
            "there. It moves at $\\vec V_\\mathrm{cm}=\\vec P_\\mathrm{lab}/M$ relative to the lab. For $2\\,\\mathrm{kg}$ "
            "at $6\\,\\mathrm{m/s}$ and $4\\,\\mathrm{kg}$ at $0$, $V_\\mathrm{cm}=2\\,\\mathrm{m/s}$.",
            "Subtract $V_\\mathrm{cm}$ from every lab velocity to enter the CM frame. Those two masses become "
            "$4\\,\\mathrm{m/s}$ and $-2\\,\\mathrm{m/s}$, and $2(4)+4(-2)=0$, as required.",
            "Lab kinetic energy splits as $K_\\mathrm{lab}=K_\\mathrm{cm}+\\tfrac12 M V_\\mathrm{cm}^2$. The second "
            "term is energy of the CM motion and cannot be dissipated in a collision of the two objects. "
            "That is why $K$ in the CM frame is the energy “available” to inelastic processes.",
            "Equal-mass 1D elastic collision in the CM frame: the particles approach with opposite velocities and "
            "recede with opposite velocities of the same size (they bounce). Transforming back to the lab recovers "
            "the velocity-exchange rule.",
            "Explosions in the CM frame send fragments both ways with $\\sum m_i\\vec v_i'=0$. Chemical energy "
            "increases $K_\\mathrm{cm}$; it does not create net $P$.",
            "AP items may ask you to “analyze in the CM frame.” Translate velocities, impose $P=0$, apply elastic "
            "or inelastic conditions, then add $V_\\mathrm{cm}$ back.",
        ],
        "Hard collision FRQs become shorter in the CM frame because one constraint ($P=0$) is already used. "
        "It is also how physicists talk about available energy.",
        "Compute $V_\\mathrm{cm}$. Subtract it from every $v$. Do the collision. Add $V_\\mathrm{cm}$ back to report lab answers.",
        lesson_figure(
            xy_graph(
                points=[(-2, 0, "m, v=-2"), (4, 0, "m, v=+4"), (0, 0, "CM at rest")],
                xlim=(-4, 6), ylim=(-2, 2), xlab="v in CM frame", ylab="",
            ),
            "Equal masses in the CM frame: opposite velocities, total $P=0$",
            "The CM sits still at the origin of this velocity picture. After a 1D elastic bounce the arrows reverse.",
        )
        + solved(
            26, "$2\\,\\mathrm{kg}$ at $6\\,\\mathrm{m/s}$ and $4\\,\\mathrm{kg}$ at $0$. Find $V_\\mathrm{cm}$.",
            [
                "$P=12\\,\\mathrm{kg\\,m/s}$, $M=6\\,\\mathrm{kg}$.",
                "$V_\\mathrm{cm}=2\\,\\mathrm{m/s}$.",
                "CM-frame velocities: $4\\,\\mathrm{m/s}$ and $-2\\,\\mathrm{m/s}$.",
            ],
            "$2\\,\\mathrm{m/s}$",
            "",
            "Easy",
        )
        + solved(
            27, "Equal masses at lab velocities $6$ and $-2\\,\\mathrm{m/s}$. Find $V_\\mathrm{cm}$.",
            [
                "$P$ per mass unit: $(6-2)/2=2$ if masses are equal.",
                "More carefully $P=m(6)+m(-2)=4m$, $M=2m$, $V_\\mathrm{cm}=2\\,\\mathrm{m/s}$.",
                "CM-frame speeds: $4$ and $-4\\,\\mathrm{m/s}$.",
            ],
            "$2\\,\\mathrm{m/s}$",
            "",
            "Medium",
        )
        + solved(
            28, "Why is $K$ in the CM frame the energy that can be lost in an inelastic collision?",
            [
                "$K_\\mathrm{lab}=K_\\mathrm{rel}+\\tfrac12 M V_\\mathrm{cm}^2$.",
                "Internal collision forces cannot change $V_\\mathrm{cm}$ when $F_\\mathrm{ext}=0$.",
                "So $\\tfrac12 M V_\\mathrm{cm}^2$ is locked; only $K_\\mathrm{cm}$ can drop.",
            ],
            "The $\\tfrac12 M V_\\mathrm{cm}^2$ piece is frozen by momentum conservation.",
            "",
            "Hard",
        )
        + _ican([
            "I can compute $V_\\mathrm{cm}=P_\\mathrm{tot}/M$.",
            "I can transform velocities into the CM frame.",
            "I can explain why CM-frame KE is the dissipatable energy.",
        ]),
        ("Forgetting to subtract $V_\\mathrm{cm}$ from both objects",
         "The CM frame is a single boost. Every velocity, including a “rest” target, changes by $-V_\\mathrm{cm}$."),
        ("Find $V_\\mathrm{cm}$ first, even if the problem never uses those words",
         "If two masses look messy in the lab, boosting to $P=0$ often halves the algebra."),
        [
            "I can compute $V_\\mathrm{cm}=P_\\mathrm{tot}/M$.",
            "I can transform velocities into the CM frame.",
            "I can explain why CM-frame KE is the dissipatable energy.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        [
            "Locate CM with sums and with $\\int x\\,dm$",
            "Compute impulse as $\\int F\\,dt=\\Delta p$",
            "Conserve total $P$ when external impulse is zero",
            "Explain rockets and loading cars with variable mass",
            "Solve 1D/2D collisions, elastic and inelastic",
            "Work in the CM frame where total $P$ is zero",
        ],
        c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
