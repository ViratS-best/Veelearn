"""Shared helpers for high-school science master courses (AP Bio through Physical Science)."""

from __future__ import annotations

from hs_curriculum import *  # noqa: F403


def animal_cell_svg(w=320, h=220):
    """Simple labeled animal cell: membrane, cytoplasm, nucleus, mitochondria."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<ellipse cx="160" cy="110" rx="140" ry="90" fill="#fef3c7" stroke="#b45309" stroke-width="3"/>'
        f'<ellipse cx="160" cy="110" rx="134" ry="84" fill="none" stroke="#f59e0b" stroke-width="1.5"/>'
        f'<circle cx="100" cy="100" r="32" fill="#fecaca" stroke="#b91c1c" stroke-width="2"/>'
        f'<circle cx="100" cy="100" r="12" fill="#b91c1c"/>'
        f'<ellipse cx="220" cy="80" rx="22" ry="12" fill="#bbf7d0" stroke="#15803d" stroke-width="1.6"/>'
        f'<ellipse cx="230" cy="140" rx="22" ry="12" fill="#bbf7d0" stroke="#15803d" stroke-width="1.6"/>'
        f'<text x="70" y="64" font-size="11">nucleus</text>'
        f'<text x="200" y="62" font-size="11">mitochondrion</text>'
        f'<text x="200" y="200" font-size="11">cell membrane</text>'
        f"</svg>"
    )


def _zeroish_force(lab) -> bool:
    if lab is None:
        return True
    s = str(lab).lower().replace(" ", "")
    if not s or s in ("0", "none", "off"):
        return True
    if s.startswith("0") and ("net" in s or "balanced" in s or "app=0" in s):
        return True
    if "f_app=0" in s or s in ("f=0", "fn=0"):
        return True
    return False


def fbd_box(labels=("F_g", "N", "F_app"), w=260, h=200):
    """Free-body diagram: weight down, normal up, optional applied force.

    Omit the third (rightward) arrow when that label is missing or zero-ish
    (e.g. ``0 net``, ``F_app=0``), so a box at rest is not drawn with a fake pull.
    """
    down = labels[0] if labels else "F_g"
    up = labels[1] if len(labels) > 1 else "N"
    right = labels[2] if len(labels) > 2 else None
    show_right = not _zeroish_force(right)
    point_left = bool(right) and "left" in str(right).lower()
    right_svg = ""
    if show_right and point_left:
        right_svg = (
            f'<line x1="95" y1="95" x2="30" y2="95" stroke="#b91c1c" stroke-width="2.4"/>'
            f'<polygon points="32,90 20,95 32,100" fill="#b91c1c"/>'
            f'<text x="28" y="88" font-size="12" fill="#b91c1c">{right}</text>'
        )
    elif show_right:
        right_svg = (
            f'<line x1="165" y1="95" x2="230" y2="95" stroke="#b91c1c" stroke-width="2.4"/>'
            f'<polygon points="228,90 240,95 228,100" fill="#b91c1c"/>'
            f'<text x="200" y="88" font-size="12" fill="#b91c1c">{right}</text>'
        )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="95" y="70" width="70" height="50" fill="#e0e7ff" stroke="#312e81" stroke-width="2"/>'
        f'<line x1="130" y1="120" x2="130" y2="175" stroke="#0f172a" stroke-width="2.4"/>'
        f'<line x1="130" y1="70" x2="130" y2="20" stroke="#0f172a" stroke-width="2.4"/>'
        f'<polygon points="125,22 130,12 135,22" fill="#0f172a"/>'
        f'<polygon points="125,178 130,188 135,178" fill="#0f172a"/>'
        f'<text x="138" y="40" font-size="12">{up}</text>'
        f'<text x="138" y="190" font-size="12">{down}</text>'
        f"{right_svg}"
        f"</svg>"
    )


def series_circuit_svg(w=320, h=140):
    """Battery and two resistors in series."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="55" width="28" height="30" fill="#fef3c7" stroke="#0f172a"/>'
        f'<line x1="48" y1="70" x2="90" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M90 70 l8 -12 l8 24 l8 -24 l8 24 l8 -12" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<line x1="138" y1="70" x2="180" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M180 70 l8 -12 l8 24 l8 -24 l8 24 l8 -12" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<line x1="228" y1="70" x2="280" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="280" y1="70" x2="280" y2="110" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="280" y1="110" x2="34" y2="110" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="34" y1="110" x2="34" y2="85" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="18" y="48" font-size="11">ε</text>'
        f'<text x="100" y="48" font-size="11">R₁</text>'
        f'<text x="190" y="48" font-size="11">R₂</text>'
        f"</svg>"
    )


