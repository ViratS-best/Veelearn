"""Physical Science units 1–4: Grade 9 / first high-school science."""
from __future__ import annotations

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, mq, fill_qs,
    xy_graph, sample_curve, number_line,
    fbd_box, atom_shells_svg, beaker_svg,
)
from .common import AUDIENCE, STRETCH_LABEL


def _pack(rows):
    return [mq(t, a, e, i, distractors=list(d)) for i, (t, a, e, d) in enumerate(rows, 1)]


def _with_ican(html, items):
    ican = "<h4>I can</h4><ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>\n"
    marker = "<h3>Quick practice"
    if marker in html:
        return html.replace(marker, ican + marker, 1)
    return html + ican


def _states_svg():
    return (
        '<svg viewBox="0 0 420 170" width="100%" style="max-width:420px" role="img">'
        '<rect x="12" y="28" width="120" height="110" fill="#fee2e2" stroke="#991b1b" stroke-width="2"/>'
        '<rect x="150" y="28" width="120" height="110" fill="#dbeafe" stroke="#1e40af" stroke-width="2"/>'
        '<rect x="288" y="28" width="120" height="110" fill="#ecfccb" stroke="#3f6212" stroke-width="2"/>'
        '<circle cx="40" cy="58" r="7" fill="#b91c1c"/><circle cx="62" cy="58" r="7" fill="#b91c1c"/>'
        '<circle cx="84" cy="58" r="7" fill="#b91c1c"/><circle cx="40" cy="80" r="7" fill="#b91c1c"/>'
        '<circle cx="62" cy="80" r="7" fill="#b91c1c"/><circle cx="84" cy="80" r="7" fill="#b91c1c"/>'
        '<circle cx="40" cy="102" r="7" fill="#b91c1c"/><circle cx="62" cy="102" r="7" fill="#b91c1c"/>'
        '<circle cx="84" cy="102" r="7" fill="#b91c1c"/>'
        '<circle cx="172" cy="70" r="7" fill="#1d4ed8"/><circle cx="198" cy="88" r="7" fill="#1d4ed8"/>'
        '<circle cx="226" cy="64" r="7" fill="#1d4ed8"/><circle cx="180" cy="108" r="7" fill="#1d4ed8"/>'
        '<circle cx="214" cy="112" r="7" fill="#1d4ed8"/><circle cx="240" cy="92" r="7" fill="#1d4ed8"/>'
        '<circle cx="318" cy="52" r="6" fill="#4d7c0f"/><circle cx="368" cy="70" r="6" fill="#4d7c0f"/>'
        '<circle cx="340" cy="100" r="6" fill="#4d7c0f"/><circle cx="390" cy="48" r="6" fill="#4d7c0f"/>'
        '<circle cx="312" cy="118" r="6" fill="#4d7c0f"/>'
        '<text x="72" y="22" text-anchor="middle" font-size="12">solid</text>'
        '<text x="210" y="22" text-anchor="middle" font-size="12">liquid</text>'
        '<text x="348" y="22" text-anchor="middle" font-size="12">gas</text>'
        "</svg>"
    )


def _density_svg():
    return (
        '<svg viewBox="0 0 340 180" width="100%" style="max-width:340px" role="img">'
        '<rect x="40" y="50" width="90" height="90" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
        '<rect x="200" y="50" width="90" height="90" fill="#fecaca" stroke="#991b1b" stroke-width="2"/>'
        '<text x="85" y="42" text-anchor="middle" font-size="12">same size</text>'
        '<text x="245" y="42" text-anchor="middle" font-size="12">same size</text>'
        '<text x="85" y="100" text-anchor="middle" font-size="13">8 g</text>'
        '<text x="245" y="100" text-anchor="middle" font-size="13">24 g</text>'
        '<text x="85" y="158" text-anchor="middle" font-size="12">lower density</text>'
        '<text x="245" y="158" text-anchor="middle" font-size="12">higher density</text>'
        "</svg>"
    )


def _ruler_svg():
    return (
        '<svg viewBox="0 0 380 120" width="100%" style="max-width:380px" role="img">'
        '<rect x="20" y="36" width="340" height="36" fill="#fef9c3" stroke="#854d0e" stroke-width="2"/>'
        '<line x1="40" y1="36" x2="40" y2="72" stroke="#0f172a"/>'
        '<line x1="100" y1="36" x2="100" y2="72" stroke="#0f172a"/>'
        '<line x1="160" y1="36" x2="160" y2="72" stroke="#0f172a"/>'
        '<line x1="220" y1="36" x2="220" y2="72" stroke="#0f172a"/>'
        '<line x1="280" y1="36" x2="280" y2="72" stroke="#0f172a"/>'
        '<line x1="340" y1="36" x2="340" y2="72" stroke="#0f172a"/>'
        '<text x="40" y="92" text-anchor="middle" font-size="11">0</text>'
        '<text x="100" y="92" text-anchor="middle" font-size="11">2</text>'
        '<text x="160" y="92" text-anchor="middle" font-size="11">4</text>'
        '<text x="220" y="92" text-anchor="middle" font-size="11">6</text>'
        '<text x="280" y="92" text-anchor="middle" font-size="11">8</text>'
        '<text x="340" y="92" text-anchor="middle" font-size="11">10 cm</text>'
        '<line x1="40" y1="24" x2="220" y2="24" stroke="#b91c1c" stroke-width="3"/>'
        '<text x="130" y="18" text-anchor="middle" font-size="12" fill="#b91c1c">object = 6 cm</text>'
        "</svg>"
    )


def _timeline_svg():
    return (
        '<svg viewBox="0 0 440 130" width="100%" style="max-width:440px" role="img">'
        '<line x1="30" y1="70" x2="410" y2="70" stroke="#0f172a" stroke-width="3"/>'
        '<circle cx="70" cy="70" r="8" fill="#4f46e5"/>'
        '<circle cx="170" cy="70" r="8" fill="#4f46e5"/>'
        '<circle cx="270" cy="70" r="8" fill="#4f46e5"/>'
        '<circle cx="370" cy="70" r="8" fill="#4f46e5"/>'
        '<text x="70" y="42" text-anchor="middle" font-size="11">Dalton</text>'
        '<text x="70" y="98" text-anchor="middle" font-size="11">solid ball</text>'
        '<text x="170" y="42" text-anchor="middle" font-size="11">Thomson</text>'
        '<text x="170" y="98" text-anchor="middle" font-size="11">plums in pudding</text>'
        '<text x="270" y="42" text-anchor="middle" font-size="11">Rutherford</text>'
        '<text x="270" y="98" text-anchor="middle" font-size="11">tiny nucleus</text>'
        '<text x="370" y="42" text-anchor="middle" font-size="11">Bohr</text>'
        '<text x="370" y="98" text-anchor="middle" font-size="11">electron shells</text>'
        "</svg>"
    )


def _periodic_mini_svg():
    return (
        '<svg viewBox="0 0 320 180" width="100%" style="max-width:320px" role="img">'
        '<rect x="20" y="40" width="44" height="44" fill="#fecaca" stroke="#0f172a"/>'
        '<text x="42" y="58" text-anchor="middle" font-size="11">H</text>'
        '<text x="42" y="74" text-anchor="middle" font-size="10">1</text>'
        '<rect x="256" y="40" width="44" height="44" fill="#fde68a" stroke="#0f172a"/>'
        '<text x="278" y="58" text-anchor="middle" font-size="11">He</text>'
        '<text x="278" y="74" text-anchor="middle" font-size="10">2</text>'
        '<rect x="20" y="90" width="44" height="44" fill="#93c5fd" stroke="#0f172a"/>'
        '<text x="42" y="108" text-anchor="middle" font-size="11">Li</text>'
        '<text x="42" y="124" text-anchor="middle" font-size="10">3</text>'
        '<rect x="68" y="90" width="44" height="44" fill="#86efac" stroke="#0f172a"/>'
        '<text x="90" y="108" text-anchor="middle" font-size="11">Be</text>'
        '<rect x="208" y="90" width="44" height="44" fill="#c4b5fd" stroke="#0f172a"/>'
        '<text x="230" y="108" text-anchor="middle" font-size="11">F</text>'
        '<rect x="256" y="90" width="44" height="44" fill="#fde68a" stroke="#0f172a"/>'
        '<text x="278" y="108" text-anchor="middle" font-size="11">Ne</text>'
        '<text x="42" y="28" text-anchor="middle" font-size="11">Group 1</text>'
        '<text x="278" y="28" text-anchor="middle" font-size="11">Group 18</text>'
        '<text x="12" y="64" font-size="11">P1</text>'
        '<text x="12" y="114" font-size="11">P2</text>'
        "</svg>"
    )


def _metal_strip_svg():
    return (
        '<svg viewBox="0 0 400 90" width="100%" style="max-width:400px" role="img">'
        '<rect x="16" y="24" width="120" height="44" fill="#94a3b8" stroke="#0f172a"/>'
        '<rect x="140" y="24" width="120" height="44" fill="#fde68a" stroke="#0f172a"/>'
        '<rect x="264" y="24" width="120" height="44" fill="#bbf7d0" stroke="#0f172a"/>'
        '<text x="76" y="50" text-anchor="middle" font-size="13">metals</text>'
        '<text x="200" y="50" text-anchor="middle" font-size="13">metalloids</text>'
        '<text x="324" y="50" text-anchor="middle" font-size="13">nonmetals</text>'
        "</svg>"
    )


def _bond_svg():
    return (
        '<svg viewBox="0 0 380 150" width="100%" style="max-width:380px" role="img">'
        '<circle cx="70" cy="70" r="28" fill="#fecaca" stroke="#991b1b" stroke-width="2"/>'
        '<circle cx="150" cy="70" r="22" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="2"/>'
        '<text x="70" y="74" text-anchor="middle" font-size="12">Na⁺</text>'
        '<text x="150" y="74" text-anchor="middle" font-size="12">Cl⁻</text>'
        '<text x="110" y="28" text-anchor="middle" font-size="12">ionic: transfer</text>'
        '<circle cx="250" cy="70" r="24" fill="#bbf7d0" stroke="#166534" stroke-width="2"/>'
        '<circle cx="320" cy="70" r="24" fill="#bbf7d0" stroke="#166534" stroke-width="2"/>'
        '<line x1="274" y1="70" x2="296" y2="70" stroke="#0f172a" stroke-width="4"/>'
        '<text x="285" y="28" text-anchor="middle" font-size="12">covalent: share</text>'
        '<text x="250" y="74" text-anchor="middle" font-size="12">H</text>'
        '<text x="320" y="74" text-anchor="middle" font-size="12">H</text>'
        "</svg>"
    )


def _balance_eq_svg():
    return (
        '<svg viewBox="0 0 360 130" width="100%" style="max-width:360px" role="img">'
        '<rect x="20" y="36" width="70" height="50" fill="#dbeafe" stroke="#1e3a8a"/>'
        '<rect x="100" y="36" width="70" height="50" fill="#dbeafe" stroke="#1e3a8a"/>'
        '<rect x="220" y="36" width="120" height="50" fill="#dcfce7" stroke="#166534"/>'
        '<text x="55" y="66" text-anchor="middle" font-size="13">2 H₂</text>'
        '<text x="135" y="66" text-anchor="middle" font-size="13">O₂</text>'
        '<text x="280" y="66" text-anchor="middle" font-size="13">2 H₂O</text>'
        '<text x="188" y="66" text-anchor="middle" font-size="16">→</text>'
        '<text x="180" y="112" text-anchor="middle" font-size="12">4 H and 2 O on each side</text>'
        "</svg>"
    )


def _mix_vs_compound_svg():
    return (
        '<svg viewBox="0 0 360 160" width="100%" style="max-width:360px" role="img">'
        '<rect x="30" y="30" width="130" height="100" fill="#e0f2fe" stroke="#0f172a"/>'
        '<circle cx="60" cy="60" r="8" fill="#1d4ed8"/><circle cx="90" cy="80" r="8" fill="#b91c1c"/>'
        '<circle cx="120" cy="55" r="8" fill="#1d4ed8"/><circle cx="70" cy="105" r="8" fill="#b91c1c"/>'
        '<circle cx="130" cy="100" r="8" fill="#1d4ed8"/>'
        '<text x="95" y="148" text-anchor="middle" font-size="12">mixture: still separate</text>'
        '<rect x="200" y="30" width="130" height="100" fill="#fef3c7" stroke="#0f172a"/>'
        '<circle cx="240" cy="70" r="10" fill="#7c3aed"/><circle cx="248" cy="70" r="6" fill="#fde68a"/>'
        '<circle cx="290" cy="95" r="10" fill="#7c3aed"/><circle cx="298" cy="95" r="6" fill="#fde68a"/>'
        '<text x="265" y="148" text-anchor="middle" font-size="12">compound: joined</text>'
        "</svg>"
    )


def _third_law_svg():
    return (
        '<svg viewBox="0 0 340 150" width="100%" style="max-width:340px" role="img">'
        '<circle cx="110" cy="70" r="28" fill="#93c5fd" stroke="#1e3a8a" stroke-width="2"/>'
        '<circle cx="230" cy="70" r="28" fill="#fecaca" stroke="#991b1b" stroke-width="2"/>'
        '<text x="110" y="74" text-anchor="middle" font-size="12">A</text>'
        '<text x="230" y="74" text-anchor="middle" font-size="12">B</text>'
        '<line x1="138" y1="70" x2="188" y2="70" stroke="#b91c1c" stroke-width="3"/>'
        '<polygon points="186,64 200,70 186,76" fill="#b91c1c"/>'
        '<line x1="202" y1="88" x2="152" y2="88" stroke="#1d4ed8" stroke-width="3"/>'
        '<polygon points="154,82 140,88 154,94" fill="#1d4ed8"/>'
        '<text x="170" y="28" text-anchor="middle" font-size="12" fill="#b91c1c">A pushes B</text>'
        '<text x="170" y="130" text-anchor="middle" font-size="12" fill="#1d4ed8">B pushes A</text>'
        "</svg>"
    )


def _reaction_types_svg():
    return (
        '<svg viewBox="0 0 520 280" width="100%" style="max-width:520px" role="img">'
        '<text x="12" y="22" font-size="13">synthesis A+B→AB</text>'
        '<circle cx="40" cy="48" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="40" y="52" text-anchor="middle" font-size="11">A</text>'
        '<text x="58" y="52" font-size="12">+</text>'
        '<circle cx="88" cy="48" r="12" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="88" y="52" text-anchor="middle" font-size="11">B</text>'
        '<text x="110" y="52" font-size="14">→</text>'
        '<circle cx="150" cy="48" r="16" fill="#ddd6fe" stroke="#5b21b6"/>'
        '<text x="150" y="52" text-anchor="middle" font-size="11">AB</text>'
        '<text x="220" y="22" font-size="13">decomposition AB→A+B</text>'
        '<circle cx="250" cy="48" r="16" fill="#ddd6fe" stroke="#5b21b6"/>'
        '<text x="250" y="52" text-anchor="middle" font-size="11">AB</text>'
        '<text x="276" y="52" font-size="14">→</text>'
        '<circle cx="310" cy="48" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="310" y="52" text-anchor="middle" font-size="11">A</text>'
        '<text x="328" y="52" font-size="12">+</text>'
        '<circle cx="356" cy="48" r="12" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="356" y="52" text-anchor="middle" font-size="11">B</text>'
        '<text x="12" y="100" font-size="13">single replacement A+BC→AC+B</text>'
        '<circle cx="40" cy="128" r="12" fill="#86efac" stroke="#166534"/>'
        '<text x="40" y="132" text-anchor="middle" font-size="11">A</text>'
        '<text x="58" y="132" font-size="12">+</text>'
        '<circle cx="88" cy="128" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="88" y="132" text-anchor="middle" font-size="11">B</text>'
        '<circle cx="112" cy="128" r="12" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="112" y="132" text-anchor="middle" font-size="11">C</text>'
        '<text x="134" y="132" font-size="14">→</text>'
        '<circle cx="168" cy="128" r="12" fill="#86efac" stroke="#166534"/>'
        '<text x="168" y="132" text-anchor="middle" font-size="11">A</text>'
        '<circle cx="192" cy="128" r="12" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="192" y="132" text-anchor="middle" font-size="11">C</text>'
        '<text x="214" y="132" font-size="12">+</text>'
        '<circle cx="244" cy="128" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="244" y="132" text-anchor="middle" font-size="11">B</text>'
        '<text x="12" y="172" font-size="13">double replacement AB+CD→AD+CB</text>'
        '<circle cx="40" cy="200" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="40" y="204" text-anchor="middle" font-size="11">A</text>'
        '<circle cx="64" cy="200" r="12" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="64" y="204" text-anchor="middle" font-size="11">B</text>'
        '<text x="84" y="204" font-size="12">+</text>'
        '<circle cx="116" cy="200" r="12" fill="#86efac" stroke="#166534"/>'
        '<text x="116" y="204" text-anchor="middle" font-size="11">C</text>'
        '<circle cx="140" cy="200" r="12" fill="#fde68a" stroke="#a16207"/>'
        '<text x="140" y="204" text-anchor="middle" font-size="11">D</text>'
        '<text x="162" y="204" font-size="14">→</text>'
        '<circle cx="196" cy="200" r="12" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="196" y="204" text-anchor="middle" font-size="11">A</text>'
        '<circle cx="220" cy="200" r="12" fill="#fde68a" stroke="#a16207"/>'
        '<text x="220" y="204" text-anchor="middle" font-size="11">D</text>'
        '<text x="242" y="204" font-size="12">+</text>'
        '<circle cx="272" cy="200" r="12" fill="#86efac" stroke="#166534"/>'
        '<text x="272" y="204" text-anchor="middle" font-size="11">C</text>'
        '<circle cx="296" cy="200" r="12" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="296" y="204" text-anchor="middle" font-size="11">B</text>'
        '<text x="12" y="244" font-size="13">combustion: fuel + O₂ → CO₂ + H₂O</text>'
        '<rect x="250" y="228" width="70" height="22" fill="#fef3c7" stroke="#854d0e"/>'
        '<text x="285" y="244" text-anchor="middle" font-size="11">fuel</text>'
        '<text x="330" y="244" font-size="13">+ O₂ → CO₂ + H₂O</text>'
        "</svg>"
    )


# ===========================================================================
# UNIT 1
# ===========================================================================

