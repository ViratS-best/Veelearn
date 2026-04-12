"""
Assemble university-tier course HTML, diagrams, worked examples, and quiz items.
"""

from __future__ import annotations

import html
import random
from typing import Any

import univ_65_snippets as snip
from univ_65_definitions import full_title, strand_label


def course_svg_badge(strand: str, short_title: str) -> str:
    """Unique inline SVG 'diagram' per course (deterministic from title)."""
    h = abs(hash(short_title + strand)) % 10000
    hue = (h * 37) % 360
    return f"""<svg viewBox="0 0 720 200" width="100%" height="200" xmlns="http://www.w3.org/2000/svg" style="border:1px solid #cbd5e1;border-radius:12px;background:linear-gradient(135deg,#f8fafc,#eef2ff);">
  <defs>
    <linearGradient id="g{h}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:hsl({hue},70%,85%);stop-opacity:1" />
      <stop offset="100%" style="stop-color:hsl({(hue+40)%360},65%,78%);stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect x="16" y="16" width="688" height="168" rx="14" fill="url(#g{h})" stroke="#94a3b8"/>
  <text x="36" y="52" font-size="18" font-family="system-ui,sans-serif" fill="#0f172a">UNIV 2026 · {html.escape(strand_label(strand))}</text>
  <text x="36" y="88" font-size="14" fill="#334155" font-family="system-ui,sans-serif">Module focus (concept map sketch)</text>
  <circle cx="120" cy="138" r="22" fill="#3b82f6" opacity="0.85"/>
  <circle cx="260" cy="130" r="22" fill="#10b981" opacity="0.85"/>
  <circle cx="400" cy="145" r="22" fill="#f59e0b" opacity="0.85"/>
  <circle cx="540" cy="128" r="22" fill="#8b5cf6" opacity="0.85"/>
  <line x1="142" y1="138" x2="238" y2="132" stroke="#64748b" stroke-width="3"/>
  <line x1="282" y1="130" x2="378" y2="142" stroke="#64748b" stroke-width="3"/>
  <line x1="422" y1="145" x2="518" y2="132" stroke="#64748b" stroke-width="3"/>
  <text x="36" y="182" font-size="12" fill="#475569">Nodes: definitions → representations → applications → limitations (annotate in your notes).</text>
</svg>"""


def render_phet_embeds(sims: list[str], sims_map: dict[str, str]) -> str:
    parts = []
    for name in sims:
        url = sims_map.get(name)
        if not url:
            continue
        safe_name = html.escape(name)
        parts.append(
            f'<div style="margin:20px 0;padding:16px;border:1px solid #dbe5ef;border-radius:12px;background:#fff;">'
            f"<h4 style=\"margin-top:0;\">PhET: {safe_name}</h4>"
            f'<iframe src="{html.escape(url)}" width="100%" height="560" '
            f'style="border:1px solid #cbd5e1;border-radius:8px;background:#f8fafc;"></iframe>'
            f"<p><strong>Graduate-style lab brief:</strong> state a falsifiable claim, manipulate 3 independent knobs, "
            f"record a small table, plot one relationship, and write one paragraph reconciling simulation with the formal notes above.</p>"
            f"</div>"
        )
    return "\n".join(parts)


def render_wiki_figs(pairs: list[tuple[str, str]]) -> str:
    out = []
    for url, cap in pairs:
        out.append(
            f'<figure style="margin:18px 0;text-align:center;">'
            f'<img src="{html.escape(url)}" alt="{html.escape(cap)}" loading="lazy" '
            f'style="max-width:100%;height:auto;border-radius:10px;border:1px solid #e2e8f0;background:#fff;"/>'
            f'<figcaption style="font-size:0.9em;color:#475569;margin-top:10px;">{html.escape(cap)} '
            f"<em>(public-domain / open license educational media)</em></figcaption></figure>"
        )
    return "<h2>Scholarly visuals from the open web</h2>" + "".join(out)


