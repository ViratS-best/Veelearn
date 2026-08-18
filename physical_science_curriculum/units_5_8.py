"""Physical Science units 5–8: Grade 9 / first high-school science."""
from __future__ import annotations

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, page_break, mq, fill_qs,
    xy_graph, sample_curve,
    fbd_box, series_circuit_svg, energy_bars_svg, field_lines_svg,
    beaker_svg, spring_mass_svg,
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


def _wave_svg():
    """Labeled wave: crest on a peak, trough on a valley, λ crest-to-crest over one full period."""
    import math
    pts = []
    for i in range(81):
        x = 20 + i * 4.5
        y = 70 - 36 * math.cos(i / 40 * 2 * math.pi)
        pts.append(f"{x:.1f},{y:.1f}")
    d = "M" + " L".join(pts)
    return (
        f'<svg viewBox="0 0 400 150" width="100%" style="max-width:400px" role="img">'
        f'<line x1="20" y1="70" x2="380" y2="70" stroke="#94a3b8" stroke-dasharray="4 3"/>'
        f'<path d="{d}" fill="none" stroke="#4f46e5" stroke-width="2.4"/>'
        f'<line x1="20" y1="12" x2="200" y2="12" stroke="#b91c1c" stroke-width="2"/>'
        f'<text x="110" y="24" text-anchor="middle" font-size="12" fill="#b91c1c">λ</text>'
        f'<line x1="200" y1="70" x2="200" y2="34" stroke="#047857" stroke-width="2"/>'
        f'<text x="212" y="54" font-size="12" fill="#047857">amplitude</text>'
        f'<text x="20" y="28" text-anchor="middle" font-size="12">crest</text>'
        f'<text x="200" y="28" text-anchor="middle" font-size="12">crest</text>'
        f'<text x="110" y="128" text-anchor="middle" font-size="12">trough</text>'
        f"</svg>"
    )


def _packed_waves_svg():
    """Same window, two wavelengths: fewer vs more crests."""
    import math
    def path(n_waves, y0, color):
        pts = []
        for i in range(81):
            x = 20 + i * 4.5
            y = y0 - 22 * math.sin(i / 80 * n_waves * 2 * math.pi)
            pts.append(f"{x:.1f},{y:.1f}")
        return f'<path d="M{" L".join(pts)}" fill="none" stroke="{color}" stroke-width="2.2"/>'
    return (
        '<svg viewBox="0 0 400 170" width="100%" style="max-width:400px" role="img">'
        '<text x="20" y="18" font-size="12">same stretch of rope</text>'
        f'{path(2, 55, "#4f46e5")}'
        '<text x="300" y="40" font-size="11" fill="#4f46e5">longer λ, lower f</text>'
        f'{path(4, 125, "#b91c1c")}'
        '<text x="300" y="110" font-size="11" fill="#b91c1c">shorter λ, higher f</text>'
        "</svg>"
    )


def _two_pitch_svg():
    """Two pressure-vs-time traces: low f vs high f in the same 4 s window."""
    import math
    def path(freq, y0, color):
        pts = []
        for i in range(81):
            t = i / 80 * 4
            x = 30 + t * 80
            y = y0 - 18 * math.sin(2 * math.pi * freq * t)
            pts.append(f"{x:.1f},{y:.1f}")
        return f'<path d="M{" L".join(pts)}" fill="none" stroke="{color}" stroke-width="2"/>'
    return (
        '<svg viewBox="0 0 380 170" width="100%" style="max-width:380px" role="img">'
        '<text x="30" y="16" font-size="12">same 4 seconds</text>'
        f'{path(1, 50, "#4f46e5")}'
        '<text x="300" y="36" font-size="11" fill="#4f46e5">low pitch (1 Hz)</text>'
        f'{path(3, 120, "#b91c1c")}'
        '<text x="300" y="106" font-size="11" fill="#b91c1c">high pitch (3 Hz)</text>'
        "</svg>"
    )


def _refract_svg():
    return (
        '<svg viewBox="0 0 320 180" width="100%" style="max-width:320px" role="img">'
        '<rect x="0" y="90" width="320" height="90" fill="#bfdbfe"/>'
        '<rect x="0" y="0" width="320" height="90" fill="#f8fafc"/>'
        '<text x="12" y="24" font-size="12">air</text>'
        '<text x="12" y="160" font-size="12">water</text>'
        '<line x1="40" y1="20" x2="160" y2="90" stroke="#b91c1c" stroke-width="2.4"/>'
        '<line x1="160" y1="90" x2="210" y2="170" stroke="#b91c1c" stroke-width="2.4"/>'
        '<line x1="160" y1="10" x2="160" y2="170" stroke="#64748b" stroke-dasharray="4 3"/>'
        '<text x="70" y="48" font-size="12" fill="#b91c1c">incident</text>'
        '<text x="200" y="140" font-size="12" fill="#b91c1c">bends toward normal</text>'
        "</svg>"
    )


def _visible_slice_svg():
    """Red → violet inside visible light only."""
    colors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#2563eb", "#7c3aed"]
    labels = ["red", "orange", "yellow", "green", "blue", "violet"]
    bits = []
    for i, (c, lab) in enumerate(zip(colors, labels)):
        x = 20 + i * 60
        bits.append(f'<rect x="{x}" y="40" width="56" height="40" fill="{c}" stroke="#0f172a"/>')
        bits.append(f'<text x="{x + 28}" y="100" text-anchor="middle" font-size="11">{lab}</text>')
    return (
        '<svg viewBox="0 0 400 120" width="100%" style="max-width:400px" role="img">'
        + "".join(bits)
        + '<text x="20" y="28" font-size="12">longer λ</text>'
        + '<text x="300" y="28" font-size="12">shorter λ</text>'
        + "</svg>"
    )


def _spectrum_svg():
    colors = ["#7c3aed", "#2563eb", "#22c55e", "#eab308", "#f97316", "#ef4444", "#9f1239"]
    labels = ["radio", "micro", "IR", "vis", "UV", "X-ray", "gamma"]
    bits = []
    for i, (c, lab) in enumerate(zip(colors, labels)):
        x = 16 + i * 52
        bits.append(f'<rect x="{x}" y="40" width="50" height="36" fill="{c}" stroke="#0f172a"/>')
        bits.append(f'<text x="{x + 25}" y="98" text-anchor="middle" font-size="10">{lab}</text>')
    return (
        '<svg viewBox="0 0 400 120" width="100%" style="max-width:400px" role="img">'
        + "".join(bits)
        + '<text x="16" y="28" font-size="12">long λ, low f</text>'
        + '<text x="268" y="28" font-size="12">short λ, high f</text>'
        + "</svg>"
    )


def _parallel_svg():
    return (
        '<svg viewBox="0 0 320 160" width="100%" style="max-width:320px" role="img">'
        '<rect x="16" y="70" width="28" height="24" fill="#fef3c7" stroke="#0f172a"/>'
        '<line x1="44" y1="82" x2="90" y2="82" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="90" y1="82" x2="90" y2="40" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="90" y1="82" x2="90" y2="124" stroke="#0f172a" stroke-width="2"/>'
        '<path d="M90 40 h70" stroke="#0f172a" stroke-width="2"/>'
        '<path d="M90 124 h70" stroke="#0f172a" stroke-width="2"/>'
        '<path d="M160 40 l8 -10 l8 20 l8 -20 l8 20 l8 -10" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        '<path d="M160 124 l8 -10 l8 20 l8 -20 l8 20 l8 -10" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        '<line x1="208" y1="40" x2="260" y2="40" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="208" y1="124" x2="260" y2="124" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="260" y1="40" x2="260" y2="124" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="260" y1="124" x2="260" y2="130" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="30" y1="94" x2="30" y2="130" stroke="#0f172a" stroke-width="2"/>'
        '<line x1="30" y1="130" x2="260" y2="130" stroke="#0f172a" stroke-width="2"/>'
        '<text x="170" y="24" font-size="11">R₁</text>'
        '<text x="170" y="150" font-size="11">R₂</text>'
        '<text x="18" y="64" font-size="11">ε</text>'
        "</svg>"
    )


def _magnet_svg():
    return (
        '<svg viewBox="0 0 340 140" width="100%" style="max-width:340px" role="img">'
        '<rect x="40" y="50" width="90" height="40" fill="#fecaca" stroke="#991b1b"/>'
        '<rect x="130" y="50" width="90" height="40" fill="#bfdbfe" stroke="#1d4ed8"/>'
        '<text x="85" y="76" text-anchor="middle" font-size="16">N</text>'
        '<text x="175" y="76" text-anchor="middle" font-size="16">S</text>'
        '<path d="M85 50 C85 10, 175 10, 175 50" fill="none" stroke="#4f46e5" stroke-width="1.6"/>'
        '<path d="M85 90 C85 130, 175 130, 175 90" fill="none" stroke="#4f46e5" stroke-width="1.6"/>'
        '<text x="240" y="40" font-size="12">field lines</text>'
        '<text x="240" y="58" font-size="12">N → S outside</text>'
        "</svg>"
    )


def _earth_layers_svg():
    return (
        '<svg viewBox="0 0 260 260" width="100%" style="max-width:260px" role="img">'
        '<circle cx="130" cy="130" r="110" fill="#fef3c7" stroke="#92400e" stroke-width="2"/>'
        '<circle cx="130" cy="130" r="88" fill="#fdba74" stroke="#9a3412"/>'
        '<circle cx="130" cy="130" r="52" fill="#fca5a5" stroke="#991b1b"/>'
        '<circle cx="130" cy="130" r="24" fill="#fecaca" stroke="#7f1d1d"/>'
        '<text x="130" y="28" text-anchor="middle" font-size="11">crust (lowest density)</text>'
        '<text x="130" y="62" text-anchor="middle" font-size="11">mantle</text>'
        '<text x="130" y="96" text-anchor="middle" font-size="11">outer core</text>'
        '<text x="130" y="136" text-anchor="middle" font-size="11">inner</text>'
        "</svg>"
    )


def _seasons_svg():
    """Both Earths share the same axis tilt in space (parallel red lines).

    North is the top of each axis, leaned toward the right of the page.
    Left Earth (June): north leans toward the Sun. Right Earth (December): north leans away.
    """
    return (
        '<svg viewBox="0 0 420 200" width="100%" style="max-width:420px" role="img">'
        '<circle cx="210" cy="100" r="22" fill="#fde047" stroke="#a16207" stroke-width="2"/>'
        '<text x="210" y="104" text-anchor="middle" font-size="11">Sun</text>'
        '<ellipse cx="80" cy="100" rx="18" ry="18" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<line x1="88" y1="82" x2="72" y2="118" stroke="#b91c1c" stroke-width="2.4"/>'
        '<text x="80" y="160" text-anchor="middle" font-size="11">June: N toward Sun</text>'
        '<ellipse cx="340" cy="100" rx="18" ry="18" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<line x1="348" y1="82" x2="332" y2="118" stroke="#b91c1c" stroke-width="2.4"/>'
        '<text x="340" y="160" text-anchor="middle" font-size="11">December: N away</text>'
        '<text x="210" y="24" text-anchor="middle" font-size="12">axis tilt stays parallel (~23.5°)</text>'
        "</svg>"
    )


def _water_cycle_svg():
    return (
        '<svg viewBox="0 0 360 180" width="100%" style="max-width:360px" role="img">'
        '<rect x="0" y="130" width="360" height="50" fill="#93c5fd"/>'
        '<rect x="0" y="150" width="360" height="30" fill="#1d4ed8"/>'
        '<ellipse cx="80" cy="40" rx="50" ry="18" fill="#e2e8f0"/>'
        '<ellipse cx="160" cy="32" rx="40" ry="16" fill="#cbd5e1"/>'
        '<path d="M80 112 C80 70, 80 70, 80 52" fill="none" stroke="#0f172a" stroke-width="2"/>'
        '<polygon points="76,60 80,48 84,60" fill="#0f172a"/>'
        '<text x="92" y="80" font-size="11">evaporation</text>'
        '<path d="M150 48 L150 90" fill="none" stroke="#1d4ed8" stroke-width="2"/>'
        '<polygon points="146,86 150,98 154,86" fill="#1d4ed8"/>'
        '<text x="160" y="78" font-size="11">precipitation</text>'
        '<text x="200" y="168" font-size="12">ocean / lake</text>'
        "</svg>"
    )


def _atm_svg():
    return (
        '<svg viewBox="0 0 280 200" width="100%" style="max-width:280px" role="img">'
        '<rect x="40" y="20" width="200" height="160" fill="#e0f2fe" stroke="#0f172a"/>'
        '<rect x="40" y="140" width="200" height="40" fill="#86efac"/>'
        '<text x="140" y="178" text-anchor="middle" font-size="12">ground</text>'
        '<text x="140" y="40" text-anchor="middle" font-size="11">thinner air (lower pressure)</text>'
        '<text x="140" y="128" text-anchor="middle" font-size="11">thicker air (higher pressure)</text>'
        '<text x="140" y="14" text-anchor="middle" font-size="11">atmosphere</text>'
        "</svg>"
    )


def _spectra_star_svg():
    return (
        '<svg viewBox="0 0 360 110" width="100%" style="max-width:360px" role="img">'
        '<rect x="20" y="30" width="320" height="36" fill="url(#g1)" stroke="#0f172a"/>'
        '<defs><linearGradient id="g1" x1="0" x2="1">'
        '<stop offset="0" stop-color="#7c3aed"/><stop offset="0.2" stop-color="#2563eb"/>'
        '<stop offset="0.4" stop-color="#22c55e"/><stop offset="0.6" stop-color="#eab308"/>'
        '<stop offset="0.8" stop-color="#f97316"/><stop offset="1" stop-color="#ef4444"/>'
        '</linearGradient></defs>'
        '<rect x="70" y="30" width="6" height="36" fill="#0f172a"/>'
        '<rect x="140" y="30" width="6" height="36" fill="#0f172a"/>'
        '<rect x="220" y="30" width="6" height="36" fill="#0f172a"/>'
        '<text x="180" y="90" text-anchor="middle" font-size="12">rainbow with dark absorption lines</text>'
        "</svg>"
    )


def _lever_svg():
    """Class-1 lever: short load arm left, long effort arm right, effort pushed down."""
    return (
        '<svg viewBox="0 0 320 150" width="100%" style="max-width:320px" role="img">'
        '<polygon points="92,108 112,108 102,78" fill="#64748b"/>'
        '<line x1="40" y1="82" x2="290" y2="82" stroke="#0f172a" stroke-width="6"/>'
        '<rect x="42" y="54" width="36" height="24" fill="#93c5fd"/>'
        '<text x="60" y="48" text-anchor="middle" font-size="11">load</text>'
        '<text x="250" y="48" font-size="11">effort</text>'
        '<line x1="260" y1="82" x2="260" y2="118" stroke="#b91c1c" stroke-width="2.4"/>'
        '<polygon points="256,114 260,126 264,114" fill="#b91c1c"/>'
        '<text x="102" y="138" text-anchor="middle" font-size="12">fulcrum</text>'
        '<text x="70" y="100" font-size="10">short arm</text>'
        '<text x="180" y="100" font-size="10">long arm</text>'
        "</svg>"
    )


def _heat_paths_svg():
    return (
        '<svg viewBox="0 0 420 160" width="100%" style="max-width:420px" role="img">'
        '<rect x="8" y="8" width="128" height="144" fill="#f8fafc" stroke="#cbd5e1"/>'
        '<text x="72" y="26" text-anchor="middle" font-size="12">conduction</text>'
        '<circle cx="72" cy="62" r="14" fill="#fecaca" stroke="#991b1b"/>'
        '<text x="72" y="66" text-anchor="middle" font-size="9">hand</text>'
        '<rect x="40" y="76" width="70" height="16" fill="#f97316" stroke="#9a3412"/>'
        '<text x="72" y="110" text-anchor="middle" font-size="10">hot rod</text>'
        '<text x="72" y="138" text-anchor="middle" font-size="10">touch / solid</text>'
        '<rect x="146" y="8" width="128" height="144" fill="#f8fafc" stroke="#cbd5e1"/>'
        '<text x="210" y="26" text-anchor="middle" font-size="12">convection</text>'
        '<ellipse cx="210" cy="88" rx="38" ry="28" fill="#bfdbfe" stroke="#1d4ed8"/>'
        '<path d="M190 88 C190 64, 230 64, 230 88 C230 110, 190 110, 190 88" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        '<polygon points="226,72 230,62 236,74" fill="#b91c1c"/>'
        '<text x="210" y="138" text-anchor="middle" font-size="10">fluid loop</text>'
        '<rect x="284" y="8" width="128" height="144" fill="#f8fafc" stroke="#cbd5e1"/>'
        '<text x="348" y="26" text-anchor="middle" font-size="12">radiation</text>'
        '<circle cx="318" cy="78" r="16" fill="#fde047" stroke="#a16207"/>'
        '<line x1="336" y1="78" x2="392" y2="78" stroke="#ea580c" stroke-width="2"/>'
        '<line x1="332" y1="64" x2="378" y2="46" stroke="#ea580c" stroke-width="2"/>'
        '<line x1="332" y1="92" x2="378" y2="110" stroke="#ea580c" stroke-width="2"/>'
        '<circle cx="400" cy="78" r="10" fill="#93c5fd"/>'
        '<text x="348" y="138" text-anchor="middle" font-size="10">rays / no fluid</text>'
        "</svg>"
    )


def _electromagnet_svg():
    return (
        '<svg viewBox="0 0 400 180" width="100%" style="max-width:400px" role="img">'
        '<rect x="140" y="70" width="160" height="22" rx="6" fill="#94a3b8" stroke="#334155"/>'
        '<polygon points="300,70 332,81 300,92" fill="#64748b" stroke="#334155"/>'
        '<text x="168" y="62" font-size="11">iron nail / core</text>'
        '<path d="M158 68 C166 48, 174 48, 182 68 S198 94, 206 68 S222 48, 230 68 S246 94, 254 68 S270 48, 278 68" fill="none" stroke="#b91c1c" stroke-width="2.6"/>'
        '<path d="M158 90 L158 128 L88 128" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        '<path d="M254 90 L254 148 L88 148" fill="none" stroke="#1d4ed8" stroke-width="2"/>'
        '<line x1="78" y1="120" x2="78" y2="136" stroke="#0f172a" stroke-width="4"/>'
        '<line x1="88" y1="116" x2="88" y2="140" stroke="#0f172a" stroke-width="6"/>'
        '<text x="40" y="108" font-size="11">battery</text>'
        '<rect x="340" y="72" width="20" height="8" fill="none" stroke="#57534e" stroke-width="2"/>'
        '<rect x="340" y="84" width="20" height="8" fill="none" stroke="#57534e" stroke-width="2"/>'
        '<text x="336" y="112" font-size="10">clips</text>'
        '<text x="160" y="172" font-size="11">coil wraps the core; current from the battery</text>'
        "</svg>"
    )


def _orbit_svg():
    return (
        '<svg viewBox="0 0 360 280" width="100%" style="max-width:360px" role="img">'
        '<circle cx="180" cy="140" r="90" fill="none" stroke="#94a3b8" stroke-dasharray="6 4"/>'
        '<circle cx="180" cy="140" r="22" fill="#fde047" stroke="#a16207" stroke-width="2"/>'
        '<text x="180" y="144" text-anchor="middle" font-size="11">Sun</text>'
        '<circle cx="270" cy="140" r="14" fill="#93c5fd" stroke="#1e3a8a"/>'
        '<text x="270" y="176" text-anchor="middle" font-size="11">Earth</text>'
        '<line x1="254" y1="140" x2="220" y2="140" stroke="#b91c1c" stroke-width="2.5"/>'
        '<polygon points="226,134 212,140 226,146" fill="#b91c1c"/>'
        '<text x="226" y="128" font-size="12" fill="#b91c1c">g</text>'
        '<line x1="270" y1="124" x2="270" y2="86" stroke="#1d4ed8" stroke-width="2.5"/>'
        '<polygon points="264,94 270,78 276,94" fill="#1d4ed8"/>'
        '<text x="278" y="100" font-size="12" fill="#1d4ed8">v</text>'
        '<text x="180" y="258" text-anchor="middle" font-size="12">inward g + sideways v = orbit</text>'
        "</svg>"
    )