def _u1_questions():
    rows = [
        ("Which state of matter keeps both a definite shape and a definite volume?",
         "solid", "A solid’s particles are packed in a nearly fixed pattern, so the sample does not flow to fill a new shape.",
         ["liquid", "gas", "plasma"]),
        ("A liquid has a definite volume. What does it not have?",
         "a definite shape", "A liquid flows. It takes the shape of the bottom of its container, but its volume stays about the same.",
         ["mass", "particles", "a temperature"]),
        ("Which picture of particles best matches a gas?",
         "far apart and moving in all directions", "Gas particles fly with lots of empty space between them, so a gas fills its whole container.",
         ["locked in a tight grid", "touching and sliding past neighbors", "all stuck in one clump"]),
        ("Ice turning into liquid water is an example of…",
         "melting", "Melting is the change from solid to liquid. The particles stay H₂O; they only move more freely.",
         ["freezing", "condensation", "sublimation"]),
        ("Steam on a bathroom mirror becoming droplets is…",
         "condensation", "Condensation is gas turning into liquid. Water vapor cools and becomes liquid water on the glass.",
         ["evaporation", "melting", "freezing"]),
        ("Density is defined as…",
         "mass divided by volume", "Density tells how much stuff is packed into a space: $D=m/V$.",
         ["mass plus volume", "volume divided by mass", "mass times volume"]),
        ("A 20 g sample fills 4 cm³. What is its density?",
         "5 g/cm³", "Divide mass by volume: $20/4=5$ grams in each cubic centimeter.",
         ["80 g/cm³", "16 g/cm³", "0.2 g/cm³"]),
        ("Two blocks have equal volume. Block A is heavier. Which has greater density?",
         "Block A", "Same $V$ and larger $m$ means larger $m/V$. The heavier equal-size block is denser.",
         ["Block B", "they must be equal", "you cannot compare without the material name"]),
        ("Water’s density is about 1 g/cm³. A 9 g pebble has volume 3 cm³. In water it will…",
         "sink", "Density is $9/3=3$ g/cm³, which is greater than 1, so the pebble sinks.",
         ["float", "hover in the middle forever", "dissolve at once"]),
        ("A liquid has density 2 g/mL and volume 6 mL. What is its mass?",
         "12 g", "Rearrange $D=m/V$ to $m=D\\times V=2\\times6=12$ g.",
         ["3 g", "8 g", "0.33 g"]),
        ("Which change is physical, not chemical?",
         "ice melting", "Melting keeps the same substance (water). The particles are still H₂O molecules.",
         ["wood burning", "iron rusting", "a cake baking"]),
        ("Which observation best hints that a chemical change happened?",
         "a new substance formed", "A chemical change makes different stuff, not just a new shape or state.",
         ["the sample was poured", "the sample was frozen", "the sample was crushed"]),
        ("Crushing a sugar cube is classified as…",
         "a physical change", "You still have sugar. Only the piece size changed.",
         ["a chemical change", "a nuclear change", "a density change that creates a new element"]),
        ("Rust forming on a nail is…",
         "a chemical change", "Iron joins with oxygen to make a new substance: iron oxide (rust).",
         ["only a color trick", "a physical change because the nail is still metal-looking", "evaporation"]),
        ("Salt stirred into water can be recovered by evaporating the water. That mixture process is…",
         "physical", "The salt and water did not become a new compound. You can separate them by a physical method.",
         ["chemical, because the salt vanished", "nuclear", "impossible to classify"]),
        ("The SI unit of mass used in most lab work is the…",
         "gram (or kilogram)", "Mass is the amount of matter. We measure it in grams or kilograms, not in liters.",
         ["liter", "second", "degree Celsius"]),
        ("A box is 2 cm by 3 cm by 4 cm. Its volume is…",
         "24 cm³", "Volume of a rectangular box is length × width × height: $2\\times3\\times4=24$.",
         ["9 cm³", "18 cm³", "24 cm"]),
        ("A student needs the volume of an irregular rock. The usual tool is…",
         "a graduated cylinder and water displacement", "The rock’s volume equals the rise in water level when it is fully under the surface.",
         ["a balance only", "a thermometer", "a meterstick alone"]),
        ("How many centimeters are in 1.5 meters?",
         150, "1 m = 100 cm, so $1.5\\times100=150$ cm.",
         [15, 1.5, 1500]),
        ("Which quantity is measured in milliliters?",
         "liquid volume", "A milliliter (mL) is a volume unit. 1 mL = 1 cm³.",
         ["mass", "time", "temperature"]),
        ("Write 3400 in scientific notation.",
         "3.4 × 10³", "Move the decimal 3 places: $3400=3.4\\times10^{3}$.",
         ["34 × 10²", "3.4 × 10⁻³", "340 × 10"]),
        ("Write 0.0056 in scientific notation.",
         "5.6 × 10⁻³", "Move the decimal 3 places to the right: $0.0056=5.6\\times10^{-3}$.",
         ["5.6 × 10³", "56 × 10⁻⁴", "0.56 × 10⁻²"]),
        ("Scientists use scientific notation mainly to…",
         "write very large or very small numbers without long strings of zeros",
         "Powers of ten pack huge or tiny values into a short, readable form.",
         ["change the actual size of a sample", "replace units", "make every number an integer"]),
        ("What ordinary number is $2.0\\times10^{4}$?",
         20000, "Move the decimal 4 places to the right: 20000.",
         [200, 0.0002, 8]),
        ("Which is larger: $3\\times10^{5}$ or $4\\times10^{4}$?",
         "3 × 10⁵", "$3\\times10^{5}=300000$ and $4\\times10^{4}=40000$. Three hundred thousand is larger.",
         ["4 × 10⁴", "they are equal", "you cannot compare different powers"]),
        ("On a data graph, the independent variable is usually placed on the…",
         "horizontal axis (x-axis)", "You choose the x values (time, for example). The measured response goes on y.",
         ["vertical axis only", "title", "legend"]),
        ("A graph of distance versus time is a straight line through the origin. That pattern means distance is…",
         "proportional to time (steady speed)", "A line through (0,0) means doubling time doubles distance at constant speed.",
         ["random", "always zero", "decreasing"]),
        ("A plotted point is (4 s, 12 m) on a distance–time graph. Average speed for those 4 s is…",
         "3 m/s", "Speed = distance/time = $12/4=3$ m/s.",
         ["16 m/s", "0.33 m/s", "48 m/s"]),
        ("Why do scientists graph lab data instead of only listing a table?",
         "patterns such as a trend or an outlier become easier to see",
         "A picture of the numbers shows shape: rising, falling, leveling, or a stray point.",
         ["graphs replace units", "tables are never allowed", "graphs change the measurements"]),
        ("If every y-value is twice the matching x-value, the graph is…",
         "a straight line with a constant steepness of 2", "The rule $y=2x$ is a line. Steepness (rise/run) equals 2.",
         ["a circle", "a random scatter with no trend", "a vertical line"]),
        ("A 45 g metal slug has volume 9 cm³. Density equals…",
         "5 g/cm³", "$45/9=5$ g/cm³.",
         ["54 g/cm³", "36 g/cm³", "0.2 g/cm³"]),
        ("Which state of matter is easiest to compress a lot, and why?",
         "gas, because of large empty spaces between particles",
         "You can push gas particles closer. Solids and liquids are already packed.",
         ["solid, because it is hard", "liquid, because it flows", "all three compress the same"]),
        ("Freezing is the reverse of melting. Freezing changes a substance from…",
         "liquid to solid", "Particles slow down and lock into a more ordered arrangement.",
         ["solid to gas", "gas to liquid", "liquid to gas"]),
        ("A student records mass 18.0 g on a balance and volume 6.0 mL in a cylinder. Density is…",
         "3.0 g/mL", "$18.0/6.0=3.0$ g/mL. Keep the division, not the product.",
         ["108 g/mL", "24 g/mL", "0.33 g/mL"]),
        ("Tearing paper versus burning paper: which statement is correct?",
         "tearing is physical; burning is chemical",
         "Tearing only changes size. Burning makes new gases and ash, which are new substances.",
         ["both are chemical", "both are physical", "tearing is chemical because the paper is “destroyed”"]),
        ("Which SI prefix means one-thousandth?",
         "milli-", "milli- means $10^{-3}$. A milliliter is one-thousandth of a liter.",
         ["kilo-", "centi- only", "mega-"]),
        ("A meterstick reading of 14.2 cm has uncertainty in the tenths place. The instrument is reporting…",
         "a measured length with one estimated digit",
         "The last digit of a measurement is estimated. That is normal, not a mistake.",
         ["an exact count of atoms", "a density", "a chemical formula"]),
        ("$7.2\\times10^{-2}$ as an ordinary decimal is…",
         "0.072", "Move the decimal 2 places left.",
         ["720", "7.2", "0.72"]),
        ("A cart’s distance–time graph is a horizontal line at 5 m after t=3 s. After t=3 s the cart is…",
         "stopped at 5 m", "Distance is not changing, so speed is zero. It sits at 5 m.",
         ["speeding up", "moving backward at 5 m/s", "at the origin"]),
        ("You have 10 g of oil (density 0.8 g/mL). What volume does that oil occupy?",
         "12.5 mL", "$V=m/D=10/0.8=12.5$ mL.",
         ["8 mL", "10.8 mL", "0.08 mL"]),
        ("A sample is heated and a brown gas appears that was not in the original solid. Best classification?",
         "chemical change", "A new gas that was not the original substance is strong evidence of a chemical change.",
         ["physical change only, because heat was used", "a change of units", "melting only"]),
        ("Convert 250 cm to meters.",
         "2.5 m", "Divide by 100: $250\\text{ cm}=2.5$ m.",
         ["25000 m", "0.25 m", "25 m"]),
        ("Which pair are both SI base-related units used in this unit?",
         "kilogram and meter", "Mass uses kg (or g in the lab). Length uses m (or cm).",
         ["pound and inch only", "calorie and mile", "ounce and gallon"]),
        ("On a mass-versus-volume graph for one pure material, the steepness of the best-fit line equals…",
         "density", "Rise/run is $\\Delta m/\\Delta V$, which is density.",
         ["temperature", "time", "the container’s color"]),
        ("A 6 cm³ cube of pine has mass 3 g. Compared with water (1 g/cm³) the pine will…",
         "float, because its density is 0.5 g/cm³",
         "$3/6=0.5$, which is less than 1, so pine floats.",
         ["sink, because wood is a solid", "sink, because 3<6", "float only if the cube is painted"]),
        ("Why can a steel ship float even though steel’s density is greater than water’s?",
         "the ship’s overall density (steel plus air inside) is less than water",
         "Density of the whole object, including empty space, decides floating. The hollow ship displaces a lot of water.",
         ["steel becomes less dense than water when shaped", "water’s density becomes zero under a ship", "gravity turns off for ships"]),
        ("Challenge Stretch: A 40 g object displaces 50 mL of water. Water is 1 g/mL. Will it float, and what is D?",
         "float; 0.80 g/mL", "$D=40/50=0.80$ g/mL, less than 1, so it floats. Displaced volume is the object’s volume.",
         ["sink; 0.80 g/mL", "float; 2.0 g/mL", "sink; 2000 g/mL"]),
        ("Challenge Stretch: Cube X is 8 g in 2 cm³. Cube Y is 8 g in 10 cm³. Both are placed in water (1 g/cm³). What happens?",
         "X sinks and Y floats", "X has $D=4$ g/cm³ (sinks). Y has $D=0.8$ g/cm³ (floats). Same mass, different packing.",
         ["both sink", "both float", "Y sinks and X floats"]),
        ("Challenge Stretch: You need oil of density 0.80 g/mL. A bottle holds 0.250 L. Convert that volume to milliliters, find the oil’s mass, and say whether that oil would float on water (1.0 g/mL).",
         "200 g; yes, it floats",
         "0.250 L = 250 mL. Mass = $0.80\\times250=200$ g. Density 0.80 g/mL is less than water’s 1.0 g/mL, so the oil floats.",
         ["250 g; it sinks", "0.80 g; it floats", "200 g; it sinks because oil is a liquid"]),
        ("Challenge Stretch: Ice density is 0.92 g/cm³. Why does an iceberg sit with most of its bulk under the water line?",
         "its density is only a little less than water, so only a small fraction sticks out",
         "Floating objects sit so that the average density matches the water they displace. 0.92 is close to 1, so most of the ice is underwater.",
         ["ice is denser than water", "air always covers 92% of any solid", "icebergs are hollow steel"]),
        ("Challenge Stretch: A mass–volume graph for one plastic goes through (0,0) and (8 cm³, 6 g). Find D, then say whether a chunk of that plastic floats or sinks in water (1 g/cm³).",
         "0.75 g/cm³; it floats",
         "Steepness = $6/8=0.75$ g/cm³. That is less than 1 g/cm³, so it floats. The origin means zero volume, zero mass.",
         ["0.75 g/cm³; it sinks", "48 g/cm³; it sinks", "1.33 g/cm³; it floats"]),
        ("Challenge Stretch: Sample A: 12 g, 3 mL. Sample B: 12 g, 6 mL. A student says “same mass so same density.” The error is…",
         "ignoring that B has twice the volume, so half the density",
         "A is 4 g/mL and B is 2 g/mL. Density needs both mass and volume.",
         ["mass can never be 12 g", "volume does not affect density", "B must be a gas"]),
        ("Challenge Stretch: A sample is 2.4 kg with volume 3.0 L. Convert mass to grams (1 kg = 1000 g) and volume to milliliters (1 L = 1000 mL), find D in g/mL, and compare with water (1.0 g/mL).",
         "0.80 g/mL; less dense than water (would float if it is a solid chunk)",
         "2400 g / 3000 mL = 0.80 g/mL, which is below 1.0 g/mL. Two unit conversions, then D, then the water comparison.",
         ["2.4 g/mL; denser than water", "800 g/mL; denser than water", "0.80 g/mL; denser than water"]),
        ("Challenge Stretch: A cylinder reads 18.0 mL. A 7.2 g pebble raises the water to 21.0 mL. Find the pebble’s density, then say whether it sinks or floats in a liquid of density 2.0 g/mL.",
         "2.4 g/mL; it sinks in that liquid",
         "Volume of the pebble is $21.0-18.0=3.0$ mL. $D=7.2/3.0=2.4$ g/mL. 2.4 > 2.0, so it sinks in the second liquid.",
         ["2.4 g/mL; it floats in that liquid", "0.34 g/mL; it floats", "7.2 g/mL; it sinks"]),
        ("Challenge Stretch: Oil (0.80 g/mL) is poured on water (1.0 g/mL) in a beaker. A plastic bead with D=0.90 g/mL will…",
         "sink through the oil and float on the water",
         "0.90 is greater than 0.80 (sinks in oil) but less than 1.0 (floats on water), so it rests at the oil–water boundary.",
         ["float on top of the oil", "sink to the bottom through both layers", "dissolve"]),
    ]
    return fill_qs(_pack(rows), 55, lambda i: mq(
        f"A {10+i} g sample has volume 5 cm³. Density in g/cm³?",
        (10 + i) / 5, f"D=m/V={(10+i)}/5.", i, distractors=[(10 + i) * 5, 5, 10 + i]
    ))


