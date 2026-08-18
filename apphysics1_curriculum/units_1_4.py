"""AP Physics 1 units 1–4: kinematics, forces, energy, and momentum (algebra-based)."""
from __future__ import annotations

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, mq,
    xy_graph, sample_curve, fbd_box, energy_bars_svg, spring_mass_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _add(qs, rows):
    i = len(qs) + 1
    for text, ans, expl, dist in rows:
        qs.append(mq(text, ans, expl, i, distractors=dist))
        i += 1


def _rel_arrows():
    return (
        '<svg viewBox="0 0 320 140" width="100%" style="max-width:320px" role="img">'
        '<rect x="20" y="50" width="160" height="36" fill="#e0e7ff" stroke="#312e81"/>'
        '<text x="100" y="73" text-anchor="middle" font-size="12">walkway +4 m/s</text>'
        '<line x1="40" y1="30" x2="140" y2="30" stroke="#b91c1c" stroke-width="3"/>'
        '<polygon points="140,24 156,30 140,36" fill="#b91c1c"/>'
        '<text x="88" y="22" font-size="11" fill="#b91c1c">walker +3 m/s vs walkway</text>'
        '<line x1="40" y1="110" x2="220" y2="110" stroke="#15803d" stroke-width="3"/>'
        '<polygon points="220,104 236,110 220,116" fill="#15803d"/>'
        '<text x="90" y="132" font-size="11" fill="#15803d">ground velocity +7 m/s</text>'
        "</svg>"
    )


def _newton3_pair():
    return (
        '<svg viewBox="0 0 320 150" width="100%" style="max-width:320px" role="img">'
        '<rect x="40" y="55" width="70" height="44" fill="#c7d2fe" stroke="#312e81"/>'
        '<rect x="210" y="55" width="70" height="44" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="75" y="82" text-anchor="middle" font-size="12">A</text>'
        '<text x="245" y="82" text-anchor="middle" font-size="12">B</text>'
        '<line x1="110" y1="70" x2="200" y2="70" stroke="#b91c1c" stroke-width="2.4"/>'
        '<polygon points="198,64 210,70 198,76" fill="#b91c1c"/>'
        '<text x="130" y="62" font-size="11" fill="#b91c1c">A on B</text>'
        '<line x1="210" y1="88" x2="120" y2="88" stroke="#1d4ed8" stroke-width="2.4"/>'
        '<polygon points="122,82 110,88 122,94" fill="#1d4ed8"/>'
        '<text x="145" y="108" font-size="11" fill="#1d4ed8">B on A</text>'
        "</svg>"
    )


def _connected_blocks():
    return (
        '<svg viewBox="0 0 340 130" width="100%" style="max-width:340px" role="img">'
        '<rect x="30" y="48" width="70" height="40" fill="#c7d2fe" stroke="#312e81"/>'
        '<rect x="160" y="48" width="70" height="40" fill="#c7d2fe" stroke="#312e81"/>'
        '<line x1="100" y1="68" x2="160" y2="68" stroke="#0f172a" stroke-width="2"/>'
        '<text x="65" y="73" text-anchor="middle" font-size="12">m₁</text>'
        '<text x="195" y="73" text-anchor="middle" font-size="12">m₂</text>'
        '<line x1="230" y1="68" x2="300" y2="68" stroke="#b91c1c" stroke-width="2.4"/>'
        '<polygon points="298,62 314,68 298,74" fill="#b91c1c"/>'
        '<text x="250" y="58" font-size="11" fill="#b91c1c">F</text>'
        '<text x="120" y="58" font-size="11">T</text>'
        "</svg>"
    )


def _fbd_pull_and_friction():
    """Level-floor FBD with both a rightward pull and leftward kinetic friction."""
    return (
        '<svg viewBox="0 0 320 210" width="100%" style="max-width:320px" role="img">'
        '<line x1="20" y1="155" x2="300" y2="155" stroke="#64748b" stroke-width="3"/>'
        '<rect x="125" y="95" width="70" height="50" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>'
        '<line x1="160" y1="95" x2="160" y2="28" stroke="#0f172a" stroke-width="2.4"/>'
        '<polygon points="155,30 160,18 165,30" fill="#0f172a"/>'
        '<text x="168" y="48" font-size="12">N</text>'
        '<line x1="160" y1="145" x2="160" y2="198" stroke="#0f172a" stroke-width="2.4"/>'
        '<polygon points="155,196 160,208 165,196" fill="#0f172a"/>'
        '<text x="168" y="192" font-size="12">F_g</text>'
        '<line x1="195" y1="118" x2="275" y2="118" stroke="#15803d" stroke-width="2.6"/>'
        '<polygon points="273,112 288,118 273,124" fill="#15803d"/>'
        '<text x="230" y="108" font-size="12" fill="#15803d">F</text>'
        '<line x1="125" y1="130" x2="45" y2="130" stroke="#b91c1c" stroke-width="2.6"/>'
        '<polygon points="47,124 32,130 47,136" fill="#b91c1c"/>'
        '<text x="52" y="122" font-size="12" fill="#b91c1c">f_k</text>'
        "</svg>"
    )


def _fbd_friction_vs_v():
    """Sliding crate: f_k left, velocity marked to the right."""
    return (
        '<svg viewBox="0 0 320 210" width="100%" style="max-width:320px" role="img">'
        '<line x1="20" y1="155" x2="300" y2="155" stroke="#64748b" stroke-width="3"/>'
        '<rect x="125" y="95" width="70" height="50" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>'
        '<line x1="160" y1="95" x2="160" y2="28" stroke="#0f172a" stroke-width="2.4"/>'
        '<polygon points="155,30 160,18 165,30" fill="#0f172a"/>'
        '<text x="168" y="48" font-size="12">N</text>'
        '<line x1="160" y1="145" x2="160" y2="198" stroke="#0f172a" stroke-width="2.4"/>'
        '<polygon points="155,196 160,208 165,196" fill="#0f172a"/>'
        '<text x="168" y="192" font-size="12">F_g</text>'
        '<line x1="125" y1="120" x2="40" y2="120" stroke="#b91c1c" stroke-width="2.6"/>'
        '<polygon points="42,114 28,120 42,126" fill="#b91c1c"/>'
        '<text x="48" y="112" font-size="12" fill="#b91c1c">f_k</text>'
        '<line x1="200" y1="80" x2="280" y2="80" stroke="#1d4ed8" stroke-width="2.4"/>'
        '<polygon points="278,74 292,80 278,86" fill="#1d4ed8"/>'
        '<text x="228" y="72" font-size="12" fill="#1d4ed8">v</text>'
        "</svg>"
    )


def _ramp_fbd():
    """Ramp FBD with N and mg cosθ on the true surface normal (5-12 rise/run, θ≈23°)."""
    # Surface (40,190)→(280,90): run 240, rise 100. û_up=(12/13,-5/13), n_out=(-5/13,-12/13).
    return (
        '<svg viewBox="0 0 340 220" width="100%" style="max-width:340px" role="img">'
        '<polygon points="40,190 300,190 300,90 280,90" fill="#e2e8f0" stroke="#334155"/>'
        '<line x1="40" y1="190" x2="280" y2="90" stroke="#334155" stroke-width="3"/>'
        '<rect x="135" y="126" width="50" height="28" transform="rotate(-22.6 160 140)" fill="#c7d2fe" stroke="#312e81"/>'
        '<line x1="160" y1="140" x2="160" y2="198" stroke="#0f172a" stroke-width="2.2"/>'
        '<polygon points="155,196 160,208 165,196" fill="#0f172a"/>'
        '<text x="168" y="190" font-size="11">F_g</text>'
        '<line x1="160" y1="140" x2="138" y2="86" stroke="#15803d" stroke-width="2.2"/>'
        '<polygon points="132,92 132,78 146,88" fill="#15803d"/>'
        '<text x="100" y="82" font-size="11" fill="#15803d">N</text>'
        '<line x1="160" y1="140" x2="214" y2="118" stroke="#b91c1c" stroke-width="2.2"/>'
        '<polygon points="210,112 226,114 212,126" fill="#b91c1c"/>'
        '<text x="218" y="110" font-size="11" fill="#b91c1c">f_k</text>'
        '<line x1="160" y1="140" x2="114" y2="159" stroke="#7c3aed" stroke-width="1.8" stroke-dasharray="4 3"/>'
        '<text x="58" y="172" font-size="10" fill="#7c3aed">mg sinθ</text>'
        '<line x1="160" y1="140" x2="179" y2="186" stroke="#c2410c" stroke-width="1.8" stroke-dasharray="4 3"/>'
        '<text x="184" y="200" font-size="10" fill="#c2410c">mg cosθ</text>'
        '<text x="268" y="182" font-size="12">θ</text>'
        "</svg>"
    )


def _explosion_svg():
    """Resting object splits into opposite-going fragments (not a stuck pair)."""
    return (
        '<svg viewBox="0 0 340 140" width="100%" style="max-width:340px" role="img">'
        '<text x="70" y="22" text-anchor="middle" font-size="12">before (at rest)</text>'
        '<circle cx="70" cy="78" r="22" fill="#c4b5fd" stroke="#5b21b6"/>'
        '<text x="70" y="82" text-anchor="middle" font-size="11">M</text>'
        '<text x="250" y="22" text-anchor="middle" font-size="12">after (splits)</text>'
        '<circle cx="210" cy="78" r="16" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<circle cx="290" cy="78" r="16" fill="#fdba74" stroke="#9a3412"/>'
        '<line x1="210" y1="78" x2="168" y2="78" stroke="#1d4ed8" stroke-width="2"/>'
        '<polygon points="170,73 158,78 170,83" fill="#1d4ed8"/>'
        '<text x="168" y="68" font-size="11" fill="#1d4ed8">m₁ v₁</text>'
        '<line x1="290" y1="78" x2="328" y2="78" stroke="#b91c1c" stroke-width="2"/>'
        '<polygon points="326,73 338,78 326,83" fill="#b91c1c"/>'
        '<text x="292" y="68" font-size="11" fill="#b91c1c">m₂ v₂</text>'
        "</svg>"
    )


def _collision_before_after():
    return (
        '<svg viewBox="0 0 340 130" width="100%" style="max-width:340px" role="img">'
        '<text x="70" y="22" text-anchor="middle" font-size="12">before</text>'
        '<circle cx="50" cy="70" r="18" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<circle cx="130" cy="70" r="18" fill="#fdba74" stroke="#9a3412"/>'
        '<line x1="70" y1="70" x2="100" y2="70" stroke="#0f172a" stroke-width="2"/>'
        '<polygon points="100,65 112,70 100,75" fill="#0f172a"/>'
        '<text x="250" y="22" text-anchor="middle" font-size="12">after (stuck)</text>'
        '<circle cx="230" cy="70" r="18" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<circle cx="262" cy="70" r="18" fill="#fdba74" stroke="#9a3412"/>'
        '<line x1="280" y1="70" x2="318" y2="70" stroke="#15803d" stroke-width="2"/>'
        '<polygon points="318,65 330,70 318,75" fill="#15803d"/>'
        "</svg>"
    )


# ===========================================================================
# UNIT 1: Kinematics
# ===========================================================================

def _u1_questions():
    qs = []
    _add(qs, [
        ("A skateboarder moves from $x=3\\,\\mathrm{m}$ to $x=15\\,\\mathrm{m}$ in $4.0\\,\\mathrm{s}$. What is the average velocity?",
         "$3\\,\\mathrm{m/s}$",
         "Average velocity is displacement over time: $\\bar{v}=\\Delta x/\\Delta t=(15-3)/4=12/4=3\\,\\mathrm{m/s}$.",
         ["$4\\,\\mathrm{m/s}$", "$12\\,\\mathrm{m/s}$", "$18\\,\\mathrm{m/s}$"]),
        ("Speed is how fast you are going, with no direction. Velocity is speed with a direction. A bee flies $6\\,\\mathrm{m/s}$ east, then $6\\,\\mathrm{m/s}$ west. Which statement is true?",
         "the speed stayed $6\\,\\mathrm{m/s}$ while the velocity reversed",
         "The magnitude (speed) is still $6\\,\\mathrm{m/s}$, but the velocity vector flipped from east to west.",
         ["both speed and velocity were unchanged", "the speed became zero when it turned", "velocity has no sign so nothing reversed"]),
        ("A cart's velocity changes from $2\\,\\mathrm{m/s}$ to $14\\,\\mathrm{m/s}$ in $3.0\\,\\mathrm{s}$ in a straight line. What is the average acceleration?",
         "$4\\,\\mathrm{m/s}^2$",
         "$\\bar{a}=\\Delta v/\\Delta t=(14-2)/3=12/3=4\\,\\mathrm{m/s}^2$.",
         ["$2\\,\\mathrm{m/s}^2$", "$6\\,\\mathrm{m/s}^2$", "$12\\,\\mathrm{m/s}^2$"]),
        ("A hiker walks $8\\,\\mathrm{m}$ north and then $3\\,\\mathrm{m}$ south. What is the displacement from the start?",
         "$5\\,\\mathrm{m}$ north",
         "Displacement is the net change in position: $8-3=5\\,\\mathrm{m}$ north. Distance traveled would be $11\\,\\mathrm{m}$.",
         ["$11\\,\\mathrm{m}$ north", "$5\\,\\mathrm{m}$ south", "$8\\,\\mathrm{m}$ north"]),
        ("Position $x$ tells you where an object is on a number line. If $x$ is decreasing with time, the velocity is",
         "negative",
         "Velocity is the rate of change of position. If $x$ is falling, $v$ is negative (motion toward smaller $x$).",
         ["positive", "always zero", "undefined until you know mass"]),
    ])
    _add(qs, [
        ("A rover starts from rest and speeds up at a constant $5\\,\\mathrm{m/s}^2$ for $4.0\\,\\mathrm{s}$. How fast is it going at $t=4.0\\,\\mathrm{s}$?",
         "$20\\,\\mathrm{m/s}$",
         "Use $v=v_0+at=0+(5)(4)=20\\,\\mathrm{m/s}$.",
         ["$5\\,\\mathrm{m/s}$", "$10\\,\\mathrm{m/s}$", "$40\\,\\mathrm{m/s}$"]),
        ("A crate sliding at $12\\,\\mathrm{m/s}$ slows at $3\\,\\mathrm{m/s}^2$. How far does it travel before stopping?",
         "$24\\,\\mathrm{m}$",
         "Use $v^2=v_0^2+2a\\Delta x$. $0=144+2(-3)\\Delta x$, so $6\\Delta x=144$ and $\\Delta x=24\\,\\mathrm{m}$.",
         ["$4\\,\\mathrm{m}$", "$36\\,\\mathrm{m}$", "$72\\,\\mathrm{m}$"]),
        ("A sprinter has $v_0=6\\,\\mathrm{m/s}$ and $a=2\\,\\mathrm{m/s}^2$. How far does the sprinter run in $3.0\\,\\mathrm{s}$?",
         "$27\\,\\mathrm{m}$",
         "$\\Delta x=v_0 t+\\tfrac12 at^2=6(3)+\\tfrac12(2)(9)=18+9=27\\,\\mathrm{m}$.",
         ["$18\\,\\mathrm{m}$", "$24\\,\\mathrm{m}$", "$36\\,\\mathrm{m}$"]),
        ("You know $v_0$, $v$, and $a$, but not $t$. Which constant-acceleration equation finds $\\Delta x$ directly?",
         "$v^2=v_0^2+2a\\Delta x$",
         "That equation has no $t$. The other standard forms all include time.",
         ["$v=v_0+at$", "$\\Delta x=\\bar{v}t$ only if $a=0$", "$F=ma$"]),
        ("A bus moving at $16\\,\\mathrm{m/s}$ brakes with $a=-4\\,\\mathrm{m/s}^2$ for $2.0\\,\\mathrm{s}$. What is its speed after those $2.0\\,\\mathrm{s}$?",
         "$8\\,\\mathrm{m/s}$",
         "$v=16+(-4)(2)=8\\,\\mathrm{m/s}$. Speed is the magnitude, still $8\\,\\mathrm{m/s}$.",
         ["$8\\,\\mathrm{m/s}$ backward", "$24\\,\\mathrm{m/s}$", "$4\\,\\mathrm{m/s}$"]),
    ])
    _add(qs, [
        ("On a $v$-$t$ graph, the area between the curve and the time axis equals",
         "displacement",
         "On AP Physics 1 you compute geometric area of the $v$-$t$ shape: that area is $\\Delta x$.",
         ["acceleration", "speed at one instant", "mass"]),
        ("A $v$-$t$ graph is a horizontal line at $v=6\\,\\mathrm{m/s}$ from $t=0$ to $t=5\\,\\mathrm{s}$. What is $\\Delta x$?",
         "$30\\,\\mathrm{m}$",
         "Rectangle area: $(6\\,\\mathrm{m/s})(5\\,\\mathrm{s})=30\\,\\mathrm{m}$.",
         ["$6\\,\\mathrm{m}$", "$11\\,\\mathrm{m}$", "$1.2\\,\\mathrm{m}$"]),
        ("The slope of a position-versus-time graph is",
         "velocity",
         "Slope is rise/run $=\\Delta x/\\Delta t$, which is velocity. Steeper means faster.",
         ["acceleration", "force", "kinetic energy"]),
        ("A $v$-$t$ graph rises in a straight line from $0$ to $10\\,\\mathrm{m/s}$ in $4.0\\,\\mathrm{s}$. What is the acceleration?",
         "$2.5\\,\\mathrm{m/s}^2$",
         "Slope of $v$-$t$ is $a=(10-0)/4=2.5\\,\\mathrm{m/s}^2$.",
         ["$10\\,\\mathrm{m/s}^2$", "$4\\,\\mathrm{m/s}^2$", "$40\\,\\mathrm{m/s}^2$"]),
        ("A $v$-$t$ graph is $+8\\,\\mathrm{m/s}$ for $3\\,\\mathrm{s}$, then $-4\\,\\mathrm{m/s}$ for $3\\,\\mathrm{s}$. Net displacement is",
         "$12\\,\\mathrm{m}$",
         "Areas: $+24\\,\\mathrm{m}$ then $-12\\,\\mathrm{m}$, so $\\Delta x=12\\,\\mathrm{m}$. Distance would be $36\\,\\mathrm{m}$.",
         ["$36\\,\\mathrm{m}$", "$0$", "$24\\,\\mathrm{m}$"]),
    ])
    _add(qs, [
        ("Use $g=10\\,\\mathrm{m/s}^2$. A stone is dropped from rest. How fast is it going after $3.0\\,\\mathrm{s}$?",
         "$30\\,\\mathrm{m/s}$ down",
         "Take down as positive: $v=0+(10)(3)=30\\,\\mathrm{m/s}$ downward.",
         ["$3\\,\\mathrm{m/s}$ down", "$15\\,\\mathrm{m/s}$ down", "$90\\,\\mathrm{m/s}$ down"]),
        ("A ball is dropped from rest and falls $45\\,\\mathrm{m}$. How long is it in the air? ($g=10\\,\\mathrm{m/s}^2$)",
         "$3.0\\,\\mathrm{s}$",
         "$\\Delta y=\\tfrac12 gt^2$ so $45=5t^2$, $t^2=9$, $t=3.0\\,\\mathrm{s}$.",
         ["$4.5\\,\\mathrm{s}$", "$9.0\\,\\mathrm{s}$", "$2.1\\,\\mathrm{s}$"]),
        ("A ball is thrown straight up at $20\\,\\mathrm{m/s}$. How high does it rise? ($g=10\\,\\mathrm{m/s}^2$)",
         "$20\\,\\mathrm{m}$",
         "At the peak $v=0$: $0=(20)^2+2(-10)\\Delta y$, so $20\\Delta y=400$ and $\\Delta y=20\\,\\mathrm{m}$.",
         ["$10\\,\\mathrm{m}$", "$40\\,\\mathrm{m}$", "$2\\,\\mathrm{m}$"]),
        ("At the highest point of a vertical toss, the acceleration of the ball is",
         "$10\\,\\mathrm{m/s}^2$ downward",
         "Gravity still pulls down. Velocity is zero for an instant; acceleration is not.",
         ["zero", "$10\\,\\mathrm{m/s}^2$ upward", "infinite"]),
        ("A pebble is thrown downward at $8\\,\\mathrm{m/s}$ from a cliff and falls for $2.0\\,\\mathrm{s}$. How far does it fall? ($g=10\\,\\mathrm{m/s}^2$)",
         "$36\\,\\mathrm{m}$",
         "Down positive: $\\Delta y=8(2)+\\tfrac12(10)(4)=16+20=36\\,\\mathrm{m}$.",
         ["$16\\,\\mathrm{m}$", "$20\\,\\mathrm{m}$", "$28\\,\\mathrm{m}$"]),
    ])
    _add(qs, [
        ("A dart is launched horizontally at $12\\,\\mathrm{m/s}$ from a $45\\,\\mathrm{m}$ ledge. How long until it hits the ground? ($g=10\\,\\mathrm{m/s}^2$)",
         "$3.0\\,\\mathrm{s}$",
         "Vertical: $45=\\tfrac12(10)t^2$, $t^2=9$, $t=3.0\\,\\mathrm{s}$. Horizontal speed does not change the fall time from rest vertically.",
         ["$3.8\\,\\mathrm{s}$", "$1.9\\,\\mathrm{s}$", "$12\\,\\mathrm{s}$"]),
        ("Using the dart above, how far from the base of the ledge does it land?",
         "$36\\,\\mathrm{m}$",
         "Range $=v_x t=(12)(3)=36\\,\\mathrm{m}$.",
         ["$45\\,\\mathrm{m}$", "$24\\,\\mathrm{m}$", "$12\\,\\mathrm{m}$"]),
        ("A soccer ball is kicked with $v_x=16\\,\\mathrm{m/s}$ and $v_y=12\\,\\mathrm{m/s}$ on level ground. Time of flight is",
         "$2.4\\,\\mathrm{s}$",
         "Time to peak is $v_y/g=12/10=1.2\\,\\mathrm{s}$. Full flight is twice that: $2.4\\,\\mathrm{s}$.",
         ["$1.2\\,\\mathrm{s}$", "$1.6\\,\\mathrm{s}$", "$12\\,\\mathrm{s}$"]),
        ("For that same kick, the range on level ground is",
         "$38.4\\,\\mathrm{m}$",
         "$R=v_x T=(16)(2.4)=38.4\\,\\mathrm{m}$.",
         ["$19.2\\,\\mathrm{m}$", "$28.8\\,\\mathrm{m}$", "$48\\,\\mathrm{m}$"]),
        ("Throughout a projectile's flight (no air), the horizontal acceleration is",
         "zero",
         "No horizontal force, so $a_x=0$ and $v_x$ is constant. $a_y=-g$.",
         ["$g$ forward", "$-g$", "equal to $a_y$"]),
    ])
    _add(qs, [
        ("A moving walkway runs at $4\\,\\mathrm{m/s}$ east. You walk $3\\,\\mathrm{m/s}$ east relative to the walkway. Your speed relative to the ground is",
         "$7\\,\\mathrm{m/s}$ east",
         "When velocities are along one line, add them: $4+3=7\\,\\mathrm{m/s}$ east.",
         ["$1\\,\\mathrm{m/s}$ east", "$4\\,\\mathrm{m/s}$ east", "$3\\,\\mathrm{m/s}$ east"]),
        ("If instead you walk $3\\,\\mathrm{m/s}$ west on that same $4\\,\\mathrm{m/s}$ east walkway, your ground velocity is",
         "$1\\,\\mathrm{m/s}$ east",
         "$v_{you,ground}=v_{you,walkway}+v_{walkway,ground}=-3+4=+1\\,\\mathrm{m/s}$ (east).",
         ["$7\\,\\mathrm{m/s}$ west", "$3\\,\\mathrm{m/s}$ west", "$0$"]),
        ("Car A goes $20\\,\\mathrm{m/s}$ north. Car B goes $12\\,\\mathrm{m/s}$ north. Velocity of A relative to B is",
         "$8\\,\\mathrm{m/s}$ north",
         "$\\vec{v}_{A/B}=\\vec{v}_A-\\vec{v}_B=20-12=8\\,\\mathrm{m/s}$ north.",
         ["$32\\,\\mathrm{m/s}$ north", "$8\\,\\mathrm{m/s}$ south", "$12\\,\\mathrm{m/s}$ north"]),
        ("Rain falls vertically at $10\\,\\mathrm{m/s}$. A bus moves $6\\,\\mathrm{m/s}$ horizontally. Speed of the rain relative to the bus is",
         "$\\sqrt{136}\\,\\mathrm{m/s}$",
         "Perpendicular components: $v=\\sqrt{10^2+6^2}=\\sqrt{136}\\,\\mathrm{m/s}$.",
         ["$16\\,\\mathrm{m/s}$", "$4\\,\\mathrm{m/s}$", "$10\\,\\mathrm{m/s}$"]),
        ("Two boats approach on a straight canal, $18\\,\\mathrm{m/s}$ east and $12\\,\\mathrm{m/s}$ west. Closing speed is",
         "$30\\,\\mathrm{m/s}$",
         "Relative speed toward each other is $18+12=30\\,\\mathrm{m/s}$.",
         ["$6\\,\\mathrm{m/s}$", "$18\\,\\mathrm{m/s}$", "$12\\,\\mathrm{m/s}$"]),
    ])
    _add(qs, [
        ("A drone's $x$-$t$ graph is a straight line from $(0,0)$ to $(6\\,\\mathrm{s},\\,18\\,\\mathrm{m})$. Average velocity during those $6\\,\\mathrm{s}$ is",
         "$3\\,\\mathrm{m/s}$",
         "$\\bar{v}=18/6=3\\,\\mathrm{m/s}$. A straight $x$-$t$ line means constant velocity.",
         ["$6\\,\\mathrm{m/s}$", "$18\\,\\mathrm{m/s}$", "$0.33\\,\\mathrm{m/s}$"]),
        ("Which quantity can be negative on a one-dimensional number line?",
         "velocity",
         "Velocity and displacement have direction (sign). Speed and distance do not.",
         ["speed", "distance", "elapsed time"]),
        ("A toy car has $a=+2\\,\\mathrm{m/s}^2$ while $v$ is already negative. What is happening?",
         "it is slowing down (speeding toward zero from the negative side)",
         "Acceleration opposite velocity means the object is slowing. Signs of $a$ and $v$ disagree.",
         ["it must be speeding up", "acceleration cannot be positive", "it is at rest"]),
        ("You need the stopping distance of a bike with known $v_0$ and constant $a<0$. The fastest equation is",
         "$0=v_0^2+2a\\Delta x$",
         "Final speed is zero, time is unknown, so the no-time equation is the tool.",
         ["$v=v_0+at$ alone, with no second step", "$F_g=mg$ only", "Bernoulli's equation"]),
        ("A $v$-$t$ triangle goes from $0$ to $12\\,\\mathrm{m/s}$ in $6\\,\\mathrm{s}$. Displacement during that interval is",
         "$36\\,\\mathrm{m}$",
         "Triangle area: $\\tfrac12(6)(12)=36\\,\\mathrm{m}$.",
         ["$72\\,\\mathrm{m}$", "$18\\,\\mathrm{m}$", "$2\\,\\mathrm{m}$"]),
        ("Dropped from rest, a nut falls $20\\,\\mathrm{m}$. Impact speed is ($g=10\\,\\mathrm{m/s}^2$)",
         "$20\\,\\mathrm{m/s}$",
         "$v^2=0+2(10)(20)=400$, so $v=20\\,\\mathrm{m/s}$ downward.",
         ["$10\\,\\mathrm{m/s}$", "$40\\,\\mathrm{m/s}$", "$\\sqrt{20}\\,\\mathrm{m/s}$"]),
        ("A ball thrown up at $15\\,\\mathrm{m/s}$ returns to the thrower's hand. Speed just before catch is",
         "$15\\,\\mathrm{m/s}$",
         "Symmetric free-fall: it leaves at $15\\,\\mathrm{m/s}$ up and returns at $15\\,\\mathrm{m/s}$ down (no air).",
         ["$0$", "$30\\,\\mathrm{m/s}$", "$7.5\\,\\mathrm{m/s}$"]),
        ("A cannonball is fired horizontally from a $80\\,\\mathrm{m}$ cliff at $25\\,\\mathrm{m/s}$. Hang time is",
         "$4.0\\,\\mathrm{s}$",
         "$80=5t^2$, $t^2=16$, $t=4.0\\,\\mathrm{s}$.",
         ["$3.2\\,\\mathrm{s}$", "$8.0\\,\\mathrm{s}$", "$2.0\\,\\mathrm{s}$"]),
        ("For that cannonball, the landing distance from the cliff base is",
         "$100\\,\\mathrm{m}$",
         "$R=(25)(4)=100\\,\\mathrm{m}$.",
         ["$80\\,\\mathrm{m}$", "$50\\,\\mathrm{m}$", "$200\\,\\mathrm{m}$"]),
        ("A kick has $v_x=20\\,\\mathrm{m/s}$, $v_y=15\\,\\mathrm{m/s}$. Maximum height is ($g=10$)",
         "$11.25\\,\\mathrm{m}$",
         "$H=v_y^2/(2g)=225/20=11.25\\,\\mathrm{m}$.",
         ["$15\\,\\mathrm{m}$", "$22.5\\,\\mathrm{m}$", "$7.5\\,\\mathrm{m}$"]),
        ("Two joggers run $4\\,\\mathrm{m/s}$ and $6\\,\\mathrm{m/s}$ east. How fast does the faster one approach a tree the slower one has already passed, relative to the slower jogger?",
         "$2\\,\\mathrm{m/s}$",
         "Relative speed along the line is $6-4=2\\,\\mathrm{m/s}$.",
         ["$10\\,\\mathrm{m/s}$", "$6\\,\\mathrm{m/s}$", "$4\\,\\mathrm{m/s}$"]),
        ("A river flows $2\\,\\mathrm{m/s}$ east. A swimmer's speed in still water is $5\\,\\mathrm{m/s}$. Maximum speed downstream is",
         "$7\\,\\mathrm{m/s}$",
         "Aim with the current: $5+2=7\\,\\mathrm{m/s}$ relative to the bank.",
         ["$5\\,\\mathrm{m/s}$", "$3\\,\\mathrm{m/s}$", "$10\\,\\mathrm{m/s}$"]),
        ("Which graph is a straight line with negative slope for an object slowing while moving in the $+x$ direction?",
         "a $v$-$t$ graph from positive $v$ down toward zero",
         "Positive $v$ decreasing means $a<0$. The $v$-$t$ slope is negative.",
         ["an $x$-$t$ graph that is a horizontal line", "an $a$-$t$ graph at $+g$", "a speed-versus-time graph that must go negative"]),
        ("A particle's acceleration is constant and nonzero. Which graph cannot be a straight horizontal line?",
         "$v$ versus $t$",
         "Constant nonzero $a$ means $v$ changes linearly with $t$, so $v$-$t$ slants. $a$-$t$ is the horizontal line.",
         ["$a$ versus $t$", "net force versus $t$ if mass is fixed", "none of the kinematic graphs"]),
        ("You throw a rock off a bridge. Compare time to fall $20\\,\\mathrm{m}$ versus the next $20\\,\\mathrm{m}$ (to $40\\,\\mathrm{m}$).",
         "the second $20\\,\\mathrm{m}$ takes less time",
         "It is already moving faster after the first $20\\,\\mathrm{m}$, so it covers the next $20\\,\\mathrm{m}$ more quickly.",
         ["equal times because $g$ is constant", "the second $20\\,\\mathrm{m}$ takes more time", "time is independent of speed"]),
        ("A skateboarder starts from rest with constant $a=3.0\\,\\mathrm{m/s}^2$ for $4.0\\,\\mathrm{s}$. How far does the board travel in those $4.0\\,\\mathrm{s}$?",
         "$24\\,\\mathrm{m}$",
         "$\\Delta x=v_0 t+\\tfrac12 at^2=0+\\tfrac12(3.0)(16)=24\\,\\mathrm{m}$.",
         ["$12\\,\\mathrm{m}$", "$48\\,\\mathrm{m}$", "$6.0\\,\\mathrm{m}$"]),
        ("AP Stretch: A ball is tossed vertically from a $15\\,\\mathrm{m}$ roof at $10\\,\\mathrm{m/s}$ upward. How long until it hits the ground $15\\,\\mathrm{m}$ below the roof? ($g=10$)",
         "$3.0\\,\\mathrm{s}$",
         "Take up positive, origin at roof: $-15=10t-5t^2$. Then $5t^2-10t-15=0$, $t^2-2t-3=0$, $(t-3)(t+1)=0$, so $t=3.0\\,\\mathrm{s}$.",
         ["$1.0\\,\\mathrm{s}$", "$2.0\\,\\mathrm{s}$", "$4.0\\,\\mathrm{s}$"]),
        ("AP Stretch: A projectile leaves the origin with $v_x=8\\,\\mathrm{m/s}$, $v_y=6\\,\\mathrm{m/s}$. What is $y$ when $x=8\\,\\mathrm{m}$? ($g=10$)",
         "$1.0\\,\\mathrm{m}$",
         "$t=x/v_x=1.0\\,\\mathrm{s}$. Then $y=6(1)-5(1)^2=1.0\\,\\mathrm{m}$.",
         ["$6.0\\,\\mathrm{m}$", "$8.0\\,\\mathrm{m}$", "$-4.0\\,\\mathrm{m}$"]),
        ("AP Stretch: Cart A moves $+9\\,\\mathrm{m/s}$ and cart B $+1\\,\\mathrm{m/s}$ on the same track, $20\\,\\mathrm{m}$ apart. How long until A catches B?",
         "$2.5\\,\\mathrm{s}$",
         "Relative speed $8\\,\\mathrm{m/s}$; time $=20/8=2.5\\,\\mathrm{s}$.",
         ["$2.0\\,\\mathrm{s}$", "$20\\,\\mathrm{s}$", "$10\\,\\mathrm{s}$"]),
        ("AP Stretch: An $x$-$t$ graph is a parabola opening upward. Which statement must be true?",
         "acceleration is positive and velocity may change sign",
         "Upward-opening $x(t)$ means $a>0$. The object can still reverse if $v$ starts negative.",
         ["velocity is always positive", "the object is at rest", "acceleration is zero"]),
        ("AP Stretch: A plane flies $200\\,\\mathrm{m/s}$ north while wind is $50\\,\\mathrm{m/s}$ west. Ground-speed magnitude is",
         "$\\sqrt{42500}\\,\\mathrm{m/s}$",
         "Perpendicular: $\\sqrt{200^2+50^2}=\\sqrt{40000+2500}=\\sqrt{42500}\\,\\mathrm{m/s}$.",
         ["$250\\,\\mathrm{m/s}$", "$150\\,\\mathrm{m/s}$", "$200\\,\\mathrm{m/s}$"]),
        ("AP Stretch: From rest, object 1 has $a=4\\,\\mathrm{m/s}^2$ and object 2 has $a=2\\,\\mathrm{m/s}^2$. The ratio of distances after the same time $t$ is",
         "$2$ to $1$",
         "$\\Delta x=\\tfrac12 at^2$, so distances scale with $a$. Ratio $4:2=2:1$.",
         ["$4$ to $1$", "$\\sqrt{2}$ to $1$", "$1$ to $1$"]),
        ("AP Stretch: A $v$-$t$ graph is a trapezoid: $v=0$ at $t=0$, $v=10$ from $t=2$ to $t=6$, then back to $0$ at $t=8$. Displacement from $0$ to $8\\,\\mathrm{s}$ is",
         "$60\\,\\mathrm{m}$",
         "Area: triangle $10$, rectangle $40$, triangle $10$, total $60\\,\\mathrm{m}$.",
         ["$80\\,\\mathrm{m}$", "$40\\,\\mathrm{m}$", "$50\\,\\mathrm{m}$"]),
        ("AP Stretch: A ball rolls off a table with speed $v$ and lands a horizontal distance $R$ away. If $v$ is doubled and table height is unchanged, the new range is",
         "$2R$",
         "Fall time depends only on height. Range $=v_x t$ doubles when $v_x$ doubles.",
         ["$4R$", "$R$", "$R/2$"]),
        ("AP Stretch: Motion is $x=6t-t^2$ (SI units) from $t=0$ to $t=6\\,\\mathrm{s}$. Average velocity over the full $6\\,\\mathrm{s}$ is",
         "$0$",
         "$x(0)=0$, $x(6)=36-36=0$, so $\\bar{v}=0/6=0$. It went out and back.",
         ["$6\\,\\mathrm{m/s}$", "$3\\,\\mathrm{m/s}$", "$-6\\,\\mathrm{m/s}$"]),
    ])
    return qs