# ===========================================================================
# UNIT 5
# ===========================================================================

def _u5_questions():
    rows = [
        ("Kinetic energy is the energy of…",
         "motion", "A rolling ball has kinetic energy. Faster or more mass means more KE in this course’s picture.",
         ["stored height only", "food calories only", "temperature of empty space with no particles"]),
        ("Gravitational potential energy is energy stored because of…",
         "height in a gravitational field", "A book on a shelf can fall. The height stores energy that can become motion.",
         ["its color", "its temperature only", "whether it is a metal"]),
        ("Chemical energy in food or fuel is a form of…",
         "stored (potential) energy in bonds", "Eating or burning releases that store as motion, heat, and other forms.",
         ["kinetic energy of the whole Earth only", "sound that cannot become other forms", "a type of charge"]),
        ("A stretched rubber band stores…",
         "elastic potential energy", "The band can snap back and do work. Spring toys work the same way.",
         ["no energy until it is painted", "only gravitational energy", "nuclear energy"]),
        ("Thermal energy is the energy of…",
         "the random motion of particles in a sample", "Hot tea’s particles jostle more than iced tea’s. That jostling is thermal energy.",
         ["only the color red", "a magnet’s poles", "empty space with no particles"]),
        ("In science, work is done when a force…",
         "moves an object in the direction of that force (at least partly)",
         "$W=F\\times d$ when force and motion line up. Holding a backpack still is tiring, but work is 0 because d=0.",
         ["exists, even if nothing moves", "is imaginary", "equals mass"]),
        ("You push a box 3 m with a 10 N force in the same direction. Work is…",
         "30 J", "$W=10\\times3=30$ joules.",
         ["13 J", "3.3 J", "0 J"]),
        ("A simple machine such as a lever…",
         "can trade force for distance (or the reverse); it does not create energy",
         "You may push with less force over a longer path. Energy is still conserved aside from waste heat.",
         ["creates extra joules from nothing", "removes gravity", "only works on the Moon"]),
        ("A ramp lets you use a smaller force over a longer path. The trade is…",
         "less force, more distance", "Ideal work in equals work out. Real ramps waste some energy as heat from friction.",
         ["less force and less distance always", "more force and less distance always", "zero distance"]),
        ("The unit of work and of energy is the…",
         "joule (J)", "1 J is about the work to lift a small apple a short distance. Force in N times distance in m.",
         ["newton only", "kilogram", "°C"]),
        ("Conservation of energy means…",
         "energy can change form but the total stays the same in a closed system",
         "A pendulum’s KE and PE swap. Add thermal energy from friction and the mechanical total drops, but energy is not destroyed.",
         ["energy is created when things move", "energy vanishes at the top of a swing", "only kinetic energy exists"]),
        ("At the top of a frictionless hill a sled has 50 J of PE and 0 J of KE. At the bottom, KE is…",
         "50 J", "PE becomes KE. Total 50 J stays 50 J if we ignore friction.",
         ["0 J", "100 J", "25 J"]),
        ("A pendulum at the bottom of its swing has…",
         "maximum KE and minimum PE (for that swing)",
         "Lowest point: least height, most speed.",
         ["maximum PE and zero KE always", "no energy", "only chemical energy"]),
        ("If friction is present, some mechanical energy becomes…",
         "thermal energy", "Rubbing warms surfaces. The “missing” KE+PE went into particle jostling.",
         ["destroyed mass", "new protons", "negative time"]),
        ("Energy bars that start as PE=4, KE=0 and end as PE=1, KE=2, thermal=1 show…",
         "total 4 throughout; some energy became thermal",
         "4=1+2+1. Conservation holds. Mechanical energy dropped because of thermal.",
         ["energy was created", "total became 1", "KE cannot exist with PE"]),
        ("Temperature measures…",
         "how hot or cold, related to average particle motion",
         "A thermometer reading is not the same as how much energy flowed. A spark can be hotter than a bathtub but has less energy to share.",
         ["the amount of heat that always flows out", "mass", "volume only"]),
        ("Heat, in this course, is…",
         "energy that flows because of a temperature difference",
         "Heat is a transfer, not a substance you “own.” Energy flows from hotter to colder until they match.",
         ["a fluid called caloric that sits in objects forever", "the same word as temperature", "only infrared light"]),
        ("A drop of boiling water and a pot of boiling water are both at 100 °C. The pot can melt more ice because it has…",
         "more thermal energy (more particles at that temperature)",
         "Same temperature, different amount of stuff. Heat that can flow depends on both T and how much material.",
         ["a higher temperature than 100 °C", "less energy", "no particles"]),
        ("Energy naturally flows from…",
         "hotter to colder",
         "Ice in a drink warms; the drink cools. They head toward the same temperature.",
         ["colder to hotter with no machine ever", "only upward", "only in metals"]),
        ("Which pair is temperature versus heat?",
         "°C reading versus joules that flow",
         "Temperature is a reading. Heat is energy on the move because of a T difference.",
         ["kg versus N", "m/s versus m", "both are °C only"]),
        ("Conduction is heat transfer by…",
         "direct particle contact, often in solids",
         "A metal spoon in soup gets hot in your hand. Particles jostle neighbors.",
         ["bulk flow of fluid only", "empty-space radiation only", "sound"]),
        ("Convection is heat transfer by…",
         "moving blobs of fluid (liquid or gas)",
         "Warm air rises; cooler air sinks. A room heater uses this loop. Boiling water rolls.",
         ["only through a vacuum", "only in metals that cannot flow", "a type of light"]),
        ("Radiation is heat transfer by…",
         "electromagnetic waves, which can travel through empty space",
         "The Sun warms Earth through space. There is no air bridge to the Sun.",
         ["only conduction through a spoon", "only convection in water", "sound through a wall"]),
        ("A vacuum bottle slows heat flow because it…",
         "cuts conduction and convection with a gap, and shiny walls cut radiation",
         "All three paths are reduced. That is why drinks stay hot or cold longer.",
         ["creates energy", "removes the drink’s mass", "turns heat into mass"]),
        ("Why is a metal pan handle hotter than a wooden spoon in the same pot?",
         "metal is a better conductor",
         "Metals pass particle jostling quickly. Wood does not.",
         ["wood has more radiation always", "metal has no particles", "convection happens only in wood"]),
        ("Melting is a phase change from…",
         "solid to liquid at the melting temperature",
         "Energy goes into loosening the particle arrangement, not into raising T during the plateau.",
         ["liquid to gas", "gas to solid", "liquid to solid"]),
        ("During a boiling plateau on a heating curve, temperature…",
         "stays the same while the liquid becomes gas",
         "Added energy is used to separate particles, not to raise the thermometer.",
         ["must rise at 10 °C per second", "must fall", "becomes undefined"]),
        ("Condensation is…",
         "gas to liquid",
         "Steam hitting a mirror becomes droplets. Energy is released to the surroundings.",
         ["solid to gas", "liquid to solid", "solid to liquid"]),
        ("Why does sweating cool you?",
         "evaporation carries thermal energy away in the water vapor",
         "The fastest-escaping particles leave. The leftover sweat is cooler, and energy left your skin.",
         ["sweat adds heat to the body", "water cannot change phase", "condensation on skin is the cooling step"]),
        ("On a heating curve, a sloped part means T is rising. A flat part means…",
         "a phase change at constant temperature",
         "Slope: one phase warming. Flat: two phases present, energy going into the change of state.",
         ["the heater is off by definition", "mass is decreasing to zero", "density is infinite"]),
        ("A 4 kg bowling ball moving faster than a 4 kg ball at rest has more…",
         "kinetic energy", "Same mass, larger speed, more KE.",
         ["gravitational PE if they are at the same height", "mass", "charge"]),
        ("Lifting a 10 N book 2 m does how much gravitational work (force along the lift)?",
         "20 J", "$W=10\\times2=20$ J, which becomes extra PE.",
         ["12 J", "5 J", "0 J"]),
        ("A pendulum loses height each swing. The “missing” PE mostly became…",
         "thermal energy (and a little sound)",
         "Air and pivot friction warm the surroundings. Total energy is not gone from the universe.",
         ["new mass", "negative KE", "destroyed Earth gravity"]),
        ("Which is a temperature unit in this course?",
         "degrees Celsius (°C)", "Heat transfer is in joules. Do not mix the two.",
         ["joules", "newtons", "meters"]),
        ("Soup heating on a stove mainly uses which transfer in the liquid?",
         "convection (rolling hot fluid)",
         "The burner also conducts into the pot. Inside the soup, warm regions rise.",
         ["only radiation through a vacuum inside the soup", "sound", "electric current in the noodles"]),
        ("You feel warmth from a campfire on your face even to the side of the smoke. That path is mostly…",
         "radiation",
         "Light and infrared travel to your skin. Convection would carry hot air upward more than sideways.",
         ["conduction through a metal rod you are not holding", "only convection into your shoes", "sound"]),
        ("Ice at 0 °C melting to water at 0 °C requires energy even though T does not rise. That energy is…",
         "used to change the arrangement (phase), not the thermometer reading",
         "The plateau on a heating curve is this energy.",
         ["unnecessary because T is already 0", "mass energy of new protons", "only sound"]),
        ("Work is 0 when you hold a 50 N suitcase still for 10 s because…",
         "distance in the force’s direction is 0",
         "$W=Fd$ with d=0. Your muscles still use chemical energy inside you; that is a different bookkeeping.",
         ["force is 0", "time is 0", "the suitcase has no mass"]),
        ("A spring-launched cart: PE_elastic → KE. If 12 J were stored and 2 J become thermal, KE is…",
         "10 J", "12−2=10 J left as motion if we ignore other stores.",
         ["14 J", "2 J", "12 J"]),
        ("Which statement is correct?",
         "a large iceberg can have more thermal energy than a cup of tea even if the tea is hotter",
         "Thermal energy depends on how many particles and how they move. Temperature is the hotness reading.",
         ["higher temperature always means more total thermal energy than any colder object", "ice cannot have thermal energy", "tea has no particles"]),
        ("A metal rod with one end in a flame: the far end warms by…",
         "conduction",
         "Particle-to-particle jostling along the solid.",
         ["convection inside solid metal (metal is not flowing)", "the rod becoming a gas at once", "sound only"]),
        ("Boiling water at 100 °C continues to take energy. The extra energy…",
         "turns liquid into steam at the same temperature",
         "That is the boiling plateau.",
         ["raises T to 200 °C at once in an open pot at sea level", "freezes the water", "removes all mass"]),
        ("A closed thermos of hot cocoa later feels cooler. Energy left mainly by…",
         "imperfect insulation (some conduction, convection, and radiation still leak)",
         "Conservation: the cocoa’s thermal energy went into the room.",
         ["the cocoa’s energy being destroyed", "mass leaving if the lid stayed sealed and nothing spilled", "the thermos creating cold"]),
        ("Which device is a simple machine?",
         "a ramp (inclined plane)",
         "Ramps, levers, pulleys, and wheels trade force and distance.",
         ["a battery", "a thermometer", "a calendar"]),
        ("At the same height, a 2 kg brick has _____ gravitational PE than a 1 kg brick (same g).",
         "twice the", "PE grows with mass. Twice the stuff at that height stores twice the PE.",
         ["half the", "the same", "zero"]),
        ("Freezing is the reverse of melting. During freezing, the sample…",
         "releases energy to the surroundings while T stays at the freezing point",
         "Particles lock into a solid. That energy leaves as heat to the room.",
         ["must rise in temperature", "gains energy from the room to freeze", "becomes a gas first"]),
        ("Challenge Stretch: A 3 kg sled starts with 72 J PE and 0 KE. At a lower point PE=18 J and 8 J became thermal. Find KE there, then the leftover mechanical energy (KE+PE).",
         "46 J KE; 64 J mechanical",
         "Energy still totals 72 J. 18 + 8 + KE = 72, so KE=46 J. Mechanical leftover is 46+18=64 J (the 8 J thermal is no longer mechanical).",
         ["54 J KE; 72 J mechanical", "46 J KE; 46 J mechanical", "26 J KE; 44 J mechanical"]),
        ("Challenge Stretch: You lift a 20 N box 1.5 m, then carry it horizontally 4 m at constant height. Work against gravity for the whole trip?",
         "30 J", "Only the lift does gravitational work: $20\\times1.5=30$ J. Horizontal carry: force of gravity is perpendicular to motion, so that part is 0 in this course’s $W=Fd$ aligned case.",
         ["80 J", "110 J", "0 J"]),
        ("Challenge Stretch: 200 g of water cools 8 °C (c_water≈4.2 J/g·°C). A 20 g iron nail cools 80 °C (c_iron≈0.45 J/g·°C). Which released more energy, and about how many joules is each?",
         "the water: about 6720 J vs the nail’s about 720 J",
         "Q=mcΔT. Water: 200×4.2×8=6720 J. Nail: 20×0.45×80=720 J. The cooler, larger water sample still dumps more energy than the hotter tiny nail — temperature is not the energy total.",
         ["the nail, because 80 °C is ten times 8 °C", "they release the same 800 J", "the water, about 720 J vs 6720 J for the nail"]),
        ("Challenge Stretch: A heating curve is flat at 0 °C for 6 minutes, then slopes up. During those 6 minutes the sample is…",
         "melting: solid and liquid together at 0 °C",
         "The plateau is the phase change. After the slope starts, it is all liquid warming.",
         ["all steam at 0 °C", "cooling", "skipping the liquid phase"]),
        ("Challenge Stretch: Rank the three heat paths for warming your hands at a fire: radiation from flames, convection of hot air, conduction if you touch a metal grate.",
         "all three can happen; touching the grate is conduction and can burn",
         "You can feel radiation on your face, hot air (convection), and a searing grate (conduction).",
         ["only conduction exists near fires", "radiation cannot happen in air", "convection needs a vacuum"]),
        ("Challenge Stretch: An ideal ramp raises a 30 N crate 2 m while you push with 10 N along the ramp. How far must you push along the ramp?",
         "6 m",
         "Work on the crate equals $30\\times2=60$ J. Ideal $W=Fd$ along the ramp: $10\\times d=60$, so d=6 m. Smaller force, longer path.",
         ["2 m", "3 m", "20 m"]),
        ("Challenge Stretch: A pendulum’s lowest point has 8 J KE. If air takes 1 J per full cycle as thermal, KE at the next bottom is about…",
         "7 J",
         "From one bottom to the next bottom is one full cycle. Mechanical energy drops by 1 J into thermal, so KE at the next bottom is 8−1=7 J (same height extremes).",
         ["8 J", "9 J", "0 J"]),
        ("Challenge Stretch: 100 g of water cools 10 °C and a 100 g iron block cools 10 °C. Water usually releases more energy because…",
         "water stores more energy per degree (higher specific heat) than iron",
         "Same mass and same ΔT does not mean same energy. Water is “stubborn” about temperature change.",
         ["iron has more mass", "water cannot store energy", "°C is larger for iron"]),
        ("Challenge Stretch: A coaster’s first peak stores 80 J PE. At a 20 J PE dip, 6 J is already thermal. Find KE at the dip, and say whether it can climb a 75 J peak next.",
         "54 J KE; no, leftover mechanical is only 74 J",
         "Mechanical leftover is 80−6=74 J. At the dip, KE=74−20=54 J. A 75 J peak would need 75 J of mechanical energy; 74 J is not enough.",
         ["54 J KE; yes, 80 J is still available", "60 J KE; yes", "74 J KE; no"]),
    ]
    return fill_qs(_pack(rows), 55, lambda i: mq(
        f"A {i} N force pushes a box {i} m in the same direction. Work in J?",
        i * i, f"W=Fd={i}×{i}={i*i} J.", i, distractors=[2 * i, i, 0]
    ))


