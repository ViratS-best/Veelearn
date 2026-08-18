"""AP Physics C: Mechanics units 5–8 (rotation through gravitation)."""
from __future__ import annotations

import math

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, page_break, mq,
    xy_graph, sample_curve,
    fbd_box, energy_bars_svg, spring_mass_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _ican(items):
    return (
        "<p><strong>I can:</strong></p><ul>"
        + "".join(f"<li>{x}</li>" for x in items)
        + "</ul>"
    )


def _add(qs, rows):
    for text, ans, expl, dist in rows:
        qs.append(mq(text, ans, expl, len(qs) + 1, distractors=dist))
    return qs


def _orbit_svg():
    return (
        '<svg viewBox="0 0 280 220" width="100%" style="max-width:280px" role="img">'
        '<circle cx="140" cy="110" r="72" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="6 4"/>'
        '<circle cx="140" cy="110" r="20" fill="#fbbf24" stroke="#b45309" stroke-width="2"/>'
        '<text x="140" y="114" text-anchor="middle" font-size="11">star</text>'
        '<circle cx="212" cy="110" r="11" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="224" y="104" font-size="11">planet</text>'
        "</svg>"
    )


def _pendulum_svg():
    return (
        '<svg viewBox="0 0 240 200" width="100%" style="max-width:240px" role="img">'
        '<line x1="20" y1="20" x2="220" y2="20" stroke="#334155" stroke-width="6"/>'
        '<line x1="120" y1="20" x2="170" y2="150" stroke="#0f172a" stroke-width="2"/>'
        '<circle cx="170" cy="150" r="14" fill="#c7d2fe" stroke="#312e81"/>'
        '<text x="178" y="154" font-size="11">m</text>'
        '<text x="128" y="90" font-size="11">L</text>'
        '<text x="150" y="50" font-size="11">θ</text>'
        "</svg>"
    )


def _torque_svg():
    return (
        '<svg viewBox="0 0 280 160" width="100%" style="max-width:280px" role="img">'
        '<circle cx="50" cy="80" r="8" fill="#64748b"/>'
        '<line x1="50" y1="80" x2="210" y2="80" stroke="#1e3a8a" stroke-width="6"/>'
        '<line x1="210" y1="80" x2="210" y2="30" stroke="#b91c1c" stroke-width="3"/>'
        '<polygon points="205,32 210,18 215,32" fill="#b91c1c"/>'
        '<text x="218" y="50" font-size="12">F</text>'
        '<text x="110" y="70" font-size="12">r</text>'
        '<text x="40" y="110" font-size="11">pivot</text>'
        "</svg>"
    )


def _wheel_svg():
    return (
        '<svg viewBox="0 0 240 160" width="100%" style="max-width:240px" role="img">'
        '<line x1="20" y1="130" x2="220" y2="130" stroke="#334155" stroke-width="3"/>'
        '<circle cx="120" cy="90" r="40" fill="#e0e7ff" stroke="#312e81" stroke-width="3"/>'
        '<circle cx="120" cy="90" r="6" fill="#312e81"/>'
        '<line x1="120" y1="90" x2="150" y2="70" stroke="#b91c1c" stroke-width="2"/>'
        '<text x="154" y="68" font-size="11">ω</text>'
        '<text x="160" y="120" font-size="11">v=ωR</text>'
        "</svg>"
    )


def _pulley_mass_svg():
    return (
        '<svg viewBox="0 0 260 200" width="100%" style="max-width:260px" role="img">'
        '<circle cx="130" cy="48" r="28" fill="#cbd5e1" stroke="#334155" stroke-width="4"/>'
        '<text x="118" y="52" font-size="11">I</text>'
        '<line x1="102" y1="48" x2="102" y2="145" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="158" y1="48" x2="158" y2="112" stroke="#0f172a" stroke-width="2"/>'
        '<rect x="84" y="145" width="36" height="30" fill="#c7d2fe" stroke="#312e81"/>'
        '<rect x="140" y="112" width="36" height="30" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="90" y="165" font-size="11">m1</text>'
        '<text x="144" y="132" font-size="11">m2</text>'
        "</svg>"
    )


def _inertia_svg():
    return (
        '<svg viewBox="0 0 320 180" width="100%" style="max-width:320px" role="img">'
        '<circle cx="80" cy="90" r="50" fill="none" stroke="#312e81" stroke-width="8"/>'
        '<circle cx="80" cy="90" r="5" fill="#312e81"/>'
        '<circle cx="80" cy="40" r="6" fill="#b91c1c"/>'
        '<circle cx="130" cy="90" r="6" fill="#b91c1c"/>'
        '<circle cx="80" cy="140" r="6" fill="#b91c1c"/>'
        '<circle cx="30" cy="90" r="6" fill="#b91c1c"/>'
        '<text x="80" y="175" text-anchor="middle" font-size="12">hoop: all dm at R</text>'
        '<circle cx="230" cy="90" r="50" fill="#c7d2fe" stroke="#312e81" stroke-width="3"/>'
        '<circle cx="230" cy="90" r="32" fill="none" stroke="#6366f1" stroke-dasharray="4 3"/>'
        '<circle cx="230" cy="90" r="16" fill="none" stroke="#6366f1" stroke-dasharray="4 3"/>'
        '<circle cx="230" cy="90" r="5" fill="#312e81"/>'
        '<text x="230" y="175" text-anchor="middle" font-size="12">disk: ∫ r² dm</text>'
        "</svg>"
    )


def _rp_svg():
    return (
        '<svg viewBox="0 0 280 200" width="100%" style="max-width:280px" role="img">'
        '<circle cx="40" cy="160" r="5" fill="#334155"/>'
        '<text x="28" y="178" font-size="12">O</text>'
        '<line x1="40" y1="160" x2="190" y2="70" stroke="#1d4ed8" stroke-width="3"/>'
        '<polygon points="186,78 198,64 178,66" fill="#1d4ed8"/>'
        '<text x="100" y="100" font-size="13">r</text>'
        '<circle cx="190" cy="70" r="10" fill="#c7d2fe" stroke="#312e81"/>'
        '<text x="204" y="64" font-size="12">m</text>'
        '<line x1="190" y1="70" x2="250" y2="70" stroke="#b91c1c" stroke-width="3"/>'
        '<polygon points="242,64 258,70 242,76" fill="#b91c1c"/>'
        '<text x="220" y="60" font-size="13">p</text>'
        '<text x="70" y="30" font-size="12">L = r × p</text>'
        "</svg>"
    )


def _skater_svg():
    return (
        '<svg viewBox="0 0 240 220" width="100%" style="max-width:240px" role="img">'
        '<line x1="120" y1="30" x2="120" y2="170" stroke="#64748b" stroke-width="4"/>'
        '<circle cx="120" cy="190" r="18" fill="#cbd5e1" stroke="#334155"/>'
        '<text x="148" y="195" font-size="11">stool</text>'
        '<circle cx="120" cy="70" r="14" fill="#e2e8f0" stroke="#0f172a"/>'
        '<line x1="120" y1="84" x2="120" y2="140" stroke="#0f172a" stroke-width="3"/>'
        '<line x1="108" y1="100" x2="100" y2="128" stroke="#0f172a" stroke-width="3"/>'
        '<line x1="132" y1="100" x2="140" y2="128" stroke="#0f172a" stroke-width="3"/>'
        '<text x="20" y="50" font-size="12">arms in</text>'
        '<text x="168" y="60" font-size="12">I ↓</text>'
        '<text x="168" y="80" font-size="12">ω ↑</text>'
        '<path d="M150 40 A40 40 0 0 1 150 100" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        "</svg>"
    )


def _gyro_svg():
    return (
        '<svg viewBox="0 0 300 200" width="100%" style="max-width:300px" role="img">'
        '<polygon points="50,160 70,160 60,140" fill="#334155"/>'
        '<line x1="60" y1="140" x2="230" y2="140" stroke="#1e3a8a" stroke-width="5"/>'
        '<ellipse cx="200" cy="140" rx="14" ry="40" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>'
        '<line x1="200" y1="140" x2="270" y2="140" stroke="#059669" stroke-width="3"/>'
        '<polygon points="262,134 278,140 262,146" fill="#059669"/>'
        '<text x="248" y="128" font-size="12">L</text>'
        '<line x1="200" y1="140" x2="200" y2="185" stroke="#b91c1c" stroke-width="2"/>'
        '<polygon points="194,178 200,190 206,178" fill="#b91c1c"/>'
        '<text x="208" y="180" font-size="12">mg</text>'
        '<text x="110" y="128" font-size="12">r</text>'
        '<text x="72" y="70" font-size="12">τ = r × mg</text>'
        '<path d="M90 100 A50 22 0 0 1 40 140" fill="none" stroke="#7c3aed" stroke-width="2"/>'
        '<text x="20" y="90" font-size="12">Ω</text>'
        '<text x="40" y="185" font-size="11">pivot</text>'
        "</svg>"
    )


def _coaxial_svg():
    return (
        '<svg viewBox="0 0 260 200" width="100%" style="max-width:260px" role="img">'
        '<line x1="130" y1="20" x2="130" y2="180" stroke="#64748b" stroke-width="4"/>'
        '<ellipse cx="130" cy="70" rx="70" ry="16" fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>'
        '<text x="175" y="62" font-size="12">I1, ω</text>'
        '<ellipse cx="130" cy="120" rx="52" ry="12" fill="#fecaca" stroke="#991b1b" stroke-width="2"/>'
        '<text x="175" y="128" font-size="12">I2 at rest</text>'
        '<text x="20" y="50" font-size="11">same axle</text>'
        '<polygon points="124,95 136,95 130,110" fill="#b91c1c"/>'
        "</svg>"
    )


# ===========================================================================
# UNIT 5: Rotation I
# ===========================================================================

def _u5_questions():
    qs = []
    _add(qs, [
        ("Angular velocity is $\\omega=d\\theta/dt$. If $\\theta=3t^2$ (radians), $\\omega$ at $t=2\\,\\mathrm{s}$ is",
         "12 rad/s", "$\\omega=6t$. At $t=2$, $\\omega=12\\,\\mathrm{rad/s}$.",
         ["6 rad/s", "3 rad/s", "24 rad/s"]),
        ("Angular acceleration $\\alpha=d\\omega/dt$. For $\\omega=6t$, $\\alpha$ is",
         "6 rad/s^2", "Derivative of $6t$ is the constant $6$.",
         ["6t", "3t^2", "0"]),
        ("If $\\omega=4t$ and $\\theta(0)=0$, then $\\theta$ at $t=2\\,\\mathrm{s}$ is",
         "8 rad", "$\\theta=2t^2$. At $t=2$, $\\theta=8\\,\\mathrm{rad}$.",
         ["4 rad", "16 rad", "2 rad"]),
        ("A point at radius $0.5\\,\\mathrm{m}$ with $\\omega=8\\,\\mathrm{rad/s}$ has speed $v=\\omega r=$",
         "4 m/s", "$8\\times 0.5=4\\,\\mathrm{m/s}$.",
         ["8 m/s", "16 m/s", "2 m/s"]),
        ("Constant $\\alpha=2\\,\\mathrm{rad/s}^2$, $\\omega(0)=0$. $\\omega$ at $t=3\\,\\mathrm{s}$ is",
         "6 rad/s", "$\\omega=\\alpha t=6\\,\\mathrm{rad/s}$.",
         ["2 rad/s", "9 rad/s", "3 rad/s"]),
        ("Torque (magnitude) is $\\tau=r F\\sin\\phi$ where $\\phi$ is the angle between $\\vec r$ and $\\vec F$. If $\\phi=90^\\circ$, $r=0.5\\,\\mathrm{m}$, $F=4\\,\\mathrm{N}$, $\\tau=$",
         "2 N·m", "$\\tau=0.5\\times 4\\times 1=2\\,\\mathrm{N\\cdot m}$.",
         ["8 N·m", "4 N·m", "0"]),
        ("If $\\vec F$ is parallel to $\\vec r$, torque is",
         "0", "$\\sin 0=0$ (or $180^\\circ$). The line of action through the pivot gives no twist.",
         ["r F", "infinite", "mg"]),
        ("Newton 2 for rotation about a fixed axis is $\\tau_\\mathrm{net}=I\\alpha$. If $I=2\\,\\mathrm{kg\\,m}^2$ and $\\alpha=3\\,\\mathrm{rad/s}^2$, $\\tau=$",
         "6 N·m", "$2\\times 3=6\\,\\mathrm{N\\cdot m}$.",
         ["5 N·m", "1.5 N·m", "9 N·m"]),
        ("A $10\\,\\mathrm{N}$ force at $0.40\\,\\mathrm{m}$ perpendicular to a wrench produces $\\tau=$",
         "4 N·m", "$10\\times 0.40=4\\,\\mathrm{N\\cdot m}$.",
         ["14 N·m", "0.04 N·m", "25 N·m"]),
        ("The lever arm is the perpendicular distance from the axis to the line of action of $\\vec F$. Then $\\tau=$",
         "F times lever arm", "Equivalent to $r F\\sin\\phi$.",
         ["F r always even if φ=0", "F/r", "I r"]),
        ("Moment of inertia about an axis is $I=\\int r_\\perp^2\\,dm$. A thin hoop of mass $M$ and radius $R$ about its center (all mass at $R$) has $I=$",
         "MR^2", "Every $dm$ has $r_\\perp=R$.",
         ["½ MR^2", "⅓ MR^2", "2 MR^2"]),
        ("A uniform disk about its central axis has $I=$",
         "½ MR^2", "Standard result of $\\int r^2\\,dm$ in polar coordinates.",
         ["MR^2", "⅓ MR^2", "⅕ MR^2"]),
        ("Uniform rod about its center, perpendicular to the rod, has $I=$",
         "ML^2 / 12", "Integrate $x^2\\,dm$ from $-L/2$ to $L/2$.",
         ["ML^2 / 3", "ML^2 / 2", "ML^2"]),
        ("Same rod about one end, axis still perpendicular, has $I=$",
         "ML^2 / 3", "Or parallel-axis: $ML^2/12+M(L/2)^2=ML^2/3$.",
         ["ML^2 / 12", "MR^2", "0"]),
        ("$M=4\\,\\mathrm{kg}$, disk $R=0.5\\,\\mathrm{m}$, $I_\\mathrm{cm}=$",
         "0.5 kg m^2", "$\\tfrac12(4)(0.25)=0.50$.",
         ["1 kg m^2", "2 kg m^2", "4 kg m^2"]),
        ("Parallel-axis theorem: $I=I_\\mathrm{cm}+Md^2$. If $I_\\mathrm{cm}=2$, $M=4$, $d=0.5$, then $I=$",
         "3 kg m^2", "$2+4(0.25)=2+1=3$.",
         ["2 kg m^2", "4 kg m^2", "1 kg m^2"]),
        ("The axis in the parallel-axis theorem must be",
         "parallel to the CM axis", "And $d$ is the distance between those parallel axes.",
         ["always perpendicular to the CM axis", "through a point of the object only", "the velocity vector"]),
        ("You cannot use $I=I_\\mathrm{cm}+Md^2$ to rotate the axis by $90^\\circ$. That needs",
         "a different I_cm about the new direction", "The theorem does not change axis orientation.",
         ["doubling I", "setting d=0", "using MR^2 always"]),
        ("A hoop $I_\\mathrm{cm}=MR^2$ about a point on its rim (parallel axis, $d=R$) has $I=$",
         "2 MR^2", "$MR^2+MR^2=2MR^2$.",
         ["MR^2", "½ MR^2", "3 MR^2"]),
        ("$I_\\mathrm{cm}=0.5\\,\\mathrm{kg\\,m}^2$, $M=2\\,\\mathrm{kg}$, $d=1\\,\\mathrm{m}$. Parallel-axis $I=$",
         "2.5 kg m^2", "$0.5+2(1)^2=2.5$.",
         ["0.5 kg m^2", "2 kg m^2", "1.5 kg m^2"]),
        ("Rolling without slipping means $v_\\mathrm{cm}=$",
         "ω R", "The contact point is instantaneously at rest.",
         ["ω / R", "α R^2", "0 always"]),
        ("A disk down an incline has $a=\\tfrac23 g\\sin\\theta$. At $30^\\circ$ and $g=10$, $a=$",
         "10/3 m/s^2", "$\\tfrac23\\times 10\\times 1/2=10/3$.",
         ["5 m/s^2", "10 m/s^2", "20/3 m/s^2"]),
        ("A hoop on the same incline has $a=$",
         "½ g sinθ", "$I/MR^2=1$, so $a=g\\sin\\theta/2$.",
         ["g sinθ", "⅔ g sinθ", "0"]),
        ("For rolling $K=\\tfrac12 Mv^2+\\tfrac12 I\\omega^2$ with $v=\\omega R$. For a disk this is",
         "¾ M v^2", "$\\tfrac12 Mv^2+\\tfrac12(\\tfrac12 M R^2)(v/R)^2=\\tfrac34 Mv^2$.",
         ["½ M v^2", "M v^2", "¼ M v^2"]),
        ("Static friction on a wheel rolling down a ramp (no slipping) does",
         "no work", "The contact point is instantaneously at rest, so $f\\cdot dr=0$.",
         ["positive work equal to mgh", "all the dissipation", "negative work μN times path"]),
        ("$W=\\int\\tau\\,d\\theta$. Constant $\\tau=6\\,\\mathrm{N\\cdot m}$ through $2\\,\\mathrm{rad}$ is",
         "12 J", "$6\\times 2=12\\,\\mathrm{J}$.",
         ["3 J", "8 J", "6 J"]),
        ("$K_\\mathrm{rot}=\\tfrac12 I\\omega^2$. If $I=4$ and $\\omega=3$ (SI), $K=$",
         "18 J", "$\\tfrac12(4)(9)=18$.",
         ["12 J", "6 J", "36 J"]),
        ("Power $P=\\tau\\omega$. If $\\tau=4\\,\\mathrm{N\\cdot m}$ and $\\omega=3\\,\\mathrm{rad/s}$, $P=$",
         "12 W", "$4\\times 3=12\\,\\mathrm{W}$.",
         ["7 W", "1.33 W", "0"]),
        ("$\\theta=2t^3$. $\\alpha$ at $t=1\\,\\mathrm{s}$ is",
         "12 rad/s^2", "$\\omega=6t^2$, $\\alpha=12t$. At $t=1$, $\\alpha=12$.",
         ["6 rad/s^2", "2 rad/s^2", "24 rad/s^2"]),
        ("$v=\\omega r$ with $\\omega=10\\,\\mathrm{rad/s}$, $r=0.2\\,\\mathrm{m}$ gives",
         "2 m/s", "$10\\times 0.2=2$.",
         ["50 m/s", "0.02 m/s", "10 m/s"]),
        ("A force through the pivot has lever arm",
         "0", "Line of action hits the axis, so $\\tau=0$.",
         ["r", "F", "I"]),
        ("Sphere $I=\\tfrac25 MR^2$ rolling down an incline has $a=$",
         "5/7 g sinθ", "$1+I/MR^2=1+2/5=7/5$, so $a=(5/7)g\\sin\\theta$.",
         ["2/5 g sinθ", "g sinθ", "5/2 g sinθ"]),
        ("$I_\\mathrm{cm}$ is the smallest $I$ among all",
         "parallel axes", "Because $Md^2\\ge 0$.",
         ["possible orientations", "masses", "angular speeds"]),
        ("$\\tau=8t$ (SI) on $I=4\\,\\mathrm{kg\\,m}^2$ from rest. $\\omega$ at $t=2\\,\\mathrm{s}$ is",
         "4 rad/s", "$\\alpha=\\tau/I=2t$, so $\\omega=t^2$. At $t=2$, $\\omega=4\\,\\mathrm{rad/s}$.",
         ["8 rad/s", "2 rad/s", "16 rad/s"]),
        ("Rod $M=3\\,\\mathrm{kg}$, $L=2\\,\\mathrm{m}$, $I_\\mathrm{cm}=ML^2/12=$",
         "1 kg m^2", "$3\\times 4/12=1$.",
         ["12 kg m^2", "4 kg m^2", "0.25 kg m^2"]),
        ("That rod about an end has $I=$",
         "4 kg m^2", "$ML^2/3=3\\times 4/3=4$.",
         ["1 kg m^2", "3 kg m^2", "12 kg m^2"]),
        ("A yo-yo descending: both $K_\\mathrm{trans}$ and $K_\\mathrm{rot}$ grow while $U$ falls. The constraint is",
         "v = ω r of the inner radius", "String unwinds without slipping on the axle.",
         ["v=0", "α=0", "I=0"]),
        ("$\\int_0^{\\pi} 4\\,d\\theta$ as work by constant $\\tau=4$ is",
         "4π J", "$4\\theta$ from $0$ to $\\pi$ is $4\\pi\\,\\mathrm{J}$.",
         ["4 J", "π J", "0"]),
        ("Tangential $a_t=\\alpha r$. If $\\alpha=6\\,\\mathrm{rad/s}^2$ and $r=0.5\\,\\mathrm{m}$, $a_t=$",
         "3 m/s^2", "$6\\times 0.5=3$.",
         ["6.5 m/s^2", "12 m/s^2", "0.5 m/s^2"]),
        ("Centripetal $a_c=\\omega^2 r$. If $\\omega=4$, $r=0.5$, $a_c=$",
         "8 m/s^2", "$16\\times 0.5=8$.",
         ["2 m/s^2", "4 m/s^2", "0.5 m/s^2"]),
        ("A disk and a hoop race from rest down the same ramp, no slipping. The winner is the",
         "disk", "Larger $a=\\tfrac23 g\\sin\\theta$ vs $\\tfrac12 g\\sin\\theta$.",
         ["hoop", "they tie", "whichever is heavier"]),
        ("Units of $I$ are",
         "kg m^2", "From $\\int r^2\\,dm$.",
         ["N m", "kg m/s", "rad/s"]),
        ("$\\theta(0)=1\\,\\mathrm{rad}$, $\\omega=2t$. $\\theta$ at $t=3$ is",
         "10 rad", "$\\theta=1+t^2=1+9=10$.",
         ["6 rad", "9 rad", "7 rad"]),
        ("$\\alpha=6t$, $\\omega(0)=0$. Using $\\alpha=\\omega d\\omega/d\\theta$ is optional; $\\omega$ at $t=2$ is",
         "12 rad/s", "$\\omega=3t^2=12$ at $t=2$.",
         ["6 rad/s", "24 rad/s", "3 rad/s"]),
        ("$I=\\int_0^L x^2\\lambda\\,dx$ with $\\lambda=M/L$ for a rod about an end equals",
         "ML^2 / 3", "$\\lambda\\int_0^L x^2\\,dx=(M/L)(L^3/3)=ML^2/3$.",
         ["ML^2 / 12", "ML^2 / 2", "ML^2"]),
        ("Disk $I=\\tfrac12 MR^2$ rolling, $K=\\tfrac12 Mv^2+\\tfrac12 I\\omega^2$. If $M=4$, $v=3$, $K=$",
         "27 J", "$\\tfrac12(4)(9)+\\tfrac12(\\tfrac12\\cdot 4 R^2)(9/R^2)=18+9=27$.",
         ["18 J", "9 J", "36 J"]),
        ("AP Stretch: $\\tau=6\\theta$ (SI) from $\\theta=1$ to $2$. $W=\\int\\tau\\,d\\theta=$",
         "9 J", "$\\int_1^2 6\\theta\\,d\\theta=3\\theta^2\\big|_1^2=12-3=9\\,\\mathrm{J}$.",
         ["6 J", "12 J", "3 J"]),
        ("AP Stretch: Parallel axis with $I_\\mathrm{cm}=ML^2/12$, $d=L/3$. $I=$",
         "7 ML^2 / 36", "$ML^2/12+M L^2/9=3ML^2/36+4ML^2/36=7ML^2/36$.",
         ["ML^2 / 12", "ML^2 / 9", "13 ML^2 / 36"]),
        ("AP Stretch: Hoop vs disk, same $M,R,\\theta$. Ratio $a_\\mathrm{disk}/a_\\mathrm{hoop}=$",
         "4/3", "$(\\tfrac23)/(\\tfrac12)=4/3$.",
         ["2", "3/2", "2/3"]),
        ("AP Stretch: $\\omega\\,d\\omega=\\alpha\\,d\\theta$ with $\\alpha=4\\theta$, $\\omega=0$ at $\\theta=0$. Then $\\omega^2$ at $\\theta=2$ is",
         "16", "$\\int_0^\\omega u\\,du=\\int_0^2 4\\theta\\,d\\theta$, $\\tfrac12\\omega^2=8$, $\\omega^2=16$.",
         ["8", "4", "32"]),
        ("AP Stretch: A string with tension $T=8\\,\\mathrm{N}$ wraps a pulley $I=0.50\\,\\mathrm{kg\\,m}^2$, $R=0.25\\,\\mathrm{m}$. The linear $a$ of the string is",
         "1 m/s^2", "$\\tau=TR=2\\,\\mathrm{N\\cdot m}$, $\\alpha=\\tau/I=4\\,\\mathrm{rad/s}^2$, then $a=\\alpha R=1\\,\\mathrm{m/s}^2$.",
         ["16 m/s^2", "4 m/s^2", "0.25 m/s^2"]),
        ("AP Stretch: Rolling disk from rest down $h=1.8\\,\\mathrm{m}$, $g=10$. Using $Mgh=\\tfrac34 Mv^2$, $v=$",
         "sqrt(24) m/s", "$18=\\tfrac34 v^2$, $v^2=24$, $v=\\sqrt{24}\\,\\mathrm{m/s}$.",
         ["6 m/s", "sqrt(36) m/s", "sqrt(12) m/s"]),
        ("AP Stretch: $\\theta=t^3-12t$. Find $\\alpha$ at the first $t>0$ when $\\omega=0$.",
         "12 rad/s^2", "$\\omega=3t^2-12=0$ gives $t=2$. Then $\\alpha=6t=12\\,\\mathrm{rad/s}^2$.",
         ["6 rad/s^2", "2 rad/s^2", "0"]),
        ("AP Stretch: $\\tau=6\\theta^2$ from $\\theta=0$ to $\\theta=2$. $W=\\int\\tau\\,d\\theta=$",
         "16 J", "$\\int_0^2 6\\theta^2\\,d\\theta=2\\theta^3\\big|_0^2=16\\,\\mathrm{J}$.",
         ["8 J", "12 J", "24 J"]),
        ("AP Stretch: A disk $I=\\tfrac12 MR^2$ and $M=2\\,\\mathrm{kg}$, $R=0.5\\,\\mathrm{m}$ about a point on its rim (parallel, $d=R$). $I_p=$",
         "0.75 kg m^2", "$I_\\mathrm{cm}=0.25$, $Md^2=2(0.25)=0.5$, sum $0.75$.",
         ["0.25 kg m^2", "0.5 kg m^2", "1 kg m^2"]),
    ])
    return qs