def build_unit1():
    title = "Physical Science Unit 1: Matter and Measurement"
    description = (
        "States of matter, density, physical versus chemical change, units, scientific notation, "
        "and reading data graphs — written for Grade 9, with every term defined and numbers you can check."
    )
    concepts = [
        "States of matter",
        "Mass, volume, and density",
        "Physical vs chemical change",
        "Measurement and units",
        "Scientific notation intro",
        "Graphs of data",
    ]
    ican1 = [
        "I can name solid, liquid, and gas by shape, volume, and particle spacing.",
        "I can use everyday pictures (ice cube, water in a cup, steam) to match a state.",
        "I can name melting, freezing, evaporation, and condensation as changes of state.",
    ]
    c1 = _with_ican(concept_block(
        "1. States of matter",
        [
            "Matter is anything that has mass and takes up space. Your desk, the air in the room, and the water in a bottle are all matter. A thought is not matter, because it has no mass and no volume.",
            "A solid keeps its own shape and its own volume. Think of an ice cube. The pieces that make it up — we call them particles — are packed close together and only jiggle in place. They do not flow across the table.",
            "A liquid has a definite volume but no definite shape. Think of water poured from a bottle into a bowl. The amount of water stays about the same, but the water takes the shape of the new container. Particles still touch, yet they can slide past one another.",
            "A gas has no definite shape and no definite volume. Think of the smell of vinegar spreading across a kitchen. Gas particles fly with lots of empty space between them, so a gas fills whatever container it is in.",
            "Heating usually makes particles move faster. That is why ice can melt into water and water can evaporate into vapor. Cooling does the reverse: vapor can condense, and liquid can freeze. The substance can stay the same chemical (H₂O) while the state changes.",
            "You will use states of matter all year. Density, phase changes, and the water cycle all start with this picture: packed, sliding, or flying particles.",
        ],
        "Later lessons on density, heat, and Earth’s water cycle all ask “solid, liquid, or gas?” If you mix up “keeps its shape” with “fills the room,” those later stories will not make sense.",
        "For any sample, ask two yes/no questions. Does it keep its own shape? Does it keep its own volume? Solid: yes and yes. Liquid: no and yes. Gas: no and no.",
        lesson_figure(
            _states_svg(),
            "Particles in a solid, a liquid, and a gas",
            "Solid: tight grid. Liquid: touching but jumbled. Gas: far apart.",
        )
        + solved(1, "A rock sits on a table. Name its state and give one reason.",
                 ["The rock keeps its own shape when you move it to a new dish.",
                  "It also keeps its own volume. It does not spread out to fill the room.",
                  "Both clues match a solid."],
                 "solid", "", "Easy")
        + solved(2, "You pour 200 mL of juice from a carton into a vase. What stays the same, and what changes?",
                 ["The amount of juice is still about 200 mL, so volume stays the same.",
                  "The juice now has the vase’s shape, so shape changes.",
                  "That pair of facts is the definition of a liquid."],
                 "volume stays; shape changes (liquid)", "", "Medium")
        + solved(3, "A closed bottle holds air. You squeeze the bottle and the volume of air gets smaller. Why is that possible for a gas but not for a brick?",
                 ["Gas particles have large empty spaces between them, so they can be pushed closer.",
                  "A brick’s particles are already packed. There is almost no empty space to squeeze out.",
                  "So gases are much easier to compress than solids."],
                 "gases have empty space between particles", "Compress means squeeze into a smaller volume.", "Hard"),
        ("Saying a liquid has no volume",
         "A liquid does have a volume. One cup of milk is still one cup in a tall glass or a wide bowl. What a liquid does not have is a shape of its own."),
        ("Use the two-question test",
         "On paper write “shape? volume?” and answer yes or no for the sample. That tiny table stops you from calling juice a gas just because it can be poured."),
        ican1, 1,
    ), ican1)

    ican2 = [
        "I can define mass, volume, and density in one sentence each.",
        "I can compute $D=m/V$ and rearrange to find mass or volume.",
        "I can predict float or sink by comparing density with water.",
    ]
    c2 = _with_ican(concept_block(
        "2. Mass, volume, and density",
        [
            "Mass is the amount of matter in an object. A bowling ball has more mass than a beach ball of the same size. In the lab we measure mass with a balance, in grams (g) or kilograms (kg).",
            "Volume is how much space an object takes. A rectangular box has volume length × width × height. An irregular rock’s volume is the amount of water it pushes aside in a graduated cylinder. That trick is called water displacement.",
            "Density is mass packed into each unit of volume. The formula is $D=m/V$. If 20 g of clay fills 4 cm³, density is $20/4=5$ g/cm³. Same-size objects can have very different densities if one is heavier.",
            "Water’s density is about 1 g/cm³ (or 1 g/mL). An object denser than the liquid it sits in will sink. An object less dense will float. A steel paper clip sinks. A steel ship can float because the ship includes a lot of air, so its overall density is less than water.",
            "You can rearrange the formula. Mass is $m=D\\times V$. Volume is $V=m/D$. Always match units: grams with cubic centimeters, or grams with milliliters. 1 mL of water is the same volume as 1 cm³.",
            "Density shows up again in Earth’s layers, in floating ice, and in whether helium balloons rise. Get comfortable with “divide mass by volume” now.",
        ],
        "Every later “will it float?” question, and Earth’s dense iron core versus lighter crust, is this same comparison of $m/V$.",
        "Write the formula first: $D=m/V$. Circle the quantity you need. Then plug in numbers with units. If you multiply when you should divide, the number will look wildly large or tiny — that is a clue to flip the operation.",
        lesson_figure(
            _density_svg(),
            "Equal volumes, different masses",
            "The red cube has more mass in the same space, so it is denser.",
        )
        + solved(4, "A 20 g sample has volume 4 cm³. Find density.",
                 ["Write $D=m/V$.",
                  "Substitute $m=20$ g and $V=4$ cm³.",
                  "Divide: $20/4=5$. Density is 5 g/cm³."],
                 "5 g/cm³", "", "Easy")
        + solved(5, "Oil has density 0.80 g/mL. You need 12 g of oil. What volume should you measure?",
                 ["Rearrange to $V=m/D$.",
                  "Substitute $V=12/0.80$.",
                  "Compute $15$ mL."],
                 "15 mL", "If you did $12\\times0.80=9.6$, you found a mass-like product, not a volume.", "Medium")
        + solved(6, "A 9 g pebble has volume 3 cm³. Will it sink in water (1 g/cm³)? Explain with a number.",
                 ["Density of the pebble is $9/3=3$ g/cm³.",
                  "Compare with water: $3>1$.",
                  "The pebble is denser than water, so it sinks."],
                 "sinks (3 g/cm³ > 1 g/cm³)", "", "Hard"),
        ("Multiplying mass and volume and calling it density",
         "Density is a quotient, not a product. $20\\times4=80$ is not density. $20/4=5$ is. If your “density” is huge compared with water’s 1 g/cm³ for a small rock, you probably multiplied."),
        ("Always write D = m / V before the numbers",
         "Seeing the division bar on paper prevents the multiply trap. Then check: should a metal be a few g/cm³, not a few hundred?"),
        ican2, 6,
    ), ican2)

    ican3 = [
        "I can tell a physical change from a chemical change.",
        "I can name clues that a new substance formed.",
        "I can classify melting, dissolving, burning, and rusting.",
    ]
    c3 = _with_ican(concept_block(
        "3. Physical vs chemical change",
        [
            "A physical change alters how matter looks or what state it is in, but it does not make a new substance. Ice melting is still water. Foil crumpled is still aluminum. Sugar dissolved in tea is still sugar — you can get it back by evaporating the water.",
            "A chemical change makes one or more new substances. The particles rearrange into different kinds of stuff. Wood burning becomes ash and gases. A nail rusting becomes iron oxide. You cannot “un-burn” the wood by cooling it.",
            "Clues that a chemical change may have happened include a color change that makes a new material, a gas forming that was not there (bubbles from a reaction, not from boiling water), a solid forming in a liquid (precipitate), or a temperature jump you did not cause with a burner.",
            "Clues are not perfect. Boiling water makes bubbles, but that is a physical change: liquid water becoming water vapor, still H₂O. Always ask: is it still the same substance?",
            "Mixtures can often be separated by physical methods: filtering sand, evaporating salt water, using a magnet on iron filings. Compounds made in a chemical change need a chemical reaction to take apart.",
            "Unit 3 will write chemical equations for these changes. Use a yes/no filter here: new substance, or just a new form of the old one?",
        ],
        "If you call burning a physical change, later balancing and conservation-of-mass work will look like magic instead of bookkeeping of atoms.",
        "Ask one question: could I get the original stuff back with scissors, a filter, a magnet, or evaporation? If yes, it is likely physical. If you need a reaction to undo it, it is chemical.",
        lesson_figure(
            beaker_svg("salt water (mixture)"),
            "A solution can still be a physical mixture",
            "Blue and red dots stay themselves. Evaporation can separate them.",
        )
        + solved(7, "Classify: ice melting on a counter.",
                 ["The substance is water before and after.",
                  "Only the state changed, from solid to liquid.",
                  "That is a physical change."],
                 "physical change", "", "Easy")
        + solved(8, "Classify: a steel nail left in wet air becomes flaky brown rust.",
                 ["The brown flakes are not the original iron metal.",
                  "Iron joined with oxygen to make a new compound.",
                  "That is a chemical change."],
                 "chemical change", "", "Medium")
        + solved(9, "A student says bubbling always means a chemical change. Why is boiling water a counterexample?",
                 ["Boiling makes bubbles of water vapor, which is still H₂O.",
                  "No new substance formed; only the state changed from liquid to gas.",
                  "Bubbles from a new gas (like CO₂ from vinegar and baking soda) can be chemical. The test is “new substance,” not “bubbles.”"],
                 "boiling is physical; bubbles can be either", "", "Hard"),
        ("Calling every color change chemical",
         "Food coloring in water changes color but is still a mixture. Mixing is physical. Look for a new substance, not just a new look."),
        ("Write “same stuff?” in the margin",
         "If the answer is yes, circle physical. If no, circle chemical. That one phrase beats memorizing a long list of examples."),
        ican3, 11,
    ), ican3)

    ican4 = [
        "I can name SI units for mass, length, volume, and time.",
        "I can convert meters and centimeters, and find a box’s volume.",
        "I can choose a balance, a cylinder, or a ruler for the right job.",
    ]
    c4 = _with_ican(concept_block(
        "4. Measurement and units",
        [
            "A measurement is a number plus a unit. “12” is not a length until you say 12 cm. Scientists use SI units so labs in different countries can compare. Length’s base unit is the meter (m). Mass’s base unit is the kilogram (kg). Time’s base unit is the second (s).",
            "In a school lab you often use smaller cousins: centimeters (cm), grams (g), and milliliters (mL). Useful facts: $1\\text{ m}=100\\text{ cm}$, $1\\text{ L}=1000\\text{ mL}$, and $1\\text{ mL}=1\\text{ cm}^{3}$.",
            "A balance measures mass. A graduated cylinder measures liquid volume. A ruler or meterstick measures length. A thermometer measures temperature in degrees Celsius in this course. Match the tool to the quantity.",
            "Volume of a rectangular solid is $V=\\ell\\times w\\times h$. Volume of an odd rock is water displacement: final water level minus starting water level. Do not use a ruler on a lumpy rock and pretend it is a box.",
            "Every measurement has some uncertainty. The last digit you write is estimated. That is not cheating; it is honest reporting. Counting 8 chairs is exact. Measuring 8.2 cm is not exact.",
            "Unit mistakes ruin density. If mass is in grams, volume should be in cm³ or mL, not in meters. Write units in every step.",
        ],
        "Density, speed, and later $F=ma$ all fail if the units do not match. Build the habit of writing the unit beside every number.",
        "Name the quantity first (mass, length, volume, time). Pick the tool. Write the number with its unit. Convert before you divide.",
        lesson_figure(
            _ruler_svg(),
            "A length measurement on a centimeter scale",
            "The object runs from 0 to 6 cm. The reading is 6 cm, not “6.”",
        )
        + solved(10, "How many centimeters are in 1.5 m?",
                 ["1 m = 100 cm.",
                  "Multiply: $1.5\\times100=150$.",
                  "The length is 150 cm."],
                 "150 cm", "", "Easy")
        + solved(11, "A box is 2 cm by 3 cm by 4 cm. Find its volume.",
                 ["Use $V=\\ell\\times w\\times h$.",
                  "Compute $2\\times3\\times4=24$.",
                  "Unit is cm³ because each edge is in cm."],
                 "24 cm³", "", "Medium")
        + solved(12, "Water in a cylinder is at 32.0 mL. A 10.0 g ring raises it to 34.0 mL. Find the ring’s volume and density.",
                 ["Volume of the ring is the water rise: $34.0-32.0=2.0$ mL.",
                  "Density is mass/volume: $10.0/2.0=5.0$ g/mL.",
                  "Report both: 2.0 mL and 5.0 g/mL."],
                 "2.0 mL; 5.0 g/mL", "", "Hard"),
        ("Reporting a number with no unit",
         "“24” could be grams, milliliters, or seconds. A scorer cannot know. Always glue the unit to the number."),
        ("Convert to matching units before dividing",
         "If mass is 1500 g and volume is 1.5 L, convert 1.5 L to 1500 mL first, then $D=1$ g/mL. Mixing liters with grams without converting is a classic trap."),
        ican4, 16,
    ), ican4)

    ican5 = [
        "I can write a large or small decimal in scientific notation.",
        "I can expand scientific notation into an ordinary number.",
        "I can compare two numbers written with powers of ten.",
    ]
    c5 = _with_ican(concept_block(
        "5. Scientific notation intro",
        [
            "Scientific notation writes a number as $a\\times10^{n}$, where $a$ is at least 1 and less than 10, and $n$ is an integer. It is a short way to write very large or very small amounts without a parade of zeros.",
            "For a large number, move the decimal left until one non-zero digit remains in front. The number of places you moved is the positive exponent. $3400=3.4\\times10^{3}$ because the decimal moved 3 places.",
            "For a small number, move the decimal right. The exponent is negative. $0.0056=5.6\\times10^{-3}$ because the decimal moved 3 places right. Negative exponents mean “tiny,” not “negative value.”",
            "To expand, move the decimal right for a positive exponent and left for a negative exponent. $2.0\\times10^{4}=20000$. $7.2\\times10^{-2}=0.072$.",
            "When you compare $3\\times10^{5}$ and $4\\times10^{4}$, expand or compare exponents first. $10^{5}$ is ten times $10^{4}$, so 300000 beats 40000. Do not compare only the 3 and the 4.",
            "You will see scientific notation on atom counts, light-year distances, and wavelengths. For now you only need the reading and writing skill — no fancy calculator tricks yet.",
        ],
        "Atom numbers and later wave speeds are ugly in long form. If $3.0\\times10^{8}$ looks scary now, Unit 6’s light speed will feel impossible.",
        "Ask: is this bigger than 10, or smaller than 1? Big → positive exponent. Tiny → negative exponent. Then count the decimal hops.",
        lesson_figure(
            number_line(-3, 5, closed=[(3, "10³"), (0, "10⁰"), (-2, "10⁻²")]),
            "Powers of ten on a number line of exponents",
            "Positive exponents are large. Zero is 1. Negative exponents are fractions.",
        )
        + solved(13, "Write 3400 in scientific notation.",
                 ["Place the decimal after the first digit: 3.400.",
                  "You moved 3 places from 3400. to 3.400.",
                  "Write $3.4\\times10^{3}$."],
                 "$3.4\\times10^{3}$", "", "Easy")
        + solved(14, "Write 0.0056 in scientific notation.",
                 ["Move the decimal right to get 5.6.",
                  "That is 3 hops, so the exponent is $-3$.",
                  "Write $5.6\\times10^{-3}$."],
                 "$5.6\\times10^{-3}$", "", "Medium")
        + solved(15, "Which is larger, $3\\times10^{5}$ or $4\\times10^{4}$? Show both as ordinary numbers.",
                 ["$3\\times10^{5}=300000$.",
                  "$4\\times10^{4}=40000$.",
                  "300000 is larger, so $3\\times10^{5}$ is larger."],
                 "$3\\times10^{5}$", "A bigger front number does not win if its power of ten is smaller.", "Hard"),
        ("Using a negative exponent to mean a negative number",
         "$10^{-3}$ is 0.001, a small positive number. It is not $-3$ and not $-1000$. The minus sits on the exponent, not on the whole value."),
        ("Count hops on paper",
         "Write the original decimal and draw arrows for each place you move. The hop count is the exponent. Guessing the exponent from the look of the zeros is how 3400 becomes $3.4\\times10^{2}$ by accident."),
        ican5, 21,
    ), ican5)

    ican6 = [
        "I can place the independent variable on the x-axis.",
        "I can read a point and a trend from a distance–time graph.",
        "I can connect the steepness of a mass–volume graph to density.",
    ]
    c6 = _with_ican(concept_block(
        "6. Graphs of data",
        [
            "A graph is a picture of measurements. The independent variable is the one you choose or that marches forward on its own, often time. It goes on the horizontal axis (x-axis). The dependent variable is what you measure in response. It goes on the vertical axis (y-axis).",
            "A distance–time graph that is a straight line through the origin means steady speed. Distance is proportional to time. The steepness of that line is speed: rise over run is meters over seconds.",
            "A horizontal line on a distance–time graph means the object is stopped. Distance is not changing. A line that gets steeper means speeding up. You will use that language again in Unit 4.",
            "For one pure material, a mass-versus-volume graph is a line through the origin. Its steepness is density. That is why we bothered with $D=m/V$ in lesson 2.",
            "Outliers are points that sit far from the pattern. They might be a real surprise, or a misread cylinder. Circle them and look back at the lab notes before you erase them.",
            "Always label axes with the quantity and the unit: “time (s)” and “distance (m),” not just “x” and “y.” A naked graph cannot be scored.",
        ],
        "Motion graphs, heating curves, and Earth’s data all use this same skill. If x and y are swapped, every later slope story is upside down.",
        "Before you read a graph, say out loud: “x is ___, y is ___.” Then read one point as a sentence: “At 4 seconds, the cart is at 12 meters.”",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", [(0, 0), (2, 6), (4, 12), (6, 12), (8, 16)])],
                points=[(4, 12, "(4 s, 12 m)"), (6, 12, "stopped")],
                xlim=(0, 9), ylim=(0, 18), w=320, h=260, xlab="t (s)", ylab="d (m)",
            ),
            "A real distance–time run, not a blank origin",
            "Steady motion, then a pause at 12 m, then motion again.",
        )
        + solved(16, "A point on a d–t graph is (4 s, 12 m). What is average speed for those 4 s?",
                 ["Average speed is distance divided by time.",
                  "Compute $12/4=3$.",
                  "Unit is m/s."],
                 "3 m/s", "", "Easy")
        + solved(17, "After t=4 s the same graph is horizontal at 12 m until t=6 s. What is the cart doing?",
                 ["Distance does not change, so speed is zero.",
                  "The cart is stopped at 12 m for 2 seconds."],
                 "stopped at 12 m", "", "Medium")
        + solved(18, "A mass–volume graph for a metal goes through (0,0) and (5 cm³, 40 g). What is the density?",
                 ["Steepness is rise/run = $\\Delta m/\\Delta V$.",
                  "$40/5=8$.",
                  "Density is 8 g/cm³. The origin confirms zero volume, zero mass."],
                 "8 g/cm³", "", "Hard"),
        ("Putting time on the vertical axis by habit",
         "Time is almost always the independent variable in this course. If you put time on y, “steepness = speed” becomes false. Label before you plot."),
        ("Read one point as a full sentence",
         "“At 4 s the distance is 12 m” is harder to misread than staring at a dot. Then divide if the question asks for speed or density."),
        ican6, 26,
    ), ican6)

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
        ("Dalton’s model pictured the atom as…",
         "a solid indivisible ball", "Dalton thought atoms were tiny hard spheres that could not be split. Later models added inner parts.",
         ["a nucleus with shells", "a plum pudding of charge", "a cloud with no nucleus"]),
        ("Thomson’s “plum pudding” idea added which particle to the atom?",
         "the electron", "Thomson found tiny negative charges (electrons) stuck in a positive bulk, like fruit in pudding.",
         ["the neutron", "the quark", "the neutrino"]),
        ("Rutherford’s gold-foil results showed that most of an atom’s mass is in a…",
         "tiny dense nucleus", "Most alpha particles went straight through. A few bounced, so a small hard center exists.",
         ["large electron cloud that fills the whole foil", "pudding of positive charge with no center", "empty cube"]),
        ("Bohr placed electrons in…",
         "specific energy shells (paths) around the nucleus", "Bohr’s picture is a solar-system-like set of allowed rings. It is a model, not a photograph.",
         ["the nucleus only", "random pudding", "between atoms only"]),
        ("Why do scientists keep changing the atomic model?",
         "new experiments force a better picture", "A model is a useful story. When data disagree, the story is updated. That is science, not failure.",
         ["older scientists were not trying", "atoms themselves keep changing element", "models are only for art class"]),
        ("The particle with a positive charge in the nucleus is the…",
         "proton", "Proton charge is $+1$. The proton count is the atomic number and names the element.",
         ["electron", "neutron", "photon"]),
        ("The particle with no charge in the nucleus is the…",
         "neutron", "Neutrons are neutral. They add mass but do not change the element’s identity.",
         ["proton", "electron", "positron"]),
        ("The very light negative particle outside the nucleus is the…",
         "electron", "Electrons occupy shells. They are the particles that move in chemical bonding and in current.",
         ["proton", "neutron", "alpha particle"]),
        ("Carbon’s atomic number is 6. How many protons does every carbon atom have?",
         6, "Atomic number = proton number. If it is not 6 protons, it is not carbon.",
         [12, 0, 14]),
        ("A lithium atom has 3 protons and 4 neutrons. Its mass number is…",
         7, "Mass number = protons + neutrons = $3+4=7$. Electrons are too light to count in this number.",
         [3, 4, 12]),
        ("An ion is an atom that has…",
         "gained or lost electrons, so it has a net charge", "Protons stay put in ordinary chemistry. Losing electrons makes a positive ion (cation). Gaining electrons makes a negative ion (anion).",
         ["changed its proton count only", "become a different element by losing neutrons", "melted"]),
        ("Na⁺ has 11 protons. How many electrons does it have?",
         10, "Neutral Na has 11 electrons. The + charge means one electron was lost: 10 electrons remain.",
         [11, 12, 1]),
        ("Cl⁻ has 17 protons. How many electrons does it have?",
         18, "The minus means one extra electron: $17+1=18$.",
         [17, 16, 35]),
        ("Isotopes of the same element have the same number of protons but different numbers of…",
         "neutrons", "Carbon-12 and carbon-14 both have 6 protons. C-14 has two extra neutrons.",
         ["protons", "electrons only, never neutrons", "nuclei that are empty"]),
        ("Carbon-14 has 6 protons. How many neutrons does it have?",
         8, "Mass number 14 minus atomic number 6 equals 8 neutrons.",
         [6, 14, 20]),
        ("Rows on the periodic table are called…",
         "periods", "A period is a horizontal row. Period 2 is Li through Ne.",
         ["groups", "families of identical atoms only", "shells of the Earth"]),
        ("Columns on the periodic table are called groups (or families). Elements in a group often have…",
         "similar chemical behavior", "Group 1 metals are all reactive in water. Group 18 gases are all very unreactive. Same column, similar outer electrons.",
         ["identical mass numbers", "the same number of neutrons always", "no protons"]),
        ("The atomic number increases by one as you move…",
         "left to right across a period (and down the table overall as Z rises)",
         "Each next element adds one proton. That is how the table is ordered.",
         ["only in jumps of 8 always", "randomly", "only for gases"]),
        ("Helium, neon, and argon sit in Group 18. They are called noble gases because they…",
         "almost never react", "Their outer shells are full, so they do not need to gain, lose, or share electrons in ordinary chemistry.",
         ["are all metals", "are all solids at room temperature", "have no electrons"]),
        ("Where are the alkali metals (Group 1, except hydrogen) found?",
         "the first column on the left", "Li, Na, K sit in Group 1. They are soft, reactive metals.",
         ["the far-right column", "the zigzag metalloid line only", "inside the nucleus"]),
        ("Metals are typically…",
         "shiny, conduct electricity, and are malleable (can be hammered)",
         "Think of a copper wire or an aluminum can. Those are metal properties.",
         ["dull, brittle, and never conduct", "always gases", "unable to form ions"]),
        ("Nonmetals are typically…",
         "poor conductors, often dull or gaseous, and brittle as solids",
         "Sulfur, oxygen, and neon are nonmetals. They do not behave like copper wire.",
         ["always shiny magnets", "the entire left side of the table", "only found in Group 1"]),
        ("Metalloids sit on the zigzag staircase and…",
         "have some properties of metals and some of nonmetals",
         "Silicon is a classic metalloid: it is used in computer chips because it is a semiconductor.",
         ["are always noble gases", "have no protons", "cannot be elements"]),
        ("Which element is a metal?",
         "iron (Fe)", "Iron is a shiny, conducting solid in the middle of the table. Oxygen and neon are nonmetals. Silicon is a metalloid.",
         ["oxygen (O)", "neon (Ne)", "silicon (Si)"]),
        ("Which element is a nonmetal used as a gas you breathe?",
         "oxygen (O)", "Oxygen is a nonmetal gas. Iron is a metal. Silicon is a metalloid.",
         ["iron (Fe)", "copper (Cu)", "sodium (Na)"]),
        ("The first electron shell can hold up to how many electrons?",
         2, "Shell 1 is full at 2 electrons. Helium has that full shell.",
         [8, 18, 1]),
        ("The second electron shell can hold up to how many electrons?",
         8, "For this course, shell 2 holds up to 8. Neon has 2 in the first shell and 8 in the second.",
         [2, 18, 32]),
        ("Carbon has atomic number 6. Its shell filling in the Bohr picture is…",
         "2 in the first shell, 4 in the second", "Place 2 in shell 1, then the remaining 4 in shell 2. Carbon does not fill shell 2.",
         ["6 in the first shell", "8 in the first shell", "2 and 8"]),
        ("Sodium has 11 electrons. Bohr filling is…",
         "2, 8, 1", "2 in shell 1, 8 in shell 2, and 1 leftover in shell 3. That single outer electron is why Na is reactive.",
         ["11 in one shell", "2, 9", "8, 3"]),
        ("Why do Group 18 atoms almost never form bonds in this course?",
         "their outer shell is already full", "A full outer shell is a stable “closed” arrangement. They have little reason to gain, lose, or share.",
         ["they have no nucleus", "they have no electrons", "they are all metals"]),
        ("Atomic number of oxygen is 8. Number of protons in an oxide ion O²⁻ is still…",
         8, "Ions change electrons, not protons. Oxygen stays element 8.",
         [10, 6, 16]),
        ("Mass number of an atom with 15 protons and 16 neutrons is…",
         31, "$15+16=31$.",
         [15, 16, 1]),
        ("A neutral atom has 20 electrons. How many protons does it have?",
         20, "Neutral means proton count equals electron count.",
         [0, 40, 10]),
        ("Two atoms have 17 protons each. One has 18 neutrons and one has 20. They are…",
         "isotopes of chlorine", "Same protons (same element), different neutrons (different mass numbers 35 and 37).",
         ["different elements", "identical in every way", "ions of sodium"]),
        ("Mg²⁺ has 12 protons. Electron count is…",
         10, "Lost two electrons: $12-2=10$.",
         [12, 14, 2]),
        ("Which statement about the periodic table is true?",
         "elements are ordered by atomic number (proton count)",
         "Modern tables run by Z, not by alphabetical name and not by random grouping.",
         ["elements are ordered by when they were discovered only", "metals are only on the right", "period means a column"]),
        ("Moving down Group 1 from Li to K, atoms have…",
         "more electron shells", "Each period adds a shell. Potassium is below sodium and has another ring of electrons.",
         ["fewer protons", "no neutrons", "identical electron counts"]),
        ("Which is a metalloid used in electronics?",
         "silicon", "Silicon sits on the staircase and is a semiconductor.",
         ["sodium", "helium", "iron"]),
        ("Fluorine is a nonmetal in Group 17. It tends to…",
         "gain one electron to fill its outer shell", "Group 17 atoms need one more electron for a full set of 8 in this course’s picture.",
         ["lose seven protons", "become a metal", "empty the nucleus"]),
        ("A Bohr diagram of neon (10 electrons) shows…",
         "2, 8 — a full outer shell", "Neon is a noble gas. Both shells in the first two rows are full.",
         ["10 in the first shell", "2, 2, 6", "8, 2"]),
        ("Rutherford fired positive particles at gold foil. Most went through because atoms are…",
         "mostly empty space", "The nucleus is tiny. Most of the foil is empty volume between nuclei.",
         ["solid pudding with no gaps", "a single giant proton", "packed like a brick with no space"]),
        ("The number that tells you the element is the…",
         "atomic number (protons)", "Change protons and you change the element. Change neutrons and you only change the isotope.",
         ["mass number only", "neutron number only", "how many shells you draw"]),
        ("An atom with 6 protons, 8 neutrons, and 6 electrons is…",
         "neutral carbon-14", "Z=6 is carbon, mass number 14, equal p and e so neutral.",
         ["oxygen-14", "carbon-6 ion", "nitrogen-8"]),
        ("Why is a neutron’s mass counted in mass number but an electron’s is not (in this course)?",
         "electrons are far lighter than protons or neutrons",
         "Mass number is a whole-number count of heavy nucleus particles only.",
         ["electrons are not real", "neutrons have charge", "protons have no mass"]),
        ("Group 2 metals tend to form 2+ ions because they…",
         "lose two outer electrons", "Two fewer electrons than protons leaves a 2+ charge. The element does not lose protons.",
         ["gain two protons", "gain two extra shells", "become noble gases by losing the nucleus"]),
        ("Aluminum has 13 electrons. Bohr filling is…",
         "2, 8, 3", "Fill shell 1 with 2, shell 2 with 8, and place 3 in shell 3.",
         ["13 in shell 1", "2, 11", "8, 5"]),
        ("Challenge Stretch: Mg²⁺ and neon both have 10 electrons. How many protons does each have, and why are they different substances?",
         "Mg²⁺ has 12 protons; neon has 10 — same electron count, different nuclei",
         "Neon is neutral: 10 protons and 10 electrons. Mg²⁺ lost two electrons from magnesium (12 protons). Matching electron clouds does not make the same element.",
         ["both have 10 protons", "Mg²⁺ has 10 protons and neon has 12", "they are the same substance"]),
        ("Challenge Stretch: Carbon-12 and carbon-14. Which quantities match, and which differ?",
         "same protons and electrons (if both neutral); different neutrons and mass number",
         "Both Z=6. C-12 has 6 neutrons; C-14 has 8. Neutral atoms have 6 electrons each.",
         ["different proton counts", "C-14 has 14 protons", "they cannot both be carbon"]),
        ("Challenge Stretch: A student draws oxygen as 8 electrons in the first shell. Fix the drawing.",
         "2 in shell 1 and 6 in shell 2", "Shell 1 cannot hold 8. Put 2 inside, then 6 outside. Atomic number is still 8.",
         ["8 in shell 2 and 0 in shell 1", "2, 8, 8", "leave all 8 in the nucleus"]),
        ("Challenge Stretch: Aluminum is 2,8,3 and argon is 2,8,8. Why is Al more reactive in this model, and which ion is Al likely to form?",
         "Al has three outer electrons to lose, forming Al³⁺; Ar already has a full outer shell",
         "Losing three outer electrons leaves 2,8 (a full second shell). Argon is already full, so it has little reason to gain or lose. Not the sodium/neon pair from the lesson.",
         ["Al gains three electrons to become Al³⁻", "Ar has more shells than Al", "Al has no outer electrons"]),
        ("Challenge Stretch: An ion has 15 protons, 16 neutrons, and 18 electrons. Give the mass number, the charge, and the element.",
         "mass 31, charge 3−, phosphorus",
         "Mass number = 15+16=31. Charge = 15−18=−3. Atomic number 15 is phosphorus, so P³⁻. Three counts, three answers.",
         ["mass 15, charge 3+, phosphorus", "mass 31, charge 3+, sulfur", "mass 18, charge 0, argon"]),
        ("Challenge Stretch: Cl-35 and Cl-37 mix in nature. If a sample’s average atomic mass is about 35.5, there is…",
         "more Cl-35 than Cl-37", "The average sits closer to 35 than to 37, so the lighter isotope is more common.",
         ["only Cl-37", "equal amounts of every isotope of every element", "more Cl-37 than Cl-35"]),
        ("Challenge Stretch: An oxygen ion has 8 protons, 10 electrons, and 8 neutrons. Give the charge, the mass number, and the Bohr filling.",
         "2− charge, mass number 16, filling 2,8",
         "8p and 10e means 2−. Mass number = 8+8=16. Ten electrons fill 2 then 8. That is O²⁻, not the neon/fluoride pair.",
         ["2+ charge, mass 18, filling 2,6", "neutral, mass 8, filling 8", "2− charge, mass 10, filling 2,8,8"]),
        ("Challenge Stretch: A Bohr diagram shows 2, 8, 8, 2. That atom is in which period and group (main-group picture)?",
         "period 4, Group 2", "Four numbers mean four shells (period 4). Two outer electrons means Group 2 (like calcium).",
         ["period 2, Group 8", "period 4, Group 18", "period 1, Group 2"]),
        ("Challenge Stretch: Gold-foil: 1 in 10,000 particles bounce back. What does that ratio say about nucleus size?",
         "the nucleus is a tiny fraction of the atom’s volume",
         "A rare bounce means a rare hit on a very small target. Most of the atom is empty space.",
         ["the nucleus fills almost the whole atom", "electrons are heavier than the nucleus", "gold has no nucleus"]),
    ]
    return fill_qs(_pack(rows), 55, lambda i: mq(
        f"An atom has {i+3} protons. Atomic number?",
        i + 3, "Atomic number equals proton count.", i, distractors=[i, i + 4, 2 * (i + 3)]
    ))