def build_unit5():
    title = "Physical Science Unit 5: Energy, Work, and Heat"
    description = (
        "Forms of energy, work and simple machines, conservation, temperature versus heat, "
        "conduction convection radiation, and phase changes — Grade 9, with energy-bar pictures."
    )
    concepts = [
        "Forms of energy",
        "Work and simple machines",
        "Conservation of energy",
        "Temperature vs heat",
        "Conduction, convection, radiation",
        "Phase changes",
    ]
    ican1 = [
        "I can name kinetic, gravitational PE, elastic PE, chemical, and thermal energy.",
        "I can give an everyday example of each.",
        "I can say energy is a stored or moving ability to cause change, measured in joules.",
    ]
    c1 = _with_ican(concept_block(
        "1. Forms of energy",
        [
            "Energy is the ability to cause change. We measure it in joules (J). A moving bike, a hot stove, a stretched bow, and a sandwich all “have energy” in different forms. Naming the form is the first skill in this unit.",
            "Kinetic energy (KE) is the energy of motion. A rolling ball has KE. More mass or more speed means more KE. Stop the ball and that KE has gone somewhere else — it did not vanish from the universe.",
            "Gravitational potential energy is stored because of height. A book on a high shelf can fall. Everyday analogy: the book is like money in a high piggy bank. Dropping it spends that store as motion.",
            "Elastic potential energy is stored in a stretch or squeeze: rubber bands, springs, trampolines. Chemical energy is stored in food and fuel. Thermal energy is the random jostling of particles — hot cocoa versus iced cocoa.",
            "Light, sound, and electric energy show up too. A speaker turns electric energy into sound. A lamp turns electric energy into light and thermal energy. We will not do Maxwell’s equations. We will just name the form.",
            "Later lessons show that these names are chapters of one bank account. The account’s total is conserved. The chapter titles change.",
        ],
        "Conservation problems are just renaming: PE to KE to thermal. If the names are mush, the bar charts will look like art instead of accounting.",
        "For any scene, list what is moving (KE), what is high (grav PE), what is stretched (elastic), what is hot (thermal), and what is food/fuel (chemical). That list is the whole lesson.",
        lesson_figure(
            energy_bars_svg(ke=1, pe=4, thermal=0),
            "Energy bars at the top of a hill",
            "Tall PE, tiny KE. The total height of the bars is the account balance.",
        )
        + solved(1, "A ball rolling on a flat floor has which main mechanical form?",
                 ["It is moving, so it has kinetic energy.",
                  "Height is not changing on a flat floor, so grav PE is not changing.",
                  "Name it KE."],
                 "kinetic energy", "", "Easy")
        + solved(2, "A stretched bow about to shoot an arrow stores which form?",
                 ["The bow is deformed like a spring.",
                  "That store is elastic potential energy.",
                  "When released, it becomes the arrow’s KE (and some thermal/sound)."],
                 "elastic potential energy", "", "Medium")
        + solved(3, "Why can a small meteor have enormous kinetic energy even if it is not as massive as a truck?",
                 ["KE grows with speed a lot in the real world (faster means much more KE).",
                 "A meteor can move many times faster than a truck.",
                 "Form is still KE; the amount can be huge because of speed."],
                 "high speed → large KE", "", "Hard"),
        ("Calling all stored energy “chemical”",
         "A book on a shelf is gravitational, not chemical. A spring is elastic, not food energy. Use the situation, not one favorite word."),
        ("List forms before numbers",
         "Write KE / PE_g / PE_el / thermal / chemical. Tick which are large. Then the bar chart draws itself."),
        ican1, 1,
    ), ican1)

    ican2 = [
        "I can compute $W=Fd$ when force and motion line up.",
        "I can explain why holding still is 0 work in the physics definition.",
        "I can say a simple machine trades force and distance, not free energy.",
    ]
    c2 = _with_ican(concept_block(
        "2. Work and simple machines",
        [
            "In everyday talk, “work” means effort. In physics, work is done when a force makes something move (at least partly) in the force’s direction. The aligned formula is $W=F\\times d$, with work in joules.",
            "Push a box 3 m with 10 N in the same direction: $W=30$ J. Hold a 50 N suitcase still: d=0, so W=0, even though your arms are tired. Your body is still using chemical energy inside muscle — that is a different account.",
            "A simple machine (ramp, lever, pulley, wheel) helps you trade a smaller force for a longer distance, or the reverse. It does not create extra joules. Ideal case: work in equals work out.",
            "Everyday analogy: a long gentle ramp into a truck. You push with less force, but you walk farther. A steep board is shorter and harder. The box still gains the same gravitational PE if it ends at the same height (ignoring friction).",
            "Friction on a real ramp turns some work into thermal energy. You must put in a bit more work than the PE you get. Conservation still holds; some energy became heat.",
            "The joule links this lesson to the next: work done on a system can show up as KE, PE, or thermal energy.",
        ],
        "Conservation bar charts often start with “someone did 20 J of work.” If work is fuzzy, the first bar has no meaning.",
        "Write F, write d, check they line up. If d=0, W=0. If a machine is involved, ask what was traded: force or distance, not extra energy from nowhere.",
        lesson_figure(
            _lever_svg(),
            "A lever trades force and distance",
            "Small effort over a long arm can lift a larger load over a short arm.",
        )
        + solved(4, "A 10 N force pushes a box 3 m in the same direction. Find work.",
                 ["$W=F d$.",
                  "$10\\times3=30$.",
                  "Work is 30 J."],
                 "30 J", "", "Easy")
        + solved(5, "You hold a 40 N backpack still for 20 s. Physics work on the backpack?",
                 ["The backpack’s distance is 0.",
                  "$W=F\\times0=0$.",
                 "Time does not enter $W=Fd$."],
                 "0 J", "Tired muscles still used chemical energy inside you.", "Medium")
        + solved(6, "An ideal lever lifts a 12 N load with 4 N effort. How do the distances compare?",
                 ["Ideal work in = work out: $4\\times d_e=12\\times d_l$.",
                  "So $d_e=3 d_l$.",
                  "You push three times as far with one-third the force."],
                 "effort moves 3× as far", "", "Hard"),
        ("Counting time as work",
         "Holding a piano for an hour is exhausting, but if it did not move, physics work on the piano is 0. Do not multiply by seconds in $W=Fd$."),
        ("Check alignment of F and d",
         "Carrying a box down a hallway at constant height: gravity is down, motion is horizontal, so gravitational work is 0. You still did work against friction, which is a different force."),
        ican2, 6,
    ), ican2)

    ican3 = [
        "I can state conservation of energy.",
        "I can swap PE and KE on a frictionless hill.",
        "I can put “missing” mechanical energy into a thermal bar.",
    ]
    c3 = _with_ican(concept_block(
        "3. Conservation of energy",
        [
            "Conservation of energy: energy can change form, but the total in a closed system stays the same. We do not destroy joules. We rename them.",
            "A sled on a smooth hill: at the top, PE is large and KE is small. At the bottom, PE is small and KE is large. If friction is ignored, the numbers add to the same total.",
            "A pendulum is the same story swinging. Bottom: max KE, min PE. Ends: max PE, min KE. Everyday analogy: a money envelope. Cash (KE) versus savings (PE). The envelope total matches unless you spend some as thermal “fees.”",
            "Friction and air resistance spend mechanical energy as thermal energy (and a little sound). The mechanical bars shrink; a thermal bar grows; the grand total still matches.",
            "Energy bar charts make this visible. Draw PE, KE, and thermal before and after. The stacked height should match if the system is closed.",
            "Work from outside can add energy (you pushing a swing). Heat leaving can remove energy (a cooling pie). Then the system was not closed, and the total inside can change — the energy went next door.",
        ],
        "Every later “where did the speed go?” question is a thermal bar, not a magic delete key.",
        "Write total before. Write total after. If mechanical dropped, add thermal. If the numbers still miss, ask whether energy entered or left the system.",
        lesson_figure(
            energy_bars_svg(ke=3, pe=1, thermal=1),
            "After a rough slide: KE, leftover PE, and thermal",
            "The three bars should add to the same total as the start.",
        )
        + solved(7, "Top of a smooth hill: PE=50 J, KE=0. Bottom: PE=0. Find KE.",
                 ["Ignore friction, so total stays 50 J.",
                  "All 50 J become KE at the bottom.",
                  "KE=50 J."],
                 "50 J", "", "Easy")
        + solved(8, "Start PE=40 J, KE=0. Later PE=10 J and 5 J became thermal. Find KE.",
                 ["Total is still 40 J.",
                  "10 + 5 + KE = 40.",
                  "KE=25 J."],
                 "25 J", "", "Medium")
        + solved(9, "A pendulum slowly dies. Where did the energy go, and was it destroyed?",
                 ["Air and the pivot warmed (thermal) and you heard a little sound.",
                  "Mechanical energy dropped.",
                  "Energy was not destroyed; it spread into the room."],
                 "became thermal (and sound); not destroyed", "", "Hard"),
        ("Saying energy is “used up” as if it were gone",
         "Used up in everyday talk means “not useful to us anymore.” In physics it still exists, usually as thermal energy we cannot easily put back into the sled."),
        ("Draw before-and-after bars",
         "Three boxes: PE, KE, thermal. Fill numbers so the totals match. That picture catches a 50 J that “became 0.”"),
        ican3, 11,
    ), ican3)

    ican4 = [
        "I can tell temperature (°C) from heat (joules flowing).",
        "I can explain why a spark can be hotter than a bathtub but melt less ice.",
        "I can say energy flows from hotter to colder.",
    ]
    c4 = _with_ican(concept_block(
        "4. Temperature vs heat",
        [
            "Temperature is a number that tells how hot or cold something is. In this course we use degrees Celsius (°C). It connects to how vigorously particles jostle, on average.",
            "Heat is energy that flows because of a temperature difference. Heat is measured in joules. It is a transfer, not a fluid sitting inside an object named “heat content” in old language.",
            "Everyday analogy: temperature is the speedometer reading of particle jostling. Heat is the money that moves from a rich (hot) account to a poorer (cold) one until they match.",
            "A drop of boiling water and a pot of boiling water are both 100 °C. The pot can melt more ice because it has more particles at that temperature — more thermal energy to share.",
            "A spark can have a very high temperature and still melt little ice. High T is not the same as lots of energy. Amount of stuff matters.",
            "Energy flows from hotter to colder on its own. Refrigerators can pump energy the other way, but they need a machine and extra energy input. That is a later story; the natural direction is hot toward cold.",
        ],
        "Phase-change plateaus make no sense if you think “adding energy always raises °C.” Heat can go into a change of state instead.",
        "Ask: is this a thermometer reading or a flow of joules? Then ask how much stuff is at that reading. A tiny spark versus a lake is the test.",
        lesson_figure(
            (
                '<svg viewBox="0 0 320 180" width="100%" style="max-width:320px" role="img">'
                '<path d="M30 30 L30 140 L120 140 L120 30" fill="none" stroke="#0f172a" stroke-width="3"/>'
                '<rect x="34" y="70" width="82" height="66" fill="#fecaca"/>'
                '<text x="75" y="108" text-anchor="middle" font-size="12">hot tea</text>'
                '<path d="M190 30 L190 140 L280 140 L280 30" fill="none" stroke="#0f172a" stroke-width="3"/>'
                '<rect x="194" y="90" width="82" height="46" fill="#bfdbfe"/>'
                '<polygon points="220,118 248,118 234,128" fill="#fff" stroke="#64748b"/>'
                '<text x="235" y="84" text-anchor="middle" font-size="12">ice</text>'
                '<line x1="124" y1="90" x2="184" y2="90" stroke="#b91c1c" stroke-width="2.4"/>'
                '<polygon points="176,86 188,90 176,94" fill="#b91c1c"/>'
                '<text x="160" y="78" text-anchor="middle" font-size="11">energy</text>'
                "</svg>"
            ),
            "Heat is energy on the move",
            "Arrow from hot tea toward ice: tea cools, ice warms. They head toward the same temperature.",
        )
        + solved(10, "Which is a temperature: 80 °C or 80 J?",
                 ["°C is a hotness reading.",
                  "Joules measure energy, including heat transfer.",
                  "80 °C is temperature."],
                 "80 °C", "", "Easy")
        + solved(11, "Why can a bathtub of warm water melt more ice than a tiny 400 °C spark?",
                 ["The spark is hotter but tiny.",
                  "The tub has far more thermal energy to give.",
                  "Temperature ≠ total energy."],
                 "tub has more energy to transfer", "", "Medium")
        + solved(12, "Ice in a drink: which way does energy flow, and what happens to each temperature?",
                 ["Drink is hotter than ice, so energy flows into the ice.",
                  "The drink’s temperature drops; ice may melt at 0 °C.",
                  "They move toward a shared final temperature."],
                 "hot → cold; drink cools", "", "Hard"),
        ("Using heat and temperature as identical words",
         "You cannot “pour 20 °C into a cup.” You can transfer joules. The thermometer then may rise."),
        ("Name the two objects and which is hotter",
         "Energy’s natural path is from the hotter name to the colder name. Write that arrow before you talk about melting."),
        ican4, 16,
    ), ican4)

    ican5 = [
        "I can define conduction, convection, and radiation.",
        "I can match a spoon, a heater loop, and sunlight to those three.",
        "I can explain a vacuum bottle in those three words.",
    ]
    c5 = _with_ican(concept_block(
        "5. Conduction, convection, radiation",
        [
            "Heat can travel three ways. Conduction is particle-to-particle contact. A metal spoon in soup burns your fingers. Solids, especially metals, are good conductors. Wood and air are poorer conductors (insulators).",
            "Convection is bulk motion of a fluid. Warm air rises; cooler air sinks. A room heater starts a loop. Boiling water rolls. There is no convection in empty space, because there is no fluid to flow.",
            "Radiation is energy in electromagnetic waves. It does not need air. The Sun warms Earth through space. You feel a campfire on your face even when the smoke goes up, not into your cheeks.",
            "Everyday analogy: conduction is whispering ear-to-ear. Convection is passing a note by walking it across the room. Radiation is shouting across a field (or through space).",
            "A thermos tries to block all three: a vacuum gap kills conduction and convection, and shiny walls reflect radiation. Nothing is perfect, so cocoa still cools — slowly.",
            "Unit 6 will treat light as a wave. For now, radiation just means “energy through waves, even in a vacuum.”",
        ],
        "Earth’s weather (Unit 8) is huge convection. The Sun’s energy is radiation. If the three words blur, seasons and climate stories collapse into “heat happens.”",
        "Point to the path: touching? conduction. Fluid circulating? convection. Across a gap or space, especially light-like? radiation.",
        lesson_figure(
            _heat_paths_svg(),
            "Three heat paths side by side",
            "Left: conduction by touch along a rod. Middle: convection as a fluid loop. Right: radiation as rays that need no fluid.",
        )
        + solved(13, "A metal pan handle gets hot. Which path?",
                 ["The handle is a solid touching the pan.",
                  "Particles jostle neighbors along the metal.",
                  "That is conduction."],
                 "conduction", "", "Easy")
        + solved(14, "Warm air rising above a heater is…",
                 ["Air is a fluid that can flow.",
                  "Hot air rises and cooler air takes its place.",
                  "That loop is convection."],
                 "convection", "", "Medium")
        + solved(15, "How does a vacuum bottle slow all three paths?",
                 ["The gap is nearly empty, so little conduction and no convection current.",
                  "Shiny walls reflect radiation.",
                  "All three are reduced, not magically zero."],
                 "vacuum + shiny walls", "", "Hard"),
        ("Calling sunlight convection",
         "There is no air between Sun and Earth that carries the energy as a flowing blob. Space is empty. That path is radiation."),
        ("Name the medium",
         "Solid contact → conduction. Liquid/gas flowing → convection. No medium needed → radiation. The medium sentence picks the word."),
        ican5, 21,
    ), ican5)

    ican6 = [
        "I can name melting, freezing, evaporation/boiling, and condensation.",
        "I can read a heating-curve plateau as a phase change at constant T.",
        "I can explain sweating as evaporation carrying energy away.",
    ]
    c6 = _with_ican(concept_block(
        "6. Phase changes",
        [
            "A phase change is a change of state: solid, liquid, or gas. Melting is solid to liquid. Freezing is the reverse. Evaporation and boiling are liquid to gas. Condensation is gas to liquid. Sublimation is solid to gas (dry ice).",
            "During a phase change, added energy can go into rearranging particles instead of raising temperature. That is why a heating curve has flat plateaus at 0 °C (ice/water) and 100 °C (water/steam) at everyday pressure.",
            "Everyday analogy: remodeling a house. You can spend money on a new layout (phase change) without making the rooms “hotter.” The thermometer can sit still while energy is busy.",
            "Boiling happens throughout a liquid at the boiling temperature. Evaporation can happen at the surface at many temperatures — puddles disappear on cool days. Sweating cools you because the escaping vapor carries energy away from your skin.",
            "Condensation releases energy. Steam burns are nasty because steam becomes liquid on your skin and dumps that extra energy. Fog on a mirror is condensation of water vapor.",
            "Unit 8’s water cycle is this lesson on a planet: evaporation from oceans, condensation into clouds, precipitation back down.",
        ],
        "If you think adding energy always raises °C, you will misread every heating-curve quiz and every “why is steam worse than water” safety talk.",
        "On a heating curve, slope means T changing in one phase. Flat means two phases and a change of state. Label the flat with melting or boiling before you pick an answer.",
        lesson_figure(
            xy_graph(
                curves=[("#b45309", [(0, -20), (8, 0), (18, 0), (40, 100), (52, 100), (64, 140)])],
                points=[(13, 0, "melt"), (46, 100, "boil")],
                xlim=(0, 70), ylim=(-30, 160), w=340, h=260, xlab="time (min)", ylab="T (°C)",
            ),
            "A heating curve for water (sketch)",
            "Flat at 0 °C: melting. Flat at 100 °C: boiling. Slopes: one phase warming.",
        )
        + solved(16, "Ice to water at 0 °C is called…",
                 ["Solid becomes liquid.",
                  "The name is melting.",
                  "T can stay 0 °C during the change."],
                 "melting", "", "Easy")
        + solved(17, "Why is a heating curve flat while water boils?",
                 ["Energy is used to separate liquid particles into gas.",
                  "That job does not raise the thermometer.",
                  "T stays at the boiling point until the liquid is gone."],
                 "phase change at constant T", "", "Medium")
        + solved(18, "Why does sweating cool you on a dry day?",
                 ["Sweat evaporates from the skin.",
                  "The escaping vapor carries thermal energy away.",
                  "Your skin loses energy and feels cooler."],
                 "evaporation removes energy", "", "Hard"),
        ("Thinking the temperature must rise whenever a heater is on",
         "During a plateau the heater is on, energy is entering, and T is stuck. The energy is busy changing state."),
        ("Label every flat and every slope",
         "Write “solid warming,” “melting,” “liquid warming,” “boiling,” “gas warming” on the curve. Then the question is a reading task, not a memory stunt."),
        ican6, 26,
    ), ican6)

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6
# ===========================================================================

