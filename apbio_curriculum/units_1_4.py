"""AP Biology units 1–4: Chemistry of Life through Cell Communication and Cell Cycle."""
from __future__ import annotations

import math

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block,
    solved,
    practice_slots,
    unit_shell,
    mq,
    xy_graph,
    sample_curve,
    animal_cell_svg,
    beaker_svg,
    energy_diagram_svg,
    atom_shells_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _hbond_svg(w=320, h=170):
    """Two waters: donor H points at acceptor O; dashed H···O (not O···O)."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="70" y1="85" x2="42" y2="52" stroke="#0f172a" stroke-width="2.2"/>'
        f'<line x1="70" y1="85" x2="118" y2="85" stroke="#0f172a" stroke-width="2.2"/>'
        f'<circle cx="70" cy="85" r="20" fill="#ef4444" stroke="#7f1d1d" stroke-width="2"/>'
        f'<text x="70" y="90" text-anchor="middle" font-size="13" fill="#fff">O</text>'
        f'<circle cx="42" cy="52" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        f'<text x="42" y="56" text-anchor="middle" font-size="11">H</text>'
        f'<circle cx="118" cy="85" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        f'<text x="118" y="89" text-anchor="middle" font-size="11">H</text>'
        f'<text x="118" y="72" text-anchor="middle" font-size="10" fill="#1d4ed8">δ+</text>'
        f'<line x1="130" y1="85" x2="178" y2="85" stroke="#64748b" stroke-width="2.6" stroke-dasharray="6 4"/>'
        f'<text x="154" y="74" text-anchor="middle" font-size="11" fill="#334155">H-bond</text>'
        f'<line x1="200" y1="85" x2="232" y2="52" stroke="#0f172a" stroke-width="2.2"/>'
        f'<line x1="200" y1="85" x2="232" y2="118" stroke="#0f172a" stroke-width="2.2"/>'
        f'<circle cx="200" cy="85" r="20" fill="#ef4444" stroke="#7f1d1d" stroke-width="2"/>'
        f'<text x="200" y="90" text-anchor="middle" font-size="13" fill="#fff">O</text>'
        f'<text x="200" y="62" text-anchor="middle" font-size="10" fill="#b91c1c">δ−</text>'
        f'<circle cx="232" cy="52" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        f'<text x="232" y="56" text-anchor="middle" font-size="11">H</text>'
        f'<circle cx="232" cy="118" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        f'<text x="232" y="122" text-anchor="middle" font-size="11">H</text>'
        f'<text x="160" y="155" text-anchor="middle" font-size="12">dashed: δ+ H of one water to δ− O of the other</text>'
        f"</svg>"
    )


def _lipid_carb_svg(w=340, h=170):
    """Hexose ring beside a fatty-acid chain."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<polygon points="40,90 70,50 120,50 150,90 120,130 70,130" fill="#fef3c7" stroke="#b45309" stroke-width="2"/>'
        f'<text x="95" y="95" text-anchor="middle" font-size="12">C6</text>'
        f'<text x="95" y="158" text-anchor="middle" font-size="11">monosaccharide</text>'
        f'<rect x="190" y="40" width="28" height="22" rx="4" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="204" y="55" text-anchor="middle" font-size="10">COOH</text>'
        f'<line x1="218" y1="51" x2="310" y2="51" stroke="#0f172a" stroke-width="3"/>'
        f'<line x1="218" y1="78" x2="290" y2="78" stroke="#0f172a" stroke-width="3"/>'
        f'<line x1="236" y1="51" x2="236" y2="78" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="258" y1="51" x2="258" y2="78" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="280" y1="51" x2="280" y2="78" stroke="#0f172a" stroke-width="2"/>'
        f'<text x="250" y="115" text-anchor="middle" font-size="11">fatty acid (hydrophobic tail)</text>'
        f"</svg>"
    )


def _aa_svg(w=320, h=140):
    """Amino acid backbone with labeled groups."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="50" width="70" height="36" rx="8" fill="#bfdbfe" stroke="#1e3a8a"/>'
        f'<text x="55" y="73" text-anchor="middle" font-size="13">H₂N</text>'
        f'<rect x="110" y="50" width="70" height="36" rx="8" fill="#e2e8f0" stroke="#334155"/>'
        f'<text x="145" y="73" text-anchor="middle" font-size="13">Cα–H</text>'
        f'<rect x="200" y="50" width="90" height="36" rx="8" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="245" y="73" text-anchor="middle" font-size="13">COOH</text>'
        f'<rect x="122" y="8" width="48" height="28" rx="6" fill="#bbf7d0" stroke="#166534"/>'
        f'<text x="146" y="27" text-anchor="middle" font-size="12">R</text>'
        f'<line x1="146" y1="36" x2="146" y2="50" stroke="#0f172a"/>'
        f'<text x="55" y="110" text-anchor="middle" font-size="11">amino</text>'
        f'<text x="245" y="110" text-anchor="middle" font-size="11">carboxyl</text>'
        f'<text x="146" y="132" text-anchor="middle" font-size="11">side chain decides chemistry</text>'
        f"</svg>"
    )


def _enzyme_ea_svg(w=320, h=190):
    """Uncatalyzed and catalyzed paths: same ΔG, lower Ea with enzyme."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="28" y1="160" x2="305" y2="160" stroke="#0f172a"/>'
        f'<line x1="28" y1="18" x2="28" y2="160" stroke="#0f172a"/>'
        f'<path d="M40 118 C90 118, 110 32, 155 28 C200 28, 220 100, 290 108" fill="none" stroke="#b45309" stroke-width="2.4"/>'
        f'<path d="M40 118 C90 118, 115 78, 155 74 C195 74, 220 100, 290 108" fill="none" stroke="#15803d" stroke-width="2.4"/>'
        f'<line x1="72" y1="118" x2="72" y2="36" stroke="#b45309" stroke-dasharray="3 3"/>'
        f'<text x="76" y="80" font-size="10" fill="#b45309">Ea</text>'
        f'<line x1="108" y1="118" x2="108" y2="78" stroke="#15803d" stroke-dasharray="3 3"/>'
        f'<text x="112" y="104" font-size="10" fill="#15803d">Ea</text>'
        f'<text x="36" y="110" font-size="11">reactants</text>'
        f'<text x="236" y="98" font-size="11">products</text>'
        f'<text x="168" y="22" font-size="11" fill="#b45309">uncatalyzed</text>'
        f'<text x="168" y="66" font-size="11" fill="#15803d">catalyzed</text>'
        f'<text x="8" y="24" font-size="11">E</text>'
        f'<text x="165" y="178" text-anchor="middle" font-size="11">reaction coordinate</text>'
        f"</svg>"
    )


def _lock_key_svg(w=300, h=150):
    """Enzyme active site matching a substrate."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<path d="M20 40 L120 40 L120 70 L90 70 L90 110 L50 110 L50 70 L20 70 Z" '
        f'fill="#c7d2fe" stroke="#312e81" stroke-width="2"/>'
        f'<text x="70" y="32" text-anchor="middle" font-size="12">enzyme</text>'
        f'<text x="70" y="88" text-anchor="middle" font-size="11">active site</text>'
        f'<rect x="160" y="72" width="44" height="36" fill="#fde68a" stroke="#92400e"/>'
        f'<text x="182" y="94" text-anchor="middle" font-size="11">S</text>'
        f'<text x="230" y="94" font-size="12">substrate</text>'
        f"</svg>"
    )


def _bilayer_svg(w=340, h=160):
    """Phospholipid bilayer with protein channel."""
    heads = "".join(
        f'<circle cx="{x}" cy="{y}" r="8" fill="#38bdf8" stroke="#0369a1"/>'
        for y in (36, 124)
        for x in range(28, 250, 28)
    )
    tails = "".join(
        f'<line x1="{x}" y1="44" x2="{x}" y2="116" stroke="#0f172a" stroke-width="2"/>'
        for x in range(28, 250, 28)
    )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f"{heads}{tails}"
        f'<rect x="250" y="28" width="36" height="104" rx="10" fill="#fde68a" stroke="#92400e"/>'
        f'<text x="268" y="84" text-anchor="middle" font-size="10">channel</text>'
        f'<text x="120" y="20" text-anchor="middle" font-size="11">hydrophilic heads</text>'
        f'<text x="120" y="152" text-anchor="middle" font-size="11">hydrophobic tails inside</text>'
        f"</svg>"
    )


def _diffusion_svg(w=300, h=150):
    """Particles moving down a concentration gradient."""
    dots_hi = "".join(
        f'<circle cx="{20 + 18 * i}" cy="{40 + (i % 3) * 18}" r="5" fill="#1d4ed8"/>'
        for i in range(8)
    )
    dots_lo = "".join(
        f'<circle cx="{190 + 22 * i}" cy="{50 + (i % 2) * 30}" r="5" fill="#93c5fd"/>'
        for i in range(3)
    )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="8" y="20" width="140" height="100" fill="#dbeafe" stroke="#1e3a8a"/>'
        f'<rect x="168" y="20" width="120" height="100" fill="#eff6ff" stroke="#1e3a8a"/>'
        f'<line x1="148" y1="20" x2="148" y2="120" stroke="#0f172a" stroke-width="3" stroke-dasharray="5 4"/>'
        f"{dots_hi}{dots_lo}"
        f'<text x="78" y="140" text-anchor="middle" font-size="11">high [solute]</text>'
        f'<text x="228" y="140" text-anchor="middle" font-size="11">low [solute]</text>'
        f"</svg>"
    )


def _pump_svg(w=300, h=150):
    """Membrane pump moving ions against a gradient."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="60" width="260" height="28" fill="#bae6fd" stroke="#0369a1"/>'
        f'<rect x="120" y="44" width="60" height="60" rx="8" fill="#fde68a" stroke="#92400e"/>'
        f'<text x="150" y="78" text-anchor="middle" font-size="11">pump</text>'
        f'<text x="70" y="40" font-size="12">3 Na⁺ out</text>'
        f'<polygon points="90,48 110,40 90,32" fill="#b91c1c"/>'
        f'<text x="190" y="40" font-size="12">2 K⁺ in</text>'
        f'<polygon points="210,32 230,40 210,48" fill="#15803d"/>'
        f'<text x="150" y="130" text-anchor="middle" font-size="12">ATP → ADP + Pᵢ</text>'
        f"</svg>"
    )


def _tonicity_svg(w=320, h=160):
    """Three cells: hypotonic swell, isotonic, hypertonic shrink."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="55" cy="70" r="42" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/>'
        f'<circle cx="160" cy="70" r="32" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>'
        f'<ellipse cx="265" cy="70" rx="18" ry="28" fill="#93c5fd" stroke="#1d4ed8" stroke-width="2"/>'
        f'<text x="55" y="140" text-anchor="middle" font-size="11">hypotonic</text>'
        f'<text x="160" y="140" text-anchor="middle" font-size="11">isotonic</text>'
        f'<text x="265" y="140" text-anchor="middle" font-size="11">hypertonic</text>'
        f"</svg>"
    )


def _atp_yield_svg(w=320, h=180):
    """Metabolic ATP yield: fermentation vs aerobic vs uncoupled leak-to-heat."""
    def bar(x, hgt, color, lab, nlab):
        y = 150 - hgt
        return (
            f'<rect x="{x}" y="{y}" width="44" height="{hgt}" fill="{color}" stroke="#0f172a"/>'
            f'<text x="{x + 22}" y="168" text-anchor="middle" font-size="11">{lab}</text>'
            f'<text x="{x + 22}" y="{y - 8}" text-anchor="middle" font-size="12">{nlab}</text>'
        )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="24" y1="150" x2="300" y2="150" stroke="#0f172a"/>'
        f'{bar(40, 12, "#fde68a", "ferment", "2 ATP")}'
        f'{bar(130, 120, "#86efac", "aerobic", "~30 ATP")}'
        f'{bar(220, 28, "#fecaca", "uncoupled", "heat")}'
        f'<text x="160" y="18" text-anchor="middle" font-size="12">ATP (or heat) per glucose</text>'
        f"</svg>"
    )


def _resp_boxes_svg(w=340, h=150):
    """Glycolysis → Krebs → ETC boxes."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="8" y="40" width="90" height="50" rx="8" fill="#fef3c7" stroke="#b45309"/>'
        f'<text x="53" y="70" text-anchor="middle" font-size="11">glycolysis</text>'
        f'<text x="110" y="68" font-size="16">→</text>'
        f'<rect x="130" y="40" width="90" height="50" rx="8" fill="#dcfce7" stroke="#166534"/>'
        f'<text x="175" y="70" text-anchor="middle" font-size="11">Krebs</text>'
        f'<text x="228" y="68" font-size="16">→</text>'
        f'<rect x="248" y="40" width="84" height="50" rx="8" fill="#dbeafe" stroke="#1e3a8a"/>'
        f'<text x="290" y="70" text-anchor="middle" font-size="11">ETC</text>'
        f'<text x="175" y="120" text-anchor="middle" font-size="12">glucose → ~30 ATP (aerobic)</text>'
        f"</svg>"
    )


def _chloro_svg(w=320, h=160):
    """Chloroplast with thylakoid and stroma labels."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<ellipse cx="160" cy="80" rx="140" ry="60" fill="#dcfce7" stroke="#166534" stroke-width="2"/>'
        f'<rect x="70" y="50" width="90" height="14" fill="#86efac" stroke="#166534"/>'
        f'<rect x="70" y="70" width="90" height="14" fill="#86efac" stroke="#166534"/>'
        f'<rect x="70" y="90" width="90" height="14" fill="#86efac" stroke="#166534"/>'
        f'<text x="115" y="44" text-anchor="middle" font-size="11">thylakoid (light)</text>'
        f'<text x="240" y="84" text-anchor="middle" font-size="11">stroma</text>'
        f'<text x="240" y="100" text-anchor="middle" font-size="11">(Calvin)</text>'
        f"</svg>"
    )


def _cascade_svg(w=330, h=140):
    """Ligand → receptor → relay → response."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="36" cy="70" r="16" fill="#fde68a" stroke="#92400e"/>'
        f'<text x="36" y="74" text-anchor="middle" font-size="11">L</text>'
        f'<rect x="70" y="40" width="50" height="60" rx="8" fill="#c7d2fe" stroke="#312e81"/>'
        f'<text x="95" y="74" text-anchor="middle" font-size="11">R</text>'
        f'<text x="132" y="74" font-size="16">→</text>'
        f'<rect x="150" y="50" width="50" height="40" rx="6" fill="#bbf7d0" stroke="#166534"/>'
        f'<text x="175" y="74" text-anchor="middle" font-size="11">relay</text>'
        f'<text x="208" y="74" font-size="16">→</text>'
        f'<rect x="226" y="50" width="90" height="40" rx="6" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="271" y="74" text-anchor="middle" font-size="11">response</text>'
        f'<text x="36" y="120" text-anchor="middle" font-size="11">ligand</text>'
        f'<text x="95" y="120" text-anchor="middle" font-size="11">receptor</text>'
        f"</svg>"
    )


def _feedback_svg(w=300, h=150):
    """Loop: stimulus → sensor → response back to stimulus."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="20" width="80" height="36" rx="8" fill="#dbeafe" stroke="#1e3a8a"/>'
        f'<text x="60" y="42" text-anchor="middle" font-size="12">stimulus</text>'
        f'<rect x="200" y="20" width="80" height="36" rx="8" fill="#dcfce7" stroke="#166534"/>'
        f'<text x="240" y="42" text-anchor="middle" font-size="12">response</text>'
        f'<path d="M100 38 C150 10, 170 10, 200 38" fill="none" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M200 56 C150 130, 90 130, 60 56" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<text x="150" y="118" text-anchor="middle" font-size="11" fill="#b91c1c">negative: shut the stimulus off</text>'
        f"</svg>"
    )


def _mitosis_svg(w=340, h=140):
    """Four mitosis stages as simple chromosome cartoons."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="40" cy="60" r="28" fill="#fef3c7" stroke="#b45309"/>'
        f'<line x1="28" y1="50" x2="52" y2="70" stroke="#7f1d1d" stroke-width="3"/>'
        f'<text x="40" y="110" text-anchor="middle" font-size="11">prophase</text>'
        f'<circle cx="120" cy="60" r="28" fill="#e0e7ff" stroke="#312e81"/>'
        f'<line x1="100" y1="60" x2="140" y2="60" stroke="#0f172a" stroke-width="2"/>'
        f'<rect x="112" y="52" width="16" height="16" fill="#b91c1c"/>'
        f'<text x="120" y="110" text-anchor="middle" font-size="11">metaphase</text>'
        f'<circle cx="200" cy="60" r="28" fill="#dcfce7" stroke="#166534"/>'
        f'<rect x="186" y="40" width="10" height="14" fill="#b91c1c"/>'
        f'<rect x="204" y="66" width="10" height="14" fill="#b91c1c"/>'
        f'<text x="200" y="110" text-anchor="middle" font-size="11">anaphase</text>'
        f'<ellipse cx="290" cy="48" rx="22" ry="16" fill="#fecaca" stroke="#b91c1c"/>'
        f'<ellipse cx="290" cy="78" rx="22" ry="16" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="290" y="110" text-anchor="middle" font-size="11">telophase</text>'
        f"</svg>"
    )


def _meiosis_svg(w=300, h=150):
    """Homolog pair crossing over, then splitting."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="40" y1="30" x2="40" y2="110" stroke="#1d4ed8" stroke-width="8"/>'
        f'<line x1="70" y1="30" x2="70" y2="110" stroke="#b91c1c" stroke-width="8"/>'
        f'<path d="M40 70 L70 70" stroke="#0f172a" stroke-width="3"/>'
        f'<text x="55" y="24" text-anchor="middle" font-size="11">crossing over</text>'
        f'<text x="130" y="70" font-size="18">→</text>'
        f'<line x1="180" y1="30" x2="180" y2="70" stroke="#1d4ed8" stroke-width="8"/>'
        f'<line x1="180" y1="70" x2="180" y2="110" stroke="#b91c1c" stroke-width="8"/>'
        f'<line x1="230" y1="30" x2="230" y2="70" stroke="#b91c1c" stroke-width="8"/>'
        f'<line x1="230" y1="70" x2="230" y2="110" stroke="#1d4ed8" stroke-width="8"/>'
        f'<text x="205" y="140" text-anchor="middle" font-size="11">recombinant chromatids</text>'
        f"</svg>"
    )


def _nondisj_svg(w=280, h=140):
    """Uneven chromosome split in anaphase."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="80" cy="70" r="40" fill="#fee2e2" stroke="#b91c1c"/>'
        f'<rect x="62" y="40" width="12" height="22" fill="#1d4ed8"/>'
        f'<rect x="84" y="40" width="12" height="22" fill="#1d4ed8"/>'
        f'<text x="80" y="125" text-anchor="middle" font-size="11">n+1 gamete</text>'
        f'<circle cx="200" cy="70" r="40" fill="#dbeafe" stroke="#1e3a8a"/>'
        f'<text x="200" y="74" text-anchor="middle" font-size="12">empty</text>'
        f'<text x="200" y="125" text-anchor="middle" font-size="11">n−1 gamete</text>'
        f"</svg>"
    )


def _qs(pairs):
    qs, idx = [], 1
    for text, ans, expl, dist in pairs:
        qs.append(mq(text, ans, expl, idx, distractors=dist))
        idx += 1
    return qs


# ===========================================================================
# UNIT 1: Chemistry of Life
# ===========================================================================