def build_unit2():
    title = "Physical Science Unit 2: Atoms and the Periodic Table"
    description = (
        "Atomic models, protons neutrons electrons, ions and isotopes, the periodic table, "
        "metals vs nonmetals, and electron shells — Grade 9 language, every word defined."
    )
    concepts = [
        "Atomic model timeline",
        "Protons, neutrons, and electrons",
        "Ions and isotopes",
        "Periodic table organization",
        "Metals, nonmetals, metalloids",
        "Electron shells intro",
    ]
    ican1 = [
        "I can name Dalton, Thomson, Rutherford, and Bohr in order with one picture each.",
        "I can explain why Rutherford needed a tiny nucleus.",
        "I can say that a model is a useful story that changes with new data.",
    ]
    c1 = _with_ican(concept_block(
        "1. Atomic model timeline",
        [
            "An atom is the smallest piece of an element that is still that element. A gold atom is still gold. Cut it into protons and electrons and it is no longer a gold atom. Models of the atom have changed as experiments improved.",
            "Dalton (early 1800s) pictured atoms as tiny solid balls that could not be split. That idea explained why elements combine in simple ratios, like water always being two parts hydrogen to one part oxygen by atom count.",
            "Thomson found the electron: a tiny negative charge. His model was a “plum pudding” — electrons stuck in a positively charged blob, like raisins in a muffin. The atom was no longer an indivisible ball.",
            "Rutherford shot fast positive particles at a thin gold foil. Most went straight through. A few bounced backward. That only makes sense if the positive mass is packed in a tiny, dense nucleus, with the rest of the atom mostly empty space.",
            "Bohr placed electrons in specific shells, like floors in a building or orbits in a simple solar-system cartoon. Electrons can jump between shells by absorbing or emitting energy. We use Bohr’s picture in this course because it is easy to count electrons.",
            "Today’s model is a cloud of probable electron locations, not tiny planets. You do not need that cloud math here. Remember the timeline: ball → pudding → nucleus → shells. Each step added a new experiment.",
        ],
        "Bonding in Unit 3 uses shells and the idea of a tiny nucleus. If the atom is still a solid pudding in your mind, ions and current will not make sense.",
        "For each name, attach one picture: Dalton ball, Thomson muffin, Rutherford bullseye nucleus, Bohr rings. Quiz questions almost always ask for the picture, not the year.",
        lesson_figure(
            _timeline_svg(),
            "Four models in time order",
            "Each new experiment added inner structure the previous model lacked.",
        )
        + solved(1, "Which model first included a tiny dense nucleus?",
                 ["Dalton’s ball has no inner parts.",
                  "Thomson’s pudding has electrons but no small hard center.",
                  "Rutherford’s gold-foil bounce requires a tiny nucleus."],
                 "Rutherford’s model", "", "Easy")
        + solved(2, "Most of Rutherford’s particles went through gold foil. What does that say about atoms?",
                 ["If atoms were solid pudding, almost every particle would hit something and scatter.",
                  "Easy passage means most of the foil’s volume is empty space.",
                  "Only a small nucleus is “in the way.”"],
                 "atoms are mostly empty space", "", "Medium")
        + solved(3, "Why is Bohr’s shell picture still taught if scientists now use electron clouds?",
                 ["Bohr’s rings let you count electrons in a Grade 9 course without cloud math.",
                  "The rings correctly capture that electrons have allowed energies and a capacity (2, then 8).",
                  "A model can be useful for one job even if a more detailed model exists for another job."],
                 "it is a useful counting model", "Useful does not mean “the final photograph of an atom.”", "Hard"),
        ("Thinking the newest model means the old ones were “wrong science”",
         "Each model matched the data of its day. Science updates stories when new data arrive. That is a feature, not a scandal."),
        ("Link one experiment to one picture",
         "Gold foil → nucleus. Electrons in a beam → Thomson. Simple ratios of compounds → Dalton. Those pairs are the quiz."),
        ican1, 1,
    ), ican1)

    ican2 = [
        "I can name the charge, location, and relative mass idea for p⁺, n, and e⁻.",
        "I can use atomic number as proton count.",
        "I can compute mass number as protons plus neutrons.",
    ]
    c2 = _with_ican(concept_block(
        "2. Protons, neutrons, and electrons",
        [
            "The nucleus is the tiny center of the atom. It holds protons and neutrons. Protons have a positive charge. We write that as $+1$. The number of protons is the atomic number. It names the element. 6 protons means carbon. 8 protons means oxygen.",
            "Neutrons have no charge. They are “neutral.” They live in the nucleus and add mass. Different numbers of neutrons make isotopes, which you will meet in the next lesson.",
            "Electrons have a negative charge ($-1$) and live outside the nucleus in shells. They are much lighter than protons or neutrons. In this course we ignore electron mass when we compute mass number.",
            "Mass number is protons plus neutrons. A lithium atom with 3 protons and 4 neutrons has mass number 7. We often write it as lithium-7.",
            "A neutral atom has equal protons and electrons, so the pluses and minuses cancel. If those counts differ, the atom is an ion (next lesson).",
            "Remember the jobs: protons = identity, neutrons = extra mass, electrons = chemistry and charge. Mix those jobs and every later formula will be off.",
        ],
        "Ions, isotopes, and electron shells all use these three particles. If you swap proton with electron, you will change the element by accident on paper.",
        "For any atom, make a three-line list: protons (atomic number), neutrons (mass number minus protons), electrons (same as protons if the atom is neutral).",
        lesson_figure(
            atom_shells_svg(protons=6, electrons=(2, 4)),
            "A carbon atom in the Bohr picture",
            "Nucleus holds 6 protons (and neutrons, not all drawn). Six electrons occupy two shells.",
        )
        + solved(4, "Carbon’s atomic number is 6. How many protons are in a carbon atom?",
                 ["Atomic number is defined as the proton count.",
                  "So carbon has 6 protons.",
                  "If it had 7 protons, it would be nitrogen, not carbon."],
                 "6 protons", "", "Easy")
        + solved(5, "A lithium atom has 3 protons and 4 neutrons. What is its mass number?",
                 ["Mass number = protons + neutrons.",
                  "Compute $3+4=7$.",
                  "Electrons are not added into this whole number."],
                 "7", "", "Medium")
        + solved(6, "A neutral atom has 20 electrons. How many protons does it have? Why?",
                 ["Neutral means total positive charge equals total negative charge.",
                  "Each proton is +1 and each electron is −1.",
                  "So there must be 20 protons as well."],
                 "20 protons", "", "Hard"),
        ("Adding electrons into the mass number",
         "Mass number counts only the heavy nucleus particles. Electrons matter for charge and bonding, not for this whole-number mass."),
        ("Table of three counts before you answer",
         "Write p⁺, n, e⁻ with numbers. Circle which one the question asked for. That stops “atomic number = mass number” mix-ups."),
        ican2, 6,
    ), ican2)

    ican3 = [
        "I can define ion and isotope in one sentence each.",
        "I can find electrons on Na⁺ and Cl⁻.",
        "I can find neutrons from mass number minus atomic number.",
    ]
    c3 = _with_ican(concept_block(
        "3. Ions and isotopes",
        [
            "An ion is an atom (or group of atoms) with a net electric charge. The charge comes from gaining or losing electrons. Protons do not jump out in ordinary chemistry. If they did, the element would change.",
            "A positive ion is called a cation. Sodium metal often loses one electron and becomes Na⁺. 11 protons and 10 electrons: more plus than minus. A negative ion is called an anion. Chlorine often gains one electron and becomes Cl⁻: 17 protons and 18 electrons.",
            "Isotopes are atoms of the same element (same protons) with different numbers of neutrons. Carbon-12 and carbon-14 both have 6 protons. Carbon-14 has 8 neutrons instead of 6. They are both carbon. They have different mass numbers: 12 and 14.",
            "To find neutrons, subtract: neutrons = mass number − atomic number. For carbon-14: $14-6=8$ neutrons.",
            "Everyday analogy: isotopes are like two backpacks of the same brand with different textbook loads. Same identity (brand = element), different mass. Ions are like the same backpack after you add or remove a charged sticker (electrons), not after you swap the brand.",
            "Nuclear changes that alter protons are not ordinary chemistry. This course keeps chemistry = electrons, identity = protons.",
        ],
        "NaCl in Unit 3 is Na⁺ next to Cl⁻. If you cannot count electrons on those ions, ionic bonding will be a slogan instead of a picture.",
        "Same protons? Same element. Different neutrons? Isotopes. Different electrons? Ions. Write those three sentences on every mixed question.",
        lesson_figure(
            atom_shells_svg(protons=11, electrons=(2, 8)),
            "Na⁺: 11 protons (11p) and 10 electrons (10e)",
            "2 electrons in the inner shell and 8 in the outer shell. Charge is 1+ because 11p minus 10e leaves 1+.",
        )
        + solved(7, "Na⁺ has 11 protons. How many electrons does it have?",
                 ["Neutral sodium would have 11 electrons.",
                  "The plus sign means one electron was lost.",
                  "$11-1=10$ electrons."],
                 "10", "", "Easy")
        + solved(8, "Carbon-14 has 6 protons. How many neutrons?",
                 ["Mass number is 14.",
                  "Neutrons = $14-6=8$."],
                 "8 neutrons", "", "Medium")
        + solved(9, "Cl-35 and Cl-37. What is the same, and what is different?",
                 ["Both have 17 protons, so both are chlorine.",
                  "Mass numbers 35 and 37 mean 18 neutrons versus 20 neutrons.",
                  "If both are neutral, both have 17 electrons. They are isotopes, not different elements."],
                 "same protons (and e⁻ if neutral); different neutrons", "", "Hard"),
        ("Changing the proton count and still calling it the same element",
         "If you lose a proton, you are not “carbon with a charge.” You are a different element. Charge in this unit comes from electrons."),
        ("Box the mass number and atomic number",
         "Mass number is the bigger whole number near the name (carbon-14). Atomic number is the table number (6). Subtract to get neutrons."),
        ican3, 11,
    ), ican3)

    ican4 = [
        "I can tell a period (row) from a group (column).",
        "I can say the table is ordered by atomic number.",
        "I can locate Group 1 metals and Group 18 noble gases.",
    ]
    c4 = _with_ican(concept_block(
        "4. Periodic table organization",
        [
            "The periodic table is a chart of the elements. It is ordered by atomic number: 1 is hydrogen, 2 is helium, and so on. Each step to the right adds one proton.",
            "A period is a horizontal row. Period 1 has H and He. Period 2 runs from lithium to neon. As you move down to a new period, atoms have more electron shells.",
            "A group (also called a family) is a vertical column. Elements in a group often behave alike because they have the same number of outer electrons. Group 1 (except hydrogen) is the alkali metals: lithium, sodium, potassium. They are all reactive metals.",
            "Group 18 is the noble gases: helium, neon, argon, and the rest. They almost never form compounds in a Grade 9 lab. Their outer shells are full.",
            "Group 17 is the halogens: fluorine, chlorine, bromine, iodine. They are reactive nonmetals. They often gain one electron.",
            "You do not need to memorize the whole table. You do need to read it: atomic number, symbol, and whether you are in a metal area, a nonmetal area, or on the staircase of metalloids.",
        ],
        "Bonding rules in Unit 3 are “look at the column.” If group versus period is fuzzy, ionic versus covalent becomes a coin flip.",
        "Point with a finger: left-right is a period (shell filling). Up-down is a group (same outer-electron count). Say that sentence before you hunt for an element.",
        lesson_figure(
            _periodic_mini_svg(),
            "A tiny slice of the table: groups and periods",
            "H and He are Period 1. Li and Ne are Period 2. He and Ne are Group 18.",
        )
        + solved(10, "Are rows called periods or groups?",
                 ["Rows run left to right.",
                  "Those rows are periods.",
                  "Groups are the columns."],
                 "periods", "", "Easy")
        + solved(11, "Why do sodium and potassium act similarly in water?",
                 ["They sit in the same group (Group 1).",
                  "Same group means the same number of outer electrons in this course’s model.",
                  "Alike outer electrons → alike reactions."],
                 "same group / same outer-electron count", "", "Medium")
        + solved(12, "Helium is in Period 1 and Group 18. Neon is in Period 2 and Group 18. What is the same, and what is different?",
                 ["Same group: both are noble gases with full outer shells.",
                  "Different periods: neon has one more shell than helium.",
                  "Both are unreactive, but neon’s atoms are larger in the Bohr picture."],
                 "same group (noble); different period (more shells for Ne)", "", "Hard"),
        ("Calling a column a period",
         "Period = row, like a sentence written across the page. Group = column, like a family portrait stacked down the page. Swap those words and every “Group 1” question is backwards."),
        ("Find the element, then name row and column",
         "Do not answer “where is it?” from memory of a song. Find the box, then say period number and group number."),
        ican4, 16,
    ), ican4)

    ican5 = [
        "I can list typical metal properties.",
        "I can list typical nonmetal properties.",
        "I can place metalloids on the staircase and name silicon as an example.",
    ]
    c5 = _with_ican(concept_block(
        "5. Metals, nonmetals, and metalloids",
        [
            "Metals take up most of the left and middle of the table. Everyday metals: iron, copper, aluminum, gold. They are usually shiny, they conduct electricity and heat, and they can be hammered into sheets (malleable) or drawn into wires (ductile).",
            "Think of a copper wire in a charger. Electrons can wander through the metal, which is why the wire works. That wandering is a preview of Unit 7, not a full circuit lesson yet.",
            "Nonmetals sit on the right side (plus hydrogen at the top left). Oxygen, nitrogen, sulfur, chlorine, and neon are nonmetals. They are often gases or dull brittle solids. They do not conduct like copper.",
            "Metalloids sit on the zigzag staircase between metals and nonmetals. Silicon is the star example. It is a semiconductor: it can conduct in a controlled way, which is why computer chips use it.",
            "Hydrogen is a nonmetal that sits in Group 1 because it has one electron, not because it is an alkali metal. Do not call hydrogen a metal.",
            "Classifying an element is the first step in predicting ionic versus covalent bonding in Unit 3: metal + nonmetal often ionic; nonmetal + nonmetal often covalent.",
        ],
        "If you call oxygen a metal, you will predict the wrong bond type for water. The staircase is a map, not decoration.",
        "Ask: shiny conductor you could hammer? Metal. Brittle or gaseous poor conductor? Nonmetal. On the zigzag and “in between”? Metalloid.",
        lesson_figure(
            _metal_strip_svg(),
            "Left metals, staircase metalloids, right nonmetals",
            "The table’s geography is the property map.",
        )
        + solved(13, "Name one metal property of copper.",
                 ["Copper is shiny.",
                  "Copper conducts electricity (wires).",
                  "Either property is enough to classify it as a metal."],
                 "shiny and/or conducts (metal)", "", "Easy")
        + solved(14, "Is oxygen a metal, a nonmetal, or a metalloid?",
                 ["Oxygen is a gas you breathe and a poor conductor.",
                  "It sits on the right side of the table.",
                  "It is a nonmetal."],
                 "nonmetal", "", "Medium")
        + solved(15, "Why is silicon used in computer chips, in one Grade 9 sentence?",
                 ["Silicon is a metalloid.",
                  "Metalloids can behave as semiconductors: they conduct in a controlled way, not like a full copper wire and not like a full insulator.",
                  "Chips need that in-between behavior."],
                 "semiconductor metalloid", "", "Hard"),
        ("Calling hydrogen an alkali metal",
         "Hydrogen sits above Group 1 because it has one electron, but it is a nonmetal gas, not a shiny hammerable metal."),
        ("Use the table’s geography",
         "Left/middle = metals, staircase = metalloids, right = nonmetals. Then confirm with one property (conducts? gas?)."),
        ican5, 21,
    ), ican5)

    ican6 = [
        "I can fill shells 2 then 8 in the Bohr picture.",
        "I can write carbon as 2,4 and sodium as 2,8,1.",
        "I can connect a full outer shell to low reactivity.",
    ]
    c6 = _with_ican(concept_block(
        "6. Electron shells intro",
        [
            "In the Bohr picture, electrons live in shells, like seats in rows around a stage. The first shell is closest to the nucleus. It holds up to 2 electrons. Hydrogen has 1. Helium has 2 and is full.",
            "The second shell holds up to 8 electrons. Lithium has 3 electrons total: 2 in the first shell and 1 in the second (written 2,1). Neon has 10 electrons: 2,8 — a full second shell.",
            "A useful Grade 9 rule: fill the inner shell first, then the next. Carbon has 6 electrons: 2,4. Oxygen has 8: 2,6. Sodium has 11: 2,8,1. The last number is the outer electrons, which do the bonding.",
            "A full outer shell is a stable “closed” arrangement in this model. Noble gases already have it. Other atoms gain, lose, or share electrons to get closer to that full-shell feeling. That is the hook for Unit 3.",
            "Do not put 8 electrons in the first shell. The first shell only has two seats. A drawing with 8 in the inner ring is a common error.",
            "Shells are a counting tool. Real electrons are not tiny planets on railroad tracks. Still, 2-8-8 filling will carry you through bonding, ions, and a first look at the table’s columns.",
        ],
        "Ionic charges and covalent sharing are “how many to a full shell?” If 2-8 filling is shaky, every formula in Unit 3 is a guess.",
        "Write the atomic number. That is the electron count for a neutral atom. Place 2, then 8, then 8, and put leftovers in the next shell. Circle the last number — those are the bonding electrons.",
        lesson_figure(
            atom_shells_svg(protons=8, electrons=(2, 6)),
            "Oxygen: 8 protons and 8 electrons",
            "Eight electrons total: 2 in the inner shell and 6 in the outer shell. The outer ring is two short of a full set of 8.",
        )
        + solved(16, "How many electrons can the first shell hold?",
                 ["The innermost shell has a capacity of 2.",
                  "Helium’s 2 electrons fill it.",
                  "It cannot hold 8."],
                 "2", "", "Easy")
        + solved(17, "Write the Bohr filling for carbon (6 electrons).",
                 ["Put 2 in shell 1.",
                  "4 electrons remain for shell 2.",
                  "Write 2,4."],
                 "2,4", "", "Medium")
        + solved(18, "Sodium is 2,8,1 and neon is 2,8. Why is sodium more reactive in this model?",
                 ["Sodium has one outer electron that it can lose to empty that third shell and leave a full 2,8 behind (like neon).",
                  "Neon already has a full outer shell, so it has little reason to gain or lose.",
                  "The extra outer electron is the reactivity clue."],
                 "Na has one outer electron to lose; Ne is full", "", "Hard"),
        ("Stuffing eight electrons into the first shell",
         "Shell 1 holds two. If you draw 8 inner dots, every later count (and every ion charge) will be wrong. Fill 2, then 8."),
        ("Always write the comma pattern",
         "2,8,1 is easier to check than a messy drawing. Count to the atomic number. The last entry is the group’s outer-electron number for main-group elements."),
        ican6, 26,
    ), ican6)

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
        ("Ionic bonding is best described as…",
         "transfer of electrons from a metal atom to a nonmetal atom",
         "The metal loses electrons and becomes a positive ion. The nonmetal gains them and becomes a negative ion. Opposite charges attract.",
         ["sharing a pair of electrons equally always", "two metals swapping protons", "mixing without charged particles"]),
        ("Covalent bonding is best described as…",
         "sharing of electrons between nonmetal atoms",
         "The atoms stay close so that a shared pair counts toward a full outer shell for each.",
         ["a metal giving electrons away with no sharing", "neutrons jumping nuclei", "only gravity holding atoms"]),
        ("NaCl is held together mainly by…",
         "ionic attraction between Na⁺ and Cl⁻",
         "Sodium has lost an electron; chlorine has gained one. Plus and minus stick together.",
         ["covalent sharing of a sodium–chlorine pair only, with no ions", "magnetic north poles", "the nuclei fusing"]),
        ("H₂ (two hydrogen atoms) is held together by…",
         "a covalent bond (shared electron pair)",
         "Two nonmetals share. There is no metal to give electrons away.",
         ["an ionic bond between H⁺ and H⁻ only in the gas tank", "a metallic lattice of H⁺", "no bond; they just sit nearby"]),
        ("A simple Grade 9 rule of thumb is…",
         "metal + nonmetal often ionic; nonmetal + nonmetal often covalent",
         "NaCl is ionic. H₂O and CO₂ are covalent. The rule can have exceptions later; it is a starting map.",
         ["all compounds are ionic", "all compounds are covalent", "metals never form compounds"]),
        ("In H₂O, the subscript 2 means…",
         "two hydrogen atoms in each molecule",
         "Subscripts tell how many atoms of that element are joined in the formula unit or molecule.",
         ["water is heated to 2 °C", "two oxygen atoms", "the charge is 2−"]),
        ("The formula CO₂ represents…",
         "one carbon atom and two oxygen atoms",
         "C has no subscript, so one carbon. O₂ means two oxygen atoms.",
         ["two carbon atoms and one oxygen", "carbon-20", "three oxygen atoms only"]),
        ("How many atoms in total are in one formula unit of MgCl₂?",
         3, "One magnesium and two chlorines: $1+2=3$ atoms.",
         [2, 1, 12]),
        ("The coefficient 2 in 2 H₂O means…",
         "two water molecules",
         "Coefficients sit in front and scale the whole formula. Subscripts sit inside and cannot be casually changed when balancing.",
         ["two extra oxygen atoms glued on", "H₂O₂ (hydrogen peroxide)", "a charge of 2+"]),
        ("Al₂O₃ contains how many aluminum atoms per formula unit?",
         2, "The subscript 2 on Al means two aluminum atoms.",
         [3, 5, 1]),
        ("A balanced equation has…",
         "the same number of each kind of atom on both sides",
         "Atoms are rearranged, not created or destroyed. Balancing is atom bookkeeping.",
         ["the same number of molecules, even if atom counts differ", "only even coefficients", "no coefficients allowed"]),
        ("Balance H₂ + O₂ → H₂O by choosing the O₂ coefficient in 2 H₂ + ? O₂ → 2 H₂O.",
         1, "Two water molecules need 2 oxygen atoms, which is one O₂ molecule. Hydrogen: 4 atoms on each side.",
         [2, 3, 0]),
        ("In N₂ + 3 H₂ → 2 NH₃, how many hydrogen atoms are on the left?",
         6, "3 H₂ means three molecules × 2 atoms each = 6 H atoms. The right side has 2 NH₃ → 6 H as well.",
         [3, 2, 5]),
        ("You may change _____ when balancing, but you must not change _____ .",
         "coefficients; subscripts",
         "Changing H₂O to H₂O₂ makes a different substance. Changing  H₂O  to  2 H₂O  makes two copies of the same substance.",
         ["subscripts; coefficients", "element symbols; nothing", "the arrow direction only; coefficients"]),
        ("For 2 Mg + O₂ → 2 MgO, the number of oxygen atoms on each side is…",
         2, "Left: one O₂ has 2 atoms. Right: 2 MgO has 2 oxygen atoms. Balanced.",
         [1, 4, 0]),
        ("A synthesis (combination) reaction has the pattern…",
         "A + B → AB",
         "Two or more reactants join into one product, like 2 H₂ + O₂ → 2 H₂O.",
         ["AB → A + B", "AB + C → AC + B always", "A → B with no atoms conserved"]),
        ("A decomposition reaction has the pattern…",
         "AB → A + B",
         "One compound splits into simpler pieces, like 2 H₂O → 2 H₂ + O₂ (with energy).",
         ["A + B → AB", "AB + CD → AD + CB only", "nothing changes"]),
        ("A combustion reaction of a hydrocarbon typically needs _____ and produces CO₂ and H₂O when complete.",
         "oxygen", "Burning methane: CH₄ + 2 O₂ → CO₂ + 2 H₂O. Oxygen is the other reactant.",
         ["only nitrogen", "only neon", "no other reactant"]),
        ("Single replacement (in this course) looks like…",
         "A + BC → AC + B",
         "A more reactive element can kick another out of a compound. Example idea: Zn + CuCl₂ → ZnCl₂ + Cu.",
         ["A + B → AB only", "AB → A + B only", "no atoms move"]),
        ("Double replacement swaps partners: AB + CD → AD + CB. The atoms…",
         "are still all present; they trade places",
         "Conservation still holds. You are not deleting elements.",
         ["vanish on the right", "change into new elements", "must all be noble gases"]),
        ("Conservation of mass means…",
         "the total mass of reactants equals the total mass of products in a closed system",
         "Atoms are rearranged. If you could weigh everything, including gases, the mass matches.",
         ["mass disappears when a gas forms", "burning always reduces mass to zero", "products must weigh less because energy left"]),
        ("12 g of carbon fully reacts with 32 g of oxygen to make CO₂ in a sealed container. The CO₂ mass is…",
         "44 g", "12 + 32 = 44. Mass is conserved. The sealed container keeps every atom inside.",
         ["32 g", "12 g", "20 g"]),
        ("A log burns and the ash weighs less than the log. Mass was not destroyed. The rest of the mass…",
         "left as gases such as CO₂ and H₂O vapor",
         "Open-air burning lets product gases escape, so the leftover solid is lighter.",
         ["turned into lost protons", "became neutrons", "violated conservation"]),
        ("If 4 g of hydrogen react completely with 32 g of oxygen to make water, the water’s mass is…",
         "36 g", "4 + 32 = 36 g of H₂O if both are fully used and nothing escapes.",
         ["32 g", "4 g", "28 g"]),
        ("Why must a balanced equation also match conservation of mass?",
         "each atom has mass, and atom counts match on both sides",
         "Same atoms ⇒ same total mass. Balancing is the atom version of conservation.",
         ["coefficients are temperatures", "mass is unrelated to atoms", "only volumes are conserved"]),
        ("A mixture…",
         "contains two or more substances that keep their own identities",
         "Salt water is still salt plus water. You can often separate them physically.",
         ["is always a new compound with a new formula", "must be chemically bonded", "cannot be separated"]),
        ("A compound…",
         "is a substance made of two or more elements chemically bonded in a fixed ratio",
         "Water is H₂O, not a random mix. Breaking it needs a chemical change.",
         ["is any mixed pile of elements", "has no formula", "is the same as a heterogeneous salad"]),
        ("Air is best classified as…",
         "a mixture of gases (mostly N₂ and O₂)",
         "The gases are not bonded into one compound formula. Their ratio can vary a little.",
         ["the compound N₂O₂ only", "a single element", "a pure ionic lattice"]),
        ("Which pair is a compound versus a mixture?",
         "H₂O versus salt stirred into water",
         "H₂O is a compound. Salt water is a mixture (solution) of a compound and water.",
         ["O₂ versus O₂", "iron versus iron", "helium versus helium"]),
        ("Filtering sand from water works because sand and water are…",
         "a mixture that can be separated physically",
         "The sand did not chemically become a new compound with the water.",
         ["a compound that filtration breaks into elements", "the same pure substance", "impossible to classify"]),
        ("MgO is ionic because magnesium is a metal and oxygen is a nonmetal. The charges are typically…",
         "Mg²⁺ and O²⁻",
         "Mg loses two electrons (Group 2). O gains two (needs 2 to fill). The compound is electrically neutral overall.",
         ["Mg⁺ and O⁺", "Mg²⁻ and O²⁺", "no charges in ionic compounds"]),
        ("How many oxygen atoms are in 3 CO₂?",
         6, "Each CO₂ has 2 oxygen atoms; three molecules give $3\\times2=6$.",
         [2, 3, 5]),
        ("Balance: N₂ + H₂ → NH₃. The hydrogen coefficient in N₂ + ? H₂ → 2 NH₃ is…",
         3, "2 NH₃ needs 6 H atoms, so 3 H₂. Nitrogen: N₂ matches two N in 2 NH₃.",
         [2, 1, 6]),
        ("CH₄ + 2 O₂ → CO₂ + 2 H₂O is a…",
         "combustion reaction",
         "A fuel burns in oxygen and, when complete, yields carbon dioxide and water.",
         ["decomposition only, with no oxygen", "synthesis of methane", "a nuclear change"]),
        ("2 H₂O₂ → 2 H₂O + O₂ is best classified as…",
         "decomposition",
         "One compound (hydrogen peroxide) splits into water and oxygen gas.",
         ["synthesis of H₂O₂", "combustion of metal", "a physical mix"]),
        ("A sealed flask holds 10 g of reactants that fully change into products. Product mass is…",
         "10 g", "Closed system: nothing enters or leaves, so mass matches.",
         ["0 g because mass becomes energy fully", "less than 10 g always", "more than 10 g always"]),
        ("Brass (copper mixed with zinc) is…",
         "a mixture (an alloy)",
         "The metals are mixed, not a single compound with one fixed tiny formula like H₂O. Alloys are mixtures of metals.",
         ["a noble gas", "a covalent molecule of CuZn only in every sample", "an element"]),
        ("You can often separate a mixture with a magnet, a filter, or evaporation. You usually cannot separate a compound that way because…",
         "the elements in a compound are chemically bonded",
         "Breaking bonds needs a chemical change, not a sieve.",
         ["compounds have no mass", "mixtures are always gases", "filters create new elements"]),
        ("In 2 H₂ + O₂ → 2 H₂O, if you start with 2 H₂ molecules and 2 O₂ molecules, leftover O₂ molecules equal…",
         1, "The equation uses only 1 O₂ for 2 H₂. One O₂ is extra (leftover).",
         [0, 2, 3]),
        ("The formula unit NaCl is electrically neutral because…",
         "one + charge cancels one − charge",
         "Na⁺ and Cl⁻ pair 1:1. Overall charge is zero even though ions are present.",
         ["both ions are negative", "there are no charges", "sodium has no protons"]),
        ("How many hydrogen atoms are in 4 NH₃?",
         12, "Each NH₃ has 3 hydrogens; $4\\times3=12$.",
         [3, 4, 7]),
        ("Water is a compound. Wet sand is…",
         "a mixture of a compound (water) and other materials",
         "The sand grains and the water stay themselves. You can dry the sand.",
         ["a new element", "a single compound called sand-water", "an ion of silicon"]),
        ("Why is O₂ written with a subscript 2?",
         "oxygen gas molecules contain two oxygen atoms bonded together",
         "The element oxygen, as a gas, is diatomic in this course. That is not the same as the coefficient 2 O₂.",
         ["oxygen’s atomic number is 2", "oxygen has a 2− charge as a molecule", "it is a typo for O"]),
        ("A student balances water as H₂ + O₂ → H₂O₂. Why is that wrong for making water?",
         "H₂O₂ is hydrogen peroxide, a different compound",
         "You changed a subscript, which changes the identity. Water is H₂O. Balance with coefficients instead: 2 H₂ + O₂ → 2 H₂O.",
         ["H₂O₂ is the only correct water formula", "coefficients are forbidden", "oxygen cannot react"]),
        ("Total atoms on the left of 2 Al + 3 Cl₂ → 2 AlCl₃: aluminum plus chlorine equals…",
         "8", "2 Al atoms + $3\\times2=6$ Cl atoms = 8 atoms. Right: 2 AlCl₃ has 2 Al and 6 Cl = 8.",
         [5, 3, 2]),
        ("Sugar (C₁₂H₂₂O₁₁) dissolved in water is a…",
         "mixture (solution)",
         "You can evaporate water and get sugar back. The sugar did not become a new compound with a new fixed formula for the whole cup.",
         ["new element", "pure covalent crystal of water only", "ionic metal"]),
        ("Challenge Stretch: You have 4 H₂ molecules and 1 O₂ molecule. Using 2 H₂ + O₂ → 2 H₂O, how many H₂O can form, and what is leftover?",
         "2 H₂O, with 2 H₂ leftover",
         "One O₂ can support only 2 H₂ (the ratio 2:1). That makes 2 H₂O. Two of the four H₂ molecules have no oxygen partner.",
         ["4 H₂O, nothing leftover", "1 H₂O, 3 H₂ leftover", "2 H₂O, 1 O₂ leftover"]),
        ("Challenge Stretch: 2 H₂ + O₂ → 2 H₂O. If 10 g H₂ would need 80 g O₂ for a complete reaction, but only 64 g O₂ is supplied, water mass cannot exceed…",
         "72 g",
         "Oxygen runs out first. 64 g O₂ is 64/80 of the needed oxygen, so hydrogen used is $10\\times(64/80)=8$ g. Water = $8+64=72$ g. (Same ratio idea without moles.)",
         ["90 g", "64 g", "10 g"]),
        ("Challenge Stretch: Balance Fe + O₂ → Fe₂O₃ as ? Fe + 3 O₂ → 2 Fe₂O₃. The iron coefficient is…",
         4, "2 Fe₂O₃ contains 4 Fe atoms, so 4 Fe on the left. Oxygen: 3 O₂ = 6 O, and 2 Fe₂O₃ has 6 O.",
         [2, 3, 6]),
        ("Challenge Stretch: Why can a balloon of H₂ and O₂ weigh the same after a spark makes water droplets, if the balloon stays sealed?",
         "atoms are rearranged into H₂O; total mass in the sealed balloon stays the same",
         "Conservation holds in a closed balloon. The substances change; the atom count does not.",
         ["mass is created by the spark", "hydrogen mass vanishes", "oxygen turns into photons with no mass"]),
        ("Challenge Stretch: Al³⁺ and O²⁻. Lowest whole-number ion counts that make a neutral compound, and the formula?",
         "two Al³⁺ and three O²⁻, formula Al₂O₃",
         "Charges must cancel: $2\\times(+3)+3\\times(-2)=0$. That is Al₂O₃, not a 1:1 formula.",
         ["one Al³⁺ and one O²⁻, formula AlO", "three Al³⁺ and two O²⁻, formula Al₃O₂", "two Al³⁺ and two O²⁻, formula AlO"]),
        ("Challenge Stretch: Unbalanced C₃H₈ + O₂ → CO₂ + H₂O. After you place coefficients so carbon, hydrogen, then oxygen all match, how many O₂ molecules are needed, and how many oxygen atoms is that?",
         "5 O₂, which is 10 oxygen atoms",
         "3 C on the left needs 3 CO₂. 8 H needs 4 H₂O. Oxygen atoms on the right: 3×2+4=10, so 5 O₂. Counting atoms on an already-balanced equation without placing coefficients is not the skill.",
         ["1 O₂ (2 atoms)", "3 O₂ (6 atoms)", "8 O₂ (16 atoms)"]),
        ("Challenge Stretch: A 50 g mixture is 20 g salt and 30 g water. After evaporating all water in an open dish, leftover mass is…",
         "20 g",
         "Water leaves as vapor (still existing, just not in the dish). The salt remains. The dish is not a closed system for the water.",
         ["50 g", "30 g", "0 g"]),
        ("Challenge Stretch: Why is air a mixture while CO₂ in a sealed bottle of soda is a compound (the CO₂ itself)?",
         "air’s gases keep separate identities; each CO₂ molecule has a fixed C:O ratio of 1:2",
         "Mixtures can vary. A compound’s formula does not. Soda is a mixture that contains the compound CO₂ plus water and other substances.",
         ["air has a single formula Air₂", "CO₂ is an element", "mixtures cannot contain compounds"]),
        ("Challenge Stretch: You must not “balance” CH₄ + O₂ → CO₂ + H₂O by writing CH₄ + O₄. What should you write instead?",
         "CH₄ + 2 O₂ → CO₂ + 2 H₂O",
         "O₄ would invent a new oxygen formula. Use coefficient 2 on O₂ and coefficient 2 on H₂O so atom counts match: 1 C, 4 H, 4 O each side.",
         ["CH₄ + O₄ → CO₂ + H₂O", "C + 4 H + 2 O → products with new subscripts", "leave it unbalanced"]),
    ]
    return fill_qs(_pack(rows), 55, lambda i: mq(
        f"How many oxygen atoms are in {i} CO₂ molecules?",
        2 * i, f"Each CO₂ has 2 oxygen atoms: 2×{i}={2*i}.", i, distractors=[i, i + 2, 3 * i]
    ))