def _u6_questions():
    rows = [
        ("A wave is a disturbance that…",
         "transfers energy without transferring the medium’s leftover bulk (the rope stays a rope)",
         "A stadium wave: people stand and sit; the “wave” travels. People do not run around the stadium.",
         ["moves all the matter permanently to the other end always", "is the same as a particle of the rope leaving", "cannot carry energy"]),
        ("The crest of a wave is…",
         "the highest point", "The trough is the lowest point. Amplitude is the height from the middle line to a crest.",
         ["the lowest point", "the wavelength itself", "the speed"]),
        ("Wavelength (λ) is…",
         "the distance from one crest to the next crest (or trough to trough)",
         "It is a length, in meters. It is not a time.",
         ["how many crests pass per second", "the height of a crest", "the energy color always"]),
        ("Frequency (f) is…",
         "how many waves pass a point each second, in hertz (Hz)",
         "1 Hz means one wave per second. Higher frequency is more waves in the same time.",
         ["the length of one wave", "the height", "a unit of mass"]),
        ("Amplitude is most closely tied to…",
         "how much energy the wave carries (for a given type)",
         "A taller water wave can do more. For sound, larger amplitude is louder. For light, related to brightness.",
         ["the color always", "the medium’s name only", "the number of seconds in a day"]),
        ("The wave-speed formula is…",
         "v = f λ", "Speed equals frequency times wavelength. Units: Hz times meters gives m/s.",
         ["v = f / λ", "v = f + λ", "v = λ / f²"]),
        ("A wave has f=5 Hz and λ=4 m. Speed is…",
         "20 m/s", "$v=5\\times4=20$ m/s.",
         ["1.25 m/s", "9 m/s", "0.8 m/s"]),
        ("If speed is fixed (same medium) and frequency doubles, wavelength…",
         "halves", "$v=fλ$ so λ=v/f. Double f, half λ.",
         ["doubles", "stays the same", "becomes zero"]),
        ("A sound wave travels 340 m/s with f=170 Hz. Wavelength is…",
         "2 m", "$λ=v/f=340/170=2$ m.",
         ["51000 m", "170 m", "0.5 m"]),
        ("Wave speed in a given medium is mostly set by…",
         "the medium (and conditions like temperature), not by how hard you wave",
         "Shouting louder does not make sound faster in the same air. It makes amplitude larger.",
         ["only the amplitude", "only the color of the wall", "your age"]),
        ("Sound is a _____ wave that needs a _____ .",
         "mechanical (vibration) wave; medium such as air, water, or a solid",
         "No air in space means no shout. Movies with space explosions you can hear are pretending.",
         ["light wave; vacuum only", "magnetic-only wave; empty space required", "silent wave; no energy"]),
        ("A higher-pitch sound has a higher…",
         "frequency", "Tiny fast vibrations: high pitch. Slow vibrations: low pitch. Loudness is amplitude, not pitch.",
         ["wavelength always, in every medium, with f falling", "mass of the listener", "color"]),
        ("Sound usually travels fastest in…",
         "solids, then liquids, then gases",
         "Particles are closer in solids, so the vibration is passed more quickly. (There are exceptions; this is the Grade 9 pattern.)",
         ["outer space vacuum", "always slowest in steel", "only in helium balloons"]),
        ("An echo is…",
         "reflected sound", "The wave bounces off a cliff or a gym wall and returns.",
         ["sound becoming light", "a change of medium into a vacuum", "frequency becoming zero"]),
        ("Why can you hear around a doorway better than you can see around it?",
         "sound waves have longer wavelengths and diffract (bend around edges) more in everyday rooms",
         "Light’s wavelength is tiny, so it casts sharper shadows. Sound leaks around corners.",
         ["sound is not a wave", "light has no energy", "doorways block all waves equally"]),
        ("White light through a prism spreads into colors because…",
         "different colors refract by different amounts",
         "The rainbow was in the white light as a mix. The prism sorts it.",
         ["the prism paints the light with pigments", "white is a single frequency", "prisms create sound"]),
        ("The color of visible light is tied mainly to…",
         "frequency (and wavelength in a given medium)",
         "Red has longer wavelength than violet in air. Frequency is what your eye-brain system treats as color.",
         ["only amplitude", "only loudness", "only temperature of your shoes"]),
        ("An object looks red in white light because it…",
         "reflects red and absorbs other visible colors",
         "You see the reflected part. A red shirt in red light still looks red; in green light it can look dark.",
         ["emits only green", "absorbs red and reflects everything else", "has no interaction with light"]),
        ("Black cloth in sunlight warms more than white cloth because black…",
         "absorbs more of the light’s energy",
         "White reflects more. Absorbed light energy becomes thermal energy.",
         ["reflects all light", "cannot absorb energy", "is colder by definition of dye"]),
        ("A green filter on a flashlight…",
         "lets green through and blocks other colors",
         "Filters subtract. They do not add a new paint.",
         ["paints the light with green pigment atoms from the plastic always", "lets only red through", "stops all light including green"]),
        ("The law of reflection says the angle of incidence equals…",
         "the angle of reflection",
         "Both angles are measured from the normal (a line perpendicular to the surface).",
         ["the angle of refraction always", "90° always", "zero always"]),
        ("Refraction is…",
         "the bending of a wave when it changes speed in a new medium",
         "A straw in water looks bent. Light slows in water and changes direction.",
         ["the bouncing of a wave from a mirror only", "sound becoming light", "a type of charge"]),
        ("Light going from air into water usually…",
         "slows down and bends toward the normal",
         "Slower in water. The ray kinks toward the dashed normal line.",
         ["speeds up and bends away always", "stops", "becomes sound"]),
        ("A mirror image looks reversed left-right in everyday talk because…",
         "light reflects, and the geometry flips front-to-back",
         "Reflection is not the same as refraction through a lens.",
         ["mirrors change the frequency to a new color always", "mirrors absorb all light", "there is no law of reflection"]),
        ("Why does a pool look shallower than it is?",
         "refraction bends the light from the bottom so your brain misjudges depth",
         "The rays kink at the water surface. Your brain assumes straight-line light.",
         ["water removes the bottom", "reflection deletes depth", "sound in the pool"]),
        ("The electromagnetic spectrum includes…",
         "radio, micro, infrared, visible, ultraviolet, X-rays, gamma",
         "All are the same kind of wave at different frequencies. Visible is the tiny rainbow slice we see.",
         ["only sound", "only water waves", "only alpha particles of helium nuclei"]),
        ("Which EM wave has the longest wavelength?",
         "radio", "Radio is long λ, low f. Gamma is short λ, high f. All travel at c in vacuum.",
         ["gamma", "X-ray", "violet visible"]),
        ("Which EM wave has the highest frequency in this list: infrared, green light, X-ray?",
         "X-ray", "X-rays are higher f than visible, which is higher than infrared.",
         ["infrared", "green light", "they all have identical f"]),
        ("In vacuum, all electromagnetic waves travel at…",
         "the same speed c (about 3×10⁸ m/s)",
         "Radio and gamma have the same speed in empty space. Frequency and wavelength trade so $c=fλ$.",
         ["speeds proportional to their color only, even in vacuum", "the speed of sound", "zero"]),
        ("UV from the Sun can cause sunburn. UV has _____ frequency than visible light.",
         "higher", "Ultraviolet is beyond violet: higher f, more energy per wave packet in a later course’s language. Here: higher f, more potentially damaging.",
         ["lower", "zero", "the same as radio"]),
        ("From crest to next crest is 2 m. That length is…",
         "wavelength", "Crest-to-crest is the definition of λ.",
         ["amplitude", "period in seconds", "frequency in Hz"]),
        ("f=10 Hz, λ=2 m, v=…",
         "20 m/s", "$10\\times2=20$.",
         ["5 m/s", "12 m/s", "0.2 m/s"]),
        ("A guitar string’s pitch rises when the string is tighter because…",
         "the vibration frequency increases",
         "Tighter (and shorter) strings vibrate faster. Faster f is higher pitch.",
         ["the room’s air becomes a vacuum", "amplitude must fall to zero", "wavelength in air becomes infinite"]),
        ("Thunder is heard after lightning because…",
         "light travels much faster than sound",
         "You see the flash almost at once. Sound crawls at about 340 m/s in air.",
         ["sound is not a wave", "light is slower than sound", "they are the same wave"]),
        ("A red apple in green light tends to look dark because…",
         "it has little red to reflect and absorbs the green",
         "No matching color to bounce to your eyes.",
         ["it reflects all green", "green light becomes red in fruit", "apples emit X-rays"]),
        ("A laser pointer hits a mirror. If the incoming angle from the normal is 30°, the outgoing angle from the normal is…",
         "30°", "Angle in equals angle out, both from the normal.",
         ["60°", "90°", "0° always"]),
        ("Radio waves and gamma rays in space have the same…",
         "speed (c)",
         "Different f and λ, same vacuum speed. $c=fλ$ still holds.",
         ["frequency", "wavelength", "ability to tan skin equally"]),
        ("3 crests pass a dock each second. Frequency is…",
         "3 Hz", "Three waves per second is 3 Hz.",
         ["3 m", "1/3 Hz", "3 m/s always without λ"]),
        ("If λ=0.5 m and v=340 m/s, f=…",
         "680 Hz", "$f=v/λ=340/0.5=680$ Hz.",
         ["170 Hz", "340.5 Hz", "0.0015 Hz"]),
        ("A transverse wave’s particles move _____ to the wave’s travel direction.",
         "perpendicular",
         "A rope wave: the rope goes up and down while the wave goes along the rope. Light is transverse. Sound in air is longitudinal (back and forth along the travel).",
         ["only in a circle of infinite radius", "not at all", "at the speed of light always"]),
        ("Loudness of a sound is most related to…",
         "amplitude", "Bigger push on the air, louder sound. Pitch is frequency.",
         ["color", "only the medium’s name", "the letter λ always"]),
        ("Infrared is often felt as…",
         "warmth (thermal radiation)",
         "Remote controls and heat lamps use IR. It is not visible, but it is still EM.",
         ["a bass guitar note", "a smell", "a proton beam"]),
        ("When light enters glass it slows. Frequency stays the same, so wavelength in glass…",
         "gets shorter",
         "$v=fλ$. Smaller v, same f, smaller λ.",
         ["gets longer", "must become sound", "becomes infinite"]),
        ("A rainbow’s red appears on the outside because…",
         "red is bent less than violet in the raindrop’s refraction",
         "Different colors take slightly different paths. That is dispersion, a refraction story.",
         ["red is a sound", "violet is longer λ than red", "raindrops absorb all red"]),
        ("You can see the Moon because…",
         "it reflects sunlight to your eyes",
         "The Moon is not a visible-light lamp. Reflection makes it visible.",
         ["it emits only radio", "it is on fire like the Sun", "sound from the Moon"]),
        ("A police siren’s pitch seems to drop after it passes (Doppler idea, Grade 9 level) because…",
         "the waves behind the source are more stretched (lower f)",
         "Motion of the source changes the spacing of waves. You do not need a formula here, just the stretch/squeeze picture.",
         ["the siren’s amplitude became the color red", "sound stops being a wave", "light speed changed in air"]),
        ("Challenge Stretch: A string wave has v=12 m/s. You count 3 crests in 0.5 s at one spot, and neighboring crests are how far apart?",
         "2 m",
         "f=3/0.5=6 Hz. $λ=v/f=12/6=2$ m. Two steps: frequency from a count, then λ from v=fλ.",
         ["4 m", "6 m", "12 m"]),
        ("Challenge Stretch: Light in vacuum c=3.0×10⁸ m/s. In glass v=2.0×10⁸ m/s. If f stays 5.0×10¹⁴ Hz, λ in glass is…",
         "4.0×10⁻⁷ m",
         "$λ=v/f=(2.0\\times10^{8})/(5.0\\times10^{14})=4.0\\times10^{-7}$ m. In vacuum it would be 6.0×10⁻⁷ m.",
         ["6.0×10⁻⁷ m", "2.5×10²² m", "1.0×10⁻⁶ m"]),
        ("Challenge Stretch: A hiker sees a firework flash and hears the boom 2.5 s later. Sound in air is 340 m/s. Find the distance, then about how long the light took if c=3.0×10⁸ m/s.",
         "850 m; about 2.8×10⁻⁶ s (tiny compared with 2.5 s)",
         "Distance ≈ $340\\times2.5=850$ m. Light time is $850/(3.0\\times10^{8})\\approx2.8\\times10^{-6}$ s, so the delay is almost all sound.",
         ["850 m; 2.5 s for the light too", "340 m; 2.5 s for light", "85 m; 0 s exactly"]),
        ("Challenge Stretch: Two lab tones travel in the same air at 330 m/s: 110 Hz and 330 Hz. Find both wavelengths, then the ratio λ_low/λ_high.",
         "3 m and 1 m; ratio 3",
         "$λ=v/f$. 330/110=3 m and 330/330=1 m. Same medium, triple frequency, one-third wavelength, so the ratio is 3.",
         ["1 m and 3 m; ratio 1/3", "330 m and 110 m; ratio 3", "3 m and 3 m; ratio 1"]),
        ("Challenge Stretch: A light ray in air hits water. The speed drops. Why does the ray bend toward the normal, not away?",
         "the part of the wavefront that hits first slows first, so the wavefront kinks toward the normal",
         "Grade 9 picture: one side of the “wave marching line” hits the slow medium first and lags, rotating the direction toward the normal.",
         ["water magnetically pulls photons sideways only", "frequency increases a lot so v rises", "reflection is the only bending"]),
        ("Challenge Stretch: A Wi-Fi radio wave has f=5.0×10⁹ Hz. Using c=3.0×10⁸ m/s, find λ, then say whether that is closer to 1 mm, 6 cm, or 300 m.",
         "0.060 m, closest to 6 cm",
         "$λ=c/f=(3.0\\times10^{8})/(5.0\\times10^{9})=0.060$ m, which is 6 cm. Not a millimeter and not a football-field radio tower wave.",
         ["0.060 m, closest to 1 mm", "1.5×10¹⁸ m, closest to 300 m", "5.0×10⁹ m, closest to 300 m"]),
        ("Challenge Stretch: Why is a red exit sign still useful in a smoky room compared with a blue one (simple wave idea)?",
         "longer-wavelength red scatters less in many smokes/fogs than blue",
         "Blue is shorter λ and more easily bounced around by small particles. Red gets through better. (Real codes also use brightness and contrast.)",
         ["red is a sound wave", "blue has longer λ than red", "smoke blocks only red"]),
        ("Challenge Stretch: Sound λ≈1 m hits a 1 m doorway and spreads into the hall. Red light λ≈7×10⁻⁷ m hits the same doorway. Which spreads more into the “shadow,” and why?",
         "the sound, because its wavelength is comparable to the gap while light’s is much smaller",
         "Diffraction is strong when λ is not tiny compared with the opening. Sound’s 1 m wave and a 1 m door match; visible light is a million times shorter, so it makes a sharp shadow. Spreading is not a one-word label — it is λ versus gap size.",
         ["the light, because it is faster", "neither, because only particles diffract", "the light, because red has the longest EM wavelength of all waves"]),
        ("Challenge Stretch: v=fλ. A student triples f and also triples λ, claiming speed is unchanged. The error is…",
         "in one medium you cannot freely triple both; if f triples at fixed v, λ must become one third",
         "v is set by the medium. $v=fλ$ is a constraint, not two independent sliders.",
         ["v always triples with f", "λ cannot exist", "frequency is a length"]),
    ]
    return fill_qs(_pack(rows), 55, lambda i: mq(
        f"A wave has frequency {i+2} Hz and wavelength 3 m. Speed in m/s?",
        3 * (i + 2), f"v=fλ={i+2}×3={3*(i+2)}.", i, distractors=[(i + 2) / 3, i + 5, 3]
    ))


def build_unit6():
    title = "Physical Science Unit 6: Waves, Sound, and Light"
    description = (
        "Wave parts, v=fλ, sound, color, reflection and refraction, and the EM spectrum — "
        "Grade 9, with a labeled sine wave, not a cell diagram."
    )
    concepts = [
        "Wave parts",
        "Speed, frequency, wavelength",
        "Sound",
        "Light and color",
        "Reflection and refraction",
        "Electromagnetic spectrum",
    ]
    ican1 = [
        "I can label crest, trough, wavelength, and amplitude.",
        "I can say a wave transfers energy, not leftover bulk matter.",
        "I can tell frequency (Hz) from wavelength (m).",
    ]
    c1 = _with_ican(concept_block(
        "1. Wave parts",
        [
            "A wave is a repeating disturbance that carries energy from one place to another. The rope in a rope wave stays a rope. The energy travels. Everyday analogy: a stadium “wave.” People stand and sit. The pattern moves. People do not run around the stadium.",
            "A crest is the highest point. A trough is the lowest point. The rest position is the middle line, like the calm rope.",
            "Amplitude is the distance from the middle line up to a crest (or down to a trough). Larger amplitude means a more energetic wave of that type: taller water, louder sound, brighter light (roughly).",
            "Wavelength, written λ (lambda), is the length of one repeat: crest to next crest, or trough to next trough. It is a distance, measured in meters.",
            "Frequency f is how many repeats pass a point each second. The unit is the hertz (Hz). One hertz means one wave per second. Period is the time for one wave, $T=1/f$, but we will lean on frequency in this course.",
            "Transverse waves shake perpendicular to the travel direction (rope, light). Longitudinal waves shake along the travel direction (sound in air: compressions and rarefactions). You only need the names and one example each.",
        ],
        "The formula $v=fλ$ is just “how many waves times how long each one is.” If crest and λ are fuzzy, the formula is alphabet soup.",
        "On every picture, mark middle line, crest, trough, one λ, and amplitude. Say out loud: λ is a length, f is a count per second.",
        lesson_figure(
            _wave_svg(),
            "A labeled sine wave",
            "Crests at the top, troughs at the bottom, λ from crest to crest, amplitude from midline up.",
        )
        + solved(1, "What is the name of the highest point on a transverse wave?",
                 ["The top of the bump is the crest.",
                  "The bottom is the trough.",
                  "Do not call the crest the wavelength."],
                 "crest", "", "Easy")
        + solved(2, "Neighboring crests are 2 m apart. What quantity is 2 m?",
                 ["Crest-to-crest distance is the definition of wavelength.",
                  "Amplitude would be a vertical height, not 2 m along the wave unless the picture said so.",
                  "So λ=2 m."],
                 "wavelength", "", "Medium")
        + solved(3, "3 crests pass a dock each second. What is the frequency, and what is not?",
                 ["Three waves per second means f=3 Hz.",
                  "That is not a length, so it is not λ.",
                  "Speed would still need a wavelength: v=fλ."],
                 "3 Hz (not a wavelength)", "", "Hard"),
        ("Calling amplitude the wavelength",
         "Amplitude is up-down size. Wavelength is along-the-wave size. Mixing them makes $v=fλ$ spit out nonsense units."),
        ("Trace one full bump with a finger",
         "Start at a crest, slide to the next crest: that path length is λ. The vertical hop to the middle is amplitude."),
        ican1, 1,
    ), ican1)

    ican2 = [
        "I can use $v=fλ$ to find v, f, or λ.",
        "I can explain that in one medium, higher f means smaller λ.",
        "I can keep units as Hz × m = m/s.",
    ]
    c2 = _with_ican(concept_block(
        "2. Speed, frequency, wavelength",
        [
            "Wave speed is how fast the disturbance travels. In a formula, $v=fλ$. Frequency times wavelength. A 5 Hz wave with 4 m wavelength has speed $5\\times4=20$ m/s.",
            "You can rearrange: $λ=v/f$ and $f=v/λ$. Same triangle as $D=m/V$: cover the letter you want.",
            "In one medium, speed is mostly a property of that medium (water versus air versus a tight string). If you raise frequency on a string with fixed v, wavelength must drop. You do not get to triple f and triple λ at once.",
            "Everyday analogy: people marching through a hallway at fixed walking speed. If they take more steps per second, each step is shorter. Steps per second is f. Step length is λ. Walking speed is v.",
            "Sound in room-temperature air is about 340 m/s. Light in vacuum is about $3.0\\times10^{8}$ m/s. Do not mix those speeds.",
            "Amplitude does not sit in $v=fλ$. Shouting louder does not make sound faster in the same air. It makes the wave “taller” (more energy).",
        ],
        "Color, pitch, and the EM spectrum are all $v=fλ$ stories. If the triangle is weak, Unit 6’s stretch set will feel like random numbers.",
        "Write v, f, λ with units. Circle the one you need. Multiply or divide. Then ask whether the size is sane: sound ~ hundreds of m/s, light ~ 10⁸ m/s.",
        lesson_figure(
            _packed_waves_svg(),
            "Shorter λ means more waves packed in the same length",
            "Top trace: two full wavelengths (two crests) in the window. Bottom: four full wavelengths (four crests). If v is fixed, packing more waves (higher f) shortens λ.",
        )
        + solved(4, "f=5 Hz, λ=4 m. Find v.",
                 ["$v=fλ$.",
                  "$5\\times4=20$.",
                  "Speed is 20 m/s."],
                 "20 m/s", "", "Easy")
        + solved(5, "Sound v=340 m/s, f=170 Hz. Find λ.",
                 ["$λ=v/f$.",
                  "$340/170=2$.",
                  "Wavelength is 2 m."],
                 "2 m", "", "Medium")
        + solved(6, "In the same medium, frequency doubles. What happens to λ if v stays the same?",
                 ["$λ=v/f$.",
                  "v fixed, f×2, so λ becomes half.",
                  "The wave is more “cramped.”"],
                 "wavelength halves", "", "Hard"),
        ("Adding f and λ instead of multiplying",
         "$v=f+λ$ is a different (wrong) recipe. Check units: Hz is 1/s, times meters, gives m/s. Adding 5 Hz to 4 m does not make a speed."),
        ("Sane-size check",
         "If you get light traveling at 20 m/s, you used a sound number. If you get sound at 3×10⁸ m/s, you used c by mistake."),
        ican2, 6,
    ), ican2)

    ican3 = [
        "I can say sound needs a medium and is a vibration wave.",
        "I can connect pitch to frequency and loudness to amplitude.",
        "I can explain an echo as reflection and thunder’s delay as slow sound.",
    ]
    c3 = _with_ican(concept_block(
        "3. Sound",
        [
            "Sound is a mechanical wave: vibrating matter. In air it is longitudinal — compressions (crowded air) and rarefactions (spread-out air) travel to your ear. No air, no shout. Space is quiet.",
            "Pitch is how high or low the note sounds. It tracks frequency. A mosquito buzz is high f. A bass drum is low f. Loudness tracks amplitude. A whisper and a shout can be the same pitch.",
            "Sound is fastest, as a Grade 9 pattern, in solids, then liquids, then gases, because particles are closer in solids and pass the vibration sooner. Steel can carry a tap farther than air.",
            "An echo is reflected sound. Clap in a gym: the wave bounces off a wall. Thunder lags lightning because light is enormously faster than 340 m/s sound. Count seconds, multiply by 340, get a rough distance.",
            "Sound bends around doorways (diffraction) better than light, because sound’s wavelength is closer to the size of the door. That is why you hear a conversation in the hall before you see the people.",
            "We will not do calculus of oscillations. If a question gives v, f, λ, it is still $v=fλ$, just with sound’s numbers.",
        ],
        "The Doppler stretch item and every “why is space silent” question sit here. Mixing sound with EM waves will make you “hear” radio in a vacuum.",
        "Ask: is there matter to vibrate? Then: pitch or loudness? Then: bounce (echo), delay (thunder), or spreading (diffraction)?",
        lesson_figure(
            _two_pitch_svg(),
            "Two pitches in the same 4 seconds",
            "More wiggles in the same time means higher frequency (higher pitch). The bottom trace has three times as many cycles.",
        )
        + solved(7, "Can you hear a shout on the Moon (no air)?",
                 ["Sound needs a medium.",
                  "The Moon’s surface has no air to carry the wave to a helmet-less ear.",
                  "Radio (EM) could still work; sound would not."],
                 "no (no medium)", "", "Easy")
        + solved(8, "A siren sounds higher pitched. What increased?",
                 ["Pitch tracks frequency.",
                  "Amplitude would be loudness.",
                  "So f increased."],
                 "frequency", "", "Medium")
        + solved(9, "Lightning, then thunder 3 s later. About how far is the storm? (340 m/s)",
                 ["Light arrives in a tiny fraction of a second, so 3 s is sound’s time.",
                  "d=vt=340×3=1020 m.",
                  "About one kilometer."],
                 "about 1020 m", "", "Hard"),
        ("Thinking louder means faster",
         "Amplitude is not in $v=fλ$. A yell and a whisper in the same air have the same speed, different amplitude."),
        ("Split pitch versus loudness on the page",
         "Write “f → pitch” and “amplitude → loudness” before you read the choices. Those two lines kill half the traps."),
        ican3, 11,
    ), ican3)

    ican4 = [
        "I can say color tracks frequency (and λ in a given medium).",
        "I can explain why an object looks red (reflects red).",
        "I can say a prism sorts mixed colors by refraction.",
    ]
    c4 = _with_ican(concept_block(
        "4. Light and color",
        [
            "Visible light is the tiny slice of the electromagnetic spectrum we can see. Different frequencies look like different colors. Red has a longer wavelength than violet in air. Amplitude relates to brightness, not to “which crayon.”",
            "White daylight is a mix of colors. A prism or a raindrop can sort the mix because each color bends a little differently (dispersion). The rainbow was in the white light; the drop did not paint it with pigments.",
            "An opaque object’s color is the color it reflects (or scatters) to your eyes. A red shirt reflects red and absorbs much of the rest. Under green light it may look dark, because there is little red to reflect.",
            "Black absorbs most visible light and warms more in the Sun. White reflects more and stays cooler. Filters let some colors through and block others — they subtract, they do not add a dye to every photon in a magical way.",
            "Everyday analogy: a stained-glass window is a bouncer at a club. Only certain colors get in. The glass does not “turn” blocked colors into the allowed one.",
            "Light can travel through vacuum. Sound cannot. That one sentence separates this lesson from the last.",
        ],
        "Reflection and the EM spectrum both need “color = frequency.” If color is “paint on the wave,” filters and black cloth will be mysteries.",
        "Ask what is absorbed versus reflected versus transmitted. You see what arrives at your eye, not what was eaten by the material.",
        lesson_figure(
            _visible_slice_svg(),
            "Visible light from red to violet",
            "Inside visible light, red is longer λ; violet is shorter λ.",
        )
        + solved(10, "Why does a red apple look red in white light?",
                 ["White light contains many colors.",
                  "The apple reflects red and absorbs much of the rest.",
                  "Your eye receives the reflected red."],
                 "reflects red", "", "Easy")
        + solved(11, "Why does black asphalt get hotter in the Sun than a white roof?",
                 ["Black absorbs more of the light’s energy.",
                  "Absorbed energy becomes thermal energy.",
                  "White reflects more, so it absorbs less."],
                 "black absorbs more", "", "Medium")
        + solved(12, "A green filter is placed on a white flashlight aimed at a red shirt. The shirt looks dark. Why?",
                 ["The filter mostly passes green and blocks red.",
                  "The shirt wants to reflect red and absorb green.",
                  "Little light that matches the shirt’s “reflect red” habit reaches it, so little returns to your eye."],
                 "no red to reflect", "", "Hard"),
        ("Thinking a filter adds its color like paint poured into the beam",
         "Filters subtract. A green filter removes other colors. It does not inject green pigment into red light that was blocked."),
        ("Trace the path: source → object → eye",
         "At each step, ask: transmitted, reflected, or absorbed? The last surviving light is the color you see."),
        ican4, 16,
    ), ican4)

    ican5 = [
        "I can state the law of reflection (from the normal).",
        "I can define refraction as bending when speed changes.",
        "I can say light in water slows and bends toward the normal.",
    ]
    c5 = _with_ican(concept_block(
        "5. Reflection and refraction",
        [
            "Reflection is a bounce. The law of reflection: the angle of incidence equals the angle of reflection. Both angles are measured from the normal — a dashed line sticking straight out of the surface, not from the surface itself.",
            "Mirrors are smooth reflectors. The Moon is a rough reflector of sunlight; you still see it by reflection. An echo is sound’s version of a bounce.",
            "Refraction is a bend when a wave changes speed as it enters a new medium. Light slows in water or glass. A straw looks kinked. A pool looks shallower because your brain assumes light traveled straight.",
            "When light goes from air into water, it slows and bends toward the normal. When it leaves water into air, it speeds up and bends away from the normal. We will not use Snell’s law numbers in this course; we will use the toward/away rule.",
            "Everyday analogy: a marching line of people hitting mud. The first marchers slow, so the line swings. That swing is the bend.",
            "Lenses use refraction to focus. You only need the idea that bending can gather or spread rays. A later optics course covers the lens formulas.",
        ],
        "Rainbows, fiber ideas, and “broken straw” demos are refraction. Mirror problems are reflection. Mixing the two words loses both labs.",
        "Bounce or speed-change? If bounce, equal angles from the normal. If speed-change, toward the normal when slowing, away when speeding up.",
        lesson_figure(
            _refract_svg(),
            "Light entering water bends toward the normal",
            "The dashed line is the normal. The ray kinks at the surface.",
        )
        + solved(13, "Incoming angle from the normal is 30°. Reflected angle?",
                 ["Law of reflection: equal angles from the normal.",
                  "Outgoing is also 30°.",
                  "Not 60° unless someone measured from the surface by mistake."],
                 "30°", "", "Easy")
        + solved(14, "Why does a straw in a glass of water look bent?",
                 ["Light from the straw changes speed at the water–air surface.",
                  "The path kinks (refraction).",
                  "Your eye traces the last direction backward as if it were straight."],
                 "refraction at the surface", "", "Medium")
        + solved(15, "Light goes air → water. Does it bend toward or away from the normal, and why?",
                 ["Light slows in water.",
                  "Slowing bends the ray toward the normal.",
                  "The marching-line-in-mud picture matches that kink."],
                 "toward the normal (slows)", "", "Hard"),
        ("Measuring angles from the mirror surface instead of the normal",
         "If the ray is 30° from the surface, it is 60° from the normal. The law uses the normal. Mixing those numbers doubles or halves the angle."),
        ("Draw the normal first",
         "A dashed perpendicular on the surface makes incidence and reflection obvious. Skipping the normal is how 30° becomes 60°."),
        ican5, 21,
    ), ican5)

    ican6 = [
        "I can list the EM spectrum from radio to gamma in order of frequency.",
        "I can say all EM waves travel at c in vacuum.",
        "I can use $c=fλ$ with scientific notation at a Grade 9 level.",
    ]
    c6 = _with_ican(concept_block(
        "6. Electromagnetic spectrum",
        [
            "Light is one slice of a family called electromagnetic (EM) waves. They can travel through vacuum. They do not need air. Radio, microwaves, infrared, visible, ultraviolet, X-rays, and gamma rays are the same kind of wave at different frequencies.",
            "Order by increasing frequency (and decreasing wavelength): radio → micro → IR → visible → UV → X-ray → gamma. A memory hook: “Raging Martians Invaded Venus Using X-ray Guns,” or any sentence you invent that keeps that order.",
            "In vacuum they all travel at c, about $3.0\\times10^{8}$ m/s. Then $c=fλ$. High f means short λ. Gamma is high f, short λ. Radio is low f, long λ.",
            "Infrared often feels like warmth. UV can sunburn. X-rays can image bones because they pass through flesh more than bone. Radio carries Wi-Fi and stations. You do not need quantum theory here — just the order and one use each.",
            "Everyday analogy: a piano keyboard of waves. Same instrument (EM), different notes (frequency). Visible is a tiny group of keys in the middle.",
            "Never confuse this keyboard with sound. Sound is a matter vibration. EM is an electric-and-magnetic disturbance that can exist in empty space. We will not write Maxwell’s equations.",
        ],
        "Sunburn, microwave ovens, and “why is space silent but not dark” all sit on this spectrum. Mixing it with sound makes radio need air.",
        "Write the seven names in order. Mark visible as a thin slice. For a number problem, use $c=fλ$ with c=3.0×10⁸ m/s unless the problem puts the wave in glass.",
        lesson_figure(
            _spectrum_svg(),
            "EM spectrum from long λ to short λ",
            "Left: radio. Right: gamma. Visible is the tiny colored band.",
        )
        + solved(16, "Which has longer wavelength: radio or gamma?",
                 ["Radio is at the long-λ, low-f end.",
                  "Gamma is at the short-λ, high-f end.",
                  "Radio has the longer wavelength."],
                 "radio", "", "Easy")
        + solved(17, "Do radio and gamma travel at different speeds in vacuum?",
                 ["In vacuum, all EM waves travel at c.",
                  "Frequency and wavelength trade to keep $c=fλ$.",
                  "Speeds match; f and λ differ."],
                 "same speed c", "", "Medium")
        + solved(18, "A microwave has f=2.45×10⁹ Hz. Using c=3.0×10⁸ m/s, estimate λ.",
                 ["$λ=c/f$.",
                  "$(3.0\\times10^{8})/(2.45\\times10^{9})\\approx0.12$ m.",
                  "About 12 cm, oven-sized."],
                 "about 0.12 m", "", "Hard"),
        ("Thinking higher frequency means higher speed in vacuum",
         "Speed is c for all of them in empty space. Higher f means shorter λ, not a faster light."),
        ("Write the seven-word order on the quiz margin",
         "Then “which has higher f” is just “which sits farther right.” The order is the whole spectrum lesson."),
        ican6, 26,
    ), ican6)

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7
# ===========================================================================

