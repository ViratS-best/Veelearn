"""AP Physics 1 units 5–8: rotation, rotating-system energy, SHM, and fluids (algebra-based)."""
from __future__ import annotations

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, page_break, mq,
    xy_graph, sample_curve, energy_bars_svg, spring_mass_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _add(qs, rows):
    i = len(qs) + 1
    for text, ans, expl, dist in rows:
        qs.append(mq(text, ans, expl, i, distractors=dist))
        i += 1


def _seesaw_svg():
    return (
        '<svg viewBox="0 0 340 140" width="100%" style="max-width:340px" role="img">'
        '<polygon points="160,100 180,100 170,80" fill="#64748b"/>'
        '<line x1="40" y1="80" x2="300" y2="80" stroke="#0f172a" stroke-width="6"/>'
        '<rect x="70" y="52" width="36" height="28" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<rect x="250" y="48" width="40" height="32" fill="#fdba74" stroke="#9a3412"/>'
        '<text x="88" y="70" text-anchor="middle" font-size="11">m</text>'
        '<text x="270" y="68" text-anchor="middle" font-size="11">M</text>'
        '<text x="88" y="128" text-anchor="middle" font-size="11">r₁</text>'
        '<text x="270" y="128" text-anchor="middle" font-size="11">r₂</text>'
        "</svg>"
    )


def _wheel_svg():
    return (
        '<svg viewBox="0 0 280 160" width="100%" style="max-width:280px" role="img">'
        '<line x1="20" y1="130" x2="260" y2="130" stroke="#334155" stroke-width="3"/>'
        '<circle cx="140" cy="90" r="40" fill="#e0e7ff" stroke="#312e81" stroke-width="3"/>'
        '<circle cx="140" cy="90" r="6" fill="#0f172a"/>'
        '<line x1="140" y1="90" x2="175" y2="70" stroke="#b91c1c" stroke-width="2"/>'
        '<text x="178" y="68" font-size="11" fill="#b91c1c">R</text>'
        '<line x1="140" y1="50" x2="210" y2="50" stroke="#15803d" stroke-width="2.4"/>'
        '<polygon points="210,45 224,50 210,55" fill="#15803d"/>'
        '<text x="160" y="42" font-size="11" fill="#15803d">v=ωR</text>'
        "</svg>"
    )


def _hoop_disk_svg():
    """Hoop mass at R versus disk mass spread inward — rotational inertia, not rolling."""
    return (
        '<svg viewBox="0 0 360 170" width="100%" style="max-width:360px" role="img">'
        '<circle cx="95" cy="80" r="48" fill="none" stroke="#312e81" stroke-width="8"/>'
        '<circle cx="95" cy="80" r="5" fill="#0f172a"/>'
        '<circle cx="143" cy="80" r="6" fill="#b91c1c"/>'
        '<circle cx="47" cy="80" r="6" fill="#b91c1c"/>'
        '<circle cx="95" cy="32" r="6" fill="#b91c1c"/>'
        '<circle cx="95" cy="128" r="6" fill="#b91c1c"/>'
        '<text x="95" y="158" text-anchor="middle" font-size="11">hoop: mass at R</text>'
        '<circle cx="265" cy="80" r="48" fill="#c7d2fe" stroke="#312e81" stroke-width="3"/>'
        '<circle cx="265" cy="80" r="28" fill="#a5b4fc" stroke="#4338ca" stroke-width="1"/>'
        '<circle cx="265" cy="80" r="12" fill="#6366f1"/>'
        '<circle cx="265" cy="80" r="5" fill="#0f172a"/>'
        '<text x="265" y="158" text-anchor="middle" font-size="11">disk: mass inward</text>'
        "</svg>"
    )


def _hit_rod_svg():
    """Particle hitting a hinged rod at lever arm d."""
    return (
        '<svg viewBox="0 0 340 160" width="100%" style="max-width:340px" role="img">'
        '<rect x="28" y="20" width="16" height="120" fill="#64748b"/>'
        '<circle cx="44" cy="80" r="8" fill="#0f172a"/>'
        '<line x1="44" y1="80" x2="270" y2="80" stroke="#0f172a" stroke-width="8"/>'
        '<text x="150" y="68" font-size="12">rod</text>'
        '<circle cx="230" cy="80" r="12" fill="#fdba74" stroke="#9a3412"/>'
        '<text x="230" y="84" text-anchor="middle" font-size="10">m</text>'
        '<line x1="230" y1="28" x2="230" y2="62" stroke="#b91c1c" stroke-width="2.4"/>'
        '<polygon points="224,60 230,72 236,60" fill="#b91c1c"/>'
        '<text x="240" y="44" font-size="12" fill="#b91c1c">v</text>'
        '<line x1="44" y1="110" x2="230" y2="110" stroke="#1d4ed8" stroke-width="1.6"/>'
        '<text x="120" y="128" font-size="12" fill="#1d4ed8">d</text>'
        '<text x="36" y="18" font-size="11">hinge</text>'
        "</svg>"
    )


def _pulley_svg():
    return (
        '<svg viewBox="0 0 260 180" width="100%" style="max-width:260px" role="img">'
        '<circle cx="130" cy="50" r="28" fill="#e2e8f0" stroke="#0f172a" stroke-width="3"/>'
        '<circle cx="130" cy="50" r="6" fill="#0f172a"/>'
        '<line x1="102" y1="50" x2="102" y2="140" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="158" y1="50" x2="158" y2="120" stroke="#0f172a" stroke-width="2"/>'
        '<rect x="84" y="140" width="36" height="28" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<rect x="140" y="120" width="36" height="36" fill="#fdba74" stroke="#9a3412"/>'
        '<text x="102" y="158" text-anchor="middle" font-size="11">m₁</text>'
        '<text x="158" y="142" text-anchor="middle" font-size="11">m₂</text>'
        '<text x="130" y="22" text-anchor="middle" font-size="11">I, R</text>'
        "</svg>"
    )


def _pipe_svg():
    return (
        '<svg viewBox="0 0 340 150" width="100%" style="max-width:340px" role="img">'
        '<path d="M20 40 L160 40 L160 55 L320 20 L320 100 L160 80 L160 95 L20 95 Z" '
        'fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<text x="70" y="72" font-size="12">A₁, v₁, P₁</text>'
        '<text x="230" y="62" font-size="12">A₂, v₂, P₂</text>'
        '<line x1="50" y1="120" x2="110" y2="120" stroke="#b91c1c" stroke-width="2"/>'
        '<polygon points="110,115 124,120 110,125" fill="#b91c1c"/>'
        '<line x1="230" y1="120" x2="310" y2="120" stroke="#b91c1c" stroke-width="3"/>'
        '<polygon points="310,114 328,120 310,126" fill="#b91c1c"/>'
        '<text x="60" y="142" font-size="11">slow, high P</text>'
        '<text x="240" y="142" font-size="11">fast, lower P</text>'
        "</svg>"
    )


def _pistons_svg():
    return (
        '<svg viewBox="0 0 300 150" width="100%" style="max-width:300px" role="img">'
        '<rect x="30" y="70" width="50" height="50" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<rect x="40" y="40" width="30" height="30" fill="#c7d2fe" stroke="#312e81"/>'
        '<rect x="180" y="50" width="90" height="70" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<rect x="200" y="20" width="50" height="30" fill="#c7d2fe" stroke="#312e81"/>'
        '<path d="M80 110 L180 110" fill="none" stroke="#1e3a8a" stroke-width="8"/>'
        '<text x="55" y="38" text-anchor="middle" font-size="11">F₁, A₁</text>'
        '<text x="225" y="16" text-anchor="middle" font-size="11">F₂, A₂</text>'
        '<text x="130" y="100" font-size="11">fluid</text>'
        "</svg>"
    )


def _tank_svg():
    return (
        '<svg viewBox="0 0 240 180" width="100%" style="max-width:240px" role="img">'
        '<path d="M40 20 L40 160 L200 160 L200 20" fill="none" stroke="#0f172a" stroke-width="3"/>'
        '<rect x="44" y="50" width="152" height="106" fill="#93c5fd"/>'
        '<line x1="44" y1="50" x2="196" y2="50" stroke="#1d4ed8" stroke-width="2"/>'
        '<circle cx="120" cy="130" r="7" fill="#b91c1c"/>'
        '<line x1="120" y1="50" x2="120" y2="130" stroke="#b91c1c" stroke-dasharray="4 3"/>'
        '<text x="128" y="95" font-size="11" fill="#b91c1c">h</text>'
        '<text x="90" y="148" font-size="11">P=P₀+ρgh</text>'
        "</svg>"
    )


def _buoyancy_fbd():
    """Submerged hanging object: F_g down, F_b up, scale tension up — all vertical."""
    return (
        '<svg viewBox="0 0 260 230" width="100%" style="max-width:260px" role="img">'
        '<rect x="90" y="8" width="60" height="20" fill="#e2e8f0" stroke="#334155"/>'
        '<text x="120" y="22" text-anchor="middle" font-size="11">scale</text>'
        '<rect x="24" y="48" width="212" height="168" fill="#dbeafe" stroke="#1e3a8a"/>'
        '<text x="200" y="68" font-size="11" fill="#1e3a8a">fluid</text>'
        '<rect x="95" y="110" width="50" height="40" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>'
        '<line x1="120" y1="28" x2="120" y2="110" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="120" y1="110" x2="120" y2="58" stroke="#15803d" stroke-width="2.6"/>'
        '<polygon points="115,60 120,48 125,60" fill="#15803d"/>'
        '<text x="128" y="54" font-size="11" fill="#15803d">T</text>'
        '<line x1="95" y1="130" x2="95" y2="78" stroke="#1d4ed8" stroke-width="2.4"/>'
        '<polygon points="90,80 95,68 100,80" fill="#1d4ed8"/>'
        '<text x="48" y="92" font-size="11" fill="#1d4ed8">F_b</text>'
        '<line x1="120" y1="150" x2="120" y2="198" stroke="#0f172a" stroke-width="2.4"/>'
        '<polygon points="115,196 120,208 125,196" fill="#0f172a"/>'
        '<text x="128" y="192" font-size="11">F_g</text>'
        "</svg>"
    )


def _hinged_rod_fbd():
    """Rod hinged at one end; F_g at the center. Hinge force at the pin."""
    return (
        '<svg viewBox="0 0 340 160" width="100%" style="max-width:340px" role="img">'
        '<rect x="28" y="20" width="16" height="120" fill="#64748b"/>'
        '<circle cx="44" cy="80" r="8" fill="#0f172a"/>'
        '<line x1="44" y1="80" x2="280" y2="80" stroke="#0f172a" stroke-width="8"/>'
        '<text x="150" y="68" font-size="12">rod</text>'
        '<line x1="162" y1="80" x2="162" y2="130" stroke="#0f172a" stroke-width="2.2"/>'
        '<polygon points="157,128 162,140 167,128" fill="#0f172a"/>'
        '<text x="168" y="124" font-size="11">F_g at CM</text>'
        '<line x1="44" y1="80" x2="44" y2="36" stroke="#15803d" stroke-width="2.2"/>'
        '<polygon points="39,38 44,26 49,38" fill="#15803d"/>'
        '<text x="52" y="34" font-size="11" fill="#15803d">H_y</text>'
        '<line x1="44" y1="80" x2="86" y2="80" stroke="#b91c1c" stroke-width="2.2"/>'
        '<polygon points="84,75 96,80 84,85" fill="#b91c1c"/>'
        '<text x="70" y="72" font-size="11" fill="#b91c1c">H_x</text>'
        '<text x="28" y="18" font-size="11">hinge</text>'
        "</svg>"
    )


def _pipe_height_svg():
    """Two-station pipe that changes area and height so FRQ labels include h."""
    return (
        '<svg viewBox="0 0 360 190" width="100%" style="max-width:360px" role="img">'
        '<path d="M20 40 L150 40 L150 55 L250 95 L250 125 L150 90 L150 105 L20 105 Z" '
        'fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<path d="M250 95 L340 95 L340 125 L250 125 Z" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
        '<line x1="20" y1="170" x2="340" y2="170" stroke="#64748b" stroke-width="2"/>'
        '<line x1="85" y1="105" x2="85" y2="170" stroke="#b91c1c" stroke-dasharray="4 3"/>'
        '<line x1="295" y1="125" x2="295" y2="170" stroke="#b91c1c" stroke-dasharray="4 3"/>'
        '<text x="90" y="148" font-size="11" fill="#b91c1c">h₁</text>'
        '<text x="300" y="158" font-size="11" fill="#b91c1c">h₂</text>'
        '<text x="55" y="78" font-size="11">A₁, v₁, P₁</text>'
        '<text x="258" y="88" font-size="11">A₂, v₂, P₂</text>'
        "</svg>"
    )


# ===========================================================================
# UNIT 5: Torque and Rotational Dynamics
# ===========================================================================

def _u5_questions():
    qs = []
    _add(qs, [
        ("Angular displacement $\\theta$ is measured in radians in the formulas $s=r\\theta$ and $v=r\\omega$. A wheel turns $2.0\\,\\mathrm{rad}$. If $r=0.50\\,\\mathrm{m}$, arc length $s$ is",
         "$1.0\\,\\mathrm{m}$",
         "$s=r\\theta=(0.50)(2.0)=1.0\\,\\mathrm{m}$.",
         ["$0.25\\,\\mathrm{m}$", "$4.0\\,\\mathrm{m}$", "$2.5\\,\\mathrm{m}$"]),
        ("Average angular velocity is $\\omega=\\Delta\\theta/\\Delta t$. A disk rotates $6.0\\,\\mathrm{rad}$ in $2.0\\,\\mathrm{s}$. $\\omega$ is",
         "$3.0\\,\\mathrm{rad/s}$",
         "$\\omega=6/2=3.0\\,\\mathrm{rad/s}$.",
         ["$12\\,\\mathrm{rad/s}$", "$8.0\\,\\mathrm{rad/s}$", "$0.33\\,\\mathrm{rad/s}$"]),
        ("Linear speed at the rim is $v=r\\omega$. For $r=0.25\\,\\mathrm{m}$ and $\\omega=8.0\\,\\mathrm{rad/s}$, $v$ is",
         "$2.0\\,\\mathrm{m/s}$",
         "$v=(0.25)(8)=2.0\\,\\mathrm{m/s}$, tangent to the circle.",
         ["$32\\,\\mathrm{m/s}$", "$8.25\\,\\mathrm{m/s}$", "$0.031\\,\\mathrm{m/s}$"]),
        ("A full turn is $2\\pi$ radians, about $6.28\\,\\mathrm{rad}$. Turning half a turn is",
         "$\\pi\\,\\mathrm{rad}$",
         "Half of $2\\pi$ is $\\pi$ radians, not $180\\,\\mathrm{m}$.",
         ["$2\\pi\\,\\mathrm{rad}$", "$180\\,\\mathrm{rad}$", "$1\\,\\mathrm{rad}$"]),
        ("If $\\omega$ is constant, a point on a rigid wheel has constant speed but changing",
         "velocity direction (hence centripetal acceleration $v^2/r$ toward the center)",
         "Speed $v=r\\omega$ is steady; the velocity vector keeps turning.",
         ["mass", "radius", "angular displacement which must be zero"]),
    ])
    _add(qs, [
        ("Torque is $\\tau=rF\\sin\\phi$, with $\\phi$ the angle between $\\vec{r}$ and $\\vec{F}$. For $r=2.0\\,\\mathrm{m}$, $F=10\\,\\mathrm{N}$, $\\phi=90^\\circ$, $\\tau$ is",
         "$20\\,\\mathrm{N\\cdot m}$",
         "$\\sin 90^\\circ=1$, so $\\tau=20\\,\\mathrm{N\\cdot m}$.",
         ["$5.0\\,\\mathrm{N\\cdot m}$", "$12\\,\\mathrm{N\\cdot m}$", "$0$"]),
        ("The same $10\\,\\mathrm{N}$ along the rod ($\\phi=0$) produces torque",
         "$0$",
         "$\\sin 0=0$. A force through the axis, or along the line to the axis, does not twist.",
         ["$20\\,\\mathrm{N\\cdot m}$", "$10\\,\\mathrm{N\\cdot m}$", "infinite"]),
        ("Lever arm is the perpendicular distance from the axis to the force's line. If $F=12\\,\\mathrm{N}$ and lever arm $0.25\\,\\mathrm{m}$, $\\tau$ is",
         "$3.0\\,\\mathrm{N\\cdot m}$",
         "$\\tau=F d_{\\perp}=(12)(0.25)=3.0\\,\\mathrm{N\\cdot m}$.",
         ["$48\\,\\mathrm{N\\cdot m}$", "$12.25\\,\\mathrm{N\\cdot m}$", "$0.021\\,\\mathrm{N\\cdot m}$"]),
        ("Pushing a door near the hinge versus near the knob, same force, the knob gives",
         "larger torque because $r$ is larger",
         "Torque scales with the moment arm. That is why doorknobs are far from hinges.",
         ["smaller torque", "identical torque always", "zero torque at the knob"]),
        ("Two equal opposite forces that do not share a line form a couple. Net force can be zero while net torque is",
         "not zero (the pair still twists)",
         "Equilibrium needs both $\\sum\\vec{F}=0$ and $\\sum\\tau=0$.",
         ["automatically zero", "infinite", "equal to the weight"]),
    ])
    _add(qs, [
        ("Rotational inertia $I$ measures how stubborn a rotation is. For a point mass, $I=mr^2$. A $2.0\\,\\mathrm{kg}$ mass on a $0.50\\,\\mathrm{m}$ massless rod about the other end has $I=$",
         "$0.50\\,\\mathrm{kg\\cdot m}^2$",
         "$I=(2.0)(0.50)^2=0.50\\,\\mathrm{kg\\cdot m}^2$.",
         ["$1.0\\,\\mathrm{kg\\cdot m}^2$", "$0.25\\,\\mathrm{kg\\cdot m}^2$", "$2.5\\,\\mathrm{kg\\cdot m}^2$"]),
        ("A hoop's mass is all at radius $R$, so $I=mR^2$ about its center. A disk's $I$ about its center is",
         "$\\tfrac12 mR^2$ (smaller than the hoop's)",
         "Mass closer to the axis is easier to spin. Disk beats hoop for the same $m$ and $R$.",
         ["$mR^2$ same as a hoop", "$2mR^2$", "$0$"]),
        ("A $4.0\\,\\mathrm{kg}$ hoop of $R=0.50\\,\\mathrm{m}$ has $I=$",
         "$1.0\\,\\mathrm{kg\\cdot m}^2$",
         "$I=mR^2=4(0.25)=1.0\\,\\mathrm{kg\\cdot m}^2$.",
         ["$0.50\\,\\mathrm{kg\\cdot m}^2$", "$2.0\\,\\mathrm{kg\\cdot m}^2$", "$8.0\\,\\mathrm{kg\\cdot m}^2$"]),
        ("That same mass as a solid disk would have $I=$",
         "$0.50\\,\\mathrm{kg\\cdot m}^2$",
         "$I=\\tfrac12 mR^2=\\tfrac12(1.0)=0.50\\,\\mathrm{kg\\cdot m}^2$.",
         ["$1.0\\,\\mathrm{kg\\cdot m}^2$", "$0.25\\,\\mathrm{kg\\cdot m}^2$", "$2.0\\,\\mathrm{kg\\cdot m}^2$"]),
        ("Moving mass farther from the axis",
         "increases $I$ (harder to angularly accelerate)",
         "$I$ grows with $r^2$. Ice-skaters pull arms in to decrease $I$.",
         ["decreases $I$", "does not change $I$", "makes $I$ negative"]),
    ])
    _add(qs, [
        ("Newton's second law for rotation is $\\tau_{\\mathrm{net}}=I\\alpha$. If $I=2.0\\,\\mathrm{kg\\cdot m}^2$ and $\\tau_{\\mathrm{net}}=8.0\\,\\mathrm{N\\cdot m}$, $\\alpha$ is",
         "$4.0\\,\\mathrm{rad/s}^2$",
         "$\\alpha=\\tau/I=8/2=4.0\\,\\mathrm{rad/s}^2$.",
         ["$16\\,\\mathrm{rad/s}^2$", "$0.25\\,\\mathrm{rad/s}^2$", "$10\\,\\mathrm{rad/s}^2$"]),
        ("A disk $I=0.50\\,\\mathrm{kg\\cdot m}^2$ is spun by a $0.20\\,\\mathrm{m}$ radius with tangent force $10\\,\\mathrm{N}$ (no friction). $\\alpha$ is",
         "$4.0\\,\\mathrm{rad/s}^2$",
         "$\\tau=rF=2.0\\,\\mathrm{N\\cdot m}$, $\\alpha=2.0/0.50=4.0\\,\\mathrm{rad/s}^2$.",
         ["$50\\,\\mathrm{rad/s}^2$", "$2.0\\,\\mathrm{rad/s}^2$", "$0.40\\,\\mathrm{rad/s}^2$"]),
        ("If two torques cancel, $\\alpha$ is",
         "$0$ (constant $\\omega$, which may be zero)",
         "Rotational first law: balanced torques mean no change in $\\omega$.",
         ["infinite", "equal to $g$", "equal to $v/r$ always"]),
        ("Angular analog of mass is $I$; analog of $a$ is $\\alpha$; analog of $F_{\\mathrm{net}}$ is",
         "$\\tau_{\\mathrm{net}}$",
         "The translation–rotation dictionary is the AP memory device.",
         ["$L$ only", "$K$ only", "$mg$"]),
        ("A pulley with frictionless axle still has $I>0$. A string tension then",
         "must provide $\\tau=TR$ to angularly accelerate the pulley",
         "Massless pulley approximations set $I=0$ and $T$ equal on both sides. Real $I$ makes the tensions differ.",
         ["is always zero", "cannot produce torque", "equals $mg$ on both sides always"]),
    ])
    _add(qs, [
        ("Rolling without slipping means $v=\\omega R$ and $a=\\alpha R$ relating center-of-mass motion to rotation. A wheel of $R=0.40\\,\\mathrm{m}$ with $\\omega=5.0\\,\\mathrm{rad/s}$ has $v_{\\mathrm{cm}}=$",
         "$2.0\\,\\mathrm{m/s}$",
         "$v=\\omega R=2.0\\,\\mathrm{m/s}$.",
         ["$12.5\\,\\mathrm{m/s}$", "$0.080\\,\\mathrm{m/s}$", "$5.4\\,\\mathrm{m/s}$"]),
        ("A hoop ($I=mR^2$) rolling without slipping has total $K=$",
         "$mv^2$ (half translational, half rotational)",
         "$K=\\tfrac12 mv^2+\\tfrac12(mR^2)(v/R)^2=mv^2$.",
         ["$\\tfrac12 mv^2$ only", "$\\tfrac14 mv^2$", "$2mv^2$"]),
        ("A solid disk ($I=\\tfrac12 mR^2$) rolling at speed $v$ has total $K=$",
         "$\\tfrac34 mv^2$",
         "$\\tfrac12 mv^2+\\tfrac12(\\tfrac12 mR^2)(v^2/R^2)=\\tfrac34 mv^2$.",
         ["$\\tfrac12 mv^2$", "$mv^2$", "$\\tfrac14 mv^2$"]),
        ("On a frictionless incline a round object",
         "slides without starting to rotate (no torque about CM)",
         "Static friction is what supplies the torque for rolling without slipping.",
         ["rolls even faster than with friction", "must roll", "floats"]),
        ("Released from rest, a disk and a hoop of equal mass roll down the same hill. The winner at the bottom is",
         "the disk (smaller $I$, more of the energy in $v$)",
         "Both lose the same $mgh$. The hoop stores more in $\\tfrac12 I\\omega^2$, so less in $\\tfrac12 mv^2$.",
         ["the hoop", "they tie", "the heavier-looking paint job"]),
    ])
    _add(qs, [
        ("Static equilibrium of an extended object requires",
         "$\\sum F_x=0$, $\\sum F_y=0$, and $\\sum\\tau=0$ about any axis",
         "No net force and no net twist. You may choose a convenient axis to kill unknown forces in the torque sum.",
         ["$\\sum F=0$ only", "$\\sum\\tau=0$ only", "$v=0$ only, even if $\\alpha\\neq 0$"]),
        ("A $20\\,\\mathrm{kg}$ child sits $1.5\\,\\mathrm{m}$ left of a seesaw pivot. Where must a $30\\,\\mathrm{kg}$ child sit on the right to balance? ($g=10$)",
         "$1.0\\,\\mathrm{m}$",
         "Torques: $(200)(1.5)=(300)x$, so $x=1.0\\,\\mathrm{m}$.",
         ["$1.5\\,\\mathrm{m}$", "$2.0\\,\\mathrm{m}$", "$0.75\\,\\mathrm{m}$"]),
        ("Choosing the pivot at a support in a torque sum makes that support's force",
         "drop out of $\\sum\\tau$ because its lever arm is zero",
         "That is the standard trick for beams with extra unknown $N$.",
         ["double", "become the only force", "equal $mg$ automatically"]),
        ("A uniform beam's weight acts at",
         "its center of mass (the geometric center if uniform)",
         "Gravity's torque uses $mg$ at the CM.",
         ["an end always", "the pivot always", "nowhere"]),
        ("If $\\sum F=0$ but $\\sum\\tau\\neq 0$, the object",
         "has a changing $\\omega$ (it starts to spin) while $v_{\\mathrm{cm}}$ stays constant",
         "Translation and rotation are separate conditions.",
         ["cannot exist", "must be at rest", "must fall linearly only"]),
    ])
    _add(qs, [
        ("A bicycle wheel turns $10\\,\\mathrm{rad}$ in $4.0\\,\\mathrm{s}$ at constant $\\omega$. That $\\omega$ is",
         "$2.5\\,\\mathrm{rad/s}$",
         "$\\omega=\\Delta\\theta/\\Delta t=2.5\\,\\mathrm{rad/s}$.",
         ["$40\\,\\mathrm{rad/s}$", "$6.0\\,\\mathrm{rad/s}$", "$0.40\\,\\mathrm{rad/s}$"]),
        ("Rim speed of a $0.30\\,\\mathrm{m}$ radius wheel at $\\omega=10\\,\\mathrm{rad/s}$ is",
         "$3.0\\,\\mathrm{m/s}$",
         "$v=r\\omega=3.0\\,\\mathrm{m/s}$.",
         ["$13\\,\\mathrm{m/s}$", "$0.030\\,\\mathrm{m/s}$", "$33\\,\\mathrm{m/s}$"]),
        ("Torque of $25\\,\\mathrm{N}$ at $37^\\circ$ to a $0.40\\,\\mathrm{m}$ wrench ($\\sin 37^\\circ=0.6$) is",
         "$6.0\\,\\mathrm{N\\cdot m}$",
         "$\\tau=(0.40)(25)(0.6)=6.0\\,\\mathrm{N\\cdot m}$.",
         ["$10\\,\\mathrm{N\\cdot m}$", "$4.0\\,\\mathrm{N\\cdot m}$", "$25\\,\\mathrm{N\\cdot m}$"]),
        ("A $6.0\\,\\mathrm{kg}$ point mass $0.50\\,\\mathrm{m}$ from an axis has $I=$",
         "$1.5\\,\\mathrm{kg\\cdot m}^2$",
         "$I=6(0.25)=1.5\\,\\mathrm{kg\\cdot m}^2$.",
         ["$3.0\\,\\mathrm{kg\\cdot m}^2$", "$0.50\\,\\mathrm{kg\\cdot m}^2$", "$12\\,\\mathrm{kg\\cdot m}^2$"]),
        ("$\\tau_{\\mathrm{net}}=6.0\\,\\mathrm{N\\cdot m}$ on $I=1.5\\,\\mathrm{kg\\cdot m}^2$ gives $\\alpha=$",
         "$4.0\\,\\mathrm{rad/s}^2$",
         "$\\alpha=6/1.5=4.0\\,\\mathrm{rad/s}^2$.",
         ["$9.0\\,\\mathrm{rad/s}^2$", "$2.5\\,\\mathrm{rad/s}^2$", "$0.25\\,\\mathrm{rad/s}^2$"]),
        ("Starting from rest, that $\\alpha$ for $3.0\\,\\mathrm{s}$ yields $\\omega=$",
         "$12\\,\\mathrm{rad/s}$",
         "$\\omega=0+\\alpha t=12\\,\\mathrm{rad/s}$.",
         ["$4.0\\,\\mathrm{rad/s}$", "$1.3\\,\\mathrm{rad/s}$", "$36\\,\\mathrm{rad/s}$"]),
        ("A rolling disk's $v_{\\mathrm{cm}}=4.0\\,\\mathrm{m/s}$ and $R=0.50\\,\\mathrm{m}$. If no slip, $\\omega=$",
         "$8.0\\,\\mathrm{rad/s}$",
         "$\\omega=v/R=8.0\\,\\mathrm{rad/s}$.",
         ["$2.0\\,\\mathrm{rad/s}$", "$4.5\\,\\mathrm{rad/s}$", "$0.125\\,\\mathrm{rad/s}$"]),
        ("Total $K$ of that disk ($I=\\tfrac12 mR^2$, $m=4.0\\,\\mathrm{kg}$) is",
         "$48\\,\\mathrm{J}$",
         "$K=\\tfrac34 mv^2=\\tfrac34(4.0)(16)=48\\,\\mathrm{J}$. Translation $32\\,\\mathrm{J}$ plus rotation $16\\,\\mathrm{J}$.",
         ["$32\\,\\mathrm{J}$", "$24\\,\\mathrm{J}$", "$16\\,\\mathrm{J}$"]),
        ("A uniform $4.0\\,\\mathrm{m}$ plank of weight $200\\,\\mathrm{N}$ is supported at both ends. Left support force is",
         "$100\\,\\mathrm{N}$",
         "Symmetry: each end holds half the weight.",
         ["$200\\,\\mathrm{N}$", "$50\\,\\mathrm{N}$", "$0$"]),
        ("If a $100\\,\\mathrm{N}$ person stands at the plank midpoint as well, each end support becomes",
         "$150\\,\\mathrm{N}$",
         "Total load $300\\,\\mathrm{N}$, still symmetric.",
         ["$100\\,\\mathrm{N}$", "$200\\,\\mathrm{N}$", "$300\\,\\mathrm{N}$"]),
        ("Which object, same $m$ and $R$, is hardest to angularly accelerate about its center?",
         "a hoop ($I=mR^2$)",
         "Largest $I$ means smallest $\\alpha$ for a given $\\tau$.",
         ["a solid disk", "a point mass at the center", "a solid sphere ($I=\\tfrac25 mR^2$)"]),
        ("Friction needed for rolling without slipping on a ramp points",
         "up the ramp (it is the torque that spins the object)",
         "Without that backward/up-ramp friction, there is no $\\tau$ about the CM.",
         ["down the ramp always", "vertically", "nowhere; friction must be zero"]),
        ("A force through the center of mass of a free rigid body",
         "changes $v_{\\mathrm{cm}}$ but produces no $\\tau$ about the CM",
         "Translation without rotation about the CM.",
         ["only spins it", "does nothing", "cancels gravity always"]),
        ("$1\\,\\mathrm{rev/s}$ is an angular speed of",
         "$2\\pi\\,\\mathrm{rad/s}$",
         "One revolution is $2\\pi$ radians each second.",
         ["$1\\,\\mathrm{rad/s}$", "$\\pi\\,\\mathrm{rad/s}$", "$360\\,\\mathrm{rad/s}$"]),
        ("A bolt is turned by a $12\\,\\mathrm{N}$ force perpendicular to a $0.25\\,\\mathrm{m}$ wrench. Torque magnitude is",
         "$3.0\\,\\mathrm{N\\cdot m}$",
         "$\\tau=rF_\\perp=(0.25)(12)=3.0\\,\\mathrm{N\\cdot m}$.",
         ["$48\\,\\mathrm{N\\cdot m}$", "$12\\,\\mathrm{N\\cdot m}$", "$0.25\\,\\mathrm{N\\cdot m}$"]),
        ("A wheel starts from rest and reaches $10\\,\\mathrm{rad/s}$ in $5.0\\,\\mathrm{s}$ with constant $\\alpha$. Angular displacement during those $5.0\\,\\mathrm{s}$ is",
         "$25\\,\\mathrm{rad}$",
         "$\\alpha=10/5=2.0\\,\\mathrm{rad/s}^2$. Then $\\theta=\\tfrac12\\alpha t^2=\\tfrac12(2.0)(25)=25\\,\\mathrm{rad}$.",
         ["$50\\,\\mathrm{rad}$", "$10\\,\\mathrm{rad}$", "$2.0\\,\\mathrm{rad}$"]),
        ("AP Stretch: A solid disk ($I=\\tfrac12 mR^2$) of mass $3.0\\,\\mathrm{kg}$ and $R=0.50\\,\\mathrm{m}$ is pulled horizontally at the axle with $18\\,\\mathrm{N}$ and rolls without slipping. Find $a_{\\mathrm{cm}}$ and the required static friction.",
         "$a=4.0\\,\\mathrm{m/s}^2$, $f_s=6.0\\,\\mathrm{N}$",
         "$F-f=ma$ and $fR=I a/R$ give $f=\\tfrac12 ma$. Then $18-\\tfrac12(3)a=3a$, so $18=4.5a$, $a=4.0\\,\\mathrm{m/s}^2$, $f=6.0\\,\\mathrm{N}$.",
         ["$a=6.0\\,\\mathrm{m/s}^2$, $f=0$ (treating it as sliding)", "$a=2.0\\,\\mathrm{m/s}^2$, $f=12\\,\\mathrm{N}$", "$a=18\\,\\mathrm{m/s}^2$"]),
        ("AP Stretch: A hoop ($I=mR^2$) of mass $4.0\\,\\mathrm{kg}$ and $R=0.40\\,\\mathrm{m}$ is pulled at the hub with $16\\,\\mathrm{N}$ and rolls without slipping. Find $a_{\\mathrm{cm}}$ and $f_s$.",
         "$a=2.0\\,\\mathrm{m/s}^2$, $f_s=8.0\\,\\mathrm{N}$",
         "For a hoop $f=ma$. Then $16-f=4a$ with $f=4a$ gives $16=8a$, $a=2.0\\,\\mathrm{m/s}^2$, $f=8.0\\,\\mathrm{N}$. Constraint $a=\\alpha R$ was used.",
         ["$a=4.0\\,\\mathrm{m/s}^2$, $f=0$", "$a=2.0\\,\\mathrm{m/s}^2$, $f=0$", "$a=\\sqrt{gh}$ from an energy race"]),
        ("AP Stretch: Point masses $m$, $2m$, and $m$ sit at $x=0$, $x=L/2$, and $x=L$ on a massless rod. $I$ about the left end is",
         "$\\tfrac32 m L^2$",
         "$I=0+(2m)(L/2)^2+m L^2=2m(L^2/4)+mL^2=\\tfrac12 mL^2+mL^2=\\tfrac32 mL^2$.",
         ["$4mL^2$", "$mL^2$", "$3mL^2$ about the midpoint of a two-mass rod"]),
        ("AP Stretch: A uniform $4.0\\,\\mathrm{m}$ beam weighs $240\\,\\mathrm{N}$, hinged on the left. A cable at the right end pulls at $37^\\circ$ above the horizontal ($\\sin=3/5$, $\\cos=4/5$). Cable tension is",
         "$200\\,\\mathrm{N}$",
         "Torques about the hinge: $240(2.0)=T\\sin 37^\\circ(4.0)= (3T/5)(4)=12T/5$. Then $480=12T/5$, $T=200\\,\\mathrm{N}$.",
         ["$240\\,\\mathrm{N}$", "$120\\,\\mathrm{N}$", "$130\\,\\mathrm{N}$ from a vertical-cable copy"]),
        ("AP Stretch: For rolling without slipping down an incline, $a=g\\sin\\theta/(1+I/mR^2)$. A disk's $a$ is",
         "$\\tfrac23 g\\sin\\theta$",
         "$I/mR^2=1/2$, denominator $3/2$, so $a=(2/3)g\\sin\\theta$.",
         ["$g\\sin\\theta$", "$\\tfrac12 g\\sin\\theta$", "$g$"]),
        ("AP Stretch: A yo-yo is modeled as $I=k mR^2$ unwinding. The string tension is less than $mg$ because",
         "the CM accelerates down, so $mg-T=ma$ with $a>0$",
         "Combined with $\\tau=TR=I\\alpha$ and $a=\\alpha R$.",
         ["tension exceeds $mg$", "massless strings pull up with $2mg$", "gravity shuts off"]),
        ("AP Stretch: Two forces $F$ north at $x=0$ and $F$ south at $x=L$ on a free rod. Net force is $0$; net torque magnitude about the CM (midpoint) is",
         "$FL$",
         "Each force has lever arm $L/2$, both torques the same sense: $2\\times F(L/2)=FL$.",
         ["$0$", "$F L/2$", "$2FL$"]),
        ("AP Stretch: A potter's wheel $I=0.80\\,\\mathrm{kg\\cdot m}^2$ spins at $15\\,\\mathrm{rad/s}$. A brake applies $\\tau=-2.4\\,\\mathrm{N\\cdot m}$ until it stops. Kinetic energy lost is",
         "$90\\,\\mathrm{J}$",
         "$\\alpha=-3.0\\,\\mathrm{rad/s}^2$, $t=5.0\\,\\mathrm{s}$, $\\theta=15(5)+\\tfrac12(-3)(25)=37.5\\,\\mathrm{rad}$. Then $K_i=\\tfrac12 I\\omega^2=90\\,\\mathrm{J}$ goes to zero, matching $|W|=|\\tau\\theta|=90\\,\\mathrm{J}$.",
         ["$4.0\\,\\mathrm{s}$ of time only", "$18\\,\\mathrm{J}$", "$0$ because $\\tau$ is internal"]),
        ("AP Stretch: Why can you choose any axis for $\\sum\\tau=0$ in statics?",
         "if the object has $a_{\\mathrm{cm}}=0$ and $\\alpha=0$, torque about every axis is zero",
         "Pick the axis that removes the most unknowns. This is an AP FRQ habit.",
         ["only the CM axis is legal", "only a hinge is legal", "torque is not a real quantity"]),
    ])
    return qs


