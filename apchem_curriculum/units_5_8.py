"""AP Chemistry units 5–8: kinetics through acids/electrochemistry."""
from __future__ import annotations

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, page_break, mq,
    xy_graph, sample_curve, beaker_svg, energy_diagram_svg, titration_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _qs(rows):
    return [mq(t, a, e, i, distractors=d) for i, (t, a, e, d) in enumerate(rows, 1)]


def _energy_cat(w=340, h=210):
    """Uncatalyzed high barrier vs catalyzed lower barrier; same ΔE."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="28" y1="190" x2="320" y2="190" stroke="#0f172a"/>'
        f'<line x1="28" y1="18" x2="28" y2="190" stroke="#0f172a"/>'
        f'<path d="M40 130 C90 130, 110 28, 160 24 C210 28, 230 118, 310 122" fill="none" stroke="#b45309" stroke-width="2.6"/>'
        f'<path d="M40 130 C90 130, 120 88, 160 84 C200 88, 230 118, 310 122" fill="none" stroke="#1d4ed8" stroke-width="2.6" stroke-dasharray="6 4"/>'
        f'<text x="8" y="24" font-size="11">E</text>'
        f'<text x="36" y="122" font-size="11">reactants</text>'
        f'<text x="250" y="112" font-size="11">products</text>'
        f'<text x="150" y="18" font-size="11" fill="#b45309">uncatalyzed Ea</text>'
        f'<text x="168" y="76" font-size="11" fill="#1d4ed8">catalyzed Ea</text>'
        f'<text x="200" y="205" font-size="11">reaction coordinate</text>'
        f"</svg>"
    )


def _mb_ea_svg(w=340, h=210):
    """Maxwell–Boltzmann energy distribution with a vertical Ea cutoff — not a catalysis overlay."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="28" y1="180" x2="320" y2="180" stroke="#0f172a"/>'
        f'<line x1="28" y1="18" x2="28" y2="180" stroke="#0f172a"/>'
        f'<path d="M36 180 C70 180, 90 40, 130 36 C170 32, 200 90, 318 176" fill="none" stroke="#1d4ed8" stroke-width="2.5"/>'
        f'<path d="M210 180 L210 92 C230 110, 260 140, 318 176 L318 180 Z" fill="#fca5a5" opacity="0.55"/>'
        f'<line x1="210" y1="28" x2="210" y2="180" stroke="#b91c1c" stroke-width="2" stroke-dasharray="5 4"/>'
        f'<text x="218" y="44" font-size="12" fill="#b91c1c">Ea</text>'
        f'<text x="236" y="108" font-size="11" fill="#7f1d1d">E ≥ Ea</text>'
        f'<text x="8" y="24" font-size="11">fraction</text>'
        f'<text x="230" y="198" font-size="11">collision energy</text>'
        f'<text x="70" y="28" font-size="11" fill="#1d4ed8">Maxwell–Boltzmann</text>'
        f"</svg>"
    )


def _energy_two_hump(w=360, h=220):
    """Two-step mechanism: intermediate valley; highest peak is the RDS."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="28" y1="198" x2="340" y2="198" stroke="#0f172a"/>'
        f'<line x1="28" y1="16" x2="28" y2="198" stroke="#0f172a"/>'
        f'<path d="M40 150 C70 150, 85 78, 105 52 C125 28, 140 48, 155 118 '
        f'C170 175, 185 168, 200 122 C220 55, 235 22, 255 20 C280 22, 300 128, 338 132" '
        f'fill="none" stroke="#7c3aed" stroke-width="2.6"/>'
        f'<text x="8" y="22" font-size="11">E</text>'
        f'<text x="36" y="142" font-size="11">A (reactants)</text>'
        f'<text x="148" y="188" font-size="11">I (intermediate)</text>'
        f'<text x="270" y="120" font-size="11">B (products)</text>'
        f'<text x="88" y="44" font-size="11" fill="#b45309">step 1 peak</text>'
        f'<text x="232" y="16" font-size="11" fill="#b91c1c">RDS (highest peak)</text>'
        f'<text x="210" y="214" font-size="11">reaction coordinate</text>'
        f"</svg>"
    )


def _energy_endo(w=320, h=200):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="28" y1="180" x2="300" y2="180" stroke="#0f172a"/>'
        f'<line x1="28" y1="16" x2="28" y2="180" stroke="#0f172a"/>'
        f'<path d="M40 140 C90 140, 110 40, 155 36 C200 40, 230 78, 290 82" fill="none" stroke="#7c3aed" stroke-width="2.5"/>'
        f'<text x="36" y="132" font-size="11">reactants</text>'
        f'<text x="230" y="74" font-size="11">products (higher E)</text>'
        f'<text x="8" y="24" font-size="11">E</text>'
        f'<text x="140" y="28" font-size="11">Ea</text>'
        f'<text x="200" y="196" font-size="11">endothermic: ΔH>0</text>'
        f"</svg>"
    )


def _galvanic_svg(w=400, h=220):
    """Two-beaker Zn/Cu cell with salt bridge — not a circuit schematic of resistors."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<path d="M30 50 L30 180 L150 180 L150 50" fill="none" stroke="#0f172a" stroke-width="2.5"/>'
        f'<rect x="34" y="100" width="112" height="76" fill="#dbeafe"/>'
        f'<rect x="82" y="70" width="16" height="110" fill="#94a3b8" stroke="#334155"/>'
        f'<text x="90" y="64" text-anchor="middle" font-size="12">Zn</text>'
        f'<text x="90" y="210" text-anchor="middle" font-size="11">Zn²⁺(aq) anode (−)</text>'
        f'<path d="M250 50 L250 180 L370 180 L370 50" fill="none" stroke="#0f172a" stroke-width="2.5"/>'
        f'<rect x="254" y="100" width="112" height="76" fill="#fecaca"/>'
        f'<rect x="302" y="70" width="16" height="110" fill="#b45309" stroke="#7c2d12"/>'
        f'<text x="310" y="64" text-anchor="middle" font-size="12">Cu</text>'
        f'<text x="310" y="210" text-anchor="middle" font-size="11">Cu²⁺(aq) cathode (+)</text>'
        f'<path d="M150 80 C180 20, 220 20, 250 80" fill="none" stroke="#64748b" stroke-width="8"/>'
        f'<text x="200" y="28" text-anchor="middle" font-size="11">salt bridge</text>'
        f'<line x1="90" y1="70" x2="90" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="90" y1="40" x2="310" y2="40" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="310" y1="40" x2="310" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<polygon points="200,34 220,40 200,46" fill="#4f46e5"/>'
        f'<text x="200" y="22" text-anchor="middle" font-size="11">e⁻</text>'
        f"</svg>"
    )


def _ice_table(caption, cols):
    """cols: list of (species, I, C, E)."""
    head = "".join(f"<th style='padding:6px 10px;border:1px solid #cbd5e1'>{c[0]}</th>" for c in cols)
    irow = "".join(f"<td style='padding:6px 10px;border:1px solid #cbd5e1'>{c[1]}</td>" for c in cols)
    crow = "".join(f"<td style='padding:6px 10px;border:1px solid #cbd5e1'>{c[2]}</td>" for c in cols)
    erow = "".join(f"<td style='padding:6px 10px;border:1px solid #cbd5e1'>{c[3]}</td>" for c in cols)
    return (
        f"<p><strong>{caption}</strong></p>"
        f"<table style='border-collapse:collapse;margin:8px 0 16px'>"
        f"<tr><th style='padding:6px 10px;border:1px solid #cbd5e1'></th>{head}</tr>"
        f"<tr><th style='padding:6px 10px;border:1px solid #cbd5e1'>I</th>{irow}</tr>"
        f"<tr><th style='padding:6px 10px;border:1px solid #cbd5e1'>C</th>{crow}</tr>"
        f"<tr><th style='padding:6px 10px;border:1px solid #cbd5e1'>E</th>{erow}</tr>"
        f"</table>"
    )


def _buffer_beaker(w=240, h=170):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<path d="M50 24 L50 140 L190 140 L190 24" fill="none" stroke="#0f172a" stroke-width="3"/>'
        f'<rect x="54" y="70" width="132" height="66" fill="#e0e7ff"/>'
        f'<circle cx="90" cy="95" r="8" fill="#1d4ed8"/>'
        f'<circle cx="130" cy="110" r="8" fill="#1d4ed8"/>'
        f'<circle cx="160" cy="92" r="8" fill="#b91c1c"/>'
        f'<circle cx="110" cy="80" r="8" fill="#b91c1c"/>'
        f'<text x="120" y="162" text-anchor="middle" font-size="12">HA (blue) + A⁻ (red)</text>'
        f"</svg>"
    )


def _weak_acid_curve(w=300, h=190):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="36" y1="160" x2="280" y2="160" stroke="#0f172a"/>'
        f'<line x1="36" y1="20" x2="36" y2="160" stroke="#0f172a"/>'
        f'<path d="M48 128 C90 118, 110 108, 140 100 C155 70, 165 40, 185 32 C220 24, 260 22, 275 20" '
        f'fill="none" stroke="#7c3aed" stroke-width="2.4"/>'
        f'<circle cx="140" cy="100" r="4" fill="#b91c1c"/>'
        f'<text x="148" y="96" font-size="11">half-eq pH=pKa</text>'
        f'<text x="188" y="50" font-size="11">eq. pt. pH>7</text>'
        f'<text x="250" y="176" font-size="11">V_b</text>'
        f'<text x="8" y="28" font-size="11">pH</text>'
        f"</svg>"
    )


def _phases_svg(w=320, h=150):
    """Liquid vs gas particulate — entropy picture, not an energy peak."""
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="16" y="20" width="130" height="100" fill="#dbeafe" stroke="#0f172a"/>'
        f'<circle cx="50" cy="55" r="8" fill="#1d4ed8"/>'
        f'<circle cx="78" cy="80" r="8" fill="#1d4ed8"/>'
        f'<circle cx="110" cy="50" r="8" fill="#1d4ed8"/>'
        f'<circle cx="95" cy="95" r="8" fill="#1d4ed8"/>'
        f'<text x="81" y="140" text-anchor="middle" font-size="11">liquid: close, fewer ways</text>'
        f'<rect x="174" y="20" width="130" height="100" fill="#f8fafc" stroke="#0f172a"/>'
        f'<circle cx="194" cy="40" r="6" fill="#b91c1c"/>'
        f'<circle cx="250" cy="70" r="6" fill="#b91c1c"/>'
        f'<circle cx="280" cy="45" r="6" fill="#b91c1c"/>'
        f'<circle cx="220" cy="95" r="6" fill="#b91c1c"/>'
        f'<text x="239" y="140" text-anchor="middle" font-size="11">gas: far, many ways (larger S)</text>'
        f"</svg>"
    )


# ===========================================================================
# UNIT 5
# ===========================================================================

def _u5_questions():
    return _qs([
        ("A rate law is:",
         "an experimental equation: rate = k[A]^m[B]^n",
         "Orders m and n come from data, not from the overall balanced equation (unless it is an elementary step).",
         ["always rate = k[A][B] from the stoichiometry", "the same as K, the equilibrium constant", "ΔH of the reaction"]),
        ("If doubling [A] at constant [B] doubles the rate, the order in A is:",
         "1 (first order)", "2^m = 2 ⇒ m=1.",
         ["0", "2", "3"]),
        ("If doubling [A] quadruples the rate, the order in A is:",
         "2", "2^m = 4 ⇒ m=2.",
         ["1", "0", "4"]),
        ("Exp 1: [A]=0.10, [B]=0.10, rate=2.0×10⁻³. Exp 2: [A]=0.20, [B]=0.10, rate=8.0×10⁻³. Order in A?",
         "2", "Rate ×4 when [A] ×2 ⇒ second order in A.",
         ["1", "0", "3"]),
        ("Same data, Exp 3: [A]=0.10, [B]=0.20, rate still 2.0×10⁻³. Order in B?",
         "0", "Changing [B] did not change the rate.",
         ["1", "2", "−1"]),
        ("For a first-order reaction, a linear graph is:",
         "ln[A] versus t", "Integrated law: ln[A]=ln[A]₀ − kt.",
         ["[A] versus t", "1/[A] versus t", "rate versus 1/T"]),
        ("Zero-order integrated plot that is linear:",
         "[A] versus t (slope = −k)",
         "[A]=[A]₀ − kt.",
         ["ln[A] vs t", "1/[A] vs t", "[A]² vs t"]),
        ("Second-order (rate=k[A]²) linear plot:",
         "1/[A] versus t", "1/[A]=1/[A]₀ + kt.",
         ["ln[A] vs t", "[A] vs t", "√[A] vs t"]),
        ("First-order half-life is 20 min. Fraction of reactant left after 60 min?",
         "1/8", "Three half-lives: (1/2)³=1/8.",
         ["1/4", "1/6", "1/3"]),
        ("If k=0.0693 min⁻¹ for a first-order reaction, t½ is closest to:",
         "10.0 min", "t½=0.693/k=0.693/0.0693=10.0 min.",
         ["0.0693 min", "69.3 min", "1.00 min"]),
        ("Collision theory says a reaction occurs when particles collide with:",
         "enough energy and proper orientation",
         "Frequency, energy, and geometry all matter.",
         ["any energy if they touch", "only if they are ions", "zero kinetic energy"]),
        ("Increasing temperature increases rate mainly because:",
         "a larger fraction of collisions exceed Ea",
         "The high-energy tail of the speed distribution grows.",
         ["Ea becomes zero", "K must increase in every reaction", "particle mass decreases"]),
        ("A higher activation energy, at the same T, means:",
         "a smaller fraction of collisions are successful, so a slower rate",
         "Fewer particles clear the barrier.",
         ["a guaranteed faster rate", "ΔH must be more negative", "the reaction is zero-order"]),
        ("Orientation matters most for:",
         "complicated molecules that must meet at a specific site",
         "A steric requirement lowers the effective collision frequency.",
         ["nuclear fusion only", "all noble-gas mixing", "phase changes"]),
        ("Concentration increases rate (usually) because:",
         "collisions become more frequent",
         "More particles per volume → more collisions per second.",
         ["Ea drops to zero", "temperature must fall", "K decreases"]),
        ("In a mechanism, the rate law of an elementary step is:",
         "written from that step's molecularity (the particles that collide)",
         "A bimolecular step A+B→ products has rate = k[A][B].",
         ["always the overall stoichiometry", "independent of slow vs fast", "equal to K"]),
        ("The slow step of a mechanism is:",
         "rate-determining; the observed rate law matches that step (after substituting intermediates)",
         "Fast steps after the slow step do not set the speed.",
         ["always unimolecular", "the step with the catalyst", "irrelevant to the rate law"]),
        ("An intermediate is a species that is:",
         "produced then consumed (does not appear in the overall equation)",
         "It should not remain in the final experimental rate law.",
         ["added at the start and recovered at the end", "the solvent", "a spectator ion always"]),
        ("A catalyst is a species that is:",
         "consumed in an early step and regenerated later (overall unchanged)",
         "It may appear in the rate law; it is not an intermediate.",
         ["produced and never used up", "always a product in the overall equation", "the same as an intermediate"]),
        ("If the slow step is A+A→X, the rate law is:",
         "rate = k[A]²", "Bimolecular in A.",
         ["rate = k[A]", "rate = k", "rate = k[X]"]),
        ("A catalyst increases rate by:",
         "providing a path with lower Ea",
         "More collisions then exceed the lower barrier.",
         ["increasing ΔH", "changing the overall stoichiometry permanently", "raising Ea"]),
        ("A catalyst does not change:",
         "ΔH or K (the equilibrium constant) at a given T",
         "It speeds forward and reverse equally in the sense that equilibrium composition is unchanged.",
         ["the rate", "the mechanism", "the value of Ea on the new path"]),
        ("On an energy diagram, a catalyzed path has:",
         "a lower peak but the same reactant and product energies",
         "Ea falls; ΔE stays the same.",
         ["products dropped below the x-axis always", "no peak at all", "higher Ea"]),
        ("Heterogeneous catalysis often works by:",
         "adsorbing reactants on a solid surface, weakening bonds and holding them in place",
         "A metal surface is a classic example (Haber process, catalytic converter).",
         ["raising the boiling point of the solvent only", "adding more product", "changing R in PV=nRT"]),
        ("Adding a catalyst to a system already at equilibrium will:",
         "not shift the position of equilibrium (K unchanged)",
         "Both directions speed up; Q still equals K.",
         ["always make more product", "always make more reactant", "change ΔG°"]),
        ("Arrhenius: k increases as T increases because:",
         "the exponential factor e^{−Ea/RT} grows as T grows",
         "Qualitative: more particles clear Ea.",
         ["Ea increases with T", "R becomes smaller", "order becomes zero"]),
        ("A plot of ln k versus 1/T is linear with slope:",
         "−Ea/R", "Arrhenius: ln k = ln A − (Ea/R)(1/T).",
         ["+Ea/R", "−R/Ea", "Ea only"]),
        ("A steeper (more negative) slope on ln k vs 1/T means:",
         "larger Ea; the rate is more sensitive to temperature",
         "Qualitative slope comparison — no derivative required.",
         ["smaller Ea", "k independent of T", "zero-order kinetics"]),
        ("Two reactions at the same T: the one with larger Ea has:",
         "the smaller k (all else similar)",
         "Fewer successful collisions.",
         ["the larger k always", "K=1", "no rate"]),
        ("If Ea is very small, the temperature dependence of k is:",
         "weaker (flatter ln k vs 1/T)",
         "Almost every collision already has enough energy.",
         ["infinitely steep", "undefined", "exactly zero-order"]),
        ("rate = k[A]²[B]. If [A] and [B] both double, the rate becomes:",
         "8 times as large", "2²×2=8.",
         ["4 times", "2 times", "unchanged"]),
        ("[A]₀=0.80 M, first-order, three half-lives. [A] remaining?",
         "0.10 M", "0.80→0.40→0.20→0.10.",
         ["0.27 M", "0.40 M", "0.08 M"]),
        ("Which statement about mechanisms is correct?",
         "The sum of elementary steps must give the overall reaction",
         "Atoms are conserved step by step.",
         ["Intermediates must appear in the overall products", "The fast step always determines the rate", "Orders must match the overall mole ratio always"]),
        ("A unimolecular elementary step A→B has rate law:",
         "rate = k[A]", "One particle rearranges.",
         ["rate = k[A]²", "rate = k", "rate = k[B]/[A]"]),
        ("Collision frequency increases when:",
         "concentration or (usually) temperature increases",
         "More particles or faster particles → more collisions.",
         ["Ea increases", "the particles become heavier", "the reaction becomes endothermic"]),
        ("The units of k for a first-order reaction are:",
         "time⁻¹ (e.g. s⁻¹)", "rate has units concentration/time; [A]¹ so k is 1/time.",
         ["M⁻¹ s⁻¹", "M s⁻¹", "M⁻² s⁻¹"]),
        ("Units of k for rate = k[A]²?",
         "M⁻¹ s⁻¹", "rate M/s divided by M².",
         ["s⁻¹", "M s⁻¹", "dimensionless"]),
        ("A catalyst in a mechanism should:",
         "cancel when the steps are added",
         "Net: catalyst is regenerated.",
         ["appear only as a product", "have a negative concentration", "be an intermediate that builds up forever"]),
        ("If ln[A] vs t is linear but [A] vs t is curved, the reaction is:",
         "first order in A", "That is the diagnostic plot.",
         ["zero order", "second order", "not dependent on [A]"]),
        ("Half-life of a first-order process is independent of:",
         "[A]₀", "t½=0.693/k only.",
         ["k", "temperature (always)", "whether a catalyst is present (Ea never matters)"]),
        ("Raising T by a modest amount often roughly doubles a rate because:",
         "the fraction of molecules with E>Ea is very sensitive to T",
         "Qualitative Arrhenius, not a law that every 10°C doubles every reaction.",
         ["Ea becomes negative", "orders change from 2 to 1", "PV=nRT requires it"]),
        ("An enzyme is a biological catalyst. It:",
         "lowers Ea of the metabolic step and is regenerated",
         "Same definition as any catalyst.",
         ["is consumed as a stoichiometric reactant", "changes ΔG° of the reaction", "appears in K"]),
        ("The observed rate law rate=k[NO]²[O₂] is consistent with a slow step that is:",
         "bimolecular in a way that produces that concentration dependence (possibly after a fast equilibrium)",
         "You cannot invent the unique mechanism from the rate law alone, but the slow step must agree with the orders.",
         ["always NO+NO+O₂ as a single three-body event only", "zero-order in NO", "unimolecular NO→ products"]),
        ("If a proposed slow step is 2 NO₂ → NO₃ + NO, the rate law is:",
         "rate = k[NO₂]²", "Elementary bimolecular.",
         ["rate = k[NO₂]", "rate = k[NO₃][NO]", "rate = k"]),
        ("A graph of 1/[A] vs t has slope +0.50 M⁻¹ s⁻¹. That slope equals:",
         "k for a second-order reaction", "Integrated second-order: slope = k.",
         ["−k for first order", "[A]₀", "Ea"]),
        ("After 2.00 half-lives of a first-order decay, the fraction remaining is:",
         "1/4", "(1/2)²=1/4.",
         ["1/2", "1/8", "0"]),
        ("AP Stretch: Initial-rate data: Exp1 [A]=0.30 M, [B]=0.10 M, rate=9.0×10⁻⁴; Exp2 [A]=0.60 M, [B]=0.10 M, rate=1.8×10⁻³; Exp3 [A]=0.30 M, [B]=0.20 M, rate=3.6×10⁻³. Order in A, order in B, and k with units?",
         "first in A, second in B; k=0.30 M⁻² s⁻¹",
         "[A]×2 at fixed [B] doubles rate ⇒ m=1. [B]×2 at fixed [A] multiplies rate by 4 ⇒ n=2. k=rate/([A][B]²)=(9.0×10⁻⁴)/((0.30)(0.10)²)=9.0×10⁻⁴/0.0030=0.30 M⁻² s⁻¹.",
         ["second in A, zero in B; k=0.010", "first in both; k=0.030", "second in A, first in B; k=0.10"]),
        ("AP Stretch: [A]₀=0.60 M, first-order, [A]=0.15 M at t=36 s. Find k and the half-life.",
         "k=0.0385 s⁻¹; t½=18.0 s",
         "ln(0.60/0.15)=ln 4=1.386=k(36) ⇒ k=0.0385 s⁻¹; t½=0.693/0.0385=18.0 s. Check: 36 s is two half-lives and 0.60→0.15 is two halvings.",
         ["k=0.0693 s⁻¹; t½=10.0 s", "k=0.015 s⁻¹; t½=46 s", "k=0.693 s⁻¹; t½=36 s"]),
        ("AP Stretch: A mechanism is (1) fast: 2A ⇌ I (2) slow: I+B → C. The predicted rate law in A,B (no I) is:",
         "rate = k′[A]²[B]",
         "Slow step rate=k₂[I][B]; from the fast equilibrium [I]=K[A]²; so rate=k₂K[A]²[B].",
         ["rate = k[I] as the experimental law with I as a starting material", "rate = k[A][B]", "rate = k[C]"]),
        ("AP Stretch: Two reactions have the same A factor. Reaction X has a steeper negative slope of ln k vs 1/T than Y. Which has the larger Ea, and which is faster at very high T if they meet?",
         "X has larger Ea; at high T they approach similar k if A is the same (X still slightly smaller k)",
         "Steeper slope ⇒ larger Ea. As 1/T→0, ln k → ln A for both.",
         ["Y has larger Ea", "X has Ea=0", "slope is unrelated to Ea"]),
        ("AP Stretch: [A]₀=1.20 M, t½=15 min (first order). Concentration after 45 min and after 60 min?",
         "0.150 M then 0.075 M",
         "45 min = 3 half-lives → 1.20/8=0.150 M. 60 min = 4 half-lives → 1.20/16=0.075 M.",
         ["0.40 M then 0.20 M", "0.60 M then 0.30 M", "0.10 M then 0.00 M"]),
        ("AP Stretch: Explain, with collision theory, why a catalyst speeds a reaction even at the same T and concentrations.",
         "The new path has lower Ea, so a larger fraction of the same collisions succeed",
         "T sets the energy distribution; Ea sets the cutoff. Lower cutoff → more successful collisions. Orientation on a surface can also improve.",
         ["The catalyst raises T inside the flask", "The catalyst increases K only", "Particles lose mass"]),
        ("AP Stretch: Initial-rate data: Exp1 [A]=0.10 M, [B]=0.10 M, rate=2.0×10⁻⁴; Exp2 [A]=0.10 M, [B]=0.20 M, rate=4.0×10⁻⁴; Exp3 [A]=0.20 M, [B]=0.10 M, rate=8.0×10⁻⁴. Find orders, k, and the predicted rate at [A]=0.30 M, [B]=0.20 M.",
         "rate=k[A]²[B]; k=0.20 M⁻² s⁻¹; predicted rate=3.6×10⁻³ M/s",
         "[B]×2 at fixed [A] doubles rate ⇒ n=1. [A]×2 at fixed [B] quadruples rate ⇒ m=2. k=(2.0×10⁻⁴)/((0.10)²(0.10))=0.20 M⁻² s⁻¹. Rate=0.20(0.30)²(0.20)=0.20(0.09)(0.20)=3.6×10⁻³.",
         ["rate=k[A][B]; k=0.020; predicted 1.2×10⁻³", "second in B only; predicted 8.0×10⁻⁴", "factor 1.5 with no table"]),
        ("AP Stretch: Why can the overall balanced equation 2A+B→C have a rate law rate=k[A] if the mechanism has a slow unimolecular step after A is supplied?",
         "Orders come from the slow elementary step, not from the overall mole ratio",
         "Stoichiometry of the net reaction does not dictate the rate law.",
         ["The rate law must be rate=k[A]²[B]", "K equals the rate law", "B cannot appear in any step"]),
        ("AP Stretch: A student plots [A] vs t and gets a curve, plots ln[A] vs t and gets a line of slope −0.0231 min⁻¹. Order, k, and t½?",
         "first order; k=0.0231 min⁻¹; t½=30.0 min",
         "Linear ln[A] ⇒ first order; |slope|=k; t½=0.693/0.0231=30.0 min.",
         ["zero order; k=0.0231 M/min; t½ depends on [A]₀ only as 0.0231", "second order; k=0.0231; t½=30", "not first order because [A] vs t was curved? that actually supports first order"]),
    ])