def _u7_questions():
    rows = [
        ("Electric charge comes in two kinds. Same kinds _____ and opposite kinds _____ .",
         "repel; attract",
         "Two + charges push apart. A + and a − pull together. That is the basic rule of static electricity.",
         ["attract; repel", "vanish; appear", "heat; freeze"]),
        ("Electrons are the particles that usually move in static labs because they are…",
         "outside the nucleus and much easier to transfer than protons",
         "Rubbing a balloon on hair moves electrons. Protons stay in nuclei.",
         ["heavier than nuclei", "positive", "not real"]),
        ("A balloon rubbed on hair often becomes negative because it…",
         "gains electrons",
         "Extra electrons mean extra minus charge. Hair may be left positive.",
         ["gains protons", "loses all electrons", "becomes a magnet north pole only"]),
        ("An object with equal amounts of + and − is called…",
         "neutral (net charge zero)",
         "Neutral does not mean “no charges.” It means they cancel as a total.",
         ["impossible", "only a conductor", "radioactive"]),
        ("Charging by friction, contact, or induction are ways to…",
         "move electrons so the net charge on an object changes or rearranges",
         "You do not create charge from nothing. You separate or transfer it.",
         ["create protons in the nucleus in a Grade 9 lab", "destroy electrons", "turn charge into mass"]),
        ("Electric current is…",
         "a flow of charge (in metal wires, a flow of electrons)",
         "Current is measured in amperes (A). A complete loop is needed for a steady current in this course.",
         ["a flow of neutrons only", "the same as voltage always", "a type of sound"]),
        ("Voltage is best thought of as…",
         "the “push” (electric potential difference) that can drive current",
         "A battery provides a voltage. Everyday analogy: a pump’s pressure, not the water itself.",
         ["the number of light bulbs only", "resistance in ohms only", "mass in kilograms"]),
        ("Resistance is…",
         "how much a device opposes current, in ohms (Ω)",
         "A thin, long, hot wire usually has more resistance than a thick, short, cool one of the same metal.",
         ["the same as current", "measured in amperes", "a type of charge"]),
        ("Ohm’s law in this course is…",
         "V = I R",
         "Voltage equals current times resistance. Cover the letter you need: I=V/R, R=V/I.",
         ["V = I / R", "V = I + R", "V = I − R"]),
        ("A 6 V battery drives current through 2 Ω. Current is…",
         "3 A", "$I=V/R=6/2=3$ A.",
         ["8 A", "12 A", "0.33 A"]),
        ("In a series circuit, current is…",
         "the same through each device (one path)",
         "There is one loop. Charge has nowhere else to go. Voltages across devices add to the battery.",
         ["split among branches", "zero in every bulb if one bulb works", "different in each wire by law"]),
        ("In a parallel circuit, voltage across each branch is…",
         "the same (each branch sees the battery’s voltage)",
         "Currents in branches add. If one bulb burns out, the other branch can still run.",
         ["split so each bulb gets a random leftover", "always zero", "only on the first bulb"]),
        ("Two 3 Ω resistors in series have equivalent resistance…",
         "6 Ω", "Series: add. $3+3=6$ Ω.",
         ["1.5 Ω", "9 Ω", "0 Ω"]),
        ("Two 6 Ω resistors in parallel have equivalent resistance…",
         "3 Ω", "$1/R=1/6+1/6=1/3$, so R=3 Ω. Parallel equivalent is smaller than either piece.",
         ["12 Ω", "6 Ω", "9 Ω"]),
        ("Holiday lights that all go dark when one bulb dies are likely wired in…",
         "series",
         "One break opens the only path. Parallel lights would leave other branches on.",
         ["parallel", "with no circuit at all", "only with magnets"]),
        ("A magnet has two poles, called…",
         "north and south",
         "Opposite poles attract. Like poles repel. You cannot isolate a single pole by snapping a bar magnet — each piece gets both.",
         ["plus and minus charge only", "hot and cold", "east and west charge"]),
        ("Magnetic field lines outside a bar magnet run from…",
         "north toward south",
         "Compasses (tiny magnets) line up with those lines. Inside the magnet the pattern continues in a loop.",
         ["south toward north outside", "randomly only", "from Earth to the Moon only"]),
        ("A compass needle points roughly north because…",
         "Earth itself behaves like a giant magnet",
         "The needle’s north pole is attracted toward Earth’s magnetic south pole, which currently sits near geographic north — a naming quirk you only need as “Earth has a magnetic field.”",
         ["the needle is electrically charged", "wind always blows north", "compasses detect sound"]),
        ("Which materials are strongly attracted to a magnet in a Grade 9 lab?",
         "iron, nickel, cobalt (and many steels)",
         "Copper, aluminum, and wood are not typical fridge-magnet materials.",
         ["all metals equally, including copper", "only water", "only plastic"]),
        ("If you break a bar magnet in half, each piece…",
         "has its own north and south",
         "Poles come in pairs. You do not get a lone north chunk.",
         ["is only north", "loses all magnetism forever always", "becomes an electric charge"]),
        ("An electromagnet is a magnet made by…",
         "electric current in a coil, often with an iron core",
         "More loops, more current, and an iron core make it stronger. Turning the current off turns the magnet off. That is the useful trick.",
         ["only permanently magnetizing rubber", "cooling water to 0 °C", "a battery with no loop"]),
        ("A straight wire with current has a magnetic field that…",
         "loops around the wire",
         "Compasses around a vertical wire circle. Reverse the current, reverse the field.",
         ["does not exist", "is only inside the battery", "points only to geographic east always"]),
        ("A coil (solenoid) with current acts like…",
         "a bar magnet with a north and south end",
         "That is why a junkyard electromagnet can lift cars and then drop them.",
         ["a sound wave only", "an uncharged balloon only", "a gravitational PE store only"]),
        ("To make an electromagnet stronger you can…",
         "increase current, add loops, or add an iron core",
         "Those three levers are the Grade 9 toolkit. You do not need calculus of B-fields.",
         ["remove all current", "use a wooden core to boost it always", "cut the wire"]),
        ("Motors use the fact that a magnetic field can…",
         "push on a current-carrying wire, producing a turn",
         "Speakers and meters use related ideas. You only need “current + magnet → force.”",
         ["delete charge", "stop all current by law", "create mass"]),
        ("A household safety device that opens a circuit when current is too large is a…",
         "fuse or circuit breaker",
         "Too much current can heat wires and start a fire. The breaker is a switch that trips. A fuse melts a metal strip.",
         ["magnet pole", "compass", "insulating paint on a window only"]),
        ("Water and a hair dryer are a bad mix because water…",
         "can conduct enough to give a shock path through you",
         "Pure water is a poor conductor; tap water with ions conducts. Wet skin is especially risky.",
         ["destroys gravity", "makes voltage zero always", "turns the dryer into a magnet only"]),
        ("The third prong on a plug is often a…",
         "ground (safety path for stray charge)",
         "If a live wire touches the metal case, the ground path can trip a breaker instead of sending current through you.",
         ["decoration", "the only current-carrying hot wire", "a magnet"]),
        ("Never overload a power strip because…",
         "too many devices can draw more current than the wires are rated for, causing heat",
         "P=VI in a later course; here: more devices, more current, more heat, fire risk.",
         ["voltage becomes infinite", "magnets appear in the wall", "Earth’s field reverses"]),
        ("Unplug a device by the plug, not by yanking the cord, because yanking can…",
         "damage insulation and expose live metal",
         "Exposed metal is a shock and fire hazard.",
         ["increase resistance in a helpful way always", "charge the cord with extra protons", "cool the wires"]),
        ("A rubbed balloon sticks to a wall because the balloon’s charge…",
         "rearranges charges in the wall (induction) so the near side is opposite and attracts",
         "The wall can stay overall neutral. Opposite near-charges still attract.",
         ["turns the wall into a north magnetic pole only", "requires the wall to be a magnet", "means the balloon lost all charge"]),
        ("A 12 V battery and a 4 Ω bulb (simple loop). Current?",
         "3 A", "$I=12/4=3$ A.",
         ["16 A", "8 A", "0.33 A"]),
        ("Three 2 Ω resistors in series. Equivalent R?",
         "6 Ω", "$2+2+2=6$.",
         ["2 Ω", "8 Ω", "0.67 Ω"]),
        ("Two 4 Ω resistors in parallel. Equivalent R?",
         "2 Ω", "$1/R=1/4+1/4=1/2$, so R=2 Ω.",
         ["8 Ω", "4 Ω", "0 Ω"]),
        ("If one bulb in a two-bulb parallel set burns out (open), the other…",
         "stays on (its branch is still a complete loop)",
         "That is the household-lighting idea. Series would go all dark.",
         ["must go out", "gets infinite current", "becomes a magnet"]),
        ("Like magnetic poles…",
         "repel", "N-N or S-S push apart. N-S pull together.",
         ["attract", "cancel Earth’s gravity", "create charge"]),
        ("A coil around an iron nail connected to a battery can pick up paper clips. Disconnect the battery and the clips often drop because…",
         "the magnetic field of the electromagnet collapses when current stops",
         "That on/off control is why electromagnets are useful.",
         ["the nail’s mass became zero", "gravity reversed", "paper clips became charged only"]),
        ("A breaker trips. What should you do before resetting it?",
         "unplug or turn off extra loads and find why current was too high",
         "Resetting into the same short or overload can trip again or cause heat.",
         ["hold it on with tape", "add more high-power devices first", "pour water on it"]),
        ("Current through a 3 Ω resistor is 2 A. Voltage across it is…",
         "6 V", "$V=IR=2\\times3=6$ V.",
         ["1.5 V", "5 V", "0.67 V"]),
        ("Why does a bird on one high-voltage wire (not touching anything else) often not get shocked?",
         "there is no complete path through the bird to a different potential",
         "Shock needs a path. Two feet on one wire at the same voltage is not a loop through the body. Do not try this; the lesson is about complete paths.",
         ["birds have no electrons", "voltage is zero on all wires", "air cannot exist near wires"]),
        ("Static cling in a dryer is…",
         "charge transfer by rubbing fabrics",
         "Opposite charges attract clothes together. A dryer sheet reduces the charge buildup.",
         ["a magnetic north pole on cotton only", "current in a series circuit of shirts", "nuclear change"]),
        ("A thicker copper wire of the same length usually has _____ resistance than a thinner one.",
         "smaller", "More room for charge to flow. Shorter also means smaller R. Hotter usually means larger R for metals.",
         ["larger always", "infinite", "zero always"]),
        ("Earth’s magnetic field is useful because it…",
         "lets compasses work and helps shield us from some solar particles (Grade 9 idea)",
         "You do not need plasma physics. Compass + “space weather shield” is enough.",
         ["causes all static cling", "is the same as gravity", "charges every proton"]),
        ("Two 3 Ω in series with a 12 V battery. Current in the loop?",
         "2 A", "Req=6 Ω. I=12/6=2 A. Same 2 A through each.",
         ["4 A", "12 A", "6 A"]),
        ("Two 3 Ω in parallel with a 12 V battery. Current through one of the 3 Ω branches?",
         "4 A", "Each branch sees 12 V. I=12/3=4 A in each. Battery supplies 8 A total.",
         ["2 A", "12 A", "3 A"]),
        ("A fuse with a 5 A rating should blow if current is…",
         "steadily above 5 A",
         "That is its job: open before wires overheat. A 5 A fuse is the wrong choice for a 15 A appliance.",
         ["exactly 0 A only", "never, fuses never open", "only when voltage is 0"]),
        ("Challenge Stretch: Two 6 Ω in parallel, then that pair in series with a 3 Ω, on 12 V. Current from the battery?",
         "2 A",
         "Parallel pair: 3 Ω. Plus series 3 Ω → Req=6 Ω. I=12/6=2 A. Multi-step series–parallel.",
         ["4 A", "1 A", "12 A"]),
        ("Challenge Stretch: Three 6 Ω in parallel. Equivalent R, then current from a 6 V battery?",
         "2 Ω and 3 A",
         "$1/R=1/6+1/6+1/6=1/2$, R=2 Ω. I=6/2=3 A from the battery (1 A per branch).",
         ["18 Ω and 1/3 A", "6 Ω and 1 A", "2 Ω and 12 A"]),
        ("Challenge Stretch: A 9 V battery, 3 Ω and 6 Ω in series. Voltage across the 6 Ω?",
         "6 V",
         "Req=9 Ω, I=1 A. V=IR=1×6=6 V on the 6 Ω (and 3 V on the 3 Ω). Series voltages add to 9 V.",
         ["9 V", "3 V", "1 V"]),
        ("Challenge Stretch: A 12 A microwave, an 8 A toaster, and a 4 A blender share a 20 A parallel kitchen circuit. Total current if all three run, and does a 20 A breaker trip?",
         "24 A; yes, it trips",
         "Parallel currents add: 12+8+4=24 A, which is above 20 A, so the breaker should open. Two devices at 20 A would sit at the limit; the third pushes it over.",
         ["12 A; no trip", "24 A; no trip because they share", "4 A; yes trip"]),
        ("Challenge Stretch: Two 6 Ω bulbs in series on 12 V versus one 6 Ω bulb alone on 12 V. Find the current in each setup, then which is brighter and why.",
         "1 A in the series pair, 2 A for the single bulb; the single bulb is brighter",
         "Series Req=12 Ω so I=12/12=1 A. Alone, I=12/6=2 A. Double the current (and the full 12 V on one bulb) means more power, so brighter.",
         ["2 A in both; equally bright", "1 A in both; series brighter", "0 A series; 2 A alone"]),
        ("Challenge Stretch: A negatively charged rod is brought near a metal can on an insulating stand, then the can is touched (grounded) and the rod is removed. The can is left…",
         "positive (electrons left through the ground while the rod was near)",
         "Induction plus grounding: the rod chased electrons away. After the path is gone, the can is short of electrons.",
         ["negative with extra electrons that arrived from the rod by contact", "neutral for sure", "a north magnetic pole"]),
        ("Challenge Stretch: Two coils: coil A has current, coil B is nearby with no battery. If you suddenly stop A’s current, B can show a brief current because…",
         "a changing magnetic field can induce current in a nearby loop (Grade 9 Faraday idea)",
         "Steady current in A makes a steady field; a sudden change makes a pulse in B. You do not need the full formula.",
         ["B gained protons", "current cannot exist without a battery ever", "gravity induced the current"]),
        ("Challenge Stretch: A 2 Ω and a 4 Ω in parallel on 12 V. Current in the 2 Ω compared with the 4 Ω is…",
         "twice as large (6 A vs 3 A)",
         "Same V. I=V/R so half the R, double the I. 12/2=6 A and 12/4=3 A. Battery supplies 9 A.",
         ["the same", "half as large", "zero in the 2 Ω"]),
        ("Challenge Stretch: A hair dryer on a GFCI near a sink has a frayed cord that dips into a puddle. Current on the hot wire is 8.0 A but only 7.2 A returns on neutral. Why does the GFCI trip, and why is the puddle a second problem?",
         "0.8 A is leaking (hot ≠ neutral), and water offers a parallel path through a person or the puddle",
         "GFCI watches for a mismatch. 8.0−7.2=0.8 A left the intended wires. Wet skin and a puddle are extra conductors, so that leak can be a shock path, not just wasted current in the dryer.",
         ["the GFCI raises voltage near water", "8.0 A is below any limit so it should not trip", "the puddle magnetizes the cord"]),
    ]
    return fill_qs(_pack(rows), 55, lambda i: mq(
        f"A {i+2} V battery drives a {i+2} Ω resistor. Current in A?",
        1, f"I=V/R={i+2}/{i+2}=1 A.", i, distractors=[2, i + 2, 0]
    ))


