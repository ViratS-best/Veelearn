#!/usr/bin/env python3
"""AP Physics C E&M Units 5–8: RC, magnetism, induction, Maxwell/LC/FRQ."""

from __future__ import annotations

import math

from curriculum_kit import lesson_figure

from hs_science import (
    concept_block, solved, practice_slots, unit_shell, page_break, mq,
    xy_graph, sample_curve, series_circuit_svg, gauss_sphere_svg, energy_bars_svg,
)
from .common import AUDIENCE, STRETCH_LABEL
from .units_1_4 import (
    _pack, _ican, _plates_svg, _gauss_cylinder_svg, _kirchhoff_loop_svg, _dipole_svg,
    _two_loop_c_svg,
)


def _rc_svg(w=340, h=150):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="55" width="26" height="28" fill="#fef3c7" stroke="#0f172a"/>'
        f'<text x="18" y="48" font-size="11">ε</text>'
        f'<line x1="46" y1="69" x2="90" y2="69" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M90 69 l8 -12 l8 24 l8 -24 l8 24 l8 -12" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<text x="100" y="44" font-size="11">R</text>'
        f'<line x1="138" y1="69" x2="200" y2="69" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="200" y1="50" x2="200" y2="88" stroke="#1d4ed8" stroke-width="4"/>'
        f'<line x1="218" y1="50" x2="218" y2="88" stroke="#1d4ed8" stroke-width="4"/>'
        f'<text x="206" y="44" font-size="11">C</text>'
        f'<line x1="218" y1="69" x2="280" y2="69" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="280" y1="69" x2="280" y2="110" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="280" y1="110" x2="34" y2="110" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="34" y1="110" x2="34" y2="83" stroke="#0f172a" stroke-width="2"/>'
        f"</svg>"
    )


def _rl_svg(w=340, h=150):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="20" y="55" width="26" height="28" fill="#fef3c7" stroke="#0f172a"/>'
        f'<text x="18" y="48" font-size="11">ε</text>'
        f'<line x1="46" y1="69" x2="90" y2="69" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M90 69 l8 -12 l8 24 l8 -24 l8 24 l8 -12" fill="none" stroke="#b91c1c" stroke-width="2"/>'
        f'<text x="100" y="44" font-size="11">R</text>'
        f'<line x1="138" y1="69" x2="190" y2="69" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M190 69 q12 -18 24 0 q12 18 24 0 q12 -18 24 0" fill="none" stroke="#7c3aed" stroke-width="2"/>'
        f'<text x="214" y="44" font-size="11">L</text>'
        f'<line x1="262" y1="69" x2="300" y2="69" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="300" y1="69" x2="300" y2="110" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="300" y1="110" x2="34" y2="110" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="34" y1="110" x2="34" y2="83" stroke="#0f172a" stroke-width="2"/>'
        f"</svg>"
    )


def _lc_svg(w=300, h=150):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="40" y1="70" x2="90" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M90 70 q14 -20 28 0 q14 20 28 0 q14 -20 28 0" fill="none" stroke="#7c3aed" stroke-width="2"/>'
        f'<text x="118" y="44" font-size="12">L</text>'
        f'<line x1="174" y1="70" x2="210" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="210" y1="52" x2="210" y2="88" stroke="#1d4ed8" stroke-width="4"/>'
        f'<line x1="226" y1="52" x2="226" y2="88" stroke="#1d4ed8" stroke-width="4"/>'
        f'<text x="214" y="44" font-size="12">C</text>'
        f'<line x1="226" y1="70" x2="260" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="260" y1="70" x2="260" y2="115" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="260" y1="115" x2="40" y2="115" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="40" y1="115" x2="40" y2="70" stroke="#0f172a" stroke-width="2"/>'
        f"</svg>"
    )


def _solenoid_svg(w=300, h=140):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<ellipse cx="70" cy="70" rx="16" ry="36" fill="none" stroke="#0f172a" stroke-width="2"/>'
        f'<ellipse cx="230" cy="70" rx="16" ry="36" fill="none" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="70" y1="34" x2="230" y2="34" stroke="#0f172a" stroke-width="2"/>'
        f'<line x1="70" y1="106" x2="230" y2="106" stroke="#0f172a" stroke-width="2"/>'
        f'<path d="M90 34 q10 36 0 72 M120 34 q10 36 0 72 M150 34 q10 36 0 72 M180 34 q10 36 0 72 M210 34 q10 36 0 72" '
        f'fill="none" stroke="#7c3aed" stroke-width="1.6"/>'
        f'<line x1="90" y1="70" x2="210" y2="70" stroke="#b91c1c" stroke-width="2"/>'
        f'<polygon points="206,65 220,70 206,75" fill="#b91c1c"/>'
        f'<text x="140" y="62" font-size="12" fill="#b91c1c">B</text>'
        f'<text x="70" y="132" font-size="11">long solenoid: uniform B along the axis</text>'
        f"</svg>"
    )


def _wire_b_svg(w=240, h=180):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<circle cx="120" cy="90" r="10" fill="#fecaca" stroke="#b91c1c"/>'
        f'<text x="120" y="94" text-anchor="middle" font-size="11">I⊙</text>'
        f'<circle cx="120" cy="90" r="32" fill="none" stroke="#4f46e5" stroke-dasharray="4 3"/>'
        f'<circle cx="120" cy="90" r="52" fill="none" stroke="#4f46e5" stroke-dasharray="4 3"/>'
        f'<circle cx="120" cy="90" r="72" fill="none" stroke="#4f46e5" stroke-dasharray="4 3"/>'
        f'<text x="160" y="40" font-size="12" fill="#4f46e5">B</text>'
        f'<text x="20" y="172" font-size="11">circles around a long straight wire</text>'
        f"</svg>"
    )


def _lorentz_svg(w=280, h=160):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<text x="20" y="28" font-size="12">× × × ×  B into page</text>'
        f'<text x="20" y="48" font-size="12">× × × ×</text>'
        f'<circle cx="90" cy="100" r="10" fill="#93c5fd" stroke="#1e3a8a"/>'
        f'<text x="86" y="104" font-size="11">+q</text>'
        f'<line x1="102" y1="100" x2="170" y2="100" stroke="#0f172a" stroke-width="2"/>'
        f'<polygon points="166,95 180,100 166,105" fill="#0f172a"/>'
        f'<text x="130" y="92" font-size="12">v</text>'
        f'<line x1="90" y1="88" x2="90" y2="40" stroke="#b91c1c" stroke-width="2"/>'
        f'<polygon points="85,44 90,30 95,44" fill="#b91c1c"/>'
        f'<text x="100" y="50" font-size="12" fill="#b91c1c">F</text>'
        f'<text x="20" y="152" font-size="11">right-hand rule: v, B, F</text>'
        f"</svg>"
    )


def _flux_loop_svg(w=280, h=170):
    """Planar loop with B into the page (×), so Φ_B = BA."""
    crosses = []
    for x in (95, 125, 155, 185):
        for y in (58, 88):
            crosses.append(
                f'<text x="{x}" y="{y}" text-anchor="middle" font-size="14" fill="#4f46e5">×</text>'
            )
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<rect x="70" y="36" width="140" height="80" fill="#eef2ff" stroke="#0f172a" stroke-width="2.4"/>'
        f"{''.join(crosses)}"
        f'<text x="218" y="80" font-size="12" fill="#4f46e5">B into page</text>'
        f'<text x="88" y="152" font-size="11">× means B is perpendicular to the loop (into the page)</text>'
        f"</svg>"
    )


def _em_wave_svg(w=320, h=160):
    xlim, ylim = (0, 6.4), (-1.6, 1.6)
    epts = sample_curve(lambda x: math.sin(x), 0, 6.28)
    return xy_graph(
        curves=[("#b91c1c", epts), ("#1d4ed8", [(x, 0) for x, _ in epts])],
        xlim=xlim, ylim=ylim, w=w, h=h, xlab="x (propagation)", ylab="E (red)",
    )


def _disp_current_svg(w=280, h=150):
    return (
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img">'
        f'<line x1="30" y1="75" x2="100" y2="75" stroke="#0f172a" stroke-width="3"/>'
        f'<line x1="100" y1="40" x2="100" y2="110" stroke="#1d4ed8" stroke-width="4"/>'
        f'<line x1="130" y1="40" x2="130" y2="110" stroke="#1d4ed8" stroke-width="4"/>'
        f'<line x1="130" y1="75" x2="200" y2="75" stroke="#0f172a" stroke-width="3"/>'
        f'<text x="40" y="64" font-size="11">I_c</text>'
        f'<text x="150" y="64" font-size="11">I_c</text>'
        f'<text x="96" y="30" font-size="11">I_d = ε₀ dΦ_E/dt</text>'
        f'<line x1="105" y1="75" x2="125" y2="75" stroke="#059669" stroke-width="2" stroke-dasharray="4 3"/>'
        f'<text x="40" y="140" font-size="11">conduction current in wires; displacement in the gap</text>'
        f"</svg>"
    )


# ===========================================================================
# UNIT 5: RC Circuits
# ===========================================================================

def _u5_questions():
    return _pack([
        ("A capacitor $C$ is charged through $R$ from emf $\\varepsilon$ (switch closed at $t=0$, $Q(0)=0$). The differential equation from the loop is",
         "$R\\dot Q+Q/C=\\varepsilon$",
         "Kirchhoff: $\\varepsilon-IR-Q/C=0$ with $I=\\dot Q$.",
         ["$R\\dot Q=Q/C$", "$Q=\\varepsilon C e^{-t/RC}$", "$I=\\varepsilon C$"]),
        ("The charging solution is $Q(t)=C\\varepsilon(1-e^{-t/\\tau})$ with $\\tau=RC$. As $t\\to\\infty$, $Q\\to$",
         "$C\\varepsilon$",
         "The exponential dies; the capacitor becomes an open circuit at the battery voltage.",
         ["0", "$\\varepsilon/R$", "$\\varepsilon/C$"]),
        ("Charging current is $I=(\\varepsilon/R)e^{-t/\\tau}$. At $t=0^+$, $I$ equals",
         "$\\varepsilon/R$",
         "Uncharged capacitor acts like a wire at the first instant.",
         ["0", "$\\varepsilon C$", "$\\varepsilon/(RC)$"]),
        ("$R=2.0\\,\\mathrm{k}\\Omega$, $C=2.0\\,\\mu\\mathrm{F}$, $\\varepsilon=12\\,\\mathrm{V}$. The initial charging current is",
         "6.0 mA",
         "$I(0)=\\varepsilon/R=12/2000=6.0\\times10^{-3}\\,\\mathrm{A}$.",
         ["24 mA", "12 A", "0"]),
        ("After a long time on that same charging circuit, the current is",
         "0",
         "Open-circuit capacitor, $I=0$, $Q=C\\varepsilon=24\\,\\mu\\mathrm{C}$.",
         ["6.0 mA", "12 A", "infinite"]),
        ("Discharging: $Q(0)=Q_0$, no battery. The DE is $R\\dot Q+Q/C=0$, so $Q(t)=$",
         "$Q_0 e^{-t/RC}$",
         "Separable: $dQ/Q=-dt/RC$.",
         ["$Q_0(1-e^{-t/RC})$", "$Q_0 t/RC$", "0 immediately"]),
        ("Discharging current has magnitude $(Q_0/\\tau)e^{-t/\\tau}$ and",
         "leaves the positive plate through $R$",
         "$I=-\\dot Q$ if $Q$ is the positive-plate charge falling.",
         ["charges the capacitor further", "is constant", "is $\\varepsilon/R$ forever"]),
        ("$Q_0=24\\,\\mu\\mathrm{C}$, $C=2.0\\,\\mu\\mathrm{F}$, $R=2.0\\,\\mathrm{k}\\Omega$. Initial discharge current magnitude is",
         "6.0 mA",
         "$V_0=Q_0/C=12\\,\\mathrm{V}$, $I(0)=V_0/R=6.0\\,\\mathrm{mA}$.",
         ["12 mA", "0", "24 A"]),
        ("During discharge, $Q$ and $I$ both",
         "decay exponentially with the same $\\tau=RC$",
         "$I\\propto Q$ because $I=V/R=Q/(RC)$.",
         ["stay constant", "grow linearly", "oscillate"]),
        ("After many time constants of discharge, $Q$ is",
         "essentially 0",
         "Exponential decay to the empty capacitor.",
         ["$C\\varepsilon$", "$Q_0/2$ forever", "infinite"]),
        ("The time constant $\\tau=RC$. For $R=100\\,\\Omega$ and $C=50\\,\\mu\\mathrm{F}$, $\\tau=$",
         "$5.0\\times10^{-3}\\,\\mathrm{s}$",
         "$(100)(50\\times10^{-6})=5.0\\times10^{-3}\\,\\mathrm{s}$.",
         ["$5.0\\,\\mathrm{s}$", "$2.0\\times10^{-3}\\,\\mathrm{s}$", "$0.50\\,\\mathrm{s}$"]),
        ("At $t=\\tau$ while charging from $0$, $Q/C\\varepsilon=$",
         "$1-e^{-1}\\approx 0.632$",
         "Standard charging fraction.",
         ["$e^{-1}\\approx 0.368$", "1", "0.5 exactly"]),
        ("At $t=\\tau$ while discharging, $Q/Q_0=$",
         "$e^{-1}\\approx 0.368$",
         "Standard decay fraction.",
         ["$0.632$", "1", "0"]),
        ("Doubling both $R$ and $C$ multiplies $\\tau$ by",
         "4",
         "$\\tau=RC$.",
         ["2", "1", "1/2"]),
        ("Larger $\\tau$ means the exponential",
         "changes more slowly",
         "The system takes longer to approach its final values.",
         ["reaches final $Q$ sooner", "oscillates", "has larger final $I$"]),
        ("On a charging $Q(t)$ graph, the curve is",
         "increasing, concave down, approaching $C\\varepsilon$",
         "$1-e^{-t/\\tau}$ shape.",
         ["a straight line through the origin", "a decaying exponential to 0", "a sinusoid"]),
        ("On a charging $I(t)$ graph, the curve is",
         "a decaying exponential from $\\varepsilon/R$ to 0",
         "$I=(\\varepsilon/R)e^{-t/\\tau}$.",
         ["increasing to $\\varepsilon/R$", "constant", "a sinusoid"]),
        ("On a discharging $Q(t)$ graph, the curve is",
         "a decaying exponential from $Q_0$ to 0",
         "$Q_0 e^{-t/\\tau}$.",
         ["$1-e^{-t/\\tau}$", "a straight line", "constant $Q_0$"]),
        ("The initial slope of charging $Q(t)$ is $I(0)=\\varepsilon/R$, so $dQ/dt|_{0}=$",
         "$\\varepsilon/R$",
         "Matches the uncharged-capacitor-as-wire picture.",
         ["0", "$C\\varepsilon$", "$\\varepsilon C/R^2$"]),
        ("If you plot $\\ln(Q/Q_0)$ versus $t$ for discharge, the slope is",
         "$-1/\\tau$",
         "$\\ln(Q/Q_0)=-t/\\tau$.",
         ["$+\\tau$", "$-\\tau$", "$RC$"]),
        ("Energy stored on the capacitor is $U=Q^2/(2C)$. While charging, $U$ approaches",
         "$\\tfrac12 C\\varepsilon^2$",
         "Final $Q=C\\varepsilon$.",
         ["$C\\varepsilon^2$", "0", "$\\varepsilon^2/R$"]),
        ("The battery supplies $\\int\\varepsilon I\\,dt=C\\varepsilon^2$ to charge from $0$ to $C\\varepsilon$, but $U_C$ is only $\\tfrac12 C\\varepsilon^2$. The other half",
         "is dissipated as heat in $R$",
         "Independent of the value of $R$ (for this DC charging story).",
         ["returns to the battery", "is stored in $L$", "vanishes from energy conservation"]),
        ("During discharge, capacitor energy ends up",
         "as thermal energy in $R$",
         "$U(0)=Q_0^2/(2C)$ becomes $\\int I^2 R\\,dt$.",
         ["back in a battery that is not present", "as magnetic energy only", "unchanged on $C$"]),
        ("Instantaneous resistor power while charging is $P=I^2 R$ with $I=(\\varepsilon/R)e^{-t/\\tau}$, which equals",
         "$(\\varepsilon^2/R)e^{-2t/\\tau}$",
         "Square the exponential: $e^{-2t/\\tau}$.",
         ["$(\\varepsilon^2/R)e^{-t/\\tau}$", "$\\tfrac12 C\\varepsilon^2$", "0 always"]),
        ("Comparing $U_C(t)$ and energy already dissipated in $R$ during charging, at every $t$ they",
         "sum to the energy so far delivered by the battery $\\varepsilon Q(t)$",
         "Loop energy accounting.",
         ["are each $\\tfrac12 C\\varepsilon^2$", "are equal to each other at all $t$", "ignore the battery"]),
        ("In a multi-loop circuit with capacitors, after a long time capacitors behave as",
         "open circuits ($I_C=0$)",
         "DC steady state: $\\dot Q=0$.",
         ["shorts ($V_C=0$)", "batteries", "inductors"]),
        ("At $t=0^+$ after a switch closes onto uncharged capacitors, those capacitors behave as",
         "shorts ($V_C=0$)",
         "$Q=0\\Rightarrow V=Q/C=0$.",
         ["open circuits", "resistors of value $R$", "emf sources of $\\varepsilon$"]),
        ("Two capacitors in series with a battery, long-time DC: the equivalent $C$ is the series combo, and the charges are",
         "equal in magnitude",
         "Same as electrostatic series capacitors.",
         ["split like parallel currents", "zero", "proportional to $1/C^2$"]),
        ("A capacitor that was already charged to $\\varepsilon$ sits in a branch that a switch then isolates. After isolation, $Q$",
         "stays at $C\\varepsilon$ (no path to change $Q$)",
         "Open switch: $I=0=\\dot Q$.",
         ["drops to 0 instantly", "grows without bound", "oscillates"]),
        ("Kirchhoff with capacitors: each capacitor contributes a term",
         "$Q/C$ (with a sign from your loop direction)",
         "Replace $IR$ with $Q/C$ on that element; still $\\sum\\Delta V=0$.",
         ["$L dI/dt$ only", "$\\varepsilon$ only", "0 always"]),
        ("$\\tau=RC$ for $R=4.0\\times10^{3}\\,\\Omega$, $C=1.0\\,\\mu\\mathrm{F}$ is",
         "$4.0\\times10^{-3}\\,\\mathrm{s}$",
         "$(4000)(1.0\\times10^{-6})=4.0\\times10^{-3}$.",
         ["$4.0\\,\\mathrm{s}$", "$4.0\\times10^{-6}\\,\\mathrm{s}$", "$250\\,\\mathrm{s}$"]),
        ("Charging, $t=2\\tau$. $Q/C\\varepsilon=1-e^{-2}\\approx$",
         "0.865",
         "$e^{-2}\\approx 0.135$.",
         ["0.135", "0.632", "1.00"]),
        ("Discharging, $t=2\\tau$. $Q/Q_0\\approx$",
         "0.135",
         "$e^{-2}\\approx 0.135$.",
         ["0.865", "0.632", "0.5"]),
        ("If $C$ is doubled at fixed $R$, the initial charging current $\\varepsilon/R$",
         "is unchanged",
         "Uncharged $C$ still looks like a wire; $C$ does not appear in $I(0)$.",
         ["doubles", "halves", "becomes zero"]),
        ("The time to reach $50\\%$ of final charge while charging satisfies $1-e^{-t/\\tau}=1/2$, so $t=$",
         "$\\tau\\ln 2$",
         "$e^{-t/\\tau}=1/2$.",
         ["$\\tau/2$", "$\\tau$", "$2\\tau$"]),
        ("Connecting an extra identical $C$ in parallel with the original (battery still attached, long time) makes final $Q_{\\mathrm{total}}$",
         "double",
         "$C_{\\mathrm{eq}}\\times 2$, $V=\\varepsilon$ still.",
         ["halve", "stay the same", "go to zero"]),
        ("The units of $RC$ are seconds because $\\Omega\\cdot\\mathrm{F}=$",
         "s",
         "Dimensional check for $\\tau$.",
         ["A", "V", "C"]),
        ("A graph of charging $V_C(t)$ has the same shape as",
         "$Q(t)$, because $V=Q/C$",
         "Just a vertical scale change.",
         ["$I(t)$", "a decaying exponential from $\\varepsilon$", "a straight line"]),
        ("A graph of discharging $V_C(t)$ has the same shape as",
         "discharging $Q(t)$",
         "Again $V=Q/C$.",
         ["charging $I(t)$ from a battery that is gone", "a rising $1-e^{-t/\\tau}$", "constant $\\varepsilon$"]),
        ("If $R\\to 0$ with a physical battery, charging would be",
         "arbitrarily fast ($\\tau\\to 0$), limited in real life by other $R$ and inductance",
         "Idealization.",
         ["impossible because $C$ forbids it", "slower", "oscillatory with $\\omega=R/L$"]),
        ("Energy dissipated in $R$ to fully charge from 0 is",
         "$\\tfrac12 C\\varepsilon^2$",
         "Battery input $C\\varepsilon^2$, stored $\\tfrac12 C\\varepsilon^2$.",
         ["$C\\varepsilon^2$", "0", "$\\varepsilon^2/R$"]),
        ("At $t=\\tau$ charging, $U_C/(\\tfrac12 C\\varepsilon^2)=(1-e^{-1})^2\\approx$",
         "0.40",
         "$(0.632)^2\\approx 0.40$.",
         ["0.632", "0.368", "1"]),
        ("A series $R$ with two parallel capacitors each $C$ (battery $\\varepsilon$). Equivalent $C$ for $\\tau$ is",
         "$2C$",
         "Parallel add, then $\\tau=R(2C)$.",
         ["$C/2$", "$C$", "$R$"]),
        ("A series $R$ with two series capacitors each $C$. $\\tau=$",
         "$R(C/2)$",
         "Series $C_{\\mathrm{eq}}=C/2$.",
         ["$2RC$", "$RC$", "$R/C$"]),
        ("Long-time voltage across $R$ in a charging series $RC$ is",
         "0",
         "$I=0$.",
         ["$\\varepsilon$", "$\\varepsilon/2$", "infinite"]),
        ("Long-time voltage across $C$ in that charging series $RC$ is",
         "$\\varepsilon$",
         "Capacitor holds the battery voltage.",
         ["0", "$IR$", "$\\varepsilon/R$"]),
        ("AP Stretch: Capacitor $C=4.0\\,\\mu\\mathrm{F}$ already holds $Q(0)=12\\,\\mu\\mathrm{C}$. At $t=0$ it is switched onto $\\varepsilon=9.0\\,\\mathrm{V}$ through $R=5.0\\,\\mathrm{k}\\Omega$ (same polarity). Solving $R\\dot Q+Q/C=\\varepsilon$ gives $Q(t)=C\\varepsilon+(Q(0)-C\\varepsilon)e^{-t/RC}$. The charge at $t=\\tau=RC$ is",
         "$27.2\\,\\mu\\mathrm{C}$",
         "$C\\varepsilon=36\\,\\mu\\mathrm{C}$, $\\tau=20\\,\\mathrm{ms}$. $Q(\\tau)=36-24/e\\approx 27.2\\,\\mu\\mathrm{C}$.",
         ["$36\\,\\mu\\mathrm{C}$", "$12\\,\\mu\\mathrm{C}$", "$24\\,\\mu\\mathrm{C}$"]),
        ("AP Stretch: $Q(t)=C\\varepsilon(1-e^{-t/\\tau})$. The time when $I=I(0)/e^2$ is",
         "$2\\tau$",
         "$I=I(0)e^{-t/\\tau}=I(0)e^{-2}$ at $t=2\\tau$.",
         ["$\\tau/2$", "$\\tau$", "$e^2\\tau$"]),
        ("AP Stretch: Charge $C=6.0\\,\\mu\\mathrm{F}$ through $R=1.0\\,\\mathrm{k}\\Omega$ from $\\varepsilon=8.0\\,\\mathrm{V}$ with $Q(0)=0$. Energy stored on $C$ at $t=3.0\\,\\mathrm{ms}$ is",
         "$2.97\\times10^{-5}\\,\\mathrm{J}$",
         "$\\tau=6.0\\,\\mathrm{ms}$ so $t=\\tau/2$. $Q=C\\varepsilon(1-e^{-1/2})\\approx 18.9\\,\\mu\\mathrm{C}$, then $U=Q^2/(2C)\\approx 2.97\\times10^{-5}\\,\\mathrm{J}$.",
         ["$1.92\\times10^{-4}\\,\\mathrm{J}$", "$9.60\\times10^{-5}\\,\\mathrm{J}$", "0"]),
        ("AP Stretch: Two-loop: left branch is $\\varepsilon=18\\,\\mathrm{V}$ in series with $R_1=3.0\\,\\Omega$; right branch is only $R_2=6.0\\,\\Omega$; shared middle branch is uncharged $C=2.0\\,\\mu\\mathrm{F}$. Switch closes at $t=0$. At $t=0^+$, the current through $R_1$ is",
         "6.0 A",
         "Uncharged $C$ is a wire, so $R_2$ is shorted. $I_{R_1}=\\varepsilon/R_1=18/3=6.0\\,\\mathrm{A}$.",
         ["2.0 A", "3.0 A", "0"]),
        ("AP Stretch: Two-loop: left $\\varepsilon=18\\,\\mathrm{V}$ with $R_1=3.0\\,\\Omega$, right $R_2=6.0\\,\\Omega$, shared uncharged $C=2.0\\,\\mu\\mathrm{F}$. Switch closes at $t=0$. As $t\\to\\infty$, the charge on $C$ is",
         "$24\\,\\mu\\mathrm{C}$",
         "$C$ is open, so $I=18/(3+6)=2.0\\,\\mathrm{A}$. Then $V_C=I R_2=12\\,\\mathrm{V}$ and $Q=CV_C=24\\,\\mu\\mathrm{C}$.",
         ["$36\\,\\mu\\mathrm{C}$", "$12\\,\\mu\\mathrm{C}$", "0"]),
        ("AP Stretch: The integrating-factor solution with $Q(0)=Q_i$ and a battery $\\varepsilon$ is $Q(t)=C\\varepsilon+(Q_i-C\\varepsilon)e^{-t/\\tau}$. If $Q_i=C\\varepsilon$, then $Q(t)$ is",
         "constant $C\\varepsilon$",
         "Already at equilibrium; no transient.",
         ["$0$", "$2C\\varepsilon e^{-t/\\tau}$", "undefined"]),
        ("AP Stretch: Capacitors $12\\,\\mu\\mathrm{F}$ and $4.0\\,\\mu\\mathrm{F}$ in series, then that pair in series with $R=5.0\\,\\mathrm{k}\\Omega$ and a battery. The charging time constant is",
         "$15\\,\\mathrm{ms}$",
         "$C_{\\mathrm{eq}}=3.0\\,\\mu\\mathrm{F}$, $\\tau=R C_{\\mathrm{eq}}=(5000)(3.0\\times10^{-6})=1.5\\times10^{-2}\\,\\mathrm{s}$.",
         ["$80\\,\\mathrm{ms}$", "$20\\,\\mathrm{ms}$", "$5.0\\,\\mathrm{ms}$"]),
        ("AP Stretch: Two-loop with $\\varepsilon=18\\,\\mathrm{V}$, $R_1=3.0\\,\\Omega$, $R_2=6.0\\,\\Omega$, and $C=2.0\\,\\mu\\mathrm{F}$ in the shared branch. After a long time, energy stored in $C$ is",
         "$1.44\\times10^{-4}\\,\\mathrm{J}$",
         "$V_C=12\\,\\mathrm{V}$ as in the long-time divider, so $U=\\tfrac12 C V_C^2=\\tfrac12(2.0\\times10^{-6})(144)=1.44\\times10^{-4}\\,\\mathrm{J}$.",
         ["$2.88\\times10^{-4}\\,\\mathrm{J}$", "$3.24\\times10^{-4}\\,\\mathrm{J}$", "0"]),
        ("AP Stretch: A $2.0\\,\\mu\\mathrm{F}$ capacitor charged to $12\\,\\mathrm{V}$ then discharges through $R_1=3.0\\,\\Omega$ in parallel with $R_2=6.0\\,\\Omega$ (no battery). Current leaving $C$ at $t=\\tau$ is",
         "$2.21\\,\\mathrm{A}$",
         "$R_{\\mathrm{eq}}=2.0\\,\\Omega$, $\\tau=4.0\\,\\mu\\mathrm{s}$, $I(0)=12/2=6.0\\,\\mathrm{A}$, so $I(\\tau)=6.0/e\\approx 2.21\\,\\mathrm{A}$.",
         ["$6.0\\,\\mathrm{A}$", "$3.0\\,\\mathrm{A}$", "0"]),
    ])