def worked_set(strand: str, idx: int, short_title: str) -> list[dict[str, Any]]:
    """Four college-style worked items per module; numbers vary with idx to reduce duplication."""
    k = idx + 1
    def box(n: int, problem: str, steps: list[str], ans: str) -> dict[str, Any]:
        return {"n": n, "problem": problem, "steps": steps, "answer": ans}

    if strand == "math":
        return [
            box(
                1,
                f"ε–δ skeleton: Show that lim<sub>x→{k}</sub> (2x + {k}) = {3*k}.",
                [
                    "Guess L = 3k. Write |2x + k − 3k| = 2|x − k|.",
                    "Given ε > 0, choose δ = ε/2.",
                    "If 0 < |x − k| < δ then |f(x) − L| = 2|x − k| < 2δ = ε.",
                    "Conclude by the ε–δ definition.",
                ],
                f"L = {3*k} with δ = ε/2.",
            ),
            box(
                2,
                f"Compute d/dx [ x^{k % 4 + 2} · ln(x) ] at x = 1 (assume x > 0).",
                [
                    "Product rule: (x^m ln x)' = m x^{m-1} ln x + x^{m-1}.",
                    f"Here m = {k % 4 + 2}.",
                    "At x = 1, ln 1 = 0 so only the second term survives: 1^{m-1} = 1.",
                    "Answer is 1.",
                ],
                "1",
            ),
            box(
                3,
                f"Evaluate ∫<sub>0</sub><sup>1</sup> ({k}x + {k % 3}) dx.",
                [
                    "Antiderivative: (k/2)x² + (k mod 3)x.",
                    "Plug bounds 0 and 1.",
                    f"Value = {k}/2 + {k % 3}.",
                    "Simplify mentally as a reduced check.",
                ],
                f"{k / 2 + (k % 3):g}",
            ),
            box(
                4,
                f"Linear algebra drill: Is the set {{(1,0,{k % 2}),(0,1,1)}} linearly independent in ℝ³?",
                [
                    "Form matrix columns and row-reduce or inspect dependence.",
                    "If k % 2 = 0, vectors are (1,0,0) and (0,1,1) — clearly independent (no scalar multiple).",
                    "If k % 2 = 1, still independent: second not multiple of first.",
                    "Conclude independence; they span a 2D plane.",
                ],
                "Yes, linearly independent.",
            ),
        ]

    if strand == "physics":
        m = 2 + (idx % 5)
        f = 18 + idx * 2
        v = 6 + idx
        return [
            box(1, f"Net force magnitude on m={m} kg with a = {f/m:.2f} m/s².", ["Use ΣF = ma.", f"F = {m}·({f/m:.2f}).", "Compute.", "Attach newtons."], f"{f:.1f} N"),
            box(2, f"Kinetic energy for m={m} kg, v={v} m/s.", ["KE = ½mv².", f"½·{m}·{v}².", "Compute in joules."], f"{0.5*m*v*v:.2f} J"),
            box(3, f"Spring energy: k={80+idx} N/m, x=0.{1 + (idx % 5)} m.", ["U = ½kx².", "Substitute.", "Joules."], f"{0.5*(80+idx)*(0.1 + 0.01*(idx%5))**2:.3f} J"),
            box(
                4,
                f"Power delivered if the same force {f:.0f} N acts at v={v} m/s along motion.",
                ["P = F·v for parallel case.", "Substitute.", "Watts."],
                f"{f*v:.1f} W",
            ),
        ]

    if strand == "chemistry":
        n = 0.5 + 0.07 * k
        v = 0.8 + 0.05 * k
        return [
            box(1, f"Molarity of {n:.3f} mol solute in {v:.3f} L solution.", ["M = n/V.", "Divide.", "mol/L."], f"{n/v:.4f} M"),
            box(
            2,
            f"pH if [H⁺] = 10<sup>−{4 + idx % 4}</sup> M.",
            ["pH = −log₁₀[H⁺].", "Here [H⁺] is an exact power of ten.", "So pH equals the exponent magnitude as a positive integer."],
            str(4 + idx % 4),
        ),
            box(3, "Balance: __ Fe + __ O₂ → __ Fe₂O₃ (smallest integers).", ["Balance O first.", "Then Fe.", "Check atom counts."], "4 Fe + 3 O₂ → 2 Fe₂O₃"),
            box(
                4,
                f"ΔH°rxn given ΔH°f values: A→B, use Hess with {k} kJ mol⁻¹ as a hypothetical intermediate step exercise.",
                ["Write target as sum of known steps.", "Flip reactions to reverse sign.", "Sum enthalpies."],
                "Follow stoichiometric scaling; final numeric value depends on provided table in exam.",
            ),
        ]

    if strand == "biology":
        p = 0.2 + 0.03 * idx
        N = 2000 + 50 * idx
        return [
            box(1, f"Hardy–Weinberg: p={p:.2f}, find q and 2pq.", ["q = 1−p.", "2pq heterozygote frequency."], f"q={1-p:.2f}, 2pq={2*p*(1-p):.4f}"),
            box(2, f"Population {N} with r={0.08 + 0.01*(idx%3):.2f} per-generation growth (discrete). Next generation?", ["N' = N(1+r).", "Compute."], f"{int(round(N*(1+0.08+0.01*(idx%3))))}"),
            box(3, "Why does inbreeding increase homozygosity without changing allele frequency?", ["Allele counts unchanged.", "Mating structure pairs identical-by-descent alleles more often.", "Increases F coefficient."], "IBD pairing ↑, p and q unchanged."),
            box(4, "Contrast directional vs stabilizing selection on a quantitative trait.", ["Directional shifts mean.", "Stabilizing reduces variance around optimum.", "Give one example each."], "Conceptual distinction; examples vary."),
        ]

    # computing
    n = 8 + idx
    return [
        box(1, f"Big-O: Show n² + {idx}n + {k} is O(n²).", ["Choose c, n₀.", "For n≥1, n² dominates.", "Bound constants."], "Take c = 2 + idx + k for n ≥ 1 (example bound)."),
        box(2, f"Master theorem style: T(n)=2T(n/2)+{k}n. Guess Θ(n log n) plausibility.", ["Compare n^{log₂2}=n to f(n)=kn.", "Same order → Θ(n log n).", "State assumptions on n power of 2."], "Θ(n log n) under standard regularity."),
        box(3, f"Hash table with m={20+idx} buckets, n={15+2*idx} keys — expected probes chaining (very rough).", ["Average load α=n/m.", "Expected chain length ~α for simple uniform hashing intuition."], f"α ≈ {(15+2*idx)/(20+idx):.3f}"),
        box(4, "Why normalize features before gradient descent on least squares?", ["Rescales contours to reduce ill-conditioning.", "Allows larger stable learning rates.", "Improves convergence empirically."], "Conditioning + step-size stability."),
    ]


