#!/usr/bin/env python3
"""AP Physics C E&M Units 1–4: electrostatics, Gauss, potential/capacitors, DC circuits."""

from __future__ import annotations

import math

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, mq,
    xy_graph, sample_curve, field_lines_svg, series_circuit_svg,
    gauss_sphere_svg, energy_bars_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _pack(rows):
    qs = []
    for i, row in enumerate(rows, 1):
        text, ans, expl = row[0], row[1], row[2]
        dist = row[3] if len(row) > 3 else None
        qs.append(mq(text, ans, expl, i, distractors=dist))
    return qs


def _ican(items):
    return "<h3>I can</h3><ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def _gauss_cylinder_svg(w=300, h=220):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="150" y1="18" x2="150" y2="202" stroke="#b91c1c" stroke-width="3"/>'
        f'<text x="158" y="28" font-size="12" fill="#b91c1c">λ</text>'
        f'<ellipse cx="150" cy="48" rx="58" ry="16" fill="none" stroke="#4f46e5" '
        f'stroke-dasharray="6 4" stroke-width="2"/>'
        f'<ellipse cx="150" cy="172" rx="58" ry="16" fill="none" stroke="#4f46e5" '
        f'stroke-dasharray="6 4" stroke-width="2"/>'
        f'<line x1="92" y1="48" x2="92" y2="172" stroke="#4f46e5" stroke-dasharray="6 4" stroke-width="2"/>'
        f'<line x1="208" y1="48" x2="208" y2="172" stroke="#4f46e5" stroke-dasharray="6 4" stroke-width="2"/>'
        f'<line x1="150" y1="110" x2="236" y2="110" stroke="#059669" stroke-width="2.2"/>'
        f'<polygon points="232,105 246,110 232,115" fill="#059669"/>'
        f'<text x="214" y="100" font-size="12" fill="#059669">E</text>'
        f'<text x="24" y="214" font-size="11">Gaussian cylinder of radius r around an infinite line</text>'
        f"</svg>"
    )


def _gauss_plane_svg(w=300, h=200):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="20" y1="100" x2="280" y2="100" stroke="#0f172a" stroke-width="6"/>'
        f'<text x="22" y="88" font-size="12">infinite sheet, charge density σ</text>'
        f'<rect x="118" y="42" width="64" height="116" fill="none" stroke="#4f46e5" '
        f'stroke-dasharray="6 4" stroke-width="2"/>'
        f'<line x1="150" y1="100" x2="150" y2="28" stroke="#059669" stroke-width="2.2"/>'
        f'<polygon points="145,32 150,18 155,32" fill="#059669"/>'
        f'<line x1="150" y1="100" x2="150" y2="172" stroke="#059669" stroke-width="2.2"/>'
        f'<polygon points="145,168 150,182 155,168" fill="#059669"/>'
        f'<text x="160" y="40" font-size="12" fill="#059669">E</text>'
        f'<text x="160" y="176" font-size="12" fill="#059669">E</text>'
        f'<text x="40" y="196" font-size="11">Gaussian pillbox straddling the sheet</text>'
        f"</svg>"
    )


def _ring_axis_svg(w=320, h=230):
    """Uniform ring: dq sources, cancelled dE_perp, surviving axial dE at P."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<ellipse cx="160" cy="158" rx="92" ry="30" fill="none" stroke="#b91c1c" stroke-width="3"/>'
        f'<circle cx="252" cy="158" r="7" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="260" y="146" font-size="11">dq</text>'
        f'<circle cx="68" cy="158" r="7" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="24" y="146" font-size="11">dq</text>'
        f'<circle cx="160" cy="40" r="5" fill="#0f172a"/>'
        f'<text x="172" y="36" font-size="12">P</text>'
        f'<line x1="160" y1="158" x2="160" y2="40" stroke="#94a3b8" stroke-dasharray="4 3"/>'
        f'<line x1="252" y1="158" x2="168" y2="46" stroke="#4f46e5" stroke-width="1.6"/>'
        f'<polygon points="176,58 160,40 180,52" fill="#4f46e5"/>'
        f'<text x="214" y="92" font-size="11" fill="#4f46e5">dE</text>'
        f'<line x1="68" y1="158" x2="152" y2="46" stroke="#4f46e5" stroke-width="1.6"/>'
        f'<polygon points="144,58 160,40 140,52" fill="#4f46e5"/>'
        f'<line x1="118" y1="78" x2="148" y2="78" stroke="#059669" stroke-width="1.6"/>'
        f'<polygon points="118,78 128,73 128,83" fill="#059669"/>'
        f'<line x1="202" y1="78" x2="172" y2="78" stroke="#059669" stroke-width="1.6"/>'
        f'<polygon points="202,78 192,73 192,83" fill="#059669"/>'
        f'<text x="86" y="70" font-size="11" fill="#059669">dE⊥ cancel</text>'
        f'<text x="168" y="118" font-size="11" fill="#1d4ed8">dE_z add</text>'
        f'<text x="18" y="218" font-size="11">Ring on axis: sideways dE pieces cancel in pairs; only axial pieces remain</text>'
        f"</svg>"
    )


def _dipole_svg(w=280, h=180):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="90" cy="90" r="14" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="90" y="94" text-anchor="middle" font-size="12">+q</text>'
        f'<circle cx="190" cy="90" r="14" fill="#bfdbfe" stroke="#1d4ed8"/>'
        f'<text x="190" y="94" text-anchor="middle" font-size="12">−q</text>'
        f'<path d="M104 90 C130 40, 150 40, 176 90" fill="none" stroke="#4f46e5" stroke-width="1.6"/>'
        f'<path d="M104 90 C130 140, 150 140, 176 90" fill="none" stroke="#4f46e5" stroke-width="1.6"/>'
        f'<path d="M104 82 C140 70, 150 70, 176 82" fill="none" stroke="#6366f1" stroke-width="1.4"/>'
        f'<path d="M104 98 C140 110, 150 110, 176 98" fill="none" stroke="#6366f1" stroke-width="1.4"/>'
        f'<text x="70" y="170" font-size="11">electric dipole: field lines leave + and enter −</text>'
        f"</svg>"
    )


def _plates_svg(w=260, h=160):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="70" y="20" width="14" height="120" fill="#fecaca" stroke="#b91c1c"/>'
        f'<rect x="176" y="20" width="14" height="120" fill="#bfdbfe" stroke="#1d4ed8"/>'
        f'<line x1="84" y1="50" x2="176" y2="50" stroke="#4f46e5" stroke-width="1.5"/>'
        f'<line x1="84" y1="80" x2="176" y2="80" stroke="#4f46e5" stroke-width="1.5"/>'
        f'<line x1="84" y1="110" x2="176" y2="110" stroke="#4f46e5" stroke-width="1.5"/>'
        f'<polygon points="168,45 176,50 168,55" fill="#4f46e5"/>'
        f'<polygon points="168,75 176,80 168,85" fill="#4f46e5"/>'
        f'<polygon points="168,105 176,110 168,115" fill="#4f46e5"/>'
        f'<text x="48" y="86" font-size="12">+Q</text>'
        f'<text x="198" y="86" font-size="12">−Q</text>'
        f'<text x="112" y="154" font-size="11">uniform E = σ/ε₀</text>'
        f"</svg>"
    )


def _equipotential_svg(w=260, h=180):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="130" cy="90" r="14" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="130" y="94" text-anchor="middle" font-size="11">+q</text>'
        f'<circle cx="130" cy="90" r="40" fill="none" stroke="#059669" stroke-dasharray="5 3"/>'
        f'<circle cx="130" cy="90" r="62" fill="none" stroke="#059669" stroke-dasharray="5 3"/>'
        f'<circle cx="130" cy="90" r="84" fill="none" stroke="#059669" stroke-dasharray="5 3"/>'
        f'<line x1="144" y1="90" x2="214" y2="90" stroke="#4f46e5" stroke-width="1.6"/>'
        f'<polygon points="210,85 222,90 210,95" fill="#4f46e5"/>'
        f'<text x="8" y="22" font-size="11">dashed circles: equipotentials (constant V)</text>'
        f'<text x="168" y="82" font-size="11" fill="#4f46e5">E</text>'
        f"</svg>"
    )


def _parallel_circuit_svg(w=300, h=170):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="18" y="70" width="26" height="28" fill="#fef3c7" stroke="#0f172a"/>'
        f'<text x="16" y="62" font-size="11">ε</text>'
        f'<line x1="44" y1="84" x2="90" y2="84" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="90" y1="40" x2="90" y2="128" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M90 40 l10 -10 l10 20 l10 -20 l10 20 l10 -10" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<path d="M90 128 l10 -10 l10 20 l10 -20 l10 20 l10 -10" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<line x1="150" y1="40" x2="230" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="150" y1="128" x2="230" y2="128" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="230" y1="40" x2="230" y2="128" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="230" y1="84" x2="44" y2="84" stroke="#0f172a" stroke-width="2" stroke-dasharray="0"/>'
        f'<line x1="34" y1="98" x2="34" y2="84" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="108" y="28" font-size="11">R₁</text>'
        f'<text x="108" y="160" font-size="11">R₂</text>'
        f"</svg>"
    )


def _kirchhoff_loop_svg(w=320, h=170):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="30" y="70" width="26" height="28" fill="#fef3c7" stroke="#0f172a"/>'
        f'<text x="28" y="62" font-size="11">ε</text>'
        f'<line x1="56" y1="84" x2="110" y2="84" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M110 84 l8 -12 l8 24 l8 -24 l8 24 l8 -12" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<line x1="158" y1="84" x2="250" y2="84" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="250" y1="84" x2="250" y2="130" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="250" y1="130" x2="44" y2="130" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="44" y1="130" x2="44" y2="98" stroke="#0f172a" stroke-width="2"/>'
        f'<circle cx="200" cy="84" r="11" fill="#fff" stroke="#1d4ed8" stroke-width="2"/>'
        f'<text x="194" y="88" font-size="11">A</text>'
        f'<text x="118" y="58" font-size="11">R</text>'
        f'<text x="70" y="40" font-size="11">loop: ΣΔV = 0</text>'
        f"</svg>"
    )


def _conductor_shell_svg(w=280, h=220):
    """Conducting shell with cavity charge and a Gaussian surface in the metal."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="140" cy="100" r="86" fill="#cbd5e1" stroke="#0f172a" stroke-width="2"/>'
        f'<circle cx="140" cy="100" r="46" fill="#fff" stroke="#0f172a" stroke-width="2"/>'
        f'<circle cx="140" cy="100" r="66" fill="none" stroke="#4f46e5" stroke-dasharray="6 4" stroke-width="2.2"/>'
        f'<circle cx="140" cy="100" r="10" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="140" y="104" text-anchor="middle" font-size="11">+q</text>'
        f'<text x="168" y="38" font-size="11" fill="#4f46e5">dashed: Gaussian in the metal</text>'
        f'<text x="186" y="78" font-size="11">conductor</text>'
        f'<text x="118" y="72" font-size="11">cavity</text>'
        f'<text x="16" y="210" font-size="11">E = 0 in the metal, so flux through the dashed sphere is 0</text>'
        f"</svg>"
    )