def build_unit5():
    title = "AP Physics C Mechanics Unit 5: Rotation I"
    description = "Angular kinematics, torque, moment of inertia, parallel-axis theorem, rolling, and rotational work."
    c1 = concept_block(
        "1. Angular kinematics",
        [
            "Rotation about a fixed axis is described by the angle $\\theta(t)$ in radians. Angular velocity is the "
            "derivative $\\omega=d\\theta/dt$, and angular acceleration is $\\alpha=d\\omega/dt=d^2\\theta/dt^2$. "
            "If $\\theta=3t^2$, then $\\omega=6t$ and $\\alpha=6\\,\\mathrm{rad/s}^2$. At $t=2\\,\\mathrm{s}$, $\\omega=12\\,\\mathrm{rad/s}$. "
            "This is Unit 1 kinematics with new letters.",
            "A point at perpendicular distance $r$ from the axis has speed $v=\\omega r$ and tangential acceleration "
            "$a_t=\\alpha r$. Centripetal acceleration $v^2/r=\\omega^2 r$ still points toward the axis. "
            "If $r=0.5\\,\\mathrm{m}$ and $\\omega=8\\,\\mathrm{rad/s}$, $v=4\\,\\mathrm{m/s}$.",
            "Integrating recovers angle: $\\theta=\\theta_0+\\int\\omega\\,dt$. If $\\omega=4t$ and $\\theta(0)=0$, "
            "$\\theta=2t^2$. At $t=2\\,\\mathrm{s}$, $\\theta=8\\,\\mathrm{rad}$ (a bit more than a full turn, since $2\\pi\\approx 6.28$).",
            "Use radians in every calculus formula. Degrees make $d\\theta/dt$ numerically wrong by $\\pi/180$.",
            "Constant $\\alpha$ recovers the Physics 1 rotation formulas as special cases, just as constant $a$ recovered SUVAT. "
            "If $\\alpha$ is not constant, integrate the actual $\\alpha(t)$ or $\\alpha(\\omega)$.",
            "The chain-rule twin $\\alpha=\\omega\\,d\\omega/d\\theta$ appears when $\\alpha$ depends on angle, matching $a=v\\,dv/dx$.",
        ],
        "Every later rotation law ($\\tau=I\\alpha$, $L=I\\omega$, rolling $a=\\alpha R$) needs fluent $\\theta,\\omega,\\alpha$ calculus.",
        "Translate: $x\\to\\theta$, $v\\to\\omega$, $a\\to\\alpha$. Differentiate or integrate with the same moves as Unit 1, and convert to linear with factors of $r$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: 3 * t * t, 0, 3))],
                points=[(2, 12, "θ(2)=12 rad")],
                xlim=(0, 3.2), ylim=(-1, 30), xlab="t (s)", ylab="θ (rad)",
            ),
            "$\\theta=3t^2$; the slope is $\\omega=6t$",
            "At $t=2\\,\\mathrm{s}$ the slope is $12\\,\\mathrm{rad/s}$. Same picture as $x=3t^2$ in Unit 1, now an angle.",
        )
        + solved(
            1, "$\\theta=3t^2$. Find $\\omega$ and $\\alpha$ at $t=2\\,\\mathrm{s}$.",
            [
                "$\\omega=6t=12\\,\\mathrm{rad/s}$.",
                "$\\alpha=6\\,\\mathrm{rad/s}^2$.",
                "Linear speed at $r=0.5\\,\\mathrm{m}$ would be $v=6\\,\\mathrm{m/s}$.",
            ],
            "$\\omega=12\\,\\mathrm{rad/s}$, $\\alpha=6\\,\\mathrm{rad/s}^2$",
            "",
            "Easy",
        )
        + solved(
            2, "$\\omega=4t$, $\\theta(0)=0$. Find $\\theta(2)$.",
            [
                "$\\theta=\\int_0^2 4t\\,dt=2t^2\\big|_0^2$.",
                "$\\theta=8\\,\\mathrm{rad}$.",
                "About $8/(2\\pi)\\approx 1.27$ revolutions.",
            ],
            "$8\\,\\mathrm{rad}$",
            "",
            "Medium",
        )
        + solved(
            3, "$\\alpha=6t$, $\\omega(0)=0$, $\\theta(0)=0$. Find $\\theta$ at $t=2\\,\\mathrm{s}$.",
            [
                "$\\omega=3t^2$.",
                "$\\theta=t^3$.",
                "At $t=2$, $\\theta=8\\,\\mathrm{rad}$.",
            ],
            "$8\\,\\mathrm{rad}$",
            "",
            "Hard",
        )
        + _ican([
            "I can differentiate $\\theta(t)$ to get $\\omega$ and $\\alpha$.",
            "I can integrate $\\omega$ to recover $\\theta$ with an initial angle.",
            "I can convert with $v=\\omega r$ and $a_t=\\alpha r$.",
        ]),
        ("Using degrees inside $\\omega=d\\theta/dt$",
         "The calculus identities assume radians. Convert to radians before differentiating, or your $\\omega$ is not in $\\mathrm{rad/s}$."),
        ("Write the angular analog of the linear equation you already trust",
         "If you would write $v=dx/dt$, write $\\omega=d\\theta/dt$ next to it. The algebra is identical."),
        [
            "I can differentiate $\\theta(t)$ to get $\\omega$ and $\\alpha$.",
            "I can integrate $\\omega$ to recover $\\theta$ with an initial angle.",
            "I can convert with $v=\\omega r$ and $a_t=\\alpha r$.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Torque as r cross F",
        [
            "Torque measures how effectively a force twists an object about a chosen axis. In words: torque is "
            "the moment of a force. As a vector, $\\vec\\tau=\\vec r\\times\\vec F$, with $\\vec r$ from the axis "
            "(or origin) to the point of application. Magnitude $\\tau=r F\\sin\\phi$, where $\\phi$ is the angle "
            "between $\\vec r$ and $\\vec F$.",
            "If $\\phi=90^\\circ$, $r=0.5\\,\\mathrm{m}$, $F=4\\,\\mathrm{N}$, then $\\tau=2\\,\\mathrm{N\\cdot m}$. "
            "If $\\vec F$ is parallel to $\\vec r$ (pushing straight at the pivot), $\\sin\\phi=0$ and $\\tau=0$.",
            "The lever arm is the perpendicular distance from the axis to the line of action of $\\vec F$. Then "
            "$\\tau=F\\times$ (lever arm), the same number.",
            "About a fixed axis, $\\tau_\\mathrm{net}=I\\alpha$, the rotational Newton 2. If $I=2\\,\\mathrm{kg\\,m}^2$ "
            "and $\\alpha=3\\,\\mathrm{rad/s}^2$, $\\tau_\\mathrm{net}=6\\,\\mathrm{N\\cdot m}$. Signs: choose a positive "
            "sense of rotation (often counterclockwise) and stick to it.",
            "Gravity's torque about a pivot is $mg$ times the horizontal lever arm of the center of mass, or "
            "$mgd\\sin\\theta$ for a pendulum rod. That will become the physical pendulum in Unit 7.",
            "FRQ move: mark the axis, draw $\\vec r$ and $\\vec F$, check $\\phi$, then write $\\tau=I\\alpha$ with that same axis.",
        ],
        "Without torque you cannot start or stop rotation, or relate a hanging mass to a pulley wheel. It is the "
        "rotational twin of force.",
        "Pick an axis. Draw $\\vec r$ from that axis to the force. Compute $r F\\sin\\phi$ with a sign. Sum torques "
        "and set the sum equal to $I\\alpha$ about the same axis.",
        lesson_figure(
            _torque_svg(),
            "Force $\\vec F$ applied perpendicular to a rod at distance $r$ from the pivot",
            "Here $\\phi=90^\\circ$, so $\\tau=rF$. A force through the pivot would produce zero torque.",
        )
        + solved(
            6, "$r=0.5\\,\\mathrm{m}$, $F=4\\,\\mathrm{N}$, perpendicular. Find $\\tau$.",
            [
                "$\\sin 90^\\circ=1$.",
                "$\\tau=0.5\\times 4=2\\,\\mathrm{N\\cdot m}$.",
                "Direction: out of the page if $r$ is right and $F$ is up (right-hand rule).",
            ],
            "$2\\,\\mathrm{N\\cdot m}$",
            "",
            "Easy",
        )
        + solved(
            7, "$I=2\\,\\mathrm{kg\\,m}^2$, $\\alpha=3\\,\\mathrm{rad/s}^2$. Find $\\tau_\\mathrm{net}$.",
            [
                "$\\tau=I\\alpha$.",
                "$\\tau=6\\,\\mathrm{N\\cdot m}$.",
                "This $\\tau$ is the algebraic sum about that axis.",
            ],
            "$6\\,\\mathrm{N\\cdot m}$",
            "",
            "Medium",
        )
        + solved(
            8, "A $10\\,\\mathrm{N}$ force at $30^\\circ$ to a $0.40\\,\\mathrm{m}$ wrench. Find $\\tau$.",
            [
                "$\\tau=r F\\sin 30^\\circ$.",
                "$\\sin 30^\\circ=1/2$.",
                "$\\tau=0.40\\times 10\\times 1/2=2.0\\,\\mathrm{N\\cdot m}$.",
            ],
            "$2.0\\,\\mathrm{N\\cdot m}$",
            "",
            "Hard",
        )
        + _ican([
            "I can compute $\\tau=r F\\sin\\phi$.",
            "I can use $\\tau_\\mathrm{net}=I\\alpha$ about a fixed axis.",
            "I can explain why a force through the pivot gives $\\tau=0$.",
        ]),
        ("Using $\\tau=rF$ when the force is not perpendicular",
         "You must include $\\sin\\phi$ or use the lever arm. A $30^\\circ$ force is only half as effective as a $90^\\circ$ force of the same size."),
        ("Name the axis in the first sentence of the solution",
         "Torque and $I$ are axis-dependent. Changing the axis changes both sides of $\\tau=I\\alpha$ together."),
        [
            "I can compute $\\tau=r F\\sin\\phi$.",
            "I can use $\\tau_\\mathrm{net}=I\\alpha$ about a fixed axis.",
            "I can explain why a force through the pivot gives $\\tau=0$.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Moment of inertia",
        [
            "Moment of inertia $I$ is the rotational analog of mass: it measures how spread-out the mass is from "
            "the axis. Definition: $I=\\int r_\\perp^2\\,dm$, where $r_\\perp$ is the perpendicular distance from "
            "the axis to the mass element. Farther mass is much harder to angularly accelerate because of the $r^2$.",
            "A thin hoop with all mass at radius $R$, about its central axis, has $I=MR^2$. A uniform disk about "
            "the same kind of axis has $I=\\tfrac12 MR^2$ because much of the mass sits inside $R$. "
            "For $M=4\\,\\mathrm{kg}$ and $R=0.5\\,\\mathrm{m}$, the disk has $I=0.50\\,\\mathrm{kg\\,m}^2$.",
            "A uniform rod about a perpendicular axis through its center has $I=ML^2/12$. About one end, $I=ML^2/3$. "
            "You can get the end result from the center result with the parallel-axis theorem next.",
            "To compute from scratch: pick $dm=\\lambda\\,dx$ or $\\sigma\\,2\\pi r\\,dr$, insert $r_\\perp^2$, integrate. "
            "Example: hoop is immediate because $r_\\perp=R$ is constant.",
            "Larger $I$ means smaller $\\alpha$ for a given torque. A hoop loses a rolling race to a disk down the "
            "same incline because more of its mass is far from the axis.",
            "AP expects the catalog (hoop, disk, sphere $\\tfrac25 MR^2$, rod) plus one integral. Quote the catalog "
            "when the object is named; integrate when $\\lambda(x)$ is given.",
        ],
        "$I$ is the number that makes $\\tau=I\\alpha$ and $K=\\tfrac12 I\\omega^2$ true. Using $m$ in those formulas "
        "is a category error.",
        "Identify the object and the axis. Quote $I$ or set up $\\int r^2\\,dm$. Keep SI units $\\mathrm{kg\\,m}^2$.",
        lesson_figure(
            _inertia_svg(),
            "Mass far from the axis contributes more to $I$ because of the $r^2$ in $\\int r^2\\,dm$",
            "A hoop (all mass at $R$) has $I=MR^2$. A disk of the same $M$ and $R$ has $I=\\tfrac12 MR^2$ because much of the mass sits at $r<R$.",
        )
        + solved(
            11, "Hoop $M$, $R$, central axis. $I=$?",
            [
                "All $dm$ have $r_\\perp=R$.",
                "$I=R^2\\int dm=MR^2$.",
                "Compare: a disk would be half of that.",
            ],
            "$MR^2$",
            "",
            "Easy",
        )
        + solved(
            12, "Disk $M=4\\,\\mathrm{kg}$, $R=0.5\\,\\mathrm{m}$. Find $I_\\mathrm{cm}$.",
            [
                "$I=\\tfrac12 MR^2$.",
                "$R^2=0.25$.",
                "$I=\\tfrac12(4)(0.25)=0.50\\,\\mathrm{kg\\,m}^2$.",
            ],
            "$0.50\\,\\mathrm{kg\\,m}^2$",
            "",
            "Medium",
        )
        + solved(
            13, "Uniform rod, axis through end, perpendicular. Get $I$ from $I_\\mathrm{cm}=ML^2/12$.",
            [
                "Distance from CM to end is $L/2$.",
                "$I=ML^2/12+M(L/2)^2=ML^2/12+ML^2/4$.",
                "$I=ML^2/3$.",
            ],
            "$ML^2/3$",
            "",
            "Hard",
        )
        + _ican([
            "I can state $I=\\int r_\\perp^2\\,dm$ in words and symbols.",
            "I can recall hoop, disk, and rod catalog values.",
            "I can explain why a hoop has larger $I$ than a disk of equal $M,R$.",
        ]),
        ("Using $I=MR^2$ for every object",
         "That is the hoop (or point mass at $R$). A disk is $\\tfrac12 MR^2$. Using $MR^2$ for a disk doubles $I$ and halves $\\alpha$."),
        ("Write the axis next to $I$",
         "$I$ about a diameter is not $I$ about the central perpendicular axis. The catalog line must match the picture."),
        [
            "I can state $I=\\int r_\\perp^2\\,dm$ in words and symbols.",
            "I can recall hoop, disk, and rod catalog values.",
            "I can explain why a hoop has larger $I$ than a disk of equal $M,R$.",
        ],
        11,
    )
    c4 = concept_block(
        "4. The parallel-axis theorem",
        [
            "If you know $I_\\mathrm{cm}$ about an axis through the center of mass, the moment about a parallel axis "
            "a distance $d$ away is $I=I_\\mathrm{cm}+Md^2$. The axes must be parallel; $d$ is the perpendicular "
            "distance between them.",
            "Numeric: $I_\\mathrm{cm}=2\\,\\mathrm{kg\\,m}^2$, $M=4\\,\\mathrm{kg}$, $d=0.5\\,\\mathrm{m}$ gives "
            "$I=2+4(0.25)=3\\,\\mathrm{kg\\,m}^2$. The extra $Md^2$ is exactly the CM treated as a point mass at distance $d$.",
            "A hoop about a point on its rim: $I_\\mathrm{cm}=MR^2$, $d=R$, so $I=2MR^2$. That is a common “yo-yo or hoop rolling about contact” value.",
            "The theorem does not rotate an axis by $90^\\circ$. A new orientation needs a new $I_\\mathrm{cm}$. "
            "It also does not apply using a non-CM starting axis unless you first find $I_\\mathrm{cm}$.",
            "Derivation sketch: $I=\\int |\\vec r_\\mathrm{cm}+\\vec d|^2\\,dm$ expands; the cross term vanishes because "
            "$\\int \\vec r_\\mathrm{cm}\\,dm=0$ by definition of CM. What remains is $I_\\mathrm{cm}+Md^2$.",
            "On FRQs, shifting from a table of $I_\\mathrm{cm}$ to a pivot at the end of a rod is this theorem in one line.",
        ],
        "Physical pendulums, rolling about the contact point, and doors (axis at the hinge) all live a distance $d$ from the CM.",
        "Look up or compute $I_\\mathrm{cm}$. Measure $d$ between parallel axes. Add $Md^2$. Refuse the theorem if the axes are not parallel.",
        lesson_figure(
            xy_graph(
                points=[(0, 0, "CM axis"), (2, 0, "new axis")],
                xlim=(-1, 4), ylim=(-2, 2), xlab="d", ylab="",
            ),
            "Two parallel axes separated by distance $d$",
            "The CM axis is the one where $I$ is smallest among all parallel axes. Any shift adds $Md^2>0$.",
        )
        + solved(
            16, "$I_\\mathrm{cm}=2$, $M=4$, $d=0.5$ (SI). Find $I$.",
            [
                "$I=I_\\mathrm{cm}+Md^2$.",
                "$d^2=0.25$.",
                "$I=2+1=3\\,\\mathrm{kg\\,m}^2$.",
            ],
            "$3\\,\\mathrm{kg\\,m}^2$",
            "",
            "Easy",
        )
        + solved(
            17, "Hoop, axis through a point on the rim, parallel to the symmetry axis. $I=$?",
            [
                "$I_\\mathrm{cm}=MR^2$.",
                "$d=R$.",
                "$I=MR^2+MR^2=2MR^2$.",
            ],
            "$2MR^2$",
            "",
            "Medium",
        )
        + solved(
            18, "Rod $I_\\mathrm{cm}=ML^2/12$, pivot at the end. Recover $I_\\mathrm{end}$.",
            [
                "$d=L/2$.",
                "$Md^2=M L^2/4$.",
                "$I=ML^2/12+ML^2/4=ML^2/3$.",
            ],
            "$ML^2/3$",
            "",
            "Hard",
        )
        + _ican([
            "I can apply $I=I_\\mathrm{cm}+Md^2$ with matching parallel axes.",
            "I can shift a hoop or rod from the CM to a rim or end.",
            "I can state that $I_\\mathrm{cm}$ is the minimum among parallel axes.",
        ]),
        ("Adding $Md^2$ onto an axis that is not through the CM",
         "The starting $I$ in the theorem must be about a CM axis. Adding $Md^2$ twice is wrong."),
        ("Sketch the two parallel arrows for the axes before computing $d$",
         "If they are not parallel in your sketch, stop. The theorem does not apply."),
        [
            "I can apply $I=I_\\mathrm{cm}+Md^2$ with matching parallel axes.",
            "I can shift a hoop or rod from the CM to a rim or end.",
            "I can state that $I_\\mathrm{cm}$ is the minimum among parallel axes.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Rolling without slipping",
        [
            "Rolling without slipping ties translation of the CM to rotation about the CM: $v_\\mathrm{cm}=\\omega R$ "
            "and $a_\\mathrm{cm}=\\alpha R$, with $R$ the radius of the wheel. The contact point is instantaneously at rest "
            "relative to the surface, so static friction can act without doing work.",
            "Energy: $K=\\tfrac12 M v_\\mathrm{cm}^2+\\tfrac12 I_\\mathrm{cm}\\omega^2=\\tfrac12 M v^2\\bigl(1+I_\\mathrm{cm}/(MR^2)\\bigr)$. "
            "A hoop ($I=MR^2$) stores as much rotational $K$ as translational $K$. A disk stores half as much rotational as translational.",
            "Down an incline of angle $\\theta$, Newton's laws plus the rolling constraint give "
            "$a=\\dfrac{g\\sin\\theta}{1+I/(MR^2)}$. For a disk, $I=\\tfrac12 MR^2$, so $a=\\tfrac23 g\\sin\\theta$. "
            "At $30^\\circ$ with $g=10$, $a=10/3\\,\\mathrm{m/s}^2$. A hoop has $a=\\tfrac12 g\\sin\\theta$, smaller.",
            "Static friction up the ramp (when rolling down) provides the torque. If the ramp is too steep or too "
            "smooth, the object slips and you must switch to kinetic friction plus independent $a$ and $\\alpha$.",
            "Instantaneous axis: you may compute $K=\\tfrac12 I_p\\omega^2$ about the contact point, with "
            "$I_p=I_\\mathrm{cm}+MR^2$. Same $K$, different bookkeeping.",
            "FRQ: write $v=\\omega R$ explicitly, then either energy or $F=ma$ plus $\\tau=I\\alpha$ with friction.",
        ],
        "Rolling is how AP combines Units 2, 3, and 5. Missing the constraint $a=\\alpha R$ is the usual loss of points.",
        "Write $v=\\omega R$. Choose energy (no slipping, no rolling friction loss) or two Newton equations plus friction. "
        "Quote $I$ for the shape, then solve for $a$ or $v$.",
        lesson_figure(
            _wheel_svg(),
            "Rolling without slipping: the CM speed and the spin are locked by $v=\\omega R$",
            "The bottom point is instantaneously at rest. Static friction can therefore torque the wheel without dissipating $K$.",
        )
        + solved(
            21, "Disk rolling without slipping. Relate $v_\\mathrm{cm}$ to $\\omega$.",
            [
                "Constraint: $v_\\mathrm{cm}=\\omega R$.",
                "Also $a_\\mathrm{cm}=\\alpha R$.",
                "This is kinematic, independent of $I$.",
            ],
            "$v_\\mathrm{cm}=\\omega R$",
            "",
            "Easy",
        )
        + solved(
            22, "Disk down a $30^\\circ$ incline, $g=10$, no slipping. Find $a_\\mathrm{cm}$.",
            [
                "$a=\\dfrac{g\\sin\\theta}{1+1/2}=\\tfrac23 g\\sin 30^\\circ$.",
                "$\\sin 30^\\circ=1/2$, so $a=\\tfrac23\\times 5$.",
                "$a=10/3\\,\\mathrm{m/s}^2$.",
            ],
            "$10/3\\,\\mathrm{m/s}^2$",
            "",
            "Medium",
        )
        + solved(
            23, "Compare hoop vs disk, same $M,R$, same incline, no slipping. Which has larger $a$, and why?",
            [
                "$a=g\\sin\\theta/(1+I/MR^2)$.",
                "Hoop has $I/MR^2=1$, disk has $1/2$.",
                "Disk has smaller denominator, hence larger $a=\\tfrac23 g\\sin\\theta$ vs hoop $\\tfrac12 g\\sin\\theta$.",
            ],
            "The disk: less $I$ relative to $MR^2$, so more of $mg\\sin\\theta$ goes into $a_\\mathrm{cm}$.",
            "",
            "Hard",
        )
        + _ican([
            "I can write the rolling constraint $v=\\omega R$.",
            "I can use $a=g\\sin\\theta/(1+I/MR^2)$ for a named shape.",
            "I can split $K$ into translational plus rotational pieces.",
        ]),
        ("Treating a rolling object as sliding frictionless",
         "Then $a=g\\sin\\theta$, which is too large. Part of the energy (or the net force budget) goes into spin."),
        ("Write $v=\\omega R$ before energy or Newton 2",
         "That one constraint reduces two unknowns to one. Without it the system is underdetermined."),
        [
            "I can write the rolling constraint $v=\\omega R$.",
            "I can use $a=g\\sin\\theta/(1+I/MR^2)$ for a named shape.",
            "I can split $K$ into translational plus rotational pieces.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Rotational work and energy",
        [
            "Work by a torque about a fixed axis is $W=\\int\\tau\\,d\\theta$. If $\\tau=6\\,\\mathrm{N\\cdot m}$ through "
            "$2\\,\\mathrm{rad}$, $W=12\\,\\mathrm{J}$. The rotational work–energy theorem says this net rotational "
            "work equals $\\Delta K_\\mathrm{rot}=\\Delta\\bigl(\\tfrac12 I\\omega^2\\bigr)$ when the axis is fixed.",
            "Power is $P=\\tau\\omega$, the twin of $P=\\vec F\\cdot\\vec v$. A motor providing $4\\,\\mathrm{N\\cdot m}$ "
            "at $\\omega=3\\,\\mathrm{rad/s}$ delivers $12\\,\\mathrm{W}$.",
            "For $I=4\\,\\mathrm{kg\\,m}^2$ and $\\omega=3\\,\\mathrm{rad/s}$, $K_\\mathrm{rot}=\\tfrac12(4)(9)=18\\,\\mathrm{J}$. "
            "That is energy you can tap with a generator or dump into heat with a brake.",
            "A falling mass unwinding a string from a pulley converts $mgy$ into both $K_\\mathrm{mass}$ and "
            "$K_\\mathrm{pulley}=\\tfrac12 I\\omega^2$ with $\\omega=v/R$. Missing the pulley $K$ understates the speed.",
            "If the axis is not fixed (rolling), include both $\\tfrac12 Mv_\\mathrm{cm}^2$ and $\\tfrac12 I_\\mathrm{cm}\\omega^2$, "
            "or use $I$ about the contact point. Do not double-count.",
            "FRQ: write $W=\\int\\tau\\,d\\theta=\\Delta\\bigl(\\tfrac12 I\\omega^2\\bigr)$ for a fixed axle, or "
            "$mgh=\\tfrac12 mv^2+\\tfrac12 I\\omega^2$ for rolling descent.",
        ],
        "Energy methods often beat $\\tau=I\\alpha$ when you want a speed, not a time. Rotational $K$ is the new term "
        "Algebra-based courses sometimes skip.",
        "Choose a fixed axis or the CM. Write the matching $K$. Set $W_\\mathrm{net}=\\Delta K$ or conserve $E$ if only conservative torques/forces do work.",
        lesson_figure(
            energy_bars_svg(ke=3, pe=2, thermal=0),
            "A rolling object stores both translational $K$ and rotational $K$; both come from lost $U$",
            "The KE bar is really $K_\\mathrm{trans}+K_\\mathrm{rot}$. A hoop puts more of that bar into spin than a disk does.",
        )
        + solved(
            26, "$\\tau=6\\,\\mathrm{N\\cdot m}$ through $\\Delta\\theta=2\\,\\mathrm{rad}$. Find $W$.",
            [
                "$W=\\tau\\Delta\\theta$ if $\\tau$ is constant.",
                "$W=12\\,\\mathrm{J}$.",
                "That $12\\,\\mathrm{J}$ is $\\Delta K_\\mathrm{rot}$ for a fixed axis.",
            ],
            "$12\\,\\mathrm{J}$",
            "",
            "Easy",
        )
        + solved(
            27, "$I=4\\,\\mathrm{kg\\,m}^2$, $\\omega=3\\,\\mathrm{rad/s}$. Find $K_\\mathrm{rot}$.",
            [
                "$K=\\tfrac12 I\\omega^2$.",
                "$\\omega^2=9$.",
                "$K=18\\,\\mathrm{J}$.",
            ],
            "$18\\,\\mathrm{J}$",
            "",
            "Medium",
        )
        + solved(
            28, "Mass $m$ falls $h$ unwinding a string from a disk pulley $I=\\tfrac12 MR^2$, starting from rest. Find $v$ of $m$.",
            [
                "$mgh=\\tfrac12 mv^2+\\tfrac12 I\\omega^2$ and $\\omega=v/R$.",
                "$I\\omega^2=\\tfrac12 M v^2$.",
                "$v=\\sqrt{2mgh/(m+M/2)}$.",
            ],
            "$v=\\sqrt{\\dfrac{2mgh}{m+M/2}}$",
            "",
            "Hard",
        )
        + _ican([
            "I can compute $W=\\int\\tau\\,d\\theta$ and $P=\\tau\\omega$.",
            "I can evaluate $K=\\tfrac12 I\\omega^2$.",
            "I can include pulley or rolling rotational $K$ in energy conservation.",
        ]),
        ("Forgetting $\\tfrac12 I\\omega^2$ when a pulley has mass",
         "Then you predict too large a speed, as if the pulley were massless. The missing energy went into spin."),
        ("Match the axis of $I$ to the $\\omega$ you use",
         "If $\\omega$ is about the CM, use $I_\\mathrm{cm}$. If you use the contact-point axis, use $I_p=I_\\mathrm{cm}+MR^2$ and that same $\\omega$."),
        [
            "I can compute $W=\\int\\tau\\,d\\theta$ and $P=\\tau\\omega$.",
            "I can evaluate $K=\\tfrac12 I\\omega^2$.",
            "I can include pulley or rolling rotational $K$ in energy conservation.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        [
            "Treat $\\theta,\\omega,\\alpha$ with the same calculus as $x,v,a$",
            "Compute torque as $\\vec r\\times\\vec F$ and use $\\tau=I\\alpha$",
            "Evaluate $I=\\int r^2\\,dm$ and catalog values",
            "Shift axes with $I=I_\\mathrm{cm}+Md^2$",
            "Apply rolling without slipping, including incline $a$",
            "Use rotational work and $\\tfrac12 I\\omega^2$",
        ],
        c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Rotation II and Angular Momentum
# ===========================================================================

def _u6_questions():
    qs = []
    _add(qs, [
        ("Angular momentum of a rigid body about a fixed axis is $L=I\\omega$. If $I=5$ and $\\omega=2$ (SI), $L=$",
         "10 kg m^2/s", "$5\\times 2=10$.",
         ["7", "2.5", "25"]),
        ("For a point particle, $\\vec L=\\vec r\\times\\vec p$. If $r=2$, $p=3$, $\\phi=90^\\circ$, $L=$",
         "6 kg m^2/s", "$rp\\sin 90^\\circ=6$.",
         ["5", "1.5", "0"]),
        ("If $\\vec r$ is parallel to $\\vec p$, $L=$",
         "0", "The particle is heading straight at or away from the origin.",
         ["rp", "Iω always", "mvr always"]),
        ("$\\tau_\\mathrm{net}=dL/dt$. If $L=4t^2$, $\\tau$ at $t=2$ is",
         "16 N·m", "$\\tau=8t=16$ at $t=2$.",
         ["4 N·m", "8 N·m", "32 N·m"]),
        ("$I=2$, $\\omega=3t$. $L(t)=$",
         "6t", "$L=I\\omega=6t$.",
         ["6", "3t", "2"]),
        ("If $\\tau_\\mathrm{net}=0$ about an axis, $L$ about that axis is",
         "constant", "Conservation of angular momentum.",
         ["zero", "maximum", "equal to K"]),
        ("Ice skater pulls arms in: $I$ halves, $\\omega$",
         "doubles", "$I\\omega$ constant, so $\\omega\\propto 1/I$.",
         ["halves", "stays the same", "becomes zero"]),
        ("$I=4$, $\\omega=3$ then $I=2$. New $\\omega=$",
         "6 rad/s", "$12=2\\omega$, $\\omega=6$.",
         ["3 rad/s", "1.5 rad/s", "12 rad/s"]),
        ("A person on a rest stool holds a spinning wheel. If they flip the wheel, the stool",
         "rotates to keep total L", "External $\\tau$ about the vertical is approximately zero.",
         ["must stay still by Newton 1 for L", "loses mass", "creates energy"]),
        ("KE $\\tfrac12 I\\omega^2$ when $I$ halves at constant $L$",
         "doubles", "$K=L^2/(2I)$, so half $I$ doubles $K$ (work done pulling arms in).",
         ["halves", "unchanged", "becomes zero"]),
        ("A spinning gyroscope feels a gravitational torque $mgr$ horizontally. It precesses rather than falling because",
         "dL is perpendicular to L", "The tip of $\\vec L$ moves sideways; that is precession.",
         ["gravity shuts off", "I becomes zero", "ω reverses"]),
        ("Precession rate (slow, horizontal wheel) is $\\Omega=\\tau/L=mgr/(I\\omega)$. Larger spin $\\omega$ means",
         "slower precession", "$\\Omega\\propto 1/\\omega$.",
         ["faster precession", "no precession change", "falling"]),
        ("Gyroscopic motion on AP is treated",
         "qualitatively with τ = dL/dt", "You justify direction with the right-hand rule, not a long DE.",
         ["with Gauss's law", "as SHM of θ always", "as linear F=ma only"]),
        ("If $\\vec L$ points along the axle out of a wheel and $\\vec\\tau$ points to the right, the tip of $\\vec L$ moves",
         "right", "That is the sense of precession.",
         ["down", "opposite L", "randomly"]),
        ("A non-spinning wheel on a pivot falls. A fast-spinning one",
         "precesses", "Spin provides large $L$ that gravity's $\\tau$ can only turn slowly.",
         ["ignores gravity forever", "floats", "has zero weight"]),
        ("A disk $I=2$ at $\\omega=6$ drops onto a rest disk $I=2$ (they stick). Final $\\omega=$",
         "3 rad/s", "$12=4\\omega$, $\\omega=3$ if friction is internal to the pair about the shared axis.",
         ["6 rad/s", "12 rad/s", "0"]),
        ("That sticking rotation is inelastic in the rotational sense: $K_\\mathrm{rot}$",
         "drops", "$\\tfrac12 I\\omega^2$: $36$ to $18$ if $I$ doubles and $L$ is fixed... $K_i=\\tfrac12(2)(36)=36$, $K_f=\\tfrac12(4)(9)=18$.",
         ["stays 36 J", "doubles", "becomes zero"]),
        ("A bullet hits the rim of a rest disk and embeds. Conserved about the axle (if axle force has no torque) is",
         "angular momentum", "Linear $P$ is not conserved because the axle can impulse.",
         ["linear P always", "KE always", "I always"]),
        ("Skater $I\\omega=12$. If $I$ becomes $3$, $\\omega=$",
         "4 rad/s", "$12/3=4$.",
         ["12 rad/s", "3 rad/s", "36 rad/s"]),
        ("Dropping mass onto a spinning merry-go-round increases $I$ and",
         "decreases ω if L is conserved", "People walking in from rest add mass at the current $\\omega$ only after friction brings them up — typically $L$ of the system about the axle is conserved if the axle's $\\tau$ is zero.",
         ["increases ω always", "stops L conservation", "changes g"]),
        ("Atwood with massive pulley: $a=\\dfrac{(m_1-m_2)g}{m_1+m_2+I/R^2}$. Extra $I/R^2$ is",
         "the pulley's inertia referred to the string", "From $\\tau=TR$ and $\\alpha=a/R$.",
         ["air drag", "a fictitious mass of Earth", "tension"]),
        ("$m_1=5$, $m_2=3$, $g=10$, $I=0.4$, $R=0.2$ (SI). $I/R^2=$",
         "10 kg", "$0.4/0.04=10$.",
         ["2 kg", "0.08 kg", "50 kg"]),
        ("For those numbers, $a=$",
         "10/9 m/s^2", "$a=20/(8+10)=20/18=10/9$.",
         ["2.5 m/s^2", "10 m/s^2", "20 m/s^2"]),
        ("Light pulley would have given $a=2.5\\,\\mathrm{m/s}^2$. The massive pulley makes $a$",
         "smaller", "Denominator grew.",
         ["larger", "unchanged", "equal to g"]),
        ("Constraint still says $a_1=-a_2$ and $\\alpha=a/R$ if the string does not slip on the pulley. That last piece needs",
         "static friction or a wrapping without slip", "Otherwise $\\alpha$ is independent of $a$.",
         ["gravity to vanish", "I=0", "T=0"]),
        ("A rotation FRQ justification should name",
         "the axis and why τ_ext is zero or not", "Conservation claims are axis-specific.",
         ["Gauss's law", "the current in a circuit", "the optical axis"]),
        ("To claim $L$ conserved about a point, show",
         "net external torque about that point is zero", "Then $dL/dt=0$.",
         ["KE is constant", "mass is constant", "θ is small"]),
        ("Rolling without slipping as a justification sentence is",
         "v_cm = ω R because the contact point does not slide", "State the geometric constraint explicitly.",
         ["friction is μN always kinetic", "I=MR^2 always", "a=g"]),
        ("Using energy on a massive pulley, you must include",
         "½ I ω^2 of the pulley", "With $\\omega=v/R$.",
         ["only mgh of Earth", "Gauss flux", "heat of fusion"]),
        ("Sign convention on an FRQ: pick",
         "one positive rotation sense and keep it", "Then $\\tau$, $\\alpha$, $\\omega$, $L$ share that sign.",
         ["a new sign each line", "degrees for α", "I as negative"]),
        ("$L=mvr$ for a particle if $\\vec r\\perp\\vec v$. A $2\\,\\mathrm{kg}$ mass at $3\\,\\mathrm{m/s}$ at $4\\,\\mathrm{m}$ perpendicular: $L=$",
         "24 kg m^2/s", "$2\\times 3\\times 4=24$.",
         ["9", "6", "12"]),
        ("$\\tau=dL/dt$ with $L=6t^3$. $\\tau$ at $t=1$ is",
         "18 N·m", "$18t^2$ at $t=1$ is $18$.",
         ["6 N·m", "3 N·m", "18t N·m"]),
        ("Person plus stool $I=3$, wheel $I=0.5$ at $\\omega=8$ vertical. If the wheel is inverted (ω flips), stool $\\omega_s$ from rest satisfies $0.5(8)+3(0)=0.5(-8)+3\\omega_s$. Then $\\omega_s=$",
         "8/3 rad/s", "$4=-4+3\\omega_s$, $3\\omega_s=8$, $\\omega_s=8/3$.",
         ["8 rad/s", "4 rad/s", "0"]),
        ("Two disks stick: $I_1\\omega_1=(I_1+I_2)\\omega_f$ assumes",
         "no external τ about the shared axis", "Friction between disks is internal.",
         ["KE conserved", "linear P conserved about a wall", "I=0"]),
        ("A planet's $L$ about the sun is constant if gravity is central, because",
         "τ = r × F and F is along -r", "Cross product of parallel vectors is zero.",
         ["mass is zero", "orbits are always circles", "Kepler forbade torque"]),
        ("$K=L^2/(2I)$. If $L$ is fixed and $I$ drops, $K$",
         "rises", "The skater does positive work pulling masses inward.",
         ["falls", "is L", "is I"]),
        ("Massive Atwood: tensions on two sides differ if the pulley has $\\alpha\\ne 0$, because",
         "net τ = (T1-T2)R = I α", "A massless pulley would force $T_1=T_2$.",
         ["gravity is different on each mass", "strings stretch by g", "I must be zero"]),
        ("If a string slips on a pulley, you cannot write",
         "α = a/R", "That is the no-slip rolling-type constraint.",
         ["F=mg", "I=∫r^2 dm", "L=Iω about the axle if you still have ω"]),
        ("Choosing the CM as origin for $L=\\sum r_i\\times p_i$ of a rigid body in the CM frame recovers",
         "L = I_cm ω", "That is the rigid-body reduction.",
         ["L=0 always", "L=M v_cm", "L=τ t always"]),
        ("A tumbling object with $\\tau_\\mathrm{ext}=0$ keeps",
         "total L vector constant", "It may look messy but $\\vec L$ is fixed in an inertial frame.",
         ["θ constant", "I constant always", "ω along every axis"]),
        ("Bullet $m v d$ angular momentum about a disk axle (impact parameter $d$) becomes $I\\omega$ after embedding if",
         "the axle exerts no torque (force through axis)", "Linear momentum is dumped into the axle.",
         ["KE is conserved", "the disk is frictionless at the embed point — then it would not catch", "g=0 is required"]),
        ("$I/R^2$ has units of",
         "mass", "$(kg m^2)/m^2=kg$.",
         ["time", "radians", "watts"]),
        ("Skater work goes into extra $K_\\mathrm{rot}$ because",
         "centrifugal-in-skater-frame muscles do work, or in inertial frame the hands have a radial v component while F is inward", "Energy is not conserved as a closed $I\\omega$ only system; the skater is doing work.",
         ["L is not conserved", "mass increases", "g does work"]),
        ("For FRQ graphs of $L(t)$, $\\tau$ is the",
         "slope", "$\\tau=dL/dt$.",
         ["area only", "height of L", "intercept"]),
        ("Area under $\\tau(t)$ is",
         "ΔL", "Impulse of torque.",
         ["Δθ always", "I", "ω"]),
        ("A hoop rolling about its CM has $L_\\mathrm{cm}=I_\\mathrm{cm}\\omega=MR^2(v/R)=MvR$. About the contact point, $L=$",
         "2 M v R", "$I_p=2MR^2$, $\\omega=v/R$, $L=2MvR$.",
         ["M v R", "½ M v R", "0"]),
        ("AP Stretch: $L=6t^2$ (SI). $\\tau$ at $t=3$ is",
         "36 N·m", "$\\tau=12t=36$.",
         ["6 N·m", "18 N·m", "54 N·m"]),
        ("AP Stretch: Disk $I=6$ at $\\omega=5$ sticks to a rest disk $I=4$. They then share $\\omega$. $\\omega_f=$",
         "3 rad/s", "$L_i=30$, $I_f=10$, so $\\omega_f=3\\,\\mathrm{rad/s}$.",
         ["5 rad/s", "2.5 rad/s", "9 rad/s"]),
        ("AP Stretch: Atwood $m_1=7$, $m_2=3$, $g=10$, pulley $I=0.60$, $R=0.20$ (SI). Find $a$.",
         "1.6 m/s^2", "$I/R^2=0.60/0.04=15$. Then $a=(7-3)10/(7+3+15)=40/25=1.6\\,\\mathrm{m/s}^2$.",
         ["4 m/s^2", "2.5 m/s^2", "10/7 m/s^2"]),
        ("AP Stretch: $I$ drops from $8$ to $2$ at constant $L=16$. $\\Delta K=$",
         "48 J", "$K=L^2/(2I)$: $256/16=16$ initially, $256/4=64$ finally, $\\Delta K=48\\,\\mathrm{J}$.",
         ["0", "16 J", "64 J"]),
        ("AP Stretch: Particle $m=2$, $\\vec r=(3,0)$, $\\vec v=(0,4)$. $L_z=m(xv_y-yv_x)=$",
         "24", "$2(3\\times 4-0)=24$.",
         ["8", "12", "0"]),
        ("AP Stretch: Massive pulley $I=0.72$, $R=0.30$, $m_1=9$, $m_2=3$, $g=10$. Find $a$.",
         "3 m/s^2", "$I/R^2=0.72/0.09=8$. Then $a=(9-3)10/(9+3+8)=60/20=3\\,\\mathrm{m/s}^2$.",
         ["6 m/s^2", "5 m/s^2", "8 m/s^2"]),
        ("AP Stretch: A pivoted gyro has $m=5\\,\\mathrm{kg}$, $g=10$, $r=0.40\\,\\mathrm{m}$, $I=0.25$, $\\omega=8$. Find $\\tau$, then $L$, then $\\Omega$.",
         "10 rad/s", "$\\tau=mgr=20\\,\\mathrm{N\\cdot m}$, $L=I\\omega=2.0$, so $\\Omega=\\tau/L=10\\,\\mathrm{rad/s}$.",
         ["20 rad/s", "2 rad/s", "0.4 rad/s"]),
        ("AP Stretch: Disk $I=2.5$ at $\\omega=8$ sticks to a rest disk $I=1.5$. The ratio $K_f/K_i$ is",
         "5/8", "$L_i=20$, $I_f=4$, $\\omega_f=5$. Then $K_i=80\\,\\mathrm{J}$, $K_f=50\\,\\mathrm{J}$, ratio $50/80=5/8$.",
         ["1", "1/2", "5/4"]),
        ("AP Stretch: A $3\\,\\mathrm{kg}$ particle at $r=2\\,\\mathrm{m}$ with $v=4\\,\\mathrm{m/s}$ perpendicular to $\\vec r$ sticks to a rest arm $I=6$ about the origin. $\\omega_f=$",
         "4/3 rad/s", "$L_i=mvr=24$. $I_f=6+md^2=6+12=18$. Then $\\omega_f=24/18=4/3\\,\\mathrm{rad/s}$.",
         ["4 rad/s", "2 rad/s", "8/3 rad/s"]),
    ])
    return qs


def build_unit6():
    title = "AP Physics C Mechanics Unit 6: Rotation II and Angular Momentum"
    description = (
        "Angular momentum L=Iω and r×p, conservation, qualitative gyroscopes, collisions that change I, "
        "Atwood with a massive pulley, and FRQ justifications."
    )
    c1 = concept_block(
        "1. Angular momentum: Iω and r × p",
        [
            "Angular momentum is the rotational analog of $p$. For a rigid body about a fixed axis, $L=I\\omega$ "
            "(magnitude, with a sign). If $I=5\\,\\mathrm{kg\\,m}^2$ and $\\omega=2\\,\\mathrm{rad/s}$, $L=10\\,\\mathrm{kg\\,m}^2/\\mathrm{s}$.",
            "For a single particle, $\\vec L=\\vec r\\times\\vec p$, so $L=rp\\sin\\phi$. If $r=2\\,\\mathrm{m}$, $p=3\\,\\mathrm{kg\\,m/s}$, "
            "and $\\phi=90^\\circ$, $L=6\\,\\mathrm{kg\\,m}^2/\\mathrm{s}$. If $\\vec r\\parallel\\vec p$, $L=0$ about that origin.",
            "The rotational Newton 2 in its general form is $\\vec\\tau_\\mathrm{net}=d\\vec L/dt$, the twin of $\\vec F=d\\vec p/dt$. "
            "If $L=4t^2$, then $\\tau=8t$. At $t=2\\,\\mathrm{s}$, $\\tau=16\\,\\mathrm{N\\cdot m}$.",
            "In the CM frame of a rigid body, the internal angular momentum is $I_\\mathrm{cm}\\omega$ about the CM axis. "
            "You can add $M\\vec r_\\mathrm{cm}\\times\\vec v_\\mathrm{cm}$ if you need $L$ about another point.",
            "Units $\\mathrm{kg\\,m}^2/\\mathrm{s}$ equal $\\mathrm{N\\cdot m\\cdot s}$, matching $\\int\\tau\\,dt=\\Delta L$.",
            "Exam move: choose an origin, then either $I\\omega$ (rigid, that axis) or $r p\\sin\\phi$ (particle).",
        ],
        "Conservation of $L$ is the rotational conservation law that solves collisions with axles, skaters, and planets. "
        "You cannot write it until $L$ itself is defined.",
        "Name the axis or origin. Write $L=I\\omega$ or $L=\\vec r\\times\\vec p$. If $\\tau(t)$ is given, $L$ is its integral.",
        lesson_figure(
            _rp_svg(),
            "Particle angular momentum uses $\\vec r$ from the origin to the particle, crossed with $\\vec p$",
            "If $\\vec p$ is along $\\vec r$, the cross product vanishes. If $\\vec p$ is perpendicular, $L=rp$.",
        )
        + solved(
            1, "$I=5$, $\\omega=2$ (SI). Find $L$.",
            [
                "$L=I\\omega$.",
                "$L=10\\,\\mathrm{kg\\,m}^2/\\mathrm{s}$.",
                "Direction of $\\vec L$ is along the axis by the right-hand rule.",
            ],
            "$10\\,\\mathrm{kg\\,m}^2/\\mathrm{s}$",
            "",
            "Easy",
        )
        + solved(
            2, "Particle $r=2$, $p=3$, $\\phi=90^\\circ$. Find $L$.",
            [
                "$L=rp\\sin\\phi$.",
                "$\\sin 90^\\circ=1$.",
                "$L=6\\,\\mathrm{kg\\,m}^2/\\mathrm{s}$.",
            ],
            "$6\\,\\mathrm{kg\\,m}^2/\\mathrm{s}$",
            "",
            "Medium",
        )
        + solved(
            3, "$L=4t^2$. Find $\\tau$ at $t=2\\,\\mathrm{s}$.",
            [
                "$\\tau=dL/dt=8t$.",
                "At $t=2$, $\\tau=16\\,\\mathrm{N\\cdot m}$.",
                "Check: $\\Delta L=\\int\\tau\\,dt$ would recover $4t^2$ plus a constant.",
            ],
            "$16\\,\\mathrm{N\\cdot m}$",
            "",
            "Hard",
        )
        + _ican([
            "I can compute $L=I\\omega$ for a rigid body about a fixed axis.",
            "I can compute $L=rp\\sin\\phi$ for a particle.",
            "I can use $\\tau=dL/dt$.",
        ]),
        ("Writing $L=I v$ or $L=m\\omega$",
         "The rigid-body formula is $I\\omega$ with $I$ in $\\mathrm{kg\\,m}^2$ and $\\omega$ in $\\mathrm{rad/s}$. Mixing linear $v$ without an $r$ is a units crash."),
        ("Circle the origin on the figure before computing $\\vec r\\times\\vec p$",
         "A different origin gives a different $L$. The axis in $I\\omega$ is the same choice."),
        [
            "I can compute $L=I\\omega$ for a rigid body about a fixed axis.",
            "I can compute $L=rp\\sin\\phi$ for a particle.",
            "I can use $\\tau=dL/dt$.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Conservation of angular momentum",
        [
            "If the net external torque about a chosen axis is zero, $L$ about that axis is constant. "
            "That is the rotational twin of “no external impulse means $P$ constant.”",
            "Ice skater: pulling arms in decreases $I$. Then $I\\omega$ stays constant, so $\\omega$ rises. "
            "If $I$ goes from $4$ to $2$ with $L=12$, $\\omega$ goes from $3$ to $6\\,\\mathrm{rad/s}$. "
            "Kinetic energy $L^2/(2I)$ doubles; the skater’s muscles do that work.",
            "A person on a frictionless stool holding a spinning wheel can make the stool turn by flipping the wheel, "
            "because total $L$ about the vertical stays zero (or constant).",
            "Planets: gravity is central, so $\\vec\\tau=\\vec r\\times\\vec F=0$ about the sun, and Kepler’s equal-area "
            "law is $L$ conservation in disguise.",
            "During a brief collision, axle forces may destroy linear $P$ but have no torque about the axle, so $L$ "
            "about the axle can still be conserved.",
            "Justification sentence: “About the axle, the bearing force has lever arm zero, so $\\tau_\\mathrm{ext}=0$ and $L$ is conserved.”",
        ],
        "This is the highest-value rotation conservation law on the AP exam. It solves problems that $F=ma$ cannot "
        "because the internal forces are unknown.",
        "Pick the axis where external torques vanish or are negligible. Write $L_i=L_f$. Then, if needed, discuss $K$ separately.",
        lesson_figure(
            _skater_svg(),
            "A skater or a person on a frictionless stool: $L$ about the vertical axle stays constant if that axle’s external torque is zero",
            "Arms in means smaller $I$ and larger $\\omega$. Muscles do the work that raises $K=L^2/(2I)$.",
        )
        + solved(
            6, "$I=4$, $\\omega=3$, then $I=2$. Find new $\\omega$ if $L$ is conserved.",
            [
                "$L=12$ initially.",
                "$12=2\\omega$.",
                "$\\omega=6\\,\\mathrm{rad/s}$.",
            ],
            "$6\\,\\mathrm{rad/s}$",
            "",
            "Easy",
        )
        + solved(
            7, "Show that $K$ doubles in that process.",
            [
                "$K=L^2/(2I)$.",
                "$K_i=144/8=18\\,\\mathrm{J}$, $K_f=144/4=36\\,\\mathrm{J}$.",
                "The extra $18\\,\\mathrm{J}$ is work done by the skater.",
            ],
            "$K$ goes from $18\\,\\mathrm{J}$ to $36\\,\\mathrm{J}$",
            "",
            "Medium",
        )
        + solved(
            8, "Why can $L$ about a disk’s axle be conserved in a bullet-disk collision while linear $P$ is not?",
            [
                "The axle can exert a large force (impulse) on the disk.",
                "That force has essentially zero lever arm about the axle, so $\\tau_\\mathrm{ext}\\approx 0$.",
                "Thus $\\Delta L=0$ about the axle while $\\Delta P\\ne 0$ for the disk-plus-bullet system if the axle is outside the system.",
            ],
            "Axle impulse has no torque about itself; it can still change linear $P$.",
            "",
            "Hard",
        )
        + _ican([
            "I can state $L$ conservation when $\\tau_\\mathrm{ext}=0$.",
            "I can solve skater $I\\omega$ problems, including the $K$ increase.",
            "I can justify $L$ vs $P$ conservation about an axle.",
        ]),
        ("Conserving $K$ automatically with $L$",
         "Pulling arms in is not an isolated energy system. $L$ is conserved; $K$ rises because work is done."),
        ("Name the axis in the conservation sentence",
         "“$L$ is conserved” is incomplete. “$L$ about the vertical axle is conserved because $\\tau_\\mathrm{ext}=0$ there” earns the point."),
        [
            "I can state $L$ conservation when $\\tau_\\mathrm{ext}=0$.",
            "I can solve skater $I\\omega$ problems, including the $K$ increase.",
            "I can justify $L$ vs $P$ conservation about an axle.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Gyroscopic motion, qualitative",
        [
            "A fast-spinning wheel has a large $\\vec L$ along its axle. Gravity on the CM, if the axle is supported "
            "at one end, produces a horizontal torque $\\tau=mgr$ (lever arm the horizontal distance from pivot to CM). "
            "Instead of falling, the wheel’s $\\vec L$ slowly changes direction: that motion is precession.",
            "Why: $\\vec\\tau=d\\vec L/dt$ says the increment $d\\vec L$ is parallel to $\\vec\\tau$, hence perpendicular "
            "to $\\vec L$ for this geometry. The tip of $\\vec L$ moves sideways, not downward.",
            "The slow-precession rate is $\\Omega=\\tau/L=mgr/(I\\omega)$. Larger spin means slower precession. "
            "Numeric: $m=2$, $g=10$, $r=0.15$, $I=0.08$, $\\omega=25$ give $\\tau=3$, $L=2$, $\\Omega=1.5\\,\\mathrm{rad/s}$.",
            "A non-spinning wheel on the same pivot simply falls: there is no large $L$ for $\\tau$ to turn sideways.",
            "AP Physics C Mechanics asks for this story, not a full Euler-angle treatment. Right-hand rule plus "
            "$\\tau=dL/dt$ is the scoring language.",
            "Nutation (bobbing) exists in real gyros; you may mention it as a higher-order effect if the exam shows a wobble, but the default model is steady precession.",
        ],
        "This is the showpiece of $\\vec\\tau=d\\vec L/dt$ as a vector equation, not merely $\\tau=I\\alpha$ about a fixed axle.",
        "Draw $\\vec L$ along the spin axle. Draw $\\vec\\tau=\\vec r\\times m\\vec g$. The wheel precesses so that $d\\vec L$ follows $\\vec\\tau$. Quote $\\Omega=\\tau/L$ if a rate is asked.",
        lesson_figure(
            _gyro_svg(),
            "A pivoted gyroscope: $\\vec L$ along the spin axle, $\\vec\\tau=\\vec r\\times m\\vec g$, and slow precession $\\Omega$",
            "Gravity’s torque is horizontal. $d\\vec L$ follows $\\vec\\tau$, so the axle walks around the pivot instead of falling. There is no rolling constraint here.",
        )
        + solved(
            11, "Why doesn’t a fast gyroscope simply fall like a non-spinning wheel?",
            [
                "Spin means a large $\\vec L$ along the axle.",
                "Gravity’s $\\vec\\tau$ is perpendicular to that $\\vec L$.",
                "$d\\vec L$ is therefore sideways: precession, not a downward flop of $L$.",
            ],
            "Torque changes the direction of $\\vec L$, not its magnitude, in the simple model.",
            "",
            "Easy",
        )
        + solved(
            12, "How does $\\Omega$ depend on $\\omega$ in $\\Omega=mgr/(I\\omega)$?",
            [
                "$\\Omega\\propto 1/\\omega$.",
                "Faster spin, slower precession.",
                "If $\\omega\\to 0$, the formula leaves the slow-precession regime and the wheel falls.",
            ],
            "$\\Omega$ decreases as spin increases",
            "",
            "Medium",
        )
        + solved(
            13, "$m=2\\,\\mathrm{kg}$, $g=10$, $r=0.15\\,\\mathrm{m}$, $I=0.08$, $\\omega=25$. Find $\\Omega$.",
            [
                "$\\tau=mgr=2\\times 10\\times 0.15=3\\,\\mathrm{N\\cdot m}$.",
                "$L=I\\omega=2.0\\,\\mathrm{kg\\,m}^2/\\mathrm{s}$.",
                "$\\Omega=\\tau/L=1.5\\,\\mathrm{rad/s}$.",
            ],
            "$1.5\\,\\mathrm{rad/s}$",
            "",
            "Hard",
        )
        + _ican([
            "I can explain precession with $\\tau=dL/dt$.",
            "I can use $\\Omega=mgr/(I\\omega)$ in the slow-precession model.",
            "I can contrast a spinning gyro with a falling non-spinning wheel.",
        ]),
        ("Saying the spinning wheel has no torque from gravity",
         "Gravity still produces $\\tau=mgr$. Spin does not cancel gravity; it redirects how $\\vec L$ responds."),
        ("Draw $L$, $\\tau$, and $dL$ as three arrows before writing $\\Omega$",
         "The vector picture is the justification. The formula is only the magnitude of the precession rate."),
        [
            "I can explain precession with $\\tau=dL/dt$.",
            "I can use $\\Omega=mgr/(I\\omega)$ in the slow-precession model.",
            "I can contrast a spinning gyro with a falling non-spinning wheel.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Collisions that change I",
        [
            "When two coaxial disks rub and then rotate together, or a person drops onto a merry-go-round, $I$ of "
            "the system about the axle jumps. If $\\tau_\\mathrm{ext}=0$ about that axle, $I_1\\omega_1=I_f\\omega_f$ "
            "with $I_f=I_1+I_2$ when they finally share $\\omega$.",
            "Example: disk $I=2$ at $\\omega=6$ drops onto a rest disk $I=2$. Then $12=4\\omega_f$ so $\\omega_f=3\\,\\mathrm{rad/s}$. "
            "Rotational KE drops from $36\\,\\mathrm{J}$ to $18\\,\\mathrm{J}$ (inelastic in the rotational sense).",
            "A bullet embedding in a rim uses $m v d = I\\omega$ about the axle (impact parameter $d$), not $mv=MV$.",
            "If someone walks from the rim toward the center of a spinning platform, $I$ decreases continuously and "
            "$\\omega$ rises, like the skater, provided they stay on the platform (internal forces).",
            "Linear $P$ of disk-plus-bullet is generally not conserved (axle impulse). Always ask which conservation law matches which axis.",
            "FRQ: “They eventually rotate as one” means a rotationally inelastic collision with $L$ conserved about the axle.",
        ],
        "These problems combine Unit 4 collisions with Unit 5’s $I$. The new feature is that $I$ after contact is a sum.",
        "Write $L_i=L_f$ about the axle. Construct $I_f$ after sticking. Check $K$ only if asked; it usually falls.",
        lesson_figure(
            _coaxial_svg(),
            "Two coaxial disks on one axle: the upper disk is spinning, the lower is at rest, then they stick",
            "Friction between the disks is internal to the pair. Add $I$ after they share $\\omega$, and conserve $L$ about the axle.",
        )
        + solved(
            16, "Disk $I=2$ at $\\omega=6$ sticks to rest disk $I=2$. Find $\\omega_f$.",
            [
                "$L_i=12$.",
                "$I_f=4$.",
                "$\\omega_f=3\\,\\mathrm{rad/s}$.",
            ],
            "$3\\,\\mathrm{rad/s}$",
            "",
            "Easy",
        )
        + solved(
            17, "Find $K_i$ and $K_f$ for that stick.",
            [
                "$K_i=\\tfrac12(2)(36)=36\\,\\mathrm{J}$.",
                "$K_f=\\tfrac12(4)(9)=18\\,\\mathrm{J}$.",
                "Half the rotational KE became thermal.",
            ],
            "$36\\,\\mathrm{J}$ then $18\\,\\mathrm{J}$",
            "",
            "Medium",
        )
        + solved(
            18, "Disk $I=3$ at $\\omega=8$ couples to rest $I=1$. Find $\\omega_f$.",
            [
                "$L_i=24$.",
                "$I_f=4$.",
                "$\\omega_f=6\\,\\mathrm{rad/s}$.",
            ],
            "$6\\,\\mathrm{rad/s}$",
            "",
            "Hard",
        )
        + _ican([
            "I can conserve $L$ when two coaxial objects stick.",
            "I can compute the drop in rotational $K$.",
            "I can explain why the axle may break linear-$P$ conservation.",
        ]),
        ("Using $m_1 v_1=m_2 v_2$ on a disk collision about an axle",
         "That is linear momentum. The axle is an external force. Use $I\\omega$ about the axle instead."),
        ("Add the $I$ values only after they share $\\omega$",
         "Before contact they have separate $\\omega$. After sticking, one $\\omega$ and $I_1+I_2$."),
        [
            "I can conserve $L$ when two coaxial objects stick.",
            "I can compute the drop in rotational $K$.",
            "I can explain why the axle may break linear-$P$ conservation.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Atwood machine with a massive pulley",
        [
            "If the pulley has moment of inertia $I$ and radius $R$, and the string does not slip, then "
            "$\\alpha=a/R$ and the two tensions are not equal: $(T_1-T_2)R=I\\alpha$. Combining with the two mass FBDs "
            "gives $a=\\dfrac{(m_1-m_2)g}{m_1+m_2+I/R^2}$.",
            "The term $I/R^2$ has units of mass: it is the pulley’s inertia referred to the linear motion of the string. "
            "For $I=0.4\\,\\mathrm{kg\\,m}^2$ and $R=0.2\\,\\mathrm{m}$, $I/R^2=10\\,\\mathrm{kg}$.",
            "With $m_1=5\\,\\mathrm{kg}$, $m_2=3\\,\\mathrm{kg}$, $g=10$, $a=20/(8+10)=10/9\\,\\mathrm{m/s}^2$, "
            "smaller than the light-pulley $2.5\\,\\mathrm{m/s}^2$.",
            "Energy check: $m_1 gh-m_2 gh=\\tfrac12 m_1 v^2+\\tfrac12 m_2 v^2+\\tfrac12 I(v/R)^2$. Same $a$ after a derivative.",
            "If the string slips, drop $\\alpha=a/R$ and treat kinetic friction on the rim as a separate torque. AP usually assumes no slip.",
            "Massless pulley is the $I=0$ limit, recovering Unit 2.",
        ],
        "This is the standard “systems plus rotation” FRQ: two translations and one rotation, linked by a constraint.",
        "Write three equations: Newton 2 for each mass, $\\tau=I\\alpha$ for the pulley, plus $a=\\alpha R$. Add them to eliminate tensions.",
        lesson_figure(
            _pulley_mass_svg(),
            "Massive pulley: $I$ on the wheel, unequal tensions, constraint $\\alpha=a/R$",
            "The shaded pulley is not a light hoop. Its $I$ enlarges the denominator of $a$ by $I/R^2$.",
        )
        + solved(
            21, "$I=0.4$, $R=0.2$. Find $I/R^2$.",
            [
                "$R^2=0.04$.",
                "$I/R^2=10\\,\\mathrm{kg}$.",
                "This adds to $m_1+m_2$ in the denominator of $a$.",
            ],
            "$10\\,\\mathrm{kg}$",
            "",
            "Easy",
        )
        + solved(
            22, "$m_1=5$, $m_2=3$, $g=10$, $I/R^2=10$. Find $a$.",
            [
                "Numerator $(5-3)10=20$.",
                "Denominator $8+10=18$.",
                "$a=20/18=10/9\\,\\mathrm{m/s}^2$.",
            ],
            "$10/9\\,\\mathrm{m/s}^2$",
            "",
            "Medium",
        )
        + solved(
            23, "$m_1=4$, $m_2=2$, $g=10$, $I/R^2=2$. Find $a$.",
            [
                "Numerator $20$.",
                "Denominator $6+2=8$.",
                "$a=20/8=2.5\\,\\mathrm{m/s}^2$.",
            ],
            "$2.5\\,\\mathrm{m/s}^2$",
            "",
            "Hard",
        )
        + _ican([
            "I can write $a=(m_1-m_2)g/(m_1+m_2+I/R^2)$.",
            "I can explain why tensions differ on a massive pulley.",
            "I can include $\\tfrac12 I\\omega^2$ in an energy check.",
        ]),
        ("Using the light-pulley $a$ when $I$ is given",
         "You would overestimate $a$. The pulley must be angularly accelerated too."),
        ("Eliminate $T$ by adding the two mass equations and the pulley equation",
         "After substituting $\\alpha=a/R$, $T$ terms become the pulley’s $I a/R^2$ contribution."),
        [
            "I can write $a=(m_1-m_2)g/(m_1+m_2+I/R^2)$.",
            "I can explain why tensions differ on a massive pulley.",
            "I can include $\\tfrac12 I\\omega^2$ in an energy check.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Justifying rotation FRQs",
        [
            "AP Physics C rotation FRQs award points for justifications, not only for formulas. A complete claim "
            "names the object, the axis, and the law, then the reason the law applies.",
            "Template for $L$ conservation: “About the [named] axis, the [bearing/axle/gravity] force has zero lever arm "
            "(or is internal), so $\\tau_\\mathrm{net}^\\mathrm{ext}=0$ and $L_i=L_f$.”",
            "Template for rolling: “The string/surface does not slip, so $v=\\omega R$ (and $a=\\alpha R$).” "
            "Then either energy or Newton plus $\\tau=I\\alpha$.",
            "Template for energy: “The axle is fixed and friction at a static contact point does no work, so "
            "$K_\\mathrm{trans}+K_\\mathrm{rot}+U$ is constant,” or include $W_\\mathrm{nc}$ if kinetic friction is present.",
            "Sign convention: “Counterclockwise is positive for $\\tau,\\alpha,\\omega,L$.” One sentence prevents later contradictions.",
            "If you use a catalog $I$, name the shape and axis: “Disk about its central axis, $I=\\tfrac12 MR^2$.” "
            "If you shift the axis, cite the parallel-axis theorem with the value of $d$.",
        ],
        "Calculus and algebra cannot rescue a missing justification on the rubric. This concept is how you convert "
        "correct physics into earned points.",
        "Before computing, write three labeled sentences: axis, conservation or Newton law, constraint. Then do the math.",
        lesson_figure(
            fbd_box(labels=("mg", "T", "f_s")),
            "An FRQ figure deserves an FBD plus a declared axis before any $I\\alpha$ equation",
            "Forces on the FBD become torques about your stated axis. Undeclared axes lose the justification point.",
        )
        + solved(
            26, "Write a one-sentence justification that $L$ is conserved about a pulley axle during a brief collision.",
            [
                "Name the axle.",
                "Note that the axle force has zero lever arm.",
                "Conclude $\\tau_\\mathrm{ext}=0$ so $L$ about the axle is constant.",
            ],
            "About the axle, the bearing force has lever arm zero, so $\\tau_\\mathrm{ext}=0$ and $L$ is conserved.",
            "",
            "Easy",
        )
        + solved(
            27, "Write the rolling-constraint justification.",
            [
                "State no slipping.",
                "Translate to $v_\\mathrm{cm}=\\omega R$.",
                "If accelerations are needed, also $a=\\alpha R$.",
            ],
            "No slip implies $v_\\mathrm{cm}=\\omega R$ (and $a_\\mathrm{cm}=\\alpha R$).",
            "",
            "Medium",
        )
        + solved(
            28, "A student writes “energy is conserved” for a skater pulling arms in. Repair the justification.",
            [
                "Mechanical $K$ of rotation is not constant; the skater does work.",
                "What is conserved is $L=I\\omega$ about the vertical if ice friction’s torque is negligible.",
                "A correct pair: $L$ conserved; $K$ increases by the work of the skater.",
            ],
            "$L$ conserved about the vertical; $K$ not conserved because the skater does work.",
            "",
            "Hard",
        )
        + _ican([
            "I can write an axis-specific $L$-conservation justification.",
            "I can state the no-slip constraint in words and symbols.",
            "I can avoid claiming energy conservation when a person does work.",
        ]),
        ("Writing “because of inertia” as a justification",
         "Inertia is not a law application. Name $\\tau=dL/dt$, $L$ conservation, $\\tau=I\\alpha$, or a constraint."),
        ("Lead with the law, then the reason, then the algebra",
         "Rubrics often have a dedicated justification point that algebra cannot substitute."),
        [
            "I can write an axis-specific $L$-conservation justification.",
            "I can state the no-slip constraint in words and symbols.",
            "I can avoid claiming energy conservation when a person does work.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        [
            "Compute $L=I\\omega$ and $L=\\vec r\\times\\vec p$",
            "Conserve $L$ when $\\tau_\\mathrm{ext}=0$",
            "Explain gyroscope precession qualitatively",
            "Handle collisions that change $I$",
            "Solve Atwood problems with a massive pulley",
            "Write AP-style justifications for rotation laws",
        ],
        c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Oscillations
# ===========================================================================

def _u7_questions():
    qs = []
    _add(qs, [
        ("Hooke's law is $F=-kx$. If $k=50\\,\\mathrm{N/m}$ and $x=0.10\\,\\mathrm{m}$, $F=$",
         "-5 N", "$F=-5\\,\\mathrm{N}$, toward equilibrium.",
         ["5 N", "-50 N", "0"]),
        ("SHM angular frequency for a mass-spring is $\\omega=\\sqrt{k/m}$. If $k=32$ and $m=2$ (SI), $\\omega=$",
         "4 rad/s", "$\\sqrt{16}=4$.",
         ["16 rad/s", "8 rad/s", "2 rad/s"]),
        ("Period $T=2\\pi/\\omega$. For $\\omega=4\\,\\mathrm{rad/s}$, $T=$",
         "π/2 s", "$2\\pi/4=\\pi/2\\,\\mathrm{s}$.",
         ["4 s", "2π s", "π s"]),
        ("If $m$ quadruples and $k$ is fixed, $T$",
         "doubles", "$T=2\\pi\\sqrt{m/k}\\propto\\sqrt{m}$.",
         ["quadruples", "halves", "is unchanged"]),
        ("Equilibrium of the spring is where $F=0$, i.e. $x=$",
         "0 if x is from the unstretched length (horizontal spring)", "Vertical springs shift the equilibrium by $mg/k$, and SHM is about that new zero.",
         ["A", "k", "infinity"]),
        ("The SHM differential equation is $\\ddot x+\\omega^2 x=0$. A solution is",
         "x=A cos(ωt+φ)", "Second derivative brings down $-\\omega^2$.",
         ["x=A t^2", "x=e^{ωt}", "x=A ω t"]),
        ("If $x=4\\cos(2t)$, then $\\omega=$",
         "2 rad/s", "The coefficient of $t$ inside cosine is $\\omega$.",
         ["4 rad/s", "8 rad/s", "1 rad/s"]),
        ("For $x=4\\cos(2t)$, $v=dx/dt$ at $t=0$ is",
         "0", "$v=-8\\sin(2t)$, $\\sin 0=0$.",
         ["-8 m/s", "4 m/s", "8 m/s"]),
        ("For $x=4\\cos(2t)$, $a$ at $t=0$ is",
         "-16 m/s^2", "$a=-16\\cos(2t)$. At $t=0$, $a=-16$.",
         ["-4 m/s^2", "16 m/s^2", "0"]),
        ("$a=-\\omega^2 x$ is the hallmark of SHM. If $\\omega=3$ and $x=2$, $a=$",
         "-18 m/s^2", "$-9\\times 2=-18$.",
         ["-6 m/s^2", "18 m/s^2", "9 m/s^2"]),
        ("Total mechanical energy in SHM is $\\tfrac12 k A^2$. If $k=8$ and $A=4$, $E=$",
         "64 J", "$\\tfrac12(8)(16)=64$.",
         ["32 J", "16 J", "8 J"]),
        ("At $x=0$ (through equilibrium), $U_\\mathrm{spring}=0$ (usual zero) so $K=$",
         "E", "All energy is kinetic; $v=\\pm A\\omega$.",
         ["0", "½ E", "U"]),
        ("At an endpoint $x=\\pm A$, $K=$",
         "0", "Turning points; $U=E$.",
         ["E", "½ k A", "mgh always"]),
        ("$v_\\mathrm{max}=A\\omega$. If $A=0.20\\,\\mathrm{m}$ and $\\omega=10\\,\\mathrm{rad/s}$, $v_\\mathrm{max}=$",
         "2 m/s", "$0.20\\times 10=2$.",
         ["0.02 m/s", "10 m/s", "50 m/s"]),
        ("$E=\\tfrac12 m v_\\mathrm{max}^2$ also. If $m=2$ and $v_\\mathrm{max}=4$, $E=$",
         "16 J", "$\\tfrac12(2)(16)=16$.",
         ["8 J", "4 J", "32 J"]),
        ("A physical pendulum has $T=2\\pi\\sqrt{I/(mgd)}$ where $d$ is",
         "distance from pivot to CM", "Torque is $-mgd\\sin\\theta$; $I$ is about the pivot.",
         ["the length of a string only", "the amplitude", "the period"]),
        ("Uniform rod about one end: $I=ML^2/3$, $d=L/2$, so $T=$",
         "2π √(2L/3g)", "$I/(mgd)=(ML^2/3)/(Mg L/2)=2L/(3g)$.",
         ["2π √(L/g)", "2π √(L/3g)", "2π √(3L/2g)"]),
        ("If $I$ about the pivot increases at fixed $m,d$, the physical pendulum",
         "slows (T increases)", "$T\\propto\\sqrt{I}$.",
         ["speeds up", "stops using gravity", "has ω=0 always"]),
        ("A simple pendulum is a physical pendulum with $I=mL^2$ and $d=L$, recovering",
         "T=2π √(L/g)", "The catalog simple-pendulum result.",
         ["T=2π √(g/L)", "T=2π √(k/m)", "T=2π I"]),
        ("Physical vs simple: a real rod is physical because",
         "mass is distributed, so I is not mL^2 with L to a point bob", "You must use the actual $I$ about the pivot.",
         ["g is different", "air is required", "θ cannot be small"]),
        ("The exact pendulum equation is $\\ddot\\theta+(g/L)\\sin\\theta=0$. Small-angle SHM uses",
         "sinθ ≈ θ with θ in radians", "Then $\\omega=\\sqrt{g/L}$.",
         ["sinθ ≈ 1", "θ in degrees in the DE", "sinθ ≈ θ^2"]),
        ("For $L=1.0\\,\\mathrm{m}$ and $g=10$, small-angle $\\omega=$",
         "√10 rad/s", "$\\sqrt{g/L}=\\sqrt{10}$.",
         ["10 rad/s", "1 rad/s", "√1 rad/s"]),
        ("Small-angle $T$ for that pendulum is about",
         "2π/√10 s", "$T=2\\pi/\\omega$.",
         ["√10 s", "2 s", "10 s"]),
        ("The small-angle replacement fails when",
         "θ is many tenths of a radian", "Then $\\sin\\theta<\\theta$ and the motion is slower than SHM predicts.",
         ["L is 1 m", "g is 10", "the bob has mass"]),
        ("Amplitude of a simple pendulum does not appear in the small-angle $T$, unlike a large-amplitude real pendulum which",
         "has a slightly longer T", "A standard beyond-SHM correction.",
         ["has T=0", "stops oscillating", "has T independent of g"]),
        ("Light damping makes the amplitude",
         "decay slowly in time", "Envelope $e^{-(b/2m)t}$ for linear drag.",
         ["grow forever", "stay exactly A", "become negative mass"]),
        ("Driven SHM at the natural $\\omega_0$ (light damping) produces",
         "large amplitude (resonance)", "The driver replenishes energy each cycle.",
         ["zero amplitude", "infinite ω", "no motion of the driver"]),
        ("Overdamped motion",
         "returns to equilibrium without oscillating", "Two real exponential roots.",
         ["oscillates faster than undamped", "has constant A", "is SHM with ω doubled"]),
        ("The energy of a damped oscillator",
         "decreases as drag does negative work", "Mechanical $E$ is not constant.",
         ["increases automatically", "is ½ k A^2 forever", "is purely U"]),
        ("To stay at constant amplitude with damping you need",
         "a driving force supplying energy", "That is the driven oscillator.",
         ["larger g only", "I=0", "negative k"]),
        ("$k=200$, $m=8$. $\\omega=$",
         "5 rad/s", "$\\sqrt{25}=5$.",
         ["25 rad/s", "√200 rad/s", "8 rad/s"]),
        ("$x=3\\cos(5t)$. Amplitude is",
         "3 m", "The factor in front of cosine.",
         ["5 m", "15 m", "3/5 m"]),
        ("For that motion $v_\\mathrm{max}=$",
         "15 m/s", "$A\\omega=15$.",
         ["3 m/s", "5 m/s", "8 m/s"]),
        ("$E=\\tfrac12 k A^2$ with $k=50$, $A=0.2$ is",
         "1 J", "$\\tfrac12(50)(0.04)=1$.",
         ["5 J", "10 J", "0.2 J"]),
        ("At $x=A/2$ in SHM, $U=\\tfrac12 k(A/2)^2=E/4$. Therefore $K=$",
         "3E/4", "$U=E/4$ because $U\\propto x^2$, so $K=3E/4$.",
         ["E/2", "E/4", "E"]),
        ("$x=2\\sin(3t)$. Then $\\omega=$",
         "3 rad/s", "Coefficient of $t$ in the sine.",
         ["2 rad/s", "6 rad/s", "1 rad/s"]),
        ("For $x=2\\sin(3t)$, $a(0)=$",
         "0", "$a=-18\\sin(3t)$, so $a(0)=0$.",
         ["-18 m/s^2", "2 m/s^2", "-6 m/s^2"]),
        ("A pendulum $L=0.40\\,\\mathrm{m}$, $g=10$. Small-angle $T=$",
         "2π √(0.04) s", "$T=2\\pi\\sqrt{L/g}=2\\pi\\sqrt{0.04}=2\\pi(0.2)$.",
         ["2π √0.4 s", "0.4 s", "4π s"]),
        ("Physical pendulum: doubling $I$ at fixed $m,d$ multiplies $T$ by",
         "√2", "$T\\propto\\sqrt{I}$.",
         ["2", "1/2", "4"]),
        ("$F=-32x$ on $m=2$. This is SHM with $\\omega=$",
         "4 rad/s", "$\\omega^2=k/m=32/2=16$.",
         ["32 rad/s", "16 rad/s", "√32 rad/s"]),
        ("Phase: $x=A\\cos(\\omega t-\\pi/2)$ is the same as",
         "A sin(ω t)", "Cosine shifted by $-\\pi/2$ is sine.",
         ["A cos(ω t)", "0", "A t"]),
        ("At $x=0$ in SHM, $|a|$ is",
         "0", "$a=-\\omega^2 x=0$ at the origin, even though $|v|$ is maximum.",
         ["maximum", "A ω^2 always at x=0", "g"]),
        ("$T=0.50\\,\\mathrm{s}$ for a mass-spring. $\\omega=$",
         "4π rad/s", "$\\omega=2\\pi/T=4\\pi$.",
         ["0.5 rad/s", "2 rad/s", "π rad/s"]),
        ("Simple pendulum $T$ is independent of",
         "bob mass (small angle, point mass)", "$m$ cancels in $mgL/I$ when $I=mL^2$.",
         ["L", "g", "the small-angle assumption's validity"]),
        ("$U=\\tfrac12 kx^2$ with $k=100$, $x=0.3$. Instantaneous $U=$",
         "4.5 J", "$\\tfrac12(100)(0.09)=4.5$.",
         ["15 J", "30 J", "0.3 J"]),
        ("If $E=4.5\\,\\mathrm{J}$ and that $U=4.5\\,\\mathrm{J}$, the mass is at",
         "a turning point", "$K=0$.",
         ["equilibrium", "x=0 only if A=0", "infinity"]),
        ("AP Stretch: $x=5\\cos(4t)$. Find $a$ at $t=\\pi/8$. Note $\\cos(\\pi/2)=0$.",
         "0", "$a=-80\\cos(4t)$; $4\\times\\pi/8=\\pi/2$, $\\cos=0$.",
         ["-80 m/s^2", "5 m/s^2", "-20 m/s^2"]),
        ("AP Stretch: $x=3\\cos(4t)$ solves $m\\ddot x=-kx$ with $m=2$. Differentiate to read $\\omega$, then $k=m\\omega^2$.",
         "32 N/m", "$\\ddot x=-16x$, so $\\omega=4$. Then $k=2\\times 16=32\\,\\mathrm{N/m}$.",
         ["18 N/m", "8 N/m", "4 N/m"]),
        ("AP Stretch: $x=2\\cos(5t)$, $m=4\\,\\mathrm{kg}$. From $x(t)$ read $\\omega$ and $A$, then $k=m\\omega^2$, then $E=\\tfrac12 k A^2$.",
         "200 J", "$\\omega=5$, $A=2$, $k=4\\times 25=100$, $E=\\tfrac12(100)(4)=200\\,\\mathrm{J}$.",
         ["50 J", "100 J", "8 J"]),
        ("AP Stretch: Rod physical pendulum $T=2\\pi\\sqrt{2L/(3g)}$. If $L=1.2\\,\\mathrm{m}$, $g=10$, then $T=$",
         "2π √0.08 s", "$2L/(3g)=2.4/30=0.08$, so $T=2\\pi\\sqrt{0.08}\\,\\mathrm{s}$.",
         ["0.08 s", "2π(1.2) s", "2π √(1.2/10) s"]),
        ("AP Stretch: $\\ddot\\theta=-(g/L)\\sin\\theta$ with $\\theta=0.30\\,\\mathrm{rad}$. The SHM model would use $\\sin\\theta\\approx 0.30$, while $\\sin 0.30\\approx 0.296$. The fractional error is small, showing",
         "0.30 rad is still a decent small angle", "The linearization is already close.",
         ["degrees were required", "SHM is exact at 0.30 rad", "g/L is wrong"]),
        ("AP Stretch: Damped envelope $A(t)=A_0 e^{-t/2}$ with $A_0=8$. $A$ at $t=2\\ln 2$ is",
         "4 m", "$e^{-\\ln 2}=1/2$, so $A=4$.",
         ["8 m", "2 m", "0"]),
        ("AP Stretch: $v=dx/dt$ for $x=3e^{-0.1 t}\\cos(5t)$ at $t=0$ (product rule) is",
         "-0.3 m/s", "$v=-0.3 e^{-0.1t}\\cos(5t)-15 e^{-0.1t}\\sin(5t)$. At $t=0$, $v=-0.3$.",
         ["0", "-15 m/s", "3 m/s"]),
        ("AP Stretch: For SHM $x=A\\cos(\\omega t)$, the time-average of $K$ over a period equals",
         "E/2", "Sin-squared and cos-squared each average to $1/2$, so $\\langle K\\rangle=\\langle U\\rangle=E/2$.",
         ["E", "0", "E/4"]),
        ("AP Stretch: $I=Md^2+I_\\mathrm{cm}$ in $T=2\\pi\\sqrt{I/(mgd)}$. If $I_\\mathrm{cm}=0$ (point mass), $T=$",
         "2π √(d/g)", "$I=Md^2$, $I/(mgd)=d/g$.",
         ["2π √(g/d)", "2π d/g", "0"]),
    ])
    return qs


def build_unit7():
    title = "AP Physics C Mechanics Unit 7: Oscillations"
    description = (
        "SHM from F=-kx, the SHM differential equation, energy in SHM, physical and small-angle pendulums, "
        "and qualitative damping/driving."
    )
    c1 = concept_block(
        "1. SHM from F = -kx",
        [
            "A restoring force proportional to displacement and opposite to it, $F=-kx$, produces simple harmonic "
            "motion. Here $k$ is the spring constant in $\\mathrm{N/m}$, and $x$ is measured from the unstretched "
            "length for a horizontal spring. If $k=50\\,\\mathrm{N/m}$ and $x=+0.10\\,\\mathrm{m}$, $F=-5\\,\\mathrm{N}$.",
            "Newton 2: $m\\ddot x=-kx$, or $\\ddot x+(k/m)x=0$. The combination $\\omega=\\sqrt{k/m}$ is the angular "
            "frequency of the oscillation, in $\\mathrm{rad/s}$, not to be confused with $\\omega$ of a spinning wheel "
            "except as the same kind of derivative-of-angle idea. If $k=32$ and $m=2$, $\\omega=4\\,\\mathrm{rad/s}$.",
            "The period is $T=2\\pi/\\omega=2\\pi\\sqrt{m/k}$. For $\\omega=4$, $T=\\pi/2\\,\\mathrm{s}$. Quadrupling $m$ doubles $T$.",
            "A vertical spring still executes SHM, but the origin for $x$ is the new equilibrium where $kx_0=mg$. "
            "Gravity is absorbed into a shifted zero; the frequency remains $\\sqrt{k/m}$.",
            "Amplitude $A$ is the maximum $|x|$ and is set by initial conditions, not by $k$ and $m$. Frequency is "
            "independent of $A$ for an ideal Hooke spring — a special feature of a linear restoring force.",
            "Any device with $F=-kx$ near equilibrium (small wiggles in a $U(x)$ well) is approximately SHM, which "
            "is why this model appears far beyond springs.",
        ],
        "This is the mechanical prototype of every later oscillation in this course, including pendulums and small wiggles in a $U(x)$ well.",
        "Write $F=-kx$, then $m\\ddot x=-kx$, then $\\omega=\\sqrt{k/m}$ and $T=2\\pi/\\omega$. Measure $x$ from the actual equilibrium.",
        lesson_figure(
            spring_mass_svg(),
            "Horizontal spring-mass: $x=0$ is equilibrium, $F=-kx$ pulls back toward the dashed line",
            "Displace to the right and the spring pulls left. That opposite-to-$x$ force is the entire cause of SHM.",
        )
        + solved(
            1, "$k=32\\,\\mathrm{N/m}$, $m=2\\,\\mathrm{kg}$. Find $\\omega$ and $T$.",
            [
                "$\\omega=\\sqrt{k/m}=\\sqrt{16}=4\\,\\mathrm{rad/s}$.",
                "$T=2\\pi/\\omega=\\pi/2\\,\\mathrm{s}$.",
                "Frequency $f=1/T=2/\\pi\\,\\mathrm{Hz}$.",
            ],
            "$\\omega=4\\,\\mathrm{rad/s}$, $T=\\pi/2\\,\\mathrm{s}$",
            "",
            "Easy",
        )
        + solved(
            2, "$k=50\\,\\mathrm{N/m}$, $x=0.10\\,\\mathrm{m}$. Find $F$.",
            [
                "$F=-kx=-5\\,\\mathrm{N}$.",
                "The minus sign means toward $x=0$.",
                "If $m=2\\,\\mathrm{kg}$, $a=F/m=-2.5\\,\\mathrm{m/s}^2$ at that instant.",
            ],
            "$-5\\,\\mathrm{N}$",
            "",
            "Medium",
        )
        + solved(
            3, "Why does a vertical spring still have $\\omega=\\sqrt{k/m}$?",
            [
                "Let $x$ be from the hanging equilibrium where $k\\delta=mg$.",
                "Net force is $-k(x)$ once gravity is balanced by the extra stretch $\\delta$.",
                "The DE is again $\\ddot x+(k/m)x=0$.",
            ],
            "Gravity shifts the origin; it does not change $\\omega$.",
            "",
            "Hard",
        )
        + _ican([
            "I can write $F=-kx$ and $\\omega=\\sqrt{k/m}$.",
            "I can compute $T=2\\pi\\sqrt{m/k}$.",
            "I can shift the origin for a vertical spring.",
        ]),
        ("Using $T=2\\pi\\sqrt{k/m}$",
         "That inverts $k$ and $m$. The mass is in the numerator under the square root: heavier oscillators are slower."),
        ("Define $x=0$ at the true equilibrium before writing $F=-kx$",
         "On a hanging spring that point is not the unstretched length."),
        [
            "I can write $F=-kx$ and $\\omega=\\sqrt{k/m}$.",
            "I can compute $T=2\\pi\\sqrt{m/k}$.",
            "I can shift the origin for a vertical spring.",
        ],
        1,
    )
    c2 = concept_block(
        "2. The differential equation of SHM",
        [
            "The equation $\\ddot x+\\omega^2 x=0$ is the SHM differential equation. Its general solution is "
            "$x(t)=A\\cos(\\omega t+\\phi)$, or equivalently $A\\cos\\omega t+B\\sin\\omega t$. "
            "The two constants $A,\\phi$ (or $A,B$) are fixed by $x(0)$ and $v(0)$.",
            "If $x=4\\cos(2t)$, then $\\omega=2\\,\\mathrm{rad/s}$ and $A=4\\,\\mathrm{m}$. Velocity is the derivative: "
            "$v=-8\\sin(2t)$. At $t=0$, $v=0$. Acceleration $a=-16\\cos(2t)=-\\omega^2 x$. At $t=0$, $a=-16\\,\\mathrm{m/s}^2$.",
            "The relation $a=-\\omega^2 x$ is a test: if a problem’s $a(x)$ is a negative constant times $x$, the motion is SHM "
            "with that $\\omega$.",
            "Differentiating a cosine twice produces a minus sign twice, i.e. $+\\omega^2$ with a minus from $a=-\\omega^2 x$. "
            "Exponentials $e^{\\omega t}$ would not stay bounded; they are not SHM solutions of this undamped equation.",
            "Phase $\\phi$ slides the cosine in time. $x=A\\sin(\\omega t)$ is just $\\phi=-\\pi/2$ in the cosine form.",
            "AP calculus task: given $x(t)$, produce $v$ and $a$ at a stated $t$, and read $A$ and $\\omega$ from the formula.",
        ],
        "This is where Mechanics uses a second-order DE explicitly. Later, the small-angle pendulum is the same DE with $\\omega=\\sqrt{g/L}$.",
        "Identify $\\omega$ from the coefficient of $t$ inside the trig function. Differentiate to get $v$ and $a$. Check $a=-\\omega^2 x$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: 4 * math.cos(2 * t), 0, 6.3))],
                points=[(0, 4, "A=4"), (math.pi / 4, 0, "t=π/4")],
                xlim=(0, 6.5), ylim=(-5, 5), xlab="t (s)", ylab="x (m)",
            ),
            "$x=4\\cos(2t)$: amplitude $4\\,\\mathrm{m}$, angular frequency $2\\,\\mathrm{rad/s}$",
            "The first zero after $t=0$ is at $\\omega t=\\pi/2$, i.e. $t=\\pi/4\\,\\mathrm{s}$. Slope there is $v=-A\\omega=-8\\,\\mathrm{m/s}$.",
        )
        + solved(
            6, "$x=4\\cos(2t)$. Find $v(0)$ and $a(0)$.",
            [
                "$v=-8\\sin(2t)$, so $v(0)=0$.",
                "$a=-16\\cos(2t)$, so $a(0)=-16\\,\\mathrm{m/s}^2$.",
                "Check: $a=-\\omega^2 x=-4\\times 4=-16$ at $t=0$.",
            ],
            "$v=0$, $a=-16\\,\\mathrm{m/s}^2$",
            "",
            "Easy",
        )
        + solved(
            7, "If $a=-9x$, what is $\\omega$?",
            [
                "Compare to $a=-\\omega^2 x$.",
                "$\\omega^2=9$.",
                "$\\omega=3\\,\\mathrm{rad/s}$ (taking $\\omega>0$).",
            ],
            "$3\\,\\mathrm{rad/s}$",
            "",
            "Medium",
        )
        + solved(
            8, "$x(0)=3$, $v(0)=0$, $\\omega=5$. Write $x(t)$.",
            [
                "Cosine with $\\phi=0$ fits $v(0)=0$ and positive $x(0)$.",
                "$A=3$.",
                "$x=3\\cos(5t)$.",
            ],
            "$x=3\\cos(5t)$",
            "Sine would have $x(0)=0$.",
            "Hard",
        )
        + _ican([
            "I can read $A$ and $\\omega$ from $x=A\\cos(\\omega t+\\phi)$.",
            "I can differentiate to get $v$ and $a$.",
            "I can test SHM with $a=-\\omega^2 x$.",
        ]),
        ("Calling $\\omega$ the number of hertz",
         "The $\\omega$ in $\\cos(\\omega t)$ is radians per second. Ordinary frequency is $f=\\omega/(2\\pi)$."),
        ("Differentiate the inside with the chain rule",
         "The derivative of $\\cos(2t)$ is $-2\\sin(2t)$, not $-\\sin(2t)$. That extra $2$ is $\\omega$."),
        [
            "I can read $A$ and $\\omega$ from $x=A\\cos(\\omega t+\\phi)$.",
            "I can differentiate to get $v$ and $a$.",
            "I can test SHM with $a=-\\omega^2 x$.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Energy in SHM",
        [
            "Mechanical energy $E=\\tfrac12 mv^2+\\tfrac12 kx^2$ is constant for an undamped spring. It also equals "
            "$\\tfrac12 k A^2$ or $\\tfrac12 m v_\\mathrm{max}^2$. If $k=8$ and $A=4$, $E=64\\,\\mathrm{J}$.",
            "At $x=0$, the spring energy is zero (usual zero) and $K=E$, so $|v|=A\\omega$. At $x=\\pm A$, $K=0$ and "
            "$U=E$. Halfway in $x$, $U=\\tfrac12 k(A/2)^2=E/4$, so $K=3E/4$ — not half, because $U$ is quadratic.",
            "If $A=0.20\\,\\mathrm{m}$ and $\\omega=10\\,\\mathrm{rad/s}$, $v_\\mathrm{max}=2\\,\\mathrm{m/s}$. "
            "If $m=2\\,\\mathrm{kg}$, $E=\\tfrac12 m v_\\mathrm{max}^2=4\\,\\mathrm{J}$? $\\tfrac12(2)(4)=4\\,\\mathrm{J}$. "
            "Also $k=m\\omega^2=200$, $\\tfrac12 k A^2=\\tfrac12(200)(0.04)=4\\,\\mathrm{J}$. Matching checks.",
            "Energy diagrams: $U=\\tfrac12 kx^2$ is a parabola. A horizontal $E$ line cuts the well at $\\pm A$.",
            "Damping slowly lowers $E$ and therefore $A$. Driving can hold $E$ steady.",
            "FRQ: switch to energy when the question asks a speed at a given $x$ without wanting $t$.",
        ],
        "Energy avoids solving the trig function when you only need $|v|$ at a location. It also previews the pendulum well.",
        "Write $E=\\tfrac12 k A^2=\\tfrac12 mv^2+\\tfrac12 kx^2$. Solve for $v$ at the given $x$. Check units in joules.",
        lesson_figure(
            energy_bars_svg(ke=2, pe=2, thermal=0),
            "In undamped SHM the sum of $K$ and $U$ bars is constant; they trade each quarter-cycle",
            "At the endpoint the PE bar is full and KE is empty. At equilibrium the bars swap.",
        )
        + solved(
            11, "$k=8$, $A=4$ (SI). Find $E$.",
            [
                "$E=\\tfrac12 k A^2$.",
                "$A^2=16$.",
                "$E=64\\,\\mathrm{J}$.",
            ],
            "$64\\,\\mathrm{J}$",
            "",
            "Easy",
        )
        + solved(
            12, "At $x=A/2$, what fraction of $E$ is kinetic?",
            [
                "$U=\\tfrac12 k(A/2)^2=E/4$.",
                "$K=E-U=3E/4$.",
                "Not $1/2$, because $U\\propto x^2$.",
            ],
            "$3/4$",
            "",
            "Medium",
        )
        + solved(
            13, "$A=0.20\\,\\mathrm{m}$, $\\omega=10$, $m=2$. Show $E$ two ways.",
            [
                "$v_\\mathrm{max}=A\\omega=2\\,\\mathrm{m/s}$, $E=\\tfrac12(2)(4)=4\\,\\mathrm{J}$.",
                "$k=m\\omega^2=200$, $E=\\tfrac12(200)(0.04)=4\\,\\mathrm{J}$.",
                "Both routes agree.",
            ],
            "$E=4\\,\\mathrm{J}$",
            "",
            "Hard",
        )
        + _ican([
            "I can write $E=\\tfrac12 k A^2$ and $E=K+U$.",
            "I can find $K$ at a given $x$ using $U\\propto x^2$.",
            "I can compute $v_\\mathrm{max}=A\\omega$.",
        ]),
        ("Saying $K=U$ at $x=A/2$",
         "That would be true if $U$ were linear in $|x|$. For a spring, $U=E/4$ at $x=A/2$, so $K=3E/4$."),
        ("Use $E$ when $t$ is unknown and $x$ is known",
         "You do not need the phase $\\phi$ to get speed from energy."),
        [
            "I can write $E=\\tfrac12 k A^2$ and $E=K+U$.",
            "I can find $K$ at a given $x$ using $U\\propto x^2$.",
            "I can compute $v_\\mathrm{max}=A\\omega$.",
        ],
        11,
    )
    c4 = concept_block(
        "4. The physical pendulum",
        [
            "A physical pendulum is any rigid body swinging about a fixed pivot under gravity. Let $d$ be the distance "
            "from pivot to the center of mass, and $I$ the moment of inertia about the pivot. The restoring torque is "
            "$-mgd\\sin\\theta$, so $I\\ddot\\theta=-mgd\\sin\\theta$.",
            "The period for small angles ($\\sin\\theta\\approx\\theta$) is $T=2\\pi\\sqrt{I/(mgd)}$. Larger $I$ means a slower swing; "
            "larger $d$ (stronger torque arm) means a faster swing, competing with $I$ often growing with $d$ too.",
            "Uniform rod about one end: $I=ML^2/3$, $d=L/2$, so $I/(mgd)=2L/(3g)$ and $T=2\\pi\\sqrt{2L/(3g)}$, "
            "which is not $2\\pi\\sqrt{L/g}$.",
            "A simple pendulum is the special case of a point mass on a massless rod: $I=mL^2$, $d=L$, recovering $T=2\\pi\\sqrt{L/g}$.",
            "You can shift $I$ from the CM with $I=I_\\mathrm{cm}+Md^2$ (parallel axis) before inserting into $T$.",
            "AP likes a rod or a disk with a hole used as a pivot. Compute $I$ about that pivot, measure $d$, then quote the $T$ formula.",
        ],
        "This combines Unit 5’s $I$ with Unit 7’s SHM. It is a standard “derive $T$” FRQ.",
        "Write $\\tau=I\\alpha$ about the pivot, insert $\\tau=-mgd\\sin\\theta$, small-angle to get $\\omega=\\sqrt{mgd/I}$, then $T=2\\pi/\\omega$.",
        lesson_figure(
            _pendulum_svg(),
            "A rigid body pivoted at the top: $d$ to the CM, $I$ about the pivot, torque $-mgd\\sin\\theta$",
            "If all mass were at the bob, $I=mL^2$ and $d=L$. A rod has a smaller $d/I$ combination and a different $T$.",
        )
        + solved(
            16, "Write $T$ for a physical pendulum in terms of $I$, $m$, $g$, $d$.",
            [
                "Small-angle $\\ddot\\theta+(mgd/I)\\theta=0$.",
                "$\\omega=\\sqrt{mgd/I}$.",
                "$T=2\\pi\\sqrt{I/(mgd)}$.",
            ],
            "$T=2\\pi\\sqrt{I/(mgd)}$",
            "",
            "Easy",
        )
        + solved(
            17, "Rod about one end. Find $T$ in terms of $L,g$.",
            [
                "$I=ML^2/3$, $d=L/2$.",
                "$I/(Mgd)=2L/(3g)$.",
                "$T=2\\pi\\sqrt{2L/(3g)}$.",
            ],
            "$2\\pi\\sqrt{2L/(3g)}$",
            "",
            "Medium",
        )
        + solved(
            18, "Show that a simple pendulum is the $I=mL^2$, $d=L$ case.",
            [
                "$I/(mgd)=mL^2/(mgL)=L/g$.",
                "$T=2\\pi\\sqrt{L/g}$.",
                "Distributed mass changes this ratio.",
            ],
            "$T=2\\pi\\sqrt{L/g}$ recovered",
            "",
            "Hard",
        )
        + _ican([
            "I can state $T=2\\pi\\sqrt{I/(mgd)}$ for a physical pendulum.",
            "I can compute $T$ for a rod about one end.",
            "I can reduce to the simple pendulum when $I=mL^2$.",
        ]),
        ("Using $T=2\\pi\\sqrt{L/g}$ for a swinging rod",
         "That assumes a point bob. A rod about its end is slower or faster depending on $I/(md)$ — here $T=2\\pi\\sqrt{2L/3g}$."),
        ("Compute $I$ about the pivot, not about the CM, unless you then add $Md^2$",
         "The DE $I\\ddot\\theta=\\tau$ uses the $I$ of the rotation that is actually happening."),
        [
            "I can state $T=2\\pi\\sqrt{I/(mgd)}$ for a physical pendulum.",
            "I can compute $T$ for a rod about one end.",
            "I can reduce to the simple pendulum when $I=mL^2$.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Small-angle pendulum",
        [
            "A simple pendulum of length $L$ has exact equation $\\ddot\\theta+(g/L)\\sin\\theta=0$. This is not SHM "
            "because of the $\\sin\\theta$. For small $\\theta$ in radians, $\\sin\\theta\\approx\\theta$, and you recover "
            "$\\ddot\\theta+(g/L)\\theta=0$, hence $\\omega=\\sqrt{g/L}$ and $T=2\\pi\\sqrt{L/g}$.",
            "If $L=1.0\\,\\mathrm{m}$ and $g=10\\,\\mathrm{m/s}^2$, $\\omega=\\sqrt{10}\\,\\mathrm{rad/s}$ and $T=2\\pi/\\sqrt{10}\\,\\mathrm{s}$.",
            "The approximation $\\sin\\theta\\approx\\theta$ is independent of mass and of amplitude only while $\\theta$ stays small "
            "(a few tenths of a radian). At large amplitude the true period is slightly longer.",
            "Degrees are illegal inside the DE. $\\sin(10^\\circ)$ is not $10$. Convert: $10^\\circ\\approx 0.17\\,\\mathrm{rad}$, where $\\sin$ and the angle still nearly match.",
            "The restoring torque came from the tangential component $mg\\sin\\theta$. Linearizing that component is the whole small-angle move.",
            "AP will ask you to “state the approximation” and to derive $T$. Writing $\\sin\\theta\\approx\\theta$ (radians) is the point.",
        ],
        "This is the most common SHM derivation on the exam. It is also how you justify treating a pendulum clock as isochronous for small swings.",
        "Start from $\\tau=I\\alpha$ or from tangential $F=ma$. Insert $mg\\sin\\theta$. Replace $\\sin\\theta$ with $\\theta$ in radians. Read $\\omega=\\sqrt{g/L}$.",
        lesson_figure(
            _pendulum_svg(),
            "Simple pendulum: the tangential restoring piece is $mg\\sin\\theta\\approx mg\\theta$ for small $\\theta$ in radians",
            "The dashed vertical is $\\theta=0$. SHM is about that vertical, not about a horizontal spring’s $x$.",
        )
        + solved(
            21, "State the small-angle approximation used for pendulum SHM.",
            [
                "$\\theta$ must be in radians.",
                "$\\sin\\theta\\approx\\theta$.",
                "Then $\\ddot\\theta+(g/L)\\theta=0$.",
            ],
            "$\\sin\\theta\\approx\\theta$ (radians)",
            "",
            "Easy",
        )
        + solved(
            22, "$L=1.0\\,\\mathrm{m}$, $g=10$. Find $\\omega$.",
            [
                "$\\omega=\\sqrt{g/L}$.",
                "$\\omega=\\sqrt{10}\\,\\mathrm{rad/s}$.",
                "$T=2\\pi/\\sqrt{10}\\,\\mathrm{s}$.",
            ],
            "$\\sqrt{10}\\,\\mathrm{rad/s}$",
            "",
            "Medium",
        )
        + solved(
            23, "Why does large amplitude make $T$ a bit larger than $2\\pi\\sqrt{L/g}$?",
            [
                "For $|\\theta|>0$, $\\sin\\theta<\\theta$ (positive $\\theta$).",
                "The restoring term $(g/L)\\sin\\theta$ is weaker than $(g/L)\\theta$.",
                "Weaker restoring means a longer period than the SHM model.",
            ],
            "Weaker-than-linear restoring at large $\\theta$ lengthens $T$.",
            "",
            "Hard",
        )
        + _ican([
            "I can replace $\\sin\\theta$ by $\\theta$ in radians to get SHM.",
            "I can compute $\\omega=\\sqrt{g/L}$ and $T=2\\pi\\sqrt{L/g}$.",
            "I can explain why the approximation needs small $\\theta$.",
        ]),
        ("Putting $10^\\circ$ into $\\sin\\theta\\approx\\theta$ without converting",
         "Ten degrees is not $10$ radians. Convert, or keep the symbol $\\theta$ in radians from the start."),
        ("Derive from $\\tau=I\\alpha$ on paper even if you remember $T=2\\pi\\sqrt{L/g}$",
         "The derivation is often the graded part, not the memorized box."),
        [
            "I can replace $\\sin\\theta$ by $\\theta$ in radians to get SHM.",
            "I can compute $\\omega=\\sqrt{g/L}$ and $T=2\\pi\\sqrt{L/g}$.",
            "I can explain why the approximation needs small $\\theta$.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Damped and driven oscillators, qualitative",
        [
            "Real oscillators lose energy. Linear drag $F=-bv$ added to $F=-kx$ gives $m\\ddot x+b\\dot x+kx=0$. "
            "Light damping (small $b$) still oscillates, but the amplitude decays as an envelope $e^{-(b/2m)t}$. "
            "The observed angular frequency is slightly less than $\\sqrt{k/m}$.",
            "Overdamping (large $b$) returns to equilibrium without oscillating — two real exponential decays. "
            "Critical damping is the fastest non-oscillatory return (door closers are near this).",
            "A driven oscillator has an extra $F_0\\cos(\\omega_d t)$. After transients die, it oscillates at the "
            "driver frequency $\\omega_d$, not at $\\omega_0$. Amplitude peaks when $\\omega_d$ is near $\\omega_0$ "
            "(resonance), more sharply if damping is light.",
            "At resonance the driver does net positive work each cycle, offsetting drag, so a large $A$ can be maintained. "
            "Far from resonance the amplitude is small.",
            "Energy of a damped free oscillator falls because drag does negative work. A driver can hold energy steady.",
            "AP qualitative: sketch a decaying cosine; mark resonance as a peak of $A$ vs $\\omega_d$; do not solve the full complex impedance unless asked (Mechanics rarely asks the full formula).",
        ],
        "Clocks, car suspensions, and seismic instruments live in this qualitative story. The DE is the same SHM equation with extra terms.",
        "Identify free vs driven, light vs overdamped. For free light damping, draw a decaying cosine. For driven, oscillate at $\\omega_d$ with a resonance peak near $\\omega_0$.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", sample_curve(lambda t: 4 * math.exp(-0.25 * t) * math.cos(2 * t), 0, 10))],
                points=[(0, 4, "A(0)")],
                xlim=(0, 10), ylim=(-5, 5), xlab="t (s)", ylab="x (m)",
            ),
            "Lightly damped SHM: a cosine under a decaying exponential envelope",
            "The wiggles still have roughly period $\\pi$, but each peak is smaller. Drag is removing mechanical energy.",
        )
        + solved(
            26, "What does light damping do to amplitude?",
            [
                "The system still oscillates.",
                "Amplitude decays slowly (exponential envelope).",
                "Frequency is close to the undamped $\\omega_0$.",
            ],
            "Slowly decaying oscillations near $\\omega_0$",
            "",
            "Easy",
        )
        + solved(
            27, "What is resonance for a driven oscillator?",
            [
                "The driver frequency $\\omega_d$ is near the natural $\\omega_0$.",
                "Amplitude becomes large, especially if $b$ is small.",
                "Steady motion is at $\\omega_d$, not at $\\omega_0$.",
            ],
            "Large $A$ when $\\omega_d\\approx\\omega_0$",
            "",
            "Medium",
        )
        + solved(
            28, "Contrast overdamped return with light damping.",
            [
                "Overdamped: no oscillation; $x(t)$ is a sum of decaying exponentials.",
                "Light damping: many oscillations under a decaying envelope.",
                "Critical damping is the border: fastest return without ringing.",
            ],
            "Overdamped: no wiggles. Light: wiggles that shrink.",
            "",
            "Hard",
        )
        + _ican([
            "I can describe light damping as a decaying cosine.",
            "I can define resonance as a large response near $\\omega_0$.",
            "I can contrast overdamped and underdamped return.",
        ]),
        ("Saying a damped oscillator has constant $E=\\tfrac12 k A^2$ with fixed $A$",
         "If $A$ is decaying, $E$ is decaying. Only a driver can hold $A$ (and $E$) steady."),
        ("On a sketch, show the envelope as well as the wiggles",
         "A plain cosine looks undamped. Graders look for shrinking peaks."),
        [
            "I can describe light damping as a decaying cosine.",
            "I can define resonance as a large response near $\\omega_0$.",
            "I can contrast overdamped and underdamped return.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        [
            "Build SHM from $F=-kx$ and $\\omega=\\sqrt{k/m}$",
            "Solve and interpret $\\ddot x+\\omega^2 x=0$",
            "Use $E=\\tfrac12 k A^2=K+U$ in SHM",
            "Derive $T$ for a physical pendulum",
            "Linearize the simple pendulum with $\\sin\\theta\\approx\\theta$",
            "Describe damping, driving, and resonance qualitatively",
        ],
        c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Gravitation
# ===========================================================================

def _u8_questions():
    qs = []
    _add(qs, [
        ("Newton's law of gravity: $F=GMm/r^2$. If $r$ doubles, $F$",
         "becomes 1/4 as large", "Inverse square: $(2r)^2=4r^2$.",
         ["doubles", "halves", "becomes 1/8"]),
        ("The force is attractive along the line joining the centers. $G$ is",
         "a universal constant", "The same $G$ appears for apples and planets.",
         ["different on the Moon", "equal to g", "1/4π"]),
        ("If $M=m=2$ and $r=1$ (toy SI with $G=1$), $F=$",
         "4 N", "$GMm/r^2=4$.",
         ["2 N", "1 N", "8 N"]),
        ("Gravity is a central force, so torque about either mass is",
         "0", "$\\vec r\\times\\vec F=0$ when $\\vec F$ is along $\\vec r$.",
         ["mgr", "GMm", "Iα always"]),
        ("The gravitational field $g$ at distance $r$ from a point mass $M$ has magnitude",
         "GM/r^2", "Force per unit mass: $F/m$.",
         ["GM/r", "GMm/r^2", "G/r^2"]),
        ("Surface $g=GM/R^2$. If $g=10$ and $R=2$ with $G=1$ (toy), $M=$",
         "40", "$M=g R^2=40$.",
         ["5", "20", "10"]),
        ("If you go to $r=2R$ from a planet's center (outside), $g$ is",
         "g_surface / 4", "$(2R)^2=4R^2$.",
         ["g_surface / 2", "2 g_surface", "unchanged"]),
        ("Inside a uniform sphere (beyond this course's usual demand) $g$ grows with $r$. Outside, $g$",
         "falls as 1/r^2", "Newton's shell idea: the planet looks like a point mass from outside.",
         ["is constant", "grows as r", "is zero"]),
        ("$GM=400$, $r=4$. Then $g=$",
         "25 m/s^2", "$400/16=25$.",
         ["100 m/s^2", "400 m/s^2", "4 m/s^2"]),
        ("Weight $mg$ with this $g$ for $m=2$ is",
         "50 N", "$2\\times 25=50$.",
         ["25 N", "400 N", "8 N"]),
        ("Circular orbit speed is $v=\\sqrt{GM/r}$. For $GM=400$, $r=4$, $v=$",
         "10 m/s", "$\\sqrt{100}=10$.",
         ["20 m/s", "100 m/s", "5 m/s"]),
        ("The centripetal force is gravity: $mv^2/r=GMm/r^2$. Canceling $m$ and one $r$ gives",
         "v^2 = GM/r", "That is the circular-orbit condition.",
         ["v^2 = GMm", "v = GM r", "v^2 = g r^2"]),
        ("If $r$ quadruples, circular $v$",
         "halves", "$v\\propto 1/\\sqrt{r}$.",
         ["quarters", "doubles", "is unchanged"]),
        ("Low orbit near a planet uses $r\\approx R$ so $v\\approx\\sqrt{gR}$. If $g=10$, $R=6.4\\times 10^6$, $v$ is about $8\\,\\mathrm{km/s}$. For toy $g=10$, $R=40$, $v=$",
         "20 m/s", "$\\sqrt{400}=20$.",
         ["10 m/s", "40 m/s", "400 m/s"]),
        ("A circular orbit is not “falling with $a=0$.” Acceleration is",
         "v^2/r toward the star", "Always centripetal; speed can still be constant.",
         ["zero", "g upward", "tangential"]),
        ("Kepler's third law for circular orbits: $T^2=4\\pi^2 r^3/(GM)$. If $r$ doubles, $T$ is multiplied by",
         "2√2", "$T\\propto r^{3/2}$, so $2^{3/2}=2\\sqrt{2}$.",
         ["2", "4", "8"]),
        ("If $r$ becomes $4$ times larger, $T$ is multiplied by",
         "8", "$4^{3/2}=8$.",
         ["4", "2", "16"]),
        ("$T^2/r^3$ for satellites of one star is",
         "the same constant 4π^2/GM", "Kepler 3; $GM$ is the star's.",
         ["different for each satellite mass", "equal to g", "zero"]),
        ("$GM=400$, $r=4$, $v=10$. Circumference $2\\pi r=8\\pi$, so $T=$",
         "0.8π", "$T=8\\pi/10=0.8\\pi$.",
         ["8π", "10", "0.4π"]),
        ("Equal areas in equal times follows from",
         "conservation of L about the star", "Central force, $\\tau=0$.",
         ["constant speed always", "T^2 = r^3 only", "escape speed"]),
        ("$U=-GMm/r$. If $GMm=400$ and $r=4$, $U=$",
         "-100 J", "$-400/4=-100$.",
         ["100 J", "-400 J", "-50 J"]),
        ("Circular-orbit total $E=-GMm/(2r)$. For those numbers $E=$",
         "-50 J", "$-400/8=-50$.",
         ["-100 J", "50 J", "0"]),
        ("$K$ in that circular orbit is",
         "50 J", "$K=GMm/(2r)=50$, and $K=-E$.",
         ["100 J", "0", "-50 J"]),
        ("Raising a circular orbit (larger $r$) makes $E$",
         "less negative (increases E)", "You must add energy to climb the well.",
         ["more negative", "unchanged", "equal to U"]),
        ("$F_r=-dU/dr$ with $U=-GMm/r$ gives",
         "-GMm/r^2", "Attractive.",
         ["+GMm/r^2", "0", "GMm/r"]),
        ("Escape speed is $\\sqrt{2GM/r}$. For $GM=400$, $r=4$, $v_\\mathrm{esc}=$",
         "10√2", "$\\sqrt{200}=10\\sqrt{2}$.",
         ["10", "20", "√2"]),
        ("$v_\\mathrm{esc}/v_\\mathrm{circ}$ at the same $r$ is",
         "√2", "$\\sqrt{2GM/r}/\\sqrt{GM/r}=\\sqrt{2}$.",
         ["2", "1/2", "1"]),
        ("$E=0$ with $U(\\infty)=0$ means at infinity",
         "K=0 (barely escapes)", "Threshold of bound vs unbound.",
         ["K is infinite", "U is -∞", "v=0 at launch"]),
        ("From rest on a surface, $v_\\mathrm{esc}=\\sqrt{2gR}$. Toy $g=10$, $R=40$ gives",
         "√800 m/s", "$\\sqrt{2\\times 10\\times 40}=\\sqrt{800}$.",
         ["20 m/s", "10 m/s", "400 m/s"]),
        ("A bound orbit has",
         "E < 0", "It cannot reach $r=\\infty$.",
         ["E>0", "E=mgh", "U>0"]),
        ("Work done by gravity as $m$ moves from $r=4$ to $r=8$ with $GMm=400$ is",
         "-50 J", "$W=\\int_4^8 (-GMm/r^2)\\,dr=GMm(1/8-1/4)=400(-1/8)=-50\\,\\mathrm{J}$.",
         ["50 J", "100 J", "0"]),
        ("An astronaut in a circular-orbit station feels weightless because",
         "the astronaut and station have the same centripetal a = GM/r^2", "Both are in free fall together; the floor need not push.",
         ["gravity is zero in space", "g points outward", "U is zero"]),
        ("At periapsis of an ellipse the planet is fastest because",
         "L conservation: smaller r means larger v_perp", "Equal areas in equal times is the same idea.",
         ["U is maximum there", "E is larger there", "g is zero"]),
        ("Circular-orbit binding energy (energy to unbind) is $GMm/(2r)$. For $GMm=400$, $r=4$ that is",
         "50 J", "$|E|=50$ because $E=-50\\,\\mathrm{J}$.",
         ["100 J", "400 J", "25 J"]),
        ("If the central $M$ doubles at fixed $r$, circular $v$",
         "is multiplied by √2", "$v=\\sqrt{GM/r}$.",
         ["doubles", "halves", "is unchanged"]),
        ("If $M$ doubles at fixed $r$, period $T$",
         "is multiplied by 1/√2", "$T=2\\pi\\sqrt{r^3/GM}$.",
         ["doubles", "halves", "is unchanged"]),
        ("Field at height $h$ above a planet of radius $R$ is $g=GM/(R+h)^2$. If $h=R$, $g$ is",
         "g_surface / 4", "$R+h=2R$.",
         ["g_surface / 2", "g_surface", "0"]),
        ("Force ratio $F(r)/F(2r)$ for gravity is",
         "4", "Inverse square.",
         ["2", "8", "1"]),
        ("Outside a uniform sphere, gravity is the same as a point mass at the center. That is why orbital $r$ is",
         "measured from the planet's center", "Not from the ground, once you are outside the surface.",
         ["always the surface radius only", "the diameter", "zero"]),
        ("Two equal stars a distance $2d$ apart. Midway between them, $g_\\mathrm{net}$ is",
         "0", "Equal opposite fields cancel.",
         ["2GM/d^2", "GM/d^2", "infinite"]),
        ("Period from $T=2\\pi r/v$ with $v=\\sqrt{GM/r}$ recovers",
         "T^2 = 4π^2 r^3 / GM", "Kepler 3 for circles.",
         ["T = 2π r / GM", "T^2 = GM / r^3", "T = v/r"]),
        ("A hyperbolic flyby has",
         "E > 0", "It can reach $r=\\infty$ with leftover $K$.",
         ["E < 0", "E = -GMm/r always", "U > 0"]),
        ("For a circular orbit, $K=-U/2$. If $U=-100\\,\\mathrm{J}$, then $K=$",
         "50 J", "Virial for $1/r$ gravity: $2K=-U$.",
         ["100 J", "-50 J", "0"]),
        ("The conventional $U(\\infty)=0$ means $U(r)$ is",
         "negative for all finite r", "$U=-GMm/r<0$.",
         ["positive everywhere", "zero at the surface", "equal to K"]),
        ("If $r$ becomes $8$ times larger, Kepler $T$ is multiplied by $8^{3/2}=$",
         "16√2", "$(8^{1/2})^3=(\\sqrt{8})^3=(2\\sqrt{2})^3=16\\sqrt{2}$.",
         ["8", "64", "4"]),
        ("A satellite already in circular orbit needs extra $\\Delta v$ to escape. Because it already has $K=GMm/(2r)$, the extra kinetic energy is",
         "GMm/(2r) more, not GMm/r", "Circular $E=-GMm/(2r)$; escape needs $E=0$. From rest you would need $GMm/r$.",
         ["zero extra", "GMm/r extra", "infinite extra"]),
        ("AP Stretch: Work by gravity from $r=3$ to $r=6$ with $GMm=720$ is $\\int_3^6 (-720/r^2)\\,dr=$",
         "-120 J", "$720(1/6-1/3)=720(-1/6)=-120$.",
         ["120 J", "-240 J", "60 J"]),
        ("AP Stretch: $U=-720/r$. Then $F_r=-dU/dr$ at $r=6$ is",
         "-20 N", "$dU/dr=720/r^2=20$, so $F_r=-20$ (inward).",
         ["20 N", "-120 N", "0"]),
        ("AP Stretch: $dg/dr$ for $g=GM/r^2$ equals $-2GM/r^3$. At $GM=720$, $r=6$, $dg/dr=$",
         "-20/3 s^{-2}", "$-2\\times 720/216=-1440/216=-20/3$.",
         ["-20", "20", "-10/3"]),
        ("AP Stretch: A satellite of $m=1$ in a circle at $r=6$, $GM=720$. Compute $E=-GMm/(2r)$, then the extra energy to reach $E=0$.",
         "60 J", "$E=-720/12=-60\\,\\mathrm{J}$, so you must add $60\\,\\mathrm{J}$.",
         ["120 J", "30 J", "0"]),
        ("AP Stretch: Instantaneous power of gravity on a circular-orbit satellite is $\\vec F\\cdot\\vec v=$",
         "0", "$\\vec F$ is radial and $\\vec v$ is tangential.",
         ["F v", "mg v", "GMm v / r^2"]),
        ("AP Stretch: $\\int_2^5 (10/x^2)\\,dx$ (a $1/r^2$-style work integral) equals",
         "3", "$10(1/2-1/5)=3$.",
         ["10", "2", "5"]),
        ("AP Stretch: From $v\\,dv=a\\,dr$ with $a=-GM/r^2$ and $v=0$ at $r=\\infty$, speed at $r$ is",
         "√(2GM/r)", "That is $v_\\mathrm{esc}$ recovered by integrating $v\\,dv=-GM\\,dr/r^2$.",
         ["√(GM/r)", "GM/r", "√(GM/r^2)"]),
        ("AP Stretch: $g=720/r^2$. The line integral $\\int_{r=9}^{r=3} (-g)\\,dr$ (inward path) equals",
         "160", "$\\int_9^3 (-720/r^2)\\,dr=720(1/3-1/9)=160$.",
         ["-160", "80", "240"]),
        ("AP Stretch: Kepler $T^2\\propto r^3$. If $r$ is multiplied by $9$, $T$ is multiplied by",
         "27", "$9^{3/2}=(9^{1/2})^3=3^3=27$.",
         ["9", "81", "3"]),
    ])
    return qs


def build_unit8():
    title = "AP Physics C Mechanics Unit 8: Gravitation"
    description = (
        "Newton's law of gravity, g=GM/r^2, circular orbit speed, Kepler from centripetal force, "
        "gravitational potential energy, and escape speed."
    )
    c1 = concept_block(
        "1. Newton's law of gravity",
        [
            "Every two point masses attract with $F=GMm/r^2$, directed along the line joining them. $G$ is a universal "
            "constant. If $r$ doubles, $F$ becomes one-fourth as large. In a toy model with $G=1$, $M=m=2$, $r=1$, $F=4\\,\\mathrm{N}$.",
            "The force is central: it points along $\\vec r$. Therefore $\\vec\\tau=\\vec r\\times\\vec F=0$ about either mass, "
            "and angular momentum of a planet about the star is conserved (Unit 6).",
            "Newton's third law still holds: the planet pulls the star with the same magnitude. The star moves much less "
            "if $M\\gg m$, which is why we often treat the star as fixed.",
            "A spherical symmetric mass distribution, from outside, is equivalent to a point mass at its center. "
            "That is why $r$ in $GM/r^2$ is measured from the planet's center, not from the ground, once you are outside.",
            "Gravity is always attractive. There is no gravitational “charge” of two signs in this course.",
            "AP numeric items often use a given $GM$ product to avoid punching $6.67\\times 10^{-11}$ every time. "
            "Keep $GM$ as a single symbol until the last line.",
        ],
        "Orbits, $g$, potential energy, and escape speed are all this one inverse-square law plus calculus or energy.",
        "Write $F=GMm/r^2$ along the line of centers, attractive. If $r$ changes by a factor, square that factor in the denominator.",
        lesson_figure(
            _orbit_svg(),
            "A star and a planet: the force on each is $GMm/r^2$ along the line joining them",
            "The dashed circle is a possible circular path. Gravity points inward toward the star at every point on that path.",
        )
        + solved(
            1, "If $r$ triples, what happens to $F$?",
            [
                "$F\\propto 1/r^2$.",
                "New $r^2$ is $9$ times larger.",
                "$F$ becomes $1/9$ as large.",
            ],
            "$F\\to F/9$",
            "",
            "Easy",
        )
        + solved(
            2, "Toy $G=1$, $M=m=2$, $r=1$. Find $F$.",
            [
                "$F=GMm/r^2$.",
                "$F=4/1=4\\,\\mathrm{N}$.",
                "Each mass feels $4\\,\\mathrm{N}$ toward the other.",
            ],
            "$4\\,\\mathrm{N}$",
            "",
            "Medium",
        )
        + solved(
            3, "Why is a planet's $L$ about the sun conserved?",
            [
                "Gravity is central: $\\vec F$ is along $-\\vec r$.",
                "$\\vec\\tau=\\vec r\\times\\vec F=0$.",
                "Then $dL/dt=0$ about the sun.",
            ],
            "Central force $\\Rightarrow\\tau=0\\Rightarrow L$ constant about the sun.",
            "",
            "Hard",
        )
        + _ican([
            "I can use $F=GMm/r^2$ and the inverse-square factor.",
            "I can explain that gravity is central and attractive.",
            "I can treat a sphere from outside as a point mass at its center.",
        ]),
        ("Measuring $r$ from the ground when using $GM/r^2$ in orbit",
         "Orbital $r$ is from the planet's center. Low orbit is $R+h$, which is nearly $R$, not $h$."),
        ("Keep $GM$ together",
         "Many items hand you $GM$. Do not split it unless a mass is asked."),
        [
            "I can use $F=GMm/r^2$ and the inverse-square factor.",
            "I can explain that gravity is central and attractive.",
            "I can treat a sphere from outside as a point mass at its center.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Little-g from GM/r^2",
        [
            "The gravitational field (acceleration of a freely falling test mass) at distance $r$ from a point mass $M$ "
            "is $g(r)=GM/r^2$, toward $M$. At a planet's surface, $g=GM/R^2$. If $g=10$ and $R=2$ in a toy $G=1$ world, $M=40$.",
            "With $GM=400$ and $r=4$, $g=400/16=25\\,\\mathrm{m/s}^2$. A $2\\,\\mathrm{kg}$ object then has weight $50\\,\\mathrm{N}$ there.",
            "At $r=2R$ outside, $g$ is $g_\\mathrm{surface}/4$. Altitude $h$ above the surface means $r=R+h$, so "
            "$g=(GM)/(R+h)^2$, not a linear drop.",
            "The $g=10\\,\\mathrm{m/s}^2$ of earlier units is this formula evaluated at Earth's surface, treated as constant "
            "only when $\\Delta r\\ll R$.",
            "Weightlessness in orbit is not “no gravity.” Gravity supplies $mv^2/r$. The astronaut and the station fall together.",
            "FRQ: if $g$ at the surface is given, $GM=g R^2$. That substitution turns orbit formulas into $g$ and $R$.",
        ],
        "Connecting $g$ to $GM/R^2$ lets you switch between “Earth numbers” and “orbit numbers” without a new constant.",
        "Write $g=GM/r^2$. At the surface, $r=R$. To go up, increase $r$, do not subtract a linear $h$ term unless the problem is the constant-$g$ approximation.",
        lesson_figure(
            xy_graph(
                curves=[("#b45309", sample_curve(lambda r: 400 / (r * r), 2, 10))],
                points=[(4, 25, "r=4, g=25")],
                xlim=(1.5, 10.5), ylim=(0, 110), xlab="r", ylab="g(r)",
            ),
            "$g=GM/r^2$ with $GM=400$: at $r=4$, $g=25$",
            "The field falls quickly. Doubling $r$ from $4$ to $8$ drops $g$ from $25$ to $6.25$, one-fourth.",
        )
        + solved(
            6, "$GM=400$, $r=4$. Find $g$.",
            [
                "$g=GM/r^2$.",
                "$r^2=16$.",
                "$g=25\\,\\mathrm{m/s}^2$.",
            ],
            "$25\\,\\mathrm{m/s}^2$",
            "",
            "Easy",
        )
        + solved(
            7, "Surface $g$, then $r=2R$. Find $g$ in terms of $g_s$.",
            [
                "Outside, $g\\propto 1/r^2$.",
                "$r=2R$ means a factor $1/4$.",
                "$g=g_s/4$.",
            ],
            "$g_s/4$",
            "",
            "Medium",
        )
        + solved(
            8, "Toy $G=1$, $g=10$, $R=2$. Find $M$.",
            [
                "$g=GM/R^2$ so $M=g R^2/G$.",
                "$M=10\\times 4=40$.",
                "Then $g$ at $r=4$ would be $40/16=2.5$.",
            ],
            "$M=40$",
            "",
            "Hard",
        )
        + _ican([
            "I can write $g=GM/r^2$.",
            "I can scale $g$ when $r$ changes.",
            "I can get $GM$ from surface $g$ and $R$.",
        ]),
        ("Using $g=10$ at geosynchronous $r$",
         "That $g$ is Earth's surface value. At several Earth-radii, $g$ is much smaller: use $GM/r^2$."),
        ("If surface $g$ and $R$ are given, replace $GM$ by $g R^2$",
         "That one substitution simplifies many orbit algebra steps."),
        [
            "I can write $g=GM/r^2$.",
            "I can scale $g$ when $r$ changes.",
            "I can get $GM$ from surface $g$ and $R$.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Circular orbit speed",
        [
            "For a circular orbit, gravity is the centripetal force: $\\dfrac{GMm}{r^2}=\\dfrac{mv^2}{r}$. Cancel $m$ and one "
            "$r$ to get $v=\\sqrt{GM/r}$. With $GM=400$ and $r=4$, $v=10$ (same units as your $GM$ choice).",
            "Acceleration is not zero: $a=v^2/r=GM/r^2$, toward the star. Speed is constant; velocity is not, because direction changes.",
            "If $r$ quadruples, $v$ halves, because $v\\propto 1/\\sqrt{r}$. Higher orbits are slower, not faster.",
            "Near-surface circular speed is $\\sqrt{gR}$. Toy $g=10$, $R=40$ gives $v=20$. Earth's real value is about $8\\,\\mathrm{km/s}$.",
            "The period is $T=2\\pi r/v=2\\pi\\sqrt{r^3/GM}$, which is Kepler's law for circles, next concept.",
            "Energy of a circular orbit will be $E=-GMm/(2r)$ once $U=-GMm/r$ is in place. You can preview: $K=GMm/(2r)=|E|$.",
        ],
        "Every satellite item starts here. If the path is a circle, this $v$ is the only speed that matches $r$.",
        "Set $GMm/r^2=mv^2/r$. Solve for $v$. Then $a=v^2/r$ if acceleration is asked. Do not set $a=0$.",
        lesson_figure(
            _orbit_svg(),
            "Circular orbit: gravity inward supplies $mv^2/r$ at every point on the dashed path",
            "The planet's velocity is tangent to the circle. Gravity is radial, so $P=\\vec F\\cdot\\vec v=0$ and speed stays constant.",
        )
        + solved(
            11, "$GM=400$, $r=4$. Find circular $v$.",
            [
                "$v=\\sqrt{GM/r}=\\sqrt{100}$.",
                "$v=10$.",
                "Then $a=v^2/r=100/4=25$, matching $g$.",
            ],
            "$10$",
            "",
            "Easy",
        )
        + solved(
            12, "If $r\\to 4r$, what happens to circular $v$?",
            [
                "$v\\propto 1/\\sqrt{r}$.",
                "Factor $1/2$.",
                "The new speed is half.",
            ],
            "$v$ halves",
            "",
            "Medium",
        )
        + solved(
            13, "Show $K=GMm/(2r)$ for a circular orbit.",
            [
                "$v^2=GM/r$.",
                "$K=\\tfrac12 m v^2=GMm/(2r)$.",
                "This $K$ is half $|U|$ once $U=-GMm/r$.",
            ],
            "$K=GMm/(2r)$",
            "",
            "Hard",
        )
        + _ican([
            "I can derive $v=\\sqrt{GM/r}$ from centripetal force.",
            "I can scale $v$ when $r$ changes.",
            "I can state that $a=GM/r^2$ inward even when speed is constant.",
        ]),
        ("Setting net force to zero in a circular orbit",
         "Net force is not zero; it is $mv^2/r$ inward. Uniform circular motion is accelerated motion."),
        ("Cancel $m$ only after writing both sides",
         "Write $GMm/r^2=mv^2/r$ first so the centripetal identification is visible for the rubric."),
        [
            "I can derive $v=\\sqrt{GM/r}$ from centripetal force.",
            "I can scale $v$ when $r$ changes.",
            "I can state that $a=GM/r^2$ inward even when speed is constant.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Kepler's third law from centripetal force",
        [
            "Period $T$ of a circular orbit is circumference over speed: $T=2\\pi r/v$. Insert $v=\\sqrt{GM/r}$ to get "
            "$T=2\\pi\\sqrt{r^3/GM}$, or $T^2=4\\pi^2 r^3/(GM)$. That is Kepler's third law for circles (and it also holds "
            "for ellipses if $r$ is replaced by the semi-major axis $a$).",
            "If $r$ doubles, $r^3$ becomes $8$ times, so $T$ becomes $2\\sqrt{2}\\approx 2.83$ times larger. "
            "If $r$ becomes $4$ times, $T$ becomes $8$ times.",
            "All satellites of one star share the same $GM$ in $T^2/r^3=4\\pi^2/GM$. The ratio $T^2/r^3$ is constant for that star.",
            "A geosynchronous orbit matches Earth's spin period. Larger $T$ requires larger $r$ by the $2/3$ power: $r\\propto T^{2/3}$.",
            "You do not need ellipses in full polar form for AP Physics C Mechanics, but you should know that equal areas "
            "in equal times is $L$ conservation, already justified because gravity is central.",
            "Numeric: $GM=400$, $r=4$, $v=10$, circumference $8\\pi$, $T=8\\pi/10=0.8\\pi$. Also $T^2=4\\pi^2 (64)/400= (256\\pi^2)/400$.",
        ],
        "Kepler's law is how you compare two orbits without finding $v$ first. It is also how you measure a star's mass from $T$ and $r$.",
        "Write $T=2\\pi r/v$ and $v=\\sqrt{GM/r}$, or quote $T^2\\propto r^3$. Scale with the $3/2$ power of the radius ratio.",
        lesson_figure(
            _orbit_svg(),
            "Larger dashed radius would mean both a longer path and a smaller $v$, so $T$ grows as $r^{3/2}$",
            "Kepler's third law is not a new force law. It is circular-orbit kinematics plus $F=GMm/r^2$.",
        )
        + solved(
            16, "If $r$ doubles, by what factor does $T$ grow?",
            [
                "$T\\propto r^{3/2}$.",
                "$2^{3/2}=2\\sqrt{2}$.",
                "About $2.83$ times longer.",
            ],
            "$2\\sqrt{2}$",
            "",
            "Easy",
        )
        + solved(
            17, "If $r\\times 4$, factor for $T$?",
            [
                "$4^{3/2}=(4^{1/2})^3=2^3=8$.",
                "Or $(4^3)^{1/2}=64^{1/2}=8$.",
                "$T$ becomes $8$ times larger.",
            ],
            "factor of $8$",
            "",
            "Medium",
        )
        + solved(
            18, "Derive $T^2=4\\pi^2 r^3/GM$ from $v=\\sqrt{GM/r}$.",
            [
                "$T=2\\pi r/v$.",
                "$T=2\\pi r/\\sqrt{GM/r}=2\\pi\\sqrt{r^3/GM}$.",
                "Square both sides.",
            ],
            "$T^2=4\\pi^2 r^3/GM$",
            "",
            "Hard",
        )
        + _ican([
            "I can state $T^2\\propto r^3$ for circular orbits about one $M$.",
            "I can scale $T$ when $r$ changes by a factor.",
            "I can derive Kepler 3 from $v=\\sqrt{GM/r}$.",
        ]),
        ("Scaling $T$ with $r$ instead of $r^{3/2}$",
         "A doubled radius is not a doubled period. Path length doubles and speed falls, so $T$ more than doubles."),
        ("Use the same $GM$ for both satellites of one planet",
         "The constant in $T^2/r^3$ characterizes the central mass, not the satellite."),
        [
            "I can state $T^2\\propto r^3$ for circular orbits about one $M$.",
            "I can scale $T$ when $r$ changes by a factor.",
            "I can derive Kepler 3 from $v=\\sqrt{GM/r}$.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Gravitational potential energy",
        [
            "Because gravity is conservative, it has a potential energy. Taking $U\\to 0$ at infinity, "
            "$U=-GMm/r$. The minus sign means bound systems have negative $U$. If $GM=400$, $m=1$, $r=4$, $U=-100\\,\\mathrm{J}$.",
            "The force is $F_r=-dU/dr$. For $U=-GMm/r$, $dU/dr=GMm/r^2$, so $F_r=-GMm/r^2$ (attractive, toward decreasing $r$).",
            "You cannot use $U=mgy$ when $r$ changes by a sizable fraction of $R$. The $mgy$ formula is the first-order "
            "expansion of $-GMm/r$ near Earth's surface.",
            "For a circular orbit, $K=GMm/(2r)$ and $U=-GMm/r$, so $E=K+U=-GMm/(2r)$. More tightly bound (smaller $r$) means more negative $E$.",
            "To move a satellite to a higher circular orbit you must add energy (less negative $E$), even though $K$ itself decreases.",
            "Path independence: work by gravity from $r_1$ to $r_2$ is $-\\Delta U=GMm(1/r_2-1/r_1)$ with care on signs. "
            "Going out, gravity does negative work on the spacecraft.",
        ],
        "Escape speed and orbital energy bookkeeping both require $U=-GMm/r$, not $mgy$.",
        "Write $U=-GMm/r$ with $U(\\infty)=0$. Then $E=K+U$. For circles, reduce with $v^2=GM/r$ to $E=-GMm/(2r)$.",
        lesson_figure(
            xy_graph(
                curves=[("#059669", sample_curve(lambda r: -400 / r, 1.5, 12))],
                points=[(4, -100, "r=4, U=-100")],
                xlim=(1, 12), ylim=(-280, 20), xlab="r", ylab="U(r)",
            ),
            "$U=-GMm/r$ with $GMm=400$: a negative well that approaches $0$ as $r\\to\\infty$",
            "A horizontal line at $E=-50$ would be the circular-orbit energy at $r=4$, because $E=U/2$ on a circle.",
        )
        + solved(
            21, "$GMm=400$, $r=4$. Find $U$.",
            [
                "$U=-GMm/r$.",
                "$U=-400/4=-100$.",
                "Units joules if $GMm$ was in $\\mathrm{J\\cdot m}$.",
            ],
            "$-100\\,\\mathrm{J}$",
            "",
            "Easy",
        )
        + solved(
            22, "Circular orbit at that $r$. Find $E$.",
            [
                "$E=-GMm/(2r)$.",
                "$E=-400/8=-50\\,\\mathrm{J}$.",
                "Also $K=50$, $U=-100$, sum $-50$.",
            ],
            "$-50\\,\\mathrm{J}$",
            "",
            "Medium",
        )
        + solved(
            23, "Show $F_r=-dU/dr$ recovers Newton's law from $U=-GMm/r$.",
            [
                "$dU/dr=GMm/r^2$.",
                "$F_r=-dU/dr=-GMm/r^2$.",
                "The minus means attraction toward smaller $r$.",
            ],
            "$F=-GMm/r^2\\,\\hat{r}$ (inward)",
            "",
            "Hard",
        )
        + _ican([
            "I can use $U=-GMm/r$ with zero at infinity.",
            "I can compute $E=-GMm/(2r)$ for a circular orbit.",
            "I can recover $F$ from $-dU/dr$.",
        ]),
        ("Using $U=mgy$ for an Earth-to-infinity problem",
         "$mgy$ is a local approximation. Escape and high orbits need $-GMm/r$."),
        ("Remember $E$ is negative for bound orbits",
         "A positive $E$ means the object can reach infinity with leftover $K$ (unbound)."),
        [
            "I can use $U=-GMm/r$ with zero at infinity.",
            "I can compute $E=-GMm/(2r)$ for a circular orbit.",
            "I can recover $F$ from $-dU/dr$.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Escape speed",
        [
            "Escape speed from a distance $r$ is the launch speed that makes $E=0$, so the object can coast to infinity "
            "with $K\\to 0$. With $U=-GMm/r$ and $K=\\tfrac12 mv^2$, $E=0$ gives $v_\\mathrm{esc}=\\sqrt{2GM/r}$.",
            "For $GM=400$, $r=4$, $v_\\mathrm{esc}=\\sqrt{200}=10\\sqrt{2}$, which is $\\sqrt{2}$ times the circular speed $10$. "
            "That $\\sqrt{2}$ factor is general: $v_\\mathrm{esc}=\\sqrt{2}\\,v_\\mathrm{circ}$ at the same $r$.",
            "From a planet's surface, $v_\\mathrm{esc}=\\sqrt{2gR}$. Toy $g=10$, $R=40$ gives $\\sqrt{800}\\approx 28.3$. "
            "Earth's actual escape from the surface is about $11\\,\\mathrm{km/s}$.",
            "Direction: if you launch slower than $v_\\mathrm{esc}$ radially, you stop and fall back (bound, $E<0$). "
            "Faster, you reach infinity with leftover speed. Gravity never “turns off”; it just gets arbitrarily weak.",
            "Escape does not require a circular path. The energy condition is path-independent (conservative force) as long as you do not hit the planet.",
            "A parabolic trajectory in the two-body problem is the $E=0$ border; ellipses are $E<0$; hyperbolas $E>0$. AP mainly wants the $v_\\mathrm{esc}$ formula and the $\\sqrt{2}$ comparison.",
        ],
        "Escape speed is the flagship energy application of $U=-GMm/r$. It also checks that you did not use $mgh$ to infinity.",
        "Set $E=0$: $\\tfrac12 mv^2-GMm/r=0$. Solve $v=\\sqrt{2GM/r}$. Compare with $v_\\mathrm{circ}=\\sqrt{GM/r}$.",
        lesson_figure(
            xy_graph(
                curves=[("#059669", sample_curve(lambda r: -400 / r, 1.5, 12))],
                dashes=[("h", 0, "E=0 escape")],
                points=[(4, -100, "surface U")],
                xlim=(1, 12), ylim=(-280, 40), xlab="r", ylab="U(r)",
            ),
            "Escape means reaching the $E=0$ line so $r$ can go to infinity",
            "At $r=4$, $U=-100$. You need $K=+100$ there to make $E=0$, hence $\\tfrac12 v^2=100$ for $m=1$, $v=\\sqrt{200}$.",
        )
        + solved(
            26, "$GM=400$, $r=4$. Find $v_\\mathrm{esc}$.",
            [
                "$v=\\sqrt{2GM/r}=\\sqrt{200}$.",
                "$v=10\\sqrt{2}$.",
                "Circular $v$ was $10$, and $\\sqrt{2}\\times 10=10\\sqrt{2}$.",
            ],
            "$10\\sqrt{2}$",
            "",
            "Easy",
        )
        + solved(
            27, "Relate $v_\\mathrm{esc}$ to $v_\\mathrm{circ}$ at the same $r$.",
            [
                "$v_\\mathrm{circ}=\\sqrt{GM/r}$.",
                "$v_\\mathrm{esc}=\\sqrt{2GM/r}$.",
                "Ratio $\\sqrt{2}$.",
            ],
            "$v_\\mathrm{esc}=\\sqrt{2}\\,v_\\mathrm{circ}$",
            "",
            "Medium",
        )
        + solved(
            28, "Why is $E=0$ the escape condition with $U(\\infty)=0$?",
            [
                "At infinity, $U=0$, so $E=K_\\infty$.",
                "The smallest nonnegative $K_\\infty$ is $0$.",
                "Thus the threshold launch has $E=0$ already at the launch $r$.",
            ],
            "Barely reaching infinity with $K=0$ means $E=0$ everywhere on the trip.",
            "",
            "Hard",
        )
        + _ican([
            "I can compute $v_\\mathrm{esc}=\\sqrt{2GM/r}$.",
            "I can compare it with circular speed by a factor $\\sqrt{2}$.",
            "I can justify $E=0$ as the escape threshold.",
        ]),
        ("Using $\\tfrac12 mv^2=mgh$ with $h\\to\\infty$",
         "That energy would be infinite. The true $U$ approaches a finite $0$ from below, so a finite $v_\\mathrm{esc}$ exists."),
        ("Compute $v_\\mathrm{esc}$ at the $r$ where you launch",
         "From a high circular orbit you already have some $K$; the extra $\\Delta v$ to escape is less than from rest on the surface."),
        [
            "I can compute $v_\\mathrm{esc}=\\sqrt{2GM/r}$.",
            "I can compare it with circular speed by a factor $\\sqrt{2}$.",
            "I can justify $E=0$ as the escape threshold.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        [
            "Use $F=GMm/r^2$ as an inverse-square central force",
            "Get $g=GM/r^2$ and scale it with radius",
            "Derive circular $v=\\sqrt{GM/r}$",
            "Obtain Kepler's $T^2\\propto r^3$ from centripetal force",
            "Work with $U=-GMm/r$ and circular $E=-GMm/(2r)$",
            "Compute escape speed from $E=0$",
        ],
        c1 + c2 + c3 + c4 + c5 + c6,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Kinematics with Calculus', ['v = dx/dt and a = dv/dt', 'Integrating to recover motion', 'Variable acceleration', '2D motion with calculus', 'Relative velocity', 'Graphical calculus of motion']), ("Newton's Laws", ['Inertial frames', 'F_net = dp/dt', 'Friction models', 'Drag proportional to v', 'Constrained motion', 'Non-constant mass intro']), ('Work, Energy, and Power', ['Work as a line integral', 'Work-energy with variable F', 'Potential energy functions', 'Conservative vs nonconservative', 'Power as F·v', 'Energy diagrams']), ('Systems of Particles and Momentum', ['Center of mass by integral', 'Impulse as integral of F', 'Conservation of p', 'Variable mass rockets qualitative', 'Collisions in 1D and 2D', 'CM frame']), ('Rotation I', ['Angular kinematics', 'Torque as r × F', 'Moment of inertia', 'Parallel axis theorem', 'Rolling', 'Rotational work']), ('Rotation II and Angular Momentum', ['L = Iω and r × p', 'Conservation of L', 'Gyroscopic qualitative', 'Collisions changing I', 'Atwood with massive pulley', 'Justifying rotation FRQs']), ('Oscillations', ['SHM from F = -kx', 'Differential equation of SHM', 'Energy in SHM', 'Physical pendulum', 'Small-angle pendulum', 'Driven/damped qualitative']), ('Gravitation', ["Newton's law of gravity", 'g from GM/r^2', 'Orbit circular speed', 'Kepler from centripetal', 'Gravitational potential energy', 'Escape speed'])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>AP Physics C Mechanics Complete</h1>"
        f"<p><strong>For:</strong> <strong>AP Physics C: Mechanics</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