def build_unit5():
    title = "AP Chemistry Unit 5: Kinetics"
    description = (
        "Rate laws from data, integrated laws and half-life arithmetic, collision theory, mechanisms, "
        "catalysts, and qualitative Arrhenius slopes — no calculus required."
    )
    c1 = concept_block(
        "1. Rate laws from data",
        [
            "The rate of a reaction is how fast a concentration changes, often written as the disappearance of "
            "a reactant or appearance of a product (with signs and coefficients so the same positive rate is "
            "shared). A rate law is an experimental equation $\\mathrm{rate}=k[A]^m[B]^n$. The constant $k$ is "
            "the rate constant; $m$ and $n$ are orders.",
            "Orders are not taken from the overall balanced equation unless that equation is a single elementary "
            "step. You find them by changing one concentration at a time in a table of initial rates.",
            "If doubling $[A]$ at constant $[B]$ doubles the rate, $2^m=2$ so $m=1$. If doubling $[A]$ "
            "quadruples the rate, $2^m=4$ so $m=2$. If the rate does not change, $m=0$.",
            "Worked table: Exp 1 $[A]=0.10$, $[B]=0.10$, rate $=2.0\\times10^{-3}$. Exp 2 $[A]=0.20$, $[B]=0.10$, "
            "rate $=8.0\\times10^{-3}$. Rate $\\times 4$ when $[A]\\times 2$ → second order in A. Exp 3 $[A]=0.10$, "
            "$[B]=0.20$, rate still $2.0\\times10^{-3}$ → zero order in B.",
            "Then $k=\\mathrm{rate}/[A]^2=(2.0\\times10^{-3})/(0.10)^2=0.20\\,\\mathrm{M^{-1}s^{-1}}$. Units of $k$ "
            "depend on overall order: first-order $k$ is $\\mathrm{s^{-1}}$; second-order $k$ is $\\mathrm{M^{-1}s^{-1}}$.",
            "Overall order is $m+n$. The rate law is how kinetics talks; $K$ (equilibrium constant) is a different "
            "symbol for a different idea (Unit 7). Do not mix $k$ and $K$.",
        ],
        "Every later kinetics item — integrated laws, mechanisms, catalysis — assumes you can read an initial-rate "
        "table. This is the experimental definition of order.",
        "Circle the two experiments that change only one species. Form the rate ratio, take the corresponding "
        "concentration ratio to the power $m$, and solve for $m$. Then plug one row into the rate law to get $k$.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", [(0.10, 0.002), (0.20, 0.008), (0.30, 0.018)])],
                points=[(0.10, 0.002, "exp1"), (0.20, 0.008, "exp2")],
                xlim=(0, 0.35), ylim=(0, 0.022), xlab="[A] (M)", ylab="rate (M/s)", w=320, h=240,
            ),
            "Initial rate vs [A] when the reaction is second order in A",
            "Quadrupling the height when [A] doubles is the signature of $m=2$. A first-order plot would be a "
            "straight line through the origin.",
        )
        + solved(1, "Doubling $[A]$ doubles the rate. What is the order in A?",
               ["Write $2^m=2$.",
                "The exponent that satisfies this is $m=1$.",
                "The reaction is first order in A."],
               "first order ($m=1$)", "", "Easy")
        + solved(2, "From Exp 1 and Exp 2 above, find the order in A.",
                 ["$[A]$ doubles from $0.10$ to $0.20$.",
                  "Rate goes from $2.0\\times10^{-3}$ to $8.0\\times10^{-3}$, a factor of $4$.",
                  "$2^m=4\\Rightarrow m=2$."],
                 "2", "", "Medium")
        + solved(3, "Using Exp 1 and order $2$ in A (zero in B), compute $k$.",
                 ["$\\mathrm{rate}=k[A]^2$.",
                  "$k=(2.0\\times10^{-3})/(0.10)^2$.",
                  "$(0.10)^2=0.010$, so $k=0.20$.",
                  "Units: $\\mathrm{M/s}$ divided by $\\mathrm{M^2}$ is $\\mathrm{M^{-1}s^{-1}}$."],
                 "$0.20\\,\\mathrm{M^{-1}s^{-1}}$", "", "Hard"),
        ("Copying stoichiometric coefficients into the rate law",
         "The overall equation $2\\,\\mathrm{H_2+O_2\\rightarrow 2\\,H_2O}$ does not imply rate $=k[H_2]^2[O_2]$. "
         "Orders come from experiments or from an elementary step in a mechanism."),
        ("Build the rate ratio with the experiment that changes only one concentration",
         "If both $[A]$ and $[B]$ change, you cannot solve for one order. Find a pair of rows that holds the "
         "other species fixed."),
        [
            "I can determine reaction order from an initial-rate table.",
            "I can compute $k$ with correct units from one experiment.",
            "I can explain why orders are not the overall coefficients.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Integrated rate laws",
        [
            "An integrated rate law tells concentration as a function of time. You do not need calculus on the "
            "AP Chemistry exam: you need the three diagnostic plots and the first-order half-life formula.",
            "Zero order: $[A]=[A]_0-kt$. A plot of $[A]$ versus $t$ is linear with slope $-k$. First order: "
            "$\\ln[A]=\\ln[A]_0-kt$. A plot of $\\ln[A]$ versus $t$ is linear with slope $-k$. Second order "
            "(in a single reactant): $1/[A]=1/[A]_0+kt$, so $1/[A]$ versus $t$ is linear with slope $+k$.",
            "To identify the order from data, plot all three. Exactly one should be linear. Curved $[A]$ vs $t$ "
            "plus linear $\\ln[A]$ vs $t$ means first order — the curve is not a failure; it is expected.",
            "First-order half-life is $t_{1/2}=0.693/k$ and does not depend on $[A]_0$. If $k=0.0693\\,\\mathrm{min^{-1}}$, "
            "$t_{1/2}=10.0$ min. After $n$ half-lives the fraction left is $(1/2)^n$. Three half-lives leave $1/8$.",
            "Numeric: $[A]_0=0.80$ M, $t_{1/2}=20$ min. After $60$ min (three half-lives) $[A]=0.10$ M. After "
            "$40$ min (two half-lives) $[A]=0.20$ M. After $80$ min, $[A]=0.050$ M.",
            "Another: $[A]_0=0.40$ M, $[A]=0.10$ M at $t=20$ s. $\\ln(0.40/0.10)=\\ln 4=1.386=k(20)$, so "
            "$k=0.0693\\,\\mathrm{s^{-1}}$ and $t_{1/2}=10.0$ s. Write $\\ln([A]_0/[A])=kt$ rather than guessing.",
        ],
        "Half-life arithmetic is the most common quantitative kinetics item. The diagnostic plots are how you "
        "justify which integrated law to use.",
        "Identify order from which graph is linear. For first order, count half-lives or use $\\ln([A]_0/[A])=kt$. "
        "Do not use $t_{1/2}=0.693/k$ for zero- or second-order processes (those half-lives depend on $[A]_0$).",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", sample_curve(lambda t: 0.80 * (0.5 ** (t / 20)), 0, 80))],
                points=[(0, 0.80, "[A]₀"), (20, 0.40, "t½"), (40, 0.20, ""), (60, 0.10, "3 t½")],
                xlim=(0, 85), ylim=(0, 1.0), xlab="t (min)", ylab="[A] (M)", w=340, h=240,
            ),
            "First-order decay: $[A]$ vs time is curved; each half-life cuts $[A]$ in half",
            "From 0.80 M, the concentration is 0.40, 0.20, 0.10 M at 20, 40, 60 min if $t_{1/2}=20$ min.",
        )
        + solved(4, "First-order $t_{1/2}=20$ min. Fraction left after $60$ min?",
               ["$60/20=3$ half-lives.",
                "Each half-life multiplies $[A]$ by $1/2$.",
                "$(1/2)^3=1/8$."],
               "$1/8$", "", "Easy")
        + solved(5, "$[A]_0=0.80$ M, first-order, three half-lives. Find $[A]$.",
                 ["$0.80\\times(1/2)^3$.",
                  "$(1/2)^3=1/8=0.125$.",
                  "$0.80\\times 0.125=0.10$ M."],
                 "$0.10$ M", "", "Medium")
        + solved(6, "$[A]_0=0.40$ M, $[A]=0.10$ M at $20$ s, first order. Find $k$ and $t_{1/2}$.",
                 ["$\\ln([A]_0/[A])=\\ln(4)=1.386$.",
                  "$1.386=k(20)\\Rightarrow k=0.0693\\,\\mathrm{s^{-1}}$.",
                  "$t_{1/2}=0.693/k=0.693/0.0693=10.0$ s.",
                  "Check: $20$ s is two half-lives, and $0.40\\rightarrow 0.10$ is two halvings."],
                 "$k=0.0693\\,\\mathrm{s^{-1}}$, $t_{1/2}=10.0$ s", "", "Hard"),
        ("Using $t_{1/2}=0.693/k$ on a second-order reaction",
         "That formula is first-order only. Second-order half-life is $1/(k[A]_0)$ and gets longer as the "
         "reactant is used up."),
        ("Count half-lives on a number line of time",
         "Mark $0$, $t_{1/2}$, $2t_{1/2}$, $3t_{1/2}$ and halve the concentration at each tick. This beats "
         "trying to remember a decimal fraction under time pressure."),
        [
            "I can name the linear plot for zero-, first-, and second-order reactions.",
            "I can use $t_{1/2}=0.693/k$ and $(1/2)^n$ for first-order decay.",
            "I can compute $k$ from $\\ln([A]_0/[A])=kt$.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Collision theory",
        [
            "Collision theory says particles must collide in order to react. Not every collision works. The "
            "collision needs enough energy to reach the transition state (to clear the activation energy $E_a$) "
            "and it needs a geometry that lets the right atoms meet.",
            "Concentration raises the collision frequency: more particles in the same volume means more hits "
            "per second. That is why most rates increase when you raise $[A]$ (unless the order in A is zero).",
            "Temperature raises the average kinetic energy. On a Maxwell–Boltzmann sketch, a larger fraction of "
            "the area lies to the right of $E_a$. Even a small $T$ increase can change the successful fraction "
            "a lot, because that tail is exponential in energy. You do not need to differentiate the curve — "
            "just compare areas beyond a vertical $E_a$ line.",
            "A larger $E_a$ at the same $T$ means a smaller successful fraction and a smaller $k$. Orientation "
            "(steric factor) is why some bimolecular reactions are slower than a naive collision count predicts.",
            "Phase and surface area matter in heterogeneous mixtures: powdered zinc reacts with acid faster than "
            "a chunk, because more collisions occur at the solid–liquid interface.",
            "Collision theory is the “why” behind the rate law and behind Arrhenius. When an FRQ asks why $T$ "
            "increases rate, write “larger fraction of collisions exceed $E_a$,” not “molecules shake more.”",
        ],
        "Without collision theory, $k$ is a magic number. With it, you can explain temperature, concentration, "
        "and catalysis in the same language as the energy diagram.",
        "Name three requirements: collision, energy $\\geq E_a$, orientation. Then say which of those the prompt "
        "changed.",
        lesson_figure(
            _mb_ea_svg(),
            "Maxwell–Boltzmann: only the tail past Ea succeeds",
            "The dashed vertical line is the energy cutoff. Shaded collisions have E ≥ Ea. Raising T fattens "
            "that tail without moving Ea. This is not a catalyzed-versus-uncatalyzed reaction-coordinate plot.",
        )
        + solved(7, "Name the two collision requirements besides “the particles must meet.”",
               ["The collision energy must be at least $E_a$.",
                "The orientation must allow the correct bonds to form.",
                "Frequency of collisions then sets how often those successful events happen."],
               "enough energy and proper orientation", "", "Easy")
        + solved(8, "Why does raising $T$ increase rate at constant concentration?",
                 ["The speed distribution spreads to higher energies.",
                  "A larger fraction of collisions exceed $E_a$.",
                  "The successful collision frequency rises, so $k$ rises.",
                  "The balanced equation and $\\Delta H$ do not have to change."],
                 "more collisions clear $E_a$", "", "Medium")
        + solved(9, "Two reactions, same $T$ and similar collision frequencies. Why is the one with larger $E_a$ slower?",
                 ["$E_a$ is the energy cutoff on the distribution.",
                  "A higher cutoff leaves a smaller fraction of successful collisions.",
                  "Smaller successful fraction means smaller $k$ and a smaller rate.",
                  "This is the same diagram as Arrhenius, read qualitatively."],
                 "fewer collisions exceed the higher barrier", "", "Hard"),
        ("Saying temperature increases rate because “equilibrium shifts”",
         "Kinetics is not Le Chatelier. A higher $T$ can make $K$ larger or smaller depending on $\\Delta H$. "
         "The rate increase is about $E_a$ and the energy distribution."),
        ("Draw a vertical line at $E_a$ on a sketch of the energy distribution",
         "Shade to the right. Higher $T$ or lower $E_a$ (catalyst) grows the shaded fraction. That picture is "
         "worth more than a slogan."),
        [
            "I can list energy and orientation as collision requirements.",
            "I can explain the effect of $T$ using the fraction of collisions above $E_a$.",
            "I can connect concentration to collision frequency.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Reaction mechanisms",
        [
            "A mechanism is a sequence of elementary steps that add to the overall reaction. An elementary step "
            "is a single collision event (or a single-molecule rearrangement). Its rate law is written from the "
            "particles that actually collide: unimolecular $A\\rightarrow$ products has rate $=k[A]$; bimolecular "
            "$A+B\\rightarrow$ products has rate $=k[A][B]$.",
            "The slowest step is rate-determining. The experimental rate law must match that slow step after you "
            "have eliminated intermediates. Fast steps after the slow step do not control the speed.",
            "An intermediate is produced in one step and consumed in a later step. It does not appear in the "
            "overall equation and should not remain in the experimental rate law. A catalyst is consumed early "
            "and regenerated later; it cancels in the overall equation but may appear in the rate law.",
            "Example: fast $A+B\\rightleftharpoons C$, slow $C\\rightarrow D$. Overall $A+B\\rightarrow D$. Slow "
            "rate $=k_2[C]$. From the fast equilibrium $K=[C]/([A][B])$ so $[C]=K[A][B]$. Observed rate "
            "$=k_2 K[A][B]=k'[A][B]$. Intermediate $C$ is gone from the rate law.",
            "The steps must add to the overall reaction, and no step may have an order that contradicts the data. "
            "Many mechanisms can fit one rate law; the exam usually asks whether a given mechanism is consistent, "
            "not whether it is the unique truth.",
            "Termolecular elementary steps (three particles at once) are rare. If the overall chemistry looks "
            "like three molecules, the mechanism is probably several bimolecular steps.",
        ],
        "Mechanisms are how AP Chemistry tests whether you understand that the rate law is about the slow "
        "collision, not about the overall recipe.",
        "Write a rate law for the slow step. If it contains an intermediate, replace that intermediate using "
        "a fast equilibrium. Check that the steps sum to the overall equation.",
        lesson_figure(
            _energy_two_hump(),
            "Two-step mechanism: intermediate valley; the highest peak is the RDS",
            "The path dips at intermediate I, then climbs a taller second peak. That taller climb is "
            "rate-determining. This is not a catalyzed-versus-uncatalyzed overlay.",
        )
        + solved(10, "The slow step is $A+A\\rightarrow X$. What is the rate law of that step?",
               ["The step is elementary and bimolecular in A.",
                "Rate $=k[A][A]=k[A]^2$.",
                "That is the predicted observed law if this step is rate-determining and A is a starting material."],
               "rate $=k[A]^2$", "", "Easy")
        + solved(11, "Define intermediate vs catalyst in a mechanism.",
                 ["An intermediate is made and then used up; it is not in the overall reactants or products.",
                  "A catalyst is present at the start, used, and regenerated; overall unchanged.",
                  "Catalysts may appear in the rate law; intermediates should be substituted out.",
                  "Both cancel when elementary steps are added, but they cancel for different reasons."],
                 "made-then-used vs used-then-remade", "", "Medium")
        + solved(12, "Fast $A+B\\rightleftharpoons C$, slow $C\\rightarrow D$. Rate law in terms of A and B?",
                 ["Slow: rate $=k_2[C]$.",
                  "Equilibrium: $K=[C]/([A][B])\\Rightarrow [C]=K[A][B]$.",
                  "Substitute: rate $=k_2 K[A][B]$.",
                  "The experimental law is first order in A and in B; $C$ does not appear."],
                 "rate $=k'[A][B]$", "", "Hard"),
        ("Leaving an intermediate in the reported experimental rate law",
         "The lab measures starting materials and products. If your rate law still has $[C]$ and $C$ is not "
         "a reagent you mix, substitute using the fast equilibrium."),
        ("Add the steps and cancel",
         "A 20-second addition check catches mechanisms that do not match the overall equation — an automatic "
         "inconsistency."),
        [
            "I can write a rate law from an elementary step.",
            "I can identify intermediates and catalysts.",
            "I can substitute a fast equilibrium to remove an intermediate.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Catalysts",
        [
            "A catalyst speeds a reaction by opening a new mechanism with a lower activation energy. On the "
            "energy diagram the peak is lower, but the reactant energy and product energy — so $\\Delta H$ and "
            "$\\Delta G^\\circ$ — stay the same. Equilibrium constant $K$ at a given $T$ does not change.",
            "Because both directions use the new path, a catalyst helps a mixture reach equilibrium faster "
            "without shifting the position of that equilibrium. Adding a catalyst to a system already at "
            "equilibrium does not make extra product.",
            "Homogeneous catalysts are in the same phase as the reactants (acid-catalyzed esterification in "
            "solution). Heterogeneous catalysts are in a different phase, often a solid surface that adsorbs "
            "molecules, weakens bonds, and holds them in a reactive orientation (Haber process on Fe, catalytic "
            "converters).",
            "Enzymes are biological catalysts: large proteins (or RNA) that bind a substrate in an active site, "
            "lower $E_a$, and are regenerated. They do not change $\\Delta G^\\circ$ of the metabolic reaction.",
            "In a mechanism a catalyst is consumed in an early step and remade in a later step. That is how you "
            "distinguish it from an intermediate when you add the steps.",
            "On FRQs, pair “lower $E_a$” with “same $\\Delta H$ / same $K$.” One without the other is incomplete.",
        ],
        "Catalysis is collision theory plus mechanisms plus equilibrium (a preview of Unit 7). It is also how "
        "industry and biology actually run slow reactions at mild temperatures.",
        "On the diagram, lower the peak only. In words: new path, lower $E_a$, more successful collisions, "
        "unchanged thermodynamics.",
        lesson_figure(
            _energy_cat(),
            "Catalyzed (dashed) vs uncatalyzed (solid) paths",
            "Same start, same finish, lower barrier. The vertical drop from reactants to products is ΔH in both "
            "cases. Kinetics changed; equilibrium composition did not.",
        )
        + solved(13, "What does a catalyst do to $E_a$ and to $\\Delta H$?",
               ["$E_a$ decreases because a new path is available.",
                "$\\Delta H$ is a state function of reactants vs products, so it is unchanged.",
                "The diagram's peak drops; the two ends stay put."],
               "lower $E_a$, same $\\Delta H$", "", "Easy")
        + solved(14, "Why does a catalyst not change $K$ at constant $T$?",
                 ["$K$ depends on the relative free energies of reactants and products.",
                  "A catalyst does not change those energies.",
                  "Forward and reverse rates both increase, so their ratio at equilibrium (related to $K$) is the same.",
                  "The system simply arrives at the same $Q=K$ sooner."],
                 "$K$ unchanged", "", "Medium")
        + solved(15, "In a mechanism, how do you recognize the catalyst vs an intermediate?",
                 ["Add the steps.",
                  "The catalyst is present among the original reactants and is regenerated among the final products "
                  "(net zero).",
                  "The intermediate appears only in the middle: produced then consumed, absent from overall reactants and products.",
                  "Both cancel in the net equation; their roles in the flask are different."],
                 "catalyst starts and finishes present; intermediate does not", "", "Hard"),
        ("Claiming a catalyst “shifts equilibrium toward products”",
         "That confuses kinetics with Le Chatelier. A catalyst does not change $K$. Only $T$ (and the reaction's "
         "$\\Delta H$) change $K$."),
        ("Annotate the diagram with two $E_a$ arrows and one $\\Delta H$ arrow",
         "Two different $E_a$ values, one $\\Delta H$. That drawing answers most catalyst FRQs by itself."),
        [
            "I can state that a catalyst lowers $E_a$ but not $\\Delta H$ or $K$.",
            "I can distinguish homogeneous, heterogeneous, and enzyme catalysis at a basic level.",
            "I can find a catalyst by adding mechanism steps.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Arrhenius qualitative",
        [
            "The Arrhenius equation is $k=A e^{-E_a/RT}$. $A$ is the frequency (pre-exponential) factor, related "
            "to collision frequency and orientation. The exponential is the fraction of collisions with enough "
            "energy. You will not differentiate this on AP Chemistry; you will read it.",
            "As $T$ increases, $E_a/RT$ shrinks, the exponential grows toward 1, and $k$ increases. As $E_a$ "
            "increases, the exponential shrinks and $k$ decreases. That is the same story as collision theory.",
            "Taking the natural log: $\\ln k=\\ln A - (E_a/R)(1/T)$. A plot of $\\ln k$ versus $1/T$ is a straight "
            "line with slope $-E_a/R$ and intercept $\\ln A$. A steeper negative slope means a larger $E_a$: "
            "that reaction's rate is more sensitive to temperature.",
            "Compare two lines on the same axes. The one that falls more steeply as $1/T$ increases (colder) "
            "has the larger barrier. At extremely high $T$, $1/T\\rightarrow 0$ and $\\ln k\\rightarrow \\ln A$, "
            "so similar $A$ values mean similar $k$ far to the left of a $1/T$ plot.",
            "A catalyst lowers $E_a$, which makes the Arrhenius slope shallower (less steep) and raises $k$ at "
            "every finite $T$. That is a quantitative restatement of the energy-diagram picture.",
            "When an item gives two $k$ values at two temperatures, you could in principle find $E_a$, but AP "
            "often asks only which reaction is more temperature-sensitive or what the slope means. Answer with "
            "$-E_a/R$ and “larger $E_a$.”",
        ],
        "Arrhenius is the algebra of collision theory. The slope of $\\ln k$ vs $1/T$ is the one graph you "
        "must not mix up with a kinetics concentration plot.",
        "Write $\\ln k=\\ln A-(E_a/R)(1/T)$. Identify slope as $-E_a/R$. Steeper magnitude → larger $E_a$ → "
        "stronger $T$ dependence.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#b45309", [(0.0015, 2.4), (0.0035, -1.6)]),
                    ("#1d4ed8", [(0.0015, 2.2), (0.0035, 0.2)]),
                ],
                xlim=(0.0012, 0.0038), ylim=(-2.2, 3.0), xlab="1/T", ylab="ln k", w=340, h=240,
            ),
            "$\\ln k$ versus $1/T$ for two reactions (same $A$ idea)",
            "The steeper brown line has the larger $E_a$. The shallower blue line is less temperature-sensitive "
            "(a catalyzed path looks like this compared with its uncatalyzed twin).",
        )
        + solved(16, "What is the slope of a graph of $\\ln k$ vs $1/T$?",
               ["Arrhenius in log form: $\\ln k=\\ln A-(E_a/R)(1/T)$.",
                "This is $y=b+mx$ with $x=1/T$.",
                "Slope $= -E_a/R$."],
               "$-E_a/R$", "", "Easy")
        + solved(17, "Reaction X has a steeper negative slope than Y on $\\ln k$ vs $1/T$. Which has larger $E_a$?",
                 ["$|\\mathrm{slope}|=E_a/R$.",
                  "Larger slope magnitude means larger $E_a$.",
                  "X has the larger activation energy.",
                  "X's rate will change more when $T$ changes."],
                 "X", "", "Medium")
        + solved(18, "Why does a catalyst make the $\\ln k$ vs $1/T$ plot less steep?",
                 ["A catalyst lowers $E_a$.",
                  "Slope is $-E_a/R$, so a smaller $E_a$ means a smaller-magnitude slope.",
                  "The line is shallower: $k$ still depends on $T$, but more weakly.",
                  "The intercept $\\ln A$ may also change if the new path has a different orientation factor."],
                 "smaller $E_a$ → shallower slope", "", "Hard"),
        ("Plotting $\\ln k$ vs $T$ and calling the slope $-E_a/R$",
         "The $x$-axis must be $1/T$, not $T$. A graph versus $T$ is curved. Read the axis labels."),
        ("State slope $= -E_a/R$ before comparing two lines",
         "Once that equation is on the page, “steeper means larger $E_a$” is a one-line conclusion."),
        [
            "I can write $\\ln k=\\ln A-(E_a/R)(1/T)$ and name the slope.",
            "I can compare $E_a$ values from the steepness of Arrhenius plots.",
            "I can explain why $k$ increases with $T$ using the exponential factor.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        ["Rate laws from data", "Integrated rate laws", "Collision theory",
         "Reaction mechanisms", "Catalysts", "Arrhenius qualitative"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6
# ===========================================================================

def _u6_questions():
    return _qs([
        ("Calorimetry measures heat using $q=mc\\Delta T$. For 50.0 g water, $c=4.18$ J/g·°C, $\\Delta T=10.0$°C, $q$ is:",
         "2090 J", "50.0×4.18×10.0=2090 J.",
         ["4.18 J", "500 J", "209 J"]),
        ("If a reaction releases 2090 J into 100.0 g water ($c=4.18$), $\\Delta T$ of the water is:",
         "5.00°C", "ΔT=q/(mc)=2090/(100.0×4.18)=5.00.",
         ["20.9°C", "2.09°C", "418°C"]),
        ("The sign of $q$ for the water when an exothermic reaction runs in a coffee-cup calorimeter is:",
         "positive for the water (the surroundings), negative for the reaction (the system)",
         "Heat leaving the reaction enters the water.",
         ["positive for both", "negative for both", "zero for the water"]),
        ("100.0 g water warms from 22.00°C to 27.00°C ($c=4.18$). Heat absorbed by water?",
         "2090 J", "ΔT=5.00; q=100.0×4.18×5.00=2090 J.",
         ["418 J", "22 J", "4.18×22 J"]),
        ("A metal sample of 20.0 g and $c=0.900$ J/g·°C cools by 10.0°C. $|q|$ for the metal is:",
         "180 J", "20.0×0.900×10.0=180.",
         ["9.00 J", "200 J", "0.900 J"]),
        ("Enthalpy $H$ is a state function, so Hess's law says:",
         "ΔH for a net path equals the sum of ΔH for any steps that add to that path",
         "You may reverse a step (flip the sign of ΔH) or multiply a step (multiply ΔH).",
         ["ΔH depends on how fast you go", "ΔH is always positive", "you cannot reverse a thermochemical equation"]),
        ("C+O₂→CO₂ ΔH=−394 kJ and CO+½O₂→CO₂ ΔH=−283 kJ. ΔH for C+½O₂→CO is:",
         "−111 kJ", "−394−(−283)=−111 kJ.",
         ["−677 kJ", "+111 kJ", "−283 kJ"]),
        ("If a reaction is reversed, ΔH:",
         "changes sign", "Endothermic and exothermic swap.",
         ["is squared", "is unchanged", "becomes zero"]),
        ("Bond enthalpies estimate ΔH as:",
         "energy in (bonds broken) minus energy out (bonds formed), using average bond energies",
         "Breaking is endothermic; forming is exothermic.",
         ["only products' bond energies", "q=mcΔT of the bonds", "K of the reaction"]),
        ("An exothermic reaction has:",
         "ΔH<0; products lower in enthalpy than reactants",
         "The system releases heat.",
         ["ΔH>0 always", "ΔH=0", "ΔS must be negative"]),
        ("Entropy $S$ measures:",
         "how many ways energy can be arranged in a sample (dispersal of energy / disorder of microstates)",
         "Gases have much larger S than liquids or solids of the same substance.",
         ["the heat of a bomb calorimeter only", "nuclear charge", "the value of k"]),
        ("2H₂O(l)→2H₂(g)+O₂(g) has ΔS that is:",
         "positive (more moles of gas)",
         "Three moles of gas from a liquid.",
         ["negative", "zero", "undefined for redox"]),
        ("N₂(g)+3H₂(g)→2NH₃(g) has ΔS that is:",
         "negative (4 mol gas → 2 mol gas)",
         "Fewer gas particles, less entropy.",
         ["positive", "zero because all are gases", "equal to ΔH"]),
        ("Which has the largest molar entropy at 25°C among H₂O(s), H₂O(l), H₂O(g)?",
         "H₂O(g)", "Gas particles occupy many more microstates.",
         ["H₂O(s)", "H₂O(l)", "all identical"]),
        ("Dissolving a solid into ions in water often increases S because:",
         "particles are freer to move in solution than in a crystal",
         "There are exceptions when water becomes highly ordered around ions.",
         ["the solid gains mass", "temperature must fall", "ΔH is always negative"]),
        ("Gibbs free energy is $ΔG=ΔH-TΔS$ (T in kelvin). A process is thermodynamically favored when:",
         "ΔG<0", "Negative ΔG means the process can go forward as written (under the stated conditions).",
         ["ΔG>0", "ΔG=ΔH always", "ΔS<0 always"]),
        ("ΔH=+40.0 kJ and ΔS=+100. J/K. At T=400 K, ΔG is:",
         "0", "TΔS=400×0.100 kJ/K=40.0 kJ; ΔG=40.0−40.0=0.",
         ["+40 kJ", "−40 kJ", "+80 kJ"]),
        ("For that same ΔH and ΔS, the reaction is product-favored at:",
         "T>400 K (high T, because −TΔS becomes more negative)",
         "Endothermic but +ΔS: entropy-driven at high T.",
         ["all T", "no T", "only T=0 K"]),
        ("If ΔH<0 and ΔS>0, ΔG is:",
         "negative at all T (favored everywhere)",
         "Both terms help.",
         ["positive at all T", "negative only at low T", "zero always"]),
        ("If ΔH>0 and ΔS<0, the process is:",
         "not thermodynamically favored at any T (ΔG>0)",
         "Both terms oppose.",
         ["favored at high T", "favored at low T", "favored at 400 K only"]),
        ("The link between ΔG° and K is that:",
         "ΔG°<0 corresponds to K>1 (products favored at equilibrium)",
         "Qualitative: a downhill standard process has a large product-heavy K.",
         ["ΔG°<0 means K=0", "K is k, the rate constant", "ΔG° equals Ea"]),
        ("If K is much greater than 1, ΔG° is:",
         "negative", "Equilibrium lies toward products.",
         ["positive", "exactly zero always", "equal to T"]),
        ("If Q=K, then ΔG is:",
         "0 (at equilibrium)",
         "No net driving force.",
         ["equal to ΔG° always", "equal to Ea", "infinite"]),
        ("A catalyst changes:",
         "rate (Ea) but not ΔG° or K at that T",
         "Thermodynamics of the states is unchanged.",
         ["ΔG° to a new value", "K to match the new rate law", "ΔH of formation of the elements"]),
        ("Raising T for an exothermic reaction (ΔH<0) makes K:",
         "smaller (Le Chatelier / van't Hoff qualitative)",
         "Heat is like a product; K shifts toward reactants.",
         ["larger always", "unchanged always", "equal to k"]),
        ("On an energy diagram, Ea is:",
         "the energy difference from reactants up to the transition-state peak",
         "ΔH is reactants to products, not to the peak.",
         ["the same as ΔH", "always equal to ΔG", "the heat absorbed by the calorimeter water only"]),
        ("An endothermic diagram has products:",
         "higher in energy than reactants",
         "ΔH>0.",
         ["lower than reactants", "at the peak", "at E=0 always"]),
        ("The activated complex / transition state is:",
         "the highest-energy arrangement along the reaction coordinate",
         "It is not a stable intermediate you can bottle.",
         ["the catalyst", "the calorimeter", "the salt bridge"]),
        ("A larger Ea (uncatalyzed vs catalyzed) means:",
         "a slower rate, not a different ΔH",
         "Peak height is kinetics; end-to-end drop is thermo.",
         ["a more negative ΔH", "K must be larger", "ΔS must be negative"]),
        ("For a two-step mechanism, the observed Ea is associated mainly with:",
         "the highest peak (rate-determining climb)",
         "The difficult step dominates the temperature sensitivity.",
         ["the average of all bond energies in the products only", "ΔG°", "q of the water"]),
        ("q=mcΔT for 25.0 g water, c=4.18, ΔT=8.00°C is:",
         "836 J", "25.0×4.18×8.00=836.",
         ["4.18 J", "200 J", "8360 J"]),
        ("Hess: if A→B ΔH=+20 and B→C ΔH=−50, A→C has ΔH:",
         "−30", "20+(−50)=−30.",
         ["+70", "−50", "+20"]),
        ("Which process has ΔS>0?",
         "Br₂(l)→Br₂(g)", "Vaporization increases entropy.",
         ["H₂O(g)→H₂O(l)", "N₂+3H₂→2NH₃", "2 Na(s)+Cl₂(g)→2NaCl(s) if gas is consumed"]),
        ("At 300 K, ΔH=−30.0 kJ, ΔS=−50.0 J/K. ΔG is:",
         "−15.0 kJ", "TΔS=300×(−0.0500)=−15.0 kJ; ΔG=−30.0−(−15.0)=−15.0 kJ.",
         ["−45 kJ", "+15 kJ", "−30 kJ"]),
        ("A reaction with ΔG°=0 has K:",
         "equal to 1", "Neither side is favored in the standard-state equilibrium sense.",
         ["0", "infinite", "equal to 0.059"]),
        ("Coffee-cup calorimetry is typically at constant:",
         "pressure, so q_p = ΔH for the process in the cup",
         "Open to the atmosphere.",
         ["volume only, so q_v=ΔU exclusively as the AP label", "volume of the universe", "magnetic field"]),
        ("If 0.0500 mol of a reaction releases 2090 J, ΔH per mole is:",
         "−41.8 kJ/mol", "q_rxn=−2090 J=−2.090 kJ; per mol −2.090/0.0500=−41.8 kJ/mol.",
         ["+41.8 kJ/mol", "−2090 kJ/mol", "−2.09 kJ/mol"]),
        ("Why is ΔS for dissolving a gas in water usually negative?",
         "gas particles lose freedom when they enter the liquid solution",
         "Gases have high S.",
         ["gases have zero entropy", "water freezes", "ΔH must be positive"]),
        ("The temperature at which ΔG=0 for ΔH=40.0 kJ, ΔS=100. J/K is:",
         "400 K", "T=ΔH/ΔS=40000 J / 100 J/K=400 K.",
         ["0.400 K", "40 K", "100 K"]),
        ("Products lower than reactants on an energy diagram means the reaction is:",
         "exothermic (ΔH<0)",
         "The system lost enthalpy.",
         ["endothermic", "ΔG>0 always", "Ea=0"]),
        ("If ΔG<0 but the reaction is extremely slow, the missing piece is:",
         "kinetics (large Ea)",
         "Thermodynamics says “allowed”; kinetics says “when.”",
         ["ΔG is actually positive", "K=0", "the calorimeter is broken always"]),
        ("Doubling all coefficients of a thermochemical equation:",
         "doubles ΔH", "ΔH is extensive in that sense.",
         ["does not change ΔH", "squares ΔH", "flips the sign only"]),
        ("S° of a perfect crystal at 0 K is taken as:",
         "0 (third-law idea)",
         "Absolute entropies are then positive at T>0.",
         ["equal to ΔH_f°", "infinite", "equal to R"]),
        ("A spontaneous process in an isolated system increases:",
         "the entropy of the universe (ΔS_univ>0)",
         "That is the second-law statement used in AP language.",
         ["only ΔH of the system", "Ea", "the value of n in PV=nRT always"]),
        ("If Q>K, ΔG is:",
         "positive (net reverse is favored)",
         "Too much product relative to equilibrium.",
         ["zero", "equal to ΔG°", "negative always"]),
        ("The difference between Ea forward and Ea reverse equals:",
         "ΔH (for the one-step diagram)",
         "Peak minus reactants vs peak minus products.",
         ["K", "T", "q of the water"]),
        ("AP Stretch: 75.0 g water ($c=4.18$) warms 6.40°C when 0.0200 mol of a salt dissolves. Find q_water and ΔH_soln in kJ/mol (assume all heat from the dissolving process).",
         "q_water=+2006 J; ΔH_soln=−100. kJ/mol",
         "q_w=75.0×4.18×6.40=2006 J. q_soln=−2.006 kJ; per mol −2.006/0.0200=−100. kJ/mol (exothermic dissolving).",
         ["q_water=−2006 J; ΔH=+100 kJ/mol", "ΔH=−2.01 kJ/mol", "q=4.18 J; ΔH=0"]),
        ("AP Stretch: Use Hess: 2S+3O₂→2SO₃ ΔH=−792 kJ and 2SO₂+O₂→2SO₃ ΔH=−196 kJ. Find ΔH for S+O₂→SO₂.",
         "−298 kJ",
         "Target is half of (first minus second): [−792−(−196)]/2=−596/2=−298 kJ.",
         ["−396 kJ", "−196 kJ", "+298 kJ"]),
        ("AP Stretch: ΔH=+80.0 kJ, ΔS=+200. J/K. Is the reaction favored at 300 K? At 500 K? Compute both ΔG values.",
         "not favored at 300 K (ΔG=+20.0 kJ); favored at 500 K (ΔG=−20.0 kJ)",
         "300 K: TΔS=60.0 kJ, ΔG=80−60=+20. 500 K: TΔS=100 kJ, ΔG=80−100=−20.",
         ["favored at both", "favored at neither", "ΔG=0 at both"]),
        ("AP Stretch: Explain why a reaction can have ΔG°<0 (K>1) and still produce almost no product in a minute of lab time.",
         "Large Ea / slow rate; thermodynamics is not a clock",
         "Diamond→graphite is the classic comparison: favored but slow.",
         ["K>1 means the rate constant k is large", "ΔG° equals speed", "the calorimeter absorbs all product"]),
        ("AP Stretch: For N₂+3H₂→2NH₃, ΔH<0. Predict the signs of ΔS and of ΔG at very high T, and whether K is larger at low T or high T.",
         "ΔS<0; at high T ΔG becomes positive; K is larger at low T",
         "Fewer gas moles ⇒ ΔS<0. −TΔS is positive and grows. Exothermic ⇒ K decreases as T rises.",
         ["ΔS>0; K larger at high T", "ΔS=0; K independent of T", "ΔG always more negative at high T"]),
        ("AP Stretch: A 1.00 g sample of CH₄ (16.0 g/mol) is burned; q_cal=−50.0 kJ (heat into calorimeter is +50.0 kJ). ΔH_comb per mole?",
         "−800. kJ/mol", "n=1.00/16.0=0.0625 mol; ΔH=−50.0/0.0625=−800 kJ/mol.",
         ["−50.0 kJ/mol", "−16.0 kJ/mol", "+800 kJ/mol"]),
        ("AP Stretch: Sketch in words an endothermic catalyzed vs uncatalyzed diagram. What is identical and what changes?",
         "identical reactant/product energies (same ΔH); both peaks lower on the catalyzed path",
         "Kinetics change; thermo of states does not.",
         ["products drop below reactants when catalyzed", "Ea becomes ΔG", "ΔH flips sign"]),
        ("AP Stretch: ΔG=ΔG°+RT ln Q. If Q is made much smaller than K by removing product, ΔG becomes:",
         "more negative (forward drive increases)",
         "ln Q decreases; the added term is more negative.",
         ["zero always", "equal to Ea", "positive and larger"]),
        ("AP Stretch: Two steps: A→I Ea=25 kJ, I→B Ea=50 kJ, A is 0, I is +15, B is +45 (kJ). Overall ΔH and which step is rate-determining?",
         "ΔH=+45 kJ; second step (peak 65 kJ above A vs first peak 25)",
         "Overall A to B is +45. First peak sits at 25 kJ. Second peak sits at 15+50=65 kJ, so the second climb is the RDS.",
         ["ΔH=−30 kJ; first step (old 40/10 diagram)", "ΔH=+15; first step", "ΔH=+45; first step because A→I is earlier"]),
    ])


def build_unit6():
    title = "AP Chemistry Unit 6: Thermodynamics"
    description = (
        "Calorimetry, Hess's law, entropy, Gibbs free energy, the thermo–equilibrium link, and energy "
        "diagrams with catalyzed versus uncatalyzed paths."
    )
    c1 = concept_block(
        "1. Calorimetry",
        [
            "Calorimetry measures heat by watching a temperature change in a known substance, usually water. "
            "The working equation is $q=mc\\Delta T$, where $m$ is mass, $c$ is specific heat capacity, and "
            "$\\Delta T=T_\\mathrm{final}-T_\\mathrm{initial}$. For liquid water, $c=4.18\\,\\mathrm{J\\,g^{-1}\\,^\\circ C^{-1}}$ "
            "is the AP workhorse value.",
            "Numeric: $50.0$ g of water warms by $10.0^\\circ$C. $q=(50.0)(4.18)(10.0)=2090$ J. Same energy with "
            "$100.0$ g and $\\Delta T=5.00^\\circ$C: $(100.0)(4.18)(5.00)=2090$ J. The water absorbed $2090$ J.",
            "In a coffee-cup (constant-pressure) calorimeter, the heat absorbed by the water is the opposite of "
            "the heat of the chemical process in the cup (if we neglect the cup itself): $q_\\mathrm{rxn}=-q_\\mathrm{water}$. "
            "An exothermic reaction makes the water warmer; $q_\\mathrm{water}>0$ and $q_\\mathrm{rxn}<0$.",
            "Molar enthalpy from a calorimeter: divide $q_\\mathrm{rxn}$ by moles of reaction. If $0.0500$ mol "
            "releases $2090$ J, $\\Delta H=-2.090\\,\\mathrm{kJ}/0.0500\\,\\mathrm{mol}=-41.8$ kJ/mol. Watch joules "
            "versus kilojoules.",
            "Metals have smaller $c$ than water. $20.0$ g of a metal with $c=0.900$ cooling by $10.0^\\circ$C "
            "releases only $180$ J — the same $\\Delta T$ in water would move much more energy because water's $c$ "
            "is large. That is why water is a good calorimeter fluid.",
            "Sign and system/surroundings language is scored carefully. The reaction is the system; the water is "
            "surroundings. Heat that leaves the system enters the water.",
        ],
        "Every later $\\Delta H$ you use in Hess's law or $\\Delta G=\\Delta H-T\\Delta S$ is a number that "
        "ultimately came from a calorimeter or from tabulated calorimetry.",
        "Write $q=mc\\Delta T$ for the water, assign the opposite sign to the reaction, then divide by moles "
        "if a molar $\\Delta H$ is asked. Convert J to kJ at the end.",
        lesson_figure(
            beaker_svg("calorimeter water, ΔT"),
            "A coffee-cup calorimeter is a beaker of water with a thermometer",
            "The chemistry happens in (or in contact with) the water. The water's temperature change is the meter "
            "for q. Styrofoam cups reduce heat leaks so the simple q=mcΔT model is closer to true.",
        )
        + solved(1, "$50.0$ g water, $c=4.18$, $\\Delta T=10.0^\\circ$C. Find $q$.",
               ["$q=mc\\Delta T$.",
                "$q=(50.0)(4.18)(10.0)$.",
                "$q=2090$ J."],
               "$2090$ J", "", "Easy")
        + solved(2, "A reaction releases $2090$ J into $100.0$ g water ($c=4.18$). Find $\\Delta T$ of the water.",
                 ["The water absorbs $2090$ J.",
                  "$\\Delta T=q/(mc)=2090/(100.0\\times 4.18)$.",
                  "$100.0\\times 4.18=418$, so $\\Delta T=5.00^\\circ$C."],
                 "$5.00^\\circ$C", "", "Medium")
        + solved(3, "$0.0500$ mol of reaction warms $100.0$ g water by $5.00^\\circ$C. Find $\\Delta H$ in kJ/mol.",
                 ["$q_\\mathrm{water}=(100.0)(4.18)(5.00)=2090$ J $=2.090$ kJ.",
                  "$q_\\mathrm{rxn}=-2.090$ kJ (exothermic).",
                  "$\\Delta H=q_\\mathrm{rxn}/n=-2.090/0.0500=-41.8$ kJ/mol.",
                  "The negative sign is required because the reaction released the heat."],
                 "$-41.8$ kJ/mol", "", "Hard"),
        ("Giving $q_\\mathrm{rxn}$ the same sign as the water's temperature rise",
         "If the water got hotter, the reaction lost heat. $q_\\mathrm{water}>0$ implies $q_\\mathrm{rxn}<0$."),
        ("Keep $q$ in a box, then convert to kJ, then divide by moles",
         "Mixing J and mol in one line is how $-41.8$ becomes $-41800$ or $-0.0418$. Three lines prevent that."),
        [
            "I can compute $q=mc\\Delta T$ for water.",
            "I can assign opposite signs to $q_\\mathrm{rxn}$ and $q_\\mathrm{water}$.",
            "I can convert calorimeter heat into a molar $\\Delta H$.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Enthalpy and Hess's law",
        [
            "Enthalpy change $\\Delta H$ is the heat at constant pressure for a process. It is a state function: "
            "it depends on the starting and ending states, not on the path. Hess's law follows immediately: if "
            "equations add to a target, their $\\Delta H$ values add to the target $\\Delta H$.",
            "You may reverse an equation if you flip the sign of $\\Delta H$, and you may multiply an equation "
            "if you multiply $\\Delta H$ by the same factor. Those are the only two legal moves, plus addition.",
            "Worked Hess: $\\mathrm{C+O_2\\rightarrow CO_2}$ $\\Delta H=-394$ kJ and "
            "$\\mathrm{CO+\\tfrac12 O_2\\rightarrow CO_2}$ $\\Delta H=-283$ kJ. Target $\\mathrm{C+\\tfrac12 O_2\\rightarrow CO}$. "
            "Keep the first equation; reverse the second ($+283$ kJ). Add: carbon in, CO out, $\\Delta H=-394+283=-111$ kJ.",
            "Formation enthalpies: $\\Delta H^\\circ_\\mathrm{rxn}=\\sum n\\Delta H_f^\\circ(\\mathrm{products})-"
            "\\sum n\\Delta H_f^\\circ(\\mathrm{reactants})$. Elements in standard states have $\\Delta H_f^\\circ=0$.",
            "Bond enthalpies are averages, so they estimate $\\Delta H$ as bonds broken minus bonds formed. They "
            "are less accurate than Hess with formation data, but they explain why making strong bonds (O=O vs "
            "weak O–O) releases more heat.",
            "Exothermic: $\\Delta H<0$, products below reactants on an enthalpy diagram. Endothermic: $\\Delta H>0$, "
            "products above. The peak above the reactants is $E_a$, a kinetics number, not $\\Delta H$.",
        ],
        "Hess's law is how you get $\\Delta H$ for a reaction you cannot run cleanly in a calorimeter. It is "
        "also the arithmetic inside every $\\Delta G=\\Delta H-T\\Delta S$ estimate.",
        "Write the target. Flip and scale the given equations until species cancel to that target. Add the "
        "$\\Delta H$ values with the same flips and scales.",
        lesson_figure(
            energy_diagram_svg(label="exothermic, ΔH<0"),
            "Enthalpy diagram for an exothermic reaction",
            "Products sit below reactants. ΔH is the end-to-end drop. Ea is the climb to the peak — a different "
            "quantity from Unit 5.",
        )
        + solved(4, "A reaction is reversed. What happens to $\\Delta H$?",
               ["Heat that was released would now have to be absorbed (or the reverse).",
                "The sign of $\\Delta H$ flips.",
                "The magnitude stays the same."],
               "sign of $\\Delta H$ flips", "", "Easy")
        + solved(5, "A→B $\\Delta H=+20$ kJ and B→C $\\Delta H=-50$ kJ. Find $\\Delta H$ for A→C.",
                 ["Hess: add the steps.",
                  "$+20+(-50)=-30$ kJ.",
                  "A→C is exothermic overall."],
                 "$-30$ kJ", "", "Medium")
        + solved(6, "Using $\\Delta H=-394$ kJ for C→CO₂ and $-283$ kJ for CO→CO₂ (each with the matching O₂), find $\\Delta H$ for C→CO.",
                 ["Keep C+O₂→CO₂ ($-394$).",
                  "Reverse CO+½O₂→CO₂ to get CO₂→CO+½O₂ ($+283$).",
                  "Add: C+½O₂→CO.",
                  "$\\Delta H=-394+283=-111$ kJ."],
                 "$-111$ kJ", "", "Hard"),
        ("Adding equations but forgetting to reverse $\\Delta H$ when you reverse the equation",
         "The species will look right and the number will have the wrong sign — a silent Hess error. Flip the "
         "sign in the same breath as you flip the arrow."),
        ("Write the target equation first and cancel species with a pencil",
         "If CO₂ does not cancel and you needed it to cancel, you used a step the wrong way. The algebra of "
         "formulas checks the algebra of $\\Delta H$."),
        [
            "I can reverse and scale thermochemical equations.",
            "I can add $\\Delta H$ values by Hess's law.",
            "I can distinguish $\\Delta H$ from $E_a$ on a diagram.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Entropy",
        [
            "Entropy $S$ measures how energy is dispersed among the microstates of a sample — often described "
            "as molecular freedom or “disorder,” if you are careful. A gas has a much larger molar entropy than "
            "the liquid or solid of the same substance because the particles explore a huge volume of positions "
            "and momenta.",
            "Phase ranking at a given $T$: $S^\\circ(\\mathrm{g})\\gg S^\\circ(\\mathrm{l})>S^\\circ(\\mathrm{s})$. "
            "Vaporization and sublimation have $\\Delta S>0$. Freezing and condensation have $\\Delta S<0$.",
            "For chemical reactions, count moles of gas. $\\mathrm{N_2+3H_2\\rightarrow 2NH_3}$ goes from $4$ mol "
            "gas to $2$ mol gas: $\\Delta S<0$. $2\\,\\mathrm{H_2O(l)\\rightarrow 2H_2(g)+O_2(g)}$ makes gas from "
            "liquid: $\\Delta S>0$. Mixing and dissolving often increase $S$, with exceptions for some ions that "
            "order water strongly.",
            "The second law: for any real spontaneous process, $\\Delta S_\\mathrm{universe}>0$. The system can "
            "lose entropy if the surroundings gain more (an exothermic reaction heating the lab).",
            "The third-law idea: a perfect crystal at $0$ K has $S=0$, so tabulated $S^\\circ$ values are absolute "
            "and positive at $25^\\circ$C. $\\Delta S^\\circ_\\mathrm{rxn}=\\sum nS^\\circ(\\mathrm{products})-"
            "\\sum nS^\\circ(\\mathrm{reactants})$.",
            "You do not need a statistical-mechanics derivation. You need to predict the sign of $\\Delta S$ from "
            "phases and gas moles, and to use that sign in $\\Delta G=\\Delta H-T\\Delta S$.",
        ],
        "Entropy is the $T\\Delta S$ term that decides whether an endothermic process can be favored at high "
        "temperature. Without a sign for $\\Delta S$, Gibbs is incomplete.",
        "Ask: did moles of gas increase? Did a condensed phase become gas? If yes, $\\Delta S>0$. Then keep "
        "that sign for the Gibbs discussion.",
        lesson_figure(
            _phases_svg(),
            "Entropy from arrangement, not from an energy peak",
            "The gas has far more microstates (positions and speeds) than the liquid. That is why S°(g) ≫ S°(l) "
            "and why vaporization has ΔS>0. Do not read entropy from an Ea hump.",
        )
        + solved(7, "Which has larger molar entropy: H₂O(l) or H₂O(g) at the same $T$?",
               ["Gas particles occupy much more volume and have more accessible microstates.",
                "Molar entropy of steam is much larger than that of liquid water.",
                "Vaporization has $\\Delta S>0$."],
               "H₂O(g)", "", "Easy")
        + solved(8, "Sign of $\\Delta S$ for $\\mathrm{N_2(g)+3H_2(g)\\rightarrow 2NH_3(g)}$?",
                 ["Reactants: $1+3=4$ mol gas.",
                  "Products: $2$ mol gas.",
                  "Fewer gas moles: $\\Delta S<0$."],
                 "$\\Delta S<0$", "", "Medium")
        + solved(9, "Sign of $\\Delta S$ for $2\\,\\mathrm{H_2O(l)\\rightarrow 2H_2(g)+O_2(g)}$?",
                 ["A liquid becomes three moles of gas.",
                  "Gases have large entropy compared with liquids.",
                  "$\\Delta S>0$, and it is a large positive value.",
                  "This is why electrolysis of water is entropy-favored even though it is endothermic."],
                 "$\\Delta S>0$", "", "Hard"),
        ("Assigning $\\Delta S>0$ whenever a reaction is “messy” or redox",
         "Count gas moles and phases. $2\\,\\mathrm{H_2+O_2\\rightarrow 2H_2O(l)}$ is redox and has $\\Delta S<0$."),
        ("Write mol gas, reactants vs products, as a one-line table",
         "If the gas-mole count drops, $\\Delta S$ is almost certainly negative. That line earns the FRQ point."),
        [
            "I can rank $S$ of solid, liquid, and gas.",
            "I can predict the sign of $\\Delta S$ from moles of gas.",
            "I can state that $\\Delta S_\\mathrm{univ}>0$ for a spontaneous process.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Gibbs free energy",
        [
            "Gibbs free energy change is $\\Delta G=\\Delta H-T\\Delta S$ with $T$ in kelvin and $\\Delta S$ "
            "converted so the units match (usually kJ). If $\\Delta G<0$, the process is thermodynamically "
            "favored (product-favored as written under those conditions). If $\\Delta G>0$, the reverse is "
            "favored. If $\\Delta G=0$, the system is at equilibrium.",
            "Worked: $\\Delta H=+40.0$ kJ, $\\Delta S=+100.\\,\\mathrm{J/K}=0.100$ kJ/K, $T=400$ K. "
            "$T\\Delta S=400\\times 0.100=40.0$ kJ. $\\Delta G=40.0-40.0=0$. That temperature is the boundary: "
            "above $400$ K the $-T\\Delta S$ term wins and $\\Delta G<0$.",
            "Four cases: $\\Delta H<0$, $\\Delta S>0$: favored at all $T$. $\\Delta H>0$, $\\Delta S<0$: never "
            "favored. $\\Delta H<0$, $\\Delta S<0$: favored at low $T$ (enthalpy-driven). $\\Delta H>0$, $\\Delta S>0$: "
            "favored at high $T$ (entropy-driven).",
            "Another numeric: $\\Delta H=-30.0$ kJ, $\\Delta S=-50.0$ J/K, $T=300$ K. $T\\Delta S=300\\times(-0.0500)=-15.0$ kJ. "
            "$\\Delta G=-30.0-(-15.0)=-15.0$ kJ still negative — low $T$ enough for this enthalpy-driven case.",
            "$\\Delta G$ is not a speed. A reaction can have $\\Delta G<0$ and still be immeasurably slow if $E_a$ "
            "is huge (diamond to graphite). Kinetics and thermodynamics answer different questions.",
            "Standard $\\Delta G^\\circ$ uses standard states (1 M, 1 bar, etc.). Nonstandard $\\Delta G$ also "
            "depends on $Q$: qualitatively, removing product makes $\\Delta G$ more negative (Unit 7 connection).",
        ],
        "Gibbs is the decision equation of AP thermodynamics: favored or not, at what temperatures, and how "
        "that connects to $K$.",
        "Convert $\\Delta S$ to kJ/K. Compute $T\\Delta S$. Subtract from $\\Delta H$. Interpret the sign, then "
        "name the temperature regime using the four-case table.",
        lesson_figure(
            _energy_endo(),
            "Endothermic does not automatically mean “not favored”",
            "If ΔS is positive, −TΔS can overpower a positive ΔH at high T. The energy diagram shows ΔH>0; "
            "it does not by itself give ΔG.",
        )
        + solved(10, "$\\Delta H=+40.0$ kJ, $\\Delta S=+0.100$ kJ/K, $T=400$ K. Find $\\Delta G$.",
               ["$T\\Delta S=(400)(0.100)=40.0$ kJ.",
                "$\\Delta G=40.0-40.0=0$.",
                "The process is at the equilibrium temperature for these $\\Delta H$ and $\\Delta S$."],
               "$0$", "", "Easy")
        + solved(11, "For those same $\\Delta H$ and $\\Delta S$, is the reaction favored at $500$ K?",
                 ["$T\\Delta S=(500)(0.100)=50.0$ kJ.",
                  "$\\Delta G=40.0-50.0=-10.0$ kJ.",
                  "Negative $\\Delta G$: favored at $500$ K.",
                  "High $T$ helps because $\\Delta S>0$."],
                 "yes; $\\Delta G=-10.0$ kJ", "", "Medium")
        + solved(12, "$\\Delta H=-30.0$ kJ, $\\Delta S=-50.0$ J/K, $T=300$ K. Find $\\Delta G$.",
                 ["$\\Delta S=-0.0500$ kJ/K.",
                  "$T\\Delta S=300\\times(-0.0500)=-15.0$ kJ.",
                  "$\\Delta G=-30.0-(-15.0)=-15.0$ kJ.",
                  "Still favored; this is the low-$T$ enthalpy-driven window."],
                 "$-15.0$ kJ", "If $T$ were much higher, $-T\\Delta S$ would turn $\\Delta G$ positive.", "Hard"),
        ("Forgetting to convert J/K to kJ/K",
         "$\\Delta H$ in kJ minus $T$ times $100$ J/K looks like $40-40000$ if you skip the conversion. Divide "
         "$\\Delta S$ by $1000$ first."),
        ("Compute $T=\\Delta H/\\Delta S$ as the boundary when both are nonzero",
         "That temperature (with consistent units) is where $\\Delta G=0$. Then you immediately know which side "
         "is “high $T$” and which is “low $T$.”"),
        [
            "I can compute $\\Delta G=\\Delta H-T\\Delta S$ with matching units.",
            "I can use the four sign cases to name the temperature regime.",
            "I can explain that $\\Delta G$ is not a rate.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Thermo and equilibrium link",
        [
            "The standard free-energy change $\\Delta G^\\circ$ and the equilibrium constant $K$ describe the "
            "same landscape. Qualitatively: $\\Delta G^\\circ<0$ means $K>1$ (products favored at equilibrium). "
            "$\\Delta G^\\circ>0$ means $K<1$. $\\Delta G^\\circ=0$ means $K=1$.",
            "You do not need to compute $\\Delta G^\\circ=-RT\\ln K$ numerically on every item, but you must know "
            "that a large $K$ is a large negative $\\Delta G^\\circ$. $K$ is not the rate constant $k$.",
            "Away from standard states, $Q$ (the reaction quotient) matters. If $Q<K$, the forward process is "
            "still favored ($\\Delta G<0$). If $Q>K$, the reverse is favored. If $Q=K$, $\\Delta G=0$. Removing "
            "product shrinks $Q$ and makes the forward drive stronger.",
            "Temperature changes $K$ in the direction Le Chatelier predicts from $\\Delta H$. Exothermic "
            "($\\Delta H<0$): higher $T$ makes $K$ smaller. Endothermic: higher $T$ makes $K$ larger. A catalyst "
            "does not change $K$ or $\\Delta G^\\circ$.",
            "Ammonia synthesis is exothermic with $\\Delta S<0$. Low $T$ helps $K$ (more ammonia at equilibrium) "
            "but hurts rate. Industry uses a moderate $T$ plus a catalyst — a compromise between Units 5 and 6.",
            "When an FRQ asks whether a reaction is “thermodynamically favored” and “kinetically favored,” "
            "answer those as two separate sentences: $\\Delta G$ vs $E_a$.",
        ],
        "This paragraph is the bridge into Unit 7. If $K$ and $\\Delta G^\\circ$ feel like two different courses, "
        "the exam will punish that split.",
        "Map the signs: $\\Delta G^\\circ$ vs $1$, $Q$ vs $K$, $\\Delta H$ vs the way $K$ moves with $T$. Keep "
        "$k$ (rate) out of this map.",
        lesson_figure(
            _energy_cat(),
            "Same equilibrium (same ends), different rates (different peaks)",
            "A catalyst lowers Ea on the way to the same product energy. K, which compares the two ends, is "
            "unchanged. That is the thermo–kinetics split in one picture.",
        )
        + solved(13, "If $K\\gg 1$, what is the sign of $\\Delta G^\\circ$?",
               ["$K>1$ means products are favored at equilibrium.",
                "That corresponds to a downhill standard process.",
                "$\\Delta G^\\circ<0$."],
               "negative", "", "Easy")
        + solved(14, "If $Q=K$, what is $\\Delta G$?",
                 ["The reaction is at equilibrium.",
                  "There is no net driving force either way.",
                  "$\\Delta G=0$ (even if $\\Delta G^\\circ$ is not zero)."],
                 "$0$", "", "Medium")
        + solved(15, "Ammonia synthesis is exothermic. How does $K$ change if $T$ is raised, and why does industry still heat the reactor?",
                 ["$\\Delta H<0$: raising $T$ makes $K$ smaller (less NH₃ at equilibrium).",
                  "But $k$ (rate) increases with $T$ because more collisions clear $E_a$.",
                  "A catalyst lets a moderate $T$ be fast enough without destroying $K$ completely.",
                  "Thermo and kinetics pull in opposite ways; the plant is a compromise."],
                 "$K$ decreases; heat is for rate, plus a catalyst", "", "Hard"),
        ("Using $k$ and $K$ as if they were the same symbol",
         "Rate constant $k$ has units and depends on $E_a$ and $T$. Equilibrium constant $K$ is a ratio of "
         "amounts at equilibrium and tracks $\\Delta G^\\circ$. Mixing them is a content error, not a typo."),
        ("Answer “favored?” with $\\Delta G$, and “fast?” with $E_a$",
         "Two boxes on your scratch paper stop the most common thermo/kinetics mash-up on FRQs."),
        [
            "I can connect $\\Delta G^\\circ<0$ with $K>1$.",
            "I can interpret $Q$ versus $K$ as the sign of $\\Delta G$.",
            "I can predict how $T$ changes $K$ from the sign of $\\Delta H$.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Energy diagrams",
        [
            "An energy diagram plots potential energy versus a reaction coordinate (a cartoon of bond-breaking "
            "and bond-making progress). Reactants start on the left, products on the right, and a peak in "
            "between is the transition state. $E_a$ is the climb from reactants to that peak. $\\Delta H$ is "
            "the elevation change from reactants to products.",
            "Exothermic: products below reactants, $\\Delta H<0$. Endothermic: products above, $\\Delta H>0$. "
            "The reverse $E_a$ is the climb from products up to the same peak. For a one-step diagram, "
            "$E_a(\\mathrm{forward})-E_a(\\mathrm{reverse})=\\Delta H$.",
            "A catalyst draws a new curve with a lower peak and the same two ends. Two-step mechanisms can show "
            "two peaks; the higher climb is usually rate-determining. An intermediate sits in the valley between "
            "peaks — a real species, unlike the transition state at a peak.",
            "Do not put a calorimeter's water temperature on this diagram. $q=mc\\Delta T$ lives in the lab; "
            "the diagram lives in the molecule's energy landscape. They connect because the $\\Delta H$ on the "
            "diagram is what the calorimeter measures for a mole of reaction.",
            "When comparing catalyzed and uncatalyzed, trace both curves with a finger: same start, same finish, "
            "different mountain. That gesture is the FRQ answer.",
            "Labels that earn points: reactants, products, $E_a$, $\\Delta H$ (with a sign), transition state, "
            "optional intermediate, optional catalyzed path. An unlabeled hump is just a doodle.",
        ],
        "The energy diagram is the one figure that carries Units 5 and 6 at once. If you can label it, you can "
        "talk about rate and heat in the same sentence without mixing the symbols.",
        "Sketch two horizontal lines (reactants, products) and a peak. Mark $E_a$ up, $\\Delta H$ end-to-end. "
        "Add a lower dashed peak if a catalyst is mentioned.",
        lesson_figure(
            _energy_cat() + _energy_endo(),
            "Left: catalyzed vs not (same ΔH). Right: endothermic (products higher)",
            "Train your eye: peak height is kinetics; the two ends are thermodynamics. A catalyst never moves "
            "the ends in this model.",
        )
        + solved(16, "On a diagram, how is $E_a$ different from $\\Delta H$?",
               ["$E_a$ is reactants up to the transition-state peak.",
                "$\\Delta H$ is reactants to products, ignoring the peak.",
                "A reaction can have a large $E_a$ and a small (even negative) $\\Delta H$."],
               "$E_a$ to the peak; $\\Delta H$ end-to-end", "", "Easy")
        + solved(17, "Products are higher than reactants. Sign of $\\Delta H$? Relation to $E_a$ reverse vs forward?",
                 ["Products higher: $\\Delta H>0$ (endothermic).",
                  "The reverse climb (products to peak) is shorter than the forward climb.",
                  "So $E_a(\\mathrm{reverse})<E_a(\\mathrm{forward})$.",
                  "The reverse is faster than the forward at the same $T$ if that is the only difference — matching $K<1$ often."],
                 "$\\Delta H>0$; reverse barrier is smaller", "", "Medium")
        + solved(18, "A→I has $E_a=40$ kJ with I at $+20$ kJ relative to A; I→B has $E_a=10$ kJ and B at $-30$ kJ vs A. Overall $\\Delta H$ and RDS?",
                 ["Overall A to B: $\\Delta H=-30$ kJ.",
                  "First peak is $40$ kJ above A; second peak is $20+10=30$ kJ above A.",
                  "The higher peak relative to the preceding valley/start is the first step's $40$ kJ climb.",
                  "The first step is rate-determining."],
                 "$\\Delta H=-30$ kJ; first step RDS", "", "Hard"),
        ("Labeling the peak as $\\Delta H$",
         "The peak is the transition state. $\\Delta H$ does not care about the peak. Mislabeling costs the "
         "kinetics point and the thermo point at once."),
        ("Draw $E_a$ as a vertical arrow to the peak, $\\Delta H$ as a vertical arrow between the two ends",
         "Two arrows, two meanings. Graders look for both."),
        [
            "I can label $E_a$, $\\Delta H$, reactants, products, and a catalyst path.",
            "I can relate forward and reverse barriers to $\\Delta H$.",
            "I can identify a rate-determining peak on a two-step diagram.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        ["Calorimetry", "Enthalpy and Hess", "Entropy",
         "Gibbs free energy", "Thermo and equilibrium link", "Energy diagrams"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7
# ===========================================================================

def _u7_questions():
    return _qs([
        ("K is the equilibrium constant: a ratio of product and reactant amounts at equilibrium, each raised to its coefficient. Q is:",
         "the same ratio written with the current (not necessarily equilibrium) amounts",
         "Compare Q to K to predict the net direction.",
         ["the rate constant k", "always equal to 1", "ΔG°"]),
        ("If Q<K, the net reaction:",
         "shifts right (forms products) until Q rises to K",
         "Too little product relative to equilibrium.",
         ["shifts left", "is already at equilibrium", "stops forever"]),
        ("If Q>K, the net reaction:",
         "shifts left (forms reactants)",
         "Too much product.",
         ["shifts right", "K increases automatically", "ΔG° changes"]),
        ("At equilibrium, Q compared with K is:",
         "Q=K", "No net change.",
         ["Q=0", "Q=∞", "Q=k"]),
        ("K is changed by:",
         "temperature (and the reaction's ΔH), not by adding a catalyst or changing concentration",
         "Concentrations change Q; T changes K.",
         ["adding product at constant T", "a catalyst", "an inert solid"]),
        ("For A⇌B, equilibrium [A]=0.20 M and [B]=0.60 M. Kc is:",
         "3.0", "K=[B]/[A]=0.60/0.20=3.0.",
         ["0.33", "0.80", "0.12"]),
        ("For 2NO₂⇌N₂O₄, Kc=[N₂O₄]/[NO₂]². If [NO₂]=0.20 and [N₂O₄]=0.040, Kc is:",
         "1.0", "0.040/(0.20)²=0.040/0.040=1.0.",
         ["0.20", "5.0", "0.008"]),
        ("Pure solids and pure liquids are:",
         "omitted from Kc (their activity is 1)",
         "CaCO₃(s)⇌CaO(s)+CO₂(g) has Kp=P_CO₂.",
         ["put in K as their molarity of 1.00 always numerically from grams", "the only species in K", "equal to Q always"]),
        ("Kp and Kc differ when:",
         "Δn_gas ≠ 0",
         "Gases in Kp use partial pressures.",
         ["the reaction is not redox", "T=0", "a catalyst is present"]),
        ("If K=50, equilibrium lies toward:",
         "products", "K>1.",
         ["reactants", "neither side", "the catalyst"]),
        ("Le Chatelier: adding a product at constant T:",
         "increases Q so the net reaction makes reactant until Q returns to the same K",
         "K itself is unchanged at constant T.",
         ["increases K", "decreases K", "stops all collisions"]),
        ("For an exothermic reaction, increasing T:",
         "decreases K (equilibrium shifts toward reactants)",
         "Heat acts like a product.",
         ["increases K", "does not affect K", "sets K=0"]),
        ("Decreasing volume (increasing P) for N₂+3H₂⇌2NH₃ shifts toward:",
         "NH₃ (fewer gas moles)",
         "The system reduces the mole count of gas.",
         ["N₂ and H₂", "no shift because Kc ignores P", "complete vacuum"]),
        ("Adding an inert gas at constant volume:",
         "does not change concentrations or Kc, so no shift",
         "Partial pressures of reactants would change at constant P, a different story.",
         ["always makes more product", "always increases K", "removes the catalyst"]),
        ("A catalyst added to a system at equilibrium:",
         "causes no shift of the position of equilibrium",
         "Both rates increase; K is the same.",
         ["makes K larger", "makes only product", "changes Δn_gas"]),
        ("Ksp of AgCl is [Ag⁺][Cl⁻]. If Ksp=1.0×10⁻¹⁰, the molar solubility s in pure water is:",
         "1.0×10⁻⁵ M", "s²=1.0×10⁻¹⁰ ⇒ s=1.0×10⁻⁵.",
         ["1.0×10⁻¹⁰ M", "1.0×10⁻²⁰ M", "0.10 M"]),
        ("A common ion (extra Cl⁻) with AgCl(s) will:",
         "decrease the solubility of AgCl",
         "Q starts above Ksp until [Ag⁺] falls.",
         ["increase solubility", "change Ksp at that T", "dissolve the solid completely always"]),
        ("CaF₂(s)⇌Ca²⁺+2F⁻ has Ksp=",
         "[Ca²⁺][F⁻]²", "Do not write CaF₂ in Ksp.",
         ["[Ca²⁺][F⁻]", "[CaF₂]", "[Ca²⁺]²[F⁻]"]),
        ("If Ksp=4.0×10⁻¹¹ for MX₂ (Ksp=4s³), s is closest to:",
         "2.2×10⁻⁴ M", "s³=1.0×10⁻¹¹; s=∛(1.0×10⁻¹¹)≈2.15×10⁻⁴.",
         ["4.0×10⁻¹¹ M", "1.0×10⁻¹¹ M", "0.25 M"]),
        ("Qsp > Ksp means:",
         "a precipitate forms (or more solid appears) until Qsp falls to Ksp",
         "The solution is supersaturated relative to equilibrium.",
         ["the solid dissolves completely", "Ksp increased", "no ions remain"]),
        ("An ICE table lists:",
         "Initial, Change, Equilibrium concentrations (or pressures)",
         "The change row follows the stoichiometry, including signs.",
         ["ionization energy", "current and voltage", "only products"]),
        ("A⇌B, [A]₀=4.0 M, [B]₀=0, K=3. At equilibrium [B] is:",
         "3.0 M", "x/(4.0−x)=3 ⇒ x=12−3x ⇒ 4x=12 ⇒ x=3.0.",
         ["4.0 M", "1.0 M", "12 M"]),
        ("In that same ICE, equilibrium [A] is:",
         "1.0 M", "4.0−3.0=1.0; check K=3.0/1.0=3.",
         ["4.0 M", "3.0 M", "0"]),
        ("If x is small compared with [A]₀ in a weak-binding equilibrium, you may:",
         "approximate [A]₀−x ≈ [A]₀ after checking x is <5% of [A]₀",
         "Then verify the percent.",
         ["always set K=0", "drop products", "set T=0"]),
        ("The change row for 2A⇌B starting from A only is:",
         "A: −2x, B: +x",
         "Stoichiometry of the change must match the equation.",
         ["A: −x, B: +2x", "A: +2x, B: −x", "both −x"]),
        ("Coupled equilibria share a species. Removing that species from one equilibrium:",
         "shifts that equilibrium to replace it (Le Chatelier) and can drag a linked insoluble salt into solution",
         "AgCl dissolves more when Ag⁺ is complexed by NH₃.",
         ["changes the temperature only", "destroys Ksp as a number at that T", "stops all equilibrium"]),
        ("AgCl(s) is more soluble in aqueous NH₃ than in water because:",
         "Ag⁺ is pulled into Ag(NH₃)₂⁺, lowering [Ag⁺] so more AgCl dissolves",
         "Ksp is unchanged; Qsp is driven below Ksp until more solid dissolves.",
         ["NH₃ raises Ksp of AgCl", "NH₃ is an acid that eats Cl⁻ only", "NH₃ heats the beaker"]),
        ("A large Kf for a complex ion means:",
         "the complex is favored; free metal ion is scarce",
         "Coupled to Ksp, solubility of the salt can rise a lot.",
         ["the salt cannot dissolve", "Ksp becomes 1", "Q is undefined"]),
        ("Amphoteric hydroxides (Zn(OH)₂, Al(OH)₃) dissolve in strong base because:",
         "a second equilibrium forms a hydroxo-complex (e.g. Zn(OH)₄²⁻)",
         "That is coupled solubility, not a change of Ksp's tabulated value.",
         ["base always raises Ksp of every salt", "OH⁻ is a common ion that always increases solubility", "the salt becomes a gas"]),
        ("Adding acid to a saturated solution of CaCO₃ increases solubility because:",
         "H⁺ removes CO₃²⁻ (making HCO₃⁻/CO₂), so more CaCO₃ dissolves",
         "Carbonate is the linked basic anion.",
         ["H⁺ raises Ksp", "CaCO₃ is a strong acid", "pressure of O₂ increases K"]),
        ("K vs k: K is equilibrium; k is:",
         "the rate constant from kinetics",
         "Different letters, different ideas.",
         ["the same number always", "only used in Hess's law", "pH"]),
        ("For A⇌2B, K=[B]²/[A]. If both concentrations equal 0.10 M, Q is:",
         "0.10", "(0.10)²/(0.10)=0.10.",
         ["1.0", "0.010", "0.20"]),
        ("If that K=0.40 and Q=0.10, the system:",
         "makes more B (Q<K)",
         "Need more product in the numerator.",
         ["makes more A", "is at equilibrium", "has K falling to 0.10"]),
        ("A graph of [reactant] vs t leveling off above zero is:",
         "equilibrium (forward rate = reverse rate, concentrations constant but not necessarily equal)",
         "Not “the reaction ran out of reactant.”",
         ["a completed irreversible reaction to zero reactant always", "a calorimeter leak", "zero-order kinetics only"]),
        ("Partial pressures in atm may be used in Kp. If P_NO₂=0.50 atm and P_N₂O₄=1.00 atm for 2NO₂⇌N₂O₄, Kp is:",
         "4.0", "1.00/(0.50)²=4.0.",
         ["2.0", "0.25", "0.50"]),
        ("Diluting an aqueous equilibrium A⇌B (K=3) at constant T:",
         "does not change K; Q may change if the reaction has Δn≠0 in solution approximations... for A⇌B with equal coefficients, dilution does not shift",
         "Same number of species on each side: no dilution shift.",
         ["changes K to 1", "always makes more A", "always makes more B"]),
        ("The common-ion effect is Le Chatelier applied to:",
         "a solubility equilibrium when one of the ions is already present",
         "Extra Cl⁻ with AgCl.",
         ["kinetics half-lives", "PES peaks", "hybridization"]),
        ("If AgCl(s) is in water and you add NaCl, [Ag⁺] at the new equilibrium is:",
         "smaller than in pure water",
         "Ksp=[Ag⁺][Cl⁻] with larger [Cl⁻] forces smaller [Ag⁺].",
         ["larger", "unchanged because Ksp rose", "zero always"]),
        ("Writing Kc for N₂(g)+3H₂(g)⇌2NH₃(g):",
         "[NH₃]²/([N₂][H₂]³)",
         "Gases in a closed flask can be written as molarities.",
         ["[N₂][H₂]³/[NH₃]²", "[NH₃]/[N₂][H₂]", "P_total"]),
        ("A small K (10⁻⁸) means:",
         "reactants predominate at equilibrium",
         "Little product when starting from reactants only.",
         ["the reaction is fast", "ΔG° is largely negative", "Q cannot be written"]),
        ("Increasing T for an endothermic dissolution (ΔH>0) typically:",
         "increases Ksp (more soluble at higher T)",
         "Le Chatelier: heat as a reactant.",
         ["decreases Ksp always", "does not affect solubility", "sets s=0"]),
        ("The equilibrium condition is about rates:",
         "forward rate equals reverse rate",
         "Concentrations are constant, not necessarily equal.",
         ["forward rate is zero", "all concentrations equal 1 M", "Q=0"]),
        ("For ICE with K=0.010 and [A]₀=1.00 for A⇌B, x is:",
         "about 0.0099 (small-x OK-ish) or solve quadratic: x=0.0099",
         "x/(1−x)=0.010 ⇒ x=0.010−0.010x ⇒ 1.010x=0.010 ⇒ x=0.00990.",
         ["1.00", "0.50", "0.010 exactly without the 1−x term being close"]),
        ("A salt MX has s=2.0×10⁻⁴ M in pure water. Ksp is:",
         "4.0×10⁻⁸", "(2.0×10⁻⁴)²=4.0×10⁻⁸.",
         ["2.0×10⁻⁴", "4.0×10⁻⁴", "2.0×10⁻⁸"]),
        ("Removing a gaseous product from a gaseous equilibrium:",
         "decreases Q, so the system makes more product",
         "Le Chatelier by changing Q, not K.",
         ["increases K", "stops the reverse reaction forever", "is the same as a catalyst"]),
        ("The units often omitted on Kc are acceptable on AP when:",
         "K is treated as dimensionless via activities, but you still raise concentrations to powers",
         "Plug in molarities as numbers in the expression.",
         ["you skip the exponents", "you include solids as 1.0 M from density always", "K equals ΔG"]),
        ("AP Stretch: H₂+I₂⇌2 HI, K=4.00. Mix [H₂]=[I₂]=[HI]=1.00 M. Compute Q, the direction, and the equilibrium concentrations.",
         "Q=1.00 so shift right; at eq [H₂]=[I₂]=0.75 M, [HI]=1.50 M",
         "Q=(1.00)²/(1.00·1.00)=1.00<4. Let [H₂]=[I₂]=1−x, [HI]=1+2x. (1+2x)/(1−x)=2 ⇒ 1+2x=2−2x ⇒ 4x=1 ⇒ x=0.25. Check: (1.50)²/(0.75·0.75)=4.",
         ["Q=4, already eq, all 1.00", "Q=1, shift left, [HI]=0.50", "Q=0, [HI]=4.00"]),
        ("AP Stretch: 2 NO₂ ⇌ N₂O₄, Kc=1.00, [NO₂]₀=1.00 M, [N₂O₄]₀=0. Solve the ICE (keep the 2x) for x and the equilibrium amounts.",
         "x=0.250; [NO₂]=0.50 M, [N₂O₄]=0.25 M",
         "K=x/(1.00−2x)²=1.00. Trial x=0.250: 1.00−0.50=0.50; (0.50)²=0.25; 0.250/0.25=1.00. The −2x on NO₂ is required.",
         ["x=0.50 with [NO₂]=0 (skipping 2x)", "x=1.00", "K=[NO₂]²/[N₂O₄] inverted"]),
        ("AP Stretch: Ksp(AgCl)=1.8×10⁻¹⁰. In 0.10 M NaCl, [Ag⁺] at equilibrium is closest to:",
         "1.8×10⁻⁹ M", "[Ag⁺](0.10)=1.8×10⁻¹⁰ ⇒ [Ag⁺]=1.8×10⁻⁹ (common ion).",
         ["1.3×10⁻⁵ M (the pure-water s)", "0.10 M", "1.8×10⁻¹⁰ M as [Ag⁺] without dividing"]),
        ("AP Stretch: Explain with Q vs K why adding NH₃ to saturated AgCl(aq) dissolves more solid even though Ksp is fixed at that T.",
         "Complexation lowers [Ag⁺], so Qsp=[Ag⁺][Cl⁻]<Ksp and solid dissolves until Qsp=Ksp again",
         "Ksp unchanged; coupled Kf for Ag(NH₃)₂⁺ removes free Ag⁺.",
         ["NH₃ increases Ksp", "NH₃ is a common ion for Cl⁻", "temperature must rise"]),
        ("AP Stretch: For PCl₅⇌PCl₃+Cl₂ (all gas), Kc=0.040 at a T. A flask has all three at 0.20 M. Q and direction?",
         "Q=0.20; shift left",
         "Q=(0.20)(0.20)/(0.20)=0.20>0.040, so net reverse (make PCl₅).",
         ["Q=0.040, eq", "Q=1.0, shift right", "Q=0.008, shift right"]),
        ("AP Stretch: Construct ICE for HA ⇌ H⁺+A⁻ with [HA]₀=0.25 M, Ka=4.0×10⁻⁶. Find x=[H⁺] with the small-x approximation and check the 5% rule.",
         "x=1.0×10⁻³ M; 0.40% so the approximation holds",
         "x²/0.25=4.0×10⁻⁶ ⇒ x²=1.0×10⁻⁶ ⇒ x=1.0×10⁻³; (0.0010/0.25)×100%=0.40%<5%.",
         ["x=4.0×10⁻⁶ M", "x=0.25 M", "x=1.0×10⁻⁵ M (the 0.10 M / 1.0×10⁻⁵ drill)"]),
        ("AP Stretch: CaCO₃(s) in a closed flask produces CO₂(g). Why does pumping away CO₂ cause more solid to decompose, in Q vs K language?",
         "K=P_CO₂ (solids omitted); removing CO₂ drops Q below K so net forward",
         "Le Chatelier by changing Q.",
         ["Ksp of CaCO₃ increases", "pumping raises T only", "solids appear in K and their mass dropped"]),
        ("AP Stretch: A⇌2B, [A]₀=1.00 M, [B]₀=0, Kc=0.200. Show that x=0.200 satisfies the ICE algebra.",
         "x=0.200; [A]=0.800 M, [B]=0.400 M",
         "E: 1.00−0.200=0.800 and 2(0.200)=0.400. K=(0.400)²/(0.800)=0.160/0.800=0.200.",
         ["x=1.00", "x=0.500 with [B]=1.00", "x=0"]),
        ("AP Stretch: 2A ⇌ B, [A]₀=2.00 M, [B]₀=0, Kc=0.50. Solve the ICE (A changes by −2x) for x and check K.",
         "x=0.50; [A]=1.00 M, [B]=0.50 M",
         "E: [A]=2.00−2x, [B]=x. K=x/(2.00−2x)²=0.50. At x=0.50: [A]=1.00, [B]=0.50, and 0.50/(1.00)²=0.50. If you wrote −x on A, K would not close.",
         ["x=3.0 from A⇌B with K=3 and [A]₀=4", "x=1.00 with [A]=0", "x=0.25 skipping the 2x"]),
    ])


def build_unit7():
    title = "AP Chemistry Unit 7: Equilibrium"
    description = (
        "K versus Q, calculating K, Le Chatelier, Ksp, ICE tables with arithmetic that closes, and coupled "
        "equilibria such as complexation of Ag⁺."
    )
    ice_demo = _ice_table(
        "ICE for A ⇌ B with K=3, starting from 4.0 M A",
        [("A", "4.0", "−x", "4.0−x"), ("B", "0", "+x", "x")],
    )
    c1 = concept_block(
        "1. K vs Q",
        [
            "The equilibrium constant $K$ is a number, at a given temperature, equal to the ratio of product "
            "amounts to reactant amounts — each raised to its stoichiometric coefficient — when the system has "
            "stopped changing net composition. $K$ does not care how you got there. It is not the rate constant $k$.",
            "The reaction quotient $Q$ uses the identical algebraic form as $K$, but with the amounts you have "
            "right now. $Q$ is a snapshot; $K$ is the snapshot at equilibrium. Comparing them is the whole game.",
            "If $Q<K$, the ratio is too reactant-heavy, so the net reaction makes products ($Q$ rises toward $K$). "
            "If $Q>K$, the net reaction makes reactants. If $Q=K$, you are at equilibrium: forward rate equals "
            "reverse rate, concentrations constant (not necessarily equal).",
            "Numeric: A⇌B, $K=3$. A mixture with $[A]=[B]=1.00$ has $Q=1.00<3$, so B will grow. A mixture with "
            "$[A]=0.20$, $[B]=0.60$ has $Q=3.0=K$ already.",
            "$K$ changes only when $T$ changes (direction set by $\\Delta H$). Adding product changes $Q$, not $K$. "
            "A catalyst changes neither $Q$ nor $K$; it only shortens the time to $Q=K$.",
            "On FRQs, write $Q$ with numbers, compare to $K$, then state the net direction in a sentence. Skipping "
            "the $Q$ calculation loses the justification point.",
        ],
        "Every Le Chatelier story is secretly a $Q$ vs $K$ story. Solubility, acids, and electrochemistry all "
        "reuse this comparison.",
        "Write the $Q$ expression, plug in the current numbers, then write $Q ? K$ and the arrow direction. Do "
        "not change $K$ unless the prompt changed $T$.",
        lesson_figure(
            xy_graph(
                curves=[("#1d4ed8", sample_curve(lambda t: 3.0 * (1 - 2.718 ** (-t / 8)), 0, 40))],
                dashes=[("h", 3.0, "eq. [B] when K=3")],
                xlim=(0, 42), ylim=(0, 4.2), xlab="time", ylab="[B]", w=320, h=240,
            ),
            "[B] approaches a plateau — that plateau is equilibrium, not “zero reactant”",
            "Q starts below K and rises. The flat region is Q=K, with both A and B still present.",
        )
        + solved(1, "If $Q<K$, which way does the net reaction go?",
               ["$Q$ is too small: not enough product in the ratio.",
                "The forward process increases $Q$.",
                "Net shift to the right until $Q=K$."],
               "toward products", "", "Easy")
        + solved(2, "A⇌B, $K=3$, $[A]=0.20$, $[B]=0.60$. Compare $Q$ to $K$.",
                 ["$Q=[B]/[A]=0.60/0.20=3.0$.",
                  "$Q=K$.",
                  "The mixture is already at equilibrium."],
                 "$Q=K=3$", "", "Medium")
        + solved(3, "A⇌B, $K=3$, mix $1.00$ M A and $1.00$ M B. Direction and new equilibrium amounts?",
                 ["$Q=1.00/1.00=1.00<3$: shift right.",
                  "Let $[A]=1.00-x$, $[B]=1.00+x$.",
                  "$(1+x)/(1-x)=3\\Rightarrow 1+x=3-3x\\Rightarrow 4x=2\\Rightarrow x=0.50$.",
                  "Equilibrium: $[A]=0.50$ M, $[B]=1.50$ M. Check: $1.50/0.50=3$."],
                 "$[A]=0.50$ M, $[B]=1.50$ M", "", "Hard"),
        ("Changing $K$ when you add product",
         "Adding product makes $Q$ larger. $K$ stays put at constant $T$. The system then shifts left to bring "
         "$Q$ back down to that same $K$."),
        ("Compute $Q$ on paper before saying “shift”",
         "A one-line $Q$ value is the evidence. “It will shift right because I added reactant” is incomplete "
         "if you never showed $Q<K$."),
        [
            "I can define $K$ vs $Q$ in plain language.",
            "I can predict direction from $Q$ vs $K$.",
            "I can explain that $T$ changes $K$ while concentration changes $Q$.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Calculating K",
        [
            "For aA+bB⇌cC+dD, $K_c=\\dfrac{[C]^c[D]^d}{[A]^a[B]^b}$ using equilibrium molarities. Gases may "
            "instead use $K_p$ in partial pressures. Pure solids and pure liquids are omitted (activity $1$). "
            "That is why $\\mathrm{CaCO_3(s)\\rightleftharpoons CaO(s)+CO_2(g)}$ has $K_p=P_{\\mathrm{CO_2}}$.",
            "Example: $2\\,\\mathrm{NO_2\\rightleftharpoons N_2O_4}$, $[NO_2]=0.20$ M, $[N_2O_4]=0.040$ M. "
            "$K_c=0.040/(0.20)^2=0.040/0.040=1.0$. Exponents are not optional: forgetting the square is a "
            "content error.",
            "If $K$ is much larger than $1$, products dominate at equilibrium. If $K$ is $10^{-8}$, reactants "
            "dominate. $K=1$ means a comparable mix (depending on the powers).",
            "$K_p$ and $K_c$ differ when $\\Delta n_\\mathrm{gas}\\neq 0$. You can still reason with either form "
            "as long as you are consistent. AP often gives all-gas concentrations in a flask and wants $K_c$.",
            "Numeric $K_p$: $2\\,\\mathrm{NO_2\\rightleftharpoons N_2O_4}$, $P_{NO_2}=0.50$ atm, $P_{N_2O_4}=1.00$ "
            "atm. $K_p=1.00/(0.50)^2=4.0$.",
            "Never put a solid in $K$. Never use the rate law exponents. Never set $K=k$. Those three mix-ups "
            "are the usual zeros.",
        ],
        "You cannot do ICE, $K_\\mathrm{sp}$, or weak-acid $K_a$ until the $K$ expression is right. This is "
        "the grammar of Unit 7.",
        "Write the balanced equation, drop solids/liquids, raise each remaining species to its coefficient, "
        "products over reactants. Then insert equilibrium values only.",
        lesson_figure(
            beaker_svg("eq. mixture A and B"),
            "K is computed from the mixture after it stops changing",
            "Both species are usually still in the beaker. K=3 does not mean “no A left.” It means [B]/[A]=3 "
            "for A⇌B.",
        )
        + solved(4, "A⇌B, $[A]_{eq}=0.20$, $[B]_{eq}=0.60$. Find $K_c$.",
               ["$K=[B]/[A]$.",
                "$K=0.60/0.20$.",
                "$K=3.0$."],
               "$3.0$", "", "Easy")
        + solved(5, "$2\\,NO_2\\rightleftharpoons N_2O_4$, $[NO_2]=0.20$, $[N_2O_4]=0.040$. Find $K_c$.",
                 ["$K=[N_2O_4]/[NO_2]^2$.",
                  "Denominator $(0.20)^2=0.040$.",
                  "$K=0.040/0.040=1.0$."],
                 "$1.0$", "", "Medium")
        + solved(6, "Write $K_p$ for $\\mathrm{CaCO_3(s)\\rightleftharpoons CaO(s)+CO_2(g)}$ and interpret a $K_p=0.15$.",
                 ["Solids omitted: $K_p=P_{\\mathrm{CO_2}}$.",
                  "If $K_p=0.15$, the equilibrium CO₂ pressure is $0.15$ atm at that $T$.",
                  "Adding more CaCO₃(s) does not change $K_p$ or that pressure.",
                  "Pumping away CO₂ drops $Q$ below $K$ so more solid decomposes."],
                 "$K_p=P_{CO_2}$", "", "Hard"),
        ("Putting the solid's “concentration” into $K$",
         "A chunk of CaCO₃ is not $1.00$ M. Solids are omitted. Extra solid does not change $K$ or the "
         "equilibrium pressure of CO₂ at that $T$."),
        ("Write the $K$ expression before touching a calculator",
         "If the exponents are wrong, every later ICE number is theatre. Box the expression, then substitute."),
        [
            "I can write $K_c$ with correct exponents.",
            "I can omit solids and liquids.",
            "I can compute $K$ from equilibrium concentrations or pressures.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Le Chatelier's principle",
        [
            "Le Chatelier's principle: if you disturb an equilibrium, the net reaction proceeds in the direction "
            "that counteracts the disturbance until $Q$ again equals the $K$ for that $T$. It is not a mystical "
            "force; it is $Q$ vs $K$ plus, when $T$ changes, a new $K$.",
            "Add product: $Q$ rises above $K$, net reverse. Remove product: $Q$ falls, net forward. Add reactant: "
            "net forward. These moves do not change $K$ at constant $T$.",
            "Temperature is different because $K$ itself changes. For an exothermic reaction, heat is like a "
            "product: raising $T$ decreases $K$ (less product at the new equilibrium). For endothermic, raising "
            "$T$ increases $K$.",
            "Pressure/volume for gases: decreasing $V$ raises all partial pressures. The system shifts toward "
            "fewer moles of gas. $\\mathrm{N_2+3H_2\\rightleftharpoons 2NH_3}$ shifts toward NH₃. If $\\Delta n_\\mathrm{gas}=0$, "
            "no shift from $P$ at constant $T$.",
            "Inert gas at constant $V$ does not change concentrations of the reactants, so $K_c$ systems do not "
            "shift. A catalyst does not shift the position; it only gets you there faster.",
            "FRQ answers that earn points name the disturbance, state whether $Q$ or $K$ changed, and give the "
            "net direction. “It shifts right” alone is incomplete.",
        ],
        "Le Chatelier is the qualitative control panel for industrial ammonia, for solubility, and for hemoglobin "
        "stories. The quantitative engine underneath is still $Q$ and $K$.",
        "Ask: did $T$ change? Then $K$ changed. Otherwise $K$ is fixed and you moved $Q$. Then pick the arrow "
        "that restores $Q=K$.",
        lesson_figure(
            beaker_svg("add product → Q up → shift left"),
            "Adding product is a Q disturbance, not a K disturbance",
            "The beaker's K is the same number after you dump in extra B. The mixture is briefly “too far right,” "
            "so net reverse occurs.",
        )
        + solved(7, "A⇌B at equilibrium. You add B at constant $T$. What happens to $K$ and to the net rate?",
               ["$K$ is unchanged (constant $T$).",
                "$Q$ increases because [B] jumped.",
                "Net reverse makes A until $Q=K$ again."],
               "$K$ same; net left", "", "Easy")
        + solved(8, "Exothermic $2\\,SO_2+O_2\\rightleftharpoons 2\\,SO_3$. Effect of raising $T$ on $K$?",
                 ["Heat is a product of the forward reaction.",
                  "Raising $T$ decreases $K$.",
                  "The new equilibrium has relatively more SO₂ and O₂."],
                 "$K$ decreases", "", "Medium")
        + solved(9, "Why does decreasing volume favor NH₃ in $\\mathrm{N_2+3H_2\\rightleftharpoons 2NH_3}$?",
                 ["Four moles of gas on the left, two on the right.",
                  "Smaller $V$ raises pressure; the system reduces the number of gas particles.",
                  "Net forward makes NH₃.",
                  "$K$ is unchanged if $T$ is unchanged; $Q$ (in pressures) was disturbed."],
                 "toward fewer gas moles", "", "Hard"),
        ("Saying a catalyst “shifts equilibrium to the right”",
         "A catalyst speeds both directions. $K$ is a thermo number. Industry uses a catalyst to go faster, not "
         "to cheat $K$."),
        ("Separate “$K$ changed” from “$Q$ changed” in the first sentence",
         "Temperature → $K$. Amounts/volume → $Q$. That split is the entire principle made testable."),
        [
            "I can predict shifts from adding/removing species.",
            "I can predict how $T$ changes $K$ using $\\Delta H$.",
            "I can treat volume and catalysts correctly.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Solubility product",
        [
            "$K_\\mathrm{sp}$ is the equilibrium constant for a slightly soluble ionic solid dissolving. For "
            "AgCl(s)⇌Ag⁺(aq)+Cl⁻(aq), $K_\\mathrm{sp}=[Ag^+][Cl^-]$. The solid is omitted. A large $K_\\mathrm{sp}$ "
            "means more soluble (comparing salts of the same ion-count type).",
            "In pure water, $[Ag^+]=[Cl^-]=s$, so $s^2=K_\\mathrm{sp}$. If $K_\\mathrm{sp}=1.0\\times10^{-10}$, "
            "$s=1.0\\times10^{-5}$ M. That $s$ is the molar solubility.",
            "Common ion: in $0.10$ M NaCl, $[Cl^-]\\approx 0.10$, so $[Ag^+]=K_\\mathrm{sp}/0.10=1.0\\times10^{-9}$ M "
            "if $K_\\mathrm{sp}=1.0\\times10^{-10}$. Solubility dropped by a factor of $10^4$ compared with pure water. "
            "That is Le Chatelier.",
            "For CaF₂, $K_\\mathrm{sp}=[Ca^{2+}][F^-]^2= (s)(2s)^2=4s^3$. Do not write $s^2$ for an MX₂ salt. "
            "If $4s^3=4.0\\times10^{-11}$, $s^3=1.0\\times10^{-11}$, $s\\approx 2.2\\times10^{-4}$ M.",
            "$Q_\\mathrm{sp}$ uses the same form with current ions. If $Q_\\mathrm{sp}>K_\\mathrm{sp}$, a precipitate "
            "forms. If $Q_\\mathrm{sp}<K_\\mathrm{sp}$, the solution is unsaturated and more solid can dissolve.",
            "Comparing solubility of different formula types by comparing $K_\\mathrm{sp}$ numbers directly is "
            "illegal: $s$ vs $4s^3$ are different algebras. Compute $s$ first, then compare.",
        ],
        "$K_\\mathrm{sp}$ is ICE for a solid. Precipitation labs, qualitative analysis, and coupled dissolving "
        "in acid or ammonia all start here.",
        "Write $K_\\mathrm{sp}$ without the solid. Relate $s$ to each ion with stoichiometry. Square or cube "
        "correctly, then take the root.",
        lesson_figure(
            beaker_svg("saturated AgCl, extra solid"),
            "A saturated solution still has undissolved solid",
            "Ksp describes the ions in contact with that solid. Extra solid does not change Ksp or the ion "
            "product at that T.",
        )
        + solved(10, "$K_\\mathrm{sp}(AgCl)=1.0\\times10^{-10}$. Molar solubility in pure water?",
               ["$s^2=1.0\\times10^{-10}$.",
                "$s=1.0\\times10^{-5}$ M.",
                "$[Ag^+]=[Cl^-]=1.0\\times10^{-5}$ M."],
               "$1.0\\times10^{-5}$ M", "", "Easy")
        + solved(11, "Same $K_\\mathrm{sp}$ in $0.10$ M NaCl. Find $[Ag^+]$.",
                 ["$[Cl^-]\\approx 0.10$ (common ion).",
                  "$[Ag^+](0.10)=1.0\\times10^{-10}$.",
                  "$[Ag^+]=1.0\\times10^{-9}$ M.",
                  "Much less soluble than in pure water."],
                 "$1.0\\times10^{-9}$ M", "", "Medium")
        + solved(12, "Write $K_\\mathrm{sp}$ for CaF₂ and $K_\\mathrm{sp}$ in terms of $s$.",
                 ["CaF₂(s)⇌Ca²⁺+2 F⁻.",
                  "$K_\\mathrm{sp}=[Ca^{2+}][F^-]^2$.",
                  "$[Ca^{2+}]=s$, $[F^-]=2s$.",
                  "$K_\\mathrm{sp}=(s)(2s)^2=4s^3$."],
                 "$4s^3$", "", "Hard"),
        ("Using $s=\\sqrt{K_\\mathrm{sp}}$ for CaF₂",
         "That square root is for MX salts. MX₂ needs $4s^3$. Wrong algebra, wrong $s$ by a lot."),
        ("Write the two-ion row of an ICE even for $K_\\mathrm{sp}$",
         "I: 0, 0 (plus solid). C: $+s$, $+2s$. E: $s$, $2s$. Then the $K$ expression cannot have the wrong powers."),
        [
            "I can write $K_\\mathrm{sp}$ omitting the solid.",
            "I can convert $K_\\mathrm{sp}$ to $s$ for MX and MX₂.",
            "I can apply the common-ion effect with $Q$ vs $K_\\mathrm{sp}$.",
        ],
        16,
    )
    c5 = concept_block(
        "5. ICE tables",
        [
            "ICE means Initial, Change, Equilibrium. It is a bookkeeping table so the stoichiometry of the "
            "change matches the balanced equation. Without the table, students invent random $x$ placements.",
            ice_demo +
            "For A⇌B, $K=3$, $[A]_0=4.0$, $[B]_0=0$: $K=x/(4.0-x)=3$. Then $x=3(4.0-x)=12-3x$, so $4x=12$, "
            "$x=3.0$. Equilibrium: $[A]=1.0$ M, $[B]=3.0$ M. Check: $3.0/1.0=3$. The check is not optional.",
            "The change row carries the coefficients: for 2 NO₂ ⇌ N₂O₄, NO₂ changes by $-2x$ and N₂O₄ by $+x$. "
            "Writing $-x$ for NO₂ is the classic ICE error and it will not satisfy a correct $K$ expression.",
            "If $K$ is very small and you start with only reactant, $x$ may be tiny compared with $[A]_0$. Then "
            "$[A]_0-x\\approx[A]_0$. After solving, check the 5% rule: $x/[A]_0\\times 100\\%$ should be $<5\\%$ "
            "or you solve the quadratic. For $K_a=1.0\\times10^{-5}$ and $0.10$ M HA, $x=1.0\\times10^{-3}$ is $1\\%$ — OK.",
            "If $Q$ is not zero at the start, the change still follows stoichiometry but $x$ might be negative "
            "(net reverse). The A⇌B mix of $1.00$ M each with $K=3$ used a positive $x$ because $Q<K$.",
            "ICE is how AP Chemistry wants to see equilibrium algebra. A paragraph of symbols without a table "
            "is harder to grade and easier to reverse.",
        ],
        "ICE is the skill that Unit 8 (weak acids, buffers) and $K_\\mathrm{sp}$ both assume. If $x$ is in the "
        "wrong cell, pH will be wrong by orders of magnitude.",
        "Draw I, C, E. Fill I from the prompt. Write C with coefficients and a single $x$. Write E as sums. "
        "Substitute E into $K$. Solve. Check $K$ and the 5% rule.",
        lesson_figure(
            _ice_table(
                "Filled ICE that actually closes ($K=3$)",
                [("A", "4.0", "−3.0", "1.0"), ("B", "0", "+3.0", "3.0")],
            ),
            "After solving, replace x with a number and verify K",
            "3.0/1.0=3. If your table does not reproduce K, the algebra or the change row is wrong.",
        )
        + solved(13, "For the $K=3$, $[A]_0=4.0$ table, why is $x=3.0$ rather than $4.0$?",
               ["$K=x/(4-x)=3$.",
                "$x=12-3x\\Rightarrow 4x=12\\Rightarrow x=3$.",
                "If $x=4$, $[A]$ would be $0$ and $K$ would be undefined/infinite, not $3$."],
               "$x=3.0$", "", "Easy")
        + solved(14, "Write the change row for $2\\,NO_2\\rightleftharpoons N_2O_4$ starting from NO₂ only.",
                 ["NO₂ is consumed twice as fast as N₂O₄ is formed.",
                  "NO₂: $-2x$. N₂O₄: $+x$.",
                  "$K=x/( [NO_2]_0-2x )^2$."],
                 "NO₂: $-2x$; N₂O₄: $+x$", "", "Medium")
        + solved(15, "HA⇌H⁺+A⁻, $[HA]_0=0.10$, $K_a=1.0\\times10^{-5}$. Find $x$ with small-$x$ and check 5%.",
                 ["$x^2/0.10=1.0\\times10^{-5}$.",
                  "$x^2=1.0\\times10^{-6}$, $x=1.0\\times10^{-3}$ M.",
                  "Percent: $0.0010/0.10\\times 100\\%=1.0\\%<5\\%$.",
                  "The approximation is acceptable; $[H^+]=1.0\\times10^{-3}$ M."],
                 "$x=1.0\\times10^{-3}$ M (1%)", "", "Hard"),
        ("Putting $+x$ on the reactant side when the reaction goes forward from all reactant",
         "If you start with only A and $Q=0<K$, A must fall. The change for A is negative."),
        ("Always substitute the E row back into $K$ as a check",
         "Ten seconds. If $K$ does not return, you inverted a ratio or dropped a coefficient of $2$."),
        [
            "I can build an I/C/E table with stoichiometric changes.",
            "I can solve $x/(4-x)=3$ type algebra and check $K$.",
            "I can apply and verify the small-$x$ approximation.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Coupled equilibria",
        [
            "Coupled equilibria share a chemical species. Disturbing one equilibrium changes the shared "
            "concentration, so the other equilibrium shifts. $K$ values stay the same at constant $T$; the "
            "amounts move.",
            "Silver chloride in ammonia is the AP flagship. AgCl(s)⇌Ag⁺+Cl⁻ has tiny $K_\\mathrm{sp}$. "
            "Ag⁺+2 NH₃⇌Ag(NH₃)₂⁺ has a large $K_f$. NH₃ pulls free Ag⁺ into the complex, $[Ag^+]$ falls, "
            "$Q_\\mathrm{sp}<K_\\mathrm{sp}$, and more AgCl dissolves. Tabulated $K_\\mathrm{sp}$ did not increase.",
            "Acid on a carbonate: H⁺ converts CO₃²⁻ into HCO₃⁻ and CO₂. Removing carbonate from the $K_\\mathrm{sp}$ "
            "expression's partner ion makes more CaCO₃ dissolve — how acid rain attacks limestone, and how "
            "qualitative analysis dissolves carbonates.",
            "Amphoteric hydroxides dissolve in excess strong base by forming hydroxo-complexes (Zn(OH)₄²⁻). "
            "Again $K_\\mathrm{sp}$ is unchanged; a second $K_f$ is coupled to it.",
            "The net equilibrium is the sum of the steps, and $K_\\mathrm{net}=K_\\mathrm{sp}\\times K_f$ (with "
            "correct stoich). A large $K_\\mathrm{net}$ means dissolving is extensive even if $K_\\mathrm{sp}$ alone "
            "is tiny.",
            "When you explain coupled solubility on an FRQ, say which ion was removed, that $Q_\\mathrm{sp}$ fell "
            "below $K_\\mathrm{sp}$, and that $K_\\mathrm{sp}$ itself is fixed at that $T$.",
        ],
        "Coupled equilibria are how AP Chemistry tests whether you see $Q$ vs $K$ in a two-reaction system. "
        "They also preview buffers (shared H⁺) without leaving this unit's logic.",
        "Identify the shared species. State how the second reaction changes that species' concentration. Then "
        "apply Le Chatelier to the first $K$.",
        lesson_figure(
            beaker_svg("AgCl(s) + NH₃(aq)"),
            "Ammonia does not rewrite Ksp; it hides Ag⁺ in a complex",
            "Free [Ag⁺] drops. The ion product [Ag⁺][Cl⁻] falls below Ksp, so more solid dissolves until the "
            "new free [Ag⁺] again satisfies Ksp together with [Cl⁻].",
        )
        + solved(16, "Why does AgCl dissolve more in NH₃(aq) than in water?",
               ["NH₃ binds Ag⁺ as Ag(NH₃)₂⁺.",
                "Free $[Ag^+]$ decreases.",
                "$Q_\\mathrm{sp}<K_\\mathrm{sp}$, so more AgCl(s) dissolves."],
               "Ag⁺ is complexed; Qsp drops", "", "Easy")
        + solved(17, "Does NH₃ change the tabulated $K_\\mathrm{sp}$ of AgCl at that $T$?",
                 ["$K_\\mathrm{sp}$ depends on $T$ (and the salt), not on NH₃.",
                  "NH₃ changes concentrations (hence $Q_\\mathrm{sp}$), not $K_\\mathrm{sp}$.",
                  "The solubility $s$ increases; the constant $K_\\mathrm{sp}$ does not."],
                 "no; $K_\\mathrm{sp}$ unchanged", "", "Medium")
        + solved(18, "Write the net coupled reaction AgCl(s)+2 NH₃ ⇌ Ag(NH₃)₂⁺ + Cl⁻ and state what $K_\\mathrm{net}$ is made of.",
                 ["Add dissolving and complexation; Ag⁺ cancels.",
                  "$K_\\mathrm{net}=K_\\mathrm{sp}\\times K_f$.",
                  "A large $K_f$ can make $K_\\mathrm{net}$ much larger than $K_\\mathrm{sp}$.",
                  "That is why a lot of solid can dissolve even though $K_\\mathrm{sp}$ is $10^{-10}$."],
                 "$K_\\mathrm{net}=K_{sp}K_f$", "", "Hard"),
        ("Claiming $K_\\mathrm{sp}$ “got bigger” because more solid dissolved",
         "Solubility $s$ and $K_\\mathrm{sp}$ are not synonyms once a second equilibrium is running. Keep the "
         "constant and the observed $s$ separate."),
        ("Name the shared ion and whether it went up or down",
         "“[Ag⁺] fell because of $K_f$” is the sentence that earns the coupling point."),
        [
            "I can explain AgCl + NH₃ with $Q_\\mathrm{sp}$ vs $K_\\mathrm{sp}$.",
            "I can keep $K_\\mathrm{sp}$ fixed while solubility changes.",
            "I can write $K_\\mathrm{net}$ as a product of $K$ values.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        ["K vs Q", "Calculating K", "Le Chatelier",
         "Solubility product", "ICE tables", "Coupled equilibria"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8
# ===========================================================================

def _u8_questions():
    return _qs([
        ("pH is defined as $-\\log[H^+]$ (with $[H^+]$ in M). For 0.010 M HCl, a strong acid, pH is:",
         "2.00", "−log(0.010)=2.00.",
         ["12.00", "0.010", "1.00"]),
        ("0.0010 M HCl has pH:",
         "3.00", "−log(1.0×10⁻³)=3.00.",
         ["11.00", "0.0010", "1.00"]),
        ("0.010 M NaOH (strong base) has pOH=2.00 and pH:",
         "12.00", "pH+pOH=14.00 at 25°C; 14.00−2.00=12.00.",
         ["2.00", "7.00", "0.010"]),
        ("A strong acid in water is best described as:",
         "essentially 100% ionized, so [H⁺] equals the formal acid concentration (for monoprotic)",
         "HCl, HBr, HI, HNO₃, H₂SO₄ (first H), HClO₄.",
         ["mostly molecules, like acetic acid", "a buffer by itself", "pH=7 always"]),
        ("[H⁺] of a solution with pH=4.00 is:",
         "1.0×10⁻⁴ M", "10^{−4}=1.0×10⁻⁴.",
         ["4.0 M", "1.0×10⁴ M", "10.0 M"]),
        ("A weak acid HA only partly ionizes. Ka is:",
         "[H⁺][A⁻]/[HA] at equilibrium",
         "Small Ka means little ionization.",
         ["[HA]/[H⁺]", "Kb of water only", "the pH directly"]),
        ("0.10 M HA with Ka=1.0×10⁻⁵. Approximate [H⁺] is:",
         "1.0×10⁻³ M", "√(Ka C)=√(1.0×10⁻⁶)=1.0×10⁻³.",
         ["0.10 M", "1.0×10⁻⁵ M", "1.0×10⁻⁶ M"]),
        ("That solution's pH is:",
         "3.00", "−log(1.0×10⁻³)=3.00.",
         ["1.00", "5.00", "7.00"]),
        ("The 5% rule for that approximation: x/C ×100% is:",
         "1.0%, so the approximation is acceptable",
         "0.0010/0.10=0.010=1.0%.",
         ["50%", "5.0% exactly as Ka", "100%"]),
        ("Larger Ka (same C) means:",
         "more ionization and a lower pH",
         "Stronger weak acid.",
         ["less ionization", "pH=7", "Ka becomes Kb"]),
        ("A buffer is a mixture that resists pH change when small amounts of acid or base are added. It contains:",
         "a weak acid and its conjugate base (or a weak base and its conjugate acid) in comparable amounts",
         "HCl alone is not a buffer.",
         ["only a strong acid", "only water", "a metal electrode"]),
        ("Henderson–Hasselbalch: pH = pKa + log([A⁻]/[HA]). If [A⁻]=[HA], pH is:",
         "equal to pKa", "log(1)=0.",
         ["7 always", "1", "14"]),
        ("pKa=4.74, [A⁻]=0.20 M, [HA]=0.10 M. pH is closest to:",
         "5.04", "4.74+log(2)=4.74+0.30=5.04.",
         ["4.44", "7.00", "9.48"]),
        ("Adding a little strong acid to a buffer:",
         "converts some A⁻ into HA; pH drops only slightly",
         "The ratio [A⁻]/[HA] falls a little.",
         ["destroys all HA", "sends pH to 1 always", "raises pH a lot"]),
        ("The best buffer capacity near pH 4.7 uses an acid with:",
         "pKa near 4.7 and similar [HA] and [A⁻]",
         "Choose the conjugate pair whose pKa matches the target.",
         ["pKa=14", "HCl/NaCl", "pKa=0"]),
        ("A strong-acid / strong-base titration curve has equivalence-point pH near:",
         "7 at 25°C", "The salt is neutral (e.g. NaCl).",
         ["1", "13", "4.7"]),
        ("A weak-acid / strong-base titration has equivalence-point pH:",
         "greater than 7 (A⁻ is a weak base)",
         "The salt hydrolyzes.",
         ["equal to 1", "less than 7", "undefined"]),
        ("At half-equivalence of a weak acid titration, pH equals:",
         "pKa", "[HA]=[A⁻] in the flask (approximately).",
         ["7 always", "0", "pKb of water"]),
        ("The steep jump on a titration curve is used to:",
         "locate the equivalence point (and choose an indicator whose range overlaps the jump)",
         "Phenolphthalein works for SA/SB and many WA/SB jumps.",
         ["measure Ka of HCl", "find the boiling point", "compute Ksp of NaCl"]),
        ("Before any base is added to a weak acid, pH is set by:",
         "the Ka ICE of HA alone",
         "No buffer yet (unless A⁻ was already present).",
         ["pH=7", "pH=pKa automatically", "the buret reading"]),
        ("In a galvanic (voltaic) cell, oxidation occurs at the:",
         "anode", "The anode is the electron source (often labeled − in galvanic cells).",
         ["cathode", "salt bridge only", "voltmeter glass"]),
        ("Reduction occurs at the:",
         "cathode", "Electrons arrive here through the wire.",
         ["anode", "only in the salt bridge", "calorimeter"]),
        ("For Zn|Zn²⁺||Cu²⁺|Cu, E°cell=1.10 V. The anode metal is:",
         "Zn (Zn → Zn²⁺ + 2e⁻)",
         "E°_ox of Zn is more favorable than of Cu; Zn is oxidized.",
         ["Cu", "the salt", "H₂"]),
        ("The salt bridge's job is to:",
         "allow ion flow to keep each beaker electrically neutral",
         "Electrons go through the wire, not through the bridge.",
         ["let electrons swim through the gel", "heat the cell", "change K of the redox"]),
        ("E°cell = E°cathode − E°anode (reduction potentials). If E°_Cu=0.34 V and E°_Zn=−0.76 V, E°cell is:",
         "1.10 V", "0.34−(−0.76)=1.10.",
         ["−1.10 V", "0.42 V", "0.34 V"]),
        ("The Nernst equation (25°C) is E = E° − (0.059/n) log Q. If Q increases (more product), E:",
         "decreases (cell is less driving)",
         "log Q grows; you subtract more.",
         ["increases always", "equals E° always", "becomes the boiling point"]),
        ("At equilibrium, Q=K and E is:",
         "0 (dead cell)",
         "No net driving voltage.",
         ["equal to E°", "infinite", "0.059 V always"]),
        ("If you increase [Cu²⁺] in the Zn/Cu cell (Q smaller), E:",
         "increases (more driving force toward products)",
         "Q=[Zn²⁺]/[Cu²⁺] for Zn+Cu²⁺→Zn²⁺+Cu.",
         ["decreases", "stays exactly E°", "becomes negative always"]),
        ("n in the Nernst equation is:",
         "moles of electrons transferred in the balanced cell reaction",
         "For Zn/Cu, n=2.",
         ["the principal quantum number", "pH", "the number of beakers"]),
        ("Qualitatively, a concentration cell (same half-reaction, different [ion]) has E°=0, so E is nonzero only because:",
         "Q ≠ 1; electrons flow until concentrations equalize",
         "Nernst still applies.",
         ["the salt bridge is a battery", "n=0", "K=0"]),
        ("pH of 0.10 M HCl is:",
         "1.00", "−log(0.10)=1.00.",
         ["13.00", "0.10", "7.00"]),
        ("Kb of A⁻ if Ka of HA is 1.0×10⁻⁵ (Kw=1.0×10⁻¹⁴) is:",
         "1.0×10⁻⁹", "Kb=Kw/Ka=1.0×10⁻¹⁴/1.0×10⁻⁵=1.0×10⁻⁹.",
         ["1.0×10⁻⁵", "1.0×10⁻¹⁴", "1.0×10⁻¹⁹"]),
        ("A solution of 0.10 M sodium acetate (A⁻) is:",
         "basic (A⁻ hydrolyzes: A⁻+H₂O⇌HA+OH⁻)",
         "Salts of weak acids are basic.",
         ["acidic like HCl", "pH=7 exactly always", "a strong acid"]),
        ("Buffer: 0.10 mol HA and 0.10 mol A⁻ in 1.00 L, pKa=4.74. After adding 0.01 mol strong acid (ignore volume), pH is closest to:",
         "4.65", "New HA=0.11, A⁻=0.09; pH=4.74+log(0.09/0.11)=4.74+log(0.818)=4.74−0.087=4.65.",
         ["1.00", "7.00", "3.00"]),
        ("In a galvanic Zn/Cu cell, electrons in the wire flow from:",
         "Zn to Cu", "Anode to cathode in the external circuit.",
         ["Cu to Zn", "through the salt bridge as e⁻", "into the water only"]),
        ("Which is not a buffer?",
         "0.10 M HCl and 0.10 M NaCl",
         "HCl is strong; Cl⁻ is not a meaningful weak-base partner.",
         ["0.10 M acetic acid and 0.10 M sodium acetate", "0.10 M NH₃ and 0.10 M NH₄Cl", "a weak acid with its conjugate base"]),
        ("At the SA/SB equivalence point, the species in the flask are mainly:",
         "water and spectator ions (e.g. Na⁺, Cl⁻)",
         "H⁺ and OH⁻ have been matched.",
         ["excess HCl at 0.10 M still", "only OH⁻ at 1 M", "solid Na metal"]),
        ("If E is positive, the cell reaction as written is:",
         "thermodynamically favored (K>1, galvanic as written)",
         "Related to ΔG=−nFE.",
         ["always endothermic", "at equilibrium", "impossible"]),
        ("pH+pOH=14.00 is reliable at:",
         "25°C (Kw=1.0×10⁻¹⁴)",
         "At other T, Kw changes so the 14.00 sum changes.",
         ["all temperatures including 0 K", "only in buffers", "only in galvanic cells"]),
        ("A diprotic H₂SO₄ first proton is strong. 0.010 M H₂SO₄ has [H⁺] from the first proton of:",
         "0.010 M (and a bit more from the weak second proton)",
         "pH a little under 2, not exactly 2.00 if you include Ka2, but AP often treats dilute H₂SO₄ carefully.",
         ["0.020 M exactly always ignoring Ka2", "7", "12"]),
        ("The cathode in the Cu beaker of a Daniell cell is positive because:",
         "Cu²⁺ consumes electrons, so that electrode draws e⁻ from the wire",
         "Reduction is a sink for electrons.",
         ["Cu metal is more reactive than Zn", "the salt bridge pumps electrons", "pH=0 there"]),
        ("Adding water to a buffer (diluting HA and A⁻ equally) makes pH:",
         "almost unchanged (ratio [A⁻]/[HA] stays the same) until capacity is considered",
         "HH depends on the ratio, not the absolute amounts, to first order.",
         ["jump to 7 always", "drop to 1", "equal to 0"]),
        ("log(2)≈0.30 is the number you use when [A⁻]/[HA]=2. pKa=5.00 then pH≈:",
         "5.30", "5.00+0.30=5.30.",
         ["4.70", "7.00", "10.00"]),
        ("If Q is made very small in a galvanic cell (high reactant ion, low product ion), E compared with E° is:",
         "larger than E°",
         "−(0.059/n)log Q is positive when Q<1.",
         ["smaller than E°", "zero", "equal to pH"]),
        ("Phenolphthalein is colorless in acid and pink in base. In a WA/SB titration it changes:",
         "near the steep region after the buffer zone, close to (or just after) equivalence",
         "Its range is ~8–9, matching a basic equivalence.",
         ["at pH 1 only", "only at half-equivalence", "in the salt bridge"]),
        ("Kw=[H⁺][OH⁻]=1.0×10⁻¹⁴ at 25°C. In 0.010 M HCl, [OH⁻] is:",
         "1.0×10⁻¹² M", "10⁻¹⁴/0.010=1.0×10⁻¹².",
         ["0.010 M", "7 M", "1.0×10⁻⁷ M"]),
        ("AP Stretch: Calculate pH of 0.080 M HCl and of 0.080 M HA with Ka=2.0×10⁻⁶. Check the 5% rule for the weak acid.",
         "pH=1.10 vs pH=3.40; x/C=0.50% so √(Ka C) holds",
         "Strong: [H⁺]=0.080, pH=1.10. Weak: √(Ka C)=√(1.6×10⁻⁷)=4.00×10⁻⁴, pH=3.40. 4.00×10⁻⁴/0.080=0.50%<5%.",
         ["both pH=1.10", "both pH=6", "weak acid pH=2.00 from treating it as strong"]),
        ("AP Stretch: A buffer is 0.30 M HA and 0.10 M A⁻, pKa=4.74. Compute pH, then the pH after adding 0.02 mol NaOH to 1.00 L (no volume change).",
         "start 4.26; after 4.37",
         "Start: 4.74+log(0.10/0.30)=4.74+log(1/3)=4.74−0.477=4.26. After: HA=0.28, A⁻=0.12; 4.74+log(0.12/0.28)=4.74+log(0.429)=4.74−0.368=4.37.",
         ["7.00 then 13", "4.74 both times", "1.00 then 2.00"]),
        ("AP Stretch: Sketch the regions of a weak-acid / strong-base curve: (i) start, (ii) buffer, (iii) half-eq, (iv) eq. pt., (v) excess base. Give pH comparisons to 7 and to pKa.",
         "start pH from Ka; buffer pH≈pKa; half-eq pH=pKa; eq pH>7; excess like dilute NaOH",
         "That sequence is the FRQ map of the curve.",
         ["all regions pH=7", "eq pH<7", "half-eq pH=14"]),
        ("AP Stretch: For Ag⁺+e⁻→Ag, n=1, E°=0.80 V. If Q=10, is E less than, equal to, or greater than 0.80 V, and why (Nernst qualitative)?",
         "less than 0.80 V because log Q>0 so you subtract (0.059/1)log 10",
         "log 10=1; subtract 0.059 V; E=0.80−0.059=0.74 V. Still positive, so still galvanic, just below E°.",
         ["greater than 0.80 V", "E=0", "E=0.80 V because Q does not appear"]),
        ("AP Stretch: Identify anode, cathode, electron flow, and a salt-bridge cation direction for Zn(s)|Zn²⁺||Cu²⁺|Cu(s).",
         "Zn anode, Cu cathode, e⁻ through the wire Zn→Cu, cations in the bridge toward the Cu beaker",
         "The cathode beaker loses + charge as Cu²⁺ becomes Cu, so cations enter that side.",
         ["Cu anode, electrons through the salt bridge", "both electrodes anodes", "anions toward Cu only as the only ion motion"]),
        ("AP Stretch: 40.0 mL of 0.0800 M HA (Ka=2.0×10⁻⁵) is titrated with 0.0800 M NaOH. pH at 20.0 mL base (half-eq) and the volume of base at equivalence?",
         "pH=4.70; 40.0 mL",
         "Half-eq: pH=pKa=−log(2.0×10⁻⁵)=4.70. Equivalence: equal moles, 40.0 mL of the same-concentration base.",
         ["pH=7.00; 20.0 mL", "pH=1.00; 80.0 mL", "pH=5.00; 25.0 mL from a different titration"]),
        ("AP Stretch: Compute [H⁺] and pH of 0.20 M HA, Ka=2.0×10⁻⁵, with √(Ka C), and state whether 5% holds.",
         "[H⁺]=2.0×10⁻³ M; pH=2.70; 1.0% so OK",
         "√(4.0×10⁻⁶)=2.0×10⁻³; −log(0.0020)=2.70; 0.0020/0.20=1.0%.",
         ["[H⁺]=0.20 M; pH=0.70", "[H⁺]=2.0×10⁻⁵; pH=4.70", "5% fails so [H⁺]=0"]),
        ("AP Stretch: Why does E decrease as a galvanic cell runs, even though E° is fixed?",
         "Q increases as products form and reactants are consumed, so (0.059/n)log Q grows and E falls toward 0",
         "Nernst, not a change of the standard tables.",
         ["E° decreases with time", "the salt bridge uses up electrons", "n becomes zero"]),
        ("AP Stretch: A student claims 0.010 M acetic acid has pH=2 because “all acids at 0.010 M have pH=2.” Refute with a calculation for Ka=1.8×10⁻⁵.",
         "pH=3.37, not 2; [H⁺]=√(Ka C)=√(1.8×10⁻⁷)=4.24×10⁻⁴ M",
         "√(1.8×10⁻⁷)=4.24×10⁻⁴; −log(4.24×10⁻⁴)=3.37. Only strong monoprotic acids have [H⁺]=C. 4.24×10⁻⁴/0.010=4.2%<5%, so the square-root step is acceptable.",
         ["the student is correct; pH=2.00", "pH=12", "pH=1.8×10⁻⁵"]),
    ])


def build_unit8():
    title = "AP Chemistry Unit 8: Acids, Bases, and Electrochemistry"
    description = (
        "Strong-acid pH arithmetic, weak-acid Ka, buffers, titration-curve regions, galvanic cells, and "
        "qualitative Nernst reasoning."
    )
    c1 = concept_block(
        "1. pH and strong acids",
        [
            "pH is a compact way to report $[H^+]$: $\\mathrm{pH}=-\\log[H^+]$ with $[H^+]$ in mol/L. Because "
            "the scale is logarithmic, each pH unit is a ten-fold change in acidity. pH $2$ is ten times as "
            "acidic (in $[H^+]$) as pH $3$.",
            "A strong acid is essentially $100\\%$ ionized in water. For monoprotic HCl, HBr, HI, HNO₃, HClO₄ "
            "(and the first proton of H₂SO₄), $[H^+]$ equals the formal concentration. So $0.010$ M HCl has "
            "$[H^+]=0.010$ M and $\\mathrm{pH}=-\\log(0.010)=2.00$. That arithmetic is non-negotiable on AP.",
            "Strong bases (Group 1 hydroxides, Ba(OH)₂) supply OH⁻ completely. $0.010$ M NaOH has $\\mathrm{pOH}=2.00$. "
            "At $25^\\circ$C, $\\mathrm{pH}+\\mathrm{pOH}=14.00$, so $\\mathrm{pH}=12.00$. Also $[OH^-]=K_w/[H^+]$ "
            "with $K_w=1.0\\times10^{-14}$: in $0.010$ M HCl, $[OH^-]=1.0\\times10^{-12}$ M.",
            "Water's own $[H^+]=1.0\\times10^{-7}$ at $25^\\circ$C is negligible next to $0.010$ M strong acid. "
            "You do not add $10^{-7}$ to $0.010$ for pH $2.00$. You would worry about water only at extremely "
            "tiny strong-acid concentrations.",
            "pH $4.00$ means $[H^+]=1.0\\times10^{-4}$ M. Inverting is $10^{-\\mathrm{pH}}$. Mixing up $-\\log(0.010)$ "
            "with $0.010$ itself is how pH “$0.010$” appears as a trap answer.",
            "Strong vs weak is about extent of ionization, not about whether the formula contains H. $0.010$ M "
            "acetic acid is not pH $2$. That contrast is the next concept.",
        ],
        "pH $2$ for $0.010$ M HCl is the calibration check for the whole acid unit. If this is shaky, every "
        "buffer and titration number will be shaky.",
        "Identify strong vs weak. If strong and monoprotic, $[H^+]=C$, then $\\mathrm{pH}=-\\log C$. For strong "
        "base, find pOH first, then $14.00-\\mathrm{pOH}$ at $25^\\circ$C.",
        lesson_figure(
            beaker_svg("0.010 M HCl → pH 2"),
            "Strong acid: every HA dumped into the beaker is already H⁺ + A⁻",
            "Ten millimoles of HCl in one liter means 0.010 mol of H⁺. −log(0.010)=2.00. No ICE table is required.",
        )
        + solved(1, "pH of $0.010$ M HCl?",
               ["HCl is strong: $[H^+]=0.010$ M.",
                "$\\mathrm{pH}=-\\log(1.0\\times10^{-2})$.",
                "$\\mathrm{pH}=2.00$."],
               "$2.00$", "", "Easy")
        + solved(2, "pH of $0.010$ M NaOH at $25^\\circ$C?",
                 ["$[OH^-]=0.010$ M, $\\mathrm{pOH}=2.00$.",
                  "$\\mathrm{pH}=14.00-2.00=12.00$.",
                  "Alternatively $[H^+]=K_w/[OH^-]=1.0\\times10^{-12}$, pH $12.00$."],
                 "$12.00$", "", "Medium")
        + solved(3, "pH of $0.0010$ M HCl, and $[OH^-]$ in that solution?",
                 ["$[H^+]=1.0\\times10^{-3}$ M, pH $=3.00$.",
                  "$[OH^-]=1.0\\times10^{-14}/1.0\\times10^{-3}=1.0\\times10^{-11}$ M.",
                  "Check: pOH $=11.00$, and $3+11=14$."],
                 "pH $3.00$; $[OH^-]=1.0\\times10^{-11}$ M", "", "Hard"),
        ("Reporting pH $=0.010$ for $0.010$ M HCl",
         "pH is the log, not the concentration copied into the answer blank. $-\\log(0.010)=2$."),
        ("Write $[H^+]$ first, then take $-\\log$",
         "Two lines prevent treating $0.10$ M HCl as pH $0.10$ or as pH $10$."),
        [
            "I can compute pH of strong monoprotic acids including $0.010$ M HCl $=2$.",
            "I can convert pOH of a strong base to pH using $14.00$ at $25^\\circ$C.",
            "I can find $[OH^-]$ in acid from $K_w$.",
        ],
        1,
    )
    c2 = concept_block(
        "2. Weak acids and Ka",
        [
            "A weak acid HA only partly ionizes: HA⇌H⁺+A⁻. The acid-dissociation constant is "
            "$K_a=[H^+][A^-]/[HA]$. A small $K_a$ means the equilibrium lies left — mostly molecules, few ions. "
            "Acetic acid's $K_a\\approx 1.8\\times10^{-5}$ is typical.",
            "ICE with $[HA]_0=C$, $x=[H^+]=[A^-]$: $K_a=x^2/(C-x)$. If $x\\ll C$, $x\\approx\\sqrt{K_a C}$. "
            "For $C=0.10$ M and $K_a=1.0\\times10^{-5}$, $x=\\sqrt{1.0\\times10^{-6}}=1.0\\times10^{-3}$ M, "
            "pH $=3.00$. Percent ionized $=1.0\\%$, under $5\\%$, so the approximation holds.",
            "Compare: $0.010$ M HCl is pH $2.00$, but $0.010$ M HA with $K_a=1.0\\times10^{-5}$ has "
            "$x=\\sqrt{1.0\\times10^{-7}}=3.16\\times10^{-4}$, pH $=3.50$. Same formal concentration, different "
            "pH, because the weak acid is not fully ionized.",
            "After you compute $x$, always check $x/C$. If it exceeds about $5\\%$, solve the quadratic "
            "$x^2+K_a x-K_a C=0$. AP loves cases where the square-root shortcut is legal.",
            "The conjugate base A⁻ has $K_b=K_w/K_a$. For $K_a=1.0\\times10^{-5}$, $K_b=1.0\\times10^{-9}$. A "
            "solution of NaA is therefore weakly basic: A⁻+H₂O⇌HA+OH⁻.",
            "Stronger weak acid means larger $K_a$, smaller pKa ($\\mathrm{p}K_a=-\\log K_a$), more $x$, lower pH "
            "at the same $C$. Do not confuse $K_a$ with pH itself.",
        ],
        "Weak-acid ICE is the last major equilibrium calculation of the course and the on-ramp to buffers. "
        "The square-root shortcut must be earned by the 5% check.",
        "Write ICE, set $K_a=x^2/(C-x)$, try $x=\\sqrt{K_a C}$, check 5%, then pH $=-\\log x$. If 5% fails, "
        "quadratic.",
        lesson_figure(
            _ice_table(
                "Weak-acid ICE (0.10 M HA, Ka=1.0e-5)",
                [("HA", "0.10", "−x", "0.10−x"), ("H⁺", "0", "+x", "x"), ("A⁻", "0", "+x", "x")],
            ),
            "Most HA remains HA when Ka is 10⁻⁵",
            "x=0.0010 leaves 0.099 M HA. Calling this “fully ionized” would wrongly give pH 1.",
        )
        + solved(4, "$0.10$ M HA, $K_a=1.0\\times10^{-5}$. Approximate $[H^+]$ and pH.",
               ["$x=\\sqrt{(1.0\\times10^{-5})(0.10)}=\\sqrt{1.0\\times10^{-6}}$.",
                "$x=1.0\\times10^{-3}$ M.",
                "pH $=3.00$."],
               "$[H^+]=1.0\\times10^{-3}$ M; pH $3.00$", "", "Easy")
        + solved(5, "Does the 5% rule hold for that calculation?",
                 ["$x/C=0.0010/0.10=0.010$.",
                  "$1.0\\%<5\\%$.",
                  "The approximation is acceptable."],
                 "yes, $1.0\\%$", "", "Medium")
        + solved(6, "$0.010$ M HA, $K_a=1.0\\times10^{-5}$. Find pH and compare with $0.010$ M HCl.",
                 ["$x=\\sqrt{(1.0\\times10^{-5})(0.010)}=\\sqrt{1.0\\times10^{-7}}=3.16\\times10^{-4}$.",
                  "pH $=-\\log(3.16\\times10^{-4})=3.50$.",
                  "$0.010$ M HCl is pH $2.00$.",
                  "The weak acid is far less ionized, so its pH is higher (less acidic)."],
                 "pH $3.50$ vs $2.00$ for HCl", "", "Hard"),
        ("Setting $[H^+]$ equal to the formal concentration of a weak acid",
         "That is the strong-acid shortcut. For acetic acid it overstates $[H^+]$ by a factor of about $25$ at "
         "$0.10$ M, which wrecks pH by more than one unit."),
        ("Box $\\sqrt{K_a C}$, then box the 5% check",
         "Two boxes. If the second fails, you know to go quadratic before you report pH."),
        [
            "I can write $K_a$ and the weak-acid ICE.",
            "I can use $x=\\sqrt{K_a C}$ and the 5% rule.",
            "I can contrast pH of $0.010$ M HCl with a weak acid at the same $C$.",
        ],
        6,
    )
    c3 = concept_block(
        "3. Buffers",
        [
            "A buffer is a mixture of a weak acid and its conjugate base (or a weak base and its conjugate acid) "
            "in comparable amounts. It resists pH change when you add small quantities of strong acid or strong "
            "base. $0.10$ M HCl is not a buffer; $0.10$ M acetic acid plus $0.10$ M acetate is.",
            "The Henderson–Hasselbalch equation is $\\mathrm{pH}=\\mathrm{p}K_a+\\log([A^-]/[HA])$. It is just "
            "the $K_a$ expression solved for pH. If $[A^-]=[HA]$, the log is zero and pH $=\\mathrm{p}K_a$. That "
            "is also the half-equivalence point of a weak-acid titration.",
            "Numeric: $\\mathrm{p}K_a=4.74$, $[A^-]=0.20$ M, $[HA]=0.10$ M. $\\log(2)=0.30$, so "
            "pH $=4.74+0.30=5.04$. If the ratio is $1/3$, $\\log(1/3)=-0.48$, pH $=4.26$.",
            "Adding strong acid converts A⁻ into HA (A⁻+H⁺→HA). The ratio $[A^-]/[HA]$ falls a little and pH "
            "drops a little. Adding strong base converts HA into A⁻. A buffer is exhausted when one component "
            "is used up — capacity, not magic.",
            "Diluting a buffer (same factor for HA and A⁻) leaves the ratio, hence the pH, nearly the same. "
            "Capacity falls because there are fewer moles to absorb incoming H⁺ or OH⁻.",
            "Choose a buffer whose $\\mathrm{p}K_a$ is near the target pH, and keep the ratio between about $0.1$ "
            "and $10$. HCl/NaCl is not that pair.",
        ],
        "Buffers are how blood, lakes, and many labs hold pH still. They are also the long middle of a weak-acid "
        "titration curve.",
        "Identify HA and A⁻. Plug the ratio into Henderson–Hasselbalch. For an add-on of strong acid or base, "
        "update the moles of HA and A⁻ first, then recompute the log term.",
        lesson_figure(
            _buffer_beaker(),
            "A buffer beaker contains both HA and A⁻",
            "Blue and red particles together. Incoming H⁺ is absorbed by A⁻; incoming OH⁻ is absorbed by HA. "
            "The ratio changes only a little if both reservoirs are large.",
        )
        + solved(7, "pH of a buffer with $[HA]=[A^-]$ and $\\mathrm{p}K_a=4.74$?",
               ["$\\log(1)=0$.",
                "pH $=4.74+0=4.74$.",
                "Equal-mole buffers sit at pKa."],
               "$4.74$", "", "Easy")
        + solved(8, "$\\mathrm{p}K_a=4.74$, $[A^-]=0.20$, $[HA]=0.10$. Find pH.",
                 ["Ratio $=2.00$.",
                  "$\\log 2=0.30$.",
                  "pH $=4.74+0.30=5.04$."],
                 "$5.04$", "", "Medium")
        + solved(9, "$1.00$ L of $0.10$ M HA and $0.10$ M A⁻, $\\mathrm{p}K_a=4.74$. Add $0.01$ mol HCl (no volume change). New pH?",
                 ["H⁺ converts $0.01$ mol A⁻ into HA.",
                  "New: HA $=0.11$ mol, A⁻ $=0.09$ mol.",
                  "pH $=4.74+\\log(0.09/0.11)=4.74+\\log(0.818)=4.74-0.087=4.65$.",
                  "Without a buffer, $0.01$ M HCl would be pH $2.00$. The buffer held near $4.7$."],
                 "$4.65$", "", "Hard"),
        ("Calling any solution that contains a weak acid a buffer",
         "You need both members of the pair in meaningful amounts. Pure $0.10$ M HA is a weak-acid ICE, not a "
         "buffer, until you add A⁻ (or titrate in some OH⁻)."),
        ("Update moles of HA and A⁻ before using Henderson–Hasselbalch",
         "The log needs the new ratio after the strong acid or base is consumed. Using the old ratio ignores "
         "the whole point of capacity."),
        [
            "I can define a buffer as weak acid plus conjugate base.",
            "I can use Henderson–Hasselbalch, including pH=pKa when the ratio is 1.",
            "I can recompute pH after adding a small amount of strong acid or base.",
        ],
        11,
    )
    c4 = concept_block(
        "4. Titration curves",
        [
            "A titration curve is pH versus volume of titrant. For strong acid with strong base, pH starts low, "
            "rises slowly, then jumps almost vertically through $7$ at equivalence ($25^\\circ$C), then levels "
            "off in excess base. The salt (NaCl-type) is pH-neutral.",
            "For a weak acid with strong base the start is the weak-acid ICE (pH higher than the strong-acid "
            "twin at the same $C$). As soon as some A⁻ appears, you are in a buffer region. At half-equivalence, "
            "$[HA]=[A^-]$ and pH $=\\mathrm{p}K_a$. Equivalence is basic because A⁻ hydrolyzes. Excess base "
            "looks like dilute NaOH.",
            "Those five regions — (i) initial HA, (ii) buffer, (iii) half-eq, (iv) eq. pt., (v) excess OH⁻ — are "
            "the FRQ map. Label them on the sketch before computing a single pH.",
            "Volume at equivalence still comes from mole matching, as in Unit 4. $25.0$ mL of $0.100$ M HA needs "
            "$25.0$ mL of $0.100$ M NaOH. Half of that, $12.5$ mL, is the pKa point.",
            "Indicators change color in a pH range of about two units. Pick one whose range overlaps the steep "
            "jump. Phenolphthalein (~8–9) fits SA/SB and most WA/SB equivalences; it does not mark half-equivalence.",
            "Reading a curve: the buffer is the relatively flat stretch before the jump. The jump's midpoint "
            "is equivalence. A weak-base / strong-acid curve is the upside-down cousin (eq. pH $<7$).",
        ],
        "Titration curves combine Units 4, 7, and 8 in one picture. If you can name the region, you know which "
        "equation to use (strong pH, Ka ICE, HH, Kb of A⁻, or excess OH⁻).",
        "Find the equivalence volume first. Halve it for pKa. Then identify which region the asked volume is in "
        "and only then compute pH.",
        lesson_figure(
            titration_svg() + _weak_acid_curve(),
            "Left: strong-acid / strong-base jump through ~7. Right: weak acid, half-eq marked, eq. pH>7",
            "The red dot is half-equivalence, pH=pKa. The vertical rise after that is equivalence, sitting "
            "above 7 because A⁻ is a weak base.",
        )
        + solved(10, "Equivalence pH of HCl titrated with NaOH at $25^\\circ$C?",
               ["The salt is NaCl, a spectator pair.",
                "The solution is like water plus Na⁺ and Cl⁻.",
                "pH near $7$."],
               "about $7$", "", "Easy")
        + solved(11, "$25.0$ mL of $0.100$ M HA with $0.100$ M NaOH. Volume at half-equivalence, and pH if $\\mathrm{p}K_a=5.00$?",
                 ["Equivalence volume $=25.0$ mL (equal moles).",
                  "Half $=12.5$ mL.",
                  "There pH $=\\mathrm{p}K_a=5.00$."],
                 "$12.5$ mL; pH $5.00$", "", "Medium")
        + solved(12, "Why is the WA/SB equivalence pH greater than $7$?",
                 ["At equivalence, HA has been converted to A⁻.",
                  "A⁻ is the conjugate base of a weak acid, so it has a $K_b=K_w/K_a>0$.",
                  "A⁻+H₂O⇌HA+OH⁻ makes the solution basic.",
                  "A strong-acid equivalence lacks this hydrolysis."],
                 "A⁻ is a weak base", "", "Hard"),
        ("Using pH $=7$ at equivalence for every titration",
         "Only the strong/strong case sits at $7$ (at $25^\\circ$C). Weak-acid equivalence is basic; weak-base "
         "equivalence is acidic."),
        ("Mark $V_e$ and $V_e/2$ on the volume axis before reading pH",
         "Those two ticks tell you whether you are in the buffer, at pKa, at equivalence, or in excess titrant."),
        [
            "I can describe SA/SB vs WA/SB curve shapes.",
            "I can identify half-equivalence as pH=pKa.",
            "I can explain why weak-acid equivalence is basic.",
        ],
        16,
    )
    c5 = concept_block(
        "5. Galvanic cells",
        [
            "A galvanic (voltaic) cell turns a spontaneous redox reaction into electron flow through a wire. "
            "Oxidation happens at the anode; reduction happens at the cathode. Electrons travel in the wire from "
            "anode to cathode — they do not swim through the salt bridge.",
            "The Daniell cell is the teaching picture: a zinc strip in Zn²⁺(aq) and a copper strip in Cu²⁺(aq), "
            "connected by a wire and a salt bridge. Zinc is oxidized (anode, often marked −): "
            "$\\mathrm{Zn\\rightarrow Zn^{2+}+2e^-}$. Copper ion is reduced (cathode, +): "
            "$\\mathrm{Cu^{2+}+2e^-\\rightarrow Cu}$. Overall $\\mathrm{Zn+Cu^{2+}\\rightarrow Zn^{2+}+Cu}$.",
            "$E^\\circ_\\mathrm{cell}=E^\\circ_\\mathrm{cathode}-E^\\circ_\\mathrm{anode}$ using reduction "
            "potentials. $E^\\circ_{Cu}=+0.34$ V, $E^\\circ_{Zn}=-0.76$ V, so $E^\\circ=0.34-(-0.76)=1.10$ V. "
            "A positive $E$ means the cell reaction as written is thermodynamically favored ($\\Delta G=-nFE<0$).",
            "The salt bridge lets ions move so each beaker stays electrically neutral. Cations in the bridge "
            "drift toward the cathode (which is losing Cu²⁺ from solution as Cu metal plates out). Anions drift "
            "toward the anode (which is producing extra Zn²⁺).",
            "If you drop Zn metal into a single beaker of Cu²⁺, the same redox happens, but the energy is heat, "
            "not a useful current. Separating the half-reactions is what makes a cell.",
            "Line notation Zn(s)|Zn²⁺||Cu²⁺|Cu(s) puts the anode on the left. The double bar is the salt bridge. "
            "Learn to translate that into a two-beaker sketch.",
        ],
        "Electrochemistry is Unit 4 redox plus a wire. If anode/cathode labels are reversed, every Nernst "
        "story in the next concept collapses.",
        "Write the two half-reactions. Oxidation = anode = electron source. Reduction = cathode = electron sink. "
        "Compute $E^\\circ$ from reduction potentials. Sketch the bridge ions toward the cathode.",
        lesson_figure(
            _galvanic_svg(),
            "Zn/Cu galvanic cell (two beakers, salt bridge, electron flow in the wire)",
            "This is not a Punnett square and not a series of resistors. Massive Zn anode, copper cathode, "
            "ions in each solution, gel bridge on top, e⁻ in the metal wire.",
        )
        + solved(13, "In the Daniell cell, which metal is the anode and what happens to it?",
               ["Zn is oxidized.",
                "Oxidation is defined to occur at the anode.",
                "The zinc strip loses mass as Zn²⁺ enters the left beaker."],
               "Zn anode, dissolving", "", "Easy")
        + solved(14, "$E^\\circ_{Cu}=0.34$ V, $E^\\circ_{Zn}=-0.76$ V. Find $E^\\circ_\\mathrm{cell}$.",
                 ["Copper ion is reduced: cathode potential $0.34$ V.",
                  "Zinc is oxidized: anode reduction potential $-0.76$ V.",
                  "$E^\\circ=0.34-(-0.76)=1.10$ V."],
                 "$1.10$ V", "", "Medium")
        + solved(15, "Which way do cations in the salt bridge move, and why?",
                 ["At the cathode, Cu²⁺ becomes Cu(s), so that beaker would go negative without extra cations.",
                  "Cations in the bridge flow toward the Cu beaker.",
                  "Anions flow toward the Zn beaker to balance the new Zn²⁺.",
                  "Electrons themselves stay in the wire."],
                 "cations toward the cathode (Cu side)", "", "Hard"),
        ("Sending electrons through the salt bridge",
         "The bridge carries ions. Electrons move in metal. Mixing those paths is the most common cell-diagram "
         "error on the exam."),
        ("Label + and − after you know which side is reduction",
         "In galvanic cells the cathode is +. If you label before assigning oxidation/reduction, the signs "
         "often come out backwards."),
        [
            "I can assign anode (ox) and cathode (red) in a galvanic cell.",
            "I can compute $E^\\circ=1.10$ V for Zn/Cu from tabulated potentials.",
            "I can describe electron flow in the wire and ion flow in the bridge.",
        ],
        21,
    )
    c6 = concept_block(
        "6. Nernst qualitative",
        [
            "Standard potentials assume $1$ M ions (and $1$ bar gases). Real cells use other concentrations, so "
            "the voltage $E$ is not exactly $E^\\circ$. The Nernst equation at $25^\\circ$C is "
            "$E=E^\\circ-\\dfrac{0.059}{n}\\log Q$, where $n$ is the moles of electrons in the balanced cell "
            "reaction and $Q$ is the reaction quotient of that cell reaction.",
            "You do not need to derive Nernst. You need the qualitative consequences. If $Q$ increases (more "
            "product ions, fewer reactant ions), $\\log Q$ increases and $E$ decreases — the cell is less "
            "driving. If $Q$ decreases, $E$ increases. If $Q=1$, $E=E^\\circ$. If $Q=K$, $E=0$ (dead battery, "
            "equilibrium).",
            "For Zn+Cu²⁺→Zn²⁺+Cu, $Q=[Zn^{2+}]/[Cu^{2+}]$ (solids omitted) and $n=2$. Raising $[Cu^{2+}]$ shrinks "
            "$Q$ and raises $E$. Raising $[Zn^{2+}]$ grows $Q$ and lowers $E$. Running the cell produces Zn²⁺ and "
            "consumes Cu²⁺, so $Q$ climbs and $E$ sags toward zero — that is why a battery dies.",
            "Numeric feel: $E^\\circ=1.10$ V, $n=2$, $Q=100$, $\\log 100=2$, subtract $(0.059/2)\\times 2=0.059$ V, "
            "so $E=1.04$ V. Still galvanic, just a bit weaker.",
            "A concentration cell has the same half-reaction in both beakers, so $E^\\circ=0$. Voltage exists "
            "only because $Q\\neq 1$. Electrons flow until the ion concentrations equalize and $E$ hits $0$.",
            "Connect to Unit 6: $E>0$ means $\\Delta G<0$. $E=0$ means $\\Delta G=0=Q=K$. Nernst is Gibbs in "
            "electrical clothing.",
        ],
        "Nernst is how AP Chemistry asks whether you understand $Q$ in a cell. It is Le Chatelier with a "
        "voltmeter.",
        "Write $Q$ for the cell reaction. If the prompt made $Q$ larger, $E$ fell. If $Q=K$, $E=0$. Mention $n$ "
        "only when you need the $0.059/n$ size.",
        lesson_figure(
            _galvanic_svg(),
            "As the cell runs, [Zn²⁺] rises and [Cu²⁺] falls — Q grows, E falls",
            "E° on the data sheet stays 1.10 V. The measured voltage does not, because Q is no longer 1.",
        )
        + solved(16, "If $Q$ increases in a galvanic cell, what happens to $E$?",
               ["Nernst subtracts a term with $\\log Q$.",
                "Larger $Q$ → larger log → larger subtraction.",
                "$E$ decreases."],
               "$E$ decreases", "", "Easy")
        + solved(17, "What is $E$ when $Q=K$?",
                 ["That is equilibrium.",
                  "No net driving force remains.",
                  "$E=0$ (dead cell). $E^\\circ$ is not zero unless $K=1$."],
                 "$0$", "", "Medium")
        + solved(18, "$E^\\circ=1.10$ V, $n=2$, $Q=100$. Estimate $E$ and interpret.",
                 ["$\\log 100=2$.",
                  "$(0.059/2)\\times 2=0.059$ V.",
                  "$E=1.10-0.059=1.04$ V.",
                  "Still positive: the cell still runs, just with a smaller voltage than standard."],
                 "$1.04$ V (still galvanic)", "", "Hard"),
        ("Thinking $E^\\circ$ changes as the battery runs",
         "$E^\\circ$ is a table value at standard states. The measured $E$ changes because $Q$ changes. Keep "
         "those symbols separate."),
        ("Write $Q$ for the cell reaction before arguing “more product”",
         "Once $Q=[Zn^{2+}]/[Cu^{2+}]$ is on the page, every concentration change has an obvious effect on $E$."),
        [
            "I can state that larger $Q$ means smaller $E$.",
            "I can identify $E=0$ at equilibrium ($Q=K$).",
            "I can apply Nernst qualitatively (and with a simple log 100 example) to Zn/Cu.",
        ],
        26,
    )
    content = unit_shell(
        title, AUDIENCE,
        ["pH and strong acids", "Weak acids and Ka", "Buffers",
         "Titration curves", "Galvanic cells", "Nernst qualitative"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [
        ('Atomic Structure and Properties',
         ['Moles and molar mass', 'Mass spectroscopy', 'Electron configuration',
          'Photoelectron spectroscopy', 'Periodic trends', 'Coulombic attraction']),
        ('Molecular and Ionic Structure',
         ['Ionic vs covalent bonding', 'Lewis structures', 'VSEPR and shape',
          'Hybridization intro', 'Bond polarity', 'Resonance and formal charge']),
        ('Intermolecular Forces and Properties',
         ['IMFs', 'Solids liquids gases particulate', 'Ideal gas law',
          'Kinetic molecular theory', 'Solutions and molarity', 'Chromatography and spectroscopy']),
        ('Chemical Reactions',
         ['Net ionic equations', 'Stoichiometry', 'Limiting reactant',
          'Titration intro', 'Redox identification', 'Types of reactions']),
        ('Kinetics',
         ['Rate laws from data', 'Integrated rate laws', 'Collision theory',
          'Reaction mechanisms', 'Catalysts', 'Arrhenius qualitative']),
        ('Thermodynamics',
         ['Calorimetry', 'Enthalpy and Hess', 'Entropy',
          'Gibbs free energy', 'Thermo and equilibrium link', 'Energy diagrams']),
        ('Equilibrium',
         ['K vs Q', 'Calculating K', 'Le Chatelier',
          'Solubility product', 'ICE tables', 'Coupled equilibria']),
        ('Acids, Bases, and Electrochemistry',
         ['pH and strong acids', 'Weak acids and Ka', 'Buffers',
          'Titration curves', 'Galvanic cells', 'Nernst qualitative']),
    ]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>AP Chemistry Complete</h1>"
        f"<p><strong>For:</strong> <strong>AP Chemistry</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