def _two_loop_c_svg(w=340, h=180):
    """Two loops sharing a capacitor branch; KVL uses Q/C."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="78" width="24" height="26" fill="#fef3c7" stroke="#0f172a"/>'
        f'<text x="18" y="70" font-size="11">ε</text>'
        f'<line x1="32" y1="78" x2="32" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="32" y1="40" x2="70" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M70 40 l8 -12 l8 24 l8 -24 l8 24 l8 -12" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<text x="82" y="22" font-size="11">R₁</text>'
        f'<line x1="118" y1="40" x2="170" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="170" y1="40" x2="170" y2="62" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="158" y1="62" x2="182" y2="62" stroke="#1d4ed8" stroke-width="4"/>'
        f'<line x1="158" y1="76" x2="182" y2="76" stroke="#1d4ed8" stroke-width="4"/>'
        f'<text x="188" y="72" font-size="11">C</text>'
        f'<text x="188" y="88" font-size="11" fill="#1d4ed8">Q/C</text>'
        f'<line x1="170" y1="76" x2="170" y2="140" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="170" y1="40" x2="220" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M220 40 l8 -12 l8 24 l8 -24 l8 24 l8 -12" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<text x="232" y="22" font-size="11">R₂</text>'
        f'<line x1="268" y1="40" x2="310" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="310" y1="40" x2="310" y2="140" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="310" y1="140" x2="32" y2="140" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="32" y1="140" x2="32" y2="104" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="48" y="170" font-size="11">two loops; shared capacitor branch contributes Q/C in KVL</text>'
        f"</svg>"
    )


def _meter_svg(w=300, h=150):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="60" width="24" height="26" fill="#fef3c7" stroke="#0f172a"/>'
        f'<path d="M70 73 l8 -10 l8 20 l8 -20 l8 20 l8 -10" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<line x1="44" y1="73" x2="70" y2="73" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="118" y1="73" x2="200" y2="73" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="200" y1="73" x2="200" y2="110" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="200" y1="110" x2="32" y2="110" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="32" y1="110" x2="32" y2="86" stroke="#0f172a" stroke-width="2"/>'
        f'<circle cx="160" cy="73" r="12" fill="#fff" stroke="#b91c1c" stroke-width="2"/>'
        f'<text x="154" y="77" font-size="11">A</text>'
        f'<line x1="70" y1="40" x2="118" y2="40" stroke="#059669" stroke-width="2"/>'
        f'<line x1="70" y1="40" x2="70" y2="62" stroke="#059669" stroke-width="2"/>'
        f'<line x1="118" y1="40" x2="118" y2="62" stroke="#059669" stroke-width="2"/>'
        f'<text x="84" y="32" font-size="11" fill="#059669">V</text>'
        f'<text x="8" y="144" font-size="11">ammeter in series; voltmeter across R</text>'
        f"</svg>"
    )


# ===========================================================================
# UNIT 1: Electrostatics
# ===========================================================================

def _u1_questions():
    return _pack([
        ("Two point charges $+2.0\\,\\mu\\mathrm{C}$ and $+3.0\\,\\mu\\mathrm{C}$ sit $0.30\\,\\mathrm{m}$ apart in vacuum. Using $k=9.0\\times10^{9}$, the Coulomb force magnitude is",
         "0.60 N",
         "$F=k q_1 q_2/r^2=(9\\times10^9)(2\\times10^{-6})(3\\times10^{-6})/(0.30)^2=0.60\\,\\mathrm{N}$, repulsive.",
         ["0.20 N", "1.8 N", "6.0 N"]),
        ("A $+4.0\\,\\mu\\mathrm{C}$ charge and a $-2.0\\,\\mu\\mathrm{C}$ charge are $0.20\\,\\mathrm{m}$ apart. With $k=9.0\\times10^{9}$, $|F|$ equals",
         "1.8 N",
         "$F=(9\\times10^9)(4\\times10^{-6})(2\\times10^{-6})/(0.20)^2=1.8\\,\\mathrm{N}$, attractive.",
         ["0.90 N", "3.6 N", "9.0 N"]),
        ("If you double both charges in Coulomb's law and triple the separation, the force is multiplied by",
         "4/9",
         "New $F'\\propto (2q)(2q)/(3r)^2=4/9$ of the original $F$.",
         ["4/3", "2/3", "9/4"]),
        ("Coulomb's law is an inverse-square law. Compared with $r$, the force at $2r$ is",
         "1/4 as large",
         "$(2r)^2=4r^2$, so $F$ drops by a factor of $4$.",
         ["1/2 as large", "twice as large", "unchanged"]),
        ("Two equal charges $+q$ experience $F=0.90\\,\\mathrm{N}$ at $r=0.10\\,\\mathrm{m}$. Using $k=9.0\\times10^{9}$, each $|q|$ is",
         "$1.0\\,\\mu\\mathrm{C}$",
         "$0.90=k q^2/(0.10)^2\\Rightarrow q^2=10^{-12}\\Rightarrow q=1.0\\times10^{-6}\\,\\mathrm{C}$.",
         ["$2.0\\,\\mu\\mathrm{C}$", "$0.10\\,\\mu\\mathrm{C}$", "$10\\,\\mu\\mathrm{C}$"]),
        ("The electric field $\\vec{E}$ at a point is defined as the electric force on a small test charge $q_0$ divided by $q_0$. SI unit of $E$ is",
         "N/C",
         "$\\vec{E}=\\vec{F}/q_0$, so newtons per coulomb (also V/m).",
         ["N", "C", "J"]),
        ("A lone $+1.0\\,\\mu\\mathrm{C}$ point charge. Using $k=9.0\\times10^{9}$, $|E|$ at $r=0.10\\,\\mathrm{m}$ is",
         "$9.0\\times10^{5}\\,\\mathrm{N/C}$",
         "$E=kq/r^2=(9\\times10^9)(1\\times10^{-6})/0.01=9.0\\times10^{5}\\,\\mathrm{N/C}$ outward.",
         ["$9.0\\times10^{3}\\,\\mathrm{N/C}$", "$9.0\\times10^{7}\\,\\mathrm{N/C}$", "$1.0\\times10^{5}\\,\\mathrm{N/C}$"]),
        ("Charges $+q$ at $x=0$ and $+q$ at $x=2a$ on the $x$-axis. Net $\\vec{E}$ at the midpoint $x=a$ is",
         "zero",
         "Equal magnitudes, opposite directions, so the vectors cancel.",
         ["$2kq/a^2$ to the right", "$kq/a^2$ to the left", "$4kq/a^2$ toward $+x$"]),
        ("A $+4.0\\,\\mu\\mathrm{C}$ charge is at the origin and $-2.0\\,\\mu\\mathrm{C}$ is at $x=0.40\\,\\mathrm{m}$. Using $k=9.0\\times10^{9}$, $E$ at $x=0.20\\,\\mathrm{m}$ points",
         "to $+x$ with $1.35\\times10^{6}\\,\\mathrm{N/C}$",
         "Each contribution is to $+x$: $k(4\\times10^{-6})/(0.20)^2=9.0\\times10^{5}$ and $k(2\\times10^{-6})/(0.20)^2=4.5\\times10^{5}$; sum $1.35\\times10^{6}\\,\\mathrm{N/C}$.",
         ["to $-x$ with $4.5\\times10^{5}\\,\\mathrm{N/C}$", "zero", "to $+x$ with $4.5\\times10^{5}\\,\\mathrm{N/C}$"]),
        ("Superposition for $\\vec{E}$ means you",
         "add field vectors from each source, then find the resultant",
         "Never add magnitudes blindly when directions differ.",
         ["add only the magnitudes of each $E$", "multiply the two fields", "average the two fields"]),
        ("A uniformly charged thin ring of radius $R$ and total charge $Q$. On the axis a distance $z$ from the center, $E$ points along the axis and has magnitude",
         "$kQz/(z^2+R^2)^{3/2}$",
         "Each $dE_\\perp$ cancels by symmetry; the axial pieces integrate to that formula.",
         ["$kQ/z^2$", "$kQ/R^2$", "$kQ/(z^2+R^2)$"]),
        ("A finite rod on the $x$-axis from $-L$ to $L$ with uniform $\\lambda>0$. At a point on the perpendicular bisector, $\\vec{E}$ is",
         "perpendicular to the rod, away from the rod",
         "Parallel components cancel; leftover $E$ is along the bisector.",
         ["parallel to the rod", "zero by symmetry", "toward the rod"]),
        ("To find $E$ of a continuous charge you replace $q$ by $dq$ and",
         "integrate $\\vec{dE}=k\\,dq\\,\\hat{r}/r^2$ with a consistent origin",
         "Choose $dq=\\lambda\\,dx$, $\\sigma\\,dA$, or $\\rho\\,dV$ to match the distribution.",
         ["take only the largest $dq$", "use Gauss's law with no symmetry check", "set $E=kq/r^2$ using the total $Q$ at the nearest point"]),
        ("An infinite line with uniform $\\lambda$ is not a Unit 1 integral you must grind by hand on AP C, but the symmetry already tells you $\\vec{E}$ is",
         "radial, depending only on perpendicular distance",
         "That cylindrical symmetry is why Gauss is the efficient later tool.",
         ["parallel to the line", "zero everywhere", "strongest at infinity"]),
        ("At the geometric center of a uniformly charged thin disk, the in-plane field is",
         "zero by symmetry",
         "Radial pieces cancel in pairs; $E_z$ is also zero at $z=0$ by odd symmetry through the plane.",
         ["infinite", "equal to $kQ/R^2$", "equal to $\\sigma/\\varepsilon_0$"]),
        ("An electric dipole is $+q$ and $-q$ separated by vector $\\vec{p}=q\\vec{d}$ from the negative to the positive charge. In a uniform $\\vec{E}$, the net force on the dipole is",
         "zero",
         "Equal-and-opposite forces on $\\pm q$ cancel; a torque $\\vec{\\tau}=\\vec{p}\\times\\vec{E}$ may remain.",
         ["$qE$ toward higher $E$", "$2qE$", "infinite"]),
        ("Far from a dipole, along the dipole axis, $|E|$ falls off approximately as",
         "$1/r^3$",
         "The two Coulomb fields nearly cancel, leaving a next-order $1/r^3$ remainder.",
         ["$1/r^2$", "$1/r$", "$1/r^4$"]),
        ("Field lines of a dipole",
         "leave the positive charge and enter the negative charge",
         "Lines begin on $+$ and end on $-$; density suggests $|E|$.",
         ["form closed loops around both charges", "never exist between the charges", "point from $-$ to $+$ in the interior"]),
        ("In a nonuniform field, a dipole can feel a net force toward",
         "the region of stronger $|E|$ if it is aligned with $\\vec{E}$",
         "The charge sitting in the stronger field feels a larger force.",
         ["always the weaker field", "always perpendicular to $\\vec{p}$", "nowhere; net force is always zero"]),
        ("Qualitatively, midway between $+q$ and $-q$ of a dipole (on the perpendicular bisector), $\\vec{E}$ is",
         "antiparallel to $\\vec{p}$",
         "Both fields have components opposite $\\vec{p}$.",
         ["parallel to $\\vec{p}$", "zero", "perpendicular to the page"]),
        ("A particle with charge $q=2.0\\,\\mu\\mathrm{C}$ and mass $m=4.0\\times10^{-4}\\,\\mathrm{kg}$ sits in a uniform $E=200\\,\\mathrm{N/C}$. Its acceleration magnitude is",
         "$1.0\\,\\mathrm{m/s^2}$",
         "$F=qE=4.0\\times10^{-4}\\,\\mathrm{N}$, so $a=F/m=1.0\\,\\mathrm{m/s^2}$.",
         ["$0.50\\,\\mathrm{m/s^2}$", "$2.0\\,\\mathrm{m/s^2}$", "$200\\,\\mathrm{m/s^2}$"]),
        ("In a uniform electric field, a charge's path is a straight line if $\\vec{v}$ is",
         "parallel or antiparallel to $\\vec{E}$",
         "Then $\\vec{F}=q\\vec{E}$ does not change the direction of $\\vec{v}$.",
         ["always perpendicular to $\\vec{E}$", "zero only", "circular always"]),
        ("If only a uniform $\\vec{E}$ acts, kinetic energy of a positive charge",
         "increases when the charge moves in the direction of $\\vec{E}$",
         "The field does positive work $qEd$ when displacement is along $\\vec{E}$.",
         ["always decreases", "is conserved because $E$ is conservative? No — $K$ can change while $U$ drops", "is independent of $q$"]),
        ("A proton ($q=+e$) is released from rest in uniform $E$. Compared with an electron released from rest in the same $E$, the proton's acceleration is",
         "much smaller and opposite in direction",
         "Same $|F|=eE$, but $m_p\\gg m_e$, and the force on the electron is opposite.",
         ["identical", "much larger", "zero"]),
        ("Work by a static electric field is path-independent. That is why later we will define",
         "electric potential $V$",
         "Conservative $\\vec{E}$ $\\Rightarrow$ a scalar $V$ with $\\vec{E}=-\\nabla V$.",
         ["magnetic flux", "resistance", "drift speed"]),
        ("On a field map, lines are denser where $|E|$ is",
         "larger",
         "Line density is a qualitative stand-in for field strength.",
         ["smaller", "zero", "undefined"]),
        ("Electric field lines never",
         "cross",
         "Two directions at one point would mean two $\\vec{E}$ vectors.",
         ["begin on positive charge", "end on negative charge", "spread in empty space"]),
        ("Near an isolated negative point charge, field lines",
         "point inward toward the charge",
         "A positive test charge would be pulled in.",
         ["point outward", "form circles around the charge", "are absent"]),
        ("Where field lines are equally spaced, parallel, and straight, $\\vec{E}$ is",
         "uniform",
         "Classic sketch between oppositely charged plates.",
         ["zero", "inverse-square", "purely dipole"]),
        ("A field map shows lines entering a region and none leaving. That region contains",
         "net negative charge",
         "Lines terminate on negative charge (Gauss, Unit 2).",
         ["net positive charge", "no charge", "only a dipole with zero net charge and no lines ending"]),
        ("A $+6.0\\,\\mu\\mathrm{C}$ charge is $0.50\\,\\mathrm{m}$ from a $+2.0\\,\\mu\\mathrm{C}$ charge. Using $k=9.0\\times10^{9}$, $|F|$ is",
         "0.432 N",
         "$F=(9\\times10^9)(6\\times10^{-6})(2\\times10^{-6})/(0.50)^2=0.432\\,\\mathrm{N}$.",
         ["0.216 N", "0.864 N", "4.32 N"]),
        ("Three charges $+q,+q,-q$ at the corners of an equilateral triangle. The net force on the $-q$ is along",
         "the altitude toward the side joining the two $+q$ charges",
         "The two attractions are equal; their resultant bisects the angle.",
         ["away from the triangle", "along a side", "zero"]),
        ("If $\\vec{E}=\\langle 3,0\\rangle\\,\\mathrm{N/C}$ and $\\vec{E}=\\langle 0,-4\\rangle\\,\\mathrm{N/C}$ from two sources, $|\\vec{E}_{\\mathrm{net}}|$ is",
         "5 N/C",
         "Orthogonal components: $\\sqrt{3^2+4^2}=5$.",
         ["7 N/C", "1 N/C", "12 N/C"]),
        ("A uniformly charged rod of length $L$ and charge $Q$ lies on $0\\le x\\le L$. The axial field $E_x$ at $x=2L$ equals",
         "$kQ/(2L^2)$",
         "$E=k\\lambda\\int_0^L dx/(2L-x)^2=k(Q/L)(1/L-1/(2L))=kQ/(2L^2)$.",
         ["$kQ/(4L^2)$", "$kQ/L^2$", "$kQ/(8L^2)$"]),
        ("At the center of a uniformly charged thin circular arc subtending $90^\\circ$ with radius $R$ and charge $Q$, $|E|$ is",
         "$\\dfrac{2kQ\\sqrt{2}}{\\pi R^2}$",
         "$E=(k\\lambda/R)\\sqrt{2}$ with $\\lambda=2Q/(\\pi R)$, so $E=2kQ\\sqrt{2}/(\\pi R^2)$.",
         ["$kQ/R^2$", "0", "$kQ/(\\pi R^2)$"]),
        ("Two infinite sheets have $\\sigma$ and $-\\sigma$. Between them, $E$ from superposition is",
         "$\\sigma/\\varepsilon_0$",
         "Each nonconducting sheet contributes $\\sigma/(2\\varepsilon_0)$ in the same direction between them.",
         ["$\\sigma/(2\\varepsilon_0)$", "0", "$2\\sigma/\\varepsilon_0$"]),
        ("Outside those same two sheets (to the left of both), net $E$ is",
         "zero",
         "The two $\\sigma/(2\\varepsilon_0)$ contributions oppose.",
         ["$\\sigma/\\varepsilon_0$", "$\\sigma/(2\\varepsilon_0)$", "$2\\sigma/\\varepsilon_0$"]),
        ("A positive test charge released from rest on a field map will start to move",
         "tangent to the local field line, in the line's direction",
         "$\\vec{F}=q\\vec{E}$ with $q>0$.",
         ["opposite the field line", "perpendicular to the line", "in a circle"]),
        ("If you reverse the sign of every source charge, every field line",
         "reverses direction",
         "$\\vec{E}$ flips; magnitudes stay the same.",
         ["disappears", "becomes denser", "is unchanged"]),
        ("Units of $k$ in $F=kq_1q_2/r^2$ are",
         "$\\mathrm{N\\cdot m^2/C^2}$",
         "Also $1/(4\\pi\\varepsilon_0)$.",
         ["N/C", "C²/N", "J/C"]),
        ("A charge $q$ moves $\\Delta\\vec{\\ell}$ in uniform $\\vec{E}$. Work by the electric force is",
         "$q\\vec{E}\\cdot\\Delta\\vec{\\ell}$",
         "Constant force: $W=\\vec{F}\\cdot\\Delta\\vec{\\ell}$.",
         ["$q|E||\\Delta\\ell|$ always", "$0$ always", "$qE/|\\Delta\\ell|$"]),
        ("Two charges of like sign are released from rest. Their accelerations",
         "increase as they separate? No — $F$ decreases with $r$, so accelerations decrease while they still recede",
         "Inverse-square force weakens with distance.",
         ["stay constant", "increase forever", "become attractive"]),
        ("The electric field of a point charge is conservative. Circulation $\\oint\\vec{E}\\cdot d\\vec{\\ell}$ around a closed loop with no changing $B$ is",
         "zero",
         "Electrostatics: $\\nabla\\times\\vec{E}=0$.",
         ["$q/\\varepsilon_0$", "$4\\pi kq$", "infinite"]),
        ("A dipole $\\vec{p}$ in uniform $\\vec{E}$ has potential energy $U=-\\vec{p}\\cdot\\vec{E}$. Stable alignment is",
         "$\\vec{p}$ parallel to $\\vec{E}$",
         "Minimum $U$ when $\\cos\\theta=1$.",
         ["$\\vec{p}$ antiparallel to $\\vec{E}$", "$\\vec{p}$ perpendicular to $\\vec{E}$", "any angle"]),
        ("If $E=300\\,\\mathrm{N/C}$ uniform over $2.0\\,\\mathrm{cm}$, a $+2.0\\,\\mu\\mathrm{C}$ charge starting from rest gains kinetic energy",
         "$1.2\\times10^{-5}\\,\\mathrm{J}$",
         "$W=qEd=(2\\times10^{-6})(300)(0.020)=1.2\\times10^{-5}\\,\\mathrm{J}$.",
         ["$1.2\\times10^{-3}\\,\\mathrm{J}$", "$6.0\\times10^{-6}\\,\\mathrm{J}$", "0"]),
        ("Field maps between a sharp positive point and a broad negative conductor are densest",
         "near the sharp point",
         "Charge crowds at sharp convex surfaces; $|E|$ is large there.",
         ["far from all conductors", "only inside the conductor", "uniform everywhere"]),
        ("AP Stretch: A rod on $0\\le x\\le L$ has $\\lambda=bx$ with $b$ constant. $E_x$ at $x=-d$ ($d>0$) on the axis is $k$ times",
         "$\\int_0^L bx\\,dx/(d+x)^2$",
         "$dq=bx\\,dx$, $r=d+x$, all $dE$ to $-x$ if $b>0$ when the field point is to the left; the integral is the exact expression.",
         ["$bL/(d)^2$", "$\\int_0^L b\\,dx/(d+x)$", "$bL^2/2$"]),
        ("AP Stretch: Uniform ring $Q$, radius $R$. On the axis at $z=R$, the ratio $E_z/(kQ/R^2)$ equals",
         "$\\sqrt{2}/4$",
         "$E_z=kQR/(2R^2)^{3/2}=kQ/(R^2\\cdot 2\\sqrt{2})=(\\sqrt{2}/4)\\,kQ/R^2$.",
         ["$1/2$", "$1/\\sqrt{2}$", "$2\\sqrt{2}$"]),
        ("AP Stretch: Rod on $0\\le x\\le L$ with $\\lambda=\\alpha x$. Field point at $x=2L$. Then $E_x=k\\alpha\\int_0^L x\\,dx/(2L-x)^2$ and the integral equals",
         "$1-\\ln 2$",
         "Substitute $u=2L-x$: $\\int_L^{2L}(2L/u^2-1/u)\\,du=1-\\ln 2$.",
         ["$\\ln 2$", "$1/2$", "$L$"]),
        ("AP Stretch: Uniform disk radius $R$, $\\sigma>0$. On the axis, $E_z=(\\sigma/(2\\varepsilon_0))\\bigl(1-z/\\sqrt{z^2+R^2}\\bigr)$ for $z>0$. As $R\\to\\infty$, $E_z\\to$",
         "$\\sigma/(2\\varepsilon_0)$",
         "Infinite nonconducting sheet limit.",
         ["$\\sigma/\\varepsilon_0$", "0", "$\\sigma/(4\\varepsilon_0)$"]),
        ("AP Stretch: Two charges $+2q$ at $x=-a$ and $-q$ at $x=+a$. The point on the $x$-axis to the right of $+a$ where $E=0$ satisfies, with distance $s$ beyond $+a$,",
         "$2/(2a+s)^2=1/s^2$",
         "Set $k(2q)/(2a+s)^2=kq/s^2$ (same direction would not cancel — actually to the right of $-q$, both fields can oppose: $+2q$ pushes $+$, $-q$ pulls $+$, so they can cancel).",
         ["$2/s^2=1/(2a+s)^2$", "$2q=q$", "no such point"]),
        ("AP Stretch: A charge $q$ with mass $m$ starts at rest at $x=0$ where $E_x=cx$ (unphysical but a calculus drill, $c$ constant). From $m\\ddot x=qcx$, if $c>0$ and $q>0$ the motion is",
         "exponentially runaway (hyperbolic functions)",
         "$\\ddot x=\\omega^2 x$ with $\\omega^2=qc/m>0$ is not SHM; solutions are $A e^{\\omega t}+B e^{-\\omega t}$.",
         ["simple harmonic", "uniform circular", "constant velocity"]),
        ("AP Stretch: Work to assemble three charges $+q$ at the vertices of an equilateral triangle of side $a$, taking $U=0$ at infinite separation, is",
         "$3kq^2/a$",
         "Three unique pairs, each $kq^2/a$.",
         ["$kq^2/a$", "$6kq^2/a$", "0"]),
        ("AP Stretch: Field of a dipole on the perpendicular bisector, distance $r\\gg d$ from the center, has magnitude about",
         "$kp/r^3$",
         "Standard far-field bisector result $E=kp/r^3$ (sometimes written with a factor $1$ in this convention of $p=qd$).",
         ["$kp/r^2$", "$kqd/r^2$", "0"]),
        ("AP Stretch: Continuous $\\lambda=\\lambda_0\\cos(\\pi x/L)$ on $-L/2\\le x\\le L/2$. Net charge on the rod is",
         "$2\\lambda_0 L/\\pi$",
         "$\\int_{-L/2}^{L/2}\\lambda_0\\cos(\\pi x/L)\\,dx=(L/\\pi)\\lambda_0\\sin(\\pi x/L)|_{-L/2}^{L/2}=2\\lambda_0 L/\\pi$.",
         ["zero", "$\\lambda_0 L$", "$\\lambda_0 L/\\pi$"]),
    ])


def build_unit1():
    title = "AP Physics C E&M Unit 1: Electrostatics"
    description = (
        "Coulomb's law, superposition of electric fields, fields of continuous charge, "
        "dipoles, motion in $\\vec{E}$, and field maps — with calculus-ready integrals."
    )
    ican1 = [
        "I can compute Coulomb forces with $k=9\\times10^9$ and the correct attractive/repulsive direction.",
        "I can write $F=k|q_1 q_2|/r^2$ and scale $F$ when charges or $r$ change.",
        "I can identify inverse-square dependence and SI units of $k$.",
    ]
    c1 = concept_block(
        "1. Coulomb's law",
        [
            "Electric charge comes in two signs. Same signs repel; opposite signs attract. The SI unit of charge is the coulomb ($\\mathrm{C}$).",
            "Coulomb's law gives the force between two point charges in vacuum: the magnitude is $F=k |q_1 q_2|/r^2$ with $k=1/(4\\pi\\varepsilon_0)=9.0\\times10^{9}\\,\\mathrm{N\\cdot m^2/C^2}$.",
            "The direction lies along the line joining the charges. Write it as a vector $\\vec{F}_{12}=k q_1 q_2\\,\\hat{r}_{12}/r^2$ with a consistent choice of $\\hat{r}$.",
            "If $q_1=+2.0\\,\\mu\\mathrm{C}$, $q_2=+3.0\\,\\mu\\mathrm{C}$, and $r=0.30\\,\\mathrm{m}$, then $F=(9.0\\times10^9)(2.0\\times10^{-6})(3.0\\times10^{-6})/(0.30)^2=0.60\\,\\mathrm{N}$, repulsive.",
            "If either charge flips sign, the magnitude is unchanged but the force becomes attractive. Never drop the signs until you have decided direction separately.",
            "Coulomb's law is the electrostatic analog of Newton's gravity law, except charge can cancel and $k$ is huge, so everyday charges of microcoulombs already produce newtons of force.",
        ],
        "Every later E&M idea — field, flux, potential, circuits — starts from this inverse-square force between charges. If Coulomb's law is shaky, Gauss and Faraday will feel like symbols with no meaning.",
        "Draw both charges, mark the line between them, compute the magnitude with $k q_1 q_2/r^2$, then put arrows using same-repel / opposite-attract. Convert $\\mu\\mathrm{C}$ to $10^{-6}\\,\\mathrm{C}$ before multiplying.",
        lesson_figure(
            field_lines_svg(kind="positive"),
            "Isolated positive point charge",
            "Force on a positive test charge is radially outward, falling as $1/r^2$.",
        )
        + solved(1, "Find the force magnitude between $+2.0\\,\\mu\\mathrm{C}$ and $+3.0\\,\\mu\\mathrm{C}$ separated by $0.30\\,\\mathrm{m}$.",
                 ["Convert: $q_1=2.0\\times10^{-6}\\,\\mathrm{C}$, $q_2=3.0\\times10^{-6}\\,\\mathrm{C}$, $r=0.30\\,\\mathrm{m}$.",
                  "Compute $q_1 q_2/r^2=(6.0\\times10^{-12})/0.090=6.67\\times10^{-11}$.",
                  "Multiply by $k=9.0\\times10^9$ to get $F=0.60\\,\\mathrm{N}$ (repulsive)."],
                 "$0.60\\,\\mathrm{N}$ (repulsive)", "", "Easy")
        + solved(2, "$+4.0\\,\\mu\\mathrm{C}$ and $-2.0\\,\\mu\\mathrm{C}$ are $0.20\\,\\mathrm{m}$ apart. Find $|F|$ and state attract or repel.",
                 ["$|q_1 q_2|=8.0\\times10^{-12}\\,\\mathrm{C}^2$, $r^2=0.040\\,\\mathrm{m}^2$.",
                  "$F=(9.0\\times10^9)(8.0\\times10^{-12})/0.040=1.8\\,\\mathrm{N}$.",
                  "Opposite signs $\\Rightarrow$ attraction along the joining line."],
                 "$1.8\\,\\mathrm{N}$, attractive", "", "Medium")
        + solved(3, "Charges $q$ and $2q$ of like sign are $r$ apart with force $F$. If both charges double and the separation becomes $3r$, the new force in terms of $F$ is",
                 ["Original $F=k(q)(2q)/r^2=2kq^2/r^2$.",
                  "New charges $2q$ and $4q$, new distance $3r$: $F'=k(2q)(4q)/(9r^2)=8kq^2/(9r^2)$.",
                  "$F'/F=(8/9)/(2)=4/9$, so $F'=(4/9)F$."],
                 "$(4/9)F$", "Scale with $q_1 q_2/r^2$; do not mix radius into the charges.", "Hard")
        + _ican(ican1),
        ("Using $r$ instead of $r^2$, or forgetting to convert $\\mu\\mathrm{C}$",
         "A factor of $10^{-6}$ missed twice is $10^{-12}$ in the product. Write charges in coulombs and square the separation in meters before multiplying by $k$."),
        ("Magnitude first, direction second",
         "Compute $k|q_1 q_2|/r^2$, then mark attract/repel on the sketch. Mixing a minus sign into $k$ is how people get a repulsive pair to 'attract' on paper."),
        ican1,
        1,
    )

    ican2 = [
        "I can add electric-field vectors from several point charges.",
        "I can use $E=kq/r^2$ for a point source and superposition for several sources.",
        "I can spot points where symmetry forces $\\vec{E}=\\vec{0}$.",
    ]
    c2 = concept_block(
        "2. Superposition of E",
        [
            "The electric field $\\vec{E}$ at a location is the force per unit test charge: $\\vec{E}=\\vec{F}/q_0$ in the limit of a tiny $q_0$ that does not disturb the sources.",
            "A single point charge produces $E=kq/r^2$, radially out if $q>0$ and in if $q<0$. The SI unit is $\\mathrm{N/C}$ (identical to $\\mathrm{V/m}$).",
            "Superposition: the net field is the vector sum of the fields of each source, computed as if the others were absent.",
            "Example: $+q$ at $x=0$ and $+q$ at $x=2a$. At the midpoint, the two fields are equal in size and opposite, so $\\vec{E}_{\\mathrm{net}}=\\vec{0}$.",
            "When directions are not opposite, resolve into components. Two perpendicular fields of $3\\,\\mathrm{N/C}$ and $4\\,\\mathrm{N/C}$ make a $5\\,\\mathrm{N/C}$ resultant.",
            "Never add the magnitudes $kq/r^2$ unless you have already checked that the vectors point the same way.",
        ],
        "Circuits, capacitors, and Gauss's law all assume you can add fields. A wrong direction on one vector poisons the entire resultant.",
        "For each source, write $E=k|q|/r^2$, draw an arrow as a positive test charge would feel, then add components. Look for midpoints of like charges where cancellation is obvious.",
        lesson_figure(
            field_lines_svg(kind="positive"),
            "Field of one positive source",
            "A second source's field is drawn the same way, then the arrows are added as vectors.",
        )
        + solved(1, "What is $|E|$ due to $+1.0\\,\\mu\\mathrm{C}$ at $0.10\\,\\mathrm{m}$? Use $k=9.0\\times10^{9}$.",
                 ["$q=1.0\\times10^{-6}\\,\\mathrm{C}$, $r^2=0.010\\,\\mathrm{m}^2$.",
                  "$E=(9.0\\times10^9)(1.0\\times10^{-6})/0.010=9.0\\times10^{5}\\,\\mathrm{N/C}$.",
                  "Direction: radially outward from the positive charge."],
                 "$9.0\\times10^{5}\\,\\mathrm{N/C}$ outward", "", "Easy")
        + solved(2, "$+q$ at $x=0$ and $+q$ at $x=2a$. Net $E$ at $x=a$?",
                 ["Distance from each charge to the midpoint is $a$.",
                  "Each field has magnitude $kq/a^2$, one to $+x$ and one to $-x$.",
                  "They cancel: $\\vec{E}=\\vec{0}$."],
                 "$\\vec{0}$", "", "Medium")
        + solved(3, "$+4.0\\,\\mu\\mathrm{C}$ at the origin, $-2.0\\,\\mu\\mathrm{C}$ at $x=0.40\\,\\mathrm{m}$. Find $\\vec{E}$ at $x=0.20\\,\\mathrm{m}$. $k=9.0\\times10^{9}$.",
                 ["Distance to each charge is $0.20\\,\\mathrm{m}$.",
                  "From $+4\\,\\mu\\mathrm{C}$: $E=9.0\\times10^{5}\\,\\mathrm{N/C}$ to $+x$. From $-2\\,\\mu\\mathrm{C}$: a positive test charge is pulled right, $E=4.5\\times10^{5}\\,\\mathrm{N/C}$ to $+x$.",
                  "Net $E=1.35\\times10^{6}\\,\\mathrm{N/C}$ in the $+x$ direction."],
                 "$1.35\\times10^{6}\\,\\mathrm{N/C}$ toward $+x$", "Both arrows can point the same way when one source is negative.", "Hard")
        + _ican(ican2),
        ("Adding $E$ magnitudes without a sketch",
         "If one field is to the right and one to the left, the net is a difference, not a sum. Always draw the two arrows on a positive test charge."),
        ("Place an imaginary $+$ at the field point",
         "The direction of $\\vec{E}$ is the direction of the force on that imaginary positive charge. That one habit prevents most superposition errors."),
        ican2,
        6,
    )

    ican3 = [
        "I can set up $\\vec{E}=\\int k\\,dq\\,\\hat{r}/r^2$ for a rod, ring, or arc.",
        "I can cancel components by symmetry before integrating.",
        "I can choose $dq=\\lambda\\,dx$, $\\sigma\\,dA$, or $\\rho\\,dV$ to match the object.",
    ]
    c3 = concept_block(
        "3. Electric field of distributions",
        [
            "A continuous charge is a crowd of tiny $dq$. Each piece makes $d\\vec{E}=k\\,dq\\,\\hat{r}/r^2$. The total field is the vector integral of $d\\vec{E}$.",
            "Match the geometry: a thin rod uses $dq=\\lambda\\,dx$, a surface uses $dq=\\sigma\\,dA$, a volume uses $dq=\\rho\\,dV$.",
            "Symmetry first. On the axis of a uniformly charged ring, sideways components cancel, leaving only $E_z=kQz/(z^2+R^2)^{3/2}$.",
            "On the perpendicular bisector of a finite symmetric rod, components parallel to the rod cancel. You integrate only the leftover perpendicular pieces.",
            "Do not replace a spread-out charge by a point charge at the nearest point. That ignores most of the integral and is almost always wrong.",
            "If the distribution has spherical, cylindrical, or planar symmetry, Unit 2 (Gauss) may replace a painful integral — but only after you justify the symmetry.",
        ],
        "AP Physics C lives on these integrals. FRQs ask you to write $dE$, drop cancelled components, and integrate, even when they do not demand a fully simplified number.",
        "Name $dq$, write $r$ from each $dq$ to the field point, kill components that cancel, integrate what remains. Keep $k$ outside if it is constant.",
        lesson_figure(
            _ring_axis_svg(),
            "Uniform ring: two $dq$ pieces and the field point $P$ on the axis",
            "Perpendicular $dE$ arrows from opposite $dq$ cancel. Only the axial pieces survive to be integrated.",
        )
        + solved(1, "On the axis of a uniformly charged ring, why is $\\vec{E}$ along the axis?",
                 ["Every $dq$ has a twin on the opposite side of the ring.",
                  "The components of $d\\vec{E}$ perpendicular to the axis cancel in pairs.",
                  "Only axial components survive, so $\\vec{E}$ is along the axis (or zero at the center)."],
                 "perpendicular components cancel; $E$ is axial", "", "Easy")
        + solved(2, "A rod lies on $0\\le x\\le L$ with uniform $\\lambda$. Write $E_x$ at $x=2L$ on the axis as an integral.",
                 ["Take $dq=\\lambda\\,dx$ at position $x$, with $0\\le x\\le L$.",
                  "Distance from $dq$ to the point $x=2L$ is $2L-x$.",
                  "$E_x=k\\lambda\\int_0^L dx/(2L-x)^2$, pointing away from the rod if $\\lambda>0$."],
                 "$E_x=k\\lambda\\int_0^L (2L-x)^{-2}\\,dx$", "", "Medium")
        + solved(3, "Evaluate that integral for $E_x$ at $x=2L$.",
                 ["Antiderivative of $(2L-x)^{-2}$ is $1/(2L-x)$.",
                  "Evaluate from $0$ to $L$: $1/L-1/(2L)=1/(2L)$.",
                  "$E_x=k\\lambda/(2L)$. With $\\lambda=Q/L$ this is $kQ/(2L^2)$."],
                 "$k\\lambda/(2L)=kQ/(2L^2)$", "Keep the substitution $u=2L-x$ if the chain rule feels shaky.", "Hard")
        + _ican(ican3),
        ("Treating the whole $Q$ as a point at the closest end",
         "That would give $kQ/L^2$ at $x=2L$, which is not $kQ/(2L^2)$. The integral averages over all the different distances."),
        ("Cancel before you integrate",
         "If symmetry kills $E_x$, do not integrate $dE_x$. Write one sentence naming the cancelled components, then integrate the rest."),
        ican3,
        11,
    )

    ican4 = [
        "I can define $\\vec{p}=q\\vec{d}$ from $-$ to $+$.",
        "I can state that a dipole in uniform $E$ has zero net force but possible torque $\\vec{p}\\times\\vec{E}$.",
        "I can recall that the far dipole field falls as $1/r^3$.",
    ]
    c4 = concept_block(
        "4. Dipole qualitative",
        [
            "An electric dipole is a pair $+q$ and $-q$ separated by a small distance. The dipole moment $\\vec{p}=q\\vec{d}$ points from the negative charge toward the positive charge.",
            "In a uniform field, the force on $+q$ and the force on $-q$ are equal and opposite, so the net force is zero. A torque $\\vec{\\tau}=\\vec{p}\\times\\vec{E}$ still tries to align $\\vec{p}$ with $\\vec{E}$.",
            "Field lines leave the positive end and enter the negative end. Between the charges, $\\vec{E}$ runs roughly from $+$ to $-$, opposite $\\vec{p}$ on the perpendicular bisector.",
            "Far away, the two Coulomb fields nearly cancel. What remains falls off like $1/r^3$, faster than a point charge's $1/r^2$.",
            "In a nonuniform field, the two forces are no longer equal. A dipole aligned with $\\vec{E}$ is pulled toward stronger $|E|$.",
            "Potential energy $U=-\\vec{p}\\cdot\\vec{E}$ is lowest when $\\vec{p}$ is parallel to $\\vec{E}$ (stable) and highest when antiparallel (unstable).",
        ],
        "Dipoles are how polar molecules and dielectric materials respond to fields. The same $\\vec{p}\\times\\vec{E}$ idea returns as $\\vec{\\mu}\\times\\vec{B}$ for current loops in Unit 6.",
        "Sketch $+$ and $-$, draw $\\vec{p}$ from $-$ to $+$, then draw $\\vec{E}$. Torque turns $\\vec{p}$ toward $\\vec{E}$. Net force is zero only if $\\vec{E}$ is uniform.",
        lesson_figure(
            _dipole_svg(),
            "Electric dipole field sketch",
            "Lines leave $+q$ and enter $-q$. On the bisector, $\\vec{E}$ is antiparallel to $\\vec{p}$.",
        )
        + solved(1, "In a uniform field, what is the net force on a dipole? What may still be nonzero?",
                 ["Forces on $\\pm q$ are $qE$ with opposite directions.",
                  "They cancel, so $\\vec{F}_{\\mathrm{net}}=\\vec{0}$.",
                  "Torque $\\tau=pE\\sin\\theta$ can still rotate the dipole."],
                 "net force $0$; torque may be nonzero", "", "Easy")
        + solved(2, "Far from a dipole, how does $|E|$ scale with distance compared with a point charge?",
                 ["A point charge has $E\\propto 1/r^2$.",
                  "A dipole's leading terms cancel.",
                  "The remainder is $E\\propto 1/r^3$."],
                 "$1/r^3$ versus $1/r^2$", "", "Medium")
        + solved(3, "A dipole $\\vec{p}$ sits in uniform $\\vec{E}$ at angle $\\theta=90^\\circ$. Compare $U$ and $\\tau$ with the aligned case $\\theta=0$.",
                 ["$U=-pE\\cos\\theta$, so $U=0$ at $90^\\circ$ and $U=-pE$ at $0^\\circ$.",
                  "$\\tau=pE\\sin\\theta$, so $\\tau$ is maximum at $90^\\circ$ and zero at $0^\\circ$.",
                  "Aligned is stable (minimum $U$, no torque); perpendicular feels the largest twisting torque."],
                 "$U$ higher by $pE$; $\\tau$ is maximum at $90^\\circ$", "", "Hard")
        + _ican(ican4),
        ("Drawing $\\vec{p}$ from $+$ to $-$",
         "The definition is $\\vec{p}$ from negative to positive. Reversing it flips the sign of $U=-\\vec{p}\\cdot\\vec{E}$ and of the torque direction."),
        ("Uniform versus nonuniform",
         "Ask first: is $E$ the same on both charges? If yes, net force is zero. If no, the charge in the stronger field wins."),
        ican4,
        16,
    )

    ican5 = [
        "I can find $\\vec{a}=q\\vec{E}/m$ in a uniform field.",
        "I can compute work $q\\vec{E}\\cdot\\Delta\\vec{\\ell}$ and the change in kinetic energy.",
        "I can say when the trajectory is a straight line versus a parabola in uniform $E$ (no gravity).",
    ]
    c5 = concept_block(
        "5. Motion of a charge in E",
        [
            "The electric force on a charge is $\\vec{F}=q\\vec{E}$. Newton's second law then gives $\\vec{a}=q\\vec{E}/m$. In a uniform field, $\\vec{a}$ is constant.",
            "If velocity is parallel to $\\vec{E}$, the path is a straight line (speeding up if $qE$ is along $\\vec{v}$, slowing if opposite).",
            "If $\\vec{v}$ has a component perpendicular to uniform $\\vec{E}$, the path is a parabola in the plane of $\\vec{v}$ and $\\vec{E}$ — electrostatic analog of constant-acceleration kinematics, not gravity and not circular orbits.",
            "Static electric forces are conservative. Work $W=q\\int\\vec{E}\\cdot d\\vec{\\ell}$ depends only on endpoints. That work equals $-\\Delta U$ and also $\\Delta K$ if electricity is the only force.",
            "Numeric example: $q=2.0\\,\\mu\\mathrm{C}$, $m=4.0\\times10^{-4}\\,\\mathrm{kg}$, $E=200\\,\\mathrm{N/C}$ gives $a=qE/m=1.0\\,\\mathrm{m/s^2}$.",
            "A proton and an electron in the same $\\vec{E}$ feel equal-magnitude opposite forces; the electron's acceleration is thousands of times larger because its mass is tiny.",
        ],
        "Connecting $\\vec{F}=q\\vec{E}$ to $a=F/m$ is how electrostatics talks to mechanics. Potential in Unit 3 is simply this work packaged as a scalar.",
        "Write $F=qE$, then $a=F/m$. Use constant-acceleration formulas only when $E$ is uniform. If $E$ varies, either integrate $a=dv/dt$ or use energy $q\\Delta V=\\Delta K$.",
        lesson_figure(
            _plates_svg(),
            "Uniform field between plates",
            "A positive charge between the plates accelerates toward the negative plate with constant $a=qE/m$.",
        )
        + solved(1, "$q=2.0\\,\\mu\\mathrm{C}$, $m=4.0\\times10^{-4}\\,\\mathrm{kg}$, uniform $E=200\\,\\mathrm{N/C}$. Find $a$.",
                 ["$F=qE=(2.0\\times10^{-6})(200)=4.0\\times10^{-4}\\,\\mathrm{N}$.",
                  "$a=F/m=(4.0\\times10^{-4})/(4.0\\times10^{-4})=1.0\\,\\mathrm{m/s^2}$.",
                  "Direction: same as $\\vec{E}$ because $q>0$."],
                 "$1.0\\,\\mathrm{m/s^2}$ along $\\vec{E}$", "", "Easy")
        + solved(2, "The same charge starts from rest and travels $2.0\\,\\mathrm{cm}$ along $\\vec{E}$. Find $\\Delta K$.",
                 ["Work $W=qEd=(2.0\\times10^{-6})(200)(0.020)=8.0\\times10^{-6}\\,\\mathrm{J}$.",
                  "Starting from rest, $\\Delta K=W$.",
                  "You could also use $v^2=2ad$ with $a=1.0\\,\\mathrm{m/s^2}$ and $K=\\tfrac12 mv^2$ to check."],
                 "$8.0\\times10^{-6}\\,\\mathrm{J}$", "", "Medium")
        + solved(3, "A proton is released from rest in uniform $E$. An electron is released from rest in the same $E$. Compare accelerations and later speeds after the same displacement $d$.",
                 ["$|F|=eE$ for both; directions opposite.",
                  "$a_e/a_p=m_p/m_e\\approx 1836$, electron much larger $a$.",
                  "Energy: $\\Delta K=eEd$ is the same magnitude, so $|v|=\\sqrt{2eEd/m}$ is much larger for the electron."],
                 "$a_e\\gg a_p$ opposite; $|v_e|\\gg|v_p|$ after the same $d$", "Energy is often cleaner than kinematics when masses differ.", "Hard")
        + _ican(ican5),
        ("Mixing gravity projectile formulas into a pure $E$ problem",
         "Unless the problem includes $mg$, do not insert $g$ or range equations. Here the constant acceleration is $qE/m$, possibly horizontal."),
        ("Energy when $E$ is not uniform",
         "If $E$ depends on position, skip $v^2=2ad$. Use $q\\Delta V=\\Delta K$ once potential is defined, or integrate $F\\,dx$ directly."),
        ican5,
        21,
    )

    ican6 = [
        "I can read field-line density as a qualitative $|E|$.",
        "I can state that lines begin on $+$ and end on $-$ and never cross.",
        "I can recognize a uniform-field map of parallel equally spaced lines.",
    ]
    c6 = concept_block(
        "6. Field maps",
        [
            "A field map is a drawing of electric field lines. By agreement, lines leave positive charge and enter negative charge.",
            "Where lines are packed tightly, $|E|$ is larger. Where they spread out, $|E|$ is smaller. Equally spaced parallel lines mean a uniform field.",
            "Lines never cross: two arrows at one point would be two different $\\vec{E}$ vectors.",
            "A closed empty region with more lines entering than leaving contains net negative charge; more leaving than entering means net positive charge. That counting is Gauss's law in cartoon form.",
            "Near a sharp conducting point, lines crowd together: charge density and $|E|$ are large there. Near a flat region they spread.",
            "A negative isolated charge has inward lines. A dipole map shows lines leaving $+$ and landing on $-$, with a characteristic looping shape.",
        ],
        "FRQs often give a field map instead of a formula. You must translate density and direction into force on a charge, flux, and later potential.",
        "Ask three questions of every map: which way would a $+$ move, where is $|E|$ largest, and is there net charge in a circled region (lines in versus out).",
        lesson_figure(
            field_lines_svg(kind="not"),
            "Isolated negative point charge $-q$",
            "Arrowheads on the rays point inward toward $-q$. A positive test charge is pulled in.",
        )
        + solved(1, "Field lines are parallel, equally spaced, and point to the right. Describe $\\vec{E}$.",
                 ["Equal spacing $\\Rightarrow$ constant magnitude.",
                  "Parallel $\\Rightarrow$ constant direction.",
                  "$\\vec{E}$ is uniform, to the right."],
                 "uniform $\\vec{E}$ to the right", "", "Easy")
        + solved(2, "Why must field lines never cross?",
                 ["$\\vec{E}$ has one direction at each point.",
                  "Crossing lines would assign two directions to one point.",
                  "That contradiction is forbidden, so lines may spread or curve but not cross."],
                 "one $\\vec{E}$ per point", "", "Medium")
        + solved(3, "A map shows eight lines leaving a small region and two entering. What can you say about the charge inside?",
                 ["Net lines out $=6$ (qualitative).",
                  "Net outward flux is positive.",
                  "The region contains net positive charge (Gauss, next unit)."],
                 "net positive charge inside", "", "Hard")
        + _ican(ican6),
        ("Thinking lines are trajectories of electrons",
         "Lines show $\\vec{E}$, the force per unit positive charge. Electrons accelerate opposite the lines, and their paths need not follow a line if they have sideways velocity."),
        ("Density, not length",
         "A long line drawn across the page is not a 'stronger' field. Count how many lines pass through a small area, not how long the artist drew them."),
        ican6,
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        ["Coulomb's law", "Superposition of E", "Electric field of distributions",
         "Dipole qualitative", "Motion of a charge in E", "Field maps"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Gauss's Law
# ===========================================================================

def _u2_questions():
    return _pack([
        ("Electric flux through a tiny flat area is $\\vec{E}\\cdot\\widehat{n}\\,\\Delta A$. If $E=4.0\\,\\mathrm{N/C}$ is uniform and perpendicular to $A=2.0\\,\\mathrm{m^2}$, the flux is",
         "$8.0\\,\\mathrm{N\\cdot m^2/C}$",
         "$\\Phi=EA$ when $\\vec{E}$ is normal to the surface.",
         ["$2.0\\,\\mathrm{N\\cdot m^2/C}$", "$0.50\\,\\mathrm{N\\cdot m^2/C}$", "0"]),
        ("If the same $E=4.0\\,\\mathrm{N/C}$ makes a $60^\\circ$ angle with the normal, $\\Phi$ on $A=2.0\\,\\mathrm{m^2}$ is",
         "$4.0\\,\\mathrm{N\\cdot m^2/C}$",
         "$\\Phi=EA\\cos 60^\\circ=8.0\\times 0.50=4.0$.",
         ["$8.0\\,\\mathrm{N\\cdot m^2/C}$", "$6.9\\,\\mathrm{N\\cdot m^2/C}$", "0"]),
        ("Flux through a closed surface is $\\oint\\vec{E}\\cdot d\\vec{A}$. For a uniform field and an empty closed box, that flux is",
         "0",
         "As much flux enters as leaves when no charge is enclosed.",
         ["$EA$", "$4\\pi r^2 E$", "$q/\\varepsilon_0$"]),
        ("The SI unit of electric flux is",
         "$\\mathrm{N\\cdot m^2/C}$",
         "Also equivalent to $\\mathrm{V\\cdot m}$.",
         ["N/C", "C", "T$\\cdot$m²"]),
        ("If $\\vec{E}$ is tangent to a surface everywhere, the flux through that surface is",
         "0",
         "$\\vec{E}\\cdot\\hat{n}=0$ when $\\vec{E}\\perp\\hat{n}$ is false — tangent means $\\vec{E}\\perp\\hat{n}$, so the dot product is zero.",
         ["$EA$", "maximum", "undefined"]),
        ("Gauss's law states that the electric flux out of a closed surface equals",
         "$q_{\\mathrm{enc}}/\\varepsilon_0$",
         "$\\oint\\vec{E}\\cdot d\\vec{A}=q_{\\mathrm{enc}}/\\varepsilon_0$. Charge outside does not appear on the right-hand side.",
         ["$q_{\\mathrm{enc}}$", "$\\varepsilon_0 q_{\\mathrm{enc}}$", "0 always"]),
        ("A closed surface encloses $q=2\\varepsilon_0$ (in SI). The net outward flux is",
         "2",
         "$\\Phi=q/\\varepsilon_0=2$.",
         ["$2\\varepsilon_0$", "0", "$1/2$"]),
        ("A charge $q$ sits outside a closed Gaussian surface. Its contribution to the right-hand side of Gauss's law is",
         "0",
         "Only enclosed charge counts. Its field still exists, but in-and-out flux cancels.",
         ["$q/\\varepsilon_0$", "$-q/\\varepsilon_0$", "$4\\pi kq$"]),
        ("Gauss's law is always true, but it is useful for finding $E$ only when",
         "symmetry makes $|E|$ constant on the surface so $E$ factors out of the integral",
         "Spherical, cylindrical, or planar symmetry are the usual cases.",
         ["the surface is a cube", "charge is moving", "you pick any potato shape"]),
        ("If net flux through a closed surface is zero, then",
         "net enclosed charge is zero",
         "$q_{\\mathrm{enc}}=\\varepsilon_0\\Phi=0$. Field on the surface need not be zero.",
         ["$\\vec{E}=\\vec{0}$ everywhere on the surface", "no charges exist in the universe", "the surface is not closed"]),
        ("A point charge $q$ at the center of a sphere of radius $r$. By symmetry $E$ is radial and constant on the sphere, so $E\\cdot 4\\pi r^2=q/\\varepsilon_0$ and $E=$",
         "$kq/r^2$",
         "$1/(4\\pi\\varepsilon_0)=k$, recovering Coulomb's field.",
         ["$q/(4\\pi r^2)$", "$q/\\varepsilon_0$", "$kqr^2$"]),
        ("Using $k=9.0\\times10^{9}$, a $+2.0\\,\\mathrm{nC}$ point charge produces $|E|$ at $0.10\\,\\mathrm{m}$ of",
         "$1.8\\times10^{3}\\,\\mathrm{N/C}$",
         "$E=(9.0\\times10^9)(2.0\\times10^{-9})/(0.10)^2=1.8\\times10^{3}\\,\\mathrm{N/C}$.",
         ["$1.8\\times10^{5}\\,\\mathrm{N/C}$", "$18\\,\\mathrm{N/C}$", "$9.0\\times10^{3}\\,\\mathrm{N/C}$"]),
        ("A uniformly charged insulating sphere, total $Q$, radius $R$. Outside ($r>R$), $E$ is the same as",
         "a point charge $Q$ at the center",
         "Spherical symmetry plus Gauss: $q_{\\mathrm{enc}}=Q$.",
         ["zero", "$Q$ spread on the surface only", "twice a point charge"]),
        ("Inside a uniformly charged insulating sphere ($\\rho$ constant), $q_{\\mathrm{enc}}=Q(r^3/R^3)$, so $E(r)\\propto$",
         "$r$",
         "$E\\cdot 4\\pi r^2=q_{\\mathrm{enc}}/\\varepsilon_0\\propto r^3\\Rightarrow E\\propto r$.",
         ["$1/r^2$", "$1/r$", "constant"]),
        ("A spherical conducting shell with inner radius $a$, outer $b$, and a charge $q$ at the center. For $a<r<b$ (inside the metal), $E$ is",
         "0",
         "Electrostatic field in the conductor material is zero.",
         ["$kq/r^2$", "$kq/b^2$", "$\\sigma/\\varepsilon_0$"]),
        ("An infinite line charge with linear density $\\lambda$. Cylindrical Gauss gives $E=$",
         "$\\lambda/(2\\pi\\varepsilon_0 r)$",
         "Also written $2k\\lambda/r$. $E$ is radial.",
         ["$\\lambda/(4\\pi\\varepsilon_0 r^2)$", "$\\lambda/\\varepsilon_0$", "$2k\\lambda/r^2$"]),
        ("For $\\lambda=2.0\\times10^{-6}\\,\\mathrm{C/m}$ at $r=0.050\\,\\mathrm{m}$, using $E=2k\\lambda/r$ and $k=9.0\\times10^{9}$, $|E|$ is",
         "$7.2\\times10^{5}\\,\\mathrm{N/C}$",
         "$E=2(9.0\\times10^9)(2.0\\times10^{-6})/0.050=7.2\\times10^{5}\\,\\mathrm{N/C}$.",
         ["$3.6\\times10^{5}\\,\\mathrm{N/C}$", "$1.8\\times10^{5}\\,\\mathrm{N/C}$", "$7.2\\times10^{3}\\,\\mathrm{N/C}$"]),
        ("On a Gaussian cylinder around an infinite line, flux through the two end caps is",
         "0",
         "$\\vec{E}$ is radial, hence parallel to the caps (perpendicular to the cap normal along the axis).",
         ["$E\\pi r^2$", "$2E\\pi r^2$", "$E\\cdot 2\\pi r L$"]),
        ("Flux through the curved wall of that cylinder of radius $r$ and length $L$ is",
         "$E\\cdot 2\\pi r L$",
         "$|E|$ constant, $\\vec{E}\\parallel\\hat{n}$.",
         ["$E\\cdot 4\\pi r^2$", "0", "$E\\cdot \\pi r^2 L$"]),
        ("A coaxial Gaussian cylinder is the right tool because $E$ depends only on",
         "perpendicular distance from the line",
         "Translational and rotational symmetry about the axis.",
         ["$z$ along the line", "the end-cap area", "time"]),
        ("An infinite nonconducting sheet with $\\sigma$ has $E=$",
         "$\\sigma/(2\\varepsilon_0)$",
         "Pillbox: flux $2EA=\\sigma A/\\varepsilon_0$. Independent of distance.",
         ["$\\sigma/\\varepsilon_0$", "$\\sigma/(4\\varepsilon_0)$", "$2\\sigma/\\varepsilon_0$"]),
        ("Just outside the surface of a conductor in electrostatics, $E=$",
         "$\\sigma/\\varepsilon_0$",
         "Pillbox with one face inside the metal ($E=0$) leaves $EA=\\sigma A/\\varepsilon_0$.",
         ["$\\sigma/(2\\varepsilon_0)$", "0", "$2\\sigma/\\varepsilon_0$"]),
        ("$E$ of an infinite sheet does not fall with distance. That is because",
         "as you move away, more of the infinite sheet contributes, compensating $1/r^2$",
         "Gauss plus planar symmetry: no $r$ remains.",
         ["the sheet has no charge", "Gauss fails", "$E$ is actually $1/r^2$"]),
        ("A conducting plate with $\\sigma$ on its surface is not the same as a thin nonconducting sheet of $\\sigma$. Just outside the conductor $E$ is",
         "twice the nonconducting-sheet value for the same $\\sigma$",
         "$\\sigma/\\varepsilon_0$ versus $\\sigma/(2\\varepsilon_0)$.",
         ["half as large", "the same", "zero"]),
        ("Two infinite nonconducting sheets $\\sigma$ and $-\\sigma$. Between them $E$ is",
         "$\\sigma/\\varepsilon_0$",
         "Superpose two contributions $\\sigma/(2\\varepsilon_0)$ in the same direction.",
         ["0", "$\\sigma/(2\\varepsilon_0)$", "$2\\sigma/\\varepsilon_0$"]),
        ("In electrostatics, $\\vec{E}$ inside the material of a conductor is",
         "0",
         "Otherwise free charges would still be accelerating.",
         ["$\\sigma/\\varepsilon_0$", "$\\rho/\\varepsilon_0$", "infinite"]),
        ("Excess charge on an isolated conductor resides",
         "on the outer surface",
         "Gauss inside the metal $\\Rightarrow q_{\\mathrm{enc}}=0$ for any interior Gaussian surface.",
         ["uniformly throughout the volume", "only at the center", "in a cloud above the surface"]),
        ("A conductor has a hollow cavity with no charge inside the cavity. $E$ in the empty cavity (screened from outside charges) is",
         "0",
         "Empty cavity plus electrostatic shielding: $E=0$ in the hole when no cavity charge is present.",
         ["$\\sigma/\\varepsilon_0$", "the same as outside", "infinite"]),
        ("Charge $+q$ in a cavity of a neutral conductor. The inner surface of the cavity acquires",
         "$-q$",
         "Gauss in the metal: $q_{\\mathrm{cavity}}+q_{\\mathrm{inner}}=0$.",
         ["$+q$", "0", "$+2q$"]),
        ("That same neutral conductor then has outer-surface charge",
         "$+q$",
         "Neutrality: inner $-q$ forces outer $+q$.",
         ["$-q$", "0", "$-2q$"]),
        ("Flux through one face of a cube if a charge $q$ sits at the cube's center, by symmetry, is",
         "$q/(6\\varepsilon_0)$",
         "Total flux $q/\\varepsilon_0$ shared equally by 6 faces.",
         ["$q/\\varepsilon_0$", "$q/(4\\varepsilon_0)$", "0"]),
        ("If that charge is moved off-center but still inside, the flux through the whole cube",
         "stays $q/\\varepsilon_0$",
         "Gauss cares only about enclosed charge, not location.",
         ["decreases", "increases", "becomes zero"]),
        ("Off-center inside, flux through one particular face",
         "is no longer $q/(6\\varepsilon_0)$ in general",
         "Faces are no longer equivalent.",
         ["is still $q/(6\\varepsilon_0)$", "is zero", "is $q/\\varepsilon_0$"]),
        ("A Gaussian surface may pass through charge. For a continuous $\\rho$, $q_{\\mathrm{enc}}$ is",
         "$\\int\\rho\\,dV$ over the interior",
         "Only the charge inside the surface.",
         ["the total charge of the universe", "$\\rho$ at one point", "zero if $\\rho$ varies"]),
        ("For $\\rho=\\alpha r$ inside a sphere of radius $R$ ($\\alpha$ constant), $q_{\\mathrm{enc}}$ for $r<R$ is",
         "$\\int_0^r \\alpha r'\\,4\\pi r'^2 dr'=\\pi\\alpha r^4$",
         "$dq=\\rho\\,4\\pi r^2 dr$.",
         ["$\\tfrac43\\pi r^3\\alpha$", "$\\alpha r$", "$4\\pi\\alpha r^2$"]),
        ("Then $E(r)$ for $r<R$ from Gauss is",
         "$\\alpha r^2/(4\\varepsilon_0)$",
         "$E 4\\pi r^2=(\\pi\\alpha r^4)/\\varepsilon_0\\Rightarrow E=\\alpha r^2/(4\\varepsilon_0)$.",
         ["$\\alpha r/(4\\varepsilon_0)$", "$kQ/r^2$", "0"]),
        ("Choosing a cube as a Gaussian surface around a point charge is legal but",
         "does not let you pull $E$ out as a constant",
         "$|E|$ and the angle to $\\hat{n}$ vary over the cube.",
         ["gives $E=q/(6L^2)$ as the field magnitude everywhere", "violates Gauss", "makes flux undefined"]),
        ("Planar symmetry: $E$ can depend only on",
         "the perpendicular distance from the plane",
         "No preferred $x$ or $y$ in the plane.",
         ["the $x$ coordinate in the plane", "time", "the Gaussian length $L$"]),
        ("Cylindrical symmetry: $E$ can depend only on",
         "radial distance from the axis",
         "Not on $\\theta$ or $z$ for an infinite uniform cylinder/line.",
         ["$z$ only", "$\\theta$ only", "both $r$ and $z$ equally"]),
        ("Spherical symmetry: $E$ can depend only on",
         "radial distance from the center",
         "And $\\vec{E}$ is radial.",
         ["$\\theta$ and $\\phi$", "only $z$", "nothing; $E$ is always $0$"]),
        ("A thick infinite slab $-d\\le x\\le d$ with uniform $\\rho$. For $|x|<d$, a pillbox from $0$ to $x$ gives $E(x)\\propto$",
         "$|x|$",
         "$q_{\\mathrm{enc}}=\\rho A x$, $\\Phi=EA$ if $E=0$ on the midplane by symmetry.",
         ["$1/x^2$", "constant", "$1/x$"]),
        ("Outside that slab, $E$ is",
         "constant (like a sheet with $\\sigma_{\\mathrm{eq}}=2\\rho d$)",
         "$E=\\rho d/\\varepsilon_0$ for a nonconducting slab using two-sided flux conventions carefully: $E=\\sigma_{\\mathrm{eq}}/(2\\varepsilon_0)=\\rho d/\\varepsilon_0$.",
         ["$1/x^2$", "0", "infinite"]),
        ("If you include charge outside a Gaussian surface in $q_{\\mathrm{enc}}$, you",
         "violate Gauss's statement",
         "Outside charge affects $\\vec{E}$ locally but not the net flux.",
         ["are required to by superposition", "must double the flux", "must use Ampere instead"]),
        ("Units: $\\varepsilon_0$ is about $8.85\\times10^{-12}$ in",
         "$\\mathrm{C^2/N\\cdot m^2}$",
         "So $q/\\varepsilon_0$ has units of flux.",
         ["N/C", "F", "T"]),
        ("A proton ($+e$) inside a Gaussian sphere. Net flux is $e/\\varepsilon_0$. An electron ($-e$) instead would give flux",
         "$-e/\\varepsilon_0$",
         "Sign of charge is the sign of flux.",
         ["$e/\\varepsilon_0$", "0", "$2e/\\varepsilon_0$"]),
        ("Field lines through an open surface can be nonzero even if $q_{\\mathrm{enc}}=0$ for some related closed surface. Open-surface flux",
         "is not constrained to $q/\\varepsilon_0$",
         "Gauss is for closed surfaces.",
         ["must be zero", "must be $q/\\varepsilon_0$", "is undefined"]),
        ("AP Stretch: $\\rho=\\beta/r$ for $a\\le r\\le b$ (and $0$ elsewhere). $q_{\\mathrm{enc}}$ for a Gaussian sphere with $a<r<b$ equals $q(a)+$",
         "$\\int_a^r (\\beta/r')4\\pi r'^2 dr'=2\\pi\\beta(r^2-a^2)$",
         "$\\rho\\,dV=(\\beta/r)4\\pi r^2 dr=4\\pi\\beta r\\,dr$, integral $2\\pi\\beta(r^2-a^2)$.",
         ["$4\\pi\\beta(r-a)$", "$\\tfrac43\\pi\\beta(r^3-a^3)$", "0"]),
        ("AP Stretch: Infinite cylinder radius $R$, uniform $\\rho$. For $r<R$, $E(r)=$",
         "$\\rho r/(2\\varepsilon_0)$",
         "$E\\cdot 2\\pi r L=(\\rho\\pi r^2 L)/\\varepsilon_0$.",
         ["$\\rho r/(4\\varepsilon_0)$", "$2k\\lambda/r$", "$\\rho R^2/(2\\varepsilon_0 r)$"]),
        ("AP Stretch: Long insulating cylinder, radius $R=0.10\\,\\mathrm{m}$, uniform $\\rho=8.85\\times10^{-6}\\,\\mathrm{C/m^3}$. A Gaussian cylinder outside at $r=0.20\\,\\mathrm{m}$ gives $E=\\rho R^2/(2\\varepsilon_0 r)$. With $\\varepsilon_0=8.85\\times10^{-12}$, $E=$",
         "$2.50\\times10^{4}\\,\\mathrm{N/C}$",
         "$E=(8.85\\times10^{-6})(0.010)/(2\\times 8.85\\times10^{-12}\\times 0.20)=2.50\\times10^{4}\\,\\mathrm{N/C}$.",
         ["$\\rho r/(2\\varepsilon_0)$", "$5.00\\times10^{4}\\,\\mathrm{N/C}$", "0"]),
        ("AP Stretch: Charge $q$ at a cube corner. If the cube were one of 8 cubes making a larger cube centered so $q$ is interior to the large cube, flux through the original small cube is",
         "$q/(8\\varepsilon_0)$",
         "The large cube would have flux $q/\\varepsilon_0$; eight identical octants share it.",
         ["$q/(6\\varepsilon_0)$", "$q/\\varepsilon_0$", "0"]),
        ("AP Stretch: A conducting sphere of radius $R$ carries $Q$. $E$ for $r<R$ (inside the metal) is $0$. $E$ for $r>R$ is $kQ/r^2$. The discontinuity in the normal $E$ at $r=R$ equals",
         "$\\sigma/\\varepsilon_0=Q/(4\\pi R^2\\varepsilon_0)$",
         "Boundary condition $E_{\\mathrm{above}}^\\perp-E_{\\mathrm{below}}^\\perp=\\sigma/\\varepsilon_0$.",
         ["0", "$\\sigma/(2\\varepsilon_0)$", "$kQ/R$"]),
        ("AP Stretch: Volume charge $\\rho=\\rho_0(1-r/R)$ for $r\\le R$. $q_{\\mathrm{enc}}(r)=4\\pi\\rho_0(r^3/3-r^4/(4R))$. Then $E(r)$ for $r<R$ is that quantity over $4\\pi\\varepsilon_0 r^2$, i.e.",
         "$(\\rho_0/\\varepsilon_0)(r/3-r^2/(4R))$",
         "Divide $q_{\\mathrm{enc}}$ by $4\\pi\\varepsilon_0 r^2$.",
         ["$\\rho_0 r/(3\\varepsilon_0)$", "$kQ/r^2$", "0"]),
        ("AP Stretch: Show that $\\oint\\vec{E}\\cdot d\\vec{A}=0$ for a Gaussian surface inside the empty cavity of a conductor with no cavity charge, together with uniqueness, implies $E=0$ in the cavity. The flux being zero is necessary but the stronger result $E=0$ uses",
         "that $V$ is constant on the cavity wall, so $V$ is constant throughout the empty cavity",
         "Uniqueness for Laplace's equation with constant boundary values.",
         ["Ampere's law", "Biot-Savart", "Ohm's law"]),
        ("AP Stretch: A nonuniform infinite slab has $\\rho=\\gamma x$ for $-d<x<d$ (odd in $x$). Midplane $E_x(0)$ is",
         "0",
         "The isolated slab with $\\rho(-x)=-\\rho(x)$ requires $E_x(-x)=-E_x(x)$, so the midplane field vanishes.",
         ["$\\gamma d/\\varepsilon_0$", "$\\gamma d^2/(2\\varepsilon_0)$", "infinite"]),
        ("AP Stretch: Uniform ball $\\rho=6.0\\times10^{-6}\\,\\mathrm{C/m^3}$. Inside at $r=0.10\\,\\mathrm{m}$, Gauss on a sphere gives $E=\\rho r/(3\\varepsilon_0)$. With $\\varepsilon_0=8.85\\times10^{-12}$, $E=$",
         "$2.26\\times10^{4}\\,\\mathrm{N/C}$",
         "$E=(6.0\\times10^{-6})(0.10)/(3\\times 8.85\\times10^{-12})=2.26\\times10^{4}\\,\\mathrm{N/C}$. Enclosed charge is $\\rho$ times the ball of radius $r$, not the whole sample.",
         ["$\\rho R/(3\\varepsilon_0)$", "$kQ/r^2$ using the full ball", "0"]),
    ])


def build_unit2():
    title = "AP Physics C E&M Unit 2: Gauss's Law"
    description = (
        "Electric flux, Gauss's law, and the three standard symmetries — sphere, cylinder, plane — "
        "plus conductors in electrostatics."
    )
    ican1 = [
        "I can compute $\\Phi=\\vec{E}\\cdot\\vec{A}$ for uniform $E$ on a flat patch.",
        "I can explain why net flux through a closed empty box in a uniform field is zero.",
        "I can state that tangent $E$ contributes no flux.",
    ]
    c1 = concept_block(
        "1. Flux",
        [
            "Electric flux measures how much electric field 'flows' through a surface. For a tiny flat patch, $\\Delta\\Phi=\\vec{E}\\cdot\\hat{n}\\,\\Delta A=E\\,\\Delta A\\cos\\theta$, where $\\theta$ is the angle between $\\vec{E}$ and the area normal.",
            "If $\\vec{E}$ is uniform and the surface is flat, $\\Phi=EA\\cos\\theta$. When $\\vec{E}$ is perpendicular to the surface ($\\theta=0$), $\\Phi=EA$. When $\\vec{E}$ is tangent, $\\Phi=0$.",
            "Example: $E=4.0\\,\\mathrm{N/C}$ straight through $A=2.0\\,\\mathrm{m^2}$ gives $\\Phi=8.0\\,\\mathrm{N\\cdot m^2/C}$. At $60^\\circ$ to the normal, $\\Phi=4.0\\,\\mathrm{N\\cdot m^2/C}$.",
            "For a closed surface, $\\hat{n}$ points outward by convention. Flux out counts positive; flux in counts negative.",
            "A uniform field through a closed empty box has equal in and out, so net flux is zero. Charge inside would unbalance that.",
            "Flux is a scalar. You add fluxes through pieces of a surface, but you do not add $\\vec{E}$ magnitudes blindly.",
        ],
        "Gauss's law is a statement about flux, not a new kind of force. If flux is muddy, the whole unit collapses to memorized formulas for $E$.",
        "Always name the normal. Write $\\Phi=EA\\cos\\theta$ with $\\theta$ from $\\vec{E}$ to $\\hat{n}$. For closed surfaces, 'outward' is the only allowed convention on the AP exam.",
        lesson_figure(
            _plates_svg(),
            "Uniform $E$ through an area",
            "If you imagine a rectangular patch between the plates, $\\Phi=EA$ when the patch faces the field.",
        )
        + solved(1, "$E=4.0\\,\\mathrm{N/C}$ uniform, perpendicular to $A=2.0\\,\\mathrm{m^2}$. Find $\\Phi$.",
                 ["$\\theta=0$, so $\\cos\\theta=1$.",
                  "$\\Phi=EA=(4.0)(2.0)=8.0\\,\\mathrm{N\\cdot m^2/C}$.",
                  "Units: field times area."],
                 "$8.0\\,\\mathrm{N\\cdot m^2/C}$", "", "Easy")
        + solved(2, "Same $E$ and $A$, but $\\vec{E}$ makes $60^\\circ$ with the normal. Find $\\Phi$.",
                 ["$\\Phi=EA\\cos 60^\\circ$.",
                  "$\\cos 60^\\circ=1/2$.",
                  "$\\Phi=8.0\\times 1/2=4.0\\,\\mathrm{N\\cdot m^2/C}$."],
                 "$4.0\\,\\mathrm{N\\cdot m^2/C}$", "", "Medium")
        + solved(3, "Why is the net flux of a uniform field through a closed cube zero if the cube is empty?",
                 ["Opposite faces have equal area.",
                  "Field entering one face equals field leaving the opposite face.",
                  "Inward flux is negative, outward positive; they cancel. $q_{\\mathrm{enc}}=0$."],
                 "in = out, net $\\Phi=0$", "", "Hard")
        + _ican(ican1),
        ("Using the angle with the surface instead of with the normal",
         "$\\theta$ in $\\vec{E}\\cdot\\hat{n}$ is from $\\vec{E}$ to the normal, not to the plane. A field 'along the surface' is $\\theta=90^\\circ$, flux zero."),
        ("Write $\\cos\\theta$ from a sketch",
         "Draw $\\hat{n}$ as an arrow sticking out of the area. Measure $\\theta$ from $\\vec{E}$ to that arrow before you reach for a calculator."),
        ican1,
        1,
    )

    ican2 = [
        "I can write $\\oint\\vec{E}\\cdot d\\vec{A}=q_{\\mathrm{enc}}/\\varepsilon_0$.",
        "I can exclude outside charges from $q_{\\mathrm{enc}}$ while still allowing them to affect local $E$.",
        "I can say Gauss is always true but only sometimes useful for finding $E$.",
    ]
    c2 = concept_block(
        "2. Gauss's law statement",
        [
            "Gauss's law: the net electric flux out of any closed surface equals the enclosed charge divided by $\\varepsilon_0$. In symbols, $\\oint\\vec{E}\\cdot d\\vec{A}=q_{\\mathrm{enc}}/\\varepsilon_0$.",
            "The left side is a property of the field on the surface. The right side cares only about charge inside. Charge outside can change $\\vec{E}$ at a point, but its net flux through the closed surface is zero.",
            "If a surface encloses $q=2\\varepsilon_0$, the net outward flux is exactly $2$, regardless of how lopsided the charge is inside.",
            "Gauss's law is always true in electrostatics (and, with Maxwell's correction, even when fields change). It is useful for computing $E$ only when symmetry lets you pull $E$ out of the integral.",
            "The three useful symmetries are spherical (point, ball, spherical shell), cylindrical (infinite line or cylinder), and planar (infinite sheet or slab).",
            "Picking a random potato-shaped surface around a point charge is legal — flux is still $q/\\varepsilon_0$ — but you cannot solve for $E$ because $|E|$ and the angle vary.",
        ],
        "This is one of Maxwell's equations. Every conductor argument and every 'find $E$ of a sphere/line/plane' FRQ is this sentence plus a symmetry story.",
        "Write flux on the left as $E$ times an area only after you have argued that $E$ is constant and parallel to $\\hat{n}$ on that piece. On the right, count only interior charge.",
        lesson_figure(
            gauss_sphere_svg(),
            "Gaussian sphere about a point charge",
            "Symmetry: $E$ is radial and constant on the sphere, so flux is $E\\cdot 4\\pi r^2=q/\\varepsilon_0$.",
        )
        + solved(1, "A closed surface encloses $q=2\\varepsilon_0$. What is the net outward flux?",
                 ["Gauss: $\\Phi=q_{\\mathrm{enc}}/\\varepsilon_0$.",
                  "Substitute $q=2\\varepsilon_0$.",
                  "$\\Phi=2$ (in SI flux units)."],
                 "$2$", "", "Easy")
        + solved(2, "A charge $q$ sits just outside a closed surface. What is its contribution to $q_{\\mathrm{enc}}$? Can it still affect $\\vec{E}$ on the surface?",
                 ["It is not enclosed, so it contributes $0$ to the right-hand side.",
                  "Its Coulomb field still exists at points on the surface.",
                  "The flux it sends in equals the flux it sends out, net zero."],
                 "$0$ on the RHS; yes it affects local $E$", "", "Medium")
        + solved(3, "Why is a cube a poor Gaussian surface for finding $|E|$ of a point charge at the center, even though flux through the cube is $q/\\varepsilon_0$?",
                 ["Total flux is known: $q/\\varepsilon_0$.",
                  "On a cube face, $|E|$ is not constant (corners are farther than face centers).",
                  "The angle between $\\vec{E}$ and $\\hat{n}$ also varies. You cannot factor $E$ out, so you cannot solve for a single $E$."],
                 "flux known, but $E$ not constant on the cube", "", "Hard")
        + _ican(ican2),
        ("Putting outside charges into $q_{\\mathrm{enc}}$",
         "Only interior charge belongs on the right. Outside charge is already included in the actual $\\vec{E}$ on the left; counting it again double-counts."),
        ("Symmetry paragraph before algebra",
         "On the exam, write: '$E$ is radial and depends only on $r$ by spherical symmetry, so on this sphere $E$ is constant and $\\vec{E}\\parallel\\hat{n}$.' Then write $E\\cdot 4\\pi r^2=q_{\\mathrm{enc}}/\\varepsilon_0$."),
        ican2,
        6,
    )

    ican3 = [
        "I can derive $E=kq/r^2$ from Gauss for a point or spherical ball, $r>R$.",
        "I can find $E\\propto r$ inside a uniform insulating sphere.",
        "I can set $E=0$ inside conducting material.",
    ]
    c3 = concept_block(
        "3. Spherical symmetry",
        [
            "Spherical symmetry means the charge distribution looks the same after any rotation about a center. Then $\\vec{E}$ can only be radial, and $|E|$ can depend only on $r$.",
            "The matching Gaussian surface is a sphere of radius $r$ centered on that same point. Then $\\oint\\vec{E}\\cdot d\\vec{A}=E\\cdot 4\\pi r^2$.",
            "A point charge $q$ at the center: $q_{\\mathrm{enc}}=q$, so $E=q/(4\\pi\\varepsilon_0 r^2)=kq/r^2$. Gauss recovers Coulomb's law.",
            "A uniformly charged insulating ball of radius $R$ and total $Q$: outside, $q_{\\mathrm{enc}}=Q$, so $E$ is again $kQ/r^2$. Inside, $q_{\\mathrm{enc}}=Q(r^3/R^3)$, so $E=kQr/R^3$, linear in $r$.",
            "Inside the metal of a conducting sphere or shell, $E=0$. A Gaussian sphere in the metal forces $q_{\\mathrm{enc}}=0$, which is how we know induced charges sit on surfaces.",
            "Walk the choice slowly: (1) Is there a center everyone agrees on? (2) Would rotating the charge distribution change anything? If yes to 1 and no to 2, use a sphere.",
        ],
        "Most AP Gauss FRQs are spheres. The inside-versus-outside split, and the conductor-versus-insulator split, are classic point-earners.",
        "Draw the Gaussian sphere first. Argue $E$ is radial and constant on it. Compute $q_{\\mathrm{enc}}$ as a function of $r$ (volume fraction if uniform $\\rho$). Then $E=q_{\\mathrm{enc}}/(4\\pi\\varepsilon_0 r^2)$.",
        lesson_figure(
            gauss_sphere_svg(),
            "Spherical Gaussian surface",
            "Use this shape only when the charge is spherically symmetric about the same center.",
        )
        + solved(1, "Point charge $+2.0\\,\\mathrm{nC}$. Find $|E|$ at $0.10\\,\\mathrm{m}$. $k=9.0\\times10^{9}$.",
                 ["Spherical Gauss $\\Leftrightarrow$ Coulomb: $E=kq/r^2$.",
                  "$q=2.0\\times10^{-9}\\,\\mathrm{C}$, $r^2=0.010$.",
                  "$E=(9.0\\times10^9)(2.0\\times10^{-9})/0.010=1.8\\times10^{3}\\,\\mathrm{N/C}$."],
                 "$1.8\\times10^{3}\\,\\mathrm{N/C}$", "", "Easy")
        + solved(2, "Uniform insulating sphere, charge $Q$, radius $R$. Find $E$ for $r>R$ and the form of $E$ for $r<R$.",
                 ["Outside: $q_{\\mathrm{enc}}=Q\\Rightarrow E=kQ/r^2$.",
                  "Inside: $q_{\\mathrm{enc}}=Q\\cdot(\\tfrac{4}{3}\\pi r^3)/(\\tfrac{4}{3}\\pi R^3)=Q r^3/R^3$.",
                  "$E=kQr/R^3$, so $E\\propto r$."],
                 "outside $kQ/r^2$; inside $kQr/R^3$", "", "Medium")
        + solved(3, "A conducting spherical shell $a<r<b$ has a point charge $q$ at the center. Find $E$ for $r<a$, $a<r<b$, and $r>b$ if the shell is neutral.",
                 ["$r<a$: like a point, $E=kq/r^2$.",
                  "$a<r<b$: inside metal, $E=0$. Inner surface therefore carries $-q$.",
                  "$r>b$: the shell is neutral so outer surface is $+q$; $E=kq/r^2$ as if all $q$ were at the center."],
                 "$kq/r^2$, then $0$, then $kq/r^2$", "", "Hard")
        + _ican(ican3),
        ("Using $kQ/r^2$ inside a uniform ball",
         "Inside, you have not enclosed all of $Q$. The field is $kQr/R^3$, which is smaller than the exterior formula evaluated at that $r$."),
        ("Name $q_{\\mathrm{enc}}(r)$ in words",
         "Write 'enclosed charge is the charge within radius $r$' and compute it with a volume integral or a fraction of $Q$. Then divide by $4\\pi\\varepsilon_0 r^2$."),
        ican3,
        11,
    )

    ican4 = [
        "I can derive $E=2k\\lambda/r=\\lambda/(2\\pi\\varepsilon_0 r)$ for an infinite line.",
        "I can explain why end-cap flux on a Gaussian cylinder is zero.",
        "I can choose cylinder length $L$ so that $q_{\\mathrm{enc}}=\\lambda L$.",
    ]
    c4 = concept_block(
        "4. Cylindrical symmetry",
        [
            "Cylindrical symmetry means an infinitely long charge distribution looks the same after sliding along its axis or rotating about its axis. Then $\\vec{E}$ is radial (away from the axis) and $|E|$ depends only on the perpendicular distance $r$.",
            "The matching Gaussian surface is a cylinder of radius $r$ and length $L$ coaxial with the line. Split the flux into curved wall plus two end caps.",
            "On the caps, $\\vec{E}$ is parallel to the cap (radial), so $\\vec{E}\\cdot\\hat{n}=0$ and cap flux is zero. On the wall, $\\vec{E}\\parallel\\hat{n}$ and $|E|$ is constant, so $\\Phi=E\\cdot 2\\pi r L$.",
            "For an infinite line, $q_{\\mathrm{enc}}=\\lambda L$. Gauss then says $E\\cdot 2\\pi r L=\\lambda L/\\varepsilon_0$, so $E=\\lambda/(2\\pi\\varepsilon_0 r)=2k\\lambda/r$.",
            "Numeric check: $\\lambda=2.0\\,\\mu\\mathrm{C/m}$, $r=5.0\\,\\mathrm{cm}$, $E=2(9.0\\times10^9)(2.0\\times10^{-6})/0.050=7.2\\times10^{5}\\,\\mathrm{N/C}$.",
            "Walk the choice slowly: if the object is not very long compared with $r$, this infinite-line result is only an approximation. Finite rods go back to Unit 1 integrals.",
        ],
        "Wires, coaxial cables, and later Ampere's law for long wires use the same cylindrical thinking. Learning the Gaussian cylinder now pays off twice.",
        "Draw the axis, then a dashed coaxial cylinder. Argue no $z$ or $\\theta$ dependence. Kill the caps. Keep $L$ in both $\\Phi$ and $q_{\\mathrm{enc}}$ so it cancels.",
        lesson_figure(
            _gauss_cylinder_svg(),
            "Gaussian cylinder around an infinite line",
            "Flux lives on the curved wall. End caps contribute nothing because $\\vec{E}$ is radial.",
        )
        + solved(1, "Why is the flux through the end caps of a coaxial Gaussian cylinder zero for an infinite line?",
                 ["$\\vec{E}$ is perpendicular to the axis (radial).",
                  "Each cap's normal is along the axis.",
                  "Radial field is tangent to the cap, so $\\vec{E}\\cdot\\hat{n}=0$."],
                 "cap flux $=0$", "", "Easy")
        + solved(2, "Derive $E$ for infinite $\\lambda$ using a cylinder of radius $r$ and length $L$.",
                 ["Wall flux $=E\\cdot 2\\pi r L$; cap flux $=0$.",
                  "$q_{\\mathrm{enc}}=\\lambda L$.",
                  "$E\\cdot 2\\pi r L=\\lambda L/\\varepsilon_0\\Rightarrow E=\\lambda/(2\\pi\\varepsilon_0 r)$."],
                 "$E=\\lambda/(2\\pi\\varepsilon_0 r)$", "", "Medium")
        + solved(3, "$\\lambda=2.0\\times10^{-6}\\,\\mathrm{C/m}$, $r=0.050\\,\\mathrm{m}$. Find $E$ using $2k\\lambda/r$ and $k=9.0\\times10^{9}$.",
                 ["$2k\\lambda=2(9.0\\times10^9)(2.0\\times10^{-6})=3.6\\times10^{4}$.",
                  "Divide by $r=0.050$: $E=7.2\\times10^{5}\\,\\mathrm{N/C}$.",
                  "Direction: radially out if $\\lambda>0$."],
                 "$7.2\\times10^{5}\\,\\mathrm{N/C}$", "", "Hard")
        + _ican(ican4),
        ("Using a sphere around a line",
         "A sphere does not match the symmetry: $|E|$ is not constant on a sphere centered on a point of the line, and $\\vec{E}$ is not normal to that sphere. Use a cylinder."),
        ("Let $L$ cancel in front of you",
         "If $L$ disappears from only one side, you dropped a cap or used $2\\pi r$ instead of $2\\pi r L$. Keep $L$ until the last line."),
        ican4,
        16,
    )

    ican5 = [
        "I can derive $E=\\sigma/(2\\varepsilon_0)$ for an infinite nonconducting sheet.",
        "I can derive $E=\\sigma/\\varepsilon_0$ just outside a conductor.",
        "I can superpose two sheets to find $E$ between $\\pm\\sigma$ plates.",
    ]
    c5 = concept_block(
        "5. Planar symmetry",
        [
            "Planar symmetry means an infinite flat sheet (or slab) looks the same after sliding in the plane. Then $\\vec{E}$ is perpendicular to the sheet and $|E|$ depends only on the distance from the plane (and often is actually constant).",
            "The matching Gaussian surface is a pillbox: a short cylinder or rectangular box that sticks out both sides of a nonconducting sheet, or that has one face buried in a conductor.",
            "Nonconducting infinite sheet with $\\sigma$: flux is $2EA$ (two ends), $q_{\\mathrm{enc}}=\\sigma A$, so $E=\\sigma/(2\\varepsilon_0)$, independent of distance.",
            "Conductor: $E=0$ inside the metal, so only the outer face of the pillbox contributes. Then $EA=\\sigma A/\\varepsilon_0$ and $E=\\sigma/\\varepsilon_0$ just outside, perpendicular to the surface.",
            "Two infinite nonconducting sheets $\\sigma$ and $-\\sigma$: between them the two $\\sigma/(2\\varepsilon_0)$ fields add, giving $E=\\sigma/\\varepsilon_0$; outside they cancel.",
            "Walk the choice slowly: if the sheet is finite and you are near an edge, planar symmetry has failed. Then you cannot use this pillbox result.",
        ],
        "Parallel-plate capacitors in Unit 3 are this picture. Mixing $\\sigma/(2\\varepsilon_0)$ with $\\sigma/\\varepsilon_0$ is one of the most common AP point losses.",
        "Ask: is the charge on a conductor or an insulator? Conductor $\\Rightarrow$ one-sided pillbox, $E=\\sigma/\\varepsilon_0$. Thin insulating sheet $\\Rightarrow$ two-sided, $E=\\sigma/(2\\varepsilon_0)$.",
        lesson_figure(
            _gauss_plane_svg(),
            "Gaussian pillbox on an infinite sheet",
            "Two end caps for a nonconducting sheet; bury one cap inside metal for a conductor.",
        )
        + solved(1, "Infinite nonconducting sheet, $\\sigma$. Why two factors of $EA$ in the flux?",
                 ["By symmetry $E$ has the same magnitude on both sides and points away if $\\sigma>0$.",
                  "Each end cap of the pillbox contributes $EA$.",
                  "Side walls have $\\vec{E}\\perp\\hat{n}$ or zero area projection, flux $0$. Total $\\Phi=2EA$."],
                 "$\\Phi=2EA$", "", "Easy")
        + solved(2, "Derive $E$ just outside a conductor with surface charge density $\\sigma$.",
                 ["Put one pillbox face inside the metal, where $E=0$.",
                  "Only the outside face contributes flux $EA$.",
                  "$EA=\\sigma A/\\varepsilon_0\\Rightarrow E=\\sigma/\\varepsilon_0$, normal to the surface."],
                 "$E=\\sigma/\\varepsilon_0$", "", "Medium")
        + solved(3, "Nonconducting sheets $\\sigma$ and $-\\sigma$. Find $E$ between them and outside.",
                 ["Each sheet makes $E=\\sigma/(2\\varepsilon_0)$ perpendicular to itself.",
                  "Between: both arrows point from $+$ to $-$, so they add: $E=\\sigma/\\varepsilon_0$.",
                  "Outside: the arrows oppose, so $E=0$."],
                 "$\\sigma/\\varepsilon_0$ between; $0$ outside", "", "Hard")
        + _ican(ican5),
        ("Using $\\sigma/(2\\varepsilon_0)$ just outside a conductor",
         "That formula is the thin insulating sheet. A conductor screens one side ($E=0$ inside), which doubles the outside field to $\\sigma/\\varepsilon_0$."),
        ("Label each side of the sheet",
         "Sketch arrows on the left and on the right before superposing a second sheet. Most 'between vs outside' errors are missing arrows."),
        ican5,
        21,
    )

    ican6 = [
        "I can state $E=0$ inside conducting material in electrostatics.",
        "I can place excess charge on outer surfaces and induced $-q$ on a cavity wall.",
        "I can use a Gaussian surface in the metal to prove $q_{\\mathrm{enc}}=0$.",
    ]
    c6 = concept_block(
        "6. Conductors in electrostatics",
        [
            "Electrostatics means charges have stopped moving. Inside the material of a conductor, $\\vec{E}$ must then be zero: otherwise free charges would still feel $q\\vec{E}$ and flow.",
            "Put a Gaussian surface entirely inside the metal. Flux is zero because $E=0$, so $q_{\\mathrm{enc}}=0$. Any excess charge therefore lives on surfaces, not in the bulk.",
            "If the conductor is solid, excess charge is on the outer surface. If there is a cavity with charge $q$ inside the hole, the inner wall of the cavity must carry $-q$ so that a Gaussian surface in the metal still encloses zero net charge.",
            "A neutral conductor with cavity charge $+q$ then has $+q$ on its outer surface. The outer field looks like that $+q$ concentrated at the center if the outer shape is a sphere.",
            "Just outside the surface, $E=\\sigma/\\varepsilon_0$ and is perpendicular to the local surface. Charge piles up at sharp points, making large $\\sigma$ and large $E$.",
            "An empty cavity (no charge inside) is screened: $E=0$ in the cavity from outside charges. That is electrostatic shielding.",
        ],
        "Cavities, induced charge, and $E=0$ in metal show up on nearly every AP E&M exam. They are Gauss plus the definition of electrostatic equilibrium.",
        "Always draw a dashed Gaussian surface that stays inside the metal. That one drawing forces $q_{\\mathrm{inner}}=-q_{\\mathrm{cavity}}$ and $E=0$ in the conductor.",
        lesson_figure(
            _conductor_shell_svg(),
            "Gaussian surface inside the conducting material",
            "The dashed sphere stays in the metal, where $E=0$. Flux is zero, so cavity charge plus inner-wall charge is zero.",
        )
        + solved(1, "Why is $E=0$ inside the material of a conductor in electrostatics?",
                 ["Free charges can move.",
                  "A nonzero $E$ would mean a nonzero force $qE$.",
                  "Charges would still be accelerating, contradicting 'electrostatic'."],
                 "$E=0$ in the metal", "", "Easy")
        + solved(2, "A charge $+q$ sits in a cavity of a neutral conductor. Find the induced charges on the inner and outer surfaces.",
                 ["Gaussian surface in the metal: $q_{\\mathrm{enc}}=0$.",
                  "Cavity $+q$ plus inner-surface charge $=0\\Rightarrow$ inner $=-q$.",
                  "Neutral overall $\\Rightarrow$ outer $=+q$."],
                 "inner $-q$, outer $+q$", "", "Medium")
        + solved(3, "That conductor is a spherical shell, inner $a$, outer $b$. Find $E$ for $r<a$ (in the cavity, off-center charge $q$), for $a<r<b$, and for $r>b$.",
                 ["Inside the metal $a<r<b$: $E=0$.",
                  "Outside $r>b$: spherically symmetric induced outer charge $+q$, so $E=kq/r^2$ as if $q$ were at the center.",
                  "In the cavity, $E$ is not $kq/r^2$ about the center if $q$ is off-center; it is the ordinary Coulomb field of $q$ plus the field of the nonuniform inner-surface charge. (If the question assumes $q$ at the center, $E=kq/r^2$ for $r<a$.)"],
                 "cavity: Coulomb of $q$ plus inner-wall field; metal $0$; outside $kq/r^2$",
                 "If $q$ is centered, cavity field is simply $kq/r^2$.", "Hard")
        + _ican(ican6),
        ("Claiming $E=0$ in an empty region just because a conductor is nearby",
         "$E=0$ in the metal. An empty cavity with a charge inside has a field. An empty cavity with no charge is screened from the outside."),
        ("Gaussian surface in the metal, every time",
         "That drawing is the entire argument. If you cannot show a surface with $E=0$ on it, you cannot conclude $q_{\\mathrm{enc}}=0$."),
        ican6,
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        ["Flux", "Gauss's law statement", "Spherical symmetry",
         "Cylindrical symmetry", "Planar symmetry", "Conductors in electrostatics"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Electric Potential and Capacitors
# ===========================================================================

def _u3_questions():
    return _pack([
        ("Electric potential difference $V_b-V_a$ is defined as minus the line integral of $\\vec{E}$ from $a$ to $b$. In a uniform field, moving a distance $d$ along $\\vec{E}$ changes $V$ by",
         "$-Ed$",
         "$\\Delta V=-\\int E\\,dx=-Ed$ when displacement is along $\\vec{E}$.",
         ["$+Ed$", "$E/d$", "0"]),
        ("If $E=200\\,\\mathrm{N/C}$ uniform and you move $0.050\\,\\mathrm{m}$ along $\\vec{E}$, $|\\Delta V|$ is",
         "10 V",
         "$|\\Delta V|=Ed=10\\,\\mathrm{V}$. Potential drops in the direction of $\\vec{E}$.",
         ["4.0 V", "4000 V", "0.25 V"]),
        ("$\\vec{E}$ points from higher potential toward",
         "lower potential",
         "$\\vec{E}=-\\nabla V$.",
         ["higher potential", "equipotentials only", "magnetic north"]),
        ("The SI unit volt equals",
         "J/C",
         "$V=U/q$, joules per coulomb.",
         ["N/C", "C/J", "T$\\cdot$m"]),
        ("In electrostatics $\\oint\\vec{E}\\cdot d\\vec{\\ell}=0$, which guarantees that $V$ is",
         "path-independent (a well-defined scalar)",
         "Conservative field.",
         ["path-dependent", "always zero", "equal to $E$"]),
        ("Potential of a point charge, taking $V(\\infty)=0$, is $V=kq/r$. For $+2.0\\,\\mathrm{nC}$ at $0.10\\,\\mathrm{m}$ with $k=9.0\\times10^{9}$, $V$ is",
         "180 V",
         "$V=(9.0\\times10^9)(2.0\\times10^{-9})/0.10=180\\,\\mathrm{V}$.",
         ["18 V", "$1.8\\times10^{3}\\,\\mathrm{V}$", "9.0 V"]),
        ("Two point charges $+q$ and $+q$ a distance $a$ apart. At the midpoint, $V$ is",
         "$4kq/a$",
         "Each contributes $kq/(a/2)=2kq/a$; scalars add: $4kq/a$.",
         ["0", "$2kq/a$", "$kq/a^2$"]),
        ("At that same midpoint, $\\vec{E}$ for two equal like charges is",
         "0",
         "Vectors cancel; scalars $V$ do not.",
         ["$4kq/a^2$", "infinite", "$2kq/a^2$"]),
        ("Potential is a scalar superposition: you",
         "add the $kq/r$ values with signs",
         "No components. Negative charges contribute negative $V$ if $V(\\infty)=0$.",
         ["add only magnitudes of $E$", "cross the potentials", "multiply $V$ values"]),
        ("A proton ($+e$) moved from $V=0$ to $V=100\\,\\mathrm{V}$ by an external agent slowly (no $\\Delta K$) requires work about",
         "$1.6\\times10^{-17}\\,\\mathrm{J}$",
         "$W_{\\mathrm{ext}}=q\\Delta V=e(100)$.",
         ["$100\\,\\mathrm{J}$", "$1.6\\times10^{-19}\\,\\mathrm{J}$", "0"]),
        ("Equipotential surfaces are surfaces of constant $V$. Field lines are",
         "perpendicular to equipotentials",
         "$\\vec{E}=-\\nabla V$ has no component along an equipotential.",
         ["parallel to equipotentials", "the same as equipotentials", "never near equipotentials"]),
        ("Moving a charge along an equipotential, work by the electrostatic force is",
         "0",
         "$\\vec{E}\\perp d\\vec{\\ell}$ so $\\vec{E}\\cdot d\\vec{\\ell}=0$.",
         ["$qEd$", "maximum", "negative always"]),
        ("Near a positive point charge, equipotentials are",
         "concentric spheres",
         "$V=kq/r$ is constant on spheres.",
         ["planes", "cylinders about a random axis", "hyperbolas only"]),
        ("Between parallel plates of a capacitor, equipotentials are",
         "planes parallel to the plates",
         "Uniform $E$ $\\Rightarrow$ $V$ changes linearly with the coordinate along $\\vec{E}$.",
         ["spheres", "the field lines themselves", "random curves"]),
        ("Where equipotentials crowd together, $|E|$ is",
         "larger",
         "$|E|=|\\Delta V|/\\Delta s$ for nearby surfaces.",
         ["smaller", "zero", "undefined"]),
        ("Capacitance is $C=Q/V$ for a pair of conductors. SI unit is the farad, equal to",
         "C/V",
         "Coulombs per volt.",
         ["V/C", "J", "N/C"]),
        ("Parallel-plate capacitor: $C=\\varepsilon_0 A/d$. If $A$ doubles and $d$ halves, $C$ is multiplied by",
         "4",
         "Proportional to $A/d$.",
         ["2", "1/2", "1"]),
        ("A capacitor has $C=2.0\\,\\mu\\mathrm{F}$ and $V=12\\,\\mathrm{V}$. The charge on each plate (magnitude) is",
         "$24\\,\\mu\\mathrm{C}$",
         "$Q=CV=(2.0\\times10^{-6})(12)=2.4\\times10^{-5}\\,\\mathrm{C}=24\\,\\mu\\mathrm{C}$.",
         ["$6.0\\,\\mu\\mathrm{C}$", "$12\\,\\mu\\mathrm{C}$", "$2.0\\,\\mu\\mathrm{C}$"]),
        ("Two capacitors $C$ and $C$ in series have equivalent capacitance",
         "$C/2$",
         "$1/C_{\\mathrm{eq}}=1/C+1/C=2/C$.",
         ["$2C$", "$C$", "0"]),
        ("Those same two in parallel have equivalent capacitance",
         "$2C$",
         "$C_{\\mathrm{eq}}=C+C$.",
         ["$C/2$", "$C$", "$C^2$"]),
        ("A dielectric with constant $\\kappa>1$ inserted while the battery remains connected",
         "increases $C$ and increases $Q$",
         "$C\\to\\kappa C$, $V$ fixed, so $Q=CV$ rises.",
         ["decreases $C$", "leaves $Q$ unchanged and drops $V$ only", "makes $C=0$"]),
        ("The same dielectric inserted after the battery is disconnected (isolated $Q$)",
         "increases $C$ and decreases $V$",
         "$Q$ fixed, $V=Q/C$ falls, $U=Q^2/(2C)$ falls.",
         ["increases $V$", "decreases $C$", "leaves $U$ unchanged"]),
        ("Dielectrics reduce $E$ inside the capacitor for fixed $Q$ because",
         "polarization produces an opposing field",
         "Bound surface charge $\\sigma_b$ weakens the net $E$.",
         ["they add free charge", "they are conductors with $E=0$", "Gauss fails"]),
        ("With dielectric filling the gap, $C=\\kappa\\varepsilon_0 A/d$. For $\\kappa=4$, $C$ is",
         "4 times the vacuum value",
         "Linear in $\\kappa$.",
         ["1/4 as large", "unchanged", "16 times"]),
        ("If a dielectric is pulled out at constant $V$, the battery",
         "takes charge back ( $Q$ drops )",
         "$C$ drops, $V$ fixed $\\Rightarrow$ $Q$ drops.",
         ["pushes more charge on ($Q$ rises)", "does nothing", "reverses polarity"]),
        ("Energy stored in a capacitor is $U=\\tfrac12 CV^2$. For $C=2.0\\,\\mu\\mathrm{F}$ and $V=10\\,\\mathrm{V}$, $U$ is",
         "$1.0\\times10^{-4}\\,\\mathrm{J}$",
         "$\\tfrac12(2.0\\times10^{-6})(100)=1.0\\times10^{-4}\\,\\mathrm{J}$.",
         ["$2.0\\times10^{-5}\\,\\mathrm{J}$", "$1.0\\times10^{-6}\\,\\mathrm{J}$", "$0.10\\,\\mathrm{J}$"]),
        ("Equivalent expressions: $U=\\tfrac12 CV^2=$",
         "$Q^2/(2C)=\\tfrac12 QV$",
         "All three are used on FRQs; pick the variables you know.",
         ["$QV$", "$C/V$", "$Q/C^2$"]),
        ("The energy density in an electric field in vacuum is",
         "$\\tfrac12\\varepsilon_0 E^2$",
         "Integrating this between plates recovers $\\tfrac12 CV^2$.",
         ["$\\varepsilon_0 E$", "$E^2/\\varepsilon_0$", "$\\sigma E$"]),
        ("If $V$ is held fixed and $C$ doubles, stored energy",
         "doubles",
         "$U\\propto C$ at fixed $V$.",
         ["halves", "quadruples", "unchanged"]),
        ("If $Q$ is held fixed and $C$ doubles, stored energy",
         "halves",
         "$U\\propto 1/C$ at fixed $Q$.",
         ["doubles", "quadruples", "unchanged"]),
        ("$\\Delta V=-\\int_a^b\\vec{E}\\cdot d\\vec{\\ell}$. For $\\vec{E}=-(200\\,\\mathrm{N/C})\\,\\hat{x}$ from $x=0$ to $x=0.10\\,\\mathrm{m}$, $V(0.10)-V(0)$ is",
         "$+20\\,\\mathrm{V}$",
         "$-\\int_0^{0.10}(-200)dx=+20\\,\\mathrm{V}$.",
         ["$-20\\,\\mathrm{V}$", "0", "$2000\\,\\mathrm{V}$"]),
        ("A spherical conductor of radius $R$ carrying $Q$ has $V_{\\mathrm{surface}}=kQ/R$ (with $V(\\infty)=0$). Inside the conductor $V$ is",
         "$kQ/R$ (constant)",
         "$E=0$ inside $\\Rightarrow$ $V$ does not change with $r$.",
         ["0", "$kQ/r$", "infinite"]),
        ("Capacitors $2\\,\\mu\\mathrm{F}$ and $6\\,\\mu\\mathrm{F}$ in series: $C_{\\mathrm{eq}}=$",
         "$1.5\\,\\mu\\mathrm{F}$",
         "$1/C=1/2+1/6=2/3$, so $C=3/2\\,\\mu\\mathrm{F}$.",
         ["$8\\,\\mu\\mathrm{F}$", "$4\\,\\mu\\mathrm{F}$", "$3\\,\\mu\\mathrm{F}$"]),
        ("Those capacitors in parallel: $C_{\\mathrm{eq}}=$",
         "$8\\,\\mu\\mathrm{F}$",
         "Add: $2+6=8$.",
         ["$1.5\\,\\mu\\mathrm{F}$", "$4\\,\\mu\\mathrm{F}$", "$12\\,\\mu\\mathrm{F}$"]),
        ("In series, the charges on the two capacitors are",
         "equal in magnitude",
         "The inner plates form an isolated pair.",
         ["proportional to $C$", "inversely to $C$", "zero"]),
        ("In parallel, the voltages on the two capacitors are",
         "equal",
         "They share the same two nodes.",
         ["inversely to $C$", "proportional to $C$", "zero"]),
        ("Work to charge a capacitor by moving $dq$ at instantaneous $v=q/C$ is $\\int_0^Q (q/C)\\,dq=$",
         "$Q^2/(2C)$",
         "That is $U$.",
         ["$Q^2/C$", "$CQ^2$", "0"]),
        ("If $d$ of a parallel-plate capacitor is doubled at fixed $Q$, $E$ between plates",
         "stays the same ( $E=\\sigma/\\varepsilon_0$ )",
         "For vacuum plates $E$ depends on $\\sigma=Q/A$, not on $d$, until fringing.",
         ["doubles", "halves", "becomes zero"]),
        ("At that same fixed $Q$, doubling $d$ makes $U$",
         "double",
         "$C$ halves, $U=Q^2/(2C)$ doubles. You do work pulling plates apart.",
         ["halve", "stay the same", "go to zero"]),
        ("$1\\,\\mathrm{V/m}$ of electric field equals",
         "$1\\,\\mathrm{N/C}$",
         "Same SI unit.",
         ["1 J", "1 T", "1 F"]),
        ("A $12\\,\\mathrm{V}$ battery connected to $4.0\\,\\mu\\mathrm{F}$ stores energy",
         "$2.88\\times10^{-4}\\,\\mathrm{J}$",
         "$U=\\tfrac12 CV^2=\\tfrac12(4\\times10^{-6})(144)=2.88\\times10^{-4}\\,\\mathrm{J}$.",
         ["$4.8\\times10^{-5}\\,\\mathrm{J}$", "$48\\,\\mathrm{J}$", "$1.44\\times10^{-5}\\,\\mathrm{J}$"]),
        ("Connecting two identical charged capacitors in parallel (isolated) shares charge. Final $U$ compared with initial $2\\times(\\tfrac12 CV^2)$ if they had equal $V$ already is",
         "unchanged (already equal $V$)",
         "If both already at same $V$, connecting changes nothing.",
         ["halves", "doubles", "goes to zero"]),
        ("If one is charged to $V$ and the other is uncharged, then paralleled, final $U$ is",
         "half of the original $U$ on the charged one",
         "Charge shares, $V\\to V/2$ on $2C$, $U_f=\\tfrac12(2C)(V/2)^2=CV^2/4=U_i/2$.",
         ["the same", "double", "zero"]),
        ("Potential of a spherical shell $Q$, $R$, for $r>R$ is $kQ/r$. Continuity at $r=R$ matches the constant interior value $kQ/R$. That continuity is required because",
         "a jump in $V$ would mean infinite $E=-dV/dr$",
         "$V$ is continuous if $E$ is finite.",
         ["$V$ is always zero", "Gauss forbids continuity", "$Q$ is zero"]),
        ("Along a field line, $V$",
         "decreases",
         "Positive charges 'fall' downhill in $V$.",
         ["increases", "is constant", "oscillates"]),
        ("A $5.0\\,\\mu\\mathrm{F}$ capacitor charged to $20\\,\\mathrm{V}$ is connected to an uncharged $15\\,\\mu\\mathrm{F}$. Shared $V$ is",
         "5.0 V",
         "$Q=100\\,\\mu\\mathrm{C}$ conserved on $20\\,\\mu\\mathrm{F}$ total, $V=5.0\\,\\mathrm{V}$.",
         ["20 V", "15 V", "10 V"]),
        ("AP Stretch: $E_r=c/r^2$ for $r>0$ (pointlike). $V(r)-V(\\infty)=\\int_r^\\infty E\\,dr=$",
         "$c/r$",
         "$-\\int_\\infty^r (-c/r^2)dr$ with $E$ outward if $c>0$: $V=c/r$.",
         ["$c/r^2$", "$c\\ln r$", "0"]),
        ("AP Stretch: Finite rod $\\lambda$ from $x=0$ to $L$. Potential at $x=-d$ ($V(\\infty)=0$) is $k\\lambda\\ln$ of",
         "$(d+L)/d$",
         "$V=k\\int_0^L dx/(d+x)=k\\lambda\\ln((d+L)/d)$.",
         ["$d/(d+L)$", "$L/d$", "$dL$"]),
        ("AP Stretch: Uniform sphere $Q,R$. $V$ at the center (vs $V(\\infty)=0$) is",
         "$\\tfrac32 kQ/R$",
         "Outside integral $kQ/R$ plus inside $\\int_0^R E(r)\\,dr$ with $E=kQr/R^3$ adds $\\tfrac12 kQ/R$.",
         ["$kQ/R$", "$2kQ/R$", "0"]),
        ("AP Stretch: $C=\\varepsilon_0 A/d$. Energy $U=\\tfrac12\\varepsilon_0 E^2\\cdot(Ad)$ with $E=V/d$ equals",
         "$\\tfrac12 CV^2$",
         "Volume times energy density matches the circuit formula.",
         ["$CV^2$", "$Q^2 C$", "0"]),
        ("AP Stretch: Dielectric $\\kappa$ fills half the gap as a slab parallel to the plates (two capacitors in series). $C_{\\mathrm{eq}}$ is",
         "$\\bigl(1/C_1+1/C_2\\bigr)^{-1}$ with $C_1=\\kappa\\varepsilon_0 A/(d/2)$ and $C_2=\\varepsilon_0 A/(d/2)$",
         "Series of vacuum and dielectric capacitors.",
         ["$\\kappa\\varepsilon_0 A/d$", "$(\\kappa+1)\\varepsilon_0 A/d$", "$\\varepsilon_0 A/d$"]),
        ("AP Stretch: The same dielectric fills half the area (side by side). Then the pieces are in",
         "parallel: $C=(\\varepsilon_0 A/2)/d+(\\kappa\\varepsilon_0 A/2)/d$",
         "Same $V$, add $C$.",
         ["series", "neither", "shorted"]),
        ("AP Stretch: $V(x,y)=ax^2-ay^2$ (saddle). $E_x=-\\partial V/\\partial x=$",
         "$-2ax$",
         "$\\vec{E}=-\\nabla V$.",
         ["$2ax$", "$a$", "0"]),
        ("AP Stretch: Uniform sphere $Q=8.0\\,\\mathrm{nC}$, $R=0.10\\,\\mathrm{m}$. Gauss gives $E=kQr/R^3$ for $r<R$. Then $V_{\\mathrm{center}}-V_{\\mathrm{surface}}=\\int_0^R E\\,dr$ equals",
         "$360\\,\\mathrm{V}$",
         "$\\int_0^R kQr/R^3\\,dr=kQ/(2R)=(9.0\\times10^{9})(8.0\\times10^{-9})/0.20=360\\,\\mathrm{V}$.",
         ["$720\\,\\mathrm{V}$", "$180\\,\\mathrm{V}$", "0"]),
        ("AP Stretch: Capacitor $C=8.0\\,\\mu\\mathrm{F}$ at $V=15\\,\\mathrm{V}$. Energy $\\tfrac12 CV^2$ and $Q^2/(2C)$ with $Q=CV$ both equal",
         "$9.00\\times10^{-4}\\,\\mathrm{J}$",
         "$Q=120\\,\\mu\\mathrm{C}$. $\\tfrac12(8.0\\times10^{-6})(225)=9.00\\times10^{-4}\\,\\mathrm{J}$, and $(120\\times10^{-6})^2/(2\\times 8.0\\times10^{-6})$ matches.",
         ["$1.80\\times10^{-3}\\,\\mathrm{J}$", "$1.20\\times10^{-4}\\,\\mathrm{J}$", "0"]),
    ])


def build_unit3():
    title = "AP Physics C E&M Unit 3: Electric Potential and Capacitors"
    description = (
        "Potential from $\\vec{E}$, point-charge $V$, equipotentials, capacitance, dielectrics, "
        "and energy stored in capacitors."
    )
    ican1 = [
        "I can use $\\Delta V=-\\int\\vec{E}\\cdot d\\vec{\\ell}$ and $\\Delta V=-Ed$ in a uniform field.",
        "I can say $\\vec{E}$ points toward decreasing $V$.",
        "I can convert N/C to V/m.",
    ]
    c1 = concept_block(
        "1. Potential from E",
        [
            "Electric potential $V$ is a scalar field whose differences tell you the work per unit charge. By definition $V_b-V_a=-\\int_a^b\\vec{E}\\cdot d\\vec{\\ell}$.",
            "In a uniform field, if you move a distance $d$ in the direction of $\\vec{E}$, the potential drops by $Ed$. Example: $E=200\\,\\mathrm{N/C}$ over $5.0\\,\\mathrm{cm}$ gives $|\\Delta V|=10\\,\\mathrm{V}$.",
            "The SI unit is the volt: $1\\,\\mathrm{V}=1\\,\\mathrm{J/C}$. Also $1\\,\\mathrm{N/C}=1\\,\\mathrm{V/m}$.",
            "Because electrostatic $\\vec{E}$ is conservative, the line integral is path-independent. That is why a single number $V$ at each point makes sense once you choose a reference (often $V(\\infty)=0$).",
            "Differentially, $\\vec{E}=-\\nabla V$. Field lines point 'downhill' on a potential map, perpendicular to the level curves.",
            "Do not confuse $V$ with $\\vec{E}$. A point can have high potential and small field (inside a charged conductor: $V$ constant, $E=0$).",
        ],
        "Capacitors are labeled in volts. Circuits are labeled in volts. You cannot do Unit 4 or 5 without a clean $\\Delta V=-\\int E\\,d\\ell$.",
        "Pick a path that is easy: along $\\vec{E}$ or perpendicular to $\\vec{E}$. Perpendicular means $dV=0$. Parallel means $|dV|=E\\,ds$.",
        lesson_figure(
            _plates_svg(),
            "Uniform $E$ between plates",
            "Potential falls steadily from the positive plate to the negative plate: $V=Ed$ across the gap.",
        )
        + solved(1, "Uniform $E=200\\,\\mathrm{N/C}$. Move $0.050\\,\\mathrm{m}$ along $\\vec{E}$. Find $|\\Delta V|$ and whether $V$ rose or fell.",
                 ["$|\\Delta V|=Ed=(200)(0.050)=10\\,\\mathrm{V}$.",
                  "Displacement is along $\\vec{E}$.",
                  "$V$ decreases by $10\\,\\mathrm{V}$."],
                 "drops by $10\\,\\mathrm{V}$", "", "Easy")
        + solved(2, "$\\vec{E}=-(200\\,\\mathrm{N/C})\\hat{x}$. Find $V(0.10)-V(0)$.",
                 ["$V(b)-V(a)=-\\int_a^b E_x\\,dx$.",
                  "$E_x=-200$, so $-\\int_0^{0.10}(-200)\\,dx=+20\\,\\mathrm{V}$.",
                  "Potential is higher at $x=0.10\\,\\mathrm{m}$."],
                 "$+20\\,\\mathrm{V}$", "", "Medium")
        + solved(3, "Inside a conductor in equilibrium, $E=0$. What does that imply for $V$ throughout the conductor, including a cavity wall?",
                 ["$dV=-\\vec{E}\\cdot d\\vec{\\ell}=0$ along any path in the metal.",
                  "So $V$ is the same at every point of the conductor.",
                  "The entire conductor, inner and outer surfaces, is one equipotential."],
                 "$V$ constant on the whole conductor", "", "Hard")
        + _ican(ican1),
        ("Thinking high $V$ means large $E$",
         "A charged metal sphere has constant $V$ and zero $E$ inside. $E$ is the slope of $V$, not $V$ itself."),
        ("Sign of the integral",
         "Write $V_b-V_a=-\\int_a^b\\vec{E}\\cdot d\\vec{\\ell}$ with limits from start to finish. Flipping the minus sign is the classic error."),
        ican1,
        1,
    )

    ican2 = [
        "I can use $V=kq/r$ with $V(\\infty)=0$ and add scalars for several charges.",
        "I can contrast $V\\neq 0$ with $E=0$ at the midpoint of two like charges.",
        "I can compute $q\\Delta V$ as change in electric potential energy.",
    ]
    c2 = concept_block(
        "2. Potential of point charges",
        [
            "A single point charge, with the reference $V(\\infty)=0$, has $V=kq/r$. Positive charges make positive $V$; negative charges make negative $V$.",
            "Example: $+2.0\\,\\mathrm{nC}$ at $0.10\\,\\mathrm{m}$ gives $V=(9.0\\times10^9)(2.0\\times10^{-9})/0.10=180\\,\\mathrm{V}$.",
            "Superposition for potential is scalar: add the $kq/r$ terms with signs. No components.",
            "Two equal like charges: at the midpoint $E=0$ (vectors cancel) but $V=4kq/a\\neq 0$ (scalars add). That contrast is an AP favorite.",
            "Potential energy of a charge $q_0$ in a preexisting $V$ is $U=q_0 V$ (with the same reference). Moving $q_0$ through $\\Delta V$ changes $U$ by $q_0\\Delta V$.",
            "To assemble a collection of point charges from infinity, add pair terms $kq_i q_j/r_{ij}$. Each pair is counted once.",
        ],
        "You will need $V=kq/r$ for conductors (the surface value $kQ/R$) and for energy of charge collections. Mixing up $E$ cancellation with $V$ cancellation costs easy points.",
        "Write a number for each source's $V$, including minus signs, then add. Only after that ask about $\\vec{E}$ with a separate vector sketch.",
        lesson_figure(
            _equipotential_svg(),
            "Point-charge potential",
            "Spheres of constant $V=kq/r$. Closer spheres mean larger $|E|$.",
        )
        + solved(1, "$+2.0\\,\\mathrm{nC}$ point charge. $V$ at $0.10\\,\\mathrm{m}$ with $V(\\infty)=0$, $k=9.0\\times10^{9}$.",
                 ["$V=kq/r$.",
                  "$(9.0\\times10^9)(2.0\\times10^{-9})=18$.",
                  "Divide by $0.10$: $V=180\\,\\mathrm{V}$."],
                 "$180\\,\\mathrm{V}$", "", "Easy")
        + solved(2, "Two charges $+q$ a distance $a$ apart. Compare $V$ and $E$ at the midpoint.",
                 ["Each $V=kq/(a/2)=2kq/a$, so $V_{\\mathrm{net}}=4kq/a$.",
                  "Each $E=kq/(a/2)^2=4kq/a^2$, opposite directions.",
                  "$E_{\\mathrm{net}}=0$ while $V\\neq 0$."],
                 "$V=4kq/a$, $\\vec{E}=\\vec{0}$", "", "Medium")
        + solved(3, "Work to assemble three $+q$ at the vertices of an equilateral triangle of side $a$, from infinite separation.",
                 ["Three unique pairs.",
                  "Each pair contributes $kq^2/a$.",
                  "$U=3kq^2/a$."],
                 "$3kq^2/a$", "", "Hard")
        + _ican(ican2),
        ("Concluding $V=0$ because $E=0$",
         "Midpoint of like charges: $E$ cancels, $V$ adds. Midpoint of opposite charges: $V$ can cancel while $E$ does not."),
        ("One table of $kq/r$",
         "List every source, its distance, its signed $V$, then add. It is harder to drop a minus sign when the table is on the page."),
        ican2,
        6,
    )

    ican3 = [
        "I can sketch equipotentials as perpendicular to field lines.",
        "I can state that work along an equipotential is zero.",
        "I can use crowding of equipotentials as a cue for large $|E|$.",
    ]
    c3 = concept_block(
        "3. Equipotentials",
        [
            "An equipotential is a surface (or a curve in a 2-D map) on which $V$ is constant. No work is done by the electrostatic force when a charge slides on that surface, because $\\vec{E}\\perp d\\vec{\\ell}$.",
            "Field lines always cross equipotentials at right angles, pointing toward falling $V$.",
            "Around a point charge, equipotentials are concentric spheres. Between parallel plates, they are planes parallel to the plates, equally spaced if $E$ is uniform.",
            "Where equipotential lines on a map crowd together, $V$ changes in a short distance, so $|E|=|\\Delta V|/\\Delta s$ is large.",
            "A conductor in equilibrium is an equipotential volume, not just a surface: $E=0$ inside the metal so $V$ cannot vary.",
            "You may choose any convenient reference. Only differences $\\Delta V$ are measurable; adding a constant to all $V$ values does not change $\\vec{E}$ or any work.",
        ],
        "FRQ field maps ask you to draw dashed equipotentials. Capacitor plates are equipotentials. Kirchhoff's loop rule is a tour of potential that must close.",
        "Draw field lines first (or use the given ones). Then cut them at right angles with dashed curves. Label higher $V$ toward the positive charges.",
        lesson_figure(
            _equipotential_svg(),
            "Equipotentials (dashed) and $E$ (solid)",
            "Circles of constant $V$ around $+q$. The radial field is perpendicular to every circle.",
        )
        + solved(1, "Why is work by $\\vec{E}$ zero along an equipotential?",
                 ["On an equipotential, $dV=0$.",
                  "$dV=-\\vec{E}\\cdot d\\vec{\\ell}$.",
                  "So $\\vec{E}\\cdot d\\vec{\\ell}=0$: either $E=0$ or $d\\vec{\\ell}\\perp\\vec{E}$."],
                 "work $=0$", "", "Easy")
        + solved(2, "Sketch the equipotentials of an isolated positive point charge.",
                 ["$V=kq/r$ depends only on $r$.",
                  "Constant $V$ $\\Rightarrow$ constant $r$.",
                  "Spheres centered on the charge (circles in a plane cut)."],
                 "concentric spheres", "", "Medium")
        + solved(3, "On a map, two equipotentials $20\\,\\mathrm{V}$ and $10\\,\\mathrm{V}$ are $2.0\\,\\mathrm{cm}$ apart and roughly parallel. Estimate $|E|$.",
                 ["$|E|\\approx|\\Delta V|/\\Delta s$.",
                  "$|\\Delta V|=10\\,\\mathrm{V}$, $\\Delta s=0.020\\,\\mathrm{m}$.",
                  "$|E|\\approx 500\\,\\mathrm{V/m}$."],
                 "$\\approx 5.0\\times10^{2}\\,\\mathrm{V/m}$", "", "Hard")
        + _ican(ican3),
        ("Drawing equipotentials parallel to field lines",
         "They must be perpendicular. Parallel would mean a component of $\\vec{E}$ along the surface and a changing $V$."),
        ("Crowding = steep slope",
         "Treat the map like a topographic map: tight contours mean a steep hill, which is a large $|E|$."),
        ican3,
        11,
    )

    ican4 = [
        "I can use $C=Q/V$ and $C=\\varepsilon_0 A/d$ for parallel plates.",
        "I can combine series ($1/C$ add) and parallel ($C$ add).",
        "I can compute $Q=CV$ from a battery voltage.",
    ]
    c4 = concept_block(
        "4. Capacitance",
        [
            "A capacitor is two conductors separated by an insulator. Capacitance $C=Q/V$ where $Q$ is the magnitude of the separated charge and $V$ is the potential difference.",
            "The farad is $1\\,\\mathrm{F}=1\\,\\mathrm{C/V}$. Practical capacitors are $\\mu\\mathrm{F}$ or $\\mathrm{pF}$.",
            "Parallel plates: $E=\\sigma/\\varepsilon_0=Q/(A\\varepsilon_0)$ (conductor plates), $V=Ed=Qd/(A\\varepsilon_0)$, so $C=\\varepsilon_0 A/d$. Larger area or smaller gap means larger $C$.",
            "Example: $C=2.0\\,\\mu\\mathrm{F}$ on $12\\,\\mathrm{V}$ holds $Q=CV=24\\,\\mu\\mathrm{C}$.",
            "Series: the same $Q$ sits on each, voltages add, $1/C_{\\mathrm{eq}}=1/C_1+1/C_2$. Two equal $C$s in series make $C/2$. Parallel: same $V$, charges add, $C_{\\mathrm{eq}}=C_1+C_2$.",
            "$C$ is a geometry-and-dielectric property. Connecting a battery does not change $C$; it changes $Q$ and $V$ together so that $Q=CV$.",
        ],
        "RC circuits in Unit 5 need $C$ as a number in $\\tau=RC$. Energy and dielectrics are this same $C$.",
        "Decide series vs parallel by asking whether the capacitors share the same two nodes (parallel) or form a single path (series). Then use $Q=CV$ on the equivalent.",
        lesson_figure(
            _plates_svg(),
            "Parallel-plate capacitor",
            "$C=\\varepsilon_0 A/d$. Uniform $E$ in the gap, $V=Ed$.",
        )
        + solved(1, "$C=2.0\\,\\mu\\mathrm{F}$, $V=12\\,\\mathrm{V}$. Find $|Q|$ on each plate.",
                 ["$Q=CV$.",
                  "$(2.0\\times10^{-6})(12)=2.4\\times10^{-5}\\,\\mathrm{C}$.",
                  "That is $24\\,\\mu\\mathrm{C}$."],
                 "$24\\,\\mu\\mathrm{C}$", "", "Easy")
        + solved(2, "Two capacitors each of $C$ in series. $C_{\\mathrm{eq}}$?",
                 ["$1/C_{\\mathrm{eq}}=1/C+1/C=2/C$.",
                  "$C_{\\mathrm{eq}}=C/2$.",
                  "Charge on each is the same; voltages add."],
                 "$C/2$", "", "Medium")
        + solved(3, "$C=\\varepsilon_0 A/d$. $A$ doubles, $d$ halves. Factor by which $C$ changes. Then if $V$ is held fixed, factor for $Q$.",
                 ["$C\\propto A/d$ becomes $2A/(d/2)=4$ times larger.",
                  "$Q=CV$ with $V$ fixed also $\\times 4$.",
                  "$E=V/d$ doubles because $d$ halved."],
                 "$C\\times 4$, $Q\\times 4$", "", "Hard")
        + _ican(ican4),
        ("Adding series capacitances like resistors in series",
         "Resistors in series add. Capacitors in series add as reciprocals. The formulas swap when you go parallel."),
        ("Geometry first",
         "Write $C=\\varepsilon_0 A/d$ (or $\\kappa\\varepsilon_0 A/d$) before using $Q=CV$. $C$ does not depend on how much charge is presently on the plates."),
        ican4,
        16,
    )

    ican5 = [
        "I can state that a dielectric multiplies $C$ by $\\kappa$.",
        "I can distinguish battery-connected (fixed $V$) from isolated (fixed $Q$).",
        "I can explain the opposing polarization field.",
    ]
    c5 = concept_block(
        "5. Dielectrics",
        [
            "A dielectric is an insulating material. Its molecules polarize in $\\vec{E}$, producing a field that opposes the applied field and reduces the net $E$ for a given free charge $Q$.",
            "The dielectric constant $\\kappa$ (or $K$) is greater than $1$. Filling the gap multiplies capacitance: $C=\\kappa\\varepsilon_0 A/d$.",
            "If the battery stays connected, $V$ is fixed. Then $C$ up $\\Rightarrow$ $Q=CV$ up. The battery supplies extra charge.",
            "If the capacitor is isolated, $Q$ is fixed. Then $C$ up $\\Rightarrow$ $V=Q/C$ down, and stored energy $U=Q^2/(2C)$ down.",
            "Example: $\\kappa=4$ fills the gap. $C$ becomes four times the vacuum value. At fixed $V$, energy $U=\\tfrac12 CV^2$ also $\\times 4$.",
            "Partial fillings become series or parallel combinations: a slab parallel to the plates (stacked in the gap) is series; a slab covering half the area is parallel.",
        ],
        "Dielectric FRQs are decision trees: is $Q$ or $V$ held fixed? That one branch determines whether $U$ rises or falls.",
        "Write a tiny table with columns $C$, $Q$, $V$, $U$ before and after insertion. Circle which of $Q$ or $V$ is constrained by the problem.",
        lesson_figure(
            energy_bars_svg(ke=0, pe=4, thermal=0),
            "Stored energy as a bar (PE of the capacitor)",
            "Inserting a dielectric at fixed $Q$ lowers this stored energy; at fixed $V$ the battery may raise it.",
        )
        + solved(1, "Vacuum capacitor, then $\\kappa=4$ fills the gap. What happens to $C$?",
                 ["$C=\\kappa\\varepsilon_0 A/d$.",
                  "$\\kappa=4$.",
                  "$C$ becomes $4$ times larger."],
                 "$C\\to 4C$", "", "Easy")
        + solved(2, "Battery remains connected during insertion. What happens to $Q$ and to $U=\\tfrac12 CV^2$?",
                 ["$V$ fixed by the battery.",
                  "$Q=CV$ increases by $\\kappa$.",
                  "$U\\propto C$ at fixed $V$ also increases by $\\kappa$."],
                 "$Q$ and $U$ both $\\times\\kappa$", "", "Medium")
        + solved(3, "Battery disconnected, then dielectric inserted. Compare $E$, $V$, and $U$.",
                 ["$Q$ fixed, $C\\times\\kappa$.",
                  "$V=Q/C$ drops by $\\kappa$; $E=V/d$ drops by $\\kappa$.",
                  "$U=Q^2/(2C)$ drops by $\\kappa$. The 'lost' energy can go into pulling the dielectric in."],
                 "$E$, $V$, $U$ all $\\div\\kappa$", "", "Hard")
        + _ican(ican5),
        ("Using the fixed-$V$ story on an isolated capacitor",
         "Disconnected means $Q$ cannot change (no path). Connected means $V$ cannot change (battery). Pick one and stick to it."),
        ("Three-row table",
         "Rows: before, constraint, after. Columns: $C,Q,V,U$. Fill the constraint first, then the others from $Q=CV$ and $U=\\tfrac12 CV^2$."),
        ican5,
        21,
    )

    ican6 = [
        "I can compute $U=\\tfrac12 CV^2=Q^2/(2C)=\\tfrac12 QV$.",
        "I can use energy density $\\tfrac12\\varepsilon_0 E^2$.",
        "I can predict how $U$ changes when $C$ changes at fixed $Q$ versus fixed $V$.",
    ]
    c6 = concept_block(
        "6. Energy stored in a capacitor",
        [
            "Charging a capacitor means an external agent (or a battery) pushes charge $dq$ through an increasing potential $v=q/C$. The work is $U=\\int_0^Q (q/C)\\,dq=Q^2/(2C)$.",
            "Equivalent forms: $U=\\tfrac12 CV^2=\\tfrac12 QV=Q^2/(2C)$. Use whichever variables are given.",
            "Example: $C=2.0\\,\\mu\\mathrm{F}$, $V=10\\,\\mathrm{V}$, $U=\\tfrac12(2.0\\times10^{-6})(100)=1.0\\times10^{-4}\\,\\mathrm{J}$.",
            "The same energy can be viewed as stored in the field: energy density $u=\\tfrac12\\varepsilon_0 E^2$ in vacuum. Integrating $u$ over the gap volume $Ad$ recovers $\\tfrac12 CV^2$.",
            "At fixed $V$, larger $C$ stores more energy. At fixed $Q$, larger $C$ stores less energy (the charge sits at a lower voltage).",
            "When two capacitors share charge, total $Q$ is conserved but $U$ often drops: the 'missing' energy can appear as heat, spark, or EM radiation unless the process is quasistatic with no resistance.",
        ],
        "Energy tracking is how you justify why a dielectric is sucked into a gap, why separating plates at fixed $Q$ takes work, and later how LC circuits trade $U_E$ with $U_B$.",
        "Choose the $U$ formula that uses the two quantities you know. If the process holds $Q$ fixed, $Q^2/(2C)$ makes the $C$ dependence obvious.",
        lesson_figure(
            energy_bars_svg(ke=0, pe=3, thermal=1),
            "Energy accounting",
            "Capacitor PE can fall while thermal energy in a resistor rises when charge is shared through $R$.",
        )
        + solved(1, "$C=2.0\\,\\mu\\mathrm{F}$, $V=10\\,\\mathrm{V}$. Find $U$.",
                 ["$U=\\tfrac12 CV^2$.",
                  "$V^2=100$.",
                  "$U=\\tfrac12(2.0\\times10^{-6})(100)=1.0\\times10^{-4}\\,\\mathrm{J}$."],
                 "$1.0\\times10^{-4}\\,\\mathrm{J}$", "", "Easy")
        + solved(2, "Isolated capacitor, $Q$ fixed, $d$ doubled. What happens to $C$, $V$, $U$?",
                 ["$C=\\varepsilon_0 A/d$ halves.",
                  "$V=Q/C$ doubles; $E=\\sigma/\\varepsilon_0$ unchanged (vacuum plates).",
                  "$U=Q^2/(2C)$ doubles: you do work pulling the plates apart."],
                 "$C\\div 2$, $V\\times 2$, $U\\times 2$", "", "Medium")
        + solved(3, "A charged $C$ at voltage $V$ is connected to an identical uncharged $C$. Find the final energy as a fraction of the initial energy.",
                 ["Initial $U_i=\\tfrac12 CV^2$, charge $Q=CV$.",
                  "Charge shares: each $C$ has $Q/2$, common $V_f=V/2$, or one equivalent $2C$ at $V/2$.",
                  "$U_f=\\tfrac12(2C)(V/2)^2=CV^2/4=U_i/2$."],
                 "$U_f=U_i/2$", "The other half typically dissipates in resistance.", "Hard")
        + _ican(ican6),
        ("Using $\\tfrac12 CV^2$ when $Q$ is the conserved quantity and $V$ changed",
         "If $V$ is not the same before and after, either compute the new $V$ first or switch to $Q^2/(2C)$."),
        ("Match the constraint to the formula",
         "Fixed $V\\to U=\\tfrac12 CV^2$. Fixed $Q\\to U=Q^2/(2C)$. Circle the constraint on the problem statement."),
        ican6,
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        ["Potential from E", "Potential of point charges", "Equipotentials",
         "Capacitance", "Dielectrics", "Energy stored in a capacitor"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: DC Circuits
# ===========================================================================

def _u4_questions():
    return _pack([
        ("Current $I$ is the charge per unit time passing a cross-section. If $12\\,\\mathrm{C}$ pass in $4.0\\,\\mathrm{s}$, $I$ is",
         "3.0 A",
         "$I=\\Delta Q/\\Delta t=12/4=3.0\\,\\mathrm{A}$.",
         ["48 A", "0.33 A", "8.0 A"]),
        ("Drift speed $v_d$ relates to current by $I=nqAv_d$. If $n$, $q$, $A$ are fixed and $I$ doubles, $v_d$",
         "doubles",
         "Linear in $I$.",
         ["halves", "quadruples", "is unchanged"]),
        ("In a metal, the charge carriers are electrons, so the conventional current (positive flow) is",
         "opposite the electron drift",
         "Conventional $I$ is the direction positive charge would move.",
         ["the same as electron drift", "zero", "perpendicular to the wire"]),
        ("Steady DC current in a single loop is",
         "the same at every cross-section of the loop",
         "Charge is not piling up (junction rule with one path).",
         ["largest near the battery", "zero in the wires", "proportional to local $A$ only, even if $I$ is defined as total"]),
        ("If $I=2.0\\,\\mathrm{A}$ for $5.0\\,\\mathrm{s}$, the charge that flows is",
         "10 C",
         "$Q=It$.",
         ["0.40 C", "2.5 C", "7.0 C"]),
        ("Ohm's law for a resistor: $V=IR$. If $R=4.0\\,\\Omega$ and $I=3.0\\,\\mathrm{A}$, $V$ is",
         "12 V",
         "$(3)(4)=12$.",
         ["7.0 V", "1.3 V", "0.75 V"]),
        ("Resistivity $\\rho$ appears in $R=\\rho L/A$. Doubling length and doubling area leaves $R$",
         "unchanged",
         "$L/A$ unchanged.",
         ["doubled", "halved", "quadrupled"]),
        ("A wire's radius doubles (length fixed). $R$ is multiplied by",
         "1/4",
         "$A\\propto r^2$, so $R\\propto 1/A$.",
         ["1/2", "2", "4"]),
        ("SI unit of resistivity is",
         "$\\Omega\\cdot\\mathrm{m}$",
         "$R$ in ohms, $L/A$ in $1/\\mathrm{m}$.",
         ["$\\Omega$", "$\\Omega/\\mathrm{m}$", "S"]),
        ("A material that does not obey $V\\propto I$ (nonlinear $I$–$V$ curve) is called",
         "nonohmic",
         "Ohmic means linear through the origin on a $V$–$I$ graph.",
         ["superconducting only", "always a dielectric", "impossible"]),
        ("Kirchhoff's junction rule is charge conservation: at a node, $\\sum I_{\\mathrm{in}}=$",
         "$\\sum I_{\\mathrm{out}}$",
         "Or $\\sum I=0$ with a sign convention.",
         ["0 always for each $I$", "$\\varepsilon/R$", "infinite"]),
        ("Kirchhoff's loop rule is energy conservation: around a closed loop, $\\sum\\Delta V=$",
         "0",
         "You return to the same potential.",
         ["$\\varepsilon$", "$IR$", "$q/C$"]),
        ("Traversing a resistor in the direction of conventional current, the potential",
         "drops by $IR$",
         "Like going downstream.",
         ["rises by $IR$", "is unchanged", "drops by $I/R$"]),
        ("Traversing an ideal battery from $-$ to $+$ (inside the battery), the potential",
         "rises by $\\varepsilon$",
         "The emf pumps charge uphill.",
         ["drops by $\\varepsilon$", "drops by $Ir$", "is unchanged"]),
        ("A single-loop circuit has $\\varepsilon=12\\,\\mathrm{V}$ and $R=4.0\\,\\Omega$. The current is",
         "3.0 A",
         "Loop: $\\varepsilon-IR=0\\Rightarrow I=3.0\\,\\mathrm{A}$.",
         ["48 A", "8.0 A", "0.33 A"]),
        ("Two resistors $2.0\\,\\Omega$ and $4.0\\,\\Omega$ in series have $R_{\\mathrm{eq}}=$",
         "$6.0\\,\\Omega$",
         "Series: add.",
         ["$1.33\\,\\Omega$", "$8.0\\,\\Omega$", "$2.0\\,\\Omega$"]),
        ("Those same two in parallel have $R_{\\mathrm{eq}}=$",
         "$\\dfrac{4}{3}\\,\\Omega$",
         "$1/R=1/2+1/4=3/4$, so $R=4/3\\,\\Omega$.",
         ["$6.0\\,\\Omega$", "$8.0\\,\\Omega$", "$1.0\\,\\Omega$"]),
        ("Identical resistors $R$ in parallel: $n$ of them make $R_{\\mathrm{eq}}=$",
         "$R/n$",
         "Each extra path lowers equivalent resistance.",
         ["$nR$", "$R$", "$n^2 R$"]),
        ("A $12\\,\\mathrm{V}$ battery drives a series pair $2.0\\,\\Omega$ and $4.0\\,\\Omega$. The current is",
         "2.0 A",
         "$R_{\\mathrm{eq}}=6.0\\,\\Omega$, $I=12/6=2.0\\,\\mathrm{A}$.",
         ["6.0 A", "3.0 A", "1.0 A"]),
        ("In that series pair, the voltage across the $4.0\\,\\Omega$ is",
         "8.0 V",
         "$V=IR=(2.0)(4.0)=8.0\\,\\mathrm{V}$.",
         ["4.0 V", "12 V", "2.0 V"]),
        ("Power in a resistor is $P=IV=I^2 R=V^2/R$. For $I=2.0\\,\\mathrm{A}$ through $4.0\\,\\Omega$, $P$ is",
         "16 W",
         "$I^2 R=4\\times 4=16\\,\\mathrm{W}$.",
         ["8.0 W", "2.0 W", "32 W"]),
        ("At fixed voltage, if $R$ doubles, power in that resistor",
         "halves",
         "$P=V^2/R$.",
         ["doubles", "quadruples", "is unchanged"]),
        ("At fixed current, if $R$ doubles, power",
         "doubles",
         "$P=I^2 R$.",
         ["halves", "is unchanged", "quadruples"]),
        ("A $12\\,\\mathrm{V}$ battery with a $6.0\\,\\Omega$ resistor (only) dissipates",
         "24 W",
         "$P=V^2/R=144/6=24\\,\\mathrm{W}$.",
         ["2.0 W", "72 W", "12 W"]),
        ("The battery supplies power $\\varepsilon I$. In a simple loop that equals the",
         "sum of $I^2 R$ in the resistors (plus $I^2 r$ if internal $r$)",
         "Energy conservation.",
         ["net charge created", "flux", "capacitance"]),
        ("An ideal ammeter has resistance",
         "0",
         "It is inserted in series and must not add $IR$ drop.",
         ["infinite", "$1\\,\\Omega$", "equal to the load"]),
        ("An ideal voltmeter has resistance",
         "infinite",
         "It is placed in parallel and must draw no current.",
         ["0", "$1\\,\\Omega$", "equal to the load"]),
        ("Placing an ammeter in parallel with a resistor typically",
         "short-circuits that branch (dangerous, huge current)",
         "Near-zero $R$ in parallel steals the current.",
         ["measures voltage correctly", "does nothing", "measures $C$"]),
        ("Placing a voltmeter in series with a resistor typically",
         "kills the current (almost open circuit)",
         "Huge series $R$.",
         ["measures current correctly", "shorts the battery", "charges a capacitor"]),
        ("A real voltmeter of $10\\,\\mathrm{k}\\Omega$ across a $10\\,\\mathrm{k}\\Omega$ resistor loads the circuit: the parallel combination is",
         "$5.0\\,\\mathrm{k}\\Omega$",
         "Two equal $R$ in parallel: $R/2$.",
         ["$20\\,\\mathrm{k}\\Omega$", "$10\\,\\mathrm{k}\\Omega$", "0"]),
        ("$I=nqAv_d$. If $A$ doubles at fixed $I$, drift speed",
         "halves",
         "Same charge per second through a larger door needs slower drift.",
         ["doubles", "unchanged", "quadruples"]),
        ("A $3.0\\,\\mathrm{m}$ wire, $A=2.0\\times10^{-6}\\,\\mathrm{m^2}$, $\\rho=1.5\\times10^{-6}\\,\\Omega\\cdot\\mathrm{m}$. $R=$",
         "$2.25\\,\\Omega$",
         "$R=\\rho L/A=(1.5\\times10^{-6})(3.0)/(2.0\\times10^{-6})=2.25\\,\\Omega$.",
         ["$0.75\\,\\Omega$", "$9.0\\,\\Omega$", "$1.5\\,\\Omega$"]),
        ("Internal resistance $r$: terminal voltage is $\\varepsilon-Ir$. For $\\varepsilon=12\\,\\mathrm{V}$, $r=1.0\\,\\Omega$, $I=2.0\\,\\mathrm{A}$, $V_{\\mathrm{term}}=$",
         "10 V",
         "$12-2=10$.",
         ["12 V", "14 V", "2.0 V"]),
        ("Two-loop circuit: left loop $\\varepsilon_1=6\\,\\mathrm{V}$, $R_1=2\\,\\Omega$; a shared $R_3=2\\,\\Omega$; right $\\varepsilon_2=6\\,\\mathrm{V}$, $R_2=2\\,\\Omega$ symmetric. Current in the shared resistor is",
         "0",
         "Equal batteries oppose through the bridge in this balanced case.",
         ["3.0 A", "6.0 A", "1.5 A"]),
        ("Series: current is the same; voltages",
         "add to the battery (and split proportional to $R$)",
         "$V_i=IR_i$.",
         ["are equal", "add as reciprocals", "are zero"]),
        ("Parallel: voltage is the same; currents",
         "add and split inversely to $R$",
         "$I_i=V/R_i$.",
         ["are equal", "add as reciprocals of $I$", "are zero"]),
        ("Three $6.0\\,\\Omega$ resistors: two in parallel, that combo in series with the third. $R_{\\mathrm{eq}}=$",
         "$9.0\\,\\Omega$",
         "Parallel of two $6\\,\\Omega$ is $3\\,\\Omega$, plus $6\\,\\Omega$ is $9\\,\\Omega$.",
         ["$2.0\\,\\Omega$", "$18\\,\\Omega$", "$4.0\\,\\Omega$"]),
        ("Brightness of identical bulbs (ohmic) tracks",
         "power $I^2 R$ or $V^2/R$",
         "More power, brighter.",
         ["only current, ignoring $R$", "only voltage, ignoring that $P=V^2/R$", "charge $Q$ on a capacitor they do not have"]),
        ("A $100\\,\\mathrm{W}$ bulb on $120\\,\\mathrm{V}$ has resistance about",
         "$144\\,\\Omega$",
         "$R=V^2/P=14400/100=144\\,\\Omega$.",
         ["$1.2\\,\\Omega$", "$12000\\,\\Omega$", "$0.83\\,\\Omega$"]),
        ("Shorting a resistor (ideal wire across it) makes its $V$",
         "0",
         "The wire forces $\\Delta V=0$ across that element.",
         ["equal to $\\varepsilon$", "infinite", "unchanged"]),
        ("Opening a switch in a branch makes that branch current",
         "0",
         "Open circuit: $R\\to\\infty$.",
         ["infinite", "equal to $\\varepsilon/r$", "unchanged"]),
        ("Maximum power from a real battery to a load $R$ occurs when $R=$",
         "the internal $r$",
         "Impedance matching: $P=I^2 R$ with $I=\\varepsilon/(R+r)$ peaks at $R=r$.",
         ["0", "infinite", "$2r$ always? peak is $R=r$"]),
        ("Junction: $I_1$ in, $I_2$ and $I_3$ out. If $I_1=5.0\\,\\mathrm{A}$ and $I_2=2.0\\,\\mathrm{A}$, then $I_3=$",
         "3.0 A",
         "$5=2+I_3$.",
         ["7.0 A", "2.5 A", "10 A"]),
        ("Loop with $\\varepsilon=9.0\\,\\mathrm{V}$, $r=1.0\\,\\Omega$, $R=8.0\\,\\Omega$. Current is",
         "1.0 A",
         "$I=9/(1+8)=1.0\\,\\mathrm{A}$.",
         ["9.0 A", "1.1 A", "8.0 A"]),
        ("Power dissipated in that $r$ is",
         "1.0 W",
         "$I^2 r=1.0\\,\\mathrm{W}$.",
         ["8.0 W", "9.0 W", "0"]),
        ("Power delivered by the emf is $\\varepsilon I=$",
         "9.0 W",
         "$9\\times 1=9$, of which $8\\,\\mathrm{W}$ is in $R$ and $1\\,\\mathrm{W}$ in $r$.",
         ["1.0 W", "8.0 W", "0"]),
        ("AP Stretch: Current density $J=I/A=\\sigma E$ with $\\sigma=1/\\rho$. If $E=0.040\\,\\mathrm{N/C}$ and $\\rho=1.7\\times10^{-8}\\,\\Omega\\cdot\\mathrm{m}$, $J=$",
         "$2.4\\times10^{6}\\,\\mathrm{A/m^2}$",
         "$J=E/\\rho=0.040/(1.7\\times10^{-8})\\approx 2.35\\times10^{6}$.",
         ["$6.8\\times10^{-10}\\,\\mathrm{A/m^2}$", "$0.040\\,\\mathrm{A/m^2}$", "$1.7\\times10^{-8}\\,\\mathrm{A/m^2}$"]),
        ("AP Stretch: A copper wire carries $I=3.0\\,\\mathrm{A}$ with cross section $A=1.5\\times10^{-6}\\,\\mathrm{m^2}$. Current density is $J=I/A$. If resistivity $\\rho=1.7\\times10^{-8}\\,\\Omega\\cdot\\mathrm{m}$, the field in the wire is $E=\\rho J=$",
         "$0.034\\,\\mathrm{N/C}$",
         "$J=2.0\\times10^{6}\\,\\mathrm{A/m^2}$, so $E=(1.7\\times10^{-8})(2.0\\times10^{6})=0.034\\,\\mathrm{N/C}$.",
         ["$5.1\\times10^{-14}\\,\\mathrm{N/C}$", "$3.0\\,\\mathrm{N/C}$", "$1.7\\times10^{-8}\\,\\mathrm{N/C}$"]),
        ("AP Stretch: Two-loop: $\\varepsilon_1=6\\,\\mathrm{V}$, $R_1=1\\,\\Omega$ on the left; $\\varepsilon_2=12\\,\\mathrm{V}$, $R_2=2\\,\\Omega$ on the right; shared $R_3=2\\,\\Omega$ in the middle. With clockwise $I_1$ left and $I_2$ right, the junction on top has $I_3=I_1-I_2$ down the middle. A correct loop equation for the left loop is",
         "$6-I_1(1)-(I_1-I_2)(2)=0$",
         "Battery up, drops on $R_1$ and on shared $R_3$ with current $I_1-I_2$.",
         ["$6+I_1+2I_2=0$", "$12=I_2$", "$I_1=I_2$"]),
        ("AP Stretch: Resistivity of a truncated cone from $r_1$ to $r_2$ over length $L$ is found by $dR=\\rho\\,dx/(\\pi[r(x)]^2)$. If $r$ varies linearly, $R=$",
         "$\\rho L/(\\pi r_1 r_2)$",
         "Standard integral result.",
         ["$\\rho L/(\\pi r_1^2)$", "$\\rho L/(\\pi r_2^2)$", "$\\rho(r_1+r_2)/L$"]),
        ("AP Stretch: A network of five $R$'s as a Wheatstone bridge is balanced when $R_1/R_2=R_3/R_4$. Then the bridge current is",
         "0",
         "Equal potential on both midpoints.",
         ["$\\varepsilon/R$", "infinite", "$\\varepsilon/(5R)$"]),
        ("AP Stretch: Battery $\\varepsilon=24\\,\\mathrm{V}$, internal $r=2.0\\,\\Omega$, load $R=10\\,\\Omega$. Current is $I=\\varepsilon/(r+R)=2.0\\,\\mathrm{A}$. Power dissipated in the load is $I^2 R=$",
         "$40\\,\\mathrm{W}$",
         "$I^2 R=(2.0)^2(10)=40\\,\\mathrm{W}$. The emf supplies $\\varepsilon I=48\\,\\mathrm{W}$; the extra $8.0\\,\\mathrm{W}$ is heat in $r$.",
         ["$48\\,\\mathrm{W}$", "$24\\,\\mathrm{W}$", "$4.8\\,\\mathrm{W}$"]),
        ("AP Stretch: Combining $I=nqAv_d$ with $J=\\sigma E$ gives $v_d=(\\sigma/nq)E$. For electrons, $\\sigma/nq$ is the",
         "mobility $\\mu$ in $v_d=\\mu E$",
         "Definition of mobility.",
         ["resistivity", "emf", "flux"]),
        ("AP Stretch: In a single-loop RC-free DC circuit, the electric field in the wire is maintained by",
         "surface charges on the conductors",
         "Kirchhoff plus electrostatics: tiny surface charge gradients steer $E$ around corners.",
         ["magnetic flux", "a nonzero $\\rho$ filling the copper bulk", "displacement current only"]),
        ("AP Stretch: Nodal analysis: two resistors $R$ from a node at $V$ to ground, and a current source $I$ into the node. Then $V=$",
         "$IR/2$",
         "KCL: $I=V/R+V/R$.",
         ["$IR$", "$2IR$", "0"]),
    ])


def build_unit4():
    title = "AP Physics C E&M Unit 4: DC Circuits"
    description = (
        "Current and drift, Ohm's law and resistivity, Kirchhoff's rules, series and parallel, "
        "power, and ideal voltmeters and ammeters."
    )
    ican1 = [
        "I can compute $I=\\Delta Q/\\Delta t$ and $Q=It$.",
        "I can use $I=nqAv_d$ and interpret conventional current.",
        "I can state that steady current is the same around a single loop.",
    ]
    c1 = concept_block(
        "1. Current and drift",
        [
            "Electric current $I$ is the amount of charge passing a cross-section per unit time: $I=dQ/dt$. The SI unit is the ampere, $1\\,\\mathrm{A}=1\\,\\mathrm{C/s}$.",
            "If $12\\,\\mathrm{C}$ pass in $4.0\\,\\mathrm{s}$, $I=3.0\\,\\mathrm{A}$. In a time $t$, $Q=It$ flows.",
            "In a wire, enormous numbers of charges creep slowly. The microscopic relation is $I=nqAv_d$, where $n$ is number density, $q$ is carrier charge, $A$ is cross-sectional area, and $v_d$ is drift speed.",
            "Drift speeds are millimeters per second or less; the signal that starts the drift travels much faster. Doubling $I$ at fixed $A$ doubles $v_d$.",
            "Electrons in metals drift opposite the conventional current. Conventional current is the direction positive charge would flow, from the battery's $+$ toward $-$ in the external circuit.",
            "In steady DC, charge does not pile up: the current into a segment equals the current out. That is the junction rule for a single path.",
        ],
        "Every circuit quantity — $V=IR$, power, RC time constants — assumes you know what $I$ is. Drift speed questions test whether $I=nqAv_d$ is real to you.",
        "For total charge, use $Q=It$. For microscopic stories, solve $v_d=I/(nqA)$. Draw an arrow of conventional current from $+$ to $-$ outside the battery.",
        lesson_figure(
            series_circuit_svg(),
            "A simple series loop",
            "In steady state the current is the same through the battery and both resistors.",
        )
        + solved(1, "$12\\,\\mathrm{C}$ pass a point in $4.0\\,\\mathrm{s}$. Find $I$.",
                 ["$I=\\Delta Q/\\Delta t$.",
                  "$12/4.0=3.0$.",
                  "Unit: amperes."],
                 "$3.0\\,\\mathrm{A}$", "", "Easy")
        + solved(2, "$I=nqAv_d$. $A$ doubles, $I$ fixed. What happens to $v_d$?",
                 ["Solve $v_d=I/(nqA)$.",
                  "$I$, $n$, $q$ fixed, $A\\times 2$.",
                  "$v_d$ halves."],
                 "$v_d\\to v_d/2$", "", "Medium")
        + solved(3, "Why is the current the same through two series resistors even if one is thicker?",
                 ["Steady state: no charge accumulation at the junction between them.",
                  "Charge per second entering the thin wire equals charge per second leaving into the thick wire.",
                  "$I$ is the same; $v_d$ is smaller in the thicker wire because $A$ is larger."],
                 "same $I$, smaller $v_d$ in the thicker wire", "", "Hard")
        + _ican(ican1),
        ("Thinking electrons move at the speed of light in the wire",
         "The drift speed is slow. What is fast is the rearrangement of the electric field (surface charges) that starts all electrons drifting almost together."),
        ("Conventional vs electron flow",
         "On AP Physics C, current arrows follow conventional current. If a problem mentions electrons, reverse that arrow for the particles themselves."),
        ican1,
        1,
    )

    ican2 = [
        "I can use $V=IR$ and $R=\\rho L/A$.",
        "I can scale $R$ when $L$ or radius changes.",
        "I can identify ohmic versus nonohmic $I$–$V$ graphs.",
    ]
    c2 = concept_block(
        "2. Ohm and resistivity",
        [
            "For many materials, the potential difference across a sample is proportional to the current: $V=IR$. $R$ is resistance, unit ohm ($\\Omega$).",
            "Resistance of a uniform wire is $R=\\rho L/A$, where $\\rho$ is resistivity (a material property, unit $\\Omega\\cdot\\mathrm{m}$), $L$ is length, and $A$ is cross-sectional area.",
            "Double the length $\\Rightarrow$ double $R$. Double the radius $\\Rightarrow$ $A\\times 4$ $\\Rightarrow$ $R$ to one-fourth.",
            "Example: $R=4.0\\,\\Omega$, $I=3.0\\,\\mathrm{A}$, $V=12\\,\\mathrm{V}$. Example: $\\rho=1.5\\times10^{-6}\\,\\Omega\\cdot\\mathrm{m}$, $L=3.0\\,\\mathrm{m}$, $A=2.0\\times10^{-6}\\,\\mathrm{m^2}$, $R=2.25\\,\\Omega$.",
            "Ohmic means a straight $I$–$V$ line through the origin. A diode or a light bulb's hot filament can be nonohmic: $R$ depends on $V$ or temperature.",
            "Microscopically, $\\vec{J}=\\sigma\\vec{E}$ with $\\sigma=1/\\rho$. Combined with $I=JA$, this is Ohm's law in local form.",
        ],
        "You cannot reduce a circuit until every resistor has an $R$. Resistivity questions test $R\\propto L/A$ independently of Kirchhoff.",
        "Write $R=\\rho L/A$ with $A=\\pi r^2$ for a round wire. For $V=IR$, first find $I$ or $R$ from the rest of the circuit, then the missing one.",
        lesson_figure(
            series_circuit_svg(),
            "Two resistors sharing one current",
            "Each obeys $V=IR$ with that same $I$; the drops add.",
        )
        + solved(1, "$R=4.0\\,\\Omega$, $I=3.0\\,\\mathrm{A}$. Find $V$.",
                 ["Ohm: $V=IR$.",
                  "$(3.0)(4.0)=12$.",
                  "$V=12\\,\\mathrm{V}$."],
                 "$12\\,\\mathrm{V}$", "", "Easy")
        + solved(2, "A wire's radius doubles, length unchanged. Factor for $R$?",
                 ["$A=\\pi r^2$ $\\times 4$.",
                  "$R=\\rho L/A$ $\\div 4$.",
                  "New resistance is $R/4$."],
                 "$R/4$", "", "Medium")
        + solved(3, "$\\rho=1.5\\times10^{-6}\\,\\Omega\\cdot\\mathrm{m}$, $L=3.0\\,\\mathrm{m}$, $A=2.0\\times10^{-6}\\,\\mathrm{m^2}$. Find $R$.",
                 ["$R=\\rho L/A$.",
                  "$(1.5\\times10^{-6})(3.0)=4.5\\times10^{-6}$.",
                  "Divide by $2.0\\times10^{-6}$: $R=2.25\\,\\Omega$."],
                 "$2.25\\,\\Omega$", "", "Hard")
        + _ican(ican2),
        ("Using diameter as if it were radius in $A=\\pi r^2$",
         "If the problem gives diameter, halve it first. Using $d$ as $r$ makes $A$ four times too large."),
        ("$A$ in the denominator",
         "Thicker wire, smaller $R$. If your intuition and your algebra disagree, you probably put $A$ in the numerator."),
        ican2,
        6,
    )

    ican3 = [
        "I can write $\\sum I=0$ at a junction and $\\sum\\Delta V=0$ around a loop.",
        "I can assign a current direction and stick to the $IR$ sign convention.",
        "I can include battery emf with the correct rise or drop.",
    ]
    c3 = concept_block(
        "3. Kirchhoff loop and junction",
        [
            "The junction rule (Kirchhoff's current law) is charge conservation: the total current into a node equals the total current out.",
            "The loop rule (Kirchhoff's voltage law) is energy conservation for electrostatics: around any closed path you return to the same potential, so $\\sum\\Delta V=0$.",
            "Sign convention that works: travel around the loop. When you cross a resistor in the direction of your assumed current, count $-IR$. When you go through a battery from $-$ to $+$, count $+\\varepsilon$.",
            "A single loop with $\\varepsilon=12\\,\\mathrm{V}$ and $R=4.0\\,\\Omega$ gives $12-I(4)=0$, so $I=3.0\\,\\mathrm{A}$.",
            "If an assumed current comes out negative, the actual current is opposite your arrow. The algebra is still correct.",
            "Multi-loop circuits need one junction equation and enough independent loops to match the number of unknown currents.",
        ],
        "RC, RL, and multi-loop capacitor circuits are Kirchhoff plus a $Q/C$ or $L\\,dI/dt$ term. This is the last purely algebraic circuit skill.",
        "Label every current with an arrow first. Write one junction. Write loops without skipping elements. Solve the linear system; then compute voltages as $IR$.",
        lesson_figure(
            _kirchhoff_loop_svg(),
            "One-loop Kirchhoff tour",
            "Rise $\\varepsilon$ through the battery, drop $IR$ through the resistor; sum zero. An ammeter in series reads $I$.",
        )
        + solved(1, "$\\varepsilon=12\\,\\mathrm{V}$, one resistor $R=4.0\\,\\Omega$. Find $I$.",
                 ["Loop: $\\varepsilon-IR=0$.",
                  "$I=\\varepsilon/R=12/4.0$.",
                  "$I=3.0\\,\\mathrm{A}$."],
                 "$3.0\\,\\mathrm{A}$", "", "Easy")
        + solved(2, "At a junction, $5.0\\,\\mathrm{A}$ flows in, $2.0\\,\\mathrm{A}$ flows out one branch. The other branch carries",
                 ["Junction: $5.0=2.0+I_3$.",
                  "$I_3=3.0\\,\\mathrm{A}$ out.",
                  "If your arrow was inward, you would get $-3.0\\,\\mathrm{A}$."],
                 "$3.0\\,\\mathrm{A}$ out", "", "Medium")
        + solved(3, "$\\varepsilon=9.0\\,\\mathrm{V}$, internal $r=1.0\\,\\Omega$, load $R=8.0\\,\\Omega$. Find $I$ and terminal voltage.",
                 ["Loop: $9.0-I(1.0)-I(8.0)=0$.",
                  "$I=9.0/9.0=1.0\\,\\mathrm{A}$.",
                  "$V_{\\mathrm{term}}=\\varepsilon-Ir=8.0\\,\\mathrm{V}$ (also $IR_{\\mathrm{load}}$)."],
                 "$I=1.0\\,\\mathrm{A}$, $V_{\\mathrm{term}}=8.0\\,\\mathrm{V}$", "", "Hard")
        + _ican(ican3),
        ("Changing the $IR$ sign convention halfway around the loop",
         "Pick a travel direction and keep it. Inconsistent signs are why loops 'don't close' even when the circuit is fine."),
        ("Arrows before algebra",
         "Draw currents on the diagram, then write $\\varepsilon-I_1 R_1-I_3 R_3=0$ by reading the drawing. Do not invent terms that are not on the path."),
        ican3,
        11,
    )

    ican4 = [
        "I can add series resistances and take parallel reciprocals.",
        "I can find series current $I=\\varepsilon/R_{\\mathrm{eq}}$ and split parallel currents as $V/R$.",
        "I can compute the voltage divider $V_i=I R_i$ in series.",
    ]
    c4 = concept_block(
        "4. Series and parallel",
        [
            "Series: one path, same current, voltages add, $R_{\\mathrm{eq}}=R_1+R_2$. A $2.0\\,\\Omega$ and $4.0\\,\\Omega$ in series make $6.0\\,\\Omega$.",
            "Parallel: same voltage, currents add, $1/R_{\\mathrm{eq}}=1/R_1+1/R_2$. Those same resistors in parallel make $4/3\\,\\Omega$.",
            "On $12\\,\\mathrm{V}$, the series pair carries $I=12/6.0=2.0\\,\\mathrm{A}$. The $4.0\\,\\Omega$ then has $V=8.0\\,\\mathrm{V}$ and the $2.0\\,\\Omega$ has $4.0\\,\\mathrm{V}$.",
            "$n$ identical resistors in parallel make $R/n$. Two identical resistors in parallel make $R/2$.",
            "Reduce mixed circuits from the inside out: replace a parallel pair by its equivalent, then that combination may be in series with something else.",
            "Example: two $6.0\\,\\Omega$ in parallel ($3.0\\,\\Omega$) in series with a third $6.0\\,\\Omega$ make $9.0\\,\\Omega$.",
        ],
        "Almost every DC FRQ starts with a series–parallel reduction, then one Kirchhoff loop. Capacitors use the swapped rules; do not mix them.",
        "Ask 'same current or same voltage?' Same current $\\Rightarrow$ series. Same two nodes $\\Rightarrow$ parallel. Then $I=\\varepsilon/R_{\\mathrm{eq}}$ or $I=V/R$ on each branch.",
        lesson_figure(
            _parallel_circuit_svg(),
            "Two resistors in parallel on one battery",
            "Each feels the full $\\varepsilon$. Currents add at the junctions.",
        )
        + solved(1, "$2.0\\,\\Omega$ and $4.0\\,\\Omega$ in series. $R_{\\mathrm{eq}}$?",
                 ["Series: add.",
                  "$2.0+4.0=6.0$.",
                  "$R_{\\mathrm{eq}}=6.0\\,\\Omega$."],
                 "$6.0\\,\\Omega$", "", "Easy")
        + solved(2, "Those two in parallel. $R_{\\mathrm{eq}}$?",
                 ["$1/R=1/2+1/4=3/4$.",
                  "$R=4/3\\,\\Omega$.",
                  "Check: equivalent must be smaller than either branch."],
                 "$4/3\\,\\Omega$", "", "Medium")
        + solved(3, "$12\\,\\mathrm{V}$ across the series pair. Find $I$ and the voltage on the $4.0\\,\\Omega$.",
                 ["$I=12/6.0=2.0\\,\\mathrm{A}$ (same in both).",
                  "$V_4=(2.0)(4.0)=8.0\\,\\mathrm{V}$.",
                  "The $2.0\\,\\Omega$ has the remaining $4.0\\,\\mathrm{V}$."],
                 "$2.0\\,\\mathrm{A}$, $8.0\\,\\mathrm{V}$ on the $4\\,\\Omega$", "", "Hard")
        + _ican(ican4),
        ("Adding parallel resistances like series",
         "Parallel $2\\,\\Omega$ and $4\\,\\Omega$ is not $6\\,\\Omega$. If your equivalent is larger than the smallest resistor, you added instead of taking reciprocals."),
        ("Redraw",
         "Stretch the circuit so parallel branches are drawn as true side-by-side paths sharing two nodes. Hidden parallels cause most reduction errors."),
        ican4,
        16,
    )

    ican5 = [
        "I can compute $P=IV=I^2 R=V^2/R$.",
        "I can match the formula to whichever of $I,V,R$ are known.",
        "I can balance battery power $\\varepsilon I$ against $\\sum I^2 R$.",
    ]
    c5 = concept_block(
        "5. Power in circuits",
        [
            "Electric power delivered to a circuit element is $P=IV$. For a resistor, $V=IR$ so also $P=I^2 R=V^2/R$.",
            "Example: $I=2.0\\,\\mathrm{A}$ through $4.0\\,\\Omega$ gives $P=16\\,\\mathrm{W}$. A $12\\,\\mathrm{V}$ battery on $6.0\\,\\Omega$ alone dissipates $P=V^2/R=24\\,\\mathrm{W}$.",
            "At fixed voltage, larger $R$ means smaller power ($P=V^2/R$). At fixed current, larger $R$ means larger power ($P=I^2 R$).",
            "A battery with emf $\\varepsilon$ supplies $\\varepsilon I$ (ideal). Internal resistance eats $I^2 r$. The load gets the rest.",
            "Example: $\\varepsilon=9.0\\,\\mathrm{V}$, $r=1.0\\,\\Omega$, $R=8.0\\,\\Omega$, $I=1.0\\,\\mathrm{A}$. Emf supplies $9.0\\,\\mathrm{W}$; $r$ dissipates $1.0\\,\\mathrm{W}$; $R$ dissipates $8.0\\,\\mathrm{W}$.",
            "Identical ohmic bulbs: brightness follows power. Series bulbs share current; the larger $R$ (if they differ) drops more $V$ and can be brighter in series — but identical bulbs in series are equally bright.",
        ],
        "Power is how circuits connect to energy. RC energy later is this same accounting with $U=\\tfrac12 CV^2$ added.",
        "Circle what is held fixed: $V$ or $I$. Then pick $V^2/R$ or $I^2 R$. Check with $\\varepsilon I=\\sum P$ on a complete circuit.",
        lesson_figure(
            energy_bars_svg(ke=0, pe=0, thermal=4),
            "Resistor power becomes thermal energy",
            "$I^2 R$ is the rate at which electrical energy becomes internal energy in the resistor.",
        )
        + solved(1, "$I=2.0\\,\\mathrm{A}$, $R=4.0\\,\\Omega$. Find $P$.",
                 ["$P=I^2 R$.",
                  "$I^2=4.0$.",
                  "$P=16\\,\\mathrm{W}$."],
                 "$16\\,\\mathrm{W}$", "", "Easy")
        + solved(2, "Fixed $12\\,\\mathrm{V}$. $R$ doubles from $6.0\\,\\Omega$ to $12\\,\\Omega$. Factor for $P$?",
                 ["$P=V^2/R$ at fixed $V$.",
                  "$R\\times 2\\Rightarrow P\\div 2$.",
                  "$24\\,\\mathrm{W}$ becomes $12\\,\\mathrm{W}$."],
                 "power halves", "", "Medium")
        + solved(3, "$\\varepsilon=9.0\\,\\mathrm{V}$, $r=1.0\\,\\Omega$, $R=8.0\\,\\Omega$. Show energy balance of power.",
                 ["$I=1.0\\,\\mathrm{A}$.",
                  "Supply $\\varepsilon I=9.0\\,\\mathrm{W}$.",
                  "$I^2 r+I^2 R=1.0+8.0=9.0\\,\\mathrm{W}$, matching."],
                 "$9\\,\\mathrm{W}$ in, $9\\,\\mathrm{W}$ dissipated", "", "Hard")
        + _ican(ican5),
        ("Using $P=I^2 R$ when $V$ is fixed and $R$ changed, without updating $I$",
         "If $V$ is fixed, $I=V/R$ changes when $R$ changes. Safer: $P=V^2/R$ when $V$ is the constraint."),
        ("Name the constraint",
         "Write 'fixed $V$' or 'fixed $I$' as the first four words of your solution. Then the correct power formula is obvious."),
        ican5,
        21,
    )

    ican6 = [
        "I can place an ammeter in series and a voltmeter in parallel.",
        "I can state ideal $R_A=0$ and $R_V=\\infty$.",
        "I can predict loading when a real voltmeter's $R$ is comparable to the circuit.",
    ]
    c6 = concept_block(
        "6. Voltmeters and ammeters",
        [
            "An ammeter measures current. It must be inserted in series with the element so that the same $I$ flows through the meter. An ideal ammeter has $R=0$ so it does not add an extra drop.",
            "A voltmeter measures potential difference. It is connected in parallel with the element. An ideal voltmeter has $R=\\infty$ so it draws no current.",
            "Putting an ammeter in parallel is a short: a near-zero resistance path that can draw a huge current and blow a fuse.",
            "Putting a voltmeter in series is nearly an open circuit: current collapses and you are not measuring the original $I$.",
            "A real voltmeter with $10\\,\\mathrm{k}\\Omega$ across a $10\\,\\mathrm{k}\\Omega$ resistor makes a $5.0\\,\\mathrm{k}\\Omega$ parallel combo and loads the voltage divider you meant to measure.",
            "In diagrams, a circle with A sits on the wire; a circle with V sits on a branch that hops across a component.",
        ],
        "Lab FRQs and circuit-identification items test placement, not just $V=IR$. A meter in the wrong place is a different circuit.",
        "Current through, voltage across. Series for A, parallel for V. If a calculated current exploded, you probably shorted with an ammeter.",
        lesson_figure(
            _meter_svg(),
            "Correct meter placement",
            "A in series with $R$; V across $R$. Swap those and the circuit is no longer the one you intended.",
        )
        + solved(1, "Ideal ammeter resistance? Ideal voltmeter resistance?",
                 ["Ammeter in series must not drop voltage: $R_A=0$.",
                  "Voltmeter in parallel must not steal current: $R_V\\to\\infty$.",
                  "Those are the ideal limits."],
                 "$R_A=0$, $R_V=\\infty$", "", "Easy")
        + solved(2, "What goes wrong if you put an ammeter in parallel with a resistor across a battery?",
                 ["The ammeter is nearly a wire.",
                  "It shorts the resistor (and possibly the battery).",
                  "Current becomes huge; the meter can be destroyed."],
                 "short circuit / huge $I$", "", "Medium")
        + solved(3, "A $10\\,\\mathrm{k}\\Omega$ voltmeter is placed across a $10\\,\\mathrm{k}\\Omega$ resistor that was part of a divider. What is the loaded resistance of that branch?",
                 ["Voltmeter and resistor are in parallel.",
                  "Two $10\\,\\mathrm{k}\\Omega$ in parallel: $5.0\\,\\mathrm{k}\\Omega$.",
                  "The divider ratio changes, so the measured $V$ is not the unloaded value."],
                 "$5.0\\,\\mathrm{k}\\Omega$ loaded branch", "", "Hard")
        + _ican(ican6),
        ("Treating a voltmeter like an ammeter",
         "If your diagram shows V sitting on the main wire in series, current will nearly stop. Move V so it hops across the component."),
        ("Say 'through' vs 'across'",
         "Current through an ammeter; voltage across a voltmeter's two leads. That language prevents swapped connections."),
        ican6,
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        ["Current and drift", "Ohm and resistivity", "Kirchhoff loop and junction",
         "Series and parallel", "Power in circuits", "Voltmeters and ammeters"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