def render_worked(worked: list[dict[str, Any]]) -> str:
    chunks = []
    for w in worked:
        steps = "".join(f"<li>{html.escape(s)}</li>" for s in w["steps"])
        chunks.append(
            f'<div style="background:#fff;border:1px solid #dbe5ef;border-radius:12px;padding:16px;margin:14px 0;">'
            f'<h4 style="margin-top:0;">Worked Example {w["n"]}</h4>'
            f'<p><strong>Problem.</strong> {w["problem"]}</p>'
            f"<p><strong>Solution outline.</strong></p><ol>{steps}</ol>"
            f'<p><strong>Result.</strong> {html.escape(str(w["answer"]))}</p></div>'
        )
    return "<h2>Worked examples (college standard)</h2>" + "".join(chunks)


def learning_outcomes(short_title: str) -> str:
    return f"""
<h2>Official learning outcomes</h2>
<ul>
<li>Explain <strong>{html.escape(short_title)}</strong> using definitions appropriate to university science and engineering texts.</li>
<li>Translate between verbal, graphical, symbolic, and (where relevant) computational representations.</li>
<li>Solve multi-step quantitative problems showing assumptions, units, and reasonableness checks.</li>
<li>Critique common misconceptions and identify the boundary conditions where models fail.</li>
</ul>"""


def build_html(
    strand: str,
    short_title: str,
    module_idx: int,
    sims_map: dict[str, str],
) -> str:
    """Full course HTML (readable newlines) for DB `courses.content` before quiz placeholders."""
    title = full_title(strand, short_title)
    S = snip.snippet(strand, module_idx)
    trio = snip.phet_trio(strand, module_idx)
    wikis = snip.wiki_pair(strand, module_idx)
    worked = worked_set(strand, module_idx, short_title)
    parts = [
        '<div class="univ-2026-course" style="background:#f8fafc;color:#0f172a;padding:12px 16px 28px;max-width:920px;margin:0 auto;line-height:1.55;">',
        f"<h1>{html.escape(title)}</h1>",
        "<p><strong>Audience:</strong> university-level (intro undergrad). Not elementary pacing.</p>",
        f"<p><strong>Focus:</strong> {html.escape(short_title)}</p>",
        "<hr/>",
        learning_outcomes(short_title),
        "<h2>Intellectual framing</h2>",
        f"<p>{html.escape(S['overview'])}</p>",
        "<h2>Formal notes</h2>",
        f"<p>{S['formal']}</p>",
        "<h2>Common pitfalls</h2>",
        f"<p>{html.escape(S['pitfall'])}</p>",
        "<h2>Concept diagram</h2>",
        course_svg_badge(strand, short_title),
        render_wiki_figs(wikis),
        "<h2>PhET laboratory</h2>",
        f"<p>{html.escape(S['lab_prompt'])}</p>",
        render_phet_embeds(trio, sims_map),
        render_worked(worked),
        "<h2>Further study</h2><ul><li>OpenStax / OER aligned chapters</li>"
        "<li>Extra problem set (instructor-style)</li>"
        "<li>One review of a research abstract</li></ul>",
        "<p><em>PhET © University of Colorado Boulder.</em></p>",
        "</div>",
    ]
    return "\n".join(parts)