def atom_shells_svg(protons=6, electrons=(2, 4), w=240, h=240):
    """Nucleus plus electron shells. Dot counts follow ``electrons`` (e.g. (2, 8) for Na⁺)."""
    import math as _m
    cx = cy = w / 2
    shells = [int(n) for n in electrons]
    radii = [48, 88, 118][: max(len(shells), 1)]
    while len(radii) < len(shells):
        radii.append(radii[-1] + 30)
    rings = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#64748b" stroke-dasharray="4 3"/>'
        for r in radii
    )
    dots = []
    for i, n in enumerate(shells):
        r = radii[i]
        for k in range(max(n, 0)):
            th = -_m.pi / 2 + (2 * _m.pi * k / n if n else 0)
            x = cx + r * _m.cos(th)
            y = cy + r * _m.sin(th)
            fill = "#3b82f6" if i == 0 else "#1d4ed8"
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{fill}"/>')
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="{cx}" cy="{cy}" r="18" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="11">{protons}p</text>'
        f"{rings}{''.join(dots)}"
        f'<text x="12" y="22" font-size="11">electrons: {sum(shells)}</text>'
        f"</svg>"
    )


def energy_bars_svg(ke=3, pe=1, thermal=0, w=260, h=180):
    """Simple energy bar chart for before/after stories."""
    def bar(x, hgt, color, lab):
        y = 150 - hgt * 22
        return (
            f'<rect x="{x}" y="{y}" width="36" height="{hgt * 22}" fill="{color}" stroke="#0f172a"/>'
            f'<text x="{x + 18}" y="168" text-anchor="middle" font-size="11">{lab}</text>'
        )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="24" y1="150" x2="240" y2="150" stroke="#0f172a"/>'
        f'{bar(40, ke, "#93c5fd", "KE")}'
        f'{bar(110, pe, "#86efac", "PE")}'
        f'{bar(180, thermal, "#fdba74", "E_th")}'
        f"</svg>"
    )


def dna_rungs_svg(w=280, h=160):
    """Short DNA ladder with A-T and G-C pairs."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="70" y1="20" x2="70" y2="140" stroke="#1d4ed8" stroke-width="8"/>'
        f'<line x1="210" y1="20" x2="210" y2="140" stroke="#b91c1c" stroke-width="8"/>'
        f'<line x1="70" y1="40" x2="210" y2="40" stroke="#64748b" stroke-width="3"/>'
        f'<line x1="70" y1="70" x2="210" y2="70" stroke="#64748b" stroke-width="3"/>'
        f'<line x1="70" y1="100" x2="210" y2="100" stroke="#64748b" stroke-width="3"/>'
        f'<line x1="70" y1="130" x2="210" y2="130" stroke="#64748b" stroke-width="3"/>'
        f'<text x="90" y="36" font-size="11">A</text><text x="180" y="36" font-size="11">T</text>'
        f'<text x="90" y="66" font-size="11">G</text><text x="180" y="66" font-size="11">C</text>'
        f'<text x="90" y="96" font-size="11">T</text><text x="180" y="96" font-size="11">A</text>'
        f'<text x="90" y="126" font-size="11">C</text><text x="180" y="126" font-size="11">G</text>'
        f"</svg>"
    )


def field_lines_svg(w=260, h=180, kind="positive"):
    """Radial field lines around a point charge, with arrowheads.

    ``kind="positive"``: arrows leave +q. Any other kind: arrows enter −q.
    """
    import math as _m
    cx, cy = 130, 90
    outgoing = kind == "positive"
    parts = []
    for i in range(8):
        th = i * _m.pi / 4
        x2 = cx + 80 * _m.cos(th)
        y2 = cy + 80 * _m.sin(th)
        parts.append(
            f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#4f46e5" stroke-width="1.6"/>'
        )
        # Arrow near the outer end (out) or near the charge (in)
        t = 0.82 if outgoing else 0.28
        ax = cx + 80 * t * _m.cos(th)
        ay = cy + 80 * t * _m.sin(th)
        # Point along the ray if outgoing, opposite if incoming
        hx, hy = (_m.cos(th), _m.sin(th)) if outgoing else (-_m.cos(th), -_m.sin(th))
        px, py = -hy, hx
        p1x, p1y = ax - 10 * hx + 5 * px, ay - 10 * hy + 5 * py
        p2x, p2y = ax - 10 * hx - 5 * px, ay - 10 * hy - 5 * py
        parts.append(
            f'<polygon points="{ax:.1f},{ay:.1f} {p1x:.1f},{p1y:.1f} {p2x:.1f},{p2y:.1f}" fill="#4f46e5"/>'
        )
    lab = "+q" if outgoing else "−q"
    fill = "#fecaca" if outgoing else "#bfdbfe"
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f"{''.join(parts)}"
        f'<circle cx="{cx}" cy="{cy}" r="14" fill="{fill}" stroke="#0f172a"/>'
        f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="12">{lab}</text>'
        f"</svg>"
    )


def punnett_svg(a="A", b="a", c="A", d="a", w=220, h=220):
    """2×2 Punnett square. Default Aa × Aa."""
    cells = [(a, c), (b, c), (a, d), (b, d)]
    labels = [f"{x}{y}" for x, y in cells]
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="50" y="50" width="140" height="140" fill="#fff" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="120" y1="50" x2="120" y2="190" stroke="#0f172a"/>'
        f'<line x1="50" y1="120" x2="190" y2="120" stroke="#0f172a"/>'
        f'<text x="85" y="40" text-anchor="middle" font-size="14">{a}</text>'
        f'<text x="155" y="40" text-anchor="middle" font-size="14">{b}</text>'
        f'<text x="28" y="90" text-anchor="middle" font-size="14">{c}</text>'
        f'<text x="28" y="160" text-anchor="middle" font-size="14">{d}</text>'
        f'<text x="85" y="90" text-anchor="middle" font-size="14">{labels[0]}</text>'
        f'<text x="155" y="90" text-anchor="middle" font-size="14">{labels[1]}</text>'
        f'<text x="85" y="160" text-anchor="middle" font-size="14">{labels[2]}</text>'
        f'<text x="155" y="160" text-anchor="middle" font-size="14">{labels[3]}</text>'
        f"</svg>"
    )


def incline_svg(angle="θ", w=280, h=180):
    """Block on a rough incline with weight, normal, and friction."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<polygon points="20,160 240,160 240,50" fill="#e2e8f0" stroke="#334155"/>'
        f'<rect x="140" y="78" width="44" height="28" transform="rotate(-28 162 92)" fill="#c7d2fe" stroke="#312e81"/>'
        f'<text x="168" y="70" font-size="12">m</text>'
        f'<text x="210" y="150" font-size="12">{angle}</text>'
        f'<line x1="162" y1="92" x2="162" y2="150" stroke="#0f172a" stroke-width="2"/>'
        f'<polygon points="157,148 162,158 167,148" fill="#0f172a"/>'
        f'<text x="168" y="140" font-size="11">F_g</text>'
        f"</svg>"
    )


