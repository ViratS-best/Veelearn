"""AP Chemistry units 1–4: atomic structure through chemical reactions."""
from __future__ import annotations

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, mq,
    xy_graph, sample_curve, atom_shells_svg, beaker_svg, titration_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _qs(rows):
    return [mq(t, a, e, i, distractors=d) for i, (t, a, e, d) in enumerate(rows, 1)]


def _bars(peaks, xlab="m/z", ylab="relative intensity", w=340, h=200, x0=None, x1=None, decreasing=False):
    """Vertical spectrum bars. peaks: [(x, height, label), ...].
    decreasing=True puts large x on the left (PES binding energy convention)."""
    pad = 36
    xs = [p[0] for p in peaks]
    lo = (min(xs) - 3) if x0 is None else x0
    hi = (max(xs) + 3) if x1 is None else x1
    ymax = max(p[1] for p in peaks) * 1.18 or 1

    def X(x):
        frac = (x - lo) / (hi - lo)
        if decreasing:
            frac = 1 - frac
        return pad + frac * (w - 2 * pad)

    def Y(y):
        return h - pad - y / ymax * (h - 2 * pad)

    bits = [
        f'<line x1="{pad}" y1="{h - pad}" x2="{w - pad}" y2="{h - pad}" stroke="#0f172a"/>',
        f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h - pad}" stroke="#0f172a"/>',
        f'<text x="{w - pad}" y="{h - 8}" text-anchor="end" font-size="11">{xlab}</text>',
        f'<text x="8" y="{pad + 4}" font-size="11">{ylab}</text>',
    ]
    for x, ht, lab in peaks:
        xpix = X(x)
        ytop = Y(ht)
        bits.append(
            f'<rect x="{xpix - 5:.1f}" y="{ytop:.1f}" width="10" height="{h - pad - ytop:.1f}" fill="#b91c1c"/>'
        )
        bits.append(f'<text x="{xpix:.1f}" y="{h - pad + 14}" text-anchor="middle" font-size="10">{lab}</text>')
    return f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">{"".join(bits)}</svg>'


def _particle_box(kind="gas", w=280, h=170):
    """Particulate view of a phase. kind: gas, liquid, solid, mix."""
    wall = (
        f'<rect x="18" y="18" width="244" height="134" fill="#f8fafc" stroke="#0f172a" stroke-width="2"/>'
    )
    if kind == "solid":
        dots = []
        for i in range(4):
            for j in range(3):
                dots.append(f'<circle cx="{50 + i * 52}" cy="{50 + j * 36}" r="9" fill="#1d4ed8"/>')
        extra = "".join(dots)
        lab = "solid: ordered, touching"
    elif kind == "liquid":
        extra = (
            '<circle cx="60" cy="70" r="8" fill="#1d4ed8"/>'
            '<circle cx="88" cy="92" r="8" fill="#1d4ed8"/>'
            '<circle cx="120" cy="68" r="8" fill="#1d4ed8"/>'
            '<circle cx="150" cy="100" r="8" fill="#1d4ed8"/>'
            '<circle cx="178" cy="74" r="8" fill="#1d4ed8"/>'
            '<circle cx="210" cy="96" r="8" fill="#1d4ed8"/>'
            '<rect x="22" y="118" width="236" height="30" fill="#bfdbfe" opacity="0.5"/>'
        )
        lab = "liquid: close, disordered"
    elif kind == "mix":
        extra = (
            '<circle cx="70" cy="70" r="9" fill="#1d4ed8"/>'
            '<circle cx="130" cy="88" r="9" fill="#1d4ed8"/>'
            '<circle cx="190" cy="64" r="9" fill="#1d4ed8"/>'
            '<circle cx="95" cy="110" r="5" fill="#b91c1c"/>'
            '<circle cx="160" cy="120" r="5" fill="#b91c1c"/>'
            '<circle cx="210" cy="108" r="5" fill="#b91c1c"/>'
        )
        lab = "solution: solute among solvent"
    else:
        extra = (
            '<circle cx="50" cy="50" r="6" fill="#1d4ed8"/><line x1="56" y1="46" x2="72" y2="38" stroke="#0f172a"/>'
            '<circle cx="140" cy="70" r="6" fill="#1d4ed8"/><line x1="146" y1="66" x2="164" y2="54" stroke="#0f172a"/>'
            '<circle cx="220" cy="48" r="6" fill="#1d4ed8"/><line x1="214" y1="52" x2="198" y2="64" stroke="#0f172a"/>'
            '<circle cx="80" cy="120" r="6" fill="#1d4ed8"/><line x1="86" y1="116" x2="104" y2="104" stroke="#0f172a"/>'
            '<circle cx="180" cy="128" r="6" fill="#1d4ed8"/><line x1="174" y1="122" x2="158" y2="110" stroke="#0f172a"/>'
        )
        lab = "gas: far apart, fast, random"
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f"{wall}{extra}"
        f'<text x="{w / 2}" y="{h - 4}" text-anchor="middle" font-size="11">{lab}</text>'
        f"</svg>"
    )


def _water_lewis(w=260, h=170):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="130" cy="90" r="22" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="130" y="96" text-anchor="middle" font-size="16">O</text>'
        f'<circle cx="70" cy="130" r="16" fill="#dbeafe" stroke="#1d4ed8"/>'
        f'<text x="70" y="136" text-anchor="middle" font-size="14">H</text>'
        f'<circle cx="190" cy="130" r="16" fill="#dbeafe" stroke="#1d4ed8"/>'
        f'<text x="190" y="136" text-anchor="middle" font-size="14">H</text>'
        f'<line x1="112" y1="102" x2="84" y2="120" stroke="#0f172a" stroke-width="3"/>'
        f'<line x1="148" y1="102" x2="176" y2="120" stroke="#0f172a" stroke-width="3"/>'
        f'<text x="118" y="58" font-size="16">··</text>'
        f'<text x="132" y="58" font-size="16">··</text>'
        f'<text x="20" y="24" font-size="12">H–O–H, two lone pairs on O</text>'
        f"</svg>"
    )


def _co2_lewis(w=320, h=110):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="70" cy="55" r="20" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="70" y="61" text-anchor="middle" font-size="15">O</text>'
        f'<circle cx="160" cy="55" r="20" fill="#e2e8f0" stroke="#334155"/>'
        f'<text x="160" y="61" text-anchor="middle" font-size="15">C</text>'
        f'<circle cx="250" cy="55" r="20" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="250" y="61" text-anchor="middle" font-size="15">O</text>'
        f'<line x1="92" y1="48" x2="138" y2="48" stroke="#0f172a" stroke-width="2.4"/>'
        f'<line x1="92" y1="62" x2="138" y2="62" stroke="#0f172a" stroke-width="2.4"/>'
        f'<line x1="182" y1="48" x2="228" y2="48" stroke="#0f172a" stroke-width="2.4"/>'
        f'<line x1="182" y1="62" x2="228" y2="62" stroke="#0f172a" stroke-width="2.4"/>'
        f'<text x="160" y="100" text-anchor="middle" font-size="12">O=C=O, linear, 180°</text>'
        f"</svg>"
    )


def _ch4_vsepr(w=240, h=200):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="120" cy="100" r="18" fill="#e2e8f0" stroke="#334155"/>'
        f'<text x="120" y="106" text-anchor="middle" font-size="14">C</text>'
        f'<circle cx="120" cy="36" r="14" fill="#dbeafe" stroke="#1d4ed8"/>'
        f'<text x="120" y="41" text-anchor="middle" font-size="12">H</text>'
        f'<circle cx="120" cy="164" r="14" fill="#dbeafe" stroke="#1d4ed8"/>'
        f'<text x="120" y="169" text-anchor="middle" font-size="12">H</text>'
        f'<circle cx="48" cy="128" r="14" fill="#dbeafe" stroke="#1d4ed8"/>'
        f'<text x="48" y="133" text-anchor="middle" font-size="12">H</text>'
        f'<circle cx="192" cy="128" r="14" fill="#dbeafe" stroke="#1d4ed8"/>'
        f'<text x="192" y="133" text-anchor="middle" font-size="12">H</text>'
        f'<line x1="120" y1="82" x2="120" y2="50" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="120" y1="118" x2="120" y2="150" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="104" y1="110" x2="62" y2="122" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="136" y1="110" x2="178" y2="122" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="120" y="196" text-anchor="middle" font-size="12">CH₄ tetrahedral, 109.5°</text>'
        f"</svg>"
    )


def _bf3_vsepr(w=260, h=180):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="130" cy="100" r="18" fill="#fde68a" stroke="#b45309"/>'
        f'<text x="130" y="106" text-anchor="middle" font-size="14">B</text>'
        f'<circle cx="130" cy="32" r="14" fill="#d1fae5" stroke="#047857"/>'
        f'<text x="130" y="37" text-anchor="middle" font-size="12">F</text>'
        f'<circle cx="52" cy="148" r="14" fill="#d1fae5" stroke="#047857"/>'
        f'<text x="52" y="153" text-anchor="middle" font-size="12">F</text>'
        f'<circle cx="208" cy="148" r="14" fill="#d1fae5" stroke="#047857"/>'
        f'<text x="208" y="153" text-anchor="middle" font-size="12">F</text>'
        f'<line x1="130" y1="82" x2="130" y2="46" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="116" y1="112" x2="66" y2="140" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="144" y1="112" x2="194" y2="140" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="130" y="176" text-anchor="middle" font-size="12">BF₃ trigonal planar, 120°</text>'
        f"</svg>"
    )


def _so2_bent(w=280, h=160):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="140" cy="70" r="18" fill="#fde68a" stroke="#b45309"/>'
        f'<text x="140" y="76" text-anchor="middle" font-size="14">S</text>'
        f'<circle cx="70" cy="120" r="16" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="70" y="126" text-anchor="middle" font-size="14">O</text>'
        f'<circle cx="210" cy="120" r="16" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="210" y="126" text-anchor="middle" font-size="14">O</text>'
        f'<line x1="124" y1="82" x2="86" y2="108" stroke="#0f172a" stroke-width="2.4"/>'
        f'<line x1="156" y1="82" x2="194" y2="108" stroke="#0f172a" stroke-width="2.4"/>'
        f'<text x="128" y="48" font-size="14">··</text>'
        f'<text x="140" y="156" text-anchor="middle" font-size="12">SO₂ bent (~120°), resonance</text>'
        f"</svg>"
    )


def _ozone_res(w=300, h=130):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<text x="20" y="40" font-size="16">O=O⁺–O⁻</text>'
        f'<text x="155" y="40" font-size="18">↔</text>'
        f'<text x="185" y="40" font-size="16">⁻O–O⁺=O</text>'
        f'<text x="20" y="80" font-size="12">Each O–O bond is identical in the real hybrid.</text>'
        f'<text x="20" y="108" font-size="12">Formal charges: the outer atoms share −1 / 0.</text>'
        f"</svg>"
    )


def _hybrid_sp3(w=280, h=180):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="140" cy="90" r="16" fill="#e2e8f0" stroke="#334155"/>'
        f'<text x="140" y="96" text-anchor="middle" font-size="12">C</text>'
        f'<line x1="140" y1="74" x2="140" y2="28" stroke="#4f46e5" stroke-width="3"/>'
        f'<line x1="140" y1="106" x2="140" y2="152" stroke="#4f46e5" stroke-width="3"/>'
        f'<line x1="126" y1="100" x2="70" y2="140" stroke="#4f46e5" stroke-width="3"/>'
        f'<line x1="154" y1="100" x2="210" y2="140" stroke="#4f46e5" stroke-width="3"/>'
        f'<text x="148" y="24" font-size="11">sp³</text>'
        f'<text x="40" y="24" font-size="12">four equivalent sp³ lobes, 109.5°</text>'
        f"</svg>"
    )


def _polar_hcl(w=280, h=140):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="90" cy="70" r="20" fill="#dbeafe" stroke="#1d4ed8"/>'
        f'<text x="90" y="76" text-anchor="middle" font-size="16">H</text>'
        f'<circle cx="190" cy="70" r="28" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="190" y="76" text-anchor="middle" font-size="16">Cl</text>'
        f'<line x1="110" y1="70" x2="162" y2="70" stroke="#0f172a" stroke-width="3"/>'
        f'<polygon points="150,62 168,70 150,78" fill="#0f172a"/>'
        f'<text x="80" y="28" font-size="14">δ+</text>'
        f'<text x="200" y="28" font-size="14">δ−</text>'
        f'<text x="140" y="128" text-anchor="middle" font-size="12">dipole points toward Cl</text>'
        f"</svg>"
    )


def _coulomb_pair(w=300, h=150):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="70" cy="70" r="22" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="70" y="76" text-anchor="middle" font-size="12">+Z</text>'
        f'<circle cx="230" cy="70" r="10" fill="#3b82f6"/>'
        f'<text x="248" y="76" font-size="12">e⁻</text>'
        f'<line x1="92" y1="70" x2="220" y2="70" stroke="#64748b" stroke-dasharray="5 4"/>'
        f'<text x="140" y="60" font-size="12">r</text>'
        f'<text x="20" y="130" font-size="12">F ∝ (Z_eff)(e) / r²  — larger Z or smaller r, stronger pull</text>'
        f"</svg>"
    )


def _ppt_beakers(w=320, h=170):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<path d="M30 30 L30 140 L110 140 L110 30" fill="none" stroke="#0f172a" stroke-width="2.5"/>'
        f'<rect x="34" y="80" width="72" height="56" fill="#bfdbfe"/>'
        f'<text x="70" y="160" text-anchor="middle" font-size="11">AgNO₃(aq)</text>'
        f'<path d="M140 30 L140 140 L220 140 L220 30" fill="none" stroke="#0f172a" stroke-width="2.5"/>'
        f'<rect x="144" y="80" width="72" height="56" fill="#bbf7d0"/>'
        f'<text x="180" y="160" text-anchor="middle" font-size="11">NaCl(aq)</text>'
        f'<path d="M250 30 L250 140 L310 140 L310 30" fill="none" stroke="#0f172a" stroke-width="2.5"/>'
        f'<rect x="254" y="80" width="52" height="56" fill="#e2e8f0"/>'
        f'<rect x="262" y="118" width="36" height="14" fill="#f8fafc" stroke="#64748b"/>'
        f'<text x="280" y="160" text-anchor="middle" font-size="11">AgCl(s)</text>'
        f'<text x="122" y="70" font-size="16">+</text>'
        f'<text x="226" y="70" font-size="16">→</text>'
        f"</svg>"
    )


def _bond_types_svg(w=420, h=180):
    """Ionic lattice vs molecular covalent vs metallic — not a precipitation cartoon."""
    lattice = []
    for i in range(3):
        for j in range(3):
            fill = "#1d4ed8" if (i + j) % 2 == 0 else "#fecaca"
            stroke = "#1e3a8a" if (i + j) % 2 == 0 else "#b91c1c"
            lattice.append(
                f'<circle cx="{28 + i * 28}" cy="{40 + j * 28}" r="9" fill="{fill}" stroke="{stroke}"/>'
            )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="8" y="16" width="120" height="120" fill="#f8fafc" stroke="#0f172a"/>'
        f"{''.join(lattice)}"
        f'<text x="68" y="168" text-anchor="middle" font-size="11">ionic lattice (NaCl)</text>'
        f'<rect x="150" y="16" width="120" height="120" fill="#f8fafc" stroke="#0f172a"/>'
        f'<circle cx="178" cy="76" r="14" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="178" y="80" text-anchor="middle" font-size="11">O</text>'
        f'<circle cx="210" cy="76" r="14" fill="#e2e8f0" stroke="#334155"/>'
        f'<text x="210" y="80" text-anchor="middle" font-size="11">C</text>'
        f'<circle cx="242" cy="76" r="14" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="242" y="80" text-anchor="middle" font-size="11">O</text>'
        f'<line x1="192" y1="70" x2="196" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="192" y1="82" x2="196" y2="82" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="224" y1="70" x2="228" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="224" y1="82" x2="228" y2="82" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="210" y="168" text-anchor="middle" font-size="11">molecule (CO₂)</text>'
        f'<rect x="292" y="16" width="120" height="120" fill="#f8fafc" stroke="#0f172a"/>'
        f'<circle cx="322" cy="48" r="10" fill="#94a3b8" stroke="#334155"/>'
        f'<circle cx="352" cy="70" r="10" fill="#94a3b8" stroke="#334155"/>'
        f'<circle cx="382" cy="50" r="10" fill="#94a3b8" stroke="#334155"/>'
        f'<circle cx="338" cy="100" r="10" fill="#94a3b8" stroke="#334155"/>'
        f'<circle cx="372" cy="108" r="10" fill="#94a3b8" stroke="#334155"/>'
        f'<circle cx="318" cy="88" r="3" fill="#4f46e5"/>'
        f'<circle cx="348" cy="44" r="3" fill="#4f46e5"/>'
        f'<circle cx="390" cy="88" r="3" fill="#4f46e5"/>'
        f'<circle cx="360" cy="92" r="3" fill="#4f46e5"/>'
        f'<text x="352" y="168" text-anchor="middle" font-size="11">metal (cations + e⁻ sea)</text>'
        f"</svg>"
    )


def _limiting_svg(w=320, h=150):
    h2 = "".join(f'<circle cx="{40 + i * 28}" cy="50" r="10" fill="#93c5fd" stroke="#1d4ed8"/>' for i in range(4))
    o2 = '<ellipse cx="80" cy="110" rx="22" ry="12" fill="#fecaca" stroke="#b91c1c"/>'
    leftover = (
        '<circle cx="220" cy="50" r="10" fill="#93c5fd" stroke="#1d4ed8"/>'
        '<circle cx="248" cy="50" r="10" fill="#93c5fd" stroke="#1d4ed8"/>'
    )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f"{h2}{o2}"
        f'<text x="20" y="24" font-size="12">before: 4 H₂ + 1 O₂</text>'
        f'<text x="200" y="24" font-size="12">after: 2 H₂O + 2 H₂ left</text>'
        f'<rect x="200" y="90" width="36" height="22" fill="#bbf7d0" stroke="#047857"/>'
        f'<rect x="244" y="90" width="36" height="22" fill="#bbf7d0" stroke="#047857"/>'
        f"{leftover}"
        f'<text x="80" y="142" font-size="11">O₂ limits; leftover H₂</text>'
        f"</svg>"
    )