def build_quizzes(
    strand: str,
    module_idx: int,
    short_title: str,
    trio: list[str],
) -> list[dict[str, Any]]:
    """12 multiple-choice questions; options shuffled by injector via `shuffle_options`."""
    title = full_title(strand, short_title)
    worked = worked_set(strand, module_idx, short_title)
    w_ans = [str(w["answer"]) for w in worked]
    d1, d2, d3 = "Result A (distractor)", "Result B (distractor)", "Result C (distractor)"

    def q(text: str, correct: str, wrongs: list[str], expl: str, oi: int) -> dict[str, Any]:
        return {
            "question_text": text,
            "question_type": "multiple_choice",
            "options": [correct] + wrongs[:3],
            "correct_answer": correct,
            "explanation": expl,
            "points": 1,
            "order_index": oi,
        }

    qs: list[dict[str, Any]] = [
        q(
            f"{title}: Primary intellectual goal of this module?",
            "Build transferable university-level models, not memorized grade-school tricks.",
            [
                "Memorize isolated facts only",
                "Skip quantitative reasoning",
                "Avoid reading formal definitions",
            ],
            "University courses reward structure, justification, and limitation analysis.",
            1,
        ),
        q(
            f"{title}: How should you read the Formal notes section?",
            "As the symbolic and structural backbone you must reconcile with examples",
            [
                "As optional decoration",
                "As something to ignore if an English summary exists",
                "As a list of unrelated formulas",
            ],
            "Formal and verbal explanations must agree.",
            2,
        ),
        q(
            f"{title}: First worked example — stated final result?",
            w_ans[0],
            [d1, w_ans[1] if w_ans[1] != w_ans[0] else "0", w_ans[2] if w_ans[2] != w_ans[0] else "n/a"],
            "Reproduce the first solution from your notes without scrolling.",
            3,
        ),
        q(
            f"{title}: Second worked example — stated final result?",
            w_ans[1],
            [w_ans[0] if w_ans[0] != w_ans[1] else d1, d2, w_ans[2] if w_ans[2] != w_ans[1] else d3],
            "Different problems can look similar; track which calculation belongs to which prompt.",
            4,
        ),
        q(
            f"{title}: Which three PhET simulations are embedded (in order)?",
            f"{trio[0]} | {trio[1]} | {trio[2]}",
            [
                f"{trio[0]} | {trio[1]} only",
                "Arithmetic | Make a Ten | Number Compare",
                f"{trio[2]} | {trio[0]} | {trio[1]}",
            ],
            "Match the iframe headings in the course body.",
            5,
        ),
        q(
            f"{title}: Why include Wikimedia or similar scholarly figures?",
            "To connect symbolic models to standard scientific visual culture and citation practice",
            ["For decoration only", "To replace all reading", "To avoid running simulations"],
            "Visual literacy is part of STEM communication.",
            6,
        ),
        q(
            f"{title}: Why read the pitfall paragraph carefully?",
            "It flags errors that survive partial understanding and break proofs on exams",
            [
                "It is optional filler",
                "It only lists typos",
                "It replaces all lectures",
            ],
            "Experts still make predictable mistakes; the module names common ones.",
            7,
        ),
        q(
            f"{title}: Third worked example — stated final result?",
            w_ans[2],
            [w_ans[0], w_ans[1], w_ans[3] if w_ans[3] != w_ans[2] else d2],
            "Middle drills often hide algebra or unit slips.",
            8,
        ),
        q(
            f"{title}: Fourth worked example — stated final result?",
            w_ans[3],
            [w_ans[0], w_ans[1], w_ans[2] if w_ans[2] != w_ans[3] else d3],
            "The last item often synthesizes multiple ideas from the module.",
            9,
        ),
        q(
            f"{title}: In a university lab report, raw PhET screenshots alone are:",
            "Insufficient without interpretation tied to claims and uncertainty",
            ["Sufficient as proof", "Better than numeric data tables", "Equivalent to a formal proof"],
            "Evidence must be interpreted, not only displayed.",
            10,
        ),
        q(
            f"{title}: Which study habit best supports transfer to timed exams?",
            "Re-derive one key result weekly from closed notes",
            [
                "Re-read highlighted PDF sentences only",
                "Memorize figure captions without redoing calculations",
                "Avoid timed practice until the final week",
            ],
            "Active reconstruction beats passive review.",
            11,
        ),
        q(
            f"{title}: Academic integrity when collaborating on problem sets:",
            "Write up your own reasoning; attribute shared ideas per your course policy",
            [
                "Identical writeups are acceptable if numbers match",
                "Citation is only needed for Wikipedia",
                "Running someone else's code without credit is fine if it executes",
            ],
            "Undisclosed copying violates most university honor codes.",
            12,
        ),
    ]
    return qs