def build_unit3():
    title = "Physical Science Unit 3: Bonding and Chemical Reactions"
    description = (
        "Ionic versus covalent bonds, formulas, balancing, reaction types, conservation of mass, "
        "and mixtures versus compounds — Grade 9, short sentences, every term defined."
    )
    concepts = [
        "Ionic vs covalent",
        "Chemical formulas",
        "Balancing equations",
        "Types of reactions",
        "Conservation of mass",
        "Mixtures vs compounds",
    ]
    ican1 = [
        "I can describe ionic bonding as electron transfer plus attraction of ions.",
        "I can describe covalent bonding as electron sharing.",
        "I can use metal+nonmetal versus nonmetal+nonmetal as a first sorting rule.",
    ]
    c1 = _with_ican(concept_block(
        "1. Ionic vs covalent",
        [
            "A chemical bond is a force that holds atoms together in a compound. Atoms bond because their outer electrons can reach a more stable, full-shell arrangement. In this course we use two main kinds: ionic and covalent.",
            "Ionic bonding is a transfer. A metal atom loses one or more electrons and becomes a positive ion. A nonmetal atom gains those electrons and becomes a negative ion. Opposite charges attract, like two magnets that snap together. Table salt is Na⁺ next to Cl⁻.",
            "Everyday analogy: ionic bonding is handing over a backpack. Sodium hands an electron to chlorine. After the handoff, one is plus and one is minus, so they stick.",
            "Covalent bonding is sharing. Two nonmetal atoms stay close and share a pair of electrons. Each atom counts the shared pair toward a full outer shell. An H₂ molecule is two hydrogens sharing. Water’s H–O bonds are covalent too.",
            "Everyday analogy: covalent bonding is two people sharing a hoodie. Neither person owns it alone, but both stay close enough to use it. That is a shared electron pair.",
            "A Grade 9 map: metal + nonmetal often ionic (NaCl, MgO). Nonmetal + nonmetal often covalent (H₂O, CO₂, O₂). Later chemistry adds exceptions. For now, the map is enough to sort most quiz examples.",
        ],
        "Every formula and every reaction in this unit is either ions stuck together or atoms sharing. If you mix up transfer with share, NaCl and H₂O become the same story, and they are not.",
        "Ask: is there a metal? If yes, picture electron handoff and charges. If both are nonmetals, picture a shared pair. Then name ionic or covalent.",
        lesson_figure(
            _bond_svg(),
            "Ionic transfer versus covalent sharing",
            "Na⁺ and Cl⁻ attract. Two H atoms share a pair (the line).",
        )
        + solved(1, "Is NaCl ionic or covalent? Why?",
                 ["Sodium is a metal. Chlorine is a nonmetal.",
                  "The metal can lose an electron; the nonmetal can gain it.",
                  "The result is Na⁺ and Cl⁻ attracting. That is ionic."],
                 "ionic", "", "Easy")
        + solved(2, "Is H₂ ionic or covalent? Why?",
                 ["Both atoms are hydrogen, a nonmetal.",
                  "There is no metal to give electrons away.",
                  "They share a pair. That is covalent."],
                 "covalent", "", "Medium")
        + solved(3, "Why does MgO contain Mg²⁺ and O²⁻ rather than Mg⁺ and O⁻?",
                 ["Magnesium is Group 2, so it has two outer electrons to lose in this model.",
                  "Oxygen needs two electrons to fill its outer shell (it has 6 outer electrons).",
                  "Losing two and gaining two makes 2+ and 2−, and the compound is still overall neutral."],
                 "Mg²⁺ and O²⁻", "", "Hard"),
        ("Calling every bond covalent because “atoms share the compound”",
         "Sharing is a specific electron-pair picture for nonmetals. Salt is not two atoms hugging a pair; it is a lattice of ions. Use metal versus nonmetal first."),
        ("Circle metal or nonmetal on each element",
         "Two circles: M or N. M+N → ionic. N+N → covalent. That two-second sort prevents a 50/50 guess."),
        ican1, 1,
    ), ican1)

    ican2 = [
        "I can read a subscript as an atom count.",
        "I can read a coefficient as a count of whole molecules or formula units.",
        "I can total the atoms in a formula such as MgCl₂ or 2 H₂O.",
    ]
    c2 = _with_ican(concept_block(
        "2. Chemical formulas",
        [
            "A chemical formula is a recipe in symbols. H₂O means each water molecule has 2 hydrogen atoms and 1 oxygen atom. The small number is a subscript. It belongs to the element just before it.",
            "If there is no subscript, the count is 1. CO₂ is 1 carbon and 2 oxygen atoms. Do not invent a 2 on carbon.",
            "A coefficient is a big number in front: 3 CO₂ means three carbon dioxide molecules. Total oxygen atoms: $3\\times2=6$. Coefficients scale the whole formula. They do not change what the substance is.",
            "Parentheses group a polyatomic piece you may meet later, like Ca(OH)₂ — two OH groups. In this unit we keep most formulas simple: H₂O, CO₂, NaCl, MgCl₂, Al₂O₃.",
            "Ionic formulas must be electrically silent overall. Ca²⁺ with Cl⁻ needs two chlorides: CaCl₂. One plus-two cancels two minus-ones.",
            "Never “fix” a formula by editing subscripts during balancing. H₂O is water. H₂O₂ is hydrogen peroxide, a different compound. Balancing uses coefficients only.",
        ],
        "Balancing is impossible if you cannot count atoms in a formula. Subscripts versus coefficients is the whole language of this unit.",
        "For a formula, write a tally: element, then count. For a coefficient, multiply every tally. Check that ionic formulas have charges that cancel.",
        lesson_figure(
            _balance_eq_svg(),
            "Coefficients in front, subscripts inside",
            "2 H₂O means two copies of water, not a new compound H₂O₂.",
        )
        + solved(4, "How many hydrogen atoms are in one H₂O molecule?",
                 ["The subscript 2 sits after H.",
                  "That means two hydrogen atoms.",
                  "Oxygen has no subscript, so one oxygen."],
                 "2 hydrogen atoms", "", "Easy")
        + solved(5, "How many oxygen atoms are in 3 CO₂?",
                 ["Each CO₂ has 2 oxygen atoms.",
                  "Three molecules: $3\\times2=6$.",
                  "Carbon total would be 3, but the question asked oxygen."],
                 "6", "", "Medium")
        + solved(6, "Why is the ionic formula CaCl₂, not CaCl?",
                 ["Calcium ions are Ca²⁺ (Group 2, lose two electrons).",
                  "Chloride ions are Cl⁻ (gain one).",
                  "You need two Cl⁻ to cancel one Ca²⁺. The formula shows that 1:2 ratio."],
                 "CaCl₂ for charge balance", "", "Hard"),
        ("Changing H₂O to H₂O₂ to “make oxygen count”",
         "That creates a different substance. Water and hydrogen peroxide are not interchangeable. Use a coefficient such as 2 H₂O instead."),
        ("Tally table: element | left | right",
         "Before any quiz click, list each element and count with coefficient × subscript. The table is the whole skill."),
        ican2, 6,
    ), ican2)

    ican3 = [
        "I can explain why we balance: same atom counts on both sides.",
        "I can change coefficients, not subscripts.",
        "I can balance a simple reaction such as hydrogen and oxygen making water.",
    ]
    c3 = _with_ican(concept_block(
        "3. Balancing equations",
        [
            "A chemical equation is a sentence: reactants (starting stuff) on the left of the arrow, products (new stuff) on the right. The arrow means “becomes.”",
            "Balancing means the same number of each kind of atom appears on both sides. Atoms are rearranged. They are not created or destroyed. That is conservation of atoms, which is conservation of mass in disguise.",
            "You may change coefficients. You must not change subscripts. 2 H₂O is two waters. H₂O₂ is not water.",
            "A reliable order: balance metals, then nonmetals other than H and O, then hydrogen, then oxygen. If a coefficient of 2 helps on one side, check all elements again. Peek at the whole equation after each change.",
            "Example: H₂ + O₂ → H₂O is not balanced. Two H₂O on the right need 4 H and 2 O. So write 2 H₂ + O₂ → 2 H₂O. Left: 4 H and 2 O. Right: 4 H and 2 O. Done.",
            "If an element is stuck, double the most complicated formula and try again with small whole numbers. There is always a set of small integers for the reactions in this course.",
        ],
        "Conservation of mass in the next lesson is this same counting job with grams attached. If the equation is unbalanced, the gram story cannot work.",
        "Make a two-column tally. Change one coefficient. Update the tally. Stop when every row matches. Do not edit subscripts when a tally is unequal.",
        lesson_figure(
            _balance_eq_svg(),
            "2 H₂ + O₂ → 2 H₂O",
            "Four H and two O on each side. Coefficients did the work.",
        )
        + solved(7, "Why is H₂ + O₂ → H₂O not balanced?",
                 ["Left has 2 H and 2 O.",
                  "Right has 2 H and only 1 O.",
                  "Oxygen atoms do not match, so the equation is not balanced."],
                 "oxygen counts do not match", "", "Easy")
        + solved(8, "Balance hydrogen and oxygen making water using coefficients.",
                 ["Put 2 in front of H₂O to get 2 O on the right.",
                  "That requires 4 H on the right, so put 2 in front of H₂.",
                  "O₂ already has 2 O, so its coefficient is 1. Result: 2 H₂ + O₂ → 2 H₂O."],
                 "2 H₂ + O₂ → 2 H₂O", "", "Medium")
        + solved(9, "In N₂ + 3 H₂ → 2 NH₃, show that hydrogen is balanced.",
                 ["Left: 3 H₂ means $3\\times2=6$ hydrogen atoms.",
                  "Right: 2 NH₃ means $2\\times3=6$ hydrogen atoms.",
                  "Six equals six. Nitrogen is 2 on each side as well."],
                 "6 H on each side", "", "Hard"),
        ("Editing subscripts to force a match",
         "H₂ + O₂ → H₂O₂ “balances” oxygen by inventing peroxide. That is a different reaction. Coefficients keep the identity of each substance."),
        ("Tally after every coefficient change",
         "Changing one number can unbalance an element you already fixed. Re-count all elements before you stop."),
        ican3, 11,
    ), ican3)

    ican4 = [
        "I can recognize synthesis and decomposition patterns.",
        "I can recognize a simple combustion of a hydrocarbon.",
        "I can recognize single- and double-replacement patterns in this course.",
    ]
    c4 = _with_ican(concept_block(
        "4. Types of reactions",
        [
            "Chemists group reactions by pattern so you are not memorizing thousands of unique stories. Five patterns appear in Physical Science: synthesis, decomposition, single replacement, double replacement, and combustion.",
            "Synthesis (combination) is A + B → AB. Pieces join. Example: 2 H₂ + O₂ → 2 H₂O. Two elements make a compound.",
            "Decomposition is AB → A + B. A compound splits. Example idea: water can be split into hydrogen and oxygen with energy. Hydrogen peroxide decomposes to water and oxygen: 2 H₂O₂ → 2 H₂O + O₂.",
            "Single replacement is A + BC → AC + B. One element kicks another out. Zinc can replace copper in a copper compound in some labs. Double replacement is AB + CD → AD + CB. Two compounds swap partners, often in solution.",
            "Combustion is burning. A fuel reacts with oxygen. For a hydrocarbon (hydrogen + carbon fuel) that burns completely, products are carbon dioxide and water. Methane: CH₄ + 2 O₂ → CO₂ + 2 H₂O.",
            "The pattern name is a label, not a new law. Conservation still holds. Balancing still holds. The label just helps you predict the product shapes.",
        ],
        "Quiz items often give an equation and ask the type. If the five patterns are blurry, you will mix burning with decomposition because both can make a gas.",
        "Count how many substances start and finish. One product from two reactants → synthesis. One reactant → decomposition. Fuel + O₂ → CO₂ + H₂O → combustion. Then check replacement swaps.",
        lesson_figure(
            _reaction_types_svg(),
            "Five reaction skeletons: join, split, single swap, double swap, burn",
            "Synthesis A+B→AB, decomposition AB→A+B, single replacement A+BC→AC+B, double replacement AB+CD→AD+CB, combustion fuel+O₂.",
        )
        + solved(10, "Classify 2 H₂ + O₂ → 2 H₂O.",
                 ["Two reactants join into one kind of product (water).",
                  "That is synthesis (combination).",
                  "It is also a combustion of hydrogen, but the pattern A+B→AB is synthesis."],
                 "synthesis (hydrogen combustion is a special case)", "", "Easy")
        + solved(11, "Classify 2 H₂O₂ → 2 H₂O + O₂.",
                 ["One compound breaks into simpler products.",
                  "That is decomposition."],
                 "decomposition", "", "Medium")
        + solved(12, "Classify CH₄ + 2 O₂ → CO₂ + 2 H₂O.",
                 ["A carbon–hydrogen fuel reacts with oxygen.",
                  "Products are CO₂ and H₂O.",
                  "That is complete combustion."],
                 "combustion", "", "Hard"),
        ("Calling every gas-making reaction combustion",
         "Decomposition of peroxide makes O₂ without a fuel burning in air. Combustion specifically needs a fuel plus oxygen (usually) and, for hydrocarbons, CO₂ and H₂O when complete."),
        ("Name the pattern in letters first",
         "Write A+B→AB or AB→A+B next to the equation. The letter skeleton is faster than rereading chemical names."),
        ican4, 16,
    ), ican4)

    ican5 = [
        "I can state conservation of mass in a closed system.",
        "I can add reactant masses to get product mass when nothing escapes.",
        "I can explain why ash can weigh less than a log in open air.",
    ]
    c5 = _with_ican(concept_block(
        "5. Conservation of mass",
        [
            "Conservation of mass says that in a chemical change, mass is not created or destroyed. If you could weigh every reactant and every product, including gases, the totals match. Atoms are the same atoms, just rearranged.",
            "A closed system is a container that does not let matter in or out. A sealed flask is closed. An open campfire is not: gases fly away.",
            "Numeric example: 12 g of carbon react with 32 g of oxygen in a sealed bottle and make carbon dioxide. Product mass is $12+32=44$ g. That 44 g is all CO₂ in the bottle.",
            "If a log burns in a fireplace, the ash is lighter than the log. The missing mass left as carbon dioxide and water vapor. Conservation still holds for the whole room plus the chimney. It does not hold for “only the leftover solid” if gases escaped.",
            "A balanced equation is the atom version of this law. Same atoms on both sides means same total mass on both sides (when you include every formula).",
            "You will use a limiting idea in stretch problems: if one reactant runs out, leftover of the other sits unused. The product mass cannot exceed what the scarce reactant can support.",
        ],
        "Every later stoichiometry course is this idea with moles. If mass “disappears” in your mind whenever a gas forms, those courses will feel like contradictions.",
        "Ask: did any gas leave? If the problem is sealed, add the masses. If it is open, the leftover solid can be lighter because product gases left.",
        lesson_figure(
            _balance_eq_svg(),
            "Same atoms, so same mass when nothing escapes",
            "2 H₂ + O₂ → 2 H₂O rearranges 4 H and 2 O; it does not delete them.",
        )
        + solved(13, "Sealed flask: 10 g of reactants fully become products. Product mass?",
                 ["The flask is closed, so no mass enters or leaves.",
                  "Conservation says product mass equals reactant mass.",
                  "The products have mass 10 g."],
                 "10 g", "", "Easy")
        + solved(14, "12 g C + 32 g O₂ → CO₂ in a sealed bottle. Mass of CO₂?",
                 ["Add the reactant masses: $12+32=44$.",
                  "All of that mass is in the product in a sealed bottle.",
                  "CO₂ mass is 44 g."],
                 "44 g", "", "Medium")
        + solved(15, "A student burns a 20 g marshmallow and the black leftover is 1 g. Was mass destroyed?",
                 ["No. Conservation still holds if you include the gases.",
                  "Most of the marshmallow’s mass left as CO₂ and H₂O vapor.",
                  "The open-air leftover is not the whole product set."],
                 "no; gases escaped", "", "Hard"),
        ("Using only the leftover solid as “the products”",
         "Ash is one product. Invisible gases are products too. Weighing only ash in open air is not a test of conservation."),
        ("Write closed or open before the arithmetic",
         "Closed → add masses. Open → leftover solid can be less. That one word choice prevents a false “mass vanished” answer."),
        ican5, 21,
    ), ican5)

    ican6 = [
        "I can define mixture versus compound.",
        "I can give an example of each (air vs water; salt water vs NaCl).",
        "I can name a physical method that can separate many mixtures.",
    ]
    c6 = _with_ican(concept_block(
        "6. Mixtures vs compounds",
        [
            "A mixture contains two or more substances that keep their own identities. Trail mix is still peanuts and raisins. Salt water is still salt and water. You can often separate a mixture with a physical method: a filter, a magnet, evaporation, or picking pieces apart.",
            "A compound is a single substance made of two or more elements chemically bonded in a fixed ratio. Water is always H₂O, not sometimes H₃O₅. Breaking water into hydrogen and oxygen is a chemical change.",
            "Everyday analogy: a mixture is a playlist of songs still themselves. A compound is a new song written from notes that are now locked in that melody. You cannot “filter” the melody back into unrelated notes without rewriting it.",
            "Air is a mixture of nitrogen, oxygen, and other gases. Their ratio can shift a little. CO₂ is a compound: each molecule is one C and two O. Soda is a mixture that contains water, sugar, and dissolved CO₂.",
            "Alloys such as brass (copper plus zinc) are mixtures of metals. They do not have one tiny molecule formula like water does, even though they are useful solids.",
            "Solutions are mixtures that look even throughout, like salt water. Being clear does not make it a compound. Evaporation still brings the salt back.",
        ],
        "Labs ask you to separate sand from salt, or to say why water has a formula and air does not. That is this distinction, not a new bonding law.",
        "Ask: can I separate it without a chemical reaction? If yes, mixture. Does it have a fixed formula like H₂O or NaCl for the whole substance? Compound (or element, if only one type of atom).",
        lesson_figure(
            _mix_vs_compound_svg(),
            "Mixture: particles stay themselves. Compound: atoms joined.",
            "Left can be filtered or evaporated apart. Right needs a chemical change to split.",
        )
        + solved(16, "Is salt water a mixture or a compound?",
                 ["You can evaporate the water and get salt back.",
                  "The salt and water kept their identities.",
                  "That is a mixture (a solution)."],
                 "mixture", "", "Easy")
        + solved(17, "Is H₂O a mixture or a compound?",
                 ["Water has a fixed formula: two H and one O bonded.",
                  "Splitting it needs a chemical change, not a sieve.",
                  "That is a compound."],
                 "compound", "", "Medium")
        + solved(18, "Why is air a mixture even though we write “N₂” and “O₂” for its main gases?",
                 ["N₂ is a covalent element molecule; O₂ is too. They are not bonded to each other as one compound of air.",
                  "The amounts can vary (stuffy room versus outside).",
                  "Separate identities plus variable ratio means mixture."],
                 "mixture of gases", "", "Hard"),
        ("Thinking a clear liquid must be a compound",
         "Salt water can look as clear as pure water. Clear means well mixed, not chemically bonded into one formula for the whole cup."),
        ("Try a separation test in your head",
         "Filter, magnet, evaporate, skim. If that would work, you are looking at a mixture. If you need electrolysis or burning to split it, you are looking at a compound (or an element)."),
        ican6, 26,
    ), ican6)

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
        ("Speed is…",
         "distance traveled divided by time",
         "Speed is how fast, without a required direction. $s=d/t$.",
         ["distance times time", "force divided by mass", "mass times velocity"]),
        ("A walker covers 12 m in 4 s. Average speed is…",
         "3 m/s", "$12/4=3$ m/s.",
         ["16 m/s", "0.33 m/s", "48 m/s"]),
        ("Velocity is speed with…",
         "direction",
         "5 m/s east is a velocity. 5 m/s with no direction named is only a speed.",
         ["only a larger number", "mass", "no units"]),
        ("A car goes 20 m east, then 20 m west, in 10 s total. Average speed is 4 m/s. Average velocity is…",
         "0 m/s (net displacement is 0)",
         "Displacement is the straight-shot change in position. Back to the start means net 0, so average velocity is 0.",
         ["4 m/s east", "40 m/s", "8 m/s"]),
        ("On a distance–time graph, a steeper straight line means…",
         "a larger constant speed",
         "Steepness is rise/run = distance/time = speed. A flatter line is slower. A horizontal line is stopped.",
         ["a larger mass", "zero speed always", "negative mass"]),
        ("Acceleration is…",
         "how quickly velocity changes",
         "Speeding up, slowing down, or turning (changing direction) all count as acceleration.",
         ["how much mass an object has", "distance divided by time only", "a type of energy"]),
        ("A bike goes from 0 to 8 m/s in 4 s. Average acceleration is…",
         "2 m/s²", "$a=\\Delta v/t=(8-0)/4=2$ m/s².",
         ["32 m/s²", "0.5 m/s²", "8 m/s²"]),
        ("A car slows from 15 m/s to 5 m/s in 5 s. Acceleration is…",
         "−2 m/s²", "$(5-15)/5=-10/5=-2$ m/s². The minus means slowing down in the chosen forward direction.",
         ["2 m/s²", "4 m/s²", "10 m/s²"]),
        ("On a speed–time graph, a horizontal line at 6 m/s means…",
         "constant speed 6 m/s (zero acceleration)",
         "Speed is not changing. Acceleration is 0. The object may still be moving.",
         ["stopped at 6 m", "speeding up by 6 m/s each second", "mass = 6 kg"]),
        ("Turning a corner at constant speed is still acceleration because…",
         "direction of velocity is changing",
         "Velocity includes direction. A new direction is a change in velocity.",
         ["speed became zero", "mass changed", "distance became zero"]),
        ("Newton’s first law says an object at rest stays at rest, and a moving object keeps moving at constant velocity, unless…",
         "a net force acts",
         "Net force is the leftover after forces combine. No leftover force → no change in velocity.",
         ["it has mass", "it is on Earth", "time passes"]),
        ("Inertia is…",
         "the tendency to resist a change in motion",
         "More mass means more inertia. A full grocery cart is harder to start or stop than an empty one.",
         ["a force measured in newtons only", "the same as speed", "a type of acceleration"]),
        ("A puck sliding on nearly frictionless ice at 3 m/s will…",
         "keep about 3 m/s in a straight line",
         "With almost no net force, Newton’s first law says constant velocity.",
         ["stop at once because no engine pushes it", "speed up forever", "turn in circles with no force"]),
        ("You lurch forward when a bus stops because…",
         "your body tends to keep moving (inertia) while the bus slows",
         "The bus has a net stopping force. You, until the seatbelt acts, keep your previous velocity.",
         ["the bus gained mass", "gravity reversed", "air disappeared"]),
        ("If all forces on a crate cancel, the crate’s acceleration is…",
         "zero",
         "Net force 0 means acceleration 0. It may be still, or moving at constant velocity.",
         ["infinite", "equal to its mass", "9.8 m/s² always"]),
        ("Newton’s second law is…",
         "F_net = m a",
         "Net force equals mass times acceleration. Units: newtons, kilograms, meters per second squared.",
         ["F = m / a", "F = m + a", "F = v / t"]),
        ("A 2 kg cart has net force 6 N. Acceleration is…",
         "3 m/s²", "$a=F/m=6/2=3$ m/s².",
         ["12 m/s²", "8 m/s²", "0.33 m/s²"]),
        ("To double the acceleration of a cart with the same net force, you must…",
         "halve the mass",
         "$a=F/m$. Same F, half m, double a.",
         ["double the mass", "remove all force", "keep mass and force unchanged"]),
        ("A 5 kg object accelerates at 2 m/s². Net force is…",
         "10 N", "$F=ma=5\\times2=10$ N.",
         ["2.5 N", "7 N", "0.4 N"]),
        ("If two people pull a wagon opposite ways with 8 N and 3 N, net force magnitude is…",
         "5 N", "Opposite directions subtract: $8-3=5$ N leftover.",
         ["11 N", "24 N", "0 N"]),
        ("Newton’s third law says forces come in pairs that are…",
         "equal in size, opposite in direction, on two different objects",
         "If A pushes B, then B pushes A with the same size force. The two forces do not cancel because they act on different objects.",
         ["unequal always", "on the same object so they always cancel", "unrelated in size"]),
        ("A swimmer pushes water backward. The water pushes the swimmer…",
         "forward",
         "Action: swimmer on water, backward. Reaction: water on swimmer, forward. That is how swimming works.",
         ["backward twice as hard", "nowhere; water cannot push", "only downward"]),
        ("Earth pulls a book downward. The third-law partner is…",
         "the book pulling Earth upward",
         "The pair is book↔Earth. The table’s upward force on the book is a different pair (book↔table).",
         ["the table pulling the Moon", "air pushing sideways only", "no partner force exists"]),
        ("A 50 N punch on a wall means the wall punches your hand with…",
         "50 N",
         "Third-law pairs are equal. Your hand hurts because the wall’s force on you is 50 N.",
         ["0 N", "100 N", "25 N"]),
        ("Why don’t the Earth–book forces cancel and leave the book floating?",
         "they act on two different objects, so each object’s net force is separate",
         "Canceling happens among forces on one free-body diagram. Earth’s pull on the book can still be canceled by the table on the book, which is a different pair.",
         ["third law is false on Earth", "the book has no mass", "gravity has no partner"]),
        ("Weight is…",
         "the gravitational force on an object",
         "On Earth, $W=mg$ with $g\\approx9.8$ N/kg (about 10 in this course if a problem says so). Weight is a force, in newtons.",
         ["the same as mass", "a volume", "a type of speed"]),
        ("Mass is…",
         "the amount of matter (inertia), in kilograms",
         "Mass does not change when you go to the Moon. Weight does, because g is smaller.",
         ["always equal to newtons on the Moon", "a force", "volume of water displaced always"]),
        ("A 2 kg bag on Earth (use g=10 N/kg) has weight…",
         "20 N", "$W=mg=2\\times10=20$ N.",
         ["2 N", "12 N", "0.2 N"]),
        ("On the Moon g is about 1.6 N/kg. A 2 kg bag’s mass and weight are…",
         "mass 2 kg; weight about 3.2 N",
         "Mass stays 2 kg. Weight is $2\\times1.6=3.2$ N, much less than on Earth.",
         ["mass 3.2 kg; weight 2 N", "mass 0; weight 2 N", "both mass and weight become zero"]),
        ("Gravity is the attractive force between…",
         "any two masses",
         "Earth pulls you; you pull Earth. Bigger mass and closer distance mean a stronger pull in this course’s qualitative picture.",
         ["only magnets", "only charged objects", "only gases"]),
        ("A runner goes 100 m in 20 s. Average speed?",
         "5 m/s", "$100/20=5$.",
         ["120 m/s", "0.2 m/s", "80 m/s"]),
        ("Velocity 4 m/s north then 4 m/s south means the speeds are equal. The velocities are…",
         "not equal, because directions differ",
         "Velocity cares about direction. North is not south.",
         ["equal as vectors", "both zero", "not speeds at all"]),
        ("From rest, a=3 m/s² for 4 s. Speed reached is…",
         "12 m/s", "$\\Delta v=at=3\\times4=12$ m/s, starting from 0.",
         ["7 m/s", "1.33 m/s", "0.75 m/s"]),
        ("A 0 N net force on a moving 5 kg ball means the ball…",
         "continues at constant velocity",
         "First law: no net force, no acceleration, velocity stays as it is (could be nonzero).",
         ["must stop", "must speed up", "loses all mass"]),
        ("Net force 12 N on 3 kg. a=…",
         "4 m/s²", "$12/3=4$.",
         ["36 m/s²", "9 m/s²", "0.25 m/s²"]),
        ("A box is pulled right 10 N and friction is 4 N left. If mass is 2 kg, a=…",
         "3 m/s²", "F_net=6 N to the right. $a=6/2=3$ m/s².",
         ["7 m/s²", "5 m/s²", "14 m/s²"]),
        ("You push a wall. The wall pushes you. If you and the wall never move, your acceleration is 0 because…",
         "other forces (friction, your feet) make your personal net force zero",
         "The wall’s push on you is real. It is balanced by other forces on you. Third law does not mean you must accelerate.",
         ["the wall’s force on you is zero", "third law is off", "you have no mass"]),
        ("g is about 9.8 N/kg near Earth’s surface. For a 10 kg crate, weight is about…",
         "98 N", "$10\\times9.8=98$ N.",
         ["10 N", "9.8 kg", "0.98 N"]),
        ("A d–t graph goes from (0 s, 0 m) to (5 s, 20 m) in a straight line, then stays at 20 m. Speed in the first 5 s is…",
         "4 m/s", "$20/5=4$ m/s, then speed 0 while the graph is flat.",
         ["20 m/s", "5 m/s", "100 m/s"]),
        ("A v–t graph rises from 0 to 10 m/s in 2 s. Acceleration in that interval is…",
         "5 m/s²", "$(10-0)/2=5$ m/s².",
         ["20 m/s²", "8 m/s²", "12 m/s²"]),
        ("Two teams tug a rope. If the rope does not move, the pulls…",
         "are equal in size and opposite, so net force on the rope is zero",
         "Balanced forces, first law. It is not that forces vanished.",
         ["must both be zero", "must be in the same direction", "mean there is no gravity"]),
        ("A 1 kg object weighs about 10 N on Earth (g=10). Its mass on the Moon is…",
         "1 kg", "Mass does not depend on g. Weight would change; mass does not.",
         ["10 kg", "0 kg", "1.6 kg"]),
        ("If F_net triples and mass stays the same, acceleration…",
         "triples", "$a=F/m$ is proportional to net force when m is fixed.",
         ["stays the same", "becomes one third", "becomes zero"]),
        ("A soccer ball sits still, then flies after a kick. The kick provided…",
         "a net force that caused acceleration",
         "Second law: unbalanced force changes velocity. After the kick, air and grass forces change the story again.",
         ["a mass increase only", "zero force by definition of rest", "a gravity shutoff"]),
        ("Free fall (ignore air) near Earth: all objects have the same…",
         "acceleration g downward",
         "A heavy rock and a light rock pick up speed at the same rate if air is ignored. Weight is larger for the heavy rock, but so is mass, so a=W/m=g.",
         ["weight", "mass", "volume"]),
        ("A bird flaps air down. The air pushes the bird…",
         "up",
         "Third-law pair: bird-on-air down, air-on-bird up. That can support weight if the sizes match.",
         ["down twice as much", "only sideways", "nowhere"]),
        ("Challenge Stretch: A 5 kg sled is pulled 14 N east while snow friction is 4 N west. Find F_net, then the acceleration.",
         "10 N east, then 2 m/s² east",
         "F_net = $14-4=10$ N east. Then $a=10/5=2$ m/s² east. Using 14/5 skips friction.",
         ["14 N east, then 2.8 m/s² east", "10 N west, then 2 m/s² west", "4 N east, then 0.8 m/s² east"]),
        ("Challenge Stretch: A ball is thrown straight up. At the top, speed is 0. The acceleration (ignore air) is…",
         "g downward, not zero",
         "Velocity is zero for an instant, but gravity still pulls, so acceleration is still g down. First law would require net force 0 to stay at rest, and gravity is still there.",
         ["zero because speed is zero", "g upward", "infinite"]),
        ("Challenge Stretch: Skater C (45 kg) and skater D (75 kg) push apart on ice. C’s acceleration is 3 m/s². Find the force size, then D’s acceleration.",
         "135 N; D accelerates 1.8 m/s²",
         "F = ma on C: $45\\times3=135$ N. Third law: D feels 135 N the other way. $a_D=135/75=1.8$ m/s². Equal force, unequal a.",
         ["135 N; D also 3 m/s²", "45 N; D accelerates 0.6 m/s²", "75 N; D accelerates 1 m/s²"]),
        ("Challenge Stretch: A 4 kg box is at rest on a table. Weight is 40 N down (g=10). The table’s upward force is 40 N. Net force is 0. The third-law partner of the weight is…",
         "the box pulling Earth upward with 40 N",
         "Weight is Earth-on-box. Partner is box-on-Earth. The table’s 40 N is a different pair (table-on-box with box-on-table).",
         ["the table’s 40 N (same pair)", "a 0 N force", "air’s 40 N"]),
        ("Challenge Stretch: A v–t graph climbs in a straight line from rest to 10 m/s in 5 s, then stays at 10 m/s for 4 s. Distance during the climb (use the triangle’s area), and total distance for the 9 s?",
         "25 m during the climb; 65 m total",
         "From rest, $v=at$ so $a=10/5=2$ m/s². Climbing triangle area is $\\tfrac12\\times5\\times10=25$ m. Then the rectangle is $10\\times4=40$ m. Total 65 m. Shade the graph and add the two areas.",
         ["50 m and 90 m", "25 m and 40 m", "10 m and 50 m"]),
        ("Challenge Stretch: A 12 N leftover force acts separately on a 3 kg cart and a 6 kg cart. Find each acceleration, then the ratio a_small/a_large.",
         "4 m/s² and 2 m/s²; ratio 2",
         "$a=12/3=4$ m/s² and $a=12/6=2$ m/s². Half the mass, twice the acceleration, so the ratio is 2.",
         ["4 and 2 m/s²; ratio 1/2", "12 and 12 m/s²; ratio 1", "3 and 6 m/s²; ratio 1/2"]),
        ("Challenge Stretch: A 1.5 kg drone has weight 15 N (g=10). Lift (up) is 18 N. Vertical acceleration is…",
         "2 m/s² up",
         "F_net=18−15=3 N up. $a=3/1.5=2$ m/s² up.",
         ["12 m/s² up", "1 m/s² down", "18 m/s² up"]),
        ("Challenge Stretch: You walk 6 m east in 2 s, then 6 m west in 3 s. Average speed for the 5 s trip, and average velocity?",
         "2.4 m/s speed; 0 m/s velocity",
         "Total distance 12 m in 5 s → $12/5=2.4$ m/s. Net displacement 0 → average velocity 0.",
         ["0 m/s speed; 2.4 m/s velocity", "2.4 m/s both", "12 m/s speed; 0 velocity"]),
        ("Challenge Stretch: Why can a heavy truck and a light car have the same acceleration from a stop if the truck’s engine provides a larger net force?",
         "if F/m is the same, a is the same — the truck needs more force because it has more mass",
         "Second law is the ratio. Matching accelerations means forces in the same ratio as the masses.",
         ["mass does not affect acceleration", "the car has more inertia so it is easier", "third law cancels F_net on trucks"]),
    ]
    return fill_qs(_pack(rows), 55, lambda i: mq(
        f"A {i} kg object has net force {3*i} N. Acceleration in m/s²?",
        3, f"a=F/m={3*i}/{i}=3.", i, distractors=[3 * i, i, 1]
    ))