def _u1_questions():
    return _qs([
        ("Water sticks to other water molecules because the slightly positive hydrogen of one molecule is attracted to the slightly negative oxygen of another. That attraction is called a:",
         "hydrogen bond",
         "A hydrogen bond is a weak attraction between a partially positive H on one polar molecule and a partially negative atom (often O or N) on another. It is not a covalent bond inside one water molecule.",
         ["covalent bond inside H₂O", "ionic bond between Na⁺ and Cl⁻", "peptide bond"]),
        ("Ice floats on liquid water because hydrogen bonds in ice:",
         "hold molecules in a more open lattice, so ice is less dense",
         "In ice, each water is locked into a hexagonal lattice with more empty space than liquid water. Lower density means ice floats, which insulates lakes in winter.",
         ["pack molecules more tightly, so ice is denser", "break completely, so ice has no structure", "turn water into a nonpolar solvent"]),
        ("A water strider can walk on a pond because water molecules at the surface pull sideways on their neighbors. That surface “skin” is:",
         "surface tension from cohesion",
         "Cohesion is water sticking to water. At the air–water surface, unbalanced hydrogen bonds create surface tension strong enough to support a light insect.",
         ["adhesion to the insect’s legs only", "high specific heat of the insect", "evaporative cooling of the pond"]),
        ("It takes a large energy input to raise the temperature of a lake. Water’s high specific heat exists because:",
         "hydrogen bonds must be disrupted before molecules move faster",
         "Temperature measures average kinetic energy. Heat first loosens hydrogen bonds; only leftover energy speeds the molecules. That is why water buffers temperature on Earth and in cells.",
         ["water has no intermolecular forces", "covalent O–H bonds break first whenever you heat water", "water is nonpolar so it ignores heat"]),
        ("Sweat cools you because the water molecules that leave as vapor are the ones with the most kinetic energy. This process is:",
         "evaporative cooling",
         "The fastest molecules escape as gas, so the remaining liquid has a lower average kinetic energy (lower temperature). That is evaporative cooling.",
         ["an increase in the remaining water’s kinetic energy", "a drop in water’s heat of vaporization", "hydrogen bonds forming more tightly in the vapor"]),
        ("CHNOPS lists the six elements that make up most living mass. They are:",
         "carbon, hydrogen, nitrogen, oxygen, phosphorus, sulfur",
         "Memorize the set: C, H, N, O, P, S. Carbon’s four bonds build the backbone; the others add polarity, energy storage (P in ATP), and disulfide bridges (S).",
         ["calcium, helium, neon, oxygen, potassium, sodium", "chlorine, helium, nickel, osmium, platinum, silver", "cobalt, hafnium, niobium, osmium, palladium, scandium"]),
        ("Carbon is the backbone of biomolecules because a carbon atom can form:",
         "four stable covalent bonds, including chains and rings",
         "Carbon has four valence electrons, so it can make four covalent bonds. That lets it form long chains, branched trees, and rings — the skeletons of sugars, lipids, proteins, and nucleic acids.",
         ["only one covalent bond, like hydrogen", "an ionic lattice like NaCl in every organic molecule", "metallic bonds that conduct in DNA"]),
        ("A molecule that has both a water-loving region and a water-fearing region is called:",
         "amphipathic",
         "Amphipathic means both hydrophilic (polar or charged) and hydrophobic (nonpolar). Phospholipids are the classic example: polar heads face water, nonpolar tails hide from it.",
         ["completely hydrophobic", "a radioactive isotope only", "a noble gas"]),
        ("Trace elements such as iron and iodine are needed in tiny amounts. Iron matters in humans because it:",
         "helps hemoglobin bind oxygen",
         "A trace element is required in very small quantity but is still essential. Iron in hemoglobin’s heme group binds O₂. Iodine is needed to make thyroid hormone.",
         ["replaces carbon in DNA backbones", "is the main atom in water", "provides all of a cell’s ATP by itself"]),
        ("Dehydration synthesis joins two monomers and releases a water molecule. The reverse reaction that splits a polymer by adding water is:",
         "hydrolysis",
         "Hydrolysis (hydro = water, lysis = split) uses water to break a covalent bond between monomers. Digestion of starch, protein, and nucleic acids is hydrolysis.",
         ["dehydration synthesis again", "hydrogen bonding only", "a change of pH with no bond breaking"]),
        ("Carbohydrates are used for quick energy and structure. The monomer of a starch or glycogen chain is:",
         "a monosaccharide such as glucose",
         "Starch (plants) and glycogen (animals) are polysaccharides built from glucose monomers linked by glycosidic bonds. Cellulose is also glucose, but the bonding geometry makes a fiber we cannot digest.",
         ["an amino acid", "a fatty acid", "a nucleotide"]),
        ("Saturated fatty acids pack tightly because their hydrocarbon tails:",
         "have no C=C double bonds, so they stay straight",
         "Saturated means every carbon–carbon bond in the tail is single, so the chain is straight and stacks. Unsaturated tails have kinks from C=C bonds and stay liquid at cooler temperatures.",
         ["are full of C=C kinks that prevent packing", "are polar and dissolve in water", "contain peptide bonds"]),
        ("Phospholipids form membranes because they are amphipathic. In water they spontaneously arrange so that:",
         "polar heads face water and nonpolar tails hide from water",
         "The hydrophobic effect drives tails inward. The resulting bilayer is the basic fabric of all cell membranes.",
         ["tails face the water and heads hide inside", "both heads and tails dissolve completely", "the molecules form peptide bonds with each other"]),
        ("A triglyceride stores more energy per gram than glycogen mainly because:",
         "its C–H tails are highly reduced and anhydrous",
         "Fats are packed with C–H bonds (lots of oxidizable energy) and do not carry the water that hydrated glycogen does, so they are a denser energy store.",
         ["fat molecules contain more nitrogen than sugars", "triglycerides are polymers of glucose", "lipids cannot be oxidized"]),
        ("Lactose is a disaccharide of glucose + galactose. Breaking lactose into those two sugars is:",
         "hydrolysis of a glycosidic bond",
         "A disaccharide is two monosaccharides joined by a glycosidic (covalent) bond. Lactase catalyzes hydrolysis of that bond.",
         ["formation of a peptide bond", "hydrogen bonding between two waters", "a change only in pH"]),
        ("Proteins are polymers of amino acids. Two amino acids are joined by a:",
         "peptide bond between carboxyl and amino groups",
         "The carboxyl carbon of one amino acid bonds to the amino nitrogen of the next, releasing water. That covalent link is a peptide bond; a chain of them is a polypeptide.",
         ["glycosidic bond", "phosphodiester bond", "ionic bond that cannot be a covalent link"]),
        ("The three-dimensional fold of a single polypeptide, stabilized by R-group interactions (H-bonds, ionic bonds, hydrophobic packing, disulfides), is the:",
         "tertiary structure",
         "Primary = sequence. Secondary = local H-bonded coils/sheets. Tertiary = overall 3-D fold of one chain. Quaternary = multiple folded chains together (like hemoglobin).",
         ["primary structure only", "a nucleotide sequence", "a triglyceride fold"]),
        ("DNA stores information in the sequence of four bases. In a double helix, adenine pairs with thymine using:",
         "two hydrogen bonds, while G pairs with C using three",
         "Complementary base pairing: A–T (2 H-bonds) and G–C (3 H-bonds). That is why the two strands are predictable from each other and why GC-rich DNA is more heat-stable.",
         ["covalent peptide bonds between A and T", "ionic bonds between phosphate groups only", "three hydrogen bonds for A–T and two for G–C"]),
        ("The backbone of DNA is built from:",
         "sugar–phosphate covalent (phosphodiester) links",
         "Each nucleotide has a phosphate, a deoxyribose sugar, and a base. Phosphodiester bonds connect the sugar of one nucleotide to the phosphate of the next, forming a directional 5′→3′ backbone.",
         ["peptide bonds between bases", "hydrogen bonds along the backbone", "glycosidic bonds between fatty acids"]),
        ("A change that replaces one amino acid with another of very different chemistry (for example, charged → hydrophobic) is most likely to:",
         "alter folding and therefore function",
         "Sequence determines fold; fold determines function. A chemically unlike substitution can wreck an active site or a binding pocket. Silent DNA changes that do not change the amino acid often do nothing to the protein.",
         ["always improve the protein", "change DNA into RNA automatically", "convert the protein into a carbohydrate"]),
        ("Sickle-cell hemoglobin differs from normal hemoglobin by one amino acid in the β chain (Glu → Val). That is a change in:",
         "primary structure that then changes shape and stickiness",
         "Primary structure is the amino-acid sequence. One charged glutamate replaced by hydrophobic valine makes hemoglobin molecules clump in low oxygen, distorting red blood cells.",
         ["only the sugar in DNA", "a change from DNA to starch", "quaternary structure with no sequence change"]),
        ("Enzymes are proteins (or RNA) whose shape creates a pocket that fits a specific substrate. That pocket is the:",
         "active site",
         "The active site is the 3-D cleft where the substrate binds and the reaction is catalyzed. Complementary shape and chemistry explain specificity.",
         ["hydrophobic tail of a phospholipid", "anticodon of tRNA only", "nuclear pore"]),
        ("Why does a protein denature (lose function) when heated too far or placed in extreme pH?",
         "weak interactions that hold tertiary shape are disrupted",
         "Heat and pH swing break hydrogen bonds and ionic interactions. The chain unfolds, the active site disappears, and catalysis stops. Peptide bonds (primary structure) usually survive milder denaturation.",
         ["all peptide bonds instantly hydrolyze at 40 °C", "DNA turns into protein", "lipids become amino acids"]),
        ("Antibodies bind one antigen tightly because of complementary shape. This is the same structure–function idea as:",
         "an enzyme’s active site fitting its substrate",
         "In both cases, 3-D shape plus chemical matching (H-bonds, charges, hydrophobic patches) create specificity. AP Biology keeps returning to this theme.",
         ["a triglyceride storing glucose rings", "ice being denser than water", "a proton having no charge"]),
        ("A channel protein lets ions cross a membrane because its interior is lined with:",
         "hydrophilic amino acids that stabilize the charged ions",
         "The protein’s fold creates a hydrophilic tunnel through the hydrophobic bilayer. Structure (the lining) explains function (ion passage).",
         ["only hydrophobic amino acids that repel all ions", "cellulose fibers", "saturated fatty acids packed as starch"]),
        ("pH is a compact way to report [H⁺]. The definition is $pH=-\\log_{10}[H^+]$. If $[H^+]=10^{-3}\\,M$, pH is:",
         "3",
         "$-\\log_{10}(10^{-3})=3$. Lower pH means more H⁺ (more acidic). Each 1-unit pH drop is a 10-fold rise in [H⁺].",
         ["−3", "11", "0.003"]),
        ("A solution of pH 5 has how many times as many H⁺ ions as a solution of pH 8?",
         "1000 times as many",
         "The difference is 3 pH units, and $10^3=1000$. pH 5 is more acidic, so it has 1000-fold higher [H⁺] than pH 8.",
         ["3 times as many", "30 times as many", "1/1000 as many"]),
        ("A buffer is a mixture that resists pH change when small amounts of acid or base are added. Blood’s carbonic acid / bicarbonate system works because:",
         "added H⁺ is absorbed by HCO₃⁻, and added OH⁻ is absorbed via H₂CO₃",
         "The weak acid H₂CO₃ and its conjugate base HCO₃⁻ trade H⁺ so [H⁺] (and pH) stay nearly constant. That protects proteins whose charge and shape depend on pH.",
         ["buffers destroy all hydrogen bonds in water", "buffers convert carbon into nitrogen", "buffers raise temperature instead of pH"]),
        ("If $[H^+]=1\\times10^{-7}\\,M$ in pure water at 25 °C, pH is 7. This is called:",
         "neutral, because [H⁺] equals [OH⁻]",
         "In pure water, $K_w=[H^+][OH^-]=10^{-14}$, so each is $10^{-7}$. Neutral means those concentrations are equal, not that there are zero ions.",
         ["acidic because 7 is a large number", "basic because 7 > 1", "undefined because logs cannot be used in biology"]),
        ("Adding acid to an unbuffered cell would protonate amino-acid side chains and often unfold proteins. A buffer protects function by:",
         "keeping pH in a narrow window so charges (and folds) stay the same",
         "Protein shape depends on which R groups are charged. Stable pH means stable charges, which means stable tertiary structure and function.",
         ["raising the boiling point of the cytosol only", "removing all water from the cell", "converting proteins into nucleic acids"]),
        ("A drop of sweat on skin absorbs heat as it vaporizes. Which property of water is doing the cooling?",
         "high heat of vaporization plus evaporative cooling",
         "Many hydrogen bonds must break for a molecule to leave as gas, so vaporization removes a large amount of heat from the remaining liquid and from your skin.",
         ["water’s ability to dissolve lipids better than salts", "ice being denser than liquid water", "water having no polarity"]),
        ("Why is water a good solvent for NaCl but a poor solvent for a long hydrocarbon?",
         "water is polar, so it stabilizes ions; hydrocarbons are nonpolar",
         "The partial charges on water surround Na⁺ and Cl⁻ (hydration shells). A hydrocarbon has no partial charges to attract water, so it is hydrophobic.",
         ["water is nonpolar and oils are polar", "NaCl is held by peptide bonds", "hydrocarbons form hydrogen bonds with water more strongly than salt does"]),
        ("Capillary rise of water in a xylem tube requires both cohesion and adhesion. Adhesion is:",
         "water sticking to the polar walls of the tube",
         "Cohesion = water–water H-bonds (the column holds together). Adhesion = water–cellulose H-bonds (the column clings to the tube so it does not slip).",
         ["water turning into ice inside the tube", "ions pumping themselves uphill without ATP", "hydrophobic tails lining the xylem"]),
        ("Why can a lake stay liquid through a cold night more easily than a dry rock of equal mass?",
         "water’s high specific heat stores a lot of thermal energy per degree",
         "Hydrogen bonds soak up heat with little temperature change. That thermal inertia is why coastal climates are milder than inland deserts.",
         ["rock has more hydrogen bonds than water", "water cannot absorb any heat", "ice forming at the bottom heats the lake"]),
        ("A polar covalent O–H bond inside one water molecule is different from a hydrogen bond because the O–H bond is:",
         "a sharing of electrons within the molecule; the H-bond is a weaker attraction between molecules",
         "Do not mix intramolecular covalent bonds with intermolecular hydrogen bonds. Boiling water breaks H-bonds between molecules; it does not split H₂O into atoms under ordinary conditions.",
         ["stronger than a covalent bond", "an ionic bond between two oxygens", "a peptide link"]),
        ("Which CHNOPS element is in nucleic acids and phospholipids but is not in a typical carbohydrate?",
         "phosphorus",
         "Carbohydrates are C, H, O. Nucleic acids and phospholipids also contain P in their phosphate groups. Proteins add N (and often S); nucleic acids add N and P.",
         ["only helium", "only calcium", "only sodium"]),
        ("Why is carbon more versatile than silicon as a backbone for Earth life, in AP-style reasoning?",
         "carbon forms stable, diverse covalent chains in water-based chemistry",
         "AP wants the functional point: carbon’s bonding lets cells build large, stable, varied molecules under aqueous, moderate-temperature conditions.",
         ["silicon cannot form any covalent bonds", "carbon is a metal", "silicon dissolves fats better than carbon"]),
        ("An unsaturated phospholipid in a winter fish membrane is useful because the kinks:",
         "keep the bilayer fluid at low temperature",
         "Kinks from C=C bonds prevent tight packing, so the membrane does not freeze solid. Cells also use cholesterol in animals as a fluidity buffer.",
         ["make the membrane a rigid crystal", "convert lipids into DNA", "remove all proteins from the membrane"]),
        ("Glycogen branching lets animals:",
         "release many glucose ends quickly when energy is needed",
         "Each branch is a free end that enzymes can chip. Starch in plants is less branched (amylopectin) or unbranched (amylose), matching slower plant energy use.",
         ["store information like DNA", "form peptide bonds with fatty acids", "pump protons without proteins"]),
        ("Why does cellulose give plant cell walls strength while starch is a food store, even though both are glucose polymers?",
         "different glycosidic geometry (β vs α) changes 3-D packing and digestibility",
         "Structure (bond orientation and hydrogen-bonded fibers) creates function (support vs digestible fuel). Humans lack cellulase, so cellulose is fiber, not calories.",
         ["cellulose is a protein and starch is a nucleic acid", "starch contains phosphorus and cellulose does not", "they are made of different elements, not different bonds"]),
        ("A protein’s primary structure is determined by:",
         "the gene’s DNA sequence, via transcription and translation",
         "DNA → mRNA → polypeptide sequence. Everything about higher-level fold starts from that order of amino acids.",
         ["random collision of lipids in the membrane", "the pH of rain", "the number of mitochondria only"]),
        ("Disulfide bridges (–S–S–) form between cysteine side chains. They are part of:",
         "tertiary (or quaternary) covalent stabilization",
         "Cysteines contain sulfur. Covalent disulfides lock a fold more tightly than H-bonds alone — important in secreted proteins like antibodies and insulin.",
         ["the sugar-phosphate DNA backbone", "glycosidic bonds in starch", "hydrogen bonds in ice only"]),
        ("If a stretch of DNA is 30% adenine, the percent thymine in that double-stranded DNA is:",
         "30%",
         "Chargaff’s rule: A = T and G = C in double-stranded DNA. If A is 30%, T is 30%, leaving 40% for G+C, so G = C = 20%.",
         ["70%", "20%", "40%"]),
        ("RNA differs from DNA in three textbook ways. One correct difference is:",
         "RNA has ribose and usually uracil; DNA has deoxyribose and thymine",
         "RNA is typically single-stranded with U instead of T and an extra –OH on the sugar. That extra –OH makes RNA less stable, which fits a short-lived messenger.",
         ["RNA uses peptide bonds in its backbone", "DNA is built from amino acids", "RNA cannot form hydrogen bonds"]),
        ("Why can a single amino-acid substitution destroy enzyme activity even if 99% of the chain is unchanged?",
         "one wrong R group in the active site can ruin substrate binding or catalysis",
         "Function is local as well as global. A catalytic residue or a shape-critical glycine-to-tryptophan swap can zero out activity.",
         ["primary structure never affects function", "enzymes are lipids so sequence is irrelevant", "all substitutions increase $k_{cat}$"]),
        ("A student claims “hydrophobic amino acids always sit on the protein surface.” The correction is:",
         "hydrophobic R groups usually pack in the core, away from water",
         "The hydrophobic effect drives nonpolar side chains inward in soluble proteins. Polar/charged groups more often face water. Membrane proteins are the exception: hydrophobic belts contact lipid tails.",
         ["all R groups are hydrophilic", "proteins have no interior", "hydrophobic means water-loving"]),
        ("AP Stretch: A plant cell’s vacuole sap is pH 5 while the cytosol is pH 7. The [H⁺] ratio (vacuole:cytosol) is $10^{2}=100$. Maintaining that gradient requires:",
         "active proton pumping, because H⁺ is moving toward a region already high in H⁺",
         "pH 5 vs 7 is a 100-fold [H⁺] difference. Protons are concentrated in the vacuole against their gradient, which requires energy (ATP-driven H⁺ pumps). Passive leak would equalize pH.",
         ["only diffusion through an open pore, which could build the gradient", "buffers destroying the membrane", "ice forming in the vacuole to trap H⁺"]),
        ("AP Stretch: You heat a DNA duplex until strands separate. A GC-rich fragment melts at a higher temperature than an AT-rich fragment of the same length because:",
         "G–C pairs have three hydrogen bonds, so more heat is needed to separate strands",
         "Stacking plus the extra H-bond per GC pair raises thermal stability. PCR primer design uses this: melting temperature tracks GC content.",
         ["A–T pairs are covalent and cannot melt", "GC pairs have no hydrogen bonds", "DNA backbones break before base pairs"]),
        ("AP Stretch: Oleic acid (one cis double bond) vs stearic acid (saturated), same chain length, in a phospholipid. At 4 °C, the membrane with more oleic acid stays fluid because:",
         "cis kinks disrupt packing, lowering the temperature at which tails freeze into a gel",
         "This is homeoviscous adaptation: cold-water organisms enrich unsaturated lipids. Trans fats pack more like saturates; cis kinks are the biologically common fluidizer.",
         ["oleic acid forms peptide bonds with water", "saturated tails always stay liquid", "double bonds convert the lipid into glucose"]),
        ("AP Stretch: Histidine’s side chain pKa is near 6. At pH 5 vs pH 8, the fraction protonated changes sharply. That matters for enzymes because:",
         "charge on a catalytic residue can appear or vanish, turning catalysis on or off",
         "Buffers keep pH near the pKa window where histidine can both donate and accept protons — a reason it is common in active sites. Extreme pH locks it in one charge state.",
         ["pKa values never affect proteins", "histidine is a sugar", "pH only changes DNA sequence"]),
        ("AP Stretch: A 100-residue protein has a buried salt bridge (Lys⁺…Glu⁻). Mutating Lys to uncharged Leu often unfolds the protein because:",
         "you leave an unpaired buried charge (Glu⁻) that is unstable in a hydrophobic core",
         "Unsatisfied charges in low-dielectric interiors are costly. Either both partners change, or the fold rearranges to expose the remaining charge — often losing function.",
         ["Leu always forms a stronger salt bridge", "primary sequence cannot affect fold", "Glu becomes a nucleotide"]),
        ("AP Stretch: Water’s cohesion lets a transpiration stream rise. If air bubbles break the continuous water column (cavitation), transport stops because:",
         "hydrogen-bonded continuity is required to pull the whole column",
         "The cohesion-tension mechanism is a physical hydrogen-bond chain under tension. A bubble is a break in that chain; adhesion to walls cannot jump a gas gap.",
         ["xylem then pumps water with ATP in every cell wall", "bubbles increase cohesion", "water becomes nonpolar in xylem"]),
        ("AP Stretch: Equal masses of glucose vs a triglyceride are oxidized. The fat yields more ATP per gram primarily because:",
         "carbons in fatty-acid tails are more reduced (more C–H, less oxygen already present)",
         "Oxidation energy tracks how far carbons have to go to CO₂. Sugars are already partly oxidized (C–O). Fats are energy-dense and anhydrous.",
         ["glucose contains more C–H bonds per gram than fat", "nitrogen in fat is oxidized instead of carbon", "glycogen has more calories because it is wet"]),
        ("AP Stretch: A buffer is most effective when pH is near the weak acid’s pKa. If pKa = 7.4 and blood pH = 7.4, adding a small amount of H⁺ will:",
         "convert some A⁻ to HA, so [H⁺] rises far less than in unbuffered water",
         "HA ⇌ H⁺ + A⁻. Extra H⁺ is soaked up by A⁻. The ratio HA/A⁻ shifts, but pH barely moves — until the buffer is exhausted.",
         ["destroy all bicarbonate immediately with no pH change possible later", "lower pH by exactly 7.4 units", "raise pH because acids are bases in blood"]),
        ("AP Stretch: Real ice is about $0.917\\,g/cm^3$ vs liquid water $1.00\\,g/cm^3$. A $40.0\\,g$ ice cube therefore has volume $40.0/0.917\\approx43.6\\,cm^3$ and displaces only $40.0\\,g$ of water while floating. If hydrogen-bond geometry instead made ice $1.08\\,g/cm^3$, that same $40.0\\,g$ of ice would:",
         "sink (it is denser than liquid), so a pond would freeze from the bottom and could solidify upward",
         "Buoyancy: an object sinks when its density exceeds the fluid’s. $1.08>1.00$, so ice would not form an insulating lid. Heat would keep leaving from the open surface while solid ice accumulated on the sediment, shrinking the liquid refuge. The $40.0\\,g$ block’s volume would be $40.0/1.08\\approx37.0\\,cm^3$, less than the $40.0\\,cm^3$ of water with the same mass — a quantitative sink, not the usual ‘ice floats so fish live’ slogan.",
         ["still float, because all ice must be less dense than water", "float higher, because $1.08>0.917$ means more buoyancy", "boil the lake, because denser ice has no hydrogen bonds"]),
    ])