def _stoich_h2o_svg(w=360, h=170):
    """Countable 2 H₂ + 1 O₂ → 2 H₂O particles — not a generic 2-blue-2-red beaker."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="36" cy="48" r="10" fill="#93c5fd" stroke="#1d4ed8"/>'
        f'<circle cx="58" cy="48" r="10" fill="#93c5fd" stroke="#1d4ed8"/>'
        f'<line x1="46" y1="48" x2="48" y2="48" stroke="#1e3a8a" stroke-width="3"/>'
        f'<circle cx="36" cy="92" r="10" fill="#93c5fd" stroke="#1d4ed8"/>'
        f'<circle cx="58" cy="92" r="10" fill="#93c5fd" stroke="#1d4ed8"/>'
        f'<text x="47" y="128" text-anchor="middle" font-size="12">2 H₂</text>'
        f'<text x="88" y="74" font-size="18">+</text>'
        f'<circle cx="118" cy="62" r="12" fill="#fecaca" stroke="#b91c1c"/>'
        f'<circle cx="144" cy="62" r="12" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="131" y="128" text-anchor="middle" font-size="12">1 O₂</text>'
        f'<text x="176" y="74" font-size="18">→</text>'
        f'<circle cx="230" cy="48" r="12" fill="#fecaca" stroke="#b91c1c"/>'
        f'<circle cx="212" cy="68" r="9" fill="#93c5fd" stroke="#1d4ed8"/>'
        f'<circle cx="248" cy="68" r="9" fill="#93c5fd" stroke="#1d4ed8"/>'
        f'<circle cx="230" cy="108" r="12" fill="#fecaca" stroke="#b91c1c"/>'
        f'<circle cx="212" cy="128" r="9" fill="#93c5fd" stroke="#1d4ed8"/>'
        f'<circle cx="248" cy="128" r="9" fill="#93c5fd" stroke="#1d4ed8"/>'
        f'<text x="230" y="158" text-anchor="middle" font-size="12">2 H₂O</text>'
        f'<text x="300" y="88" font-size="11">count: 2 + 1 → 2</text>'
        f"</svg>"
    )


def _imf_stack(w=280, h=190):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="40" y="20" width="200" height="32" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="140" y="42" text-anchor="middle" font-size="12">hydrogen bonding (strongest IMF)</text>'
        f'<rect x="40" y="64" width="200" height="32" fill="#fed7aa" stroke="#c2410c"/>'
        f'<text x="140" y="86" text-anchor="middle" font-size="12">dipole–dipole</text>'
        f'<rect x="40" y="108" width="200" height="32" fill="#fde68a" stroke="#b45309"/>'
        f'<text x="140" y="130" text-anchor="middle" font-size="12">London dispersion (always present)</text>'
        f'<text x="140" y="170" text-anchor="middle" font-size="11">ionic / network covalent are not IMFs</text>'
        f"</svg>"
    )


def _tlc_svg(w=200, h=210):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="70" y="16" width="60" height="170" fill="#fef3c7" stroke="#0f172a"/>'
        f'<line x1="70" y1="170" x2="130" y2="170" stroke="#1d4ed8" stroke-width="2"/>'
        f'<circle cx="100" cy="155" r="6" fill="#1d4ed8"/>'
        f'<circle cx="100" cy="90" r="8" fill="#b91c1c"/>'
        f'<circle cx="100" cy="50" r="7" fill="#047857"/>'
        f'<line x1="70" y1="28" x2="130" y2="28" stroke="#64748b" stroke-dasharray="4 3"/>'
        f'<text x="140" y="32" font-size="11">solvent front</text>'
        f'<text x="140" y="94" font-size="11">spot B</text>'
        f'<text x="140" y="160" font-size="11">origin</text>'
        f"</svg>"
    )


def _redox_flow(w=300, h=120):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="36" width="80" height="48" fill="#dbeafe" stroke="#1d4ed8"/>'
        f'<text x="60" y="66" text-anchor="middle" font-size="14">Zn</text>'
        f'<rect x="200" y="36" width="80" height="48" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="240" y="66" text-anchor="middle" font-size="14">Cu²⁺</text>'
        f'<polygon points="110,60 190,60 190,52 210,70 190,88 190,80 110,80" fill="#4f46e5"/>'
        f'<text x="150" y="28" text-anchor="middle" font-size="12">2 e⁻ transferred</text>'
        f'<text x="60" y="108" text-anchor="middle" font-size="11">oxidized</text>'
        f'<text x="240" y="108" text-anchor="middle" font-size="11">reduced</text>'
        f"</svg>"
    )


# ===========================================================================
# UNIT 1
# ===========================================================================

def _u1_questions():
    return _qs([
        ("A 36.0 g sample of H₂O has molar mass 18.0 g/mol. How many moles of water are present?",
         "2.00 mol", "n = 36.0/18.0 = 2.00 mol.", ["1.00 mol", "18.0 mol", "0.500 mol"]),
        ("Convert 2.00 mol of NaCl (58.5 g/mol) into grams.",
         "117 g", "m = nM = 2.00×58.5 = 117 g.", ["29.3 g", "58.5 g", "1170 g"]),
        ("How many molecules are in 2.00 mol of CO₂? Use $N_A=6.022\\times10^{23}$.",
         "1.204×10²⁴", "2.00×6.022×10²³ = 1.204×10²⁴ molecules.",
         ["6.022×10²³", "3.011×10²³", "2.00×10²³"]),
        ("Glucose is C₆H₁₂O₆ (180. g/mol). A 45.0 g sample contains how many moles?",
         "0.250 mol", "45.0/180. = 0.250 mol.", ["0.500 mol", "1.00 mol", "8.10 mol"]),
        ("In plain language, one mole is best described as:",
         "6.022×10²³ particles of that substance",
         "A mole is a counting unit, like a dozen, but equal to Avogadro's number of particles.",
         ["the mass of one atom in grams", "always 22.4 grams of gas", "the charge of one electron"]),
        ("Chlorine is 75.0% ³⁵Cl and 25.0% ³⁷Cl. What is the average atomic mass?",
         "35.5 amu", "0.750(35)+0.250(37)=26.25+9.25=35.5 amu.", ["36.0 amu", "35.0 amu", "37 amu"]),
        ("An element has isotopes of mass 10.0 (80.0%) and 11.0 (20.0%). Average atomic mass?",
         "10.2 amu", "0.800(10.0)+0.200(11.0)=8.00+2.20=10.2.", ["10.5 amu", "11.0 amu", "9.0 amu"]),
        ("Cl₂ can show mass-spec peaks near 70, 72, and 74. The best explanation is:",
         "³⁵Cl and ³⁷Cl combine in three mass pairings",
         "³⁵Cl–³⁵Cl = 70, ³⁵Cl–³⁷Cl = 72, ³⁷Cl–³⁷Cl = 74.",
         ["chlorine always ionizes to Cl³⁺", "fragmentation of water", "the molecule has three bonds"]),
        ("In an elemental mass spectrum, the relative height of an isotope peak is proportional to:",
         "the natural abundance of that isotope",
         "More atoms of an isotope produce a taller ion signal at that m/z.",
         ["the nuclear charge only", "the boiling point", "the number of valence electrons"]),
        ("Mg is 79% ²⁴Mg, 10% ²⁵Mg, and 11% ²⁶Mg. Average atomic mass?",
         "24.32 amu", "0.79(24)+0.10(25)+0.11(26)=18.96+2.50+2.86=24.32.",
         ["25.00 amu", "24.00 amu", "26 amu"]),
        ("What is the ground-state electron configuration of O (Z=8)?",
         "1s² 2s² 2p⁴", "Eight electrons fill 1s, then 2s, then four in 2p.",
         ["1s² 2s² 2p⁶", "1s² 2s⁶", "1s² 2p⁶"]),
        ("Iron is [Ar] 4s² 3d⁶. The configuration of Fe²⁺ is:",
         "[Ar] 3d⁶", "Transition metals lose 4s electrons before 3d electrons.",
         ["[Ar] 4s² 3d⁴", "[Ar] 4s² 3d⁶", "[Ar] 3d⁴"]),
        ("Which orbital-filling statement violates Hund's rule for a p subshell?",
         "putting both electrons in the same p orbital before each has one",
         "Hund: place one electron in each degenerate orbital before pairing.",
         ["filling 1s before 2s", "giving paired electrons opposite spins", "using the Aufbau order"]),
        ("The maximum number of electrons that can occupy the entire 2p subshell is:",
         "6", "Three 2p orbitals × 2 electrons each = 6.", ["2", "3", "8"]),
        ("Chromium is often written 4s¹ 3d⁵ rather than 4s² 3d⁴ because:",
         "a half-filled 3d set is especially stable",
         "The 4s¹ 3d⁵ arrangement gives five unpaired 3d electrons.",
         ["chromium has only 5 electrons", "4s cannot hold two electrons", "PES forbids 4s²"]),
        ("On a PES plot, the peak at the highest binding energy corresponds to:",
         "the most tightly held inner electrons (often 1s)",
         "Inner electrons feel a larger effective nuclear charge at smaller r.",
         ["valence electrons", "the 2p electrons of every atom", "unpaired electrons only"]),
        ("Neon is 1s² 2s² 2p⁶. Relative PES peak areas (1s : 2s : 2p) are closest to:",
         "2 : 2 : 6", "Peak area tracks electron count in that subshell.",
         ["1 : 1 : 1", "2 : 6 : 2", "8 : 2 : 6"]),
        ("The 1s PES peak of fluorine is at higher binding energy than the 1s peak of oxygen because:",
         "F has a larger nuclear charge at a similar inner radius",
         "Both 1s electrons sit close to the nucleus; F has Z=9 vs O Z=8.",
         ["F has more shielding than O", "oxygen 1s electrons are farther out", "fluorine is a gas"]),
        ("A PES spectrum shows only two peaks, with areas 2 and 1. The element is most likely:",
         "Li", "Li is 1s² 2s¹, so a tall inner peak and a small valence peak.",
         ["He", "Be", "C"]),
        ("A photon ejects a 2p electron more easily than a 1s electron of the same atom because:",
         "the 2p electron has a smaller binding energy",
         "Valence electrons are farther from the nucleus and more shielded.",
         ["2p electrons have greater mass", "1s electrons are unpaired", "PES cannot eject 1s electrons"]),
        ("Across period 3 from Na to Cl, atomic radius generally:",
         "decreases", "Z_eff rises while n stays 3, so the cloud is pulled in.",
         ["increases steadily", "is unchanged", "jumps up at each metal"]),
        ("Mg has a higher first ionization energy than Al, even though Al is to the right, mainly because:",
         "Al's electron is in 3p, slightly higher energy than Mg's 3s²",
         "Removing a 3p electron from Al costs less than breaking Mg's filled 3s².",
         ["Al has a larger nuclear charge so it is easier", "Mg is a noble gas", "Al is smaller than Mg"]),
        ("Electronegativity of F compared with I is:",
         "greater for F", "F is smaller and has a higher Z_eff on bonding electrons.",
         ["greater for I", "equal", "undefined for halogens"]),
        ("A Na⁺ ion is smaller than a Na atom because:",
         "Na⁺ has lost the 3s electron and the remaining cloud is held more tightly",
         "Fewer electrons and a 2p⁶ outer shell at n=2 shrink the radius.",
         ["Na⁺ has more protons than Na", "cations always add electrons", "Na⁺ is isoelectronic with K"]),
        ("A huge jump after the second ionization energy (IE2 ≪ IE3) most likely means the element is in:",
         "group 2", "The third electron comes from a much more stable inner shell.",
         ["group 1", "group 17", "group 18"]),
        ("Coulomb's law says if the electron–nucleus distance doubles while charges stay the same, the attractive force becomes:",
         "1/4 as large", "F ∝ 1/r², so doubling r divides F by 4.",
         ["1/2 as large", "twice as large", "unchanged"]),
        ("Why is the valence electron of F more strongly attracted than that of Li?",
         "F has a larger Z_eff at a smaller valence radius",
         "Both are in n=2, but F has Z=9 vs Li Z=3 after similar inner shielding.",
         ["F has more electron shells", "Li has a larger nuclear charge", "F valence electrons are farther out"]),
        ("Be has a higher first IE than Li primarily because:",
         "same n, but Be has a larger nuclear charge so stronger Coulomb pull",
         "The 2s electron in Be feels Z_eff ≈ 2 vs ≈ 1 in Li.",
         ["Be is larger than Li", "Li has a filled 2s subshell", "Be has more shielding shells"]),
        ("Inner 1s electrons experience a stronger attraction than valence electrons mainly because:",
         "r is much smaller, and F grows as 1/r²",
         "Even with similar charges, a tiny radius makes F very large.",
         ["1s electrons have more mass", "valence electrons have charge +2", "PES cannot detect valence electrons"]),
        ("Cs has a much lower first IE than Li even though both are group 1 because:",
         "the Cs valence electron is in a much larger shell (larger r)",
         "Coulomb attraction falls rapidly as r increases down the group.",
         ["Cs has fewer protons than Li", "Li is more metallic", "Cs valence electrons are 1s"]),
        ("A 4.00 g sample of He (4.00 g/mol) contains how many atoms?",
         "6.022×10²³", "n=1.00 mol, so N=N_A atoms.",
         ["1.204×10²⁴", "4.00×10²³", "2.00 mol atoms"]),
        ("Si is 92.2% ²⁸Si, 4.7% ²⁹Si, and 3.1% ³⁰Si. Average atomic mass is closest to:",
         "28.11 amu", "0.922(28)+0.047(29)+0.031(30)=25.816+1.363+0.930=28.109.",
         ["29.00 amu", "28.00 amu", "30 amu"]),
        ("Cu is [Ar] 4s¹ 3d¹⁰. The configuration of Cu⁺ is:",
         "[Ar] 3d¹⁰", "The 4s electron is lost first, leaving a full 3d¹⁰.",
         ["[Ar] 4s¹ 3d⁹", "[Ar] 4s² 3d⁸", "[Ar] 3d⁹"]),
        ("Nitrogen is 1s² 2s² 2p³ and oxygen is 1s² 2s² 2p⁴. Compared with N, the O 2p PES peak is:",
         "taller (more electrons) and at slightly higher BE",
         "O has four 2p electrons vs three, and a larger Z.",
         ["missing", "at much lower BE than N 1s", "exactly half as tall"]),
        ("Rank ionic radii from largest to smallest: O²⁻, F⁻, Na⁺, Mg²⁺ (all 1s²2s²2p⁶).",
         "O²⁻ > F⁻ > Na⁺ > Mg²⁺",
         "Same electron count; more protons pull harder, so radius shrinks from O²⁻ to Mg²⁺.",
         ["Mg²⁺ > Na⁺ > F⁻ > O²⁻", "F⁻ > O²⁻ > Na⁺ > Mg²⁺", "all equal because they are isoelectronic"]),
        ("If nuclear charge doubles and distance also doubles, Coulomb force becomes:",
         "half as large", "F₂/F₁ = (2)/(2)² = 2/4 = 1/2.",
         ["4 times", "unchanged", "1/4 as large"]),
        ("A compound is 40.0% C, 6.7% H, and 53.3% O by mass. The empirical formula is:",
         "CH₂O", "Assume 100 g: 3.33 mol C, 6.7 mol H, 3.33 mol O → C:H:O = 1:2:1.",
         ["C₂H₂O", "CH₄O", "CO₂"]),
        ("A mass spectrum of BrCl can show a molecular-ion near 114, 116, and 118. That pattern is from:",
         "⁷⁹Br/⁸¹Br with ³⁵Cl/³⁷Cl mass combinations",
         "Bromine and chlorine each have two common isotopes, so several molecular masses appear.",
         ["the molecule breaking into C atoms", "only ⁷⁹Br–³⁵Cl existing", "PES of the 1s electrons"]),
        ("Which pair is isoelectronic?",
         "F⁻ and Ne", "Both have 10 electrons (1s²2s²2p⁶).",
         ["Na and Ne", "O²⁻ and F", "K⁺ and Na"]),
        ("A rough Z_eff for a Li valence electron (Z=3, two inner shielders) is closest to:",
         "1", "Z_eff ≈ Z − inner electrons = 3 − 2 = 1.",
         ["3", "2", "6"]),
        ("When 2.00 mol of Al metal forms Al³⁺, how many moles of electrons are transferred?",
         "6.00 mol e⁻", "Each Al loses 3 e⁻, so 2.00×3 = 6.00 mol electrons.",
         ["2.00 mol e⁻", "3.00 mol e⁻", "1.50 mol e⁻"]),
        ("Across a period, 1s binding energy generally increases because:",
         "nuclear charge rises while 1s radius stays very small",
         "Coulomb attraction on inner electrons grows with Z.",
         ["atoms get much larger", "shielding of 1s by valence electrons dominates", "1s electrons pair less"]),
        ("The second ionization energy of Na is enormous compared with the first because:",
         "the second electron is taken from a stable 2p⁶ core",
         "Na⁺ is like neon; ripping a core electron costs far more energy.",
         ["Na has two valence electrons", "IE always doubles", "Na²⁺ is smaller than He"]),
        ("An element has isotopes 63 (69.2%) and 65 (30.8%). Average atomic mass?",
         "63.62 amu", "0.692(63)+0.308(65)=43.60+20.02=63.62 (copper-like).",
         ["64.00 amu", "65 amu", "63 amu"]),
        ("How many moles are in 1.5055×10²⁴ molecules of N₂? Use $N_A=6.022\\times10^{23}$.",
         "2.500 mol", "1.5055×10²⁴ / 6.022×10²³ = 2.500 mol.",
         ["1.000 mol", "6.022 mol", "0.250 mol"]),
        ("A 1s electron vs a 2s electron of the same atom: the Coulomb force on the 1s electron is larger mainly due to:",
         "much smaller r in F ∝ 1/r²",
         "Inner orbitals sit closer to the nucleus.",
         ["the 1s electron having charge +2", "2s electrons having more protons", "PES forbidding 2s ionization"]),
        ("AP Stretch: 50.0 g of CaCO₃ (100. g/mol) is completely decomposed. How many formula units of CaCO₃ were in the sample? Use $N_A=6.022\\times10^{23}$.",
         "3.011×10²³", "n=50.0/100.=0.500 mol; N=0.500×6.022×10²³=3.011×10²³.",
         ["6.022×10²³", "50.0×10²³", "1.00×10²³"]),
        ("AP Stretch: An unknown has isotopes 24 (80.0%), 25 (10.0%), and 26 (10.0%). Average atomic mass?",
         "24.3 amu", "0.800(24)+0.100(25)+0.100(26)=19.2+2.5+2.6=24.3 amu.",
         ["25.0 amu", "24.0 amu", "26.0 amu"]),
        ("AP Stretch: Justify the electron configuration of Fe³⁺ given Fe is [Ar] 4s² 3d⁶.",
         "[Ar] 3d⁵", "Lose both 4s electrons and one 3d electron, leaving a half-filled 3d⁵.",
         ["[Ar] 4s² 3d³", "[Ar] 4s¹ 3d⁵", "[Ar] 3d⁶"]),
        ("AP Stretch: Phosphorus is 1s² 2s² 2p⁶ 3s² 3p³. Expected PES peak-area ratio from highest BE to lowest is:",
         "2:2:6:2:3", "Electron counts in 1s, 2s, 2p, 3s, 3p.",
         ["2:8:5", "15:1", "2:2:6:5"]),
        ("AP Stretch: Using Coulomb's law, explain why the first IE of Al is lower than that of Mg even though Al has a larger Z.",
         "Al's electron is 3p (farther/higher E) vs Mg's 3s²",
         "The extra proton is more than offset by placing the electron in a 3p orbital that is less tightly held.",
         ["Al is larger in every shell including 1s", "Mg has a greater nuclear charge", "Al forms a −1 ion"]),
        ("AP Stretch: Compare 1s binding energies of C (Z=6) and N (Z=7). The larger 1s BE belongs to:",
         "N, because Z is larger at nearly the same 1s radius",
         "Inner electrons of N feel a stronger nuclear pull.",
         ["C, because it has fewer electrons", "they are equal", "N, because it is larger"]),
        ("AP Stretch: A 2.38 g sample of a CoCl₂ hydrate is heated and leaves 1.30 g of anhydrous CoCl₂ (130. g/mol). Determine n in CoCl₂·nH₂O (H₂O=18.0 g/mol).",
         "CoCl₂·6H₂O",
         "n_CoCl₂=1.30/130.=0.0100 mol. Mass of water=2.38−1.30=1.08 g; n_H₂O=1.08/18.0=0.0600 mol. Ratio 0.0600/0.0100=6.",
         ["CoCl₂·H₂O", "CoCl₂·5H₂O", "CoCl₂·2H₂O"]),
        ("AP Stretch: Successive IE values (kJ/mol) are 578, 1817, 2745, 11577. The element is in which group?",
         "group 13",
         "IE1–IE3 are moderate (three valence electrons). The huge jump to IE4 means the fourth electron is core, so group 13.",
         ["group 1 (jump after IE1)", "group 2 (jump after IE2)", "group 14 (jump after IE4)"]),
        ("AP Stretch: Two electrons feel charges +1 and +1 at distance r, then +2 and +1 at distance 3r. The ratio F_new/F_old is:",
         "2/9", "F ∝ q₁q₂/r² so (2·1)/(3)² = 2/9.",
         ["2", "6", "2/3"]),
    ])


def build_unit1():
    title = "AP Chemistry Unit 1: Atomic Structure and Properties"
    description = (
        "Moles, mass spectrometry, electron configuration, PES, periodic trends, and Coulombic attraction "
        "with worked arithmetic and labeled atomic diagrams."
    )
    c1 = concept_block(
        "1. Moles and molar mass",
        [
            "A mole is a counting unit, just as a dozen means 12. One mole of anything contains "
            "$N_A=6.022\\times10^{23}$ particles — atoms, molecules, or formula units. The mole lets chemists "
            "count particles by weighing a sample on a balance.",
            "Molar mass $M$ is the mass of one mole, in grams per mole. Numerically it matches the formula mass "
            "in amu: H₂O is $18.0$ amu per molecule, so $18.0$ g/mol. Carbon-12 is defined so that $12$ g of ¹²C "
            "is exactly one mole of carbon atoms.",
            "The two conversions you will use constantly are $n=m/M$ (grams to moles) and $N=nN_A$ (moles to "
            "particles). Always write the unit you want to cancel. Going grams → moles → molecules is a two-step "
            "chain, not a single magic formula.",
            "Example of the chain: $36.0$ g H₂O is $36.0/18.0=2.00$ mol, which is "
            "$2.00\\times6.022\\times10^{23}=1.204\\times10^{24}$ molecules. Notice the arithmetic is ordinary "
            "division and multiplication; the chemistry is knowing which number is $M$ and which is $N_A$.",
            "Hydrates, gases, and solutions all still count moles. If a label says $0.250$ mol of glucose, that "
            "is $0.250\\times180.=45.0$ g, regardless of whether the glucose is dissolved or crystalline.",
            "On the AP exam, mole questions are rarely isolated. They open stoichiometry, gas-law, and titration "
            "items. If $n$ is wrong, every later step is wrong, so treat $n=m/M$ as a habit you check twice.",
        ],
        "Every later unit — gases, solutions, kinetics, equilibrium, acids — reports amounts in moles. "
        "Molar mass is how a laboratory balance talks to a balanced equation.",
        "Write the given mass and the molar mass, divide to get moles, then (only if asked) multiply by "
        "$6.022\\times10^{23}$. Keep three significant figures unless the problem is built on tidy numbers like $2.00$.",
        lesson_figure(
            beaker_svg("1.00 mol H₂O = 18.0 g"),
            "A mole is a counted pile, not a volume",
            "Eighteen grams of water is one mole of molecules, about $6.022\\times10^{23}$ H₂O particles.",
        )
        + solved(1, "How many moles are in $36.0$ g of H₂O ($18.0$ g/mol)?",
               ["Write $n=m/M$.",
                "Substitute: $n=36.0/18.0$.",
                "Divide: $n=2.00$ mol."],
               "$2.00$ mol", "", "Easy")
        + solved(2, "What mass of NaCl ($58.5$ g/mol) is $2.00$ mol?",
                 ["Write $m=nM$.",
                  "Substitute: $m=(2.00)(58.5)$.",
                  "Multiply: $m=117$ g."],
                 "$117$ g", "Do not divide when the prompt already gives moles and asks for grams.", "Medium")
        + solved(3, "A $45.0$ g sample of C₆H₁₂O₆ ($180.$ g/mol) is how many molecules?",
                 ["Convert to moles: $n=45.0/180.=0.250$ mol.",
                  "Convert moles to molecules: $N=nN_A=0.250\\times6.022\\times10^{23}$.",
                  "Compute: $N=1.506\\times10^{23}$ molecules.",
                  "The two-step chain is required; $45.0\\times N_A$ would be meaningless."],
                 "$1.51\\times10^{23}$ molecules",
                 "Molar mass of glucose: $6(12)+12(1)+6(16)=72+12+96=180$ g/mol.", "Hard"),
        ("Using $22.4$ L as if it were a mass",
         "STP molar volume ($22.4$ L/mol) applies to an ideal gas at $0^\\circ$C and $1$ atm, not to a pile of "
         "solid NaCl and not to a solution. For solids and liquids, grams and molar mass are the correct bridge."),
        ("Box the quantity you must cancel",
         "If the prompt gives grams and wants molecules, you must pass through moles. Write "
         "$\\mathrm{g}\\times(1\\ \\mathrm{mol}/M\\ \\mathrm{g})\\times N_A$ so the gram unit actually cancels."),
        [
            "I can convert grams to moles using $n=m/M$.",
            "I can convert moles to particles using Avogadro's number.",
            "I can explain a mole as a counting unit of $6.022\\times10^{23}$ particles.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Mass spectroscopy",
        [
            "A mass spectrometer ionizes atoms or molecules, then separates the ions by mass-to-charge ratio "
            "$m/z$. For singly charged atomic ions, the peak position is essentially the isotope mass number.",
            "Most elements are mixtures of isotopes — atoms with the same $Z$ but different numbers of neutrons. "
            "The atomic mass on the periodic table is a weighted average of those isotope masses, not the mass "
            "of a typical single atom.",
            "If chlorine is $75.0\\%$ ³⁵Cl and $25.0\\%$ ³⁷Cl, the average is "
            "$0.750(35)+0.250(37)=26.25+9.25=35.5$ amu. That $35.5$ is what you use in molar-mass arithmetic, "
            "even though no chlorine atom weighs $35.5$ amu.",
            "Peak height (or area) is proportional to how common that isotope is. A spectrum of neon with a tall "
            "peak at $20$ and a short peak at $22$ means ²⁰Ne is much more abundant than ²²Ne.",
            "Molecules show a molecular-ion peak and sometimes fragment peaks. Cl₂ can appear at $70$, $72$, and "
            "$74$ because two chlorine isotopes can pair in three ways. That pattern is evidence, not a mistake.",
            "On FRQs you may be asked to compute an average mass from a sketched spectrum or to justify why a "
            "compound containing Br or Cl shows a cluster of molecular-ion peaks.",
        ],
        "Mass spectra connect the particle picture (individual isotope masses) to the number you use in the "
        "mole formula. Without this idea, $35.5$ g/mol for Cl looks like a typo.",
        "Read each bar as “this many nucleons, this relative abundance.” Multiply mass × fractional abundance, "
        "then add. Percents must be converted to decimals first ($75\\% = 0.75$).",
        lesson_figure(
            _bars([(35, 3, "35"), (37, 1, "37")], xlab="m/z", ylab="intensity"),
            "Mass spectrum of atomic chlorine",
            "The 35 peak is about three times the 37 peak, matching a roughly 3:1 natural abundance.",
        )
        + solved(4, "Find the average atomic mass of Cl that is $75.0\\%$ ³⁵Cl and $25.0\\%$ ³⁷Cl.",
               ["Convert percents to fractions: $0.750$ and $0.250$.",
                "Weight the masses: $0.750(35)=26.25$ and $0.250(37)=9.25$.",
                "Add: $26.25+9.25=35.5$ amu."],
               "$35.5$ amu", "", "Easy")
        + solved(5, "Isotopes of mass $10.0$ ($80.0\\%$) and $11.0$ ($20.0\\%$). Average mass?",
                 ["$0.800(10.0)=8.00$.",
                  "$0.200(11.0)=2.20$.",
                  "Sum: $8.00+2.20=10.2$ amu."],
                 "$10.2$ amu", "A 1:4 peak-height ratio on a spectrum would tell the same story.", "Medium")
        + solved(6, "Mg is $79\\%$ ²⁴Mg, $10\\%$ ²⁵Mg, $11\\%$ ²⁶Mg. Compute the average atomic mass.",
                 ["$0.79(24)=18.96$.",
                  "$0.10(25)=2.50$.",
                  "$0.11(26)=2.86$.",
                  "Add: $18.96+2.50+2.86=24.32$ amu."],
                 "$24.32$ amu", "Check that the percents add to $100\\%$ before multiplying.", "Hard"),
        ("Averaging the mass numbers without weighting",
         "$(35+37)/2=36$ is not the atomic mass of chlorine, because the isotopes are not equally common. "
         "Always multiply by the fractional abundance."),
        ("Convert percent to a decimal before multiplying",
         "Using $75\\times35$ instead of $0.75\\times35$ inflates the answer by 100. Write $0.750$, not $75$, "
         "next to the mass."),
        [
            "I can compute a weighted-average atomic mass from isotope percents.",
            "I can read a mass spectrum's peak heights as relative abundances.",
            "I can explain Cl₂ or BrCl molecular-ion clusters using isotopes.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Electron configuration",
        [
            "An orbital is a region of space where an electron is likely to be found. Each orbital holds at most "
            "two electrons, and those two must have opposite spins (Pauli exclusion). The labels $1s$, $2s$, $2p$ "
            "name the shell ($n$) and the shape of the orbital set.",
            "The Aufbau order fills lower-energy orbitals first: $1s$, then $2s$, then $2p$, then $3s$, $3p$, "
            "$4s$, $3d$, and so on. Hund's rule says that degenerate orbitals (the three $2p$ orbitals) each get "
            "one electron before any pairing occurs.",
            "Oxygen ($Z=8$) is $1s^2 2s^2 2p^4$. The $2p$ subshell has four electrons: three orbitals, so two "
            "orbitals have one electron and one orbital has a pair. That is why O has two unpaired electrons and "
            "is paramagnetic.",
            "For ions, add electrons for anions and remove them for cations. Main-group atoms lose valence "
            "electrons from the highest $n$. Transition metals are the exception you must memorize: they lose "
            "$ns$ electrons before $(n-1)d$ electrons. Fe is $[Ar]\\,4s^2 3d^6$; Fe²⁺ is $[Ar]\\,3d^6$.",
            "Chromium and copper are famous exceptions: Cr is $4s^1 3d^5$ and Cu is $4s^1 3d^{10}$. Half-filled "
            "and filled $d$ sets are especially stable, so one $4s$ electron is “promoted.”",
            "Configurations connect directly to PES (peak counts) and to periodic trends (which electron is "
            "farthest out). If you cannot write the configuration, you cannot justify IE or radius on an FRQ.",
        ],
        "Electron configuration is the map of where the electrons actually sit. Periodic trends, PES, and "
        "ion charges are all configuration in disguise.",
        "Write $Z$, pour electrons into the Aufbau buckets, apply Hund in the last subshell, then for cations "
        "of transition metals strip $s$ before $d$.",
        lesson_figure(
            atom_shells_svg(protons=8, electrons=(2, 6)),
            "Oxygen: 8 protons, 8 electrons in two shells",
            "The inner shell holds 2 electrons (1s). The outer shell holds 6 (2s²2p⁴). This Bohr-like picture "
            "is a cartoon of the configuration, not a claim that orbits are circular tracks.",
        )
        + solved(7, "Write the ground-state configuration of O ($Z=8$).",
               ["Eight electrons to place.",
                "Fill $1s^2$ (2 e⁻) then $2s^2$ (2 e⁻); four remain.",
                "Place four in $2p$: $2p^4$.",
                "Result: $1s^2 2s^2 2p^4$."],
               "$1s^2 2s^2 2p^4$", "", "Easy")
        + solved(8, "Fe is $[Ar]\\,4s^2 3d^6$. Write Fe²⁺.",
                 ["Cations of transition metals lose $4s$ electrons first.",
                  "Remove two electrons from $4s$.",
                  "The $3d^6$ set remains: $[Ar]\\,3d^6$."],
                 "$[Ar]\\,3d^6$", "Fe³⁺ would be $[Ar]\\,3d^5$.", "Medium")
        + solved(9, "How many unpaired electrons does N ($1s^2 2s^2 2p^3$) have?",
                 ["The $1s$ and $2s$ electrons are paired.",
                  "Hund's rule puts one electron in each of the three $2p$ orbitals.",
                  "No pairing in $2p$, so there are three unpaired electrons.",
                  "That is why atomic nitrogen is paramagnetic."],
                 "3 unpaired", "Pairing would violate Hund for a $p^3$ configuration.", "Hard"),
        ("Removing $3d$ electrons before $4s$ from Fe",
         "Neutral Fe is written $4s^2 3d^6$ because $4s$ fills before $3d$ in Aufbau. Once the atom is ionized, "
         "the $4s$ electrons are the ones that leave. Fe²⁺ is not $[Ar]\\,4s^2 3d^4$."),
        ("Count $Z$ on your fingers before writing orbitals",
         "If the superscripts do not add to $Z$ (or to $Z$ minus charge for an ion), the configuration cannot "
         "be right. This ten-second check catches most configuration errors."),
        [
            "I can write ground-state configurations using Aufbau, Hund, and Pauli.",
            "I can write Fe²⁺ and Fe³⁺ by removing $4s$ then $3d$ electrons.",
            "I can count unpaired electrons in a $p$ or $d$ subshell.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Photoelectron spectroscopy",
        [
            "Photoelectron spectroscopy (PES) fires high-energy photons at atoms and measures how much energy "
            "is needed to eject each type of electron. That energy is the binding energy: the Coulomb attraction "
            "holding that electron to the nucleus, reported per mole of electrons.",
            "A PES spectrum is a plot of signal versus binding energy. AP plots usually put large binding energy "
            "on the left. Each peak is a subshell. Peak position tells how tightly those electrons are held; "
            "peak area (or height, when widths are similar) tells how many electrons live there.",
            "Neon is $1s^2 2s^2 2p^6$. You should see three peaks with relative areas $2:2:6$. The $1s$ peak is "
            "farthest left (highest BE). The $2p$ peak is tallest and at the lowest binding energy of the three.",
            "Comparing elements: the $1s$ peak of F is at higher BE than the $1s$ peak of O because F has a "
            "larger nuclear charge while the $1s$ radius stays tiny. Coulomb's law, not a new idea.",
            "Lithium shows two peaks (areas $2$ and $1$) because it is $1s^2 2s^1$. Beryllium's valence peak "
            "grows to area $2$ ($2s^2$). You can identify an unknown from the pattern of areas even without "
            "being told the element name.",
            "PES is how the exam asks Coulombic attraction without saying the words. If a prompt shows a spectrum "
            "and asks why a peak moved, answer with $Z_\\mathrm{eff}$ and $r$, not with a memorized slogan.",
        ],
        "PES is experimental evidence for shells and subshells. It is also the cleanest way the AP exam tests "
        "whether you understand that inner electrons are held more tightly.",
        "Match peak count to the number of occupied subshells, match areas to electron counts, and match "
        "left-versus-right to inner-versus-valence. Then justify shifts with Coulomb's law.",
        lesson_figure(
            _bars([(870, 2, "1s"), (48, 2, "2s"), (22, 6, "2p")], xlab="binding energy (decreasing →)", ylab="signal", x0=0, x1=920, decreasing=True),
            "PES cartoon for neon (high BE on the left)",
            "The 1s peak is farthest left: small area (2 e⁻) but much higher binding energy. The 2p peak is farthest right and tallest (6 e⁻).",
        )
        + solved(10, "Ne is $1s^2 2s^2 2p^6$. Relative PES peak areas?",
               ["Count electrons in each subshell: $2$, $2$, and $6$.",
                "Areas track those counts.",
                "Ratio $2:2:6$."],
               "$2:2:6$", "", "Easy")
        + solved(11, "Why is the F $1s$ peak at higher binding energy than the O $1s$ peak?",
                 ["Both $1s$ electrons sit at a similarly small radius.",
                  "F has $Z=9$ and O has $Z=8$, so F's nucleus pulls harder.",
                  "Larger $Z$ at similar $r$ means larger $F$ and larger BE.",
                  "Shielding of a $1s$ electron by the other $1s$ electron is similar in both atoms."],
                 "F $1s$ BE is larger because $Z$ is larger", "", "Medium")
        + solved(12, "A PES spectrum has two peaks with areas $2$ and $1$. Identify the element.",
                 ["Two occupied subshells: $1s$ and a valence $s$.",
                  "Area $2$ is $1s^2$; area $1$ is a single valence electron.",
                  "That configuration is $1s^2 2s^1$, which is lithium.",
                  "He would be a single peak of area $2$; Be would be $2$ and $2$."],
                 "Li", "Peak count plus area is enough to identify period-2 elements.", "Hard"),
        ("Reading the tallest peak as “highest energy electrons”",
         "Height is about how many electrons, not how energetic they are. The $2p$ peak of Ne is tall because "
         "there are six electrons, even though they are the easiest to remove."),
        ("Label each peak with a subshell before answering",
         "Write $1s$, $2s$, $2p$ under the bars. Then the question “which electrons are hardest to remove?” "
         "is just “which labeled peak is farthest left?”"),
        [
            "I can match PES peak areas to electron counts in subshells.",
            "I can identify inner versus valence peaks by binding energy.",
            "I can justify a BE shift using nuclear charge and radius.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Periodic trends",
        [
            "Atomic radius generally decreases from left to right across a period because electrons are added "
            "to the same shell while nuclear charge rises. The effective nuclear charge $Z_\\mathrm{eff}$ — the "
            "pull actually felt after shielding — goes up, so the cloud shrinks.",
            "Radius increases down a group because a new shell ($n$) is added. Even though $Z$ is larger, the "
            "outer electron is much farther away, and Coulomb's $1/r^2$ dependence wins.",
            "First ionization energy is the energy required to remove the most loosely held electron from a "
            "gaseous atom. IE generally increases across a period and decreases down a group — the reverse of "
            "radius — because a smaller, more tightly held electron is harder to steal.",
            "Two famous exceptions: Be > B and Mg > Al for first IE, because a $p$ electron is slightly higher "
            "in energy (and easier to remove) than a filled $s^2$ set; and N > O / P > S because pairing in "
            "$p^4$ raises electron–electron repulsion.",
            "Electronegativity is the ability of an atom in a bond to attract shared electrons. It rises toward "
            "fluorine. Electron affinity is the energy change when a gaseous atom gains an electron; it is more "
            "negative (more favorable) toward Cl/F, with noble gases near zero.",
            "Cations are smaller than their atoms; anions are larger. Isoelectronic ions (O²⁻, F⁻, Ne, Na⁺, "
            "Mg²⁺) shrink as $Z$ increases because the same 10 electrons feel a stronger pull.",
        ],
        "Trends let you predict size, IE, and bond polarity without memorizing every value. FRQs ask you to "
        "justify with $Z_\\mathrm{eff}$ and $r$, not to recite “increases to the right.”",
        "Always name the shell $n$ and whether $Z_\\mathrm{eff}$ rose. If two atoms share $n$, charge wins. If "
        "they differ in $n$, distance usually wins.",
        lesson_figure(
            _coulomb_pair(),
            "Why radius falls across a period",
            "Same shell, larger $Z_\\mathrm{eff}$, smaller $r$. Ionization energy then rises because that smaller "
            "cloud is harder to pull off.",
        )
        + solved(13, "Which is larger, Na or Cl? Justify with $n$ and $Z_\\mathrm{eff}$.",
               ["Both are in period 3, so $n=3$ for the valence shell.",
                "Cl has a larger nuclear charge and larger $Z_\\mathrm{eff}$.",
                "The stronger pull shrinks Cl, so Na is larger."],
               "Na is larger", "", "Easy")
        + solved(14, "Rank O²⁻, F⁻, Na⁺, Mg²⁺ from largest to smallest radius.",
                 ["All have 10 electrons (isoelectronic).",
                  "Proton counts: O 8, F 9, Na 11, Mg 12.",
                  "More protons at the same electron count means a stronger pull and a smaller ion.",
                  "Largest to smallest: O²⁻ > F⁻ > Na⁺ > Mg²⁺."],
                 "O²⁻ > F⁻ > Na⁺ > Mg²⁺", "", "Medium")
        + solved(15, "IE values jump from $1451$ to $7733$ kJ/mol after the second electron. What group?",
                 ["IE1 and IE2 are moderate, so two valence electrons come off reasonably.",
                  "IE3 is huge, so the third electron is a core electron.",
                  "Two valence electrons means group 2.",
                  "Group 1 would jump after IE1; group 13 would jump after IE3."],
                 "group 2", "Successive-IE tables are group identification problems.", "Hard"),
        ("Saying “Cl wants 8 electrons so it is smaller”",
         "Octet language does not explain size. Size is Coulomb's law: more $Z_\\mathrm{eff}$ at the same $n$ "
         "pulls the cloud in. Cl is smaller than Na for that reason, not because of a future ion charge."),
        ("Compare $n$ first, then $Z_\\mathrm{eff}$",
         "If you skip the shell check, you will claim F is larger than I because “nonmetals are small,” which "
         "fails down a group. Down a group, $n$ increases and radius increases."),
        [
            "I can justify radius and IE trends using $n$ and $Z_\\mathrm{eff}$.",
            "I can rank isoelectronic ions by nuclear charge.",
            "I can identify a group from a jump in successive ionization energies.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Coulombic attraction",
        [
            "Coulomb's law for two charges is $F=k\\dfrac{q_1 q_2}{r^2}$. In an atom, $q_1$ is the effective "
            "nuclear charge felt by an electron and $q_2$ is the electron's charge. Attraction is stronger when "
            "the nucleus looks more positive and when the electron is closer.",
            "This one equation is the engine under PES, IE, radius, and electronegativity. You do not need "
            "calculus — only the qualitative meaning of a larger numerator or a larger denominator.",
            "If $r$ doubles, $F$ becomes one-fourth as large. If $Z_\\mathrm{eff}$ doubles at constant $r$, $F$ "
            "doubles. Inner $1s$ electrons are held fiercely because $r$ is tiny; $1/r^2$ explodes as $r$ shrinks.",
            "Lithium versus cesium: both have $Z_\\mathrm{eff}\\approx 1$ for the valence electron, but Cs has "
            "that electron in $n=6$ rather than $n=2$. The much larger $r$ makes $F$ small, so Cs has a low IE "
            "and a large radius.",
            "Lithium versus fluorine: both valence shells are $n=2$, but F has a much larger $Z_\\mathrm{eff}$. "
            "The numerator grows, $r$ actually shrinks a bit, and F holds electrons tightly — high IE, high EN, "
            "high $1s$ BE.",
            "When an FRQ says “justify in terms of Coulombic attraction,” write a sentence that names charge and "
            "distance. “Fluorine wants an octet” is not Coulomb's law and will not earn the reasoning point.",
        ],
        "Coulomb's law is the single model that unifies Unit 1. If you can say whether $q$ or $r$ changed, you "
        "can answer almost any trend or PES shift.",
        "Write $F\\propto q_1 q_2/r^2$, circle what changed in the problem, and state whether $F$ increased or "
        "decreased. That sentence is the justification.",
        lesson_figure(
            atom_shells_svg(protons=3, electrons=(2, 1)),
            "Lithium: valence electron at larger $r$ than the 1s pair",
            "The 1s electrons sit close to +3 protons. The 2s electron is farther out and is shielded, so it "
            "feels roughly +1 and is much easier to remove.",
        )
        + solved(16, "If only the distance from nucleus to electron doubles, what happens to $F$?",
               ["Coulomb: $F\\propto 1/r^2$.",
                "New $r$ is $2r$, so $1/(2r)^2=1/4r^2$.",
                "$F$ becomes one-fourth as large."],
               "$F$ is $1/4$ as large", "", "Easy")
        + solved(17, "Nuclear charge doubles and distance also doubles. Ratio $F_\\mathrm{new}/F_\\mathrm{old}$?",
                 ["$F\\propto q/r^2$ for a single electron.",
                  "Numerator $\\times 2$; denominator $\\times 4$.",
                  "Ratio $=2/4=1/2$.",
                  "The force is half as large."],
                 "$1/2$", "Distance squared beats a single factor of charge.", "Medium")
        + solved(18, "Why is the first IE of Cs much smaller than that of Li, even though Cs has far more protons?",
                 ["Both valence electrons feel $Z_\\mathrm{eff}\\approx 1$ after inner-shell shielding.",
                  "The Cs electron is in a much higher shell, so $r$ is much larger.",
                  "$F\\propto 1/r^2$ therefore drops sharply.",
                  "A weaker attractive force means less energy is needed to remove the electron."],
                 "larger $r$ for Cs valence electron",
                 "More protons do not help if they are fully shielded by inner shells.", "Hard"),
        ("Claiming more protons always means higher IE",
         "That fails down a group. Cs has 55 protons and a tiny first IE because the valence electron is far "
         "away. Distance in the denominator can overpower a larger $Z$."),
        ("Name $q$ and $r$ in the sentence you write",
         "Graders look for Coulombic language: effective nuclear charge and distance. A sentence that only "
         "says “it is more reactive” does not earn the justification point."),
        [
            "I can apply $F\\propto q_1 q_2/r^2$ to a doubled distance or charge.",
            "I can contrast Li vs F (same $n$, different $Z_\\mathrm{eff}$) and Li vs Cs (different $n$).",
            "I can justify PES and IE using Coulombic attraction rather than slogans.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        ["Moles and molar mass", "Mass spectroscopy", "Electron configuration",
         "Photoelectron spectroscopy", "Periodic trends", "Coulombic attraction"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2
# ===========================================================================

def _u2_questions():
    return _qs([
        ("NaCl is best classified as:",
         "ionic, electron transfer from Na to Cl",
         "A metal and a nonmetal form ions held by Coulomb attraction.",
         ["covalent network", "metallic crystal of Cl", "H-bonded molecular solid"]),
        ("The bond in Cl₂ is:",
         "nonpolar covalent (electrons shared equally)",
         "Two identical atoms share a pair; ΔEN = 0.",
         ["ionic", "metallic", "hydrogen bonding"]),
        ("How many valence electrons are in a Lewis structure of CO₂?",
         "16", "C contributes 4, each O contributes 6: 4+12=16.", ["8", "12", "24"]),
        ("The formal charge on C in CO₂ (O=C=O) is:",
         "0", "FC = 4 − 0 − 8/2 = 0.", ["+2", "−2", "+4"]),
        ("A valid Lewis structure must generally give hydrogen how many electrons?",
         "2 (a duet)", "H has only a 1s orbital; it is satisfied with 2 electrons.",
         ["8", "6", "0"]),
        ("The electron-domain geometry of CH₄ is:",
         "tetrahedral", "Four bonding domains, no lone pairs.",
         ["square planar", "trigonal planar", "linear"]),
        ("The bond angle in BF₃ is closest to:",
         "120°", "Three domains, trigonal planar.", ["109.5°", "90°", "180°"]),
        ("H₂O has two bonds and two lone pairs. The molecular shape is:",
         "bent", "The four domains are tetrahedral, but the molecular shape names only atoms: bent.",
         ["linear", "tetrahedral", "trigonal planar"]),
        ("CO₂ is linear while SO₂ is bent. The difference is:",
         "S has a lone pair; C in CO₂ does not",
         "Two domains (CO₂) vs three domains (SO₂).",
         ["S is smaller than C", "CO₂ has ionic bonds", "SO₂ is a network solid"]),
        ("NH₃ bond angles are a bit less than 109.5° because:",
         "the lone pair takes more space than a bonding pair",
         "Lone-pair repulsion compresses H–N–H angles.",
         ["nitrogen has no valence electrons", "the molecule is linear", "H is more electronegative than N"]),
        ("Carbon in CH₄ is described as:",
         "sp³ hybridized", "Four electron domains → four sp³ orbitals.",
         ["sp", "sp²", "unhybridized 2p only"]),
        ("The carbon atoms in ethene C₂H₄ (three domains each) are:",
         "sp²", "Three domains: three sp² orbitals plus an unhybridized p for the π bond.",
         ["sp³", "sp", "dsp³"]),
        ("The C in CO₂ (two double bonds, linear) is:",
         "sp", "Two domains → sp hybrids; two p orbitals form the two π bonds.",
         ["sp³", "sp²", "sp³d"]),
        ("A σ bond is best described as:",
         "head-on overlap along the internuclear axis",
         "Every single bond is a σ bond; extra bonds in doubles/triples are π.",
         ["side-on overlap of p orbitals only", "a transfer of electrons", "an IMF"]),
        ("How many π bonds are in a C≡C triple bond?",
         "2", "One σ plus two π.", ["1", "3", "0"]),
        ("In HCl, the dipole arrow points toward:",
         "Cl", "Cl is more electronegative, so it is δ−.",
         ["H", "the midpoint with no direction", "neither atom"]),
        ("Which molecule is nonpolar even though it has polar bonds?",
         "CO₂", "Two equal C=O dipoles cancel in a linear molecule.",
         ["H₂O", "NH₃", "HCl"]),
        ("CCl₄ is nonpolar because:",
         "tetrahedral geometry cancels four identical C–Cl dipoles",
         "Vector sum of the bond dipoles is zero.",
         ["C–Cl bonds are nonpolar", "chlorine cannot form dipoles", "the molecule is bent"]),
        ("The most polar bond among C–H, N–H, O–H, F–H is:",
         "F–H", "Fluorine has the highest EN, so ΔEN is largest.",
         ["C–H", "N–H", "O–H"]),
        ("A molecule is polar if it has:",
         "polar bonds arranged so dipoles do not cancel",
         "Need both ΔEN > 0 and an asymmetric shape.",
         ["any lone pair on a distant atom in the sample", "only London forces", "identical atoms only"]),
        ("Ozone, O₃, is best described by:",
         "two resonance structures with identical O–O bonds in the hybrid",
         "The real molecule is an average; bonds are equal, not one single and one double.",
         ["one O=O and one O–O that never switch", "an ionic O²⁻ lattice", "a triple bond"]),
        ("Formal charge formula is:",
         "valence − nonbonding − ½(bonding)",
         "FC = V − N − B/2.",
         ["protons minus neutrons", "Z_eff − n", "bonds minus lone pairs only"]),
        ("In the best Lewis structure of NCO⁻, the formal charges should:",
         "be as close to zero as possible, with negative FC on the more EN atom",
         "That rule selects O as the δ− end rather than putting −1 on C.",
         ["all be +1", "ignore electronegativity", "put +1 on fluorine"]),
        ("SO₂ has two equivalent resonance forms. Each S–O bond order in the hybrid is:",
         "1.5", "Average of a single and a double bond.", ["1", "2", "3"]),
        ("A structure with FC = +2 on O and −1 on C is usually:",
         "worse than one with smaller formal charges",
         "Minimize formal charges; put negative FC on more electronegative atoms.",
         ["required by VSEPR", "proof of ionic bonding", "the only legal Lewis structure"]),
        ("Which solid contains a sea of delocalized valence electrons?",
         "Cu metal", "Metallic bonding.",
         ["NaCl", "ice", "CO₂(s)"]),
        ("The lattice of NaCl is held together by:",
         "Coulomb attraction between Na⁺ and Cl⁻",
         "Ionic bonding is not sharing; it is ion–ion attraction.",
         ["hydrogen bonds between Na and Cl", "London forces only", "covalent network bonds"]),
        ("Diamond is a:",
         "covalent network of sp³ carbon atoms",
         "Each C is tetrahedrally bonded to four others; melting point is extremely high.",
         ["molecular solid of C₄ units", "ionic crystal", "metal"]),
        ("The bond angle in BeCl₂ (two domains) is:",
         "180°", "Linear electron-domain geometry.", ["120°", "109.5°", "90°"]),
        ("PCl₅ has five domains. The electron-domain geometry is:",
         "trigonal bipyramidal", "Five domains around P.",
         ["octahedral", "tetrahedral", "square planar"]),
        ("How many lone pairs are on the central atom of NH₃?",
         "1", "N has 5 valence e⁻; three bonds use 3; one lone pair remains.",
         ["0", "2", "3"]),
        ("SF₆ has six bonding domains. Molecular shape?",
         "octahedral", "All six domains are bonds; 90° angles.",
         ["trigonal bipyramidal", "tetrahedral", "see-saw"]),
        ("The hybridization of O in H₂O (four domains) is:",
         "sp³", "Two bonds + two lone pairs = four sp³ orbitals.",
         ["sp", "sp²", "unhybridized"]),
        ("Which molecule has a net dipole?",
         "SO₂", "Bent, polar S–O bonds, dipoles do not cancel.",
         ["CO₂", "BF₃", "BeCl₂"]),
        ("In the Lewis structure of O₂, the bond is a:",
         "double bond (one σ and one π)",
         "Each O needs 8 e⁻; a double bond plus two lone pairs each works.",
         ["single bond", "triple bond", "ionic bond"]),
        ("XeF₄ has four bonds and two lone pairs. Molecular shape?",
         "square planar", "Octahedral domains with two opposite lone pairs.",
         ["tetrahedral", "see-saw", "linear"]),
        ("The carbon in HCN (H–C≡N) is:",
         "sp", "Two domains (H and N).",
         ["sp²", "sp³", "sp³d"]),
        ("A polar molecule that can hydrogen-bond with itself is:",
         "NH₃", "N–H bonds plus a lone pair on N.",
         ["CH₄", "CCl₄", "CO₂"]),
        ("Formal charge on N in NH₄⁺ (all N–H single bonds, no lone pair on N) is:",
         "+1", "FC = 5 − 0 − 8/2 = +1.", ["0", "−1", "+5"]),
        ("Resonance is required when:",
         "two or more valid Lewis structures differ only in electron placement",
         "The actual structure is a hybrid; electrons are delocalized.",
         ["the molecule is ionic", "VSEPR fails", "the atom lacks a nucleus"]),
        ("Which compound is most ionic in character?",
         "NaF", "Largest ΔEN among typical pairs listed: metal + fluorine.",
         ["CO", "Cl₂", "CH₄"]),
        ("The number of σ bonds in C₂H₄ is:",
         "5", "Four C–H σ plus one C–C σ; the extra C–C bond is π.",
         ["1", "6", "4"]),
        ("BF₃ is often drawn with B having an incomplete octet. That is accepted because:",
         "B is stable with 6 electrons in many compounds",
         "Period-2 boron is a known exception to the octet rule.",
         ["boron has 8 protons so it must have 8 electrons", "F cannot form bonds", "BF₃ is ionic NaCl-like"]),
        ("The molecular shape of PCl₃ (three bonds, one lone pair) is:",
         "trigonal pyramidal", "Like ammonia.",
         ["trigonal planar", "T-shaped", "linear"]),
        ("In a C=C double bond, rotation is restricted because:",
         "the π bond requires parallel p orbitals",
         "Twisting would break the side-on overlap.",
         ["the σ bond is ionic", "hydrogen bonding locks the atoms", "VSEPR forbids 120°"]),
        ("Which central atom can expand its octet?",
         "S in SF₆", "Period-3 and below can use d orbitals / extra domains.",
         ["F in HF", "O in H₂O", "N in NH₃"]),
        ("AP Stretch: Draw (in words) the best Lewis structure of NO₃⁻ and state the N–O bond order in the hybrid.",
         "4/3 (three equivalent resonance forms)",
         "Three forms each with two single and one double N–O; average bond order 4/3.",
         ["1", "2", "3"]),
        ("AP Stretch: Explain why NH₃ is polar but BF₃ is not, even though both have polar bonds.",
         "NH₃ is pyramidal (dipoles add); BF₃ is trigonal planar (dipoles cancel)",
         "Shape decides whether bond dipoles cancel.",
         ["N is less electronegative than B", "BF₃ has hydrogen bonds", "NH₃ is linear"]),
        ("AP Stretch: For SO₂, give the electron-domain geometry, molecular shape, and hybridization of S.",
         "trigonal planar domains, bent molecule, sp²",
         "Three domains (two bonds + one lone pair).",
         ["tetrahedral, bent, sp³", "linear, linear, sp", "octahedral, bent, sp³d²"]),
        ("AP Stretch: For NO₂⁻, assign formal charges on both oxygen atoms in one Lewis contributor, then give the N–O bond order in the resonance hybrid.",
         "double-bonded O is 0, single-bonded O is −1; hybrid N–O bond order = 3/2",
         "Two equivalent contributors. In one snapshot: double-bonded O has FC=0; single-bonded O has FC=−1; N is 0. Three bonding pairs shared over two N–O links → 3/2.",
         ["bond order 4/3 as in CO₃²⁻", "bond order 2 with FC=0 on both O", "bond order 1; FC=+1 on both O"]),
        ("AP Stretch: Assign formal charges in N≡C–O⁻ versus ⁻N=C=O and choose the better contributor.",
         "N≡C–O⁻ is better (negative FC on O)",
         "Both can have small FCs, but negative charge on the more electronegative O is preferred.",
         ["⁻N=C=O is better because N likes −1 more than O", "they are ionic crystals", "neither is valid"]),
        ("AP Stretch: Rank the N–N bond length in N₂, N₂H₂ (H–N=N–H), and N₂H₄. Support each rank with a bond order counted from Lewis (σ+π).",
         "N₂ shortest (BO 3), then N₂H₂ (BO 2), then N₂H₄ longest (BO 1)",
         "N₂ is N≡N (1 σ+2 π). N₂H₂ is N=N (1 σ+1 π). N₂H₄ is H₂N–NH₂ (1 σ). Higher bond order → shorter bond. Do not rank by molar mass.",
         ["N₂H₄ shortest because it has more atoms", "all three N–N lengths equal", "N₂ longest because it is a gas"]),
        ("AP Stretch: Count σ and π bonds in CH₃CN (acetonitrile, H₃C–C≡N).",
         "5 σ and 2 π",
         "Three C–H σ + one C–C σ + one C–N σ (the σ inside C≡N) = 5 σ. The triple bond also contributes 2 π. Counting the C–N σ twice is the 6 σ error.",
         ["6 σ and 2 π", "4 σ and 3 π", "5 σ and 1 π"]),
        ("AP Stretch: Explain why BeF₂ is linear and nonpolar while OF₂ is bent and polar.",
         "Be has two domains; O has four (two lone pairs)",
         "Different domain counts → different shapes → different dipole cancellation.",
         ["F is nonpolar in OF₂ only", "BeF₂ has hydrogen bonds", "OF₂ is ionic"]),
        ("AP Stretch: A molecule is AX₂E₂. Predict shape, hybridization, and whether it is polar if the outer atoms are identical.",
         "bent, sp³, polar",
         "Four domains like water; dipoles cannot cancel.",
         ["linear, sp, nonpolar", "tetrahedral, sp³, nonpolar", "square planar, sp³d², nonpolar"]),
    ])


def build_unit2():
    title = "AP Chemistry Unit 2: Molecular and Ionic Structure"
    description = (
        "Ionic versus covalent bonding, Lewis structures, VSEPR, hybridization, polarity, resonance, and "
        "formal charge with labeled molecule diagrams."
    )
    c1 = concept_block(
        "1. Ionic vs covalent bonding",
        [
            "Ionic bonding is the Coulomb attraction between cations and anions after electrons transfer, "
            "typically from a metal to a nonmetal. NaCl is a lattice of Na⁺ and Cl⁻, not a molecule of "
            "“Na–Cl.” The solid is held by $F\\propto q_1 q_2/r^2$ summed over the crystal.",
            "Covalent bonding is the sharing of electron pairs between nuclei, typically two nonmetals. The "
            "shared pair sits between the atoms and is attracted to both nuclei. Cl₂, CO₂, and H₂O are covalent.",
            "Electronegativity difference $\\Delta EN$ is a useful guide, not a law. Large $\\Delta EN$ (NaF) is "
            "ionic; zero $\\Delta EN$ (Cl₂) is nonpolar covalent; in-between (HCl) is polar covalent — unequal "
            "sharing, not full transfer.",
            "Metallic bonding is a third category: metal cations in a sea of delocalized valence electrons. "
            "That is why metals conduct and why Cu is not described with a Lewis octet diagram of Cu–Cu molecules.",
            "Network covalent solids (diamond, SiO₂, SiC) are giant lattices of covalent bonds. They are not "
            "ionic and not molecular. Their melting points are extremely high because you must break bonds, "
            "not just IMFs, to melt them.",
            "On the exam, classify first: ionic lattice, molecular covalent, network covalent, or metallic. "
            "The properties (melting point, conductivity, solubility) follow from that classification.",
        ],
        "Bond type decides whether you draw a Lewis molecule, a lattice of ions, or a network. Mixing those "
        "pictures is a common FRQ zero.",
        "Ask: metal + nonmetal → ionic; two nonmetals → covalent; elemental metal → metallic. Then check "
        "whether the covalent substance is molecular (CO₂) or network (diamond).",
        lesson_figure(
            _bond_types_svg(),
            "Three bonding pictures: lattice vs molecule vs metal",
            "NaCl is a 3-D ionic lattice, not an Na–Cl molecule. CO₂ is a discrete covalent molecule. Cu is "
            "cations in a delocalized electron sea. Precipitation of AgCl belongs in Unit 4, not here.",
        )
        + solved(1, "Classify NaCl, Cl₂, and Cu.",
               ["Na (metal) + Cl (nonmetal) → ionic lattice.",
                "Cl₂ is two identical nonmetals → nonpolar covalent molecule.",
                "Cu is an elemental metal → metallic bonding."],
               "ionic; covalent; metallic", "", "Easy")
        + solved(2, "Why does solid NaCl conduct only when molten or dissolved?",
                 ["In the solid, ions are locked in the lattice and cannot move.",
                  "Melting frees ions to migrate; dissolving does the same in water.",
                  "Electrical current in ionic materials is moving ions, not a sea of electrons.",
                  "Molecular covalent solids never conduct this way because they have no ions."],
                 "mobile ions are required", "", "Medium")
        + solved(3, "Diamond melts above $3500^\\circ$C; dry ice sublimes at $-78^\\circ$C. Explain with bond type.",
                 ["Diamond is a covalent network: each C is bonded to four others.",
                  "Melting diamond means breaking C–C bonds throughout the lattice.",
                  "Dry ice is molecular CO₂ held by weak IMFs, not by C–O bond breaking between molecules.",
                  "IMF disruption takes little energy compared with breaking a network of covalent bonds."],
                 "network bonds vs IMFs", "CO₂ molecules stay intact when dry ice sublimes.", "Hard"),
        ("Drawing NaCl as a molecule with a single Na–Cl bond",
         "The formula unit NaCl is not a molecule. The crystal is a 3-D stack of ions. Lewis structures are "
         "for covalent molecules and polyatomic ions, not for NaCl(s)."),
        ("Classify before drawing",
         "If you start a Lewis structure for NaCl, stop. If you start a lattice picture for CO₂, stop. The "
         "first sentence of an FRQ answer should name the bond type."),
        [
            "I can classify ionic, covalent, metallic, and network solids.",
            "I can relate conductivity of NaCl to mobile ions.",
            "I can contrast diamond with molecular CO₂ using bonds versus IMFs.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Lewis structures",
        [
            "A Lewis structure shows valence electrons as dots and bonding pairs as lines. Count valence "
            "electrons from the periodic group numbers: C has 4, N has 5, O has 6, F has 7, H has 1. Add one "
            "electron for each negative charge on an ion; subtract one for each positive charge.",
            "Hydrogen is content with a duet (2 electrons). Period-2 C, N, O, F generally complete an octet. "
            "Boron often has 6 electrons (BF₃). Period-3 atoms (P, S, Cl) can expand the octet (PCl₅, SF₆).",
            "CO₂ has $4+6+6=16$ valence electrons. The skeleton is O–C–O. Completing octets works with two "
            "double bonds: O=C=O. Each atom has 8 electrons, and the formal charges are all zero — a sign the "
            "structure is a good one.",
            "Formal charge is $\\mathrm{FC}=V-N-B/2$: valence electrons minus nonbonding electrons minus half "
            "the bonding electrons. Good structures minimize formal charges and put negative FC on the more "
            "electronegative atom.",
            "If two (or more) Lewis structures are equally reasonable and differ only in where a double bond "
            "sits, the molecule is described by resonance. You must draw the contributors; the real molecule "
            "is the hybrid, not one snapshot.",
            "Practice the count: NH₄⁺ has $5+4-1=8$ valence electrons and four N–H bonds, no lone pair on N. "
            "That is why N has FC $=+1$ and why ammonium is tetrahedral like methane.",
        ],
        "Lewis structures are the input to VSEPR, hybridization, polarity, and resonance. A wrong electron "
        "count makes every later prediction wrong.",
        "Total the valence electrons, draw the skeleton with the least electronegative atom in the center "
        "(H never central), place pairs to make octets/duets, then compute formal charges and adjust.",
        lesson_figure(
            _co2_lewis(),
            "Lewis structure of CO₂",
            "16 valence electrons, two double bonds, linear, formal charges of zero on each atom.",
        )
        + solved(4, "How many valence electrons are in the Lewis structure of CO₂?",
               ["C contributes 4; each O contributes 6.",
                "Total $4+12=16$.",
                "Those 16 electrons appear as two double bonds and two lone pairs on each O."],
               "16", "", "Easy")
        + solved(5, "Compute the formal charge on C in O=C=O.",
                 ["Carbon's valence number $V=4$.",
                  "Nonbonding electrons on C: $N=0$.",
                  "Bonding electrons: 8 (two double bonds), so $B/2=4$.",
                  "FC $=4-0-4=0$."],
                 "0", "", "Medium")
        + solved(6, "Valence electron count and FC on N in NH₄⁺.",
                 ["N has 5, four H have 4, minus 1 for the + charge: 8 electrons.",
                  "Four N–H single bonds use all 8 electrons; N has no lone pair.",
                  "FC on N $=5-0-8/2=+1$.",
                  "Each H has FC $=1-0-2/2=0$."],
                 "8 electrons; FC(N)=+1", "The +1 sits on nitrogen, matching the ion charge.", "Hard"),
        ("Forgetting to add or subtract electrons for the ion charge",
         "NO₃⁻ has $5+18+1=24$ electrons, not 23. Missing the extra electron produces the wrong number of "
         "bonds and the wrong formal charges."),
        ("Count electrons on paper before drawing any lines",
         "Circle the total. Every pair you draw spends 2 of that total. If you have electrons left over or "
         "run out too soon, the skeleton or the charge is wrong."),
        [
            "I can count valence electrons including ion charge.",
            "I can compute formal charge with $V-N-B/2$.",
            "I can build a valid Lewis structure for CO₂ and NH₄⁺.",
        ],
        6,
    )
    c3 = concept_block(
        "3. VSEPR and shape",
        [
            "VSEPR (valence shell electron-pair repulsion) says that electron domains — bonding pairs and lone "
            "pairs — spread out to minimize repulsion. The electron-domain geometry is the arrangement of those "
            "domains. The molecular shape names only the positions of the atoms.",
            "Two domains: linear, $180^\\circ$ (CO₂, BeCl₂). Three domains: trigonal planar, $120^\\circ$ (BF₃). "
            "Four domains: tetrahedral, $109.5^\\circ$ (CH₄). Five: trigonal bipyramidal. Six: octahedral.",
            "Water has four domains (two bonds, two lone pairs), so the electron-domain geometry is tetrahedral, "
            "but the molecular shape is bent. The H–O–H angle is a bit less than $109.5^\\circ$ because lone "
            "pairs take more space than bonding pairs.",
            "Ammonia is trigonal pyramidal (three bonds, one lone pair). BF₃ is trigonal planar with no lone "
            "pair, so $120^\\circ$. Do not call BF₃ “the same shape as ammonia.”",
            "SO₂ has three domains (two bonds, one lone pair): electron-domain geometry trigonal planar, "
            "molecular shape bent, angle near $120^\\circ$. CO₂ has two domains and is linear. Same “two outer "
            "oxygens,” completely different shapes, because the lone pair on S counts as a domain.",
            "Expanded octets: PCl₅ is trigonal bipyramidal; SF₆ is octahedral; XeF₄ is square planar (two lone "
            "pairs opposite each other). Learn the AXE patterns rather than inventing angles.",
        ],
        "Shape decides polarity, IMF type, and often boiling point. Lewis gives the domains; VSEPR turns "
        "domains into a 3-D name and an angle.",
        "Count domains around the central atom (lone pairs included). Name the domain geometry, then name the "
        "molecular shape from how many of those domains are atoms.",
        lesson_figure(
            _ch4_vsepr() + _bf3_vsepr(),
            "Four domains vs three domains",
            "CH₄ is tetrahedral (109.5°). BF₃ is trigonal planar (120°). Count domains; do not copy a memorized "
            "angle onto every molecule.",
        )
        + solved(7, "What is the molecular shape of CH₄?",
               ["Carbon has four bonding pairs and no lone pairs.",
                "Four domains → tetrahedral domain geometry.",
                "All four domains are atoms, so the molecular shape is tetrahedral."],
               "tetrahedral", "", "Easy")
        + solved(8, "Why is H₂O bent rather than linear or tetrahedral as a molecular shape?",
                 ["Oxygen has two bonds and two lone pairs: four domains.",
                  "Domain geometry is tetrahedral, not linear.",
                  "Molecular shape names atoms only: two atoms + two lone pairs = bent.",
                  "Calling water tetrahedral would pretend the lone pairs are atoms."],
                 "bent (four domains, two lone pairs)", "", "Medium")
        + solved(9, "Predict electron-domain geometry and molecular shape of SO₂.",
                 ["Lewis: S has a double-bond-ish connection to each O plus a lone pair (resonance).",
                  "Three domains around S.",
                  "Three domains → trigonal planar electron-domain geometry.",
                  "One domain is a lone pair, so the molecular shape is bent."],
                 "trigonal planar domains; bent molecule",
                 "This is why SO₂ is polar and CO₂ is not.", "Hard"),
        ("Using the molecular formula to guess linear",
         "H₂O and CO₂ both look like “central atom plus two outer atoms.” Only the domain count distinguishes "
         "them. Always draw Lewis first."),
        ("Write domain count, then two names",
         "On an FRQ: “four domains, tetrahedral electron geometry, bent molecular shape, angle $<109.5^\\circ$.” "
         "That sequence earns the points in order."),
        [
            "I can count electron domains including lone pairs.",
            "I can name domain geometry and molecular shape separately.",
            "I can contrast CO₂ (linear) with SO₂ or H₂O (bent).",
        ],
        11,
    )
    c4 = concept_block(
        "4. Hybridization intro",
        [
            "Hybridization is a model that mixes atomic orbitals on the central atom to make new orbitals that "
            "point toward the VSEPR domains. You do not need the calculus of orbital math — you need a count: "
            "the number of hybrid orbitals equals the number of electron domains.",
            "Four domains → $sp^3$ (CH₄, NH₃, H₂O), tetrahedral arrangement of hybrids. Three domains → $sp^2$ "
            "(BF₃, C in C₂H₄, S in SO₂). Two domains → $sp$ (BeCl₂, C in CO₂, C in HCN).",
            "In ethene, each carbon has three domains, so $sp^2$. The three $sp^2$ orbitals make the three $\\sigma$ "
            "bonds. The leftover unhybridized $p$ orbital on each carbon overlaps side-on to make the $\\pi$ bond. "
            "A double bond is always one $\\sigma$ plus one $\\pi$.",
            "A triple bond is one $\\sigma$ plus two $\\pi$. The carbon in acetylene is $sp$ (two domains). Two $p$ "
            "orbitals remain to form the two $\\pi$ bonds of C≡C.",
            "Expanded-octet shapes use $sp^3d$ (trigonal bipyramidal) and $sp^3d^2$ (octahedral) in the AP "
            "hybridization language. SF₆ is $sp^3d^2$. XeF₄ (square planar) is also $sp^3d^2$ because there are "
            "six domains counting the two lone pairs.",
            "Hybridization does not replace VSEPR; it is the orbital story that matches the domain count you "
            "already found. If the domain count is wrong, the hybrid label is wrong.",
        ],
        "Hybrid labels ($sp$, $sp^2$, $sp^3$) appear on multiple-choice items and as quick FRQ fill-ins. They "
        "also explain why a double bond cannot freely rotate ($\\pi$ overlap).",
        "Count domains around the atom in question. 2 → $sp$, 3 → $sp^2$, 4 → $sp^3$. Then assign leftover $p$ "
        "orbitals to $\\pi$ bonds.",
        lesson_figure(
            _hybrid_sp3(),
            "Four $sp^3$ hybrids around carbon in methane",
            "Each hybrid points at a hydrogen. The 109.5° angle is the VSEPR tetrahedron expressed in orbitals.",
        )
        + solved(10, "What is the hybridization of C in CH₄?",
               ["Four bonding domains, no lone pairs.",
                "Four domains require four hybrids.",
                "Four hybrids from $s+p+p+p$ is $sp^3$."],
               "$sp^3$", "", "Easy")
        + solved(11, "Hybridization of each C in C₂H₄, and how many $\\pi$ bonds are in the molecule?",
                 ["Each C is bonded to two H and one C: three domains.",
                  "Three domains → $sp^2$.",
                  "The extra C–C connection is a $\\pi$ bond from leftover $p$ orbitals.",
                  "The molecule has one $\\pi$ bond (and five $\\sigma$ bonds)."],
                 "$sp^2$; one $\\pi$ bond", "", "Medium")
        + solved(12, "For CO₂, give the hybridization of C and the number of $\\pi$ bonds.",
                 ["Carbon has two domains (two double-bonded oxygens): linear.",
                  "Two domains → $sp$.",
                  "Each C=O double bond contains one $\\pi$; there are two double bonds.",
                  "Two $\\pi$ bonds, plus two $\\sigma$ bonds from C to the oxygens."],
                 "$sp$; two $\\pi$ bonds", "The two $\\pi$ bonds are perpendicular to each other.", "Hard"),
        ("Matching hybridization to the number of atoms instead of domains",
         "Water has two atoms attached but four domains, so O is $sp^3$, not $sp$. Lone pairs count."),
        ("Count domains on the atom the question names",
         "In CH₃CN the two carbons are different: the methyl carbon is $sp^3$ (four domains) and the cyanide "
         "carbon is $sp$ (two domains). Read which carbon is asked."),
        [
            "I can assign $sp$, $sp^2$, or $sp^3$ from domain count.",
            "I can state that a double bond is one $\\sigma$ plus one $\\pi$.",
            "I can explain restricted rotation using $\\pi$ overlap.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Bond polarity",
        [
            "A bond is polar when two atoms share electrons unequally. The more electronegative atom gets a "
            "partial negative charge $\\delta-$ and the other is $\\delta+$. The dipole arrow points toward the "
            "more electronegative atom (the $\\delta-$ end).",
            "H–Cl is polar: Cl is $\\delta-$. C–H is only slightly polar and is often treated as nearly nonpolar "
            "in AP arguments. F–H is the most polar single bond among the common examples because F has the "
            "highest electronegativity.",
            "A molecule can have polar bonds and still be nonpolar overall if the bond dipoles cancel as vectors. "
            "CO₂ is linear: two equal C=O dipoles point opposite ways and cancel. CCl₄ is tetrahedral: four equal "
            "C–Cl dipoles cancel. BF₃ is trigonal planar and nonpolar for the same reason.",
            "Water is bent, so the two O–H dipoles add toward the lone-pair side: water is polar. Ammonia is "
            "pyramidal and polar. SO₂ is bent and polar. Shape is not optional when you judge polarity.",
            "Polar molecules have dipole–dipole IMFs (and hydrogen bonding if H is on N, O, or F). That is why "
            "H₂O boils so much higher than CO₂ even though CO₂ is heavier. Bond polarity plus shape plus IMF is "
            "one story, not three separate chapters.",
            "On FRQs, say: (1) bonds polar because $\\Delta EN>0$, (2) molecular shape from VSEPR, (3) dipoles "
            "cancel or do not. Skipping step 2 is how students call CO₂ polar.",
        ],
        "Polarity controls IMFs, solubility (“like dissolves like”), and boiling points in Unit 3. Getting "
        "CO₂ wrong here will cost you chromatography and vapor-pressure items later.",
        "Draw the shape, draw dipole arrows on each polar bond, then ask whether the arrows cancel. If they "
        "do not, the molecule is polar.",
        lesson_figure(
            _polar_hcl() + _co2_lewis(),
            "A polar bond (HCl) versus a nonpolar molecule with polar bonds (CO₂)",
            "HCl has one dipole. CO₂ has two opposite dipoles that cancel, so the molecule's net dipole is zero.",
        )
        + solved(13, "In HCl, toward which atom does the dipole arrow point?",
               ["Cl is more electronegative than H.",
                "Cl is $\\delta-$ and H is $\\delta+$.",
                "The arrow points toward Cl."],
               "toward Cl", "", "Easy")
        + solved(14, "Why is CO₂ nonpolar while H₂O is polar?",
                 ["Both have polar bonds (C=O and O–H).",
                  "CO₂ is linear, so the two dipoles are equal and opposite and cancel.",
                  "H₂O is bent, so the two O–H dipoles add and do not cancel.",
                  "Net dipole: CO₂ zero; H₂O nonzero."],
                 "shape: linear cancel vs bent add", "", "Medium")
        + solved(15, "Is CCl₄ polar? Justify with geometry.",
                 ["C–Cl bonds are polar ($\\Delta EN>0$).",
                  "Four identical bonds in a tetrahedron.",
                  "The four dipole vectors sum to zero.",
                  "The molecule is nonpolar despite polar bonds."],
                 "nonpolar", "CHCl₃ would be polar because the bonds are not identical.", "Hard"),
        ("Calling any molecule with oxygen polar",
         "CO₂ and O₂ have oxygen and are nonpolar. Polarity is about the vector sum, not about whether oxygen "
         "is present."),
        ("Sketch dipoles on the VSEPR shape",
         "A 10-second drawing of arrows on CO₂ versus H₂O prevents the most common polarity mistake on the exam."),
        [
            "I can assign $\\delta+$ and $\\delta-$ using electronegativity.",
            "I can decide molecular polarity from shape plus bond dipoles.",
            "I can explain why CO₂ and CCl₄ are nonpolar.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Resonance and formal charge",
        [
            "Resonance is required when two or more valid Lewis structures differ only in the placement of "
            "electrons, not in the placement of atoms. Ozone, nitrate, carbonate, and benzene are classic "
            "cases. The real molecule is a hybrid: the electrons are delocalized.",
            "Ozone can be drawn O=O⁺–O⁻ or ⁻O–O⁺=O. Neither picture is the molecule. Each O–O connection in "
            "the hybrid is identical, with bond order $1.5$. You should not say “one single bond and one double "
            "bond that switch back and forth.”",
            "Bond order in a resonance hybrid is (number of bonding pairs in that set of links) divided by "
            "(number of links). For CO₃²⁻ there are four C–O bonding pairs spread over three links, so bond "
            "order is $4/3$. For NO₃⁻ the N–O bond order is also $4/3$.",
            "Formal charge helps you choose among Lewis structures that are not equivalent. Minimize the "
            "absolute values of formal charges, and if a $-1$ must exist, place it on the more electronegative "
            "atom. That is why N≡C–O⁻ is a better contributor than ⁻N=C=O for cyanate.",
            "A structure with FC $=+2$ on oxygen is almost never preferred if an alternative with zeros and a "
            "single $-1$ on oxygen exists. Formal charge is a bookkeeping tool, not a real extra proton.",
            "Resonance energy / delocalization makes the hybrid more stable than any one contributor. That is "
            "why the two O–O bonds in ozone are equal in length, and why nitrate does not have one short and "
            "two long N–O bonds.",
        ],
        "Resonance and formal charge show up on nearly every AP bonding FRQ. Bond order of $4/3$ and “identical "
        "bonds in the hybrid” are high-value sentences.",
        "Draw all major contributors, compute FC on each atom, average the bond orders, and state that the "
        "real molecule is the hybrid with equal bonds.",
        lesson_figure(
            _ozone_res() + _so2_bent(),
            "Resonance in ozone (and the bent shape of SO₂)",
            "Two contributors, one hybrid. SO₂ is also a resonance species and is bent because of the lone pair on S.",
        )
        + solved(16, "Ozone has two major resonance structures. What is each O–O bond order in the hybrid?",
               ["One contributor has a double bond and a single bond.",
                "The other contributor swaps which link is double.",
                "Average bond order $=(2+1)/2=1.5$."],
               "1.5", "", "Easy")
        + solved(17, "Formal charge on N in NH₄⁺ with four N–H bonds and no lone pair on N?",
                 ["$V=5$, $N=0$, $B=8$.",
                  "FC $=5-0-4=+1$.",
                  "The ion charge is $+1$, matching the FC on nitrogen.",
                  "Hydrogen FCs are zero."],
                 "+1", "", "Medium")
        + solved(18, "In CO₃²⁻, what is the C–O bond order in the resonance hybrid?",
                 ["Carbonate has three equivalent contributors.",
                  "Total of four C–O bonding pairs (one double and two singles in any snapshot).",
                  "Those four pairs are shared among three C–O links.",
                  "Bond order $=4/3$."],
                 "$4/3$", "All three C–O lengths are equal in the real ion.", "Hard"),
        ("Saying the bonds “resonate back and forth” as if the molecule flipped 10¹⁵ times a second",
         "The hybrid is the actual structure. Electrons are delocalized. There are not two species rapidly "
         "interconverting in ozone at equilibrium in that cartoon sense."),
        ("Compute bond order as total bonding pairs over number of links",
         "Write the fraction. $4/3$ is a better FRQ answer than “a little more than one” because it shows you "
         "counted."),
        [
            "I can describe a resonance hybrid as the real structure with equal bonds.",
            "I can compute bond order for ozone ($1.5$) and carbonate ($4/3$).",
            "I can use formal charge to choose a better Lewis contributor.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        ["Ionic vs covalent bonding", "Lewis structures", "VSEPR and shape",
         "Hybridization intro", "Bond polarity", "Resonance and formal charge"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3
# ===========================================================================

def _u3_questions():
    return _qs([
        ("The strongest IMF in a sample of pure H₂O(l) is:",
         "hydrogen bonding",
         "H is bound to O, and O has lone pairs.",
         ["only London forces", "ionic bonds between molecules", "metallic bonds"]),
        ("Which substance has only London dispersion forces between molecules?",
         "CH₄", "Nonpolar molecule; no H–N/O/F.",
         ["H₂O", "NH₃", "HF"]),
        ("Boiling point of F₂ vs I₂: I₂ is higher mainly because:",
         "I₂ is larger/more polarizable, so stronger London forces",
         "Both are nonpolar; dispersion grows with electron cloud size.",
         ["I₂ is ionic", "F₂ has hydrogen bonds", "I₂ has a smaller molar mass"]),
        ("Hydrogen bonding requires H attached to:",
         "N, O, or F", "The H must be highly δ+ and find a lone pair on N, O, or F.",
         ["C, Si, or Ge", "any halogen including I", "a metal"]),
        ("Dipole–dipole forces are significant in:",
         "HCl(l)", "Polar molecules with a permanent dipole.",
         ["Cl₂(l)", "CH₄(l)", "He(l)"]),
        ("In a particulate drawing of a gas vs a solid of the same substance, gas particles are:",
         "far apart and disordered, solid particles close and ordered",
         "Phase is about spacing and order, not about changing the molecule's formula.",
         ["larger atoms", "always ionized", "locked in a crystal of new compounds"]),
        ("Which change is endothermic?",
         "liquid → gas (vaporization)",
         "You must put in energy to separate particles against IMFs.",
         ["gas → liquid", "liquid → solid", "deposition"]),
        ("A molecular solid is held together by IMFs, while a covalent network is held by:",
         "covalent bonds throughout the lattice",
         "Diamond vs dry ice.",
         ["only London forces", "metallic electrons only", "hydrogen bonds only"]),
        ("At the same T, the average kinetic energy of He(g) and Xe(g) is:",
         "the same, because KE_avg depends only on T",
         "KMT: $K_\\mathrm{avg}=(3/2)RT$ per mole, independent of molar mass.",
         ["larger for Xe because it is heavier", "larger for He because it is faster", "zero for both"]),
        ("When a molecular solid melts, the species that stay intact are:",
         "the molecules", "Melting disrupts IMFs, not intramolecular bonds.",
         ["individual atoms from every bond", "a plasma of nuclei", "ions only"]),
        ("Ideal gas law is $PV=nRT$. For $n=1.00$ mol, $T=273$ K, $P=1.00$ atm, $R=0.0821$, $V$ is closest to:",
         "22.4 L", "(1.00)(0.0821)(273)=22.4 L.", ["1.00 L", "0.0821 L", "273 L"]),
        ("$n=0.500$ mol, $T=300$ K, $V=10.0$ L, $R=0.0821$. Pressure?",
         "1.23 atm", "P=nRT/V=(0.500)(0.0821)(300)/10.0=1.2315 atm.",
         ["12.3 atm", "0.123 atm", "2.46 atm"]),
        ("$P=3.00$ atm, $V=8.21$ L, $T=300$ K, $R=0.0821$. Moles of gas?",
         "1.00 mol", "n=PV/RT=24.63/24.63=1.00.", ["3.00 mol", "8.21 mol", "0.333 mol"]),
        ("If T (Kelvin) doubles at constant n and P, volume:",
         "doubles", "Charles's law: V∝T at constant P,n.",
         ["halves", "is unchanged", "squares"]),
        ("A 2.00 L flask of He at 1.00 atm and 300 K is compared with 2.00 L of O₂ at the same T and P. The flasks contain:",
         "equal moles of gas", "Avogadro: equal V, T, P → equal n.",
         ["more moles of O₂ because it is heavier", "more moles of He", "zero moles of He"]),
        ("According to KMT, gas pressure arises from:",
         "collisions of particles with the container walls",
         "More frequent or more forceful collisions raise P.",
         ["IMFs pulling the walls inward", "electrons leaving the atoms", "gravity on each molecule"]),
        ("At the same T, lighter gas particles move:",
         "faster on average", "Same KE_avg; KE=½mv² so smaller m means larger v_rms.",
         ["slower", "at identical speed to heavy particles", "only in straight lines with no speed"]),
        ("Ideal gas assumptions include:",
         "particles have negligible volume and negligible IMFs",
         "Real gases deviate at high P / low T when those assumptions fail.",
         ["particles attract strongly at all T", "particles have most of the container's volume", "collisions are inelastic always"]),
        ("Raising T at constant V and n increases P because:",
         "particles hit the walls harder and more often",
         "KE_avg rises with T.",
         ["the container shrinks", "moles increase", "R decreases"]),
        ("A Maxwell–Boltzmann distribution at higher T is:",
         "shifted to higher speeds with a lower peak",
         "More particles in the high-speed tail.",
         ["a single spike at v=0", "narrower and taller at the same most-probable speed", "unchanged"]),
        ("Molarity is:",
         "moles of solute per liter of solution",
         "M = n/V with V in liters of solution, not of solvent alone.",
         ["moles of solvent per liter of solute", "grams per milliliter of water", "mole fraction of water"]),
        ("0.500 mol of NaCl in 0.250 L of solution has molarity:",
         "2.00 M", "M=0.500/0.250=2.00.", ["0.125 M", "0.500 M", "4.00 M"]),
        ("5.85 g NaCl (58.5 g/mol) dissolved to 0.500 L. Molarity?",
         "0.200 M", "n=5.85/58.5=0.100 mol; M=0.100/0.500=0.200.",
         ["11.7 M", "1.00 M", "0.100 M"]),
        ("25.0 mL of 2.00 M HCl is diluted to 100.0 mL. New molarity?",
         "0.500 M", "M1V1=M2V2 → (2.00)(25.0)=(M2)(100.0) → M2=0.500.",
         ["8.00 M", "2.00 M", "0.250 M"]),
        ("A beaker of 1.0 M glucose vs 1.0 M NaCl: the NaCl solution has:",
         "more dissolved particles per liter (van't Hoff)",
         "NaCl produces Na⁺ and Cl⁻; glucose stays molecular.",
         ["fewer particles", "identical particle counts", "only solvent particles"]),
        ("In paper chromatography, the solvent front is 8.0 cm and a spot moved 4.0 cm. Rf is:",
         "0.50", "Rf = distance spot / distance solvent = 4.0/8.0=0.50.",
         ["2.0", "32", "0.00"]),
        ("A polar dye sticks to polar paper and has a small Rf in a nonpolar solvent because:",
         "it prefers the stationary phase over the mobile phase",
         "Like dissolves like: polar analyte + polar paper.",
         ["it has no mass", "Rf is always 1 for polar dyes", "paper chromatography requires ions"]),
        ("UV-vis absorbance of a colored solution is useful because absorbance is proportional to:",
         "concentration (Beer's law, A=εbc)",
         "A calibration curve of A vs c is linear in the dilute range.",
         ["the container's mass", "temperature only", "the nuclear charge of the solvent"]),
        ("IR spectroscopy is used mainly to:",
         "identify functional groups by bond vibrations",
         "Different bonds absorb different infrared frequencies.",
         ["count neutrons", "measure pH", "find the boiling point directly"]),
        ("In a mass spectrum of a molecular sample, the molecular-ion peak gives:",
         "the molar mass of the intact ionized molecule",
         "m/z of M⁺· is the molecular mass for z=1.",
         ["the melting point", "the pH", "the number of lone pairs"]),
        ("Which IMF ranking for boiling point is correct (similar size otherwise)?",
         "H-bonding > dipole–dipole > dispersion (for small molecules)",
         "Water vs H₂S vs CH₄ as a teaching comparison.",
         ["dispersion always beats H-bonding", "ionic IMFs in CH₄", "all IMFs equal"]),
        ("A sample of 2.00 mol O₂ occupies 44.8 L at STP (0°C, 1 atm). This matches:",
         "22.4 L/mol × 2.00 mol", "Molar volume at STP times moles.",
         ["O₂ being twice as heavy as N₂", "a van der Waals correction of 44.8", "molarity 2.00 M"]),
        ("If n and T are constant and P is tripled, V becomes:",
         "1/3 as large", "Boyle: PV constant.",
         ["3 times as large", "9 times", "unchanged"]),
        ("Real gases deviate most from ideal at:",
         "high P and low T", "Volume of particles and IMFs become important.",
         ["low P and high T", "in a vacuum with one particle", "only if the gas is monatomic"]),
        ("0.200 mol of KCl in 0.100 L of solution is:",
         "2.00 M", "M=0.200/0.100=2.00.", ["0.0200 M", "0.300 M", "20.0 M"]),
        ("A nonpolar pigment travels farther on TLC with a nonpolar solvent. Rf is:",
         "larger than that of a polar pigment",
         "Nonpolar analyte prefers the nonpolar mobile phase.",
         ["always 0", "undefined", "smaller than polar pigments always"]),
        ("The average KE of gas molecules depends on:",
         "temperature only (for an ideal gas)",
         "Not on P, V, or identity at a given T.",
         ["molar mass only", "color", "the container material"]),
        ("Mixing 50.0 mL of 1.00 M NaCl with 50.0 mL of water (assume additive volumes) gives:",
         "0.500 M", "n=0.0500 mol; V=0.100 L; M=0.500.",
         ["1.00 M", "2.00 M", "0.0500 M"]),
        ("Which particulate picture matches a liquid?",
         "particles touching, disordered, not filling the container as a gas would",
         "Liquids have definite volume, indefinite shape.",
         ["a rigid lattice", "particles at huge separations", "a single molecule"]),
        ("Beer's law: if path length doubles and concentration is unchanged, absorbance:",
         "doubles", "A=εbc, linear in b.",
         ["halves", "is squared", "is unchanged"]),
        ("NH₃ has a higher boiling point than PH₃ primarily because:",
         "NH₃ hydrogen-bonds; PH₃ does not (H not on N/O/F in the same way / P less EN)",
         "N–H is the classic H-bond case; P–H is a poor H-bond donor.",
         ["PH₃ is ionic", "NH₃ is heavier", "PH₃ has more electrons so stronger H-bonds"]),
        ("A 0.250 L solution contains 10.0 g of NaOH (40.0 g/mol). Molarity?",
         "1.00 M", "n=10.0/40.0=0.250 mol; M=0.250/0.250=1.00.",
         ["0.250 M", "4.00 M", "10.0 M"]),
        ("At constant T, v_rms of He vs CH₄ (16 g/mol): He (4 g/mol) is faster by a factor of:",
         "2", "v_rms ∝ 1/√M; √(16/4)=2.",
         ["4", "16", "1"]),
        ("Chromatography separates components because they:",
         "partition differently between mobile and stationary phases",
         "Different IMFs → different Rf values.",
         ["have different nuclear charges only", "all have Rf=1", "are all gases"]),
        ("If 1.00 mol of gas at 2.00 atm occupies 10.0 L, T with R=0.0821 is closest to:",
         "243 K", "T=PV/nR=20.0/0.0821≈243.6 K.",
         ["24.3 K", "486 K", "82 K"]),
        ("A solution labeled 0.10 M K₂SO₄ contains [K⁺] equal to:",
         "0.20 M", "Each formula unit yields 2 K⁺.",
         ["0.10 M", "0.05 M", "0.30 M"]),
        ("AP Stretch: 0.400 mol of N₂ in 5.00 L at 400 K (R=0.0821). Find P, then the new P if T falls to 200 K at constant V.",
         "2.63 atm then 1.31 atm",
         "P=nRT/V: (0.400)(0.0821)(400)/5.00=13.136/5.00=2.627 atm, which rounds to 2.63 atm. Halving T at constant n,V halves P: 2.627/2=1.314 atm, which rounds to 1.31 atm.",
         ["2.63 atm then 5.26 atm", "0.658 atm then 0.329 atm", "13.1 atm then 6.57 atm"]),
        ("AP Stretch: Explain why I₂(s) sublimes more readily than NaCl(s) at similar T, using IMFs vs ionic bonds.",
         "I₂ is a molecular solid with weak London forces; NaCl is an ionic lattice",
         "Separating I₂ molecules costs little energy compared with separating Na⁺ and Cl⁻.",
         ["I₂ has stronger bonds than NaCl", "NaCl is a gas", "I₂ is a network covalent solid"]),
        ("AP Stretch: A student dilutes 20.0 mL of 6.00 M HCl to 250.0 mL. Moles of HCl and final molarity?",
         "0.120 mol and 0.480 M",
         "n=(6.00)(0.0200)=0.120 mol; M=0.120/0.250=0.480.",
         ["6.00 mol and 0.480 M", "0.120 mol and 6.00 M", "1.50 mol and 0.0200 M"]),
        ("AP Stretch: Two balloons hold equal moles of He and CO₂ at the same T. Compare v_rms and KE_avg.",
         "KE_avg equal; He has larger v_rms",
         "KE_avg depends only on T; v_rms is larger for smaller M.",
         ["He has larger KE_avg", "CO₂ is faster", "both speeds and KE match exactly"]),
        ("AP Stretch: A TLC plate: solvent front 10.0 cm; spots at 2.0, 5.0, and 9.0 cm. Rf values, and which is least polar if the solvent is nonpolar?",
         "0.20, 0.50, 0.90; the 0.90 spot is least polar",
         "Rf=d_spot/d_front. Largest Rf travels with nonpolar solvent → least polar analyte.",
         ["2, 5, 9; the 0.20 spot is least polar", "0.80, 0.50, 0.10; 0.20 is least polar", "all Rf=1"]),
        ("AP Stretch: 3.00 g of an unknown gas occupies 1.68 L at STP. Molar mass? (22.4 L/mol at STP)",
         "40.0 g/mol", "n=1.68/22.4=0.0750 mol; M=3.00/0.0750=40.0 g/mol (like Ar).",
         ["22.4 g/mol", "3.00 g/mol", "80.0 g/mol"]),
        ("AP Stretch: Why does a 1.0 M solution of CaCl₂ have a greater particle concentration than 1.0 M glucose?",
         "CaCl₂ → 3 ions per formula unit; glucose stays one molecule",
         "van't Hoff factor i≈3 vs i=1.",
         ["CaCl₂ has a smaller molar mass so more moles", "glucose ionizes into 6 carbons", "both have identical particle counts"]),
        ("AP Stretch: A rigid flask of N₂ has its amount of gas doubled and its kelvin temperature halved. Using KMT, what happens to P, and what happens to average KE per molecule?",
         "P is unchanged; average KE is halved",
         "P∝nT at constant V: n×2 and T×½ cancel, so P stays the same. Average KE depends only on T, so KE_avg is cut in half. Collision frequency rises with n but each impact is weaker.",
         ["P doubles; KE_avg doubles", "P is unchanged; KE_avg unchanged because P did not change", "P halves; KE_avg doubles"]),
        ("AP Stretch: 40.0 g of NaOH (40.0 g/mol) is dissolved and diluted to 2.00 L. Then 25.0 mL of that solution is diluted to 100.0 mL. Final [NaOH]?",
         "0.125 M",
         "Stock: n=1.00 mol in 2.00 L → 0.500 M. Dilution: (0.500)(25.0)=(M2)(100.0) → M2=0.125.",
         ["0.500 M", "1.00 M", "0.0250 M"]),
    ])


def build_unit3():
    title = "AP Chemistry Unit 3: Intermolecular Forces and Properties"
    description = (
        "IMFs, particulate views of phases, the ideal gas law, kinetic molecular theory, molarity, and "
        "chromatography/spectroscopy with particle-box and beaker figures."
    )
    c1 = concept_block(
        "1. Intermolecular forces",
        [
            "Intermolecular forces (IMFs) are the attractions between neighboring molecules, not the covalent "
            "bonds inside a molecule. Breaking IMFs is a phase change (melt, boil). Breaking covalent bonds is "
            "a chemical reaction. Water boiling leaves H₂O molecules intact.",
            "London dispersion forces exist in every sample with electrons. They come from temporary dipoles. "
            "Larger, more polarizable electron clouds (I₂ vs F₂, C₈H₁₈ vs CH₄) mean stronger dispersion and "
            "higher boiling points for otherwise similar substances.",
            "Dipole–dipole forces add extra attraction between polar molecules (HCl, CH₂Cl₂). Hydrogen bonding "
            "is a specially strong dipole force when H is bound to N, O, or F and is attracted to a lone pair "
            "on N, O, or F of a neighbor. It is still an IMF, not a covalent bond.",
            "Ionic bonds and network covalent bonds are not IMFs. NaCl(s) is held by ion–ion Coulomb forces. "
            "Diamond is held by C–C bonds. Those solids have enormous melting points compared with ice or I₂(s).",
            "Ranking boiling points: compare IMF type first (H-bonding vs dipole vs dispersion), then molar "
            "mass / polarizability if the type is the same. NH₃ boils higher than PH₃ because of hydrogen "
            "bonding, even though PH₃ is heavier.",
            "On FRQs, name the specific IMF in each substance and connect it to a property (boiling point, "
            "vapor pressure, solubility). “It has stronger IMFs” without naming which force is incomplete.",
        ],
        "IMFs explain why water is a liquid at room temperature, why I₂ is a solid, and why chromatography "
        "separates dyes. Unit 3 is mostly “what holds the particles next to each other?”",
        "Classify each molecule (polar? H on N/O/F?). Name the strongest IMF. Then compare sizes if you are "
        "still tied. Larger polarizable cloud → stronger dispersion.",
        lesson_figure(
            _imf_stack(),
            "IMF strength for small molecular substances",
            "Hydrogen bonding is the strongest common IMF. Dispersion is always present and can dominate in "
            "large nonpolar molecules (oils, I₂).",
        )
        + solved(1, "What is the strongest IMF in liquid water?",
               ["Water is polar and has H bound to O.",
                "Each molecule can donate and accept hydrogen bonds.",
                "The strongest IMF is hydrogen bonding (dispersion is also present)."],
               "hydrogen bonding", "", "Easy")
        + solved(2, "Why does I₂ have a higher boiling point than F₂?",
                 ["Both are nonpolar, so only dispersion forces act between molecules.",
                  "I₂ has far more electrons and a more polarizable cloud.",
                  "Stronger London forces mean more energy is needed to separate molecules.",
                  "I₂ is therefore a solid at room temperature while F₂ is a gas."],
                 "stronger dispersion in I₂", "", "Medium")
        + solved(3, "Why does NH₃ boil higher than PH₃ even though PH₃ has a larger molar mass?",
                 ["NH₃ has N–H bonds and a lone pair on N: classic hydrogen bonding.",
                  "PH₃ has only weak dipole/dispersion; P–H is a poor hydrogen-bond donor.",
                  "The extra IMF in ammonia outweighs the extra dispersion in the heavier PH₃.",
                  "Name the forces; do not stop at “ammonia is polar.”"],
                 "H-bonding in NH₃", "This is a standard AP comparison.", "Hard"),
        ("Calling hydrogen bonding a covalent bond inside one water molecule",
         "The O–H covalent bond is intramolecular. Hydrogen bonding is the attraction from that H to a lone "
         "pair on a neighboring molecule. Boiling water does not produce H and O atoms."),
        ("Name the force, then the property",
         "Write “H₂O has hydrogen bonding, so its boiling point is high / vapor pressure is low.” Graders "
         "award the IMF name and the link to the property separately."),
        [
            "I can name dispersion, dipole–dipole, and hydrogen bonding.",
            "I can compare boiling points using IMF type and polarizability.",
            "I can distinguish IMFs from ionic or network covalent bonding.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Solids, liquids, gases at the particulate level",
        [
            "A solid has particles close together in a mostly ordered arrangement; it has definite shape and "
            "volume. A liquid has particles close together but disordered; definite volume, no definite shape. "
            "A gas has particles far apart, disordered, filling the container.",
            "For a molecular substance, the particles in all three phases are the same molecules. Ice, liquid "
            "water, and steam are all H₂O. The difference is how strongly IMFs hold neighbors in place, not a "
            "change of formula.",
            "Ionic solids are lattices of ions. Metallic solids are cations in an electron sea. Network solids "
            "are atoms covalently bonded in 3-D. Molecular solids are molecules packed by IMFs. Those four "
            "pictures predict melting point and conductivity.",
            "Energy and phase: fusion (s→l) and vaporization (l→g) are endothermic because you work against "
            "attractions. Condensation and freezing release that energy. Temperature stays constant during a "
            "pure-substance phase change at constant P while the energy goes into changing the arrangement.",
            "Vapor pressure is the pressure of gas in equilibrium with its liquid. Strong IMFs mean low vapor "
            "pressure. Boiling occurs when vapor pressure equals external pressure.",
            "Particulate diagrams on the AP exam are scored strictly: count particles, keep molecules intact "
            "unless a reaction is stated, and show gases with large empty space.",
        ],
        "If you cannot sketch the particles, you will misread almost every Unit 3 visual item. The same "
        "sketches return in equilibrium and kinetics.",
        "Identify the type of solid first, then draw the correct particles (molecules vs ions vs atoms) with "
        "the correct spacing.",
        lesson_figure(
            _particle_box("solid") + _particle_box("liquid") + _particle_box("gas"),
            "Same particles, three arrangements",
            "Solid: ordered and touching. Liquid: touching but disordered. Gas: far apart with a range of speeds.",
        )
        + solved(4, "What stays the same when ice melts to liquid water: formula, IMFs present, or particle spacing?",
               ["The formula is still H₂O.",
                "Hydrogen bonding still exists in the liquid, but particles can slide.",
                "Spacing increases slightly; order is lost. Molecules do not break into H and O."],
               "molecules remain H₂O", "", "Easy")
        + solved(5, "Why is vaporization endothermic?",
                 ["Molecules in a liquid attract each other by IMFs.",
                  "To enter the gas, they must move far apart.",
                  "Energy must be supplied to overcome those attractions.",
                  "The energy does not go into breaking O–H covalent bonds in water."],
                 "energy is required to separate molecules", "", "Medium")
        + solved(6, "Compare melting points of I₂(s), NaCl(s), and diamond using the type of attraction.",
                 ["I₂ is a molecular solid: London forces, low melting point.",
                  "NaCl is ionic: strong Coulomb forces between ions, high melting point.",
                  "Diamond is network covalent: C–C bonds throughout, extremely high melting point.",
                  "The ranking is I₂ ≪ NaCl < diamond."],
                 "IMF vs ionic vs network", "", "Hard"),
        ("Drawing steam as H and O atoms",
         "Unless the problem says water decomposed, gas particles are H₂O molecules far apart. Breaking "
         "molecules would be electrolysis or a chemical reaction, not boiling."),
        ("Label each circle as a molecule or ion",
         "A particulate key (○ = H₂O, ● = Na⁺) prevents counting errors and shows the grader you know what "
         "the particles are."),
        [
            "I can sketch solid, liquid, and gas particulate views.",
            "I can explain fusion and vaporization as overcoming attractions.",
            "I can classify molecular, ionic, metallic, and network solids.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Ideal gas law",
        [
            "The ideal gas law is $PV=nRT$. $P$ is pressure, $V$ is volume, $n$ is moles, $T$ is temperature in "
            "kelvin, and $R$ is the gas constant. A common AP value is $R=0.0821\\ \\mathrm{L\\cdot atm\\cdot mol^{-1}\\cdot K^{-1}}$ "
            "when $P$ is in atm and $V$ is in liters.",
            "Kelvin is required: $T=\\,^\\circ\\mathrm{C}+273$. Using Celsius in $PV=nRT$ is a guaranteed error. "
            "At $0^\\circ$C and $1.00$ atm (STP in many AP items), one mole of ideal gas occupies about $22.4$ L "
            "because $(1)(0.0821)(273)\\approx 22.4$.",
            "Worked numbers: $n=1.00$ mol, $T=273$ K, $P=1.00$ atm → $V=22.4$ L. Another: $n=0.500$ mol, "
            "$T=300$ K, $V=10.0$ L → $P=(0.500)(0.0821)(300)/10.0=1.23$ atm.",
            "A designed clean case: $P=3.00$ atm, $V=8.21$ L, $T=300$ K, $R=0.0821$ → $n=PV/RT=24.63/24.63=1.00$ "
            "mol. When the arithmetic is this tidy, still write the substitution so a grader sees $PV/RT$.",
            "Combined gas law at constant $n$: $P_1 V_1/T_1=P_2 V_2/T_2$. Boyle ($T$ fixed): $PV$ constant. "
            "Charles ($P$ fixed): $V\\propto T$. Gay-Lussac ($V$ fixed): $P\\propto T$. Avogadro ($P,T$ fixed): "
            "$V\\propto n$.",
            "Molar mass from a gas: $n=m/M$, so $PM=dRT$ where $d=m/V$ is density. At STP, $n=V/22.4$, then "
            "$M=m/n$. That is a standard FRQ move.",
        ],
        "Gases are how chemistry counts moles without a balance sometimes. Titration of a gas-producing "
        "reaction, molar mass of an unknown, and stoichiometry of combustion all start with $PV=nRT$.",
        "List $P,V,n,T,R$ with units. Convert °C to K. Solve the algebra for the missing variable, then "
        "substitute numbers on a second line.",
        lesson_figure(
            _particle_box("gas"),
            "An ideal gas: lots of empty space",
            "Volume in $PV=nRT$ is the container volume. Particle volume is assumed negligible.",
        )
        + solved(7, "$n=1.00$ mol, $T=273$ K, $P=1.00$ atm, $R=0.0821$. Find $V$.",
               ["Write $V=nRT/P$.",
                "Substitute: $V=(1.00)(0.0821)(273)/1.00$.",
                "$(0.0821)(273)=22.413$, so $V=22.4$ L."],
               "$22.4$ L", "", "Easy")
        + solved(8, "$n=0.500$ mol, $T=300$ K, $V=10.0$ L, $R=0.0821$. Find $P$.",
                 ["$P=nRT/V$.",
                  "Numerator: $(0.500)(0.0821)(300)=12.315$.",
                  "Divide by $10.0$: $P=1.23$ atm."],
                 "$1.23$ atm", "", "Medium")
        + solved(9, "$P=3.00$ atm, $V=8.21$ L, $T=300$ K, $R=0.0821$. Find $n$.",
                 ["$n=PV/RT$.",
                  "$PV=(3.00)(8.21)=24.63$.",
                  "$RT=(0.0821)(300)=24.63$.",
                  "$n=24.63/24.63=1.00$ mol."],
                 "$1.00$ mol", "27°C is 300 K. Convert temperature first.", "Hard"),
        ("Leaving temperature in Celsius",
         "$300^\\circ$C is $573$ K, not $300$ K. $27^\\circ$C is $300$ K. Always add 273 (or 273.15) before "
         "using $PV=nRT$."),
        ("Write a data table of $P,V,n,T,R$",
         "Five quantities, one unknown. Crossing off the knowns makes the algebra obvious and prevents using "
         "$22.4$ L when the gas is not at STP."),
        [
            "I can solve $PV=nRT$ for any one variable with $T$ in kelvin.",
            "I can compute the $22.4$ L STP molar volume from the gas law.",
            "I can use $n=V/22.4$ at STP to find molar mass.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Kinetic molecular theory",
        [
            "Kinetic molecular theory (KMT) models an ideal gas as tiny particles in constant random motion, "
            "with negligible volume, negligible IMFs, and elastic collisions. Pressure is the result of "
            "collisions with the walls.",
            "Average kinetic energy of gas particles depends only on temperature: $K_\\mathrm{avg}=(3/2)RT$ "
            "per mole. At the same $T$, He and Xe have the same average KE even though Xe is heavier. Xe "
            "particles simply move more slowly: $K=\\tfrac12 mv^2$.",
            "Root-mean-square speed scales as $v_\\mathrm{rms}\\propto 1/\\sqrt{M}$. Helium ($4$ g/mol) vs "
            "methane ($16$ g/mol): $v_\\mathrm{He}/v_\\mathrm{CH_4}=\\sqrt{16/4}=2$. Helium is twice as fast "
            "at the same $T$.",
            "Raise $T$ at constant $V$ and $n$: particles move faster, hit harder and more often, so $P$ rises. "
            "Raise $n$ at constant $T$ and $V$: more particles hit the walls per second, so $P$ rises. These "
            "are the particulate stories behind Gay-Lussac and Avogadro.",
            "The Maxwell–Boltzmann distribution is a speed histogram. Higher $T$ shifts it right and flattens "
            "the peak. A heavier gas at the same $T$ has a peak at lower speed. Qualitatively read the graph; "
            "you do not need to integrate it.",
            "Real gases fail the ideal picture at high $P$ (particle volume matters) and low $T$ (IMFs matter). "
            "That is why $PV=nRT$ is a model, not a law of nature at every condition.",
        ],
        "KMT is how you earn “explain” points on gas FRQs. A formula without a collision story is incomplete.",
        "Same $T$ → same average KE. Smaller $M$ → larger speed. Pressure → wall collisions. Deviations → "
        "volume and IMFs at high $P$ / low $T$.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#1d4ed8", sample_curve(lambda v: v**2 * (2.718 ** (-v**2 / 8)), 0.1, 8)),
                    ("#b91c1c", sample_curve(lambda v: 0.55 * v**2 * (2.718 ** (-v**2 / 18)), 0.1, 10)),
                ],
                xlim=(0, 10), ylim=(0, 3.2), xlab="speed", ylab="fraction of particles", w=320, h=220,
            ),
            "Maxwell–Boltzmann idea: two temperatures (or two masses)",
            "The broader, right-shifted curve is the hotter sample (or the lighter gas). The peak is lower "
            "because the same particles are spread over more speeds.",
        )
        + solved(10, "At the same $T$, compare average KE of He(g) and Xe(g).",
               ["KMT: average KE depends only on temperature.",
                "Both gases are at the same $T$.",
                "Average KE is the same; Xe is slower because it is heavier."],
               "equal average KE", "", "Easy")
        + solved(11, "He is $4$ g/mol and CH₄ is $16$ g/mol. Ratio of $v_\\mathrm{rms}$ (He/CH₄) at the same $T$?",
                 ["$v_\\mathrm{rms}\\propto 1/\\sqrt{M}$.",
                  "Ratio $=\\sqrt{M_\\mathrm{CH_4}/M_\\mathrm{He}}=\\sqrt{16/4}$.",
                  "$\\sqrt{4}=2$.",
                  "Helium is twice as fast."],
                 "2", "", "Medium")
        + solved(12, "Using KMT, why does $P$ increase when $n$ increases at constant $T$ and $V$?",
                 ["Temperature fixed, so average KE and typical collision force stay similar.",
                  "More moles means more particles in the same box.",
                  "More particles strike the walls each second.",
                  "More collisions per second means larger pressure."],
                 "more wall collisions per second",
                 "Do not say the particles get hotter; $T$ was held constant.", "Hard"),
        ("Saying heavier gases have more kinetic energy at the same $T$",
         "They have more mass but less speed. The product $\\tfrac12 mv^2$ averages to the same value at a "
         "given temperature."),
        ("Answer with collisions, then the variable",
         "“Faster particles hit harder and more often, so $P$ increases with $T$ at constant $V$.” That "
         "sentence is the KMT template."),
        [
            "I can state that average KE depends only on $T$.",
            "I can use $v_\\mathrm{rms}\\propto 1/\\sqrt{M}$.",
            "I can explain $P$ using wall collisions.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Solutions and molarity",
        [
            "A solution is a homogeneous mixture. The solute is the dissolved species; the solvent is the "
            "majority component (often water). At the particulate level, solute particles are scattered among "
            "solvent particles, not sitting in a clump at the bottom.",
            "Molarity is $M=n/V$, moles of solute per liter of solution. The volume is the solution volume "
            "after mixing, not the volume of water you started with. $0.500$ mol in $0.250$ L is $2.00$ M.",
            "Making a solution from a solid: compute moles from grams, then divide by flask volume. $5.85$ g "
            "NaCl ($58.5$ g/mol) is $0.100$ mol; in a $0.500$ L flask that is $0.200$ M.",
            "Dilution: moles of solute stay the same, so $M_1 V_1=M_2 V_2$. Diluting $25.0$ mL of $2.00$ M HCl "
            "to $100.0$ mL gives $M_2=(2.00)(25.0)/100.0=0.500$ M. You add solvent; you do not destroy solute.",
            "Ionic solutes separate into ions. $0.10$ M K₂SO₄ has $[K^+]=0.20$ M and $[SO_4^{2-}]=0.10$ M. "
            "That particle count matters for colligative properties and for later equilibrium problems.",
            "“Like dissolves like”: polar and ionic solutes dissolve in polar solvents (water); nonpolar "
            "solutes dissolve in nonpolar solvents. That is an IMF matching rule, the same rule as chromatography.",
        ],
        "Almost every titration, kinetics run, and equilibrium ICE table is done in moles per liter. Molarity "
        "is the concentration language of AP Chemistry.",
        "Find moles first (from mass or from $M\\times V$), then divide by the solution volume in liters. For "
        "dilution, conserve moles with $M_1 V_1=M_2 V_2$.",
        lesson_figure(
            beaker_svg("1.0 M solution") + _particle_box("mix"),
            "Molarity is a count per liter of mixture",
            "Blue circles: solvent. Red circles: solute. Homogeneous means the red particles are spread through "
            "the beaker, not layered.",
        )
        + solved(13, "What is the molarity of $0.500$ mol NaCl in $0.250$ L of solution?",
               ["$M=n/V$.",
                "$M=0.500/0.250$.",
                "$M=2.00$ M."],
               "$2.00$ M", "", "Easy")
        + solved(14, "$5.85$ g NaCl ($58.5$ g/mol) is dissolved and diluted to $0.500$ L. Find $M$.",
                 ["$n=5.85/58.5=0.100$ mol.",
                  "$V=0.500$ L.",
                  "$M=0.100/0.500=0.200$ M."],
                 "$0.200$ M", "", "Medium")
        + solved(15, "$25.0$ mL of $2.00$ M HCl is diluted to $100.0$ mL. New molarity?",
                 ["Moles of HCl are unchanged: $n=M_1 V_1=(2.00)(0.0250)=0.0500$ mol.",
                  "Alternatively: $M_1 V_1=M_2 V_2$.",
                  "$(2.00)(25.0)=M_2(100.0)$.",
                  "$M_2=50.0/100.0=0.500$ M."],
                 "$0.500$ M", "Volumes may stay in mL if both sides use mL.", "Hard"),
        ("Using milliliters as if they were liters in $M=n/V$",
         "$250$ mL is $0.250$ L. Dividing moles by $250$ instead of $0.250$ makes molarity 1000 times too "
         "small. Convert volume to liters unless you are using $M_1 V_1=M_2 V_2$ with matching units."),
        ("Compute $n$ on its own line",
         "Grams → moles, or $M\\times V$ → moles, then divide. Combining everything in one fraction invites "
         "a unit error."),
        [
            "I can compute molarity from moles and liters.",
            "I can convert grams of solute into $M$.",
            "I can use $M_1 V_1=M_2 V_2$ for dilution.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Chromatography and spectroscopy",
        [
            "Chromatography separates a mixture because components partition differently between a mobile phase "
            "(the moving solvent) and a stationary phase (paper, a column packing, a TLC plate). The component "
            "that spends more time in the mobile phase travels farther.",
            "The retention factor is $R_f=$ (distance the spot moved) / (distance the solvent front moved). If "
            "the front is $8.0$ cm and a spot is at $4.0$ cm, $R_f=0.50$. $R_f$ has no units and must be between "
            "$0$ and $1$.",
            "Like dissolves like: a nonpolar dye in a nonpolar solvent on polar paper has a large $R_f$. A polar "
            "dye sticks to polar paper and lags behind. Changing the solvent changes $R_f$ because the IMF match "
            "changes.",
            "Spectroscopy reads how matter interacts with light. Beer's law is $A=\\varepsilon b c$: absorbance "
            "is proportional to path length $b$ and concentration $c$. A calibration curve of $A$ versus $c$ is "
            "linear for dilute colored solutions.",
            "Infrared (IR) spectroscopy identifies bonds by their vibration frequencies (O–H, C=O, C–H). "
            "Photoelectron spectroscopy was Unit 1. Mass spectrometry gives $m/z$ of ions, including a "
            "molecular-ion peak near the molar mass.",
            "These tools are how AP Chemistry asks you to identify a substance without “tasting it.” Connect "
            "the method to the molecular feature: polarity → chromatography; concentration of a chromophore → "
            "UV-vis; functional group → IR; mass → MS.",
        ],
        "Separation and identification questions are easy points if you remember $R_f$ arithmetic and Beer's "
        "law, and if you can say why a polar spot barely moves.",
        "For TLC: measure both distances, divide, then justify with IMFs. For UV-vis: $A\\propto c$. For IR: "
        "name the bond. For MS: read $m/z$.",
        lesson_figure(
            _tlc_svg(),
            "Paper / TLC chromatogram",
            "Origin at the bottom, solvent front dashed at the top. The green spot traveled farther (larger "
            "$R_f$) than the red spot in this solvent.",
        )
        + solved(16, "Solvent front $8.0$ cm, spot $4.0$ cm. What is $R_f$?",
               ["$R_f=d_\\mathrm{spot}/d_\\mathrm{front}$.",
                "$R_f=4.0/8.0$.",
                "$R_f=0.50$."],
               "$0.50$", "", "Easy")
        + solved(17, "If path length doubles in a UV-vis cell and $c$ is unchanged, what happens to $A$?",
                 ["Beer's law: $A=\\varepsilon b c$.",
                  "$\\varepsilon$ and $c$ fixed; $b$ doubles.",
                  "$A$ doubles."],
                 "$A$ doubles", "", "Medium")
        + solved(18, "A nonpolar solvent is used on polar paper. Which spot has the larger $R_f$: a polar dye or a nonpolar dye? Justify with IMFs.",
                 ["Polar paper (stationary) attracts the polar dye more strongly.",
                  "The nonpolar dye prefers the nonpolar mobile phase and travels farther.",
                  "Larger distance / same front → larger $R_f$ for the nonpolar dye.",
                  "This is “like dissolves like” applied to two phases."],
                 "nonpolar dye has larger $R_f$", "", "Hard"),
        ("Computing $R_f$ as front divided by spot, or using cm as if they were a concentration",
         "$R_f$ is spot over front, a number less than 1. $8/4=2$ is not an allowed $R_f$."),
        ("Write both distances on the sketch",
         "Bracket the solvent front and the center of the spot. Division is then obvious, and you will not "
         "grab the plate length by accident."),
        [
            "I can compute $R_f$ from two measured distances.",
            "I can justify TLC order using IMFs and like-dissolves-like.",
            "I can apply $A=\\varepsilon b c$ qualitatively.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        ["IMFs", "Solids liquids gases particulate", "Ideal gas law",
         "Kinetic molecular theory", "Solutions and molarity", "Chromatography and spectroscopy"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4
# ===========================================================================

def _u4_questions():
    return _qs([
        ("The net ionic equation for AgNO₃(aq)+NaCl(aq) is:",
         "Ag⁺(aq)+Cl⁻(aq)→AgCl(s)",
         "Na⁺ and NO₃⁻ are spectators.",
         ["Na⁺+NO₃⁻→NaNO₃", "AgNO₃+NaCl→AgCl+NaNO₃", "Ag+Cl→AgCl"]),
        ("Spectator ions in the AgCl precipitation are:",
         "Na⁺ and NO₃⁻", "They start and finish as aqueous ions.",
         ["Ag⁺ and Cl⁻", "only Ag⁺", "H⁺ and OH⁻"]),
        ("Strong electrolytes in water include:",
         "soluble ionic compounds and strong acids",
         "They exist as ions, which is why they appear split in net ionic equations.",
         ["pure water only", "all molecular compounds", "insoluble salts as molecules in solution"]),
        ("Pb(NO₃)₂(aq)+2KI(aq) produces a yellow solid. The net ionic equation includes:",
         "Pb²⁺(aq)+2I⁻(aq)→PbI₂(s)",
         "K⁺ and NO₃⁻ are spectators.",
         ["K⁺+NO₃⁻→KNO₃(s)", "Pb+I₂→PbI₂", "2K+Pb→alloy"]),
        ("HCl(aq)+NaOH(aq) net ionic equation is:",
         "H⁺(aq)+OH⁻(aq)→H₂O(l)",
         "Na⁺ and Cl⁻ are spectators in a strong-acid / strong-base neutralization.",
         ["HCl+NaOH→NaCl+H₂O as molecules only", "Na⁺+Cl⁻→NaCl(s)", "H⁺+Cl⁻→HCl(g)"]),
        ("For 2H₂+O₂→2H₂O, moles of water from 3.00 mol O₂ (H₂ in excess) are:",
         "6.00 mol", "Mole ratio 2 H₂O / 1 O₂ → 3.00×2=6.00.",
         ["3.00 mol", "1.50 mol", "2.00 mol"]),
        ("Mass of H₂O (18.0 g/mol) produced from 4.00 mol H₂ with excess O₂ in 2H₂+O₂→2H₂O?",
         "72.0 g", "4.00 mol H₂ → 4.00 mol H₂O → 4.00×18.0=72.0 g.",
         ["36.0 g", "18.0 g", "8.00 g"]),
        ("N₂+3H₂→2NH₃. If 2.00 mol N₂ react completely, NH₃ produced is:",
         "4.00 mol", "Ratio 2 NH₃ / 1 N₂.",
         ["2.00 mol", "6.00 mol", "1.00 mol"]),
        ("How many moles of O₂ are needed to burn 2.00 mol CH₄ in CH₄+2O₂→CO₂+2H₂O?",
         "4.00 mol", "2 mol O₂ per mol CH₄.",
         ["2.00 mol", "1.00 mol", "8.00 mol"]),
        ("44.0 g CO₂ (44.0 g/mol) came from burning CH₄. Moles of CH₄ that burned?",
         "1.00 mol", "n_CO₂=1.00 mol; mole ratio 1:1 with CH₄.",
         ["44.0 mol", "2.00 mol", "0.500 mol"]),
        ("2H₂+O₂→2H₂O with 4.00 mol H₂ and 1.00 mol O₂. Limiting reactant?",
         "O₂", "Need 2 mol H₂ per 1 mol O₂; 4 mol H₂ would need 2 mol O₂, but only 1 mol O₂ is present.",
         ["H₂", "H₂O", "neither; they match exactly"]),
        ("In that same mixture, moles of H₂O produced?",
         "2.00 mol", "O₂ limits: 1.00 mol O₂ → 2.00 mol H₂O.",
         ["4.00 mol", "1.00 mol", "3.00 mol"]),
        ("Leftover H₂ after 4.00 mol H₂ reacts with 1.00 mol O₂?",
         "2.00 mol H₂", "H₂ used = 2.00 mol; leftover = 2.00 mol.",
         ["0 mol", "4.00 mol", "1.00 mol"]),
        ("2Al+3CuCl₂→2AlCl₃+3Cu. 0.400 mol Al and 0.450 mol CuCl₂. Limiting reactant?",
         "CuCl₂", "0.400 mol Al needs 0.600 mol CuCl₂; only 0.450 mol is available.",
         ["Al", "Cu", "AlCl₃"]),
        ("From 0.450 mol CuCl₂ limiting, moles of Cu metal produced?",
         "0.450 mol", "3 Cu / 3 CuCl₂ = 1:1.",
         ["0.300 mol", "0.600 mol", "0.150 mol"]),
        ("25.0 mL of 0.100 M HCl requires how many mL of 0.100 M NaOH to neutralize?",
         "25.0 mL", "Equal moles of H⁺ and OH⁻; same M and 1:1 stoichiometry.",
         ["12.5 mL", "50.0 mL", "0.100 mL"]),
        ("40.0 mL of 0.100 M NaOH titrates 20.0 mL of HCl. Molarity of HCl?",
         "0.200 M", "mmol OH⁻=4.00; mmol H⁺=4.00; M=4.00/20.0=0.200.",
         ["0.0500 M", "0.100 M", "0.400 M"]),
        ("At the equivalence point of a strong-acid / strong-base titration, the mixture is:",
         "H⁺ and OH⁻ have been matched mole-for-mole (pH near 7 at 25°C)",
         "Spectators remain; neither acid nor base is in excess.",
         ["still 1 M strong acid", "pure solid NaOH", "only gas"]),
        ("A buret reading goes from 2.40 mL to 18.90 mL. Volume delivered?",
         "16.50 mL", "18.90−2.40=16.50 mL.",
         ["21.30 mL", "18.90 mL", "2.40 mL"]),
        ("Phenolphthalein is used in many SA/SB titrations because it changes color:",
         "near the steep pH jump around equivalence",
         "The indicator is chosen so its range overlaps the steep region.",
         ["at pH 1 only", "only in the solid acid", "when the buret is empty"]),
        ("In 2Ag⁺+Cu→2Ag+Cu²⁺, the species oxidized is:",
         "Cu", "Cu goes from 0 to +2; oxidation is loss of electrons.",
         ["Ag⁺", "Ag metal", "the water solvent"]),
        ("In that same reaction, Ag⁺ is:",
         "reduced (gains electrons)",
         "Ag⁺ → Ag(s); oxidation number  +1 → 0.",
         ["oxidized", "a spectator", "the reducing agent"]),
        ("The reducing agent is the species that:",
         "is oxidized (loses electrons) and causes reduction of the other species",
         "Cu is the reducing agent in Cu + 2Ag⁺.",
         ["always water", "the product with highest charge", "an inert salt"]),
        ("Oxidation number of S in SO₄²⁻?",
         "+6", "O is −2 each (total −8); ion is −2, so S is +6.",
         ["+4", "−2", "+2"]),
        ("Oxidation number of N in NO₃⁻?",
         "+5", "3(−2)+N=−1 → N=+5.",
         ["+3", "−1", "+2"]),
        ("2Mg+O₂→2MgO is classified as:",
         "synthesis (combination) and redox",
         "Two elements form a compound; Mg is oxidized.",
         ["double replacement", "acid–base only", "nuclear"]),
        ("CaCO₃→CaO+CO₂ is:",
         "decomposition",
         "One compound becomes two products.",
         ["synthesis", "single replacement", "combustion of a hydrocarbon"]),
        ("Zn+CuSO₄→ZnSO₄+Cu is:",
         "single replacement (and redox)",
         "Zn displaces Cu²⁺.",
         ["double replacement with no redox", "combustion", "decomposition of Zn"]),
        ("CH₄+2O₂→CO₂+2H₂O is:",
         "combustion",
         "Hydrocarbon plus oxygen to CO₂ and H₂O.",
         ["double replacement", "neutralization only", "fusion"]),
        ("AgNO₃+NaCl→AgCl+NaNO₃ is:",
         "double replacement (precipitation)",
         "Cations swap partners; AgCl is insoluble.",
         ["combustion", "single replacement of Na", "synthesis of Ag metal"]),
        ("How many moles of electrons are transferred when 1.00 mol Cu reduces 2.00 mol Ag⁺?",
         "2.00 mol e⁻", "Each Cu loses 2 e⁻; each Ag⁺ gains 1 e⁻.",
         ["1.00 mol e⁻", "0 mol", "4.00 mol e⁻"]),
        ("25.0 mL of 0.200 M Ba(OH)₂ titrates HCl. Moles of OH⁻ available?",
         "0.0100 mol", "n_Ba(OH)₂=0.00500 mol; 2 OH⁻ each → 0.0100 mol OH⁻.",
         ["0.00500 mol", "0.200 mol", "0.0250 mol"]),
        ("Percent yield if 8.00 g product is obtained and theoretical yield is 10.0 g?",
         "80.0%", "(8.00/10.0)×100%=80.0%.",
         ["125%", "8.00%", "10%"]),
        ("Which ion is typically a spectator in NaOH(aq)+HCl(aq)?",
         "Na⁺", "Also Cl⁻; both remain aqueous.",
         ["H⁺", "OH⁻", "H₂O"]),
        ("Fe₂O₃+3CO→2Fe+3CO₂. If 1.00 mol Fe₂O₃ reacts, moles of Fe?",
         "2.00 mol", "Ratio 2 Fe / 1 Fe₂O₃.",
         ["1.00 mol", "3.00 mol", "0.500 mol"]),
        ("A titration curve of strong acid with strong base has equivalence near pH:",
         "7 (at 25°C)", "The salt is neutral (NaCl-type).",
         ["1", "14", "4"]),
        ("Which is a redox reaction?",
         "2Na+Cl₂→2NaCl", "Na 0→+1, Cl 0→−1.",
         ["NaCl(aq)+AgNO₃(aq)→AgCl(s)+NaNO₃(aq)", "HCl+NaOH→NaCl+H₂O", "NaCl dissolving in water"]),
        ("Limiting reactant is the reactant that:",
         "is consumed first and determines the maximum product",
         "Compare required vs available moles using the ratio.",
         ["has the largest mass automatically", "is always oxygen", "remains after the reaction"]),
        ("In 2KClO₃→2KCl+3O₂, moles of O₂ from 4.00 mol KClO₃?",
         "6.00 mol", "3/2 × 4.00=6.00.",
         ["4.00 mol", "3.00 mol", "2.00 mol"]),
        ("Net ionic for Ba²⁺(aq)+SO₄²⁻(aq) is:",
         "Ba²⁺(aq)+SO₄²⁻(aq)→BaSO₄(s)",
         "Barium sulfate is insoluble.",
         ["Ba+S+2O₂→BaSO₄", "H⁺+OH⁻→H₂O", "Ba²⁺+2NO₃⁻→Ba(NO₃)₂"]),
        ("Oxidation number of Cr in Cr₂O₇²⁻?",
         "+6", "2Cr+7(−2)=−2 → 2Cr=12 → Cr=+6.",
         ["+3", "+7", "−2"]),
        ("If 0.300 mol of limiting A produces a theoretical 0.600 mol B (from A→2B) but 0.450 mol B is isolated, percent yield is:",
         "75.0%", "0.450/0.600=0.750=75.0%.",
         ["150%", "45%", "60%"]),
        ("H₂SO₄ is diprotic. 20.0 mL of 0.100 M H₂SO₄ needs how many mL of 0.100 M NaOH for complete neutralization?",
         "40.0 mL", "0.00200 mol H₂SO₄ supplies 0.00400 mol H⁺; V_NaOH=40.0 mL.",
         ["20.0 mL", "10.0 mL", "80.0 mL"]),
        ("Which equation is balanced?",
         "2C₂H₆+7O₂→4CO₂+6H₂O",
         "4 C, 12 H, 14 O on both sides.",
         ["C₂H₆+O₂→CO₂+H₂O", "C₂H₆+7O₂→4CO₂+6H₂O", "2C₂H₆+O₂→4CO₂+6H₂O"]),
        ("In electrolysis language vs a beaker reaction: adding Zn to Cu²⁺ is a:",
         "spontaneous redox (displacement) in a single container",
         "Not yet a galvanic cell with a wire; still redox.",
         ["only an acid–base reaction", "a precipitation of Zn metal from Cu", "nuclear fusion"]),
        ("Theoretical yield of water from 2.00 mol H₂ and 2.00 mol O₂ (2H₂+O₂→2H₂O) is:",
         "2.00 mol H₂O", "H₂ limits (needs 1.00 mol O₂; 2.00 mol O₂ is excess).",
         ["4.00 mol H₂O", "2.00 mol O₂ of water", "1.00 mol H₂O"]),
        ("AP Stretch: 2Al+3Cu²⁺→2Al³⁺+3Cu. 0.240 mol Al is mixed with 0.300 mol Cu²⁺. Identify the limiter, moles of Cu formed, and leftover moles of the excess reactant.",
         "Cu²⁺ limits; 0.300 mol Cu; 0.040 mol Al left",
         "Al would need 0.240×(3/2)=0.360 mol Cu²⁺, but only 0.300 mol Cu²⁺ is present, so Cu²⁺ limits. Cu formed=0.300 mol. Al used=0.300×(2/3)=0.200 mol; leftover Al=0.040 mol.",
         ["Al limits; 0.240 mol Cu; 0.060 mol Cu²⁺ left", "Cu²⁺ limits; 0.450 mol Cu; 0 Al left", "neither limits; 0.540 mol Cu"]),
        ("AP Stretch: 35.00 mL of 0.1500 M HCl is titrated with 0.1000 M NaOH. Volume of NaOH at equivalence?",
         "52.50 mL", "n_HCl=(0.1500)(0.03500)=0.005250 mol; V_NaOH=0.005250/0.1000=0.05250 L=52.50 mL.",
         ["35.00 mL", "23.33 mL", "150.0 mL"]),
        ("AP Stretch: Assign oxidation numbers in 2MnO₄⁻+5C₂O₄²⁻+16H⁺→2Mn²⁺+10CO₂+8H₂O and state what is reduced.",
         "Mn +7→+2 is reduced",
         "Mn in MnO₄⁻ is +7; Mn²⁺ is +2. C in oxalate is +3; in CO₂ is +4 (oxidized).",
         ["C is reduced", "H⁺ is reduced to H₂O only as redox", "O is oxidized from −2 to 0"]),
        ("AP Stretch: 12.0 g of C (12.0 g/mol) burns in excess O₂. Mass of CO₂ (44.0 g/mol) if percent yield is 80.0%?",
         "35.2 g", "n_C=1.00 mol → theoretical CO₂=1.00 mol=44.0 g; 80.0% of 44.0=35.2 g.",
         ["44.0 g", "12.0 g", "80.0 g"]),
        ("AP Stretch: Write the balanced net ionic equation for the reaction of acetic acid (weak) with NaOH and identify the spectator.",
         "HC₂H₃O₂(aq)+OH⁻(aq)→C₂H₃O₂⁻(aq)+H₂O(l); Na⁺ spectator",
         "Weak acid is written as a molecule; OH⁻ is the reacting base.",
         ["H⁺+OH⁻→H₂O with acetate as a molecule spectator", "Na⁺+C₂H₃O₂⁻→NaC₂H₃O₂(s)", "CH₄+OH⁻→CO₂"]),
        ("AP Stretch: 0.500 mol Fe₂O₃ reacts with 0.900 mol CO (Fe₂O₃+3CO→2Fe+3CO₂). Limiter, Fe produced, leftover excess?",
         "CO limits; 0.600 mol Fe; 0.200 mol Fe₂O₃ left",
         "0.500 mol Fe₂O₃ needs 1.50 mol CO; only 0.900 mol CO → CO limits. Fe=0.900×(2/3)=0.600 mol. Fe₂O₃ used=0.900/3=0.300 mol; leftover=0.200 mol.",
         ["Fe₂O₃ limits; 1.00 mol Fe; 0 CO left", "CO limits; 0.900 mol Fe; 0.500 mol Fe₂O₃ left", "both limit; 1.40 mol Fe"]),
        ("AP Stretch: A 0.204 g sample of a monoprotic acid (HA) is titrated with 27.50 mL of 0.1000 M NaOH to the equivalence point. Molar mass of HA?",
         "74.2 g/mol", "n_NaOH=(0.1000)(0.02750)=0.002750 mol=n_HA; M=0.204/0.002750=74.18 g/mol.",
         ["204 g/mol", "7.42 g/mol", "27.5 g/mol"]),
        ("AP Stretch: Balance in acid: Cr₂O₇²⁻+Fe²⁺→Cr³⁺+Fe³⁺. How many Fe²⁺ are oxidized per Cr₂O₇²⁻, and what mass of Fe (55.8 g/mol) is oxidized by 0.100 mol of dichromate?",
         "6 Fe²⁺; 33.5 g Fe",
         "Each Cr goes +6→+3 (3 e⁻); two Cr gain 6 e⁻. Each Fe²⁺ loses 1 e⁻, so 6 Fe²⁺ per dichromate. n_Fe=0.600 mol; mass=0.600×55.8=33.5 g.",
         ["5 Fe²⁺; 27.9 g (MnO₄⁻ counting)", "3 Fe²⁺; 16.7 g", "1 Fe²⁺; 5.58 g"]),
        ("AP Stretch: 2.00 L of 0.500 M AgNO₃ is mixed with 1.00 L of 0.500 M CaCl₂. Mass of AgCl (143.4 g/mol) produced?",
         "143 g",
         "n_Ag⁺=(0.500)(2.00)=1.00 mol; n_CaCl₂=(0.500)(1.00)=0.500 mol so n_Cl⁻=1.00 mol. AgCl=1.00 mol≈143 g.",
         ["71.7 g", "286 g", "0.500 mol as 71.7 g skipping the ion count"]),
    ])


def build_unit4():
    title = "AP Chemistry Unit 4: Chemical Reactions"
    description = (
        "Net ionic equations, stoichiometry, limiting reactants, introductory titration, redox identification, "
        "and reaction types with precipitation and particle diagrams."
    )
    c1 = concept_block(
        "1. Net ionic equations",
        [
            "A complete ionic equation writes strong electrolytes as free ions. A net ionic equation cancels "
            "spectator ions — ions that appear unchanged on both sides — and keeps only the species that actually "
            "change. For AgNO₃(aq)+NaCl(aq), the net ionic equation is $\\mathrm{Ag^+(aq)+Cl^-(aq)\\rightarrow AgCl(s)}$.",
            "Soluble ionic compounds and strong acids are split into ions. Insoluble solids, gases, weak acids, "
            "and molecular nonelectrolytes stay written as compounds. That is why acetic acid in a neutralization "
            "is $\\mathrm{HC_2H_3O_2}$, not $\\mathrm{H^+}$, on the AP exam.",
            "Precipitation is the classic net-ionic story: two aqueous solutions supply ions, and an insoluble "
            "pair forms a solid. Pb²⁺ + 2 I⁻ → PbI₂(s). Potassium and nitrate stay dissolved as spectators.",
            "Strong-acid / strong-base neutralization nets to $\\mathrm{H^+(aq)+OH^-(aq)\\rightarrow H_2O(l)}$. "
            "The salt ions (Na⁺, Cl⁻) are spectators unless they form an insoluble product, which they do not "
            "in the HCl/NaOH case.",
            "You must also know solubility patterns at AP level: nitrates are soluble; Group 1 and ammonium "
            "salts are soluble; most chlorides are soluble except Ag⁺, Pb²⁺, Hg₂²⁺; most hydroxides and phosphates "
            "are insoluble except with Group 1 / Ca²⁺, Ba²⁺ (OH⁻ partial). Use the course solubility table when given.",
            "A net ionic equation is scored for (1) correct species, (2) states, (3) balance, including charge "
            "balance. $\\mathrm{Ag^+ + Cl^- \\rightarrow AgCl}$ without (aq) and (s) may lose a point.",
        ],
        "Net ionic language is how AP Chemistry talks about precipitation, neutralization, and later equilibrium "
        "of slightly soluble salts. Spectators never belong in $K_\\mathrm{sp}$ expressions either.",
        "Write the full molecular equation, split the strong electrolytes, cross out ions that do not change, "
        "and check that atoms and charge still balance.",
        lesson_figure(
            _ppt_beakers(),
            "Precipitation of AgCl",
            "Two clear solutions mix. Ag⁺ and Cl⁻ form a white solid. Na⁺ and NO₃⁻ remain dissolved spectators.",
        )
        + solved(1, "Write the net ionic equation for AgNO₃(aq)+NaCl(aq).",
               ["Full equation: AgNO₃ + NaCl → AgCl(s) + NaNO₃.",
                "Ionic: Ag⁺ + NO₃⁻ + Na⁺ + Cl⁻ → AgCl(s) + Na⁺ + NO₃⁻.",
                "Cancel Na⁺ and NO₃⁻.",
                "Net: $\\mathrm{Ag^+(aq)+Cl^-(aq)\\rightarrow AgCl(s)}$."],
               "$\\mathrm{Ag^+ + Cl^- \\rightarrow AgCl(s)}$", "", "Easy")
        + solved(2, "What are the spectator ions in Pb(NO₃)₂(aq)+2 KI(aq) → PbI₂(s)+2 KNO₃(aq)?",
                 ["Split: Pb²⁺ + 2 NO₃⁻ + 2 K⁺ + 2 I⁻ → PbI₂(s) + 2 K⁺ + 2 NO₃⁻.",
                  "K⁺ and NO₃⁻ appear on both sides.",
                  "They are spectators.",
                  "Net ionic: Pb²⁺ + 2 I⁻ → PbI₂(s)."],
                 "K⁺ and NO₃⁻", "", "Medium")
        + solved(3, "Write the net ionic equation for HC₂H₃O₂(aq)+NaOH(aq).",
                 ["Acetic acid is weak: keep it molecular.",
                  "NaOH is strong: write Na⁺ and OH⁻.",
                  "Na⁺ is a spectator. OH⁻ takes the proton from the weak acid.",
                  "Net: $\\mathrm{HC_2H_3O_2(aq)+OH^-(aq)\\rightarrow C_2H_3O_2^-(aq)+H_2O(l)}$."],
                 "$\\mathrm{HC_2H_3O_2 + OH^- \\rightarrow C_2H_3O_2^- + H_2O}$",
                 "Do not write H⁺ + OH⁻ for a weak acid.", "Hard"),
        ("Splitting a weak acid into H⁺ in the net ionic equation",
         "Weak acids are mostly molecules. The reacting species is the molecule plus OH⁻ (or another base), "
         "not a flood of free H⁺. That distinction returns in Unit 8 buffers."),
        ("Cancel only species that are identical on both sides",
         "Do not cancel Ag⁺ just because silver appears in AgCl(s). The solid is a different species. Spectators "
         "must match formula, charge, and state."),
        [
            "I can cancel spectators to write a net ionic equation.",
            "I can keep weak acids molecular.",
            "I can include (aq) and (s) and balance charge.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Stoichiometry",
        [
            "Stoichiometry is mole-to-mole conversion using the coefficients of a balanced equation. The "
            "coefficients are not grams. For $2\\,\\mathrm{H_2 + O_2 \\rightarrow 2\\,H_2O}$, two moles of H₂ "
            "make two moles of water, which is $2\\times 18.0=36.0$ g of water, not $2$ g.",
            "The reliable chain is grams A → moles A → moles B → grams B. The middle step uses the mole ratio. "
            "If $3.00$ mol O₂ react with excess H₂, water produced is $3.00\\times(2/1)=6.00$ mol, or $108$ g.",
            "Combustion of methane: $\\mathrm{CH_4 + 2\\,O_2 \\rightarrow CO_2 + 2\\,H_2O}$. Burning $2.00$ mol "
            "CH₄ requires $4.00$ mol O₂ and produces $2.00$ mol CO₂. If you collect $44.0$ g CO₂ ($1.00$ mol), "
            "$1.00$ mol of CH₄ burned.",
            "Ammonia synthesis: $\\mathrm{N_2 + 3\\,H_2 \\rightarrow 2\\,NH_3}$. Complete reaction of $2.00$ mol "
            "N₂ yields $4.00$ mol NH₃. The $3:1$ hydrogen ratio is how you later detect a limiting reactant.",
            "Percent yield is $\\mathrm{(actual/theoretical)\\times 100\\%}$. If theory says $10.0$ g and you "
            "isolate $8.00$ g, the yield is $80.0\\%$. Actual cannot exceed theoretical unless the sample is wet "
            "or impure — an FRQ discussion point.",
            "Every AP calculation problem is this chain plus maybe $PV=nRT$ or $M=n/V$ on one end. Balance first, "
            "then convert to moles, then use the ratio.",
        ],
        "Stoichiometry is the arithmetic of conservation of atoms. Kinetics, equilibrium, and titrations all "
        "assume you can move between moles of A and moles of B.",
        "Balance. Convert the given to moles. Multiply by (coefficients of wanted)/(coefficients of given). "
        "Convert moles of wanted into the asked unit (g, L, molecules).",
        lesson_figure(
            _stoich_h2o_svg(),
            "Coefficients count particles (and moles): 2 H₂ + 1 O₂ → 2 H₂O",
            "Count the molecules: two H₂ (blue pairs) and one O₂ (red pair) make two water molecules. Masses come after the mole step.",
        )
        + solved(4, "For $2\\,\\mathrm{H_2+O_2\\rightarrow 2\\,H_2O}$, how many moles of H₂O from $3.00$ mol O₂ (excess H₂)?",
               ["The ratio is $2$ mol H₂O per $1$ mol O₂.",
                "Multiply: $3.00\\times 2=6.00$.",
                "Answer $6.00$ mol H₂O."],
               "$6.00$ mol", "", "Easy")
        + solved(5, "Mass of water from $4.00$ mol H₂ and excess O₂? H₂O is $18.0$ g/mol.",
                 ["Mole ratio $2\\,\\mathrm{H_2}:2\\,\\mathrm{H_2O}$ is $1:1$.",
                  "So $4.00$ mol H₂ → $4.00$ mol H₂O.",
                  "Mass $=4.00\\times 18.0=72.0$ g."],
                 "$72.0$ g", "", "Medium")
        + solved(6, "$\\mathrm{N_2+3H_2\\rightarrow 2NH_3}$. How many grams of NH₃ ($17.0$ g/mol) from $2.00$ mol N₂?",
                 ["Ratio $2$ mol NH₃ per $1$ mol N₂.",
                  "$2.00$ mol N₂ → $4.00$ mol NH₃.",
                  "Mass $=4.00\\times 17.0=68.0$ g.",
                  "Do not use $3.00$ from the H₂ coefficient; N₂ was the given."],
                 "$68.0$ g", "", "Hard"),
        ("Treating coefficients as grams",
         "The $2$ in $2\\,\\mathrm{H_2O}$ is two moles of water, $36$ g, not $2$ g. Always pass through moles."),
        ("Write the mole ratio as a fraction with units",
         "$\\dfrac{2\\ \\mathrm{mol\\ H_2O}}{1\\ \\mathrm{mol\\ O_2}}$ makes the cancellation visible and prevents "
         "inverting the ratio."),
        [
            "I can convert moles of reactant to moles of product with a coefficient ratio.",
            "I can extend the chain to grams using molar mass.",
            "I can compute percent yield from actual and theoretical masses.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Limiting reactant",
        [
            "The limiting reactant is the reactant that is used up first. It sets the maximum amount of product. "
            "The other reactant is in excess and some of it will be left over. You cannot decide the limiter by "
            "comparing masses alone; you must compare moles to the required ratio.",
            "Classic: $2\\,\\mathrm{H_2 + O_2 \\rightarrow 2\\,H_2O}$ with $4.00$ mol H₂ and $1.00$ mol O₂. "
            "The equation wants $2$ mol H₂ per $1$ mol O₂. To use $1.00$ mol O₂ you need $2.00$ mol H₂. You have "
            "$4.00$ mol H₂, so H₂ is excess and O₂ limits. Water produced: $2.00$ mol. Leftover H₂: $2.00$ mol.",
            "A visual: four H₂ molecules and one O₂ molecule make two H₂O molecules, with two H₂ unused. Counting "
            "particles is the same logic as counting moles.",
            "Method: pick one reactant, compute how much of the other is required, compare with how much you "
            "have. If you have less than required, that second reactant limits. Then compute product from the "
            "limiter only.",
            "Aluminum example: $2\\,\\mathrm{Al + 3\\,CuCl_2 \\rightarrow 2\\,AlCl_3 + 3\\,Cu}$. With $0.400$ mol "
            "Al you need $0.600$ mol CuCl₂. If only $0.450$ mol CuCl₂ is present, CuCl₂ limits. Copper metal: "
            "$0.450$ mol (1:1 with CuCl₂).",
            "Theoretical yield always comes from the limiter. Percent yield then uses that theoretical amount. "
            "Mixing leftover excess into the product mass is a lab error and an FRQ trap.",
        ],
        "Limiting-reactant arithmetic is on every AP Chemistry exam. It is also how you later decide which "
        "species remains after a precipitation or a titration past the endpoint.",
        "Convert both givens to moles. Use the ratio to see which runs out. Compute product from that reactant "
        "only. Subtract to find leftover excess.",
        lesson_figure(
            _limiting_svg(),
            "Four H₂ and one O₂: oxygen limits",
            "Two water molecules form. Two H₂ molecules remain. The leftover hydrogen does not make extra water "
            "because there is no oxygen left.",
        )
        + solved(7, "$2\\,\\mathrm{H_2+O_2\\rightarrow 2\\,H_2O}$ with $4.00$ mol H₂ and $1.00$ mol O₂. What limits?",
               ["Need $2$ mol H₂ per $1$ mol O₂.",
                "For $1.00$ mol O₂ you need $2.00$ mol H₂; you have $4.00$ mol H₂.",
                "O₂ is used up first: O₂ limits."],
               "O₂", "", "Easy")
        + solved(8, "In that mixture, moles of H₂O produced and moles of leftover H₂?",
                 ["O₂ limits: $1.00$ mol O₂ → $2.00$ mol H₂O.",
                  "H₂ consumed $=2.00$ mol (the 2:1 ratio).",
                  "Leftover H₂ $=4.00-2.00=2.00$ mol.",
                  "Check: leftover cannot be negative."],
                 "$2.00$ mol H₂O; $2.00$ mol H₂ left", "", "Medium")
        + solved(9, "$2\\,\\mathrm{Al+3\\,CuCl_2\\rightarrow 2\\,AlCl_3+3\\,Cu}$ with $0.400$ mol Al and $0.450$ mol CuCl₂. Limiter and moles of Cu?",
                 ["$0.400$ mol Al would need $0.400\\times(3/2)=0.600$ mol CuCl₂.",
                  "Only $0.450$ mol CuCl₂ is available, so CuCl₂ limits.",
                  "Cu produced $=0.450$ mol (coefficient ratio $3/3=1$).",
                  "Al leftover $=0.400-0.450\\times(2/3)=0.400-0.300=0.100$ mol."],
                 "CuCl₂ limits; $0.450$ mol Cu", "", "Hard"),
        ("Picking the reactant with the smaller mass as the limiter",
         "2 g of H₂ is $1$ mol; 16 g of O₂ is $0.50$ mol. The masses alone do not tell you the limiter. Convert "
         "to moles and use the balanced ratio."),
        ("Make two columns: available vs required",
         "A two-row table (H₂ and O₂) with “have” and “need” makes the limiter obvious and gives leftover as "
         "a subtraction."),
        [
            "I can identify a limiting reactant from moles and a ratio.",
            "I can compute product from the limiter only.",
            "I can find leftover excess reactant.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Titration intro",
        [
            "A titration measures the concentration of an unknown solution by reacting it with a standard "
            "solution of known concentration. At the equivalence point, moles of acid and base have been matched "
            "according to the balanced equation — not necessarily equal volumes.",
            "For HCl + NaOH → NaCl + H₂O, the mole ratio is $1:1$. If $25.0$ mL of $0.100$ M HCl is used, "
            "$n_{\\mathrm{H^+}}=(0.100)(0.0250)=0.00250$ mol, so you need $0.00250$ mol NaOH. At $0.100$ M that "
            "is $25.0$ mL of base.",
            "Unequal concentrations: $40.0$ mL of $0.100$ M NaOH delivers $0.00400$ mol OH⁻. If the acid volume "
            "was $20.0$ mL, $M_{\\mathrm{HCl}}=0.00400/0.0200=0.200$ M. Write millimoles if you prefer: "
            "$40.0\\times 0.100=4.00$ mmol, divided by $20.0$ mL is $0.200$ M.",
            "Diprotic acids double the proton count: $20.0$ mL of $0.100$ M H₂SO₄ supplies $0.00200$ mol H₂SO₄ "
            "and $0.00400$ mol H⁺ if both protons neutralize, so $40.0$ mL of $0.100$ M NaOH is required.",
            "The indicator changes color near the equivalence point. For strong acid / strong base, pH jumps "
            "through $7$ at $25^\\circ$C, and phenolphthalein (colorless to pink near pH 8–9) is a common choice. "
            "The full curve shape is Unit 8; here you need moles and the steep jump idea.",
            "Buret volume is final minus initial. $18.90-2.40=16.50$ mL delivered. Using the final reading alone "
            "is a lab error that ruins the unknown's molarity.",
        ],
        "Titration is the laboratory version of stoichiometry. Later you will overlay weak-acid equilibria on "
        "the same mole counting.",
        "Compute moles from the known solution ($M\\times V$ with $V$ in liters). Use the balanced ratio. Divide "
        "moles of unknown by its volume to get molarity.",
        lesson_figure(
            titration_svg(),
            "Strong-acid / strong-base titration sketch",
            "pH starts low, stays buffered-looking only weakly, then jumps vertically near equivalence (eq. pt.) "
            "and levels off in excess base. Unit 8 will add weak-acid and buffer shapes.",
        )
        + solved(10, "$25.0$ mL of $0.100$ M HCl titrated with $0.100$ M NaOH. Volume of NaOH at equivalence?",
               ["$n_{\\mathrm{HCl}}=(0.100)(0.0250)=0.00250$ mol.",
                "Ratio $1:1$, so $n_{\\mathrm{NaOH}}=0.00250$ mol.",
                "$V=0.00250/0.100=0.0250$ L $=25.0$ mL."],
               "$25.0$ mL", "", "Easy")
        + solved(11, "$40.0$ mL of $0.100$ M NaOH titrates $20.0$ mL of HCl. Find $M_{\\mathrm{HCl}}$.",
                 ["$n_{\\mathrm{OH^-}}=(0.100)(0.0400)=0.00400$ mol.",
                  "At equivalence $n_{\\mathrm{H^+}}=0.00400$ mol.",
                  "$M=0.00400/0.0200=0.200$ M."],
                 "$0.200$ M", "", "Medium")
        + solved(12, "$20.0$ mL of $0.100$ M H₂SO₄ (both protons) with $0.100$ M NaOH. Volume of NaOH?",
                 ["$n_{\\mathrm{H_2SO_4}}=(0.100)(0.0200)=0.00200$ mol.",
                  "Two H⁺ per H₂SO₄ → $0.00400$ mol H⁺.",
                  "Need $0.00400$ mol NaOH.",
                  "$V=0.00400/0.100=0.0400$ L $=40.0$ mL."],
                 "$40.0$ mL", "Forgetting the $2$ H⁺ is the usual error.", "Hard"),
        ("Assuming equal volumes mean equivalence",
         "Equivalence is equal moles (adjusted by the ratio), not equal milliliters, unless the concentrations "
         "and coefficients happen to match."),
        ("Convert mL to L when using $M=n/V$, or stay in millimoles",
         "$M\\times \\mathrm{mL} = \\mathrm{mmol}$. Then mmol / mL = M. Mixing L and mL without converting "
         "shifts the answer by 1000."),
        [
            "I can find moles delivered from $M\\times V$.",
            "I can solve for unknown molarity at equivalence.",
            "I can account for diprotic acids with a $2:1$ proton ratio.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Redox identification",
        [
            "Oxidation is loss of electrons; reduction is gain of electrons. The reducing agent is oxidized "
            "(it donates electrons). The oxidizing agent is reduced (it takes electrons). In "
            "$\\mathrm{Cu + 2\\,Ag^+ \\rightarrow Cu^{2+} + 2\\,Ag}$, copper is oxidized and is the reducing agent; "
            "Ag⁺ is reduced and is the oxidizing agent.",
            "Oxidation numbers are a bookkeeping tool. Elemental atoms are $0$. Oxygen is usually $-2$ (except "
            "peroxides). Hydrogen is usually $+1$ (except metal hydrides). The numbers in a compound sum to "
            "zero; in an ion they sum to the ion charge.",
            "S in SO₄²⁻: $S + 4(-2) = -2$, so $S=+6$. N in NO₃⁻: $N+3(-2)=-1$, so $N=+5$. Cr in Cr₂O₇²⁻: "
            "$2\\,Cr + 7(-2) = -2$, so $2\\,Cr=+12$, $Cr=+6$. Mn in MnO₄⁻ is $+7$.",
            "A redox reaction has oxidation numbers that change. $2\\,\\mathrm{Na + Cl_2 \\rightarrow 2\\,NaCl}$ "
            "is redox (Na $0\\rightarrow +1$, Cl $0\\rightarrow -1$). AgNO₃ + NaCl precipitation is not redox; "
            "charges of Ag⁺ and Cl⁻ do not change when they form AgCl(s).",
            "Electron count must match. Each Cu loses $2e^-$; each Ag⁺ gains $1e^-$, so two Ag⁺ are needed per "
            "Cu. That is the same arithmetic you will use in electrochemistry (Unit 8) for $n$ in $q=nF$ and "
            "in balancing MnO₄⁻ half-reactions (Mn gains $5e^-$).",
            "Assign oxidation numbers first, then say which element increased (oxidized) and which decreased "
            "(reduced). Do not guess from “a metal is present.”",
        ],
        "Redox identification is the on-ramp to galvanic cells. If you cannot say what is oxidized, you cannot "
        "label an anode.",
        "Assign oxidation numbers to every element. Find the increase (oxidation) and the decrease (reduction). "
        "Name the agents as the entire species that contains that element.",
        lesson_figure(
            _redox_flow(),
            "Electrons flow from the species being oxidized to the species being reduced",
            "Zn metal would similarly reduce Cu²⁺. Oxidation happens at the electron source; reduction happens "
            "where electrons arrive.",
        )
        + solved(13, "In $\\mathrm{Cu+2Ag^+\\rightarrow Cu^{2+}+2Ag}$, what is oxidized?",
               ["Cu goes from $0$ (element) to $+2$.",
                "Oxidation number increased: copper lost electrons.",
                "Cu is oxidized (and is the reducing agent)."],
               "Cu", "", "Easy")
        + solved(14, "Oxidation number of S in SO₄²⁻?",
                 ["Four oxygens at $-2$ each contribute $-8$.",
                  "The ion charge is $-2$.",
                  "$S + (-8) = -2$, so $S=+6$."],
                 "$+6$", "", "Medium")
        + solved(15, "In $\\mathrm{MnO_4^- + Fe^{2+} \\rightarrow Mn^{2+} + Fe^{3+}}$ (acid), how many Fe²⁺ are oxidized per MnO₄⁻?",
                 ["Mn goes from $+7$ in permanganate to $+2$: it gains $5e^-$.",
                  "Each Fe²⁺ → Fe³⁺ loses $1e^-$.",
                  "Five Fe²⁺ supply the five electrons.",
                  "The balanced ratio is $1\\,\\mathrm{MnO_4^-}:5\\,\\mathrm{Fe^{2+}}$."],
                 "5", "", "Hard"),
        ("Calling precipitation redox because a solid appears",
         "Ag⁺ and Cl⁻ keep the same oxidation numbers in AgCl(s). A new phase is not automatically a redox "
         "event. Check oxidation numbers."),
        ("Write the old and new oxidation numbers above the atoms",
         "A tiny $+7\\rightarrow +2$ annotation on Mn makes the five-electron count obvious before you balance "
         "the rest of the half-reaction."),
        [
            "I can identify oxidation as electron loss and reduction as electron gain.",
            "I can assign oxidation numbers in polyatomic ions.",
            "I can match electron counts between two half-reactions.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Types of reactions",
        [
            "AP Chemistry still uses classification as a quick recognition tool: synthesis (combination), "
            "decomposition, single replacement, double replacement (including precipitation and some "
            "neutralizations), combustion, and acid–base. Many reactions are two types at once (synthesis and redox).",
            "Synthesis: $2\\,\\mathrm{Mg + O_2 \\rightarrow 2\\,MgO}$. Decomposition: "
            "$\\mathrm{CaCO_3 \\rightarrow CaO + CO_2}$ or $2\\,\\mathrm{KClO_3 \\rightarrow 2\\,KCl + 3\\,O_2}$. "
            "Single replacement: $\\mathrm{Zn + CuSO_4 \\rightarrow ZnSO_4 + Cu}$ (also redox).",
            "Double replacement swaps ions: $\\mathrm{AgNO_3 + NaCl \\rightarrow AgCl(s) + NaNO_3}$. Combustion of "
            "a hydrocarbon: $\\mathrm{CH_4 + 2\\,O_2 \\rightarrow CO_2 + 2\\,H_2O}$. Neutralization is acid + base "
            "to water and a salt.",
            "Not every double replacement happens: you need a driving force — a precipitate, a gas (CO₂ from "
            "carbonate + acid), or water (acid–base). Mixing NaCl(aq) and KNO₃(aq) is just a mixture of ions.",
            "Balancing is part of classification work. $2\\,\\mathrm{C_2H_6 + 7\\,O_2 \\rightarrow 4\\,CO_2 + 6\\,H_2O}$ "
            "has $4$ C, $12$ H, and $14$ O on both sides. An unbalanced combustion equation cannot give a correct "
            "mole ratio.",
            "On mixed FRQs you may need to classify, write net ionic, identify redox, and do limiting-reactant "
            "math on the same prompt. Practice seeing those layers instead of treating them as separate chapters.",
        ],
        "Classification is pattern recognition that speeds up net ionic and redox decisions. Combustion "
        "stoichiometry is a favorite quantitative follow-up.",
        "Name the pattern, check for a driving force, then balance. If oxidation numbers change, also label it "
        "redox.",
        lesson_figure(
            _redox_flow(),
            "Single replacement is often redox",
            "A more active metal (Zn) donates electrons to a metal ion (Cu²⁺). Double replacement precipitation "
            "usually is not redox.",
        )
        + solved(16, "Classify $2\\,\\mathrm{Mg+O_2\\rightarrow 2\\,MgO}$.",
               ["Two elements form one compound: synthesis.",
                "Mg $0\\rightarrow +2$ and O $0\\rightarrow -2$: also redox.",
                "Both labels are correct."],
               "synthesis and redox", "", "Easy")
        + solved(17, "Classify $\\mathrm{CH_4+2O_2\\rightarrow CO_2+2H_2O}$.",
                 ["A hydrocarbon reacts with oxygen to give CO₂ and H₂O.",
                  "That is combustion.",
                  "It is also redox (C is oxidized, O is reduced)."],
                 "combustion (and redox)", "", "Medium")
        + solved(18, "Is $\\mathrm{AgNO_3(aq)+NaCl(aq)\\rightarrow AgCl(s)+NaNO_3(aq)}$ redox? Classify it.",
                 ["Ag stays $+1$; Cl stays $-1$; Na stays $+1$; N stays $+5$.",
                  "No oxidation number changes: not redox.",
                  "Ions swap partners and a solid forms: double replacement / precipitation.",
                  "The net ionic equation is Ag⁺ + Cl⁻ → AgCl(s)."],
                 "precipitation, not redox", "", "Hard"),
        ("Forcing every reaction into exactly one type",
         "Synthesis of MgO is also redox. Combustion is also redox. Use as many accurate labels as the prompt "
         "asks for."),
        ("Look for the driving force in double replacement",
         "If no solid, gas, or water forms, there is no net reaction. “NaCl + KNO₃” is not a chemistry event."),
        [
            "I can classify synthesis, decomposition, single and double replacement, and combustion.",
            "I can recognize when a reaction is also redox.",
            "I can balance a hydrocarbon combustion equation.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        ["Net ionic equations", "Stoichiometry", "Limiting reactant",
         "Titration intro", "Redox identification", "Types of reactions"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