def build_unit4():
    title = "Physical Science Unit 4: Motion and Forces"
    description = (
        "Speed versus velocity, acceleration, Newton’s three laws, and weight versus mass — "
        "Grade 9 algebra only, with free-body pictures and real motion graphs."
    )
    concepts = [
        "Speed and velocity",
        "Acceleration",
        "Newton's first law",
        "Newton's second law",
        "Newton's third law",
        "Gravity and weight",
    ]
    ican1 = [
        "I can compute average speed as distance/time.",
        "I can tell speed from velocity (direction).",
        "I can read a distance–time graph for motion versus rest.",
    ]
    c1 = _with_ican(concept_block(
        "1. Speed and velocity",
        [
            "Speed tells how fast something moves. Average speed is distance traveled divided by time: $s=d/t$. If you walk 12 meters in 4 seconds, speed is $12/4=3$ m/s. Units are meters per second in this course, sometimes km/h in everyday life.",
            "Distance is the full path length, like the odometer. Displacement is the straight-shot change from start to finish, with a direction. Walk 20 m east and 20 m back west: distance 40 m, displacement 0.",
            "Velocity is speed with a direction. “5 m/s east” is a velocity. “5 m/s” alone is a speed. Two cars can have the same speed and opposite velocities if they go north and south.",
            "Average velocity is displacement divided by time. If you end where you began, average velocity is 0 even if you ran the whole time. Average speed is not 0, because distance is not 0.",
            "A distance–time graph that is a straight climb means constant speed. A flat line means stopped. A steeper climb means faster. Time belongs on the horizontal axis.",
            "You need this language for acceleration and for Newton’s laws. Forces change velocity, not “motion” as a vague word. Rest is just velocity zero.",
        ],
        "Newton’s first law is about constant velocity, not “staying still only.” If speed and velocity are the same word in your mind, that law sounds like a contradiction.",
        "Write two labels on every word problem: distance (path) and displacement (arrow from start to end). Divide each by time for speed versus average velocity.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", [(0, 0), (3, 9), (6, 9), (9, 15)])],
                points=[(3, 9, "9 m"), (6, 9, "rest")],
                xlim=(0, 10), ylim=(0, 18), w=320, h=250, xlab="t (s)", ylab="d (m)",
            ),
            "Distance versus time for a real trip",
            "Steady motion, a stop, then motion again. Flat means speed 0.",
        )
        + solved(1, "A walker covers 12 m in 4 s. Find average speed.",
                 ["Write $s=d/t$.",
                  "Substitute $12/4$.",
                  "Speed is 3 m/s."],
                 "3 m/s", "", "Easy")
        + solved(2, "A car goes 20 m east, then 20 m west, in 10 s. Compare average speed and average velocity.",
                 ["Distance is $20+20=40$ m, so average speed is $40/10=4$ m/s.",
                  "Displacement is 0 (back at the start).",
                  "Average velocity is $0/10=0$."],
                 "4 m/s speed; 0 velocity", "", "Medium")
        + solved(3, "A d–t graph is a straight line from (0 s, 0 m) to (5 s, 20 m). What is the speed, and how do you know it is constant?",
                 ["Speed = $20/5=4$ m/s.",
                  "A straight line means the steepness is constant, so speed is constant.",
                  "If it were speeding up, the graph would curve upward."],
                 "4 m/s, constant", "", "Hard"),
        ("Using displacement in the speed formula",
         "Speed uses path distance. If you plug in 0 displacement for a round trip, you wrongly get speed 0 for a runner who is exhausted."),
        ("Arrow for velocity, odometer for speed",
         "Sketch a start dot and an end dot. The path length is speed’s numerator. The arrow from start to end is velocity’s numerator."),
        ican1, 1,
    ), ican1)

    ican2 = [
        "I can define acceleration as a change in velocity over time.",
        "I can compute $a=\\Delta v/t$ including a negative when slowing down.",
        "I can find distance as the area under a v–t graph (triangle or rectangle).",
    ]
    c2 = _with_ican(concept_block(
        "2. Acceleration",
        [
            "Acceleration is how quickly velocity changes. The formula for average acceleration in a straight line is $a=\\Delta v/t=(v_f-v_i)/t$. Units are m/s², meaning “(m/s) per second.”",
            "Speeding up in the forward direction is positive acceleration if forward is positive. Slowing down is negative acceleration (sometimes called deceleration in everyday talk). Turning is also acceleration, because direction is part of velocity.",
            "Example: 0 to 8 m/s in 4 s is $a=8/4=2$ m/s². A car going from 15 m/s to 5 m/s in 5 s has $a=(5-15)/5=-2$ m/s². From rest, the speed after time t is $v=at$ (because $\\Delta v=at$).",
            "A speed–time graph that climbs is speeding up. A flat line at 6 m/s is constant speed, so acceleration is 0 even though the object is moving. A downward line is slowing down (if speed is plotted as positive forward).",
            "Distance traveled is the area between the v–t graph and the time axis. A straight climb from rest to speed v in time t is a triangle: area is $\\tfrac12\\times t\\times v$. A later stretch at constant speed is a rectangle: area is $v\\times t$. Everyday analogy: a gas pedal changes how fast your speedometer needle moves, not just the speed itself.",
            "Newton’s second law will connect net force to this quantity. If you think acceleration means “moving,” you will say a cruising highway car is accelerating when it is not (straight, steady speed).",
        ],
        "F=ma is meaningless if a is “any motion.” Cruising at 20 m/s with net force 0 has acceleration 0. Distance on a v–t sketch is the shaded area.",
        "Write v_start and v_end with direction signs. Subtract, then divide by time. For distance, shade the v–t region and add triangle plus rectangle areas.",
        lesson_figure(
            xy_graph(
                curves=[("#059669", [(0, 0), (2, 10), (6, 10), (8, 4)])],
                points=[(2, 10, "10 m/s"), (6, 10, "steady")],
                xlim=(0, 9), ylim=(0, 12), w=320, h=250, xlab="t (s)", ylab="v (m/s)",
            ),
            "Speed versus time",
            "Speeds up, holds 10 m/s (a=0), then slows. The area under the graph is the distance traveled. Flat is not “stopped.”",
        )
        + solved(4, "A bike goes from 0 to 8 m/s in 4 s. Find acceleration.",
                 ["$\\Delta v=8-0=8$ m/s.",
                  "Divide by time: $8/4=2$.",
                  "Acceleration is 2 m/s²."],
                 "2 m/s²", "", "Easy")
        + solved(5, "A car slows from 15 m/s to 5 m/s in 5 s. Find acceleration.",
                 ["$\\Delta v=5-15=-10$ m/s.",
                  "$-10/5=-2$.",
                  "Acceleration is $-2$ m/s² (slowing down)."],
                 "−2 m/s²", "", "Medium")
        + solved(6, "A v–t graph climbs in a straight line from (0 s, 0 m/s) to (4 s, 8 m/s). Find a, then the distance in those 4 s.",
                 ["$a=\\Delta v/t=8/4=2$ m/s².",
                  "The graph is a triangle from rest: area is $\\tfrac12\\times 4\\times 8=16$ m.",
                  "Check: from rest, $v=at=8$ m/s, so average speed is 4 m/s times 4 s = 16 m."],
                 "2 m/s²; 16 m", "", "Hard"),
        ("Thinking any moving object is accelerating",
         "Steady straight motion is velocity without acceleration. Newton’s first law is built for that case."),
        ("Always subtract v_end minus v_start",
         "Reversing the subtraction flips the sign and turns slowing into speeding on paper. Write the two speeds in a column first."),
        ican2, 6,
    ), ican2)

    ican3 = [
        "I can state Newton’s first law in terms of net force and velocity.",
        "I can define inertia and connect it to mass.",
        "I can give a seatbelt or ice-puck example.",
    ]
    c3 = _with_ican(concept_block(
        "3. Newton's first law",
        [
            "Newton’s first law: an object at rest stays at rest, and an object in motion keeps a constant velocity (same speed and direction), unless a net force acts on it. Net force means the leftover force after you combine all pushes and pulls on that one object.",
            "Everyday analogy: a grocery cart. If you stop pushing on a smooth floor, it still rolls for a while. Friction is a force that finally slows it. In space, with almost no friction, a drifting tool keeps drifting.",
            "Inertia is the stubbornness of motion. Mass measures inertia. A full cart is harder to start and harder to stop than an empty cart. Inertia is not a force. It is a property of the object.",
            "If all forces cancel, net force is 0, so acceleration is 0. The object might be still, or sliding at a constant 3 m/s. Both are “first-law motion.”",
            "You lurch forward when a bus stops because your body has inertia. The bus has a net stopping force (brakes). You keep your old velocity until the seatbelt (a force on you) changes it.",
            "A free-body diagram (FBD) is a sketch of one object with arrows for each force on it. If arrows cancel, first law applies. Unit 4’s later lessons add numbers to those arrows.",
        ],
        "Second law is F_net = ma. If you think objects “want to stop” on their own, you will invent extra forces and get the wrong a.",
        "List every force on the object. If they cancel, predict constant velocity. If they do not, you need second law next. Do not include forces the object exerts on someone else on that FBD.",
        lesson_figure(
            fbd_box(labels=("F_g", "N", "0 net")),
            "A box at rest on a table",
            "Weight down and the table’s normal force up cancel. There is no sideways force. Net force is 0, so a=0.",
        )
        + solved(7, "A puck slides on nearly frictionless ice at 3 m/s. What happens next if no one touches it?",
                 ["Net force is about 0.",
                  "First law: velocity stays 3 m/s in a straight line.",
                  "It does not need a continuing push to “keep moving.”"],
                 "keeps 3 m/s straight", "", "Easy")
        + solved(8, "Why do you lurch forward when a bus stops?",
                 ["You and the bus had the same forward velocity.",
                  "The bus feels a net stopping force; you do not, until the seatbelt or seat acts.",
                  "Your inertia keeps you moving forward relative to the bus."],
                 "inertia; bus slows, you do not yet", "", "Medium")
        + solved(9, "Forces on a crate: 10 N right and 10 N left. The crate is moving at 2 m/s. What is its acceleration, and what does first law say about the 2 m/s?",
                 ["Net force is 0, so acceleration is 0.",
                  "The 2 m/s stays 2 m/s (constant velocity).",
                  "Motion does not require a leftover force; a change in motion does."],
                 "a=0; speed stays 2 m/s", "", "Hard"),
        ("Believing that a force is required to keep a constant speed",
         "That is the everyday friction world talking. First law says leftover force is required to change velocity, not to have velocity."),
        ("Draw the FBD for one object only",
         "If you put “person pushes box” and “box pushes person” on the same diagram, they look like they cancel and the box could never accelerate. Those two forces belong on two diagrams."),
        ican3, 11,
    ), ican3)

    ican4 = [
        "I can use $F_{\\mathrm{net}}=ma$ to find F, m, or a.",
        "I can subtract opposite forces to get F_net.",
        "I can say that more mass means less acceleration for the same net force.",
    ]
    c4 = _with_ican(concept_block(
        "4. Newton's second law",
        [
            "Newton’s second law: $F_{\\mathrm{net}}=ma$. Net force equals mass times acceleration. Force is measured in newtons (N). One newton is the net force that gives a 1 kg mass an acceleration of 1 m/s².",
            "Everyday analogy: pushing a skateboard versus pushing a loaded dresser with the same effort. The dresser has more mass, so it accelerates less. Same F, larger m, smaller a, because $a=F/m$.",
            "Forces in opposite directions subtract. Pull 8 N east and friction 3 N west: $F_{\\mathrm{net}}=5$ N east. Then $a=F/m$ using that leftover, not the 8 N.",
            "Example: 2 kg cart, net force 6 N, $a=6/2=3$ m/s². Example: 5 kg, $a=2$ m/s², $F=10$ N.",
            "If net force triples and mass is unchanged, acceleration triples. If mass doubles and net force is unchanged, acceleration halves. The law is a ratio, not a slogan.",
            "Direction of a matches direction of F_net. If the leftover force is left, acceleration is left, even if the object is still moving right (it is slowing down).",
        ],
        "Every later “will it speed up?” question is this ratio. Gravity’s $W=mg$ is second law with a=g.",
        "Draw the FBD, find leftover force, then divide by mass. Never divide a single force by mass if another force is fighting it.",
        lesson_figure(
            fbd_box(labels=("F_g", "N", "F_app")),
            "Applied force to the right, with weight and normal",
            "If friction is smaller than F_app, F_net is to the right and the box accelerates right.",
        )
        + solved(10, "A 2 kg cart has net force 6 N. Find a.",
                 ["Write $a=F/m$.",
                  "Substitute $6/2$.",
                  "Acceleration is 3 m/s²."],
                 "3 m/s²", "", "Easy")
        + solved(11, "A wagon is pulled 9 N east with 3 N friction west. Mass is 3 kg. Find a.",
                 ["F_net = $9-3=6$ N east.",
                  "$a=6/3=2$ m/s² east.",
                  "If you used 9/3=3, you ignored friction."],
                 "2 m/s² east", "", "Medium")
        + solved(12, "The same 8 N net force acts separately on 2 kg and 4 kg boxes. Compare accelerations.",
                 ["$a=8/2=4$ m/s² for the small box.",
                  "$a=8/4=2$ m/s² for the large box.",
                  "Half the mass gives twice the acceleration."],
                 "4 m/s² vs 2 m/s²", "", "Hard"),
        ("Using the largest force instead of the leftover",
         "Friction, weight, and a pull can fight. Second law uses the vector leftover on that object, not the first number in the sentence."),
        ("FBD, then leftover, then divide",
         "Three lines on paper beat a calculator guess. If a looks huge (like 80 m/s² for a person), you probably forgot a force or mixed units (grams instead of kilograms)."),
        ican4, 16,
    ), ican4)

    ican5 = [
        "I can state that third-law pairs are equal, opposite, and on two objects.",
        "I can name the partner of a given force.",
        "I can explain why those two forces do not cancel on one FBD.",
    ]
    c5 = _with_ican(concept_block(
        "5. Newton's third law",
        [
            "Newton’s third law: if object A pushes object B, then B pushes A with a force of the same size, opposite direction, along the same line. Forces come in pairs. There is no lonely force.",
            "Everyday analogy: a swimmer. You push water backward. Water pushes you forward. You cannot swim in empty space with nothing to push. A bird flaps air down; air pushes the bird up.",
            "The two forces act on two different objects. They never sit on the same free-body diagram, so they do not cancel each other. Your punch on a wall is 50 N; the wall’s punch on your hand is 50 N. Your hand’s FBD includes the wall, not the “you-on-wall” arrow.",
            "Earth pulls a book down (weight). The partner is the book pulling Earth up, not the table’s upward force. The table’s force is a different pair: table-on-book and book-on-table.",
            "Equal forces do not mean equal accelerations. If you and a heavier friend push apart on ice, the forces match, but you (smaller mass) accelerate more. That is second law on each person.",
            "Third law is why rockets work in space: exhaust is pushed backward, rocket is pushed forward. There is still something to push — the exhaust gas.",
        ],
        "Mixing the table’s normal force with the weight’s third-law partner is the classic trap. Gravity pairs with a pull on Earth, not with the table.",
        "Name both objects in the pair: “Earth on book” and “book on Earth.” If your two names are the same object twice, you have not found the partner.",
        lesson_figure(
            _third_law_svg(),
            "A pushes B, B pushes A",
            "Equal arrows, opposite ways, two different people (or pucks).",
        )
        + solved(13, "You push a wall with 50 N. How hard does the wall push you?",
                 ["Third-law pairs are equal in size.",
                  "The wall pushes your hand with 50 N.",
                  "That is why a punch can hurt."],
                 "50 N", "", "Easy")
        + solved(14, "A swimmer pushes water backward. Which way does water push the swimmer?",
                 ["The partner is opposite in direction.",
                  "Backward on water means forward on the swimmer.",
                  "That forward force can move the swimmer through the pool."],
                 "forward", "", "Medium")
        + solved(15, "A 60 kg person and a 90 kg person push apart on ice. Compare forces and accelerations.",
                 ["Third law: the push forces are equal in size.",
                  "Second law: $a=F/m$, so 60 kg gets the larger acceleration.",
                  "Equal force does not mean equal a."],
                 "equal F; larger a for 60 kg", "", "Hard"),
        ("Canceling a third-law pair on one diagram",
         "If those two arrows were on the same object, nothing could ever start moving. Each arrow belongs to a different object’s FBD."),
        ("Write A-on-B and B-on-A",
         "If you cannot name two objects, you do not have a third-law pair yet. Weight’s partner is never “the table” unless the table is Earth, which it is not."),
        ican5, 21,
    ), ican5)

    ican6 = [
        "I can tell mass (kg) from weight (N).",
        "I can compute $W=mg$ with a given g.",
        "I can say mass stays the same on the Moon while weight drops.",
    ]
    c6 = _with_ican(concept_block(
        "6. Gravity and weight",
        [
            "Gravity is the attractive force between any two masses. Earth pulls you down; you pull Earth up (third law). Earth’s pull on you is large enough to notice because Earth has enormous mass and you are close to it.",
            "Weight is the gravitational force on an object. It is a force, so its unit is the newton. Near Earth’s surface, $W=mg$, where g is about 9.8 N/kg (or 9.8 m/s² as a free-fall acceleration). Many Grade 9 problems let you use g=10 to keep the arithmetic friendly.",
            "Mass is the amount of matter, measured in kilograms. Mass does not change when you travel to the Moon. Weight does, because the Moon’s g is smaller (about 1.6 N/kg). A 2 kg bag is still 2 kg on the Moon, but its weight drops from about 20 N to about 3.2 N if g=10 on Earth.",
            "Everyday analogy: mass is how much “stuff” is in the backpack. Weight is how hard the backpack presses on your shoulder in that gravity. On the Moon your shoulder gets a break; the books are still there.",
            "In free fall with air ignored, every object has acceleration g downward. A heavy rock has more weight, but also more mass, so $a=W/m=g$ is the same. Air resistance can change that story for feathers.",
            "On a table, weight down is often balanced by the table’s upward normal force, so the book does not accelerate through the wood. That balance is first law, not “no gravity.”",
        ],
        "Confusing kg with N will break every F=ma problem. Bathroom “scales” in everyday talk often show kg, but physics weight is newtons.",
        "Label m in kg and W in N. Write $W=mg$ with the g the problem gives. If the location changes (Earth versus Moon), change g, not m.",
        lesson_figure(
            fbd_box(labels=("W=mg", "N", "F_app=0")),
            "Weight down, normal up",
            "At rest, N = W. There is no rightward applied force. Mass is still m kilograms, not newtons.",
        )
        + solved(16, "A 2 kg bag on Earth, g=10 N/kg. Find weight.",
                 ["Write $W=mg$.",
                  "$2\\times10=20$.",
                  "Weight is 20 N, not 2 N."],
                 "20 N", "", "Easy")
        + solved(17, "The same 2 kg bag on the Moon, g=1.6 N/kg. Find mass and weight.",
                 ["Mass stays 2 kg.",
                  "Weight is $2\\times1.6=3.2$ N.",
                  "The bag is easier to lift; it is not “less stuff.”"],
                 "2 kg; 3.2 N", "", "Medium")
        + solved(18, "Why do a hammer and a (airless) feather fall together in a vacuum demo?",
                 ["Weight is larger on the hammer, but mass is larger too.",
                  "$a=W/m=g$ for both when air is gone.",
                  "Air, not gravity’s law, is why feathers lag on Earth."],
                 "same g = W/m", "", "Hard"),
        ("Calling mass “weight in kilograms”",
         "Kilograms measure mass. Newtons measure weight. A 60 kg person weighs about 600 N on Earth if g=10, not 60 N."),
        ("Write both m and g before multiplying",
         "If g is missing, you cannot get newtons from kilograms alone. If the problem says Moon, swap g, not the 2 in 2 kg."),
        ican6, 26,
    ), ican6)

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