def build_unit1():
    title = "AP Biology Unit 1: Chemistry of Life"
    description = (
        "Water’s hydrogen bonds, the CHNOPS toolkit, the four macromolecule families, "
        "how shape creates function, and pH/buffers — taught with diagrams and fully worked examples."
    )

    c1 = concept_block(
        "1. Water and hydrogen bonding",
        [
            "A water molecule is bent, with oxygen hogging electrons more than hydrogen. That unequal sharing is a polar covalent bond: oxygen carries a partial negative charge, and each hydrogen carries a partial positive charge.",
            "The attraction between the $\\delta^+$ hydrogen of one water and the $\\delta^-$ oxygen of another is a hydrogen bond. Each bond is weak compared with a covalent O–H bond, but a huge number of them acting together give water its unusual properties.",
            "Cohesion means water sticks to water. That is why a water column in xylem can be pulled as a unit, and why a pond has surface tension. Adhesion means water sticks to other polar surfaces, such as cellulose in a plant wall.",
            "Specific heat is the energy needed to raise $1\\,g$ of a substance by $1^{\\circ}C$. Water’s value is high because incoming heat first disrupts hydrogen bonds; only then do molecules speed up. Lakes therefore change temperature slowly.",
            "Heat of vaporization is also high. When the fastest molecules leave as gas, they take energy with them. That is evaporative cooling — the reason sweating and transpiration dump heat.",
            "Ice is less dense than liquid water because hydrogen bonds lock molecules into an open hexagonal lattice. Floating ice insulates the water below, a structure–function story that reaches from molecules to ecosystems.",
        ],
        "Every later unit assumes you know why water is the solvent of life: polarity, hydrogen bonds, and the hydrophobic effect that folds proteins and builds membranes.",
        "For any water question, name the level: covalent bond inside one molecule, or hydrogen bond between molecules. Then connect that interaction to the property (cohesion, solvent, specific heat, ice density).",
        lesson_figure(
            _hbond_svg(),
            "Two water molecules and a hydrogen bond",
            "Dashed line: intermolecular hydrogen bond. Solid O–H links inside each molecule are polar covalent bonds.",
        )
        + solved(1, "Name the attraction that lets a water strider stand on a pond, and say which molecules are sticking together.",
                 ["The insect is supported by the ‘skin’ of the pond, called surface tension.",
                  "Surface tension exists because water molecules pull on neighboring water molecules.",
                  "That water–water sticking is cohesion, caused by hydrogen bonds."],
                 "cohesion / hydrogen bonds (surface tension)", "", "Easy")
        + solved(2, "A $1\\,kg$ rock and $1\\,kg$ of water absorb the same heat. Which rises more in temperature, and why?",
                 ["Specific heat of water is higher because hydrogen bonds absorb energy before kinetic energy (temperature) rises.",
                  "The rock has weaker intermolecular attractions, so the same energy goes more directly into molecular motion.",
                  "Therefore the rock’s temperature increases more than the water’s."],
                 "the rock; water’s high specific heat", "", "Medium")
        + solved(3, "Explain, in one causal chain, why a deep lake can stay liquid under ice in January.",
                 ["Hydrogen bonds in ice hold water in a spacious lattice, so ice is less dense than liquid water and floats.",
                  "The floating layer is a poor conductor and slows heat loss from the water below.",
                  "Water’s high specific heat further resists freezing of the whole lake.",
                  "Aquatic organisms remain in liquid water under the ice."],
                 "floating ice + high specific heat insulate liquid water below",
                 "AP loves this chain: molecular structure → density → habitat.", "Hard"),
        ("Calling every O–H interaction a hydrogen bond",
         "The O–H link inside one water molecule is a polar covalent bond (electrons shared). A hydrogen bond is the weaker attraction between two different molecules. Boiling breaks hydrogen bonds between molecules; it does not normally split water into atoms."),
        ("Label charges before you pick a property",
         "Sketch $\\delta^-$ on oxygen and $\\delta^+$ on hydrogens. Cohesion, adhesion, solvent behavior, and ice structure all fall out of those partial charges."),
        [
            "I can distinguish polar covalent bonds inside water from hydrogen bonds between water molecules.",
            "I can connect cohesion, adhesion, specific heat, and evaporative cooling to hydrogen bonding.",
            "I can explain why ice floats and why that matters for aquatic life.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Elements of life and CHNOPS",
        [
            "Living things are built from a short list of elements. The six that dominate biomass are carbon, hydrogen, nitrogen, oxygen, phosphorus, and sulfur — remembered as CHNOPS.",
            "Carbon is the backbone atom because it can form four covalent bonds at once. It builds chains, branches, and rings, so a small set of monomers can make huge, varied polymers.",
            "Functional groups are clusters of atoms that give a molecule its chemical personality. Hydroxyl (–OH) is polar and water-loving. Carboxyl (–COOH) can donate H⁺ (acid). Amino (–NH₂) can accept H⁺ (base). Phosphate stores and transfers energy. Sulfhydryl (–SH) can form disulfide bridges.",
            "A monomer is a small repeating unit. A polymer is a long chain of monomers. Cells join monomers by dehydration synthesis (remove water to make a covalent bond) and split polymers by hydrolysis (add water to break the bond).",
            "Trace elements such as Fe, I, and Zn are needed in tiny amounts but are still essential — iron in hemoglobin, iodine in thyroid hormone. Essential means the organism cannot make a substitute that does the same job.",
            "Isotopes of an element have the same proton number but different neutrons. Radioactive isotopes let researchers label DNA or date fossils; heavy isotopes (like $^{15}N$) let them trace atoms through reactions without radioactivity.",
        ],
        "Macromolecule units only make sense if you already know which atoms are available and how dehydration vs hydrolysis remodel covalent bonds.",
        "When a question shows a mystery molecule, circle the functional groups first. They tell you solubility, acid/base behavior, and which polymer family you are in.",
        lesson_figure(
            atom_shells_svg(protons=6, electrons=(2, 4)),
            "Carbon: six protons, four valence electrons",
            "Four valence electrons mean four covalent bonds — the reason carbon skeletons can branch and ring.",
        )
        + solved(4, "Which six elements are CHNOPS, and which of them is in ATP’s ‘high-energy’ groups?",
                 ["C, H, N, O, P, S.",
                  "ATP’s energy is stored in phosphate groups, so phosphorus is the CHNOPS member in those groups.",
                  "The molecule also contains C, H, N, O in the adenine and ribose portions."],
                 "C H N O P S; phosphorus in the phosphates", "", "Easy")
        + solved(5, "Starch is broken into glucose during digestion. Name the reaction type and what molecule is consumed.",
                 ["Starch is a polymer; glucose is the monomer.",
                  "Splitting a polymer by adding water is hydrolysis.",
                  "Each glycosidic bond broken consumes one H₂O."],
                 "hydrolysis; water", "", "Medium")
        + solved(6, "A mystery molecule has a long C–H chain plus a –COOH at one end. Which polymer family is it closest to, and is the tail hydrophilic?",
                 ["A carboxyl plus a hydrocarbon tail is a fatty acid (lipid family).",
                  "The tail is nonpolar C–H, so it is hydrophobic (water-fearing).",
                  "The –COOH can be polar/acidic, so the whole molecule is amphipathic if the tail is long."],
                 "lipid / fatty acid; tail is hydrophobic", "", "Hard"),
        ("Treating CHNOPS as the only elements that ever appear",
         "CHNOPS dominate mass, but Fe, I, Ca, Na, K, and others are essential. ‘Most of the mass’ is not the same as ‘the complete list of needed elements.’"),
        ("Find the functional group, then the family",
         "Amino + carboxyl on a central carbon → amino acid. Phosphate + sugar + base → nucleotide. Many C–H with a carboxyl → fatty acid. Ring of C and O with –OH groups → sugar."),
        [
            "I can list CHNOPS and say what carbon’s four bonds allow.",
            "I can recognize major functional groups and their hydrophilic or acidic/basic behavior.",
            "I can contrast dehydration synthesis with hydrolysis.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Carbohydrates and lipids",
        [
            "Carbohydrates are sugars and sugar polymers. The usual empirical formula for a monosaccharide is $C_n(H_2O)_n$. Glucose ($C_6H_{12}O_6$) is the cell’s favorite fuel and the monomer of starch, glycogen, and cellulose.",
            "Two monosaccharides join by a glycosidic bond (dehydration). Sucrose is glucose + fructose. Lactose is glucose + galactose. Polysaccharides are long chains: starch and glycogen store glucose; cellulose is a structural fiber in plant walls.",
            "The difference between starch and cellulose is not the elements — both are glucose — it is the 3-D geometry of the glycosidic bond ($\\alpha$ vs $\\beta$). Geometry changes packing and which enzymes can cut the chain. Structure, then function.",
            "Lipids are a mixed club defined by hydrophobicity more than by a single monomer. Fats (triglycerides) are three fatty acids attached to glycerol. They store energy, cushion organs, and insulate.",
            "Saturated tails have only C–C single bonds and pack like straight sticks (often solid at room temperature). Unsaturated tails have C=C double bonds that kink, so they pack loosely (often liquid oils). Phospholipids have two tails plus a phosphate head: they are amphipathic and form bilayers.",
            "Steroids such as cholesterol share a four-ring carbon skeleton. Cholesterol is a fluidity buffer in animal membranes and a precursor of steroid hormones. Lipids do not form true polymers the way proteins and nucleic acids do, but they still follow ‘shape plus polarity equals job.’",
        ],
        "Membranes, energy storage, and plant structure are all lipid/carbohydrate stories. Unit 2’s bilayer and Unit 3’s fuels assume this vocabulary.",
        "Ask two questions: is it a sugar polymer or a hydrophobic molecule? Then ask: energy store, structure, or membrane?",
        lesson_figure(
            _lipid_carb_svg(),
            "A hexose ring beside a fatty-acid tail",
            "Left: carbohydrate monomer. Right: hydrophobic hydrocarbon tail with a carboxyl head.",
        )
        + solved(7, "Name the monomer of glycogen and the job of glycogen in a mammal.",
                 ["Glycogen is a branched polymer of glucose.",
                  "Animals store it in liver and muscle.",
                  "When energy is needed, hydrolysis releases glucose quickly from many branch ends."],
                 "glucose; short-term energy storage", "", "Easy")
        + solved(8, "A membrane from a tropical plant vs an Arctic fish: which should have more unsaturated phospholipids, and why?",
                 ["Cold membranes risk packing into a gel (too rigid).",
                  "Cis double bonds kink tails and keep the bilayer fluid.",
                  "The Arctic fish needs more unsaturated lipids than the tropical plant at the same body-temperature logic for membranes."],
                 "Arctic fish; kinks maintain fluidity in the cold", "", "Medium")
        + solved(9, "Why can humans get calories from starch but not from cellulose, even though both are glucose chains?",
                 ["Starch has $\\alpha$-glycosidic bonds that our amylase can hydrolyze.",
                  "Cellulose has $\\beta$-glycosidic bonds and hydrogen-bonded fibers.",
                  "We lack cellulase, so cellulose is structural fiber for us, not fuel.",
                  "Same monomer, different bond geometry, different function and digestibility."],
                 "α vs β glycosidic geometry; we digest starch, not cellulose", "", "Hard"),
        ("Saying lipids are ‘polymers of fatty acids’ the way proteins are polymers of amino acids",
         "Triglycerides are not long repeating chains with a single repeating covalent backbone like polypeptides. Phospholipids and steroids are even less ‘polymer-like.’ Hydrophobic behavior is the unifying idea."),
        ("Match the polysaccharide to the organism and the job",
         "Plant store: starch. Plant wall: cellulose. Arthropod/fungal wall: chitin. Animal store: glycogen. If the question gives a job, pick the matching polymer."),
        [
            "I can name glycosidic bonds and contrast starch, glycogen, and cellulose.",
            "I can explain saturated vs unsaturated tails and membrane fluidity.",
            "I can describe why phospholipids form bilayers.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Proteins and nucleic acids",
        [
            "A protein is a polymer of amino acids. Every amino acid has a central carbon bonded to H, an amino group, a carboxyl group, and a variable side chain called the R group. The R group is the chemical personality: hydrophobic, polar, acidic, or basic.",
            "A peptide bond covalently joins the carboxyl carbon of one amino acid to the amino nitrogen of the next. The sequence of amino acids is primary structure. It is encoded by DNA.",
            "Secondary structure is local folding: $\\alpha$ helices and $\\beta$ sheets, held by hydrogen bonds along the backbone. Tertiary structure is the overall 3-D fold of one chain, held by R-group interactions. Quaternary structure is multiple folded chains packing together, as in hemoglobin.",
            "Nucleic acids store and transfer information. DNA is usually a double helix of two antiparallel strands. RNA is usually single-stranded and uses uracil instead of thymine, and ribose instead of deoxyribose.",
            "A nucleotide has three parts: a phosphate, a five-carbon sugar, and a nitrogenous base. The backbone is sugar–phosphate covalent bonds (phosphodiester). The information is the base sequence. A pairs with T (two H-bonds); G pairs with C (three H-bonds).",
            "The central flow in cells is DNA → RNA → protein. Sequence in nucleic acids specifies sequence in proteins; protein sequence specifies fold; fold specifies function. Change the sequence, and you may change the job — the theme of Units 5–6.",
        ],
        "Genetics, gene expression, and almost every enzyme story rest on polymer sequence and complementary pairing.",
        "For proteins, climb the structure ladder (1° 2° 3° 4°). For nucleic acids, separate backbone chemistry from base-pairing information.",
        lesson_figure(
            _aa_svg(),
            "Amino acid: backbone plus R group",
            "Peptide bonds join the carboxyl of one residue to the amino of the next. The R group is the chemical personality.",
        )
        + solved(10, "If one DNA strand is 5′-ATGC-3′, what is the complementary strand written 5′ to 3′?",
                 ["Pair A with T, T with A, G with C, C with G, and remember strands are antiparallel.",
                  "The 3′ to 5′ complement of ATGC is TACG.",
                  "Flip to 5′→3′: GCAT."],
                 "5′-GCAT-3′", "", "Easy")
        + solved(11, "dsDNA is 22% guanine. What percent is adenine?",
                 ["G = C, so C is also 22%. G + C = 44%.",
                  "The remaining 56% is A + T, and A = T, so each is 28%.",
                  "Adenine is 28%."],
                 "28%", "", "Medium")
        + solved(12, "A mutation changes an active-site serine (polar) to leucine (hydrophobic). Predict the most likely result and why.",
                 ["Primary sequence changed at a chemically important residue.",
                  "Tertiary contacts in the active site likely shift; substrate binding or catalysis can fail.",
                  "Function is lost or reduced even if most of the chain is unchanged."],
                 "likely loss of enzyme activity from a disrupted active site",
                 "AP wants the structure–function sentence, not a lucky guess.", "Hard"),
        ("Thinking hydrogen bonds hold the DNA backbone together",
         "Backbone = covalent phosphodiester bonds (strong). Base pairs = hydrogen bonds (weaker, unzip for replication and transcription). Mixing those two is a classic AP miss."),
        ("Write Chargaff math on paper",
         "G = C, A = T, and all four add to 100%. If they give one base, fill the partner first, then split the remainder."),
        [
            "I can describe peptide bonds and the four levels of protein structure.",
            "I can apply complementary base pairing and Chargaff’s rules.",
            "I can connect a sequence change to a possible function change.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Structure meets function",
        [
            "AP Biology’s favorite sentence is: the shape of a molecule, organelle, or organism exists because it does a job. Change the shape, and the job usually changes.",
            "An enzyme’s active site is a pocket whose shape and charges match one substrate (or a small family). That is why one enzyme does not catalyze every reaction in the cell.",
            "Hemoglobin’s quaternary structure lets it bind four O₂ and change affinity as pH and CO₂ change (Bohr effect). A single Glu→Val swap in sickle-cell disease makes hemoglobin sticky, distorting red blood cells — sequence → shape → disease.",
            "Phospholipids are amphipathic, so they form bilayers with tails in and heads out. Channel proteins fold so a hydrophilic tunnel crosses that hydrophobic core. Each fold solves a transport problem.",
            "Cellulose fibers are strong because β-glucose chains hydrogen-bond into cables. Glycogen is branched so many ends can release glucose at once. Same sugar, different architecture, different job.",
            "When you meet an AP figure of a mutated protein, a clogged channel, or a bent membrane lipid, ask: which interaction was lost (H-bond, ionic, hydrophobic, disulfide), and which function should fail?",
        ],
        "Units 2–6 keep testing this habit. If you only memorize names, FRQs feel like traps. If you argue from shape, they feel like stories.",
        "Always write a three-part chain: structure (what is the shape/chemistry?) → interaction (what binds or packs?) → function (what job appears or disappears?).",
        lesson_figure(
            _lock_key_svg(),
            "Active site complementary to a substrate",
            "The pocket’s shape and chemistry — not a slogan — are why one enzyme fits one substrate.",
        )
        + solved(13, "Why does a channel that moves K⁺ usually reject Na⁺ even though both are +1 cations?",
                 ["The channel’s pore is a precisely sized, precisely lined tunnel.",
                  "K⁺ fits the lining so water can be replaced by protein oxygens; Na⁺ is smaller and does not pay that energy bill the same way.",
                  "Selectivity is structure (pore geometry + chemistry), not the charge alone."],
                 "pore size and lining select K⁺ over Na⁺", "", "Easy")
        + solved(14, "Antibodies bind one antigen. How is that the same logic as enzyme specificity?",
                 ["Both use a 3-D binding site complementary in shape and chemistry.",
                  "Noncovalent interactions (H-bonds, ionic, van der Waals, hydrophobic) add up to a tight, specific fit.",
                  "A mutation that reshapes the site can lose binding, just as an active-site mutation can lose catalysis."],
                 "complementary binding sites; sequence → shape → specific binding", "", "Medium")
        + solved(15, "A soluble enzyme has a hydrophobic core. What happens if you mutate several core leucines to lysines (charged), and why?",
                 ["Lysines want water and will be unhappy in a dry core, or they will force the protein to unfold so they can reach solvent.",
                  "Unfolding destroys the active-site geometry.",
                  "Catalysis collapses even though peptide bonds still exist."],
                 "unfolding / loss of function from unsatisfied buried charges", "", "Hard"),
        ("Memorizing ‘structure determines function’ without a mechanism",
         "AP graders want the mechanism: which bond, which pocket, which packing. The slogan alone earns little. Name the interaction that was lost."),
        ("Build the chain on the FRQ margin",
         "Write S→I→F: structure, interaction, function. Then pick the answer that completes that chain. Distractors usually skip a step or reverse cause and effect."),
        [
            "I can explain enzyme and antibody specificity using complementary shape.",
            "I can predict how a chemically unlike amino-acid swap may ruin a fold.",
            "I can apply structure–function thinking to membranes and polysaccharides.",
        ],
        21,
    )

    c6 = concept_block(
        "6. pH and buffers",
        [
            "An acid is a substance that increases [H⁺] in water. A base decreases [H⁺] (often by releasing OH⁻ or accepting H⁺). pH is defined as $pH=-\\log_{10}[H^+]$, so it is a compressed scale: each 1-unit drop means 10 times more H⁺.",
            "Pure water at 25 °C has $[H^+]=1\\times10^{-7}\\,M$, so pH 7. That is called neutral because [H⁺] equals [OH⁻], not because there are no ions.",
            "Cells care about pH because amino-acid side chains gain or lose protons as pH changes. Charge changes mean hydrogen bonds and ionic bonds rearrange, so proteins denature or lose catalytic residues.",
            "A buffer is a weak acid plus its conjugate base (or a weak base plus its conjugate acid). It resists pH change: extra H⁺ is soaked up by the conjugate base; extra OH⁻ is soaked up via the weak acid.",
            "Blood uses carbonic acid and bicarbonate: $CO_2+H_2O\\rightleftharpoons H_2CO_3\\rightleftharpoons H^++HCO_3^-$. Fast breathing dumps CO₂ and can raise pH; holding CO₂ can lower pH. Physiology is chemistry here.",
            "On AP calculations, if pH goes from 6 to 4, [H⁺] rose by $10^{2}=100$-fold. If they give [H⁺], take the negative log. If they give a 10-fold change, move pH by 1 unit in the correct direction (more H⁺ → lower pH).",
        ],
        "Enzyme graphs in Unit 3 and hemoglobin in later units assume you can read pH as [H⁺] and explain why buffers protect shape.",
        "Convert every pH story into [H⁺] (powers of ten), then ask which macromolecule charges would change.",
        lesson_figure(
            beaker_svg("buffer: HA / A⁻"),
            "A buffered solution",
            "Weak acid HA and conjugate base A⁻ trade protons so pH barely moves when small amounts of acid or base are added.",
        )
        + solved(16, "If $[H^+]=1\\times10^{-4}\\,M$, what is the pH, and is the solution acidic or basic?",
                 ["$pH=-\\log_{10}(10^{-4})=4$.",
                  "pH 4 is less than 7, so the solution is acidic.",
                  "[H⁺] is $10^{-4}$, which is greater than $10^{-7}$."],
                 "pH 4; acidic", "", "Easy")
        + solved(17, "How many times greater is [H⁺] at pH 3 than at pH 6?",
                 ["Difference = 3 pH units.",
                  "Each unit is a factor of 10, so $10^3=1000$.",
                  "pH 3 is more acidic, so it has 1000 times more H⁺."],
                 "1000-fold greater at pH 3", "", "Medium")
        + solved(18, "Blood pH is ~7.4. Explain how bicarbonate buffering plus lungs keep a sprinter’s extra CO₂ from crashing pH, in steps.",
                 ["Extra CO₂ shifts $CO_2+H_2O\\rightleftharpoons H_2CO_3\\rightleftharpoons H^++HCO_3^-$ toward H⁺.",
                  "HCO₃⁻ binds much of that H⁺, forming H₂CO₃, so free [H⁺] rises only a little.",
                  "Breathing then removes CO₂, pulling the equilibrium back and restoring pH.",
                  "Without the conjugate pair, the same H⁺ would drop pH far more and denature proteins."],
                 "HCO₃⁻ absorbs H⁺; ventilation removes CO₂", "", "Hard"),
        ("Thinking a pH drop of 1 is ‘only 1 more H⁺’",
         "pH is logarithmic. A drop of 1 is a 10-fold increase in [H⁺]; a drop of 2 is 100-fold. Linear thinking misses every AP pH item."),
        ("Write powers of ten, then talk about proteins",
         "First compute the [H⁺] factor. Then say: extra protons change side-chain charges, so folds and enzyme rates change. That two-step answer beats a memorized ‘pH matters.’"),
        [
            "I can convert between pH and [H⁺] using powers of ten.",
            "I can explain why pH changes denature proteins.",
            "I can describe how a weak acid / conjugate base buffer resists pH change.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Water’s polarity, hydrogen bonds, and the properties that follow",
            "CHNOPS, functional groups, dehydration and hydrolysis",
            "Carbohydrates and lipids as fuel, structure, and membrane fabric",
            "Proteins and nucleic acids: sequence, fold, and base pairing",
            "Structure–function reasoning with real molecular examples",
            "pH as [H⁺] and how buffers protect macromolecules",
        ],
        body,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


def _bacteria_svg(w=280, h=140):
    """Simple prokaryote: nucleoid, ribosomes, cell wall."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<ellipse cx="140" cy="70" rx="120" ry="50" fill="#fef9c3" stroke="#a16207" stroke-width="6"/>'
        f'<ellipse cx="140" cy="70" rx="112" ry="42" fill="none" stroke="#ca8a04" stroke-width="2"/>'
        f'<path d="M90 70 C100 50, 130 50, 140 70 C150 90, 180 90, 190 70" fill="none" stroke="#b91c1c" stroke-width="3"/>'
        f'<circle cx="70" cy="60" r="4" fill="#64748b"/>'
        f'<circle cx="80" cy="85" r="4" fill="#64748b"/>'
        f'<circle cx="210" cy="55" r="4" fill="#64748b"/>'
        f'<text x="140" y="128" text-anchor="middle" font-size="11">wall + membrane; DNA in nucleoid (no nucleus)</text>'
        f"</svg>"
    )


# ===========================================================================
# UNIT 2: Cell Structure and Function
# ===========================================================================

def _u2_questions():
    return _qs([
        ("A prokaryotic cell differs from a eukaryotic cell because a prokaryote:",
         "lacks a nucleus and membrane-bound organelles",
         "Prokaryotes (bacteria and archaea) have a nucleoid region of DNA, ribosomes, and usually a cell wall, but no nucleus or mitochondria. Eukaryotes package DNA in a nucleus and have internal membranes.",
         ["is always larger than any eukaryote", "has mitochondria but no ribosomes", "stores DNA only as RNA"]),
        ("Which structure is found in both prokaryotes and eukaryotes and is the site of protein synthesis?",
         "ribosome",
         "Ribosomes are RNA–protein machines that translate mRNA. They are not membrane-bound, so they exist in both cell types. Nuclei and mitochondria are eukaryotic.",
         ["nucleus", "chloroplast", "Golgi apparatus"]),
        ("Plant cells have organelles animal cells lack. Two defining plant structures are:",
         "chloroplasts and a cellulose cell wall (plus a large central vacuole)",
         "Chloroplasts run photosynthesis. Cellulose walls give shape. A large vacuole stores water and ions. Animals have mitochondria but not chloroplasts or cellulose walls.",
         ["lysosomes only, and no mitochondria", "flagella made of peptidoglycan", "a nucleoid instead of a nucleus"]),
        ("Why can a bacterium divide in minutes while a human cell is much larger and slower?",
         "a high surface-area-to-volume ratio lets the small cell exchange materials fast",
         "Volume grows faster than surface as a cell enlarges. Diffusion distances increase. Small prokaryotes keep a large SA/V, so membranes can serve the cytoplasm quickly.",
         ["bacteria have no DNA to copy", "large cells always have higher SA/V", "eukaryotes lack ribosomes"]),
        ("Archaea are prokaryotes but are not bacteria. An AP-safe distinction is that archaea:",
         "often live in extreme habitats and have distinct membrane lipids and machinery",
         "Three domains: Bacteria, Archaea, Eukarya. Archaea are prokaryotic in structure but molecularly closer to eukaryotes in some transcription/translation features.",
         ["archaea have nuclei like plants", "archaea are a type of virus", "archaea never have cell walls of any kind"]),
        ("Compartmentalization means eukaryotic organelles create separate rooms. The advantage is:",
         "incompatible reactions can run at the same time in different places",
         "Lysosomes are acidic; the cytosol is not. Mitochondrial inner membranes hold the ETC. Separating spaces raises local concentrations and protects the rest of the cell.",
         ["it prevents all proteins from ever being made", "it makes cells smaller than bacteria", "it removes the need for membranes"]),
        ("Which organelle hosts most ATP production from cellular respiration in eukaryotes?",
         "mitochondrion",
         "Glycolysis is cytosolic, but pyruvate oxidation, the Krebs cycle, and the electron transport chain occur in mitochondria. The inner membrane’s folds (cristae) add surface for the ETC.",
         ["smooth ER", "cell wall", "central vacuole"]),
        ("The Golgi apparatus’s job is to:",
         "modify, sort, and ship proteins and lipids from the ER",
         "Vesicles from the rough ER arrive at the cis Golgi. Cargo is glycosylated and sorted, then leaves the trans face toward the plasma membrane, lysosomes, or secretion.",
         ["digest worn-out organelles as the only function", "copy DNA", "make all ATP"]),
        ("Rough ER looks ‘rough’ because of attached ribosomes. Proteins made there are typically:",
         "secreted, membrane-bound, or sent to organelles of the endomembrane system",
         "A signal peptide docks the ribosome on the ER. Cytosolic proteins are made on free ribosomes instead.",
         ["all mitochondrial matrix enzymes exclusively", "DNA polymerases in the nucleoid", "cellulose fibers in the wall"]),
        ("A macrophage digesting a bacterium uses a lysosome. The lysosome can do this because:",
         "it contains hydrolytic enzymes at acidic pH, sealed away from the cytosol",
         "Compartmentalization protects the cell: if those enzymes leaked at cytosolic pH they would be less active, and even then the membrane normally contains them.",
         ["lysosomes synthesize the bacterium’s DNA", "lysosomes are found only in plants", "lysosomes pump the bacterium out without enzymes"]),
        ("The fluid mosaic model says membranes are:",
         "a phospholipid bilayer with proteins drifting in it",
         "Lipids give the fluid bilayer; proteins mosaic it as channels, pumps, receptors, and enzymes. Cholesterol in animals buffers fluidity.",
         ["a rigid wall of cellulose only", "a single layer of protein with DNA on the outside", "ice with trapped ions"]),
        ("Which molecule crosses a pure phospholipid bilayer most easily by simple diffusion?",
         "O₂ (small and nonpolar)",
         "The hydrophobic core blocks ions and large polar molecules. Small nonpolar gases (O₂, CO₂) slip through. Water is small but polar, so it is slower unless aquaporins help.",
         ["Na⁺", "glucose without a protein", "a protein hormone"]),
        ("Cholesterol in an animal membrane at moderate temperature:",
         "reduces fluidity by restraining phospholipid motion",
         "At high T, cholesterol stiffens; at low T, it prevents tight packing (keeps some fluidity). It is a fluidity buffer, not a pump.",
         ["pumps Na⁺ using ATP", "stores genetic information", "is a carbohydrate wall"]),
        ("Glycoproteins on the outer membrane surface are used mainly for:",
         "cell identity and recognition",
         "Carbohydrate chains (glycolipids/glycoproteins) face the extracellular side and act as ID tags — blood types, immune self vs nonself, tissue sorting.",
         ["storing starch inside the bilayer core", "copying DNA", "making ATP in animals"]),
        ("Integral membrane proteins often have a belt of hydrophobic amino acids because that belt:",
         "contacts the fatty-acid tails of the bilayer",
         "Structure matches environment: hydrophobic R groups sit in the lipid core; hydrophilic regions face water on one or both sides.",
         ["must bind DNA in the nucleoid", "dissolves the membrane completely", "is made of cellulose"]),
        ("Passive transport moves a solute:",
         "down its concentration (or electrochemical) gradient, without ATP",
         "Simple diffusion and facilitated diffusion are both passive. The energy source is the gradient itself, not ATP hydrolysis.",
         ["against its gradient using ATP", "only through the nucleus", "from low to high concentration in every case"]),
        ("Facilitated diffusion of glucose uses a carrier. It is still passive because:",
         "glucose moves toward lower concentration; the protein only provides a path",
         "The protein is a door, not a pump. If the gradient reverses, net flow reverses. Insulin can add more doors (GLUT4) but the direction is still downhill.",
         ["the carrier burns ATP for every glucose", "glucose is pumped into a higher concentration always", "diffusion cannot use proteins"]),
        ("Osmosis is the net movement of water:",
         "across a membrane toward the side with higher solute concentration (lower water potential)",
         "Water itself moves from high water potential to low water potential. Solute lowers water potential, so water ‘follows’ solute when the membrane is more permeable to water than to the solute.",
         ["toward the side with less solute in every living cell regardless of pressure", "only through ion pumps", "from ice to vapor inside the bilayer"]),
        ("Aquaporins raise the rate of water crossing membranes. They do not:",
         "change the direction water ‘wants’ to go; they only speed the path",
         "Direction is set by water potential. More channels change kinetics (rate), not the equilibrium condition.",
         ["ever exist in kidney or plant cells", "allow any water movement", "are proteins"]),
        ("A charged ion crossing a membrane passively must consider the electrochemical gradient, meaning:",
         "both concentration and electrical potential across the membrane",
         "A + ion is pulled toward the negative side of the membrane as well as toward lower chemical concentration. AP often tests this with K⁺ leak and resting potential.",
         ["only gravity", "only temperature", "only the number of neutrons"]),
        ("The Na⁺/K⁺ pump moves 3 Na⁺ out and 2 K⁺ in per ATP. This is active transport because:",
         "both ions move against their gradients using ATP",
         "Na⁺ is already higher outside; K⁺ is already higher inside. The pump builds those gradients, which later drive secondary transport and nerve signals.",
         ["ions are moving down their gradients", "ATP is produced by the pump", "the pump is a carbohydrate"]),
        ("Secondary active transport (cotransport) uses:",
         "the downhill flow of one solute to drag another solute uphill",
         "A proton or Na⁺ gradient, built by a pump, is the battery. A cotransporter lets that ion back in only if a sugar or amino acid rides along against its own gradient. ATP was spent earlier, not at the cotransporter itself.",
         ["only simple diffusion of O₂", "a nucleus pumping DNA", "breaking the membrane into ice"]),
        ("Endocytosis brings large cargo in by wrapping membrane around it. Exocytosis:",
         "fuses vesicles with the plasma membrane to release cargo",
         "Secreted proteins leave this way. The membrane area is recycled between endocytosis and exocytosis.",
         ["pumps individual Na⁺ ions with no vesicles", "is the same as osmosis", "occurs only in prokaryotes that lack membrane"]),
        ("Why does blocking ATP production eventually stop the Na⁺/K⁺ pump but not immediately stop O₂ diffusion into the cell?",
         "the pump needs ATP; O₂ diffusion is passive",
         "Active transport requires a cellular energy source. Simple diffusion of a nonpolar gas does not. Over time, dying gradients affect many processes, but the first distinction is ATP dependence.",
         ["O₂ diffusion requires more ATP than the pump", "the pump is passive and diffusion is active", "ATP is only used to move gases"]),
        ("A plant’s proton pump acidifies the cell wall. That gradient can then drive sucrose uptake by cotransport. The sucrose step is:",
         "secondary active transport",
         "ATP ran the H⁺ pump (primary). Sucrose rides the H⁺ return (secondary). AP wants you to separate those two energy steps.",
         ["simple diffusion of sucrose through the bilayer core", "osmosis of sucrose", "facilitated diffusion that builds a sucrose gradient from nothing without any prior pump"]),
        ("A cell in a hypertonic solution will:",
         "lose water and shrink (plasmolyze if it is a plant cell)",
         "Hypertonic means the surroundings have higher solute (lower Ψ) than the cell, so water leaves. Animal cells crenate; plant cells plasmolyze (membrane pulls from the wall).",
         ["gain water and burst in every case", "have no water movement ever", "pump the whole solution into the nucleus"]),
        ("An animal cell in distilled water (hypotonic) tends to burst because:",
         "water enters down its water-potential gradient and there is no strong wall",
         "Plant cells have walls that generate turgor (Ψp rises) and usually stop net entry. Animal cells lack that wall, so they lyse in strongly hypotonic baths.",
         ["water leaves the cell in hypotonic solution", "distilled water has enormous solute concentration", "hypotonic means equal solute inside and out"]),
        ("Water potential $\\Psi=\\Psi_s+\\Psi_p$. Solute potential $\\Psi_s=-iCRT$ is always:",
         "zero or negative (solute lowers Ψ)",
         "Adding solute makes it harder for water to leave that side by osmosis, which is a more negative Ψs. Pressure potential can be positive (turgor) or zero (open beaker).",
         ["always positive and larger than pressure", "equal to pH", "independent of concentration"]),
        ("Open beaker, 0.5 M sucrose, i=1, R=0.0831 L·bar/mol·K, T=300 K. $\\Psi_s=-iCRT$ is closest to:",
         "−12.5 bar",
         "$-(1)(0.5)(0.0831)(300)=-12.465$ bar, about $-12.5$ bar. Open beaker: $\\Psi_p=0$, so $\\Psi\\approx-12.5$ bar.",
         ["+12.5 bar", "0 bar", "−0.5 bar"]),
        ("A cell has $\\Psi_s=-9$ bar and $\\Psi_p=+4$ bar. A beaker has $\\Psi=-6$ bar. Water will:",
         "leave the cell (−5 bar is higher Ψ than −6 bar)",
         "Cell Ψ = −9+4 = −5 bar. Water moves from higher Ψ to lower Ψ: −5 bar (cell) to −6 bar (beaker), so water leaves the cell.",
         ["enter the cell, because −5 is more negative than −6", "not move because pressures are equal", "enter the cell because solute is higher outside"]),
        ("Surface-area-to-volume ratio falls as a cube grows. A cube of side 1 has SA/V = 6; side 2 has SA/V = 3. Cells stay small or add folds because:",
         "membrane exchange must keep up with cytoplasmic volume",
         "Microvilli, cristae, and thylakoid stacks are all SA tricks. AP figures of folded membranes are asking this.",
         ["volume must always exceed surface", "DNA cannot fit in small cells", "prokaryotes need low SA/V to survive"]),
        ("Which list is only endomembrane-system members?",
         "nuclear envelope, ER, Golgi, vesicles, lysosomes, plasma membrane",
         "Mitochondria and chloroplasts are semi-autonomous (endosymbiotic), not part of the vesicle-trafficking endomembrane stream, even though they are organelles.",
         ["mitochondria, chloroplasts, nucleoid", "ribosomes, cellulose, glycogen", "flagellin, peptidoglycan, capsule only"]),
        ("A pulse-chase experiment labels secreted protein in the ER, then the label appears in Golgi, then outside the cell. This order supports:",
         "the secretory pathway ER → Golgi → vesicle → exterior",
         "Classic Palade logic: location over time traces the path. The protein is not made in the Golgi first.",
         ["proteins being made in the nucleus from lipids", "mitochondria secreting starch", "diffusion of DNA out of lysosomes"]),
        ("Plant cells in hypotonic soil become turgid, not lysed, because:",
         "the wall pushes back (positive Ψp) until Ψ_cell equals Ψ_outside",
         "Water enters, volume tries to rise, the wall resists, pressure climbs, net water flow stops at equilibrium. That firmness is turgor, which supports herbaceous plants.",
         ["plant membranes are impermeable to water", "plants have no vacuoles", "hypotonic means water leaves plant cells"]),
        ("K⁺ is high inside neurons. It still can leak out through channels because:",
         "its chemical gradient outward can outweigh the electrical pull inward, until electrochemical equilibrium",
         "Nernst/electrochemical thinking: ‘down the gradient’ for an ion is not only concentration. Resting potential is largely K⁺ leak plus the pump maintaining the concentrations.",
         ["K⁺ is uncharged", "channels always use ATP", "K⁺ cannot pass proteins"]),
        ("Which statement about simple vs facilitated diffusion is correct?",
         "both are passive; facilitated needs a protein, simple does not",
         "Do not confuse ‘uses a protein’ with ‘uses ATP.’ Facilitated = protein + downhill. Active = ATP (or another energy coupling) + usually uphill.",
         ["facilitated diffusion always requires ATP", "simple diffusion is only for glucose", "both require a nucleus"]),
        ("Contractile vacuoles in freshwater protists expel water. They exist because the habitat is:",
         "hypotonic to the cytoplasm, so water constantly enters",
         "Without a wall, the protist would lyse. The vacuole is an active water-export strategy — energy spent to solve an osmosis problem.",
         ["hypertonic, so water never enters", "isotonic, so no net water movement ever occurs in fresh water", "made of pure sucrose"]),
        ("A channel is open and a carrier flips conformation. Both can do facilitated diffusion. The carrier can saturate because:",
         "there are a limited number of binding sites that can be occupied",
         "Rate vs concentration for a carrier looks like an enzyme curve (approaches Vmax). A pure lipid path for O₂ does not saturate the same way.",
         ["carriers create ATP from glucose", "channels never let ions through", "saturation means the gradient reversed"]),
        ("Why do mitochondria and chloroplasts support endosymbiosis?",
         "they have their own circular DNA, 70S-type ribosomes, and double membranes",
         "They divide somewhat independently and their genomes encode some of their proteins. That is the living-bacteria-inside-a-host story AP expects.",
         ["they lack membranes", "they are made of cellulose", "they are found in all viruses"]),
        ("Plasmolysis is:",
         "the plasma membrane pulling away from the cell wall as a plant cell loses water",
         "Hypertonic surroundings → water out → limp cell, membrane shrinks from the wall. The opposite of turgid.",
         ["an animal cell bursting in hypotonic solution", "a bacterium growing a nucleus", "osmosis stopping because Ψp is infinite"]),
        ("Na⁺/glucose cotransport in the gut: Na⁺ enters down its gradient, glucose rides in against its gradient. The Na⁺ gradient was built by:",
         "the Na⁺/K⁺ pump using ATP on the other membrane face",
         "Primary pump charges the battery; cotransporter spends the battery. Blocking the pump with a toxin eventually stops glucose uptake even though the cotransporter itself does not hydrolyze ATP.",
         ["simple diffusion of glucose building the Na⁺ gradient", "chloroplasts in the intestinal cell", "osmosis of NaCl through aquaporins only"]),
        ("Which molecule needs a protein to cross efficiently and also needs ATP to accumulate inside against a gradient?",
         "an ion such as H⁺ being pumped into a vacuole",
         "Ions cannot cross the bilayer well, and concentrating them uphill is active transport. O₂ needs neither protein nor ATP to enter.",
         ["O₂ entering mitochondria", "CO₂ leaving a respiring cell by simple diffusion", "N₂ in air dissolving passively"]),
        ("A red blood cell (no wall) in 0.9% NaCl stays the same volume. That solution is:",
         "isotonic to the cell",
         "Isotonic: no net water movement. 0.9% saline is the classic isotonic IV fluid. Distilled water would be hypotonic; concentrated brine hypertonic.",
         ["hypertonic, so the cell bursts", "hypotonic, so the cell shrinks", "pure lipid with no water potential"]),
        ("Cristae and thylakoids both:",
         "increase membrane surface for electron-transport proteins",
         "Same SA/V logic in two energy organelles. Folded membranes are not for storing DNA as chromatin; they are workbenches for the ETC and ATP synthase.",
         ["store cellulose", "are cell walls", "remove the need for gradients"]),
        ("Water potential of pure water at atmospheric pressure is defined as:",
         "0",
         "That is the reference. Adding solute makes Ψ negative. Positive pressure can raise Ψ above the solute value but pure open water is 0.",
         ["+100 bar always", "−iCRT with C=1 by definition for pure water", "equal to pH 7"]),
        ("If you raise T in $\\Psi_s=-iCRT$, solute potential becomes:",
         "more negative (larger magnitude) if C is constant",
         "T is in kelvin. Warmer solution: more negative Ψs, so a slightly stronger osmotic pull, all else equal. AP may sneak this in with a calculation.",
         ["more positive, because heat destroys solute", "unchanged, because R cancels T", "undefined above 25 °C"]),
        ("AP Stretch: A cube cell of side 4 arbitrary units vs side 1. Volume rose 64-fold while surface rose 16-fold, so SA/V fell 4-fold. Which adaptation best restores exchange?",
         "microvilli or membrane infoldings that add surface without a huge volume jump",
         "You cannot beat the geometry of a smooth cube by wishing. Folds, flattening, or staying small restore SA/V. Adding more cytoplasm alone makes the problem worse.",
         ["filling the cell with extra cytosol only", "removing all membranes", "converting to a perfect sphere of even larger radius"]),
        ("AP Stretch: Cell Ψs = −7.2 bar, Ψp = +2.0 bar. Outside is an open 0.3 M sucrose bath at 293 K (i=1, R=0.0831). Outside Ψ ≈ −7.3 bar. Net water flow is:",
         "out of the cell, because cell Ψ = −5.2 bar is higher than outside Ψ ≈ −7.3 bar",
         "Outside: Ψs = −(0.3)(0.0831)(293) ≈ −7.30, Ψp=0. Cell Ψ = −7.2+2.0 = −5.2 bar. Water moves from higher Ψ to lower Ψ: −5.2 (cell) → −7.3 (bath), so water leaves. Turgor (Ψp) will fall; a plant cell can plasmolyze.",
         ["into the cell because −5.2 is more negative than −7.3", "into the cell, raising turgor until Ψ values meet", "no net flow because Ψs values −7.2 and −7.3 are nearly equal"]),
        ("AP Stretch: An epithelial cell keeps [Na⁺]in = 12 mM vs [Na⁺]out = 145 mM. A 1:1 Na⁺/glucose symporter uses that ~12-fold Na⁺ gradient to concentrate glucose. After a mitochondrial poison collapses ATP, [Na⁺]in rises toward 145 mM and glucose accumulation fails because:",
         "the Na⁺ battery that pays for uphill glucose is gone, even though the cotransporter protein is still in the membrane",
         "Primary pumps spend ATP to hold [Na⁺] low inside. Secondary cotransport spends that gradient, not ATP at the glucose protein. When ATP falls, Na⁺ leaks in, ΔG for Na⁺ entry approaches 0, and glucose can no longer be piled 100-fold inside. GLUT-style facilitated diffusion would still run downhill if a gradient remained.",
         ["glucose channels begin to require O₂ instead of Na⁺", "osmosis reverses the phospholipid bilayer", "ATP concentration rises and poisons GLUT carriers immediately"]),
        ("AP Stretch: A mutant aquaporin speeds water flow 10×. In an isotonic bath, net volume change of an animal cell is still ~0 because:",
         "rate constants rose equally in both directions; net driving force is still ~0",
         "Aquaporins are facilitators. Equilibrium (or steady isotonic volume) is set by Ψ, not by how many doors exist. Kinetics ≠ thermodynamics.",
         ["the cell must burst if any aquaporin is present", "isotonic means water cannot move at all, even in exchange", "aquaporins pump water with ATP in isotonic solution"]),
        ("AP Stretch: Compare 0.2 M NaCl vs 0.2 M glucose, both open beakers, same T. Which has the more negative Ψs and why?",
         "NaCl, because i≈2, so −iCRT is about twice as negative",
         "van’t Hoff factor: NaCl ionizes. Glucose does not (i=1). Equal molarity is not equal osmolarity. AP will trap students who ignore i.",
         ["glucose, because it is larger", "they are identical because C is 0.2 for both", "NaCl has i=0"]),
        ("AP Stretch: A lysosomal enzyme has optimum pH ~5. If a vesicle fails to acidify (H⁺ pump broken), degradation slows because:",
         "the enzyme’s active-site charges are wrong at cytosolic pH ~7",
         "Compartmentalization is not decoration: pH is part of the structure–function match. The same polypeptide can be sluggish at the wrong pH without being genetically mutated.",
         ["lysosomal enzymes only cut DNA in the nucleus", "pH 7 hydrolyzes peptide bonds too fast so substrate vanishes", "H⁺ pumps synthesize the enzyme from lipids"]),
        ("AP Stretch: In a U-tube with a membrane permeable only to water, side A is 0.4 M sucrose, side B is 0.2 M sucrose, pistons hold volumes fixed. At equilibrium:",
         "pressure is higher on A, with Ψ_A = Ψ_B even though concentrations differ",
         "Water tries to enter A (higher solute). With volume fixed, Ψp rises on A until Ψ matches. This is the physical meaning of osmotic pressure.",
         ["concentrations must become equal even if the solute cannot cross", "pressure is higher on B", "water potential is undefined in U-tubes"]),
        ("AP Stretch: Why is a eukaryotic cell’s ER–Golgi–lysosome system a better explanation for hydrolytic safety than ‘the cytosol has no water’?",
         "hydrolysis needs water, which the cytosol has; the real protection is a sealed acidic compartment",
         "The naive answer (no water in cells) is false. Compartmentalization plus pH optima keep digestion on a leash. That is the AP-level correction.",
         ["the cytosol is anhydrous like a lipid droplet", "lysosomes contain no hydrolases", "ER destroys all water molecules"]),
        ("AP Stretch: An absorptive cell adds 800 microvilli, each a cylinder with radius $0.050\\,\\mu m$ and height $1.0\\,\\mu m$. Extra membrane area is about $800\\times 2\\pi r h\\approx 251\\,\\mu m^2$. This restores exchange better than doubling the whole cell’s radius because:",
         "folds add surface with almost no added cytoplasmic volume, so SA/V rises instead of falling",
         "Doubling radius multiplies volume by 8 and surface by only 4, so demand outruns supply. Microvilli are thin cylinders: lots of lateral area, tiny interior. That is why intestine, kidney, and cristae use folding rather than becoming giant spheres.",
         ["automatically double SA/V of a smooth sphere", "need fewer transporters because volume rose", "switch to simple diffusion of proteins through the bilayer"]),
    ])


def build_unit2():
    title = "AP Biology Unit 2: Cell Structure and Function"
    description = (
        "Prokaryotes vs eukaryotes, organelles, membranes, passive and active transport, "
        "and tonicity/water potential with internally consistent calculations."
    )

    c1 = concept_block(
        "1. Prokaryote vs eukaryote",
        [
            "A cell is the smallest unit that is fully alive. Two architectural plans exist. A prokaryotic cell (bacteria and archaea) has no nucleus: its DNA sits in a nucleoid region, and it has no mitochondria or chloroplasts.",
            "A eukaryotic cell (animals, plants, fungi, protists) wraps DNA in a nuclear envelope and contains membrane-bound organelles. That extra internal membrane is not decoration; it is how a larger cell stays organized.",
            "Both types have a plasma membrane, cytosol, ribosomes, and DNA. If an AP item asks ‘which is in all cells?’, ribosomes and membranes are safer answers than nuclei or mitochondria.",
            "Size matters. As a cell grows, volume (demand) rises faster than surface area (supply). Prokaryotes stay small and keep a high surface-area-to-volume ratio, so diffusion across the membrane can serve the whole cytoplasm.",
            "Plant cells are eukaryotic but add a cellulose wall, chloroplasts, and usually a large central vacuole. Fungi have walls too (chitin), but no chloroplasts. Animals have none of those three plant extras.",
            "The three-domain view puts Archaea beside Bacteria as prokaryotes, yet archaeal membranes and information machinery are distinct. ‘No nucleus’ does not mean ‘identical to E. coli.’",
        ],
        "Every later organelle and transport story assumes you can tell which rooms a cell even has. Mixing bacterial nucleoids with nuclei is an instant AP miss.",
        "Make a two-column list: shared (membrane, ribosomes, DNA) vs eukaryotic-only (nucleus, ER, mitochondria). Then add the plant extras.",
        lesson_figure(
            _bacteria_svg(),
            "A prokaryotic cell",
            "DNA is a nucleoid loop, not a nucleus. Dots are ribosomes. The thick outline is wall plus membrane.",
        )
        + solved(1, "A cell has ribosomes and DNA but no nucleus. Is it prokaryotic or eukaryotic, and what is the DNA region called?",
                 ["No nucleus means it is not a eukaryotic cell.",
                  "The DNA region in a prokaryote is the nucleoid.",
                  "Ribosomes are expected in both cell types."],
                 "prokaryotic; nucleoid", "", "Easy")
        + solved(2, "Why is ‘mitochondria’ a bad answer for ‘found in all living cells’?",
                 ["Mitochondria are eukaryotic organelles (endosymbiotic).",
                  "Bacteria make ATP at their plasma membrane and have no mitochondria.",
                  "All cells do have ribosomes and a plasma membrane, which are better ‘universal’ structures."],
                 "prokaryotes lack mitochondria", "", "Medium")
        + solved(3, "A cube-shaped cell doubles its side length from 1 to 2. Show that SA/V halves, and say why that threatens a cell.",
                 ["SA scales as $6s^2$: 6 → 24 (×4). Volume scales as $s^3$: 1 → 8 (×8).",
                  "SA/V goes from 6 to 3.",
                  "Each unit of cytoplasm now has less membrane for nutrient import and waste export, so the cell may starve or poison itself unless it folds membranes or divides."],
                 "SA/V: 6 → 3; exchange cannot keep up with volume", "", "Hard"),
        ("Calling anything without a cell wall a prokaryote",
         "Animal cells have no wall and are eukaryotic. Walls appear in plants, fungi, and most prokaryotes, but wall is not the definition — nucleus vs nucleoid is."),
        ("Circle ‘all cells’ vs ‘plant cells’ vs ‘eukaryotes’ in the stem",
         "The qualifier in the question is the whole game. ‘All cells’ → membrane/ribosomes/DNA. ‘Eukaryotes’ → nucleus. ‘Plants’ → chloroplasts/wall/vacuole."),
        [
            "I can contrast nucleoid vs nucleus and list shared cell features.",
            "I can identify plant-only eukaryotic structures.",
            "I can explain why SA/V limits cell size.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Organelles and compartmentalization",
        [
            "Compartmentalization means wrapping a reaction in a membrane so it has its own pH, enzymes, and concentrations. Eukaryotes are specialists at this.",
            "The nucleus stores chromosomes and runs transcription. The nucleolus (inside) assembles ribosomal subunits. Nuclear pores control traffic of RNA and proteins.",
            "The endomembrane system is a shipping network: nuclear envelope, ER, Golgi, vesicles, lysosomes, and the plasma membrane. Rough ER (ribosome-studded) builds proteins for secretion or membranes. Smooth ER makes lipids and detoxifies.",
            "The Golgi is the post office: it modifies glycoproteins, sorts them, and ships vesicles to the correct address. Lysosomes are acidic hydrolysis chambers. Vacuoles in plants store water, ions, and pigments and help with turgor.",
            "Mitochondria convert energy from food into ATP. Chloroplasts convert light into sugar. Both have double membranes and their own DNA — clues they began as engulfed prokaryotes (endosymbiosis).",
            "The cytoskeleton (microtubules, actin, intermediate filaments) is not an ‘organelle’ in the membrane sense, but it gives shape, moves vesicles, and pulls chromosomes. Structure again matches function: tracks for motors, cables for tension.",
        ],
        "Respiration, photosynthesis, secretion, and digestion FRQs all name rooms. If you put the Krebs cycle in the nucleus, the chemistry cannot save you.",
        "For each organelle, memorize one verb: nucleus stores, ribosome builds, ER packages, Golgi ships, lysosome digests, mitochondrion respires, chloroplast photosynthesizes.",
        lesson_figure(
            animal_cell_svg(),
            "A labeled animal cell",
            "Nucleus (red) holds DNA. Green ovals are mitochondria. The outer line is the plasma membrane — not a plant wall.",
        )
        + solved(4, "Where are secreted antibodies synthesized and then processed before leaving a plasma cell?",
                 ["Secreted proteins are made by ribosomes on rough ER.",
                  "They travel in vesicles to the Golgi for modification and sorting.",
                  "Secretory vesicles fuse with the plasma membrane (exocytosis)."],
                 "rough ER → Golgi → exocytosis", "", "Easy")
        + solved(5, "Why is a lysosome’s acid hydrolase safer inside the lysosome than free in the cytosol?",
                 ["The lysosome is a sealed compartment at pH ~5, where those enzymes work.",
                  "The cytosol is near pH 7, so leaked enzymes are less active.",
                  "The membrane also physically contains them, protecting cytosolic proteins from digestion."],
                 "acidic compartmentalization + membrane containment", "", "Medium")
        + solved(6, "Give two independent lines of evidence that mitochondria came from bacteria.",
                 ["They have circular DNA and bacteria-like ribosomes, and they divide by binary fission-like splitting.",
                  "They have a double membrane consistent with engulfment.",
                  "Their genomes encode some of their own proteins, leftover from a once-free organism."],
                 "own circular DNA/ribosomes + double membrane (endosymbiosis)", "", "Hard"),
        ("Putting ribosomes only in eukaryotes",
         "Protein synthesis is universal. Prokaryotes are packed with ribosomes. What they lack is a nucleus and membrane-bound organelles."),
        ("Trace a secreted protein like a package",
         "On FRQs, write the path with arrows: ribosome + RER → vesicle → Golgi → vesicle → plasma membrane. Graders look for that sequence."),
        [
            "I can assign major organelles a job and a location.",
            "I can explain an advantage of compartmentalization.",
            "I can outline the secretory pathway and endosymbiosis evidence.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Membrane structure",
        [
            "The plasma membrane is a phospholipid bilayer. Hydrophilic heads face water; hydrophobic tails hide inside. This arrangement is spontaneous in water because of the hydrophobic effect you met in Unit 1.",
            "The fluid mosaic model (Singer and Nicolson) says lipids move laterally and proteins are embedded or attached, like tiles in a moving mosaic. Membranes are not static walls.",
            "Cholesterol in animal membranes is a fluidity buffer: it stiffens a membrane that is too fluid at high temperature and keeps it from packing into a gel at low temperature.",
            "Proteins do the specialized jobs: channels, pumps, receptors, enzymes, anchors. Integral proteins span the bilayer with hydrophobic amino acids. Peripheral proteins sit on one face.",
            "Carbohydrate chains on glycolipids and glycoproteins face the outside and act as identity badges. That is why blood types and immune recognition are membrane stories.",
            "Selective permeability follows chemistry: small nonpolar molecules (O₂, CO₂) cross the tail region easily; ions and large polar molecules need proteins. The bilayer is the fence; proteins are the gates.",
        ],
        "Transport, signaling, and nerve impulses are membrane-protein stories sitting on this lipid fabric.",
        "For any crossing question, first ask: can it dissolve in the hydrophobic core? If no, it needs a protein. Then ask whether the direction is down or up the gradient.",
        lesson_figure(
            _bilayer_svg(),
            "Phospholipid bilayer with a protein channel",
            "Blue heads face water. Tails form the oily core. The yellow protein provides a hydrophilic path for cargo that cannot dissolve in tails.",
        )
        + solved(7, "Rank O₂, H₂O, and Na⁺ from easiest to hardest crossing of a pure bilayer, and justify.",
                 ["O₂ is small and nonpolar → easiest.",
                  "H₂O is small but polar → slow without aquaporins.",
                  "Na⁺ is charged → essentially blocked without a channel or pump."],
                 "O₂ > H₂O > Na⁺", "", "Easy")
        + solved(8, "A winter-active fish increases unsaturated phospholipids. What property is it tuning, and how do kinks help?",
                 ["It is keeping membrane fluidity at low temperature.",
                  "Cis double bonds kink tails so they cannot pack into a rigid gel.",
                  "Proteins in the membrane can still move and function."],
                 "fluidity; unsaturated kinks prevent packing", "", "Medium")
        + solved(9, "Why do glycoprotein sugars face the extracellular side, not the cytosolic side, of the plasma membrane?",
                 ["They are added in the ER/Golgi lumen, which is topologically outside.",
                  "Vesicle fusion preserves that orientation: lumen becomes extracellular space.",
                  "That outside face is exactly where cell–cell recognition happens."],
                 "endomembrane topology puts sugars outside for recognition", "", "Hard"),
        ("Drawing heads in the middle of the bilayer",
         "Heads love water, so they must face the cytosol and the extracellular fluid. Tails occupy the dry middle. A reversed sandwich would be physically unstable."),
        ("Fence then gate",
         "Write ‘bilayer blocks X because…’ and ‘protein Y allows X because…’ as two sentences. Mixing those ideas produces ‘Na⁺ dissolves in tails’ distractors."),
        [
            "I can describe the fluid mosaic bilayer and amphipathic phospholipids.",
            "I can predict which solutes need proteins to cross.",
            "I can explain cholesterol and glycoproteins in functional terms.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Passive transport",
        [
            "Passive transport is movement that does not require the cell to spend ATP at the transporter. The driving force is the concentration gradient, or for ions the electrochemical gradient.",
            "Simple diffusion is through the bilayer itself. Facilitated diffusion still goes downhill but uses a channel (open pore) or a carrier (protein that changes shape when cargo binds).",
            "Osmosis is the net diffusion of water through a membrane. Water moves toward the side with more solute if the solute cannot cross as freely — more precisely, water moves from higher water potential to lower water potential.",
            "Aquaporins are water channels. They change how fast water moves, not which way it ‘wants’ to go. Direction is thermodynamics; aquaporins are kinetics.",
            "A carrier can saturate: once every protein is busy, adding more solute barely raises rate. That graph looks like an enzyme’s $V_{max}$ curve. O₂ simple diffusion does not saturate in the same way.",
            "Ions listen to voltage as well as concentration. K⁺ may leak out of a neuron even though the inside is negative, until the electrical pull balances the chemical push. That balance is the Nernst idea behind resting potential.",
        ],
        "Tonicity, nerves, and later gas exchange all use ‘downhill through a path.’ Mixing passive with pumping is the most common Unit 2 error.",
        "Ask: is cargo going high→low? If yes, it can be passive. Then ask: bilayer or protein? If protein, channel vs carrier.",
        lesson_figure(
            _diffusion_svg(),
            "Solute spreading from high to low concentration",
            "Net motion is downhill. No ATP is drawn on the figure because the gradient is the energy source.",
        )
        + solved(10, "Glucose enters a red blood cell through GLUT1 toward lower [glucose]. Name the transport mode.",
                 ["A protein is required (glucose is large and polar).",
                  "Movement is down the concentration gradient.",
                  "No ATP is used at GLUT1, so this is facilitated diffusion (passive)."],
                 "facilitated diffusion", "", "Easy")
        + solved(11, "Why does adding aquaporins not reverse the direction of osmosis?",
                 ["Aquaporins are paths, not pumps.",
                  "Net direction follows water potential (solute and pressure).",
                  "More paths speed both directions; the net driving force is unchanged."],
                 "they change rate, not equilibrium direction", "", "Medium")
        + solved(12, "Sketch the logic: a carrier’s rate vs [solute] plateaus, but O₂ diffusion rate keeps rising more linearly in the same range. Why?",
                 ["Carriers have a finite number of binding sites that can be full (saturation).",
                  "O₂ uses the entire bilayer area as a path, not a limited number of pockets.",
                  "The plateau is evidence of a finite protein catalyst-like transporter, not of ATP use."],
                 "limited carrier sites vs bulk bilayer path", "", "Hard"),
        ("Labeling any protein-mediated transport as active",
         "Facilitated diffusion uses proteins and is still passive. Active means energy is used to move cargo against a gradient (or to maintain a gradient). Look at direction and ATP, not merely at ‘protein.’"),
        ("Write high → low on the paper",
         "Draw two boxes with concentrations and an arrow. If your arrow points low→high, you need a pump or cotransporter story, not osmosis-of-solute."),
        [
            "I can distinguish simple diffusion, facilitated diffusion, and osmosis.",
            "I can explain electrochemical gradients for ions.",
            "I can interpret saturation of a carrier.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Active transport",
        [
            "Active transport moves a solute against its gradient and therefore needs an energy source. The textbook example is ATP hydrolysis at a pump.",
            "The sodium–potassium pump is a P-type ATPase: 3 Na⁺ out, 2 K⁺ in, per ATP. It is electrogenic (nets +1 charge out) and builds the gradients neurons later spend.",
            "Primary active transport is the pump that burns ATP (or light, in bacteriorhodopsin) directly. Secondary active transport, or cotransport, spends a gradient that a pump already built.",
            "A symporter moves two solutes the same way; an antiporter moves them opposite ways. Intestinal Na⁺/glucose symport lets Na⁺ fall inward while glucose is scooped uphill into the cell.",
            "Bulk transport uses vesicles. Endocytosis (phagocytosis, pinocytosis, receptor-mediated) brings cargo in. Exocytosis secretes it. These cost energy to remodel the cytoskeleton and membranes, even though each molecule is not threaded through a tiny pump.",
            "If you poison ATP production, pumps fail first. Passive leaks continue for a while, gradients run down, and then secondary transporters fail too — a cascade AP loves to test.",
        ],
        "Nerve impulses, stomach acid, plant mineral uptake, and lysosome acidification are all pump stories. Unit 3’s proton gradient is the same idea in mitochondria.",
        "Split the energy bill: who hydrolyzes ATP (primary), and who merely rides the resulting gradient (secondary)?",
        lesson_figure(
            _pump_svg(),
            "A membrane pump using ATP",
            "Cargo moves uphill. ATP → ADP + Pᵢ is drawn because this is primary active transport, not facilitated diffusion.",
        )
        + solved(13, "Does the Na⁺/K⁺ pump move Na⁺ with or against its gradient in a typical animal cell? Name the energy source.",
                 ["[Na⁺] is already higher outside, so pumping Na⁺ out is against the gradient.",
                  "[K⁺] is higher inside, so pumping K⁺ in is also against its gradient.",
                  "The energy source is ATP hydrolysis."],
                 "both ions against their gradients; ATP", "", "Easy")
        + solved(14, "A plant proton pump uses ATP to push H⁺ out. Sucrose then enters with H⁺ on a cotransporter. Classify each step.",
                 ["H⁺ out against its gradient with ATP = primary active transport.",
                  "H⁺ back in downhill, sucrose in uphill on the same protein = secondary active (symport).",
                  "ATP was not hydrolyzed at the sucrose protein, but sucrose uptake still depends on the pump."],
                 "primary H⁺ pump; secondary H⁺/sucrose symport", "", "Medium")
        + solved(15, "Ouabain blocks the Na⁺/K⁺ pump. Explain in three steps why glucose absorption in the small intestine later slows.",
                 ["The pump normally keeps [Na⁺] low inside the epithelial cell.",
                  "Na⁺/glucose symporters need that inward Na⁺ gradient as a battery.",
                  "When the battery runs down, glucose can no longer be accumulated against its gradient, even if the symporter protein is intact."],
                 "secondary glucose uptake collapses when the Na⁺ gradient collapses", "", "Hard"),
        ("Thinking cotransport is free because the cotransporter does not bind ATP",
         "Someone paid ATP at the pump. Secondary transport is not magic; it is a saved gradient being spent. If the stem says ‘no ATP at this protein,’ still look for a coupled gradient."),
        ("Annotate arrows with ‘down’ or ‘up’ plus the energy source",
         "A messy diagram is how students pick ‘glucose simple diffusion’ for gut uptake. Force every arrow to confess its driving force."),
        [
            "I can define primary vs secondary active transport.",
            "I can describe the Na⁺/K⁺ pump stoichiometry and why it matters.",
            "I can explain endocytosis/exocytosis as bulk membrane traffic.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Tonicity and water potential",
        [
            "Tonicity describes how a solution makes a cell gain or lose water. It depends on solutes that cannot freely cross the membrane (effective osmoles), not on every molecule present.",
            "Hypertonic surroundings have more effective solute than the cell → water leaves → animal cell shrinks (crenates), plant cell plasmolyzes. Hypotonic: water enters → animal cell may lyse, plant cell becomes turgid. Isotonic: no net water change.",
            "Water potential $\\Psi$ is the free-energy status of water, in bars or MPa. Water moves from high $\\Psi$ to low $\\Psi$. Pure water at atmospheric pressure is $\\Psi=0$.",
            "The equation is $\\Psi=\\Psi_s+\\Psi_p$. Solute potential $\\Psi_s=-iCRT$, where $i$ is particles per formula unit (glucose $i=1$, NaCl $i\\approx2$), $C$ is molarity, $R=0.0831$ L·bar/mol·K, and $T$ is in kelvin. $\\Psi_s$ is never positive.",
            "Pressure potential $\\Psi_p$ is 0 in an open beaker. In a turgid plant cell it is positive because the wall pushes back. That positive pressure is why plants stand up.",
            "Work every AP water-potential item on paper: compute $\\Psi$ on both sides, then draw one arrow from the less negative (or more positive) side to the more negative side. Do not ‘follow the solute’ as a slogan without checking pressure.",
        ],
        "Plant FRQs, IV-fluid items, and kidney concentrating stories all reduce to Ψ arithmetic plus a membrane that water can cross.",
        "Compute numbers before adjectives. ‘Hypertonic’ is a cell-behavior word; $\\Psi$ is the physics. Use both, but do the algebra first.",
        lesson_figure(
            _tonicity_svg(),
            "Animal cells in three baths",
            "Left: hypotonic bath, cell swells. Middle: isotonic. Right: hypertonic bath, cell shrinks.",
        )
        + solved(16, "An animal cell is placed in seawater far saltier than its cytosol. What happens to its volume, and which tonicity word applies?",
                 ["Outside has more solute, so outside Ψ is lower (more negative).",
                  "Water leaves the cell and the cell shrinks.",
                  "The seawater is hypertonic to the cell."],
                 "shrinks; hypertonic", "", "Easy")
        + solved(17, "Open beaker of 0.4 M glucose at 295 K, $i=1$, $R=0.0831$. Find $\\Psi$.",
                 ["$\\Psi_p=0$ in an open beaker.",
                  "$\\Psi_s=-iCRT=-(1)(0.4)(0.0831)(295)$.",
                  "$(0.4)(0.0831)=0.03324$; times $295=9.8058$; so $\\Psi_s\\approx-9.81$ bar.",
                  "$\\Psi\\approx-9.81$ bar."],
                 "about −9.81 bar", "", "Medium")
        + solved(18, "Cell: $\\Psi_s=-8.0$ bar, $\\Psi_p=+3.0$ bar. Beaker (open): 0.25 M sucrose, 300 K, $i=1$, $R=0.0831$. Which way does water move?",
                 ["Cell $\\Psi=-8.0+3.0=-5.0$ bar.",
                  "Beaker $\\Psi_s=-(0.25)(0.0831)(300)=-6.2325$ bar; $\\Psi_p=0$; $\\Psi\\approx-6.23$ bar.",
                  "Water moves from higher Ψ to lower Ψ: from −5.0 (cell) to −6.23 (beaker), so water leaves the cell.",
                  "The cell will lose turgor; a plant cell would plasmolyze if enough water left."],
                 "water leaves the cell (−5.0 → −6.23 bar)", "", "Hard"),
        ("Forgetting $i$ for salts",
         "0.3 M NaCl is about 0.6 osmolar because $i\\approx2$. Treating it like 0.3 M glucose underestimates how negative $\\Psi_s$ is and can reverse your arrow."),
        ("Always compute both sides’ Ψ",
         "Students compare only concentrations and ignore turgor. A cell with high $\\Psi_p$ can have higher Ψ than a concentrated open beaker even if its $\\Psi_s$ is more negative. Do the sum."),
        [
            "I can predict swell/shrink using hypotonic, isotonic, and hypertonic.",
            "I can calculate $\\Psi_s=-iCRT$ with T in kelvin.",
            "I can decide water’s direction from two Ψ values, including pressure.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Prokaryotic vs eukaryotic architecture and SA/V",
            "Organelles and the payoff of compartmentalization",
            "Fluid mosaic membranes and selective permeability",
            "Passive transport, osmosis, and electrochemical gradients",
            "Primary and secondary active transport and vesicles",
            "Tonicity and water-potential calculations",
        ],
        body,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Cellular Energetics
# ===========================================================================

def _u3_questions():
    return _qs([
        ("An enzyme speeds a reaction by:",
         "lowering the activation energy, not by changing ΔG",
         "Activation energy $E_a$ is the energy hill to the transition state. The enzyme binds the substrate so that hill is shorter. The difference in free energy between reactants and products (ΔG) stays the same, so equilibrium is unchanged — only the rate changes.",
         ["raising ΔG so the reaction stores more energy", "being consumed as a reactant", "heating the whole cell to 100 °C as its only mechanism"]),
        ("The active site is complementary to the substrate. A competitive inhibitor:",
         "resembles the substrate and binds the active site, blocking substrate",
         "Competitive inhibitors fight for the same pocket. Adding lots of substrate can outcompete them (same $V_{max}$, higher apparent $K_m$). Noncompetitive inhibitors bind elsewhere and change shape.",
         ["binds only DNA", "raises $V_{max}$ by opening a second active site", "is always a lipid in the bilayer core"]),
        ("Induced fit means:",
         "the enzyme slightly changes shape around the substrate after binding",
         "The lock-and-key picture is too rigid. Both enzyme and substrate adjust, straining bonds toward the transition state. That is catalysis, not just sticking.",
         ["the substrate is chopped before it binds", "enzymes are carbohydrates that never fold", "ATP is the only possible substrate"]),
        ("Why are enzymes specific for one reaction or a small family?",
         "the 3-D chemistry of the active site matches one transition state",
         "Shape plus charges plus H-bond donors/acceptors create specificity. A mirror-image sugar often will not fit even if the formula is the same.",
         ["they randomly collide with every molecule in the cell equally", "specificity comes from the nucleus pumping substrates", "all enzymes bind every amino acid polymer"]),
        ("Cofactors are nonprotein helpers. A metal ion at an active site is a cofactor; an organic helper such as NAD⁺ is a:",
         "coenzyme",
         "Many vitamins are coenzyme precursors (niacin → NAD). Without the helper, the protein fold may be present but catalysis fails.",
         ["competitive inhibitor of itself", "a second substrate that is a polysaccharide wall", "an isotope of carbon only"]),
        ("Raising temperature from 10 °C to 30 °C usually increases enzyme rate at first because:",
         "more collisions have energy ≥ $E_a$",
         "Kinetic energy rises, so more substrate–enzyme encounters are productive. Beyond the optimum, the protein denatures and rate crashes. That is why the graph is a hill, not an endless climb.",
         ["enzymes melt into lipids at 20 °C in every species", "ΔG becomes more positive as T rises, stopping all reactions", "active sites disappear below 37 °C in all organisms"]),
        ("A stomach protease (pepsin) works at pH ~2; a blood enzyme at pH ~7.4. The difference exists because:",
         "each protein’s catalytic residues have a charge state that matches its pH",
         "pH changes which R groups are protonated. The ‘wrong’ pH is a reversible denaturation/charge mismatch, not a change in the gene. Location (stomach vs blood) selected different optima.",
         ["pepsin is a nucleic acid", "blood enzymes are made of cellulose", "pH cannot affect proteins"]),
        ("Noncompetitive inhibition lowers $V_{max}$ because:",
         "some enzyme molecules are locked in a less active shape no matter how much substrate you add",
         "The inhibitor’s allosteric site is not the substrate pocket, so flooding with substrate does not fully rescue rate. Competitive inhibition is the one you can dilute out with substrate.",
         ["$V_{max}$ rises when inhibitors bind", "noncompetitive inhibitors destroy all substrate molecules", "ATP is produced by the inhibitor"]),
        ("Feedback inhibition of a biosynthetic pathway usually uses the pathway’s:",
         "end product as an allosteric inhibitor of an early enzyme",
         "When the final metabolite is abundant, it binds an allosteric site on an early enzyme and slows the pathway. That prevents making more of what the cell already has. Activators exist too, but the classic AP story is end-product inhibition.",
         ["DNA primer as a competitive substrate", "a lysosome digesting the first enzyme’s gene", "cellulose as a coenzyme"]),
        ("On a rate vs [substrate] plot, $K_m$ is the [S] at half $V_{max}$. A smaller $K_m$ means:",
         "higher affinity — the enzyme reaches half speed at lower [S]",
         "Do not confuse $K_m$ with $V_{max}$. $V_{max}$ is speed when every enzyme is busy; $K_m$ is a concentration that reports how sticky the enzyme is for substrate.",
         ["the enzyme is slower at saturating [S]", "the enzyme has been denatured", "ΔG of the reaction is smaller"]),
        ("Glycolysis occurs in the cytosol and splits glucose into:",
         "two pyruvate, with net 2 ATP and 2 NADH",
         "Investment of 2 ATP, payoff of 4 ATP, net 2. No oxygen is required for glycolysis itself. Pyruvate’s fate depends on whether the cell can run aerobic respiration.",
         ["six CO₂ in the cytosol", "one acetyl-CoA only", "32 ATP with no NADH"]),
        ("The Krebs (citric acid) cycle in eukaryotes runs in the:",
         "mitochondrial matrix",
         "Pyruvate is oxidized to acetyl-CoA as it enters. Each turn (per acetyl-CoA) yields 3 NADH, 1 FADH₂, 1 ATP (or GTP), and 2 CO₂. Two turns per glucose.",
         ["thylakoid lumen", "nuclear envelope lumen", "cell wall"]),
        ("The electron transport chain pumps protons using energy from:",
         "high-energy electrons originally harvested from food (NADH/FADH₂)",
         "Electrons flow to O₂, the terminal acceptor. The proton gradient then drives ATP synthase (chemiosmosis). This is oxidative phosphorylation — most of the ATP from glucose.",
         ["the nucleus transcribing rRNA", "cellulose hydrolysis only", "Na⁺/K⁺ pumps in the cristae as the ETC"]),
        ("If cyanide blocks cytochrome c oxidase, [H⁺] in the intermembrane space falls and ATP from oxidative phosphorylation collapses because:",
         "electron flow stops, so proton pumping stops, so ATP synthase has no gradient",
         "The chain is a series. Block the end, and upstream carriers stay reduced. No flow, no pumping, no proton-motive force. Glycolysis might continue briefly with fermentation.",
         ["O₂ production in mitochondria increases", "glucose is no longer polar", "ATP synthase begins to run glycolysis"]),
        ("Fermentation regenerates NAD⁺ so glycolysis can continue. Lactic acid fermentation does this by:",
         "reducing pyruvate to lactate, oxidizing NADH back to NAD⁺",
         "The point is not ‘to make lactate for fun.’ Without NAD⁺, glycolysis stops and no ATP is made in anaerobic muscle. Yeast instead make ethanol + CO₂.",
         ["pumping protons in the thylakoid", "running the Krebs cycle without enzymes", "converting lactate into oxygen"]),
        ("The light reactions of photosynthesis occur in the thylakoid membrane and produce:",
         "ATP, NADPH, and O₂ (from water)",
         "Photolysis splits H₂O, releasing O₂. Electrons travel the photosynthetic ETC, making a proton gradient (ATP) and reducing NADP⁺ to NADPH. The Calvin cycle later spends ATP and NADPH.",
         ["glucose directly inside the thylakoid lumen as the only product", "CO₂ from splitting water", "NADH for the Krebs cycle in the stroma"]),
        ("The Calvin cycle (stroma) fixes carbon when Rubisco attaches CO₂ to:",
         "RuBP (ribulose bisphosphate)",
         "The product is an unstable 6-carbon that splits into two 3-PGA. ATP and NADPH then reduce carbon to G3P. Some G3P leaves to make sugar; the rest rebuilds RuBP.",
         ["glucose 6-phosphate as the first CO₂ acceptor", "chlorophyll a in PSII", "O₂ in photorespiration as the intended substrate"]),
        ("Why is O₂ a product of photosynthesis but a reactant of aerobic respiration?",
         "water is split in the light reactions; O₂ later accepts electrons at the mitochondrial ETC",
         "The atoms in photosynthetic O₂ come from H₂O, not from CO₂ (van Niel / isotope experiments). Respiration uses that O₂ as the terminal electron acceptor, making H₂O again. The two processes cycle the same atoms.",
         ["O₂ is made from CO₂ in the Calvin cycle", "mitochondria split water to make O₂", "plants never respire"]),
        ("A graph of photosynthetic rate vs light intensity saturates because:",
         "another factor (CO₂, Rubisco, ETC capacity) becomes limiting",
         "This is the law of limiting factors. At high light, adding more photons does not help if carbon fixation is the bottleneck. AP graphs often show a plateau, then a drop at extreme T.",
         ["light is never used in photosynthesis", "chlorophyll is made of cellulose", "saturation means the plant has died"]),
        ("C4 and CAM plants reduce photorespiration in hot, dry climates by:",
         "concentrating CO₂ around Rubisco (spatial or temporal separation from O₂)",
         "Rubisco can bind O₂ when stomata close and [O₂]/[CO₂] rises. C4 uses a four-carbon shuttle in mesophyll vs bundle-sheath. CAM opens stomata at night. Both are fitness strategies for water vs carbon.",
         ["eliminating photosystem II", "turning off the Calvin cycle forever", "using mitochondria as the only CO₂-fixing organelle"]),
        ("Natural selection favors energy strategies that:",
         "match ATP yield and cost to the organism’s habitat and lifestyle",
         "Yeast switch between respiration and fermentation. Muscle fibers are glycolytic or oxidative. Plants invest in C4 anatomy only where the water/photorespiration tradeoff pays. Fitness is context, not ‘more ATP always wins.’",
         ["always maximize ATP even if it costs more water than the habitat allows", "never use fermentation because it yields 2 ATP", "store energy only as DNA"]),
        ("Why does a hibernating mammal still run metabolism, just slower?",
         "cells still need ATP for pumps, repair, and a lower-rate basal metabolism",
         "Energy strategy can be ‘turn the thermostat down,’ not ‘off.’ Uncoupling proteins in brown fat even waste the proton gradient as heat — a different fitness goal than ATP yield.",
         ["hibernation replaces ATP with cellulose", "pumps stop needing gradients in winter", "DNA replication is the only remaining ATP use and it accelerates"]),
        ("Anaerobic soil bacteria that use sulfate as a terminal electron acceptor are using:",
         "anaerobic respiration, not the same as lactic fermentation",
         "Fermentation has no ETC. Anaerobic respiration has an ETC with a non-O₂ acceptor (nitrate, sulfate). Both happen without O₂, but the ATP yield and machinery differ. AP wants that vocabulary split.",
         ["the Calvin cycle in reverse in animals", "photosystem I only", "glycolysis stopping on purpose to save NAD⁺"]),
        ("Endotherms spend more energy on heat than many ectotherms. The tradeoff is:",
         "stable internal T for enzymes vs a higher food requirement",
         "Enzyme optima are easier to keep if body T is stable. The fitness cost is calories. Ectotherms can survive on less food but enzyme rates track the environment.",
         ["endotherms have no enzymes", "ectotherms cannot have mitochondria", "heat is made by chloroplasts in mammals"]),
        ("Storing energy as fat vs glycogen: fat is denser per gram; glycogen is:",
         "faster to mobilize and can feed glycolysis without oxygen as quickly",
         "Muscle glycogen supports sprint ATP via glycolysis. Fat feeds slower aerobic pathways. Fitness is about which fuel matches the activity, not which number is larger in a table.",
         ["glycogen stores more calories per gram than fat", "fat can be used by the brain as readily as glucose in all mammals without ketones", "glycogen is a nucleic acid"]),
        ("ATP is the cell’s rechargeable battery. Hydrolysis of ATP to ADP + Pᵢ is exergonic, so it can be:",
         "coupled to an endergonic reaction to make the pair exergonic overall",
         "Cells do not ‘use heat’ to push biosynthesis. They couple a downhill ATP step to an uphill step, often by transferring a phosphate (phosphorylation) so the intermediate is reactive.",
         ["converted into a gene", "used only to lower temperature", "an enzyme that is consumed"]),
        ("If reaction A has $ΔG=+4$ kcal/mol and ATP hydrolysis has $ΔG=-7.3$ kcal/mol, a 1:1 coupling has net $ΔG$ about:",
         "−3.3 kcal/mol (spontaneous as written)",
         "$+4 + (-7.3) = -3.3$. The coupled pair can proceed. If the uphill reaction were +8, one ATP would not be enough without additional coupling.",
         ["+11.3 kcal/mol", "0 by definition for all couplings", "+4 kcal/mol because ATP is ignored"]),
        ("ATP synthase makes ATP when protons flow:",
         "down their electrochemical gradient through the enzyme (chemiosmosis)",
         "The synthase is a rotary motor. In mitochondria, H⁺ flows from intermembrane space to matrix. In chloroplasts, from thylakoid lumen to stroma. Same machine, opposite organelle geometry.",
         ["up their gradient using light inside ATP synthase itself in animals", "through the nuclear pores only", "from NADH directly into glucose"]),
        ("Phosphofructokinase (PFK) in glycolysis is inhibited by ATP and citrate and activated by AMP. This is:",
         "allosteric feedback that matches glycolysis to energy charge",
         "When ATP is plentiful, you do not burn more glucose at PFK. When AMP is high, the cell is hungry and PFK opens. That is energy-strategy regulation at a single enzyme.",
         ["a change in the DNA sequence of glucose", "Rubisco fixing AMP", "competitive inhibition by cellulose"]),
        ("Why must NAD⁺ be regenerated (via ETC or fermentation) for glycolysis to continue?",
         "glycolysis needs NAD⁺ as an electron acceptor at GAPDH; a finite pool would stay stuck as NADH",
         "Coenzymes are recycled, not consumed in stoichiometric tons. This is why fermentation ‘exists’: not for lactate glory, but for NAD⁺.",
         ["NAD⁺ is a carbohydrate stored in the wall", "glycolysis uses NAD⁺ to pump protons in the thylakoid", "NAD⁺ is converted into O₂"]),
        ("A competitive inhibitor raises apparent $K_m$ but not true $V_{max}$. On a graph that means:",
         "you need more substrate to reach the same half-speed, but saturating [S] still hits the original $V_{max}$",
         "That is how you distinguish competitive from noncompetitive on AP plots. Noncompetitive drops the ceiling ($V_{max}$).",
         ["$V_{max}$ falls and $K_m$ is unchanged always", "the enzyme is destroyed", "ΔG reverses"]),
        ("Boiling an enzyme usually abolishes activity because:",
         "tertiary structure (active site) unfolds; peptide bonds may still be intact",
         "Denaturation is a structure–function item from Unit 1 living in Unit 3. Cooling a boiled enzyme rarely restores activity if the unfold was severe (aggregation).",
         ["primary structure is rewritten by heat into a new gene", "substrates become radioactive", "boiling creates a better active site"]),
        ("In mitochondria, where is [H⁺] highest during active respiration?",
         "intermembrane space",
         "ETC complexes pump out of the matrix into the intermembrane space. ATP synthase lets H⁺ back into the matrix. Mix this up with chloroplasts (lumen high H⁺) on every AP exam.",
         ["matrix", "cytosol exclusively", "the nucleolus"]),
        ("How many CO₂ are released per glucose in aerobic respiration once both pyruvates are fully oxidized?",
         "6",
         "Glucose is C₆. Each pyruvate (C₃) loses 1 C as CO₂ to make acetyl-CoA, then 2 more in the Krebs cycle: 3 per pyruvate × 2 = 6. That matches 6 O₂ used in the overall equation.",
         ["2", "12", "1"]),
        ("Photosystem II’s electrons come from water. Photosystem I’s electrons, in linear flow, come from:",
         "the chain after PSII (plastocyanin), and they ultimately reduce NADP⁺",
         "Linear (noncyclic) flow: H₂O → PSII → ETC → PSI → NADP⁺. Cyclic flow around PSI makes extra ATP but no NADPH or O₂. AP may ask which products vanish if PSII is blocked: O₂ and the electron supply.",
         ["the Calvin cycle’s G3P", "O₂ in the air as an electron donor to PSI", "ATP synthase spinning backward"]),
        ("A poison that makes the inner mitochondrial membrane leaky to H⁺ (uncoupler) will:",
         "increase O₂ use while ATP synthesis falls, with energy lost as heat",
         "Electrons still flow (O₂ still consumed) but the gradient cannot be maintained, so ATP synthase starves. Brown fat does a controlled version of this.",
         ["stop electron flow and stop O₂ use while ATP skyrockets", "convert mitochondria into chloroplasts", "raise ΔG of ATP hydrolysis to zero"]),
        ("Rubisco’s oxygenase activity (photorespiration) is costly because:",
         "it burns ATP/NADPH without net carbon gain and can release CO₂",
         "In hot closed-stomata leaves, [O₂]/[CO₂] rises. Photorespiration is a leak in the carbon-fixing machine. C4/CAM are evolutionary patches.",
         ["it makes extra glucose from O₂", "it is the main source of O₂ on Earth", "it replaces the need for light reactions"]),
        ("Which comparison of ATP yield is fairest?",
         "aerobic respiration of glucose >> fermentation, because NADH is cashed at the ETC",
         "Fermentation: net 2 ATP/glucose. Aerobic: on the order of 30. The extra is oxidative phosphorylation. Do not claim glycolysis ‘makes 32 ATP.’",
         ["fermentation makes more ATP than the ETC", "glycolysis requires O₂ to make its net 2 ATP", "the Krebs cycle makes 32 ATP in the cytosol"]),
        ("A plant in the dark still needs ATP. It gets it from:",
         "cellular respiration of stored sugars, like other eukaryotes",
         "Photosynthesis is not 24-hour ATP. Roots never photosynthesize. Dark still means mitochondria. ‘Plants only photosynthesize’ is a middle-school leftover.",
         ["the Calvin cycle running without NADPH", "splitting CO₂ into ATP", "fermentation of cellulose in the nucleus"]),
        ("Why does adding more enzyme (not substrate) raise $V_{max}$?",
         "$V_{max}$ is proportional to enzyme concentration when [S] is saturating",
         "More catalytic sites, higher ceiling. $K_m$ is a property of the enzyme–substrate pair and does not have to change. This is how cells regulate capacity: make more enzyme, or activate more.",
         ["enzyme amount cannot change rate", "$K_m$ is enzyme concentration", "ΔG depends on enzyme amount"]),
        ("Chemiosmosis is used in both mitochondria and chloroplasts. A true shared statement is:",
         "a proton gradient drives ATP synthase",
         "The electron sources and terminal acceptors differ (food → O₂ vs water → NADP⁺), and the high-H⁺ compartment differs, but the coupling principle is the same — a reason AP teaches them as a pair.",
         ["both split water to make O₂ as the only ATP source", "both fix CO₂ in the matrix", "both require a nucleus inside the organelle to pump H⁺"]),
        ("If NADPH is abundant and NADP⁺ is scarce, chloroplasts may shift toward cyclic electron flow to:",
         "make ATP without making more NADPH",
         "Calvin needs a higher ATP:NADPH ratio than linear flow alone may provide. Cyclic flow around PSI is a tuning knob. Fitness again: match products to the Calvin demand.",
         ["make O₂ without PSII", "fix nitrogen in the lumen", "run glycolysis in the thylakoid"]),
        ("A mutant PFK that cannot bind ATP at its allosteric site would:",
         "keep running glycolysis even when ATP is already high, wasting glucose",
         "Loss of feedback is as dangerous as a dead enzyme. Regulation is part of energy strategy.",
         ["stop glycolysis at all ATP levels", "fix CO₂", "pump protons without an ETC"]),
        ("Oxygen consumption by isolated mitochondria rises when ADP is added (respiratory control) because:",
         "ATP synthase can run, H⁺ flows in, the gradient eases, and the ETC can resume pumping",
         "If synthase is stuck (no ADP), the gradient maxes out and ETC thermodynamically stalls. ADP is the ‘need ATP’ signal. Beautiful coupling.",
         ["ADP is the terminal electron acceptor instead of O₂", "ADP denatures cytochrome oxidase", "mitochondria convert ADP into O₂"]),
        ("G3P from the Calvin cycle can become glucose, but five of every six G3P carbons stay to rebuild RuBP. That matters because:",
         "the cycle must regenerate the CO₂ acceptor or fixation stops",
         "Students think ‘Calvin makes a glucose and is done.’ Regeneration is the majority of the cycle’s work. Same logic as the Krebs cycle regenerating oxaloacetate.",
         ["RuBP is made from O₂", "G3P cannot leave the chloroplast ever", "Rubisco is regenerated from ATP only"]),
        ("An ectothermic fish’s enzymes have a lower temperature optimum than a bird’s. That is adaptation because:",
         "the protein’s weak interactions are tuned so the active site is intact at the animal’s real body T",
         "‘Optimum’ is not morally better at 37 °C. It is matching structure to habitat. A bird enzyme in a cold fish would be too rigid; a cold-adapted enzyme in a bird might unfold.",
         ["fish enzymes are RNA and bird enzymes are DNA", "birds lack mitochondria", "temperature optima cannot evolve"]),
        ("AP Stretch: On a Lineweaver–Burk plot ($1/v$ vs $1/[S]$), the x-intercept is $-1/K_m$ and the y-intercept is $1/V_{max}$. Competitive inhibition raises apparent $K_m$, so $|x$-intercept$|$ shrinks toward the origin, while the y-intercept is unchanged. A mystery inhibitor leaves the y-intercept matching the control but moves the x-intercept closer to zero. The inhibitor is:",
         "competitive — same $V_{max}$, higher apparent $K_m$",
         "Same y-intercept means $1/V_{max}$ (and $V_{max}$) is unchanged. A larger apparent $K_m$ makes $|-1/K_m|$ smaller, so the x-intercept slides toward the origin, not farther out. Noncompetitive inhibition lowers $V_{max}$ and therefore raises the y-intercept.",
         ["noncompetitive, because $K_m$ never changes in any inhibition", "an uncoupler of oxidative phosphorylation", "a photosystem II blocker"]),
        ("AP Stretch: Isolated thylakoids are soaked in pH 4 buffer, then rapidly shifted to pH 8 with ADP + Pᵢ in the dark. ATP appears briefly because:",
         "an artificial H⁺ gradient (lumen acidic vs stroma basic) drives ATP synthase without light",
         "This is the Jagendorf experiment: the gradient, not light per se, is the immediate energy source for photophosphorylation. Light’s job in vivo is to build that gradient.",
         ["the Calvin cycle ran in the dark using pH 4 as carbon", "PSII split water after the pH jump with no photons", "ATP synthase uses pH 8 as a substrate instead of ADP"]),
        ("AP Stretch: A cell has plenty of O₂ but a poisoned Krebs cycle (no acetyl-CoA oxidation). NADH from glycolysis can still feed the ETC only if:",
         "pyruvate oxidation or other NADH sources continue — if those also stop, the ETC starves of electrons even with O₂ present",
         "O₂ is the acceptor, not the donor. No NADH/FADH₂ ⇒ no flow. Students treat O₂ as sufficient for oxidative phosphorylation. It is necessary, not sufficient.",
         ["O₂ can replace NADH as the electron donor to complex I", "glycolysis produces 32 ATP in the matrix automatically", "the ETC runs on cellulose"]),
        ("AP Stretch: Compare ΔG of ATP hydrolysis in a cell (~ −11 to −13 kcal/mol) vs standard −7.3. It is more negative in vivo because:",
         "mass action: cells keep [ATP]/[ADP][Pᵢ] far from equilibrium",
         "ΔG = ΔG° + RT ln Q. Pumps and mitochondria maintain a high ATP ratio, so hydrolysis is even more strongly downhill — which is why coupling works so well. The battery is kept charged.",
         ["cells have a different chemical formula for ATP", "ΔG° is defined to be more negative inside mitochondria only", "temperature in cells is 0 K"]),
        ("AP Stretch: C4 anatomy spends about 2 extra ATP per CO₂ on the PEP-carboxylase shuttle versus C3. In a cool, wet forest where stomata stay open and photorespiration is already low, C3 often has higher growth because:",
         "the extra ATP tax is not repaid when Rubisco is not wasting energy on O₂",
         "C4 (and CAM) are fitness tools for heat/drought, not universally ‘better photosynthesis.’ If photorespiration is cheap, paying 2 extra ATP per carbon is a net loss. That is why C3 trees dominate many temperate wet canopies.",
         ["C3 plants never make sugar in forests", "C4 leaves cannot open stomata", "the extra ATP is required to split water in PSII only in forests"]),
        ("AP Stretch: If a mutation removes the allosteric AMP site on PFK but leaves catalytic function, which patient-level metabolic pattern is most likely?",
         "poor ability to ramp up glycolysis during energy demand; or, if the site was inhibitory ATP, the opposite — here AMP is the activator, so exercise ATP supply lags",
         "AMP should activate PFK when energy is low. Losing that site means glycolysis does not hear the ‘we are hungry’ signal. The catalytic site still works at a basal rate, but regulation is deaf.",
         ["the person cannot transcribe any genes", "Rubisco replaces PFK in muscle", "mitochondria vanish"]),
        ("AP Stretch: In the light, chloroplast stroma pH rises (H⁺ pumped into the lumen). Some Calvin enzymes activate at high pH/Mg²⁺. This coupling means:",
         "carbon fixation turns on when the light reactions are actually running",
         "Post-translational, physiological regulation — not a new gene each sunrise. Structure (pH-sensitive enzymes) meets function (don’t run Calvin without ATP/NADPH).",
         ["the Calvin cycle prefers acidic stroma like a lysosome", "light directly ligates CO₂ to RuBP without Rubisco", "stroma pH rise stops ATP synthase"]),
        ("AP Stretch: Oligomycin blocks ATP synthase’s proton pore. O₂ use then slows even though complexes I–IV are intact. A later protonophore restores O₂ consumption but ATP from oxidative phosphorylation stays near zero. The AP explanation is:",
         "the stalled gradient back-pressures the ETC; the protonophore relieves that back-pressure without routing H⁺ through ATP synthase",
         "When H⁺ cannot re-enter through ATP synthase, ΔpH grows until pumping (and therefore electron flow and O₂ use) stall. A leak pathway lets H⁺ return, so the ETC runs again, but the return path is not the synthase, so phosphorylation does not resume. That two-step contrast is not the same as naming DNP’s heat effect alone.",
         ["oligomycin converts O₂ into glucose in the matrix", "the protonophore repairs ATP synthase’s catalytic sites", "complexes I–IV require oligomycin as a cofactor"]),
        ("AP Stretch: A graph shows photosynthetic O₂ output vs wavelength (action spectrum) not identical to chlorophyll a’s absorption peaks. The AP explanation is:",
         "accessory pigments absorb other wavelengths and pass energy to the reaction center",
         "The action spectrum is the organism’s, not one molecule’s. Carotenoids fill the green-yellow gap somewhat and protect from photodamage. Structure of the antenna → function of broader light use.",
         ["plants reflect all light they use", "water splitting works only in green light", "Rubisco absorbs 700 nm photons directly"]),
    ])


def build_unit3():
    title = "AP Biology Unit 3: Cellular Energetics"
    description = (
        "Enzymes, respiration, photosynthesis, energy strategies, and ATP coupling — "
        "with energy diagrams, rate graphs, and consistent stoichiometry."
    )

    c1 = concept_block(
        "1. Enzyme structure and specificity",
        [
            "A chemical reaction can be spontaneous (negative $ΔG$) and still be slow if the path over the transition-state hill is high. That hill is the activation energy $E_a$. Cells cannot survive by boiling themselves to supply $E_a$ for every reaction.",
            "An enzyme is a catalyst, usually a protein, that binds a substrate at an active site and lowers $E_a$. It is not consumed. It does not change $ΔG$ or the equilibrium constant; it only helps the reaction reach equilibrium faster.",
            "Specificity comes from complementary shape and chemistry: hydrogen bonds, ionic contacts, and hydrophobic patches that fit one substrate (or a close family) and stabilize the transition state more than the ground state.",
            "Induced fit: the enzyme wraps around the substrate after binding, straining bonds. Think of it as the protein using binding energy to pay for reaching the transition state.",
            "Cofactors (metal ions) and coenzymes (organic helpers such as NAD⁺, FAD, coenzyme A) sit in many active sites. Vitamins often exist because we cannot synthesize those coenzyme pieces.",
            "Inhibitors prove the geometry. A competitive inhibitor mimics the substrate and occupies the active site. A noncompetitive (allosteric) inhibitor binds elsewhere and reshapes the site so catalysis fails even when substrate is present.",
        ],
        "Every metabolic pathway in this unit is a sequence of enzyme-catalyzed steps. If you treat enzymes as ‘magic speed dust,’ regulation and poisons will make no sense.",
        "Write two sentences on every enzyme item: (1) what happens to $E_a$ and rate, (2) what does not change (ΔG, equilibrium). Then name the site the inhibitor hits.",
        lesson_figure(
            _enzyme_ea_svg(),
            "Reaction coordinate: uncatalyzed vs catalyzed",
            "The enzyme shortens the hill (lower Ea). Reactants vs products (ΔG) stay at the same relative heights.",
        )
        + solved(1, "Does an enzyme make a +ΔG reaction negative? What does it change?",
                 ["Catalysts do not alter ΔG of the reaction as written.",
                  "They lower $E_a$, so a larger fraction of collisions succeed per second.",
                  "A +ΔG reaction still needs coupling (often to ATP) to proceed net forward."],
                 "no; it lowers $E_a$ / raises rate only", "", "Easy")
        + solved(2, "Methotrexate resembles folic acid and binds dihydrofolate reductase’s active site. What kind of inhibitor is it, and what happens if you flood the cell with substrate?",
                 ["It is a substrate look-alike in the active site → competitive.",
                  "High [substrate] can outcompete the inhibitor for the pocket.",
                  "$V_{max}$ can still be reached; apparent $K_m$ rises."],
                 "competitive; extra substrate relieves inhibition", "", "Medium")
        + solved(3, "A mutation replaces a catalytic serine with alanine. Binding still occurs weakly, but $k_{cat}$ collapses. Interpret.",
                 ["The active-site chemistry (the –OH that attacks) is gone.",
                  "Shape may still allow some binding, so $K_m$ might not explode, but chemistry fails.",
                  "This separates binding from catalysis — both are parts of ‘specificity,’ but catalysis needs the right functional groups."],
                 "binding ≠ catalysis; the nucleophilic R group was required", "", "Hard"),
        ("Saying enzymes are used up like reactants",
         "If they were used up, cells would have to rebuild every catalyst after every reaction. Catalysts regenerate. That is why a little enzyme can process a lot of substrate."),
        ("Sketch the energy hill and mark $E_a$ vs ΔG",
         "A 10-second drawing stops you from picking ‘enzymes make ΔG more negative’ on a multiple-choice item."),
        [
            "I can explain how enzymes lower $E_a$ without changing ΔG.",
            "I can contrast competitive and noncompetitive inhibition.",
            "I can connect active-site chemistry to specificity.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Environmental effects on enzymes",
        [
            "Each enzyme has an optimum temperature and pH where its fold and catalytic residues are correctly set. Those optima match the enzyme’s real workplace: pepsin at pH 2, trypsin at pH ~8, a hot-spring polymerase at 75 °C.",
            "From low T up to the optimum, rate usually rises because molecules collide more often with enough energy. Past the optimum, hydrogen bonds and hydrophobic packing fail, the active site unravels, and rate falls — often steeply.",
            "pH changes the protonation of R groups. Histidine is especially sensitive near neutrality. A charge that should attract substrate can vanish, or a salt bridge that held the fold can break.",
            "Substrate concentration: at low [S], rate is almost linear in [S]. At high [S], enzyme is saturated and rate approaches $V_{max}$. $K_m$ is [S] at $V_{max}/2$ — a report of affinity (lower $K_m$, tighter effective binding).",
            "Cells regulate enzymes without destroying them: allosteric activators/inhibitors, phosphorylation, and feedback inhibition by a pathway’s end product. Phosphofructokinase listening to ATP/AMP is the canonical example.",
            "On AP graphs, read axes first. A temperature hill vs a pH hill vs a hyperbolic [S] curve vs a sigmoid allosteric curve are four different stories. Match the shape to the mechanism before you talk.",
        ],
        "FRQs will hand you a graph and a mutant. If you cannot read $K_m$, $V_{max}$, and denaturation off a picture, Unit 3 becomes guesswork.",
        "Ask: is this kinetics (how fast) or thermodynamics (will it go)? Environment mostly hits kinetics via structure. Then name the structural reason (unfolding vs charge vs occupancy).",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", sample_curve(lambda t: 14 * math.exp(-((t - 37) ** 2) / 220), 0, 70))],
                xlim=(0, 70), ylim=(0, 16), xlab="temp (°C)", ylab="rate",
                points=[(37, 14, "opt 37 °C")],
            ),
            "Enzyme rate vs temperature",
            "Collisions help up to the optimum; then denaturation wins. The curve is a hill, not a straight climb.",
        )
        + solved(4, "Pepsin’s rate is high at pH 2 and nearly zero at pH 7. Why did the protein not ‘forget’ its gene?",
                 ["The amino-acid sequence is unchanged.",
                  "At pH 7 the catalytic residues and fold are in the wrong charge/shape state.",
                  "Activity is a function of environment acting on structure, not of a new mutation."],
                 "wrong pH disrupts charge/fold; sequence is the same", "", "Easy")
        + solved(5, "Two enzymes have the same $V_{max}$. Enzyme A has $K_m=0.1$ mM, B has $K_m=2$ mM. Which is more effective at 0.1 mM substrate, and why?",
                 ["At [S]=0.1 mM, A is at its $K_m$ so it runs at half $V_{max}$.",
                  "B is far below its $K_m$, so it is mostly idle.",
                  "A has higher affinity and wins at low [S], even though their ceilings match."],
                 "enzyme A; lower $K_m$ means better performance at low [S]", "", "Medium")
        + solved(6, "ATP inhibits PFK allosterically. Sketch what happens to glycolysis when ATP is high, and why that is useful.",
                 ["High ATP binds an allosteric site, shifting PFK toward a low-affinity shape.",
                  "Fructose-6-phosphate is not phosphorylated as readily; glycolysis slows.",
                  "The cell stops burning glucose for ATP it does not need — feedback matched to energy charge."],
                 "glycolysis slows; prevents wasting glucose when energy-rich", "", "Hard"),
        ("Assuming hotter is always faster",
         "A fever of 42 °C can wreck human enzymes. Thermophiles have different amino-acid packing so their ‘hill’ is shifted right. Copying a human enzyme into a hot spring without redesign fails."),
        ("Name the axis, then the mechanism",
         "If x is temperature, talk collisions then unfolding. If x is [S], talk occupancy and $V_{max}$. If x is inhibitor, say competitive vs allosteric. Graph literacy is the strategy."),
        [
            "I can interpret temperature, pH, and [S] effects on enzyme rate.",
            "I can use $K_m$ and $V_{max}$ in a sentence that means something.",
            "I can explain feedback inhibition with PFK or a similar enzyme.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Cellular respiration",
        [
            "Cellular respiration is the controlled oxidation of food to harvest electrons and make ATP. The overall aerobic story is $C_6H_{12}O_6+6O_2\\rightarrow 6CO_2+6H_2O$ plus a large ATP yield (on the order of 30 per glucose, not a mystic 38 in living cells).",
            "Glycolysis in the cytosol: glucose → 2 pyruvate, net 2 ATP + 2 NADH. It does not require oxygen. If oxygen and mitochondria are available, pyruvate enters the mitochondrion.",
            "Pyruvate oxidation makes acetyl-CoA + CO₂ + NADH. The citric acid cycle in the matrix finishes oxidizing the carbons to CO₂ and loads NADH and FADH₂. Those reduced coenzymes are the real payoff, not the cycle’s 2 ATP per glucose.",
            "The electron transport chain in the inner membrane lets electrons fall toward O₂. Released energy pumps H⁺ into the intermembrane space. ATP synthase lets H⁺ flow back into the matrix and phosphorylates ADP (oxidative phosphorylation).",
            "If oxygen is missing, many cells ferment: they dump electrons from NADH onto pyruvate (or a derivative) so NAD⁺ returns and glycolysis can keep making 2 ATP. Fermentation is not an ETC with a substitute gas; it has no chemiosmotic pump.",
            "Poisons map the path: cyanide blocks the last complex; oligomycin blocks ATP synthase; uncouplers leak H⁺. Predicting what happens to O₂ use, NADH, and ATP is the AP skill.",
        ],
        "Photosynthesis will look like this pathway run with different electron donors and acceptors. Learn chemiosmosis once, use it twice.",
        "Follow the carbons (where is CO₂ released?), then the electrons (who holds them?), then the protons (where is the gradient?), then ATP (substrate-level vs oxidative).",
        lesson_figure(
            _resp_boxes_svg(),
            "Three stages of aerobic respiration",
            "Glycolysis (cytosol) → Krebs (matrix) → ETC (inner membrane). Most ATP is from the last stage.",
        )
        + solved(7, "Where is the proton gradient in respiring mitochondria, and which way do H⁺ flow through ATP synthase?",
                 ["H⁺ is pumped into the intermembrane space (high [H⁺] there).",
                  "ATP synthase lets H⁺ flow down into the matrix.",
                  "That downhill flow is the immediate energy source for ATP."],
                 "high H⁺ in intermembrane space; flow into matrix", "", "Easy")
        + solved(8, "A muscle cell with no O₂ still makes 2 ATP per glucose. Name the pathway pair and the molecule that must be regenerated.",
                 ["Glycolysis plus lactic fermentation.",
                  "Pyruvate is reduced to lactate so NADH is oxidized.",
                  "NAD⁺ regeneration is the point; lactate is the byproduct."],
                 "glycolysis + lactate fermentation; NAD⁺", "", "Medium")
        + solved(9, "Uncoupler DNP lets H⁺ leak across the inner membrane. Predict ATP, O₂ use, and heat, briefly.",
                 ["The gradient cannot be maintained, so ATP from oxidative phosphorylation falls.",
                  "Electron flow may speed (less back-pressure), so O₂ use can rise.",
                  "The energy of the gradient becomes heat instead of ATP."],
                 "ATP down; O₂ use up; heat up", "", "Hard"),
        ("Crediting glycolysis with ~30 ATP",
         "Net 2 ATP from glycolysis is substrate-level. The big harvest is NADH cashed at the ETC when oxygen is present. Keep the books separate."),
        ("Draw the mitochondrion and write ‘H⁺’ on the correct side",
         "Mixing matrix vs intermembrane space is the difference between a 5 and a 2 on chemiosmosis items. Thirty seconds of labeling prevents it."),
        [
            "I can place glycolysis, Krebs, and ETC in the correct compartments.",
            "I can explain chemiosmosis and the role of O₂.",
            "I can contrast fermentation with anaerobic respiration.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Photosynthesis",
        [
            "Photosynthesis converts light energy into chemical energy in sugars. The simplified equation $6CO_2+6H_2O\\rightarrow C_6H_{12}O_6+6O_2$ hides two stages: light reactions and the Calvin cycle.",
            "In the thylakoid membrane, photosystem II splits water (photolysis). O₂ is released; electrons enter an ETC that pumps H⁺ into the thylakoid lumen; ATP is made as H⁺ exits to the stroma through ATP synthase. Photosystem I reduces NADP⁺ to NADPH.",
            "The Calvin cycle in the stroma uses ATP and NADPH to fix CO₂. Rubisco attaches CO₂ to RuBP. Products rearrange to G3P. Some G3P becomes sugar; most carbon is used to rebuild RuBP so the cycle can continue.",
            "The O₂ you breathe comes from water, not from CO₂. Isotope experiments settled that. CO₂’s carbon becomes the carbon of sugar.",
            "Light intensity, CO₂ concentration, and temperature each can limit rate. Graphs plateau when a different factor becomes limiting. Extreme heat closes stomata, raising photorespiration (Rubisco binding O₂).",
            "C4 and CAM plants add CO₂-concentrating tricks so Rubisco sees more CO₂ and less O₂ when water is scarce. They spend extra ATP for that privilege — a Unit 3 preview of ecological tradeoffs.",
        ],
        "You cannot explain plant productivity, climate, or the O₂ in Earth’s air without this pathway. It is also the conceptual mirror of respiration.",
        "Separate the stages on paper: light reactions (ATP, NADPH, O₂) vs Calvin (sugar, ADP, NADP⁺). Then match each chemical to thylakoid vs stroma.",
        lesson_figure(
            _chloro_svg(),
            "Chloroplast: thylakoids vs stroma",
            "Light reactions on stacked thylakoid membranes. Calvin cycle in the surrounding stroma.",
        )
        + solved(10, "A researcher labels H₂O with $^{18}O$. Where does the label appear in the photosynthetic products?",
                 ["Photolysis of water occurs at PSII.",
                  "The O atoms of O₂ gas come from water.",
                  "The label shows up in O₂, not in the carbohydrate’s oxygen as the primary product."],
                 "in O₂ gas from photolysis", "", "Easy")
        + solved(11, "If PSII is blocked by a herbicide, which products drop first, and does the Calvin cycle keep running for long?",
                 ["No electron extraction from water → no O₂, and the chain cannot reduce NADP⁺ well.",
                  "ATP from linear flow also falls (though cyclic PSI flow might linger briefly).",
                  "Calvin needs ATP and NADPH, so sugar production stops once pools run out."],
                 "O₂/NADPH (and then sugar) collapse; Calvin cannot continue unaided", "", "Medium")
        + solved(12, "Why does a C4 leaf spend ATP to pump CO₂ to bundle-sheath cells?",
                 ["In heat, stomata close, [O₂]/[CO₂] rises, and Rubisco wastes energy in photorespiration.",
                  "C4 anatomy plus PEP carboxylase concentrates CO₂ around Rubisco.",
                  "The extra ATP is the price of keeping water and still fixing carbon — a fitness tradeoff."],
                 "to suppress photorespiration while conserving water", "", "Hard"),
        ("Thinking plants do not respire",
         "Leaves and roots run mitochondria day and night. Photosynthesis can outrun respiration in the light, so net O₂ is released, but both pathways exist in the same eukaryotic cell.",),
        ("Box the two stages before reading choices",
         "If the question mentions O₂, think water and PSII. If it mentions sugar, think Calvin and stroma. Mixing those boxes is the usual trap."),
        [
            "I can separate light reactions from the Calvin cycle by location and products.",
            "I can state that photosynthetic O₂ comes from water.",
            "I can explain limiting factors and why C4/CAM exist.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Fitness and energy strategies",
        [
            "Fitness means leaving more successful offspring, not ‘being in shape.’ Energy strategies are traits that help an organism get enough ATP and carbon in its real habitat.",
            "Fermentation yields only 2 ATP per glucose but is fast and oxygen-independent. Sprinting muscle and yeast in crushed grapes use it. Respiration yields far more ATP when O₂ and mitochondria are available.",
            "Organisms also choose fuels: glycogen for quick cytosolic ATP, fat for dense long-term stores, uncoupling in brown fat for heat. Each choice has a cost.",
            "Plants choose carbon-concentrating pathways where photorespiration would be expensive. Animals choose endothermy or ectothermy with different food bills. Bacteria choose electron acceptors that exist in their mud.",
            "Regulation is part of strategy. PFK sensing ATP/AMP, insulin moving GLUT4, stomata opening at night in CAM — these are switches that match supply to demand.",
            "When an FRQ asks ‘justify the advantage,’ name the habitat constraint (oxygen, water, cold, food scarcity) and the ATP or water number that constraint changes. Vague ‘it is better’ does not earn the point.",
        ],
        "Unit 7 (selection) and Unit 8 (ecology) will reuse these tradeoffs. Energetics is where the numbers live.",
        "Always pair a strategy with a limitation: ‘more ATP but needs O₂’; ‘saves water but costs ATP’; ‘fast ATP but low yield.’",
        lesson_figure(
            _atp_yield_svg(),
            "Three fates of glucose energy",
            "Fermentation: 2 ATP, fast, no O₂. Aerobic respiration: ~30 ATP when the proton gradient drives ATP synthase. Uncoupling: the same gradient leaks as heat instead of ATP.",
        )
        + solved(13, "Why might a yeast in a high-sugar, low-oxygen vat ferment even though respiration ‘makes more ATP’?",
                 ["Oxygen may be scarce, so the ETC cannot run.",
                  "Fermentation regenerates NAD⁺ and produces ATP (2 per glucose) fast.",
                  "In that habitat, 2 ATP with NAD⁺ recycle beats 0 ATP from a stalled respiration plan."],
                 "O₂ is limiting; fermentation keeps glycolysis’s 2 ATP flowing", "", "Easy")
        + solved(14, "Brown-fat uncoupling proteins waste the proton gradient as heat. When is that adaptive?",
                 ["In a newborn or hibernator, heat can matter more than ATP efficiency.",
                  "The same leak in sprinting skeletal muscle would steal ATP from contraction.",
                  "Fitness is tissue- and context-specific, not a universal ‘never waste gradient.’"],
                 "when heat has higher fitness value than extra ATP", "", "Medium")
        + solved(15, "CAM vs C3 in a desert: name the water-saving mechanism and the energetic tax.",
                 ["CAM opens stomata at night, stores carbon as acid, and closes stomata by day.",
                  "Less daytime water loss.",
                  "The tax is extra ATP to run the concentrating shuttle, and a slower carbon supply to Rubisco.",
                  "In a wet cool forest, C3 without the tax often wins."],
                 "night stomata / day closed; extra ATP cost", "", "Hard"),
        ("Treating ‘more ATP’ as always fitter",
         "A pathway that needs oxygen is useless in anaerobic mud. A C4 pump is wasteful in a cool wet climate. Selection sees net offspring, not a textbook ATP table."),
        ("Write the tradeoff in six words",
         "‘More ATP / needs oxygen.’ ‘Saves water / costs ATP.’ If you cannot finish that sentence, you do not yet have the AP answer."),
        [
            "I can define fitness in reproductive terms and apply it to metabolism.",
            "I can contrast fermentation vs respiration as habitat strategies.",
            "I can explain C4/CAM and uncoupling as tradeoffs, not decorations.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Coupled reactions and ATP",
        [
            "An endergonic reaction ($ΔG>0$) will not run net forward on its own. An exergonic reaction ($ΔG<0$) can. Cells couple them so the sum of $ΔG$ values is negative.",
            "ATP is the usual coupling coin. Hydrolysis of ATP to ADP + Pᵢ (or transfer of the phosphate to a substrate) is strongly exergonic, especially in a living cell that keeps [ATP] high relative to ADP.",
            "Mechanistically, coupling is often not ‘two reactions that happen to be nearby.’ A phosphate is glued onto a molecule, making a high-energy intermediate that can then form the desired bond (glutamine synthesis is a classic example).",
            "ATP is regenerated by substrate-level phosphorylation (a phosphate handed off from a metabolite) or by chemiosmotic ATP synthase. You already met both in respiration and photosynthesis.",
            "Energy charge regulation: high ATP inhibits PFK and other catabolic enzymes; high AMP activates them. The battery’s state is a signal as well as a fuel.",
            "When you see $ΔG^{\\circ}$ tables on an exam, add the values for the coupled pair. If the sum is negative, the pair can proceed. If not, the cell needs another ATP or a different pathway.",
        ],
        "Active transport, biosynthesis, and mechanical work are all coupling problems. Unit 2’s pumps are this idea in a membrane.",
        "Write $ΔG_{uphill}+ΔG_{ATP}$ and look at the sign. Then name the intermediate (phosphorylated substrate) if the question asks how, not just whether.",
        lesson_figure(
            energy_diagram_svg(label="coupled: hill paid by ATP"),
            "An uphill reaction can proceed when paired with ATP hydrolysis",
            "The enzyme binds both processes so the net free-energy change is downhill.",
        )
        + solved(16, "A biosynthetic step has $ΔG=+3.4$ kcal/mol. ATP hydrolysis is $-7.3$ kcal/mol. Can a 1:1 coupling work?",
                 ["Net $ΔG=+3.4-7.3=-3.9$ kcal/mol.",
                  "The sum is negative, so the coupled pair can proceed as written.",
                  "The enzyme must actually link the steps (shared intermediate), not merely coexist in the cell."],
                 "yes; net about −3.9 kcal/mol", "", "Easy")
        + solved(17, "Why is ATP a better immediate donor than glucose for a single pump cycle?",
                 ["Glucose oxidation is a long pathway with many enzymes.",
                  "ATP hydrolysis is a single, controllable, highly exergonic step that a pump can couple directly.",
                  "Glucose is the warehouse; ATP is the coin in the pocket."],
                 "ATP is a ready, one-step energy coin; glucose is a stored fuel", "", "Medium")
        + solved(18, "PFK is inhibited by ATP even though ATP is also a substrate of PFK. How can both be true?",
                 ["The catalytic site binds ATP as a phosphate donor (needed for the reaction).",
                  "A separate allosteric site binds ATP when concentration is high and shuts the enzyme down.",
                  "Low vs high ATP therefore means ‘use me’ vs ‘we have enough’ — two sites, two meanings."],
                 "substrate site vs allosteric inhibitory site", "", "Hard"),
        ("Adding ΔG values that are not actually coupled",
         "Thermodynamics only helps if an enzyme creates a shared path. Two reactions in different organelles do not couple just because their ΔG numbers look convenient on a worksheet."),
        ("Always state net ΔG with a sign",
         "Graders look for the arithmetic and the word ‘exergonic’ or ‘endergonic’ for the pair. Then add the biological meaning (pump ran, glutamine was made)."),
        [
            "I can add ΔG values to test whether coupling can work.",
            "I can describe ATP as a phosphorylated energy coin regenerated by chemiosmosis or substrate-level phosphorylation.",
            "I can explain energy-charge regulation of PFK.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Enzyme catalysis, active sites, and inhibitors",
            "Temperature, pH, $K_m$/$V_{max}$, and feedback control",
            "Glycolysis, Krebs, ETC, and fermentation",
            "Light reactions, Calvin cycle, and carbon-concentrating strategies",
            "Fitness tradeoffs in energy metabolism",
            "ATP coupling and energy charge",
        ],
        body,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Cell Communication and Cell Cycle
# ===========================================================================

def _u4_questions():
    return _qs([
        ("A ligand is a signaling molecule. It causes a response only in cells that:",
         "have a matching receptor",
         "Reception is shape-specific binding. A hormone in the blood bathes many cells; only those with the receptor transduce the signal. That is why insulin does not order every cell to do the same thing.",
         ["lack membranes", "have no proteins", "are prokaryotes without DNA"]),
        ("A steroid hormone is nonpolar, so it usually:",
         "crosses the membrane and binds an intracellular receptor that can alter transcription",
         "Lipid-soluble messengers skip membrane receptors. Peptide hormones cannot cross and must bind extracellular domains, then use second messengers.",
         ["always binds a G protein on the outer face and never enters", "is a carbohydrate wall component", "pumps Na⁺ as its only function"]),
        ("Transduction often amplifies a signal because:",
         "each enzyme in a cascade activates many molecules of the next enzyme",
         "One receptor can activate many G proteins; each adenylyl cyclase makes many cAMP; each kinase phosphorylates many targets. A few ligands can change a cell’s chemistry in seconds.",
         ["one ligand is consumed to make one ATP only", "receptors destroy all second messengers instantly with no cascade", "amplification means the ligand becomes DNA"]),
        ("A phosphorylation cascade is a series of:",
         "kinases activating other kinases by adding phosphate groups",
         "Kinases put phosphates on; phosphatases take them off. The phosphate is a reversible switch that changes protein shape. That is why signal duration depends on both adding and removing phosphates.",
         ["ribosomes translating the ligand", "lipids becoming amino acids", "DNA ligase joining Okazaki fragments"]),
        ("cAMP is a second messenger. It is made from ATP by adenylyl cyclase after a G-protein-coupled receptor is activated. Second messengers exist because:",
         "the first messenger (ligand) often cannot enter, so an inside signal must be generated",
         "cAMP, Ca²⁺, IP₃, and DAG carry the message in the cytosol. They also allow amplification and branching to several targets.",
         ["the ligand is always DNA", "second messengers are chromosomes", "G proteins transcribe mRNA directly"]),
        ("Negative feedback returns a system toward a set point. Positive feedback:",
         "amplifies a change until a climax event stops it",
         "Body temperature uses negative feedback (sweat/shiver). Childbirth oxytocin is positive: stretch → more oxytocin → more contraction → more stretch, until delivery ends the loop.",
         ["always lowers the stimulus in every known pathway", "is the same as a competitive inhibitor on Rubisco", "cannot occur in cells"]),
        ("Insulin lowers blood glucose; glucagon raises it. Together they are:",
         "antagonistic hormones using negative feedback on blood sugar",
         "High glucose → insulin → uptake/storage → glucose falls toward set point. Low glucose → glucagon → glycogen breakdown. Homeostasis is a pair of opposing loops, not one hormone.",
         ["positive feedback that never stops", "steroid receptors inside mitochondria only", "cell-cycle cyclins"]),
        ("Quorum sensing in bacteria is communication that:",
         "triggers group behaviors when signal concentration shows the population is dense",
         "Each cell releases an autoinducer. High density means high signal, and genes for biofilm or light turn on. It is ligand/receptor logic at community scale.",
         ["mitosis in the nucleus of bacteria", "photosystem II activation", "Hardy–Weinberg equilibrium"]),
        ("Apoptosis is programmed cell death. It is useful because:",
         "damaged or extra cells can be removed without spilling lytic enzymes into neighbors",
         "Webbing between embryonic fingers is removed by apoptosis. Virus-infected cells can self-destruct. Caspases are the protease cascade. Cancer often breaks this pathway.",
         ["it is the same as necrosis from a crushed limb in every case", "it creates extra fingers", "it is mitosis running backward to make DNA"]),
        ("A phosphatase that never turns off would tend to:",
         "shut signaling down even when the ligand is still bound, by stripping phosphates from the cascade",
         "Response size is a balance of kinases vs phosphatases (and of cAMP vs phosphodiesterase). Diseases can hit either side.",
         ["lock every kinase in the ‘on’ state forever", "synthesize new receptors from cellulose", "convert cAMP into glucose"]),
        ("Mitosis produces:",
         "two daughter nuclei with the same chromosome number as the parent nucleus",
         "It is nuclear division for growth, repair, and asexual reproduction. Cytokinesis splits the cytoplasm. DNA was already duplicated in S phase, so each daughter gets one copy of each chromatid pair.",
         ["four haploid gametes in animals as its only product", "a single haploid nucleus", "crossing over between non-sister chromatids as a required step"]),
        ("Chromosomes line up at the spindle equator during:",
         "metaphase",
         "Prophase: condense and spindle forms. Metaphase: line up. Anaphase: sister chromatids separate. Telophase: nuclei reform. AP expects the order and what the spindle microtubules are attached to (kinetochores).",
         ["G1", "cytokinesis only in plants", "S phase"]),
        ("Sister chromatids are:",
         "identical copies joined at a centromere after DNA replication",
         "They separate in mitosis (and in meiosis II). Homologous chromosomes are the maternal and paternal versions of the ‘same’ chromosome and pair in meiosis I — not in mitosis.",
         ["the X and Y chromosomes only", "two unrelated chromosomes from different species", "ribosomes"]),
        ("A cell with 2n=6 chromosomes after S phase has how many chromatids at metaphase of mitosis?",
         "12",
         "Six chromosomes were duplicated: 6 chromosomes × 2 chromatids = 12 chromatids, still counted as 6 chromosomes until sisters separate. Then 12 chromosomes move apart, 6 to each pole.",
         ["3", "6", "24"]),
        ("Plant cytokinesis differs from animal cytokinesis because plants:",
         "build a cell plate (new wall) instead of a cleavage furrow",
         "Vesicles from the Golgi lay down a new cell wall in the middle. Animals pinch an actin-myosin ring. Both follow mitosis; the mechanics match the presence or absence of a wall.",
         ["never divide", "use binary fission without chromosomes", "separate homologs in mitosis"]),
        ("The G1 checkpoint asks, roughly:",
         "is the cell large enough, with intact DNA and growth-factor permission, to enter S?",
         "Passing G1/S commits the cell to DNA replication. G2/M checks replication completeness. The metaphase checkpoint checks kinetochore attachment. Cancer is checkpoint failure.",
         ["whether fermentation has made 32 ATP", "whether Rubisco is present", "whether the cell is a prokaryote with a nucleus"]),
        ("Cyclins rise and fall; cyclin-dependent kinases (CDKs) are present more steadily. The pair works because:",
         "cyclin must bind CDK to activate it, so oscillating cyclin times the kinase",
         "MPF (mitosis-promoting factor) is cyclin + CDK. When cyclin is destroyed, MPF dies and the cell exits mitosis. That is a molecular clock, not a slogan.",
         ["cyclins are DNA; CDKs are lipids", "CDKs transcribe cyclin genes by being ribosomes", "checkpoints are only in bacteria"]),
        ("Growth factors are external signals that:",
         "bind receptors and can push a cell past G1 toward division",
         "Density-dependent inhibition and anchorage dependence are other social controls. Tumor cells often ignore them. This links signaling (concept 1) to the cell cycle.",
         ["are organelles that digest cyclins in the nucleus as their only job", "replace the need for DNA replication", "are the spindle fibers"]),
        ("p53 is a tumor-suppressor protein that can halt the cycle or trigger apoptosis after DNA damage. Loss of both p53 copies:",
         "lets damaged cells keep dividing, raising cancer risk",
         "Tumor suppressors are brakes (need both copies lost — two-hit). Proto-oncogenes are accelerators (one hyperactive copy can drive). AP loves that contrast.",
         ["instantly converts the cell into a gamete", "raises DNA repair to 100% forever", "is required for photosynthesis"]),
        ("A cell that stays in G0:",
         "has left the division cycle (examples: many neurons) unless signaled back",
         "Not every cell cycles constantly. Differentiation often means G0. Stem cells remain able to re-enter. This is regulation, not a failed mitosis.",
         ["is stuck in anaphase forever", "has no DNA", "must be a prokaryote"]),
        ("Meiosis produces haploid cells so that:",
         "fertilization can restore diploidy without doubling chromosome number each generation",
         "Without meiosis, chromosome number would explode. Meiosis I separates homologs (reductive). Meiosis II separates sisters, looking mitosis-like.",
         ["mitosis can be skipped in embryos", "DNA replication is unnecessary in gametes", "haploid cells have twice the DNA of diploid cells"]),
        ("Crossing over happens in prophase I between:",
         "non-sister chromatids of homologous chromosomes",
         "Chiasmata lock homologs together and swap DNA, creating recombinant chromatids. That is a source of variation plus a mechanical need for proper segregation.",
         ["sister chromatids of the same chromosome only, which cannot create new allele combinations", "two nonhomologous chromosomes as the standard process", "ribosomes"]),
        ("Independent assortment means:",
         "each homolog pair orients independently at metaphase I, so gametes get mixed maternal/paternal chromosomes",
         "For n pairs, $2^n$ chromosome combinations (ignoring crossing over). Humans: $2^{23}$ — already huge — then crossing over multiplies diversity more.",
         ["all maternal chromosomes always go to the same pole", "DNA does not replicate before meiosis I", "mitosis uses independent assortment of homologs"]),
        ("A diploid cell with 2n=8 enters meiosis. At the end of meiosis I each daughter has:",
         "4 chromosomes, each still made of 2 chromatids (haploid, replicated)",
         "Homologs have separated, so the number is n=4, but sisters are still attached until meiosis II. This ‘haploid but duplicated’ state is a classic AP checkpoint.",
         ["8 chromosomes unreplicated", "2 chromosomes", "16 chromatids as 16 separate haploid chromosomes already"]),
        ("Mitosis vs meiosis: a true distinction is:",
         "mitosis keeps 2n→2n with identical sisters splitting; meiosis I is 2n→n with homologs splitting",
         "Both can have spindles and a metaphase. The pairing of homologs (synapsis) is meiosis-specific. Mixing those events is the usual error.",
         ["meiosis has no cytokinesis", "mitosis always makes gametes in animals", "meiosis II reduces ploidy from 2n to n"]),
        ("Nondisjunction is failure of chromosomes to separate. In meiosis I it means:",
         "a pair of homologs went to the same pole",
         "Result: two n+1 and two n−1 gametes if it is one pair. In meiosis II, sisters fail, producing two normal, one n+1, one n−1 among the four. Trisomy 21 is usually from maternal meiosis errors.",
         ["DNA failing to unwind in transcription", "crossing over happening too perfectly", "cytokinesis building two walls in plants only"]),
        ("A karyotype showing three chromosome 21s is:",
         "trisomy 21 (Down syndrome), an aneuploidy",
         "Aneuploidy = wrong number of a particular chromosome. Polyploidy = extra whole sets (common in plants). Those words are not interchangeable.",
         ["haploidy", "a translocation-free euploid 2n=46", "polyploidy with 69 complete sets"]),
        ("Why does nondisjunction create variation that is often harmful, yet meiosis still includes risky pairing?",
         "the same pairing/crossing-over machinery that can fail is also what generates diversity and holds homologs for segregation",
         "Biology is a tradeoff: recombination and reduction division are worth the error rate. Selection cannot invent a perfect chromosome dance.",
         ["nondisjunction is the goal of meiosis", "mitosis is riskier for chromosome number in gametes", "karyotypes cannot detect extra chromosomes"]),
        ("A human gamete should have:",
         "23 chromosomes (n), one of each homolog pair",
         "22 autosomes + one sex chromosome. Fertilization: 23+23=46. If a gamete has 24, the zygote is aneuploid (47).",
         ["46 sister chromatids as 46 homolog pairs", "92 chromosomes after S phase of the gamete", "0 chromosomes because DNA is in mitochondria"]),
        ("Sexual reproduction’s variation sources include mutation, crossing over, independent assortment, and:",
         "random fertilization",
         "Two gametes, each already unique, combine. Asexual clones skip these shuffles (except mutation). AP Unit 4/5 will reuse this list.",
         ["binary fission of mitochondria as the main nuclear-diversity engine", "DNA replication errors that always make extra whole genomes on purpose", "photosynthesis"]),
        ("Epinephrine on a liver cell uses a GPCR → G protein → adenylyl cyclase → cAMP → kinase cascade → glycogen breakdown. Cutting the pathway at cAMP phosphodiesterase (which destroys cAMP) would:",
         "weaken the glucose-release response",
         "Phosphodiesterase is the off switch for cAMP. More of it, shorter signal. Caffeine inhibits some phosphodiesterases — the opposite direction.",
         ["increase cAMP and lock the response on", "convert the receptor into a steroid receptor", "start mitosis immediately"]),
        ("A receptor tyrosine kinase (RTK) dimerizes and phosphorylates itself. The phosphate docks relay proteins. This is still:",
         "signal transduction at the membrane, often leading to a transcription or growth response",
         "Growth-factor receptors are often RTKs. Oncogenic mutations can make them fire without ligand — Unit 4 meeting cancer.",
         ["meiosis I pairing", "a Calvin-cycle enzyme", "simple diffusion of the ligand through DNA"]),
        ("Positive feedback in the action potential (Na⁺ channels opening cause depolarization that opens more Na⁺ channels) ends when:",
         "channels inactivate and K⁺ exits, restoring polarity — the climax has a built-in stop",
         "Positive feedback is not ‘uncontrolled forever.’ It runs to a defined event, then other machinery terminates it. Same logic as oxytocin and birth.",
         ["Na⁺ channels stay open for the rest of the organism’s life", "the membrane dissolves", "ATP synthase reverses in the axon"]),
        ("Why can the same ligand (epinephrine) dilate some vessels and constrict others?",
         "different target cells express different receptors or different transduction wiring",
         "The ligand is not the message by itself. Receptor isoform + cascade + available enzymes decide the response. Structure (which receptor) → function (which output).",
         ["epinephrine is a different molecule in each tissue", "blood cells lack proteins", "ligands only work in plants"]),
        ("Colchicine blocks microtubule polymerization. Mitosis stalls at:",
         "metaphase, because kinetochores never get a proper spindle attachment",
         "The spindle-assembly checkpoint holds anaphase until every chromosome is attached. No microtubules, no satisfaction of that checkpoint. Used in karyotyping to accumulate metaphases.",
         ["G0 because DNA cannot be copied without microtubules", "S phase", "cytokinesis in bacteria only"]),
        ("If sister chromatids failed to separate in mitosis, a daughter cell could receive:",
         "both sisters of some chromosomes and none of others (aneuploid daughters)",
         "Mitotic nondisjunction is a cancer/genome-instability issue, not only a meiosis story. The mechanism is the same word; the products are diploid-lineage cells, not gametes.",
         ["a guaranteed perfect 2n clone", "four haploid cells", "no nucleus in either daughter by definition"]),
        ("MPF activity peaks at the start of mitosis then crashes because:",
         "cyclin is degraded, so CDK loses its partner",
         "The crash lets the cell exit mitosis. If cyclin cannot be destroyed, the cell may be trapped in a mitotic state. Proteolysis is a regulatory tool, not just garbage collection.",
         ["DNA is degraded", "the nuclear envelope becomes cellulose", "ATP is converted into cyclin"]),
        ("A proto-oncogene vs a tumor-suppressor gene: which statement is accurate?",
         "a gain-of-function in one proto-oncogene allele can drive division; tumor suppressors usually need both alleles lost",
         "Accelerator vs brake. ras is a classic proto-oncogene (GTPase stuck on). rb and p53 are brakes. Chemotherapy logic starts here.",
         ["tumor suppressors cause cancer when they become more active", "proto-oncogenes are only in prokaryotes", "both classes are carbohydrates"]),
        ("Independent assortment of one human with 2n=46, no crossing over, yields how many chromosome-combination gametes?",
         "$2^{23}$",
         "23 homolog pairs, two orientations each, independent. Crossing over and fertilization multiply further. Write $2^n$ with n = haploid pair count.",
         ["23", "46", "2"]),
        ("Synapsis is:",
         "pairing of homologs along their length in prophase I",
         "The synaptonemal complex holds them for crossing over. Mitosis does not do this. If synapsis fails, homologs mis-segregate (another nondisjunction route).",
         ["fusion of two sperm", "DNA replication in G0", "cytokinesis in animals only"]),
        ("A 2n=4 organism: after meiosis II, each gamete DNA amount relative to a G1 diploid cell is:",
         "half the DNA and half the chromosome number",
         "G1 diploid has 4 chromosomes, 4 chromatids worth of DNA. Gamete has 2 chromosomes, unreplicated. Both n and C are halved versus G1 diploid.",
         ["the same DNA amount as G1 diploid", "twice the DNA of G1 diploid", "zero DNA"]),
        ("Why is anaphase I not the same as mitotic anaphase?",
         "homologs (each still two chromatids) separate in anaphase I; sisters separate in mitosis",
         "Look at the centromeres: in anaphase I, sisters remain attached. That visual is the highest-yield meiosis drawing skill on AP.",
         ["there is no spindle in meiosis I", "DNA unreplicates during anaphase I", "plant cells skip anaphase I"]),
        ("Aneuploidy of sex chromosomes is often milder than of autosomes because:",
         "Y has few genes, and extra X chromosomes can be inactivated (Barr bodies)",
         "XXX, XXY, XO are seen in live births more than most autosome trisomies. That is dosage compensation meeting nondisjunction, not ‘sex chromosomes do not matter.’",
         ["sex chromosomes never undergo nondisjunction", "autosomes have no genes", "Barr bodies add extra autosomes"]),
        ("A signal that never gets terminated (broken GTPase on a G protein, like some oncogenic ras) causes:",
         "constitutive transduction as if ligand were always present",
         "Off switches matter as much as on switches. Phosphodiesterase, phosphatases, GTP hydrolysis, receptor endocytosis — list them on FRQs when asked how a signal stops.",
         ["immediate apoptosis of all neighboring cells only", "a permanent G0 with no transcription", "conversion of the cell into a chloroplast"]),
        ("Density-dependent inhibition fails in a culture of cancer cells. They:",
         "keep dividing after a monolayer is confluent, piling up",
         "Normal cells stop when they touch (cadherin/contact signaling into the cycle). The observation is old; the mechanism is signaling into checkpoints.",
         ["immediately become haploid", "lose all cyclins and die in G1 necessarily", "start meiosis"]),
        ("A researcher measures DNA per cell: G1 = 10 pg, G2 = 20 pg. A cell with 15 pg is most likely in:",
         "S phase (replication incomplete)",
         "S is the only time DNA amount is intermediate. Mitotic cells are at 20 pg until cytokinesis. This is a data-table staple.",
         ["G0 with extra chromosomes from meiosis", "anaphase of meiosis II in a gamete with 15 chromosomes of 1 pg each without replication context", "G1"]),
        ("AP Stretch: A drug blocks the metaphase checkpoint by faking ‘all kinetochores attached.’ The danger is:",
         "anaphase begins with unattached chromosomes, producing aneuploid daughters",
         "Checkpoints exist because attachment is stochastic. Overriding them is how some chemotherapies also kill — but the AP point is the causal chain to aneuploidy.",
         ["the cell cannot enter G1 ever again because DNA cannot unwind", "crossing over increases to 100% of chromatids in mitosis", "chloroplasts fail to divide"]),
        ("AP Stretch: Two ligands use different receptors on the same cell but share the cAMP pool. This cross-talk means:",
         "the response is not a private wire; pathways can add, subtract, or occlude each other",
         "AP wants systems thinking: a cell is not one cartoon cascade. Shared second messengers are a feature (integration) and a bug (side effects of drugs).",
         ["receptors cannot exist on one cell in pairs", "cAMP is a steroid that enters the nucleus as DNA", "shared pools prove the ligands are identical molecules"]),
        ("AP Stretch: In meiosis I, cohesin is cleaved on chromosome arms but protected at centromeres (shugoshin). If shugoshin fails, the likely result is:",
         "sisters separate in meiosis I, wrecking reductional division",
         "The molecular difference between anaphase I and II is where cohesin still holds. This is the modern mechanism under the old ‘homologs vs sisters’ vocabulary.",
         ["DNA replication repeats in metaphase I", "mitosis gains synapsis", "gametes become tetraploid automatically"]),
        ("AP Stretch: A heterozygous inversion loop in prophase I can produce recombinant chromatids with duplications and deletions. That is why:",
         "crossovers inside inversions often yield inviable gametes, suppressing recovered recombinants",
         "Structure (inverted sequence) changes the function of crossing over. Variation is not always free. Chromosomal mutations meet meiosis here.",
         ["inversions always increase fertility", "crossing over cannot occur on inverted homologs in any configuration", "inversions convert meiosis into mitosis"]),
        ("AP Stretch: MPF activates APC/C, which leads to cyclin destruction, which inactivates MPF. This is:",
         "negative feedback that makes mitosis a pulse, not a permanent state",
         "A kinase turning on its own off-switch is how you get a one-way ratchet through the cycle. Positive feedback also exists (MPF activating more MPF). The exam may ask you to label the loop type from a diagram.",
         ["positive feedback that never ends mitosis", "a G-protein-coupled receptor on cyclin", "independent assortment of cyclins"]),
        ("AP Stretch: A neuron in G0 still transduces neurotransmitter signals for decades without dividing. This shows:",
         "cell communication is not the same process as the cell cycle, even though some signals (growth factors) can link them",
         "Unit 4 is two stories that share receptors: everyday signaling vs division control. Do not force every ligand into mitosis.",
         ["G0 cells cannot have receptors", "neurotransmitters are cyclins", "neurons must enter S phase to release neurotransmitter"]),
        ("AP Stretch: Compare binary fission in a bacterium with mitosis. The deepest shared need is:",
         "replicated genomes must be segregated before the cell splits, even if a spindle of microtubules is not used",
         "Prokaryotes use a different apparatus (Par proteins, membrane growth) but the information problem is the same. Eukaryotic mitosis is a solution for multiple linear chromosomes.",
         ["both require a nucleus", "both require crossing over of homologs", "bacteria pair 23 homologs"]),
        ("AP Stretch: An individual is 47,XXY. Nondisjunction could have occurred in:",
         "paternal meiosis I (XY fail to separate) or maternal meiosis (extra X in the egg), among other routes",
         "You must track sex chromosomes as homologs that sometimes pair (XY in male meiosis I). Multiple parental origins are possible; a pedigree or marker would distinguish them.",
         ["only mitosis in the zygote that always yields four gametes", "photorespiration", "S phase skipping in the father only with no meiosis"]),
        ("AP Stretch: If every kinetochore is attached and under tension, the spindle checkpoint releases separase. Separase cleaves cohesin. The AP-level claim is:",
         "mechanical tension is transduced into a chemical decision to start anaphase",
         "This is signal transduction inside the cycle: a physical state (tension) becomes a protease cascade. Unit 4’s two halves fuse in that sentence.",
         ["tension is irrelevant; anaphase is timed only by cyclin transcription in G1", "separase copies DNA", "cohesin is a ligand from a neighboring cell"]),
    ])


def build_unit4():
    title = "AP Biology Unit 4: Cell Communication and Cell Cycle"
    description = (
        "Reception, transduction, and response; feedback; mitosis; checkpoints; meiosis; "
        "and how nondisjunction creates aneuploidy — with cascade and chromosome diagrams."
    )

    c1 = concept_block(
        "1. Signal transduction",
        [
            "Cells talk with chemical messages called ligands. A target cell can respond only if it has a receptor whose shape and chemistry fit that ligand. No receptor, no message — even if the ligand is in the blood at high concentration.",
            "Reception is binding. Transduction is the inside relay that converts binding into chemistry (often phosphorylation cascades and second messengers). Response is what actually changes: enzyme activity, ion flow, or gene transcription.",
            "Hydrophilic ligands (peptides, epinephrine) cannot cross the bilayer, so their receptors sit in the membrane: G-protein-coupled receptors (GPCRs), receptor tyrosine kinases (RTKs), and ion-channel receptors. Hydrophobic ligands (steroids, thyroid hormone) slip inside and often bind transcription factors.",
            "Amplification is why a tiny amount of hormone can matter. One receptor activates many G proteins; each cyclase makes many cAMP; each kinase phosphorylates many substrates. Cascades multiply.",
            "Second messengers (cAMP, Ca²⁺, IP₃, DAG) are small intracellular molecules generated after reception. They spread the message through the cytoplasm faster than a giant protein could, and they let one receptor talk to many kinds of target.",
            "Every ‘on’ switch needs an ‘off’ switch: GTP hydrolysis on G proteins, phosphodiesterases that chew cAMP, phosphatases that remove phosphates, receptor endocytosis. Diseases and drugs often hit the off switch.",
        ],
        "The cell cycle, insulin control of glucose, and many cancers are transduction stories. Unit 6’s gene regulation is a common endpoint of these pathways.",
        "Label any pathway with three words — reception, transduction, response — then ask whether the ligand was membrane-impermeant. That decides receptor location.",
        lesson_figure(
            _cascade_svg(),
            "Ligand → receptor → relay → response",
            "The ligand never has to become the response. Shape matching at R starts a cascade that can amplify.",
        )
        + solved(1, "Insulin is a peptide. Where is its receptor, and why can insulin not use a steroid-style intracellular receptor?",
                 ["Peptides are hydrophilic and large; they do not cross the plasma membrane.",
                  "The receptor must have an extracellular binding domain.",
                  "Binding then transduces (phosphorylation, vesicle movement of GLUT4) without insulin entering as a transcription factor."],
                 "membrane receptor; insulin cannot cross the bilayer", "", "Easy")
        + solved(2, "Why does a phosphorylation cascade amplify more than a 1:1 ligand–receptor binding event alone?",
                 ["Each kinase, once on, can modify many molecules of the next protein.",
                  "Those stay modified until phosphatases reverse them, so one receptor’s activity is multiplied in time and number.",
                  "The ligand itself is not used up as a stoichiometric fuel for every downstream molecule."],
                 "each catalytic step activates many targets", "", "Medium")
        + solved(3, "A mutant G protein cannot hydrolyze GTP. Predict the signaling phenotype.",
                 ["G proteins are on while GTP-bound and off after hydrolysis to GDP.",
                  "Stuck-GTP means the G protein keeps activating its effector (for example adenylyl cyclase).",
                  "The pathway behaves as if ligand were constantly present — a classic oncogenic pattern (ras is a related GTPase story)."],
                 "constitutive (always-on) transduction", "", "Hard"),
        ("Assuming every hormone enters the nucleus",
         "Only lipid-soluble messengers commonly do. Peptide and most amine hormones are extracellular ligands. Mixing those classes scrambles receptor location and the entire cascade."),
        ("Write R → T → R on the FRQ margin",
         "Reception, transduction, response. Then fill each arrow with a molecule (ligand, cAMP, kinase, transcription factor). Empty arrows lose points."),
        [
            "I can locate receptors for hydrophilic vs hydrophobic ligands.",
            "I can explain amplification by cascades and second messengers.",
            "I can name ways a signal is turned off.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Feedback and cell response",
        [
            "A response is whatever the pathway changes: glycogen breakdown, opening an ion channel, moving a transcription factor into the nucleus, or triggering apoptosis (programmed cell death).",
            "Negative feedback counters a change and restores a set point. If body temperature rises, you sweat; if it falls, you shiver. The product of the pathway reduces the original stimulus.",
            "Positive feedback reinforces a change until a defined event stops the loop. Oxytocin in labor, platelet plugging, and the Na⁺ influx of an action potential are examples. It is not ‘homeostasis forever’; it is a one-way push to a climax.",
            "The same ligand can cause different responses in different cells because receptors and available enzymes differ. Epinephrine on liver vs vascular smooth muscle is the textbook split.",
            "Quorum sensing shows that unicellular organisms also communicate: autoinducer concentration reports crowd size, then group behaviors (biofilm, virulence, glow) switch on.",
            "Apoptosis is a tidy death program (caspases) used in development and in destroying infected or damaged cells. When apoptosis fails, tumors keep cells they should have discarded.",
        ],
        "Homeostasis FRQs and cancer FRQs both ask you to name the loop type and the consequence of breaking it.",
        "Decide negative vs positive first: does the output shut the input down, or does it make more of the same until a stop event?",
        lesson_figure(
            _feedback_svg(),
            "A negative-feedback loop",
            "The response reduces the stimulus (red return arrow). Homeostasis lives in that return.",
        )
        + solved(4, "Blood glucose rises after a meal. Name the hormone, the direction of the feedback, and the set-point idea.",
                 ["Insulin is released.",
                  "Glucose uptake and storage lower blood glucose toward the normal range.",
                  "That is negative feedback on the stimulus (high glucose)."],
                 "insulin; negative feedback toward a glucose set point", "", "Easy")
        + solved(5, "Why is childbirth oxytocin classified as positive feedback, and what stops it?",
                 ["Uterine stretch causes oxytocin release, which causes stronger contraction, which causes more stretch.",
                  "The loop amplifies until the baby is delivered.",
                  "Delivery removes the stretch stimulus, so the loop loses its input."],
                 "amplifies to delivery; birth removes the stimulus", "", "Medium")
        + solved(6, "Two tissues see the same epinephrine concentration but respond differently. What must differ inside those cells?",
                 ["Receptor subtypes (α vs β adrenergic) and/or the transduction components present.",
                  "Available enzymes (glycogen phosphorylase vs a contractile apparatus) determine the output.",
                  "The ligand is not a universal command; the cell’s protein set is the interpreter."],
                 "different receptors or different downstream machinery", "", "Hard"),
        ("Calling all feedback ‘negative’ because biology likes balance",
         "Positive feedback is real and graded on the AP exam. Look for amplification to a climax (birth, clotting, action potential), then a separate stop condition."),
        ("Name the stimulus, the sensor, the output, and the effect on the stimulus",
         "If the output reduces the stimulus, negative. If it increases the stimulus, positive. This four-box sketch works for hormones and for molecular loops like MPF."),
        [
            "I can contrast negative and positive feedback with biological examples.",
            "I can explain why one ligand can cause two responses.",
            "I can describe apoptosis as a controlled response.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Mitosis",
        [
            "The cell cycle is G1 (grow), S (replicate DNA), G2 (prepare), and M (mitosis + cytokinesis). Mitosis divides the nucleus so each daughter gets a complete, identical set of chromosomes.",
            "After S phase, each chromosome consists of two sister chromatids joined at a centromere. They are replicas, not homologs. Homologs are the maternal and paternal copies and do not pair in mitosis.",
            "Prophase: chromosomes condense, spindle forms, nuclear envelope breaks down (in most animals). Metaphase: kinetochores attach and chromosomes line up. Anaphase: sisters separate. Telophase: nuclei reform.",
            "The spindle is made of microtubules. Motor proteins and shortening microtubules pull chromatids. If a kinetochore is unattached, the metaphase checkpoint delays anaphase.",
            "Cytokinesis splits cytoplasm: a cleavage furrow in animals, a cell plate in plants. Mitosis can occur without immediate cytokinesis (some multinucleate cells), which proves they are distinct steps.",
            "Mitosis makes more of the same cell type for growth, repair, and asexual reproduction. It is not how animals make haploid gametes — that is meiosis, two concepts from now.",
        ],
        "Cancer, karyotypes, and cloning arguments all assume you can stage mitosis and count chromatids vs chromosomes.",
        "At every stage, ask two counts: how many chromosomes, and how many chromatids? They are not the same after S phase.",
        lesson_figure(
            _mitosis_svg(),
            "Four named stages of mitosis",
            "Metaphase line-up, then anaphase splitting of sisters. Telophase rebuilds two nuclei.",
        )
        + solved(7, "A cell is 2n=4. After S phase, how many chromosomes and how many chromatids are present?",
                 ["Chromosome number is still 4 (each chromosome is a duplicated unit).",
                  "Each has 2 chromatids, so 8 chromatids.",
                  "Only when sisters separate in anaphase does the count of chromosomes become 8 briefly, then 4 per daughter."],
                 "4 chromosomes, 8 chromatids", "", "Easy")
        + solved(8, "What is the difference between sister chromatids and homologous chromosomes?",
                 ["Sisters are identical copies made in S phase, joined at a centromere.",
                  "Homologs are the two versions of a chromosome (maternal and paternal), which may carry different alleles.",
                  "Mitosis splits sisters. Meiosis I splits homologs."],
                 "sisters = copies; homologs = maternal/paternal pair", "", "Medium")
        + solved(9, "A poison freezes microtubules. Where does mitosis arrest, and why does a checkpoint cause that arrest?",
                 ["Kinetochores cannot attach to a working spindle.",
                  "The spindle-assembly checkpoint blocks anaphase-promoting signals until every chromosome is attached.",
                  "Cells accumulate in prometaphase/metaphase — the basis of some karyotype protocols and some chemotherapies."],
                 "metaphase arrest; unattached kinetochores block anaphase", "", "Hard"),
        ("Counting ‘chromosomes’ as chromatids after S phase",
         "A duplicated chromosome is still one chromosome with two chromatids. If you double-count, every later meiosis number will be wrong. Draw an X and call it one chromosome."),
        ("Narrate the movie in four verbs",
         "Condense, line up, split sisters, rebuild nuclei. If a choice adds ‘pair homologs’ to mitosis, it is describing meiosis."),
        [
            "I can order prophase, metaphase, anaphase, and telophase with the correct events.",
            "I can count chromosomes vs chromatids after S phase.",
            "I can contrast animal vs plant cytokinesis.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Cell cycle regulation",
        [
            "The cycle is not a free-running clock in healthy tissues. Checkpoints ask questions: Is DNA intact? Is the cell big enough? Are all kinetochores attached? Fail the question, and the cycle pauses or the cell dies.",
            "Cyclins are proteins whose amounts rise and fall. Cyclin-dependent kinases (CDKs) need cyclin partners to become active. Together they phosphorylate the targets that drive S phase or mitosis.",
            "MPF (mitosis-promoting factor) is G2 cyclin plus CDK. It triggers nuclear-envelope breakdown and spindle formation. Then cyclin is destroyed, MPF collapses, and the cell can exit mitosis. A pulse, not a siren that never stops.",
            "External signals matter. Growth factors are ligands that transduce into G1 cyclins. Contact inhibition and anchorage dependence are social rules: stop when crowded; divide only if attached to a surface. Cancer cells break those rules.",
            "Proto-oncogenes are normal accelerators (ras, growth-factor receptors). A gain-of-function mutation can turn one into an oncogene. Tumor-suppressor genes are brakes (p53, Rb). Usually both copies must fail. Two different math stories: one-hit vs two-hit.",
            "p53 can pause the cycle for repair or send the cell to apoptosis. Loss of p53 is common in tumors because damaged cells then keep dividing. This is Unit 4’s bridge from signaling to cancer.",
        ],
        "AP essays on cancer are checkpoint essays. If you only memorized stage names, you cannot explain why a mutation causes a tumor.",
        "Classify every cancer gene as accelerator (proto-oncogene) or brake (tumor suppressor), then say how many alleles must break.",
        lesson_figure(
            xy_graph(
                curves=[("#7c3aed", sample_curve(lambda t: 1 + 12 / (1 + math.exp(-1.2 * (t - 8))), 0, 16))],
                xlim=(0, 16), ylim=(0, 14), xlab="cycle time", ylab="MPF activity",
                points=[(10, 12.2, "mitosis")],
            ),
            "MPF activity rises as the cell enters mitosis",
            "Cyclin accumulation arms CDK. After mitosis, cyclin destruction crashes MPF so the cell can exit.",
        )
        + solved(10, "Why does destroying mitotic cyclin help a cell finish mitosis?",
                 ["MPF is cyclin+CDK; without cyclin the kinase goes quiet.",
                  "Exit from mitosis (reforming nuclei, undoing mitotic phosphorylation) requires MPF to fall.",
                  "If cyclin cannot be degraded, the cell can stick in a mitotic state."],
                 "MPF collapse lets the cell exit mitosis", "", "Easy")
        + solved(11, "Is ras a proto-oncogene or a tumor suppressor, and why can one mutant allele be enough?",
                 ["Normal ras is a GTPase switch in growth-factor pathways — an accelerator.",
                  "A mutation that blocks GTP hydrolysis leaves ras ‘on.’",
                  "That is a gain of function, so one allele can drive extra division (dominant at the cellular level)."],
                 "proto-oncogene; one hyperactive copy can drive", "", "Medium")
        + solved(12, "A cell has damaged DNA. Outline a p53-centered decision tree.",
                 ["Sensors activate p53.",
                  "p53 can induce CDK inhibitors (pause at a checkpoint) and DNA-repair genes.",
                  "If damage is severe, p53 promotes apoptosis so the mutation is not inherited by daughter cells.",
                  "No p53: the cell may replicate the damaged genome — cancer risk."],
                 "pause/repair or apoptosis; loss of p53 lets damaged cells divide", "", "Hard"),
        ("Treating oncogenes and tumor suppressors as synonyms",
         "One is a stuck accelerator; the other is a cut brake. The genetics differ (gain vs loss of function; one allele vs both). Mixing them loses the cancer FRQ."),
        ("Draw a checkpoint as a yes/no gate",
         "G1: growth factors and DNA OK? G2: replication complete? M: all kinetochores attached? Put the mutant protein on one gate."),
        [
            "I can explain cyclin–CDK timing, including MPF.",
            "I can contrast proto-oncogenes with tumor suppressors.",
            "I can connect growth-factor signaling to the G1 checkpoint.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Meiosis",
        [
            "Meiosis is a reduction division that makes haploid gametes (or spores). Fertilization then restores diploidy. Without meiosis, chromosome number would double every generation.",
            "DNA replicates once, then two divisions occur. Meiosis I separates homologous pairs (the diploid → haploid cut). Meiosis II separates sister chromatids, looking like a mitosis of haploid cells.",
            "In prophase I, homologs pair (synapsis) and non-sister chromatids exchange DNA (crossing over). That creates recombinant chromosomes and also helps hold homologs together for proper alignment.",
            "At metaphase I, each pair lines up independently of the other pairs (independent assortment). For $n$ pairs there are $2^n$ ways to assign maternal/paternal chromosomes to a pole, before you even count crossing over.",
            "Anaphase I: homologs move apart, but sisters stay attached. That is the picture you must be able to draw. Anaphase II: sisters finally split.",
            "Mitosis conserves identity; meiosis shuffles it. The three shuffles are crossing over, independent assortment, and (after meiosis) random fertilization. Mutation adds new alleles; meiosis deals the deck.",
        ],
        "Unit 5 genetics assumes you know when alleles segregate (anaphase I for homologs, anaphase II for sisters after a crossover).",
        "For any ‘what is in this cell?’ question, write 2n or n, and write replicated or unreplicated. Those two bits of data beat memorizing a table of names.",
        lesson_figure(
            _meiosis_svg(),
            "Crossing over between non-sister chromatids",
            "Homologs (blue vs red) swap segments. The products are recombinant chromatids, not identical sisters.",
        )
        + solved(13, "A cell is 2n=6. What is n, and how many chromosomes are in each product of meiosis?",
                 ["n = 3.",
                  "Meiosis starts with 6 chromosomes (3 pairs).",
                  "Each gamete should receive 3 chromosomes, one from each pair."],
                 "n=3; 3 chromosomes per gamete", "", "Easy")
        + solved(14, "At the end of meiosis I in that cell, are the products haploid, and are the chromosomes still duplicated?",
                 ["Homologs have separated, so each cell has 3 chromosomes → haploid.",
                  "Sisters are still attached, so each chromosome is still two chromatids.",
                  "Meiosis II exists to split those sisters."],
                 "haploid but still replicated (3 chromosomes, 6 chromatids)", "", "Medium")
        + solved(15, "Compute $2^n$ chromosome combinations from independent assortment for 2n=8, ignoring crossing over.",
                 ["n = 4 pairs.",
                  "$2^4=16$ different gamete chromosome combinations.",
                  "Crossing over would make many more unique chromatids than 16."],
                 "16 combinations from assortment alone", "", "Hard"),
        ("Drawing homologs separating in mitosis",
         "Mitosis never pairs homologs and never reduces ploidy. If your anaphase sketch shows two different-looking partners splitting as pairs, you drew meiosis I by mistake."),
        ("Stamp ‘I vs II’ on every meiosis question",
         "I = homologs, reduction, crossing over. II = sisters, mitosis-like. Most wrong choices simply swap I and II."),
        [
            "I can state why meiosis halves chromosome number.",
            "I can describe crossing over and independent assortment as variation sources.",
            "I can distinguish meiosis I from meiosis II using homologs vs sisters.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Nondisjunction and variation",
        [
            "Nondisjunction is a failure of chromosomes or chromatids to separate. If it happens in meiosis I, both homologs of a pair go to one cell. If it happens in meiosis II, both sisters of one chromosome go to one cell.",
            "The math of one meiosis-I failure for a single pair: two gametes with n+1 and two with n−1. For a meiosis-II failure: two normal, one n+1, one n−1. Fertilization with a normal gamete then yields trisomy or monosomy.",
            "Aneuploidy means the wrong number of a particular chromosome (trisomy 21, XO Turner syndrome). Polyploidy means extra whole sets (3n, 4n), common and often tolerated in plants, usually lethal in humans.",
            "A karyotype is a photograph of condensed chromosomes. It diagnoses aneuploidy and large rearrangements (deletions, inversions, translocations). It cannot see a single-base mutation — that is Unit 6 territory.",
            "Variation is not only errors. Mutation creates new alleles. Meiosis shuffles existing alleles. Fertilization combines two shuffles. Natural selection in Unit 7 then sorts that variation.",
            "Sex-chromosome aneuploidies are often milder because of Barr-body inactivation of extra X chromosomes and because the Y carries few genes. That is dosage compensation meeting a meiotic accident — still a structure–function story.",
        ],
        "Pedigrees and chromosomal inheritance in Unit 5 start from these numbers. If n+1 is fuzzy, Punnett squares for sex-linked traits will be too.",
        "Sketch four gametes and put the extra chromosome in the correct two (meiosis I) or one (meiosis II). The sketch is the answer.",
        lesson_figure(
            _nondisj_svg(),
            "Nondisjunction products: n+1 and n−1",
            "One gamete received both partners; the other received none. Fertilization then yields trisomy or monosomy.",
        )
        + solved(16, "Define aneuploidy vs polyploidy with one example each.",
                 ["Aneuploidy: extra or missing individual chromosomes — trisomy 21.",
                  "Polyploidy: extra complete sets — a 4n plant.",
                  "A human 3n zygote is polyploid and almost never viable; a plant 4n may be fertile."],
                 "aneuploidy = wrong count of one chromosome; polyploidy = extra sets", "", "Easy")
        + solved(17, "A nondisjunction in meiosis I for chromosome 21 produces what gamete set (for that chromosome)?",
                 ["The two homologs failed to separate.",
                  "Two gametes get both (n+1) and two get none (n−1).",
                  "No normal gametes for that chromosome from that meiosis."],
                 "two n+1 and two n−1", "", "Medium")
        + solved(18, "Why might 47,XXY (Klinefelter) be live-born while trisomy 1 is not seen in births?",
                 ["Chromosome 1 is gene-rich; an extra copy wrecks dosage for thousands of genes.",
                  "Extra X chromosomes can be largely silenced as Barr bodies, and Y is gene-poor.",
                  "The same error (nondisjunction) has different fitness depending on which chromosome’s dosage is broken."],
                 "dosage: autosome 1 intolerant; extra X partly inactivated", "", "Hard"),
        ("Using ‘nondisjunction’ as a synonym for mutation of a gene’s bases",
         "Nondisjunction is a segregation error (whole chromosomes). A substitution is a sequence error. Karyotypes see the first; sequencing sees the second."),
        ("Draw four products, then fertilize one with a normal 23",
         "If you cannot place the extra chromosome into specific gametes, you cannot predict the zygote. The drawing forces the arithmetic."),
        [
            "I can predict n+1 / n−1 gametes from meiosis I vs II errors.",
            "I can define aneuploidy, trisomy, monosomy, and polyploidy.",
            "I can list mutation, crossing over, assortment, and fertilization as variation sources.",
        ],
        26,
    )

    body = c1 + c2 + c3 + c4 + c5 + c6
    content = unit_shell(
        title,
        AUDIENCE,
        [
            "Ligands, receptors, cascades, and second messengers",
            "Negative vs positive feedback and varied cellular responses",
            "Mitosis stages, chromatid counts, and cytokinesis",
            "Checkpoints, cyclin–CDK, and cancer genetics",
            "Meiosis I vs II, crossing over, and independent assortment",
            "Nondisjunction, aneuploidy, and sources of variation",
        ],
        body,
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()