def build_unit5():
    title = "AP Physics C E&M Unit 5: RC Circuits"
    description = (
        "Charging and discharging capacitors, the time constant $\\tau=RC$, exponential graphs, "
        "energy bookkeeping, and multi-loop circuits with $C$."
    )
    q_charge = sample_curve(lambda t: 1 - math.exp(-t), 0, 5)
    i_charge = sample_curve(lambda t: math.exp(-t), 0, 5)
    q_dis = sample_curve(lambda t: math.exp(-t), 0, 5)

    ican1 = [
        "I can write the charging DE $R\\dot Q+Q/C=\\varepsilon$ and $Q=C\\varepsilon(1-e^{-t/\\tau})$.",
        "I can evaluate $I(0)=\\varepsilon/R$ and $Q(\\infty)=C\\varepsilon$.",
        "I can compute $\\tau=RC$ and $Q=C\\varepsilon$ numerically.",
    ]
    c1 = concept_block(
        "1. Charging a capacitor",
        [
            "A series loop with battery $\\varepsilon$, resistor $R$, and capacitor $C$ is the prototype RC circuit. Charge $Q$ on the capacitor and current $I=dQ/dt$ are the unknowns.",
            "Kirchhoff around the loop: $\\varepsilon-IR-Q/C=0$. Substituting $I=\\dot Q$ yields the first-order DE $R\\dot Q+Q/C=\\varepsilon$.",
            "With $Q(0)=0$, the solution is $Q(t)=C\\varepsilon\\bigl(1-e^{-t/\\tau}\\bigr)$ where the time constant is $\\tau=RC$. Current is $I(t)=(\\varepsilon/R)e^{-t/\\tau}$.",
            "At the instant the switch closes, $Q=0$ so $V_C=0$: the capacitor behaves like a wire and $I=\\varepsilon/R$. After a long time, $I=0$ and $Q=C\\varepsilon$: the capacitor behaves like an open circuit.",
            "Numeric: $R=2.0\\,\\mathrm{k}\\Omega$, $C=2.0\\,\\mu\\mathrm{F}$, $\\varepsilon=12\\,\\mathrm{V}$ give $\\tau=4.0\\,\\mathrm{ms}$, $I(0)=6.0\\,\\mathrm{mA}$, $Q(\\infty)=24\\,\\mu\\mathrm{C}$.",
            "The DE is the same pattern as other linear first-order equations: an exponential transient plus a constant particular solution $Q=C\\varepsilon$.",
        ],
        "Every later transient (RL, and the envelope of damped LC) uses this same 'time constant plus exponential' language. Charging is also how $\\tfrac12 C\\varepsilon^2$ gets stored.",
        "Write KVL with $Q/C$ and $IR$. Replace $I$ by $\\dot Q$. Identify $\\tau=RC$. Apply $Q(0)$ to fix the constant. Then $I=\\dot Q$.",
        lesson_figure(
            _rc_svg() + xy_graph(
                curves=[("#b91c1c", q_charge)],
                xlim=(0, 5), ylim=(0, 1.2), w=300, h=180, xlab="t/τ", ylab="Q/(Cε)",
            ),
            "Series RC and charging $Q(t)$",
            "The curve is $1-e^{-t/\\tau}$, approaching $C\\varepsilon$ with decreasing slope $I(t)$.",
        )
        + solved(1, "$R=2.0\\,\\mathrm{k}\\Omega$, $C=2.0\\,\\mu\\mathrm{F}$, $\\varepsilon=12\\,\\mathrm{V}$. Find $\\tau$ and $I(0)$.",
                 ["$\\tau=RC=(2000)(2.0\\times10^{-6})=4.0\\times10^{-3}\\,\\mathrm{s}$.",
                  "At $t=0$, $Q=0$ so $V_C=0$.",
                  "$I(0)=\\varepsilon/R=12/2000=6.0\\,\\mathrm{mA}$."],
                 "$\\tau=4.0\\,\\mathrm{ms}$, $I(0)=6.0\\,\\mathrm{mA}$", "", "Easy")
        + solved(2, "For that circuit, find $Q(\\infty)$ and $I(\\infty)$.",
                 ["After a long time the exponential is gone.",
                  "$Q\\to C\\varepsilon=(2.0\\times10^{-6})(12)=24\\,\\mu\\mathrm{C}$.",
                  "$I\\to 0$ (open capacitor)."],
                 "$24\\,\\mu\\mathrm{C}$, $I=0$", "", "Medium")
        + solved(3, "Write the DE and verify that $Q=C\\varepsilon(1-e^{-t/RC})$ satisfies $Q(0)=0$ and the DE.",
                 ["$Q(0)=C\\varepsilon(1-1)=0$.",
                  "$\\dot Q=(\\varepsilon/R)e^{-t/RC}$.",
                  "$R\\dot Q+Q/C=\\varepsilon e^{-t/RC}+\\varepsilon(1-e^{-t/RC})=\\varepsilon$."],
                 "solution checks", "", "Hard")
        + _ican(ican1),
        ("Using $Q=C\\varepsilon e^{-t/\\tau}$ for charging",
         "That exponential-to-zero is discharge (or charging current). Charging charge is $C\\varepsilon(1-e^{-t/\\tau})$."),
        ("Instant vs long-time cartoons",
         "At $t=0^+$, replace uncharged $C$ by a wire. After a long time, delete that branch (open). Solve the remaining resistor circuit each time."),
        ican1,
        1,
    )

    ican2 = [
        "I can write $Q=Q_0 e^{-t/RC}$ for discharge.",
        "I can find $I(0)=V_0/R=Q_0/(RC)$.",
        "I can state that both $Q$ and $I$ share $\\tau=RC$.",
    ]
    c2 = concept_block(
        "2. Discharging",
        [
            "Disconnect the battery and let the capacitor drain through $R$. Kirchhoff: $-IR-Q/C=0$, or $R\\dot Q+Q/C=0$.",
            "Separate variables: $dQ/Q=-dt/RC$. Integrate from $Q_0$ at $t=0$ to $Q(t)$: $Q(t)=Q_0 e^{-t/RC}$.",
            "Current magnitude is $|I|=(Q_0/\\tau)e^{-t/\\tau}= (V_0/R)e^{-t/\\tau}$. Charge and current decay together.",
            "Example: $Q_0=24\\,\\mu\\mathrm{C}$, $C=2.0\\,\\mu\\mathrm{F}$ so $V_0=12\\,\\mathrm{V}$, $R=2.0\\,\\mathrm{k}\\Omega$, $I(0)=6.0\\,\\mathrm{mA}$, same $\\tau=4.0\\,\\mathrm{ms}$.",
            "After one time constant, $Q=0.368\\,Q_0$. After two, about $0.135\\,Q_0$. After many $\\tau$, the capacitor is empty.",
            "There is no minus-sign mystery if you define $I=-\\dot Q$ when $Q$ is the decaying positive-plate charge: current leaves the positive plate through $R$.",
        ],
        "Discharge is the cleanest exponential on the exam. It is also the energy dump $Q_0^2/(2C)\\to$ heat in $R$.",
        "No battery $\\Rightarrow$ DE is homogeneous. $Q(0)=Q_0$ fixes $A$. Then $I=V/R=Q/(RC)$.",
        lesson_figure(
            xy_graph(
                curves=[("#1d4ed8", q_dis)],
                xlim=(0, 5), ylim=(0, 1.2), w=300, h=180, xlab="t/τ", ylab="Q/Q₀",
            ),
            "Discharging $Q(t)$",
            "Pure exponential decay $e^{-t/\\tau}$. At $t=\\tau$ the height is about $0.37\\,Q_0$.",
        )
        + solved(1, "A capacitor with $Q_0=24\\,\\mu\\mathrm{C}$ and $C=2.0\\,\\mu\\mathrm{F}$ discharges through $2.0\\,\\mathrm{k}\\Omega$. Find $V_0$ and $I(0)$.",
                 ["$V_0=Q_0/C=12\\,\\mathrm{V}$.",
                  "$I(0)=V_0/R=12/2000=6.0\\,\\mathrm{mA}$.",
                  "Direction: from the $+$ plate through $R$ to the $-$ plate."],
                 "$12\\,\\mathrm{V}$, $6.0\\,\\mathrm{mA}$", "", "Easy")
        + solved(2, "Write $Q(t)$ and evaluate $Q(\\tau)/Q_0$.",
                 ["$Q=Q_0 e^{-t/\\tau}$.",
                  "At $t=\\tau$, $Q=Q_0 e^{-1}$.",
                  "$e^{-1}\\approx 0.368$."],
                 "$0.368\\,Q_0$", "", "Medium")
        + solved(3, "Show $\\int I^2 R\\,dt$ from $0$ to $\\infty$ equals $Q_0^2/(2C)$.",
                 ["$I=(Q_0/\\tau)e^{-t/\\tau}$, $\\tau=RC$.",
                  "$\\int_0^\\infty I^2 R\\,dt=(Q_0^2 R/\\tau^2)\\int e^{-2t/\\tau}dt=(Q_0^2 R/\\tau^2)(\\tau/2)$.",
                  "$R/\\tau=1/C$, so the integral is $Q_0^2/(2C)$."],
                 "all stored $U$ becomes heat", "", "Hard")
        + _ican(ican2),
        ("Using $1-e^{-t/\\tau}$ for discharge",
         "That rising curve is charging $Q$ or charging $V_C$. Discharge falls from $Q_0$ toward zero."),
        ("$V=Q/C$ still holds during the transient",
         "At every instant the capacitor is in quasistatic electrostatics. Ohm's law on $R$ uses that instantaneous $V$."),
        ican2,
        6,
    )

    ican3 = [
        "I can compute $\\tau=RC$ and convert $\\Omega\\cdot\\mathrm{F}$ to seconds.",
        "I can use $1-e^{-1}\\approx 0.632$ and $e^{-1}\\approx 0.368$.",
        "I can find $t=\\tau\\ln 2$ for half of the remaining gap.",
    ]
    c3 = concept_block(
        "3. Time constant",
        [
            "The time constant $\\tau=RC$ is the only time scale in series RC. After one $\\tau$, a charging capacitor has gained about $63\\%$ of its final charge; a discharging capacitor has $37\\%$ left.",
            "Units: ohm times farad is second. Check: $R=100\\,\\Omega$, $C=50\\,\\mu\\mathrm{F}$, $\\tau=5.0\\,\\mathrm{ms}$.",
            "Doubling $R$ or $C$ doubles $\\tau$. Doubling both multiplies $\\tau$ by four. Larger $\\tau$ means a slower exponential.",
            "Half-filling the remaining gap always takes $\\tau\\ln 2\\approx 0.69\\tau$. That is not $\\tau/2$.",
            "Initial charging current $\\varepsilon/R$ does not depend on $C$, but the time that current lasts does: bigger $C$ means bigger $\\tau$.",
            "When several capacitors combine, first find $C_{\\mathrm{eq}}$, then $\\tau=R C_{\\mathrm{eq}}$ (if there is a single $R$ in series with that equivalent).",
        ],
        "AP multiple choice loves $\\tau=RC$ arithmetic and the $63\\%/37\\%$ numbers. FRQs ask you to read $\\tau$ from a graph as the time to $0.63$ of final $V$.",
        "Compute $RC$ in SI (ohms and farads). Mark $t=\\tau$ on any sketch. For 'how long to half', solve the exponential, do not guess $\\tau/2$.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", q_charge)],
                dashes=[("v", 1, "t=τ")],
                xlim=(0, 5), ylim=(0, 1.2), w=300, h=180, xlab="t/τ", ylab="Q/(Cε)",
            ),
            "Charging curve with $t=\\tau$ marked",
            "Height at $t=\\tau$ is $1-e^{-1}\\approx 0.63$ of the plateau.",
        )
        + solved(1, "$R=100\\,\\Omega$, $C=50\\,\\mu\\mathrm{F}$. Find $\\tau$.",
                 ["$\\tau=RC$.",
                  "$(100)(50\\times10^{-6})=5.0\\times10^{-3}$.",
                  "Unit: seconds."],
                 "$5.0\\,\\mathrm{ms}$", "", "Easy")
        + solved(2, "Charging from 0. What fraction of $C\\varepsilon$ is on $C$ at $t=\\tau$? At $t=2\\tau$?",
                 ["$1-e^{-1}\\approx 0.632$.",
                  "$1-e^{-2}\\approx 0.865$.",
                  "Not $50\\%$ at $t=\\tau/2$."],
                 "$0.632$ and $0.865$", "", "Medium")
        + solved(3, "Time to reach half the final charge while charging: solve $1-e^{-t/\\tau}=1/2$.",
                 ["$e^{-t/\\tau}=1/2$.",
                  "$-t/\\tau=\\ln(1/2)=-\\ln 2$.",
                  "$t=\\tau\\ln 2\\approx 0.693\\tau$."],
                 "$t=\\tau\\ln 2$", "", "Hard")
        + _ican(ican3),
        ("Calling $t=\\tau/2$ the half-charge time",
         "Exponentials are not linear. Half of the remaining difference always takes $\\ln 2$ times $\\tau$, measured from that moment."),
        ("SI units before multiplying",
         "Convert $\\mathrm{k}\\Omega$ to $10^3\\,\\Omega$ and $\\mu\\mathrm{F}$ to $10^{-6}\\,\\mathrm{F}$. Then $RC$ lands in seconds, not a mystery number."),
        ican3,
        11,
    )

    ican4 = [
        "I can sketch charging $Q$ as $1-e^{-t/\\tau}$ and $I$ as a decaying exponential.",
        "I can sketch discharging $Q$ and $I$ as decaying exponentials.",
        "I can read $\\tau$ from a graph using $63\\%$ or a log plot.",
    ]
    c4 = concept_block(
        "4. Qualitative graphs",
        [
            "Charging $Q(t)$ and $V_C(t)$: start at 0, steepest at $t=0$, flatten toward a horizontal asymptote $C\\varepsilon$ or $\\varepsilon$. Shape $1-e^{-t/\\tau}$.",
            "Charging $I(t)$ and $V_R(t)$: start at $\\varepsilon/R$ or $\\varepsilon$, decay exponentially to 0. Shape $e^{-t/\\tau}$.",
            "Discharging $Q$, $V_C$, $|I|$, $V_R$: all decay exponentially from their initial values to 0, same $\\tau$.",
            "A $\\ln Q$ versus $t$ plot for discharge is a straight line with slope $-1/\\tau$. That is how you extract $\\tau$ from data.",
            "Never draw a triangle or a straight line through the origin for $Q(t)$ unless the problem has forced a constant current (not a simple $R$).",
            "At $t=0$ the charging $Q$ graph is tangent to the line $Q=(\\varepsilon/R)t$. That tangent is a useful sketching check.",
        ],
        "AP loves 'which graph' items. If you mix up $1-e^{-t/\\tau}$ with $e^{-t/\\tau}$, you lose the set.",
        "Ask: is this a quantity that starts at 0 and fills, or one that starts high and dies? Fillers are $1-e^{-}$; dyers are $e^{-}$.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", q_charge), ("#1d4ed8", i_charge)],
                xlim=(0, 5), ylim=(0, 1.2), w=300, h=180, xlab="t/τ", ylab="normalized",
            ),
            "Charging: $Q$ (red) rises, $I$ (blue) falls",
            "Both share $\\tau$. The current is the slope of the charge curve.",
        )
        + solved(1, "Which charging graph starts at 0 and approaches a positive constant: $Q$ or $I$?",
                 ["$Q$ starts at 0 and $\\to C\\varepsilon$.",
                  "$I$ starts at $\\varepsilon/R$ and $\\to 0$.",
                  "So $Q$ (and $V_C$) is the rising curve."],
                 "rising: $Q$ (and $V_C$)", "", "Easy")
        + solved(2, "How is charging $I(t)$ related to the slope of $Q(t)$?",
                 ["$I=dQ/dt$.",
                  "The $Q$ curve is steepest at $t=0$ and flattens.",
                  "That matches $I$ large then $\\to 0$."],
                 "$I$ is the slope of $Q$", "", "Medium")
        + solved(3, "Discharge data: $\\ln(Q/Q_0)$ versus $t$ is a line through the origin with slope $-200\\,\\mathrm{s^{-1}}$. Find $\\tau$ and, if $R=2.0\\,\\mathrm{k}\\Omega$, find $C$.",
                 ["Slope $=-1/\\tau=-200$.",
                  "$\\tau=1/200=5.0\\times10^{-3}\\,\\mathrm{s}$.",
                  "$C=\\tau/R=(5.0\\times10^{-3})/2000=2.5\\,\\mu\\mathrm{F}$."],
                 "$\\tau=5.0\\,\\mathrm{ms}$, $C=2.5\\,\\mu\\mathrm{F}$", "", "Hard")
        + _ican(ican4),
        ("Drawing $Q(t)$ as a straight line to $C\\varepsilon$",
         "A constant slope would mean constant $I$, which would require $V_R$ constant while $V_C$ rises — that contradicts KVL with a fixed battery."),
        ("Match the vertical intercept to the physics",
         "If the intercept is 0, you are looking at charging $Q$ or $V_C$. If the intercept is $\\varepsilon/R$, you are looking at charging $I$."),
        ican4,
        16,
    )

    ican5 = [
        "I can compute $U=\\tfrac12 C\\varepsilon^2$ as the stored energy after charging.",
        "I can account for the matching $\\tfrac12 C\\varepsilon^2$ dissipated in $R$.",
        "I can track $U\\propto Q^2$ during discharge ($U=U_0 e^{-2t/\\tau}$).",
    ]
    c5 = concept_block(
        "5. Energy in RC",
        [
            "The capacitor stores $U=Q^2/(2C)=\\tfrac12 CV^2$. After a complete charge from 0 to $C\\varepsilon$, $U_C=\\tfrac12 C\\varepsilon^2$.",
            "The battery, however, supplied $\\int\\varepsilon I\\,dt=\\varepsilon Q_{\\mathrm{final}}=C\\varepsilon^2$. The extra $\\tfrac12 C\\varepsilon^2$ was dissipated as heat in $R$. Remarkably, that split does not depend on the value of $R$.",
            "During discharge there is no battery. All of $Q_0^2/(2C)$ becomes $\\int I^2 R\\,dt$ in the resistor.",
            "Because $U\\propto Q^2$ and $Q\\propto e^{-t/\\tau}$ on discharge, $U(t)=U_0 e^{-2t/\\tau}$. Energy decays twice as fast as charge.",
            "At $t=\\tau$ while charging, $Q\\approx 0.632\\,C\\varepsilon$ so $U_C$ is only about $40\\%$ of the final stored energy.",
            "Energy bars help: battery chemical energy $\\to$ capacitor PE $+$ resistor thermal. Never invent a third hidden reservoir without a name.",
        ],
        "Energy questions separate students who only memorize $Q(t)$ from students who can close an energy ledger. LC in Unit 8 swaps this $U_E$ with magnetic energy.",
        "Write three numbers: energy from the battery so far $\\varepsilon Q$, energy on $C$ equal to $Q^2/(2C)$, and the difference as heat. Check they add.",
        lesson_figure(
            energy_bars_svg(ke=0, pe=2, thermal=2),
            "After a full charge from a battery",
            "Equal bars of capacitor PE and resistor thermal, summing to the battery input $C\\varepsilon^2$.",
        )
        + solved(1, "$C=2.0\\,\\mu\\mathrm{F}$, $\\varepsilon=12\\,\\mathrm{V}$, charged fully from 0. Find $U_C$.",
                 ["$U=\\tfrac12 C\\varepsilon^2$.",
                  "$\\varepsilon^2=144$.",
                  "$U=\\tfrac12(2.0\\times10^{-6})(144)=1.44\\times10^{-4}\\,\\mathrm{J}$."],
                 "$1.44\\times10^{-4}\\,\\mathrm{J}$", "", "Easy")
        + solved(2, "How much energy did the battery supply, and how much became heat?",
                 ["Battery: $\\varepsilon Q=C\\varepsilon^2=2.88\\times10^{-4}\\,\\mathrm{J}$.",
                  "Stored: half of that.",
                  "Heat in $R$: the other half, $1.44\\times10^{-4}\\,\\mathrm{J}$."],
                 "battery $2.88\\times10^{-4}\\,\\mathrm{J}$; heat $1.44\\times10^{-4}\\,\\mathrm{J}$", "", "Medium")
        + solved(3, "On discharge, show $U(t)=U_0 e^{-2t/\\tau}$.",
                 ["$Q=Q_0 e^{-t/\\tau}$.",
                  "$U=Q^2/(2C)=[Q_0^2/(2C)]e^{-2t/\\tau}$.",
                  "The extra $2$ is from squaring the exponential."],
                 "$U=U_0 e^{-2t/\\tau}$", "", "Hard")
        + _ican(ican5),
        ("Claiming the battery supplied only $\\tfrac12 C\\varepsilon^2$",
         "The battery integral is $\\varepsilon Q=C\\varepsilon^2$. Half of that is stored; half is heat. Both halves matter on an FRQ ledger."),
        ("Square the exponential for energy",
         "If $Q$ has $e^{-t/\\tau}$, then $U\\propto Q^2$ has $e^{-2t/\\tau}$. Forgetting the $2$ is the usual energy-graph error."),
        ican5,
        21,
    )

    ican6 = [
        "I can replace uncharged $C$ by a wire at $t=0^+$ and by an open circuit after a long time.",
        "I can write $Q/C$ in KVL for multi-loop transients.",
        "I can find series/parallel $C_{\\mathrm{eq}}$ before computing $\\tau$.",
    ]
    c6 = concept_block(
        "6. Multi-loop with C",
        [
            "With several loops, Kirchhoff still holds: junctions for currents, loops for $\\Delta V$, and each capacitor contributes $Q/C$ (signed by your travel direction).",
            "Two snapshots solve most AP multi-loop capacitor problems without the full DE. At $t=0^+$, uncharged capacitors are wires ($V_C=0$). After a long time, capacitor branches carry zero current (open).",
            "If a capacitor is already charged and a switch isolates it, $Q$ stays put because $\\dot Q=0$ with no path.",
            "Series capacitors still share $|Q|$; parallel capacitors share $V$. Combine them into $C_{\\mathrm{eq}}$ before you talk about a single $\\tau=R C_{\\mathrm{eq}}$.",
            "Example: two equal $C$ in series with one $R$ have $\\tau=R(C/2)$. Two equal $C$ in parallel with one $R$ have $\\tau=R(2C)$.",
            "A capacitor in one branch of a two-loop resistor network, after a long time, simply removes that branch from the DC resistor problem.",
        ],
        "This is the FRQ skill: redraw the circuit twice (instant and long-time), solve two different resistor networks, then if needed write one DE for the in-between.",
        "Redraw. Label $t=0^+$ and $t\\to\\infty$ on two copies. Replace $C$ by a wire or an open as appropriate. Only then write numbers.",
        lesson_figure(
            _two_loop_c_svg(),
            "Two loops sharing a capacitor branch",
            "Each loop still obeys Kirchhoff: the capacitor contributes $Q/C$. After a long time $I_C=0$, so that branch drops out of the current network.",
        )
        + solved(1, "After a long time, how do capacitors behave in a DC circuit?",
                 ["$I_C=\\dot Q=0$.",
                  "No current through a capacitor branch.",
                  "Treat those branches as open circuits."],
                 "open circuits", "", "Easy")
        + solved(2, "Two identical $C$ in parallel, then that combo in series with $R$ and a battery. Find $\\tau$.",
                 ["Parallel: $C_{\\mathrm{eq}}=2C$.",
                  "Single time constant $\\tau=R C_{\\mathrm{eq}}$.",
                  "$\\tau=2RC$."],
                 "$\\tau=2RC$", "", "Medium")
        + solved(3, "Uncharged $C$ in one branch of a two-loop resistor circuit, switch closes at $t=0$. Why must you recompute all currents at $t=0^+$ rather than using the long-time currents?",
                 ["At $t=0^+$, $V_C=0$, so that branch is a short.",
                  "The resistor network is different from the long-time open-branch network.",
                  "Currents jump to the shorted-network values, then evolve toward the open-network values."],
                 "different networks at $0^+$ and $\\infty$", "", "Hard")
        + _ican(ican6),
        ("Using long-time currents at $t=0^+$",
         "Those two instants are different circuits. An uncharged capacitor is not an open circuit at the first instant."),
        ("Two redraws before any DE",
         "Most of the points are in the two resistor reductions. Write the DE only if the question asks for $Q(t)$ in between."),
        ican6,
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        ["Charging a capacitor", "Discharging", "Time constant",
         "Qualitative graphs", "Energy in RC", "Multi-loop with C"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Magnetic Fields
# ===========================================================================

def _u6_questions():
    return _pack([
        ("The magnetic force on a charge is $\\vec{F}=q\\vec{v}\\times\\vec{B}$. If $\\vec{v}\\parallel\\vec{B}$, $F$ is",
         "0",
         "$\\sin\\theta=0$.",
         ["$qvB$", "$qB/v$", "infinite"]),
        ("A proton with $v$ perpendicular to uniform $B$ moves in a circle of radius",
         "$mv/(qB)$",
         "$qvB=mv^2/r$.",
         ["$qB/(mv)$", "$mvq/B$", "$B/(mv)$"]),
        ("$q=2.0\\times10^{-6}\\,\\mathrm{C}$, $v=3.0\\times10^{5}\\,\\mathrm{m/s}$, $B=0.50\\,\\mathrm{T}$, $\\theta=90^\\circ$. $|F|=$",
         "0.30 N",
         "$qvB=(2.0\\times10^{-6})(3.0\\times10^{5})(0.50)=0.30\\,\\mathrm{N}$.",
         ["0.15 N", "3.0 N", "0"]),
        ("The force $\\vec{F}=q\\vec{v}\\times\\vec{B}$ does",
         "no work (always $\\perp\\vec{v}$)",
         "Magnetic forces change direction of $\\vec{v}$, not $K$, when $B$ is the only force.",
         ["positive work always", "negative work always", "$qvB$ joules per second always"]),
        ("Right-hand rule for $q>0$: fingers from $\\vec{v}$ toward $\\vec{B}$, thumb along",
         "$\\vec{F}$",
         "For $q<0$, reverse the thumb.",
         ["$-\\vec{F}$ always even for $q>0$", "$\\vec{v}$", "$\\vec{B}$"]),
        ("Force on a straight wire is $\\vec{F}=I\\vec{\\ell}\\times\\vec{B}$. For $I=2.0\\,\\mathrm{A}$, $\\ell=0.40\\,\\mathrm{m}$, $B=0.50\\,\\mathrm{T}$ perpendicular, $|F|=$",
         "0.40 N",
         "$ILB=(2)(0.40)(0.50)=0.40\\,\\mathrm{N}$.",
         ["0.10 N", "1.6 N", "0"]),
        ("If the wire is parallel to $\\vec{B}$, the magnetic force on the current is",
         "0",
         "$\\sin 0=0$.",
         ["$ILB$", "maximum", "attractive to the battery"]),
        ("Two parallel wires with currents in the same direction",
         "attract",
         "Each $B$ and $I\\times B$ points toward the other wire.",
         ["repel", "feel zero force", "rotate only"]),
        ("Opposite currents in parallel wires",
         "repel",
         "Forces reverse when one $I$ flips.",
         ["attract", "cancel $B$ everywhere", "produce no $F$"]),
        ("The ampere can be defined via the force per unit length between long parallel wires: $F/\\ell=\\mu_0 I_1 I_2/(2\\pi d)$. For $I_1=I_2=1\\,\\mathrm{A}$ and $d=1\\,\\mathrm{m}$, $F/\\ell=$",
         "$2.0\\times10^{-7}\\,\\mathrm{N/m}$",
         "$\\mu_0/(2\\pi)=2\\times10^{-7}$.",
         ["$4\\pi\\times10^{-7}\\,\\mathrm{N/m}$", "1 N/m", "0"]),
        ("Biot–Savart: $d\\vec{B}=(\\mu_0/4\\pi)\\,I\\,d\\vec{\\ell}\\times\\hat{r}/r^2$. $dB$ is zero when $d\\vec{\\ell}$ is",
         "parallel to $\\hat{r}$",
         "Cross product vanishes.",
         ["perpendicular to $\\hat{r}$", "equal to $I$", "at the field point"]),
        ("Qualitatively, a current element produces circles of $B$ around $d\\vec{\\ell}$ (right-hand thumb along $I$). A long straight wire therefore has $B$ in",
         "circles around the wire",
         "Same as the Ampere result.",
         ["radial spikes", "along the wire", "zero everywhere"]),
        ("Biot–Savart is the magnetic analog of",
         "Coulomb's law for a charge element (but with a cross product)",
         "Both are inverse-square element laws.",
         ["Gauss's law for $E$ in a conductor", "Ohm's law", "Faraday's law"]),
        ("At the center of a circular loop of radius $R$ carrying $I$, $B=$",
         "$\\mu_0 I/(2R)$",
         "Every $d\\ell$ is perpendicular to $\\hat{r}$ and equidistant.",
         ["$\\mu_0 I/(2\\pi R)$", "$\\mu_0 I/(4\\pi R)$", "0"]),
        ("Biot–Savart always works; Ampere's law is the efficient tool when",
         "symmetry makes $|B|$ constant on a loop so $B$ factors out of $\\oint\\vec{B}\\cdot d\\vec{\\ell}$",
         "Same philosophy as Gauss.",
         ["the current is tiny", "you refuse to use symmetry", "charges are static only"]),
        ("Ampere's law: $\\oint\\vec{B}\\cdot d\\vec{\\ell}=\\mu_0 I_{\\mathrm{enc}}$. For a long straight wire, a circle of radius $r$ gives $B=$",
         "$\\mu_0 I/(2\\pi r)$",
         "$B\\cdot 2\\pi r=\\mu_0 I$.",
         ["$\\mu_0 I/(2 r)$", "$\\mu_0 I/(4\\pi r^2)$", "0"]),
        ("$I=5.0\\,\\mathrm{A}$, $r=0.020\\,\\mathrm{m}$. Using $B=2.0\\times10^{-7} I/r$ (since $\\mu_0/(2\\pi)=2.0\\times10^{-7}$), $B=$",
         "$5.0\\times10^{-5}\\,\\mathrm{T}$",
         "$(2.0\\times10^{-7})(5.0)/0.020=5.0\\times10^{-5}\\,\\mathrm{T}$.",
         ["$1.0\\times10^{-4}\\,\\mathrm{T}$", "$2.0\\times10^{-6}\\,\\mathrm{T}$", "0"]),
        ("Inside a long solenoid, Ampere's law with a rectangular loop gives $B=$",
         "$\\mu_0 n I$",
         "$n$ is turns per unit length; outside $B\\approx 0$.",
         ["$\\mu_0 I/(2\\pi r)$", "$\\mu_0 I/(2R)$", "0 always"]),
        ("Ampere is always true (magnetostatics), but a random potato loop around a wire",
         "does not let you pull $B$ out as a constant",
         "Same warning as a cubic Gaussian surface.",
         ["violates Ampere", "gives $B=0$", "gives $E=\\sigma/\\varepsilon_0$"]),
        ("$I_{\\mathrm{enc}}$ is the current piercing any surface bounded by the Amperian loop, with sign from the right-hand rule. A current outside the loop contributes",
         "0 to $I_{\\mathrm{enc}}$",
         "It can still affect local $\\vec{B}$, but net $\\oint B\\cdot d\\ell$ ignores it.",
         ["$\\mu_0 I$", "twice $I$", "$-I$ always"]),
        ("Long solenoid, $n=1000\\,\\mathrm{m^{-1}}$, $I=2.0\\,\\mathrm{A}$. Interior $B=\\mu_0 n I=$",
         "$2.5\\times10^{-3}\\,\\mathrm{T}$",
         "$\\mu_0=4\\pi\\times10^{-7}$, $nI=2000$, $B=2.51\\times10^{-3}\\,\\mathrm{T}$.",
         ["$2.0\\times10^{-7}\\,\\mathrm{T}$", "$8.0\\times10^{-4}\\,\\mathrm{T}$", "0"]),
        ("Outside an ideal infinite solenoid, $B$ is",
         "0",
         "Ampere plus symmetry: no enclosed current for a loop outside.",
         ["$\\mu_0 n I$", "$\\mu_0 I/(2\\pi r)$", "infinite"]),
        ("A long wire's $B$ falls as",
         "$1/r$",
         "$\\mu_0 I/(2\\pi r)$.",
         ["$1/r^2$", "constant", "$r$"]),
        ("A toroid with $N$ turns and mean radius $r$ has $B=\\mu_0 N I/(2\\pi r)$ inside the core (ideal). This is Ampere on a",
         "circle inside the doughnut",
         "Enclosed current $NI$.",
         ["straight line along the axis", "Gaussian sphere", "pillbox"]),
        ("Superposition: $B$ of two long parallel wires is the vector sum. Midway between equal parallel currents in the same direction, $B$ is",
         "0",
         "Circles of $B$ are opposite there.",
         ["twice one wire", "infinite", "$\\mu_0 n I$"]),
        ("Torque on a magnetic dipole $\\vec{\\mu}=I\\vec{A}$ is $\\vec{\\tau}=\\vec{\\mu}\\times\\vec{B}$. Maximum torque is",
         "$\\mu B$ (when $\\vec{\\mu}\\perp\\vec{B}$)",
         "$\\sin 90^\\circ=1$.",
         ["0 always", "$\\mu/B$", "$IAB/2$ always"]),
        ("A single loop, $I=2.0\\,\\mathrm{A}$, $A=0.050\\,\\mathrm{m^2}$, $B=0.40\\,\\mathrm{T}$, $\\theta=90^\\circ$ between $\\hat{n}$ and $\\vec{B}$. $\\tau=$",
         "0.040 N·m",
         "$\\tau=IAB=(2)(0.050)(0.40)=0.040\\,\\mathrm{N\\cdot m}$.",
         ["0.016 N·m", "0", "2.5 N·m"]),
        ("Net force on a closed current loop in a uniform $\\vec{B}$ is",
         "0",
         "Analog of an electric dipole in uniform $E$: torque without net $F$.",
         ["$I\\ell B$", "$\\mu B$", "infinite"]),
        ("Potential energy $U=-\\vec{\\mu}\\cdot\\vec{B}$ is minimum when",
         "$\\vec{\\mu}$ is parallel to $\\vec{B}$",
         "Stable alignment.",
         ["antiparallel", "perpendicular", "undefined"]),
        ("$N$ turns multiply both $\\mu$ and $\\tau$ by",
         "$N$",
         "$\\mu=NIA$.",
         ["$1/N$", "$N^2$", "0"]),
        ("A negative charge with $\\vec{v}$ to the right and $\\vec{B}$ into the page feels $\\vec{F}$",
         "down the page (opposite the $+q$ rule)",
         "Reverse the right-hand-rule thumb.",
         ["up the page", "into the page", "to the right"]),
        ("Pitch of a helix: $v_\\parallel$ is unchanged by $B$. Period $T=2\\pi m/(qB)$ is independent of",
         "$v_\\perp$ (nonrelativistic)",
         "Cyclotron period.",
         ["$B$", "$q$", "$m$"]),
        ("A current-carrying rod on rails in uniform $B$ (motional later) still feels $I\\ell B$. Direction of $F$ is",
         "given by $I\\vec{\\ell}\\times\\vec{B}$",
         "Same wire force rule.",
         ["always toward increasing $B$", "along the current", "along $B$"]),
        ("If $B$ is in tesla, $I$ in amperes, $\\ell$ in meters, $F$ is in",
         "newtons",
         "SI consistency.",
         ["tesla", "weber", "volts"]),
        ("Ampere's law in magnetostatics assumes",
         "steady currents so $\\oint B\\cdot d\\ell=\\mu_0 I_{\\mathrm{enc}}$ with no displacement current",
         "Maxwell will add $\\mu_0\\varepsilon_0 d\\Phi_E/dt$ in Unit 8 when $E$ is changing.",
         ["changing $E$ is required", "no currents exist", "Gauss for magnetism failed"]),
        ("A coaxial cable: $I$ on the inner conductor, $-I$ on the outer sheath. Between them $B$ is",
         "$\\mu_0 I/(2\\pi r)$",
         "Enclosed current is $I$.",
         ["0", "$\\mu_0 n I$", "$2\\mu_0 I/r$"]),
        ("Outside the coaxial cable, $B$ is",
         "0",
         "$I_{\\mathrm{enc}}=I-I=0$.",
         ["$\\mu_0 I/(2\\pi r)$", "$\\mu_0 n I$", "infinite"]),
        ("Inside the wire of radius $R$ with uniform $J$, $B(r)=$",
         "$\\mu_0 I r/(2\\pi R^2)$",
         "$I_{\\mathrm{enc}}=I(r^2/R^2)$, then Ampere.",
         ["$\\mu_0 I/(2\\pi r)$", "0", "$\\mu_0 n I$"]),
        ("The magnetic field does not do work, so a charged particle's speed in a magnetic-only region",
         "stays constant",
         "$K$ conserved; direction can change.",
         ["increases steadily", "goes to 0", "goes to $c$"]),
        ("For $F=ILB$ to be valid, $I$ must be",
         "the current in a straight segment of length $\\ell$ in uniform $B$ (or use $I\\int d\\vec{\\ell}\\times\\vec{B}$ more generally)",
         "The integral form covers curves.",
         ["zero", "displacement current only", "the drift speed in m/s"]),
        ("A square loop, side $a$, current $I$, uniform $B$ in the plane of the loop. $\\tau=$",
         "$Ia^2 B$",
         "$\\mu=Ia^2$, $\\theta=90^\\circ$.",
         ["0 because $B$ is uniform? No, torque is nonzero", "$I a B$", "0 because net $F=0$ implies $\\tau=0$ (false)"]),
        ("The direction of $\\vec{\\mu}$ for a loop is the thumb of the right hand when fingers follow $I$. $\\vec{\\mu}$ is along",
         "the loop's area vector $\\vec{A}$",
         "Same sense.",
         ["the current around the rim only", "$-\\vec{B}$ always", "gravity"]),
        ("$B$ of a long wire at $r$ does not depend on a Gaussian sphere because",
         "magnetism uses Ampere loops, not electric Gauss surfaces, to find $B$",
         "Different symmetry tool.",
         ["Gauss for $E$ gives $B$", "there is no $B$", "$B$ is $\\sigma/\\varepsilon_0$"]),
        ("If you reverse $I$ in a solenoid, interior $\\vec{B}$",
         "reverses",
         "Linear in $I$.",
         ["stays the same", "becomes $E$", "vanishes only if $n$ is even"]),
        ("A particle with $v$ at $30^\\circ$ to $\\vec{B}$ has $v_\\perp=v/2$. Radius of the helix is",
         "$mv_\\perp/(qB)=mv/(2qB)$",
         "Use the perpendicular component.",
         ["$mv/(qB)$", "$2mv/(qB)$", "0"]),
        ("Units: $1\\,\\mathrm{T}=$",
         "$1\\,\\mathrm{N\\cdot s/(C\\cdot m)}$",
         "From $F=qvB$.",
         ["1 V", "1 Wb", "1 A"]),
        ("AP Stretch: Integrate Biot–Savart along an infinite wire: $\\int_{-\\infty}^{\\infty} R\\,dx/(x^2+R^2)^{3/2}=2/R$ yields $B=$",
         "$\\mu_0 I/(2\\pi R)$",
         "Agrees with Ampere.",
         ["$\\mu_0 I/(4\\pi R)$", "$\\mu_0 I/(2R)$", "0"]),
        ("AP Stretch: Finite wire from $\\theta_1$ to $\\theta_2$ (angles from the field point's perpendicular). $B=(\\mu_0 I/(4\\pi r))(\\sin\\theta_1+\\sin\\theta_2)$. For a semi-infinite wire $\\theta_1=0,\\theta_2=90^\\circ$, $B=$",
         "$\\mu_0 I/(4\\pi r)$",
         "Half of the usual extra-factor story versus infinite.",
         ["$\\mu_0 I/(2\\pi r)$", "0", "$\\mu_0 I/(2 r)$"]),
        ("AP Stretch: Uniform $B$ in $z$, particle $q,m$ with $\\vec{v}=v\\hat{x}$. The cyclotron angular frequency $\\omega=qB/m$ in $\\ddot x=\\omega \\dot y$ etc. comes from",
         "$\\vec{a}=(q/m)\\vec{v}\\times\\vec{B}$",
         "Linear ODE with constant coefficients.",
         ["$F=qE$", "Gauss", "Ohm"]),
        ("AP Stretch: Ampere–Maxwell will add displacement current. In magnetostatics we omit it because",
         "$\\partial\\vec{E}/\\partial t=0$",
         "Steady fields.",
         ["$\\varepsilon_0=0$", "there is no $E$ in the universe", "Biot–Savart failed"]),
        ("AP Stretch: Magnetic moment of a spinning uniformly charged disk (qualitative AP C) scales as",
         "$I A$ with $I=Q/T$ and $A$ an effective area — i.e. proportional to $Q\\omega R^2$",
         "Each ring is a current loop.",
         ["$Q/R$ only", "$\\sigma/\\varepsilon_0$", "0 because $B$ does no work"]),
        ("AP Stretch: Force between two parallel infinite sheets of surface current $K$ involves $B=\\mu_0 K/2$ on each side (analog of $\\sigma/2\\varepsilon_0$). The force per area is",
         "$\\mu_0 K_1 K_2/2$ in appropriate relative-direction conventions",
         "Sheet analog of $F/\\ell=\\mu_0 I_1 I_2/(2\\pi d)$ but independent of $d$.",
         ["0 always", "$K/\\varepsilon_0$", "$\\sigma_1\\sigma_2/(2\\varepsilon_0)$"]),
        ("AP Stretch: Long straight wire carries $I=8.0\\,\\mathrm{A}$. Ampere's law on a circle of radius $r=0.040\\,\\mathrm{m}$ gives $B=\\mu_0 I/(2\\pi r)=$",
         "$4.0\\times10^{-5}\\,\\mathrm{T}$",
         "$\\mu_0/(2\\pi)=2.0\\times10^{-7}$. Then $B=(2.0\\times10^{-7})(8.0)/0.040=4.0\\times10^{-5}\\,\\mathrm{T}$.",
         ["$2.0\\times10^{-6}\\,\\mathrm{T}$", "$\\mu_0 I/(4\\pi r)$", "0"]),
        ("AP Stretch: A rectangular Amperian loop for a solenoid must have one long side inside, where $B$ is parallel to $d\\vec{\\ell}$, and the outside plus ends contribute",
         "0 in the idealization $B_{\\mathrm{out}}=0$ and $B\\perp$ ends or $B=0$ there",
         "That is why $B\\ell=\\mu_0 (n\\ell) I$.",
         ["$B\\cdot 4\\pi r^2$", "$\\mu_0\\varepsilon_0 d\\Phi_E/dt$ only", "the full $2\\pi r B$"]),
        ("AP Stretch: Work by an external agent rotating a dipole $\\vec{\\mu}$ in uniform $B$ from $\\theta=0$ to $\\theta=180^\\circ$ is",
         "$2\\mu B$",
         "$\\Delta U=\\mu B-( -\\mu B)=2\\mu B$.",
         ["0", "$\\mu B$", "$-\\mu B$"]),
    ])


def build_unit6():
    title = "AP Physics C E&M Unit 6: Magnetic Fields"
    description = (
        "Lorentz force, force on a current, Biot–Savart, Ampere's law, solenoids and wires, "
        "and torque on a loop."
    )
    ican1 = [
        "I can compute $|F|=qvB\\sin\\theta$ and use the right-hand rule.",
        "I can find the cyclotron radius $r=mv/(qB)$.",
        "I can state that magnetic forces do no work.",
    ]
    c1 = concept_block(
        "1. Force on a moving charge",
        [
            "A charge in a magnetic field feels $\\vec{F}=q\\vec{v}\\times\\vec{B}$. The magnitude is $qvB\\sin\\theta$, and $\\vec{F}$ is perpendicular to both $\\vec{v}$ and $\\vec{B}$.",
            "If $\\vec{v}$ is parallel to $\\vec{B}$, $F=0$. If $\\vec{v}$ is perpendicular, $F$ is maximum and the path (when $B$ is uniform) is a circle of radius $r=mv/(qB)$.",
            "Numeric: $q=2.0\\,\\mu\\mathrm{C}$, $v=3.0\\times10^{5}\\,\\mathrm{m/s}$, $B=0.50\\,\\mathrm{T}$, $\\theta=90^\\circ$ gives $F=0.30\\,\\mathrm{N}$.",
            "Because $\\vec{F}\\perp\\vec{v}$, a magnetic force never does work. Kinetic energy is constant if magnetism is the only force; only the direction of $\\vec{v}$ changes.",
            "Right-hand rule for $q>0$: fingers from $\\vec{v}$ toward $\\vec{B}$, thumb along $\\vec{F}$. Reverse for negative charge.",
            "A velocity with both parallel and perpendicular pieces makes a helix: $v_\\parallel$ is constant, the perpendicular motion is circular at the cyclotron frequency $\\omega=qB/m$.",
        ],
        "This force is how motors, mass spectrometers, and later motional emf get started. It is not the electric force $q\\vec{E}$; both can act at once as the Lorentz force $q(\\vec{E}+\\vec{v}\\times\\vec{B})$.",
        "Write $F=qvB\\sin\\theta$ with $\\theta$ between $\\vec{v}$ and $\\vec{B}$. Sketch $\\times$ for $B$ into the page. Apply RHR, then reverse if $q<0$.",
        lesson_figure(
            _lorentz_svg(),
            "Right-hand rule in a uniform $B$ into the page",
            "A positive charge moving right feels $F$ up the page; it will curve, not speed up.",
        )
        + solved(1, "$q=2.0\\times10^{-6}\\,\\mathrm{C}$, $v=3.0\\times10^{5}\\,\\mathrm{m/s}$, $B=0.50\\,\\mathrm{T}$ perpendicular. Find $|F|$.",
                 ["$\\sin 90^\\circ=1$.",
                  "$qvB=(2.0\\times10^{-6})(3.0\\times10^{5})(0.50)$.",
                  "$F=0.30\\,\\mathrm{N}$."],
                 "$0.30\\,\\mathrm{N}$", "", "Easy")
        + solved(2, "Why does this force not change the particle's kinetic energy?",
                 ["$\\vec{F}\\perp\\vec{v}$ by the cross product.",
                  "Power $P=\\vec{F}\\cdot\\vec{v}=0$.",
                  "So $dK/dt=0$."],
                 "no work, $K$ constant", "", "Medium")
        + solved(3, "Uniform $B$, $v\\perp B$. Derive $r=mv/(qB)$.",
                 ["Centripetal force is magnetic: $qvB=mv^2/r$.",
                  "Cancel one $v$ (if $v\\neq 0$).",
                  "$r=mv/(qB)$."],
                 "$r=mv/(qB)$", "", "Hard")
        + _ican(ican1),
        ("Using $qE$ formulas on a magnetic-only problem",
         "No electric field means no $qE$. Circles here are not gravity projectiles and not SHM springs."),
        ("Angle between $v$ and $B$",
         "If the problem says '$B$ into the page, $v$ to the right', $\\theta=90^\\circ$. Do not insert $30^\\circ$ from a random triangle."),
        ican1,
        1,
    )

    ican2 = [
        "I can compute $F=ILB\\sin\\theta$ on a straight wire.",
        "I can state that parallel currents attract and opposite currents repel.",
        "I can use $F/\\ell=\\mu_0 I_1 I_2/(2\\pi d)$.",
    ]
    c2 = concept_block(
        "2. Force on a current",
        [
            "A current is many moving charges. Summing $q\\vec{v}\\times\\vec{B}$ on a straight segment gives $\\vec{F}=I\\vec{\\ell}\\times\\vec{B}$, magnitude $ILB\\sin\\theta$.",
            "Example: $I=2.0\\,\\mathrm{A}$, $\\ell=0.40\\,\\mathrm{m}$, $B=0.50\\,\\mathrm{T}$ perpendicular $\\Rightarrow$ $F=0.40\\,\\mathrm{N}$.",
            "If the wire is parallel to $\\vec{B}$, $F=0$. Curved wires use $I\\int d\\vec{\\ell}\\times\\vec{B}$.",
            "Two long parallel wires: each sits in the other's circling $B$. Same-direction currents attract; opposite currents repel.",
            "The force per unit length is $F/\\ell=\\mu_0 I_1 I_2/(2\\pi d)$. For $1\\,\\mathrm{A}$ at $1\\,\\mathrm{m}$, that is $2.0\\times10^{-7}\\,\\mathrm{N/m}$, historically related to the definition of the ampere.",
            "This is still not a gravitational orbit and not a spring. It is $I\\vec{\\ell}\\times\\vec{B}$.",
        ],
        "Motors are this force arranged to make torque. Rails and sliding bars in Unit 7 combine this force with Faraday.",
        "Draw $I$ as an arrow on the wire, sketch $B$ at the wire, then RHR for $\\vec{\\ell}\\times\\vec{B}$. For two wires, find $B$ due to wire 1 at wire 2 first.",
        lesson_figure(
            _wire_b_svg(),
            "A second parallel wire would sit in these $B$ circles",
            "Same-direction currents: $I\\times B$ pulls the wires together.",
        )
        + solved(1, "$I=2.0\\,\\mathrm{A}$, $\\ell=0.40\\,\\mathrm{m}$, $B=0.50\\,\\mathrm{T}$ perpendicular. Find $|F|$.",
                 ["$F=ILB\\sin 90^\\circ$.",
                  "$(2.0)(0.40)(0.50)=0.40$.",
                  "Unit: newtons."],
                 "$0.40\\,\\mathrm{N}$", "", "Easy")
        + solved(2, "Why do parallel currents in the same direction attract?",
                 ["Wire 1 makes circling $B$ at wire 2 (RHR).",
                  "$I_2\\vec{\\ell}\\times\\vec{B}_1$ points toward wire 1.",
                  "Newton's third law matches the force on wire 1."],
                 "attract", "", "Medium")
        + solved(3, "$I_1=I_2=1.0\\,\\mathrm{A}$, $d=1.0\\,\\mathrm{m}$. Find $F/\\ell$.",
                 ["$F/\\ell=\\mu_0 I_1 I_2/(2\\pi d)$.",
                  "$\\mu_0/(2\\pi)=2.0\\times10^{-7}$.",
                  "$F/\\ell=2.0\\times10^{-7}\\,\\mathrm{N/m}$."],
                 "$2.0\\times10^{-7}\\,\\mathrm{N/m}$", "", "Hard")
        + _ican(ican2),
        ("Using Coulomb's law between the wires",
         "The wires are electrically neutral overall. The force is magnetic, from currents, not leftover static charge."),
        ("Find $B$ first, then $F$",
         "Two-step: $B=\\mu_0 I_1/(2\\pi d)$ at wire 2, then $F=I_2 \\ell B$. That is the same as the $F/\\ell$ formula."),
        ican2,
        6,
    )

    ican3 = [
        "I can write $d\\vec{B}=(\\mu_0/4\\pi)I d\\vec{\\ell}\\times\\hat{r}/r^2$.",
        "I can recall $B=\\mu_0 I/(2R)$ at the center of a loop.",
        "I can say Biot–Savart always works; Ampere is for high symmetry.",
    ]
    c3 = concept_block(
        "3. Biot-Savart qualitative",
        [
            "Biot–Savart is the magnetic analog of Coulomb's law for a current element: $d\\vec{B}=(\\mu_0/4\\pi)\\,I\\,d\\vec{\\ell}\\times\\hat{r}/r^2$.",
            "The cross product means a current element produces no $dB$ on its own axis ($d\\vec{\\ell}\\parallel\\hat{r}$) and maximum $dB$ to the side.",
            "Right-hand rule: thumb along $I$, fingers curl in the direction of $\\vec{B}$. A long wire therefore has circular field lines.",
            "A famous integral: at the center of a circular loop, every piece is perpendicular and equidistant, so $B=\\mu_0 I/(2R)$.",
            "Biot–Savart always applies (magnetostatics). Ampere's law is faster when symmetry lets $B$ slide out of $\\oint\\vec{B}\\cdot d\\vec{\\ell}$.",
            "Do not use Gauss's law for $E$ to find $B$. Magnetism has $\\oint\\vec{B}\\cdot d\\vec{A}=0$ (no monopoles), which does not give the wire's $1/r$ field by itself.",
        ],
        "When Ampere's symmetry fails (finite wire, arc, loop off-center), you are back to Biot–Savart. AP C expects the loop-center and infinite-wire results as landmarks.",
        "Sketch $d\\vec{\\ell}$, the $\\vec{r}$ to the field point, and whether they are perpendicular. If symmetry is cylindrical or solenoid-like, switch to Ampere.",
        lesson_figure(
            _wire_b_svg(),
            "Biot–Savart's qualitative output for a long wire",
            "Circles of $B$, density falling as you move out — later made precise by Ampere as $1/r$.",
        )
        + solved(1, "When is $dB=0$ from a particular $d\\vec{\\ell}$?",
                 ["$d\\vec{B}\\propto d\\vec{\\ell}\\times\\hat{r}$.",
                  "Cross product is zero if $d\\vec{\\ell}\\parallel\\hat{r}$.",
                  "No field on the element's own line of motion."],
                 "when $d\\vec{\\ell}\\parallel\\hat{r}$", "", "Easy")
        + solved(2, "State $B$ at the center of a single circular loop.",
                 ["Every $d\\ell$ is $\\perp\\hat{r}$ and at distance $R$.",
                  "The integral gives $B=\\mu_0 I/(2R)$.",
                  "Direction: through the center, RHR along $I$ around the loop."],
                 "$B=\\mu_0 I/(2R)$", "", "Medium")
        + solved(3, "Why is Ampere better than Biot–Savart for an infinite straight wire, even though both give $B=\\mu_0 I/(2\\pi r)$?",
                 ["Biot–Savart requires integrating $x$ from $-\\infty$ to $\\infty$.",
                  "Cylindrical symmetry makes $|B|$ constant on a circle.",
                  "Ampere then gives $B\\cdot 2\\pi r=\\mu_0 I$ in one line."],
                 "symmetry lets Ampere skip the integral", "", "Hard")
        + _ican(ican3),
        ("Using $kq/r^2$ for a current element",
         "Electric and magnetic element laws look similar, but $B$ has $\\mu_0/4\\pi$, a cross product, and $I d\\ell$ instead of $dq$."),
        ("Thumb along current",
         "For wires, the RHR for $B$ is not the same hand motion as $q\\vec{v}\\times\\vec{B}$. Thumb along $I$, fingers along the circling $B$."),
        ican3,
        11,
    )

    ican4 = [
        "I can write $\\oint\\vec{B}\\cdot d\\vec{\\ell}=\\mu_0 I_{\\mathrm{enc}}$.",
        "I can derive $B=\\mu_0 I/(2\\pi r)$ for a long wire.",
        "I can explain when Ampere is true but not useful for finding $|B|$.",
    ]
    c4 = concept_block(
        "4. Ampere's law",
        [
            "Ampere's law (magnetostatics) says $\\oint\\vec{B}\\cdot d\\vec{\\ell}=\\mu_0 I_{\\mathrm{enc}}$. The left side is a circulation of $\\vec{B}$; the right side counts current piercing a surface bounded by your loop.",
            "Walk the symmetry the way you walked Gauss. Long wire: $B$ is circular, $|B|$ depends only on $r$. Choose a circle of radius $r$. Then $\\oint B\\cdot d\\ell=B\\cdot 2\\pi r=\\mu_0 I$, so $B=\\mu_0 I/(2\\pi r)$.",
            "Numeric: $I=5.0\\,\\mathrm{A}$, $r=2.0\\,\\mathrm{cm}$, $B=(2.0\\times10^{-7})(5.0)/0.020=5.0\\times10^{-5}\\,\\mathrm{T}$.",
            "Solenoid: rectangular Amperian loop with one side inside. Ideal outside $B=0$, so $B\\ell=\\mu_0 (n\\ell)I$ and $B=\\mu_0 n I$.",
            "Current outside the loop does not appear in $I_{\\mathrm{enc}}$. A potato-shaped loop around a wire is legal but useless for extracting a single $B$.",
            "Inside a thick wire of uniform $J$, $I_{\\mathrm{enc}}=I(r^2/R^2)$, so $B=\\mu_0 I r/(2\\pi R^2)$, linear in $r$ — Ampere analog of Gauss inside a uniform ball.",
        ],
        "Ampere is to Biot–Savart what Gauss is to Coulomb. Maxwell will add displacement current; for this unit, currents are steady.",
        "Choose the loop so $B$ is constant and parallel to $d\\vec{\\ell}$ on the useful parts, and zero or perpendicular on the rest. Then factor $B$.",
        lesson_figure(
            _wire_b_svg(),
            "Amperian circle around a long wire",
            "On this circle $B$ is tangent and constant, so circulation is $B\\cdot 2\\pi r$.",
        )
        + solved(1, "State Ampere's law (magnetostatics) and the long-wire $B$.",
                 ["$\\oint\\vec{B}\\cdot d\\vec{\\ell}=\\mu_0 I_{\\mathrm{enc}}$.",
                  "Circle: $B\\cdot 2\\pi r=\\mu_0 I$.",
                  "$B=\\mu_0 I/(2\\pi r)$."],
                 "$B=\\mu_0 I/(2\\pi r)$", "", "Easy")
        + solved(2, "$I=5.0\\,\\mathrm{A}$, $r=0.020\\,\\mathrm{m}$. Find $B$.",
                 ["Use $\\mu_0/(2\\pi)=2.0\\times10^{-7}$.",
                  "$B=2.0\\times10^{-7}\\times 5.0/0.020$.",
                  "$B=5.0\\times10^{-5}\\,\\mathrm{T}$."],
                 "$5.0\\times10^{-5}\\,\\mathrm{T}$", "", "Medium")
        + solved(3, "Uniform current density in a wire of radius $R$. Find $B(r)$ for $r<R$.",
                 ["$I_{\\mathrm{enc}}=I\\cdot(\\pi r^2)/(\\pi R^2)=I r^2/R^2$.",
                  "Ampere: $B\\cdot 2\\pi r=\\mu_0 I r^2/R^2$.",
                  "$B=\\mu_0 I r/(2\\pi R^2)$."],
                 "$B=\\mu_0 I r/(2\\pi R^2)$", "", "Hard")
        + _ican(ican4),
        ("Putting outside currents into $I_{\\mathrm{enc}}$",
         "Only currents through the soap-film surface count. Outside currents can still change $\\vec{B}$ locally, just as outside charges change $\\vec{E}$ without changing net electric flux."),
        ("Symmetry sentence first",
         "Write 'by cylindrical symmetry $B$ is azimuthal and constant on this circle' before $B\\cdot 2\\pi r=\\mu_0 I$. That sentence is points."),
        ican4,
        16,
    )

    ican5 = [
        "I can use $B=\\mu_0 n I$ inside a long solenoid and $B\\approx 0$ outside.",
        "I can use $B=\\mu_0 I/(2\\pi r)$ for a long wire.",
        "I can treat a coaxial return current as $I_{\\mathrm{enc}}=0$ outside.",
    ]
    c5 = concept_block(
        "5. Solenoid and wire",
        [
            "A long solenoid is a helical coil of many turns. Interior field is along the axis, nearly uniform, $B=\\mu_0 n I$ with $n=N/\\ell$ the turn density. Ideal exterior field is zero.",
            "Example: $n=1000\\,\\mathrm{m^{-1}}$, $I=2.0\\,\\mathrm{A}$, $B=\\mu_0 n I\\approx 2.5\\times10^{-3}\\,\\mathrm{T}$.",
            "A long straight wire remains $B=\\mu_0 I/(2\\pi r)$ in circles. Superpose two wires as vectors.",
            "Coaxial cable: current $I$ on the inner conductor and $-I$ on the sheath. Between them $B=\\mu_0 I/(2\\pi r)$; outside, $I_{\\mathrm{enc}}=0$ so $B=0$.",
            "A toroid is a solenoid bent into a doughnut: $B=\\mu_0 N I/(2\\pi r)$ inside the core (ideal), $0$ outside.",
            "These three — wire, solenoid, toroid — are the Ampere greatest hits. Match the Amperian loop to the object's symmetry.",
        ],
        "Inductance in Unit 7 is 'how much $\\Phi_B$ a solenoid makes per ampere'. You need $B=\\mu_0 n I$ first.",
        "Name the object. If it is long and tightly wound, use $\\mu_0 n I$ inside. If it is a single long wire, use $\\mu_0 I/(2\\pi r)$. If it is coaxial, check $I_{\\mathrm{enc}}$.",
        lesson_figure(
            _solenoid_svg(),
            "Long solenoid",
            "Interior $B$ is axial and uniform; exterior $B$ is neglected in the idealization.",
        )
        + solved(1, "$n=1000\\,\\mathrm{m^{-1}}$, $I=2.0\\,\\mathrm{A}$. Interior solenoid $B$?",
                 ["$B=\\mu_0 n I$.",
                  "$nI=2000\\,\\mathrm{A/m}$.",
                  "$B=(4\\pi\\times10^{-7})(2000)\\approx 2.5\\times10^{-3}\\,\\mathrm{T}$."],
                 "$2.5\\times10^{-3}\\,\\mathrm{T}$", "", "Easy")
        + solved(2, "Coaxial cable, $I$ inner and $-I$ sheath. $B$ outside?",
                 ["Amperian circle outside both.",
                  "$I_{\\mathrm{enc}}=I+(-I)=0$.",
                  "$B=0$."],
                 "$B=0$ outside", "", "Medium")
        + solved(3, "Why is $B$ independent of $r$ inside an ideal long solenoid?",
                 ["Ampere rectangle: interior side length $\\ell$ encloses $n\\ell$ turns, current $n\\ell I$, independent of how far the side sits from the wall (as long as it is inside).",
                  "Outside contribution is taken to be 0.",
                  "So $B\\ell=\\mu_0 n\\ell I$ with no leftover $r$."],
                 "uniform interior $B=\\mu_0 n I$", "", "Hard")
        + _ican(ican5),
        ("Using $\\mu_0 I/(2\\pi r)$ inside a solenoid",
         "That is the long-wire formula. A solenoid's interior field is axial, not circling a single wire, and it does not fall as $1/r$."),
        ("List $n$ versus $N$",
         "$n$ is turns per meter. If the problem gives $N$ turns on length $\\ell$, form $n=N/\\ell$ before using $B=\\mu_0 n I$."),
        ican5,
        21,
    )

    ican6 = [
        "I can compute $\\tau=IAB\\sin\\theta=\\mu B\\sin\\theta$.",
        "I can define $\\vec{\\mu}=I\\vec{A}$ with RHR.",
        "I can state net $F=0$ on a loop in uniform $B$, with possible torque.",
    ]
    c6 = concept_block(
        "6. Torque on a loop",
        [
            "A current loop is a magnetic dipole $\\vec{\\mu}=I\\vec{A}$, where $\\vec{A}$ is the area vector from the right-hand rule (fingers along $I$, thumb along $\\vec{\\mu}$).",
            "In a uniform $\\vec{B}$, net force on the closed loop is zero, but a torque $\\vec{\\tau}=\\vec{\\mu}\\times\\vec{B}$ tries to align $\\vec{\\mu}$ with $\\vec{B}$.",
            "Magnitude $\\tau=IAB\\sin\\theta$. Example: $I=2.0\\,\\mathrm{A}$, $A=0.050\\,\\mathrm{m^2}$, $B=0.40\\,\\mathrm{T}$, $\\theta=90^\\circ$ gives $\\tau=0.040\\,\\mathrm{N\\cdot m}$.",
            "$N$ turns multiply $\\mu$ and $\\tau$ by $N$. Potential energy $U=-\\vec{\\mu}\\cdot\\vec{B}$ is lowest when aligned (stable).",
            "This is the electric-dipole analog: $\\vec{p}\\times\\vec{E}$ became $\\vec{\\mu}\\times\\vec{B}$. Same 'uniform field: torque without net force' story.",
            "A motor is a loop arranged so that current can be commutated and the torque keeps turning the coil.",
        ],
        "Galvanometers, motors, and the energy of magnetic dipoles all start here. You will see $\\mu$ again if a loop sits in a nonuniform $B$ (net force toward stronger field).",
        "Find area $A$, find $\\vec{\\mu}$ by RHR, find $\\theta$ between $\\vec{\\mu}$ and $\\vec{B}$, then $\\tau=\\mu B\\sin\\theta$. If $B$ is uniform, say net $F=0$ out loud.",
        lesson_figure(
            _flux_loop_svg(),
            "A current loop in a field",
            "× marks: $\\vec{B}$ into the page, perpendicular to the area. Net force is still zero in uniform $B$; torque depends on the angle between $\\vec{\\mu}$ and $\\vec{B}$.",
        )
        + solved(1, "What is $\\vec{\\mu}$ for a single loop?",
                 ["$\\mu=IA$.",
                  "Direction: RHR from the sense of $I$.",
                  "Along the area vector."],
                 "$\\vec{\\mu}=I\\vec{A}$", "", "Easy")
        + solved(2, "$I=2.0\\,\\mathrm{A}$, $A=0.050\\,\\mathrm{m^2}$, $B=0.40\\,\\mathrm{T}$, $\\theta=90^\\circ$. Find $\\tau$.",
                 ["$\\tau=IAB\\sin 90^\\circ$.",
                  "$(2.0)(0.050)(0.40)=0.040$.",
                  "Unit: $\\mathrm{N\\cdot m}$."],
                 "$0.040\\,\\mathrm{N\\cdot m}$", "", "Medium")
        + solved(3, "Uniform $B$: net force on the loop? Energy difference between $\\theta=0$ and $\\theta=180^\\circ$?",
                 ["Net $F=0$ in uniform $B$.",
                  "$U=-\\mu B\\cos\\theta$, so $U(0)=-\\mu B$ and $U(180^\\circ)=+\\mu B$.",
                  "Difference $2\\mu B$ is the work to flip the dipole."],
                 "$F_{\\mathrm{net}}=0$, $\\Delta U=2\\mu B$", "", "Hard")
        + _ican(ican6),
        ("Claiming torque is zero because net force is zero",
         "A couple can twist without a net force. The two sides of the loop feel opposite forces that rotate it."),
        ("Area vector, not 'along the current'",
         "$\\vec{\\mu}$ punches through the loop, perpendicular to the plane, not tangent to the wire."),
        ican6,
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        ["Force on a moving charge", "Force on a current", "Biot-Savart qualitative",
         "Ampere's law", "Solenoid and wire", "Torque on a loop"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Induction
# ===========================================================================

def _u7_questions():
    return _pack([
        ("Magnetic flux through a flat loop is $\\Phi_B=\\vec{B}\\cdot\\vec{A}=BA\\cos\\theta$. If $B=0.40\\,\\mathrm{T}$ is perpendicular to $A=0.050\\,\\mathrm{m^2}$, $\\Phi_B=$",
         "0.020 Wb",
         "$BA=(0.40)(0.050)=0.020\\,\\mathrm{Wb}$.",
         ["0.080 Wb", "8.0 Wb", "0"]),
        ("If that $B$ is parallel to the plane of the loop, $\\Phi_B=$",
         "0",
         "$\\cos 90^\\circ=0$.",
         ["0.020 Wb", "BA/2", "infinite"]),
        ("The weber equals",
         "$\\mathrm{T\\cdot m^2}$",
         "Also $\\mathrm{V\\cdot s}$.",
         ["T", "N/C", "H"]),
        ("For $N$ turns, the flux linkage is",
         "$N\\Phi_B$",
         "Each turn contributes $\\Phi_B$ if they share the same flux.",
         ["$\\Phi_B/N$", "$\\Phi_B$", "$B/N$"]),
        ("Flux can change because $B$, $A$, or $\\theta$",
         "changes with time",
         "Any of the three in $BA\\cos\\theta$.",
         ["is required to be constant by Gauss", "cannot change", "only $A$ may change"]),
        ("Faraday's law: $\\mathcal{E}=-d\\Phi_B/dt$ (for one turn). If $\\Phi_B$ increases uniformly by $0.020\\,\\mathrm{Wb}$ in $0.010\\,\\mathrm{s}$, $|\\mathcal{E}|=$",
         "2.0 V",
         "$0.020/0.010=2.0\\,\\mathrm{V}$.",
         ["0.20 V", "0.0002 V", "20 V"]),
        ("For $N$ turns, $\\mathcal{E}=-N d\\Phi_B/dt$. $N=50$, $d\\Phi_B/dt=0.040\\,\\mathrm{Wb/s}$, $|\\mathcal{E}|=$",
         "2.0 V",
         "$50\\times 0.040=2.0\\,\\mathrm{V}$.",
         ["0.040 V", "1250 V", "0"]),
        ("The minus sign is Lenz's law: the induced current's $B$ tries to",
         "oppose the change in flux",
         "Not 'oppose $B$' if $B$ is decreasing — then induced $B$ supports $B$.",
         ["always cancel $B$ completely", "point along $v$", "heat the air"]),
        ("If $\\Phi_B$ is constant, Faraday says $\\mathcal{E}=$",
         "0",
         "Need $d\\Phi_B/dt$, not merely nonzero $B$.",
         ["$BA$", "$B$", "infinite"]),
        ("A changing $B$ in a stationary loop induces $\\mathcal{E}$ even with $v=0$ because",
         "$d\\Phi_B/dt\\neq 0$",
         "Transformer electric field, not motional $v\\times B$.",
         ["charges feel $qvB$ with $v=0$", "Ohm failed", "Gauss failed"]),
        ("Lenz: flux of $B$ into the page through a loop is increasing. Induced current is",
         "counterclockwise (induced $B$ out of the page)",
         "Increasing into-page flux needs induced $B$ out; RHR then gives counterclockwise current.",
         ["clockwise", "zero", "into the page along a radius"]),
        ("A magnet's north pole moves toward a loop along its axis. The loop faces a",
         "repulsive induced pole (opposes the approach)",
         "Induced current fights the increase of flux.",
         ["attractive south that pulls it in faster", "no effect", "electric charge on the magnet"]),
        ("If you try to decrease the flux through a conducting loop, the induced current",
         "tries to maintain the flux (induced $B$ in the original direction)",
         "Oppose the change.",
         ["always reverses $B$", "stops instantly", "produces $E=0$"]),
        ("Lenz plus $P=I^2 R$ means you do positive mechanical work when you force flux to change against the induced force. That work",
         "becomes thermal energy in the loop (or stored $LI^2/2$ if $L$ matters)",
         "Energy conservation.",
         ["creates charge", "violates Faraday", "is zero because $B$ does no work on charges? The agent does work"]),
        ("Eddy currents in a metal sheet moving into $B$ produce magnetic drag. That is Lenz applied to",
         "many tiny loops in the bulk metal",
         "Laminations reduce them.",
         ["Gauss for $E$", "Ohm's internal $r$ only", "displacement current only"]),
        ("Motional emf on a rod of length $\\ell$ moving at $v$ perpendicular to uniform $B$ (and to $\\ell$) is",
         "$B\\ell v$",
         "$\\mathcal{E}=\\int (\\vec{v}\\times\\vec{B})\\cdot d\\vec{\\ell}$.",
         ["$B\\ell/v$", "$Bv/\\ell$", "0 always"]),
        ("$B=0.50\\,\\mathrm{T}$, $\\ell=0.20\\,\\mathrm{m}$, $v=4.0\\,\\mathrm{m/s}$ all mutually perpendicular. $\\mathcal{E}=$",
         "0.40 V",
         "$(0.50)(0.20)(4.0)=0.40\\,\\mathrm{V}$.",
         ["0.10 V", "4.0 V", "2.5 V"]),
        ("On rails, area increase $dA=\\ell v\\,dt$ so $d\\Phi_B/dt=B\\ell v$, matching motional $\\mathcal{E}$. The current is $\\mathcal{E}/R$ if the loop resistance is $R$. Magnetic force on the rod then is",
         "$I\\ell B$ opposing $v$ (Lenz drag)",
         "You must pull to keep $v$ constant.",
         ["$I\\ell B$ speeding the rod up", "0 because $K$ of charges is constant? The rod as a whole can still feel $F$", "$qvB$ on the rail only"]),
        ("Charges in the moving rod feel $q(\\vec{v}\\times\\vec{B})$ until $qE$ balances, giving $\\Delta V=B\\ell v$ between the ends. That is the",
         "motional-emf microscopic picture",
         "Same number as Faraday on the growing loop.",
         ["displacement current", "Ampere on a solenoid", "Gauss on a sphere"]),
        ("If $v$ is parallel to $\\vec{B}$, motional $\\mathcal{E}$ along a perpendicular rod is",
         "0",
         "$\\vec{v}\\times\\vec{B}=0$.",
         ["$B\\ell v$", "infinite", "$IR$"]),
        ("Self-inductance $L$ is defined by $N\\Phi_B=LI$ or $\\mathcal{E}=-L dI/dt$. SI unit henry (H) equals",
         "Wb/A or V·s/A",
         "From the definition.",
         ["T", "F", "Ω"]),
        ("A long solenoid: $L=\\mu_0 n^2 A\\ell$. If you double $n$ at fixed length and area, $L$ is multiplied by",
         "4",
         "$L\\propto n^2$.",
         ["2", "1/2", "1"]),
        ("If $I$ ramps at $2.0\\,\\mathrm{A/s}$ through $L=0.50\\,\\mathrm{H}$, $|\\mathcal{E}|=$",
         "1.0 V",
         "$L|dI/dt|=0.50\\times 2.0=1.0\\,\\mathrm{V}$.",
         ["0.25 V", "4.0 V", "0"]),
        ("Inductors oppose",
         "changes in current (Lenz for self-flux)",
         "Not current itself: a constant $I$ has $\\mathcal{E}=0$ (ideal $L$).",
         ["voltage forever", "charge on a capacitor only", "mass"]),
        ("Energy stored in an inductor is",
         "$\\tfrac12 LI^2$",
         "Analog of $\\tfrac12 CV^2$.",
         ["$LI$", "$L/I^2$", "$Q^2/(2L)$"]),
        ("RL circuit, battery $\\varepsilon$, series $R$ and $L$. The DE is $L\\dot I+RI=\\varepsilon$. Time constant $\\tau=$",
         "$L/R$",
         "Analog of $RC$, but inverted roles of $L$ vs $C$.",
         ["$RC$", "$RL$", "$R/L$ as a time? that would be 1/seconds"]),
        ("RL growth: $I(t)=(\\varepsilon/R)(1-e^{-t/\\tau})$. At $t=0^+$, $I=$",
         "0",
         "Inductor as open circuit at the first instant.",
         ["$\\varepsilon/R$", "$\\varepsilon L$", "infinite"]),
        ("After a long time in that RL circuit, $I=$",
         "$\\varepsilon/R$",
         "Inductor as a wire ($dI/dt=0$).",
         ["0", "$\\varepsilon L/R$", "infinite"]),
        ("$L=0.20\\,\\mathrm{H}$, $R=10\\,\\Omega$. $\\tau=$",
         "0.020 s",
         "$L/R=0.20/10=0.020\\,\\mathrm{s}$.",
         ["2.0 s", "50 s", "0.20 s"]),
        ("RL current decay (no battery) is $I=I_0 e^{-t/\\tau}$ with the same $\\tau=L/R$. Energy $\\tfrac12 LI^2$ becomes",
         "heat in $R$",
         "Analog of capacitor discharge.",
         ["charge on $L$", "Gauss flux", "unchanged forever"]),
        ("$\\Phi_B$ through a coil in a uniform $B$ that is ramped. Even if the coil does not move, Faraday still gives $\\mathcal{E}$ because",
         "$B$ is changing",
         "Transformer emf.",
         ["$v$ must be nonzero", "Ampere forbids it", "$R=0$ is required"]),
        ("A loop's area is shrinking in constant $B$ perpendicular to the plane. Flux",
         "decreases, so there is an emf",
         "$dA/dt\\neq 0$.",
         ["is constant because $B$ is", "is zero because $v=0$ at the center", "cannot be defined"]),
        ("Lenz drag on a sliding bar: to keep $v$ constant you must apply $F_{\\mathrm{ext}}=I\\ell B=$",
         "$B^2\\ell^2 v/R$",
         "$I=B\\ell v/R$.",
         ["$B\\ell v$", "0", "$mg$ always"]),
        ("Power you supply $F_{\\mathrm{ext}}v$ equals",
         "$I^2 R$ (energy conservation)",
         "Mechanical in, thermal out.",
         ["$\\tfrac12 LI^2$ only", "0", "$qV$ with $q=0$"]),
        ("Mutual inductance $M$: $\\mathcal{E}_2=-M dI_1/dt$. $M$ is symmetric: $M_{12}=M_{21}$ in typical linear media. Units still",
         "henry",
         "Same as $L$.",
         ["farad", "tesla", "weber only"]),
        ("An ideal inductor in DC steady state is replaced by",
         "a wire",
         "$dI/dt=0\\Rightarrow\\mathcal{E}_L=0$.",
         ["an open circuit", "a capacitor", "a battery"]),
        ("An ideal inductor at the instant a current would jump is replaced by",
         "an open circuit (current cannot jump)",
         "Dual of the capacitor's $V$ cannot jump.",
         ["a wire", "a short with $R=0$ and $I=\\infty$", "a resistor of value $L$"]),
        ("Series $L$ add; parallel $L$ combine like",
         "parallel resistors ($1/L$ add) in the uncoupled ideal case",
         "Same pattern as $R$, opposite of $C$.",
         ["parallel capacitors", "series $C$", "Gauss spheres"]),
        ("If $\\Phi_B$ through a loop oscillates as $\\Phi_0\\cos\\omega t$, $\\mathcal{E}=$",
         "$\\Phi_0\\omega\\sin\\omega t$ (with a sign)",
         "Derivative of cosine.",
         ["$\\Phi_0\\cos\\omega t$", "0", "$\\Phi_0/\\omega$"]),
        ("A superconducting loop ($R=0$) traps flux: $d\\Phi_B/dt=0$ so $\\Phi_B$ is",
         "constant",
         "Persistent current adjusts to keep $\\Phi_B$ fixed.",
         ["always 0", "always $BA$", "undefined"]),
        ("Sign of motional $I$ on rails: area growing, $B$ into the page. Induced current's $B$ is",
         "out of the page, so current is counterclockwise if 'into' was $\\times$",
         "Lenz.",
         ["into the page to add flux", "zero", "along $B$"]),
        ("$L$ of a solenoid scales as $n^2 A\\ell$. Energy density of $B$ is $\\tfrac12 B^2/\\mu_0$, and $\\int u\\,dV$ recovers",
         "$\\tfrac12 LI^2$",
         "Field-energy view.",
         ["$\\tfrac12 CV^2$ without $B$", "0", "$I^2 R$"]),
        ("Faraday for a stationary circuit in changing $B$ implies a circling $\\vec{E}$ with $\\oint\\vec{E}\\cdot d\\vec{\\ell}=-d\\Phi_B/dt$. That $\\vec{E}$ is",
         "nonconservative (electrostatics' $\\oint E\\cdot d\\ell=0$ is dropped)",
         "Induction electric field.",
         ["still a gradient of $V$ globally with $V$ single-valued on the loop without a cut", "magnetic", "zero in the wire"]),
        ("If resistance of a sliding-bar loop doubles, induced $I$ at given $v$",
         "halves, so magnetic drag halves",
         "$I=\\mathcal{E}/R$.",
         ["doubles", "is unchanged", "becomes $\\mathcal{E}$"]),
        ("Units check: $B\\ell v$ has units of",
         "volts",
         "$(T)(m)(m/s)=\\mathrm{Wb/s}=\\mathrm{V}$.",
         ["tesla", "newtons", "amperes"]),
        ("A coil of $N=100$, area $0.010\\,\\mathrm{m^2}$, $B$ from $0$ to $0.20\\,\\mathrm{T}$ in $0.050\\,\\mathrm{s}$ perpendicular. Average $|\\mathcal{E}|=$",
         "4.0 V",
         "$N\\Delta\\Phi/\\Delta t=100(0.0020)/0.050=4.0\\,\\mathrm{V}$.",
         ["0.040 V", "2.0 V", "20 V"]),
        ("AP Stretch: Inductor $L=0.40\\,\\mathrm{H}$ carrying $1.5\\,\\mathrm{A}$ is disconnected from its battery and left to decay through $R=8.0\\,\\Omega$. Current at $t=0.025\\,\\mathrm{s}$ is",
         "$0.910\\,\\mathrm{A}$",
         "$\\tau=L/R=0.050\\,\\mathrm{s}$, so $I=1.5\\,e^{-0.50}\\approx 0.910\\,\\mathrm{A}$.",
         ["$1.5\\,\\mathrm{A}$", "$0.75\\,\\mathrm{A}$", "0"]),
        ("AP Stretch: Solenoid $n=1000\\,\\mathrm{m^{-1}}$, $A=0.010\\,\\mathrm{m^2}$, $\\ell=0.20\\,\\mathrm{m}$ carries $I=4.0\\,\\mathrm{A}$. Energy $U=\\tfrac12 L I^2$ with $L=\\mu_0 n^2 A\\ell$ equals",
         "$0.020\\,\\mathrm{J}$",
         "$L=(4\\pi\\times10^{-7})(10^6)(0.010)(0.20)=2.51\\times10^{-3}\\,\\mathrm{H}$, so $U=\\tfrac12(2.51\\times10^{-3})(16)\\approx 0.020\\,\\mathrm{J}$.",
         ["$0.080\\,\\mathrm{J}$", "$\\tfrac12 LI$", "$5.0\\times10^{-3}\\,\\mathrm{J}$"]),
        ("AP Stretch: A bar moves so $x(t)$, $A=x\\ell$, $B$ uniform. $\\mathcal{E}=B\\ell\\dot x$. If the bar has mass $m$ and is released with $v_0$ (no $F_{\\mathrm{ext}}$), $m\\dot v=-(B^2\\ell^2/R)v$ so $v=$",
         "$v_0 e^{-t/\\tau_m}$ with $\\tau_m=mR/(B^2\\ell^2)$",
         "Magnetic damping analog of linear drag.",
         ["constant $v_0$", "$v_0+at$", "circular SHM"]),
        ("AP Stretch: $\\oint\\vec{E}\\cdot d\\vec{\\ell}=-d\\Phi_B/dt$ around a circle of radius $r$ inside a solenoid with uniform $B(t)$ gives $E_{\\theta}=$",
         "$(r/2)|dB/dt|$",
         "$E\\cdot 2\\pi r=\\pi r^2 |dB/dt|$.",
         ["$r|dB/dt|$", "0 because $E=0$ in magnetostatics", "$B/\\mu_0$"]),
        ("AP Stretch: Long solenoid of radius $R=0.050\\,\\mathrm{m}$ has $B$ increasing at $40\\,\\mathrm{T/s}$. Faraday on a circle of radius $r=0.080\\,\\mathrm{m}$ (outside the windings) uses flux $\\Phi_B=B\\pi R^2$ through that circle. Then $E_{\\theta}=$",
         "$0.625\\,\\mathrm{V/m}$",
         "$E\\cdot 2\\pi r=\\pi R^2\\,dB/dt$, so $E=(R^2/(2r))(40)=(0.0025/0.16)\\times 40=0.625\\,\\mathrm{V/m}$.",
         ["$(r/2)(40)\\,\\mathrm{V/m}$", "0 because $r>R$", "$\\mu_0 n I$"]),
        ("AP Stretch: Energy delivered by a battery while RL current grows to $\\varepsilon/R$ is $\\int\\varepsilon I\\,dt$. Of that, $\\tfrac12 LI_{\\infty}^2$ is stored and the rest is",
         "$\\int I^2 R\\,dt$, which equals $\\tfrac12 LI_{\\infty}^2$ as well for this linear growth-to-steady story",
         "Analog of the RC half-and-half.",
         ["zero heat", "$C\\varepsilon^2$", "Gauss energy"]),
        ("AP Stretch: Kirchhoff for RL: traversing $L$ in the direction of increasing $I$ counts a drop $L dI/dt$. That sign implements",
         "Lenz (back emf)",
         "Opposes the increase.",
         ["Ohm", "Gauss", "a gravitational minus $mg$"]),
        ("AP Stretch: A rectangular loop of length $\\ell$ sits beside a long wire, spanning $r=a$ to $r=b$. Magnetic flux through the rectangle is",
         "$(\\mu_0 I \\ell/2\\pi)\\ln(b/a)$",
         "$\\Phi_B=\\int_a^b (\\mu_0 I/(2\\pi r))\\ell\\,dr=(\\mu_0 I \\ell/2\\pi)\\ln(b/a)$.",
         ["0 always", "$\\mu_0 I/(2\\pi a)$", "$BA$ using $B$ only at the center"]),
        ("AP Stretch: Magnetic flux through one turn is $\\Phi_B=(0.040\\,\\mathrm{Wb})\\cos(120 t)$ with $t$ in seconds. Peak $|\\mathcal{E}|=|d\\Phi_B/dt|$ is",
         "$4.8\\,\\mathrm{V}$",
         "$d\\Phi_B/dt=-0.040\\times 120\\sin(120 t)$, so the peak magnitude is $4.8\\,\\mathrm{V}$.",
         ["$0.040\\,\\mathrm{V}$", "$120\\,\\mathrm{V}$", "0"]),
    ])


def build_unit7():
    title = "AP Physics C E&M Unit 7: Induction"
    description = (
        "Magnetic flux, Faraday's law, Lenz's law, motional emf, inductance, and RL circuits "
        "with the DE $L\\dot I+RI=\\varepsilon$."
    )
    i_rl = sample_curve(lambda t: 1 - math.exp(-t), 0, 5)

    ican1 = [
        "I can compute $\\Phi_B=BA\\cos\\theta$ in webers.",
        "I can include $N$ as flux linkage $N\\Phi_B$.",
        "I can name $B$, $A$, and $\\theta$ as the three ways flux changes.",
    ]
    c1 = concept_block(
        "1. Magnetic flux",
        [
            "Magnetic flux $\\Phi_B$ through a surface is $\\Phi_B=\\int\\vec{B}\\cdot d\\vec{A}$. For a flat loop in uniform $B$, $\\Phi_B=BA\\cos\\theta$, where $\\theta$ is the angle between $\\vec{B}$ and the area vector.",
            "The SI unit is the weber: $1\\,\\mathrm{Wb}=1\\,\\mathrm{T\\cdot m^2}=1\\,\\mathrm{V\\cdot s}$.",
            "Example: $B=0.40\\,\\mathrm{T}$ perpendicular to $A=0.050\\,\\mathrm{m^2}$ gives $\\Phi_B=0.020\\,\\mathrm{Wb}$. If $B$ lies in the plane of the loop, $\\Phi_B=0$.",
            "A coil of $N$ turns that all see the same flux has flux linkage $N\\Phi_B$. Faraday will pick up that factor $N$.",
            "Flux changes if $B$ changes, if the area changes, or if the loop rotates ($\\theta$ changes). Any of those three produces emf.",
            "Gauss for magnetism says the flux of $B$ through a closed surface is zero (no monopoles). Faraday uses flux through an open surface bounded by a circuit.",
        ],
        "Faraday is a statement about $d\\Phi_B/dt$. If flux is fuzzy, the minus sign of Lenz has nothing to grab onto.",
        "Draw $\\vec{A}$ with RHR on the loop. Compute $BA\\cos\\theta$. If there are $N$ turns, multiply. Then ask which of $B,A,\\theta$ will depend on time.",
        lesson_figure(
            _flux_loop_svg(),
            "Flux through a loop",
            "$\\Phi_B=BA$ when $\\vec{B}$ is into the page ($\\times$), perpendicular to the rectangle.",
        )
        + solved(1, "$B=0.40\\,\\mathrm{T}$ perpendicular to $A=0.050\\,\\mathrm{m^2}$. Find $\\Phi_B$.",
                 ["$\\theta=0$, $\\cos\\theta=1$.",
                  "$\\Phi_B=BA=(0.40)(0.050)=0.020$.",
                  "Unit: weber."],
                 "$0.020\\,\\mathrm{Wb}$", "", "Easy")
        + solved(2, "Same loop, $B$ parallel to the plane. $\\Phi_B$?",
                 ["$\\theta=90^\\circ$.",
                  "$\\cos 90^\\circ=0$.",
                  "$\\Phi_B=0$ even though $B\\neq 0$."],
                 "0", "", "Medium")
        + solved(3, "List three independent ways $\\Phi_B$ of a planar loop can change in time.",
                 ["Change $|B|$ (electromagnet, moving magnet).",
                  "Change $A$ (expanding loop, sliding bar).",
                  "Change $\\theta$ (rotating coil, generator)."],
                 "$B$, $A$, or $\\theta$ can vary", "", "Hard")
        + _ican(ican1),
        ("Confusing $\\Phi_B$ with $\\Phi_E$",
         "Electric flux is $E A$ and appears in Gauss. Magnetic flux is $B A$ and appears in Faraday. Different letters, different laws."),
        ("Area vector first",
         "If you never draw $\\vec{A}$, you cannot know $\\cos\\theta$. A loop 'face-on' to $B$ has maximum flux; 'edge-on' has zero."),
        ican1,
        1,
    )

    ican2 = [
        "I can use $\\mathcal{E}=-N d\\Phi_B/dt$ and compute magnitudes from $\\Delta\\Phi/\\Delta t$.",
        "I can state that constant $B$ through a fixed loop gives zero emf.",
        "I can distinguish transformer emf (changing $B$) from motional $v\\times B$.",
    ]
    c2 = concept_block(
        "2. Faraday's law",
        [
            "Faraday's law: the emf around a loop equals minus the rate of change of magnetic flux through any surface bounded by that loop. One turn: $\\mathcal{E}=-d\\Phi_B/dt$. $N$ turns: $\\mathcal{E}=-N d\\Phi_B/dt$.",
            "Example: $\\Phi_B$ rises by $0.020\\,\\mathrm{Wb}$ in $0.010\\,\\mathrm{s}$ $\\Rightarrow$ $|\\mathcal{E}|=2.0\\,\\mathrm{V}$. With $N=50$ and $d\\Phi_B/dt=0.040\\,\\mathrm{Wb/s}$, $|\\mathcal{E}|=2.0\\,\\mathrm{V}$.",
            "The minus sign is not optional decoration; it is Lenz's law, unpacked in the next concept.",
            "A stationary loop in a changing $B$ still has emf. There is an induced circling electric field with $\\oint\\vec{E}\\cdot d\\vec{\\ell}=-d\\Phi_B/dt$. That $\\vec{E}$ is not conservative.",
            "A moving bar in constant $B$ also has emf, equal to $B\\ell v$, which matches $d(BA)/dt$ when area grows. Same Faraday, different microscopic story.",
            "If flux is constant, emf is zero even if $B$ itself is huge. You need a derivative.",
        ],
        "This is Maxwell's third equation in integral form. Generators, transformers, and inductors are Faraday machines.",
        "Compute $\\Phi_B(t)$, differentiate, multiply by $N$, attach a minus sign for direction via Lenz. For averages, $|\\mathcal{E}|=N|\\Delta\\Phi_B|/\\Delta t$.",
        lesson_figure(
            _flux_loop_svg(),
            "If $B$ through this loop increases, Faraday produces emf around the rectangle",
            "× marks: $\\vec{B}$ into the page. Stationary wires, changing $B$: still $\\mathcal{E}=-d\\Phi_B/dt$.",
        )
        + solved(1, "$\\Delta\\Phi_B=0.020\\,\\mathrm{Wb}$ in $0.010\\,\\mathrm{s}$, one turn. Find $|\\mathcal{E}|$.",
                 ["$|\\mathcal{E}|=|\\Delta\\Phi_B|/\\Delta t$.",
                  "$0.020/0.010=2.0$.",
                  "Unit: volt."],
                 "$2.0\\,\\mathrm{V}$", "", "Easy")
        + solved(2, "$N=50$, $d\\Phi_B/dt=0.040\\,\\mathrm{Wb/s}$. Find $|\\mathcal{E}|$.",
                 ["$\\mathcal{E}=-N d\\Phi_B/dt$.",
                  "$50\\times 0.040=2.0$.",
                  "$|\\mathcal{E}|=2.0\\,\\mathrm{V}$."],
                 "$2.0\\,\\mathrm{V}$", "", "Medium")
        + solved(3, "A coil sits in a constant uniform $B$. You rotate it at angular speed $\\omega$ with $\\Phi_B=BA\\cos\\omega t$. Find $\\mathcal{E}(t)$.",
                 ["$\\Phi_B=BA\\cos\\omega t$.",
                  "$\\mathcal{E}=-N d\\Phi_B/dt=NBA\\omega\\sin\\omega t$ (one turn: drop $N$).",
                  "This is a generator: changing $\\theta$ at fixed $B$ and $A$."],
                 "$\\mathcal{E}=NBA\\omega\\sin\\omega t$", "", "Hard")
        + _ican(ican2),
        ("Thinking a strong magnet near a loop always gives emf",
         "A parked magnet, constant flux, gives zero emf. Motion or a changing $B$ is required."),
        ("Average vs instantaneous",
         "If you only have $\\Delta\\Phi$ and $\\Delta t$, you get the average emf. Instantaneous emf needs the derivative of a formula for $\\Phi_B(t)$."),
        ican2,
        6,
    )

    ican3 = [
        "I can apply Lenz: induced $B$ opposes the change in flux.",
        "I can find the sense of $I$ with RHR once induced $B$ is known.",
        "I can connect Lenz drag to energy conservation.",
    ]
    c3 = concept_block(
        "3. Lenz's law",
        [
            "Lenz's law: the induced current produces its own magnetic field that opposes the change in flux that created it. If flux into the page is increasing, the loop tries to make flux out of the page.",
            "Right-hand rule then gives the current direction. Increasing into-page flux $\\Rightarrow$ induced $B$ toward you $\\Rightarrow$ counterclockwise current (standard $\\times$/$\\cdot$ convention).",
            "A north pole approaching a loop faces a north pole (repulsion). The loop fights the increase of toward-loop flux. When the magnet recedes, the loop tries to attract it back.",
            "Lenz is energy conservation wearing a magnetic costume. If induced current helped the change, you would get free energy: a magnet would be sucked in faster and faster while $I^2 R$ heat appeared.",
            "Eddy currents are Lenz in bulk metal: many microscopic loops. They make magnetic drag; laminating the metal cuts the loops and reduces heating.",
            "Oppose the change, not necessarily the field. If $B$ is decreasing, induced $B$ is in the same direction as the original $B$, trying to maintain the flux.",
        ],
        "Direction points on Faraday FRQs are Lenz points. The minus sign in $\\mathcal{E}=-d\\Phi_B/dt$ is this paragraph.",
        "Ask: is flux through the loop increasing or decreasing, and in which direction? Induced $B$ fights that trend. Then RHR for $I$.",
        lesson_figure(
            _flux_loop_svg(),
            "If $B$ into the page ($\\times$ marks) is increasing, induced current fights that increase",
            "Induced $B$ would point out of the page (dots); current around the rectangle follows the right-hand rule.",
        )
        + solved(1, "Flux into the page through a loop is increasing. Direction of induced $B$?",
                 ["Change is 'more into the page'.",
                  "Oppose: make $B$ out of the page.",
                  "Induced field toward you."],
                 "induced $B$ out of the page", "", "Easy")
        + solved(2, "A magnet's north pole moves toward a conducting ring along the axis. Does the ring attract or repel the magnet?",
                 ["Toward-loop flux of $B$ is increasing.",
                  "Induced current makes a north pole facing the magnet.",
                  "Like poles: repulsion (Lenz drag)."],
                 "repel", "", "Medium")
        + solved(3, "Why would a 'Lenz-violating' loop that attracted an approaching magnet (helping the flux increase) be a perpetual-motion machine?",
                 ["The magnet would speed up as it approached.",
                  "Kinetic energy would increase while $I^2 R$ heat also appeared.",
                  "Energy would be created; Lenz forbids that by making you do work against drag."],
                 "would create energy; Lenz prevents it", "", "Hard")
        + _ican(ican3),
        ("Opposing $B$ rather than opposing $d\\Phi_B/dt$",
         "If the original $B$ is shrinking, induced $B$ is parallel to it, not antiparallel. Always fight the change."),
        ("Two-step direction",
         "Step 1: induced $B$ direction from Lenz. Step 2: RHR from that $B$ to the current. Skipping step 1 is how CCW and CW get swapped."),
        ican3,
        11,
    )

    ican4 = [
        "I can compute motional $\\mathcal{E}=B\\ell v$.",
        "I can match it to $d(BA)/dt$ for a sliding bar.",
        "I can find Lenz drag $F=B^2\\ell^2 v/R$.",
    ]
    c4 = concept_block(
        "4. Motional emf",
        [
            "Charges in a conductor moving at $\\vec{v}$ in $\\vec{B}$ feel $q(\\vec{v}\\times\\vec{B})$. They separate until $qE$ balances that force, leaving $\\mathcal{E}=B\\ell v$ between the ends when $\\vec{v}$, $\\vec{\\ell}$, and $\\vec{B}$ are mutually perpendicular.",
            "Numeric: $B=0.50\\,\\mathrm{T}$, $\\ell=0.20\\,\\mathrm{m}$, $v=4.0\\,\\mathrm{m/s}$ $\\Rightarrow$ $\\mathcal{E}=0.40\\,\\mathrm{V}$.",
            "On rails, the sliding bar makes the loop area grow as $dA=\\ell v\\,dt$, so $d\\Phi_B/dt=B\\ell v$, the same emf. Faraday and $v\\times B$ agree.",
            "Current $I=\\mathcal{E}/R=B\\ell v/R$. The magnetic force on the bar is $I\\ell B$ opposite $v$. To keep constant speed you pull with $F_{\\mathrm{ext}}=B^2\\ell^2 v/R$. Your power $F_{\\mathrm{ext}}v$ equals $I^2 R$.",
            "If $\\vec{v}\\parallel\\vec{B}$, motional emf along a perpendicular rod is zero. Orientation matters.",
            "This is not a projectile problem and not SHM. It is Faraday plus $I\\vec{\\ell}\\times\\vec{B}$.",
        ],
        "Sliding-bar FRQs combine Units 6 and 7. Energy conservation $F v=I^2 R$ is the check that Lenz drag was in the right direction.",
        "Write $\\mathcal{E}=B\\ell v$, then $I=\\mathcal{E}/R$, then $F=I\\ell B$ opposite velocity. If mass is given, $m a=-b v$ with $b=B^2\\ell^2/R$.",
        lesson_figure(
            _flux_loop_svg(),
            "Growing area as a stand-in for a sliding bar on rails",
            "× marks: $\\vec{B}$ into the page. If the right side moves outward, $A$ increases, $\\Phi_B$ increases, and Faraday plus Lenz produce drag.",
        )
        + solved(1, "$B=0.50\\,\\mathrm{T}$, $\\ell=0.20\\,\\mathrm{m}$, $v=4.0\\,\\mathrm{m/s}$ mutually perpendicular. Find $\\mathcal{E}$.",
                 ["$\\mathcal{E}=B\\ell v$.",
                  "$(0.50)(0.20)(4.0)=0.40$.",
                  "Unit: volt."],
                 "$0.40\\,\\mathrm{V}$", "", "Easy")
        + solved(2, "Loop resistance $R=2.0\\,\\Omega$ with that emf. Find $I$ and the magnetic force magnitude on the bar.",
                 ["$I=\\mathcal{E}/R=0.40/2.0=0.20\\,\\mathrm{A}$.",
                  "$F=I\\ell B=(0.20)(0.20)(0.50)=0.020\\,\\mathrm{N}$.",
                  "Direction: opposite $v$ (Lenz)."],
                 "$0.20\\,\\mathrm{A}$, $0.020\\,\\mathrm{N}$ drag", "", "Medium")
        + solved(3, "Show $F_{\\mathrm{ext}}v=I^2 R$ when $v$ is held constant.",
                 ["$F_{\\mathrm{ext}}=B^2\\ell^2 v/R$.",
                  "$F_{\\mathrm{ext}}v=B^2\\ell^2 v^2/R$.",
                  "$I=B\\ell v/R$ so $I^2 R=B^2\\ell^2 v^2/R$, matching."],
                 "mechanical power = Joule heating", "", "Hard")
        + _ican(ican4),
        ("Forgetting Lenz on the force direction",
         "If your magnetic force on the bar is in the direction of $v$, you are generating energy. Reverse it."),
        ("Mutual perpendiculars",
         "Write a sentence: '$v$ is $\\perp\\ell$ is $\\perp B$'. If any pair is parallel, that factor's sine is zero."),
        ican4,
        16,
    )

    ican5 = [
        "I can use $\\mathcal{E}=-L dI/dt$ and $L=N\\Phi_B/I$.",
        "I can recall $L=\\mu_0 n^2 A\\ell$ for a solenoid.",
        "I can compute $U=\\tfrac12 LI^2$.",
    ]
    c5 = concept_block(
        "5. Inductance",
        [
            "A circuit that produces flux through itself has self-inductance $L$ defined by $N\\Phi_B=LI$, or equivalently $\\mathcal{E}=-L dI/dt$. The unit is the henry.",
            "A long solenoid: $B=\\mu_0 n I$, flux per turn $BA=\\mu_0 n I A$, $N=n\\ell$ turns, so $L=\\mu_0 n^2 A\\ell$. Doubling $n$ quadruples $L$.",
            "Example: $L=0.50\\,\\mathrm{H}$ and $dI/dt=2.0\\,\\mathrm{A/s}$ give $|\\mathcal{E}|=1.0\\,\\mathrm{V}$ of back emf.",
            "An inductor opposes changes in current, not current itself. Constant $I$ means $\\mathcal{E}_L=0$ (ideal).",
            "Energy stored in the magnetic field is $U=\\tfrac12 LI^2$, matching $\\int u\\,dV$ with $u=B^2/(2\\mu_0)$.",
            "Mutual inductance $M$ couples two circuits: $\\mathcal{E}_2=-M dI_1/dt$. Transformers are mutual inductance with a shared core.",
        ],
        "RL transients need $L$ as a number. LC oscillations need $L$ and $C$ together. This is the magnetic twin of capacitance.",
        "If you know geometry, build $L$ from $N\\Phi_B/I$. If you know $L$ and $dI/dt$, Faraday is just $L|dI/dt|$. Store energy as $\\tfrac12 LI^2$.",
        lesson_figure(
            _solenoid_svg(),
            "A solenoid is a lumped inductor",
            "More turns per meter (larger $n$) means much larger $L$ because $L\\propto n^2$.",
        )
        + solved(1, "$L=0.50\\,\\mathrm{H}$, $dI/dt=2.0\\,\\mathrm{A/s}$. Find $|\\mathcal{E}|$.",
                 ["$\\mathcal{E}=-L dI/dt$.",
                  "$|\\mathcal{E}|=(0.50)(2.0)=1.0$.",
                  "Unit: volt."],
                 "$1.0\\,\\mathrm{V}$", "", "Easy")
        + solved(2, "Why does $L$ of a solenoid scale as $n^2$?",
                 ["$B\\propto n I$, so flux per turn $\\propto n$.",
                  "Number of turns $N=n\\ell$ adds another $n$.",
                  "$L=N\\Phi_B/I\\propto n^2$."],
                 "$L\\propto n^2$", "", "Medium")
        + solved(3, "Current $I$ in $L$. Energy? If $I$ doubles, energy?",
                 ["$U=\\tfrac12 LI^2$.",
                  "Doubling $I$ multiplies $U$ by 4.",
                  "That energy came from the battery fighting back emf while $I$ grew."],
                 "$U=\\tfrac12 LI^2$; $\\times 4$ if $I\\times 2$", "", "Hard")
        + _ican(ican5),
        ("Treating $L$ like $C$ in series/parallel formulas without thinking",
         "Uncoupled inductors combine like resistors, not like capacitors. Series $L$ add; parallel $1/L$ add."),
        ("Constant current still 'has inductance'",
         "The device still has $L$, but $\\mathcal{E}_L=0$ when $dI/dt=0$. Inductance shows up when you try to change $I$."),
        ican5,
        21,
    )

    ican6 = [
        "I can write $L\\dot I+RI=\\varepsilon$ and $\\tau=L/R$.",
        "I can use $I=0$ at $t=0^+$ and $I=\\varepsilon/R$ after a long time for growth.",
        "I can write decay $I=I_0 e^{-Rt/L}$.",
    ]
    c6 = concept_block(
        "6. RL circuits",
        [
            "Series battery, resistor, and inductor: Kirchhoff gives $L dI/dt+RI=\\varepsilon$. This is the same first-order linear DE as RC, with $I$ playing the role that $Q$ played.",
            "Time constant $\\tau=L/R$. For $L=0.20\\,\\mathrm{H}$ and $R=10\\,\\Omega$, $\\tau=0.020\\,\\mathrm{s}$.",
            "Current growth from $I(0)=0$: $I(t)=(\\varepsilon/R)(1-e^{-t/\\tau})$. At $t=0^+$ the inductor is an open circuit ($I$ cannot jump). After a long time it is a wire and $I=\\varepsilon/R$.",
            "Decay with battery gone: $I=I_0 e^{-t/\\tau}$. Energy $\\tfrac12 LI^2$ becomes heat in $R$.",
            "The graphs match RC with a dictionary: $I$ in RL growth looks like $Q$ in RC charging; $V_L=L dI/dt$ looks like charging current — a decaying exponential.",
            "Do not import LC sinusoids here unless both $L$ and $C$ are present (Unit 8). RL is exponential, not oscillatory (ideal series RL with $R>0$).",
        ],
        "This is the last linear transient before LC. Switch problems again use two cartoons: open inductor at $0^+$, wire after a long time.",
        "Write $L\\dot I+RI=\\varepsilon$. Identify $\\tau=L/R$. Apply $I(0)$. After a long time set $\\dot I=0$. Sketch $1-e^{-t/\\tau}$ for growth.",
        lesson_figure(
            _rl_svg() + xy_graph(
                curves=[("#7c3aed", i_rl)],
                xlim=(0, 5), ylim=(0, 1.2), w=300, h=180, xlab="t/τ", ylab="I/(ε/R)",
            ),
            "Series RL and rising $I(t)$",
            "Same $1-e^{-t/\\tau}$ shape as charging $Q$, with $\\tau=L/R$.",
        )
        + solved(1, "$L=0.20\\,\\mathrm{H}$, $R=10\\,\\Omega$. Find $\\tau$.",
                 ["$\\tau=L/R$.",
                  "$0.20/10=0.020$.",
                  "Unit: seconds."],
                 "$0.020\\,\\mathrm{s}$", "", "Easy")
        + solved(2, "Growth from 0, battery $\\varepsilon$. $I(0^+)$ and $I(\\infty)$?",
                 ["Current cannot jump: $I(0^+)=0$ (open $L$).",
                  "After a long time $dI/dt=0$, so $I=\\varepsilon/R$ (wire $L$).",
                  "In between: $I=(\\varepsilon/R)(1-e^{-t/\\tau})$."],
                 "$0$ then $\\varepsilon/R$", "", "Medium")
        + solved(3, "Time to reach half of $\\varepsilon/R$ during growth.",
                 ["$1-e^{-t/\\tau}=1/2$.",
                  "$t=\\tau\\ln 2=(L/R)\\ln 2$.",
                  "Not $\\tau/2$."],
                 "$t=(L/R)\\ln 2$", "", "Hard")
        + _ican(ican6),
        ("Using $\\tau=RC$ on an RL circuit",
         "RL uses $L/R$. The reciprocal structure versus $RC$ is because $L$ is in the derivative term the way $C$ was in the $Q/C$ term."),
        ("Two cartoons again",
         "$t=0^+$: inductor open. Long time: inductor a wire. Those redraws solve most switch questions without solving the DE."),
        ican6,
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        ["Magnetic flux", "Faraday's law", "Lenz's law",
         "Motional emf", "Inductance", "RL circuits"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Maxwell, LC, Mixed FRQ
# ===========================================================================

def _u8_questions():
    return _pack([
        ("An ideal LC circuit oscillates at $\\omega=1/\\sqrt{LC}$. If $L=0.25\\,\\mathrm{H}$ and $C=1.0\\,\\mu\\mathrm{F}$, $\\omega=$",
         "$2.0\\times10^{3}\\,\\mathrm{rad/s}$",
         "$\\sqrt{LC}=\\sqrt{2.5\\times10^{-7}}=5.0\\times10^{-4}$, $\\omega=1/\\sqrt{LC}=2.0\\times10^{3}$.",
         ["$4.0\\times10^{6}\\,\\mathrm{rad/s}$", "$2.0\\times10^{-3}\\,\\mathrm{rad/s}$", "$1.0\\,\\mathrm{rad/s}$"]),
        ("The period is $T=2\\pi\\sqrt{LC}$. If $L=0.25\\,\\mathrm{H}$ and $C=1.0\\,\\mu\\mathrm{F}$, $T=$",
         "$\\pi\\times10^{-3}\\,\\mathrm{s}$",
         "$\\omega=1/\\sqrt{LC}=2.0\\times10^{3}\\,\\mathrm{rad/s}$, so $T=2\\pi/\\omega=\\pi\\times10^{-3}\\,\\mathrm{s}$.",
         ["$2.0\\times10^{3}\\,\\mathrm{s}$", "$2\\pi\\times10^{3}\\,\\mathrm{s}$", "0"]),
        ("Energy sloshes between $\\tfrac12 Q^2/C$ and $\\tfrac12 LI^2$. When $Q=0$, $|I|$ is",
         "maximum",
         "All energy is magnetic.",
         ["0", "equal to $Q/C$", "undefined"]),
        ("The DE $L\\ddot Q+Q/C=0$ is SHM in charge, analogous to $m\\ddot x+kx=0$ with $\\omega^2=1/(LC)$. This is the allowed spring analog in E&M.",
         "yes: LC $\\leftrightarrow$ mass-spring",
         "Dictionary: $Q\\leftrightarrow x$, $L\\leftrightarrow m$, $1/C\\leftrightarrow k$.",
         ["projectile motion", "Kepler $1/r^2$", "Gauss for gravity"]),
        ("If $Q=Q_m\\cos\\omega t$, then $I=-\\omega Q_m\\sin\\omega t$. Peak current is",
         "$\\omega Q_m=Q_m/\\sqrt{LC}$",
         "$I_m=\\omega Q_m$.",
         ["$Q_m$", "$Q_m RC$", "0"]),
        ("Maxwell added displacement current $I_d=\\varepsilon_0 d\\Phi_E/dt$ to Ampere's law so that $\\oint\\vec{B}\\cdot d\\vec{\\ell}=\\mu_0(I_c+I_d)$. Between charging capacitor plates, $I_d$ equals",
         "the conduction current in the wires",
         "Charge conservation: $I_d=\\dot Q=I_c$.",
         ["0", "$\\varepsilon/R$ always after a long time", "the magnetic flux"]),
        ("For parallel plates, $\\Phi_E=EA$ and $E=\\sigma/\\varepsilon_0=Q/(A\\varepsilon_0)$, so $\\varepsilon_0 d\\Phi_E/dt=$",
         "$dQ/dt$",
         "That is $I_d$.",
         ["0", "$Q/\\varepsilon_0$", "$EA$"]),
        ("Displacement current exists even in empty space when",
         "$\\vec{E}$ is changing",
         "No need for a material.",
         ["$B$ is static and $E$ is static", "only inside copper", "only if $R=0$"]),
        ("Ampere–Maxwell is required so that the total current (conduction plus displacement) is continuous. That means",
         "conduction current can stop at a plate while $I_d=\\dot Q$ continues the current through the gap",
         "An Amperian loop's surface can be stretched through the gap; $I_d$ keeps $\\oint B\\cdot d\\ell=\\mu_0(I_c+I_d)$ consistent.",
         ["charge is created", "Gauss for $E$ is false", "Faraday is false"]),
        ("In SI, $I_d=\\varepsilon_0 d\\Phi_E/dt$ has units of",
         "amperes",
         "Same as $I_c$.",
         ["volts", "tesla", "webers"]),
        ("Electromagnetic waves in vacuum travel at $c=1/\\sqrt{\\mu_0\\varepsilon_0}\\approx$",
         "$3.0\\times10^{8}\\,\\mathrm{m/s}$",
         "Maxwell's prediction.",
         ["$3.0\\times10^{6}\\,\\mathrm{m/s}$", "$331\\,\\mathrm{m/s}$", "infinite"]),
        ("In a plane EM wave, $\\vec{E}$, $\\vec{B}$, and the propagation direction are",
         "mutually perpendicular ($E=cB$ in vacuum)",
         "Transverse wave.",
         ["all parallel", "$E$ longitudinal only", "$B=0$"]),
        ("A radio wave is a traveling oscillation of $\\vec{E}$ and $\\vec{B}$ produced by",
         "accelerating charges (changing currents in an antenna)",
         "Static charges do not radiate.",
         ["a bar magnet at rest", "a charged capacitor sitting forever at constant $Q$", "a DC solenoid with constant $I$"]),
        ("Qualitatively, Faraday says a changing $B$ makes circling $E$; Ampere–Maxwell says a changing $E$ makes circling $B$. Together they",
         "sustain a wave that does not need a medium",
         "The EM wave bootstrap.",
         ["forbid waves", "require air", "cancel Gauss"]),
        ("The Poynting vector $\\vec{S}=\\vec{E}\\times\\vec{B}/\\mu_0$ points in the",
         "direction of energy flow (propagation)",
         "Qualitative AP C idea.",
         ["direction of $\\vec{E}$ only", "direction of $\\vec{B}$ only", "toward decreasing $V$ always"]),
        ("A particle in crossed uniform $\\vec{E}$ and $\\vec{B}$ (both constant) with $\\vec{v}\\perp$ both can have $qE=qvB$, so $v=$",
         "$E/B$",
         "Velocity selector.",
         ["$B/E$", "$EB$", "0 only"]),
        ("A region with $E$ between plates and $B$ into the page: a charge that goes straight must satisfy that balance. If $v$ is smaller than $E/B$, the electric force",
         "wins (path curves toward the electric force)",
         "Compare $qE$ and $qvB$.",
         ["always loses", "is zero", "does no work? It does work, unlike $qvB$"]),
        ("Faraday + Gauss on a hybrid FRQ: flux of $E$ through a Gaussian sphere still equals $q_{\\mathrm{enc}}/\\varepsilon_0$ even if a $B$ field is present, because",
         "Gauss for $E$ cares about charge, not about $B$",
         "Different Maxwell equation.",
         ["$B$ cancels $E$", "Gauss fails when $B\\neq 0$", "you must use Ampere instead"]),
        ("A loop in changing $B$ plus a static $E$ of a nearby point charge: net emf is still $-d\\Phi_B/dt$ because the electrostatic $E$ is conservative and",
         "contributes 0 to $\\oint E\\cdot d\\ell$",
         "Only the induced nonconservative $E$ survives the loop integral.",
         ["doubles Faraday", "cancels Faraday", "makes $\\Phi_B=q/\\varepsilon_0$"]),
        ("Work by electric vs magnetic forces: in a velocity selector $qE$ does",
         "work (can change $K$ if the path has a component along $E$)",
         "Magnetic part still does none.",
         ["no work ever", "all the centripetal work", "negative work equal to $qvB$"]),
        ("On AP C, a calculator number without a derived expression often earns",
         "fewer points than a symbolic derivation with a boxed expression",
         "Show the law, then substitute.",
         ["more points always", "zero if any number appears", "credit only for the calculator"]),
        ("A good habit: keep $\\varepsilon_0$, $\\mu_0$, $k$ symbolic until the last line unless the problem gives numbers and asks for a numerical value. Then",
         "substitute once, with units",
         "Avoid premature rounding.",
         ["round every factor to 1", "drop $\\pi$", "replace $\\varepsilon_0$ by 1 always"]),
        ("If an FRQ says 'express your answer in terms of $Q$, $R$, $\\varepsilon_0$', using $k$ without converting $k=1/(4\\pi\\varepsilon_0)$ can",
         "lose the match to the allowed variables",
         "Translate.",
         ["earn extra credit", "be required", "replace Gauss"]),
        ("Checking dimensions: $1/\\sqrt{LC}$ must be",
         "rad/s (or 1/s)",
         "Time constant check.",
         ["farads", "henry", "coulombs"]),
        ("A numeric $E=9.0\\times10^{9}q/r^2$ used $k$. The same $E$ as $q/(4\\pi\\varepsilon_0 r^2)$ is preferred when the rubric lists",
         "$\\varepsilon_0$",
         "Same physics, different letters.",
         ["$k$ only", "$\\mu_0$ only", "$g$"]),
        ("To justify $E=kQ/r^2$ outside a ball you must cite",
         "Gauss's law plus spherical symmetry (Gaussian sphere)",
         "Not 'because Coulomb said so' if the charge is spread out — though the result matches a point.",
         ["Faraday's law", "Ampere's law", "Ohm's law"]),
        ("To justify $\\mathcal{E}=B\\ell v$ on a sliding bar you may cite either",
         "Faraday $d(BA)/dt$ or $\\int(\\vec{v}\\times\\vec{B})\\cdot d\\vec{\\ell}$",
         "Both are acceptable if set up.",
         ["Gauss for $E$ only", "Biot–Savart only", "LC energy only"]),
        ("To justify $B=\\mu_0 n I$ you cite",
         "Ampere's law with a rectangular loop and $B_{\\mathrm{out}}\\approx 0$",
         "Symmetry paragraph required.",
         ["Coulomb", "Gauss for $E$", "Ohm"]),
        ("A justification that only restates the answer ('$E$ is $kQ/r^2$ because that is the field') earns",
         "little or no justification credit",
         "Name the law and the symmetry/surface.",
         ["full credit always", "calculator credit", "Lenz credit"]),
        ("If a Gaussian surface is a cube around a point charge, you may still say flux is $q/\\varepsilon_0$, but you may not claim $|E|=q/(6L^2)$ as the field at every point because",
         "$|E|$ is not constant on the cube",
         "True vs useful Gauss.",
         ["Gauss is false", "the cube is not closed", "$q=0$"]),
        ("LC: if $C$ doubles, $\\omega$ is multiplied by",
         "$1/\\sqrt{2}$",
         "$\\omega\\propto 1/\\sqrt{C}$.",
         ["2", "$\\sqrt{2}$", "1/2"]),
        ("Maximum $U_E$ in LC equals maximum $U_B$ equals",
         "the total energy $Q_m^2/(2C)$",
         "They trade; sum is constant (ideal).",
         ["0", "$I_m R$", "$\\varepsilon^2/R$"]),
        ("Displacement current through a capacitor is largest when $|dQ/dt|$ is largest, i.e. when",
         "$|I|$ in the wires is largest",
         "$I_d=I_c$.",
         ["$Q$ is largest and $I=0$", "after a long time on DC", "$B=0$ everywhere"]),
        ("In vacuum, $E=cB$ for a plane wave. If $E=3.0\\,\\mathrm{N/C}$, $B=$",
         "$1.0\\times10^{-8}\\,\\mathrm{T}$",
         "$B=E/c=3/(3\\times10^8)=10^{-8}\\,\\mathrm{T}$.",
         ["$3.0\\,\\mathrm{T}$", "$9.0\\times10^{8}\\,\\mathrm{T}$", "0"]),
        ("A velocity selector with $E=200\\,\\mathrm{N/C}$, $B=0.050\\,\\mathrm{T}$ selects $v=$",
         "$4.0\\times10^{3}\\,\\mathrm{m/s}$",
         "$v=E/B=200/0.050=4000\\,\\mathrm{m/s}$.",
         ["10 m/s", "$4.0\\times10^{-4}\\,\\mathrm{m/s}$", "0"]),
        ("Symbolic first: $C=\\kappa\\varepsilon_0 A/d$, then numbers. If $\\kappa$ is unknown, you",
         "leave $\\kappa$ in the answer",
         "Do not invent 1.",
         ["set $\\kappa=0$", "set $\\kappa=\\varepsilon_0$", "drop $A$"]),
        ("An FRQ asks for $E$ inside a uniform ball. The expected path is Gaussian sphere, $q_{\\mathrm{enc}}=Q r^3/R^3$, $E 4\\pi r^2=q_{\\mathrm{enc}}/\\varepsilon_0$. Skipping the $q_{\\mathrm{enc}}$ step and writing $kQ/r^2$ is",
         "incorrect inside",
         "That is the exterior formula.",
         ["fine always", "required by Faraday", "Ohm's law"]),
        ("An FRQ asks for induced $E$ around a solenoid. Faraday on a circle, not Gauss, is the tool because",
         "you need $\\oint E\\cdot d\\ell=-d\\Phi_B/dt$",
         "Changing $B$, circling $E$.",
         ["Gauss gives circling $E$", "Ampere without Maxwell gives $E$", "Ohm gives $E=IR$ in empty space"]),
        ("Calculator: $e^{-1}=0.367879$. AP often accepts $0.37$ or $1/e$. Showing $e^{-t/RC}$ before the number",
         "protects method points if the arithmetic slips",
         "Symbolic then numeric.",
         ["is forbidden", "replaces the answer line", "requires a graphing window"]),
        ("If $L$ and $C$ are both present with $R=0$, do not use $\\tau=RC$ or $\\tau=L/R$ as the time scale; use",
         "$T=2\\pi\\sqrt{LC}$",
         "Oscillation, not exponential.",
         ["$RC$", "$L/R$", "$\\ell/v$ from projectiles"]),
        ("A mixed part (a) Gauss for $E$ of a sheet, part (b) Faraday as $B$ through a loop on the sheet region changes: the $E$ from Gauss is",
         "electrostatic (or slowly varying) while Faraday's emf is from $d\\Phi_B/dt$",
         "Name which field you are finding.",
         ["the same circling $E$ as Faraday always", "zero because of $B$", "Ohmic"]),
        ("LC energy conservation: $Q^2/(2C)+LI^2/2=$ constant. Differentiating and using $I=\\dot Q$ recovers",
         "the DE $L\\ddot Q+Q/C=0$",
         "Energy method = Newton method.",
         ["Gauss", "Coulomb only", "projectile range"]),
        ("Maxwell consistency: Ampere–Maxwell plus Gauss for $E$ recovers charge conservation. That is why $I_d$ was needed. On AP C you should be able to say",
         "displacement current keeps the current continuous when $Q$ piles up on a plate ($I_d=\\dot Q$ in the gap)",
         "Integral form: $\\oint B\\cdot d\\ell=\\mu_0(I_c+\\varepsilon_0 d\\Phi_E/dt)$ matches $I_c$ in the wire to $\\dot Q$ on the plate. No nabla needed.",
         ["charge is not conserved", "Faraday contradicts Gauss", "solenoids cannot have $B$"]),
        ("EM wave qualitative: $E$ and $B$ oscillate in phase in a plane wave in vacuum, meaning they",
         "reach maxima at the same $x,t$",
         "Not $E$ max when $B=0$.",
         ["are $90^\\circ$ out of phase like $LC$'s $Q$ and $I$", "never exist together", "point the same way"]),
        ("Combining $E$ and $B$: cyclotron plus a weak $E$ along $B$ accelerates $v_\\parallel$ while $r=mv_\\perp/(qB)$ uses only $v_\\perp$. This is not an orbit under gravity.",
         "true",
         "Keep $v_\\perp$ and $v_\\parallel$ separate.",
         ["treat as projectile $y=v_0 t-\\tfrac12 gt^2$", "use Kepler", "set $B=E$ always"]),
        ("When a problem gives $k=9\\times 10^9$ and wants a number, using $1/(4\\pi\\varepsilon_0)$ without a value for $\\varepsilon_0$ can leave you stuck. Then",
         "use the given $k$",
         "Honor the given constants.",
         ["invent $g=10$", "set $k=1$", "skip the question"]),
        ("AP Stretch: LC with $Q=Q_m\\sin(\\omega t)$ and $\\omega=1/\\sqrt{LC}$, so $Q(0)=0$. If $L=1.0\\,\\mathrm{H}$, $C=1.0\\,\\mu\\mathrm{F}$, and $Q_m=5.0\\,\\mu\\mathrm{C}$, the current at $t=0$ is",
         "$5.0\\,\\mathrm{mA}$",
         "$I=\\omega Q_m\\cos(\\omega t)$, so $I(0)=\\omega Q_m$. $\\omega=1.0\\times10^{3}\\,\\mathrm{rad/s}$, hence $I(0)=5.0\\,\\mathrm{mA}$.",
         ["0", "$5.0\\,\\mathrm{A}$", "$5.0\\,\\mu\\mathrm{A}$"]),
        ("AP Stretch: Between plates of a charging capacitor, Ampere–Maxwell on a loop of radius $r<R_{\\mathrm{plate}}$ with uniform $I_d$ over the gap gives $B=$",
         "$\\mu_0 I_d r/(2\\pi R_{\\mathrm{plate}}^2)$ analog of the wire interior if $I_d$ is uniform over the plate area",
         "Enclosed displacement current fraction $\\pi r^2/(\\pi R^2)$.",
         ["$\\mu_0 n I$", "0 because no conduction current pierces a surface through the gap? That was the paradox; $I_d$ fixes it", "$\\sigma/\\varepsilon_0$"]),
        ("AP Stretch: Speed $c=1/\\sqrt{\\mu_0\\varepsilon_0}$. Combining Faraday $E=B\\ell v$ ideas with Ampere on a wave front is beyond typical AP algebra, but you must know $c$ is",
         "fixed by $\\varepsilon_0$ and $\\mu_0$, independent of frequency in vacuum",
         "No ether wind on AP C.",
         ["$\\sqrt{k/m}$", "$E/B$ only for DC", "$\\ell/t$ of a projectile"]),
        ("AP Stretch: Crossed uniform $E=400\\,\\mathrm{N/C}$ and $B=0.20\\,\\mathrm{T}$. Selector speed is $E/B=2.0\\times10^{3}\\,\\mathrm{m/s}$. A proton with $v=1.0\\times10^{3}\\,\\mathrm{m/s}$ (electric and magnetic forces opposing) has $|F_{\\mathrm{net}}|/e$ equal to",
         "$200\\,\\mathrm{N/C}$",
         "$|E-vB|=|400-(1.0\\times10^{3})(0.20)|=200\\,\\mathrm{N/C}$.",
         ["$400\\,\\mathrm{N/C}$", "0", "$800\\,\\mathrm{N/C}$"]),
        ("AP Stretch: Justify $E=0$ inside a conductor in electrostatics using Gauss: any Gaussian surface in the metal has $\\Phi=0$ because $E=0$, hence $q_{\\mathrm{enc}}=0$. The $E=0$ starting point itself is from",
         "the definition of electrostatic equilibrium (no ongoing drift of free charge)",
         "Then Gauss locates the charge on surfaces.",
         ["Faraday requiring $d\\Phi_B/dt=0$ only", "Ampere requiring $I=0$ only", "Ohm requiring $R=0$"]),
        ("AP Stretch: Uniform insulating ball $Q=4.0\\,\\mathrm{nC}$, $R=0.20\\,\\mathrm{m}$. At $r=0.10\\,\\mathrm{m}$, Gauss gives $E=kQr/R^3$. A concentric loop of that same $r$ has $B_\\perp$ drop from $0.80\\,\\mathrm{T}$ to $0$ in $4.0\\,\\mathrm{ms}$. The pair $(E,|\\mathcal{E}|)$ is",
         "$450\\,\\mathrm{N/C}$ and $2\\pi\\,\\mathrm{V}$",
         "$E=(9.0\\times10^{9})(4.0\\times10^{-9})(0.10)/(0.20)^3=450\\,\\mathrm{N/C}$. Faraday: $\\Phi_B=0.80\\pi (0.10)^2=0.008\\pi\\,\\mathrm{Wb}$, $|\\mathcal{E}|=0.008\\pi/0.004=2\\pi\\,\\mathrm{V}$.",
         ["$900\\,\\mathrm{N/C}$ and $0$", "$kQ/r^2$ and $0.80\\,\\mathrm{V}$", "$0$ and $2\\pi\\,\\mathrm{V}$"]),
        ("AP Stretch: Infinite line $\\lambda=3.0\\,\\mu\\mathrm{C/m}$. Gauss (cylinder) at $r=0.030\\,\\mathrm{m}$ gives $E=2k\\lambda/r$. A concentric loop of that $r$ has $B_\\perp=0.50\\,\\mathrm{T}$ drop to $0$ in $2.0\\,\\mathrm{ms}$. The pair $(E,|\\mathcal{E}|)$ is",
         "$1.80\\times10^{6}\\,\\mathrm{N/C}$ and $0.225\\pi\\,\\mathrm{V}$",
         "$E=2(9.0\\times10^{9})(3.0\\times10^{-6})/0.030=1.80\\times10^{6}\\,\\mathrm{N/C}$. $\\Phi_B=0.50\\pi(0.030)^2$, $|\\mathcal{E}|=\\Phi_B/0.002=0.225\\pi\\,\\mathrm{V}$.",
         ["$2k\\lambda/r^2$ and $0$", "$0$ and $0.50\\,\\mathrm{V}$", "$\\sigma/\\varepsilon_0$ and $2\\pi\\,\\mathrm{V}$"]),
        ("AP Stretch: Parallel plates hold $Q=8.85\\,\\mathrm{nC}$ on $A=0.010\\,\\mathrm{m^2}$ ($\\varepsilon_0=8.85\\times10^{-12}$). Gauss (pillbox) gives $E=\\sigma/\\varepsilon_0$. A loop of area $0.010\\,\\mathrm{m^2}$ in the gap has $B_\\perp=0.20\\,\\mathrm{T}$ fall to $0$ in $2.0\\,\\mathrm{ms}$. The pair $(E,|\\mathcal{E}|)$ is",
         "$1.00\\times10^{5}\\,\\mathrm{N/C}$ and $1.0\\,\\mathrm{V}$",
         "$E=Q/(A\\varepsilon_0)=8.85\\times10^{-9}/(0.010\\times 8.85\\times10^{-12})=1.00\\times10^{5}\\,\\mathrm{N/C}$. Faraday: $|\\mathcal{E}|=(0.20)(0.010)/0.002=1.0\\,\\mathrm{V}$.",
         ["$8.85\\,\\mathrm{N/C}$ and $0$", "$\\sigma/\\varepsilon_0$ and $0.20\\,\\mathrm{V}$", "$0$ and $1.0\\,\\mathrm{V}$"]),
        ("AP Stretch: Coaxial cable $a=1.0\\,\\mathrm{mm}$, $b=4.0\\,\\mathrm{mm}$, length $\\ell=2.0\\,\\mathrm{m}$. Ampere gives $B=\\mu_0 I/(2\\pi r)$ between the conductors. If $I$ increases at $800\\,\\mathrm{A/s}$, Faraday on a loop spanning $a$ to $b$ along $\\ell$ gives $|\\mathcal{E}|=$",
         "$4.44\\times10^{-4}\\,\\mathrm{V}$",
         "$M=(\\mu_0 \\ell/2\\pi)\\ln(b/a)=(2.0\\times10^{-7})(2)\\ln 4\\approx 5.55\\times10^{-7}\\,\\mathrm{H}$, so $|\\mathcal{E}|=M\\,dI/dt\\approx 4.44\\times10^{-4}\\,\\mathrm{V}$.",
         ["$\\mu_0 I/(2\\pi a)$", "0", "$4.0\\,\\mathrm{V}$"]),
    ])


def build_unit8():
    title = "AP Physics C E&M Unit 8: Maxwell, LC, and Mixed FRQ"
    description = (
        "LC oscillations, displacement current, electromagnetic waves, mixed $E$ and $B$ FRQs, "
        "calculator-versus-symbolic habits, and justifications with Gauss and Faraday."
    )
    q_lc = sample_curve(lambda t: math.cos(t), 0, 4 * math.pi)
    i_lc = sample_curve(lambda t: -math.sin(t), 0, 4 * math.pi)

    ican1 = [
        "I can use $\\omega=1/\\sqrt{LC}$ and $T=2\\pi\\sqrt{LC}$.",
        "I can write $L\\ddot Q+Q/C=0$ and the energy trade $Q^2/(2C)\\leftrightarrow LI^2/2$.",
        "I can map LC to the mass-spring analog (the allowed SHM analog).",
    ]
    c1 = concept_block(
        "1. LC oscillations",
        [
            "An ideal inductor $L$ and capacitor $C$ with no resistor form an LC oscillator. Kirchhoff: $L\\dot I+Q/C=0$. With $I=\\dot Q$ this is $L\\ddot Q+Q/C=0$.",
            "That is simple harmonic motion for charge, the one allowed spring analog in this course: $Q\\leftrightarrow x$, $L\\leftrightarrow m$, $1/C\\leftrightarrow k$, so $\\omega=1/\\sqrt{LC}$.",
            "Period $T=2\\pi\\sqrt{LC}$. Example: $L=0.25\\,\\mathrm{H}$, $C=1.0\\,\\mu\\mathrm{F}$, $\\omega=2.0\\times10^{3}\\,\\mathrm{rad/s}$, $T=\\pi\\,\\mathrm{ms}$.",
            "Energy sloshes from electric $\\tfrac12 Q^2/C$ to magnetic $\\tfrac12 LI^2$ and back. When $Q=0$, current is maximum; when $I=0$, $|Q|$ is maximum.",
            "If $Q=Q_m\\cos\\omega t$, then $I=-\\omega Q_m\\sin\\omega t$ and $I_m=Q_m/\\sqrt{LC}$. Total energy $Q_m^2/(2C)$ is constant.",
            "Tiny resistance slowly drains the energy (damped oscillation). Large $R$ can overdamp. AP C mainly wants the ideal $\\omega$ and the energy trade.",
        ],
        "This is how radios tune and how you see both $C$ and $L$ in one DE. It is not a pendulum lab and not a gravitational orbit.",
        "Write the loop with $L\\dot I$ and $Q/C$. Convert to $\\ddot Q$. Read $\\omega=1/\\sqrt{LC}$. Sketch $Q$ as cosine and $I$ as sine, $90^\\circ$ out of phase.",
        lesson_figure(
            _lc_svg() + xy_graph(
                curves=[("#1d4ed8", q_lc), ("#b91c1c", i_lc)],
                xlim=(0, 12.6), ylim=(-1.4, 1.4), w=320, h=180, xlab="ωt", ylab="Q, I",
            ),
            "LC loop and $Q$ (blue) versus $I$ (red)",
            "Charge and current are a quarter-cycle apart, like $x$ and $v$ in mass-spring SHM.",
        )
        + solved(1, "$L=0.25\\,\\mathrm{H}$, $C=1.0\\,\\mu\\mathrm{F}$. Find $\\omega$.",
                 ["$\\omega=1/\\sqrt{LC}$.",
                  "$LC=(0.25)(1.0\\times10^{-6})=2.5\\times10^{-7}$.",
                  "$\\sqrt{LC}=5.0\\times10^{-4}$, so $\\omega=2.0\\times10^{3}\\,\\mathrm{rad/s}$."],
                 "$2.0\\times10^{3}\\,\\mathrm{rad/s}$", "", "Easy")
        + solved(2, "When is capacitor energy maximum in an LC cycle? When is inductor energy maximum?",
                 ["$U_E=Q^2/(2C)$ is max at max $|Q|$, which is when $I=0$.",
                  "$U_B=\\tfrac12 LI^2$ is max at max $|I|$, which is when $Q=0$.",
                  "They trade; sum is constant."],
                 "$U_E$ max at $I=0$; $U_B$ max at $Q=0$", "", "Medium")
        + solved(3, "From $Q=Q_m\\cos\\omega t$, find $I_m$ in terms of $Q_m,L,C$.",
                 ["$I=\\dot Q=-\\omega Q_m\\sin\\omega t$.",
                  "$I_m=\\omega Q_m$.",
                  "$\\omega=1/\\sqrt{LC}$ so $I_m=Q_m/\\sqrt{LC}$."],
                 "$I_m=Q_m/\\sqrt{LC}$", "", "Hard")
        + _ican(ican1),
        ("Using $\\tau=RC$ as the LC time scale",
         "There is no exponential $\\tau$ in ideal LC. The time scale is the period $2\\pi\\sqrt{LC}$."),
        ("Dictionary with mass-spring",
         "Only this analog is invited: $L$ like mass, $1/C$ like $k$, $Q$ like $x$. Do not import $g$ or orbits."),
        ican1,
        1,
    )

    ican2 = [
        "I can write $I_d=\\varepsilon_0 d\\Phi_E/dt$ and $I_d=\\dot Q$ between plates.",
        "I can state Ampere–Maxwell $\\oint B\\cdot d\\ell=\\mu_0(I_c+I_d)$.",
        "I can explain why $I_d$ lets an Amperian surface pass through a capacitor gap.",
    ]
    c2 = concept_block(
        "2. Maxwell displacement current idea",
        [
            "Ampere's magnetostatics law $\\oint\\vec{B}\\cdot d\\vec{\\ell}=\\mu_0 I_{\\mathrm{enc}}$ fails when current piles onto a capacitor plate: a soap-film surface through the wire sees $I$, but a stretched surface through the gap sees $I=0$, even though the loop is the same.",
            "Maxwell's fix is displacement current $I_d=\\varepsilon_0 d\\Phi_E/dt$. Between plates, $\\Phi_E=EA$ and $E=Q/(A\\varepsilon_0)$, so $I_d=\\dot Q$, matching the wire's conduction current $I_c$.",
            "The unified law is $\\oint\\vec{B}\\cdot d\\vec{\\ell}=\\mu_0(I_c+I_d)$. Changing electric flux makes $B$ just as a real current does.",
            "Displacement current can exist in empty space; no material is required, only $\\partial\\vec{E}/\\partial t$.",
            "This is the missing piece that makes Maxwell's equations consistent with charge conservation: when $Q$ accumulates, $I_d$ continues the 'current' through the gap.",
            "After a long time on DC, $\\dot Q=0$ so $I_d=0$ in the gap, matching $I=0$ in the wires.",
        ],
        "Without $I_d$ you cannot have electromagnetic waves, and Ampere's law is ambiguous for capacitors. This is the last Maxwell patch AP C expects in words and in $I_d=\\dot Q$.",
        "When a surface cuts a wire, count $I_c$. When it cuts a charging gap, count $I_d=\\varepsilon_0 d\\Phi_E/dt=\\dot Q$. They agree for the same loop.",
        lesson_figure(
            _disp_current_svg(),
            "Conduction current in the wires, displacement current in the gap",
            "An Amperian loop around the left wire can have its surface stretched through the gap; $I_d$ keeps $I_{\\mathrm{enc}}$ the same.",
        )
        + solved(1, "A capacitor is charging with $I=3.0\\,\\mathrm{mA}$ in the wires. What is $I_d$ in the gap?",
                 ["Charge conservation: $\\dot Q=I$.",
                  "$I_d=\\varepsilon_0 d\\Phi_E/dt=\\dot Q$.",
                  "$I_d=3.0\\,\\mathrm{mA}$."],
                 "$3.0\\,\\mathrm{mA}$", "", "Easy")
        + solved(2, "Show $I_d=\\dot Q$ for parallel plates.",
                 ["$E=Q/(A\\varepsilon_0)$ between plates (ideal).",
                  "$\\Phi_E=EA=Q/\\varepsilon_0$.",
                  "$I_d=\\varepsilon_0 d\\Phi_E/dt=\\dot Q$."],
                 "$I_d=\\dot Q$", "", "Medium")
        + solved(3, "Why did magnetostatics Ampere need this patch for a charging capacitor?",
                 ["The same closed loop can bound a surface cut by the wire ($I_{\\mathrm{enc}}=I$) or stretched through the gap ($I_{\\mathrm{enc}}=0$).",
                  "Those cannot both equal $\\oint B\\cdot d\\ell/\\mu_0$.",
                  "$I_d$ in the gap restores uniqueness and matches $I$."],
                 "surfaces would disagree without $I_d$", "", "Hard")
        + _ican(ican2),
        ("Setting $I_d=0$ in a charging gap because 'there is no charge flowing through empty space'",
         "That was exactly the paradox. Changing $\\Phi_E$ counts as a current for Ampere."),
        ("Match $I_d$ to $\\dot Q$",
         "If you can name the wire current, you already know $I_d$ in an ideal gap. Compute $\\varepsilon_0 d\\Phi_E/dt$ only when asked to show the identity."),
        ican2,
        6,
    )

    ican3 = [
        "I can state $c=1/\\sqrt{\\mu_0\\varepsilon_0}$ and $E=cB$ for a plane wave.",
        "I can say $\\vec{E}$, $\\vec{B}$, and $\\vec{v}$ are mutually perpendicular.",
        "I can name accelerating charges as the source of EM waves.",
    ]
    c3 = concept_block(
        "3. Electromagnetic waves qualitative",
        [
            "Faraday: a changing $\\vec{B}$ produces a circling $\\vec{E}$. Ampere–Maxwell: a changing $\\vec{E}$ produces a circling $\\vec{B}$. Those two facts can bootstrap a traveling wave of $\\vec{E}$ and $\\vec{B}$ that needs no medium.",
            "In vacuum the speed is $c=1/\\sqrt{\\mu_0\\varepsilon_0}\\approx 3.0\\times10^{8}\\,\\mathrm{m/s}$, independent of frequency.",
            "A plane wave is transverse: $\\vec{E}\\perp\\vec{B}\\perp$ the propagation direction, with $E=cB$. The Poynting vector $\\vec{E}\\times\\vec{B}/\\mu_0$ points along the energy flow.",
            "In a plane wave in vacuum, $E$ and $B$ oscillate in phase: they peak together, unlike $Q$ and $I$ in LC which are a quarter-cycle apart.",
            "Sources are accelerating charges — antennas with changing currents — not a static point charge and not a DC solenoid with constant $I$.",
            "Light, radio, and microwaves are the same kind of wave at different frequencies. AP C wants the structure, not a full derivation of the wave equation.",
        ],
        "This is why Maxwell's equations are one subject instead of eight disconnected formulas. Waves are Gauss, Faraday, and Ampere–Maxwell talking to each other.",
        "Memorize $c$, the three perpendiculars, $E=cB$, and 'accelerating charges radiate'. If a problem gives $E$, get $B=E/c$.",
        lesson_figure(
            _em_wave_svg(),
            "A snapshot of $E_y$ versus $x$ for a wave traveling in $+x$",
            "A $B_z$ oscillation (not drawn as a second curve here) would peak at the same places, with $B=E/c$.",
        )
        + solved(1, "What is $c$ in terms of $\\varepsilon_0$ and $\\mu_0$?",
                 ["Maxwell: $c=1/\\sqrt{\\mu_0\\varepsilon_0}$.",
                  "Numerically about $3.0\\times10^{8}\\,\\mathrm{m/s}$.",
                  "Vacuum, any frequency."],
                 "$c=1/\\sqrt{\\mu_0\\varepsilon_0}$", "", "Easy")
        + solved(2, "$E=3.0\\,\\mathrm{N/C}$ in a plane wave. Find $B$.",
                 ["$E=cB$.",
                  "$B=E/c=3.0/(3.0\\times10^{8})$.",
                  "$B=1.0\\times10^{-8}\\,\\mathrm{T}$."],
                 "$1.0\\times10^{-8}\\,\\mathrm{T}$", "", "Medium")
        + solved(3, "Why does a charged capacitor sitting forever at constant $Q$ not radiate an EM wave, while an AC antenna does?",
                 ["Constant $Q$ means constant $E$ in the gap (ideal DC).",
                  "No $\\partial E/\\partial t$ or $\\partial B/\\partial t$ to bootstrap a wave.",
                  "An antenna has accelerating charges / changing $I$, so changing fields that launch a wave."],
                 "need changing fields (accelerating charges)", "", "Hard")
        + _ican(ican3),
        ("Thinking $E$ and $B$ in a wave are a quarter-cycle out of phase like LC",
         "LC's $Q$ and $I$ are quadrature because one is the derivative of the other in a lumped circuit. A traveling plane wave has $E$ and $B$ in phase."),
        ("Three arrows",
         "Draw $\\vec{E}$, $\\vec{B}$, and $\\vec{c}$ as a mutually perpendicular triad. If two are parallel, it is not a vacuum plane wave."),
        ican3,
        11,
    )

    ican4 = [
        "I can use $v=E/B$ in a velocity selector.",
        "I can keep Gauss for $E$ and Faraday for emf as separate laws in one problem.",
        "I can split $v_\\perp$ and $v_\\parallel$ in combined $E$ and $B$ motion.",
    ]
    c4 = concept_block(
        "4. Combining E and B FRQ",
        [
            "The Lorentz force $q(\\vec{E}+\\vec{v}\\times\\vec{B})$ is the full electromagnetic force on a point charge. Magnetic pieces do no work; electric pieces can.",
            "Velocity selector: crossed $\\vec{E}$ and $\\vec{B}$ with $qE=qvB$ gives a straight-line speed $v=E/B$. Example: $E=200\\,\\mathrm{N/C}$, $B=0.050\\,\\mathrm{T}$, $v=4.0\\times10^{3}\\,\\mathrm{m/s}$.",
            "If $v<E/B$, the electric force wins and the path curves toward the electric force. If $v>E/B$, magnetic force wins.",
            "A hybrid FRQ might use Gauss to find $E$ of a sheet in part (a) and Faraday to find emf when $B$ through a loop changes in part (b). Name the law each time; $B$ does not cancel Gauss.",
            "If $\\vec{E}\\parallel\\vec{B}$, motion along $B$ is $a_\\parallel=qE/m$ while the perpendicular motion is cyclotron motion at $\\omega=qB/m$. Do not treat this as a gravity projectile.",
            "Electrostatic $\\oint\\vec{E}\\cdot d\\vec{\\ell}=0$ still holds for the Coulomb field of static charges, even if a changing $B$ adds a nonconservative induced $E$. Around a loop, only Faraday's piece survives.",
        ],
        "The exam mixes units on purpose. Your job is to label which Maxwell equation or force law each part needs, then not use a projectile or orbit formula.",
        "Write $F=qE$ and $F=qvB$ as competing magnitudes when both fields are uniform. For field-finding, write Gauss or Faraday in words before the algebra.",
        lesson_figure(
            _lorentz_svg(),
            "Magnetic force in a region that might also have $\\vec{E}$",
            "Add $q\\vec{E}$ as a second arrow. Straight motion means the two forces cancel.",
        )
        + solved(1, "$E=200\\,\\mathrm{N/C}$, $B=0.050\\,\\mathrm{T}$, crossed. Selector speed?",
                 ["$qE=qvB$.",
                  "$v=E/B=200/0.050$.",
                  "$v=4.0\\times10^{3}\\,\\mathrm{m/s}$."],
                 "$4.0\\times10^{3}\\,\\mathrm{m/s}$", "", "Easy")
        + solved(2, "A Gaussian sphere around a point charge sits in a region that also has a uniform $B$. Net electric flux?",
                 ["Gauss for $E$: $\\Phi_E=q/\\varepsilon_0$.",
                  "$B$ does not appear.",
                  "The flux is still $q/\\varepsilon_0$."],
                 "$q/\\varepsilon_0$", "", "Medium")
        + solved(3, "$\\vec{E}$ and $\\vec{B}$ both along $+z$, proton with $v_x$ and $v_z$. Describe the motion.",
                 ["$v_z$ accelerates: $a_z=eE/m$.",
                  "$v_x,v_y$ cyclotron about $z$ at $\\omega=eB/m$.",
                  "Helix with increasing pitch, not a gravitational parabola."],
                 "helix plus $a_\\parallel=qE/m$", "", "Hard")
        + _ican(ican4),
        ("Using $y=v_0 t-\\tfrac12 gt^2$ because the path 'looks curved'",
         "Curvature here is $qvB$ or $qE$, not $g$, unless the problem includes gravity explicitly."),
        ("One law per part",
         "In the margin write 'Gauss', 'Faraday', or 'Lorentz' before you write symbols. Mixed FRQs punish unlabeled algebra."),
        ican4,
        16,
    )

    ican5 = [
        "I can derive symbolically, then substitute numbers once.",
        "I can match the answer's letters to the allowed-variable list.",
        "I can keep $1-e^{-t/\\tau}$ visible beside a decimal.",
    ]
    c5 = concept_block(
        "5. Calculator vs symbolic habits",
        [
            "AP Physics C scores method. A boxed expression in the allowed variables often outranks a calculator dump with no law named.",
            "Keep $\\varepsilon_0$, $\\mu_0$, $Q$, $R$, $d$ symbolic until the last line unless the problem hands you $k=9.0\\times10^9$ and asks for a number.",
            "If the rubric lists $\\varepsilon_0$ and you used $k$, convert $k=1/(4\\pi\\varepsilon_0)$ so the letters match.",
            "Check dimensions before you box: $1/\\sqrt{LC}$ is rad/s, $RC$ is seconds, $B\\ell v$ is volts, $q/\\varepsilon_0$ is flux.",
            "For exponentials, write $1-e^{-1}$ or $1/e$ as well as $0.632$ or $0.368$. Exact form shows you knew $t=\\tau$.",
            "Do not round every factor to $1$. Keep one extra digit until the end, then match significant figures to the given data.",
        ],
        "Many lost points are arithmetic or letter-list mismatches, not physics. This concept is how you stop donating those points.",
        "Order: law, symbol algebra, allowed-variable check, then one substitution with units. Box the expression, then the number if asked.",
        lesson_figure(
            xy_graph(
                curves=[("#b91c1c", sample_curve(lambda t: 1 - math.exp(-t), 0, 4))],
                dashes=[("h", 0.632, "1-1/e")],
                xlim=(0, 4), ylim=(0, 1.2), w=300, h=180, xlab="t/τ", ylab="Q/Qmax",
            ),
            "Leave $1-1/e$ on the page, not only $0.63$",
            "The horizontal mark is the exact charging fraction at $t=\\tau$.",
        )
        + solved(1, "An FRQ says 'in terms of $Q,R,\\varepsilon_0$'. You found $E=kQ/R^2$. What should you write?",
                 ["$k=1/(4\\pi\\varepsilon_0)$.",
                  "$E=Q/(4\\pi\\varepsilon_0 R^2)$.",
                  "Now the letters match the list."],
                 "$Q/(4\\pi\\varepsilon_0 R^2)$", "", "Easy")
        + solved(2, "You need $1-e^{-1}$ numerically. What two things should appear?",
                 ["The exact $1-1/e$ (or $1-e^{-1}$).",
                  "A decimal such as $0.632$.",
                  "Method points survive a rounding slip."],
                 "exact form and a decimal", "", "Medium")
        + solved(3, "Show that $B\\ell v$ has units of volts.",
                 ["$[B]=\\mathrm{T}=\\mathrm{N\\cdot s/(C\\cdot m)}$.",
                  "$[B\\ell v]=\\mathrm{N\\cdot m/C}=\\mathrm{J/C}=\\mathrm{V}$.",
                  "Also $\\mathrm{T\\cdot m^2/s}=\\mathrm{Wb/s}=\\mathrm{V}$."],
                 "units check as volts", "", "Hard")
        + _ican(ican5),
        ("Boxing only a calculator number on a 'derive' prompt",
         "The word 'derive' means a law plus algebra. The number is the last line, not the only line."),
        ("Allowed-variable checklist",
         "Before you box, underline every letter in your answer and every letter in the prompt's list. Extra letters ($k$ vs $\\varepsilon_0$) are a mismatch."),
        ican5,
        21,
    )

    ican6 = [
        "I can justify exterior $E$ of a ball with Gauss plus spherical symmetry.",
        "I can justify $\\mathcal{E}=-d\\Phi_B/dt$ with Faraday and a named surface.",
        "I can write a symmetry sentence so $E$ or $B$ may be factored out of an integral.",
    ]
    c6 = concept_block(
        "6. Justifying with Gauss and Faraday",
        [
            "A justification names a law and a surface or path, plus a symmetry sentence that lets you pull $E$ or $B$ out of an integral.",
            "Gauss example: 'Spherical symmetry implies $\\vec{E}$ is radial and $|E|$ depends only on $r$. On a Gaussian sphere of radius $r$, $\\vec{E}\\parallel\\hat{n}$ and $|E|$ is constant, so $E\\cdot 4\\pi r^2=q_{\\mathrm{enc}}/\\varepsilon_0$.'",
            "Faraday example: 'Magnetic flux through the loop is $BA$. Faraday: $\\mathcal{E}=-d\\Phi_B/dt$.' For induced $E$ in a solenoid: 'Azimuthal $E$ constant on a circle of radius $r$, $\\Phi_B=B\\pi r^2$ for $r$ inside, so $E\\cdot 2\\pi r=\\pi r^2 dB/dt$.'",
            "Restating the answer ('$E$ is $kQ/r^2$ because that is the field of a sphere') earns little justification credit.",
            "A cube around a point charge still has flux $q/\\varepsilon_0$, but you must not claim $|E|=q/(6L^2)$ everywhere, because $|E|$ is not constant on the cube. True versus useful.",
            "Ampere justifications look the same: name the Amperian loop, argue $B$ is tangent and constant, count $I_{\\mathrm{enc}}$. Mixing Gauss language onto $B$ ('Gaussian sphere for a wire') is the wrong tool.",
        ],
        "Rubrics separate 'correct expression' from 'justification'. This concept is how you collect both columns on mixed Gauss/Faraday FRQs.",
        "Template: law, surface/path, symmetry, factor the field, equate to $q_{\\mathrm{enc}}/\\varepsilon_0$ or $-d\\Phi_B/dt$. Then algebra. Then numbers if asked.",
        lesson_figure(
            gauss_sphere_svg(),
            "The Gaussian sphere is the justification, not a decoration",
            "Write why this shape matches spherical symmetry before you write $E\\cdot 4\\pi r^2$.",
        )
        + solved(1, "Justify $E=kQ/r^2$ for $r>R$ outside a uniformly charged insulating ball.",
                 ["Spherical symmetry: $E$ radial, depends only on $r$.",
                  "Gaussian sphere of radius $r>R$: $E\\cdot 4\\pi r^2=Q/\\varepsilon_0$.",
                  "$E=Q/(4\\pi\\varepsilon_0 r^2)=kQ/r^2$."],
                 "Gauss + sphere + $q_{\\mathrm{enc}}=Q$", "", "Easy")
        + solved(2, "Justify $E_\\theta=(r/2)dB/dt$ inside a long solenoid with uniform $B(t)$.",
                 ["Faraday: $\\oint E\\cdot d\\ell=-d\\Phi_B/dt$.",
                  "Circle of radius $r$ inside: $\\Phi_B=B\\pi r^2$; $E$ azimuthal and constant by symmetry.",
                  "$E\\cdot 2\\pi r=\\pi r^2 dB/dt\\Rightarrow E=(r/2)dB/dt$ (magnitude)."],
                 "Faraday on a circle", "", "Medium")
        + solved(3, "A student uses a cube as a Gaussian surface around a point charge and writes $E=q/(6a^2)$ as 'the field'. What is right and what is wrong?",
                 ["Right: net flux through the closed cube is $q/\\varepsilon_0$, so average $E_\\perp A$ over a face is $q/(6\\varepsilon_0)$.",
                  "Wrong: $|E|$ is not equal to that average divided by $a^2$ at every point; corners are farther than face centers, and $\\vec{E}$ is not normal to the face everywhere.",
                  "The expression is not the Coulomb field. Use a sphere if you want $|E|$."],
                 "flux OK; $|E|$ not constant on the cube", "", "Hard")
        + _ican(ican6),
        ("Skipping the symmetry sentence",
         "Algebra without 'why $E$ is constant on this surface' is treated as unjustified even when the formula is the usual one."),
        ("Name the surface",
         "Write 'Gaussian sphere of radius $r$' or 'circle of radius $r$ inside the solenoid'. A nameless integral is hard to award."),
        ican6,
        26,
    )

    content = unit_shell(
        title, AUDIENCE,
        ["LC oscillations", "Maxwell displacement current idea", "Electromagnetic waves qualitative",
         "Combining E and B FRQ", "Calculator vs symbolic habits", "Justifying with Gauss and Faraday"],
        "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [
        ('Electrostatics', ["Coulomb's law", 'Superposition of E', 'Electric field of distributions',
                            'Dipole qualitative', 'Motion of a charge in E', 'Field maps']),
        ("Gauss's Law", ['Flux', "Gauss's law statement", 'Spherical symmetry',
                         'Cylindrical symmetry', 'Planar symmetry', 'Conductors in electrostatics']),
        ('Electric Potential and Capacitors', ['Potential from E', 'Potential of point charges', 'Equipotentials',
                                              'Capacitance', 'Dielectrics', 'Energy stored in a capacitor']),
        ('DC Circuits', ['Current and drift', 'Ohm and resistivity', 'Kirchhoff loop and junction',
                         'Series and parallel', 'Power in circuits', 'Voltmeters and ammeters']),
        ('RC Circuits', ['Charging a capacitor', 'Discharging', 'Time constant',
                         'Qualitative graphs', 'Energy in RC', 'Multi-loop with C']),
        ('Magnetic Fields', ['Force on a moving charge', 'Force on a current', 'Biot-Savart qualitative',
                             "Ampere's law", 'Solenoid and wire', 'Torque on a loop']),
        ('Induction', ['Magnetic flux', "Faraday's law", "Lenz's law",
                       'Motional emf', 'Inductance', 'RL circuits']),
        ('Maxwell, LC, and Mixed FRQ', ['LC oscillations', 'Maxwell displacement current idea',
                                        'Electromagnetic waves qualitative', 'Combining E and B FRQ',
                                        'Calculator vs symbolic habits', 'Justifying with Gauss and Faraday']),
    ]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>AP Physics C E&M Complete</h1>"
        f"<p><strong>For:</strong> <strong>AP Physics C: Electricity and Magnetism</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