def build_unit7():
    title = "Physical Science Unit 7: Electricity and Magnetism Intro"
    description = (
        "Charge and static, current and Ohm’s law, series versus parallel, magnets, electromagnets, "
        "and household safety — Grade 9 numbers you can check, with circuit pictures."
    )
    concepts = [
        "Charge and static electricity",
        "Current and circuits",
        "Series vs parallel",
        "Magnets and poles",
        "Electromagnets",
        "Household safety",
    ]
    ican1 = [
        "I can state that like charges repel and unlike attract.",
        "I can say electrons move in static labs, not protons.",
        "I can define neutral as net charge zero.",
    ]
    c1 = _with_ican(concept_block(
        "1. Charge and static electricity",
        [
            "Electric charge is a property of matter that makes it push or pull electrically. There are two kinds, plus and minus. Same kinds repel. Opposite kinds attract. Everyday analogy: two north ends of fridge magnets also repel, but that is magnetism — similar slogan, different force. Keep the names straight.",
            "Electrons are negative and live outside the nucleus. They are the particles you usually move when you rub a balloon on hair. Protons are positive and stay in the nucleus in these labs. Gaining electrons makes an object negative. Losing electrons makes it positive.",
            "Neutral means net charge zero: equal plus and minus, not “no charges exist.” A huge object can be neutral and still have trillions of both kinds.",
            "Charge is conserved. Rubbing separates charge; it does not invent it. The balloon’s extra electrons came from the hair (or the other way around, depending on the materials).",
            "Charging by contact shares charge by touching. Charging by induction rearranges charges without a spark of contact: a charged balloon near a wall pushes like charges away, so the near side of the wall is opposite and the balloon sticks.",
            "Sparks happen when charge jumps through air. Lightning is a giant spark. You do not need Maxwell’s field math. You need the two-kind rule and “electrons move.”",
        ],
        "Current is moving charge. If static charge is fuzzy, circuits will feel like a new language instead of the same electrons in a loop.",
        "For any static demo, ask: which object gained electrons? Which lost them? Then apply repel/attract. Do not move protons in your story.",
        lesson_figure(
            field_lines_svg(kind="negative"),
            "A negative charge and the idea of a surrounding field",
            "Other charges feel a push or pull in the space around it. Lines are a drawing tool, not strings.",
        )
        + solved(1, "Two balloons rubbed the same way push apart. Why?",
                 ["They gained the same kind of leftover charge.",
                  "Like charges repel.",
                  "If they had opposite leftover charge, they would attract."],
                 "like charges repel", "", "Easy")
        + solved(2, "A balloon becomes negative after rubbing hair. What happened to electrons?",
                 ["Negative means extra electrons.",
                  "The balloon gained electrons from the hair.",
                  "Protons did not hop from hair to balloon."],
                 "balloon gained electrons", "", "Medium")
        + solved(3, "Why can a charged balloon stick to a neutral wall?",
                 ["The balloon’s charge rearranges charges in the wall (induction).",
                  "The near side of the wall becomes opposite in charge.",
                  "Opposite near-charges attract, even if the wall’s total is still zero."],
                 "induction: opposite near side", "", "Hard"),
        ("Moving protons in the rubbing story",
         "Nuclei are heavy and locked in solids. The mobile characters in Grade 9 static are electrons. If you “transfer protons,” every sign will be backwards."),
        ("Label + or − on each object before the force",
         "Once the signs are on the page, repel versus attract is automatic. Guessing the force without signs is a coin flip."),
        ican1, 1,
    ), ican1)

    ican2 = [
        "I can define current, voltage, and resistance in one sentence each.",
        "I can use $V=IR$.",
        "I can say a complete loop is needed for a steady bulb.",
    ]
    c2 = _with_ican(concept_block(
        "2. Current and circuits",
        [
            "A circuit is a closed path that charge can travel. A battery, wires, and a bulb in a loop can light. A gap (open switch) stops the steady current. Everyday analogy: a bike loop. If the path is broken, you cannot keep riding the loop.",
            "Current I is the flow of charge, measured in amperes (A). In metal wires, electrons are the movers. We still draw a simple arrow for current in the direction from the battery’s + toward − in the old “positive flow” picture. Either story is fine if you are consistent; this course will treat I as “how much charge flow.”",
            "Voltage V is the electric push, measured in volts (V). A 6 V battery pushes harder than a 1.5 V cell. Analogy: water pressure in a pump, not the amount of water.",
            "Resistance R is the opposition to current, in ohms (Ω). Thin, long, hot wires resist more (for typical metals). A bulb’s filament is a designed resistor that glows.",
            "Ohm’s law: $V=IR$. Then $I=V/R$ and $R=V/I$. A 6 V battery on 2 Ω gives $I=3$ A. If R rises, I falls for the same V.",
            "Energy from the battery becomes light and thermal energy in the bulb. That is Unit 5 conservation in electric clothes.",
        ],
        "Series and parallel are just how we share V and I. Without V=IR, those lessons are slogans.",
        "Write the triangle V, I, R. Circle the unknown. Then ask whether the loop is closed. An open switch makes I=0 no matter what V is.",
        lesson_figure(
            series_circuit_svg(),
            "A battery and two resistors in one loop",
            "Current has one path. The battery’s voltage is shared across the resistors.",
        )
        + solved(4, "A 6 V battery, 2 Ω resistor, complete loop. Find I.",
                 ["$I=V/R$.",
                  "$6/2=3$.",
                  "Current is 3 A."],
                 "3 A", "", "Easy")
        + solved(5, "Current is 2 A through 3 Ω. Find V across the resistor.",
                 ["$V=IR$.",
                  "$2\\times3=6$.",
                  "Voltage is 6 V."],
                 "6 V", "", "Medium")
        + solved(6, "Why does an open switch leave a bulb dark even with a fresh battery?",
                 ["Current needs a complete path.",
                  "The gap is infinite resistance in this course’s picture: I=0.",
                  "Voltage still exists at the battery, but no flow means no glowing filament."],
                 "no complete path, I=0", "", "Hard"),
        ("Mixing up V and I",
         "A battery’s 6 V is not “6 amps.” Amps measure flow. Volts measure push. A tiny current can still have a large voltage (static spark)."),
        ("Cover the needed letter in V = I R",
         "If you want I, cover I, see V/R. That triangle is faster than guessing whether to multiply or divide."),
        ican2, 6,
    ), ican2)

    ican3 = [
        "I can say series is one path (same I) and parallel is branches (same V).",
        "I can add series resistances and use the parallel “smaller than either” idea.",
        "I can predict which string goes all-dark when one bulb dies.",
    ]
    c3 = _with_ican(concept_block(
        "3. Series vs parallel",
        [
            "Series means one path. Current is the same through each device. Resistances add: $R=R_1+R_2$. Voltages across devices add up to the battery. If one bulb burns out (opens), the whole string goes dark.",
            "Parallel means branches. Each branch sees the same voltage (the battery’s voltage in a simple two-branch lab). Currents in the branches add. Two 6 Ω in parallel act like 3 Ω — the equivalent is smaller than either resistor, because you opened a second highway for charge.",
            "Everyday analogy: series is a single-lane tunnel. Everyone crawls at the same rate. Parallel is two toll booths. The voltage “price” is the same at each booth; the cars split.",
            "Household lights are parallel so one lamp can be off while another is on. Cheap old holiday strings were series, which is why one dead bulb could darken the whole string.",
            "Numbers: two 3 Ω in series → 6 Ω. Two 6 Ω in parallel → 3 Ω. A 12 V battery on that parallel pair: each 6 Ω has I=12/6=2 A, battery supplies 4 A.",
            "Combination circuits (parallel pair, then series) show up in stretch problems. Reduce the parallel first, then add the series piece.",
        ],
        "Safety math in the next lesson is parallel currents adding at a breaker. If series and parallel are swapped, you will “trip” the wrong number.",
        "Sketch the path. One loop without a split? Series — same I, add R. Split and rejoin? Parallel — same V, currents add. Then do the arithmetic.",
        lesson_figure(
            _parallel_svg(),
            "Two resistors in parallel on one battery",
            "Each branch can run even if the other is removed. Voltages match.",
        )
        + solved(7, "Two 3 Ω in series. Equivalent R?",
                 ["Series resistances add.",
                  "$3+3=6$.",
                  "Equivalent is 6 Ω."],
                 "6 Ω", "", "Easy")
        + solved(8, "Two 6 Ω in parallel. Equivalent R?",
                 ["$1/R=1/6+1/6=2/6=1/3$.",
                  "So R=3 Ω.",
                  "Check: parallel equivalent must be less than 6 Ω."],
                 "3 Ω", "", "Medium")
        + solved(9, "Two identical bulbs in series look dimmer than one bulb on the same battery. Why?",
                 ["Resistances add, so total R is larger and I is smaller.",
                  "Each bulb also gets only part of the battery voltage.",
                  "Less current and less voltage per bulb means dimmer."],
                 "larger Req, smaller I, shared V", "", "Hard"),
        ("Adding parallel resistors as if they were series",
         "Two 6 Ω in parallel are not 12 Ω. Extra paths make it easier to flow, so equivalent R drops. If your parallel R is larger than either piece, you added instead of combining."),
        ("Color the paths with two pencils",
         "One color for series (single road). Two colors for branches. Then you will not apply the wrong rule."),
        ican3, 11,
    ), ican3)

    ican4 = [
        "I can name north and south poles and the attract/repel rule.",
        "I can say field lines outside run N toward S.",
        "I can explain why snapping a magnet does not make a lone pole.",
    ]
    c4 = _with_ican(concept_block(
        "4. Magnets and poles",
        [
            "A magnet has two poles, north and south. Opposite poles attract. Like poles repel. That slogan matches charge, but magnetism is not the same as static cling. A charged balloon is not a bar magnet.",
            "You cannot isolate a single pole by cutting a bar magnet. Each piece becomes a smaller magnet with both poles. Everyday analogy: a two-headed arrow. Cut it and each piece still has two ends.",
            "A magnetic field is the “influence region” around a magnet. We draw field lines coming out of north and looping to south outside the magnet. A compass needle lines up with those lines. Earth itself is a magnet, which is why compasses work.",
            "Iron, nickel, cobalt, and many steels are strongly attracted. Copper coins and aluminum cans are not typical fridge-magnet metals. Not every metal is magnetic in the everyday sense.",
            "A magnetic field can exist without a current (a permanent magnet) or with a current (next lesson). Keep “charge” and “pole” as different words.",
            "We will not do Earth-core dynamo calculus. “Earth has a magnetic field, compasses work, some solar particles are deflected” is the Grade 9 space link.",
        ],
        "Electromagnets are coils that act like these bar magnets. If poles and field lines are mush, the coil lesson has nothing to look like.",
        "For two magnets, label N and S on both, then apply unlike-attract / like-repel. For a compass, remember it is a tiny magnet in Earth’s field.",
        lesson_figure(
            _magnet_svg(),
            "A bar magnet and looping field lines",
            "Outside, lines run from N toward S. Opposite poles would attract.",
        )
        + solved(10, "What happens if two north poles face each other?",
                 ["Like poles repel.",
                  "The magnets push apart.",
                  "They would attract only if one were flipped to south."],
                 "they repel", "", "Easy")
        + solved(11, "You snap a bar magnet in half. Can you hold a piece that is only north?",
                 ["Each piece still has two poles.",
                  "Poles come in pairs in this course.",
                  "You now have two smaller complete magnets."],
                 "no; each piece has N and S", "", "Medium")
        + solved(12, "Why does a compass needle point roughly north?",
                 ["The needle is a magnet.",
                  "Earth has a magnetic field.",
                  "The needle lines up with that field (with a naming quirk about geographic versus magnetic poles you can treat as “points toward the Arctic region”)."],
                 "Earth is a magnet; needle aligns", "", "Hard"),
        ("Calling a charged balloon a magnet",
         "Static is charge. Magnetism is poles and fields from magnets or currents. A balloon sticking to hair is not a north-south story."),
        ("Label N and S before the force",
         "Same habit as + and −. Unlabeled ends make attract/repel a guess."),
        ican4, 16,
    ), ican4)

    ican5 = [
        "I can define an electromagnet as current in a coil (often with iron).",
        "I can name three ways to make it stronger.",
        "I can say the magnet turns off when current stops.",
    ]
    c5 = _with_ican(concept_block(
        "5. Electromagnets",
        [
            "A current-carrying wire has a magnetic field looping around it. A coil of many loops (a solenoid) stacks those fields and acts like a bar magnet with a north end and a south end. Reverse the current, flip the poles.",
            "An iron core in the coil makes the electromagnet much stronger. More loops and more current also strengthen it. Those are the three Grade 9 levers. Turning the current off collapses the field — the junkyard magnet drops the car.",
            "Everyday analogy: a temporary super-fridge-magnet with a switch. Permanent magnets cannot be switched off. Electromagnets can. That is why scrapyards, doorbells, and many relays use them.",
            "A motor uses the push of a magnet on a current-carrying wire to make a turn. A speaker uses a coil and a magnet to shake a cone and make sound. You do not need the right-hand rule on a test that only asks “current plus magnet can make a force.”",
            "A changing magnetic field can even start a current in a nearby loop (a Grade 9 Faraday peek). A sudden stop of current in coil A can pulse coil B. Steady fields do not keep inducing. Change does.",
            "We will not compute B with formulas from a college course. Strength qualitative + V=IR in the coil is enough.",
        ],
        "Household breakers and motors sit on “current makes magnetism” and “magnetism can push current.” If the coil is just a decoration, those devices are magic.",
        "Ask: is there current? Then a field. Is there iron, more loops, more I? Then stronger. Is the switch off? Then field (ideally) gone.",
        lesson_figure(
            _electromagnet_svg(),
            "A nail-core electromagnet",
            "A battery drives current through a coil wrapped on an iron nail. The core and loops make a magnet you can switch off.",
        )
        + solved(13, "Name one way to strengthen an electromagnet.",
                 ["Increase the current, or add loops, or add an iron core.",
                  "Any one of those three is a correct lever.",
                  "Removing current would weaken it to off."],
                 "more I, more loops, or iron core", "", "Easy")
        + solved(14, "Why do the paper clips often fall when you disconnect the battery from a nail-coil?",
                 ["The electromagnet’s field is made by current.",
                  "No current, field collapses (ignoring a bit of leftover magnetism in cheap nails).",
                  "Gravity then wins."],
                 "current off → field gone", "", "Medium")
        + solved(15, "A nearby coil with no battery shows a brief current when you open the first coil’s switch. Why a brief current, not a steady one?",
                 ["A changing field can induce current.",
                  "Opening the switch is a change.",
                  "After the field is steady at zero, the change is over, so the induced pulse ends."],
                 "induction needs a changing field", "", "Hard"),
        ("Thinking any metal core works as well as iron",
         "A wooden or copper core does not boost like iron. Iron is special among everyday materials for this job."),
        ("Switch, loops, current, core — four-word checklist",
         "On, many loops, large I, iron: strong. Missing any of those: weaker or off."),
        ican5, 21,
    ), ican5)

    ican6 = [
        "I can explain fuses/breakers as over-current shutoffs.",
        "I can say water plus outlets is a shock path.",
        "I can describe a ground prong as a safety path.",
    ]
    c6 = _with_ican(concept_block(
        "6. Household safety",
        [
            "Household circuits are parallel so devices can switch independently. Currents add at the breaker. A 10 A toaster plus a 5 A kettle is 15 A together. If the breaker is 15 A, you are at the limit.",
            "Wires heat when current is large (energy becoming thermal). A fuse melts a strip and opens the loop. A breaker is a reusable switch that trips. Never tape a breaker on. Find the overload or short first.",
            "Water with dissolved ions conducts. Hair dryers and sinks do not mix. Wet skin lowers resistance, so a given voltage can drive a more dangerous current through a person. GFCI outlets near water trip if hot and neutral currents do not match — a clue that current is leaking through a person or water.",
            "The third prong is a ground path. If a live wire touches a metal case, current can race to ground and trip a breaker instead of racing through you. Do not defeat that prong with a cheap adapter “because it fits.”",
            "Unplug by the plug, not by yanking the cord. Damaged insulation exposes metal. Overloaded strips and frayed cords are fire starters. These are not scare slogans; they are $P=VI$ and $I=V/R$ in a house.",
            "A bird on one wire often is not shocked because both feet are at nearly the same voltage — no path through the body. That is a complete-path lesson, not an invitation to climb poles.",
        ],
        "This unit’s math is useless if a student still thinks “more devices” cannot add current. Safety is parallel addition plus I=V/R through a human.",
        "Before resetting anything, lower the load. Near water, use GFCI. Three-prong plugs stay three-prong. Those three habits are the quiz and the life skill.",
        lesson_figure(
            _parallel_svg(),
            "Household branches in parallel",
            "Currents add at the supply. That sum is what a breaker watches.",
        )
        + solved(16, "A fuse is rated 5 A. A device draws 8 A. What should happen?",
                 ["8 A is above 5 A.",
                  "The fuse should open (melt) to protect the wires.",
                  "Putting a bigger fuse in to “make it work” can let the wires overheat."],
                 "fuse opens", "", "Easy")
        + solved(17, "Toaster 10 A and kettle 5 A on one 15 A parallel circuit. Total current?",
                 ["Parallel currents add.",
                  "$10+5=15$ A.",
                  "That equals the breaker’s rating — no spare room."],
                 "15 A", "", "Medium")
        + solved(18, "Why is a GFCI used by a sink?",
                 ["It compares current on hot versus neutral.",
                  "A mismatch means current is leaking — possibly through a person.",
                  "It opens quickly, faster than a regular breaker for that kind of leak."],
                 "trips on current mismatch (leak)", "", "Hard"),
        ("Resetting a breaker without unplugging the overload",
         "The trip was a message. Clearing the extra load first is the procedure. Forcing it on repeats the heat."),
        ("Add the amps for parallel devices",
         "Write each device’s current in a list and add. That sum is what the breaker sees. Series thinking (sharing one current) is the trap in a kitchen."),
        ican6, 26,
    ), ican6)

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8
# ===========================================================================