def build_unit5():
    title = "AP Physics Unit 5: Torque and Rotational Dynamics"
    description = (
        "Angular kinematics, torque, rotational inertia, $\\tau=I\\alpha$, rolling without slipping, and static "
        "equilibrium — algebra-based AP Physics 1."
    )
    concepts = [
        "Angular displacement and velocity",
        "Torque",
        "Rotational inertia",
        "Newton 2 for rotation",
        "Rolling without slipping",
        "Static equilibrium",
    ]

    c1 = concept_block(
        "1. Angular displacement and velocity",
        [
            "A rigid body turning about a fixed axis needs an angle. Angular displacement $\\theta$ is measured in "
            "radians in every AP formula. One full turn is $2\\pi$ radians, not $360$ in the $s=r\\theta$ equation.",
            "Arc length along a circle is $s=r\\theta$ with $\\theta$ in radians. A wheel of radius $0.50\\,\\mathrm{m}$ that "
            "turns $2.0\\,\\mathrm{rad}$ moves a rim point $1.0\\,\\mathrm{m}$ along the rim.",
            "Average angular velocity is $\\omega=\\Delta\\theta/\\Delta t$, in $\\mathrm{rad/s}$. If a disk turns $6.0\\,\\mathrm{rad}$ "
            "in $2.0\\,\\mathrm{s}$, $\\omega=3.0\\,\\mathrm{rad/s}$. That ratio is the definition of average $\\omega$.",
            "A point at radius $r$ has linear speed $v=r\\omega$, tangent to the circle. The same $\\omega$ gives larger "
            "$v$ farther from the axis. Rim of $r=0.25\\,\\mathrm{m}$ at $\\omega=8.0\\,\\mathrm{rad/s}$ has $v=2.0\\,\\mathrm{m/s}$.",
            "If $\\omega$ is constant, speed is constant, but velocity keeps changing direction. There is still a "
            "center-pointing acceleration $v^2/r$. Angular acceleration $\\alpha=\\Delta\\omega/\\Delta t$ is zero in that special case.",
            "The translation dictionary: $\\theta\\leftrightarrow x$, $\\omega\\leftrightarrow v$, $\\alpha\\leftrightarrow a$. "
            "The constant-$\\alpha$ equations look like the Unit 1 set: $\\omega=\\omega_0+\\alpha t$, $\\theta=\\omega_0 t+\\tfrac12\\alpha t^2$, $\\omega^2=\\omega_0^2+2\\alpha\\theta$.",
        ],
        "Rolling, $K_{\\mathrm{rot}}$, and $\\tau=I\\alpha$ all use $\\omega$ in $\\mathrm{rad/s}$. If you feed degrees into $v=r\\omega$, "
        "every later numeric answer in this unit will be wrong by a factor of $\\pi/180$.",
        "Convert to radians first. Then $s=r\\theta$ and $v=r\\omega$ are ordinary multiplications.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: 3 * t, 0, 4))],
                points=[(0, 0, "start"), (4, 12, "θ=12 rad")],
                xlim=(-0.3, 5), ylim=(-1, 14), xlab="t (s)", ylab="θ (rad)", w=300, h=240,
            ),
            "Angle versus time at constant $\\omega=3\\,\\mathrm{rad/s}$",
            "Straight $\\theta$-$t$ line: slope is $\\omega$. Analog of constant-velocity $x$-$t$.",
        )
        + solved(1, "A wheel of radius $0.50\\,\\mathrm{m}$ turns $2.0\\,\\mathrm{rad}$. Find the arc length a rim point travels.",
                 ["Use $s=r\\theta$ with $\\theta$ in radians.",
                  "$s=(0.50)(2.0)=1.0\\,\\mathrm{m}$.",
                  "If someone used $2^\\circ$ by mistake, the answer would be nonsense."],
                 "$1.0\\,\\mathrm{m}$", "", "Easy")
        + solved(2, "A disk rotates $6.0\\,\\mathrm{rad}$ in $2.0\\,\\mathrm{s}$ at constant $\\omega$. Find $\\omega$ and the rim speed if $R=0.40\\,\\mathrm{m}$.",
                 ["$\\omega=\\Delta\\theta/\\Delta t=6/2=3.0\\,\\mathrm{rad/s}$.",
                  "$v=R\\omega=(0.40)(3.0)=1.2\\,\\mathrm{m/s}$.",
                  "Direction of $\\vec{v}$ is tangent, not along a radius."],
                 "$\\omega=3.0\\,\\mathrm{rad/s}$, $v=1.2\\,\\mathrm{m/s}$", "", "Medium")
        + solved(3, "A wheel starts at rest and has constant $\\alpha=4.0\\,\\mathrm{rad/s}^2$ for $3.0\\,\\mathrm{s}$. Find $\\omega$ and $\\theta$.",
                 ["$\\omega=\\omega_0+\\alpha t=0+4(3)=12\\,\\mathrm{rad/s}$.",
                  "$\\theta=\\omega_0 t+\\tfrac12\\alpha t^2=\\tfrac12(4)(9)=18\\,\\mathrm{rad}$.",
                  "Check: $\\omega^2=0+2(4)(18)=144$, $\\omega=12\\,\\mathrm{rad/s}$.",
                  "Same algebra as $v=v_0+at$ and $\\Delta x=v_0 t+\\tfrac12 at^2$."],
                 "$\\omega=12\\,\\mathrm{rad/s}$, $\\theta=18\\,\\mathrm{rad}$", "", "Hard"),
        ("Leaving $\\theta$ in degrees inside $s=r\\theta$",
         "The radian is the ratio of arc to radius, a pure number that makes $s=r\\theta$ true. Degrees require a conversion first: multiply by $\\pi/180$."),
        ("Write the translation dictionary on the page",
         "$\\theta,\\omega,\\alpha$ beside $x,v,a$. Then steal the Unit 1 equations with new letters."),
        [
            "I can use $s=r\\theta$ and $v=r\\omega$ with $\\theta$ in radians.",
            "I can compute $\\omega=\\Delta\\theta/\\Delta t$ from a time interval.",
            "I can apply the constant-$\\alpha$ angular equations analogously to Unit 1.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Torque",
        [
            "Torque is a twist: $\\tau=r F\\sin\\phi$, where $\\vec{r}$ goes from the axis to the point where $\\vec{F}$ is applied "
            "and $\\phi$ is the angle between those two vectors. The SI unit is the newton-meter, $\\mathrm{N\\cdot m}$.",
            "When $\\phi=90^\\circ$, $\\sin\\phi=1$ and $\\tau=rF$. A $10\\,\\mathrm{N}$ force at $2.0\\,\\mathrm{m}$ perpendicular to a wrench "
            "gives $\\tau=20\\,\\mathrm{N\\cdot m}$. When $\\phi=0$, the force is along the rod and $\\tau=0$.",
            "Lever arm $d_\\perp$ is the perpendicular distance from the axis to the force's line of action. Then $\\tau=F d_\\perp$, "
            "the same number. A $12\\,\\mathrm{N}$ force with lever arm $0.25\\,\\mathrm{m}$ gives $3.0\\,\\mathrm{N\\cdot m}$.",
            "Doorknobs sit far from hinges because larger $r$ means larger torque for a tired human's limited $F$. "
            "Pushing near the hinge is a workout with little $\\alpha$.",
            "Torque has a sense: clockwise or counterclockwise. Assign $+$ to one sense and keep it, just as you did "
            "for one-dimensional forces.",
            "A pair of equal opposite forces that do not share a line (a couple) can have $\\sum F=0$ while $\\sum\\tau\\neq 0$. "
            "The object then spins about the CM without the CM accelerating.",
        ],
        "Equilibrium, rolling friction's job, and $\\tau=I\\alpha$ all start with a correct torque. A force drawn without "
        "a lever arm is not yet a torque.",
        "Draw the axis. Draw $\\vec{r}$ and $\\vec{F}$. Either use $rF\\sin\\phi$ or measure $d_\\perp$ and use $F d_\\perp$.",
        lesson_figure(
            _seesaw_svg(),
            "Two weights on a seesaw: torques about the fulcrum",
            "Each weight's torque is $mg$ times its horizontal distance to the pivot when the board is level.",
        )
        + solved(4, "A perpendicular $10\\,\\mathrm{N}$ force acts $2.0\\,\\mathrm{m}$ from an axis. Find $\\tau$.",
                 ["$\\phi=90^\\circ$, $\\sin\\phi=1$.",
                  "$\\tau=rF=20\\,\\mathrm{N\\cdot m}$.",
                  "Sense: the way the force would twist about that axis."],
                 "$20\\,\\mathrm{N\\cdot m}$", "", "Easy")
        + solved(5, "A $25\\,\\mathrm{N}$ force is applied at $37^\\circ$ to a $0.40\\,\\mathrm{m}$ wrench ($\\sin 37^\\circ=0.60$). Find $\\tau$.",
                 ["$\\tau=rF\\sin\\phi=(0.40)(25)(0.60)=6.0\\,\\mathrm{N\\cdot m}$.",
                  "If the force were along the wrench, $\\tau$ would be $0$.",
                  "The parallel component does not twist."],
                 "$6.0\\,\\mathrm{N\\cdot m}$", "", "Medium")
        + solved(6, "A $20\\,\\mathrm{kg}$ child sits $1.5\\,\\mathrm{m}$ left of a seesaw pivot. Where should a $30\\,\\mathrm{kg}$ child sit on the right to balance? ($g=10$)",
                 ["Balance means $\\sum\\tau=0$ (and the pivot supplies the net vertical force).",
                  "Left torque: $(200\\,\\mathrm{N})(1.5\\,\\mathrm{m})=300\\,\\mathrm{N\\cdot m}$.",
                  "Right: $(300\\,\\mathrm{N})x=300$, so $x=1.0\\,\\mathrm{m}$.",
                  "The heavier child sits closer to the pivot."],
                 "$1.0\\,\\mathrm{m}$ to the right of the pivot", "", "Hard"),
        ("Using $\\tau=rF$ when the force is not perpendicular",
         "The sine (or the lever arm) is required. A force through the axis always gives zero torque, even if it is huge."),
        ("Pick a sign for clockwise versus counterclockwise before adding",
         "Then $\\sum\\tau$ is an ordinary signed sum, the rotational twin of $\\sum F_x$."),
        [
            "I can compute $\\tau=rF\\sin\\phi$ with $\\mathrm{N\\cdot m}$.",
            "I can use lever arm $d_\\perp$ as an equivalent method.",
            "I can balance a seesaw with $\\sum\\tau=0$.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Rotational inertia",
        [
            "Rotational inertia $I$ (also called moment of inertia) says how hard it is to change $\\omega$. "
            "For a single point mass, $I=mr^2$. A $2.0\\,\\mathrm{kg}$ mass on a $0.50\\,\\mathrm{m}$ stick about the far end has $I=0.50\\,\\mathrm{kg\\cdot m}^2$.",
            "Mass farther from the axis counts more because of the $r^2$. That is why a long wrench is easier to start "
            "turning — and why a skater spins faster after pulling mass inward (Unit 6 will add $L$ conservation).",
            "AP Physics 1 gives you catalog formulas: hoop or thin ring about its center $I=mR^2$; solid disk or cylinder "
            "about its central axis $I=\\tfrac12 mR^2$; solid sphere about a diameter $I=\\tfrac25 mR^2$. Use the catalog; do not try to invent $I$ from a picture of slices.",
            "A $4.0\\,\\mathrm{kg}$ hoop of $R=0.50\\,\\mathrm{m}$ has $I=1.0\\,\\mathrm{kg\\cdot m}^2$. The same mass as a disk has $I=0.50\\,\\mathrm{kg\\cdot m}^2$. "
            "The disk is easier to spin.",
            "For several point masses, add: $I=\\sum m_i r_i^2$. Two equal masses on a dumbbell about the midpoint: "
            "$I=2m(\\ell/2)^2=m\\ell^2/2$ if the bar is massless and length $\\ell$.",
            "$I$ depends on the axis. The same object has a different $I$ about a different line. Always name the axis "
            "when you quote $I$.",
        ],
        "$\\tau=I\\alpha$ is useless if $I$ is the wrong catalog formula. Rolling races are secretly $I$ comparisons.",
        "Identify the object (hoop, disk, point mass) and the axis. Write the matching $I$, then stop — do not invent a new formula.",
        lesson_figure(
            _hoop_disk_svg(),
            "Mass distributed at radius $R$ versus packed nearer the hub",
            "A hoop puts all mass at $R$ ($I=mR^2$). A disk puts some mass closer in ($I=\\tfrac12 mR^2$).",
        )
        + solved(7, "A $2.0\\,\\mathrm{kg}$ point mass is $0.50\\,\\mathrm{m}$ from an axis. Find $I$.",
                 ["$I=mr^2=(2.0)(0.25)=0.50\\,\\mathrm{kg\\cdot m}^2$.",
                  "Units: $\\mathrm{kg\\cdot m}^2$.",
                  "If $r$ doubled, $I$ would quadruple."],
                 "$0.50\\,\\mathrm{kg\\cdot m}^2$", "", "Easy")
        + solved(8, "A $4.0\\,\\mathrm{kg}$ hoop and a $4.0\\,\\mathrm{kg}$ disk both have $R=0.50\\,\\mathrm{m}$. Compare $I$ about the center.",
                 ["Hoop: $I=mR^2=4(0.25)=1.0\\,\\mathrm{kg\\cdot m}^2$.",
                  "Disk: $I=\\tfrac12 mR^2=0.50\\,\\mathrm{kg\\cdot m}^2$.",
                  "Same torque would give the disk twice the $\\alpha$."],
                 "hoop $1.0$, disk $0.50\\,\\mathrm{kg\\cdot m}^2$", "", "Medium")
        + solved(9, "Masses $m$ and $2m$ sit at opposite ends of a massless rod of length $2\\ell$. Find $I$ about the midpoint.",
                 ["Each mass is a distance $\\ell$ from the midpoint.",
                  "$I=m\\ell^2+(2m)\\ell^2=3m\\ell^2$.",
                  "The CM is not at the midpoint; it is closer to $2m$. This $I$ is still about the geometric middle, which is a legal axis.",
                  "If you needed $I$ about the CM you would shift the axis (not required on every AP item)."],
                 "$I=3m\\ell^2$ about the midpoint", "", "Hard"),
        ("Using $I=mR^2$ for a solid disk",
         "That formula is the hoop. A disk is $\\tfrac12 mR^2$. Mixing them reverses who wins a rolling race."),
        ("Write the object name and the axis next to $I$",
         "“Disk about central axis: $\\tfrac12 mR^2$.” That one line prevents catalog mix-ups on FRQs."),
        [
            "I can compute $I=mr^2$ for a point mass.",
            "I can select $I=mR^2$ versus $I=\\tfrac12 mR^2$ for hoop versus disk.",
            "I can add point-mass contributions $I=\\sum mr^2$.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Newton's second law for rotation",
        [
            "The rotational twin of $F_{\\mathrm{net}}=ma$ is $\\tau_{\\mathrm{net}}=I\\alpha$. Net torque about an axis equals "
            "$I$ about that same axis times angular acceleration about that axis.",
            "If $I=2.0\\,\\mathrm{kg\\cdot m}^2$ and $\\tau_{\\mathrm{net}}=8.0\\,\\mathrm{N\\cdot m}$, then $\\alpha=4.0\\,\\mathrm{rad/s}^2$. "
            "Direction of $\\alpha$ matches the net torque's sense.",
            "A tangent force $F$ at the rim of a disk gives $\\tau=RF$ if the force is perpendicular to the radius. "
            "Then $\\alpha=RF/I$. For $I=0.50$, $R=0.20$, $F=10$, $\\alpha=4.0\\,\\mathrm{rad/s}^2$.",
            "If torques cancel, $\\alpha=0$ and $\\omega$ is constant (including zero). That is the rotational first law, "
            "used constantly in statics.",
            "A pulley with nonzero $I$ needs a net torque. The two string tensions are then not equal: $(T_2-T_1)R=I\\alpha$. "
            "The massless-pulley shortcut is the $I=0$ special case.",
            "Always use one consistent axis. Mixing $\\tau$ about a hinge with $I$ about the CM is a mismatch unless you "
            "know the parallel-axis story (beyond typical AP 1 algebra drills).",
        ],
        "Atwood machines with massive pulleys (Unit 6) are this law plus $F=ma$ for each hanging mass. Get $\\tau=I\\alpha$ "
        "clean now.",
        "List torques about one axis, sum them with signs, set the sum equal to $I\\alpha$ with that same $I$.",
        lesson_figure(
            _pulley_svg(),
            "A pulley with rotational inertia $I$",
            "String tensions need not match if $I\\neq 0$. Net torque $ (T_2-T_1)R=I\\alpha$.",
        )
        + solved(10, "Given $I=2.0\\,\\mathrm{kg\\cdot m}^2$ and $\\tau_{\\mathrm{net}}=8.0\\,\\mathrm{N\\cdot m}$, find $\\alpha$.",
                 ["$\\alpha=\\tau/I=8/2=4.0\\,\\mathrm{rad/s}^2$.",
                  "Units: $\\mathrm{N\\cdot m}/(\\mathrm{kg\\cdot m}^2)=\\mathrm{rad/s}^2$.",
                  "Same pattern as $a=F/m$."],
                 "$4.0\\,\\mathrm{rad/s}^2$", "", "Easy")
        + solved(11, "A disk $I=0.50\\,\\mathrm{kg\\cdot m}^2$ and $R=0.20\\,\\mathrm{m}$ is pulled by a $10\\,\\mathrm{N}$ tangent force. Find $\\alpha$ (axle frictionless).",
                 ["$\\tau=RF=2.0\\,\\mathrm{N\\cdot m}$.",
                  "$\\alpha=2.0/0.50=4.0\\,\\mathrm{rad/s}^2$.",
                  "If a second opposite $10\\,\\mathrm{N}$ acted at the other side as a couple, $\\tau$ would double."],
                 "$4.0\\,\\mathrm{rad/s}^2$", "", "Medium")
        + solved(12, "A potter's wheel $I=2.0\\,\\mathrm{kg\\cdot m}^2$ spins at $8.0\\,\\mathrm{rad/s}$. A brake applies $\\tau=-4.0\\,\\mathrm{N\\cdot m}$. Find time to stop and the angle while stopping.",
                 ["$\\alpha=\\tau/I=-2.0\\,\\mathrm{rad/s}^2$.",
                  "$0=8.0+(-2.0)t$ so $t=4.0\\,\\mathrm{s}$.",
                  "$\\theta=\\omega_0 t+\\tfrac12\\alpha t^2=8(4)+\\tfrac12(-2)(16)=32-16=16\\,\\mathrm{rad}$.",
                  "Or $\\omega^2=\\omega_0^2+2\\alpha\\theta\\Rightarrow 0=64-4\\theta$, $\\theta=16\\,\\mathrm{rad}$."],
                 "$4.0\\,\\mathrm{s}$, $16\\,\\mathrm{rad}$", "", "Hard"),
        ("Using $F=ma$ on a rotating disk as if $a$ were $r\\alpha$ without a torque equation",
         "The CM may not even be accelerating. Rotation about a fixed axle is $\\tau=I\\alpha$, not a fake linear $F=ma$ on the rim."),
        ("Keep $\\tau$, $I$, and $\\alpha$ about the same axis",
         "Write the axis in words: “about the axle.” Then the symbols match."),
        [
            "I can solve $\\alpha=\\tau_{\\mathrm{net}}/I$.",
            "I can find $\\tau=RF$ for a tangent rim force.",
            "I can combine $\\tau=I\\alpha$ with constant-$\\alpha$ kinematics to stop a wheel.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Rolling without slipping",
        [
            "Rolling without slipping ties translation to rotation: $v_{\\mathrm{cm}}=\\omega R$ and $a_{\\mathrm{cm}}=\\alpha R$. "
            "The contact point is instantaneously at rest relative to the surface.",
            "A wheel with $R=0.40\\,\\mathrm{m}$ and $\\omega=5.0\\,\\mathrm{rad/s}$ has $v_{\\mathrm{cm}}=2.0\\,\\mathrm{m/s}$ if it rolls without slipping. "
            "If $v>\\omega R$, the tire is skidding (kinetic friction).",
            "Total kinetic energy is $K=\\tfrac12 m v_{\\mathrm{cm}}^2+\\tfrac12 I\\omega^2$. With $\\omega=v/R$, a disk ($I=\\tfrac12 mR^2$) has "
            "$K=\\tfrac34 mv^2$. A hoop ($I=mR^2$) has $K=mv^2$.",
            "Static friction can act up the ramp to provide the torque that increases $\\omega$ as the object speeds up. "
            "On ice (frictionless), a ball slides: $a=g\\sin\\theta$ with $\\alpha=0$.",
            "Energy on a hill: $mgh=\\tfrac12 mv^2+\\tfrac12 I(v/R)^2=\\tfrac12 m(1+I/mR^2)v^2$. A disk reaches "
            "$v=\\sqrt{4gh/3}$. A hoop reaches only $\\sqrt{gh}$. The disk wins the race.",
            "Acceleration down a ramp without slipping is $a=g\\sin\\theta/(1+I/mR^2)$. For a disk, $a=\\tfrac23 g\\sin\\theta$. "
            "Smaller $I$ means larger $a$.",
        ],
        "Unit 6 energy problems with rolling objects reuse this $K$ split. If you only write $\\tfrac12 mv^2$ for a rolling "
        "disk, you will overshoot the speed at the bottom.",
        "Write $v=\\omega R$ first. Then $K$ has two pieces. Then $mgh$ equals that sum if the hill is friction-enough-to-roll but not dissipative (static friction does no work if the contact point does not slide).",
        lesson_figure(
            _wheel_svg(),
            "Rolling without slipping: $v=\\omega R$",
            "The hub moves forward at $v$ while the wheel spins at $\\omega=v/R$. Contact point is instantaneously at rest.",
        )
        + solved(13, "A wheel of $R=0.40\\,\\mathrm{m}$ rolls without slipping at $\\omega=5.0\\,\\mathrm{rad/s}$. Find $v_{\\mathrm{cm}}$.",
                 ["$v=\\omega R=(5.0)(0.40)=2.0\\,\\mathrm{m/s}$.",
                  "If it were sliding with $\\omega=0$, $v$ would be independent of $R$.",
                  "No-slip is the link."],
                 "$2.0\\,\\mathrm{m/s}$", "", "Easy")
        + solved(14, "A $4.0\\,\\mathrm{kg}$ disk rolls at $v=4.0\\,\\mathrm{m/s}$ without slipping. Find total $K$.",
                 ["$K=\\tfrac34 mv^2=\\tfrac34(4.0)(16)=48\\,\\mathrm{J}$.",
                  "Translational piece $\\tfrac12 mv^2=32\\,\\mathrm{J}$.",
                  "Rotational piece $16\\,\\mathrm{J}$."],
                 "$48\\,\\mathrm{J}$", "", "Medium")
        + solved(15, "A disk and a hoop, same $m$ and $R$, roll from rest down height $h$. Compare $v$ at the bottom (no slipping, no energy loss).",
                 ["Disk: $mgh=\\tfrac34 mv^2\\Rightarrow v=\\sqrt{4gh/3}$.",
                  "Hoop: $mgh=mv^2\\Rightarrow v=\\sqrt{gh}$.",
                  "Disk is faster: $\\sqrt{4/3}\\,\\sqrt{gh}$ versus $\\sqrt{gh}$.",
                  "Both beat a sliding frictionless block? No: a sliding block on ice would get $\\sqrt{2gh}$, faster still, because none of $mgh$ is stored in spin — but it is not rolling."],
                 "disk $\\sqrt{4gh/3}$, hoop $\\sqrt{gh}$; disk wins", "", "Hard"),
        ("Writing only $\\tfrac12 mv^2$ for a rolling object",
         "You omitted $\\tfrac12 I\\omega^2$. The object is both moving and spinning. Both stores of $K$ count."),
        ("Use static friction for $\\tau$ but not as a worker if there is no slipping",
         "The contact point is instantaneously at rest, so static friction's work is zero in the standard model. Energy still conserves mechanically."),
        [
            "I can use $v=\\omega R$ for rolling without slipping.",
            "I can write $K=\\tfrac12 mv^2+\\tfrac12 I\\omega^2$ and simplify with $v=\\omega R$.",
            "I can compare disk and hoop speeds from the same height $h$.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Static equilibrium",
        [
            "An extended object is in static equilibrium when it is not translating and not rotating: "
            "$\\sum F_x=0$, $\\sum F_y=0$, and $\\sum\\tau=0$. Rest is the usual AP case ($v=0$, $\\omega=0$).",
            "You may compute torques about any axis you like in statics. Choose an axis through an unknown force to "
            "make that force's torque zero. Hinges love this trick.",
            "A uniform beam's weight acts at its center. A $4.0\\,\\mathrm{m}$ plank of weight $200\\,\\mathrm{N}$ supported at both ends "
            "has $100\\,\\mathrm{N}$ at each end by symmetry.",
            "Seesaws: $m_1 g r_1=m_2 g r_2$ for a massless board. The $20\\,\\mathrm{kg}$ and $30\\,\\mathrm{kg}$ children at $1.5\\,\\mathrm{m}$ "
            "and $1.0\\,\\mathrm{m}$ were this rule.",
            "If $\\sum F=0$ but $\\sum\\tau\\neq 0$, the CM stays put (or moves steadily) while the object spins up. "
            "Both conditions are required to “just sit there.”",
            "FRQ habit: draw every force on the beam, pick an axis, write $\\sum\\tau=0$, then use $\\sum F_y=0$ for the leftover support.",
        ],
        "This is the last purely translational/rotational statics skill before Unit 6 adds $L$ and rolling $K$. "
        "Ladder and hanging-sign problems are this lesson with extra geometry.",
        "Draw the beam. Place $mg$ at the CM. Pick the axis that deletes the ugliest unknown. Solve $\\sum\\tau=0$, then $\\sum F$.",
        lesson_figure(
            _seesaw_svg(),
            "Balanced seesaw: $\\sum\\tau=0$ about the fulcrum",
            "The fulcrum's force has zero lever arm, so it drops out of the torque equation — then $\\sum F_y=0$ finds it.",
        )
        + solved(16, "A uniform $4.0\\,\\mathrm{m}$ plank weighs $200\\,\\mathrm{N}$ and rests on two end supports. Find each support force.",
                 ["By symmetry, each support holds $100\\,\\mathrm{N}$.",
                  "Check torques about the left end: $200(2.0)=N_R(4.0)$, so $N_R=100\\,\\mathrm{N}$.",
                  "Then $N_L+N_R=200$, $N_L=100\\,\\mathrm{N}$."],
                 "$100\\,\\mathrm{N}$ each", "", "Easy")
        + solved(17, "The same plank now has a $100\\,\\mathrm{N}$ person at the midpoint. Find each support.",
                 ["Total load $300\\,\\mathrm{N}$, still symmetric.",
                  "Each support $150\\,\\mathrm{N}$.",
                  "Torque about left: $200(2)+100(2)=N_R(4)$, $600=4N_R$, $N_R=150\\,\\mathrm{N}$."],
                 "$150\\,\\mathrm{N}$ each", "", "Medium")
        + solved(18, "A $3.0\\,\\mathrm{m}$ uniform beam weighs $180\\,\\mathrm{N}$, hinged on the left, with a vertical cable at the right end. A $120\\,\\mathrm{N}$ sign hangs $1.0\\,\\mathrm{m}$ from the hinge. Find the cable tension.",
                 ["Axis at the hinge so the hinge forces drop out of $\\sum\\tau$.",
                  "Beam CM at $1.5\\,\\mathrm{m}$: torque $180(1.5)=270\\,\\mathrm{N\\cdot m}$.",
                  "Sign: $120(1.0)=120\\,\\mathrm{N\\cdot m}$. Cable: $T(3.0)$.",
                  "$270+120=3T$, so $T=130\\,\\mathrm{N}$."],
                 "$130\\,\\mathrm{N}$", "", "Hard"),
        ("Forgetting the beam's own weight at the CM",
         "A uniform beam is not massless unless the problem says so. Put $mg$ at the midpoint."),
        ("Put the axis on a hinge or support with two unknown components",
         "Those forces then have zero lever arm. $\\sum\\tau=0$ becomes a one-unknown equation for the remaining torque."),
        [
            "I can state the three equilibrium conditions $\\sum F_x$, $\\sum F_y$, $\\sum\\tau$.",
            "I can choose an axis that removes unknown forces from the torque sum.",
            "I can solve a hinged-beam plus cable problem for tension.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Energy and Momentum of Rotating Systems
# ===========================================================================

def _u6_questions():
    qs = []
    _add(qs, [
        ("Rotational kinetic energy is $K_{\\mathrm{rot}}=\\tfrac12 I\\omega^2$. A disk with $I=0.50\\,\\mathrm{kg\\cdot m}^2$ at $\\omega=4.0\\,\\mathrm{rad/s}$ has $K_{\\mathrm{rot}}=$",
         "$4.0\\,\\mathrm{J}$",
         "$K=\\tfrac12(0.50)(16)=4.0\\,\\mathrm{J}$.",
         ["$2.0\\,\\mathrm{J}$", "$8.0\\,\\mathrm{J}$", "$1.0\\,\\mathrm{J}$"]),
        ("Doubling $\\omega$ multiplies $K_{\\mathrm{rot}}$ by",
         "$4$",
         "$K\\propto\\omega^2$, same as $K\\propto v^2$ in translation.",
         ["$2$", "$8$", "$1$"]),
        ("A hoop rolling at $v$ has $K_{\\mathrm{tot}}=mv^2$. The rotational share of that total is",
         "half",
         "$\\tfrac12 mv^2$ translational and $\\tfrac12 mv^2$ rotational.",
         ["all of it", "one quarter", "none"]),
        ("Work by a torque through angle $\\theta$ (radians) is $W=\\tau\\theta$ when $\\tau$ is constant. $\\tau=5.0\\,\\mathrm{N\\cdot m}$ through $2.0\\,\\mathrm{rad}$ does",
         "$10\\,\\mathrm{J}$",
         "$W=(5)(2)=10\\,\\mathrm{J}=\\Delta K_{\\mathrm{rot}}$ if it is the net torque.",
         ["$2.5\\,\\mathrm{J}$", "$7.0\\,\\mathrm{J}$", "$0$"]),
        ("A rolling object's gravitational $U$ still uses $h$ of the",
         "center of mass",
         "$U=mgh_{\\mathrm{cm}}$. Rotation does not change that height story.",
         ["the contact point always", "the highest pebble on the rim only", "zero always"]),
    ])
    _add(qs, [
        ("Angular momentum of a rigid body about a fixed axis is $L=I\\omega$. If $I=2.0\\,\\mathrm{kg\\cdot m}^2$ and $\\omega=3.0\\,\\mathrm{rad/s}$, $L$ is",
         "$6.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$",
         "$L=I\\omega=6.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
         ["$1.5\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "$5.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "$0.67\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$"]),
        ("A point particle has $L=mvr_{\\perp}$ (or $r mv\\sin\\phi$). A $2.0\\,\\mathrm{kg}$ blob at $4.0\\,\\mathrm{m/s}$ with perpendicular lever arm $0.50\\,\\mathrm{m}$ has $L=$",
         "$4.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$",
         "$L=(2)(4)(0.50)=4.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
         ["$16\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "$1.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "$8.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$"]),
        ("The analog of $J=\\Delta p$ is $\\tau_{\\mathrm{net}}\\Delta t=\\Delta L$ (impulse of torque). A $3.0\\,\\mathrm{N\\cdot m}$ torque for $2.0\\,\\mathrm{s}$ changes $L$ by",
         "$6.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$",
         "$\\Delta L=\\tau\\Delta t=6.0$.",
         ["$1.5$", "$5.0$", "$0$"]),
        ("Direction of $\\vec{L}$ for AP 1 is usually just a sense: into the page or out, matching $\\omega$. Reversing $\\omega$ reverses",
         "$L$",
         "Angular momentum is a signed (or right-hand) quantity.",
         ["mass", "$g$", "the radius only"]),
        ("A particle moving straight at constant $v$ can still have nonzero $L$ about a point not on its line because",
         "the lever arm $r_\\perp$ need not be zero",
         "$L=mv d$ with $d$ the perpendicular distance from the point to the line of motion.",
         ["$L$ must be zero if $a=0$", "mass is zero", "time stopped"]),
    ])
    _add(qs, [
        ("If net external torque on a system is zero, angular momentum of that system is",
         "conserved",
         "Internal torques cancel in pairs. Ice-skater, turntable, and exploding disk problems live here.",
         ["zero always", "equal to $K$", "undefined"]),
        ("A skater with $I_i=4.0\\,\\mathrm{kg\\cdot m}^2$ at $\\omega_i=2.0\\,\\mathrm{rad/s}$ pulls arms in to $I_f=2.0\\,\\mathrm{kg\\cdot m}^2$. $\\omega_f$ is",
         "$4.0\\,\\mathrm{rad/s}$",
         "$I\\omega$ constant: $8=2\\omega_f$, $\\omega_f=4.0\\,\\mathrm{rad/s}$.",
         ["$2.0\\,\\mathrm{rad/s}$", "$1.0\\,\\mathrm{rad/s}$", "$8.0\\,\\mathrm{rad/s}$"]),
        ("That skater's $K_{\\mathrm{rot}}$ compared with before is",
         "doubled (work was done pulling the arms in)",
         "$K=\\tfrac12 I\\omega^2$: $I$ halves, $\\omega$ doubles, $K$ doubles. The skater's muscles did positive work.",
         ["halved", "unchanged", "zero"]),
        ("A child steps onto a resting merry-go-round. If the axle is frictionless, $L$ of child+wheel is",
         "conserved (external axle force has no torque if it is at the axis)",
         "The child's linear $mvr$ becomes shared $I\\omega$. $K$ drops.",
         ["not conserved because the child moved", "equal to $mg$", "infinite"]),
        ("Dropping a spinning disk onto a resting disk (they then rotate together) conserves",
         "$L$ about the common axis if axle torque is negligible during the stick",
         "It is the rotational analog of a perfectly inelastic collision.",
         ["$K$ only", "both $L$ and $K$", "neither"]),
    ])
    _add(qs, [
        ("A $0.20\\,\\mathrm{kg}$ blob at $5.0\\,\\mathrm{m/s}$ hits and sticks at the rim of a resting disk ($R=0.40\\,\\mathrm{m}$, $I_{\\mathrm{disk}}=0.080\\,\\mathrm{kg\\cdot m}^2$). $L$ before about the disk axis is",
         "$0.40\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$",
         "$L=m v R=(0.20)(5.0)(0.40)=0.40$ if $v$ is perpendicular.",
         ["$1.0$", "$0.080$", "$0$"]),
        ("After they stick, $I_{\\mathrm{tot}}=I_{\\mathrm{disk}}+mR^2=0.080+0.032=0.112\\,\\mathrm{kg\\cdot m}^2$. Then $\\omega=$",
         "$3.57\\,\\mathrm{rad/s}$ approximately, $0.40/0.112$",
         "$L_f=I\\omega=0.40$, $\\omega=0.40/0.112\\approx 3.57\\,\\mathrm{rad/s}$.",
         ["$5.0\\,\\mathrm{rad/s}$", "$0$", "$12.5\\,\\mathrm{rad/s}$"]),
        ("Kinetic energy in that stick-and-spin",
         "decreases (rotational inelastic collision)",
         "Some $K$ becomes thermal at the latch.",
         ["increases", "is conserved", "becomes negative"]),
        ("A bullet missing the axis but caught in a door is modeled as",
         "conserving $L$ about the hinge if the hinge's impulse has zero torque",
         "The hinge can exert force (change $p$) with no $\\tau$.",
         ["conserving linear $p$ of the door alone", "conserving $K$", "using $F=ma$ only on the bullet afterward"]),
        ("If the blob bounces off elastically instead of sticking, you would also need",
         "a second equation ($K$ or relative speed), not $L$ alone",
         "$L$ conservation is one equation; two unknown final speeds need more.",
         ["nothing else", "mass to vanish", "$g=9.8$"]),
    ])
    _add(qs, [
        ("Two masses $m$ and $2m$ hang on a massive pulley $I$, radius $R$. The linear acceleration satisfies $(2m-m)g=(m+2m+I/R^2)a$. If $I=0$, $a$ is",
         "$g/3$",
         "Light-pulley Atwood: $a=(2m-m)g/(3m)=g/3$.",
         ["$g$", "$g/2$", "$2g/3$"]),
        ("If the pulley has $I=mR^2$, that same pair has $a=$",
         "$g/4$",
         "Denominator $3m+m=4m$, $a=mg/(4m)=g/4$, smaller because some energy/inertia is in the pulley.",
         ["$g/3$", "$g$", "$g/5$"]),
        ("Tensions on the two sides of a massive pulley are",
         "unequal (their difference provides $\\tau$)",
         "$(T_{\\mathrm{large}}-T_{\\mathrm{small}})R=I\\alpha$.",
         ["always equal", "both zero", "both $mg$"]),
        ("A string unwinding from a yo-yo-like disk: you must write",
         "$mg-T=ma$ and $TR=I\\alpha$ with $a=\\alpha R$",
         "Two Newton's laws plus the rolling/unwinding link.",
         ["only $T=mg$", "only energy, never forces", "Pascal's principle"]),
        ("Energy check on a massive-pulley Atwood: loss of $U_g$ equals",
         "$K$ of both masses plus $K_{\\mathrm{rot}}$ of the pulley",
         "Three energy stores. Forgetting the pulley $K$ overestimates speeds.",
         ["only the heavier mass's $K$", "heat only", "nothing; energy fails"]),
    ])
    _add(qs, [
        ("Justifying a conservation law on an AP FRQ means naming the system and the condition. $L$ is conserved if",
         "net external torque about the stated axis is zero (or negligible during the event)",
         "“Frictionless axle” or “impulse at the hinge” are the usual justifications.",
         ["the object is moving", "$K$ is large", "mass is in kilograms"]),
        ("Linear $p$ of a system is conserved if",
         "net external impulse is zero",
         "Different condition from $L$. A hinge can change $p$ without changing $L$ about the hinge.",
         ["$\\tau_{\\mathrm{net}}=0$ only", "always", "never during collisions"]),
        ("Mechanical energy is conserved if",
         "no nonconservative work (or it is accounted as $E_{\\mathrm{th}}$)",
         "A latching collision conserves $L$ but not $K$.",
         ["$L$ is conserved, therefore $K$ is too", "always in rotation", "never with pulleys"]),
        ("Choosing “the two disks plus the axle” as the system for a drop-on-disk collision lets you",
         "treat axle forces as having no torque if they act at the axis",
         "System choice is the justification. Write it in a sentence.",
         ["ignore mass", "set $g=0$", "use Bernoulli"]),
        ("An FRQ that asks “whether $K$ increases when the skater pulls in” wants you to say",
         "the skater does positive work; $L$ is conserved so $\\omega$ rises and $K$ rises",
         "Do not claim energy conservation of $K$ alone during the pull.",
         ["$K$ must fall", "muscles cannot do work", "$I$ increased"]),
    ])
    _add(qs, [
        ("A rod $I=0.12\\,\\mathrm{kg\\cdot m}^2$ spins at $5.0\\,\\mathrm{rad/s}$. $K_{\\mathrm{rot}}$ is",
         "$1.5\\,\\mathrm{J}$",
         "$\\tfrac12(0.12)(25)=1.5\\,\\mathrm{J}$.",
         ["$0.60\\,\\mathrm{J}$", "$3.0\\,\\mathrm{J}$", "$0.30\\,\\mathrm{J}$"]),
        ("$L$ of that rod is",
         "$0.60\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$",
         "$L=I\\omega=0.60$.",
         ["$1.5$", "$0.024$", "$5.12$"]),
        ("A turntable $I=0.20$ at $3.0\\,\\mathrm{rad/s}$ receives a clay blob that increases $I$ to $0.30$ and they rotate together. $\\omega_f$ is",
         "$2.0\\,\\mathrm{rad/s}$",
         "$0.20(3)=0.30\\omega_f$, $\\omega_f=2.0\\,\\mathrm{rad/s}$.",
         ["$3.0\\,\\mathrm{rad/s}$", "$4.5\\,\\mathrm{rad/s}$", "$1.0\\,\\mathrm{rad/s}$"]),
        ("$K$ ratio $K_f/K_i$ for that clay drop is",
         "$2/3$",
         "$K\\propto I\\omega^2$ with $I\\omega$ fixed, so $K\\propto 1/I$, hence $0.20/0.30=2/3$.",
         ["$3/2$", "$1$", "$0$"]),
        ("Masses $4.0\\,\\mathrm{kg}$ and $6.0\\,\\mathrm{kg}$ over a light pulley: $a=$ ($g=10$)",
         "$2.0\\,\\mathrm{m/s}^2$",
         "$a=(6-4)10/10=2.0\\,\\mathrm{m/s}^2$.",
         ["$10\\,\\mathrm{m/s}^2$", "$4.0\\,\\mathrm{m/s}^2$", "$1.0\\,\\mathrm{m/s}^2$"]),
        ("If that pulley has $I/R^2=2.0\\,\\mathrm{kg}$, the new $a$ is",
         "$1.67\\,\\mathrm{m/s}^2$",
         "$a=20/(10+2)=20/12=5/3\\approx 1.67\\,\\mathrm{m/s}^2$.",
         ["$2.0\\,\\mathrm{m/s}^2$", "$2.4\\,\\mathrm{m/s}^2$", "$0$"]),
        ("A disk rolling from height $5.0\\,\\mathrm{m}$ ($g=10$) has $v=\\sqrt{4gh/3}=$",
         "$\\sqrt{200/3}\\,\\mathrm{m/s}$",
         "$4(10)(5)/3=200/3$, $v=\\sqrt{200/3}\\,\\mathrm{m/s}$.",
         ["$10\\,\\mathrm{m/s}$", "$\\sqrt{100}\\,\\mathrm{m/s}$", "$\\sqrt{50}\\,\\mathrm{m/s}$"]),
        ("Work $W=\\tau\\theta$ of $4.0\\,\\mathrm{N\\cdot m}$ through $3.0\\,\\mathrm{rad}$ equals $\\Delta K$ of",
         "$12\\,\\mathrm{J}$",
         "Net rotational work becomes $K_{\\mathrm{rot}}$.",
         ["$1.3\\,\\mathrm{J}$", "$7.0\\,\\mathrm{J}$", "$0$"]),
        ("A particle flies past a point with impact parameter (perpendicular distance) $d=0.80\\,\\mathrm{m}$ at $v=5.0\\,\\mathrm{m/s}$, $m=0.40\\,\\mathrm{kg}$. $L$ about that point is",
         "$1.6\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$",
         "$L=mvd=(0.40)(5.0)(0.80)=1.6$.",
         ["$2.0$", "$0.32$", "$10$"]),
        ("If a central force always aims at that point, $L$ about it",
         "stays constant ($\\tau=0$ because $\\phi=0$ or $180^\\circ$)",
         "Gravity on a planet about the Sun is the famous case; AP 1 uses the $\\tau=0$ idea.",
         ["grows steadily", "must be zero", "equals $mv$"]),
        ("Two disks $I$ and $2I$ spin opposite ways at the same $\\omega$ and then couple. $\\omega_f$ is",
         "$\\omega/3$ in the $2I$ disk's original sense",
         "$L=I\\omega-2I\\omega=-I\\omega=(3I)\\omega_f$, $\\omega_f=-\\omega/3$.",
         ["$0$", "$\\omega$", "$-\\omega$"]),
        ("A hanging mass $m$ unwinds a disk $I=\\tfrac12 MR^2$ with $M=2m$. Then $a=$",
         "$g/2$",
         "$mg-T=ma$, $TR=I a/R$, $T=(I/R^2)a=m a$. Then $mg=2ma$, $a=g/2$.",
         ["$g$", "$g/3$", "$2g/3$"]),
        ("System justification: “I include both hanging masses and the pulley because”",
         "then gravity and axle forces are the externals I must track; string tensions are internal",
         "Internal $T$ cancels in the system's energy story; it does not cancel in $\\tau_{\\mathrm{net}}$ on the pulley alone.",
         ["massless strings have no tension", "g disappears", "the pulley cannot rotate"]),
        ("A spinning ice-skater raises her arms slowly. If $L$ is conserved, $\\omega$ falls and $K$",
         "falls (her muscles do negative work on the rotating system as $I$ grows)",
         "Opposite of pulling in.",
         ["rises", "is unchanged", "becomes $mgh$"]),
        ("A hoop ($I=mR^2$) of mass $2.0\\,\\mathrm{kg}$ rolls without slipping at $v_{\\mathrm{cm}}=3.0\\,\\mathrm{m/s}$. Total kinetic energy is",
         "$18\\,\\mathrm{J}$",
         "For a hoop, $K_{\\mathrm{rot}}=\\tfrac12 mR^2(v/R)^2=\\tfrac12 mv^2$, so $K_{\\mathrm{tot}}=mv^2=(2.0)(9.0)=18\\,\\mathrm{J}$.",
         ["$9.0\\,\\mathrm{J}$", "$4.5\\,\\mathrm{J}$", "$27\\,\\mathrm{J}$"]),
        ("A $0.50\\,\\mathrm{kg}$ bead on a $0.40\\,\\mathrm{m}$ string moves in a horizontal circle at $5.0\\,\\mathrm{m/s}$. Angular momentum about the center is",
         "$1.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$",
         "$L=mvr=(0.50)(5.0)(0.40)=1.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
         ["$2.5\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "$0.20\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "$10\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$"]),
        ("AP Stretch: A rod hinged at one end, $I=\\tfrac13 m\\ell^2$, falls from horizontal. $\\omega$ at the vertical is",
         "$\\sqrt{3g/\\ell}$",
         "$mg(\\ell/2)=\\tfrac12 I\\omega^2=\\tfrac16 m\\ell^2\\omega^2$, so $\\omega^2=3g/\\ell$.",
         ["$\\sqrt{2g/\\ell}$", "$\\sqrt{g/\\ell}$", "$\\sqrt{6g/\\ell}$"]),
        ("AP Stretch: A bullet of mass $m$ and speed $v$ hits the free end of a hanging rod of length $\\ell$ and rotational inertia $I$ about the hinge, and sticks. Immediately after, $\\omega$ about the hinge is",
         "$m v \\ell / (I+m\\ell^2)$",
         "$L_i=mv\\ell=I_f\\omega$ with $I_f=I+m\\ell^2$.",
         ["$v/\\ell$", "$mv/I$", "$0$"]),
        ("AP Stretch: A bullet of mass $m$ and speed $v$ sticks at the end of a hanging rod of length $\\ell$ and inertia $I$ about the hinge. After the inelastic stick, the maximum swing uses",
         "$\\tfrac12 I_f\\omega^2= (m_{\\mathrm{tot}} g)(\\text{CM rise})$",
         "Energy after the inelastic hit, with $I_f=I+m\\ell^2$ and $\\omega=mv\\ell/I_f$; not the bullet's original $\\tfrac12 mv^2$.",
         ["$\\tfrac12 mv^2=mgh$ of the bullet alone", "momentum $mv=m_{\\mathrm{tot}}v_{\\mathrm{cm}}$ only, with no energy", "Bernoulli"]),
        ("AP Stretch: Why is $K$ not conserved when a skater catches a thrown ball and keeps holding it?",
         "the catch is inelastic in the rotating frame; deformation/thermal energy appears",
         "$L$ about the ice-skater's axis can still be conserved if ice torque is negligible.",
         ["$L$ failed", "mass increased $g$", "time reversed"]),
        ("AP Stretch: A pulley $I=0.050\\,\\mathrm{kg\\cdot m}^2$, $R=0.10\\,\\mathrm{m}$, masses $2.0$ and $3.0\\,\\mathrm{kg}$. $a$ is ($g=10$)",
         "$1.0\\,\\mathrm{m/s}^2$",
         "$I/R^2=5.0\\,\\mathrm{kg}$, $a=(1.0)(10)/(5+5)=10/10=1.0\\,\\mathrm{m/s}^2$.",
         ["$2.0\\,\\mathrm{m/s}^2$", "$10\\,\\mathrm{m/s}^2$", "$0.50\\,\\mathrm{m/s}^2$"]),
        ("AP Stretch: A pulley $I=0.050\\,\\mathrm{kg\\cdot m}^2$, $R=0.10\\,\\mathrm{m}$, hanging masses $2.0\\,\\mathrm{kg}$ and $3.0\\,\\mathrm{kg}$, has $a=1.0\\,\\mathrm{m/s}^2$ ($g=10$). Tension on the $3.0\\,\\mathrm{kg}$ side is",
         "$27\\,\\mathrm{N}$",
         "$3g-T_h=3a$ gives $30-T_h=3.0$, so $T_h=27\\,\\mathrm{N}$. Light side: $T_\\ell-20=2.0$, $T_\\ell=22\\,\\mathrm{N}$. Difference $5\\,\\mathrm{N}$, $\\tau=0.50\\,\\mathrm{N\\cdot m}=I\\alpha=0.050(10)$.",
         ["$30\\,\\mathrm{N}$", "$20\\,\\mathrm{N}$", "$10\\,\\mathrm{N}$"]),
        ("AP Stretch: Pulley $I=0.050\\,\\mathrm{kg\\cdot m}^2$, $R=0.10\\,\\mathrm{m}$, hanging $2.0\\,\\mathrm{kg}$ and $3.0\\,\\mathrm{kg}$, $g=10$. If you treat only the two masses as the system and set the pulley $I=0$, the predicted $a$ is",
         "too large: $2.0\\,\\mathrm{m/s}^2$ instead of the true $1.0\\,\\mathrm{m/s}^2$",
         "$a_{\\mathrm{no}\\,I}=(3-2)g/(3+2)=2.0\\,\\mathrm{m/s}^2$. With $I/R^2=5.0\\,\\mathrm{kg}$, $a=10/10=1.0\\,\\mathrm{m/s}^2$. Omitting the wheel's inertia overpredicts $a$.",
         ["too small: $0.50\\,\\mathrm{m/s}^2$ instead of $1.0$", "unchanged at $1.0\\,\\mathrm{m/s}^2$", "negative"]),
        ("AP Stretch: A turntable $I=0.40\\,\\mathrm{kg\\cdot m}^2$ at $6.0\\,\\mathrm{rad/s}$ is sped up by average $\\tau=4.0\\,\\mathrm{N\\cdot m}$ lasting $0.50\\,\\mathrm{s}$. Find $\\Delta L$, $\\omega$ after, and $\\Delta K$.",
         "$\\Delta L=2.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$, $\\omega=11\\,\\mathrm{rad/s}$, $\\Delta K=17\\,\\mathrm{J}$",
         "$\\Delta L=\\tau\\Delta t=2.0$. Then $\\omega_f=6.0+2.0/0.40=11\\,\\mathrm{rad/s}$. $K_i=7.2\\,\\mathrm{J}$, $K_f=24.2\\,\\mathrm{J}$, so $\\Delta K=17\\,\\mathrm{J}$.",
         ["$\\Delta L=0.30$ from a one-step $\\tau\\Delta t$ copy", "$\\omega=6.0\\,\\mathrm{rad/s}$ unchanged", "$\\Delta K=0$ because $L$ changed"]),
        ("AP Stretch: A free dumbbell rotating about the CM has $L=I_{\\mathrm{cm}}\\omega$. An off-center hit that does not aim through the CM",
         "changes both $v_{\\mathrm{cm}}$ and $\\omega$",
         "Net impulse changes $p$; torque about the CM changes $L_{\\mathrm{cm}}$.",
         ["only changes $v_{\\mathrm{cm}}$", "only changes $\\omega$", "cannot change $L$"]),
    ])
    return qs


def build_unit6():
    title = "AP Physics Unit 6: Energy and Momentum of Rotating Systems"
    description = (
        "Rotational kinetic energy, angular momentum, conservation of $L$, sticky rotational collisions, "
        "massive pulleys, and FRQ system justifications — still algebra-based AP Physics 1."
    )
    concepts = [
        "Rotational kinetic energy",
        "Angular momentum",
        "Conservation of L",
        "Collisions with rotation",
        "Atwood and pulleys with rotation",
        "Justifying with systems",
    ]

    c1 = concept_block(
        "1. Rotational kinetic energy",
        [
            "A spinning object stores kinetic energy even if its center of mass is nailed in place: "
            "$K_{\\mathrm{rot}}=\\tfrac12 I\\omega^2$. A disk with $I=0.50\\,\\mathrm{kg\\cdot m}^2$ at $4.0\\,\\mathrm{rad/s}$ has $K=4.0\\,\\mathrm{J}$.",
            "This is the rotational twin of $\\tfrac12 mv^2$. Double $\\omega$ and $K_{\\mathrm{rot}}$ quadruples. "
            "The $I$ already contains the “how far from the axis” information.",
            "Rolling objects have both pieces: $K=\\tfrac12 mv_{\\mathrm{cm}}^2+\\tfrac12 I\\omega^2$. With no slipping, substitute $\\omega=v/R$. "
            "A hoop then has equal split; a disk has more energy in translation than in spin.",
            "A constant torque doing work through an angle (in radians) does $W=\\tau\\theta$. If that is the net rotational work, "
            "it equals $\\Delta K_{\\mathrm{rot}}$. A $5.0\\,\\mathrm{N\\cdot m}$ torque through $2.0\\,\\mathrm{rad}$ does $10\\,\\mathrm{J}$.",
            "Gravitational potential energy still uses the CM height. A falling rod converts $mgh_{\\mathrm{cm}}$ into $\\tfrac12 I\\omega^2$ "
            "about the hinge if the hinge does no work.",
            "Forgetting $K_{\\mathrm{rot}}$ on a massive pulley makes predicted hanging-mass speeds too big. The wheel is a third "
            "energy bank beside the two masses.",
        ],
        "Conservation of $L$ problems still need $K$ when an FRQ asks whether energy was lost. You cannot discuss that "
        "without $\\tfrac12 I\\omega^2$.",
        "Write $K_{\\mathrm{trans}}+K_{\\mathrm{rot}}+U$. Substitute $\\omega=v/R$ only when there is a no-slip or no-slip-unwinding link.",
        lesson_figure(
            energy_bars_svg(ke=3, pe=2, thermal=0),
            "A rolling object at mid-hill: KE includes spin plus CM motion",
            "The KE bar is $\\tfrac12 mv^2+\\tfrac12 I\\omega^2$, not translation alone. PE is $mgh_{\\mathrm{cm}}$.",
        )
        + solved(1, "A flywheel has $I=0.50\\,\\mathrm{kg\\cdot m}^2$ and $\\omega=4.0\\,\\mathrm{rad/s}$. Find $K_{\\mathrm{rot}}$.",
                 ["$K=\\tfrac12 I\\omega^2=\\tfrac12(0.50)(16)=4.0\\,\\mathrm{J}$.",
                  "If $\\omega$ doubles to $8.0$, $K$ becomes $16\\,\\mathrm{J}$.",
                  "Units: $(\\mathrm{kg\\cdot m}^2)(\\mathrm{rad/s})^2=\\mathrm{J}$."],
                 "$4.0\\,\\mathrm{J}$", "", "Easy")
        + solved(2, "A $4.0\\,\\mathrm{kg}$ hoop rolls at $3.0\\,\\mathrm{m/s}$ without slipping. Find total $K$.",
                 ["$K=mv^2=(4.0)(9.0)=36\\,\\mathrm{J}$.",
                  "Half is translation ($18\\,\\mathrm{J}$), half rotation ($18\\,\\mathrm{J}$).",
                  "A disk at the same $v$ would have only $K=\\tfrac34 mv^2=27\\,\\mathrm{J}$."],
                 "$36\\,\\mathrm{J}$", "", "Medium")
        + solved(3, "A uniform rod of mass $m$ and length $\\ell$, hinged at one end, starts from rest horizontally. Find $\\omega$ when it is vertical. Use $I=\\tfrac13 m\\ell^2$ about the hinge and $g$.",
                 ["CM drops $\\ell/2$, so $\\Delta U=-mg\\ell/2$.",
                  "That becomes $K=\\tfrac12 I\\omega^2=\\tfrac12(\\tfrac13 m\\ell^2)\\omega^2=m\\ell^2\\omega^2/6$.",
                  "$mg\\ell/2=m\\ell^2\\omega^2/6$, so $\\omega^2=3g/\\ell$, $\\omega=\\sqrt{3g/\\ell}$.",
                  "The hinge force does no work (no motion at the point of application)."],
                 "$\\omega=\\sqrt{3g/\\ell}$", "", "Hard"),
        ("Using $\\tfrac12 mv_{\\mathrm{tip}}^2$ as the rod's entire $K$",
         "Different points of the rod have different speeds. $I$ already averages $v=r\\omega$ correctly as $\\tfrac12 I\\omega^2$."),
        ("List every spinning piece in the energy table",
         "Masses, pulley, rolling wheel. If it has $I$ and $\\omega$, it has $K_{\\mathrm{rot}}$."),
        [
            "I can compute $K_{\\mathrm{rot}}=\\tfrac12 I\\omega^2$.",
            "I can add translational and rotational $K$ for rolling objects.",
            "I can convert $mgh_{\\mathrm{cm}}$ into $\\tfrac12 I\\omega^2$ for a falling hinged rod.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Angular momentum",
        [
            "Angular momentum is the rotational twin of $p$. For a rigid body about a fixed axis, $L=I\\omega$. "
            "If $I=2.0\\,\\mathrm{kg\\cdot m}^2$ and $\\omega=3.0\\,\\mathrm{rad/s}$, then $L=6.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
            "A single particle has $L=m v r_\\perp$, where $r_\\perp$ is the perpendicular distance from the chosen point "
            "to the particle's line of motion (the lever arm of $\\vec{p}$). A $2.0\\,\\mathrm{kg}$ object at $4.0\\,\\mathrm{m/s}$ with $r_\\perp=0.50\\,\\mathrm{m}$ has $L=4.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
            "Net torque changes $L$: $\\tau_{\\mathrm{net}}=\\Delta L/\\Delta t$ in the average sense, or $\\tau_{\\mathrm{net}}\\Delta t=\\Delta L$. "
            "A $3.0\\,\\mathrm{N\\cdot m}$ torque for $2.0\\,\\mathrm{s}$ delivers an angular impulse of $6.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
            "Even a particle in straight-line motion can have nonzero $L$ about a point off to the side. The lever arm "
            "is the impact parameter. A central force aimed at that point produces zero torque, so that $L$ stays constant.",
            "Signs: pick a sense (out of the page, or counterclockwise). $L$ and $\\omega$ share that sense. "
            "Opposite rotation means opposite $L$.",
            "Do not mix $L=I\\omega$ for an extended rigid body with $L=mvr$ for a particle without saying the axis. "
            "The blob-on-a-disk collision uses $m v R$ of the blob about the disk's center, then $I\\omega$ afterward.",
        ],
        "Conservation of $L$ is this quantity staying constant. If $L$ is a foggy $I\\omega$, the skater and turntable "
        "stories become memorized trivia.",
        "Name the axis. For a rigid body use $I\\omega$. For a free particle use $mvd$ with $d$ the perpendicular distance to the line of $\\vec{v}$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", [(0, 2), (4, 2)])],
                points=[(0, 0, "axis"), (0, 2, "L")],
                dashes=[("h", 2, "L constant")],
                xlim=(-0.4, 5), ylim=(-0.5, 4), xlab="t (s)", ylab="L", w=300, h=220,
            ),
            "Angular momentum versus time when $\\tau_{\\mathrm{net}}=0$",
            "Horizontal $L$-$t$ means conserved $L$. A jump in $L$ would require an angular impulse.",
        )
        + solved(4, "A wheel has $I=2.0\\,\\mathrm{kg\\cdot m}^2$ and $\\omega=3.0\\,\\mathrm{rad/s}$. Find $L$.",
                 ["$L=I\\omega=6.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
                  "If a brake applies $\\tau=-2.0\\,\\mathrm{N\\cdot m}$ for $1.0\\,\\mathrm{s}$, $\\Delta L=-2.0$.",
                  "Then $L_f=4.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$."],
                 "$6.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "", "Easy")
        + solved(5, "A $0.40\\,\\mathrm{kg}$ particle moves at $5.0\\,\\mathrm{m/s}$ along a line whose perpendicular distance from point P is $0.80\\,\\mathrm{m}$. Find $L$ about P.",
                 ["$L=m v d=(0.40)(5.0)(0.80)=1.6\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
                  "If the line went through P, $d=0$ and $L=0$.",
                  "A force always aimed at P would not change this $L$."],
                 "$1.6\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "", "Medium")
        + solved(6, "A $2.0\\,\\mathrm{kg}$ clay flies at $5.0\\,\\mathrm{m/s}$ perpendicular to a radius and sticks at $R=0.40\\,\\mathrm{m}$ on a free disk. Find the clay's $L$ about the disk center just before impact.",
                 ["Treat the clay as a particle: $L=m v R$ when $\\vec{v}\\perp\\vec{r}$.",
                  "$L=(2.0)(5.0)(0.40)=4.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
                  "After sticking, that $L$ becomes $(I_{\\mathrm{disk}}+mR^2)\\omega$.",
                  "The disk's own $L_i$ is added if it was already spinning."],
                 "$4.0\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "", "Hard"),
        ("Using $L=mv$ with no lever arm",
         "Linear momentum $p=mv$ is not $L$. You must multiply by a perpendicular distance to an axis."),
        ("Write the axis in the sentence “$L$ about …”",
         "About the axle, about the hinge, about the CM. Different axes, different $L$ numbers."),
        [
            "I can compute $L=I\\omega$ for a rigid body.",
            "I can compute $L=mvd$ for a particle about a point.",
            "I can use $\\tau\\Delta t=\\Delta L$ as angular impulse.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Conservation of $L$",
        [
            "If the net external torque on a system about an axis is zero (or negligible during a short event), "
            "that system's angular momentum about the axis is conserved: $L_i=L_f$.",
            "The ice-skater: pulling arms in decreases $I$. With $L=I\\omega$ fixed, $\\omega$ increases. "
            "$I_i=4.0$ at $2.0\\,\\mathrm{rad/s}$ going to $I_f=2.0$ gives $\\omega_f=4.0\\,\\mathrm{rad/s}$.",
            "Kinetic energy of the skater increases. Muscles do positive work while pulling mass toward the axis. "
            "$L$ conservation is not $K$ conservation.",
            "A child stepping onto a merry-go-round: the axle can exert a force at the axis ($\\tau=0$). "
            "Linear momentum of the child is not conserved (the axle pushes), but $L$ of child+wheel about the axle is.",
            "Two disks dropped together: $I_1\\omega_1+I_2\\omega_2=(I_1+I_2)\\omega_f$ if they then rotate as one. "
            "$K$ falls, as in a sticky linear collision.",
            "Justify in a sentence: name the system, name the axis, say why $\\tau_{\\mathrm{ext}}\\approx 0$ (frictionless ice, "
            "impulse at a hinge, internal explosions).",
        ],
        "Almost every Unit 6 FRQ is “is $L$ conserved? is $K$ conserved? is $p$ conserved?” with different answers. "
        "The next screens train the $L$ half of that triad.",
        "Write $I_i\\omega_i=I_f\\omega_f$ or $mvr+I\\omega$ matching. Then, separately, compare $K_i$ and $K_f$.",
        lesson_figure(
            energy_bars_svg(ke=4, pe=0, thermal=0),
            "Skater after pulling in: taller KE bar, same $L$",
            "$L$ is unchanged; $K_{\\mathrm{rot}}$ grew because the skater did work. Thermal bar stays empty on ideal ice.",
        )
        + solved(7, "A skater has $I=4.0\\,\\mathrm{kg\\cdot m}^2$ at $\\omega=2.0\\,\\mathrm{rad/s}$, then $I=2.0\\,\\mathrm{kg\\cdot m}^2$. Find $\\omega_f$.",
                 ["$L_i=8.0=L_f=2.0\\,\\omega_f$.",
                  "$\\omega_f=4.0\\,\\mathrm{rad/s}$.",
                  "$K_i=\\tfrac12(4)(4)=8.0\\,\\mathrm{J}$, $K_f=\\tfrac12(2)(16)=16\\,\\mathrm{J}$."],
                 "$4.0\\,\\mathrm{rad/s}$ (and $K$ doubled)", "", "Easy")
        + solved(8, "A turntable $I=0.20\\,\\mathrm{kg\\cdot m}^2$ at $3.0\\,\\mathrm{rad/s}$ receives clay; $I$ becomes $0.30$. They rotate together. Find $\\omega_f$ and $K_f/K_i$.",
                 ["$0.20(3.0)=0.30\\omega_f$, so $\\omega_f=2.0\\,\\mathrm{rad/s}$.",
                  "$K\\propto I\\omega^2$ with $I\\omega$ fixed means $K\\propto 1/I$.",
                  "$K_f/K_i=0.20/0.30=2/3$."],
                 "$2.0\\,\\mathrm{rad/s}$, $K$ ratio $2/3$", "", "Medium")
        + solved(9, "Disks $I$ and $2I$ spin opposite ways at the same $\\omega$ and then lock. Find $\\omega_f$.",
                 ["Take the $I$ disk's sense as positive: $L_i=I\\omega-2I\\omega=-I\\omega$.",
                  "$I_f=3I$, so $3I\\omega_f=-I\\omega$, $\\omega_f=-\\omega/3$.",
                  "They rotate slowly in the heavier disk's original sense.",
                  "$K$ drops a lot: this is rotationally inelastic."],
                 "$\\omega_f=-\\omega/3$", "", "Hard"),
        ("Claiming $K$ is conserved because $L$ is conserved",
         "Those are different conditions. Sticky disks conserve $L$ and dump $K$. A skater pulling in conserves $L$ and raises $K$ via muscle work."),
        ("Write a justification sentence before the algebra",
         "“System = skater+arms. Ice torque negligible. $L$ about the vertical axis is conserved.” Graders look for that sentence."),
        [
            "I can state the $\\tau_{\\mathrm{net}}=0$ condition for conserving $L$.",
            "I can solve $I_i\\omega_i=I_f\\omega_f$ for a skater or turntable.",
            "I can compare $K$ before and after when $L$ is conserved but $I$ changes.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Collisions with rotation",
        [
            "A particle hitting a rod or disk is a collision that may conserve $L$ about a clever axis even when "
            "linear $p$ of the extended object is not conserved (a hinge or axle can impulse).",
            "Just before: $L$ of the projectile about the axis is $m v d$ (often $m v \\ell$ at the end of a rod). "
            "Just after a stick: $L=(I_{\\mathrm{rod}}+m d^2)\\omega$.",
            "Example numbers: $0.20\\,\\mathrm{kg}$ at $5.0\\,\\mathrm{m/s}$ sticks at $R=0.40\\,\\mathrm{m}$ on a disk with $I=0.080\\,\\mathrm{kg\\cdot m}^2$. "
            "$L_i=0.40$, $I_f=0.112$, $\\omega\\approx 3.57\\,\\mathrm{rad/s}$. $K$ falls.",
            "If the projectile bounces, you need a second rule (elastic $K$, or a given rebound speed). "
            "$L$ alone is one equation.",
            "After a sticky hit on a hanging rod, a second phase begins: the rod swings up, and now you use energy "
            "with the leftover $\\tfrac12 I_f\\omega^2$ converting into CM gravitational energy. Do not feed the bullet's original $K$ into that swing.",
            "This is the ballistic pendulum's rotational cousin. Separate the timeline: (1) $L$ during the hit, (2) energy during the swing.",
        ],
        "Hinged-rod FRQs are among the hardest AP Physics 1 items. The split — $L$ then $E$ — is the whole method.",
        "Axis at the hinge. $L_i$ of the bullet. $I_f$ of rod+bullet. Then, later, $\\tfrac12 I_f\\omega^2=mgh_{\\mathrm{cm}}$.",
        lesson_figure(
            _hit_rod_svg(),
            "A particle hits a hinged rod at lever arm $d$",
            "About the hinge, $L=mvd$ just before the stick. After, $L=I_f\\omega$ with $I_f=I_{\\mathrm{rod}}+md^2$.",
        )
        + solved(10, "A $0.20\\,\\mathrm{kg}$ blob at $5.0\\,\\mathrm{m/s}$ sticks at $R=0.40\\,\\mathrm{m}$ on a resting disk $I=0.080\\,\\mathrm{kg\\cdot m}^2$. Find $L_i$ about the center.",
                 ["$v$ is perpendicular to the radius.",
                  "$L=m v R=(0.20)(5.0)(0.40)=0.40\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$.",
                  "Disk $L_i=0$."],
                 "$0.40\\,\\mathrm{kg\\cdot m}^2/\\mathrm{s}$", "", "Easy")
        + solved(11, "Continue: find $\\omega$ after they stick.",
                 ["$I_f=0.080+mR^2=0.080+0.032=0.112\\,\\mathrm{kg\\cdot m}^2$.",
                  "$0.40=0.112\\,\\omega$.",
                  "$\\omega=0.40/0.112\\approx 3.57\\,\\mathrm{rad/s}$."],
                 "$0.40/0.112\\,\\mathrm{rad/s}\\approx 3.57\\,\\mathrm{rad/s}$", "", "Medium")
        + solved(12, "A bullet of mass $m$ speed $v$ sticks at the end of a hanging rod of length $\\ell$ and inertia $I$ about the hinge. Find $\\omega$ just after, then the energy available to swing.",
                 ["$L_i=m v \\ell=(I+m\\ell^2)\\omega$, so $\\omega=m v \\ell/(I+m\\ell^2)$.",
                  "$K_{\\mathrm{after}}=\\tfrac12(I+m\\ell^2)\\omega^2$, which is less than $\\tfrac12 mv^2$.",
                  "That $K_{\\mathrm{after}}$ equals $M g h_{\\mathrm{cm}}$ at the top of the swing if it comes to rest there.",
                  "The hinge impulse has zero torque, so $L$ about the hinge is the conserved quantity during the hit."],
                 "$\\omega=mv\\ell/(I+m\\ell^2)$; swing uses leftover $K$, not $\\tfrac12 mv^2$", "", "Hard"),
        ("Using $\\tfrac12 mv^2=mgh$ of the bullet as the swing energy",
         "The stick is inelastic. Only the $K$ remaining after $L$ conservation climbs the arc."),
        ("Split the story at the word “immediately after”",
         "Before that instant: $L$. After that instant: energy, with $\\omega$ from the first part as the new initial condition."),
        [
            "I can compute a projectile's $L$ about a hinge or axle.",
            "I can find $\\omega$ after a sticky rotational collision.",
            "I can refuse to conserve $K$ during the stick, then use leftover $K$ for a later swing.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Atwood machines and pulleys with rotation",
        [
            "When a pulley has rotational inertia $I$, it is not a massless redirect. The two tensions differ, "
            "and some of the falling mass's lost $U_g$ becomes $\\tfrac12 I\\omega^2$.",
            "Linear link: $a=\\alpha R$ if the string does not slip. Force equations: $m_2 g-T_2=m_2 a$, $T_1-m_1 g=m_1 a$ "
            "(if $m_2$ descends). Pulley: $(T_2-T_1)R=I\\alpha=I a/R$.",
            "Combining those gives $a=(m_2-m_1)g / (m_1+m_2+I/R^2)$. The extra $I/R^2$ acts like more mass in the denominator. "
            "If $I=0$, you recover the Unit 2 Atwood formula.",
            "Example: $m$ and $2m$ with $I=mR^2$ yields $a=g/4$ instead of $g/3$. The pulley slowed the system.",
            "Energy check: $m_2 g h-m_1 g h=\\tfrac12 m_1 v^2+\\tfrac12 m_2 v^2+\\tfrac12 I(v/R)^2$. "
            "If your speeds beat this audit, you omitted the wheel.",
            "A single hanging mass unwinding a yo-yo or disk is the same pair: $mg-T=ma$ and $TR=I a/R$. "
            "For $I=\\tfrac12 M R^2$ and $M=2m$, $a=g/2$.",
        ],
        "This is the last heavy dynamics mash-up in AP Physics 1: two translations plus one rotation. "
        "System energy is the fastest check.",
        "Write three equations ($m_1$, $m_2$, pulley) plus $a=\\alpha R$. Or use the combined denominator $m_1+m_2+I/R^2$.",
        lesson_figure(
            _pulley_svg(),
            "Massive pulley with two hanging masses",
            "Unequal $T$, $I\\alpha$ in the middle, $a=\\alpha R$ if the string does not slip.",
        )
        + solved(13, "Masses $m$ and $2m$ hang on a light pulley. Find $a$.",
                 ["$I=0$, $a=(2m-m)g/(3m)=g/3$.",
                  "This is the Unit 2 result.",
                  "Tensions are equal when $I=0$: $T=2 m_1 m_2 g/(m_1+m_2)=4mg/3$."],
                 "$a=g/3$", "", "Easy")
        + solved(14, "The same masses, now $I=mR^2$. Find $a$.",
                 ["$a=(2m-m)g/(3m+I/R^2)=(mg)/(3m+m)=g/4$.",
                  "The extra $m$ in the denominator is $I/R^2$.",
                  "Slower than $g/3$, as expected."],
                 "$a=g/4$", "", "Medium")
        + solved(15, "Pulley $I=0.050\\,\\mathrm{kg\\cdot m}^2$, $R=0.10\\,\\mathrm{m}$, masses $2.0\\,\\mathrm{kg}$ and $3.0\\,\\mathrm{kg}$. Find $a$ and the larger tension ($g=10$).",
                 ["$I/R^2=5.0\\,\\mathrm{kg}$.",
                  "$a=(1.0)(10)/(2+3+5)=10/10=1.0\\,\\mathrm{m/s}^2$.",
                  "Heavier mass: $30-T_h=3(1)$, so $T_h=27\\,\\mathrm{N}$.",
                  "Lighter: $T_\\ell-20=2(1)$, $T_\\ell=22\\,\\mathrm{N}$. Check: $(27-22)(0.10)=0.50=I\\alpha=0.050(10)$."],
                 "$a=1.0\\,\\mathrm{m/s}^2$, $T_h=27\\,\\mathrm{N}$", "", "Hard"),
        ("Setting both tensions equal on a massive pulley",
         "Equal $T$ would mean zero net torque and $\\alpha=0$. If the pulley is spinning up, the tensions cannot match."),
        ("Add $I/R^2$ in the denominator beside the two masses",
         "That one extra term is the entire massive-pulley correction to $a$."),
        [
            "I can write $a=(m_2-m_1)g/(m_1+m_2+I/R^2)$.",
            "I can explain why pulley $I$ reduces $a$.",
            "I can solve for two different tensions and check $\\tau=I\\alpha$.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Justifying with systems",
        [
            "AP Physics 1 scores points for the sentence that names a system and a conservation law's condition, "
            "not only for the algebra. This concept is that sentence, practiced on rotation.",
            "Linear momentum: net external impulse $\\approx 0$. Angular momentum: net external torque about a named "
            "axis $\\approx 0$. Mechanical energy: no (or accounted) nonconservative work.",
            "A hinge can exert a large force (so $p$ of the rod is not conserved) with zero torque about the hinge "
            "(so $L$ about the hinge is conserved). That contrast is an FRQ favorite.",
            "A frictionless axle does the same for a turntable. Ice under a skater makes $\\tau_{\\mathrm{ext}}\\approx 0$ "
            "about the vertical axis, while the skater's muscles still do work on the arms (so $K$ can change).",
            "If you include both hanging masses and the pulley as one system, string tensions are internal. "
            "Gravity and the axle force are external. Energy of that system still tracks $U_g$ and all three $K$ stores.",
            "Write before you compute: “System = bullet + rod. Axis = hinge. Hinge impulse has no torque, so $L$ is "
            "conserved during the brief hit. The hit is inelastic, so $K$ is not.” That paragraph is the lesson.",
        ],
        "Every stretch item in this unit is easier if the justification is written first. The algebra is then just "
        "the symbol version of the sentence.",
        "Three checkboxes: $p$? $L$? $E_{\\mathrm{mech}}$? Each yes needs a condition. Mixed yes/no is normal.",
        lesson_figure(
            _hinged_rod_fbd(),
            "Forces on a hinged rod: hinge force may be large",
            "The hinge force changes $p$ but drops out of $\\tau$ and of $L$ about the hinge. $F_g$ acts at the center. System choice plus axis choice is the justification.",
        )
        + solved(16, "A bullet hits a hinged rod and sticks. Which of $p$, $L$ (about hinge), and $K$ are conserved during the hit? Justify.",
                 ["$p$ of bullet+rod: not conserved; the hinge impulses.",
                  "$L$ about the hinge: conserved; hinge force has zero lever arm.",
                  "$K$: not conserved; the stick is inelastic (thermal/deformation)."],
                 "$L$ yes; $p$ no; $K$ no", "", "Easy")
        + solved(17, "A skater pulls her arms in on frictionless ice. Same three questions.",
                 ["$p$: horizontal $p$ of skater+Earth is a larger story; for the skater alone, ice can push, but often $p_{\\mathrm{cm}}$ stays ~0 by symmetry.",
                  "$L$ about the vertical CM axis: conserved; ice torque negligible.",
                  "$K$: not conserved as a closed mechanical number — muscles do positive work, $K$ rises."],
                 "$L$ conserved, $K$ increases due to muscle work", "", "Medium")
        + solved(18, "Massive-pulley Atwood. You want $a$. Contrast treating “masses only” versus “masses + pulley.”",
                 ["Masses only: tensions are external, you must keep both $T$s; easy to forget $I$.",
                  "Masses + pulley energy: tensions internal, $U_g$ feeds three $K$ terms including $\\tfrac12 I\\omega^2$.",
                  "Masses only with $I=0$ overpredicts $a$ (example: $2.0$ vs $1.0\\,\\mathrm{m/s}^2$ when $I/R^2$ equals the mass sum).",
                  "The better system is the one whose neglected internals match the law you are using."],
                 "include the pulley in energy; omitting $I$ makes $a$ too large", "", "Hard"),
        ("Writing “momentum is conserved” with no system and no axis",
         "Graders cannot award the justification point. Name objects, name the axis, name the neglected external."),
        ("Fill the $p$ / $L$ / $K$ triad in three short lines before calculating",
         "Yes/no plus one reason each. Then the algebra cannot wander into the wrong conservation law."),
        [
            "I can justify $L$ conservation with system, axis, and $\\tau_{\\mathrm{ext}}\\approx 0$.",
            "I can explain how a hinge can break $p$ conservation while keeping $L$.",
            "I can choose a system that makes the intended internals cancel.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Oscillations
# ===========================================================================

def _u7_questions():
    qs = []
    _add(qs, [
        ("Simple harmonic motion (SHM) happens when the restoring force is proportional to displacement from equilibrium and opposite it: $F=-kx$ for a spring. If $k=50\\,\\mathrm{N/m}$ and $x=+0.10\\,\\mathrm{m}$, $F$ is",
         "$5.0\\,\\mathrm{N}$ toward equilibrium",
         "$|F|=kx=5.0\\,\\mathrm{N}$, direction opposite the stretch.",
         ["$5.0\\,\\mathrm{N}$ farther from equilibrium", "$500\\,\\mathrm{N}$", "$0.002\\,\\mathrm{N}$"]),
        ("Equilibrium for a horizontal spring is where",
         "the spring is unstretched (net force zero)",
         "That is $x=0$ in $F=-kx$. A hanging spring's equilibrium already includes $mg$.",
         ["the amplitude", "the wall", "maximum speed"]),
        ("Acceleration in SHM is largest in magnitude at",
         "maximum $|x|$ (the endpoints)",
         "$a=F/m=-kx/m$, so $|a|$ tracks $|x|$.",
         ["equilibrium", "half amplitude always", "nowhere; $a=0$ in SHM"]),
        ("Velocity in SHM is largest at",
         "equilibrium ($x=0$)",
         "All energy is kinetic there. Endpoints have $v=0$.",
         ["the endpoints", "everywhere the same", "only at $t=0$ by definition"]),
        ("A mass on a spring is in SHM only if we can treat $F$ as $-kx$ (Hooke's law). A force $-kx^3$ would",
         "not be SHM (restoring, but not linear in $x$)",
         "SHM is the special linear restoring case. Period formulas below assume that.",
         ["still have the same $T=2\\pi\\sqrt{m/k}$", "stop oscillating", "have $a=0$"]),
    ])
    _add(qs, [
        ("Period of a mass-spring is $T=2\\pi\\sqrt{m/k}$, independent of amplitude. For $m=4.0\\,\\mathrm{kg}$ and $k=16\\,\\mathrm{N/m}$, $T$ is",
         "$\\pi\\,\\mathrm{s}$",
         "$T=2\\pi\\sqrt{4/16}=2\\pi(1/2)=\\pi\\,\\mathrm{s}$.",
         ["$2\\pi\\,\\mathrm{s}$", "$\\pi/2\\,\\mathrm{s}$", "$4\\,\\mathrm{s}$"]),
        ("Frequency is $f=1/T$. For that oscillator, $f$ is",
         "$1/\\pi\\,\\mathrm{Hz}$",
         "$f=1/\\pi\\,\\mathrm{Hz}$. Angular frequency $2\\pi f=2\\,\\mathrm{rad/s}=\\sqrt{k/m}$.",
         ["$\\pi\\,\\mathrm{Hz}$", "$2\\,\\mathrm{Hz}$", "$16\\,\\mathrm{Hz}$"]),
        ("Doubling $m$ at fixed $k$ multiplies $T$ by",
         "$\\sqrt{2}$",
         "$T\\propto\\sqrt{m}$. Double $k$ instead and $T$ is divided by $\\sqrt{2}$.",
         ["$2$", "$4$", "$1/2$"]),
        ("Amplitude does not appear in $T=2\\pi\\sqrt{m/k}$. If you pull a mass twice as far (still SHM), the period",
         "stays the same",
         "Larger $A$ means larger typical speeds, which exactly compensates the longer path.",
         ["doubles", "halves", "becomes zero"]),
        ("A hanging mass on a vertical spring uses the same $T=2\\pi\\sqrt{m/k}$ measured about the new hanging equilibrium. Gravity",
         "shifts the zero of $x$ but does not change $T$ in the ideal model",
         "The extra $mg$ is balanced by a constant stretch $mg/k$. Oscillation is around that point.",
         ["adds $2\\pi\\sqrt{L/g}$", "destroys SHM", "makes $T$ proportional to $g$"]),
    ])
    _add(qs, [
        ("A simple pendulum's small-angle period is $T=2\\pi\\sqrt{L/g}$. For $L=10\\,\\mathrm{m}$ and $g=10\\,\\mathrm{m/s}^2$, $T$ is",
         "$2\\pi\\,\\mathrm{s}$",
         "$T=2\\pi\\sqrt{1}=2\\pi\\,\\mathrm{s}$.",
         ["$\\pi\\,\\mathrm{s}$", "$10\\,\\mathrm{s}$", "$2\\,\\mathrm{s}$"]),
        ("For $L=2.5\\,\\mathrm{m}$ and $g=10$, $T$ is",
         "$\\pi\\,\\mathrm{s}$",
         "$T=2\\pi\\sqrt{0.25}=2\\pi(0.50)=\\pi\\,\\mathrm{s}$.",
         ["$2\\pi\\,\\mathrm{s}$", "$5.0\\,\\mathrm{s}$", "$0.50\\,\\mathrm{s}$"]),
        ("Pendulum period does not depend on",
         "mass (or small amplitude, in the standard model)",
         "$m$ cancels. A heavier bob ticks with the same $T$.",
         ["length", "$g$", "the square root of $L$"]),
        ("If $g$ were smaller (high mountain), a pendulum clock would",
         "run slow ($T$ larger)",
         "$T\\propto 1/\\sqrt{g}$.",
         ["run fast", "be unchanged", "stop"]),
        ("The small-angle model uses a restoring component $mg\\sin\\theta\\approx mg\\theta$ with $\\theta$ in radians. Large swings",
         "are not perfect SHM; $T$ grows slightly",
         "AP 1 mostly stays in the small-angle formula.",
         ["have $T=0$", "depend on mass strongly", "have $a$ independent of $\\theta$"]),
    ])
    _add(qs, [
        ("Total mechanical energy in ideal SHM is $E=\\tfrac12 kA^2$ for a spring. If $k=50\\,\\mathrm{N/m}$ and $A=0.20\\,\\mathrm{m}$, $E$ is",
         "$1.0\\,\\mathrm{J}$",
         "$E=\\tfrac12(50)(0.04)=1.0\\,\\mathrm{J}$.",
         ["$10\\,\\mathrm{J}$", "$2.0\\,\\mathrm{J}$", "$0.20\\,\\mathrm{J}$"]),
        ("At an endpoint, that $1.0\\,\\mathrm{J}$ is all",
         "spring potential energy",
         "$K=0$, $U=\\tfrac12 kA^2$.",
         ["kinetic", "gravitational only", "thermal"]),
        ("At equilibrium, that $1.0\\,\\mathrm{J}$ is all",
         "kinetic energy",
         "$U_s=0$ (about hanging/horizontal equilibrium), $K=E$. $v_{\\max}=A\\sqrt{k/m}$.",
         ["potential", "zero", "heat"]),
        ("A $4.0\\,\\mathrm{kg}$ mass, $k=16\\,\\mathrm{N/m}$, $A=0.50\\,\\mathrm{m}$. $v_{\\max}$ is",
         "$1.0\\,\\mathrm{m/s}$",
         "$v_{\\max}=A\\sqrt{k/m}=0.50\\sqrt{4}=1.0\\,\\mathrm{m/s}$.",
         ["$2.0\\,\\mathrm{m/s}$", "$0.50\\,\\mathrm{m/s}$", "$4.0\\,\\mathrm{m/s}$"]),
        ("Energy bars in SHM slosh between $K$ and $U$ at frequency",
         "$2f$ (two energy swaps per oscillation cycle)",
         "Each pass through equilibrium is a $K$ peak. There are two per period.",
         ["$f/2$", "never", "only once ever"]),
    ])
    _add(qs, [
        ("The $x$-$t$ graph of SHM is a cosine or sine curve. If $x=A\\cos(2\\pi t/T)$ and $T=2.0\\,\\mathrm{s}$, $A=0.10\\,\\mathrm{m}$, then $x(0)$ is",
         "$0.10\\,\\mathrm{m}$ (released from rest at $+A$)",
         "$\\cos 0=1$. Starting at $+A$ with $v=0$ is the cosine story.",
         ["$0$", "$-0.10\\,\\mathrm{m}$", "$0.20\\,\\mathrm{m}$"]),
        ("The $v$-$t$ graph is a shifted sinusoid, zero at the $x$ peaks. Slope of $x$-$t$ is",
         "velocity",
         "Same as Unit 1. Steepest $x$-$t$ at equilibrium.",
         ["force", "period", "mass"]),
        ("The $a$-$t$ graph is opposite in sign to $x$-$t$ (because $a=-kx/m$). When $x$ is most positive, $a$ is",
         "most negative",
         "Restoring. The $a$ graph looks like an upside-down $x$ graph.",
         ["most positive too", "zero", "infinite"]),
        ("One full SHM cycle on $x$-$t$ is from peak to next same-direction peak. That time is",
         "$T$",
         "Count the period off the graph as the repeat time.",
         ["$T/4$ always", "$2T$", "the amplitude"]),
        ("If two SHM $x$-$t$ graphs have the same $T$ but different $A$, they are",
         "the same frequency with different heights",
         "Period formula did not use $A$.",
         ["different frequencies", "not SHM", "phase-locked to $a=g$"]),
    ])
    _add(qs, [
        ("Damping is a resistive force (often drag or internal friction) that removes mechanical energy. Light damping makes the $x$-$t$ envelope",
         "slowly shrink while the oscillation continues",
         "Amplitude falls over many cycles. Frequency stays close to the undamped value.",
         ["grow forever", "become a straight $x=vt$ line", "stop in one half-period always"]),
        ("The energy bars of a damped oscillator show $K+U$ falling while",
         "thermal energy rises",
         "Mechanical energy is not conserved; total energy of oscillator+surroundings still accounts.",
         ["$K+U$ rising", "mass decreasing", "$g$ changing"]),
        ("Driving an oscillator at its natural frequency (resonance) can",
         "build large amplitude when damping is small",
         "Qualitative AP 1: push in step with the motion.",
         ["always destroy the spring instantly", "force $T=0$", "make $k$ negative"]),
        ("Overdamped motion (very strong resistance) returns to equilibrium",
         "without oscillating (a slow creep)",
         "The mass never crosses equilibrium, or barely does, depending on the textbook wording — AP 1 wants “no oscillation” for heavy damping.",
         ["faster than light damping with many wiggles", "at $T=2\\pi\\sqrt{m/k}$ still", "with growing $A$"]),
        ("A pendulum in air eventually stops because",
         "drag and pivot friction drain $E_{\\mathrm{mech}}$",
         "Ideal $T=2\\pi\\sqrt{L/g}$ ignored that. Real clocks need an escapement (a drive) to replace the lost energy.",
         ["$g$ shuts off", "mass increases", "$L$ becomes zero"]),
    ])
    _add(qs, [
        ("A $1.0\\,\\mathrm{kg}$ mass on $k=100\\,\\mathrm{N/m}$ has $T=$",
         "$\\pi/5\\,\\mathrm{s}$",
         "$T=2\\pi\\sqrt{0.01}=2\\pi(0.10)=\\pi/5\\,\\mathrm{s}$.",
         ["$2\\pi\\,\\mathrm{s}$", "$10\\,\\mathrm{s}$", "$\\pi\\,\\mathrm{s}$"]),
        ("That oscillator's $f$ is",
         "$5/\\pi\\,\\mathrm{Hz}$",
         "$f=1/T=5/\\pi\\,\\mathrm{Hz}\\approx 1.59\\,\\mathrm{Hz}$.",
         ["$5\\,\\mathrm{Hz}$", "$\\pi/5\\,\\mathrm{Hz}$", "$100\\,\\mathrm{Hz}$"]),
        ("Pendulum $L=0.40\\,\\mathrm{m}$, $g=10$. $T=$",
         "$0.40\\pi\\,\\mathrm{s}$",
         "$T=2\\pi\\sqrt{0.04}=2\\pi(0.20)=0.40\\pi\\,\\mathrm{s}$.",
         ["$2\\pi\\,\\mathrm{s}$", "$0.40\\,\\mathrm{s}$", "$4.0\\,\\mathrm{s}$"]),
        ("$E=\\tfrac12 kA^2=8.0\\,\\mathrm{J}$ with $k=400\\,\\mathrm{N/m}$ means $A=$",
         "$0.20\\,\\mathrm{m}$",
         "$8=200 A^2$, $A^2=0.04$, $A=0.20\\,\\mathrm{m}$.",
         ["$0.040\\,\\mathrm{m}$", "$4.0\\,\\mathrm{m}$", "$0.02\\,\\mathrm{m}$"]),
        ("At $x=A/2$ on a horizontal spring, $U_s/E$ is",
         "$1/4$",
         "$U=\\tfrac12 k (A/2)^2=E/4$. Then $K=3E/4$.",
         ["$1/2$", "$1$", "$0$"]),
        ("$v_{\\max}$ for $A=0.20\\,\\mathrm{m}$, $T=\\pi\\,\\mathrm{s}$ (so $\\sqrt{k/m}=2\\,\\mathrm{rad/s}$) is",
         "$0.40\\,\\mathrm{m/s}$",
         "$v_{\\max}=A\\sqrt{k/m}=0.20\\times 2=0.40\\,\\mathrm{m/s}$.",
         ["$0.20\\,\\mathrm{m/s}$", "$2.0\\,\\mathrm{m/s}$", "$\\pi\\,\\mathrm{m/s}$"]),
        ("A graph of $x(t)$ that repeats every $4.0\\,\\mathrm{s}$ has $f=$",
         "$0.25\\,\\mathrm{Hz}$",
         "$f=1/4=0.25\\,\\mathrm{Hz}$.",
         ["$4.0\\,\\mathrm{Hz}$", "$2.0\\,\\mathrm{Hz}$", "$0.40\\,\\mathrm{Hz}$"]),
        ("If $x$-$t$ is a cosine starting at $+A$, $a$-$t$ at $t=0$ is",
         "most negative (maximum restoring acceleration)",
         "$x$ max means $a$ min (most negative).",
         ["zero", "most positive", "undefined"]),
        ("Two springs $k$ in parallel (both stretched the same $x$) act like",
         "$k_{\\mathrm{eff}}=2k$, so $T$ is smaller by $\\sqrt{2}$",
         "Forces add. Stiffer, shorter period.",
         ["$k/2$", "$k$", "$0$"]),
        ("Two identical springs in series act like",
         "$k_{\\mathrm{eff}}=k/2$, longer $T$ by $\\sqrt{2}$",
         "Each takes half the stretch. Softer pair.",
         ["$2k$", "$k$", "$4k$"]),
        ("A cart SHM on a horizontal air track with $A=0.30\\,\\mathrm{m}$ has $x=0$ at $t=T/4$ if it started at $+A$. Its speed then is",
         "$v_{\\max}$",
         "Equilibrium crossing.",
         ["$0$", "$v_{\\max}/2$", "$gT$"]),
        ("Changing amplitude from $5^\\circ$ to $10^\\circ$ on a small-angle pendulum (still small) changes $T$ by about",
         "zero in the SHM model",
         "Same as the spring: $T$ independent of $A$.",
         ["a factor of $2$", "a factor of $4$", "it stops being a pendulum"]),
        ("Light damping: after many periods the motion is still roughly sinusoidal but",
         "with a decreasing amplitude envelope",
         "That is the qualitative $x$-$t$ picture AP 1 wants.",
         ["with increasing $A$", "with $T=0$", "as uniform circular motion in $x$ only"]),
        ("Resonance disaster (qualitative) happens when",
         "a periodic drive matches the natural period and damping is too small to bleed energy fast enough",
         "Amplitude grows. Soldiers breaking step on bridges is the folklore version.",
         ["$k=0$", "$m=0$", "damping is infinite"]),
        ("A $0.80\\,\\mathrm{kg}$ cart on a $320\\,\\mathrm{N/m}$ spring has oscillation period",
         "$\\pi/10\\,\\mathrm{s}$",
         "$T=2\\pi\\sqrt{m/k}=2\\pi\\sqrt{0.80/320}=2\\pi\\sqrt{0.0025}=2\\pi(0.050)=\\pi/10\\,\\mathrm{s}$.",
         ["$2\\pi\\,\\mathrm{s}$", "$0.80\\,\\mathrm{s}$", "$\\pi\\,\\mathrm{s}$"]),
        ("A simple pendulum of length $2.5\\,\\mathrm{m}$ on Earth ($g=10$) has period",
         "$\\pi\\,\\mathrm{s}$",
         "$T=2\\pi\\sqrt{L/g}=2\\pi\\sqrt{0.25}=\\pi\\,\\mathrm{s}$.",
         ["$2.5\\,\\mathrm{s}$", "$2\\pi\\,\\mathrm{s}$", "$0.50\\,\\mathrm{s}$"]),
        ("AP Stretch: A hanging $m$ stretches a spring by $0.40\\,\\mathrm{m}$ at the new equilibrium ($g=10$). $k$ is",
         "$25m\\,\\mathrm{N/m}$ if $m$ is in kg — specifically $k=mg/0.40=25m$",
         "$mg=k\\delta$, $k=m(10)/0.40=25m$. Then $T=2\\pi\\sqrt{m/k}=2\\pi\\sqrt{1/25}=2\\pi/5\\,\\mathrm{s}$.",
         ["$k=0.40 m$", "$k=mg$", "$k=0$"]),
        ("AP Stretch: A hanging mass $m$ stretches a spring $0.40\\,\\mathrm{m}$ to a new equilibrium ($g=10$), so $k=25m$ in SI units. The hanging oscillator's period is",
         "$2\\pi/5\\,\\mathrm{s}$",
         "$T=2\\pi\\sqrt{m/(25m)}=2\\pi/5\\,\\mathrm{s}$, independent of $m$.",
         ["$2\\pi\\sqrt{0.40/10}\\,\\mathrm{s}$ as if it were a pendulum of length $0.40\\,\\mathrm{m}$", "$2\\,\\mathrm{s}$", "$5\\,\\mathrm{s}$"]),
        ("AP Stretch: Compare $T_{\\mathrm{spring}}$ from the stretch $\\delta=0.40\\,\\mathrm{m}$ with a pendulum of length $\\delta$. $T_{\\mathrm{pend}}=$",
         "$2\\pi\\sqrt{0.040}\\,\\mathrm{s}=0.40\\pi\\,\\mathrm{s}$",
         "$T_{\\mathrm{pend}}=2\\pi\\sqrt{L/g}=2\\pi\\sqrt{0.04}=0.40\\pi\\,\\mathrm{s}$. $T_{\\mathrm{spring}}=2\\pi/5=0.40\\pi\\,\\mathrm{s}$ too! For a hanging spring, $T=2\\pi\\sqrt{\\delta/g}$, same form as a pendulum of length $\\delta$.",
         ["$2\\pi\\,\\mathrm{s}$", "$0$", "$\\pi\\,\\mathrm{s}$"]),
        ("AP Stretch: Position $x=0.12\\cos(5t)$ (SI). Amplitude, $\\omega=\\sqrt{k/m}$, and $T$ are",
         "$A=0.12\\,\\mathrm{m}$, $\\omega=5\\,\\mathrm{rad/s}$, $T=2\\pi/5\\,\\mathrm{s}$",
         "Read off the cosine: the coefficient of $t$ inside is $\\omega=2\\pi/T$.",
         ["$A=5\\,\\mathrm{m}$, $T=0.12\\,\\mathrm{s}$", "$A=0.12$, $T=5\\,\\mathrm{s}$", "$A=0$, $T=2\\pi$"]),
        ("AP Stretch: At $x=0$ the mass is $4.0\\,\\mathrm{kg}$ with $v=2.0\\,\\mathrm{m/s}$ and $k=100\\,\\mathrm{N/m}$. $A$ is",
         "$0.40\\,\\mathrm{m}$",
         "$E=\\tfrac12 mv^2=8.0\\,\\mathrm{J}=\\tfrac12 kA^2=50 A^2$, $A^2=0.16$, $A=0.40\\,\\mathrm{m}$.",
         ["$2.0\\,\\mathrm{m}$", "$0.080\\,\\mathrm{m}$", "$8.0\\,\\mathrm{m}$"]),
        ("AP Stretch: A pendulum is moved from Earth ($g=10$) to a planet with $g=2.5$. The period multiplies by",
         "$2$",
         "$T\\propto 1/\\sqrt{g}$, $\\sqrt{10/2.5}=2$.",
         ["$4$", "$1/2$", "$1$"]),
        ("AP Stretch: Damped $x$-$t$ peaks: $0.20$, $0.10$, $0.050\\,\\mathrm{m}$ on successive same-side peaks. The motion is",
         "lightly damped exponential-looking decay of amplitude (halving each cycle here)",
         "Still oscillating. Energy drops by about a factor of four each of those cycles because $E\\propto A^2$.",
         ["driven at resonance growing", "not oscillatory", "SHM with constant $A$"]),
        ("AP Stretch: To keep a clock pendulum's amplitude constant against light damping you need",
         "a small periodic energy input each swing (an escapement)",
         "Replace the mechanical energy drained per cycle.",
         ["to increase $g$", "to cut $L$ to zero", "to remove the bob's mass"]),
        ("AP Stretch: A mass between two horizontal springs, each $k$, displaced $x$ from the middle, feels $F=$",
         "$-2kx$ (both springs restore), so $k_{\\mathrm{eff}}=2k$",
         "Left spring stretched or compressed and right spring the opposite; both push toward the middle.",
         ["$0$ because they cancel", "$-kx$", "$+2kx$ away from the middle"]),
    ])
    return qs


def build_unit7():
    title = "AP Physics Unit 7: Oscillations"
    description = (
        "Restoring forces and SHM, mass-spring and pendulum periods, energy in SHM, sinusoidal graphs, and "
        "qualitative damping — algebra-based, with $T=2\\pi\\sqrt{m/k}$ and $T=2\\pi\\sqrt{L/g}$ as given relations."
    )
    concepts = [
        "Restoring force and SHM",
        "Period of a spring",
        "Period of a pendulum",
        "Energy in SHM",
        "Graphs of SHM",
        "Damping qualitative",
    ]

    c1 = concept_block(
        "1. Restoring force and SHM",
        [
            "A restoring force always points toward equilibrium. For an ideal spring it is also proportional to how far "
            "you are from equilibrium: $F=-kx$. The minus sign is the restore. If $k=50\\,\\mathrm{N/m}$ and $x=+0.10\\,\\mathrm{m}$, $F=-5.0\\,\\mathrm{N}$.",
            "Simple harmonic motion (SHM) is the motion you get from that linear restoring force (and no drag, in the ideal model). "
            "The object overshoots, is pulled back, overshoots the other way, and repeats.",
            "Acceleration $a=F/m=-kx/m$ is most negative when $x$ is most positive. At equilibrium $x=0$, $a=0$ but speed is largest. "
            "At the endpoints $v=0$ and $|a|$ is largest. Those two facts are the SHM personality test.",
            "Equilibrium of a horizontal spring is the unstretched position. A hanging spring's equilibrium is already stretched "
            "by $mg/k$; SHM $x$ is measured from that hanging rest point, not from the unstretched length.",
            "Not every restoring force is SHM. $F=-kx^3$ restores but is not linear, so the period would depend on amplitude. "
            "AP Physics 1's period formulas assume the Hooke (or small-angle pendulum) linear case.",
            "The SHM toolkit is $F=-kx$, the period formulas in the next lessons, and energy "
            "$E=\\tfrac12 kA^2$. Treat the $x$-$t$ cosine as a given shape you read, not a formula you invent.",
        ],
        "Period, energy, and graphs are all decorations on $F=-kx$. If restoring versus equilibrium is fuzzy, every later "
        "SHM graph will feel like a random wave.",
        "Ask: where is $x=0$? Is $F$ toward that point and proportional to $x$? If yes, you may use the SHM toolkit.",
        lesson_figure(
            spring_mass_svg(),
            "Horizontal spring-mass: $x$ measured from the dashed equilibrium",
            "Stretch right, force left. That opposite pair is the restoring force $F=-kx$.",
        )
        + solved(1, "A spring has $k=50\\,\\mathrm{N/m}$. Find the force when $x=+0.10\\,\\mathrm{m}$.",
                 ["$F=-kx=-50(0.10)=-5.0\\,\\mathrm{N}$.",
                  "Magnitude $5.0\\,\\mathrm{N}$ toward equilibrium (left).",
                  "If $x$ were negative (compression), $F$ would be positive (right), still toward $x=0$."],
                 "$5.0\\,\\mathrm{N}$ toward equilibrium", "", "Easy")
        + solved(2, "A $2.0\\,\\mathrm{kg}$ mass is at $x=+0.20\\,\\mathrm{m}$ on $k=80\\,\\mathrm{N/m}$. Find $a$.",
                 ["$F=-80(0.20)=-16\\,\\mathrm{N}$.",
                  "$a=F/m=-8.0\\,\\mathrm{m/s}^2$.",
                  "Largest $|x|$ would mean largest $|a|$."],
                 "$-8.0\\,\\mathrm{m/s}^2$ (toward $-x$)", "", "Medium")
        + solved(3, "A hanging $0.50\\,\\mathrm{kg}$ mass stretches a spring $0.10\\,\\mathrm{m}$ to a new rest point ($g=10$). Find $k$, then $a$ when the mass is $0.04\\,\\mathrm{m}$ below that new equilibrium.",
                 ["At the new rest, $mg=k\\delta$: $5.0=k(0.10)$, so $k=50\\,\\mathrm{N/m}$.",
                  "SHM displacement from hanging equilibrium: $x=+0.04\\,\\mathrm{m}$ down.",
                  "$F=-kx=-2.0\\,\\mathrm{N}$ (upward, toward equilibrium).",
                  "$a=-2.0/0.50=-4.0\\,\\mathrm{m/s}^2$ (up if down is positive)."],
                 "$k=50\\,\\mathrm{N/m}$, $|a|=4.0\\,\\mathrm{m/s}^2$ toward hanging equilibrium", "", "Hard"),
        ("Measuring $x$ from the unstretched length while the mass already hangs at a new zero",
         "Oscillation $x$ is from the hanging equilibrium. Using the unstretched length as $x=0$ secretly leaves a constant $mg$ unbalanced in the SHM equation."),
        ("Connect $|a|$ to $|x|$ with $a=-kx/m$",
         "Endpoints: max $|a|$, zero $v$. Middle: max $|v|$, zero $a$. Recite that pair on every SHM item."),
        [
            "I can use $F=-kx$ with the restoring direction.",
            "I can find $a=-kx/m$ at a given $x$.",
            "I can locate hanging-spring equilibrium using $mg=k\\delta$.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Period of a spring",
        [
            "The time for one full mass-spring cycle is $T=2\\pi\\sqrt{m/k}$. AP Physics 1 gives you this formula. "
            "A $4.0\\,\\mathrm{kg}$ mass on $k=16\\,\\mathrm{N/m}$ has $T=2\\pi\\sqrt{1/4}=\\pi\\,\\mathrm{s}$.",
            "Frequency $f=1/T$ is cycles per second (hertz). The related angular frequency $\\omega=2\\pi f=\\sqrt{k/m}$ "
            "is the number that appears in $x=A\\cos(\\omega t)$ — read $\\omega$ from that written cosine.",
            "$T$ does not depend on amplitude. Pull farther (within Hooke's law) and the mass moves faster in proportion, "
            "so the round trip takes the same time. That independence is a defining SHM surprise.",
            "Heavier mass means larger $T$ ($T\\propto\\sqrt{m}$). Stiffer spring means smaller $T$ ($T\\propto 1/\\sqrt{k}$). "
            "Double $m$, multiply $T$ by $\\sqrt{2}$.",
            "A hanging vertical spring uses the same $T$, with $x$ about hanging equilibrium. Gravity already got absorbed "
            "into the new zero. $T$ does not include $g$ for the ideal spring.",
            "Two springs in parallel (same stretch) give $k_{\\mathrm{eff}}=k_1+k_2$. In series, $1/k_{\\mathrm{eff}}=1/k_1+1/k_2$. "
            "Then plug $k_{\\mathrm{eff}}$ into $T=2\\pi\\sqrt{m/k_{\\mathrm{eff}}}$.",
        ],
        "Pendulum period looks similar but uses $L$ and $g$ instead of $m$ and $k$. Mixing the two formulas is the "
        "classic exam swap.",
        "Write $T=2\\pi\\sqrt{m/k}$. Check that $A$ is not in the formula. Convert to $f=1/T$ only if asked.",
        lesson_figure(
            spring_mass_svg(),
            "Mass $m$ and stiffness $k$ set the period",
            "Amplitude is how far you pull; it does not enter $T=2\\pi\\sqrt{m/k}$.",
        )
        + solved(4, "Find $T$ for $m=4.0\\,\\mathrm{kg}$ and $k=16\\,\\mathrm{N/m}$.",
                 ["$T=2\\pi\\sqrt{m/k}=2\\pi\\sqrt{4/16}=2\\pi(0.50)=\\pi\\,\\mathrm{s}$.",
                  "$f=1/\\pi\\,\\mathrm{Hz}$.",
                  "$\\omega=\\sqrt{k/m}=2.0\\,\\mathrm{rad/s}$."],
                 "$T=\\pi\\,\\mathrm{s}$", "", "Easy")
        + solved(5, "A $1.0\\,\\mathrm{kg}$ mass on $k=100\\,\\mathrm{N/m}$. Find $T$ and $f$.",
                 ["$T=2\\pi\\sqrt{0.01}=2\\pi(0.10)=\\pi/5\\,\\mathrm{s}$.",
                  "$f=5/\\pi\\,\\mathrm{Hz}$.",
                  "If $A$ doubles, $T$ is unchanged."],
                 "$T=\\pi/5\\,\\mathrm{s}$, $f=5/\\pi\\,\\mathrm{Hz}$", "", "Medium")
        + solved(6, "A hanging mass stretches a spring $0.40\\,\\mathrm{m}$ to equilibrium ($g=10$). Find $T$ of small vertical oscillations.",
                 ["$mg=k\\delta\\Rightarrow k=mg/0.40=25m$ (SI).",
                  "$T=2\\pi\\sqrt{m/k}=2\\pi\\sqrt{m/(25m)}=2\\pi/5\\,\\mathrm{s}$.",
                  "Mass canceled. Any mass that stretches this spring $0.40\\,\\mathrm{m}$ has this $T$.",
                  "Note $T=2\\pi\\sqrt{\\delta/g}$, the same form as a pendulum of length $\\delta$."],
                 "$T=2\\pi/5\\,\\mathrm{s}$", "", "Hard"),
        ("Putting amplitude into the period formula",
         "$T=2\\pi\\sqrt{m/k}$ has no $A$. Larger $A$ is a taller cosine, not a slower one, in ideal SHM."),
        ("Use hanging stretch $\\delta$ to find $k=mg/\\delta$, then $T$",
         "That two-step is how AP sneaks $g$ into a spring problem without claiming $T$ depends on $g$ directly."),
        [
            "I can compute $T=2\\pi\\sqrt{m/k}$ and $f=1/T$.",
            "I can scale $T$ when $m$ or $k$ changes.",
            "I can find $T$ for a hanging spring from the equilibrium stretch.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Period of a pendulum",
        [
            "A simple pendulum is a small bob on a light string. For small angles, the restoring piece of weight is "
            "approximately proportional to the angle, so the motion is approximately SHM.",
            "The period is $T=2\\pi\\sqrt{L/g}$. Length $L$ is to the CM of the bob. Gravity $g$ sits under the root. "
            "Mass does not appear. For $L=10\\,\\mathrm{m}$ and $g=10\\,\\mathrm{m/s}^2$, $T=2\\pi\\,\\mathrm{s}$.",
            "For $L=2.5\\,\\mathrm{m}$ and $g=10$, $T=\\pi\\,\\mathrm{s}$. Doubling $L$ multiplies $T$ by $\\sqrt{2}$, not by $2$.",
            "On a planet with smaller $g$, $T$ is larger: the clock runs slow. That is a favorite comparison item.",
            "Amplitude (if still small) does not enter $T$, same surprise as the spring. A $5^\\circ$ swing and a $10^\\circ$ "
            "swing tick together in the SHM model.",
            "Do not use $T=2\\pi\\sqrt{m/k}$ on a pendulum, and do not use $T=2\\pi\\sqrt{L/g}$ on a mass-spring. "
            "The letters tell you which machine you have.",
        ],
        "Energy of a pendulum still uses $mgh$ of the bob, not $\\tfrac12 kA^2$. Mixing spring energy with pendulum period "
        "is the other classic mash-up error.",
        "Identify $L$ and $g$. Ignore mass and small $A$. Write $T=2\\pi\\sqrt{L/g}$.",
        lesson_figure(
            xy_graph(
                curves=[("#0f766e", sample_curve(lambda t: 0.2 * __import__("math").cos(t), 0, 6.28))],
                points=[(0, 0.2, "θ max")],
                xlim=(-0.3, 7), ylim=(-0.35, 0.35), xlab="t (s)", ylab="θ (rad)", w=320, h=220,
            ),
            "Small-angle pendulum angle versus time",
            "Cosine SHM. Period is the repeat time, set by $L$ and $g$, not by how tall the cosine is.",
        )
        + solved(7, "A pendulum has $L=10\\,\\mathrm{m}$ and $g=10\\,\\mathrm{m/s}^2$. Find $T$.",
                 ["$T=2\\pi\\sqrt{L/g}=2\\pi\\sqrt{1}=2\\pi\\,\\mathrm{s}$.",
                  "Mass is not needed.",
                  "A $20\\,\\mathrm{m}$ pendulum would have $T=2\\pi\\sqrt{2}\\,\\mathrm{s}$."],
                 "$2\\pi\\,\\mathrm{s}$", "", "Easy")
        + solved(8, "$L=2.5\\,\\mathrm{m}$, $g=10$. Find $T$.",
                 ["$T=2\\pi\\sqrt{0.25}=2\\pi(0.50)=\\pi\\,\\mathrm{s}$.",
                  "$f=1/\\pi\\,\\mathrm{Hz}$.",
                  "Same $T$ as the $m=4$, $k=16$ spring — coincidence of numbers, different machines."],
                 "$\\pi\\,\\mathrm{s}$", "", "Medium")
        + solved(9, "A clock pendulum is designed for $g=10$. It is moved to a planet with $g=2.5$. By what factor does $T$ change, and does the clock run fast or slow?",
                 ["$T\\propto 1/\\sqrt{g}$.",
                  "Factor $\\sqrt{10/2.5}=\\sqrt{4}=2$. Period doubles.",
                  "Each “second” of the clock lasts twice as long: the clock runs slow.",
                  "To fix it you would shorten $L$ by a factor of $4$ (because $T\\propto\\sqrt{L}$)."],
                 "$T$ doubles; clock runs slow", "", "Hard"),
        ("Using the bob's mass in the pendulum period",
         "$m$ cancels in the small-angle model, just as it canceled in $a=g\\sin\\theta$ on a frictionless ramp. Heavier bobs do not tick slower."),
        ("Write $L$ as the string length to the CM, not the arc length of the swing",
         "Arc length is $s=L\\theta$. Period cares about $L$ and $g$, not about how long the arc is this particular swing."),
        [
            "I can compute $T=2\\pi\\sqrt{L/g}$ with $g=10$.",
            "I can scale $T$ when $L$ or $g$ changes.",
            "I can explain why mass and small amplitude drop out.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Energy in SHM",
        [
            "An ideal mass-spring trades spring energy and kinetic energy: $E=\\tfrac12 kA^2=\\tfrac12 mv^2+\\tfrac12 kx^2$ "
            "at every moment. For $k=50\\,\\mathrm{N/m}$ and $A=0.20\\,\\mathrm{m}$, $E=1.0\\,\\mathrm{J}$.",
            "At an endpoint, $v=0$ and $U_s=E$. At equilibrium, $U_s=0$ (horizontal spring) and $K=E$. "
            "Maximum speed is $v_{\\max}=A\\sqrt{k/m}$. For $m=4$, $k=16$, $A=0.50$, $v_{\\max}=1.0\\,\\mathrm{m/s}$.",
            "Halfway in $x$ ($x=A/2$), $U_s=E/4$ and $K=3E/4$. Energy is not split 50-50 at the geometric middle of the stretch, "
            "because $U\\propto x^2$.",
            "A pendulum's energy is $mgh$ plus $K$, with $h$ from the lowest point. At the bottom, $K=mgh_{\\mathrm{max}}$. "
            "That is Unit 3 energy, not $\\tfrac12 kA^2$, unless you are approximating a small angle with an effective $k$.",
            "Energy bars for SHM: the $K$ and $U$ bars slosh twice per period (two equilibrium passages per cycle). "
            "Total bar height is constant if damping is absent.",
            "If damping is present, the total $K+U$ bar slowly shortens and a thermal bar grows. That picture is the next lesson.",
        ],
        "Graphs of SHM are easier if you already know where $K$ and $U$ peak. Energy is the decoder ring for $x$, $v$, and $a$ shapes.",
        "Write $E=\\tfrac12 kA^2$. At a given $x$, $U=\\tfrac12 kx^2$ and $K=E-U$. Then $v=\\sqrt{2K/m}$.",
        lesson_figure(
            energy_bars_svg(ke=2, pe=2, thermal=0),
            "SHM at a mid-stretch: both $K$ and $U$ nonempty",
            "Total height $\\tfrac12 kA^2$. Endpoints empty the $K$ bar; equilibrium empties the spring $U$ bar.",
        )
        + solved(10, "Find $E$ for $k=50\\,\\mathrm{N/m}$ and $A=0.20\\,\\mathrm{m}$.",
                 ["$E=\\tfrac12 kA^2=\\tfrac12(50)(0.04)=1.0\\,\\mathrm{J}$.",
                  "At the end, $U=1.0\\,\\mathrm{J}$, $K=0$.",
                  "At the middle, $K=1.0\\,\\mathrm{J}$, $U=0$."],
                 "$1.0\\,\\mathrm{J}$", "", "Easy")
        + solved(11, "$m=4.0\\,\\mathrm{kg}$, $k=16\\,\\mathrm{N/m}$, $A=0.50\\,\\mathrm{m}$. Find $v_{\\max}$.",
                 ["$v_{\\max}=A\\sqrt{k/m}=0.50\\sqrt{16/4}=0.50\\times 2=1.0\\,\\mathrm{m/s}$.",
                  "Or $E=\\tfrac12(16)(0.25)=2.0\\,\\mathrm{J}=\\tfrac12(4)v^2$, $v=1.0\\,\\mathrm{m/s}$.",
                  "That speed occurs at $x=0$."],
                 "$1.0\\,\\mathrm{m/s}$", "", "Medium")
        + solved(12, "A $4.0\\,\\mathrm{kg}$ mass on $k=100\\,\\mathrm{N/m}$ passes $x=0$ at $2.0\\,\\mathrm{m/s}$. Find $A$, then $K$ at $x=A/2$.",
                 ["$E=\\tfrac12 mv^2=8.0\\,\\mathrm{J}=\\tfrac12 kA^2=50 A^2$, so $A^2=0.16$, $A=0.40\\,\\mathrm{m}$.",
                  "At $x=A/2=0.20\\,\\mathrm{m}$, $U=\\tfrac12(100)(0.04)=2.0\\,\\mathrm{J}$.",
                  "$K=8.0-2.0=6.0\\,\\mathrm{J}$.",
                  "Not $4.0\\,\\mathrm{J}$; the $x^2$ dependence makes the split $U=E/4$, $K=3E/4$."],
                 "$A=0.40\\,\\mathrm{m}$, $K=6.0\\,\\mathrm{J}$ at $x=A/2$", "", "Hard"),
        ("Splitting energy 50-50 at $x=A/2$",
         "$U\\propto x^2$, so $x=A/2$ stores only a quarter of $E$ as $U$. Three quarters remain kinetic."),
        ("Use $E=\\tfrac12 kA^2$ as the budget, then subtract $U(x)$",
         "That budget line is faster than solving $v$ from $a=kx/m$ at one point and then mixing signs."),
        [
            "I can compute $E=\\tfrac12 kA^2$ for a spring oscillator.",
            "I can find $v_{\\max}=A\\sqrt{k/m}$.",
            "I can split $K$ and $U$ at a given $x$ using $U\\propto x^2$.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Graphs of SHM",
        [
            "The position graph of SHM is a sine or cosine wave. A common start is $x=A\\cos(2\\pi t/T)$, released from rest "
            "at $+A$. At $t=0$, $x=A$ and $v=0$.",
            "Velocity is the slope of $x$-$t$. The $v$-$t$ graph is a sinusoid shifted by a quarter period: zero at the $x$ peaks, "
            "largest when $x$ crosses zero. Steeper $x$-$t$ means larger $|v|$ at that instant.",
            "Acceleration is opposite $x$ because $a=-kx/m$. The $a$-$t$ graph looks like an upside-down $x$-$t$ graph. "
            "When $x$ is most positive, $a$ is most negative.",
            "Period $T$ is the time from one peak to the next peak of the same kind. Frequency is $1/T$. "
            "Two graphs with the same $T$ and different $A$ are the same pitch, different volume.",
            "If $x=0.12\\cos(5t)$ in SI units, $A=0.12\\,\\mathrm{m}$, the $5$ is $\\omega=2\\pi/T=5\\,\\mathrm{rad/s}$, so $T=2\\pi/5\\,\\mathrm{s}$. "
            "Read the numbers; do not differentiate.",
            "Match three sketches on an FRQ: $x$ cosine, $v$ sine (or inverted sine), $a$ inverted cosine. "
            "Zeros of $v$ line up with peaks of $x$. Zeros of $a$ line up with zeros of $x$.",
        ],
        "Damping will shrink these sines. If the undamped shapes are shaky, the decaying envelope will be unreadable.",
        "Sketch $x$ first. Put $v=0$ at $x$ peaks. Put $a$ as a flipped copy of $x$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: 2 * __import__("math").cos(3.1416 * t / 2), 0, 8))],
                points=[(0, 2, "A"), (2, 0, "eq"), (4, -2, "−A")],
                xlim=(-0.4, 8.5), ylim=(-2.8, 2.8), xlab="t (s)", ylab="x (m)", w=340, h=240,
            ),
            "$x(t)$ for SHM with $T=4\\,\\mathrm{s}$, $A=2\\,\\mathrm{m}$, starting at $+A$",
            "Cosine. Slope (velocity) is zero at the peaks and steepest at the axis crossings.",
        )
        + solved(13, "$x=A\\cos(2\\pi t/T)$ with $T=2.0\\,\\mathrm{s}$, $A=0.10\\,\\mathrm{m}$. Find $x(0)$ and $x(0.50\\,\\mathrm{s})$.",
                 ["$x(0)=A(1)=0.10\\,\\mathrm{m}$.",
                  "$t=0.50\\,\\mathrm{s}$ is $T/4$, a quarter cycle to equilibrium: $x=0$.",
                  "At that instant $|v|$ is $v_{\\max}$."],
                 "$0.10\\,\\mathrm{m}$, then $0$", "", "Easy")
        + solved(14, "For that motion, describe $a$ at $t=0$ and at $t=T/4$.",
                 ["At $t=0$, $x=+A$, so $a=-kA/m$, the most negative value.",
                  "At $t=T/4$, $x=0$, so $a=0$.",
                  "The $a$ graph is an inverted cosine."],
                 "$a$ most negative at $t=0$; $a=0$ at $t=T/4$", "", "Medium")
        + solved(15, "Read $x=0.12\\cos(5t)$ (SI). Find $A$, $\\omega$, $T$, and $v_{\\max}$ if $m=3.0\\,\\mathrm{kg}$ implies $k=m\\omega^2$.",
                 ["$A=0.12\\,\\mathrm{m}$, $\\omega=5.0\\,\\mathrm{rad/s}$, $T=2\\pi/5\\,\\mathrm{s}$.",
                  "$k=m\\omega^2=3(25)=75\\,\\mathrm{N/m}$.",
                  "$v_{\\max}=A\\omega=0.12(5)=0.60\\,\\mathrm{m/s}$.",
                  "All from the written cosine plus the product $v_{\\max}=A\\omega$."],
                 "$A=0.12\\,\\mathrm{m}$, $T=2\\pi/5\\,\\mathrm{s}$, $v_{\\max}=0.60\\,\\mathrm{m/s}$", "", "Hard"),
        ("Drawing $a$-$t$ in phase with $x$-$t$",
         "They are opposites. Positive $x$ means negative $a$. If your three stacked graphs all peak together, the $a$ graph is wrong."),
        ("Mark $T$ as peak-to-peak on $x$-$t$, not zero-to-zero",
         "Zero to the next zero is $T/2$. Students who call that $T$ double every frequency."),
        [
            "I can sketch $x(t)$ as a cosine released from $+A$.",
            "I can align zeros of $v$ with peaks of $x$ and zeros of $a$ with zeros of $x$.",
            "I can read $A$ and $T$ (or $\\omega$) from $x=A\\cos(\\omega t)$.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Damping, qualitative",
        [
            "Damping is a resistive force — air drag, internal rubber friction, a dashpot — that removes mechanical energy "
            "from the oscillator. Ideal SHM ignored it. Real swings slowly die.",
            "Light damping: the $x$-$t$ graph is still a wiggle, but the amplitude envelope shrinks. Period stays close to "
            "the undamped $T$. Energy $E\\propto A^2$ falls faster than $A$ itself.",
            "Energy bars: $K+U$ slowly lose height while a thermal bar grows. The oscillator plus the air still conserve "
            "total energy; the mechanical pair does not.",
            "Heavy (over)damping: the mass creeps back to equilibrium without a real oscillation. A door closer is closer "
            "to this than to a ringing spring.",
            "Resonance: a periodic push at the natural period can rebuild the amplitude if damping is small. "
            "Pushing a swing in time with the motion is the playground version. Qualitative AP 1 does not require a driven-oscillator formula.",
            "Clocks need an escapement — a little energy each swing — to replace what damping steals. Otherwise even a "
            "good pendulum stops.",
        ],
        "Fluids (next unit) will add drag in a different costume. Recognizing “mechanical energy is leaking” is the "
        "shared idea.",
        "Look at $x$-$t$: shrinking envelope means light damping. No wiggles means overdamped. Growing envelope means a drive at resonance.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", sample_curve(
                    lambda t: 2 * (0.75 ** t) * __import__("math").cos(3.1416 * t), 0, 6))],
                points=[(0, 2, "start")],
                xlim=(-0.3, 6.5), ylim=(-2.4, 2.4), xlab="t (s)", ylab="x", w=340, h=240,
            ),
            "Lightly damped $x(t)$: decaying cosine envelope",
            "Still oscillatory. Peaks get smaller. Thermal energy is rising offstage.",
        )
        + solved(16, "Describe the $x$-$t$ graph of a lightly damped mass-spring released from rest at $+A$.",
                 ["It starts at $+A$ like a cosine.",
                  "Each later peak is smaller.",
                  "It still crosses equilibrium many times before looking dead."],
                 "decaying cosine (shrinking amplitude)", "", "Easy")
        + solved(17, "Successive same-side peaks are $0.20$, $0.10$, $0.050\\,\\mathrm{m}$. What happens to energy each of those cycles?",
                 ["$E\\propto A^2$, so energy ratios are $0.04 : 0.01 : 0.0025$, i.e. factors of $1/4$ each listed step.",
                  "Amplitude halved, energy became one quarter.",
                  "The missing energy is thermal (and maybe sound)."],
                 "energy $\\times 1/4$ when $A$ halves", "", "Medium")
        + solved(18, "A pendulum clock in air would stop. What must the mechanism do, and what would resonance look like if a periodic shove matched $T$?",
                 ["Damping drains $E_{\\mathrm{mech}}$ each swing.",
                  "An escapement (or a parent pushing a swing) adds a little energy each cycle to hold $A$ steady.",
                  "If you push at the natural $T$ and damping is small, $A$ can grow — resonance.",
                  "If damping is huge, even a matched push barely moves it."],
                 "add energy each cycle; matched drive can grow $A$ if damping is small", "", "Hard"),
        ("Calling a decaying wiggle “not SHM, so $T=2\\pi\\sqrt{m/k}$ is useless”",
         "Light damping keeps the period close to that value. You can still estimate $T$ from peak-to-peak times on the decaying graph."),
        ("Read the envelope, not just one wiggle",
         "Connect the peaks with a dashed decaying curve. That envelope is the damping story; the wiggle inside is the oscillator."),
        [
            "I can describe light damping as a shrinking $x$-$t$ envelope.",
            "I can connect falling $A$ to falling $E\\propto A^2$ and rising thermal energy.",
            "I can explain resonance qualitatively as a drive matching the natural period.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Fluids
# ===========================================================================

def _u8_questions():
    qs = []
    _add(qs, [
        ("Density is mass per volume, $\\rho=m/V$. An $800\\,\\mathrm{kg}$ block occupying $0.40\\,\\mathrm{m}^3$ has $\\rho=$",
         "$2.0\\times 10^3\\,\\mathrm{kg/m}^3$",
         "$\\rho=800/0.40=2000\\,\\mathrm{kg/m}^3$.",
         ["$320\\,\\mathrm{kg/m}^3$", "$800.4\\,\\mathrm{kg/m}^3$", "$0.0005\\,\\mathrm{kg/m}^3$"]),
        ("Pressure is force per area, $P=F/A$, perpendicular to the surface. $200\\,\\mathrm{N}$ on $0.050\\,\\mathrm{m}^2$ is",
         "$4.0\\times 10^3\\,\\mathrm{Pa}$",
         "$P=200/0.050=4000\\,\\mathrm{Pa}$. A pascal is a $\\mathrm{N/m}^2$.",
         ["$10\\,\\mathrm{Pa}$", "$200.05\\,\\mathrm{Pa}$", "$0.00025\\,\\mathrm{Pa}$"]),
        ("Gauge pressure at depth $h$ in a liquid is $\\rho g h$. Fresh water $\\rho=1000\\,\\mathrm{kg/m}^3$, $h=2.0\\,\\mathrm{m}$, $g=10$ gives",
         "$2.0\\times 10^4\\,\\mathrm{Pa}$",
         "$P=1000(10)(2)=20000\\,\\mathrm{Pa}$ above the surface pressure.",
         ["$20\\,\\mathrm{Pa}$", "$200\\,\\mathrm{Pa}$", "$500\\,\\mathrm{Pa}$"]),
        ("Absolute pressure is $P_0+\\rho g h$ if $P_0$ is the surface pressure. With $P_0=1.0\\times 10^5\\,\\mathrm{Pa}$ and $\\rho gh=2.0\\times 10^4\\,\\mathrm{Pa}$, $P_{\\mathrm{abs}}=$",
         "$1.2\\times 10^5\\,\\mathrm{Pa}$",
         "Add them: $1.2\\times 10^5\\,\\mathrm{Pa}$.",
         ["$8.0\\times 10^4\\,\\mathrm{Pa}$", "$2.0\\times 10^4\\,\\mathrm{Pa}$", "$1.0\\times 10^5\\,\\mathrm{Pa}$"]),
        ("Pressure in a static fluid at a given depth is",
         "the same in all directions (and on any orientation of a small surface)",
         "That is why dams are thick at the bottom: $P$ grows with depth, not with “which way.”",
         ["only downward", "only on horizontal floors", "zero on vertical walls"]),
    ])
    _add(qs, [
        ("Pascal's principle: a change in pressure in a confined incompressible fluid is transmitted undiminished. Hydraulic lift: $F_1/A_1=F_2/A_2$. If $F_1=40\\,\\mathrm{N}$, $A_1=0.010\\,\\mathrm{m}^2$, $A_2=0.20\\,\\mathrm{m}^2$, $F_2=$",
         "$800\\,\\mathrm{N}$",
         "$P=40/0.010=4000\\,\\mathrm{Pa}=F_2/0.20$, so $F_2=800\\,\\mathrm{N}$.",
         ["$40\\,\\mathrm{N}$", "$2.0\\,\\mathrm{N}$", "$8000\\,\\mathrm{N}$"]),
        ("The output piston moves a smaller distance. If $A_2=20 A_1$ and the small piston moves $0.10\\,\\mathrm{m}$, the large piston moves",
         "$0.0050\\,\\mathrm{m}$",
         "Volumes match: $A_1 d_1=A_2 d_2$, $d_2=d_1/20=0.0050\\,\\mathrm{m}$. Energy $F d$ matches in the ideal case.",
         ["$2.0\\,\\mathrm{m}$", "$0.10\\,\\mathrm{m}$", "$20\\,\\mathrm{m}$"]),
        ("Hydraulics trade force for distance, like a",
         "lever (mechanical advantage, work in $\\approx$ work out if ideal)",
         "You push a long way with a small force; the car rises a little way with a large force.",
         ["battery", "pendulum clock", "fuse"]),
        ("If the fluid can leak, Pascal's undiminished-pressure story",
         "fails because the fluid is no longer a confined system",
         "The principle assumes a closed, incompressible liquid.",
         ["still holds exactly", "makes $P$ negative", "creates energy"]),
        ("A barber chair cylinder has $A=0.012\\,\\mathrm{m}^2$ and must support $720\\,\\mathrm{N}$. Minimum fluid pressure is",
         "$6.0\\times 10^4\\,\\mathrm{Pa}$",
         "$P=F/A=720/0.012=60000\\,\\mathrm{Pa}$.",
         ["$8.6\\,\\mathrm{Pa}$", "$720\\,\\mathrm{Pa}$", "$0.012\\,\\mathrm{Pa}$"]),
    ])
    _add(qs, [
        ("Buoyant force is the net upward force from pressure increasing with depth. Archimedes: $F_b=\\rho_{\\mathrm{fluid}} V_{\\mathrm{displaced}} g$. Water, $V=0.0020\\,\\mathrm{m}^3$, $g=10$ gives",
         "$20\\,\\mathrm{N}$",
         "$F_b=1000(0.0020)(10)=20\\,\\mathrm{N}$.",
         ["$0.020\\,\\mathrm{N}$", "$2000\\,\\mathrm{N}$", "$10\\,\\mathrm{N}$"]),
        ("A $15\\,\\mathrm{N}$ object floating in water displaces",
         "$15\\,\\mathrm{N}$ of water (weight of displaced fluid equals the object's weight)",
         "For floating, $F_b=mg$. Only part of the volume may be submerged.",
         ["$0$", "its entire volume always, even if $\\rho_{\\mathrm{obj}}\\ll\\rho_w$", "$30\\,\\mathrm{N}$ of water"]),
        ("An object denser than the fluid",
         "sinks; $F_b$ equals the fluid weight of the object's full volume, which is less than $mg$",
         "Net force $mg-F_b$ is down. Apparent weight is $mg-F_b$.",
         ["floats with $V_{\\mathrm{sub}}=0$", "has $F_b=0$", "has negative mass"]),
        ("Apparent weight of a $50\\,\\mathrm{N}$ rock that displaces $20\\,\\mathrm{N}$ of water is",
         "$30\\,\\mathrm{N}$",
         "Scale reading in water: $mg-F_b=30\\,\\mathrm{N}$.",
         ["$70\\,\\mathrm{N}$", "$50\\,\\mathrm{N}$", "$20\\,\\mathrm{N}$"]),
        ("A boat sinks lower when you board it because",
         "it must displace more water to make a larger $F_b$ matching the extra weight",
         "Floating condition $F_b=m_{\\mathrm{tot}}g$.",
         ["water density fell", "buoyancy vanished", "$g$ increased"]),
    ])
    _add(qs, [
        ("Continuity for incompressible flow: $A_1 v_1=A_2 v_2$ (volume flow rate $Q$ is constant). If $A_1=0.040\\,\\mathrm{m}^2$, $v_1=2.0\\,\\mathrm{m/s}$, $A_2=0.010\\,\\mathrm{m}^2$, then $v_2=$",
         "$8.0\\,\\mathrm{m/s}$",
         "$Q=0.080\\,\\mathrm{m}^3/\\mathrm{s}=A_2 v_2$, $v_2=8.0\\,\\mathrm{m/s}$. Narrower means faster.",
         ["$0.50\\,\\mathrm{m/s}$", "$2.0\\,\\mathrm{m/s}$", "$4.0\\,\\mathrm{m/s}$"]),
        ("Volume flow rate $Q=Av$. A hose $A=4.0\\times 10^{-4}\\,\\mathrm{m}^2$ at $5.0\\,\\mathrm{m/s}$ delivers",
         "$2.0\\times 10^{-3}\\,\\mathrm{m}^3/\\mathrm{s}$",
         "$Q=(4.0\\times 10^{-4})(5.0)=2.0\\times 10^{-3}\\,\\mathrm{m}^3/\\mathrm{s}$.",
         ["$1.25\\times 10^4\\,\\mathrm{m}^3/\\mathrm{s}$", "$5.0004\\,\\mathrm{m}^3/\\mathrm{s}$", "$0$"]),
        ("Mass flow rate for constant $\\rho$ is $\\rho Q$. Water at that $Q$ has $\\dot m=$",
         "$2.0\\,\\mathrm{kg/s}$",
         "$\\rho Q=1000(0.0020)=2.0\\,\\mathrm{kg/s}$.",
         ["$0.0020\\,\\mathrm{kg/s}$", "$1000\\,\\mathrm{kg/s}$", "$2.0\\times 10^6\\,\\mathrm{kg/s}$"]),
        ("Why does a river speed up in a narrow gorge (idealized)?",
         "continuity: smaller $A$, larger $v$ to keep $Q$",
         "Incompressible water has nowhere else to go.",
         ["Pascal's principle alone", "$g$ is larger in gorges", "buoyancy reversed"]),
        ("If flow could pile up in a pipe, continuity would fail. Steady incompressible flow means",
         "the same volume per second through every cross-section",
         "That is the meaning of $A_1 v_1=A_2 v_2$.",
         ["speed is the same everywhere", "pressure is the same everywhere", "the pipe must have constant $A$"]),
    ])
    _add(qs, [
        ("Bernoulli's equation (ideal, steady, incompressible, along a streamline) is $P+\\rho g h+\\tfrac12\\rho v^2=\\mathrm{constant}$. It is an energy-per-volume statement. If height is fixed and speed rises, pressure",
         "falls",
         "Faster fluid, lower $P$. That is the venturi / airplane-wing qualitative story on AP 1.",
         ["rises", "must be zero", "becomes $\\rho g h$ only"]),
        ("A horizontal pipe: $v_1=2.0\\,\\mathrm{m/s}$, $v_2=8.0\\,\\mathrm{m/s}$, $\\rho=1000$. The pressure drop $P_1-P_2$ is",
         "$3.0\\times 10^4\\,\\mathrm{Pa}$",
         "$\\tfrac12\\rho(v_2^2-v_1^2)=500(64-4)=500(60)=30000\\,\\mathrm{Pa}$.",
         ["$6000\\,\\mathrm{Pa}$", "$10\\,\\mathrm{Pa}$", "$0$ because it is horizontal"]),
        ("Torricelli: speed of efflux from a hole a depth $h$ below a large open surface is",
         "$\\sqrt{2gh}$",
         "Like falling from rest through $h$. For $h=5.0\\,\\mathrm{m}$, $g=10$, $v=10\\,\\mathrm{m/s}$.",
         ["$gh$", "$2gh$", "$\\rho g h$"]),
        ("A roof blows off in a storm (qualitative) because",
         "fast air over the roof has lower pressure than the stiller air inside",
         "Bernoulli plus a path for the pressure difference to lift the roof.",
         ["air has no mass", "Pascal says pressure cannot differ", "buoyancy of the shingles"]),
        ("Bernoulli assumes no viscous losses. Real pipes",
         "need extra pressure to overcome drag; $P+\\rho gh+\\tfrac12\\rho v^2$ is not perfectly constant",
         "AP 1 mostly uses the ideal equation and then a qualitative “friction in the pipe” comment.",
         ["are always ideal", "have $\\rho=0$", "cannot have flow"]),
    ])
    _add(qs, [
        ("Fluid FRQ habit: start with a labeled figure showing $A$, $v$, $P$, $h$. Then pick",
         "continuity and/or Bernoulli and/or $P=\\rho g h$ and/or $F_b=\\rho V g$",
         "Name the law before substituting. That is the scoring language.",
         ["Gauss's law", "Snell's law", "$F=-kx$ only"]),
        ("When the pipe area changes, you almost always need",
         "continuity to relate the two speeds before Bernoulli can find $\\Delta P$",
         "Bernoulli has both $v_1$ and $v_2$. Continuity supplies the missing speed.",
         ["only Pascal", "only Archimedes", "Hooke's law"]),
        ("When an object floats, write $F_b=mg$ and $F_b=\\rho_f V_{\\mathrm{sub}} g$. Then",
         "$V_{\\mathrm{sub}}/V=\\rho_{\\mathrm{obj}}/\\rho_f$",
         "The fraction submerged equals the density ratio (if fully floating, not sunk).",
         ["$V_{\\mathrm{sub}}=0$", "$\\rho_{\\mathrm{obj}}=0$", "$g$ cancels so floating is impossible"]),
        ("A manometer FRQ: the height difference $\\Delta h$ of the liquid columns means",
         "$\\Delta P=\\rho g\\Delta h$ between the two sides",
         "Connect that $\\Delta P$ to whatever tanks or pipes are attached.",
         ["$\\Delta P=0$ always", "$\\Delta P=\\tfrac12\\rho v^2$ with no $h$", "the liquid has no density"]),
        ("Units check: $\\tfrac12\\rho v^2$ has units of",
         "pressure (pascals)",
         "That is why it sits next to $P$ in Bernoulli. $\\mathrm{(kg/m^3)(m/s)^2=N/m^2}$.",
         ["joules with no volume", "newtons", "radians"]),
    ])
    _add(qs, [
        ("A cube $0.10\\,\\mathrm{m}$ on a side has mass $0.80\\,\\mathrm{kg}$. Density is",
         "$800\\,\\mathrm{kg/m}^3$",
         "$V=0.0010\\,\\mathrm{m}^3$, $\\rho=800\\,\\mathrm{kg/m}^3$.",
         ["$8.0\\,\\mathrm{kg/m}^3$", "$0.80\\,\\mathrm{kg/m}^3$", "$80\\,\\mathrm{kg/m}^3$"]),
        ("Gauge pressure $30\\,\\mathrm{m}$ under a freshwater lake ($g=10$) is",
         "$3.0\\times 10^5\\,\\mathrm{Pa}$",
         "$\\rho gh=1000(10)(30)=3.0\\times 10^5\\,\\mathrm{Pa}$.",
         ["$30\\,\\mathrm{Pa}$", "$300\\,\\mathrm{Pa}$", "$3.0\\times 10^3\\,\\mathrm{Pa}$"]),
        ("Force on a $2.0\\,\\mathrm{m}^2$ viewing window if that gauge pressure were uniform on it would be",
         "$6.0\\times 10^5\\,\\mathrm{N}$",
         "$F=PA$ (here using the $3.0\\times 10^5\\,\\mathrm{Pa}$ figure as a rough uniform estimate).",
         ["$1.5\\times 10^5\\,\\mathrm{N}$", "$3.0\\times 10^5\\,\\mathrm{N}$", "$2.0\\,\\mathrm{N}$"]),
        ("Hydraulic: small $A=4.0\\times 10^{-4}\\,\\mathrm{m}^2$, $F=50\\,\\mathrm{N}$. Large $A=0.020\\,\\mathrm{m}^2$. $F_{\\mathrm{out}}=$",
         "$2500\\,\\mathrm{N}$",
         "$P=50/(4.0\\times 10^{-4})=1.25\\times 10^5\\,\\mathrm{Pa}$, $F=P A=2500\\,\\mathrm{N}$.",
         ["$50\\,\\mathrm{N}$", "$1.0\\,\\mathrm{N}$", "$2.0\\times 10^6\\,\\mathrm{N}$"]),
        ("A $4.0\\,\\mathrm{N}$ wood block floats with $75\\%$ submerged. Weight of displaced water is",
         "$4.0\\,\\mathrm{N}$",
         "Floating: $F_b=mg$. The $75\\%$ tells you $\\rho_{\\mathrm{wood}}=0.75\\rho_w$.",
         ["$3.0\\,\\mathrm{N}$", "$5.33\\,\\mathrm{N}$", "$0$"]),
        ("Then $\\rho_{\\mathrm{wood}}/\\rho_w=$",
         "$0.75$",
         "Fraction submerged for a floater.",
         ["$1.33$", "$0$", "$4$"]),
        ("A $10\\,\\mathrm{N}$ metal is fully submerged and $F_b=2.0\\,\\mathrm{N}$. Apparent weight is",
         "$8.0\\,\\mathrm{N}$",
         "$10-2=8.0\\,\\mathrm{N}$.",
         ["$12\\,\\mathrm{N}$", "$2.0\\,\\mathrm{N}$", "$10\\,\\mathrm{N}$"]),
        ("Pipe narrows from $12\\,\\mathrm{cm}^2$ to $4.0\\,\\mathrm{cm}^2$. If $v_{\\mathrm{wide}}=1.5\\,\\mathrm{m/s}$, $v_{\\mathrm{narrow}}=$",
         "$4.5\\,\\mathrm{m/s}$",
         "$12(1.5)=4.0 v$, $v=4.5\\,\\mathrm{m/s}$.",
         ["$0.50\\,\\mathrm{m/s}$", "$1.5\\,\\mathrm{m/s}$", "$6.0\\,\\mathrm{m/s}$"]),
        ("Hole $h=5.0\\,\\mathrm{m}$ below an open tank surface. Exit speed ($g=10$) is",
         "$10\\,\\mathrm{m/s}$",
         "$v=\\sqrt{2gh}=\\sqrt{100}=10\\,\\mathrm{m/s}$.",
         ["$5.0\\,\\mathrm{m/s}$", "$50\\,\\mathrm{m/s}$", "$\\sqrt{10}\\,\\mathrm{m/s}$"]),
        ("Horizontal venturi: $v$ doubles. The $\\tfrac12\\rho v^2$ term becomes",
         "four times larger",
         "$v^2$ scaling. Pressure must drop to compensate if $h$ is fixed.",
         ["twice as large", "unchanged", "half"]),
        ("A helium balloon rises because",
         "$F_b$ of displaced air exceeds the balloon's weight",
         "Same Archimedes law, low-density object in a fluid.",
         ["helium has negative mass", "Pascal forbids pressure", "continuity forces it up"]),
        ("Blood-flow qualitative: plaque narrows an artery, local $v$ rises and local $P$",
         "drops (Bernoulli), which can collapse a floppy vessel further",
         "Continuity plus Bernoulli. A grim AP-style application.",
         ["rises a lot", "is unrelated to $v$", "becomes $mgh$ only"]),
        ("A cube of wood $\\rho=600$ floats in water $\\rho=1000$. Fraction above water is",
         "$0.40$",
         "Submerged fraction $0.60$, so $40\\%$ above.",
         ["$0.60$", "$0$", "$1$"]),
        ("Pressure at $4.0\\,\\mathrm{m}$ depth in a pool versus $4.0\\,\\mathrm{m}$ depth in a thin tube of the same water is",
         "the same ($P$ depends on depth, not on total water volume)",
         "A common trap: the lake is not “heavier” at the same $h$.",
         ["much larger in the pool", "zero in the tube", "negative in the tube"]),
        ("A $1.2\\,\\mathrm{m}$ column of water ($\\rho=1000\\,\\mathrm{kg/m}^3$, $g=10$) produces gauge pressure",
         "$1.2\\times 10^4\\,\\mathrm{Pa}$",
         "$P_g=\\rho g h=1000\\times 10\\times 1.2=1.2\\times 10^4\\,\\mathrm{Pa}$.",
         ["$1.2\\,\\mathrm{Pa}$", "$120\\,\\mathrm{Pa}$", "$1.2\\times 10^3\\,\\mathrm{Pa}$"]),
        ("A garden hose narrows from $8.0\\,\\mathrm{cm}^2$ to $2.0\\,\\mathrm{cm}^2$. If water speed in the wide part is $1.5\\,\\mathrm{m/s}$, speed in the nozzle is",
         "$6.0\\,\\mathrm{m/s}$",
         "Continuity $A_1 v_1=A_2 v_2$ gives $v_2=(8.0/2.0)(1.5)=6.0\\,\\mathrm{m/s}$.",
         ["$1.5\\,\\mathrm{m/s}$", "$0.375\\,\\mathrm{m/s}$", "$3.0\\,\\mathrm{m/s}$"]),
        ("AP Stretch: A U-tube has $0.25\\,\\mathrm{m}$ of oil ($\\rho=800$) on one side balancing extra water height $h$ on the other. $h=$",
         "$0.20\\,\\mathrm{m}$",
         "$800 g (0.25)=1000 g h\\Rightarrow h=0.20\\,\\mathrm{m}$.",
         ["$0.25\\,\\mathrm{m}$", "$0.080\\,\\mathrm{m}$ from a shorter oil column", "$0.32\\,\\mathrm{m}$"]),
        ("AP Stretch: A tank open to air has a hole $3.2\\,\\mathrm{m}$ down. How far horizontally does the stream travel if the hole is $1.8\\,\\mathrm{m}$ above the ground? ($g=10$)",
         "$4.8\\,\\mathrm{m}$",
         "$v_x=\\sqrt{2g(3.2)}=8.0\\,\\mathrm{m/s}$. Fall $1.8=5 t^2$, $t^2=0.36$, $t=0.60\\,\\mathrm{s}$. Range $4.8\\,\\mathrm{m}$.",
         ["$8.0\\,\\mathrm{m}$", "$1.8\\,\\mathrm{m}$", "$3.2\\,\\mathrm{m}$"]),
        ("AP Stretch: A $5.0\\,\\mathrm{kg}$ cube $0.10\\,\\mathrm{m}$ on a side is held fully under water then released ($g=10$, $\\rho_w=1000$). Initial $a$, and the scale reading if it instead hung fully under, are",
         "$8.0\\,\\mathrm{m/s}^2$ down, $40\\,\\mathrm{N}$",
         "$V=0.0010\\,\\mathrm{m}^3$, $F_b=10\\,\\mathrm{N}$, $mg=50\\,\\mathrm{N}$. Net $40\\,\\mathrm{N}$ down so $a=8.0\\,\\mathrm{m/s}^2$. Scale reads $mg-F_b=40\\,\\mathrm{N}$.",
         ["$5.0\\,\\mathrm{m/s}^2$ down (the $2.0\\,\\mathrm{kg}$ cube copy)", "$8.0\\,\\mathrm{m/s}^2$ up", "$50\\,\\mathrm{N}$ on the scale"]),
        ("AP Stretch: Water ($\\rho=1000$) flows from a wide pipe at height $4.0\\,\\mathrm{m}$ with $v_1=2.0\\,\\mathrm{m/s}$ into a narrow pipe at height $1.0\\,\\mathrm{m}$ where $A_2=A_1/2$. Find $v_2$ and $P_2-P_1$ ($g=10$).",
         "$v_2=4.0\\,\\mathrm{m/s}$, $P_2-P_1=2.4\\times 10^4\\,\\mathrm{Pa}$",
         "Continuity: $v_2=4.0\\,\\mathrm{m/s}$. Bernoulli: $P_2=P_1+\\rho g(3.0)+\\tfrac12\\rho(4-16)=P_1+30000-6000$, so $P_2-P_1=2.4\\times 10^4\\,\\mathrm{Pa}$.",
         ["$v_2=2.0\\,\\mathrm{m/s}$, $\\Delta P=0$", "$\\tfrac32\\rho v^2$ with no height term", "$P_2<P_1$ by $3.0\\times 10^4\\,\\mathrm{Pa}$ ignoring speed"]),
        ("AP Stretch: A raft $5.0\\,\\mathrm{m}$ by $2.0\\,\\mathrm{m}$ sits $0.080\\,\\mathrm{m}$ deeper after cargo is loaded ($\\rho_w=1000$, $g=10$). Cargo mass is",
         "$8.0\\times 10^2\\,\\mathrm{kg}$",
         "$\\Delta V=5.0\\times 2.0\\times 0.080=0.80\\,\\mathrm{m}^3$. Extra $F_b=8.0\\times 10^3\\,\\mathrm{N}$, so $m=800\\,\\mathrm{kg}$.",
         ["$1.6\\times 10^3\\,\\mathrm{kg}$ from the $8\\times 4$ barge", "$80\\,\\mathrm{kg}$", "$8.0\\times 10^3\\,\\mathrm{kg}$ forgetting to divide by $g$"]),
        ("AP Stretch: A pontoon $6.0\\,\\mathrm{m}$ by $3.0\\,\\mathrm{m}$ must support extra $2700\\,\\mathrm{kg}$ of gear ($\\rho_w=1000$, $g=10$). Additional sink depth is",
         "$0.15\\,\\mathrm{m}$",
         "$mg=2.70\\times 10^4\\,\\mathrm{N}=\\rho g A\\Delta h=1.8\\times 10^5\\,\\Delta h$, so $\\Delta h=0.15\\,\\mathrm{m}$.",
         ["$0.050\\,\\mathrm{m}$", "$1.5\\,\\mathrm{m}$", "why the truck-mass was $1.6\\times 10^3\\,\\mathrm{kg}$"]),
        ("AP Stretch: An open elevator filled with a pool of water accelerates upward. At a given depth, gauge pressure compared with at rest is",
         "larger, because the effective $g$ is $g+a$ in $P=\\rho g_{\\mathrm{eff}} h$",
         "The fluid must provide a larger pressure gradient to accelerate with the elevator.",
         ["smaller", "unchanged", "zero"]),
        ("AP Stretch: Continuity plus a leak: if $10\\%$ of $Q$ leaks out before the exit, $A_{\\mathrm{exit}} v_{\\mathrm{exit}}$ equals",
         "$0.90$ of the upstream $Q$",
         "Mass/volume is not conserved through the leaky segment; you must reduce $Q$.",
         ["$1.10 Q$", "$Q$ still", "$0$"]),
        ("AP Stretch: A $3.0\\,\\mathrm{kg}$ metal cylinder ($V=0.0020\\,\\mathrm{m}^3$) hangs from a scale. Reading in air, then fully under water ($\\rho=1000$, $g=10$), are",
         "$30\\,\\mathrm{N}$ in air, $10\\,\\mathrm{N}$ in water",
         "$mg=30\\,\\mathrm{N}$. $F_b=20\\,\\mathrm{N}$. Apparent weight $mg-F_b=10\\,\\mathrm{N}$ on the scale under water.",
         ["$F_b$ depends only on the object's density", "$30\\,\\mathrm{N}$ both times", "$20\\,\\mathrm{N}$ in air"]),
    ])
    return qs


def build_unit8():
    title = "AP Physics Unit 8: Fluids"
    description = (
        "Density and pressure, Pascal hydraulics, buoyancy, continuity, Bernoulli, and FRQ habits for AP Physics 1 "
        "fluids — with pipe diagrams, not cells or circuits."
    )
    concepts = [
        "Density and pressure",
        "Pascal and hydraulic systems",
        "Buoyancy",
        "Continuity",
        "Bernoulli",
        "Fluid FRQ habits",
    ]

    c1 = concept_block(
        "1. Density and pressure",
        [
            "Density is how much mass is packed into a volume: $\\rho=m/V$, in $\\mathrm{kg/m}^3$. An $800\\,\\mathrm{kg}$ block "
            "of $0.40\\,\\mathrm{m}^3$ has $\\rho=2000\\,\\mathrm{kg/m}^3$. Fresh water is about $1000\\,\\mathrm{kg/m}^3$.",
            "Pressure is force per area, $P=F/A$, with the force perpendicular to the surface. The pascal is "
            "$1\\,\\mathrm{Pa}=1\\,\\mathrm{N/m}^2$. A $200\\,\\mathrm{N}$ push on $0.050\\,\\mathrm{m}^2$ is $4000\\,\\mathrm{Pa}$.",
            "In a static liquid, pressure grows with depth: the gauge pressure is $\\rho g h$. At $2.0\\,\\mathrm{m}$ in water "
            "with $g=10$, $\\rho g h=20000\\,\\mathrm{Pa}$ above the surface pressure.",
            "Absolute pressure adds the surface pressure: $P=P_0+\\rho g h$. If $P_0=1.0\\times 10^5\\,\\mathrm{Pa}$ and "
            "$\\rho g h=2.0\\times 10^4\\,\\mathrm{Pa}$, then $P=1.2\\times 10^5\\,\\mathrm{Pa}$.",
            "At a given depth, pressure does not pick a favorite direction. A dam feels huge sideways force at the bottom "
            "because $P$ is large there, not because water “only pushes down.”",
            "A wide lake and a thin tube of the same liquid have the same $P$ at the same $h$. Volume of the lake does "
            "not add extra pressure. That trap shows up every year.",
        ],
        "Buoyancy is nothing but pressure being larger on the bottom face than on the top face. If $\\rho g h$ is shaky, "
        "Archimedes will feel like a slogan.",
        "Write $\\rho=m/V$ and $P=F/A$ with units. For depth, write $P_{\\mathrm{gauge}}=\\rho g h$ and add $P_0$ only if asked for absolute pressure.",
        lesson_figure(
            _tank_svg(),
            "Pressure in a static tank grows with depth $h$",
            "$P=P_0+\\rho g h$ at the marked point. Same $h$ in a skinny tube would match this $P$.",
        )
        + solved(1, "An $800\\,\\mathrm{kg}$ sample occupies $0.40\\,\\mathrm{m}^3$. Find $\\rho$.",
                 ["$\\rho=m/V=800/0.40=2000\\,\\mathrm{kg/m}^3$.",
                  "That is twice the density of water.",
                  "It would sink if placed in a freshwater pond."],
                 "$2.0\\times 10^3\\,\\mathrm{kg/m}^3$", "", "Easy")
        + solved(2, "Find gauge pressure $2.0\\,\\mathrm{m}$ under freshwater ($\\rho=1000$, $g=10$).",
                 ["$P_{\\mathrm{gauge}}=\\rho g h=1000(10)(2)=2.0\\times 10^4\\,\\mathrm{Pa}$.",
                  "If $P_0=1.0\\times 10^5\\,\\mathrm{Pa}$, absolute $P=1.2\\times 10^5\\,\\mathrm{Pa}$.",
                  "Force on a $0.50\\,\\mathrm{m}^2$ horizontal lid at that depth from gauge pressure: $F=1.0\\times 10^4\\,\\mathrm{N}$."],
                 "$2.0\\times 10^4\\,\\mathrm{Pa}$ gauge", "", "Medium")
        + solved(3, "Compare pressure $4.0\\,\\mathrm{m}$ down in a pool versus $4.0\\,\\mathrm{m}$ down in a thin water-filled tube standing beside it.",
                 ["Both have the same $h$ and same $\\rho$.",
                  "$P_{\\mathrm{gauge}}=\\rho g h$ is therefore the same.",
                  "The pool's extra water to the sides does not pile extra pressure at that depth.",
                  "Dams care about depth, not about “how much lake is behind you” at the same $h$."],
                 "equal pressures at equal depths", "", "Hard"),
        ("Thinking a bigger lake means bigger pressure at the same depth",
         "Pressure is $\\rho g h$ plus $P_0$, not “total weight of the lake divided by the dam.” Two different $h$ values, not two different lake sizes, change $P$."),
        ("Label gauge versus absolute before adding $1.0\\times 10^5\\,\\mathrm{Pa}$",
         "Many AP numbers already are gauge. Adding atmosphere twice is a $10^5\\,\\mathrm{Pa}$ error."),
        [
            "I can compute $\\rho=m/V$ and $P=F/A$ with SI units.",
            "I can compute $P_{\\mathrm{gauge}}=\\rho g h$ using $g=10$.",
            "I can explain why pressure at a depth does not depend on the lake's width.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Pascal's principle and hydraulic systems",
        [
            "Pascal's principle: if you raise the pressure of a confined incompressible fluid, that increase shows up "
            "everywhere in the fluid. A squeeze at a small piston becomes a squeeze at a large piston.",
            "Hydraulics use $F_1/A_1=F_2/A_2$ because the pressure is the same. $F_1=40\\,\\mathrm{N}$ on $A_1=0.010\\,\\mathrm{m}^2$ "
            "gives $P=4000\\,\\mathrm{Pa}$, so on $A_2=0.20\\,\\mathrm{m}^2$ you get $F_2=800\\,\\mathrm{N}$.",
            "Volume of liquid is conserved: $A_1 d_1=A_2 d_2$. The large piston moves less. If $A_2=20 A_1$ and $d_1=0.10\\,\\mathrm{m}$, "
            "then $d_2=0.0050\\,\\mathrm{m}$. Ideal work $F_1 d_1=F_2 d_2$.",
            "A hydraulic jack is a lever made of liquid. Small force, long travel in; large force, short travel out. "
            "You do not get free energy.",
            "If the fluid leaks or contains big bubbles, the confined-incompressible assumption fails and the lift sags. "
            "Pascal is not magic; it is a closed-system pressure statement.",
            "A barber-chair cylinder with $A=0.012\\,\\mathrm{m}^2$ holding $720\\,\\mathrm{N}$ needs $P=6.0\\times 10^4\\,\\mathrm{Pa}$ in the fluid "
            "(plus whatever extra the pump adds).",
        ],
        "Bernoulli will add speed. Pascal is the static, confined-fluid tool. Using Bernoulli on a resting hydraulic "
        "jack is the wrong law.",
        "Write $P=F/A$ on both pistons and set the pressures equal. Then use $A d$ matching for distances.",
        lesson_figure(
            _pistons_svg(),
            "Hydraulic pistons sharing one fluid pressure",
            "Small $F_1$ on small $A_1$ makes the same $P$ as large $F_2$ on large $A_2$. Distances trade the other way.",
        )
        + solved(4, "$F_1=40\\,\\mathrm{N}$, $A_1=0.010\\,\\mathrm{m}^2$, $A_2=0.20\\,\\mathrm{m}^2$. Find $F_2$.",
                 ["$P=F_1/A_1=4000\\,\\mathrm{Pa}$.",
                  "$F_2=P A_2=800\\,\\mathrm{N}$.",
                  "Force ratio equals area ratio $20$."],
                 "$800\\,\\mathrm{N}$", "", "Easy")
        + solved(5, "If the small piston in that jack moves $0.10\\,\\mathrm{m}$, how far does the large piston move?",
                 ["$A_1 d_1=A_2 d_2$.",
                  "$d_2=(0.010/0.20)(0.10)=0.0050\\,\\mathrm{m}$.",
                  "Check work: $40(0.10)=4.0\\,\\mathrm{J}$ and $800(0.0050)=4.0\\,\\mathrm{J}$."],
                 "$0.0050\\,\\mathrm{m}$", "", "Medium")
        + solved(6, "A chair cylinder $A=0.012\\,\\mathrm{m}^2$ must support $720\\,\\mathrm{N}$. Find the required fluid pressure, then the small-piston force if $A_1=3.0\\times 10^{-4}\\,\\mathrm{m}^2$.",
                 ["$P=720/0.012=6.0\\times 10^4\\,\\mathrm{Pa}$.",
                  "$F_1=P A_1=(6.0\\times 10^4)(3.0\\times 10^{-4})=18\\,\\mathrm{N}$.",
                  "A modest push holds a person because of the area ratio $40$.",
                  "The person still rises only a short distance for a long pump stroke."],
                 "$P=6.0\\times 10^4\\,\\mathrm{Pa}$, $F_1=18\\,\\mathrm{N}$", "", "Hard"),
        ("Expecting $F_2=F_1$ because “pressure is the same”",
         "Pressure is the same; force is pressure times area. Different areas, different forces."),
        ("Match $F d$ on both sides as a check",
         "If the works disagree in an ideal (no leak, incompressible) jack, an area or a distance is wrong."),
        [
            "I can apply $F_1/A_1=F_2/A_2$ to a hydraulic lift.",
            "I can use $A_1 d_1=A_2 d_2$ for piston travel.",
            "I can check ideal work in equals work out.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Buoyancy",
        [
            "Buoyant force is the leftover upward push because pressure is larger on the bottom of a submerged object "
            "than on the top. Archimedes' statement: $F_b$ equals the weight of the displaced fluid, $F_b=\\rho_f V_{\\mathrm{disp}} g$.",
            "Water, $V=0.0020\\,\\mathrm{m}^3$, $g=10$: $F_b=20\\,\\mathrm{N}$. That number does not care what the object is made of — "
            "only how much fluid it shoved aside.",
            "Floating: $F_b=mg$. The object sinks in until the displaced weight matches its own weight. "
            "A $15\\,\\mathrm{N}$ toy displaces $15\\,\\mathrm{N}$ of water. Fraction submerged is $\\rho_{\\mathrm{obj}}/\\rho_f$ if $\\rho_{\\mathrm{obj}}<\\rho_f$.",
            "Sinking: the object is fully under and $F_b=\\rho_f V_{\\mathrm{obj}} g < mg$. Apparent weight on a spring scale is "
            "$mg-F_b$. A $50\\,\\mathrm{N}$ rock displacing $20\\,\\mathrm{N}$ of water reads $30\\,\\mathrm{N}$ in water.",
            "A boat sits lower when you board because it must displace more water. A helium balloon rises because "
            "displaced air weighs more than the balloon.",
            "Free-body diagram: $F_g$ down, $F_b$ up, maybe a tension or scale force. Then $F_{\\mathrm{net}}=ma$ if it is accelerating "
            "at the moment of release.",
        ],
        "Continuity and Bernoulli are about moving fluids. Buoyancy is often a static FBD. Keep the tools in separate drawers "
        "until a problem mixes them (a floating pipe with flow is rare on AP 1).",
        "Compute $V_{\\mathrm{disp}}$, then $F_b=\\rho_f V g$. Compare with $mg$ to decide float, sink, or hover.",
        lesson_figure(
            _buoyancy_fbd(),
            "Object in a fluid: weight down, buoyancy up, scale tension vertical",
            "If $F_b=mg$ it can float or hover. If $F_b<mg$ and fully under, it sinks. A scale reads $mg-F_b$.",
        )
        + solved(7, "Find $F_b$ on $0.0020\\,\\mathrm{m}^3$ of displaced freshwater ($g=10$).",
                 ["$F_b=\\rho V g=1000(0.0020)(10)=20\\,\\mathrm{N}$ up.",
                  "Object identity did not enter.",
                  "If the object weighs $15\\,\\mathrm{N}$, it cannot be fully under while floating — only part of $V$ is displaced."],
                 "$20\\,\\mathrm{N}$ up", "", "Easy")
        + solved(8, "A $4.0\\,\\mathrm{N}$ wood block floats with $75\\%$ submerged. Find $\\rho_{\\mathrm{wood}}/\\rho_w$.",
                 ["Floating: $F_b=4.0\\,\\mathrm{N}=\\rho_w (0.75 V) g$.",
                  "Also $mg=\\rho_{\\mathrm{wood}} V g=4.0\\,\\mathrm{N}$.",
                  "Divide: $\\rho_{\\mathrm{wood}}/\\rho_w=0.75$."],
                 "$0.75$", "", "Medium")
        + solved(9, "A $2.0\\,\\mathrm{kg}$ cube $0.10\\,\\mathrm{m}$ on a side is held fully under water and released ($g=10$, $\\rho_w=1000$). Find initial $a$.",
                 ["$V=0.0010\\,\\mathrm{m}^3$, $F_b=10\\,\\mathrm{N}$, $mg=20\\,\\mathrm{N}$.",
                  "The cube is denser than water ($\\rho=2000$). Net force $10\\,\\mathrm{N}$ down.",
                  "$a=10/2.0=5.0\\,\\mathrm{m/s}^2$ down.",
                  "Apparent weight would be $10\\,\\mathrm{N}$ if you hung it from a scale while fully under."],
                 "$5.0\\,\\mathrm{m/s}^2$ down", "", "Hard"),
        ("Using the object's density inside $F_b=\\rho_{\\mathrm{obj}} V g$",
         "Buoyancy uses the fluid's density and the displaced volume. Object density decides $mg$ and whether it floats."),
        ("Draw $F_b$ and $mg$ before talking about floating fractions",
         "The comparison $F_b$ versus $mg$ is the whole decision tree. The fraction $V_{\\mathrm{sub}}/V$ comes after you know it floats."),
        [
            "I can compute $F_b=\\rho_f V_{\\mathrm{disp}} g$.",
            "I can use $F_b=mg$ for floating and find the submerged fraction.",
            "I can find apparent weight $mg-F_b$ for a fully submerged sinker.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Continuity",
        [
            "For a liquid you can treat as incompressible, the volume per second through a pipe is the same at every "
            "cross-section if there are no leaks: $A_1 v_1=A_2 v_2$. That product $Q=Av$ is the volume flow rate.",
            "If $A_1=0.040\\,\\mathrm{m}^2$, $v_1=2.0\\,\\mathrm{m/s}$, and $A_2=0.010\\,\\mathrm{m}^2$, then $v_2=8.0\\,\\mathrm{m/s}$. "
            "Narrower pipe, faster flow. A river gorge is the same idea.",
            "A hose with $A=4.0\\times 10^{-4}\\,\\mathrm{m}^2$ at $5.0\\,\\mathrm{m/s}$ delivers $Q=2.0\\times 10^{-3}\\,\\mathrm{m}^3/\\mathrm{s}$. "
            "Mass per second is $\\rho Q=2.0\\,\\mathrm{kg/s}$ for water.",
            "Put your thumb over a hose outlet: $A$ drops, $v$ rises, the water travels farther (more speed, same $Q$ "
            "if the tap setting is unchanged).",
            "If $10\\%$ leaks out, the downstream $Q$ is only $90\\%$ of the upstream $Q$. Continuity is not a slogan; "
            "it is bookkeeping of volume.",
            "Continuity gives speeds. Bernoulli (next) turns those speeds into pressure changes. Most pipe FRQs need both.",
        ],
        "Bernoulli without continuity is an equation with too many unknowns. Continuity supplies the missing speed.",
        "Compute $Q=A v$ on the side you know. Set $Q$ equal on the other side (unless there is a leak). Solve for the unknown $v$ or $A$.",
        lesson_figure(
            _pipe_svg(),
            "Incompressible flow: narrow section is faster",
            "$A_1 v_1=A_2 v_2$. The wide region is slow; the constriction is fast. Pressure will follow in Bernoulli.",
        )
        + solved(10, "$A_1=0.040\\,\\mathrm{m}^2$, $v_1=2.0\\,\\mathrm{m/s}$, $A_2=0.010\\,\\mathrm{m}^2$. Find $v_2$.",
                 ["$Q=A_1 v_1=0.080\\,\\mathrm{m}^3/\\mathrm{s}$.",
                  "$v_2=Q/A_2=8.0\\,\\mathrm{m/s}$.",
                  "Speed $\\times 4$ because area $\\div 4$."],
                 "$8.0\\,\\mathrm{m/s}$", "", "Easy")
        + solved(11, "A hose $A=4.0\\times 10^{-4}\\,\\mathrm{m}^2$ at $5.0\\,\\mathrm{m/s}$. Find $Q$ and the mass flow of water.",
                 ["$Q=2.0\\times 10^{-3}\\,\\mathrm{m}^3/\\mathrm{s}$.",
                  "$\\dot m=\\rho Q=2.0\\,\\mathrm{kg/s}$.",
                  "In one minute that is $120\\,\\mathrm{kg}$ of water."],
                 "$Q=2.0\\times 10^{-3}\\,\\mathrm{m}^3/\\mathrm{s}$, $\\dot m=2.0\\,\\mathrm{kg/s}$", "", "Medium")
        + solved(12, "Wide area $12\\,\\mathrm{cm}^2$ at $1.5\\,\\mathrm{m/s}$ narrows to $4.0\\,\\mathrm{cm}^2$. Find $v_{\\mathrm{narrow}}$. Then, if $10\\%$ leaks before the exit, find the new exit speed for that same $4.0\\,\\mathrm{cm}^2$.",
                 ["No leak: $12(1.5)=4.0 v\\Rightarrow v=4.5\\,\\mathrm{m/s}$.",
                  "With a $10\\%$ leak, $Q_{\\mathrm{exit}}=0.90 Q_1$, so $v_{\\mathrm{exit}}=0.90\\times 4.5=4.05\\,\\mathrm{m/s}$.",
                  "Leaks reduce $Q$, so they reduce the exit speed compared with the sealed-pipe prediction.",
                  "Keep $A$ in consistent units; $\\mathrm{cm}^2$ ratios cancel if both areas use $\\mathrm{cm}^2$."],
                 "$4.5\\,\\mathrm{m/s}$ sealed; $4.05\\,\\mathrm{m/s}$ with a $10\\%$ leak", "", "Hard"),
        ("Thinking speed is the same throughout a pipe of changing $A$",
         "That would pile liquid up or require a vacuum. Incompressible steady flow must speed up in the narrow part."),
        ("Compute $Q$ first, then divide by the other $A$",
         "One number, $Q$, travels down the pipe. Speeds are $Q/A$ at each station."),
        [
            "I can use $A_1 v_1=A_2 v_2$ for incompressible flow.",
            "I can compute $Q=Av$ and $\\dot m=\\rho Q$.",
            "I can adjust $Q$ when a leak removes volume.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Bernoulli's equation",
        [
            "Bernoulli's equation for ideal, steady, incompressible flow along a streamline is "
            "$P+\\rho g h+\\tfrac12\\rho v^2=\\mathrm{constant}$. It is mechanical energy per volume: pressure work, gravitational energy, kinetic energy.",
            "If the pipe is horizontal, $h$ drops out and a speed-up requires a pressure drop: "
            "$P_1-P_2=\\tfrac12\\rho(v_2^2-v_1^2)$. With $v_1=2.0$, $v_2=8.0$, $\\rho=1000$, the drop is $3.0\\times 10^4\\,\\mathrm{Pa}$.",
            "That is why a venturi throat has low pressure, why a storm can lift a roof (fast air, low $P$), and why "
            "a qualitative airplane-wing story talks about faster air and lower pressure.",
            "Torricelli's result: a hole a depth $h$ below a large open surface behaves like falling from rest through $h$: "
            "$v=\\sqrt{2gh}$. For $h=5.0\\,\\mathrm{m}$ and $g=10$, $v=10\\,\\mathrm{m/s}$. Then treat the jet as a horizontal projectile.",
            "Real pipes have viscosity. Then $P+\\rho g h+\\tfrac12\\rho v^2$ is not perfectly constant; you need extra pressure "
            "to fight drag. AP 1 mostly uses the ideal equation plus a sentence about losses.",
            "Never apply Bernoulli between two points that are not on the same flowing streamline, and do not use it "
            "as a replacement for $P=\\rho g h$ in a static tank (static is $v=0$, which is a legal but boring Bernoulli).",
        ],
        "The last concept is how to write this on an FRQ without mixing in Gauss's law or circuits. The physics is here; "
        "the habits are next.",
        "Get $v$ from continuity. Then write Bernoulli between two labeled points. Cancel terms that are equal (same $h$, or $P=P_0$ at two open surfaces).",
        lesson_figure(
            _pipe_svg(),
            "Horizontal constriction: faster flow, lower pressure",
            "Continuity raises $v$ in the throat. Bernoulli then lowers $P$. That pair is the venturi.",
        )
        + solved(13, "Horizontal pipe, $v_1=2.0\\,\\mathrm{m/s}$, $v_2=8.0\\,\\mathrm{m/s}$, $\\rho=1000$. Find $P_1-P_2$.",
                 ["$h_1=h_2$, so $P_1+\\tfrac12\\rho v_1^2=P_2+\\tfrac12\\rho v_2^2$.",
                  "$P_1-P_2=\\tfrac12(1000)(64-4)=500\\times 60=3.0\\times 10^4\\,\\mathrm{Pa}$.",
                  "Pressure is lower in the fast section."],
                 "$3.0\\times 10^4\\,\\mathrm{Pa}$", "", "Easy")
        + solved(14, "A tank open to air has a hole $5.0\\,\\mathrm{m}$ below the surface. Find exit speed ($g=10$).",
                 ["Large surface: $v_{\\mathrm{top}}\\approx 0$, $P=P_0$ at top and at the free jet.",
                  "$\\rho g h=\\tfrac12\\rho v^2\\Rightarrow v=\\sqrt{2gh}=\\sqrt{100}=10\\,\\mathrm{m/s}$.",
                  "Same number as dropping from rest through $5.0\\,\\mathrm{m}$."],
                 "$10\\,\\mathrm{m/s}$", "", "Medium")
        + solved(15, "That hole is $1.8\\,\\mathrm{m}$ above the ground, but the water surface is $3.2\\,\\mathrm{m}$ above the hole. Find the horizontal range of the stream ($g=10$).",
                 ["$v_x=\\sqrt{2g(3.2)}=\\sqrt{64}=8.0\\,\\mathrm{m/s}$.",
                  "Fall $1.8=\\tfrac12(10)t^2=5t^2$, so $t^2=0.36$, $t=0.60\\,\\mathrm{s}$.",
                  "Range $x=v_x t=4.8\\,\\mathrm{m}$.",
                  "Continuity was not needed because the tank surface is wide ($v_{\\mathrm{top}}\\approx 0$)."],
                 "$4.8\\,\\mathrm{m}$", "", "Hard"),
        ("Using Bernoulli without first finding the second speed",
         "If $A$ changes, continuity is the other equation. Leaving $v_2$ as a mystery makes $P_2$ a mystery."),
        ("Cancel $P_0$ at two open surfaces, then cancel $\\rho$",
         "Torricelli pops out. If one surface is closed and pressurized, keep that extra $P$."),
        [
            "I can write $P+\\rho g h+\\tfrac12\\rho v^2$ as a constant along a streamline.",
            "I can find a horizontal venturi pressure drop from two speeds.",
            "I can use $v=\\sqrt{2gh}$ at a tank hole and then projectile range.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Fluid FRQ habits",
        [
            "A fluids free-response on AP Physics 1 is mostly a diagram plus a named law. Draw the pipe or tank, "
            "label $A$, $v$, $P$, $h$, and $\\rho$. Then write the name: continuity, Bernoulli, $P=\\rho g h$, Pascal, or Archimedes.",
            "Changing area almost always means continuity first, Bernoulli second. Floating almost always means $F_b=mg$ "
            "and $V_{\\mathrm{sub}}/V=\\rho_{\\mathrm{obj}}/\\rho_f$. Depth almost always means $\\rho g h$.",
            "Manometers: a liquid height difference $\\Delta h$ means $\\Delta P=\\rho g\\Delta h$ between the two sides. "
            "Connect those two sides to the tanks the problem actually drew.",
            "Units: $\\tfrac12\\rho v^2$ is a pressure. If your Bernoulli terms do not all have units of pascals, a $\\rho$ or a $g$ is missing.",
            "System sentences still matter: “incompressible, no leak, steady flow” justifies continuity. "
            "“Ideal, no viscosity, along a streamline” justifies Bernoulli. “Confined fluid” justifies Pascal.",
            "Stay in AP Physics 1: no Gauss's law, no electric-field maps, no circuit diagrams for these items. "
            "A pipe that changes area is the right picture, not a cell and not a series circuit.",
        ],
        "This is the last unit of AP Physics 1. The habit of naming the law, drawing the figure, and checking units "
        "is the same habit as Unit 1 kinematics — only the symbols changed.",
        "Sketch, name the law, substitute, check pascals and $\\mathrm{m/s}$. If an area changed and you never used $Av$, look again.",
        lesson_figure(
            _pipe_height_svg(),
            "FRQ figure: label both stations, including height, before writing equations",
            "Station 1: $A_1,v_1,P_1,h_1$. Station 2: $A_2,v_2,P_2,h_2$. Continuity then Bernoulli.",
        )
        + solved(16, "A pipe changes area. You are asked for $\\Delta P$ on the horizontal. Which two equations, in order?",
                 ["Continuity: $A_1 v_1=A_2 v_2$ to get the unknown speed.",
                  "Bernoulli with $h_1=h_2$: $P_1-P_2=\\tfrac12\\rho(v_2^2-v_1^2)$.",
                  "Skip Pascal; the fluid is moving."],
                 "continuity, then Bernoulli", "", "Easy")
        + solved(17, "A U-tube has $0.10\\,\\mathrm{m}$ of oil ($\\rho=800$) balancing extra water height $h$. Find $h$.",
                 ["Equal pressures at the oil-water matching level.",
                  "$800(10)(0.10)=1000(10)h$.",
                  "$h=0.080\\,\\mathrm{m}$ of water."],
                 "$0.080\\,\\mathrm{m}$", "", "Medium")
        + solved(18, "A barge $8.0\\,\\mathrm{m}$ by $4.0\\,\\mathrm{m}$ sinks $0.050\\,\\mathrm{m}$ deeper when a truck boards. Find the truck's mass ($\\rho_w=1000$, $g=10$). Name the law.",
                 ["Archimedes: extra $F_b$ equals extra weight.",
                  "$\\Delta V=8.0(4.0)(0.050)=1.6\\,\\mathrm{m}^3$.",
                  "$F_b=\\rho g\\Delta V=1.6\\times 10^4\\,\\mathrm{N}$.",
                  "$m=F_b/g=1.6\\times 10^3\\,\\mathrm{kg}$."],
                 "$1.6\\times 10^3\\,\\mathrm{kg}$ (Archimedes)", "", "Hard"),
        ("Starting algebra before naming the fluid law",
         "Wrong law, pretty numbers, zero method points. Write “continuity” or “Bernoulli” or “Archimedes” as a heading."),
        ("Label two stations on the figure with subscripts 1 and 2",
         "Then every symbol in Bernoulli has a home. Unlabeled pipes produce mixed $v$ from the wrong place."),
        [
            "I can choose continuity, Bernoulli, $\\rho g h$, Pascal, or Archimedes from a prompt.",
            "I can use a manometer height as $\\Delta P=\\rho g\\Delta h$.",
            "I can check that Bernoulli terms all have pressure units.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Kinematics', ['Position velocity acceleration', 'Constant acceleration equations', 'Graphs of motion', 'Free fall', 'Projectile motion', 'Relative motion']), ('Force and Translational Dynamics', ['Newton 1 and inertia', 'Newton 2 and net force', 'Newton 3 pairs', 'Friction and drag', 'Inclined planes', 'Systems and connected objects']), ('Work, Energy, and Power', ['Work by a constant force', 'Work-energy theorem', 'Gravitational potential energy', 'Conservation of energy', 'Power', 'Springs and elastic energy']), ('Linear Momentum', ['Momentum and impulse', 'Conservation of momentum', 'Elastic collisions', 'Inelastic collisions', 'Center of mass', 'Explosions']), ('Torque and Rotational Dynamics', ['Angular displacement and velocity', 'Torque', 'Rotational inertia', 'Newton 2 for rotation', 'Rolling without slipping', 'Static equilibrium']), ('Energy and Momentum of Rotating Systems', ['Rotational kinetic energy', 'Angular momentum', 'Conservation of L', 'Collisions with rotation', 'Atwood and pulleys with rotation', 'Justifying with systems']), ('Oscillations', ['Restoring force and SHM', 'Period of a spring', 'Period of a pendulum', 'Energy in SHM', 'Graphs of SHM', 'Damping qualitative']), ('Fluids', ['Density and pressure', 'Pascal and hydraulic systems', 'Buoyancy', 'Continuity', 'Bernoulli', 'Fluid FRQ habits'])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>AP Physics Complete</h1>"
        f"<p><strong>For:</strong> <strong>AP Physics 1</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