def build_unit1():
    title = "AP Physics Unit 1: Kinematics"
    description = (
        "Algebra-based AP Physics 1 kinematics: position, velocity, acceleration, the three constant-acceleration "
        "equations, motion graphs, free fall with $g=10\\,\\mathrm{m/s}^2$, projectiles, and relative velocity — "
        "with matching graphs and fully worked examples."
    )
    concepts = [
        "Position, velocity, and acceleration",
        "Constant-acceleration equations",
        "Graphs of motion",
        "Free fall",
        "Projectile motion",
        "Relative motion",
    ]

    c1 = concept_block(
        "1. Position, velocity, and acceleration",
        [
            "Position $x$ is a number that says where an object is on a chosen line, measured from an origin you pick. "
            "If a cart is at $x=5\\,\\mathrm{m}$, it is five meters on the positive side of that origin.",
            "Displacement $\\Delta x=x_f-x_i$ is the change in position. It has a sign. Distance is how much ground "
            "was covered, always nonnegative. Walk $4\\,\\mathrm{m}$ east then $1\\,\\mathrm{m}$ west: distance $5\\,\\mathrm{m}$, displacement $+3\\,\\mathrm{m}$.",
            "Velocity tells you how fast position is changing and in which direction. Average velocity is "
            "$\\bar{v}=\\Delta x/\\Delta t$. Speed is the magnitude of velocity: how fast, with the sign stripped off.",
            "Acceleration tells you how fast velocity is changing: $\\bar{a}=\\Delta v/\\Delta t$. If velocity goes from "
            "$2\\,\\mathrm{m/s}$ to $8\\,\\mathrm{m/s}$ in $3\\,\\mathrm{s}$, then $\\bar{a}=2\\,\\mathrm{m/s}^2$.",
            "An object can have negative velocity (moving toward smaller $x$) and positive acceleration (velocity becoming "
            "less negative). Speeding up means $v$ and $a$ have the same sign; slowing down means opposite signs.",
            "These three words — position, velocity, acceleration — are the vocabulary of the entire unit. Every later "
            "equation is just a tool for connecting them when acceleration happens to be constant.",
        ],
        "Free fall, projectiles, and Newton's second law all report answers as $v$ or $a$. If you mix speed with velocity, "
        "you will get the wrong sign on every two-dimensional problem that follows.",
        "Write a tiny number line, mark $x_i$ and $x_f$, then compute $\\Delta x$ before you divide by time. Ask whether "
        "you need a signed quantity (velocity, displacement) or a magnitude (speed, distance).",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: 2 + 3 * t, 0, 4))],
                points=[(0, 2, "t=0"), (4, 14, "t=4 s")],
                xlim=(-0.5, 5), ylim=(-1, 16), xlab="t (s)", ylab="x (m)", w=320, h=260,
            ),
            "Position versus time for constant velocity $3\\,\\mathrm{m/s}$",
            "Straight $x$-$t$ line: slope is velocity. From $x=2\\,\\mathrm{m}$ to $x=14\\,\\mathrm{m}$ in $4\\,\\mathrm{s}$.",
        )
        + solved(1, "A runner goes from $x=2\\,\\mathrm{m}$ to $x=14\\,\\mathrm{m}$ in $4.0\\,\\mathrm{s}$. Find the average velocity.",
                 ["Displacement: $\\Delta x=14-2=12\\,\\mathrm{m}$.",
                  "Average velocity: $\\bar{v}=\\Delta x/\\Delta t=12/4=3\\,\\mathrm{m/s}$.",
                  "The positive sign means motion toward increasing $x$."],
                 "$3\\,\\mathrm{m/s}$", "", "Easy")
        + solved(2, "Velocity changes from $-4\\,\\mathrm{m/s}$ to $+8\\,\\mathrm{m/s}$ in $3.0\\,\\mathrm{s}$. Find average acceleration.",
                 ["$\\Delta v=8-(-4)=12\\,\\mathrm{m/s}$.",
                  "$\\bar{a}=\\Delta v/\\Delta t=12/3=4\\,\\mathrm{m/s}^2$.",
                  "Acceleration is positive even though the motion started in the negative direction."],
                 "$4\\,\\mathrm{m/s}^2$", "The object reversed direction during the interval.", "Medium")
        + solved(3, "A bee flies $6\\,\\mathrm{m}$ east, then $2\\,\\mathrm{m}$ west, in a total of $4.0\\,\\mathrm{s}$. Find distance, displacement, average speed, and average velocity.",
                 ["Distance $=6+2=8\\,\\mathrm{m}$. Displacement $=6-2=+4\\,\\mathrm{m}$ (east).",
                  "Average speed $=8/4=2\\,\\mathrm{m/s}$.",
                  "Average velocity $=4/4=+1\\,\\mathrm{m/s}$ (east).",
                  "Speed and velocity disagree because the path folded back."],
                 "distance $8\\,\\mathrm{m}$; $\\Delta x=+4\\,\\mathrm{m}$; speed $2\\,\\mathrm{m/s}$; $\\bar{v}=+1\\,\\mathrm{m/s}$",
                 "", "Hard"),
        ("Calling speed a signed number",
         "Speed cannot be negative. If your calculator shows $-3\\,\\mathrm{m/s}$, that is a velocity. Report speed as $3\\,\\mathrm{m/s}$ and say the direction separately."),
        ("Sketch the number line first",
         "Before dividing, mark start and end. That sketch makes $\\Delta x$ obvious and prevents subtracting in the wrong order."),
        [
            "I can distinguish displacement from distance and velocity from speed in one dimension.",
            "I can compute average velocity and average acceleration from a table of $x$ or $v$ versus $t$.",
            "I can tell from signs whether an object is speeding up or slowing down.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Constant-acceleration equations",
        [
            "When acceleration is constant, three algebraic equations connect $v_0$, $v$, $a$, $\\Delta x$, and $t$. "
            "Pick the equation that contains the unknown and omits the quantity you were not given.",
            "The velocity-update equation is $v=v_0+at$. It is just the definition of constant $a$, rearranged. "
            "If $v_0=5\\,\\mathrm{m/s}$, $a=2\\,\\mathrm{m/s}^2$, and $t=3\\,\\mathrm{s}$, then $v=11\\,\\mathrm{m/s}$.",
            "The position-update equation is $\\Delta x=v_0 t+\\tfrac12 at^2$. The $\\tfrac12 at^2$ piece is extra distance "
            "from speeding up (or less distance from slowing down). If you drop the $\\tfrac12$, every free-fall height will be wrong.",
            "When time is missing, use $v^2=v_0^2+2a\\Delta x$. Stopping distances and peak heights of tosses live here, "
            "because $v=0$ at the end and $t$ was never measured.",
            "A fourth cousin is $\\Delta x=\\tfrac12(v_0+v)t$, average velocity times time, valid only for constant $a$. "
            "It is handy when you know both end speeds and the clock reading.",
            "List the five symbols, tick the ones you know, circle the unknown, and choose. Units stay in the algebra: "
            "meters, seconds, and meters per second squared must be consistent before you multiply.",
        ],
        "Projectiles are just these equations used twice — once for $x$ with $a_x=0$, once for $y$ with $a_y=-g$. "
        "If the one-dimensional versions are shaky, two-dimensional motion will feel like a pile of letters.",
        "Write knowns with signs. Choose a positive direction and keep it. Then pick the equation missing the leftover variable.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", sample_curve(lambda t: 4 + 2 * t, 0, 5))],
                points=[(0, 4, "v0=4"), (5, 14, "v=14")],
                xlim=(-0.4, 6), ylim=(-1, 16), xlab="t (s)", ylab="v (m/s)", w=320, h=260,
            ),
            "Velocity versus time for $a=+2\\,\\mathrm{m/s}^2$",
            "Straight slanted $v$-$t$ line: slope is $a$. Area under the line would be $\\Delta x$.",
        )
        + solved(4, "A rover starts from rest with $a=4\\,\\mathrm{m/s}^2$. Find $v$ after $3.0\\,\\mathrm{s}$.",
                 ["Known: $v_0=0$, $a=4\\,\\mathrm{m/s}^2$, $t=3\\,\\mathrm{s}$. Unknown: $v$.",
                  "Use $v=v_0+at=0+(4)(3)=12\\,\\mathrm{m/s}$.",
                  "Units: $(\\mathrm{m/s}^2)(\\mathrm{s})=\\mathrm{m/s}$."],
                 "$12\\,\\mathrm{m/s}$", "", "Easy")
        + solved(5, "A crate sliding at $10\\,\\mathrm{m/s}$ slows at $2\\,\\mathrm{m/s}^2$. How far until it stops?",
                 ["Known: $v_0=10$, $v=0$, $a=-2$. Unknown: $\\Delta x$. Time not given.",
                  "$0=10^2+2(-2)\\Delta x$.",
                  "$0=100-4\\Delta x$, so $\\Delta x=25\\,\\mathrm{m}$."],
                 "$25\\,\\mathrm{m}$", "", "Medium")
        + solved(6, "A cart has $v_0=8\\,\\mathrm{m/s}$ and $a=-2\\,\\mathrm{m/s}^2$. Find position relative to the start after $5.0\\,\\mathrm{s}$, and say whether it turned around.",
                 ["$\\Delta x=v_0 t+\\tfrac12 at^2=8(5)+\\tfrac12(-2)(25)=40-25=15\\,\\mathrm{m}$.",
                  "Velocity at $5\\,\\mathrm{s}$: $v=8+(-2)(5)=-2\\,\\mathrm{m/s}$.",
                  "It reversed when $v=0$: $0=8-2t$ so $t=4\\,\\mathrm{s}$, which is before $5\\,\\mathrm{s}$.",
                  "So it went forward, stopped at $t=4\\,\\mathrm{s}$, and came back slightly."],
                 "$\\Delta x=+15\\,\\mathrm{m}$; yes, it reversed at $t=4\\,\\mathrm{s}$", "", "Hard"),
        ("Dropping the one-half in $\\tfrac12 at^2$",
         "The extra distance from speeding up is not $at^2$. If $v_0=0$, $\\Delta x=\\tfrac12 at^2$, which is half of what a constant-speed guess $v=at$ would suggest using $v t$."),
        ("Table of knowns before choosing a formula",
         "Five symbols, one unknown. If $t$ is missing, $v^2=v_0^2+2a\\Delta x$ is almost always the path. If $\\Delta x$ is missing and you have $t$, use $v=v_0+at$ or $\\Delta x=v_0 t+\\tfrac12 at^2$."),
        [
            "I can select the constant-acceleration equation that matches the given data.",
            "I can substitute with units and a consistent sign convention.",
            "I can find stopping distance and turnaround time from $v=0$.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Graphs of motion",
        [
            "An $x$-$t$ graph plots position against clock time. The slope of that graph is velocity. A horizontal $x$-$t$ "
            "segment means the object is standing still. A straight slant means constant velocity.",
            "A $v$-$t$ graph plots velocity against time. Its slope is acceleration. Its area (with sign) is displacement. "
            "AP Physics 1 loves asking you to read one of those two features without writing a long equation.",
            "An $a$-$t$ graph is usually a horizontal line in this unit because we study constant acceleration. The area "
            "under $a$-$t$ is the change in velocity $\\Delta v$.",
            "Curved $x$-$t$ means changing slope, hence changing velocity, hence nonzero acceleration. A parabola on $x$-$t$ "
            "matches a straight line on $v$-$t$.",
            "When $v$ is negative, the $v$-$t$ graph sits below the time axis. That area is negative displacement. "
            "Distance is the total of absolute areas.",
            "Translate every story into the graph that makes the asked quantity a slope or an area. That habit is faster "
            "than restarting from $v=v_0+at$ on every multiple-choice item.",
        ],
        "Free-fall and projectile questions are often given as graphs instead of numbers. If you can see that a $v$-$t$ "
        "triangle's area is $\\Delta x$, you already have the FRQ method.",
        "Name the axes out loud. Slope of $x$-$t$ is $v$. Slope of $v$-$t$ is $a$. Area of $v$-$t$ is $\\Delta x$.",
        lesson_figure(
            xy_graph(
                curves=[("#0f766e", [(0, 0), (3, 9), (6, 9), (8, 3)])],
                points=[(3, 9, "cruise"), (8, 3, "slow")],
                xlim=(-0.4, 9), ylim=(-1, 12), xlab="t (s)", ylab="v (m/s)", w=320, h=260,
            ),
            "A piecewise $v$-$t$ graph: speed up, cruise, then slow",
            "Area of each piece is that interval's displacement. Slope of each piece is $a$.",
        )
        + solved(7, "A $v$-$t$ graph is a horizontal line at $6\\,\\mathrm{m/s}$ for $4.0\\,\\mathrm{s}$. Find $\\Delta x$ and $a$.",
                 ["Area of the rectangle: $(6\\,\\mathrm{m/s})(4\\,\\mathrm{s})=24\\,\\mathrm{m}$.",
                  "Slope is zero, so $a=0$.",
                  "Constant velocity motion."],
                 "$\\Delta x=24\\,\\mathrm{m}$, $a=0$", "", "Easy")
        + solved(8, "Velocity rises linearly from $0$ to $10\\,\\mathrm{m/s}$ in $4.0\\,\\mathrm{s}$. Find $a$ and $\\Delta x$.",
                 ["$a=$ slope $=(10-0)/4=2.5\\,\\mathrm{m/s}^2$.",
                  "Area of the triangle: $\\tfrac12(4)(10)=20\\,\\mathrm{m}$.",
                  "Check: $\\Delta x=0+\\tfrac12(2.5)(16)=20\\,\\mathrm{m}$."],
                 "$a=2.5\\,\\mathrm{m/s}^2$, $\\Delta x=20\\,\\mathrm{m}$", "", "Medium")
        + solved(9, "A $v$-$t$ graph is $+8\\,\\mathrm{m/s}$ for $3.0\\,\\mathrm{s}$, then $-4\\,\\mathrm{m/s}$ for $3.0\\,\\mathrm{s}$. Find displacement and distance.",
                 ["First area: $+(8)(3)=+24\\,\\mathrm{m}$.",
                  "Second area: $(-4)(3)=-12\\,\\mathrm{m}$.",
                  "Displacement $=24-12=+12\\,\\mathrm{m}$.",
                  "Distance $=24+12=36\\,\\mathrm{m}$."],
                 "$\\Delta x=+12\\,\\mathrm{m}$; distance $36\\,\\mathrm{m}$", "", "Hard"),
        ("Reading height on a $v$-$t$ graph as position",
         "The height of a $v$-$t$ graph is velocity, not position. Position is recovered from area, or from an $x$-$t$ graph."),
        ("Compute geometric area with signs",
         "Split the graph into rectangles and triangles. Put a minus sign on pieces below the time axis. Add for $\\Delta x$; add absolute values for distance."),
        [
            "I can read velocity as the slope of $x$-$t$ and acceleration as the slope of $v$-$t$.",
            "I can find displacement from the signed area of a $v$-$t$ graph.",
            "I can match a motion story to the shapes of $x(t)$, $v(t)$, and $a(t)$.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Free fall",
        [
            "Free fall means the only force is gravity (we ignore air in the basic model). Near Earth, that produces a "
            "constant acceleration of magnitude $g$. In this course use $g=10\\,\\mathrm{m/s}^2$ unless a problem writes $9.8$.",
            "Choose a sign convention and keep it. Many students take up as positive, so $a=-10\\,\\mathrm{m/s}^2$. "
            "Others take down as positive when the object is only falling. Both work if you never switch mid-problem.",
            "Dropped from rest, $v_0=0$ and $\\Delta y=\\tfrac12 gt^2$ if down is positive. After $2.0\\,\\mathrm{s}$ the "
            "speed is $20\\,\\mathrm{m/s}$ and the fall distance is $20\\,\\mathrm{m}$.",
            "Thrown upward, velocity is zero for an instant at the peak, but acceleration is still $g$ downward. "
            "That single sentence is one of the most tested ideas on AP Physics 1.",
            "Time to the peak is $t_{\\mathrm{up}}=v_0/g$ when up is positive. Height is $H=v_0^2/(2g)$. A $20\\,\\mathrm{m/s}$ "
            "toss rises for $2.0\\,\\mathrm{s}$ and reaches $20\\,\\mathrm{m}$.",
            "Coming down from the same height takes the same time as going up (no air). Impact speed equals launch speed "
            "if you return to the same vertical position.",
        ],
        "Projectiles are free fall in the vertical direction glued to constant-velocity motion horizontally. "
        "Get vertical free fall right, and the next lesson is mostly bookkeeping.",
        "Write $a=\\pm 10\\,\\mathrm{m/s}^2$ with your chosen sign before substituting. At the peak, set $v_y=0$, never $a=0$.",
        lesson_figure(
            xy_graph(
                curves=[("#b45309", sample_curve(lambda t: 20 * t - 5 * t * t, 0, 4))],
                points=[(0, 0, "throw"), (2, 20, "peak"), (4, 0, "catch")],
                xlim=(-0.3, 5), ylim=(-4, 24), xlab="t (s)", ylab="y (m)", w=320, h=260,
            ),
            "Height versus time for a $20\\,\\mathrm{m/s}$ upward toss ($g=10$)",
            "Parabola. Peak at $t=2\\,\\mathrm{s}$, $y=20\\,\\mathrm{m}$. Acceleration is still downward at the peak.",
        )
        + solved(10, "A stone is dropped from rest. Find its speed after $3.0\\,\\mathrm{s}$ ($g=10\\,\\mathrm{m/s}^2$).",
                 ["Take down as positive: $v_0=0$, $a=10\\,\\mathrm{m/s}^2$.",
                  "$v=0+(10)(3)=30\\,\\mathrm{m/s}$ downward.",
                  "Distance fallen: $\\Delta y=\\tfrac12(10)(9)=45\\,\\mathrm{m}$ if you also need it."],
                 "$30\\,\\mathrm{m/s}$ down", "", "Easy")
        + solved(11, "A ball is thrown straight up at $20\\,\\mathrm{m/s}$. Find time to the peak and maximum height.",
                 ["Up positive: $a=-10\\,\\mathrm{m/s}^2$. At peak $v=0$.",
                  "$0=20-10t$ so $t=2.0\\,\\mathrm{s}$.",
                  "$H=v_0^2/(2g)=400/20=20\\,\\mathrm{m}$.",
                  "Or $\\Delta y=20(2)+\\tfrac12(-10)(4)=40-20=20\\,\\mathrm{m}$."],
                 "$2.0\\,\\mathrm{s}$; $20\\,\\mathrm{m}$", "", "Medium")
        + solved(12, "From a $45\\,\\mathrm{m}$ roof a ball is thrown downward at $10\\,\\mathrm{m/s}$. Find impact speed and time of flight ($g=10$).",
                 ["Down positive: $v_0=10$, $a=10$, $\\Delta y=45$.",
                  "$v^2=10^2+2(10)(45)=100+900=1000$, so $v=\\sqrt{1000}=10\\sqrt{10}\\,\\mathrm{m/s}$.",
                  "Time: $45=10t+5t^2$, so $t^2+2t-9=0$.",
                  "Positive root $t=-1+\\sqrt{10}\\approx 2.16\\,\\mathrm{s}$."],
                 "$v=10\\sqrt{10}\\,\\mathrm{m/s}$ down; $t=-1+\\sqrt{10}\\,\\mathrm{s}$",
                 "The quadratic is required because $v_0\\neq 0$.", "Hard"),
        ("Setting acceleration to zero at the top",
         "Velocity is zero at the peak. Acceleration is still $g$ down because gravity did not switch off. A force diagram at the top still shows $F_g$ down."),
        ("Pick up-positive or down-positive once",
         "Write $a=\\pm 10$ on the paper before the first substitution. If the object goes up and then down, up-positive is usually cleaner."),
        [
            "I can use $g=10\\,\\mathrm{m/s}^2$ with a consistent sign in free-fall algebra.",
            "I can find peak time and height for a vertical toss.",
            "I can explain why acceleration is not zero at the highest point.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Projectile motion",
        [
            "A projectile is an object in free fall that also has a horizontal velocity. We split the motion into two "
            "independent one-dimensional problems that share the same clock $t$.",
            "Horizontally there is no force (no air), so $a_x=0$ and $x=v_x t$. Vertically the acceleration is $g$ downward, "
            "so $y$ uses the free-fall equations. Never mix an $x$ number into a $y$ equation except through $t$.",
            "Launched horizontally from a height $h$, $v_{0y}=0$. Fall time is $t=\\sqrt{2h/g}$. Range is $R=v_x t$. "
            "From $h=45\\,\\mathrm{m}$ with $v_x=12\\,\\mathrm{m/s}$, $t=3.0\\,\\mathrm{s}$ and $R=36\\,\\mathrm{m}$.",
            "Launched at an angle, $v_x=v\\cos\\theta$ and $v_y=v\\sin\\theta$. On level ground the time of flight is "
            "$T=2v_y/g$ and the range is $R=v_x T$. Peak height is still $H=v_y^2/(2g)$.",
            "The trajectory $y$ versus $x$ is a parabola. The launch point is the start of that curve. At the peak, "
            "$v_y=0$ but $v_x$ is unchanged, so the velocity is horizontal, not zero.",
            "AP problems love a cliff: the landing is not at launch height, so $T=2v_y/g$ is illegal. Solve the vertical "
            "quadratic for $t$, then multiply by $v_x$.",
        ],
        "Relative motion and later circular-motion comparisons still use this split: perpendicular components do not "
        "feed each other. Learning the split here pays off for the rest of the course.",
        "Draw $v_x$ and $v_y$ at launch. Solve time from the vertical story, then find $x$ from $v_x t$.",
        lesson_figure(
            xy_graph(
                curves=[("#7c3aed", sample_curve(lambda x: 0.75 * x - (x * x) / 80.0, 0, 60))],
                points=[(0, 0, "launch"), (30, 11.25, "peak"), (60, 0, "land")],
                xlim=(-4, 68), ylim=(-2, 16), xlab="x (m)", ylab="y (m)", w=340, h=240,
            ),
            "Trajectory for $v_x=20\\,\\mathrm{m/s}$, $v_y=15\\,\\mathrm{m/s}$ ($g=10$)",
            "Parabola from the marked launch point. Peak at $x=30\\,\\mathrm{m}$, $y=11.25\\,\\mathrm{m}$; range $60\\,\\mathrm{m}$.",
        )
        + solved(13, "A dart is launched horizontally at $15\\,\\mathrm{m/s}$ from a $20\\,\\mathrm{m}$ ledge. Find hang time ($g=10$).",
                 ["Vertical: $v_{0y}=0$, $\\Delta y=20\\,\\mathrm{m}$ down.",
                  "$20=\\tfrac12(10)t^2=5t^2$, so $t^2=4$ and $t=2.0\\,\\mathrm{s}$.",
                  "Horizontal speed is not needed for hang time from rest vertically."],
                 "$2.0\\,\\mathrm{s}$", "", "Easy")
        + solved(14, "For that dart, how far from the base does it land, and what is the impact $v_y$?",
                 ["$R=v_x t=(15)(2)=30\\,\\mathrm{m}$.",
                  "$v_y=0+(10)(2)=20\\,\\mathrm{m/s}$ down.",
                  "Impact speed $\\sqrt{15^2+20^2}=25\\,\\mathrm{m/s}$."],
                 "$R=30\\,\\mathrm{m}$; $v_y=20\\,\\mathrm{m/s}$ down; speed $25\\,\\mathrm{m/s}$", "", "Medium")
        + solved(15, "A kick on level ground has $v=25\\,\\mathrm{m/s}$ with $\\cos\\theta=4/5$ and $\\sin\\theta=3/5$. Find time of flight, range, and max height ($g=10$).",
                 ["$v_x=20\\,\\mathrm{m/s}$, $v_y=15\\,\\mathrm{m/s}$.",
                  "$T=2v_y/g=30/10=3.0\\,\\mathrm{s}$.",
                  "$R=(20)(3)=60\\,\\mathrm{m}$.",
                  "$H=v_y^2/(2g)=225/20=11.25\\,\\mathrm{m}$."],
                 "$T=3.0\\,\\mathrm{s}$, $R=60\\,\\mathrm{m}$, $H=11.25\\,\\mathrm{m}$", "", "Hard"),
        ("Using $T=2v_y/g$ off a cliff",
         "That formula assumes you land at the same height you started. From a ledge, solve $\\Delta y=v_y t-\\tfrac12 gt^2$ for the physical positive $t$.",),
        ("Share one clock between $x$ and $y$",
         "Find $t$ from the direction that has the extra information (usually $y$). Then $x=v_x t$. Do not invent two different times."),
        [
            "I can split a projectile into $a_x=0$ and $a_y=-g$ sharing one time $t$.",
            "I can find hang time from a horizontal launch off a ledge.",
            "I can compute range and peak height from $v_x$ and $v_y$ on level ground.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Relative motion",
        [
            "Relative velocity answers “how does A look from B?” In one dimension you subtract: "
            "$\\vec{v}_{A/B}=\\vec{v}_A-\\vec{v}_B$. If A is at $20\\,\\mathrm{m/s}$ east and B at $12\\,\\mathrm{m/s}$ east, A is only $8\\,\\mathrm{m/s}$ east relative to B.",
            "When you walk on a moving walkway, the ground velocity is the walkway velocity plus your velocity relative "
            "to the walkway, added as vectors along the line. Walk $+3\\,\\mathrm{m/s}$ on a $+4\\,\\mathrm{m/s}$ belt: $+7\\,\\mathrm{m/s}$ relative to the floor.",
            "Walking against the belt subtracts. The same $3\\,\\mathrm{m/s}$ west on a $4\\,\\mathrm{m/s}$ east belt is $+1\\,\\mathrm{m/s}$ east on the ground.",
            "In two dimensions, add perpendicular components with the Pythagorean theorem. Rain falling at $10\\,\\mathrm{m/s}$ "
            "and a bus moving at $6\\,\\mathrm{m/s}$ give a relative speed $\\sqrt{10^2+6^2}=\\sqrt{136}\\,\\mathrm{m/s}$.",
            "River problems use the same addition: the water's velocity plus the swimmer's velocity relative to the water "
            "equals velocity relative to the bank. Aiming upstream can cancel the current's sideways piece.",
            "Relative motion does not change accelerations that come from real forces in an inertial frame. It only "
            "changes how you describe velocities. Keep the frames named: “relative to the ground,” “relative to the cart.”",
        ],
        "Later, center-of-mass frames for collisions are just a careful relative-velocity story. Getting the subtraction "
        "right now prevents sign errors in Unit 4.",
        "Name three objects: A, B, and the ground. Write $\\vec{v}_{A/\\mathrm{g}}=\\vec{v}_{A/B}+\\vec{v}_{B/\\mathrm{g}}$ and plug in signs.",
        lesson_figure(
            _rel_arrows(),
            "Walker on a moving walkway",
            "Add collinear velocities: $3\\,\\mathrm{m/s}$ on the belt plus $4\\,\\mathrm{m/s}$ belt gives $7\\,\\mathrm{m/s}$ on the ground.",
        )
        + solved(16, "A walkway moves $4\\,\\mathrm{m/s}$ east. You walk $3\\,\\mathrm{m/s}$ east on it. Find your ground speed.",
                 ["$v_{you,g}=v_{you,w}+v_{w,g}$.",
                  "$3+4=7\\,\\mathrm{m/s}$ east.",
                  "Same direction, so the speeds add."],
                 "$7\\,\\mathrm{m/s}$ east", "", "Easy")
        + solved(17, "Train A moves $22\\,\\mathrm{m/s}$ north; train B moves $10\\,\\mathrm{m/s}$ south on a parallel track. Find velocity of A relative to B.",
                 ["Take north as positive: $v_A=+22$, $v_B=-10$.",
                  "$v_{A/B}=v_A-v_B=22-(-10)=32\\,\\mathrm{m/s}$ north.",
                  "They close at $32\\,\\mathrm{m/s}$."],
                 "$32\\,\\mathrm{m/s}$ north", "", "Medium")
        + solved(18, "A river flows $3\\,\\mathrm{m/s}$ east. A boat's speed in still water is $5\\,\\mathrm{m/s}$. Find the speed across to a due-north dock, and the heading relative to the water.",
                 ["To go due north, the east components must cancel: boat must have $3\\,\\mathrm{m/s}$ west relative to water.",
                  "North component: $\\sqrt{5^2-3^2}=4\\,\\mathrm{m/s}$. That is the crossing speed relative to the bank.",
                  "The heading is upstream of north, a $3$-$4$-$5$ right triangle.",
                  "Time to cross a $40\\,\\mathrm{m}$ river would be $40/4=10\\,\\mathrm{s}$."],
                 "crossing speed $4\\,\\mathrm{m/s}$ north; aim with a $3$-$4$-$5$ upstream component",
                 "", "Hard"),
        ("Adding speeds that point opposite ways as if they were both positive",
         "Draw arrows. Opposite directions subtract. Closing speed of two oncoming cars is the sum of their ground speeds."),
        ("Label every velocity with two subscripts",
         "Write $v_{\\text{rain, bus}}$ not just “$10$.” The second name is the frame. That habit kills most relative-motion errors."),
        [
            "I can add collinear velocities for walkways, trains, and rivers.",
            "I can subtract to find $\\vec{v}_{A/B}$.",
            "I can combine perpendicular velocity components with $v=\\sqrt{v_x^2+v_y^2}$.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Force and Translational Dynamics
# ===========================================================================

def _u2_questions():
    qs = []
    _add(qs, [
        ("Newton's first law says that if the net force on an object is zero, the object",
         "keeps constant velocity (which may be zero)",
         "Inertia: no net force means no change in velocity. Rest is just the special case $v=0$.",
         ["must be at rest", "must speed up", "must travel in a circle"]),
        ("A hockey puck slides at constant $8\\,\\mathrm{m/s}$ on ideal ice. The net force on the puck is",
         "$0$",
         "Constant velocity means $\\vec{a}=0$, so $\\vec{F}_{\\mathrm{net}}=m\\vec{a}=0$.",
         ["$8\\,\\mathrm{N}$ forward", "equal to its weight", "equal to $mv$"]),
        ("A $2\\,\\mathrm{kg}$ book sits still on a table. The table's normal force has magnitude",
         "$20\\,\\mathrm{N}$",
         "Weight $mg=20\\,\\mathrm{N}$ down. At rest, $N=20\\,\\mathrm{N}$ up so $F_{\\mathrm{net}}=0$.",
         ["$2\\,\\mathrm{N}$", "$10\\,\\mathrm{N}$", "$0$"]),
        ("You are a passenger in a car that brakes hard. You lurch forward relative to the seat because",
         "your body tends to keep its previous velocity (inertia)",
         "No mysterious forward force on you. The car slowed; you had not yet.",
         ["a large forward force appears", "gravity reversed", "friction disappeared on the Earth"]),
        ("Which pair can be a Newton's first-law situation?",
         "a crate pulled right by $12\\,\\mathrm{N}$ with $12\\,\\mathrm{N}$ of friction left, moving at constant $3\\,\\mathrm{m/s}$",
         "Net force is zero, so velocity is constant — including a nonzero constant velocity.",
         ["any object that is moving", "only objects with $v=0$", "an object with a single unbalanced force"]),
    ])
    _add(qs, [
        ("Newton's second law is $\\vec{F}_{\\mathrm{net}}=m\\vec{a}$. Net force means",
         "the vector sum of all forces on that one object",
         "Add every force that acts on the object whose mass you wrote. Do not include forces it exerts on others.",
         ["the largest force only", "weight always", "the force from the last thing it touched"]),
        ("A $5\\,\\mathrm{kg}$ sled has $F_{\\mathrm{net}}=20\\,\\mathrm{N}$ east. Its acceleration is",
         "$4\\,\\mathrm{m/s}^2$ east",
         "$a=F/m=20/5=4\\,\\mathrm{m/s}^2$ in the net-force direction.",
         ["$100\\,\\mathrm{m/s}^2$ east", "$0.25\\,\\mathrm{m/s}^2$ east", "$20\\,\\mathrm{m/s}^2$ east"]),
        ("A $3\\,\\mathrm{kg}$ box is pulled right with $18\\,\\mathrm{N}$ while friction is $6\\,\\mathrm{N}$ left. Acceleration is",
         "$4\\,\\mathrm{m/s}^2$ right",
         "$F_{\\mathrm{net}}=18-6=12\\,\\mathrm{N}$, $a=12/3=4\\,\\mathrm{m/s}^2$ right.",
         ["$6\\,\\mathrm{m/s}^2$ right", "$8\\,\\mathrm{m/s}^2$ right", "$2\\,\\mathrm{m/s}^2$ right"]),
        ("Mass is $4\\,\\mathrm{kg}$ and $a=3\\,\\mathrm{m/s}^2$ upward in an elevator. The net force is",
         "$12\\,\\mathrm{N}$ up",
         "$F_{\\mathrm{net}}=ma=12\\,\\mathrm{N}$ upward. That net force is $T-mg$, not $T$ alone.",
         ["$40\\,\\mathrm{N}$ up", "$12\\,\\mathrm{N}$ down", "$4\\,\\mathrm{N}$ up"]),
        ("If you double the net force on a cart and also double its mass, the acceleration",
         "stays the same",
         "$a=F/m$ is unchanged if $F$ and $m$ scale by the same factor.",
         ["doubles", "halves", "becomes four times larger"]),
    ])
    _add(qs, [
        ("Newton's third law says forces always come in pairs that are",
         "equal in magnitude, opposite in direction, and on two different objects",
         "If A pushes B, B pushes A with the same strength the other way. They do not cancel because they do not act on the same free-body diagram.",
         ["both on the same object so they cancel", "unequal if one object is heavier", "only present during collisions"]),
        ("A $60\\,\\mathrm{kg}$ student stands on Earth. The student-Earth gravity pair has magnitude",
         "$600\\,\\mathrm{N}$",
         "Earth pulls the student $600\\,\\mathrm{N}$ down; the student pulls Earth $600\\,\\mathrm{N}$ up. Same magnitude.",
         ["$60\\,\\mathrm{N}$", "$6\\,\\mathrm{N}$", "$0$ because Earth is huge"]),
        ("A bat hits a ball. The force of the bat on the ball compared with the force of the ball on the bat is",
         "equal in magnitude and opposite in direction",
         "Third-law pair during the contact. The ball accelerates more because its mass is smaller ($a=F/m$).",
         ["larger on the ball because it flies away", "larger on the bat because the batter is strong", "zero on the bat"]),
        ("Why don't a third-law pair cancel on a free-body diagram of block A?",
         "the partner force acts on block B, not on A",
         "A free-body diagram includes only forces on that one object.",
         ["they have different magnitudes", "one is a fake force", "they last different times"]),
        ("A box pushes down on a table with $50\\,\\mathrm{N}$. The third-law partner is",
         "the table pushing up on the box with $50\\,\\mathrm{N}$",
         "Partner of “box on table” is “table on box.” Weight's partner is the box pulling the Earth, not the normal force.",
         ["Earth pulling the box down with $50\\,\\mathrm{N}$", "friction on the box", "air drag"]),
    ])
    _add(qs, [
        ("Kinetic friction on a sliding object has magnitude $f_k=\\mu_k N$. If $\\mu_k=0.20$ and $N=50\\,\\mathrm{N}$, then $f_k$ is",
         "$10\\,\\mathrm{N}$",
         "$f_k=(0.20)(50)=10\\,\\mathrm{N}$, opposite the velocity.",
         ["$50\\,\\mathrm{N}$", "$0.20\\,\\mathrm{N}$", "$250\\,\\mathrm{N}$"]),
        ("Static friction can be any value up to $\\mu_s N$. A $4\\,\\mathrm{kg}$ block needs $8\\,\\mathrm{N}$ to start moving. $\\mu_s$ is at least",
         "$0.20$",
         "$N=mg=40\\,\\mathrm{N}$. At the breaking point $f_s=\\mu_s N=8$, so $\\mu_s=8/40=0.20$.",
         ["$2.0$", "$0.80$", "$8$"]),
        ("A $5\\,\\mathrm{kg}$ crate is pulled horizontally at constant speed with $15\\,\\mathrm{N}$. $\\mu_k$ is",
         "$0.30$",
         "Constant speed: $f_k=15\\,\\mathrm{N}$ and $N=50\\,\\mathrm{N}$, so $\\mu_k=15/50=0.30$.",
         ["$0.15$", "$3.0$", "$15$"]),
        ("Drag force from air grows with speed and always",
         "opposes the velocity relative to the air",
         "Drag is a contact force with the fluid, opposite the motion through that fluid. Terminal speed is when drag (+buoyancy) balances weight.",
         ["points downward always", "is constant like kinetic friction", "is $\\mu N$"]),
        ("On level ground, doubling the weight of a sliding box (same $\\mu_k$) doubles $f_k$ because",
         "$N$ doubles, and $f_k=\\mu_k N$",
         "Normal force matches the larger weight. $\\mu_k$ is a property of the surfaces, not the mass by itself.",
         ["mass appears in $f=\\mu m$ with no $g$", "friction is always $10\\,\\mathrm{N}$", "drag doubled"]),
    ])
    _add(qs, [
        ("A block sits on a $30^\\circ$ frictionless incline. The component of weight down the slope is",
         "$mg\\sin 30^\\circ=0.5\\,mg$",
         "Tilt the axes: $mg\\sin\\theta$ down the ramp, $mg\\cos\\theta$ into the ramp (canceled by $N$).",
         ["$mg\\cos 30^\\circ$", "$mg$", "$0$"]),
        ("On a frictionless incline with $\\sin\\theta=0.6$, a $2\\,\\mathrm{kg}$ block's acceleration down the slope is ($g=10$)",
         "$6\\,\\mathrm{m/s}^2$",
         "$a=g\\sin\\theta=10(0.6)=6\\,\\mathrm{m/s}^2$. Mass cancels.",
         ["$10\\,\\mathrm{m/s}^2$", "$12\\,\\mathrm{m/s}^2$", "$4\\,\\mathrm{m/s}^2$"]),
        ("For that $2\\,\\mathrm{kg}$ block, if $\\cos\\theta=0.8$, the normal force is",
         "$16\\,\\mathrm{N}$",
         "$N=mg\\cos\\theta=20(0.8)=16\\,\\mathrm{N}$, not equal to the full weight.",
         ["$20\\,\\mathrm{N}$", "$12\\,\\mathrm{N}$", "$8\\,\\mathrm{N}$"]),
        ("A $5\\,\\mathrm{kg}$ box on a rough $37^\\circ$ ramp ($\\sin=3/5$, $\\cos=4/5$) has $\\mu_k=0.25$. $f_k$ is",
         "$10\\,\\mathrm{N}$",
         "$N=mg\\cos\\theta=50(0.8)=40\\,\\mathrm{N}$, $f_k=0.25(40)=10\\,\\mathrm{N}$ up the ramp if sliding down.",
         ["$12.5\\,\\mathrm{N}$", "$40\\,\\mathrm{N}$", "$7.5\\,\\mathrm{N}$"]),
        ("Net force down that same rough ramp is then",
         "$20\\,\\mathrm{N}$",
         "$mg\\sin\\theta=50(0.6)=30\\,\\mathrm{N}$ down; friction $10\\,\\mathrm{N}$ up; net $20\\,\\mathrm{N}$ down. $a=4\\,\\mathrm{m/s}^2$.",
         ["$30\\,\\mathrm{N}$", "$10\\,\\mathrm{N}$", "$40\\,\\mathrm{N}$"]),
    ])
    _add(qs, [
        ("Two blocks are tied by a string and pulled on frictionless ice by $F$ on the front block. The string tension is",
         "less than $F$ (it only accelerates the rear block)",
         "The front block feels $F$ forward and $T$ back. Only $T$ pulls the rear mass.",
         ["equal to $F$ always", "greater than $F$", "zero if the string is light"]),
        ("Atwood: masses $3\\,\\mathrm{kg}$ and $5\\,\\mathrm{kg}$ over a light frictionless pulley. Acceleration is ($g=10$)",
         "$2.5\\,\\mathrm{m/s}^2$",
         "$a=(5-3)g/(5+3)=20/8=2.5\\,\\mathrm{m/s}^2$.",
         ["$10\\,\\mathrm{m/s}^2$", "$4\\,\\mathrm{m/s}^2$", "$1.25\\,\\mathrm{m/s}^2$"]),
        ("Tension in that Atwood string is",
         "$37.5\\,\\mathrm{N}$",
         "$T=2m_1 m_2 g/(m_1+m_2)=2(3)(5)(10)/8=37.5\\,\\mathrm{N}$. Check: $5\\,\\mathrm{kg}$ side $mg-T=ma\\Rightarrow 50-T=12.5$, $T=37.5\\,\\mathrm{N}$.",
         ["$50\\,\\mathrm{N}$", "$30\\,\\mathrm{N}$", "$80\\,\\mathrm{N}$"]),
        ("Treating two stuck crates as one system of mass $8\\,\\mathrm{kg}$ pulled by $24\\,\\mathrm{N}$ (frictionless) gives $a=$",
         "$3\\,\\mathrm{m/s}^2$",
         "Internal tension cancels in the system. $a=24/8=3\\,\\mathrm{m/s}^2$ for both.",
         ["$24\\,\\mathrm{m/s}^2$", "$8\\,\\mathrm{m/s}^2$", "$0$"]),
        ("A $2\\,\\mathrm{kg}$ and $6\\,\\mathrm{kg}$ block are pushed by $16\\,\\mathrm{N}$ on frictionless ice, $2\\,\\mathrm{kg}$ in front. Force of $6\\,\\mathrm{kg}$ on $2\\,\\mathrm{kg}$ is",
         "$4\\,\\mathrm{N}$",
         "System $a=16/8=2\\,\\mathrm{m/s}^2$. Front mass: $F_{\\mathrm{contact}}=m_f a=4\\,\\mathrm{N}$.",
         ["$16\\,\\mathrm{N}$", "$12\\,\\mathrm{N}$", "$8\\,\\mathrm{N}$"]),
    ])
    _add(qs, [
        ("A $4\\,\\mathrm{kg}$ object has forces $10\\,\\mathrm{N}$ east and $6\\,\\mathrm{N}$ west. Acceleration magnitude is",
         "$1\\,\\mathrm{m/s}^2$",
         "$F_{\\mathrm{net}}=4\\,\\mathrm{N}$, $a=4/4=1\\,\\mathrm{m/s}^2$.",
         ["$4\\,\\mathrm{m/s}^2$", "$2.5\\,\\mathrm{m/s}^2$", "$16\\,\\mathrm{m/s}^2$"]),
        ("If net force is zero, which quantity must be constant?",
         "velocity",
         "First law / second law with $a=0$. Position can still change; acceleration is zero.",
         ["position", "kinetic energy if it is moving in a circle", "none; it must stop"]),
        ("A scale in an elevator reads $48\\,\\mathrm{N}$ for a $4\\,\\mathrm{kg}$ backpack. The elevator's acceleration is ($g=10$)",
         "$2\\,\\mathrm{m/s}^2$ up",
         "Reading is $N$. $N-mg=ma\\Rightarrow 48-40=4a$, $a=2\\,\\mathrm{m/s}^2$ up.",
         ["$2\\,\\mathrm{m/s}^2$ down", "$12\\,\\mathrm{m/s}^2$ up", "$0$"]),
        ("Pushing a wall with $40\\,\\mathrm{N}$, the wall pushes you with",
         "$40\\,\\mathrm{N}$",
         "Third law. Whether you move depends on other forces on you (friction, etc.).",
         ["$0$ if the wall does not move", "$40\\,\\mathrm{N}$ times the wall's mass", "less than $40\\,\\mathrm{N}$"]),
        ("A $10\\,\\mathrm{kg}$ sled on level snow has $\\mu_k=0.05$. Pulling horizontally, the force needed for constant speed is",
         "$5\\,\\mathrm{N}$",
         "$N=100\\,\\mathrm{N}$, $f_k=5\\,\\mathrm{N}$. Match it for $a=0$.",
         ["$10\\,\\mathrm{N}$", "$50\\,\\mathrm{N}$", "$0.05\\,\\mathrm{N}$"]),
        ("On a frictionless $30^\\circ$ ramp, time to slide $20\\,\\mathrm{m}$ from rest is ($g=10$, $\\sin 30=1/2$)",
         "$2.8\\,\\mathrm{s}$ approximately, exactly $\\sqrt{8}\\,\\mathrm{s}$",
         "$a=5\\,\\mathrm{m/s}^2$, $20=\\tfrac12(5)t^2$, $t^2=8$, $t=\\sqrt{8}=2\\sqrt{2}\\,\\mathrm{s}$.",
         ["$2.0\\,\\mathrm{s}$", "$4.0\\,\\mathrm{s}$", "$8.0\\,\\mathrm{s}$"]),
        ("Two masses $m$ and $2m$ hang on an Atwood machine. Acceleration is",
         "$g/3$",
         "$a=(2m-m)g/(3m)=g/3$.",
         ["$g$", "$g/2$", "$2g/3$"]),
        ("A $3\\,\\mathrm{kg}$ block and $5\\,\\mathrm{kg}$ block connected by a string are pulled by $24\\,\\mathrm{N}$ on frictionless ice ($5\\,\\mathrm{kg}$ in front). Tension is",
         "$9\\,\\mathrm{N}$",
         "$a=24/8=3\\,\\mathrm{m/s}^2$. Rear: $T=3(3)=9\\,\\mathrm{N}$.",
         ["$24\\,\\mathrm{N}$", "$15\\,\\mathrm{N}$", "$8\\,\\mathrm{N}$"]),
        ("True or false as a third-law statement: “weight and normal force are always a third-law pair.”",
         "false",
         "They can be equal on a resting horizontal table, but they act on the same object and are different interactions (gravity vs contact).",
         ["true always", "true only in elevators", "true if friction is zero"]),
        ("A $6\\,\\mathrm{kg}$ object has $a=2\\,\\mathrm{m/s}^2$. If a $10\\,\\mathrm{N}$ drag appears opposite $v$, the new net force needed to keep that $a$ is",
         "$22\\,\\mathrm{N}$ in the $a$ direction",
         "Originally $F_{\\mathrm{net}}=12\\,\\mathrm{N}$. To keep $a$, applied force must overcome the extra $10\\,\\mathrm{N}$ of drag: $22\\,\\mathrm{N}$ if drag is the new extra resistance.",
         ["$12\\,\\mathrm{N}$", "$10\\,\\mathrm{N}$", "$2\\,\\mathrm{N}$"]),
        ("Which free-body diagram is correct for a box sliding down a rough ramp?",
         "$F_g$ straight down, $N$ perpendicular to the ramp, $f$ up the ramp",
         "Weight is vertical. Normal is perpendicular to the surface. Kinetic friction opposes sliding, so up the ramp.",
         ["$F_g$ parallel to the ramp only", "$N$ vertical", "friction down the ramp if it is sliding down"]),
        ("A $1\\,\\mathrm{kg}$ hanging mass pulls a $4\\,\\mathrm{kg}$ cart by a string over a light pulley (table frictionless). Acceleration is ($g=10$)",
         "$2\\,\\mathrm{m/s}^2$",
         "$a=m_h g/(m_h+m_c)=10/5=2\\,\\mathrm{m/s}^2$.",
         ["$10\\,\\mathrm{m/s}^2$", "$8\\,\\mathrm{m/s}^2$", "$2.5\\,\\mathrm{m/s}^2$"]),
        ("Tension in that string is",
         "$8\\,\\mathrm{N}$",
         "Cart: $T=4a=8\\,\\mathrm{N}$. Hang: $10-T=2$, $T=8\\,\\mathrm{N}$.",
         ["$10\\,\\mathrm{N}$", "$4\\,\\mathrm{N}$", "$2\\,\\mathrm{N}$"]),
        ("If the table for that cart has $\\mu_k=0.1$, the new acceleration is",
         "$1.2\\,\\mathrm{m/s}^2$",
         "Friction on cart $f=0.1(40)=4\\,\\mathrm{N}$. $10-4=(1+4)a$, $6=5a$, $a=1.2\\,\\mathrm{m/s}^2$.",
         ["$2\\,\\mathrm{m/s}^2$", "$0.8\\,\\mathrm{m/s}^2$", "$6\\,\\mathrm{m/s}^2$"]),
        ("A $10\\,\\mathrm{kg}$ crate is shoved with $40\\,\\mathrm{N}$ on level rough floor ($\\mu_k=0.20$, $g=10$). Its acceleration is",
         "$2.0\\,\\mathrm{m/s}^2$",
         "$N=mg=100\\,\\mathrm{N}$, $f_k=20\\,\\mathrm{N}$. Net force $40-20=20\\,\\mathrm{N}$, so $a=20/10=2.0\\,\\mathrm{m/s}^2$.",
         ["$4.0\\,\\mathrm{m/s}^2$", "$6.0\\,\\mathrm{m/s}^2$", "$0.20\\,\\mathrm{m/s}^2$"]),
        ("On ice ($\\mu=0$), a $4.0\\,\\mathrm{kg}$ box on a $30^\\circ$ ramp has acceleration down the slope ($g=10$, $\\sin 30^\\circ=1/2$)",
         "$5.0\\,\\mathrm{m/s}^2$",
         "$a=g\\sin\\theta=5.0\\,\\mathrm{m/s}^2$. The mass cancels in $mg\\sin\\theta=ma$.",
         ["$10\\,\\mathrm{m/s}^2$", "$8.7\\,\\mathrm{m/s}^2$", "$2.0\\,\\mathrm{m/s}^2$"]),
        ("AP Stretch: A $5\\,\\mathrm{kg}$ block on a rough horizontal floor ($\\mu_s=0.4$, $\\mu_k=0.3$) is pulled with $15\\,\\mathrm{N}$. What happens? ($g=10$)",
         "it stays at rest; static friction is $15\\,\\mathrm{N}$",
         "$f_{s,\\max}=0.4(50)=20\\,\\mathrm{N}$. Applied $15\\,\\mathrm{N}<20\\,\\mathrm{N}$, so it does not start. Static friction matches $15\\,\\mathrm{N}$.",
         ["it accelerates at $3\\,\\mathrm{m/s}^2$", "kinetic friction is $15\\,\\mathrm{N}$", "it moves at constant speed"]),
        ("AP Stretch: Elevator of mass $M$ accelerates up at $g/5$. The cable tension is",
         "$6Mg/5$",
         "$T-Mg=M(g/5)$, so $T=6Mg/5$.",
         ["$Mg$", "$Mg/5$", "$4Mg/5$"]),
        ("AP Stretch: Two identical masses $m$ connected by a string, one on a frictionless table, one hanging. Acceleration of the pair is",
         "$g/2$",
         "$a=mg/(2m)=g/2$.",
         ["$g$", "$2g$", "$g/4$"]),
        ("AP Stretch: A $6.0\\,\\mathrm{kg}$ crate on a level floor ($\\mu_s=0.40$, $\\mu_k=0.25$) is pulled horizontally with $30\\,\\mathrm{N}$ ($g=10$). Does it start, and if it slides what is $a$?",
         "it slips; $a=2.5\\,\\mathrm{m/s}^2$",
         "$N=60\\,\\mathrm{N}$, $f_{s,\\max}=24\\,\\mathrm{N}$. Applied $30\\,\\mathrm{N}>24\\,\\mathrm{N}$, so it starts. Then $f_k=15\\,\\mathrm{N}$, $a=(30-15)/6=2.5\\,\\mathrm{m/s}^2$.",
         ["it stays at rest because $30<\\mu_s mg$ if someone uses $g=9.8$ wrong", "$a=5.0\\,\\mathrm{m/s}^2$ ignoring friction", "it slips with $a=0$"]),
        ("AP Stretch: A $2.0\\,\\mathrm{kg}$ block sits on a $3.0\\,\\mathrm{kg}$ block; you pull only the bottom block with $10\\,\\mathrm{N}$ on frictionless ice. They do not slip. Acceleration of each is",
         "$2.0\\,\\mathrm{m/s}^2$",
         "System mass $5.0\\,\\mathrm{kg}$, $a=10/5=2.0\\,\\mathrm{m/s}^2$. Static friction on the top block is $m_{\\mathrm{top}}a=4.0\\,\\mathrm{N}$.",
         ["$10\\,\\mathrm{m/s}^2$", "$3.3\\,\\mathrm{m/s}^2$", "$0$ for the top block"]),
        ("AP Stretch: A $2.0\\,\\mathrm{kg}$ block rides on a $3.0\\,\\mathrm{kg}$ block pulled by $10\\,\\mathrm{N}$ on ice without slipping. Friction on the top block is",
         "$4.0\\,\\mathrm{N}$",
         "Only friction accelerates the top: $f=(2.0)(2.0)=4.0\\,\\mathrm{N}$ forward.",
         ["$10\\,\\mathrm{N}$", "$6.0\\,\\mathrm{N}$", "$0$"]),
        ("AP Stretch: A person of mass $m$ pulls down on a rope with force $F$ over a pulley attached to the ceiling, accelerating upward. If the rope is pulled so two segments support the person, a model $2T-mg=ma$ means",
         "two upward rope forces act on the person-harness system",
         "Count forces on the chosen system. Two rope ends can mean $2T$ up.",
         ["weight doubled", "mass doubled", "g became $2g$"]),
        ("AP Stretch: A $5.0\\,\\mathrm{kg}$ crate ($\\mu_k=0.20$) is shoved with $50\\,\\mathrm{N}$ at $37^\\circ$ below the horizontal ($\\sin=3/5$, $\\cos=4/5$, $g=10$). Find $N$ and $a$.",
         "$N=80\\,\\mathrm{N}$, $a=4.8\\,\\mathrm{m/s}^2$",
         "Downward component $30\\,\\mathrm{N}$ so $N=50+30=80\\,\\mathrm{N}$. Then $f_k=16\\,\\mathrm{N}$, $F_x=40\\,\\mathrm{N}$, $a=(40-16)/5=4.8\\,\\mathrm{m/s}^2$.",
         ["$N=50\\,\\mathrm{N}$, $a=10\\,\\mathrm{m/s}^2$", "$N=20\\,\\mathrm{N}$, $a=8.0\\,\\mathrm{m/s}^2$", "$a=4.0\\,\\mathrm{m/s}^2$ using $F_x$ only and $N=mg$"]),
        ("AP Stretch: A $5.0\\,\\mathrm{kg}$ block on a rough table ($\\mu_k=0.20$) connects over a light frictionless pulley to a $3.0\\,\\mathrm{kg}$ hanging mass. Find $a$ and $T$ ($g=10$).",
         "$a=2.5\\,\\mathrm{m/s}^2$, $T=22.5\\,\\mathrm{N}$",
         "$f_k=0.20(50)=10\\,\\mathrm{N}$. Then $(30-10)/(5+3)=2.5\\,\\mathrm{m/s}^2$. Hang: $30-T=7.5$, so $T=22.5\\,\\mathrm{N}$.",
         ["$a=6.0\\,\\mathrm{m/s}^2$, $T=30\\,\\mathrm{N}$", "$a=2.5\\,\\mathrm{m/s}^2$, $T=10\\,\\mathrm{N}$", "$a=1.0\\,\\mathrm{m/s}^2$, $T=20\\,\\mathrm{N}$"]),
    ])
    return qs


def build_unit2():
    title = "AP Physics Unit 2: Force and Translational Dynamics"
    description = (
        "Newton's laws for AP Physics 1: inertia, net force and $F=ma$, third-law pairs, friction and drag, "
        "inclined planes, and connected systems — always with a free-body diagram before the algebra."
    )
    concepts = [
        "Newton 1 and inertia",
        "Newton 2 and net force",
        "Newton 3 pairs",
        "Friction and drag",
        "Inclined planes",
        "Systems and connected objects",
    ]

    c1 = concept_block(
        "1. Newton's first law and inertia",
        [
            "Newton's first law is the law of inertia: if the net force on an object is zero, its velocity does not "
            "change. Rest is allowed, and so is steady straight-line motion at constant speed.",
            "Net force means the vector sum of every force that acts on that object. Balanced forces ($10\\,\\mathrm{N}$ "
            "right and $10\\,\\mathrm{N}$ left) give $F_{\\mathrm{net}}=0$ even though forces are present.",
            "Mass measures inertia: how stubborn the velocity is. A full shopping cart is harder to start and harder to "
            "stop than an empty one, even on the same floor.",
            "A hockey puck on ideal ice keeps its velocity because horizontal $F_{\\mathrm{net}}=0$. Gravity and the "
            "normal force still exist; they cancel vertically.",
            "When a bus brakes, you slide forward relative to the bus because your body tries to keep the old velocity. "
            "That is not a forward force on you; it is the first law viewed from an accelerating frame of the bus.",
            "The first law tells you when you may write $a=0$. Constant speed in a straight line is an $a=0$ situation, "
            "so the forces on your free-body diagram must sum to zero.",
        ],
        "Every later force problem starts by asking whether $a$ is zero. If you skip that question, you will use $F=ma$ "
        "with the wrong acceleration, including on ramps and in elevators.",
        "Ask: is velocity changing? If not, $F_{\\mathrm{net}}=0$ and the first law applies. Draw the box and arrows before arithmetic.",
        lesson_figure(
            fbd_box(("F_g", "N", "0 (balanced)"),),
            "Free-body diagram of a book at rest on a table",
            "Weight down, normal up, equal magnitudes. Net force is zero, so acceleration is zero.",
        )
        + solved(1, "A $2.0\\,\\mathrm{kg}$ book rests on a table. Find the normal force ($g=10$).",
                 ["Weight $F_g=mg=20\\,\\mathrm{N}$ down.",
                  "At rest, $a=0$, so $N-F_g=0$.",
                  "$N=20\\,\\mathrm{N}$ up."],
                 "$20\\,\\mathrm{N}$ up", "", "Easy")
        + solved(2, "A $5.0\\,\\mathrm{kg}$ crate is pulled right with $12\\,\\mathrm{N}$ and friction $12\\,\\mathrm{N}$ left while moving at $3\\,\\mathrm{m/s}$. What is $a$?",
                 ["$F_{\\mathrm{net}}=12-12=0$.",
                  "Newton 1: $a=0$.",
                  "It continues at $3\\,\\mathrm{m/s}$ to the right. Constant velocity is not “no forces.”"],
                 "$a=0$ (constant $3\\,\\mathrm{m/s}$ right)", "", "Medium")
        + solved(3, "An elevator cable breaks (brief nightmare model) so the elevator is in free fall. A $4.0\\,\\mathrm{kg}$ backpack was on the floor. What does a spring scale between backpack and floor read?",
                 ["Both elevator and backpack accelerate downward at $g$.",
                  "Relative acceleration is zero; they do not press.",
                  "$N=0$, so the scale reads $0$.",
                  "This is still Newton's first law in the falling frame: apparent weight vanishes."],
                 "scale reads $0$", "Apparent weight is $N$, not $mg$ by itself.", "Hard"),
        ("Thinking a moving object must have a forward force",
         "Ancient intuition says motion needs an engine at all times. Newton says only a change in velocity needs a net force. Friction is often the unbalanced force that stops things, not a requirement for moving."),
        ("Write $a=0$ explicitly when speed is constant in a line",
         "Then every pair of opposite components must match. That checklist is the first-law problem."),
        [
            "I can state Newton's first law in terms of net force and constant velocity.",
            "I can recognize balanced-force situations that include nonzero speed.",
            "I can draw a free-body diagram for an object at rest on a surface.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Newton's second law and net force",
        [
            "Newton's second law: $\\vec{F}_{\\mathrm{net}}=m\\vec{a}$. The net force on an object equals its mass times "
            "its acceleration, and $\\vec{a}$ points the same way as $\\vec{F}_{\\mathrm{net}}$.",
            "Mass $m$ is in kilograms. Force is in newtons: $1\\,\\mathrm{N}=1\\,\\mathrm{kg\\cdot m/s}^2$. If $m=5\\,\\mathrm{kg}$ "
            "and $a=4\\,\\mathrm{m/s}^2$, then $F_{\\mathrm{net}}=20\\,\\mathrm{N}$.",
            "Net force is a sum. If $18\\,\\mathrm{N}$ pulls right and $6\\,\\mathrm{N}$ of friction pulls left, $F_{\\mathrm{net}}=12\\,\\mathrm{N}$ "
            "right. Only that remainder makes acceleration.",
            "Weight is the gravitational force $F_g=mg$ near Earth. It is one force among others. It is not automatically "
            "equal to the normal force, and it is not $F_{\\mathrm{net}}$ unless gravity is the only force.",
            "In an elevator, $T-mg=ma$ if up is positive. A scale reads the normal force, which can be larger or smaller "
            "than $mg$ when $a\\neq 0$.",
            "Always draw the object, list forces, choose axes, write $\\sum F_x=ma_x$ and $\\sum F_y=ma_y$. That ritual "
            "is the entire translational half of AP Physics 1.",
        ],
        "Friction, ramps, and connected masses are all second-law problems with extra geometry. If $F=ma$ is fuzzy, "
        "those lessons become memorized special cases instead of the same law.",
        "Circle the system. Draw every force on that system. Sum components. Only then write $ma$.",
        lesson_figure(
            _fbd_pull_and_friction(),
            "Crate being pulled right while friction also acts",
            "Horizontal net force is $F$ minus $f_k$. Vertical $N$ and $F_g$ cancel on a level floor.",
        )
        + solved(4, "A $5.0\\,\\mathrm{kg}$ sled has net force $20\\,\\mathrm{N}$ east. Find $a$.",
                 ["$a=F_{\\mathrm{net}}/m=20/5=4\\,\\mathrm{m/s}^2$.",
                  "Direction matches the net force: east.",
                  "Check units: $\\mathrm{N/kg}=\\mathrm{m/s}^2$."],
                 "$4\\,\\mathrm{m/s}^2$ east", "", "Easy")
        + solved(5, "A $3.0\\,\\mathrm{kg}$ box is pulled right with $18\\,\\mathrm{N}$; kinetic friction is $6.0\\,\\mathrm{N}$. Find $a$.",
                 ["$F_{\\mathrm{net},x}=18-6=12\\,\\mathrm{N}$.",
                  "$a=12/3=4.0\\,\\mathrm{m/s}^2$ right.",
                  "Vertical: $N=mg=30\\,\\mathrm{N}$ if the pull is horizontal."],
                 "$4.0\\,\\mathrm{m/s}^2$ right", "", "Medium")
        + solved(6, "A $4.0\\,\\mathrm{kg}$ backpack in an elevator has a scale reading $48\\,\\mathrm{N}$. Find the elevator's acceleration ($g=10$).",
                 ["Scale reading is $N=48\\,\\mathrm{N}$. Weight is $40\\,\\mathrm{N}$.",
                  "Up positive: $N-mg=ma\\Rightarrow 48-40=4a$.",
                  "$a=2.0\\,\\mathrm{m/s}^2$ upward.",
                  "If the reading had been $32\\,\\mathrm{N}$, $a$ would be $2.0\\,\\mathrm{m/s}^2$ down."],
                 "$2.0\\,\\mathrm{m/s}^2$ up", "", "Hard"),
        ("Using $F_g$ as if it were $F_{\\mathrm{net}}$",
         "Weight is only the gravity arrow. Net force is the leftover after you add normal force, tension, friction, and applied forces."),
        ("Split into $x$ and $y$ equations",
         "On a level floor, $y$ usually gives $N=mg$ (if no vertical applied component). Then $x$ gives $a$. Mixing the axes is the classic mess."),
        [
            "I can define net force as the vector sum of forces on one object.",
            "I can compute $a=F_{\\mathrm{net}}/m$ with direction.",
            "I can apply $N-mg=ma$ to an elevator scale reading.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Newton's third-law pairs",
        [
            "Forces come in pairs: if object A exerts a force on B, then B exerts a force on A that is equal in "
            "magnitude, opposite in direction, and of the same type (both gravity, or both contact, and so on).",
            "The pair never lives on the same free-body diagram. “Earth on book” is on the book's diagram; “book on Earth” "
            "is on Earth's diagram. They cannot cancel each other on the book.",
            "A bat hitting a ball is a contact pair. The forces are equal. The ball's acceleration is larger because "
            "the ball's mass is smaller. Equal force does not mean equal acceleration.",
            "Weight and normal force are often equal for a book at rest, but they are not a third-law pair. They are "
            "different interactions on the same object. The partner of weight is the book pulling up on Earth.",
            "Identify pairs by swapping the names: “A on B” partners with “B on A.” If the names do not swap, it is not "
            "the third-law partner.",
            "Internal forces in a two-block system are third-law pairs. When you treat both blocks as one system, those "
            "internal forces cancel in the system's $F_{\\mathrm{net}}$, which is why system thinking is powerful.",
        ],
        "Connected objects and collisions both require you to know which forces cancel inside a system. Third law is "
        "the reason tension can disappear from a two-mass $F=ma$ if you choose the system cleverly.",
        "Write the two names on every force arrow: who exerts it, who feels it. The partner is the names reversed.",
        lesson_figure(
            _newton3_pair(),
            "Contact pair between blocks A and B",
            "Equal-length opposite arrows on two different objects. They do not cancel on A's diagram.",
        )
        + solved(7, "A $60\\,\\mathrm{kg}$ student stands on Earth ($g=10$). Find the magnitude of the gravity pair.",
                 ["Student's weight $mg=600\\,\\mathrm{N}$ down (Earth on student).",
                  "Partner: student on Earth, $600\\,\\mathrm{N}$ up.",
                  "Earth's acceleration is tiny because Earth's mass is huge, but the forces match."],
                 "$600\\,\\mathrm{N}$", "", "Easy")
        + solved(8, "A bat exerts $200\\,\\mathrm{N}$ on a $0.40\\,\\mathrm{kg}$ ball for a short contact. What force does the ball exert on the bat, and what is the ball's acceleration during contact if that $200\\,\\mathrm{N}$ is the net force?",
                 ["Third law: ball on bat is $200\\,\\mathrm{N}$ opposite the bat's force.",
                  "Ball: $a=F/m=200/0.40=500\\,\\mathrm{m/s}^2$ in the direction of the hit.",
                  "The bat's acceleration is much smaller because the batter-bat system has more mass."],
                 "$200\\,\\mathrm{N}$ on the bat; $a_{\\mathrm{ball}}=500\\,\\mathrm{m/s}^2$", "", "Medium")
        + solved(9, "A box weighs $50\\,\\mathrm{N}$ and sits at rest. Identify whether $N$ and $F_g$ are a third-law pair, and name the true partner of each.",
                 ["$N=50\\,\\mathrm{N}$ up and $F_g=50\\,\\mathrm{N}$ down happen to match (first law on the box).",
                  "They are not a third-law pair: both act on the box, and they are different interactions.",
                  "Partner of $F_g$ (Earth on box) is box on Earth upward.",
                  "Partner of $N$ (table on box) is box on table downward."],
                 "not a third-law pair; partners swap the two objects", "", "Hard"),
        ("Canceling a third-law pair on one free-body diagram",
         "If both arrows are on the same object, they are not a third-law pair. Equal-and-opposite on one object is Newton's first/second law, not the third."),
        ("Swap the object names to test a pair",
         "“Table on book” matches “book on table.” “Earth on book” matches “book on Earth.” Weight is not partnered with $N$."),
        [
            "I can state the three properties of a Newton's third-law pair.",
            "I can explain why the pair does not cancel on one free-body diagram.",
            "I can distinguish equal $N$ and $mg$ from a true third-law pair.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Friction and drag",
        [
            "Friction is a contact force parallel to the surface, opposing slipping (or the attempted slipping). "
            "It is not the same as the normal force, which is perpendicular to the surface.",
            "Kinetic friction (object already sliding) has magnitude $f_k=\\mu_k N$. The coefficient $\\mu_k$ is a pure "
            "number that depends on the two surfaces. If $\\mu_k=0.20$ and $N=50\\,\\mathrm{N}$, then $f_k=10\\,\\mathrm{N}$.",
            "Static friction can be any size from zero up to $f_{s,\\max}=\\mu_s N$. It matches whatever it must, up to that "
            "cap, to prevent slipping. If you do not need that much, it does not use the maximum.",
            "On a level floor with a horizontal pull, $N=mg$ (no extra vertical forces). Then $f_k=\\mu_k mg$. "
            "Pushing down while you pull increases $N$ and therefore increases friction.",
            "Drag is friction with a fluid (air or water). It opposes velocity relative to the fluid and typically grows "
            "as speed grows. Terminal speed is the steady speed when drag (and sometimes buoyancy) balances weight.",
            "Direction errors are the usual exam trap: kinetic friction opposes velocity; static friction opposes the "
            "attempted relative slide, which you diagnose from the other forces.",
        ],
        "Ramps and connected systems almost always include friction in AP problems. If you grab $\\mu N$ without finding "
        "$N$ from the perpendicular equation, the parallel equation will be wrong.",
        "Find $N$ first from the perpendicular direction. Then $f=\\mu N$ if it is kinetic, or $f\\le\\mu_s N$ if static.",
        lesson_figure(
            _fbd_friction_vs_v(),
            "Sliding crate with kinetic friction opposite velocity",
            "Blue $v$ is to the right, so $f_k$ is to the left. Magnitude $\\mu_k N$.",
        )
        + solved(10, "A $5.0\\,\\mathrm{kg}$ crate slides on level ground with $\\mu_k=0.20$. Find $f_k$ ($g=10$).",
                 ["$N=mg=50\\,\\mathrm{N}$.",
                  "$f_k=\\mu_k N=0.20(50)=10\\,\\mathrm{N}$.",
                  "Direction: opposite the velocity."],
                 "$10\\,\\mathrm{N}$ opposite $v$", "", "Easy")
        + solved(11, "That crate is pulled horizontally with $18\\,\\mathrm{N}$. Find $a$.",
                 ["$F_{\\mathrm{net}}=18-10=8\\,\\mathrm{N}$.",
                  "$a=8/5=1.6\\,\\mathrm{m/s}^2$ in the pull direction.",
                  "If the pull were only $10\\,\\mathrm{N}$, $a$ would be zero."],
                 "$1.6\\,\\mathrm{m/s}^2$", "", "Medium")
        + solved(12, "A $4.0\\,\\mathrm{kg}$ block has $\\mu_s=0.40$ and $\\mu_k=0.30$ on a level floor. You pull with $12\\,\\mathrm{N}$ horizontally. Does it start, and if it were already sliding what would $a$ be?",
                 ["$N=40\\,\\mathrm{N}$, $f_{s,\\max}=0.40(40)=16\\,\\mathrm{N}$.",
                  "$12<16$, so if it starts at rest it stays at rest; static friction is $12\\,\\mathrm{N}$.",
                  "If it is already sliding, $f_k=0.30(40)=12\\,\\mathrm{N}$, so $a=0$ while sliding at that pull.",
                  "Starting and continuing are different tests: $\\mu_s$ versus $\\mu_k$."],
                 "stays at rest if originally still; $a=0$ if already sliding at this $12\\,\\mathrm{N}$",
                 "", "Hard"),
        ("Always using $f=\\mu N$ at the maximum for static cases",
         "Static friction equals the maximum only when the object is just about to slip. Below that, $f_s$ equals the needed balancing force."),
        ("Compute $N$ from the perpendicular equation before $\\mu N$",
         "A downward push or a ramp changes $N$. Writing $f=\\mu mg$ blindly is the shortcut that fails on AP FRQs."),
        [
            "I can compute $f_k=\\mu_k N$ with the correct direction.",
            "I can compare an applied force with $f_{s,\\max}$ to decide if slipping starts.",
            "I can explain terminal speed as balanced weight and drag.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Inclined planes",
        [
            "On a ramp, the smart axes are parallel and perpendicular to the surface, not horizontal and vertical. "
            "Weight $mg$ still points straight down; you split it into components.",
            "The component down the slope is $mg\\sin\\theta$. The component into the slope is $mg\\cos\\theta$, which "
            "the normal force balances on a dry ramp with no other perpendicular forces: $N=mg\\cos\\theta$.",
            "Frictionless, $a=g\\sin\\theta$ down the ramp. Mass cancels. A $30^\\circ$ ramp gives $a=5\\,\\mathrm{m/s}^2$ "
            "with $g=10$. A $3$-$4$-$5$ ramp ($\\sin\\theta=0.6$) gives $a=6\\,\\mathrm{m/s}^2$.",
            "With kinetic friction, $f_k=\\mu_k N=\\mu_k mg\\cos\\theta$, usually up the ramp if the block slides down. "
            "Then $mg\\sin\\theta-f_k=ma$.",
            "The normal force is not equal to the weight on an incline. Drawing $N$ vertically is the diagram error that "
            "ruins the algebra.",
            "If the ramp angle increases, $mg\\sin\\theta$ grows and $N$ shrinks, so friction's maximum $\\mu_s N$ shrinks "
            "too. The block slips when $\\tan\\theta=\\mu_s$.",
        ],
        "Rolling, energy on a slope, and later rotational problems still start with this component split. It is the "
        "geometry backbone of AP Physics 1.",
        "Redraw $mg$ as a hypotenuse. Opposite the angle along the ramp is $mg\\sin\\theta$. Adjacent into the ramp is $mg\\cos\\theta$.",
        lesson_figure(
            _ramp_fbd(),
            "Ramp FBD: $N$ perpendicular, $F_g$ split, friction up the ramp",
            "Weight stays vertical. $mg\\sin\\theta$ is down-ramp, $mg\\cos\\theta$ into the ramp, $N$ is perpendicular, $f_k$ opposes the slide.",
        )
        + solved(13, "A $2.0\\,\\mathrm{kg}$ block is on a frictionless ramp with $\\sin\\theta=0.50$. Find $a$ ($g=10$).",
                 ["$F_{\\mathrm{net}}=mg\\sin\\theta=20(0.50)=10\\,\\mathrm{N}$ down the ramp.",
                  "$a=10/2=5.0\\,\\mathrm{m/s}^2$, or $a=g\\sin\\theta=5.0\\,\\mathrm{m/s}^2$.",
                  "Mass canceled, as expected."],
                 "$5.0\\,\\mathrm{m/s}^2$ down the ramp", "", "Easy")
        + solved(14, "A $5.0\\,\\mathrm{kg}$ box is on a $3$-$4$-$5$ ramp ($\\sin\\theta=0.6$, $\\cos\\theta=0.8$) with $\\mu_k=0.25$. Find $f_k$ and $a$ while sliding down ($g=10$).",
                 ["$N=mg\\cos\\theta=50(0.8)=40\\,\\mathrm{N}$.",
                  "$f_k=0.25(40)=10\\,\\mathrm{N}$ up the ramp.",
                  "$mg\\sin\\theta=30\\,\\mathrm{N}$ down. Net $20\\,\\mathrm{N}$ down.",
                  "$a=20/5=4.0\\,\\mathrm{m/s}^2$ down the ramp."],
                 "$f_k=10\\,\\mathrm{N}$; $a=4.0\\,\\mathrm{m/s}^2$ down", "", "Medium")
        + solved(15, "For $\\mu_s=0.75$ on a ramp, find $\\tan\\theta$ when the block is just about to slip from rest.",
                 ["At the breaking point $mg\\sin\\theta=\\mu_s mg\\cos\\theta$.",
                  "Cancel $mg$: $\\tan\\theta=\\mu_s=0.75$.",
                  "If $\\theta$ is smaller than that, static friction is less than the maximum and the block stays.",
                  "Mass canceled again: a heavier block does not change the critical angle."],
                 "$\\tan\\theta=0.75$", "", "Hard"),
        ("Drawing the normal force vertically on a ramp",
         "The surface can only push perpendicular to itself. Tilt $N$. Weight stays vertical. Components live in the tilted axes."),
        ("Write $N=mg\\cos\\theta$ before friction",
         "Then $f=\\mu N$ uses the correct $N$. Using $mg$ instead of $N$ is the most common numeric error on ramp FRQs."),
        [
            "I can resolve $mg$ into $mg\\sin\\theta$ and $mg\\cos\\theta$ on an incline.",
            "I can find $a=g\\sin\\theta$ when the ramp is frictionless.",
            "I can include $\\mu_k mg\\cos\\theta$ in the parallel equation.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Systems and connected objects",
        [
            "When two objects are tied by a string or stacked, you may treat them as one system or as two objects. "
            "The system trick: internal forces (string tension, contact forces) cancel by Newton's third law, so only external forces accelerate the total mass.",
            "Example: $2\\,\\mathrm{kg}$ and $6\\,\\mathrm{kg}$ pushed by $16\\,\\mathrm{N}$ on frictionless ice. System mass $8\\,\\mathrm{kg}$, "
            "$a=2\\,\\mathrm{m/s}^2$ for both. Then zoom in on one mass to find the internal force.",
            "Atwood's machine is two masses hanging on a pulley. If the pulley is light and frictionless, "
            "$a=(m_2-m_1)g/(m_1+m_2)$ and $T=2m_1 m_2 g/(m_1+m_2)$. For $3\\,\\mathrm{kg}$ and $5\\,\\mathrm{kg}$, $a=2.5\\,\\mathrm{m/s}^2$ and $T=37.5\\,\\mathrm{N}$.",
            "A hanging mass pulling a cart is the same idea: the hanging weight is the external force that is not canceled, "
            "and both masses sit in the denominator because both accelerate.",
            "Never put both masses on one free-body diagram unless you have decided they are one system. Mixing tension "
            "and both weights on a single sloppy sketch is how Atwood problems explode.",
            "Check with a limit: if $m_2\\gg m_1$, Atwood $a$ approaches $g$ and $T$ approaches $2m_1 g$. If the masses "
            "are equal, $a=0$ and $T=mg$. Limits catch algebra bugs.",
        ],
        "Unit 6 will add a rotating pulley with rotational inertia. The system method you practice here is the same, "
        "with one extra $\\tau=I\\alpha$ equation for the pulley.",
        "First find $a$ from the system. Then isolate one mass to find $T$ or the contact force.",
        lesson_figure(
            _connected_blocks(),
            "Two blocks pulled by an external $F$ on a frictionless surface",
            "System: $a=F/(m_1+m_2)$. Rear block: $T=m_1 a$. Front block: $F-T=m_2 a$.",
        )
        + solved(16, "Blocks $2.0\\,\\mathrm{kg}$ and $6.0\\,\\mathrm{kg}$ are pushed by $16\\,\\mathrm{N}$ on frictionless ice. Find $a$.",
                 ["System mass $8.0\\,\\mathrm{kg}$.",
                  "$a=16/8=2.0\\,\\mathrm{m/s}^2$.",
                  "Both blocks have this same $a$ because they move together."],
                 "$2.0\\,\\mathrm{m/s}^2$", "", "Easy")
        + solved(17, "If the $2.0\\,\\mathrm{kg}$ block is in front, find the contact force from the $6.0\\,\\mathrm{kg}$ block.",
                 ["Front mass only feels the contact force (no other horizontal force).",
                  "$F_c=m_{\\mathrm{front}}a=2(2)=4.0\\,\\mathrm{N}$.",
                  "Check the back: $16-F_c=6(2)=12$, so $F_c=4.0\\,\\mathrm{N}$."],
                 "$4.0\\,\\mathrm{N}$", "", "Medium")
        + solved(18, "Atwood masses $3.0\\,\\mathrm{kg}$ and $5.0\\,\\mathrm{kg}$, light frictionless pulley. Find $a$ and $T$ ($g=10$).",
                 ["$a=(5-3)(10)/(8)=20/8=2.5\\,\\mathrm{m/s}^2$.",
                  "For $3\\,\\mathrm{kg}$ going up: $T-30=3(2.5)$, so $T=37.5\\,\\mathrm{N}$.",
                  "For $5\\,\\mathrm{kg}$ going down: $50-T=5(2.5)=12.5$, so $T=37.5\\,\\mathrm{N}$.",
                  "Same $T$ from both sides: the algebra checks."],
                 "$a=2.5\\,\\mathrm{m/s}^2$, $T=37.5\\,\\mathrm{N}$", "", "Hard"),
        ("Putting tension and both weights on one muddled diagram",
         "Either draw two diagrams (one per mass) or one system diagram that omits internal $T$. Do not do a hybrid."),
        ("Find $a$ from total mass, then zoom in for $T$",
         "System first, internal force second. That order keeps the algebra short and the checks obvious."),
        [
            "I can find a two-mass acceleration from $F_{\\mathrm{ext}}/m_{\\mathrm{total}}$.",
            "I can solve for tension by isolating one mass after $a$ is known.",
            "I can analyze a light-pulley Atwood machine with $g=10$.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Work, Energy, and Power
# ===========================================================================

def _u3_questions():
    qs = []
    _add(qs, [
        ("Work by a constant force is $W=Fd\\cos\\theta$, with $\\theta$ between $\\vec{F}$ and $\\Delta\\vec{x}$. If $F=20\\,\\mathrm{N}$, $d=3\\,\\mathrm{m}$, and $\\theta=0$, work is",
         "$60\\,\\mathrm{J}$",
         "$W=(20)(3)(1)=60\\,\\mathrm{J}$. The joule is a newton-meter.",
         ["$23\\,\\mathrm{J}$", "$6.7\\,\\mathrm{J}$", "$0$"]),
        ("A $50\\,\\mathrm{N}$ force pulls at $60^\\circ$ while the object moves $4.0\\,\\mathrm{m}$. Work by that force is",
         "$100\\,\\mathrm{J}$",
         "$\\cos 60^\\circ=1/2$, so $W=50(4)(0.5)=100\\,\\mathrm{J}$.",
         ["$200\\,\\mathrm{J}$", "$50\\,\\mathrm{J}$", "$400\\,\\mathrm{J}$"]),
        ("The work done by the kinetic friction force is usually negative because",
         "friction points opposite the displacement, so $\\cos\\theta=-1$",
         "Negative work removes mechanical energy from the object (often into thermal energy).",
         ["friction has no direction", "work cannot be negative", "mass is negative"]),
        ("A $10\\,\\mathrm{N}$ force is perpendicular to a $5.0\\,\\mathrm{m}$ displacement. Work by that force is",
         "$0$",
         "$\\cos 90^\\circ=0$, so $W=0$. The force still exists; it does no work.",
         ["$50\\,\\mathrm{J}$", "$15\\,\\mathrm{J}$", "$-50\\,\\mathrm{J}$"]),
        ("Gravity does work $W_g=-mg\\Delta h$ if $h$ is height. Lifting a $2\\,\\mathrm{kg}$ book $3\\,\\mathrm{m}$ at constant speed, work by gravity is ($g=10$)",
         "$-60\\,\\mathrm{J}$",
         "Height increases, gravity points down, $W_g=-20(3)=-60\\,\\mathrm{J}$. Your hand does $+60\\,\\mathrm{J}$.",
         ["$+60\\,\\mathrm{J}$", "$0$ because speed is constant", "$6\\,\\mathrm{J}$"]),
    ])
    _add(qs, [
        ("The work-energy theorem says $W_{\\mathrm{net}}=\\Delta K$. If net work is $+40\\,\\mathrm{J}$, kinetic energy",
         "increases by $40\\,\\mathrm{J}$",
         "Net work on the object becomes a change in $\\tfrac12 mv^2$.",
         ["decreases by $40\\,\\mathrm{J}$", "is unchanged", "becomes $40\\,\\mathrm{J}$ regardless of the start"]),
        ("A $4.0\\,\\mathrm{kg}$ cart speeds from rest to $6.0\\,\\mathrm{m/s}$. $\\Delta K$ is",
         "$72\\,\\mathrm{J}$",
         "$K_f=\\tfrac12(4)(36)=72\\,\\mathrm{J}$, $K_i=0$, so $\\Delta K=72\\,\\mathrm{J}$.",
         ["$24\\,\\mathrm{J}$", "$12\\,\\mathrm{J}$", "$144\\,\\mathrm{J}$"]),
        ("How much net work is required for that $72\\,\\mathrm{J}$ increase?",
         "$72\\,\\mathrm{J}$",
         "Work-energy theorem: $W_{\\mathrm{net}}=\\Delta K=72\\,\\mathrm{J}$.",
         ["$36\\,\\mathrm{J}$", "$0$", "$4\\,\\mathrm{J}$"]),
        ("A $2.0\\,\\mathrm{kg}$ object slows from $8.0\\,\\mathrm{m/s}$ to $4.0\\,\\mathrm{m/s}$. Net work on it is",
         "$-48\\,\\mathrm{J}$",
         "$\\Delta K=\\tfrac12(2)(16-64)=16-64=-48\\,\\mathrm{J}$.",
         ["$+48\\,\\mathrm{J}$", "$-16\\,\\mathrm{J}$", "$0$"]),
        ("If only a conservative force does work, $\\Delta K+\\Delta U=0$. That is equivalent to",
         "mechanical energy is conserved",
         "The work-energy theorem plus $W_{\\mathrm{cons}}=-\\Delta U$ yields $K+U$ constant.",
         ["momentum is always zero", "temperature is constant", "net force is zero"]),
    ])
    _add(qs, [
        ("Gravitational potential energy near Earth can be written $U_g=mgh$ with a chosen $h=0$. A $3.0\\,\\mathrm{kg}$ brick $4.0\\,\\mathrm{m}$ above that zero has ($g=10$)",
         "$120\\,\\mathrm{J}$",
         "$U=mgh=3(10)(4)=120\\,\\mathrm{J}$.",
         ["$12\\,\\mathrm{J}$", "$7\\,\\mathrm{J}$", "$40\\,\\mathrm{J}$"]),
        ("If you move the zero to the brick's current height, the new $U_g$ of that brick is",
         "$0$",
         "Only differences $\\Delta U$ are physical. Changing the zero shifts all $U$ values equally.",
         ["$120\\,\\mathrm{J}$ still", "undefined", "infinite"]),
        ("Dropping that brick $4.0\\,\\mathrm{m}$ (no air), $\\Delta U_g$ is",
         "$-120\\,\\mathrm{J}$",
         "Height falls by $4\\,\\mathrm{m}$, so $U$ falls by $120\\,\\mathrm{J}$. That energy becomes kinetic.",
         ["$+120\\,\\mathrm{J}$", "$0$", "$-30\\,\\mathrm{J}$"]),
        ("A $2.0\\,\\mathrm{kg}$ ball falls $5.0\\,\\mathrm{m}$ from rest. Speed just before impact, using energy, is ($g=10$)",
         "$10\\,\\mathrm{m/s}$",
         "$mgh=\\tfrac12 mv^2\\Rightarrow v=\\sqrt{2gh}=\\sqrt{100}=10\\,\\mathrm{m/s}$.",
         ["$5\\,\\mathrm{m/s}$", "$20\\,\\mathrm{m/s}$", "$\\sqrt{10}\\,\\mathrm{m/s}$"]),
        ("Path independence: gravity's work between two heights depends on",
         "only the change in height, not the path shape",
         "That is why $U_g=mgh$ is allowed. Friction's work does depend on path length.",
         ["the exact curve taken", "the time taken", "the mass of Earth only, not $h$"]),
    ])
    _add(qs, [
        ("Mechanical energy $K+U$ is conserved when",
         "no nonconservative work (like friction) removes or adds mechanical energy",
         "Gravity and ideal springs can trade $K$ and $U$. Kinetic friction makes $E_{\\mathrm{mech}}$ drop.",
         ["always, even with friction", "only if the object is at rest", "only in space"]),
        ("A $2.0\\,\\mathrm{kg}$ block slides from rest down a frictionless $5.0\\,\\mathrm{m}$ height. Speed at the bottom is",
         "$10\\,\\mathrm{m/s}$",
         "$mgh=\\tfrac12 mv^2$, $v=\\sqrt{2gh}=10\\,\\mathrm{m/s}$. The ramp length does not enter.",
         ["depends on the ramp length", "$5\\,\\mathrm{m/s}$", "$\\sqrt{5}\\,\\mathrm{m/s}$"]),
        ("The same block on a rough ramp loses $20\\,\\mathrm{J}$ to thermal energy. If $mgh=100\\,\\mathrm{J}$, $K$ at the bottom is",
         "$80\\,\\mathrm{J}$",
         "$E_i=100\\,\\mathrm{J}=K_f+20\\,\\mathrm{J}$, so $K_f=80\\,\\mathrm{J}$.",
         ["$100\\,\\mathrm{J}$", "$120\\,\\mathrm{J}$", "$20\\,\\mathrm{J}$"]),
        ("A pendulum is released from height $h$. Speed at the bottom (no drag) is",
         "$\\sqrt{2gh}$",
         "Same energy trade as a drop: $mgh=\\tfrac12 mv^2$.",
         ["$gh$", "$2gh$", "$\\sqrt{gh}$"]),
        ("Energy bars: at a frictionless track's highest point a car is at rest. At the lowest point the bars show",
         "all kinetic, height of the original PE bar",
         "Total bar height stays the same; PE emptied into KE.",
         ["all thermal", "empty bars", "KE and PE both full and doubled"]),
    ])
    _add(qs, [
        ("Average power is $P=W/\\Delta t$. Doing $100\\,\\mathrm{J}$ of work in $4.0\\,\\mathrm{s}$ is",
         "$25\\,\\mathrm{W}$",
         "$P=100/4=25\\,\\mathrm{W}$. A watt is a joule per second.",
         ["$400\\,\\mathrm{W}$", "$4\\,\\mathrm{W}$", "$100\\,\\mathrm{W}$"]),
        ("Instantaneous power by a force aligned with velocity is $P=Fv$. If $F=30\\,\\mathrm{N}$ and $v=4.0\\,\\mathrm{m/s}$, $P$ is",
         "$120\\,\\mathrm{W}$",
         "$P=(30)(4)=120\\,\\mathrm{W}$.",
         ["$7.5\\,\\mathrm{W}$", "$34\\,\\mathrm{W}$", "$0$"]),
        ("Lifting a $20\\,\\mathrm{kg}$ crate $3.0\\,\\mathrm{m}$ at constant speed in $6.0\\,\\mathrm{s}$, average power against gravity is ($g=10$)",
         "$100\\,\\mathrm{W}$",
         "$W=mgh=600\\,\\mathrm{J}$, $P=600/6=100\\,\\mathrm{W}$.",
         ["$10\\,\\mathrm{W}$", "$60\\,\\mathrm{W}$", "$200\\,\\mathrm{W}$"]),
        ("Two engines do the same work. The one that finishes in half the time has",
         "twice the average power",
         "$P=W/t$. Same $W$, half $t$, double $P$.",
         ["half the power", "the same power", "four times the power"]),
        ("A $40\\,\\mathrm{N}$ pull at $60^\\circ$ above the velocity of $5.0\\,\\mathrm{m/s}$ does power",
         "$100\\,\\mathrm{W}$",
         "$P=Fv\\cos\\theta=40(5)(0.5)=100\\,\\mathrm{W}$.",
         ["$200\\,\\mathrm{W}$", "$40\\,\\mathrm{W}$", "$0$"]),
    ])
    _add(qs, [
        ("Elastic energy in an ideal spring is $U_s=\\tfrac12 kx^2$. For $k=200\\,\\mathrm{N/m}$ and $x=0.10\\,\\mathrm{m}$, $U_s$ is",
         "$1.0\\,\\mathrm{J}$",
         "$U=\\tfrac12(200)(0.01)=1.0\\,\\mathrm{J}$.",
         ["$20\\,\\mathrm{J}$", "$2.0\\,\\mathrm{J}$", "$0.10\\,\\mathrm{J}$"]),
        ("Hooke's law: $F_s=-kx$. If $k=50\\,\\mathrm{N/m}$ and the spring is stretched $0.20\\,\\mathrm{m}$, force magnitude is",
         "$10\\,\\mathrm{N}$ toward equilibrium",
         "$|F|=(50)(0.20)=10\\,\\mathrm{N}$, restoring.",
         ["$250\\,\\mathrm{N}$", "$10\\,\\mathrm{N}$ away from equilibrium", "$0.004\\,\\mathrm{N}$"]),
        ("A $4.0\\,\\mathrm{kg}$ block compresses a $k=400\\,\\mathrm{N/m}$ spring by $0.20\\,\\mathrm{m}$ and is released on frictionless ice. Max speed is",
         "$2.0\\,\\mathrm{m/s}$",
         "$\\tfrac12 kx^2=\\tfrac12 mv^2\\Rightarrow v=x\\sqrt{k/m}=0.20\\sqrt{100}=2.0\\,\\mathrm{m/s}$.",
         ["$4.0\\,\\mathrm{m/s}$", "$8.0\\,\\mathrm{m/s}$", "$0.20\\,\\mathrm{m/s}$"]),
        ("Doubling the compression of a spring multiplies stored energy by",
         "$4$",
         "$U\\propto x^2$. Double $x$, quadruple $U$.",
         ["$2$", "$8$", "$1$ (unchanged)"]),
        ("Work by an ideal spring between two stretches equals",
         "$-\\Delta U_s$",
         "The spring force is conservative. $W_{\\mathrm{spring}}=\\tfrac12 k x_i^2-\\tfrac12 k x_f^2$.",
         ["always positive", "$kx$", "$mgh$"]),
    ])
    _add(qs, [
        ("Pushing a wall with $50\\,\\mathrm{N}$ while the wall does not move, work by you on the wall is",
         "$0$",
         "Displacement of the point of application is zero, so $W=0$.",
         ["$50\\,\\mathrm{J}$", "infinite", "negative"]),
        ("A $3.0\\,\\mathrm{kg}$ cart going $4.0\\,\\mathrm{m/s}$ has kinetic energy",
         "$24\\,\\mathrm{J}$",
         "$K=\\tfrac12(3)(16)=24\\,\\mathrm{J}$.",
         ["$12\\,\\mathrm{J}$", "$6\\,\\mathrm{J}$", "$48\\,\\mathrm{J}$"]),
        ("To double that cart's speed, kinetic energy must be multiplied by",
         "$4$",
         "$K\\propto v^2$. Double $v$, quadruple $K$.",
         ["$2$", "$8$", "$\\sqrt{2}$"]),
        ("A roller-coaster car starts $20\\,\\mathrm{m}$ above the bottom. Speed at the bottom (frictionless, $g=10$) is",
         "$20\\,\\mathrm{m/s}$",
         "$v=\\sqrt{2gh}=\\sqrt{400}=20\\,\\mathrm{m/s}$.",
         ["$10\\,\\mathrm{m/s}$", "$14\\,\\mathrm{m/s}$", "$40\\,\\mathrm{m/s}$"]),
        ("If friction does $-100\\,\\mathrm{J}$ of work on a $2.0\\,\\mathrm{kg}$ coaster that started with $U=200\\,\\mathrm{J}$ at rest, $K$ at the bottom is",
         "$100\\,\\mathrm{J}$",
         "$200-100=100\\,\\mathrm{J}$ of kinetic energy remains.",
         ["$200\\,\\mathrm{J}$", "$300\\,\\mathrm{J}$", "$0$"]),
        ("A $100\\,\\mathrm{W}$ motor runs for $5.0\\,\\mathrm{s}$. Energy it transfers is",
         "$500\\,\\mathrm{J}$",
         "$W=P t=100(5)=500\\,\\mathrm{J}$.",
         ["$20\\,\\mathrm{J}$", "$100\\,\\mathrm{J}$", "$5\\,\\mathrm{J}$"]),
        ("Spring $k=800\\,\\mathrm{N/m}$ stores $16\\,\\mathrm{J}$. The compression $|x|$ is",
         "$0.20\\,\\mathrm{m}$",
         "$16=\\tfrac12(800)x^2=400x^2$, $x^2=0.04$, $|x|=0.20\\,\\mathrm{m}$.",
         ["$0.040\\,\\mathrm{m}$", "$0.02\\,\\mathrm{m}$", "$4.0\\,\\mathrm{m}$"]),
        ("A force does $30\\,\\mathrm{J}$ of work while friction does $-10\\,\\mathrm{J}$. If those are the only two, $\\Delta K$ is",
         "$20\\,\\mathrm{J}$",
         "$W_{\\mathrm{net}}=20\\,\\mathrm{J}=\\Delta K$.",
         ["$30\\,\\mathrm{J}$", "$-10\\,\\mathrm{J}$", "$40\\,\\mathrm{J}$"]),
        ("Choosing $h=0$ at a tabletop, a $1.0\\,\\mathrm{kg}$ mass on the floor $0.80\\,\\mathrm{m}$ below has $U_g=$ ($g=10$)",
         "$-8.0\\,\\mathrm{J}$",
         "Negative potential energy is allowed; it means below your zero.",
         ["$+8.0\\,\\mathrm{J}$", "$0$", "$-0.80\\,\\mathrm{J}$"]),
        ("A child slides down a curved slide. Gravity's work depends on",
         "the vertical drop only",
         "Conservative force: path shape does not matter for $W_g$.",
         ["the arc length only", "the time only", "the child's speed at the top only"]),
        ("Power needed to tow at constant $10\\,\\mathrm{m/s}$ against $200\\,\\mathrm{N}$ of drag is",
         "$2000\\,\\mathrm{W}$",
         "$P=Fv=2000\\,\\mathrm{W}$ because the tow force matches drag at constant speed.",
         ["$20\\,\\mathrm{W}$", "$200\\,\\mathrm{W}$", "$0$ because $a=0$"]),
        ("A spring launches a block up a frictionless ramp. The block rises until",
         "$\\tfrac12 kx^2=mgh$ (all spring energy becomes gravitational $U$)",
         "Mechanical energy conserved; $K=0$ at the highest point if it does not leave the track with leftover speed along the track... for a block that stops, yes $U_s=U_g$.",
         ["$kx=mg$", "$x=h$", "energy is not useful here"]),
        ("Which force is nonconservative in typical AP models?",
         "kinetic friction",
         "Its work depends on path length and becomes thermal energy. Gravity and ideal springs are conservative.",
         ["gravity near Earth in the $mgh$ model", "ideal spring force", "a constant $mg$ over a closed height loop with no air"]),
        ("A $5.0\\,\\mathrm{kg}$ object is lifted at constant $2.0\\,\\mathrm{m/s}$. Instantaneous power against gravity is ($g=10$)",
         "$100\\,\\mathrm{W}$",
         "$F=mg=50\\,\\mathrm{N}$, $P=Fv=100\\,\\mathrm{W}$.",
         ["$10\\,\\mathrm{W}$", "$25\\,\\mathrm{W}$", "$0$ because $a=0$"]),
        ("A motor raises a $20\\,\\mathrm{kg}$ crate $3.0\\,\\mathrm{m}$ in $2.0\\,\\mathrm{s}$ at constant speed ($g=10$). Average power against gravity is",
         "$300\\,\\mathrm{W}$",
         "$W=mgh=(20)(10)(3.0)=600\\,\\mathrm{J}$. Then $P=W/t=300\\,\\mathrm{W}$.",
         ["$60\\,\\mathrm{W}$", "$600\\,\\mathrm{W}$", "$120\\,\\mathrm{W}$"]),
        ("A $200\\,\\mathrm{N/m}$ spring is compressed $0.10\\,\\mathrm{m}$ from equilibrium. Stored elastic energy is",
         "$1.0\\,\\mathrm{J}$",
         "$U_s=\\tfrac12 kx^2=\\tfrac12(200)(0.010)=1.0\\,\\mathrm{J}$.",
         ["$20\\,\\mathrm{J}$", "$2.0\\,\\mathrm{J}$", "$0.10\\,\\mathrm{J}$"]),
        ("AP Stretch: A $5.0\\,\\mathrm{kg}$ crate starts from rest and slides $10.0\\,\\mathrm{m}$ down a ramp with $\\sin\\theta=0.80$ and $\\cos\\theta=0.60$. If $\\mu_k=0.50$ and $g=10$, find speed at the bottom and thermal energy generated.",
         "$v=10\\,\\mathrm{m/s}$, $E_{\\mathrm{th}}=150\\,\\mathrm{J}$",
         "$h=8.0\\,\\mathrm{m}$, $U$ drop $=400\\,\\mathrm{J}$. $N=30\\,\\mathrm{N}$, $f_k=15\\,\\mathrm{N}$, $W_f=-150\\,\\mathrm{J}$. Then $K=250\\,\\mathrm{J}$, $v=\\sqrt{100}=10\\,\\mathrm{m/s}$, and $E_{\\mathrm{th}}=150\\,\\mathrm{J}$.",
         ["$v=\\sqrt{160}\\,\\mathrm{m/s}$ ignoring friction", "$v=8.0\\,\\mathrm{m/s}$, $E_{\\mathrm{th}}=0$", "$K=400\\,\\mathrm{J}$ with no thermal bar"]),
        ("AP Stretch: A block is launched by a spring on level frictionless ice, then climbs a frictionless hill of height $h$. Minimum $x$ of a spring $k$ for mass $m$ is",
         "$x=\\sqrt{2mgh/k}$",
         "$\\tfrac12 kx^2=mgh$, so $x=\\sqrt{2mgh/k}$.",
         ["$x=mgh/k$", "$x=\\sqrt{mgh/k}$", "$x=2mgh/k$"]),
        ("AP Stretch: Power of a constant $F$ pulling a crate from rest: after time $t$, $v=at=Ft/m$, so $P=Fv$ grows",
         "linearly with $t$",
         "$P=F(Ft/m)=(F^2/m)t$. Instantaneous power increases as the object speeds up.",
         ["as $1/t$", "is constant", "as $t^2$ only if $F$ changes"]),
        ("AP Stretch: A pendulum bob of mass $m$ is caught by a spring at the bottom. If it started from height $h$ and the spring compresses $x$ at the lowest point of the bob, energy says",
         "$mgh=\\tfrac12 kx^2$ only if the bob is instantaneously at rest there; otherwise leftover $K$ remains",
         "If the spring is still compressing, $K$ is not yet zero. Set $mgh=\\tfrac12 kx^2+K$.",
         ["$mgh=kx$ always", "energy cannot be used with springs and gravity together", "mass cancels so $h=x$"]),
        ("AP Stretch: You carry a $10\\,\\mathrm{kg}$ backpack horizontally at constant speed for $20\\,\\mathrm{m}$. Work by you on the backpack (idealized, no bounce) is closest to",
         "$0$",
         "The force you exert is upward (supporting weight); displacement is horizontal; $\\cos 90^\\circ=0$.",
         ["$2000\\,\\mathrm{J}$", "$200\\,\\mathrm{J}$", "$20\\,\\mathrm{J}$"]),
        ("AP Stretch: A $1.0\\,\\mathrm{kg}$ ball dropped from $5.0\\,\\mathrm{m}$ embeds in snow and stops in $0.20\\,\\mathrm{m}$. Including gravity in the snow, the average resistive force is ($g=10$)",
         "$260\\,\\mathrm{N}$",
         "Total height drop to rest is $5.2\\,\\mathrm{m}$, so $mg(5.2)=52\\,\\mathrm{J}$ is removed by the snow force over $0.20\\,\\mathrm{m}$: $F_{\\mathrm{avg}}(0.20)=52$, hence $F_{\\mathrm{avg}}=260\\,\\mathrm{N}$ (upward).",
         ["$50\\,\\mathrm{N}$", "$250\\,\\mathrm{N}$", "$10\\,\\mathrm{N}$"]),
        ("AP Stretch: Two springs in series with $k$ and $2k$, overall stretch $x_{\\mathrm{tot}}$ under force $F$. The energy stored compared with one spring $k$ stretched $x_{\\mathrm{tot}}$ is",
         "less, because the series pair is softer (smaller effective $k$)",
         "Series $k_{\\mathrm{eff}}=(2/3)k$. $U=\\tfrac12 k_{\\mathrm{eff}} x^2$ is smaller than $\\tfrac12 k x^2$ for the same total $x$.",
         ["more", "the same", "zero"]),
        ("AP Stretch: A motor rated $400\\,\\mathrm{W}$ lifts a $20\\,\\mathrm{kg}$ load at constant speed. Maximum speed is ($g=10$)",
         "$2.0\\,\\mathrm{m/s}$",
         "$P=mgv\\Rightarrow v=P/mg=400/200=2.0\\,\\mathrm{m/s}$.",
         ["$20\\,\\mathrm{m/s}$", "$0.50\\,\\mathrm{m/s}$", "$4.0\\,\\mathrm{m/s}$"]),
        ("AP Stretch: On an energy-bar diagram, thermal energy appears after a slide. The total of KE+PE+thermal compared with the initial PE is",
         "the same (energy is still conserved, just not all mechanical)",
         "Friction converts mechanical energy into $E_{\\mathrm{th}}$, but the sum of all forms is constant in the isolated system.",
         ["smaller always, energy vanished", "larger, friction creates energy", "undefined"]),
    ])
    return qs


def build_unit3():
    title = "AP Physics Unit 3: Work, Energy, and Power"
    description = (
        "Work by a constant force, the work-energy theorem, gravitational potential energy, conservation of "
        "mechanical energy, power, and springs — with energy-bar diagrams and $g=10\\,\\mathrm{m/s}^2$."
    )
    concepts = [
        "Work by a constant force",
        "Work-energy theorem",
        "Gravitational potential energy",
        "Conservation of energy",
        "Power",
        "Springs and elastic energy",
    ]

    c1 = concept_block(
        "1. Work by a constant force",
        [
            "In physics, work is not “effort.” Work by a constant force is $W=Fd\\cos\\theta$, where $d$ is the "
            "displacement of the point where the force is applied and $\\theta$ is the angle between $\\vec{F}$ and $\\Delta\\vec{x}$.",
            "If you push $20\\,\\mathrm{N}$ in the same direction as a $3.0\\,\\mathrm{m}$ move, $\\cos 0=1$ and $W=60\\,\\mathrm{J}$. "
            "A joule is a newton-meter: $1\\,\\mathrm{J}=1\\,\\mathrm{N\\cdot m}$.",
            "If $\\theta=90^\\circ$, $\\cos\\theta=0$ and $W=0$. Carrying a backpack horizontally, your upward force does no "
            "work on the pack even though your arms get tired. Tiredness is biology; work is $Fd\\cos\\theta$.",
            "Kinetic friction usually points opposite the displacement, so $\\cos 180^\\circ=-1$ and $W_f=-f_k d$. "
            "Negative work means that force is removing mechanical energy from the object.",
            "Gravity's work depends only on the change in height: $W_g=-mg\\Delta h$ if $h$ increases upward. "
            "Lift a $2\\,\\mathrm{kg}$ book $3\\,\\mathrm{m}$ and gravity does $-60\\,\\mathrm{J}$ while you do $+60\\,\\mathrm{J}$ at constant speed.",
            "Only the component of force along the motion earns work. Resolve $F$ first, then multiply by $d$. "
            "That habit prevents the $60^\\circ$ trap of using $F d$ with no cosine.",
        ],
        "The work-energy theorem is just a bookkeeping of this quantity. If work is muddy, energy conservation will "
        "feel like a slogan instead of a calculation.",
        "Write $\\vec{F}$, write $\\Delta\\vec{x}$, mark $\\theta$, then $W=Fd\\cos\\theta$ with the sign sitting in the cosine.",
        lesson_figure(
            fbd_box(("F_g", "N", "F along Δx"),),
            "Force along the displacement does positive work",
            "When $\\vec{F}$ and $\\Delta\\vec{x}$ point together, $W>0$. Perpendicular forces do zero work.",
        )
        + solved(1, "A $20\\,\\mathrm{N}$ force pushes a crate $3.0\\,\\mathrm{m}$ in the same direction. Find the work by that force.",
                 ["$\\theta=0$, $\\cos 0=1$.",
                  "$W=(20\\,\\mathrm{N})(3.0\\,\\mathrm{m})=60\\,\\mathrm{J}$.",
                  "Units: $\\mathrm{N\\cdot m}=\\mathrm{J}$."],
                 "$60\\,\\mathrm{J}$", "", "Easy")
        + solved(2, "A $50\\,\\mathrm{N}$ pull at $60^\\circ$ above the horizontal moves a box $4.0\\,\\mathrm{m}$ horizontally. Work by the pull?",
                 ["$\\cos 60^\\circ=1/2$.",
                  "$W=50(4)(0.5)=100\\,\\mathrm{J}$.",
                  "The vertical component does no work on a horizontal displacement."],
                 "$100\\,\\mathrm{J}$", "", "Medium")
        + solved(3, "A $5.0\\,\\mathrm{kg}$ box slides $3.0\\,\\mathrm{m}$ on a level floor with $\\mu_k=0.20$. Find work by friction and by gravity ($g=10$).",
                 ["$N=50\\,\\mathrm{N}$, $f_k=10\\,\\mathrm{N}$.",
                  "$W_f=-10(3)=-30\\,\\mathrm{J}$.",
                  "$W_g=0$ because $\\Delta h=0$ (gravity perpendicular to $\\Delta\\vec{x}$).",
                  "Normal force also does zero work (perpendicular)."],
                 "$W_f=-30\\,\\mathrm{J}$, $W_g=0$", "", "Hard"),
        ("Using $W=Fd$ when the force is at an angle",
         "The cosine is not optional. At $90^\\circ$ the work is zero even if $F$ and $d$ are both large."),
        ("Mark $\\theta$ on a sketch of $\\vec{F}$ and $\\Delta\\vec{x}$",
         "If they oppose, $\\theta=180^\\circ$ and work is negative. That sign is how friction drains $K$."),
        [
            "I can compute $W=Fd\\cos\\theta$ with correct units of joules.",
            "I can explain why a perpendicular force does no work.",
            "I can find negative work by kinetic friction.",
        ],
        1,
    )

    c2 = concept_block(
        "2. The work-energy theorem",
        [
            "Kinetic energy is the energy of motion: $K=\\tfrac12 mv^2$. A $4\\,\\mathrm{kg}$ cart at $6\\,\\mathrm{m/s}$ has "
            "$K=72\\,\\mathrm{J}$. Double the speed and $K$ becomes four times larger.",
            "The work-energy theorem: $W_{\\mathrm{net}}=\\Delta K=K_f-K_i$. Net work on an object is exactly the change "
            "in its kinetic energy. Speed up, net work positive; slow down, net work negative.",
            "You can either add the work of every force, or group some forces into potential energy. Both stories must "
            "agree. If $W_{\\mathrm{net}}=+40\\,\\mathrm{J}$, then $K$ rises by $40\\,\\mathrm{J}$.",
            "A $2\\,\\mathrm{kg}$ object going from $8\\,\\mathrm{m/s}$ to $4\\,\\mathrm{m/s}$ has $\\Delta K=\\tfrac12(2)(16-64)=-48\\,\\mathrm{J}$. "
            "Something did $-48\\,\\mathrm{J}$ of net work (often friction).",
            "The theorem is about one object (or one system whose internal energy you are not tracking as heat). "
            "If two objects collide and stick, thermal energy hides inside; then $W_{\\mathrm{net}}=\\Delta K$ for the pair needs care.",
            "On AP Physics 1 you will often use the theorem when a numerical force acts through a known distance, "
            "and use $mgh$ plus $\\tfrac12 mv^2$ when gravity is the star. Both are the same physics in different outfits.",
        ],
        "Conservation of energy is the work-energy theorem plus a decision about which works you rewrite as $\\Delta U$. "
        "That rewrite is the bridge into the next two concepts.",
        "Compute $K_i$ and $K_f$ from speeds. Their difference is $W_{\\mathrm{net}}$. Then ask which forces contributed.",
        lesson_figure(
            energy_bars_svg(ke=1, pe=0, thermal=0),
            "Energy bars just after a push that raised kinetic energy",
            "Net positive work fattens the KE bar. The theorem says that extra height equals $W_{\\mathrm{net}}$.",
        )
        + solved(4, "A $4.0\\,\\mathrm{kg}$ cart goes from rest to $6.0\\,\\mathrm{m/s}$. Find $\\Delta K$ and the required net work.",
                 ["$K_i=0$, $K_f=\\tfrac12(4)(36)=72\\,\\mathrm{J}$.",
                  "$\\Delta K=72\\,\\mathrm{J}$.",
                  "$W_{\\mathrm{net}}=72\\,\\mathrm{J}$."],
                 "$72\\,\\mathrm{J}$", "", "Easy")
        + solved(5, "A $2.0\\,\\mathrm{kg}$ box slows from $8.0\\,\\mathrm{m/s}$ to $4.0\\,\\mathrm{m/s}$. Find net work.",
                 ["$K_i=\\tfrac12(2)(64)=64\\,\\mathrm{J}$.",
                  "$K_f=\\tfrac12(2)(16)=16\\,\\mathrm{J}$.",
                  "$W_{\\mathrm{net}}=16-64=-48\\,\\mathrm{J}$."],
                 "$-48\\,\\mathrm{J}$", "", "Medium")
        + solved(6, "A $5.0\\,\\mathrm{kg}$ sled is pulled $6.0\\,\\mathrm{m}$ by a $20\\,\\mathrm{N}$ horizontal force with $f_k=8.0\\,\\mathrm{N}$, starting from rest. Find the final speed.",
                 ["$W_{\\mathrm{pull}}=20(6)=120\\,\\mathrm{J}$, $W_f=-8(6)=-48\\,\\mathrm{J}$.",
                  "$W_{\\mathrm{net}}=72\\,\\mathrm{J}=\\Delta K=\\tfrac12(5)v^2$.",
                  "$72=2.5 v^2$, so $v^2=28.8$ and $v=\\sqrt{28.8}=2\\sqrt{7.2}\\approx 5.37\\,\\mathrm{m/s}$.",
                  "Cleaner: $v=\\sqrt{2(72)/5}=\\sqrt{28.8}\\,\\mathrm{m/s}$."],
                 "$v=\\sqrt{28.8}\\,\\mathrm{m/s}$", "", "Hard"),
        ("Setting $W_{\\mathrm{net}}=K_f$ and forgetting $K_i$",
         "The theorem uses the change $\\Delta K$. If the object was already moving, subtract $K_i$."),
        ("List every force's work, then add",
         "Pull, friction, gravity, normal. Many are zero. The sum is $\\Delta K$. Skipping friction is the usual miss."),
        [
            "I can compute $K=\\tfrac12 mv^2$ with joules.",
            "I can apply $W_{\\mathrm{net}}=\\Delta K$ including negative work.",
            "I can find a final speed from net work and mass.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Gravitational potential energy",
        [
            "Potential energy is stored energy due to position in a force field. Near Earth we use $U_g=mgh$, where "
            "$h$ is height above a zero you choose. A $3\\,\\mathrm{kg}$ brick $4\\,\\mathrm{m}$ up has $U=120\\,\\mathrm{J}$ if $g=10$.",
            "Only changes $\\Delta U_g=mg\\Delta h$ matter in equations. You may put $h=0$ on the floor, the table, or "
            "the bottom of a ramp. Moving the zero adds the same constant to every $U$, which cancels in $\\Delta U$.",
            "When an object falls, $U_g$ decreases and (without friction) $K$ increases by the same number. "
            "Drop $2\\,\\mathrm{kg}$ through $5\\,\\mathrm{m}$: $\\Delta U=-100\\,\\mathrm{J}$, so $\\Delta K=+100\\,\\mathrm{J}$ and $v=10\\,\\mathrm{m/s}$ from rest.",
            "Gravity is a conservative force in this model: work by gravity between two points depends only on the "
            "height change, not on whether you took a curvy slide or a straight drop.",
            "Negative $U_g$ is legal. If the floor is $h=0$ and a stone is in a $2\\,\\mathrm{m}$ hole, $U=-mg(2)$. "
            "It simply means “below my zero.”",
            "Do not mix $U_g$ with electrical energy or with $mc^2$. On AP Physics 1, $mgh$ is the gravitational story "
            "near Earth's surface, with $g=10\\,\\mathrm{m/s}^2$ unless told otherwise.",
        ],
        "Conservation of energy is mostly $\\Delta K=-\\Delta U_g$ on ramps and pendulums. If $h$ is measured inconsistently, "
        "every speed at the bottom will be fiction.",
        "Write $h=0$ on the diagram in ink. Measure every height from that same line.",
        lesson_figure(
            energy_bars_svg(ke=0, pe=4, thermal=0),
            "A raised object: tall PE bar, empty KE bar",
            "The PE bar's height is $mgh$ relative to your chosen zero. Dropping converts it into KE.",
        )
        + solved(7, "A $3.0\\,\\mathrm{kg}$ brick sits $4.0\\,\\mathrm{m}$ above $h=0$. Find $U_g$ ($g=10$).",
                 ["$U=mgh=3(10)(4)=120\\,\\mathrm{J}$.",
                  "If you moved the zero to the brick, $U$ would read $0$.",
                  "The physics of a later drop uses $\\Delta U$, which would still be $-120\\,\\mathrm{J}$."],
                 "$120\\,\\mathrm{J}$", "", "Easy")
        + solved(8, "A $2.0\\,\\mathrm{kg}$ ball falls $5.0\\,\\mathrm{m}$ from rest. Find impact speed using energy ($g=10$).",
                 ["$mgh=\\tfrac12 mv^2$.",
                  "Mass cancels: $v=\\sqrt{2gh}=\\sqrt{100}=10\\,\\mathrm{m/s}$.",
                  "Check with free fall: $v^2=2(10)(5)=100$."],
                 "$10\\,\\mathrm{m/s}$", "", "Medium")
        + solved(9, "A pendulum bob is pulled aside so it is $0.45\\,\\mathrm{m}$ higher than the bottom. Find speed at the bottom (no drag, $g=10$).",
                 ["$mgh=\\tfrac12 mv^2$.",
                  "$v=\\sqrt{2(10)(0.45)}=\\sqrt{9}=3.0\\,\\mathrm{m/s}$.",
                  "The arc length never entered. Only the height change did.",
                  "If there were drag, $K$ at the bottom would be smaller than $mgh$."],
                 "$3.0\\,\\mathrm{m/s}$", "", "Hard"),
        ("Measuring $h$ along the ramp instead of vertically",
         "$h$ in $mgh$ is vertical height. A $5\\,\\mathrm{m}$ ramp at $30^\\circ$ drops $2.5\\,\\mathrm{m}$, not $5\\,\\mathrm{m}$."),
        ("Mark $h=0$ on the figure before assigning numbers",
         "Then every $U$ value is measured from that mark. Inconsistent zeros are the silent energy bug."),
        [
            "I can compute $U_g=mgh$ relative to a stated zero.",
            "I can convert a height drop into a speed using $mgh=\\tfrac12 mv^2$.",
            "I can explain why only $\\Delta h$, not path shape, matters for gravity's work.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Conservation of energy",
        [
            "Mechanical energy is $E_{\\mathrm{mech}}=K+U$. It is conserved when nonconservative forces do no work "
            "(or we include their work separately). Gravity and ideal springs trade $K$ and $U$ without changing the sum.",
            "A frictionless slide from height $h$ gives $v=\\sqrt{2gh}$ at the bottom, independent of the slide's wiggles. "
            "That is the payoff of a conservative force.",
            "Kinetic friction does negative work and raises thermal energy $E_{\\mathrm{th}}$. Then "
            "$K_i+U_i=K_f+U_f+E_{\\mathrm{th}}$ (with $E_{\\mathrm{th}}=-W_f$ if $W_f$ is negative).",
            "Energy-bar charts make the story visible: a PE bar shrinks, a KE bar grows, and a thermal bar may appear. "
            "The total height of all bars stays the same for an isolated system.",
            "Choose two positions, write $K$ and $U$ at each, and include $W_{\\mathrm{nc}}$ if friction or a motor is present. "
            "That two-line energy audit is the standard AP FRQ layout.",
            "Energy does not care about direction the way momentum does. A pendulum's speed at the bottom is the same "
            "from either side if the starting heights match. (The velocity signs differ.)",
        ],
        "Springs, loops, and later rolling objects are all conservation-of-energy problems with extra $U$ or extra $K$. "
        "The skeleton never changes: before + nonconservative work = after.",
        "Pick point A and point B. Fill $K$ and $U$ at both. Put friction's work on the side that makes $E_{\\mathrm{th}}$ grow.",
        lesson_figure(
            energy_bars_svg(ke=3, pe=1, thermal=1),
            "After a rough slide: some PE became KE, some became thermal",
            "Mechanical energy dropped; total energy (including $E_{\\mathrm{th}}$) did not.",
        )
        + solved(10, "A $2.0\\,\\mathrm{kg}$ block starts from rest $5.0\\,\\mathrm{m}$ above the bottom of a frictionless ramp. Find $v$ at the bottom ($g=10$).",
                 ["$K_i+U_i=K_f+U_f$.",
                  "$0+mgh=\\tfrac12 mv^2+0$.",
                  "$v=\\sqrt{2gh}=\\sqrt{100}=10\\,\\mathrm{m/s}$."],
                 "$10\\,\\mathrm{m/s}$", "", "Easy")
        + solved(11, "The same block loses $20\\,\\mathrm{J}$ to thermal energy on a rough ramp. $U_i=100\\,\\mathrm{J}$. Find $K_f$.",
                 ["$100=K_f+20$.",
                  "$K_f=80\\,\\mathrm{J}$.",
                  "Then $v=\\sqrt{2K/m}=\\sqrt{80}=4\\sqrt{5}\\,\\mathrm{m/s}$ if asked."],
                 "$80\\,\\mathrm{J}$", "", "Medium")
        + solved(12, "A $3.0\\,\\mathrm{kg}$ block slides $5.0\\,\\mathrm{m}$ down a $3$-$4$-$5$ ramp ($\\sin\\theta=0.6$, $\\cos\\theta=0.8$) with $\\mu_k=0.20$, starting from rest. Find $K$ at the bottom ($g=10$).",
                 ["Height drop $h=5(0.6)=3.0\\,\\mathrm{m}$, so $U$ drop $=mgh=90\\,\\mathrm{J}$.",
                  "$N=mg\\cos\\theta=30(0.8)=24\\,\\mathrm{N}$, $f_k=4.8\\,\\mathrm{N}$.",
                  "$W_f=-4.8(5)=-24\\,\\mathrm{J}$, so $E_{\\mathrm{th}}=24\\,\\mathrm{J}$.",
                  "$K_f=90-24=66\\,\\mathrm{J}$."],
                 "$66\\,\\mathrm{J}$", "", "Hard"),
        ("Using ramp length as $h$",
         "Energy needs the vertical drop. Trigonometry converts length to height: $h=L\\sin\\theta$."),
        ("Write a before/after energy table",
         "Rows: $K$, $U_g$, $U_s$, $E_{\\mathrm{th}}$. That table is what graders want to see on an FRQ."),
        [
            "I can state when $K+U$ is constant.",
            "I can include thermal energy when friction does work.",
            "I can solve a ramp speed using height, not path length, plus $W_f$ if needed.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Power",
        [
            "Power is the rate of doing work or transferring energy: $P=W/\\Delta t$. The SI unit is the watt: "
            "$1\\,\\mathrm{W}=1\\,\\mathrm{J/s}$. Doing $100\\,\\mathrm{J}$ in $4\\,\\mathrm{s}$ is $25\\,\\mathrm{W}$.",
            "If a force is aligned with velocity, the instantaneous power is $P=Fv$. A $30\\,\\mathrm{N}$ force on an object "
            "moving at $4\\,\\mathrm{m/s}$ delivers $120\\,\\mathrm{W}$.",
            "At an angle, $P=Fv\\cos\\theta$. Only the parallel component of $\\vec{F}$ contributes, the same cosine as in work.",
            "Lifting at constant speed, $F=mg$ and $P=mgv$. A $20\\,\\mathrm{kg}$ crate lifted at $2\\,\\mathrm{m/s}$ needs "
            "$400\\,\\mathrm{W}$ from the motor (ideal, $g=10$).",
            "Two machines can do the same work; the faster one has larger average power. Time in the denominator is "
            "the whole point of the idea.",
            "On AP FRQs, power often appears as a rated motor: $P=400\\,\\mathrm{W}$ cannot lift $20\\,\\mathrm{kg}$ faster "
            "than $v=P/mg=2\\,\\mathrm{m/s}$ at constant speed.",
        ],
        "Later, electrical power $P=IV$ is a different course. Here, stay with mechanical $P=W/t$ and $P=Fv\\cos\\theta$.",
        "If you have work and time, divide. If you have force and speed, multiply with the cosine.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", sample_curve(lambda t: 12 * t, 0, 4))],
                points=[(4, 48, "P grows")],
                xlim=(-0.3, 5), ylim=(-4, 56), xlab="t (s)", ylab="P (W)", w=300, h=240,
            ),
            "Instantaneous power $P=Fv$ while speeding up under constant $F$",
            "If $F$ is constant, $v$ rises linearly and so does $P$. Average power is less than the final $P$.",
        )
        + solved(13, "A motor does $100\\,\\mathrm{J}$ of work in $4.0\\,\\mathrm{s}$. Find average power.",
                 ["$P=W/t=100/4=25\\,\\mathrm{W}$.",
                  "Units: $\\mathrm{J/s}=\\mathrm{W}$.",
                  "That is a small motor compared with a $1000\\,\\mathrm{W}$ hair dryer."],
                 "$25\\,\\mathrm{W}$", "", "Easy")
        + solved(14, "Lift a $20\\,\\mathrm{kg}$ crate $3.0\\,\\mathrm{m}$ at constant speed in $6.0\\,\\mathrm{s}$. Find average power ($g=10$).",
                 ["$W=mgh=20(10)(3)=600\\,\\mathrm{J}$.",
                  "$P=600/6=100\\,\\mathrm{W}$.",
                  "Or $v=0.50\\,\\mathrm{m/s}$, $P=mgv=200(0.50)=100\\,\\mathrm{W}$."],
                 "$100\\,\\mathrm{W}$", "", "Medium")
        + solved(15, "A $40\\,\\mathrm{N}$ force at $60^\\circ$ to the velocity $5.0\\,\\mathrm{m/s}$ — find instantaneous power. Then find how far the object would move in $4.0\\,\\mathrm{s}$ if $v$ stayed $5.0\\,\\mathrm{m/s}$.",
                 ["$P=Fv\\cos 60^\\circ=40(5)(0.5)=100\\,\\mathrm{W}$.",
                  "At constant $v$, $d=vt=20\\,\\mathrm{m}$.",
                  "$W=P t=400\\,\\mathrm{J}$, which matches $Fd\\cos\\theta=40(20)(0.5)=400\\,\\mathrm{J}$.",
                  "The two power formulas agree."],
                 "$P=100\\,\\mathrm{W}$; $d=20\\,\\mathrm{m}$", "", "Hard"),
        ("Saying power is zero because $a=0$",
         "At constant speed you can still do work against friction or gravity. Power can be nonzero while $a=0$."),
        ("Match the formula to the givens",
         "$W/t$ when energy and time are known. $Fv\\cos\\theta$ when force and velocity are known. Do not mix the two blindly."),
        [
            "I can compute average power as $W/\\Delta t$ in watts.",
            "I can use $P=Fv\\cos\\theta$ for instantaneous mechanical power.",
            "I can find a lift speed from a motor rating using $P=mgv$.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Springs and elastic energy",
        [
            "An ideal spring pulls or pushes toward equilibrium with $F_s=-kx$ (Hooke's law). The minus sign means "
            "restoring: stretch to the right, force to the left. If $k=50\\,\\mathrm{N/m}$ and $x=0.20\\,\\mathrm{m}$, $|F|=10\\,\\mathrm{N}$.",
            "The stiffness $k$ is in $\\mathrm{N/m}$. A large $k$ is a stiff spring. Energy stored is $U_s=\\tfrac12 kx^2$. "
            "For $k=200\\,\\mathrm{N/m}$ and $x=0.10\\,\\mathrm{m}$, $U_s=1.0\\,\\mathrm{J}$.",
            "Because $U_s$ depends on $x^2$, doubling the stretch quadruples the energy. That is a favorite multiple-choice twist.",
            "On frictionless ice, a compressed spring can give all of $U_s$ to $K$: $\\tfrac12 kx^2=\\tfrac12 mv^2$, so "
            "$v=x\\sqrt{k/m}$. A $4\\,\\mathrm{kg}$ block, $k=400\\,\\mathrm{N/m}$, $x=0.20\\,\\mathrm{m}$ leaves at $2.0\\,\\mathrm{m/s}$.",
            "The spring force is conservative, so you may use $U_s$ in energy equations just like $U_g$. Work by the "
            "spring is $-\\Delta U_s$.",
            "Unit 7 will put this mass on the spring and let it oscillate. The energy story stays $E=\\tfrac12 kA^2=K+U_s$ "
            "at every moment. Learn $U_s$ now and SHM energy will feel familiar.",
        ],
        "Oscillations, energy of rotating systems with torsion, and many FRQ launchers are spring problems. "
        "Hooke's law plus $\\tfrac12 kx^2$ is the whole algebraic toolkit.",
        "Measure $x$ from equilibrium, not from the end of the table. Then $U_s=\\tfrac12 kx^2$ and $F=-kx$.",
        lesson_figure(
            spring_mass_svg(),
            "Horizontal spring-mass with equilibrium at the dashed line",
            "Displacement $x$ is from $x=0$, not from the wall. Energy $\\tfrac12 kx^2$ uses that same $x$.",
        )
        + solved(16, "A spring with $k=200\\,\\mathrm{N/m}$ is stretched $0.10\\,\\mathrm{m}$. Find $U_s$.",
                 ["$U=\\tfrac12 kx^2=\\tfrac12(200)(0.01)=1.0\\,\\mathrm{J}$.",
                  "Force magnitude $|F|=kx=20\\,\\mathrm{N}$ if asked.",
                  "Units: $(\\mathrm{N/m})(\\mathrm{m}^2)=\\mathrm{N\\cdot m}=\\mathrm{J}$."],
                 "$1.0\\,\\mathrm{J}$", "", "Easy")
        + solved(17, "A $4.0\\,\\mathrm{kg}$ block compresses $k=400\\,\\mathrm{N/m}$ by $0.20\\,\\mathrm{m}$ and is released on frictionless ice. Find max speed.",
                 ["$\\tfrac12 kx^2=\\tfrac12 mv^2$.",
                  "$v=x\\sqrt{k/m}=0.20\\sqrt{400/4}=0.20\\sqrt{100}=2.0\\,\\mathrm{m/s}$.",
                  "Max speed is at equilibrium, where $U_s=0$ and $K$ is largest."],
                 "$2.0\\,\\mathrm{m/s}$", "", "Medium")
        + solved(18, "A spring $k=200\\,\\mathrm{N/m}$ launches a $0.50\\,\\mathrm{kg}$ block from $x=0.20\\,\\mathrm{m}$ compression up a frictionless slope. How high does the block rise? ($g=10$)",
                 ["$\\tfrac12 kx^2=mgh$ at the highest point (momentarily at rest along the track).",
                  "$\\tfrac12(200)(0.04)=4.0\\,\\mathrm{J}=0.50(10)h=5h$.",
                  "$h=0.80\\,\\mathrm{m}$.",
                  "The slope angle never entered because there is no friction."],
                 "$0.80\\,\\mathrm{m}$", "", "Hard"),
        ("Measuring $x$ from the unstretched length when a hanging mass already stretched it to a new equilibrium",
         "For oscillation energy, $x$ is from the hanging equilibrium. For a launch on a table, $x$ is from the unstretched length if that is the force-free point. Read which equilibrium the problem uses."),
        ("Use energy when you want speed or height; use $F=-kx$ when you want acceleration at one position",
         "$F=ma$ at a single $x$ gives $a=-kx/m$. Energy connects two positions without finding $a$."),
        [
            "I can use Hooke's law $F=-kx$ with the restoring direction.",
            "I can compute $U_s=\\tfrac12 kx^2$ and scale it when $x$ doubles.",
            "I can convert spring energy into kinetic or gravitational energy.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Linear Momentum
# ===========================================================================

def _u4_questions():
    qs = []
    _add(qs, [
        ("Momentum is $\\vec{p}=m\\vec{v}$. A $5.0\\,\\mathrm{kg}$ cart at $6.0\\,\\mathrm{m/s}$ east has momentum",
         "$30\\,\\mathrm{kg\\cdot m/s}$ east",
         "$p=(5)(6)=30\\,\\mathrm{kg\\cdot m/s}$ in the velocity direction.",
         ["$1.2\\,\\mathrm{kg\\cdot m/s}$ east", "$11\\,\\mathrm{kg\\cdot m/s}$ east", "$30\\,\\mathrm{N}$ east"]),
        ("Impulse is $J=F_{\\mathrm{avg}}\\Delta t$, equal to $\\Delta p$. A $8.0\\,\\mathrm{N}$ force for $0.50\\,\\mathrm{s}$ delivers",
         "$4.0\\,\\mathrm{N\\cdot s}$",
         "$J=(8)(0.50)=4.0\\,\\mathrm{N\\cdot s}$, which is also $4.0\\,\\mathrm{kg\\cdot m/s}$ of $\\Delta p$.",
         ["$16\\,\\mathrm{N\\cdot s}$", "$8.5\\,\\mathrm{N\\cdot s}$", "$0.0625\\,\\mathrm{N\\cdot s}$"]),
        ("A $2.0\\,\\mathrm{kg}$ ball changes velocity from $3.0\\,\\mathrm{m/s}$ east to $5.0\\,\\mathrm{m/s}$ west. $\\Delta p$ is",
         "$16\\,\\mathrm{kg\\cdot m/s}$ west",
         "Take east positive: $p_i=+6$, $p_f=-10$, $\\Delta p=-16\\,\\mathrm{kg\\cdot m/s}$ (west).",
         ["$4\\,\\mathrm{kg\\cdot m/s}$ west", "$16\\,\\mathrm{kg\\cdot m/s}$ east", "$2\\,\\mathrm{kg\\cdot m/s}$ west"]),
        ("Softening a landing increases $\\Delta t$ so that for the same $\\Delta p$ the average force",
         "decreases",
         "$F_{\\mathrm{avg}}=\\Delta p/\\Delta t$. Longer time, smaller force. That is why airbags work.",
         ["increases", "is unchanged", "becomes zero"]),
        ("The area under an $F$-$t$ graph is",
         "impulse (and therefore $\\Delta p$)",
         "On AP Physics 1 you compute the geometric area of the $F$-$t$ shape; that area equals $\\Delta p$.",
         ["work", "kinetic energy", "mass"]),
    ])
    _add(qs, [
        ("If the net external impulse on a system is zero, the system's total momentum is",
         "conserved (constant)",
         "Internal impulses cancel by Newton's third law. Isolated system: $\\vec{p}_{\\mathrm{tot}}$ stays put.",
         ["zero always", "equal to total $K$", "undefined"]),
        ("Cart $4.0\\,\\mathrm{kg}$ at $6.0\\,\\mathrm{m/s}$ catches a $2.0\\,\\mathrm{kg}$ cart at rest and they stick. Common speed is",
         "$4.0\\,\\mathrm{m/s}$",
         "$24+0=6v$, $v=4.0\\,\\mathrm{m/s}$ in the original direction.",
         ["$6.0\\,\\mathrm{m/s}$", "$3.0\\,\\mathrm{m/s}$", "$12\\,\\mathrm{m/s}$"]),
        ("A $3.0\\,\\mathrm{kg}$ clay at $8.0\\,\\mathrm{m/s}$ hits $5.0\\,\\mathrm{kg}$ clay at rest and they stick. $v_f$ is",
         "$3.0\\,\\mathrm{m/s}$",
         "$24=8v_f$, $v_f=3.0\\,\\mathrm{m/s}$.",
         ["$8.0\\,\\mathrm{m/s}$", "$5.0\\,\\mathrm{m/s}$", "$0$"]),
        ("Two skaters push apart at rest. If $40\\,\\mathrm{kg}$ moves $3.0\\,\\mathrm{m/s}$ left, the $60\\,\\mathrm{kg}$ skater moves",
         "$2.0\\,\\mathrm{m/s}$ right",
         "$0=40(-3)+60v$, $v=2.0\\,\\mathrm{m/s}$ right.",
         ["$3.0\\,\\mathrm{m/s}$ right", "$2.0\\,\\mathrm{m/s}$ left", "$0$"]),
        ("Momentum conservation requires you to",
         "choose a closed system and a consistent sign convention",
         "If Earth is left out while friction is large, momentum of the cart alone is not conserved.",
         ["ignore mass", "set $K$ constant always", "use $g=9.8$ only"]),
    ])
    _add(qs, [
        ("A 1D elastic collision also conserves kinetic energy. Equal masses swapping velocities is the",
         "standard elastic result for $m_1=m_2$ in one dimension",
         "The incoming mass stops (if the target was at rest) and the target takes $v_1$.",
         ["inelastic result", "explosion result", "impossible"]),
        ("A $2.0\\,\\mathrm{kg}$ cart at $6.0\\,\\mathrm{m/s}$ elastically hits a resting $2.0\\,\\mathrm{kg}$ cart. Afterward the first cart's speed is",
         "$0$",
         "Equal-mass 1D elastic, target at rest: velocities exchange. First stops, second goes $6.0\\,\\mathrm{m/s}$.",
         ["$6.0\\,\\mathrm{m/s}$", "$3.0\\,\\mathrm{m/s}$", "$12\\,\\mathrm{m/s}$"]),
        ("Relative speed of separation equals relative speed of approach for a 1D elastic collision. If approach is $10\\,\\mathrm{m/s}$, separation is",
         "$10\\,\\mathrm{m/s}$",
         "That is the elastic extra rule besides momentum conservation.",
         ["$0$", "$5\\,\\mathrm{m/s}$", "$20\\,\\mathrm{m/s}$"]),
        ("In a perfectly elastic collision, which is conserved?",
         "both momentum and kinetic energy of the system",
         "That is the definition in the AP model (no sound, no heat, no deformation leftover).",
         ["only momentum", "only $K$", "neither"]),
        ("A light ball bouncing off a heavy wall elastically with incoming speed $v$ rebounds at",
         "about $v$ the other way (wall barely moves)",
         "$\\Delta p\\approx 2mv$ for the ball. The Earth-wall takes the opposite impulse.",
         ["$0$", "$v/2$", "$2v$ the same way"]),
    ])
    _add(qs, [
        ("A perfectly inelastic collision is one where the objects",
         "stick together and move with a common velocity",
         "Momentum is conserved (if isolated); kinetic energy is not — some becomes thermal/deformation.",
         ["bounce with $K$ conserved", "never touch", "must have equal mass"]),
        ("$4.0\\,\\mathrm{kg}$ at $6.0\\,\\mathrm{m/s}$ sticks to $2.0\\,\\mathrm{kg}$ at rest. $K$ before is $72\\,\\mathrm{J}$; $K$ after is",
         "$48\\,\\mathrm{J}$",
         "$v=4.0\\,\\mathrm{m/s}$, $K_f=\\tfrac12(6)(16)=48\\,\\mathrm{J}$. Lost $24\\,\\mathrm{J}$.",
         ["$72\\,\\mathrm{J}$", "$24\\,\\mathrm{J}$", "$96\\,\\mathrm{J}$"]),
        ("The fraction of $K$ remaining after a 1D stick of mass $m$ into $M$ at rest is",
         "$m/(m+M)$",
         "$v=m u/(m+M)$, $K_f/K_i=m/(m+M)$.",
         ["$M/(m+M)$", "$1$", "$0$ always"]),
        ("Why is $K$ not conserved when clay sticks?",
         "deformation and thermal energy store the missing $K$",
         "Momentum still balances; energy hid in the mess.",
         ["momentum failed", "mass vanished", "time reversed"]),
        ("Two identical gliders approach at $\\pm 4.0\\,\\mathrm{m/s}$ and stick. Final velocity is",
         "$0$",
         "Total $p=0$, so $v_f=0$. All $K$ became thermal.",
         ["$4.0\\,\\mathrm{m/s}$", "$8.0\\,\\mathrm{m/s}$", "$2.0\\,\\mathrm{m/s}$"]),
    ])
    _add(qs, [
        ("The center of mass of two objects on a line is $x_{\\mathrm{cm}}=(m_1 x_1+m_2 x_2)/(m_1+m_2)$. For $2\\,\\mathrm{kg}$ at $x=0$ and $4\\,\\mathrm{kg}$ at $x=6\\,\\mathrm{m}$, $x_{\\mathrm{cm}}$ is",
         "$4.0\\,\\mathrm{m}$",
         "$(0+24)/6=4.0\\,\\mathrm{m}$, closer to the heavier mass.",
         ["$3.0\\,\\mathrm{m}$", "$6.0\\,\\mathrm{m}$", "$2.0\\,\\mathrm{m}$"]),
        ("If no external force acts, the center of mass",
         "moves at constant velocity (which may be zero)",
         "The CM follows Newton's first law for the system.",
         ["must sit at the geometric middle", "accelerates toward the heavier mass", "stops during collisions"]),
        ("During an isolated collision, the CM velocity",
         "does not jump; it stays the same before and after",
         "Internal impulses cancel. $v_{\\mathrm{cm}}=p_{\\mathrm{tot}}/M$ is constant.",
         ["becomes zero", "equals the faster object's $v$", "is undefined"]),
        ("$3.0\\,\\mathrm{kg}$ at $2.0\\,\\mathrm{m/s}$ and $1.0\\,\\mathrm{kg}$ at $6.0\\,\\mathrm{m/s}$, same direction. $v_{\\mathrm{cm}}$ is",
         "$3.0\\,\\mathrm{m/s}$",
         "$p_{\\mathrm{tot}}=6+6=12$, $M=4$, $v_{\\mathrm{cm}}=3.0\\,\\mathrm{m/s}$.",
         ["$4.0\\,\\mathrm{m/s}$", "$8.0\\,\\mathrm{m/s}$", "$2.0\\,\\mathrm{m/s}$"]),
        ("A $1.0\\,\\mathrm{m}$ uniform rod has CM at",
         "its geometric center, $0.50\\,\\mathrm{m}$ from either end",
         "Uniform density: CM at the midpoint.",
         ["an end", "$0.25\\,\\mathrm{m}$ from the heavy paint", "outside the rod"]),
    ])
    _add(qs, [
        ("An explosion of a resting object into two pieces is a reverse inelastic collision: total $p$ stays",
         "$0$ if it started at rest (isolated)",
         "The pieces fly opposite ways so $m_1 v_1+m_2 v_2=0$.",
         ["equal to the chemical energy", "infinite", "equal to $K$"]),
        ("A $4.0\\,\\mathrm{kg}$ firework at rest splits into $1.0\\,\\mathrm{kg}$ at $12\\,\\mathrm{m/s}$ east. The $3.0\\,\\mathrm{kg}$ piece goes",
         "$4.0\\,\\mathrm{m/s}$ west",
         "$0=1(12)+3v$, $v=-4.0\\,\\mathrm{m/s}$.",
         ["$12\\,\\mathrm{m/s}$ west", "$4.0\\,\\mathrm{m/s}$ east", "$3.0\\,\\mathrm{m/s}$ west"]),
        ("Kinetic energy after an explosion compared with before (object at rest) is",
         "larger; chemical/elastic energy became $K$",
         "Momentum can still be zero while $K$ is not.",
         ["smaller always", "the same", "zero"]),
        ("A person on ice throws a $2.0\\,\\mathrm{kg}$ brick at $10\\,\\mathrm{m/s}$. If the person+skates mass is $40\\,\\mathrm{kg}$, recoil speed is",
         "$0.50\\,\\mathrm{m/s}$ opposite the throw",
         "$0=2(10)+40v$, $v=-0.50\\,\\mathrm{m/s}$.",
         ["$10\\,\\mathrm{m/s}$", "$5.0\\,\\mathrm{m/s}$", "$0$"]),
        ("Gun-and-bullet recoil is the same idea as",
         "an explosion of a two-piece system that started at rest",
         "Forward $p$ of the bullet, backward $p$ of the gun.",
         ["an elastic bounce with $K$ conserved necessarily", "a third-law violation", "a massless bullet"]),
    ])
    _add(qs, [
        ("A $0.20\\,\\mathrm{kg}$ ball at $15\\,\\mathrm{m/s}$ is caught in $0.030\\,\\mathrm{s}$. Average force magnitude is",
         "$100\\,\\mathrm{N}$",
         "$\\Delta p=3.0\\,\\mathrm{kg\\cdot m/s}$, $F=\\Delta p/\\Delta t=100\\,\\mathrm{N}$.",
         ["$3.0\\,\\mathrm{N}$", "$0.45\\,\\mathrm{N}$", "$75\\,\\mathrm{N}$"]),
        ("If the catch takes $0.10\\,\\mathrm{s}$ instead, average force becomes",
         "$30\\,\\mathrm{N}$",
         "Same $\\Delta p$, longer time: $3.0/0.10=30\\,\\mathrm{N}$.",
         ["$100\\,\\mathrm{N}$ still", "$300\\,\\mathrm{N}$", "$3.0\\,\\mathrm{N}$"]),
        ("A $1500\\,\\mathrm{kg}$ car at $20\\,\\mathrm{m/s}$ hits a wall and stops. Impulse from the wall has magnitude",
         "$3.0\\times 10^4\\,\\mathrm{N\\cdot s}$",
         "$\\Delta p=30000\\,\\mathrm{kg\\cdot m/s}$.",
         ["$75\\,\\mathrm{N\\cdot s}$", "$1520\\,\\mathrm{N\\cdot s}$", "$0$"]),
        ("Glider $m$ at $v$ hits resting glider $2m$ and they stick. $v_f$ is",
         "$v/3$",
         "$mv=(3m)v_f$, $v_f=v/3$.",
         ["$v/2$", "$2v/3$", "$v$"]),
        ("$K$ remaining in that stick, as a fraction of original $K$, is",
         "$1/3$",
         "$K_f/K_i=m/(m+2m)=1/3$.",
         ["$2/3$", "$1$", "$0$"]),
        ("Elastic, equal mass, target at rest: the target's speed afterward equals",
         "the incoming speed of the first mass",
         "Velocity exchange.",
         ["half the incoming speed", "zero", "twice the incoming speed"]),
        ("Two pieces $m$ and $2m$ explode from rest. If $m$ goes $6.0\\,\\mathrm{m/s}$, $2m$ goes",
         "$3.0\\,\\mathrm{m/s}$ the other way",
         "$m(6)+2m(v)=0$, $v=-3.0\\,\\mathrm{m/s}$.",
         ["$6.0\\,\\mathrm{m/s}$ the other way", "$12\\,\\mathrm{m/s}$", "$2.0\\,\\mathrm{m/s}$"]),
        ("CM of $1\\,\\mathrm{kg}$ at $x=2\\,\\mathrm{m}$ and $3\\,\\mathrm{kg}$ at $x=6\\,\\mathrm{m}$ is at",
         "$5.0\\,\\mathrm{m}$",
         "$(2+18)/4=5.0\\,\\mathrm{m}$.",
         ["$4.0\\,\\mathrm{m}$", "$6.0\\,\\mathrm{m}$", "$2.0\\,\\mathrm{m}$"]),
        ("A $F$-$t$ triangle peaks at $20\\,\\mathrm{N}$ and lasts $0.40\\,\\mathrm{s}$. Impulse is",
         "$4.0\\,\\mathrm{N\\cdot s}$",
         "Triangle area $\\tfrac12(0.40)(20)=4.0\\,\\mathrm{N\\cdot s}$.",
         ["$8.0\\,\\mathrm{N\\cdot s}$", "$20\\,\\mathrm{N\\cdot s}$", "$0.40\\,\\mathrm{N\\cdot s}$"]),
        ("A $0.40\\,\\mathrm{kg}$ hockey puck at $5.0\\,\\mathrm{m/s}$ rebounds elastically from a heavy board at $5.0\\,\\mathrm{m/s}$ the other way. $|\\Delta p|$ is",
         "$4.0\\,\\mathrm{kg\\cdot m/s}$",
         "$p_i=+2.0$, $p_f=-2.0$, $\\Delta p=-4.0\\,\\mathrm{kg\\cdot m/s}$.",
         ["$2.0\\,\\mathrm{kg\\cdot m/s}$", "$0$", "$8.0\\,\\mathrm{kg\\cdot m/s}$"]),
        ("Throwing sand backward from a cart (no external horizontal force) makes the cart",
         "speed up forward",
         "The sand's backward momentum is balanced by extra forward momentum of the cart.",
         ["slow down", "stop instantly", "gain mass and slow always"]),
        ("Which collision conserves $K$ of the two-object system in the AP idealization?",
         "perfectly elastic",
         "Inelastic (especially perfectly inelastic) convert some $K$ to other forms.",
         ["perfectly inelastic", "any stick-together crash", "any explosion"]),
        ("A $2.0\\,\\mathrm{kg}$ fish at $1.0\\,\\mathrm{m/s}$ swallows a $0.50\\,\\mathrm{kg}$ fish at rest. Their speed is",
         "$0.80\\,\\mathrm{m/s}$",
         "$2.0=2.5 v$, $v=0.80\\,\\mathrm{m/s}$.",
         ["$1.0\\,\\mathrm{m/s}$", "$0.50\\,\\mathrm{m/s}$", "$1.5\\,\\mathrm{m/s}$"]),
        ("If the little fish had been swimming toward the big one at $1.0\\,\\mathrm{m/s}$, $v_f$ after swallowing would be",
         "$0.60\\,\\mathrm{m/s}$ in the big fish's original direction",
         "$p=2.0(1.0)+0.50(-1.0)=1.5$, $v=1.5/2.5=0.60\\,\\mathrm{m/s}$.",
         ["$0$", "$1.0\\,\\mathrm{m/s}$", "$0.80\\,\\mathrm{m/s}$"]),
        ("A catcher's mitt stops a $0.25\\,\\mathrm{kg}$ baseball from $8.0\\,\\mathrm{m/s}$ in $0.050\\,\\mathrm{s}$. Average force magnitude is",
         "$40\\,\\mathrm{N}$",
         "$\\Delta p=mv=2.0\\,\\mathrm{kg\\cdot m/s}$. Then $F_{\\mathrm{avg}}=\\Delta p/\\Delta t=40\\,\\mathrm{N}$.",
         ["$2.0\\,\\mathrm{N}$", "$0.40\\,\\mathrm{N}$", "$160\\,\\mathrm{N}$"]),
        ("Two identical clay lumps of mass $m$ approach at $+u$ and $-u$ and stick together. Combined speed afterward is",
         "$0$",
         "Momenta cancel: $mu-mu=0$. The blobs stop as a combined lump.",
         ["$u$", "$u/2$", "$2u$"]),
        ("AP Stretch: A $0.020\\,\\mathrm{kg}$ dart at $250\\,\\mathrm{m/s}$ embeds in a $0.48\\,\\mathrm{kg}$ cart at rest on ice. Combined speed is",
         "$10\\,\\mathrm{m/s}$",
         "$p_i=5.0\\,\\mathrm{kg\\cdot m/s}=(0.50)v$, so $v=10\\,\\mathrm{m/s}$. Kinetic energy falls from $625\\,\\mathrm{J}$ to $25\\,\\mathrm{J}$.",
         ["$250\\,\\mathrm{m/s}$", "$5.0\\,\\mathrm{m/s}$", "$0$"]),
        ("AP Stretch: A $0.050\\,\\mathrm{kg}$ dart at $80\\,\\mathrm{m/s}$ embeds in a $1.95\\,\\mathrm{kg}$ wood block at rest, then the pair slides up a frictionless slope. Height reached is ($g=10$)",
         "$0.20\\,\\mathrm{m}$",
         "$p_i=4.0=(2.00)v$, so $v=2.0\\,\\mathrm{m/s}$. Then $h=v^2/(2g)=4/20=0.20\\,\\mathrm{m}$.",
         ["$8.0\\,\\mathrm{m}$ using the dart's $v$ alone", "$2.0\\,\\mathrm{m}$", "$0.080\\,\\mathrm{m}$"]),
        ("AP Stretch: Two carts $m$ and $2m$ approach with velocities $+v$ and $-v$. They stick. $v_f$ is",
         "$-v/3$",
         "$p=mv-2mv=-mv$, $M=3m$, $v_f=-v/3$.",
         ["$0$", "$+v/3$", "$-v$"]),
        ("AP Stretch: A $5.0\\,\\mathrm{kg}$ cart at rest is pushed $20\\,\\mathrm{N}$ for $0.30\\,\\mathrm{s}$, then $10\\,\\mathrm{N}$ opposite for $0.20\\,\\mathrm{s}$. Speed afterward, and the distance it coasts in the next $2.0\\,\\mathrm{s}$ on ice, are",
         "$0.80\\,\\mathrm{m/s}$, $1.6\\,\\mathrm{m}$",
         "Net impulse $6.0-2.0=4.0\\,\\mathrm{N\\cdot s}$, so $v=4.0/5.0=0.80\\,\\mathrm{m/s}$. Coasting: $\\Delta x=(0.80)(2.0)=1.6\\,\\mathrm{m}$.",
         ["$1.2\\,\\mathrm{m/s}$, $2.4\\,\\mathrm{m}$ (first pulse only)", "$0.40\\,\\mathrm{m/s}$, $0.80\\,\\mathrm{m}$", "$4.0\\,\\mathrm{m/s}$, $8.0\\,\\mathrm{m}$"]),
        ("AP Stretch: In the CM frame of an isolated two-cart collision, total momentum is",
         "$0$",
         "That is the definition of the CM frame: $v'_{\\mathrm{cm}}=0$, so $p'_{\\mathrm{tot}}=0$.",
         ["$mv_{\\mathrm{cm}}$", "infinite", "equal to $K$"]),
        ("AP Stretch: A $4.0\\,\\mathrm{kg}$ glider at $6.0\\,\\mathrm{m/s}$ hits a $2.0\\,\\mathrm{kg}$ glider at rest elastically in 1D. The two speeds after the bounce are",
         "$2.0\\,\\mathrm{m/s}$ and $8.0\\,\\mathrm{m/s}$",
         "$v_{1f}=(m_1-m_2)v_1/(m_1+m_2)=(2/6)(6)=2.0\\,\\mathrm{m/s}$, $v_{2f}=2 m_1 v_1/(m_1+m_2)=8.0\\,\\mathrm{m/s}$.",
         ["$6.0\\,\\mathrm{m/s}$ and $0$", "$4.0\\,\\mathrm{m/s}$ and $4.0\\,\\mathrm{m/s}$", "$-2.0\\,\\mathrm{m/s}$ and $6.0\\,\\mathrm{m/s}$"]),
        ("AP Stretch: A $4.0\\,\\mathrm{kg}$ glider at $6.0\\,\\mathrm{m/s}$ collides elastically in 1D with a $2.0\\,\\mathrm{kg}$ glider at rest. Kinetic energy of the pair after the bounce is",
         "$72\\,\\mathrm{J}$, equal to $K$ before",
         "$K_i=\\tfrac12(4)(36)=72\\,\\mathrm{J}$. After: $\\tfrac12(4)(4)+\\tfrac12(2)(64)=8+64=72\\,\\mathrm{J}$. Elastic means $K$ matches.",
         ["$36\\,\\mathrm{J}$", "$0$", "$144\\,\\mathrm{J}$"]),
        ("AP Stretch: A balloon releases air to the left. The balloon moves right because",
         "the system of balloon+air conserves momentum; air's left $p$ requires balloon right $p$",
         "This is an explosion-like thrust, not a violation of Newton's laws.",
         ["air has no mass", "a third-law failure", "the balloon's mass increased"]),
        ("AP Stretch: A $6.0\\,\\mathrm{kg}$ crate sliding at $4.0\\,\\mathrm{m/s}$ on ice feels $9.0\\,\\mathrm{N}$ of friction for $2.0\\,\\mathrm{s}$, then ice is frictionless. Speed after those $2.0\\,\\mathrm{s}$, and extra friction time that would have been needed to stop it from $4.0\\,\\mathrm{m/s}$, are",
         "$1.0\\,\\mathrm{m/s}$, $0.67\\,\\mathrm{s}$",
         "Impulse $18\\,\\mathrm{N\\cdot s}$ removes $18$ of the original $p=24$. Leftover $p=6.0$, $v=1.0\\,\\mathrm{m/s}$. Full stop needs $t=24/9=2.67\\,\\mathrm{s}$, so $0.67\\,\\mathrm{s}$ more.",
         ["$4.0\\,\\mathrm{m/s}$, $0$", "$0$, $2.0\\,\\mathrm{s}$", "$2.0\\,\\mathrm{m/s}$, $1.0\\,\\mathrm{s}$"]),
    ])
    return qs


def build_unit4():
    title = "AP Physics Unit 4: Linear Momentum"
    description = (
        "Momentum and impulse, conservation of momentum, elastic and inelastic collisions, center of mass, "
        "and explosions — algebra-based AP Physics 1 with sign conventions and energy comparisons."
    )
    concepts = [
        "Momentum and impulse",
        "Conservation of momentum",
        "Elastic collisions",
        "Inelastic collisions",
        "Center of mass",
        "Explosions",
    ]

    c1 = concept_block(
        "1. Momentum and impulse",
        [
            "Momentum is inertia in motion: $\\vec{p}=m\\vec{v}$. It has direction. A $5\\,\\mathrm{kg}$ cart at $6\\,\\mathrm{m/s}$ east "
            "has $p=30\\,\\mathrm{kg\\cdot m/s}$ east. Twice the mass at the same velocity means twice the momentum.",
            "Impulse is a push lasting a time: $\\vec{J}=\\vec{F}_{\\mathrm{avg}}\\Delta t$. It equals the change in momentum: "
            "$\\vec{J}=\\Delta\\vec{p}$. A $8\\,\\mathrm{N}$ force for $0.50\\,\\mathrm{s}$ delivers $4.0\\,\\mathrm{N\\cdot s}$ of impulse.",
            "The units $\\mathrm{N\\cdot s}$ and $\\mathrm{kg\\cdot m/s}$ are the same. That equality is the impulse-momentum theorem, "
            "which is Newton's second law multiplied through by $\\Delta t$.",
            "Softening a landing lengthens $\\Delta t$ so $F_{\\mathrm{avg}}=\\Delta p/\\Delta t$ drops. Bending your knees, "
            "airbags, and crumple zones are all longer-time, smaller-force stories with the same $\\Delta p$.",
            "The area under an $F$-versus-$t$ graph is impulse. A triangular pulse of peak $20\\,\\mathrm{N}$ lasting $0.40\\,\\mathrm{s}$ "
            "has area $4.0\\,\\mathrm{N\\cdot s}$.",
            "Signs matter: a ball going east that rebounds west has a large $\\Delta p$ because the two momenta subtract. "
            "Catching the ball (stopping it) is a smaller $\\Delta p$ than reversing it.",
        ],
        "Collisions are just large impulses over short times. If impulse is clear, conservation of momentum is the "
        "same law with internal pairs canceling.",
        "Write $p_i$ and $p_f$ with a sign convention. Subtract to get $\\Delta p$. Then $F_{\\mathrm{avg}}=\\Delta p/\\Delta t$ if time is given.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", [(0, 0), (0.1, 20), (0.4, 0)])],
                points=[(0.1, 20, "peak F")],
                xlim=(-0.05, 0.5), ylim=(-2, 24), xlab="t (s)", ylab="F (N)", w=320, h=240,
            ),
            "A short force pulse; area is impulse",
            "Triangle area $\\tfrac12$ base times height equals $J=\\Delta p$.",
        )
        + solved(1, "A $5.0\\,\\mathrm{kg}$ cart moves at $6.0\\,\\mathrm{m/s}$ east. Find its momentum.",
                 ["$p=mv=(5)(6)=30\\,\\mathrm{kg\\cdot m/s}$.",
                  "Direction: east, with the velocity.",
                  "If it later stopped, $\\Delta p=-30\\,\\mathrm{kg\\cdot m/s}$."],
                 "$30\\,\\mathrm{kg\\cdot m/s}$ east", "", "Easy")
        + solved(2, "An $8.0\\,\\mathrm{N}$ force acts for $0.50\\,\\mathrm{s}$ on a $2.0\\,\\mathrm{kg}$ cart that started at rest. Find impulse and final speed.",
                 ["$J=F\\Delta t=4.0\\,\\mathrm{N\\cdot s}=\\Delta p$.",
                  "$\\Delta p=m\\Delta v=2 v_f$, so $v_f=2.0\\,\\mathrm{m/s}$.",
                  "Direction matches the force."],
                 "$J=4.0\\,\\mathrm{N\\cdot s}$, $v=2.0\\,\\mathrm{m/s}$", "", "Medium")
        + solved(3, "A $0.20\\,\\mathrm{kg}$ ball at $15\\,\\mathrm{m/s}$ is caught in $0.030\\,\\mathrm{s}$. Find average force. Compare with a $0.10\\,\\mathrm{s}$ catch.",
                 ["$\\Delta p=0-3.0=-3.0\\,\\mathrm{kg\\cdot m/s}$, $|\\Delta p|=3.0$.",
                  "$F_{\\mathrm{avg}}=3.0/0.030=100\\,\\mathrm{N}$.",
                  "For $0.10\\,\\mathrm{s}$: $F=30\\,\\mathrm{N}$.",
                  "Same impulse, longer time, gentler force."],
                 "$100\\,\\mathrm{N}$ then $30\\,\\mathrm{N}$", "", "Hard"),
        ("Using $F=mv$ instead of $p=mv$",
         "Momentum is $mv$, not a force. Impulse $F\\Delta t$ changes that momentum. Mixing the symbols is a vocabulary error that wrecks units."),
        ("Compute $\\Delta p$ with signs before dividing by time",
         "A rebound doubles the change compared with a catch. Write $p_f-p_i$ on paper."),
        [
            "I can compute $\\vec{p}=m\\vec{v}$ with direction.",
            "I can use $J=F\\Delta t=\\Delta p$ including from an $F$-$t$ area.",
            "I can explain why a longer collision time reduces average force.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Conservation of momentum",
        [
            "If the net external impulse on a system is zero, the system's total momentum does not change. "
            "That is conservation of momentum. Internal pushes cancel by Newton's third law.",
            "Choose the system so the messy forces are internal. Two colliding carts on a low-friction track: "
            "the collision forces are internal, so $m_1 v_1+m_2 v_2$ before equals the same sum after.",
            "Example: $4\\,\\mathrm{kg}$ at $6\\,\\mathrm{m/s}$ catches $2\\,\\mathrm{kg}$ at rest and they stick. "
            "$24=6v$, so $v=4\\,\\mathrm{m/s}$. Momentum was conserved; kinetic energy was not.",
            "Signs: pick a positive direction. A skater throwing a brick left gives the skater a rightward velocity "
            "so the sum stays zero if they started at rest.",
            "If friction with the Earth matters during a long slide, Earth is an external actor and the cart's "
            "momentum alone is not conserved. Short collisions often let you ignore friction during the impulse.",
            "Write one line: $p_{\\mathrm{tot},i}=p_{\\mathrm{tot},f}$. That line is the whole isolated-system collision.",
        ],
        "Elastic, inelastic, and explosion problems are this same line plus an energy comment. Conservation of $p$ "
        "is the backbone of the unit.",
        "Name the system. Check external horizontal forces. If they are negligible during the event, equate total $p$.",
        lesson_figure(
            _collision_before_after(),
            "Two carts before and after they stick",
            "Total mass grows in the stuck picture; total $p$ stays the same if the track impulse is negligible.",
        )
        + solved(4, "A $4.0\\,\\mathrm{kg}$ cart at $6.0\\,\\mathrm{m/s}$ sticks to a $2.0\\,\\mathrm{kg}$ cart at rest. Find $v_f$.",
                 ["$p_i=24\\,\\mathrm{kg\\cdot m/s}$.",
                  "$p_f=(6.0)v_f$.",
                  "$v_f=4.0\\,\\mathrm{m/s}$ forward."],
                 "$4.0\\,\\mathrm{m/s}$", "", "Easy")
        + solved(5, "Two skaters at rest push apart. $40\\,\\mathrm{kg}$ moves $3.0\\,\\mathrm{m/s}$ left. Find the $60\\,\\mathrm{kg}$ skater's velocity.",
                 ["$p_i=0$.",
                  "$40(-3)+60v=0$.",
                  "$v=2.0\\,\\mathrm{m/s}$ right."],
                 "$2.0\\,\\mathrm{m/s}$ right", "", "Medium")
        + solved(6, "A $3.0\\,\\mathrm{kg}$ fish at $1.0\\,\\mathrm{m/s}$ swallows a $0.50\\,\\mathrm{kg}$ fish coming toward it at $1.0\\,\\mathrm{m/s}$. Find $v_f$.",
                 ["Take the big fish's direction as positive.",
                  "$p_i=3.0(1.0)+0.50(-1.0)=2.5\\,\\mathrm{kg\\cdot m/s}$.",
                  "Combined mass $m_f=3.5\\,\\mathrm{kg}$.",
                  "$v_f=2.5/3.5=5/7\\,\\mathrm{m/s}$ in the original direction."],
                 "$5/7\\,\\mathrm{m/s}$ in the big fish's original direction", "", "Hard"),
        ("Forgetting opposite signs when objects approach",
         "Head-on means one velocity is negative. Adding speeds as if both were positive invents extra momentum."),
        ("Write $p_i=p_f$ as a single equation with masses and velocities",
         "Then solve. If they stick, there is one unknown $v_f$. If they bounce, you need an extra energy (or elasticity) rule."),
        [
            "I can state the isolated-system condition for conserving momentum.",
            "I can solve a 1D sticking collision for $v_f$.",
            "I can handle opposite-direction momenta with a sign convention.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Elastic collisions",
        [
            "A perfectly elastic collision conserves both momentum and kinetic energy of the two-object system. "
            "No leftover deformation, heat, or sound in the ideal AP model.",
            "In one dimension with equal masses and the target at rest, the velocities exchange: the incoming cart "
            "stops and the target leaves at the original speed. That result is worth memorizing after you have seen why.",
            "The extra elastic rule can be written: relative speed of separation equals relative speed of approach. "
            "If they approach at $10\\,\\mathrm{m/s}$, they separate at $10\\,\\mathrm{m/s}$ (1D).",
            "For masses $m_1$ hitting resting $m_2$, "
            "$v_{1f}=\\dfrac{m_1-m_2}{m_1+m_2}v_1$ and $v_{2f}=\\dfrac{2m_1}{m_1+m_2}v_1$. "
            "A $3\\,\\mathrm{kg}$ cart at $4\\,\\mathrm{m/s}$ on a $1\\,\\mathrm{kg}$ cart gives $v_{1f}=2\\,\\mathrm{m/s}$, $v_{2f}=6\\,\\mathrm{m/s}$.",
            "A bouncy ball off a heavy wall is approximately elastic with $v_f\\approx -v_i$. Then $|\\Delta p|\\approx 2mv$, "
            "twice the impulse of a catch.",
            "Always check $K_i=K_f$ numerically on elastic problems. If the numbers drift, a sign in the momentum line is wrong.",
        ],
        "You need a contrast with inelastic collisions. Elastic is the rare “both $p$ and $K$ conserved” case; "
        "most everyday crashes are not elastic.",
        "Write conservation of $p$. Write $K_i=K_f$ or the relative-speed rule. Two equations, two unknown final velocities.",
        lesson_figure(
            xy_graph(
                curves=[("#2563eb", [(0, 4), (1, 4), (1.2, 0), (3, 0)]),
                        ("#dc2626", [(0, 0), (1, 0), (1.2, 4), (3, 4)])],
                points=[(1.1, 2, "hit")],
                xlim=(-0.2, 3.4), ylim=(-1, 6), xlab="t", ylab="v", w=320, h=240,
            ),
            "Equal-mass 1D elastic: velocity exchange",
            "Blue cart's $v$ drops to zero; red target's $v$ jumps to the original blue value.",
        )
        + solved(7, "A $2.0\\,\\mathrm{kg}$ cart at $6.0\\,\\mathrm{m/s}$ hits a resting equal-mass cart elastically in 1D. Find both final speeds.",
                 ["Equal mass, target at rest: velocities swap.",
                  "Incoming cart stops: $v_{1f}=0$.",
                  "Target: $v_{2f}=6.0\\,\\mathrm{m/s}$."],
                 "$0$ and $6.0\\,\\mathrm{m/s}$", "", "Easy")
        + solved(8, "A ball hits a heavy wall elastically at $5.0\\,\\mathrm{m/s}$ and rebounds at $5.0\\,\\mathrm{m/s}$. Mass $0.40\\,\\mathrm{kg}$. Find $|\\Delta p|$.",
                 ["$p_i=+2.0\\,\\mathrm{kg\\cdot m/s}$, $p_f=-2.0$.",
                  "$\\Delta p=-4.0\\,\\mathrm{kg\\cdot m/s}$.",
                  "Magnitude $4.0\\,\\mathrm{kg\\cdot m/s}$, twice a catch."],
                 "$4.0\\,\\mathrm{kg\\cdot m/s}$", "", "Medium")
        + solved(9, "Elastic 1D: $3.0\\,\\mathrm{kg}$ at $4.0\\,\\mathrm{m/s}$ hits $1.0\\,\\mathrm{kg}$ at rest. Find both $v_f$ and check $K$.",
                 ["$v_{1f}=(3-1)4/4=2.0\\,\\mathrm{m/s}$.",
                  "$v_{2f}=(2\\cdot 3\\cdot 4)/4=6.0\\,\\mathrm{m/s}$.",
                  "$K_i=\\tfrac12(3)(16)=24\\,\\mathrm{J}$.",
                  "$K_f=\\tfrac12(3)(4)+\\tfrac12(1)(36)=6+18=24\\,\\mathrm{J}$."],
                 "$2.0\\,\\mathrm{m/s}$ and $6.0\\,\\mathrm{m/s}$; $K$ conserved", "", "Hard"),
        ("Using the stick-together velocity for a bounce",
         "If they bounce, they do not share one $v_f$. Elastic needs two final speeds and an extra equation."),
        ("Check kinetic energy after solving",
         "If $K_f$ is not $K_i$ on an elastic problem, a sign or a mixed-up mass is hiding in the momentum line."),
        [
            "I can state that elastic collisions conserve $p$ and $K$.",
            "I can use velocity exchange for equal-mass 1D hits on a resting target.",
            "I can apply the two-mass elastic formulas and verify $K$.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Inelastic collisions",
        [
            "An inelastic collision conserves momentum (if isolated) but not kinetic energy. Some $K$ becomes thermal "
            "energy, sound, and permanent deformation.",
            "A perfectly inelastic collision is the stick-together case: one common $v_f=p_{\\mathrm{tot}}/m_{\\mathrm{tot}}$. "
            "It loses the most $K$ of any 1D collision that conserves $p$.",
            "Example: $4\\,\\mathrm{kg}$ at $6\\,\\mathrm{m/s}$ sticks to $2\\,\\mathrm{kg}$ at rest. $v_f=4\\,\\mathrm{m/s}$, "
            "$K_i=72\\,\\mathrm{J}$, $K_f=48\\,\\mathrm{J}$. Lost $24\\,\\mathrm{J}$.",
            "The remaining fraction of $K$ when mass $m$ hits resting $M$ and sticks is $m/(m+M)$. A bullet in a block "
            "leaves only a tiny fraction of the bullet's original $K$.",
            "Two identical objects approaching at opposite speeds and sticking end at rest. All $K$ becomes thermal. "
            "Momentum was zero the whole time.",
            "Never force $K$ to be conserved on a clay collision. The AP exam will ask you to compute the missing $K$ "
            "and name it as thermal/deformation energy.",
        ],
        "Ballistic pendulum FRQs combine this lesson with $mgh$. Momentum during the embed, energy during the swing. "
        "Mixing those two intervals is a classic mistake.",
        "Use momentum only during the collision. Use energy only on the frictionless rise afterward, unless the problem includes friction.",
        lesson_figure(
            energy_bars_svg(ke=2, pe=0, thermal=2),
            "After a stick-together crash: KE down, thermal up",
            "Total energy still accounts; mechanical energy does not. Momentum was the conserved vector.",
        )
        + solved(10, "A $4.0\\,\\mathrm{kg}$ cart at $6.0\\,\\mathrm{m/s}$ sticks to $2.0\\,\\mathrm{kg}$ at rest. Find $v_f$ and $K_f$.",
                 ["$v_f=4.0\\,\\mathrm{m/s}$.",
                  "$K_i=72\\,\\mathrm{J}$.",
                  "$K_f=\\tfrac12(6)(16)=48\\,\\mathrm{J}$."],
                 "$4.0\\,\\mathrm{m/s}$, $K_f=48\\,\\mathrm{J}$", "", "Easy")
        + solved(11, "Two identical $2.0\\,\\mathrm{kg}$ gliders at $+4.0$ and $-4.0\\,\\mathrm{m/s}$ stick. Find $v_f$ and the lost $K$.",
                 ["$p_i=8-8=0$, so $v_f=0$.",
                  "$K_i=2\\times\\tfrac12(2)(16)=32\\,\\mathrm{J}$.",
                  "All $32\\,\\mathrm{J}$ becomes thermal."],
                 "$v_f=0$; $32\\,\\mathrm{J}$ lost", "", "Medium")
        + solved(12, "A $0.10\\,\\mathrm{kg}$ bullet at $400\\,\\mathrm{m/s}$ embeds in a $1.9\\,\\mathrm{kg}$ block. Find $v$ then the height on a frictionless slope ($g=10$).",
                 ["$p_i=40=2.0 v$, so $v=20\\,\\mathrm{m/s}$.",
                  "$K_f=\\tfrac12(2)(400)=400\\,\\mathrm{J}$ (versus $K_{\\mathrm{bullet}}=8000\\,\\mathrm{J}$).",
                  "$mgh=400\\Rightarrow h=400/(2.0\\cdot 10)=20\\,\\mathrm{m}$.",
                  "Do not use $8000\\,\\mathrm{J}$ for the height — that $K$ was already gone after the embed."],
                 "$20\\,\\mathrm{m/s}$, then $h=20\\,\\mathrm{m}$", "", "Hard"),
        ("Using the bullet's original $K$ as the block's $mgh$",
         "The embed is inelastic. Only the leftover $K$ after sticking climbs the hill."),
        ("Separate the timeline: collide, then rise",
         "Momentum for the fast collision. Energy for the slow gravitational climb. Two different conservation laws for two different intervals."),
        [
            "I can define a perfectly inelastic collision as sticking with shared $v_f$.",
            "I can compute the kinetic energy lost to thermal energy.",
            "I can combine a ballistic embed with a later energy-based height.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Center of mass",
        [
            "The center of mass (CM) is the mass-weighted average position: "
            "$x_{\\mathrm{cm}}=(m_1 x_1+m_2 x_2)/(m_1+m_2)$. For $2\\,\\mathrm{kg}$ at $x=0$ and $4\\,\\mathrm{kg}$ at $x=6\\,\\mathrm{m}$, $x_{\\mathrm{cm}}=4.0\\,\\mathrm{m}$.",
            "The CM sits closer to the heavier piece. A uniform rod's CM is at its geometric center.",
            "The system's total momentum is $M\\vec{v}_{\\mathrm{cm}}$. If $3\\,\\mathrm{kg}$ moves at $2\\,\\mathrm{m/s}$ and $1\\,\\mathrm{kg}$ at $6\\,\\mathrm{m/s}$ the same way, "
            "$v_{\\mathrm{cm}}=3.0\\,\\mathrm{m/s}$.",
            "With no external force, $v_{\\mathrm{cm}}$ is constant. Collisions shuffle the pieces around the CM; the CM itself does not jerk.",
            "In the CM frame, total momentum is zero. That frame makes elastic collision pictures symmetric and is a "
            "powerful AP Stretch view, still algebraic: subtract $v_{\\mathrm{cm}}$ from every velocity.",
            "Explosions: pieces fly both ways, but the CM of all fragments keeps the original velocity (zero if the bomb was at rest).",
        ],
        "Rotational dynamics will treat extended objects as if gravity acted at the CM. Learning to locate it now "
        "makes torque and balance problems shorter.",
        "Compute $x_{\\mathrm{cm}}$ as a weighted average. Compute $v_{\\mathrm{cm}}$ as total $p$ over total mass.",
        lesson_figure(
            xy_graph(
                points=[(0, 0, "2 kg"), (6, 0, "4 kg"), (4, 0, "CM")],
                xlim=(-1, 8), ylim=(-2, 2), xlab="x (m)", ylab="", w=340, h=160,
            ),
            "CM closer to the heavier mass",
            "$(2\\cdot 0+4\\cdot 6)/6=4\\,\\mathrm{m}$. Not the midpoint at $3\\,\\mathrm{m}$.",
        )
        + solved(13, "Find $x_{\\mathrm{cm}}$ of $2.0\\,\\mathrm{kg}$ at $x=0$ and $4.0\\,\\mathrm{kg}$ at $x=6.0\\,\\mathrm{m}$.",
                 ["$x_{\\mathrm{cm}}=(0+24)/6=4.0\\,\\mathrm{m}$.",
                  "Closer to $4\\,\\mathrm{kg}$, as expected.",
                  "Midpoint $3.0\\,\\mathrm{m}$ would be wrong."],
                 "$4.0\\,\\mathrm{m}$", "", "Easy")
        + solved(14, "Masses $3.0\\,\\mathrm{kg}$ at $2.0\\,\\mathrm{m/s}$ and $1.0\\,\\mathrm{kg}$ at $6.0\\,\\mathrm{m/s}$, same direction. Find $v_{\\mathrm{cm}}$.",
                 ["$p_{\\mathrm{tot}}=6+6=12\\,\\mathrm{kg\\cdot m/s}$.",
                  "$M=4.0\\,\\mathrm{kg}$.",
                  "$v_{\\mathrm{cm}}=3.0\\,\\mathrm{m/s}$."],
                 "$3.0\\,\\mathrm{m/s}$", "", "Medium")
        + solved(15, "Two carts collide in isolation. Explain what happens to $v_{\\mathrm{cm}}$ and how to find it from the initial velocities.",
                 ["No external impulse, so $v_{\\mathrm{cm}}$ is the same before and after.",
                  "$v_{\\mathrm{cm}}=(m_1 v_1+m_2 v_2)/(m_1+m_2)$ using initial (or final) values.",
                  "During the collision the pieces change speed; the weighted average velocity does not.",
                  "If they stick, $v_f=v_{\\mathrm{cm}}$ exactly."],
                 "$v_{\\mathrm{cm}}$ constant; equals $p_{\\mathrm{tot}}/M$", "", "Hard"),
        ("Averaging positions without weighting by mass",
         "The midpoint is only correct for equal masses. Always multiply by $m$ before adding."),
        ("Find $v_{\\mathrm{cm}}$ first on collision problems",
         "It is a free check: after a stick, $v_f$ must equal that $v_{\\mathrm{cm}}$. After a bounce, the CM still moves at that speed."),
        [
            "I can compute $x_{\\mathrm{cm}}$ as a mass-weighted average.",
            "I can find $v_{\\mathrm{cm}}=p_{\\mathrm{tot}}/M$.",
            "I can explain why $v_{\\mathrm{cm}}$ is constant in an isolated collision.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Explosions",
        [
            "An explosion is an inelastic process run backward: chemical or spring energy becomes kinetic energy, "
            "while momentum of an isolated system stays the same.",
            "If a firework is at rest, $p_{\\mathrm{tot}}=0$ after the burst too. Pieces fly opposite ways: "
            "$m_1 v_1+m_2 v_2=0$. A $1\\,\\mathrm{kg}$ piece at $12\\,\\mathrm{m/s}$ east means a $3\\,\\mathrm{kg}$ piece at $4\\,\\mathrm{m/s}$ west.",
            "Kinetic energy after is larger than before. That extra $K$ came from stored energy, not from a momentum leak.",
            "Recoil of a gun, a person throwing a brick on ice, and a balloon releasing air are all two-piece explosions. "
            "The thrown object's forward $p$ equals the thrower's backward $p$.",
            "If the original object was moving, conserve the original $p_{\\mathrm{tot}}$, not zero. Fragments' momenta "
            "must still add to $M v_{\\mathrm{original}}$.",
            "Draw after-arrows in opposite directions when $p_i=0$. Check that $K_f>K_i$. Those two sentences catch most explosion errors.",
        ],
        "Thrust and later rocket-style AP questions (qualitative) are explosion thinking. Unit 6's angular explosions "
        "will add $L$ conservation to this $p$ conservation.",
        "Set $p_i=p_f$. If at rest, $0=m_1 v_1+m_2 v_2$. Then, if asked, compute the $K$ gained from the stored energy.",
        lesson_figure(
            _explosion_svg(),
            "Resting object splits into opposite-going fragments",
            "Opposite momenta, larger total $K$. The CM of both pieces stays put if $p_i=0$.",
        )
        + solved(16, "A $4.0\\,\\mathrm{kg}$ object at rest splits into $1.0\\,\\mathrm{kg}$ at $12\\,\\mathrm{m/s}$ east. Find the other piece's velocity.",
                 ["$0=1(12)+3v$.",
                  "$v=-4.0\\,\\mathrm{m/s}$ (west).",
                  "Check $p$: $12-12=0$."],
                 "$4.0\\,\\mathrm{m/s}$ west", "", "Easy")
        + solved(17, "A $40\\,\\mathrm{kg}$ student on ice throws a $2.0\\,\\mathrm{kg}$ brick at $10\\,\\mathrm{m/s}$. Find recoil speed.",
                 ["$0=2(10)+40v$.",
                  "$v=-0.50\\,\\mathrm{m/s}$.",
                  "The student moves opposite the throw at $0.50\\,\\mathrm{m/s}$."],
                 "$0.50\\,\\mathrm{m/s}$ opposite the throw", "", "Medium")
        + solved(18, "A $5.0\\,\\mathrm{kg}$ cart moving at $2.0\\,\\mathrm{m/s}$ fires a $1.0\\,\\mathrm{kg}$ ball at $12\\,\\mathrm{m/s}$ forward relative to the ground. Find the cart's speed after (ignore friction).",
                 ["$p_i=5(2)=10\\,\\mathrm{kg\\cdot m/s}$.",
                  "Ball $p=1(12)=12$. Cart mass left $4.0\\,\\mathrm{kg}$ with speed $v$.",
                  "$10=12+4v$, so $v=-0.50\\,\\mathrm{m/s}$ (cart slows and reverses).",
                  "$K_i=10\\,\\mathrm{J}$, $K_f=\\tfrac12(1)(144)+\\tfrac12(4)(0.25)=72+0.5=72.5\\,\\mathrm{J}$. Extra $K$ came from the firing energy."],
                 "$0.50\\,\\mathrm{m/s}$ backward", "", "Hard"),
        ("Forcing $K$ to stay constant in an explosion",
         "Explosions add kinetic energy. Momentum conservation does not require $K$ conservation."),
        ("Keep the original $p_{\\mathrm{tot}}$ if the bomb was already moving",
         "Only a resting isolated object has $p_f=0$. A moving grenade's fragments still add to $M v$."),
        [
            "I can treat an explosion as momentum conservation plus extra $K$.",
            "I can solve two-piece recoil from rest.",
            "I can include a nonzero initial momentum when the system was already moving.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