def _u8_questions():
    rows = [
        ("Earth’s layers from outside in are…",
         "crust, mantle, outer core, inner core",
         "The crust is thin and least dense. The inner core is solid iron-nickel and most dense in this course’s picture.",
         ["inner core, ocean, crust, cloud", "mantle, then crust at the center", "only crust and air"]),
        ("Why is the crust on top of the mantle in the density story?",
         "the crust is less dense, so it “floats” on denser mantle rock in a slow, solid way",
         "Same idea as oil on water, but rock is solid and the motion is geologic-slow.",
         ["the crust is the densest layer", "gravity is off in the crust", "the mantle is a gas"]),
        ("The outer core is liquid metal. That matters because…",
         "moving liquid iron is linked to Earth’s magnetic field (Grade 9 idea)",
         "You do not need dynamo math. Liquid metal + motion → magnetism is the hook back to Unit 7.",
         ["liquid metal means Earth has no gravity", "the crust is liquid iron", "air is liquid metal"]),
        ("A sample of crust rock is 2.7 g/cm³ and a core-like metal is 10 g/cm³. Which sinks in a density column of those melted ideas?",
         "the metal", "10 > 2.7, so the denser stuff belongs deeper in Earth’s gravity well.",
         ["the crust rock", "they must layer the same", "density does not affect layering"]),
        ("Earthquakes and volcanoes are more common at…",
         "plate boundaries, where crust pieces interact",
         "Physical science meets Earth science: moving plates, not random magic.",
         ["only at the North Pole", "only in the inner core where people live", "nowhere; the crust never moves"]),
        ("Air pressure is caused by…",
         "the weight of the air above you (particles colliding with surfaces)",
         "More air piled above means more pressure. That is why pressure is higher at sea level than on a mountain.",
         ["the color of the sky", "Earth’s magnetic poles only", "sound from birds"]),
        ("As you climb a mountain, air pressure usually…",
         "decreases",
         "Less atmosphere above you. Ears “pop” as pressure changes.",
         ["increases because you are closer to space", "becomes infinite", "is unrelated to height"]),
        ("A sealed bag of chips puffs up on a mountain because…",
         "outside pressure dropped while inside pressure stayed about the same",
         "The bag is a flexible wall. Higher inside push inflates it.",
         ["the chips gained mass", "gravity reversed", "the bag became a vacuum pump"]),
        ("Weather maps’ “highs” and “lows” are about…",
         "air pressure patterns that help drive wind",
         "Air tends to move from higher pressure toward lower pressure. That is a force-from-pressure-difference idea.",
         ["only temperature in the core", "ocean salinity only", "star color"]),
        ("A deeper dive in a pool means more pressure because…",
         "more water weight is above you",
         "Same story as the atmosphere, now with a liquid. Water is denser, so pressure rises fast with depth.",
         ["water has no weight", "pressure is only from air even underwater", "depth lowers pressure"]),
        ("The water cycle’s main phase changes are…",
         "evaporation (and transpiration), condensation, then precipitation",
         "Liquid → gas up, gas → liquid in clouds, then rain/snow down. Energy from the Sun drives evaporation.",
         ["only freezing of the inner core", "nuclear fusion in clouds", "magnets pulling rain"]),
        ("Clouds form when water vapor…",
         "cools and condenses onto tiny particles",
         "Condensation is the gas-to-liquid change from Unit 5, now in the sky.",
         ["evaporates more", "becomes helium", "turns into rock"]),
        ("Rain is precipitation of liquid water. Snow is precipitation of…",
         "solid water (ice crystals)",
         "Same cycle, different temperature history in the cloud.",
         ["liquid nitrogen", "pure salt", "iron from the core"]),
        ("The Sun’s role in the water cycle is mainly to…",
         "supply energy for evaporation",
         "Without that energy, oceans would not send much vapor aloft.",
         ["push tectonic plates each hour", "create Earth’s magnetic field each minute", "stop condensation"]),
        ("A puddle disappearing on a warm day is…",
         "evaporation",
         "Liquid to vapor at the surface. The vapor is still water — a physical change.",
         ["a chemical change into oxygen", "condensation", "the puddle sinking as a solid"]),
        ("Seasons are caused mainly by…",
         "Earth’s tilted axis as Earth orbits the Sun",
         "When your hemisphere tilts toward the Sun, daylight is longer and rays are more direct: summer. Tilt away: winter. Not “Earth is closer in summer” as the main reason.",
         ["Earth hopping much closer every June for the whole planet equally", "the Moon’s phase", "Earth’s magnetic field flipping each month"]),
        ("Earth’s axis tilt is about…",
         "23.5°",
         "That tilt, not a huge change in Sun distance, is the season engine for a given hemisphere.",
         ["0° (no tilt)", "90°", "180°"]),
        ("In June, the Northern Hemisphere has summer because…",
         "it is tilted toward the Sun",
         "Meanwhile the Southern Hemisphere is tilted away and has winter. Distance from the Sun is not the main seasonal switch.",
         ["the North Pole is always in darkness in June", "Earth stops orbiting", "the Sun turns off UV"]),
        ("If Earth had no tilt, seasons would be…",
         "much weaker (no strong summer/winter contrast from tilt)",
         "Day length and ray angle would not swing as they do now.",
         ["stronger", "caused by magnetism only", "exactly the same as now"]),
        ("Direct rays (high Sun in the sky) spread energy over…",
         "a smaller area, so that ground warms more",
         "Winter Sun sits lower; the same energy smears over more ground. That is a geometry of tilt and latitude.",
         ["a larger area always when the Sun is high", "no area", "only the ocean floor"]),
        ("Planets stay in orbit because…",
         "gravity pulls them toward the Sun while their motion keeps them from falling straight in",
         "Gravity is the inward pull. Sideways speed makes a curve — an orbit — instead of a crash. No calculus needed: “pull + sideways motion.”",
         ["a giant invisible string you can grab", "they have no mass", "magnetism of ice"]),
        ("A more massive planet pulls with a _____ gravitational force on a nearby moon (same distance).",
         "larger",
         "More mass, stronger pull. Closer also means stronger pull in this course’s qualitative rule.",
         ["smaller always", "zero", "magnetic-only"]),
        ("The Moon’s gravity on Earth is the main cause of…",
         "ocean tides (along with the Sun’s smaller share)",
         "Tides are a gravity-and-motion story, not a wind story.",
         ["Earth’s seasons", "Earth’s magnetic field", "the water cycle’s evaporation energy"]),
        ("Weight is less on the Moon because…",
         "the Moon’s g is smaller, while your mass stays the same",
         "Unit 4 again: mass versus weight, now in space class.",
         ["your mass is deleted", "there is no inertia on the Moon", "the Moon has no gravity at all"]),
        ("If the Sun’s gravity suddenly vanished (thought experiment), planets would…",
         "fly off in a straight line at their current velocity (first law)",
         "Gravity is the force that bends the path. Remove it, first law takes over.",
         ["stop dead", "spiral into Earth", "become negatively charged"]),
        ("Stars produce energy mainly by…",
         "nuclear fusion in their cores (Grade 9: light nuclei joining, releasing energy)",
         "The Sun is not burning wood. Fusion is a nuclear change, not a campfire chemical change.",
         ["burning coal", "only reflecting other stars", "sound"]),
        ("A star’s spectrum (rainbow with dark lines) can tell us…",
         "which elements are in the star’s atmosphere",
         "Each element eats specific colors, leaving fingerprints — absorption lines. That is “spectra intro,” not a full quantum course.",
         ["only the star’s age in days with no other data", "Earth’s crust density", "the number of planets with oceans for sure"]),
        ("A hot star’s visible color tends to be _____ than a cooler star’s.",
         "bluer (higher-frequency light)",
         "A stove coil: hotter glows brighter and whiter/bluer. Cooler stars look redder. Do not confuse with red-shift motion yet unless a stretch item says so.",
         ["always redder when hotter", "unrelated to temperature", "only green"]),
        ("The Sun looks yellow-white and is a medium star. Night stars that look red are often…",
         "cooler at the surface than the Sun",
         "Color is a temperature clue in this intro.",
         ["always hotter than the Sun", "not stars", "only planets"]),
        ("Dark lines in a solar spectrum are there because…",
         "cooler gases above the photosphere absorb specific wavelengths",
         "The missing colors are the fingerprints. Continuous rainbow plus missing slices.",
         ["the Sun has no hydrogen", "space paints black stripes on light", "sound waves block colors"]),
        ("Which layer is least dense?",
         "crust", "Density increases toward the center in the simple layered model.",
         ["inner core", "outer core", "lower mantle compared with crust"]),
        ("Why do your ears pop on a plane’s climb?",
         "outside pressure falls; trapped air in the ear tries to equalize",
         "Pressure difference on a membrane is a force. Yawning or chewing helps open a path.",
         ["the cabin creates extra rock density", "gravity shuts off", "sound becomes light"]),
        ("Dew on grass in the morning is usually…",
         "condensation of water vapor onto cool surfaces",
         "Air near the ground cooled overnight. Gas became liquid droplets.",
         ["evaporation of the grass into hydrogen", "precipitation from space ice only", "a chemical change into nitrogen"]),
        ("December in Australia is summer because…",
         "the Southern Hemisphere is tilted toward the Sun then",
         "Seasons are opposite in the two hemispheres. It is not “the whole Earth closer.”",
         ["Australia is closer to the Sun as a country every December for distance-only reasons", "the tilt disappears", "the Moon heats Australia"]),
        ("A satellite stays in orbit because it is…",
         "falling around Earth — gravity pulls while sideways speed keeps missing the ground",
         "Orbit is free-fall with the right sideways speed, not a place with zero gravity.",
         ["beyond all gravity", "held by air", "magnetically locked to the crust"]),
        ("Fusion in the Sun joins hydrogen into helium and releases energy that eventually leaves as…",
         "sunlight (EM radiation) and other radiation",
         "That radiation is Unit 6’s spectrum hitting Earth: visible, IR, UV.",
         ["sound through space", "ocean water", "crust rock"]),
        ("A 3.0 g crust sample has volume 1.0 cm³. Density is 3.0 g/cm³. A 11 g metal grain of 1.0 cm³ would sit _____ in a density ranking of Earth’s layers.",
         "deeper (denser, like core material)",
         "11 g/cm³ is core-like compared with ~3 g/cm³ crust.",
         ["in the atmosphere", "above the crust always", "in orbit"]),
        ("Wind is air moving. A simple driver is…",
         "pressure differences (and heating differences that help cause them)",
         "Uneven heating → pressure patterns → air flows. Convection from Unit 5 on a planetary scale.",
         ["Earth’s inner core freezing each night", "stars pulling air by spectra", "sound from the ocean floor"]),
        ("Snow, melt, river, ocean, cloud is a…",
         "water-cycle path using melting, flow, evaporation, condensation",
         "Phase changes plus gravity plus solar energy.",
         ["nuclear fusion path", "series circuit of ice", "magnetic cycle only"]),
        ("Equator versus pole: the equator gets more direct sunlight on average, so it is…",
         "warmer, which helps drive atmospheric convection",
         "Latitude plus tilt sets the energy budget. Poles get slanted, spread-out rays.",
         ["colder because it is closer to space", "the same T as poles always", "heated only by Earth’s core at the surface"]),
        ("The inner core is solid even though it is extremely hot because…",
         "enormous pressure keeps it solid",
         "Temperature is not the only variable. Pressure can lock a metal solid. Grade 9 qualitative fact.",
         ["it is actually ice", "there is no pressure there", "it is empty"]),
        ("A helium balloon rises because…",
         "the balloon plus helium is less dense than the surrounding air",
         "Unit 1 density again, now in the atmosphere.",
         ["helium is magnetic north", "gravity does not act on helium", "balloons have no mass"]),
        ("If Earth’s tilt increased a lot, seasonal contrasts would likely…",
         "become more extreme",
         "More tilt, more summer/winter difference in daylight and ray angle.",
         ["disappear", "depend only on the Moon", "reverse gravity"]),
        ("Comets’ tails point away from the Sun mainly because of…",
         "solar wind and sunlight pushing dust and gas, not because the comet is “falling up”",
         "A qualitative space fact tying radiation and particles to gravity-bound icy bodies.",
         ["Earth’s seasons", "ocean tides on the comet", "sound from the Sun"]),
        ("Two absorption-line patterns match hydrogen’s lab fingerprint. The star’s atmosphere…",
         "contains hydrogen",
         "Matching lines is the ID method. That is the whole spectra intro.",
         ["cannot contain hydrogen", "must be a planet", "is made of crust rock"]),
        ("Day and night are caused by…",
         "Earth rotating on its axis",
         "Orbit around the Sun is the year. Rotation is the day. Tilt-plus-orbit is the season.",
         ["the Sun orbiting Earth each day in the modern model", "the Moon blocking the Sun each night", "stars turning off"]),
        ("Challenge Stretch: Crust ~2.7 g/cm³, mantle ~3.4, outer core ~11. A 54 g sample has volume 5.0 cm³. Find D, then choose crust-like, mantle-like, or core-like.",
         "10.8 g/cm³; core-like metal",
         "$D=54/5.0=10.8$ g/cm³, near outer-core values, far above crust or mantle rock.",
         ["10.8 g/cm³; crust rock", "2.7 g/cm³; crust", "54 g/cm³; atmosphere"]),
        ("Challenge Stretch: A hiker’s water boils at 92 °C on a 3000 m peak. Sea-level boiling is 100 °C. Combine pressure-with-height and boiling-with-pressure to explain both numbers.",
         "higher up, the air column is thinner (lower pressure), so bubbles form at a lower temperature",
         "Pressure drops with height because less air sits above you. Boiling is easier at lower pressure, so the thermometer reads 92 °C, not 100 °C.",
         ["the mountain is always hotter than 100 °C", "water’s density becomes zero at 3000 m", "gravity is stronger on mountains so boiling T rises"]),
        ("Challenge Stretch: A snowflake lands, melts on a sidewalk, the puddle dries, and the vapor later forms frost on a cold window. Name the four phase changes in order.",
         "already solid snow, then melting, then evaporation, then deposition",
         "Solid → liquid (melt), liquid → gas (evaporate), gas → solid frost (deposition). Not the glacier-to-cloud melt–evaporate–condense path.",
         ["fusion of hydrogen, then rusting", "only freezing twice", "ionic bonding into NaCl"]),
        ("Challenge Stretch: On March 21 both hemispheres get similar sunlight. On December 21, Cape Town (south) has long days while London (north) has short days. Which hemisphere is leaning toward the Sun in December, and why is Earth–Sun distance not the explanation?",
         "the Southern Hemisphere; both cities are essentially the same distance from the Sun that day",
         "Tilt aims the south toward the Sun in December, so Cape Town’s rays are more intense and days are longer. Distance is shared; tilt-plus-intensity is not.",
         ["the Northern Hemisphere; London is much closer to the Sun as a city", "neither; Cape Town is closer to the Sun", "the Sun’s fusion pauses for London"]),
        ("Challenge Stretch: A 5.0 kg lander weighs 18 N on a small moon. Find g on that moon, then the lander’s weight on Earth if g_E=9.8 N/kg.",
         "3.6 N/kg on the moon; 49 N on Earth",
         "$g=W/m=18/5.0=3.6$ N/kg. Mass stays 5.0 kg, so Earth weight is $5.0\\times9.8=49$ N. New g, two weights.",
         ["18 N/kg; 18 N on Earth", "3.6 N/kg; 18 N on Earth", "9.8 N/kg; 49 N on the moon"]),
        ("Challenge Stretch: A probe has 8 km/s of sideways speed at a place where, if dropped from rest, gravity would add about 0.008 km/s of inward speed each second. Why does it miss the planet in the next second instead of falling in?",
         "g pulls inward and changes the direction of v, but the large sideways speed carries it far enough around that the path stays a curve",
         "Two arrows: inward g and tangent v. If sideways speed were 0 it would fall in. With 8 km/s sideways, one second of inward tug only bends the path; it does not cancel the sideways motion.",
         ["the planet’s gravity is zero at that height", "the probe has no mass", "magnetism cancels gravity exactly"]),
        ("Challenge Stretch: A star’s spectrum shows hydrogen lines shifted toward red compared with a lab lamp. A Grade 9 reading is…",
         "the star is moving away (Doppler-like stretch of light waves)",
         "Same idea as a dropping pitch, now with light. You do not need Hubble’s law numbers. Stretch of λ means receding in this intro.",
         ["the star must be cooler only, with no motion idea", "hydrogen vanished", "the star is a planet"]),
        ("Challenge Stretch: Air column: 1 m² of atmosphere weighs about 100,000 N at sea level (10⁵ Pa). On a peak where the column is half as massive, pressure is about…",
         "half as large",
         "Pressure is force/area from the weight above. Half the weight, half the pressure (same area).",
         ["unchanged", "doubled", "zero"]),
        ("Challenge Stretch: Why is the inner core denser than the crust even though both are “solid”?",
         "it is iron-nickel under huge pressure, not the lighter silicate rock of crust",
         "Solid does not mean same density. Unit 1: different materials pack different mass into the same volume.",
         ["solids all have density 1 g/cm³", "the crust is pure gold", "density decreases toward Earth’s center"]),
    ]
    return fill_qs(_pack(rows), 55, lambda i: mq(
        f"A {3+i} g crust sample has volume 1 cm³. Density in g/cm³?",
        3 + i, f"D=m/V={3+i}/1={3+i}.", i, distractors=[1, i, (3 + i) * 2]
    ))