def titration_svg(w=280, h=180):
    """Sketch of a strong-acid / strong-base titration curve."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="36" y1="150" x2="250" y2="150" stroke="#0f172a"/>'
        f'<line x1="36" y1="20" x2="36" y2="150" stroke="#0f172a"/>'
        f'<path d="M50 120 C90 118, 110 116, 130 110 C145 90, 150 40, 165 28 C190 22, 230 20, 245 18" '
        f'fill="none" stroke="#b91c1c" stroke-width="2.4"/>'
        f'<text x="240" y="168" font-size="11">V_b</text>'
        f'<text x="8" y="28" font-size="11">pH</text>'
        f'<text x="150" y="70" font-size="11">eq. pt.</text>'
        f"</svg>"
    )


def spring_mass_svg(w=240, h=180):
    """Horizontal spring attached to a mass, equilibrium marked."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="10" y="40" width="14" height="100" fill="#64748b"/>'
        f'<path d="M24 90 l12 -14 l12 28 l12 -28 l12 28 l12 -28 l12 14" fill="none" stroke="#0f172a" stroke-width="2"/>'
        f'<rect x="108" y="72" width="40" height="36" fill="#93c5fd" stroke="#1e3a8a"/>'
        f'<line x1="160" y1="40" x2="160" y2="140" stroke="#94a3b8" stroke-dasharray="4 3"/>'
        f'<text x="148" y="34" font-size="11">x=0</text>'
        f'<text x="116" y="94" font-size="12">m</text>'
        f"</svg>"
    )


def gauss_sphere_svg(w=240, h=200):
    """Point charge inside a spherical Gaussian surface."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="120" cy="100" r="70" fill="none" stroke="#4f46e5" stroke-dasharray="6 4" stroke-width="2"/>'
        f'<circle cx="120" cy="100" r="10" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="120" y="104" text-anchor="middle" font-size="11">+q</text>'
        f'<text x="120" y="28" text-anchor="middle" font-size="12">Gaussian sphere</text>'
        f"</svg>"
    )


def energy_diagram_svg(w=280, h=180, label="uncatalyzed"):
    """Reaction-coordinate energy diagram with a hump."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="30" y1="150" x2="260" y2="150" stroke="#0f172a"/>'
        f'<line x1="30" y1="20" x2="30" y2="150" stroke="#0f172a"/>'
        f'<path d="M40 110 C80 110, 100 40, 140 36 C180 36, 200 90, 250 95" fill="none" stroke="#b45309" stroke-width="2.4"/>'
        f'<text x="40" y="102" font-size="11">reactants</text>'
        f'<text x="210" y="88" font-size="11">products</text>'
        f'<text x="124" y="28" font-size="11">{label}</text>'
        f'<text x="8" y="28" font-size="11">E</text>'
        f"</svg>"
    )


def beaker_svg(label="solution", w=200, h=180):
    """Beaker with particles in a liquid."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<path d="M50 30 L50 150 L150 150 L150 30" fill="none" stroke="#0f172a" stroke-width="3"/>'
        f'<rect x="54" y="70" width="92" height="76" fill="#bfdbfe"/>'
        f'<circle cx="80" cy="100" r="5" fill="#1d4ed8"/>'
        f'<circle cx="110" cy="90" r="5" fill="#1d4ed8"/>'
        f'<circle cx="95" cy="120" r="5" fill="#b91c1c"/>'
        f'<circle cx="125" cy="125" r="5" fill="#b91c1c"/>'
        f'<text x="100" y="170" text-anchor="middle" font-size="12">{label}</text>'
        f"</svg>"
    )