def build_unit8():
    title = "Physical Science Unit 8: Earth-Space Physical Science"
    description = (
        "Earth’s layers and density, atmosphere and pressure, the water cycle as phase change, "
        "seasons and tilt, orbital gravity, and star spectra — Grade 9, with custom Earth diagrams."
    )
    concepts = [
        "Earth's layers and density",
        "Atmosphere and pressure",
        "Water cycle as phase change",
        "Seasons and Earth's tilt",
        "Solar system gravity",
        "Stars and spectra intro",
    ]
    ican1 = [
        "I can name crust, mantle, outer core, inner core from outside in.",
        "I can connect density to why dense metal sits deeper.",
        "I can link the liquid outer core to Earth’s magnetic field at a Grade 9 level.",
    ]
    c1 = _with_ican(concept_block(
        "1. Earth's layers and density",
        [
            "Earth is layered like a peach: a thin skin (crust), a thick rocky mantle, a liquid metal outer core, and a solid metal inner core. You will not dig there. We infer layers from earthquake waves, density, and rocks that reach the surface.",
            "Density is the organizer. Crust rock is around 2.7 g/cm³. The core is many times denser, iron-nickel rich. In gravity, denser stuff sinks. Earth sorted itself when it was hotter and more mixed, a long time ago.",
            "Everyday analogy: a shaken bottle of oil and water. When it settles, oil (less dense) is on top. Earth’s “settling” happened in molten times; now the layers are mostly locked, with slow mantle motion.",
            "The outer core’s liquid iron in motion is the Grade 9 reason Earth has a magnetic field (Unit 7’s compass). The inner core is solid because pressure is enormous even though it is extremely hot. Hot does not always mean liquid when pressure is huge.",
            "Plates of crust move slowly. Earthquakes and volcanoes cluster at their edges. That is motion and force on a planetary scale, not a new kind of physics.",
            "When a question gives mass and volume of a “mystery sample,” compute $D=m/V$ and match it to crust-like or core-like numbers.",
        ],
        "Atmosphere, gravity, and magnetism all sit on this layered ball. If the core is “just more dirt,” the compass lesson has no engine.",
        "List the four layers outside-in. Write “density up toward the center.” Then, for a sample, compute D and compare with ~3 versus ~10 g/cm³.",
        lesson_figure(
            _earth_layers_svg(),
            "Earth in cross section (not to scale)",
            "Yellow-tan crust, orange mantle, red outer core, pink inner core. Density rises inward.",
        )
        + solved(1, "Name Earth’s layers from the surface inward.",
                 ["Start at the surface: crust.",
                  "Then mantle, then liquid outer core, then solid inner core.",
                  "Do not put the crust in the center."],
                 "crust, mantle, outer core, inner core", "", "Easy")
        + solved(2, "Why is the crust “on top” in the density story?",
                 ["Crust is less dense than mantle and core.",
                  "Denser material sank toward the center long ago.",
                  "Less dense rock ended up as the outer layer."],
                 "crust is least dense", "", "Medium")
        + solved(3, "A 10 g metal grain has volume 1 cm³. Crust is ~2.7 g/cm³. Is this grain crust-like?",
                 ["D=10/1=10 g/cm³.",
                  "That is far above 2.7.",
                  "It is core-like metal, not crust rock."],
                 "no; ~10 g/cm³ is core-like", "", "Hard"),
        ("Thinking all solids have the same density",
         "Ice, crust rock, and iron are all solids and pack very differently. Solid is a state, not a density number."),
        ("Compute D, then match the layer",
         "Do not guess “it came from the mantle” from the word rock. The number 3 versus 10 g/cm³ is the tell."),
        ican1, 1,
    ), ican1)

    ican2 = [
        "I can say air pressure comes from the weight of air above.",
        "I can predict lower pressure at higher altitude.",
        "I can explain a puffed chip bag on a mountain.",
    ]
    c2 = _with_ican(concept_block(
        "2. Atmosphere and pressure",
        [
            "The atmosphere is the blanket of gases around Earth, mostly nitrogen and oxygen — a mixture (Unit 3). It is thicker (more particles per volume) near the ground and thinner high up.",
            "Air pressure is the push from air particles hitting a surface. A tall stack of air weighs more than a short stack, so sea-level pressure is larger than mountain pressure. Everyday number: about 100,000 N on each square meter at sea level (10⁵ Pa). You do not feel crushed because fluids in your body push back.",
            "Everyday analogy: standing at the bottom of a swimming pool versus the surface. More water above you, more squeeze. Air is a thinner ocean you live at the bottom of.",
            "A bag of chips puffs on a mountain because outside pressure dropped. Inside the bag, pressure stayed closer to the factory’s sea-level value, so the bag inflates.",
            "Wind is air moving, often from higher pressure toward lower pressure, steered also by Earth’s spin (you do not need Coriolis math). Uneven heating (equator versus pole, land versus sea) helps build those pressure patterns — convection on a planet.",
            "Water pressure underwater uses the same weight-above idea. Go deeper, more pressure. That is why submarines need strong hulls.",
        ],
        "Boiling-point stretch items and weather both need “pressure is weight of fluid above.” If pressure is “just a weather-map decoration,” mountains and ears popping are mysteries.",
        "Ask: did the column of air (or water) above get shorter or taller? Shorter column, less pressure. Then apply that to ears, bags, and boiling.",
        lesson_figure(
            _atm_svg(),
            "Atmosphere piled on the ground",
            "More air above you at the surface: higher pressure. Thin air on a peak: lower pressure.",
        )
        + solved(4, "Does air pressure go up or down as you climb a mountain?",
                 ["Less atmosphere sits above you.",
                  "Less weight of air, less pressure.",
                  "Pressure decreases."],
                 "decreases", "", "Easy")
        + solved(5, "Why does a sealed chip bag puff on a mountain?",
                 ["Outside pressure fell.",
                  "Inside pressure is still near the original.",
                  "The bag’s walls are pushed outward."],
                 "outside P dropped", "", "Medium")
        + solved(6, "Why can water boil below 100 °C on a high peak?",
                 ["Boiling is when bubbles can form against the surrounding pressure.",
                  "Lower air pressure means bubbles form more easily.",
                  "The boiling temperature drops. Sea-level 100 °C is not a universal law."],
                 "lower P, lower boiling T", "", "Hard"),
        ("Thinking you leave the atmosphere at a mountain peak",
         "There is still air — just less of it. Planes fly in thin air, not in outer-space vacuum. Pressure is lower, not zero."),
        ("Column above you",
         "Draw a stack of boxes of air. Cross some out as you climb. The leftover stack is the pressure story."),
        ican2, 6,
    ), ican2)

    ican3 = [
        "I can name evaporation, condensation, and precipitation in the cycle.",
        "I can say the Sun supplies energy for evaporation.",
        "I can treat the cycle as Unit 5 phase changes on a planet.",
    ]
    c3 = _with_ican(concept_block(
        "3. Water cycle as phase change",
        [
            "The water cycle is water moving among ocean, air, land, and ice, changing phase as it goes. It is Unit 5’s melting, evaporation, condensation, and freezing, plus gravity pulling rain down.",
            "The Sun supplies energy that evaporates water from oceans, lakes, and wet ground. Plants also release vapor (transpiration). That is liquid (or ice, via sublimation) becoming gas.",
            "High up, air cools. Water vapor condenses onto tiny particles and makes cloud droplets or ice crystals. Condensation is gas to liquid (or deposition to solid). Energy is released to the air in that step.",
            "Precipitation is water falling: rain, snow, sleet, hail. Then runoff and groundwater return water toward the ocean. The story repeats. Everyday analogy: a pot of water, a lid with droplets, and drips — a kitchen cycle.",
            "A puddle on a warm day shrinks by evaporation, a physical change. The water is still H₂O. Dew on grass is condensation on a cold surface.",
            "Mass of water on Earth is roughly conserved in this cycle (ignoring tiny losses to space). Conservation of mass from Unit 3 still holds. The water changes address, not identity.",
        ],
        "If the cycle is “rain happens,” you missed the energy and phase names this whole course practiced. Weather is applied physical science.",
        "For any diagram, label the phase at each arrow: liquid, gas, or solid. Then name the change: evaporation, condensation, melting, freezing, precipitation.",
        lesson_figure(
            _water_cycle_svg(),
            "Evaporation up, precipitation down",
            "Sun-driven vapor rises; cooling makes clouds; gravity returns the water.",
        )
        + solved(7, "What phase change turns ocean water into vapor?",
                 ["Liquid becomes gas.",
                  "The name is evaporation (or boiling, if it were at boiling T throughout).",
                  "The Sun’s energy pays for that change."],
                 "evaporation", "", "Easy")
        + solved(8, "Cloud droplets form by which phase change?",
                 ["Vapor becomes liquid (or ice).",
                  "That is condensation (or deposition).",
                  "Cooling high in the atmosphere helps."],
                 "condensation", "", "Medium")
        + solved(9, "Trace glacier ice to a raindrop using common liquid steps.",
                 ["Ice melts to liquid water.",
                  "Water evaporates to vapor.",
                  "Vapor condenses to a cloud droplet that can fall as rain."],
                 "melt → evaporate → condense", "", "Hard"),
        ("Calling rain a chemical change into a new compound",
         "Rain is still H₂O. The cycle rearranges state and location, not the water molecule’s identity."),
        ("Write the phase on every arrow",
         "If an arrow has no phase name, you cannot tell evaporation from condensation. The labels are the answer."),
        ican3, 11,
    ), ican3)

    ican4 = [
        "I can say seasons come from tilt plus orbit, not from “much closer in summer.”",
        "I can explain opposite seasons in opposite hemispheres.",
        "I can connect direct rays and longer days to summer warming.",
    ]
    c4 = _with_ican(concept_block(
        "4. Seasons and Earth's tilt",
        [
            "Earth orbits the Sun once a year and rotates once a day. Seasons are not mainly “we are much closer in summer.” Earth’s orbit is only slightly oval. The season engine is the tilt of Earth’s axis, about 23.5°, as Earth goes around the Sun.",
            "When the Northern Hemisphere tilts toward the Sun, that hemisphere gets more direct rays and longer daylight: summer. The Southern Hemisphere tilts away then: winter. Six months later the roles swap. June can be winter in Australia.",
            "Direct rays hit a smaller patch of ground, so that patch gets more energy per square meter. Winter Sun sits lower; the same sunlight smears over a larger area and passes through more atmosphere. Days are also shorter.",
            "Everyday analogy: a flashlight straight onto a floor makes a small bright circle. Tilt the flashlight and the patch is larger and dimmer. Tilt is the flashlight angle.",
            "If Earth had no tilt, seasons would be weak. You would still have day and night from rotation, and a small distance effect from the oval orbit, but not the strong summer/winter swing we know.",
            "Day and night are rotation. The year is the orbit. Seasons are tilt-during-orbit. Keep those three clocks separate.",
        ],
        "The “closer in July” myth fails the Southern Hemisphere test. If you cannot explain Sydney’s summer in December, you do not own this lesson.",
        "Name the hemisphere, then ask whether it is tilted toward or away on that date. Toward: summer. Away: winter. Same Sun distance for both.",
        lesson_figure(
            _seasons_svg(),
            "Tilt, not a huge jump in Sun distance",
            "June: Northern axis toward the Sun. December: Northern axis away. The red line is the axis.",
        )
        + solved(10, "What is the main cause of seasons?",
                 ["Earth is tilted.",
                  "As Earth orbits, a hemisphere leans toward or away from the Sun.",
                  "That changes daylight and ray directness."],
                 "axial tilt during the orbit", "", "Easy")
        + solved(11, "Why is it summer in Sydney when it is winter in New York?",
                 ["They are in opposite hemispheres.",
                  "When the North tilts away, the South tilts toward.",
                  "Both are about the same distance from the Sun that day."],
                 "opposite tilts (not different distances)", "", "Medium")
        + solved(12, "Why do direct (high) Sun rays warm a patch more than low winter rays?",
                 ["The same energy hits a smaller area when the Sun is high.",
                  "Low Sun smears energy over more ground.",
                  "More joules per square meter means more warming."],
                 "energy concentrated on a smaller area", "", "Hard"),
        ("“Summer happens because Earth is closer to the Sun”",
         "Then both hemispheres would have summer together. They do not. Tilt explains opposite seasons. Distance is a small extra, not the main switch."),
        ("Globe, flashlight, tilt",
         "If you can picture the flashlight patch, you can picture June versus December. Draw the axis before you pick an answer."),
        ican4, 16,
    ), ican4)

    ican5 = [
        "I can say gravity plus sideways motion makes an orbit.",
        "I can tell mass from weight on another world.",
        "I can name tides as mostly the Moon’s gravity.",
    ]
    c5 = _with_ican(concept_block(
        "5. Solar system gravity",
        [
            "Gravity pulls any two masses together. The Sun is massive, so it pulls the planets strongly. The pull is stronger when masses are larger and when objects are closer. We will not use Newton’s full inverse-square formula unless a number is handed to you as g.",
            "Planets do not fall straight into the Sun because they also have sideways speed. Gravity bends the straight-line path (Newton’s first law) into a curve — an orbit. Everyday analogy: a ball on a string you swing. The string’s pull is inward; the ball’s motion is around. Cut the string (no pull) and the ball flies off straight.",
            "Satellites, including the Moon and the ISS, are in free-fall around Earth. They are not “beyond gravity.” They keep missing the ground because of sideways speed.",
            "Mass stays the same on the Moon. Weight drops because g is smaller. A 2 kg probe is still 2 kg; its weight is $mg$.",
            "The Moon’s gravity stretches Earth’s oceans (and the Sun helps a bit): tides. Seasons are not tides. Do not mix those chapters.",
            "If the Sun’s gravity vanished in a thought experiment, planets would go straight at their current velocity. That is first law, now in space.",
        ],
        "Stars and spectra still sit in a gravitational solar system. If orbit is “no gravity in space,” weightlessness on the ISS is misunderstood (they are falling together).",
        "Write two ingredients of orbit: inward pull, sideways speed. For weight, change g, not kilograms.",
        lesson_figure(
            _orbit_svg(),
            "Earth on a circular path around the Sun",
            "Gravity points inward (g). Velocity is tangent (v). The two arrows together make an orbit, not a seasons-tilt sketch.",
        )
        + solved(13, "Why don’t planets fall straight into the Sun?",
                 ["The Sun’s gravity pulls inward.",
                  "Planets also move sideways.",
                  "The combination is a curve around the Sun, an orbit."],
                 "gravity + sideways speed", "", "Easy")
        + solved(14, "A 2 kg probe on a world with g=4.9 N/kg. Mass and weight?",
                 ["Mass is still 2 kg.",
                  "W=2×4.9=9.8 N.",
                  "Half of Earth’s g (9.8) gives half the Earth weight."],
                 "2 kg; 9.8 N", "", "Medium")
        + solved(15, "If the Sun’s gravity vanished, what would planets do, and which law is that?",
                 ["No net force from the Sun.",
                  "First law: constant velocity — a straight line.",
                  "They would not stop dead and would not keep circling."],
                 "straight-line coast (first law)", "", "Hard"),
        ("“There is no gravity in space”",
         "Astronauts float because they and their station fall together, not because g=0. Earth’s gravity at ISS height is still most of surface g."),
        ("Two arrows: inward g, tangent velocity",
         "That sketch is the orbit. Missing either arrow gives a crash or a straight escape."),
        ican5, 21,
    ), ican5)

    ican6 = [
        "I can say stars shine by fusion, not by burning wood.",
        "I can treat spectral lines as element fingerprints.",
        "I can connect hotter stars to bluer light at an intro level.",
    ]
    c6 = _with_ican(concept_block(
        "6. Stars and spectra intro",
        [
            "Stars are glowing balls of gas. The Sun is our star. They make energy by nuclear fusion in the core: light nuclei join and release energy. That is not a chemical campfire. The energy eventually leaves as electromagnetic radiation — Unit 6’s spectrum: visible, IR, UV, and more.",
            "A spectrum is a spread of colors. A hot dense glow makes a rainbow (continuous spectrum). Cooler gas in front can absorb specific colors and leave dark lines. Those lines are fingerprints. Hydrogen’s pattern in a lab lamp matching a star means the star’s atmosphere has hydrogen.",
            "Everyday analogy: a barcode. Each element has its own barcode of missing (or bright) lines. You do not need energy-level math. Match the bars, name the element.",
            "Hotter stars look bluer; cooler stars look redder, like a stove coil going from red to white-hot. The Sun is a medium-temperature yellow-white star. This is a temperature-color clue, not a full brightness-distance lab.",
            "If a star’s barcode is shifted toward red compared with the lab, a Grade 9 Doppler-like reading is that the star is moving away (waves stretched). You do not need Hubble’s law numbers here.",
            "Light from stars travels through vacuum at c. Sound from stars does not arrive. Space is dark between stars except for that EM radiation — and silent.",
        ],
        "This closes the course: atoms (Unit 2) leave fingerprints in starlight, waves (Unit 6) carry the light, gravity (Unit 4/8) holds the star and the planet. Physical science is one story.",
        "Ask: fusion or chemical burn? Fingerprint lines or paint? Hot-blue versus cool-red? Then you have the intro spectra toolkit.",
        lesson_figure(
            _spectra_star_svg(),
            "A rainbow with dark absorption lines",
            "The black slices are element fingerprints, not dirt on the telescope.",
        )
        + solved(16, "What process powers the Sun, at a Grade 9 level?",
                 ["Not burning coal or wood.",
                  "Nuclei join in the core: fusion.",
                  "Energy leaves as sunlight and other radiation."],
                 "nuclear fusion", "", "Easy")
        + solved(17, "Dark lines in the Sun’s rainbow match hydrogen’s lab lines. Conclusion?",
                 ["Matching fingerprints mean the same element.",
                  "The Sun’s atmosphere contains hydrogen.",
                  "The lines are missing colors, not extra paint."],
                 "hydrogen is present", "", "Medium")
        + solved(18, "A star looks redder than the Sun. Intro conclusion about surface temperature?",
                 ["Cooler objects glow redder on the stove-coil scale.",
                  "The star’s surface is cooler than the Sun’s in this simple color rule.",
                  "(A later course adds brightness and distance; here color is the clue.)"],
                 "cooler surface", "", "Hard"),
        ("Thinking stars are on fire like logs",
         "Fire is a chemical reaction with oxygen. Space has no air for a campfire. Fusion is a nuclear process in a hot, dense core."),
        ("Compare the barcode to a lab chart",
         "Do not invent elements from the star’s color alone when lines are given. Lines ID the gas. Color ID’s the rough temperature."),
        ican6, 26,
    ), ican6)

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Matter and Measurement', ['States of matter', 'Mass volume density', 'Physical vs chemical change', 'Measurement and units', 'Scientific notation intro', 'Graphs of data']), ('Atoms and the Periodic Table', ['Atomic model timeline', 'Protons neutrons electrons', 'Ions and isotopes', 'Periodic table organization', 'Metals nonmetals metalloids', 'Electron shells intro']), ('Bonding and Chemical Reactions', ['Ionic vs covalent', 'Chemical formulas', 'Balancing equations', 'Types of reactions', 'Conservation of mass', 'Mixtures vs compounds']), ('Motion and Forces', ['Speed and velocity', 'Acceleration', "Newton's first law", "Newton's second law", "Newton's third law", 'Gravity and weight']), ('Energy, Work, and Heat', ['Forms of energy', 'Work and simple machines', 'Conservation of energy', 'Temperature vs heat', 'Conduction convection radiation', 'Phase changes']), ('Waves, Sound, and Light', ['Wave parts', 'Speed frequency wavelength', 'Sound', 'Light and color', 'Reflection and refraction', 'Electromagnetic spectrum']), ('Electricity and Magnetism Intro', ['Charge and static electricity', 'Current and circuits', 'Series vs parallel', 'Magnets and poles', 'Electromagnets', 'Household safety']), ('Earth-Space Physical Science', ["Earth's layers and density", 'Atmosphere and pressure', 'Water cycle as phase change', "Seasons and Earth's tilt", 'Solar system gravity', 'Stars and spectra intro'])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>Physical Science Complete</h1>"
        f"<p><strong>For:</strong> <strong>High school Physical Science</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
