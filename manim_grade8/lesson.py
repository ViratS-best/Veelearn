"""3Blue1Brown-style silent-brand lessons with generated voiceover.

No course labels on screen. One idea at a time. Full scene wipe between beats
so leftover graphics cannot overlap the next line.
"""
import os
import re
from pathlib import Path

from decimal import Decimal

from manimlib import *

from voice import ensure_voice, spoken

GOLD = "#ffff00"
TEAL = "#5cd6d6"
BLUE = "#58c4dd"
WHITE = "#ece6e2"
GREY = "#888888"
PINK = "#ff8080"
GREEN = "#83c167"
RED = "#ff6b6b"
FONT = "Georgia"
FONT_MATH = "Arial"
CREAM = WHITE
MUTED = GREY
SOUND_DIR = Path(__file__).resolve().parent / "sounds"

SUP_MAP = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "ⁿ": "n", "⁻": "-",
}
PLAIN = {
    "×": " x ", "÷": " / ", "·": "*", "√": "sqrt ",
    "π": "pi", "θ": "theta", "≤": "<=", "≥": ">=", "≠": "!=",
    "→": "->", "←": "<-", "∞": "inf", "±": "+/-", "°": " deg",
    "−": "-", "–": "-",
}
SUP_CHARS = set(SUP_MAP)
# Include ASCII hyphen so binary minus never becomes a low "_" glyph.
OPS = set("×÷·+=<>≤≥≠-−–")


def caretify(text) -> str:
    """Keep ^ for exponents so 10³ becomes 10^3, never '10 3'."""
    s = str(text).replace("−", "-").replace("–", "-").replace("→", " -> ").replace("⇒", " -> ")
    s = s.replace("×", " x ").replace("·", " x ").replace("÷", " / ").replace("√", "sqrt ")
    s = re.sub(
        r"[⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁻]+",
        lambda m: "^" + "".join(SUP_MAP.get(c, c) for c in m.group(0)),
        s,
    )
    return " ".join(s.split())


def clean(text) -> str:
    return caretify(text)


def _pretty_minus(s) -> str:
    """Keep ASCII hyphen; Georgia + DirectWrite hangs on U+2212 on some Windows installs."""
    return str(s).replace("−", "-").replace("–", "-")


def power_mob(base, exp, base_size=52, exp_size=28, base_color=WHITE, exp_color=GOLD):
    b = Text(_pretty_minus(base), font=FONT_MATH, font_size=base_size).set_color(base_color)
    e = Text(_pretty_minus(exp), font=FONT_MATH, font_size=exp_size).set_color(exp_color)
    e.next_to(b.get_corner(UR), RIGHT, buff=0.04)
    e.shift(0.08 * UP)
    return VGroup(b, e)


def _read_atom(s, i):
    n = len(s)
    if i >= n:
        return "", i
    if s[i] == "(":
        depth = 1
        j = i + 1
        while j < n and depth:
            if s[j] == "(":
                depth += 1
            elif s[j] == ")":
                depth -= 1
            j += 1
        return s[i:j], j
    m = re.match(r"-?\d+(?:\.\d+)?", s[i:])
    if m:
        return m.group(0), i + m.end()
    if s[i].isalpha():
        return s[i], i + 1
    return "", i


def tokenize_math(text):
    s = str(text).replace("−", "-").replace("–", "-").replace("→", "->").replace("⇒", "->")
    i, n, out = 0, len(s), []
    while i < n:
        if s[i].isspace():
            i += 1
            continue
        if s.startswith("->", i) or s.startswith("=>", i):
            out.append(("arrow",))
            i += 2
            continue
        if s[i] == "√":
            atom, i = _read_atom(s, i + 1)
            out.append(("sqrt", atom or ""))
            continue
        if s.startswith("sqrt", i) and (i + 4 >= n or not s[i + 4].isalpha()):
            i += 4
            while i < n and s[i].isspace():
                i += 1
            atom, i = _read_atom(s, i)
            out.append(("sqrt", atom or ""))
            continue
        # Compound English (two-way, best-fit): keep a hyphen, not a minus bar.
        if s[i] == "-" and i > 0 and i + 1 < n and s[i - 1].isalpha() and s[i + 1].isalpha():
            out.append(("txt", "-"))
            i += 1
            continue
        # 3-4-5 triples: hyphen, not minus. 169-144=25 stays a minus (one hyphen).
        if s[i] == "-" and i > 0 and s[i - 1].isdigit() and i + 1 < n and s[i + 1].isdigit():
            nxt = s[i + 1:i + 8]
            if re.match(r"\d+-\d", nxt):
                out.append(("txt", "-"))
                i += 1
                continue
        if s[i] == "-" and i + 1 < n and s[i + 1].isdigit():
            prev = out[-1][0] if out else None
            if prev in (None, "op", "arrow"):
                out.append(("op", "-"))
                i += 1
                continue
            # Binary-looking but glued (rare): still treat as operator.
            out.append(("op", "-"))
            i += 1
            continue
        if s[i] in OPS or s[i] == "/":
            ch = "-" if s[i] in "-−–" else s[i]
            out.append(("op", ch))
            i += 1
            continue
        if s[i] == "(" or s[i].isdigit():
            atom, i = _read_atom(s, i)
            exp = ""
            if i < n and s[i] in SUP_CHARS:
                while i < n and s[i] in SUP_CHARS:
                    exp += SUP_MAP.get(s[i], s[i])
                    i += 1
            elif i < n and s[i] == "^":
                m = re.match(r"-?[0-9n]+", s[i + 1:])
                if m:
                    exp = m.group(0)
                    i += 1 + m.end()
            out.append(("pow", atom, exp) if exp else ("txt", atom))
            continue
        m = re.match(r"[A-Za-z][A-Za-z']*", s[i:])
        if m:
            word = m.group(0)
            i += m.end()
            exp = ""
            if len(word) == 1 and i < n and s[i] in SUP_CHARS:
                while i < n and s[i] in SUP_CHARS:
                    exp += SUP_MAP.get(s[i], s[i])
                    i += 1
            elif len(word) == 1 and i < n and s[i] == "^":
                em = re.match(r"-?[0-9n]+", s[i + 1:])
                if em:
                    exp = em.group(0)
                    i += 1 + em.end()
            out.append(("pow", word, exp) if exp else ("txt", word))
            continue
        # Skip unknown glyphs that Georgia cannot draw (prevents random junk).
        if ord(s[i]) > 127 and s[i] not in "√πθ≤≥≠±°×÷·":
            i += 1
            continue
        out.append(("txt", s[i]))
        i += 1
    return out


def token_mob(tok, size, color, font=FONT_MATH):
    kind = tok[0]
    if kind == "pow":
        return power_mob(tok[1], tok[2], size, max(14, int(size * 0.55)), color, GOLD)
    if kind == "sqrt":
        return radical_mob(tok[1] or "", size, color, font)
    if kind == "arrow":
        return Text("so", font=font, font_size=max(16, int(size * 0.5))).set_color(TEAL)
    if kind == "op":
        if tok[1] == "-":
            h = max(0.32, size * 0.011)
            w = max(0.14, size * 0.0044)
            pad = Rectangle(width=w, height=h).set_stroke(width=0).set_fill(BLACK, 0)
            bar = Line(LEFT * (w * 0.38), RIGHT * (w * 0.38))
            bar.set_stroke(color, max(2.2, size / 24.0))
            bar.move_to(pad.get_center())
            return VGroup(pad, bar)
        shown = {"*": "x", "·": "x"}.get(tok[1], tok[1])
        col = GOLD if tok[1] == "=" else (TEAL if tok[1] in "×÷·*" else color)
        return Text(shown, font=font, font_size=size).set_color(col)
    word = _pretty_minus(tok[1])
    if word.lower() == "pi":
        word = "π"
    return Text(word, font=font, font_size=size).set_color(color)


def radical_mob(inner_text, size, color, font=FONT_MATH):
    """Drawn radical + vinculum. No LaTeX, no 'sqrt' letters."""
    inner = Text(_pretty_minus(inner_text or " "), font=font, font_size=size).set_color(color)
    h = max(inner.get_height(), size * 0.012)
    w = max(inner.get_width(), 0.35)
    inner.shift(0.18 * RIGHT + 0.02 * DOWN)
    hook_l = inner.get_left() + 0.16 * LEFT
    base_y = inner.get_bottom()[1] - 0.04
    top_y = inner.get_top()[1] + 0.10
    tick = Line(
        np.array([hook_l[0] - 0.12, base_y + 0.10, 0]),
        np.array([hook_l[0] - 0.02, base_y, 0]),
    ).set_stroke(TEAL, max(2.0, size / 22.0))
    stem = Line(
        np.array([hook_l[0] - 0.02, base_y, 0]),
        np.array([hook_l[0] + 0.04, top_y, 0]),
    ).set_stroke(TEAL, max(2.0, size / 22.0))
    bar = Line(
        np.array([hook_l[0] + 0.04, top_y, 0]),
        np.array([inner.get_right()[0] + 0.10, top_y, 0]),
    ).set_stroke(TEAL, max(2.0, size / 22.0))
    return VGroup(tick, stem, bar, inner)


def formula(text, size=36, color=WHITE, max_width=12.0, font=FONT_MATH):
    tokens = tokenize_math(text)
    if not tokens:
        return Text("", font=font, font_size=size).set_color(color)
    # Multi-step chains (a -> b -> c) stack vertically so arrows never jam.
    if any(t[0] == "arrow" for t in tokens):
        chunks, cur = [], []
        for t in tokens:
            if t[0] == "arrow":
                if cur:
                    chunks.append(cur)
                    cur = []
            else:
                cur.append(t)
        if cur:
            chunks.append(cur)
        rows = []
        for ci, chunk in enumerate(chunks):
            pieces = [token_mob(tok, size, color, font) for tok in chunk]
            row = VGroup(*pieces).arrange(RIGHT, buff=0.12, aligned_edge=ORIGIN)
            rows.append(row)
            if ci < len(chunks) - 1:
                rows.append(Text("so", font=font, font_size=max(16, int(size * 0.45))).set_color(TEAL))
        return VGroup(*rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    pieces = [token_mob(tok, size, color, font) for tok in tokens]
    punct = set(",.;:?!")

    def pack_row(items):
        if not items:
            return VGroup()
        g = VGroup(items[0][1])
        for tok, p in items[1:]:
            is_punct = tok[0] == "txt" and str(tok[1]) in punct
            gap = 0.02 if is_punct else 0.12
            edge = DOWN if is_punct else ORIGIN
            p.next_to(g, RIGHT, buff=gap, aligned_edge=edge)
            g.add(p)
        return g

    rows, row, row_w = [], [], 0.0
    for tok, p in zip(tokens, pieces):
        gap = 0.02 if (tok[0] == "txt" and str(tok[1]) in punct) else 0.12
        w = p.get_width()
        if row and row_w + gap + w > max_width:
            rows.append(pack_row(row))
            row, row_w = [(tok, p)], w
        else:
            row.append((tok, p))
            row_w = row_w + (gap if len(row) > 1 else 0) + w
    if row:
        rows.append(pack_row(row))
    return rows[0] if len(rows) == 1 else VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)


def T(text, size=36, color=WHITE, width=40, font=FONT):
    max_w = min(12.4, max(4.5, 0.30 * float(width)))
    s = str(text).replace("→", ", so ").replace("←", " from ").replace("·", ".")
    s = re.sub(r"\s+([,.;:?!])", r"\1", s)
    s = re.sub(r"\bpi\b", "π", s, flags=re.I)
    s = re.sub(
        r"[⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁻]+",
        lambda m: "^" + "".join(SUP_MAP.get(c, c) for c in m.group(0)),
        s,
    )
    words = re.findall(r"[A-Za-z]{3,}", s)
    mathish = bool(re.search(r"[=^√×÷π]|/\d|\d/\d", s))
    prose = any(len(w) >= 7 for w in words)
    # Superscripts / caret powers must go through formula (power_mob), never Georgia Text.
    if re.search(r"\^[+-]?\d", s):
        return formula(s, size, color, max_w, FONT_MATH)
    # Long English through formula turns "you" into yo^u, "1 parallel" into "1parallel",
    # and periods into middle dots. Keep real sentences as Text.
    if mathish and len(words) < 5 and not prose:
        return formula(s, size, color, max_w, FONT_MATH)
    mob = Text(s, font=font, font_size=size).set_color(color)
    if mob.get_width() > max_w:
        mob.set_width(max_w)
    return mob


def has(text, *needles):
    t = caretify(text).lower()
    return any(n.lower() in t for n in needles)


def _fmt_n(n):
    n = float(n)
    if abs(n - round(n)) < 1e-6:
        return str(int(round(n)))
    for d in (2, 3, 4, 5, 6, 8):
        k = round(n * d)
        if abs(n * d - k) < 1e-6:
            return f"{int(k)}/{d}"
    return f"{n:.3f}".rstrip("0").rstrip(".")


def _read_coef(sign, num):
    sgn = -1.0 if sign == "-" else 1.0
    if not num:
        return sgn
    return sgn * float(num)


def parse_lin_system(text):
    """Two-variable ax + by = c equations from a beat (ASCII minus only)."""
    s = caretify(text)
    out = []
    std = re.compile(
        r"([+-]?)\s*(\d+(?:\.\d+)?)?\s*([A-Za-z])"
        r"(?:\s*([+-])\s*(\d+(?:\.\d+)?)?\s*([A-Za-z]))?"
        r"\s*=\s*([+-]?\d+(?:\.\d+)?)"
    )
    for m in std.finditer(s):
        a_sign, a_num, v1, b_sign, b_num, v2, c = m.groups()
        if not v2:
            continue
        src = m.group(0).replace("−", "-").replace("–", "-")
        out.append({
            "a": _read_coef(a_sign or "+", a_num),
            "b": _read_coef(b_sign, b_num),
            "c": float(c),
            "x": v1,
            "y": v2,
            "src": src,
        })
    return out


def solve_lin_system(e1, e2):
    a1, b1, c1 = e1["a"], e1["b"], e1["c"]
    a2, b2, c2 = e2["a"], e2["b"], e2["c"]
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-8:
        same = abs(a1 * c2 - a2 * c1) < 1e-6 and abs(b1 * c2 - b2 * c1) < 1e-6
        return ("inf" if same else "none", None)
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return ("one", (x, y))


def pair_from_text(text):
    t = caretify(text)

    def num(raw):
        raw = raw.replace(" ", "")
        if "/" in raw:
            a, b = raw.split("/", 1)
            return float(a) / float(b)
        return float(raw)

    m = re.search(
        r"\(\s*(-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)\s*,\s*(-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)\s*\)",
        t,
    )
    if m:
        return num(m.group(1)), num(m.group(2))
    m = re.search(
        r"\bx\s*=\s*(-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)\s*,\s*y\s*=\s*(-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)",
        t,
    )
    if m:
        return num(m.group(1)), num(m.group(2))
    m = re.search(r"\ba\s*=\s*(-?\d+(?:\.\d+)?)\s*,\s*c\s*=\s*(-?\d+(?:\.\d+)?)", t)
    if m:
        return num(m.group(1)), num(m.group(2))
    m = re.search(r"\bc\s*=\s*(-?\d+(?:\.\d+)?)\s*,\s*a\s*=\s*(-?\d+(?:\.\d+)?)", t)
    if m:
        return num(m.group(2)), num(m.group(1))
    m = re.search(
        r"\by\s*=\s*(-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)\s*,\s*x\s*=\s*(-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?)",
        t,
    )
    if m:
        return num(m.group(2)), num(m.group(1))
    if "1/3" in t.replace(" ", ""):
        xm = re.search(r"2\((\d+)\)", t)
        if xm:
            return float(xm.group(1)), 1.0 / 3.0
    return None


def fmt_lin_eq(e):
    src = str(e.get("src") or "").replace("−", "-").replace("–", "-")
    if src and "=" in src:
        return src
    x, y = e.get("x", "x"), e.get("y", "y")

    def term(coef, var, first):
        if abs(coef) < 1e-9:
            return ""
        mag = abs(coef)
        body = var if abs(mag - 1) < 1e-9 else f"{_fmt_n(mag)}{var}"
        if first:
            return body if coef > 0 else f"-{body}"
        return f" + {body}" if coef > 0 else f" - {body}"

    left = (term(e["a"], x, True) + term(e["b"], y, abs(e["a"]) < 1e-9)).strip() or "0"
    return f"{left} = {_fmt_n(e['c'])}"


def parse_sci(text):
    found = re.findall(r"([+-]?\d+(?:\.\d+)?)\s*[x*]\s*10\^(-?\d+)", caretify(text))
    return [(a, int(e)) for a, e in found]


def parse_power(text):
    return re.findall(r"(\(-?\d+\)|[A-Za-z]|\d+)\^(-?\d+|n)", caretify(text))


def extract_math(text):
    chunks = re.split(r"(?<=[.!?])\s+", str(text).strip())
    for chunk in chunks:
        if "=" in chunk or any(c in chunk for c in "⁰¹²³⁴⁵⁶⁷⁸⁹√×^"):
            return chunk.strip()
    return str(text).strip()


def sci_value(coeff, exp):
    val = Decimal(str(coeff)) * (Decimal(10) ** int(exp))
    shown = format(val, "f")
    if "." in shown:
        shown = shown.rstrip("0").rstrip(".")
    return shown


def expand_sci(coeff, exp):
    return sci_value(coeff, exp)


class LessonScene(Scene):
    unit_num = 1
    unit_title = "Exponents"
    subtitle = ""
    parts = []

    def construct(self):
        self._voice_left = 0.0
        self.bg = FullScreenRectangle()
        self.bg.set_fill("#111111", 1).set_stroke(width=0)
        self.add(self.bg)
        parts = list(self.parts)
        if os.environ.get("G8_SMOKE"):
            first = dict(parts[0])
            first["beats"] = list(first.get("beats", []))[:2]
            first["examples"] = list(first.get("examples", []))[:1]
            parts = [first]
        self.intro()
        for i, part in enumerate(parts, 1):
            self.play_part(i, part)
        self.outro()

    def play(self, *args, **kwargs):
        rt = float(kwargs.get("run_time", 1.0))
        self._voice_left = max(0.0, self._voice_left - rt)
        return super().play(*args, **kwargs)

    def wait(self, duration=1.0, **kwargs):
        self._voice_left = max(0.0, self._voice_left - float(duration))
        return super().wait(duration, **kwargs)

    def narrate(self, text):
        try:
            path, dur = ensure_voice(text)
            self.add_sound(str(path), gain=-3)
            self._voice_left = max(self._voice_left, dur)
            return dur
        except Exception as err:
            print("voice skipped:", err)
            words = len(spoken(text).split())
            self._voice_left = max(self._voice_left, max(2.4, words * 0.42))
            return self._voice_left

    def rest(self):
        self.wait(max(0.55, self._voice_left + 0.4))
        self._voice_left = 0.0

    def wipe(self, run_time=0.4):
        fading = []
        for mob in list(self.mobjects):
            if mob is self.bg:
                continue
            if type(mob).__name__ in ("CameraFrame",):
                continue
            fading.append(mob)
        if fading:
            self.play(FadeOut(VGroup(*fading), shift=0.12 * DOWN), run_time=run_time)
            self.remove(*fading)

    def sfx(self, name, gain=-12):
        path = SOUND_DIR / f"{name}.wav"
        if path.exists():
            self.add_sound(str(path), gain=gain)

    def pop_flash(self, point, color=GOLD, radius=0.7):
        self.play(Flash(point, color=color, flash_radius=radius,
                        line_length=0.22, num_lines=12, run_time=0.45))

    def morph_number(self, mob, nxt_text, size=56, color=GOLD):
        nxt = formula(nxt_text, size, color, 16).move_to(mob)
        try:
            self.play(Transform(mob, nxt), run_time=0.5)
        except Exception:
            self.play(FadeOut(mob), FadeIn(nxt), run_time=0.45)
            return nxt
        return mob

    def highlight(self, mob, color=GOLD):
        # Fade the full box. ShowCreation leaves L-shaped cyan/gold dashes.
        try:
            rect = SurroundingRectangle(mob, buff=0.12)
            rect.set_stroke(color, 2)
            self.play(FadeIn(rect), run_time=0.2)
            self.play(FadeOut(rect), run_time=0.2)
        except Exception:
            pass

    def intro(self):
        line = f"Let's build a clear picture of {self.unit_title}. {self.subtitle}."
        self.narrate(line)
        title = Text(self.unit_title, font=FONT, font_size=52).set_color(WHITE)
        if title.get_width() > 12:
            title.set_width(12)
        under = Line(LEFT * 2.2, RIGHT * 2.2).set_stroke(GOLD, 4)
        sub = T(self.subtitle, 28, GREY, 42)
        stack = VGroup(title, under, sub).arrange(DOWN, buff=0.28).move_to(0.4 * UP)
        self.play(FadeIn(title, 0.15 * UP), run_time=0.7)
        self.play(ShowCreation(under), FadeIn(sub, 0.2 * UP), run_time=0.7)
        self.rest()

        self.wipe()
        self.narrate("Here is the path we will take. Each idea gets its own moving picture.")
        rows = VGroup()
        for i, part in enumerate(self.parts, 1):
            n = Text(str(i) + ".", font=FONT, font_size=28).set_color(GOLD)
            label = T(part["title"], 30, WHITE, 34)
            rows.add(VGroup(n, label).arrange(RIGHT, buff=0.22))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(0.15 * DOWN)
        self.play(LaggedStart(*[FadeIn(r, 0.2 * RIGHT) for r in rows], lag_ratio=0.14), run_time=2.4)
        self.rest()

    def outro(self):
        self.wipe()
        self.narrate("That's the idea. Pause, rewind any step, and try a problem on your own.")
        done = Text("Try a problem.", font=FONT, font_size=52).set_color(GOLD)
        self.play(FadeIn(done, 0.15 * UP), run_time=0.7)
        self.highlight(done, TEAL)
        self.rest()
        self.play(FadeOut(done), run_time=0.6)

    def play_part(self, index, part):
        self.wipe()
        self.narrate(part["title"] + ". Watch how the pieces move.")
        title = Text(part["title"], font=FONT, font_size=46).set_color(WHITE)
        if title.get_width() > 12:
            title.set_width(12)
        self.play(FadeIn(title, 0.12 * UP), run_time=0.65)
        self.rest()

        visual_kind = part.get("visual")
        for bi, beat in enumerate(part.get("beats", [])):
            self.play_beat(beat, visual_kind, bi)
        examples = part.get("examples", [])[:1]
        if examples:
            self.play_example(examples[0])

    def play_beat(self, beat, visual_kind, index):
        self.wipe()
        self.narrate(beat)
        self.animate_visual(visual_kind, index, beat)
        self.rest()

    def play_example(self, ex):
        self.wipe()
        problem = ex["problem"]
        self.narrate("Here is a worked example. " + problem)
        head = T("Worked example", 26, GOLD, 28)
        head.to_edge(UP, buff=0.55)
        self.play(FadeIn(head, 0.15 * DOWN), run_time=0.4)
        prob = T(problem, 38, WHITE, 34)
        if prob.get_width() > 12:
            prob.set_width(12)
        prob.next_to(head, DOWN, buff=0.35)
        self.play(FadeIn(prob, 0.1 * UP), run_time=1.2)
        self.highlight(prob)
        self.rest()

        pic = None
        if self._example_wants_picture(ex):
            pic = self._example_picture(ex)
            if pic is not None:
                try:
                    self.play(
                        pic.animate.scale(0.62).to_edge(RIGHT, buff=0.35).shift(0.15 * DOWN),
                        run_time=0.35,
                    )
                except Exception:
                    pass

        stack = VGroup(prob)
        for si, step in enumerate(ex.get("steps", []), 1):
            self.narrate("Step " + str(si) + ". " + step)
            n = Text(str(si) + ".", font=FONT, font_size=30).set_color(GOLD)
            body = T(step, 32, WHITE, 32)
            if body.get_width() > 10.4:
                body.set_width(10.4)
            row = VGroup(n, body).arrange(RIGHT, buff=0.2, aligned_edge=ORIGIN)
            row.next_to(stack, DOWN, buff=0.32, aligned_edge=LEFT)
            if row.get_bottom()[1] < -2.6:
                self.play(stack.animate.scale(0.88).shift(0.35 * UP), run_time=0.35)
                row.next_to(stack, DOWN, buff=0.28, aligned_edge=LEFT)
            self.play(FadeIn(n, 0.15 * LEFT), FadeIn(body, 0.1 * UP), run_time=1.0)
            stack.add(row)
            self.highlight(body, TEAL)
            self.rest()

        self.narrate("So the answer is " + str(ex["answer"]) + ".")
        ans = formula(ex["answer"], 40, GOLD, 11)
        box = SurroundingRectangle(ans, buff=0.22)
        box.set_stroke(GREEN, 3)
        pack = VGroup(box, ans).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(pack, 0.4 * UP), run_time=0.7)
        self.rest()

    def _example_wants_picture(self, ex):
        if getattr(self, "unit_num", 0) in (3, 4, 5, 6, 7):
            return True
        ans = caretify(ex.get("answer", ""))
        src = str(ex.get("problem", "")) + " " + ans
        if pair_from_text(src):
            return True
        if re.search(r"\(\s*-?\d+(?:\.\d+)?(?:\s*/\s*\d+)?\s*,", ans):
            return True
        return has(ans, "no solution", "infinitely") and getattr(self, "unit_num", 0) in (5, 6)

    def _example_picture(self, ex):
        if getattr(self, "unit_num", 0) == 3:
            blob = " . ".join([ex.get("problem", ""), str(ex.get("answer", ""))])
            return self.anim_slope(0, blob)
        if getattr(self, "unit_num", 0) == 4:
            blob = " . ".join([ex.get("problem", ""), str(ex.get("answer", ""))])
            return self.anim_function(0, blob)
        if getattr(self, "unit_num", 0) == 6:
            blob = " . ".join(
                [ex.get("problem", "")]
                + list(ex.get("steps", []))
                + [str(ex.get("answer", ""))]
            )
            eqs = parse_lin_system(blob)
            pair = pair_from_text(blob)
            if len(eqs) >= 2:
                kind, xy = solve_lin_system(eqs[0], eqs[1])
                return self._elim_graph(eqs[0], eqs[1], kind, xy or pair)
            return self.anim_system(0, blob)
        if getattr(self, "unit_num", 0) == 5:
            blob = " . ".join(
                [ex.get("problem", "")]
                + [str(ex.get("answer", ""))]
            )
            return self.anim_system(0, blob)
        if getattr(self, "unit_num", 0) == 7:
            blob = " ".join(
                [ex.get("problem", "")]
                + list(ex.get("steps", []))
                + [str(ex.get("answer", ""))]
            )
            if has(blob, "volume", "radius", "diameter", "tank", "can has", "cubic"):
                return self.anim_cylinder(0, blob)
            return self.anim_pythag(0, blob)
        ans = caretify(ex.get("answer", ""))
        src = str(ex.get("problem", "")) + " " + ans
        if has(ans, "no solution"):
            return self.demo_sys_parallel(src)
        if has(ans, "infinitely"):
            return self.demo_sys_same_line(src)
        pair = pair_from_text(ans) or pair_from_text(src)
        if pair:
            return self.demo_cross(pair[0], pair[1])
        return None

    def animate_visual(self, kind, beat_i, beat=""):
        makers = {
            "exponent": self.anim_exponent,
            "sci": self.anim_sci,
            "balance": self.anim_balance,
            "slope": self.anim_slope,
            "function": self.anim_function,
            "system": self.anim_system,
            "pythag": self.anim_pythag,
            "cylinder": self.anim_cylinder,
            "scatter": self.anim_scatter,
            "roots": self.anim_roots,
        }
        fn = makers.get(kind)
        return fn(beat_i, beat) if fn else None


    def _card(self, txt, color=TEAL, w=1.35, h=0.95):
        r = RoundedRectangle(w, h, corner_radius=0.12)
        r.set_stroke(color, 3).set_fill(color, 0.14)
        raw = str(txt).strip()
        if raw in "-+" or re.search(r"[=^*/]|x|10", raw):
            t = formula(raw, 28, CREAM, max(8, w * 12))
        else:
            t = T(raw, 28, CREAM, max(8, w * 12))
        if t.get_width() > w * 0.84:
            t.set_width(w * 0.84)
        if t.get_height() > h * 0.72:
            t.set_height(h * 0.72)
        t.move_to(r)
        return VGroup(r, t)

    def demo_show_math(self, text, size=40):
        chunk = extract_math(text)
        t = caretify(text)
        if "=" not in chunk:
            xm = re.search(r"x\s*=\s*-?\d+", t)
            if xm:
                chunk = xm.group(0)
            else:
                dm = re.search(r"does (\d+)", t, re.I)
                if dm:
                    chunk = "x = " + dm.group(1)
        words = re.findall(r"[A-Za-z]{3,}", chunk)
        if len(words) >= 4:
            mob = T(chunk, size, WHITE, 42)
        else:
            mob = formula(chunk, size, WHITE, 12)
        if mob.get_width() > 12.2:
            mob.set_width(12.2)
        mob.move_to(0.2 * DOWN)
        self.play(FadeIn(mob, 0.15 * UP), run_time=0.7)
        return mob

    # ----- exponents: picture matches THIS beat's numbers -----

    def anim_exponent(self, beat_i, beat):
        t = caretify(beat)
        tl = t.lower()
        inside = re.search(r"\(-(\d+)\)\^2", t)
        if has(beat, "inside the power") or (has(beat, "parenthes") and inside):
            n = int(inside.group(1)) if inside else 3
            return self.demo_signed_square(True, n)
        outside = re.search(r"(?<!\()-(\d+)\^2", t)
        if has(beat, "then apply the minus", "square 4 first", "square 3 first") or outside:
            n = int(outside.group(1)) if outside else 3
            return self.demo_signed_square(False, n)
        if has(beat, "irrational") or (has(beat, "rational") and "sqrt" in tl):
            sqs = re.findall(r"sqrt\s*(\d+)", tl)
            irr, rat = "7", "49"
            for s in sqs:
                n = int(s)
                r = int(round(n ** 0.5))
                if r * r == n:
                    rat = s
                else:
                    irr = s
            return self.demo_rational_split(irr, rat)
        if has(beat, "root", "sqrt", "undoes"):
            m = re.search(r"sqrt\s*(\d+)", tl)
            n = int(m.group(1)) if m else 64
            root = int(round(n ** 0.5))
            return self.demo_root_undo(n, root)
        pop = re.search(r"\((\d+)\^(\d+)\)\^(\d+)", t)
        if pop or has(beat, "power of a power"):
            if pop:
                return self.demo_power_of_power(pop.group(1), pop.group(2), pop.group(3))
            return self.demo_power_of_power()
        prod = re.search(r"(\d+)\^(\d+)\s*x\s*\1\^(\d+)", t)
        if prod:
            return self.demo_product_rule(prod.group(1), prod.group(2), prod.group(3))
        bare = re.search(r"([A-Za-z])\^(\d+)\s+x\s+\1(?:\^(\d+))?", t)
        if bare:
            return self.demo_product_rule(bare.group(1), bare.group(2), bare.group(3) or "1")
        quot = re.search(r"(\d+)\^(\d+)\s*/\s*\1\^(\d+)", t)
        if quot or has(beat, "subtract exponents"):
            if quot:
                return self.demo_quotient_rule(quot.group(1), quot.group(2), quot.group(3))
            return self.demo_quotient_rule()
        if has(beat, "coefficient") or re.search(r"\(\d+x", t):
            return self.demo_coeff_product(beat)
        if has(beat, "same base", "add exponents"):
            if prod:
                return self.demo_product_rule(prod.group(1), prod.group(2), prod.group(3))
            return self.demo_product_rule()
        simple = re.search(r"(\d+)\^(\d+)", t)
        if simple:
            return self.demo_factor_stack(int(simple.group(1)), int(simple.group(2)))
        return self.demo_show_math(beat)

    def demo_factor_stack(self, base=4, exp=3):
        base, exp = int(base), int(exp)
        n = max(2, min(exp, 5))
        cards = VGroup(self._card(str(base), TEAL, 1.2))
        for i in range(n - 1):
            cards.add(self._card("× " + str(base), BLUE if i % 2 == 0 else PINK, 1.35))
        cards.arrange(RIGHT, buff=0.16).move_to(0.45 * DOWN)
        running = base
        prod = formula(str(base), 48, GOLD, 8).next_to(cards, DOWN, buff=0.4)
        self.sfx("pop", -12)
        self.play(GrowFromCenter(cards[0]), run_time=0.25)
        self.play(FadeIn(prod, UP), run_time=0.2)
        extras = list(cards)[1:]
        for card in extras:
            self.play(FadeIn(card, LEFT), run_time=0.22)
            running *= base
            prod = self.morph_number(prod, str(running), 48, GOLD)
        self.sfx("ding", -10)
        value = base ** exp
        eq = VGroup(power_mob(str(base), str(exp)), formula("= " + str(value), 32, GOLD, 10)).arrange(RIGHT, buff=0.15)
        eq.next_to(prod, DOWN, buff=0.2)
        self.play(GrowFromCenter(eq), run_time=0.3)
        return VGroup(cards, prod, eq)

    def demo_signed_square(self, parens=True, n=3):
        n = int(n)
        sq = n * n
        if parens:
            left = self._card("(-" + str(n) + ")", BLUE, 1.6)
            right = self._card("(-" + str(n) + ")", PINK, 1.6)
            result = formula(str(sq), 56, GREEN, 8)
            tag = formula("minus is INSIDE", 22, GREEN, 24)
        else:
            left = self._card("-", RED, 0.9)
            right = self._card(str(n) + " × " + str(n), TEAL, 1.7)
            result = formula("-" + str(sq), 56, RED, 8)
            tag = formula("minus is OUTSIDE", 22, RED, 24)
        pair = VGroup(left, right).arrange(RIGHT, buff=0.9).move_to(0.5 * UP + 0.4 * DOWN)
        self.play(FadeIn(left, LEFT), FadeIn(right, RIGHT), run_time=0.35)
        self.sfx("thud", -10)
        self.play(left.animate.shift(0.45 * RIGHT), right.animate.shift(0.45 * LEFT), run_time=0.3)
        result.move_to(0.85 * DOWN)
        tag.next_to(result, DOWN, buff=0.2)
        self.play(GrowFromCenter(result), FadeIn(tag), run_time=0.4)
        self.pop_flash(result.get_center(), GREEN if parens else RED)
        return VGroup(left, right, result, tag)

    def demo_root_undo(self, n=81, root=9):
        sq = Square(1.8).set_stroke(GOLD, 4).set_fill(GOLD, 0.1)
        nine = formula(f"{root} × {root}", 26, CREAM, 12).move_to(sq)
        g = VGroup(sq, nine).move_to(0.2 * LEFT + 0.3 * DOWN)
        self.play(ShowCreation(sq), FadeIn(nine), run_time=0.4)
        arrow = Arrow(g.get_right(), g.get_right() + 2.2 * RIGHT, fill_color=TEAL, buff=0.1)
        out = formula(str(root), 52, TEAL, 8).next_to(arrow, RIGHT, buff=0.2)
        lab = VGroup(radical_mob(str(n), 22, GOLD), formula("= " + str(root), 22, GOLD, 8)).arrange(RIGHT, buff=0.1)
        lab.next_to(g, DOWN, buff=0.35)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(arrow), GrowFromCenter(out), FadeIn(lab), run_time=0.5)
        return VGroup(g, arrow, out, lab)

    def demo_rational_split(self, irr="2", rat="16"):
        irr, rat = str(irr), str(rat)
        root = int(int(rat) ** 0.5)
        good = VGroup(
            radical_mob(rat, 28, TEAL),
            formula("= " + str(root), 28, TEAL, 10),
        ).arrange(RIGHT, buff=0.12)
        bad = VGroup(
            radical_mob(irr, 28, PINK),
            T("never ends", 22, PINK, 16),
        ).arrange(RIGHT, buff=0.12)
        a = formula("rational", 20, TEAL, 16)
        b = formula("irrational", 20, PINK, 16)
        good.move_to(3 * LEFT + 0.2 * DOWN)
        bad.move_to(3 * RIGHT + 0.2 * DOWN)
        a.next_to(good, DOWN, buff=0.2)
        b.next_to(bad, DOWN, buff=0.2)
        self.play(GrowFromCenter(good), FadeIn(a), run_time=0.35)
        self.play(GrowFromCenter(bad), FadeIn(b), run_time=0.35)
        self.play(good.animate.shift(0.12 * UP), bad.animate.shift(0.12 * UP), run_time=0.2)
        self.play(good.animate.shift(0.12 * DOWN), bad.animate.shift(0.12 * DOWN), run_time=0.2)
        return VGroup(good, bad, a, b)

    def demo_power_of_power(self, base="2", inner="3", outer="4"):
        inner, outer = str(inner), str(outer)
        out_exp = str(int(inner) * int(outer))
        inner_m = power_mob(str(base), inner, 42, 22)
        wrapb = RoundedRectangle(2.4, 1.6, corner_radius=0.14).set_stroke(BLUE, 3)
        wrapb.move_to(inner_m)
        g = VGroup(wrapb, inner_m).move_to(2.2 * LEFT + 0.2 * DOWN)
        outer_lab = formula("to the " + outer, 24, GOLD, 16).next_to(g, UR, buff=0.1)
        self.play(GrowFromCenter(g), FadeIn(outer_lab), run_time=0.4)
        arrow = Arrow(g.get_right() + 0.3 * RIGHT, 1.3 * RIGHT, fill_color=GOLD, buff=0.05)
        out = power_mob(str(base), out_exp, 48, 24)
        out.move_to(3.1 * RIGHT + 0.15 * DOWN)
        hint = formula(f"{inner} × {outer} = {out_exp}", 22, TEAL, 16).next_to(out, DOWN, buff=0.2)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(arrow), run_time=0.25)
        self.play(GrowFromCenter(out), FadeIn(hint), run_time=0.4)
        return VGroup(g, outer_lab, arrow, out, hint)

    def demo_product_rule(self, base="3", e1="2", e2="4"):
        e1, e2 = str(e1), str(e2)
        total = str(int(e1) + int(e2))
        a = VGroup(power_mob(str(base), e1), formula("×", 28, TEAL, 4), power_mob(str(base), e2)).arrange(RIGHT, buff=0.18)
        a.move_to(2.3 * LEFT + 0.2 * DOWN)
        self.play(FadeIn(a, LEFT), run_time=0.35)
        plus = formula(f"{e1} + {e2} = {total}", 24, TEAL, 16).next_to(a, DOWN, buff=0.3)
        self.play(FadeIn(plus), run_time=0.35)
        arrow = Arrow(ORIGIN, 1.4 * RIGHT, fill_color=GOLD)
        out = power_mob(str(base), total, 48, 24).move_to(3.0 * RIGHT + 0.15 * DOWN)
        self.sfx("ding", -10)
        self.play(ShowCreation(arrow), GrowFromCenter(out), run_time=0.45)
        return VGroup(a, plus, arrow, out)

    def demo_quotient_rule(self, base="5", e1="7", e2="3"):
        e1, e2 = str(e1), str(e2)
        total = str(int(e1) - int(e2))
        a = VGroup(power_mob(str(base), e1), formula("/", 32, MUTED, 4), power_mob(str(base), e2)).arrange(RIGHT, buff=0.16)
        a.move_to(2.2 * LEFT + 0.2 * DOWN)
        self.play(FadeIn(a, UP), run_time=0.35)
        minus = formula(f"{e1} - {e2} = {total}", 24, PINK, 16).next_to(a, DOWN, buff=0.3)
        self.play(FadeIn(minus), run_time=0.3)
        out = power_mob(str(base), total, 48, 24).move_to(3.0 * RIGHT)
        self.play(GrowFromCenter(out), run_time=0.4)
        return VGroup(a, minus, out)

    def demo_coeff_product(self, beat="(2x³)(5x²) = 10x⁵"):
        t = caretify(beat)
        m = re.search(r"\((\d+)x\^(\d+)\)\s*\((\d+)x\^(\d+)\)", t)
        if m:
            a, e1, b, e2 = m.group(1), m.group(2), m.group(3), m.group(4)
            prod_n = str(int(a) * int(b))
            et = str(int(e1) + int(e2))
        else:
            a, e1, b, e2, prod_n, et = "2", "3", "5", "2", "10", "5"
        left = formula(extract_math(beat), 32, CREAM, 12)
        left.move_to(0.55 * UP)
        if left.get_width() > 12:
            left.set_width(12)
        self.play(FadeIn(left, DOWN), run_time=0.35)
        nums = formula(f"{a} × {b} = {prod_n}", 28, TEAL, 16).move_to(1.5 * LEFT + 0.55 * DOWN)
        vars_ = VGroup(formula(f"x^{e1} × x^{e2} =", 26, GOLD, 12), power_mob("x", et, 36, 20)).arrange(RIGHT, buff=0.12)
        vars_.move_to(2.2 * RIGHT + 0.55 * DOWN)
        self.play(FadeIn(nums, LEFT), FadeIn(vars_, RIGHT), run_time=0.4)
        out = formula(prod_n + "x^" + et, 40, GREEN, 12).move_to(1.35 * DOWN)
        self.sfx("ding", -10)
        self.play(GrowFromCenter(out), run_time=0.35)
        return VGroup(left, nums, vars_, out)

    def _sci_term(self, coeff, exp, size=32):
        return VGroup(
            formula(str(coeff), size, CREAM, 8),
            formula("×", max(22, size - 8), TEAL, 4),
            power_mob("10", str(exp), size, max(16, int(size * 0.55))),
        ).arrange(RIGHT, buff=0.1)

    def _sci_operate(self, scis, op):
        a, e1 = scis[0]
        b, e2 = scis[1]
        if op == "mul":
            lead = Decimal(str(a)) * Decimal(str(b))
            et = e1 + e2
            lead_txt = f"{a} × {b} = {lead}"
            exp_txt = f"{e1} + {e2} = {et}"
        else:
            lead = Decimal(str(a)) / Decimal(str(b))
            et = e1 - e2
            lead_txt = f"{a} / {b} = {lead}"
            exp_txt = f"{e1} - {e2} = {et}"
        if len(scis) >= 3:
            out_c, out_e = scis[2]
        else:
            out_c, out_e = format(lead, "f").rstrip("0").rstrip("."), et
        left = self._sci_term(a, e1, 28)
        right = self._sci_term(b, e2, 28)
        if op == "mul":
            pair = VGroup(left, formula("×", 28, TEAL, 4), right).arrange(RIGHT, buff=0.16)
        else:
            bar = Line(LEFT * 2.4, RIGHT * 2.4).set_stroke(CREAM, 4)
            pair = VGroup(left, bar, right).arrange(DOWN, buff=0.14)
        pair.move_to(1.05 * UP)
        self.play(FadeIn(pair, DOWN), run_time=0.35)
        nums = formula(lead_txt, 26, TEAL, 20).move_to(1.6 * LEFT + 0.35 * DOWN)
        exps = formula(exp_txt, 26, GOLD, 20).move_to(1.8 * RIGHT + 0.35 * DOWN)
        self.play(FadeIn(nums, LEFT), FadeIn(exps, RIGHT), run_time=0.35)
        out = self._sci_term(out_c, out_e, 40).move_to(1.45 * DOWN)
        self.sfx("ding", -10)
        self.play(GrowFromCenter(out), run_time=0.4)
        return VGroup(pair, nums, exps, out)

    def _sci_rewrite(self, scis):
        c1, e1 = scis[0]
        c2, e2 = scis[1]
        hop = int(e2) - int(e1)
        before = self._sci_term(c1, e1, 36).move_to(1.25 * UP)
        self.play(FadeIn(before, DOWN), run_time=0.35)
        hint = formula(str(c1) + " = " + str(c2) + " × 10^" + str(hop), 24, TEAL, 28)
        hint.next_to(before, DOWN, buff=0.3)
        self.play(FadeIn(hint), run_time=0.3)
        after = self._sci_term(c2, e2, 42).move_to(1.05 * DOWN)
        self.sfx("whoosh", -11)
        self.play(GrowFromCenter(after), run_time=0.4)
        return VGroup(before, hint, after)

    # ----- scientific notation / zero & negative exponents -----

    def anim_sci(self, beat_i, beat):
        t = caretify(beat)
        scis = parse_sci(beat)
        if has(beat, "do not read", "minus lives"):
            m = re.search(r"(\d+)\^(-?\d+)", t)
            if m and int(m.group(2)) < 0:
                return self.demo_not_negative_eight(m.group(1), m.group(2))
            return self.demo_not_negative_eight()
        if len(scis) >= 2 and has(beat, "larger", "compare", "beats"):
            return self.demo_sci_compare(scis[0], scis[1])
        if len(scis) >= 2 and has(beat, "adjust", "rewrite", "1-to-10", "not between", "proper"):
            return self._sci_rewrite(scis)
        glued = str(beat).replace(" ", "")
        if has(beat, "when you multiply") and has(beat, "when you divide"):
            return self.demo_sci_rules()
        if len(scis) >= 2 and (")(" in glued or has(beat, "multiply")):
            return self._sci_operate(scis, "mul")
        if len(scis) >= 2 and has(beat, "divide", "quotient"):
            return self._sci_operate(scis, "div")
        if scis:
            return self.demo_sci_expand(scis[0][0], scis[0][1])
        flip = re.search(r"\((\d+)/(\d+)\)\^-1", t)
        if flip or has(beat, "flip"):
            if flip:
                return self.demo_flip_fraction(flip.group(1), flip.group(2))
            return self.demo_flip_fraction()
        if has(beat, "nonzero") or re.search(r"(?<!10)\d+\^0\b", t):
            m = re.search(r"(\d+)\^0", t)
            return self.demo_zero_power(m.group(1) if m else "9")
        if has(beat, "reciprocal", "negative exponent") or re.search(r"(?<!10)\d+\^-\d+", t):
            m = re.search(r"(\d+)\^(-?\d+)", t)
            if m and int(m.group(2)) < 0:
                return self.demo_negative_exp(m.group(1), m.group(2))
            return self.demo_negative_exp()
        return self.demo_show_math(beat)

    def demo_zero_power(self, base="7"):
        seven = power_mob(str(base), "0", 56, 28)
        seven.move_to(2.2 * LEFT)
        self.play(GrowFromCenter(seven), run_time=0.35)
        arrow = Arrow(LEFT * 0.2, RIGHT * 0.9, fill_color=GOLD)
        one = formula("1", 64, GREEN, 6).move_to(2.4 * RIGHT)
        why = formula("anything (not 0) to the 0 is 1", 20, MUTED, 36).to_edge(DOWN, buff=1.15)
        self.sfx("ding", -9)
        self.play(ShowCreation(arrow), GrowFromCenter(one), FadeIn(why), run_time=0.5)
        self.play(WiggleOutThenIn(one, run_time=0.4, n_wiggles=4))
        return VGroup(seven, arrow, one, why)

    def demo_negative_exp(self, base="2", exp="-3"):
        exp_i = abs(int(exp))
        denom = int(base) ** exp_i
        src = power_mob(str(base), str(exp), 48, 26)
        src.move_to(3.0 * LEFT)
        self.play(GrowFromCenter(src), run_time=0.3)
        bar = Line(LEFT * 0.7, RIGHT * 0.7).set_stroke(GOLD, 4)
        top = formula("1", 40, GOLD, 6)
        bot = formula(str(denom), 40, GOLD, 8)
        frac = VGroup(top, bar, bot).arrange(DOWN, buff=0.08).move_to(2.5 * RIGHT)
        mid = T("reciprocal", 20, TEAL, 14)
        self.sfx("whoosh", -10)
        self.play(FadeIn(frac, LEFT), FadeIn(mid, UP), run_time=0.4)
        self.pop_flash(frac.get_center(), TEAL)
        return VGroup(src, frac, mid)

    def demo_not_negative_eight(self, base="2", exp="-3"):
        exp_i = abs(int(str(exp)))
        denom = int(base) ** exp_i
        wrong = VGroup(
            T("not", 22, RED, 8),
            formula("-" + str(denom), 48, RED, 8),
        ).arrange(DOWN, buff=0.12).move_to(2.5 * LEFT)
        self.play(GrowFromCenter(wrong), run_time=0.3)
        self.sfx("wrong", -8)
        cross = VGroup(
            Line(wrong.get_corner(UL), wrong.get_corner(DR)),
            Line(wrong.get_corner(UR), wrong.get_corner(DL)),
        ).set_stroke(RED, 5)
        self.play(ShowCreation(cross), run_time=0.3)
        right = power_mob(str(base), str(exp), 48, 26).move_to(2.4 * RIGHT)
        lab = T("the minus is in the exponent", 22, GOLD, 32).to_edge(DOWN, buff=1.15)
        self.play(GrowFromCenter(right), FadeIn(lab), run_time=0.4)
        return VGroup(wrong, cross, right, lab)

    def demo_flip_fraction(self, num="1", den="2"):
        num, den = str(num), str(den)
        a = formula(num + "/" + den, 48, CREAM, 10).move_to(2.4 * LEFT)
        self.play(FadeIn(a), run_time=0.25)
        shown = den + "/" + num
        if num == "1":
            shown = den + "/" + num + " = " + den
        b = formula(shown, 48, GOLD, 14).move_to(2.3 * RIGHT)
        self.sfx("pop", -11)
        self.play(FadeOut(a), GrowFromCenter(b), run_time=0.45)
        self.remove(a)
        return VGroup(b)

    def demo_sci_expand(self, coeff="3.2", exp=4):
        exp = int(exp)
        result = expand_sci(coeff, exp)
        before = self._sci_term(coeff, exp, 34).move_to(1.55 * UP)
        self.play(FadeIn(before, DOWN), run_time=0.3)
        direction = "right" if exp >= 0 else "left"
        note = T(
            "decimal moves " + str(abs(exp)) + " places " + direction,
            22, TEAL, 36,
        )
        note.next_to(before, DOWN, buff=0.28)
        self.play(FadeIn(note), run_time=0.25)
        chars = list(result)
        tiles = VGroup()
        for ch in chars:
            color = GOLD if ch == "." else (PINK if exp < 0 else (BLUE if int(exp) == 5 else TEAL))
            tiles.add(self._card(ch, color, 0.62 if ch != "." else 0.38, 0.82))
        tiles.arrange(RIGHT, buff=0.08).move_to(0.85 * DOWN)
        self.sfx("whoosh", -11)
        self.play(LaggedStart(*[GrowFromCenter(t) for t in tiles], lag_ratio=0.08), run_time=0.7)
        return VGroup(before, note, tiles)

    def demo_sci_rules(self):
        mul = T("multiply: add the exponents", 32, TEAL, 36)
        div = T("divide: subtract the exponents", 32, GOLD, 36)
        pack = VGroup(mul, div).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(0.15 * DOWN)
        self.play(FadeIn(mul, LEFT), run_time=0.4)
        self.play(FadeIn(div, RIGHT), run_time=0.4)
        return pack

    def demo_sci_compare(self, left, right):
        a, e1 = left
        b, e2 = right
        m1 = VGroup(formula(str(a), 32, CREAM, 8), formula("×", 28, TEAL, 4), power_mob("10", str(e1), 32, 18)).arrange(RIGHT, buff=0.1)
        m2 = VGroup(formula(str(b), 32, CREAM, 8), formula("×", 28, TEAL, 4), power_mob("10", str(e2), 32, 18)).arrange(RIGHT, buff=0.1)
        pair = VGroup(m1, m2).arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(0.2 * DOWN)
        self.play(FadeIn(m1, LEFT), FadeIn(m2, RIGHT), run_time=0.45)
        winner = m1 if e1 > e2 else m2
        tag = formula("compare the power of 10 first", 22, GOLD, 36).to_edge(DOWN, buff=1.05)
        self.highlight(winner, GOLD)
        self.play(FadeIn(tag), run_time=0.3)
        return VGroup(pair, tag)

    # ----- one-variable equations: algebra pictures, not xy-graphs -----

    def anim_balance(self, beat_i, beat):
        t = caretify(beat)
        if has(beat, "no solution", "never true", "contradiction", "nothing works", "numbers disagree", "none"):
            return self.demo_no_solution(beat)
        if has(beat, "identity", "every x", "infinitely", "every x works", "numbers match", "always true"):
            return self.demo_identity(beat)
        if "->" in t or "→" in beat:
            return self.demo_eq_chain(beat)
        if (
            has(beat, "distribut", "minus in front", "hits every", "minus a group", "hidden grouping")
            or re.search(r"-?\d*\([^)]+\)", t.replace(" ", ""))
        ):
            return self.demo_distribute(beat)
        if has(beat, "becomes", "simplifies to"):
            return self.demo_eq_chain(beat)
        if has(beat, "fraction", "decimal", "denominator", "0.5") or re.search(r"/\s*\d", t):
            return self.demo_clear_fraction(beat)
        if has(beat, "stay equal", "parentheses first", "do to the other"):
            return self.demo_scale(beat)
        if has(beat, "both sides", "collect", "x terms", "across the equals"):
            return self.demo_both_sides(beat)
        if has(beat, "check", "original", "make sense"):
            return self.demo_show_math(beat)
        if "=" in beat:
            return self.demo_both_sides(beat)
        return self.demo_scale(beat)

    def _axes_pair(self, xrange=(-1, 8), yrange=(-2, 10), h=3.0, w=3.6):
        axes = Axes(xrange, yrange, height=h, width=w)
        axes.set_stroke(MUTED, 2)
        return axes

    def demo_eq_graph_solve(self, beat):
        """Graph left side vs right side; mark the intersection (the solution)."""
        sol = self._guess_solution(beat)
        axes = self._axes_pair((-1, max(8, sol + 2)), (-2, 12))
        # Generic rising line vs horizontal — shows a unique x meets a constant.
        left = axes.get_graph(lambda x: 0.55 * x + 2.0).set_stroke(BLUE, 5)
        right = axes.get_graph(lambda x: 0.55 * sol + 2.0).set_stroke(PINK, 5)
        x_hit = sol
        y_hit = 0.55 * sol + 2.0
        dot = Dot(axes.c2p(x_hit, y_hit), fill_color=GOLD).scale(1.25)
        tip = formula(f"x = {sol}", 26, GOLD, 12)
        tip.next_to(dot, UR, buff=0.1)
        eq = formula(extract_math(beat), 22, CREAM, 10)
        if eq.get_width() > 5.5:
            eq.set_width(5.5)
        pack = VGroup(axes, left, right)
        g = VGroup(pack, eq).arrange(RIGHT, buff=0.45).move_to(0.25 * DOWN)
        self.play(ShowCreation(axes), FadeIn(eq), run_time=0.35)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(left), run_time=0.45)
        self.play(ShowCreation(right), run_time=0.35)
        self.play(GrowFromCenter(dot), FadeIn(tip), run_time=0.35)
        self.pop_flash(dot.get_center(), GOLD, 0.55)
        return VGroup(g, dot, tip)

    def demo_eq_graph_parallel(self, beat):
        axes = self._axes_pair((-1, 6), (-1, 6))
        l1 = axes.get_graph(lambda x: 0.8 * x + 1.2).set_stroke(BLUE, 5)
        l2 = axes.get_graph(lambda x: 0.8 * x + 2.6).set_stroke(PINK, 5)
        lab = formula("parallel  ->  no solution", 22, RED, 28)
        eq = formula(extract_math(beat), 20, CREAM, 10)
        if eq.get_width() > 11:
            eq.set_width(11)
        pack = VGroup(VGroup(axes, l1, l2), lab, eq).arrange(DOWN, buff=0.18).move_to(0.2 * DOWN)
        self.play(ShowCreation(axes), FadeIn(eq), run_time=0.35)
        self.play(ShowCreation(l1), ShowCreation(l2), run_time=0.55)
        self.sfx("wrong", -9)
        self.play(FadeIn(lab), run_time=0.3)
        return pack

    def demo_eq_graph_same(self, beat):
        axes = self._axes_pair((-1, 6), (-1, 6))
        l1 = axes.get_graph(lambda x: 0.6 * x + 1).set_stroke(BLUE, 8, 0.45)
        l2 = axes.get_graph(lambda x: 0.6 * x + 1).set_stroke(GOLD, 4)
        lab = formula("same line  ->  every x works", 22, GREEN, 32)
        eq = formula(extract_math(beat), 20, CREAM, 10)
        if eq.get_width() > 11:
            eq.set_width(11)
        pack = VGroup(VGroup(axes, l1, l2), lab, eq).arrange(DOWN, buff=0.18).move_to(0.2 * DOWN)
        self.play(ShowCreation(axes), FadeIn(eq), run_time=0.35)
        self.play(ShowCreation(l1), ShowCreation(l2), FadeIn(lab), run_time=0.7)
        self.sfx("success", -10)
        return pack

    def demo_eq_chain(self, beat):
        """Stacked algebra steps only — no xy-graph for one-variable work."""
        raw = caretify(extract_math(beat))
        raw = re.sub(r"\bbecomes\b", "->", raw, flags=re.I)
        raw = re.sub(r"\bsimplifies to\b", "->", raw, flags=re.I)
        raw = re.sub(r",?\s*\bso\b", " -> ", raw, flags=re.I)
        raw = re.sub(r"\.\s*(None|Check|Multiplying).*$", "", raw, flags=re.I)
        chain = formula(raw, 30, CREAM, 11)
        if chain.get_width() > 11.5:
            chain.set_width(11.5)
        if chain.get_height() > 3.6:
            chain.set_height(3.6)
        chain.move_to(0.15 * DOWN)
        self.play(FadeIn(chain, UP), run_time=0.5)
        self.sfx("whoosh", -11)
        return chain

    def demo_number_line_check(self, beat):
        sol = self._guess_solution(beat)
        line = NumberLine(x_range=(-2, max(16, sol + 2), 2), width=10)
        line.set_stroke(MUTED, 3)
        tip = Dot(line.n2p(sol), fill_color=GOLD).scale(1.3)
        lab = formula(f"check x = {sol}", 26, GOLD, 20).next_to(tip, UP, buff=0.25)
        g = VGroup(line, tip, lab).move_to(0.3 * DOWN)
        self.play(ShowCreation(line), run_time=0.4)
        self.sfx("ding", -10)
        self.play(GrowFromCenter(tip), FadeIn(lab), run_time=0.4)
        return g

    def _guess_solution(self, beat):
        t = caretify(beat)
        m = re.search(r"x\s*=\s*(-?\d+(?:\.\d+)?)", t)
        if m:
            try:
                return float(m.group(1)) if "." in m.group(1) else int(m.group(1))
            except ValueError:
                pass
        # Common curriculum answers used as graph targets.
        for val in (16, 14, 11, 10, 8, 5, 4, 3, 18, 6):
            if re.search(rf"(?<!\d){val}(?!\d)", t):
                return val
        return 4

    def demo_scale(self, beat=""):
        left_txt, right_txt = "left", "right"
        if beat:
            chunk = caretify(extract_math(beat))
            chunk = re.sub(r"\bbecomes\b.*", "", chunk, flags=re.I)
            if "=" in chunk:
                left_txt, right_txt = chunk.split("=", 1)
                left_txt = left_txt.strip()
                right_txt = re.split(r"[.!?]", right_txt)[0].strip()
                if len(left_txt) > 28 or len(right_txt) > 28:
                    left_txt, right_txt = "left", "right"
        lw = max(1.6, min(3.6, 0.28 * max(4, len(left_txt)) + 0.7))
        rw = max(1.5, min(3.6, 0.28 * max(3, len(right_txt)) + 0.7))
        base = Line(LEFT * 2.4, RIGHT * 2.4).set_stroke(MUTED, 5)
        fulcrum = Triangle().set_fill(GOLD, 1).set_stroke(width=0).scale(0.28)
        fulcrum.next_to(base, DOWN, buff=0)
        left = self._card(left_txt, BLUE, lw, 0.85)
        right = self._card(right_txt, TEAL, rw, 0.85)
        left.move_to(1.45 * LEFT + 0.72 * UP)
        right.move_to(1.45 * RIGHT + 0.72 * UP)
        g = VGroup(base, fulcrum, left, right).move_to(0.35 * DOWN)
        self.play(ShowCreation(base), GrowFromCenter(fulcrum), run_time=0.35)
        self.sfx("thud", -11)
        self.play(FadeIn(left, DOWN), FadeIn(right, DOWN), run_time=0.3)
        self.play(g.animate.rotate(0.1), run_time=0.2)
        self.play(g.animate.rotate(-0.2), run_time=0.25)
        self.play(g.animate.rotate(0.1), run_time=0.2)
        return g

    def demo_distribute(self, beat="3(x + 4) = 3x + 12"):
        t = caretify(beat)
        fac_s, inner = "a", "b + c"
        m = re.search(r"((?:-?\d+(?:\.\d+)?)|-)\s*\(\s*([^)]+?)\s*\)", t)
        numeric = False
        if m:
            fac_s, inner = m.group(1), m.group(2).strip()
            numeric = True
        fac_n = -1 if fac_s in ("-", "-1") else (int(float(fac_s)) if numeric and fac_s else 1)

        def split_terms(s):
            u = s.replace(" ", "")
            if not u:
                return []
            if u[0] not in "+-":
                u = "+" + u
            return re.findall(r"[+-][^+-]+", u)

        def mul_one(term):
            sign = -1 if term.startswith("-") else 1
            body = term[1:]
            if body == "x":
                n, var = 1, "x"
            elif body.endswith("x") and re.fullmatch(r"\d*x", body):
                num = body[:-1]
                n, var = (int(num) if num else 1), "x"
            elif re.fullmatch(r"\d+(?:\.\d+)?", body):
                n, var = int(float(body)), ""
            else:
                return None
            tot = fac_n * sign * n
            if var:
                if tot == 1:
                    return "x"
                if tot == -1:
                    return "-x"
                return str(tot) + "x"
            return str(tot)

        def join_out(parts):
            bits = []
            for i, p in enumerate(parts):
                if i == 0:
                    bits.append(p)
                elif p.startswith("-"):
                    bits.append("- " + p[1:])
                else:
                    bits.append("+ " + p.lstrip("+"))
            return " ".join(bits)

        if not numeric:
            return self.demo_show_math(beat)
        terms = split_terms(inner)
        products = [mul_one(term) for term in terms] if terms else []
        if not products or any(p is None for p in products):
            out_txt = inner
        else:
            out_txt = join_out(products)
        eq = formula(extract_math(beat), 28, CREAM, 11)
        if eq.get_width() > 11.5:
            eq.set_width(11.5)
        eq.move_to(0.9 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        box_w = max(3.4, min(6.2, 0.42 * max(8, len(inner)) + 1.6))
        box = RoundedRectangle(box_w, 1.05, corner_radius=0.12).set_stroke(BLUE, 3)
        inside = formula(inner, 28, CREAM, box_w - 0.4)
        if inside.get_width() > box_w * 0.82:
            inside.set_width(box_w * 0.82)
        inside.move_to(box)
        factor = formula(str(fac_n) if fac_s != "-" else "-1", 36, GOLD, 6)
        factor.next_to(box, LEFT, buff=0.3)
        group = VGroup(factor, box, inside).move_to(0.28 * DOWN)
        a1 = Arrow(factor.get_right() + 0.08 * UP, inside.get_left() + 0.12 * LEFT + 0.16 * UP, fill_color=GOLD, buff=0.04)
        a2 = Arrow(factor.get_right() + 0.08 * DOWN, inside.get_right() + 0.05 * LEFT + 0.16 * DOWN, fill_color=TEAL, buff=0.04)
        out = formula(out_txt, 32, GREEN, 12).next_to(group, DOWN, buff=0.32)
        self.play(FadeIn(factor), ShowCreation(box), FadeIn(inside), run_time=0.4)
        self.sfx("pop", -11)
        self.play(ShowCreation(a1), ShowCreation(a2), run_time=0.35)
        self.play(GrowFromCenter(out), run_time=0.3)
        return VGroup(eq, group, a1, a2, out)

    def demo_both_sides(self, beat="6x - 7 = 5x + 7"):
        t = caretify(beat)
        chunk = extract_math(beat)
        left_txt, right_txt = "x terms", "numbers"
        if "=" in chunk:
            left_txt, right_txt = caretify(chunk).split("=", 1)
            left_txt = left_txt.strip()
            right_txt = re.split(r"[.!?]", right_txt)[0].strip()
            right_txt = re.split(r"\bbecomes\b|->", right_txt, flags=re.I)[0].strip()
        eq = formula(chunk if "=" in chunk else t, 28, CREAM, 11)
        if eq.get_width() > 11.5:
            eq.set_width(11.5)
        eq.move_to(0.95 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        lw = max(1.7, min(3.8, 0.26 * max(4, len(left_txt)) + 0.8))
        rw = max(1.6, min(3.8, 0.26 * max(3, len(right_txt)) + 0.8))
        left = self._card(left_txt, BLUE, lw, 0.9)
        right = self._card(right_txt, TEAL, rw, 0.9)
        mid = formula("=", 32, GOLD, 4)
        row = VGroup(left, mid, right).arrange(RIGHT, buff=0.28).move_to(0.15 * DOWN)
        self.play(FadeIn(row), run_time=0.35)
        self.sfx("thud", -11)
        xm = re.search(r"x\s*=\s*(-?\d+)", t)
        extras = VGroup(eq, row)
        if xm:
            ans = formula("x = " + xm.group(1), 32, GREEN, 10).next_to(row, DOWN, buff=0.32)
            self.play(GrowFromCenter(ans), run_time=0.3)
            extras.add(ans)
        return extras

    def demo_no_solution(self, beat="x + 1 = x + 4"):
        t = caretify(beat)
        falses = []
        for a, b in re.findall(r"(?<![A-Za-zx*/])(-?\d+)\s*=\s*(-?\d+)(?![x\d.])", t):
            if a != b:
                key = a + " = " + b
                if key not in falses:
                    falses.append(key)
        shown = " ,  ".join(falses) if falses else extract_math(beat)
        eq = formula(shown, 36, CREAM, 12)
        if eq.get_width() > 12:
            eq.set_width(12)
        eq.move_to(0.45 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        no = formula("no solution", 36, RED, 20).move_to(0.55 * DOWN)
        self.sfx("wrong", -9)
        self.play(GrowFromCenter(no), run_time=0.35)
        return VGroup(eq, no)

    def demo_identity(self, beat="2(x + 1) = 2x + 2"):
        t = caretify(beat)
        trues = []
        for a, b in re.findall(r"(?<![A-Za-zx*/])(-?\d+)\s*=\s*(-?\d+)(?![x\d.])", t):
            if a == b:
                key = a + " = " + b
                if key not in trues:
                    trues.append(key)
        shown = trues[0] if trues else extract_math(beat)
        eq = formula(shown, 36, CREAM, 12)
        if eq.get_width() > 12:
            eq.set_width(12)
        eq.move_to(0.45 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        yes = formula("always true", 32, GREEN, 20).move_to(0.5 * DOWN)
        self.sfx("success", -10)
        self.play(GrowFromCenter(yes), run_time=0.4)
        return VGroup(eq, yes)

    def demo_clear_fraction(self, beat="(x + 2)/3 = 4"):
        t = caretify(beat)
        if "->" in t:
            return self.demo_eq_chain(beat)
        left_s, right_s, denom = None, None, None
        m = re.search(r"\(([^)]+)\)\s*/\s*(\d+)\s*=\s*(-?\d+)", t)
        m2 = re.search(r"\bx\s*/\s*(\d+)\s*([+-]\s*\d+)?\s*=\s*(-?\d+)", t)
        m3 = re.search(r"0\.5\s*x\s*=\s*(-?\d+)", t)
        if m:
            left_s, denom, right_s = "(" + m.group(1) + ")/" + m.group(2), m.group(2), m.group(3)
        elif m2:
            extra = (m2.group(2) or "").replace(" ", "")
            left_s = "x/" + m2.group(1) + extra
            denom, right_s = m2.group(1), m2.group(3)
        elif m3:
            left_s, denom, right_s = "0.5x", "2", m3.group(1)
        if left_s is None:
            chunk = extract_math(beat)
            if "=" in chunk:
                left_s, right_s = chunk.split("=", 1)
                left_s, right_s = left_s.strip(), right_s.strip()
            else:
                left_s, right_s = "left", "right"
            denom = "d"
        eq = formula(extract_math(beat), 28, CREAM, 11)
        if eq.get_width() > 11:
            eq.set_width(11)
        eq.move_to(0.85 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        lw = max(2.2, min(4.2, 0.28 * max(6, len(left_s)) + 0.9))
        rw = max(1.5, min(3.2, 0.28 * max(3, len(right_s)) + 0.8))
        left = self._card(left_s, BLUE, lw, 0.9)
        right = self._card(right_s, TEAL, rw, 0.9)
        pair = VGroup(left, formula("=", 28, GOLD, 4), right).arrange(RIGHT, buff=0.25).move_to(0.2 * DOWN)
        times = formula("times " + str(denom) + " on both sides", 22, TEAL, 32).next_to(pair, DOWN, buff=0.28)
        self.play(FadeIn(pair), run_time=0.35)
        self.sfx("whoosh", -11)
        self.play(pair.animate.scale(1.08), FadeIn(times), run_time=0.35)
        return VGroup(eq, pair, times)

    # ----- slope: different lines each beat -----

    def _fmt_slope(self, v):
        v = float(v)
        if abs(v - round(v)) < 1e-8:
            return str(int(round(v)))
        for d in (2, 3, 4, 5, 6, 8):
            n = round(v * d)
            if abs(v * d - n) < 1e-6:
                return f"{int(n)}/{d}"
        return f"{v:.2f}"

    def _fmt_line_eq(self, m, b):
        ms = self._fmt_slope(m)
        if abs(float(b)) < 1e-9:
            return f"y = {ms}x"
        bs = self._fmt_slope(abs(b))
        sign = "+" if float(b) >= 0 else "-"
        return f"y = {ms}x {sign} {bs}"

    def _to_slope_f(self, s):
        s = str(s).strip()
        if "/" in s:
            n, d = s.split("/", 1)
            den = float(d)
            return float(n) / den if den else 0.0
        return float(s)

    def _slope_window(self, lines, pts=None, verts=None, horizs=None, square=False):
        xs = [-1.0, 0.0, 4.0]
        ys = [-1.0, 0.0, 1.0]
        for ln in lines or []:
            m, b = float(ln[0]), float(ln[1])
            ys.append(b)
            xs.append(0.0)
            far = (-1, 1, 2, 3, 4) if abs(b) > 8 or abs(m) > 4 else (-2, 1, 2, 3, 5, 8)
            for xv in far:
                xs.append(xv)
                ys.append(m * xv + b)
        for p in pts or []:
            xs.append(float(p[0]))
            ys.append(float(p[1]))
        for xv in verts or []:
            xs.append(float(xv))
        for yv in horizs or []:
            ys.append(float(yv))
        xmin, xmax = min(xs) - 1.1, max(xs) + 1.1
        ymin, ymax = min(ys) - 1.1, max(ys) + 1.1
        if xmax - xmin < 6:
            pad = (6 - (xmax - xmin)) / 2
            xmin -= pad
            xmax += pad
        if ymax - ymin < 6:
            pad = (6 - (ymax - ymin)) / 2
            ymin -= pad
            ymax += pad
        if square:
            sp = max(xmax - xmin, ymax - ymin)
            cx, cy = (xmin + xmax) / 2, (ymin + ymax) / 2
            xmin, xmax = cx - sp / 2, cx + sp / 2
            ymin, ymax = cy - sp / 2, cy + sp / 2

        def step(span):
            if span <= 8:
                return 1
            if span <= 16:
                return 2
            if span <= 40:
                return 5
            if span <= 80:
                return 10
            return 20

        return (xmin, xmax, step(xmax - xmin)), (ymin, ymax, step(ymax - ymin))

    def _draw_slope_fn(self, axes, m, b, color, width=5):
        mm, bb = float(m), float(b)
        try:
            line = axes.get_graph(lambda x, a=mm, c=bb: a * x + c)
            line.set_stroke(color, width)
            return line
        except Exception:
            xr = axes.x_range
            x0, x1 = float(xr[0]), float(xr[1])
            return Line(axes.c2p(x0, mm * x0 + bb), axes.c2p(x1, mm * x1 + bb)).set_stroke(color, width)

    def _parse_slope_beat(self, beat):
        t = caretify(beat)
        compact = re.sub(r"[fgh]\(x\)=", "y=", t.replace(" ", ""))
        num = r"-?\d+(?:\.\d+)?(?:/\d+)?"
        lines, verts, horizs = [], [], []
        for m in re.finditer(
            rf"y=\(?(?P<m>{num})\)?x(?:(?P<sg>[+-])(?P<b>\d+(?:\.\d+)?(?:/\d+)?))?",
            compact,
        ):
            slope = self._to_slope_f(m.group("m"))
            b = 0.0
            if m.group("b") is not None:
                b = self._to_slope_f(m.group("b"))
                if m.group("sg") == "-":
                    b = -b
            lines.append((slope, b, compact[m.start():m.end()]))
        for m in re.finditer(rf"y=(?P<b>{num})\+(?P<m>{num})x", compact):
            slope = self._to_slope_f(m.group("m"))
            b = self._to_slope_f(m.group("b"))
            key = (round(slope, 6), round(b, 6))
            if all(abs(key[0] - ln[0]) > 1e-6 or abs(key[1] - ln[1]) > 1e-6 for ln in lines):
                lines.append((slope, b, compact[m.start():m.end()]))
        for m in re.finditer(r"(?P<a>-?\d+)x(?P<bs>[+-])(?P<bb>\d+)y=(?P<c>-?\d+)", compact):
            # Reject "y=-2x+4y=-2x+4" glued twice (looks like 2x+4y=-2).
            if m.start() > 0 and compact[m.start() - 1] in "=-":
                continue
            a = float(m.group("a"))
            bco = float(m.group("bb")) * (1 if m.group("bs") == "+" else -1)
            c = float(m.group("c"))
            if abs(bco) < 1e-9:
                continue
            slope = -a / bco
            b = c / bco
            lines.append((slope, b, compact[m.start():m.end()]))
        for m in re.finditer(rf"(?<![A-Za-z0-9])x=(?P<k>{num})(?!\d)(?![xy])", compact):
            prefix = compact[max(0, m.start() - 10):m.start()].lower()
            if "set" in prefix or "when" in prefix:
                continue
            verts.append(self._to_slope_f(m.group("k")))
        for m in re.finditer(rf"(?<![A-Za-z0-9])y=(?P<k>{num})(?!\d)(?![x(]|[+-]\d)", compact):
            prefix = compact[max(0, m.start() - 10):m.start()].lower()
            if "set" in prefix or "when" in prefix:
                continue
            horizs.append(self._to_slope_f(m.group("k")))
        pts = [(int(a), int(b)) for a, b in re.findall(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", t)]
        return lines, verts, horizs, pts, t

    def anim_slope(self, beat_i, beat):
        lines, verts, horizs, pts, t = self._parse_slope_beat(beat)
        uniq = []
        for ln in lines:
            if not any(abs(ln[0] - u[0]) < 1e-6 and abs(ln[1] - u[1]) < 1e-6 for u in uniq):
                uniq.append(ln)
        lines = uniq
        tl = t.lower()
        want_par = has(beat, "parallel")
        want_perp = has(beat, "perpendicular")
        want_steps = has(beat, "step", "climbs", "rise over run", "equal x-steps", "up 1")

        if len(lines) >= 2:
            m1, b1, _ = lines[0]
            m2, b2, _ = lines[1]
            lab1 = self._fmt_line_eq(m1, b1)
            if abs(m1 - m2) < 1e-6 and abs(b1 - b2) > 1e-6:
                return self.demo_parallel(
                    m1, b1, b2, f"same slope {self._fmt_slope(m1)}  never meet"
                )
            if want_perp:
                return self.demo_perp(m1, b1, m2, b2)
            return self.demo_slope_line(m1, lab1, intercept=b1, m2=m2, b2=b2, points=pts)

        if len(lines) == 1:
            m, b, raw = lines[0]
            lab = self._fmt_line_eq(m, b)
            if abs(m) < 1e-9:
                lab = f"y = {self._fmt_slope(b)}  m = 0"
            # "set x = 0" in intercept work is not a vertical line.
            if verts and abs(m) < 1e-9:
                return self.demo_vertical(verts[0], y_flat=b)
            return self.demo_slope_line(m, lab, intercept=b, points=pts, show_steps=want_steps)

        if verts and horizs:
            if want_perp:
                return self.demo_perp(0, horizs[0], vertical_x=verts[0],
                                     label="horizontal meets vertical")
            return self.demo_vertical(verts[0], y_flat=horizs[0])
        if verts:
            return self.demo_vertical(verts[0])
        if horizs:
            k = horizs[0]
            return self.demo_slope_line(0, f"y = {self._fmt_slope(k)}  m = 0", intercept=k)

        if len(pts) >= 2:
            x1, y1 = pts[0]
            x2, y2 = pts[1]
            run = x2 - x1
            rise = y2 - y1
            if run == 0:
                return self.demo_vertical(x1)
            m = rise / run
            b = y1 - m * x1
            lab = f"m = {rise}/{run}"
            return self.demo_slope_line(m, lab, intercept=b, points=pts, show_steps=True)

        ur = re.search(r"up\s+(-?\d+).{0,24}right\s+(-?\d+)", tl)
        if has(beat, "up 1") and has(beat, "right 2") and has(beat, "right 4"):
            return self.demo_similar_stairs()
        if ur:
            rise, run = int(ur.group(1)), int(ur.group(2))
            m = rise / run if run else 0
            return self.demo_slope_line(m, f"up {rise}, right {run}", intercept=0,
                                        points=[(0, 0), (run, rise), (2 * run, 2 * rise)],
                                        show_steps=True)

        rec = re.search(r"reciprocals?:\s*(-?\d+(?:/\d+)?)\s+and\s+(-?\d+(?:/\d+)?)", tl)
        if rec or (want_perp and not want_par and not has(beat, "horizontal", "vertical")):
            m1 = self._to_slope_f(rec.group(1)) if rec else 2.0
            m2 = self._to_slope_f(rec.group(2)) if rec else -0.5
            return self.demo_perp(m1, 2, m2, 4)

        if want_par:
            return self.demo_parallel(0.5, 1, 3)
        if want_perp and has(beat, "horizontal", "vertical"):
            return self.demo_perp(0, 2, vertical_x=3, label="horizontal meets vertical")
        if want_perp:
            return self.demo_perp(2, 2, -0.5, 4)
        if has(beat, "horizontal") and has(beat, "vertical", "undefined"):
            return self.demo_vertical(2, y_flat=3)
        if has(beat, "horizontal") or has(beat, "slope 0"):
            return self.demo_slope_line(0, "m = 0  flat", intercept=3)
        if has(beat, "vertical", "undefined"):
            return self.demo_vertical(2)

        if has(beat, "rise over run", "change in y"):
            return self.demo_slope_line(1, "rise / run", intercept=1,
                                        points=[(0, 1), (2, 3)], show_steps=True)
        if has(beat, "positive") and has(beat, "negative", "falls"):
            return self.demo_slope_line(1.5, "climbs  /  falls", intercept=0.5, m2=-1, b2=4)
        if has(beat, "origin") or has(beat, "b is missing"):
            return self.demo_slope_line(3, "y = 3x  through origin", intercept=0)
        if has(beat, "y-axis") or (has(beat, "intercept") and has(beat, "slope") and "m is" in tl):
            return self.demo_slope_line(1, "m slope   b intercept", intercept=3)
        if has(beat, "step", "next point"):
            return self.demo_slope_line(1, "from b, step with m", intercept=-3, show_steps=True)
        if has(beat, "plug") or has(beat, "two points"):
            return self.demo_slope_line(2, "two points to m, then b", intercept=6,
                                        points=[(0, 6), (2, 10)])
        if has(beat, "picture of that equation"):
            return self.demo_slope_line(2, "y = 2x - 1", intercept=-1, points=[(2, 3), (4, 7)])
        if has(beat, "second point"):
            return self.demo_slope_line(2, "check (4, 7)", intercept=-1, points=[(4, 7)])
        if has(beat, "set x = 0") or (has(beat, "y-intercept") and has(beat, "x-intercept")):
            return self.demo_slope_line(-1, "x and y intercepts", intercept=7,
                                        points=[(0, 7), (7, 0)])
        if has(beat, "standard form", "fastest two"):
            return self.demo_slope_line(-1, "plot the intercepts", intercept=5,
                                        points=[(0, 5), (5, 0)])
        if has(beat, "rate") and has(beat, "start"):
            return self.demo_slope_line(4, "m rate   b start", intercept=8)
        if has(beat, "two plans", "meeting point", "system"):
            return self.demo_slope_line(5, "two plans meet", intercept=20, m2=10, b2=5,
                                        points=[(3, 35)])
        if has(beat, "drain"):
            return self.demo_slope_line(-3, "draining", intercept=9)
        if has(beat, "hours", "liters", "read a point"):
            return self.demo_slope_line(-4, "(3, 12) on the line", intercept=24, points=[(3, 12)])
        if has(beat, "equal x-steps", "straight", "constant rate"):
            return self.demo_slope_line(3, "equal steps", intercept=1, show_steps=True)
        if has(beat, "negative", "falls"):
            return self.demo_slope_line(-2, "m = -2  falls", intercept=4)

        h = sum(ord(c) for c in t) + 17 * int(beat_i or 0)
        slopes = (0.5, 1, 1.5, 3, -0.5, -1, -1.5, 0.75, 2.5)
        intercepts = (0, 1, 2, 3, 4, -1, -2, 0.5, 2.5, 5)
        m = slopes[h % len(slopes)]
        b = intercepts[(h // 9) % len(intercepts)]
        if abs(m - 2) < 1e-9 and abs(b - 1) < 1e-9:
            b = 3
        return self.demo_slope_line(m, f"m = {self._fmt_slope(m)}", intercept=b)

    def _slope_caption(self, text, size=22, color=GOLD):
        s = str(text).replace("→", ", so ").replace("->", ", so ")
        s = re.sub(r"\s+([,.;:?!])", r"\1", s)
        s = re.sub(r"\s{2,}", " ", s).strip()
        mob = Text(s, font=FONT_MATH, font_size=size).set_color(color)
        if mob.get_width() > 10.2:
            mob.set_width(10.2)
        return mob

    def _pt_label(self, px, py):
        return f"({self._fmt_slope(px)}, {self._fmt_slope(py)})"

    def demo_similar_stairs(self):
        xr, yr = self._slope_window([(0.5, 0)], pts=[(0, 0), (2, 1), (4, 2)])
        axes = Axes(xr, yr, height=3.2, width=3.8)
        axes.set_stroke(MUTED, 2)
        line = self._draw_slope_fn(axes, 0.5, 0, GOLD, 5)
        small_run = Line(axes.c2p(0, 0), axes.c2p(2, 0)).set_stroke(TEAL, 5)
        small_rise = Line(axes.c2p(2, 0), axes.c2p(2, 1)).set_stroke(PINK, 5)
        big_run = Line(axes.c2p(0, 0), axes.c2p(4, 0)).set_stroke(TEAL, 3)
        big_rise = Line(axes.c2p(4, 0), axes.c2p(4, 2)).set_stroke(PINK, 3)
        d0 = Dot(axes.c2p(0, 0), fill_color=BLUE)
        d1 = Dot(axes.c2p(2, 1), fill_color=GOLD)
        d2 = Dot(axes.c2p(4, 2), fill_color=GOLD)
        a = self._slope_caption("up 1, right 2", 18, TEAL).next_to(small_run, DOWN, buff=0.08)
        b = self._slope_caption("up 2, right 4", 18, PINK).next_to(big_rise, RIGHT, buff=0.08)
        lab = self._slope_caption("same slope 1/2")
        g = VGroup(axes, line, big_run, big_rise, small_run, small_rise, d0, d1, d2, a, b)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(axes), ShowCreation(line), run_time=0.5)
        self.play(ShowCreation(small_run), ShowCreation(small_rise), FadeIn(a), run_time=0.4)
        self.play(ShowCreation(big_run), ShowCreation(big_rise), FadeIn(b), run_time=0.4)
        self.play(GrowFromCenter(d0), GrowFromCenter(d1), GrowFromCenter(d2), FadeIn(lab), run_time=0.3)
        return VGroup(pack, a, b)

    def demo_slope_line(self, m, label, intercept=1, points=None, show_steps=False, m2=None, b2=None):
        extra = [(m2, b2)] if m2 is not None else []
        xr, yr = self._slope_window([(m, intercept)] + extra, pts=points, square=False)
        axes = Axes(xr, yr, height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        line = self._draw_slope_fn(axes, m, intercept, GOLD, 5)
        drawn = [axes, line]
        line2 = None
        if m2 is not None:
            line2 = self._draw_slope_fn(axes, m2, b2 if b2 is not None else 0, PINK, 5)
            drawn.append(line2)
        dots = []
        pt_labs = []
        if points:
            for i, (px, py) in enumerate(points):
                col = BLUE if i == 0 else GOLD
                d = Dot(axes.c2p(float(px), float(py)), fill_color=col).scale(1.15)
                dots.append(d)
                pl = self._slope_caption(self._pt_label(px, py), 16, col)
                pl.next_to(d, UR, buff=0.08)
                pt_labs.append(pl)
        g = VGroup(*drawn, *dots, *pt_labs)
        lab = self._slope_caption(label)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.15).move_to(0.35 * DOWN)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(ShowCreation(line), run_time=0.5)
        if line2 is not None:
            self.play(ShowCreation(line2), run_time=0.45)
        if dots:
            self.play(*[GrowFromCenter(d) for d in dots], *[FadeIn(p) for p in pt_labs], run_time=0.3)
        steps = []
        if show_steps and points and len(points) >= 2:
            x1, y1 = float(points[0][0]), float(points[0][1])
            x2, y2 = float(points[1][0]), float(points[1][1])
            run_seg = Line(axes.c2p(x1, y1), axes.c2p(x2, y1)).set_stroke(TEAL, 4)
            rise_seg = Line(axes.c2p(x2, y1), axes.c2p(x2, y2)).set_stroke(PINK, 4)
            self.play(ShowCreation(run_seg), ShowCreation(rise_seg), run_time=0.4)
            steps.extend([run_seg, rise_seg])
        elif show_steps:
            x0 = 0.0
            run = 2.0 if abs(float(m) - 0.5) < 1e-6 else 1.0
            y0 = float(m) * x0 + float(intercept)
            run_seg = Line(axes.c2p(x0, y0), axes.c2p(x0 + run, y0)).set_stroke(TEAL, 4)
            rise_seg = Line(axes.c2p(x0 + run, y0), axes.c2p(x0 + run, y0 + float(m) * run)).set_stroke(PINK, 4)
            self.play(ShowCreation(run_seg), ShowCreation(rise_seg), run_time=0.4)
            steps.extend([run_seg, rise_seg])
        idot = Dot(axes.c2p(0, intercept), fill_color=TEAL)
        extras = [idot]
        on_pt = points and any(
            abs(float(p[0])) < 1e-6 and abs(float(p[1]) - float(intercept)) < 1e-6 for p in points
        )
        if not on_pt:
            ilab = self._slope_caption(self._pt_label(0, intercept), 16, TEAL)
            ilab.next_to(idot, LEFT, buff=0.1)
            extras.append(ilab)
        self.play(GrowFromCenter(idot), FadeIn(lab), run_time=0.28)
        if len(extras) > 1:
            self.play(FadeIn(extras[1]), run_time=0.2)
        if line2 is None:
            try:
                self.play(MoveAlongPath(idot, line), run_time=0.8)
            except Exception:
                self.play(idot.animate.shift(0.4 * RIGHT), run_time=0.35)
        return VGroup(pack, *extras, *steps)

    def demo_vertical(self, x=2, y_flat=None, label=None):
        xr, yr = self._slope_window([], verts=[x], horizs=[y_flat] if y_flat is not None else None)
        axes = Axes(xr, yr, height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        vline = Line(axes.c2p(float(x), yr[0]), axes.c2p(float(x), yr[1])).set_stroke(PINK, 5)
        parts = [axes, vline]
        if y_flat is not None:
            hline = Line(axes.c2p(xr[0], float(y_flat)), axes.c2p(xr[1], float(y_flat))).set_stroke(TEAL, 5)
            parts.append(hline)
            shown = label or f"x = {self._fmt_slope(x)}  y = {self._fmt_slope(y_flat)}"
        else:
            shown = label or f"x = {self._fmt_slope(x)}  undefined slope"
        lab = self._slope_caption(shown, 22, PINK)
        g = VGroup(*parts)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(vline), run_time=0.5)
        if y_flat is not None:
            self.play(ShowCreation(parts[-1]), run_time=0.35)
        self.play(FadeIn(lab), run_time=0.25)
        return pack

    def demo_parallel(self, m=0.5, b1=1, b2=3, label=None):
        xr, yr = self._slope_window([(m, b1), (m, b2)])
        axes = Axes(xr, yr, height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        l1 = self._draw_slope_fn(axes, m, b1, BLUE, 4)
        l2 = self._draw_slope_fn(axes, m, b2, GOLD, 4)
        shown = label or f"same slope {self._fmt_slope(m)}  never meet"
        lab = self._slope_caption(shown, 20, TEAL)
        g = VGroup(axes, l1, l2)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(ShowCreation(l1), ShowCreation(l2), FadeIn(lab), run_time=0.7)
        return pack

    def demo_perp(self, m1=2, b1=2, m2=-0.5, b2=4, label=None, vertical_x=None):
        lines = [(m1, b1)]
        verts = [vertical_x] if vertical_x is not None else []
        if vertical_x is None:
            lines.append((m2, b2))
        xr, yr = self._slope_window(lines, verts=verts, square=True)
        axes = Axes(xr, yr, height=3.3, width=3.3)
        axes.set_stroke(MUTED, 2)
        l1 = self._draw_slope_fn(axes, m1, b1, BLUE, 4)
        if vertical_x is not None:
            l2 = Line(axes.c2p(float(vertical_x), yr[0]), axes.c2p(float(vertical_x), yr[1])).set_stroke(PINK, 5)
            ix, iy = float(vertical_x), float(m1) * float(vertical_x) + float(b1)
        else:
            l2 = self._draw_slope_fn(axes, m2, b2, PINK, 4)
            if abs(float(m1) - float(m2)) > 1e-6:
                ix = (float(b2) - float(b1)) / (float(m1) - float(m2))
                iy = float(m1) * ix + float(b1)
            else:
                ix, iy = 0.0, float(b1)
        if vertical_x is None:
            shown = label or f"slopes  {self._fmt_slope(m1)}  and  {self._fmt_slope(m2)}"
        else:
            shown = label or "horizontal meets vertical"
        lab = self._slope_caption(shown, 20, GOLD)
        g = VGroup(axes, l1, l2)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(ShowCreation(l1), ShowCreation(l2), run_time=0.65)
        elbow = Square(side_length=0.22).set_stroke(GOLD, 3).set_fill(GOLD, 0)
        elbow.move_to(axes.c2p(ix, iy))
        self.play(GrowFromCenter(elbow), FadeIn(lab), run_time=0.35)
        return VGroup(pack, elbow)

    # ----- functions -----

    def _fn_num(self, v):
        if v is None:
            return ""
        if abs(float(v) - round(float(v))) < 1e-9:
            return str(int(round(float(v))))
        return f"{float(v):.1f}"

    def _parse_fn(self, beat):
        t = caretify(beat)
        compact = t.replace(" ", "")
        spec = {
            "kind": "linear",
            "m": 2.0,
            "b": -1.0,
            "xin": 3,
            "yout": 5,
            "label": "2x - 1",
            "fn_name": "f",
            "var": "x",
            "parsed": False,
            "solve": None,
            "marks": [],
        }
        if has(beat, "v-shape") or "|x|" in compact.lower() or has(beat, "each piece is a line"):
            spec.update(kind="abs", label="|x|", xin=2, yout=2, parsed=True)
            return spec
        if "2^x" in compact.lower() or has(beat, "grows by multiplying"):
            spec.update(kind="exp", label="2^x", xin=3, yout=8, parsed=True)
            return spec
        if has(beat, "area") and has(beat, "square"):
            spec.update(kind="quad", label="s^2", fn_name="A", var="s", xin=6, yout=36, parsed=True)
            return spec
        if "x^2" in compact.lower() or has(beat, "parabola", "x to the 2"):
            spec.update(kind="quad", label="x^2", xin=3, yout=9, parsed=True)
            return spec
        if re.search(r"[A-Za-z]\([A-Za-z]\)=m[A-Za-z][+-]b", compact, re.I):
            spec.update(label="mx + b", m=1.5, b=1.0, xin=2, yout=4.0, parsed=True)
            return spec
        mset = re.search(r"(-?)(\d*)x([+-]\d+)=(\d+)", compact)
        if mset and (has(beat, "solve") or has(beat, "set 2x") or "set" in compact.lower()):
            sign, coef, btxt, rhs = mset.groups()
            m = float(coef or "1")
            if sign == "-":
                m = -m
            b = float(btxt.replace("+", ""))
            mag = self._fn_num(abs(m))
            bpart = (" + " if b >= 0 else " - ") + self._fn_num(abs(b))
            if abs(m - 1) < 1e-9:
                lab = "x" + bpart
            elif abs(m + 1) < 1e-9:
                lab = "-x" + bpart
            else:
                lab = ("-" if m < 0 else "") + mag + "x" + bpart
            spec.update(kind="linear", m=m, b=b, label=lab, parsed=True, solve=float(rhs),
                        xin=(float(rhs) - b) / m if m else 3)
            spec["yout"] = float(rhs)
            return spec
        mlin = re.search(r"([A-Za-z])\(([A-Za-z])\)=(-?)(\d*\.?\d*)\2([+-]\d+)", compact)
        mconst = re.search(r"([A-Za-z])\(([A-Za-z])\)=(-?\d+)(?![0-9.x])", compact)
        if mlin:
            fn, var, sign, coef, btxt = mlin.groups()
            m = float(coef or "1")
            if sign == "-":
                m = -m
            b = float(btxt.replace("+", ""))
            mag = self._fn_num(abs(m))
            bpart = (" + " if b >= 0 else " - ") + self._fn_num(abs(b))
            if abs(m - 1) < 1e-9:
                lab = var + bpart
            elif abs(m + 1) < 1e-9:
                lab = "-" + var + bpart
            else:
                lab = ("-" if m < 0 else "") + mag + var + bpart
            spec.update(kind="linear", m=m, b=b, label=lab, fn_name=fn, var=var, parsed=True)
            spec["yout"] = m * spec["xin"] + b
        elif mconst and not has(beat, "solve"):
            fn, var, val = mconst.group(1), mconst.group(2), float(mconst.group(3))
            spec.update(kind="const", m=0.0, b=val, label=self._fn_num(val),
                        fn_name=fn, var=var, xin=0, yout=val, parsed=True)
        for fn, xv, yv in re.findall(r"([A-Za-z])\((-?\d+(?:\.\d+)?)\)=(-?\d+(?:\.\d+)?)", compact):
            xi, yi = float(xv), float(yv)
            spec["marks"].append((xi, yi))
            spec["fn_name"] = fn
            spec["xin"] = xi
            spec["yout"] = yi
        if has(beat, "solve") or has(beat, "set 2x"):
            mt = re.search(r"=(\d+)\.?$", compact)
            if mt:
                spec["solve"] = float(mt.group(1))
                spec["parsed"] = True
        if has(beat, "g(t)", "different letter"):
            spec.update(fn_name="g", var="t", kind="generic", label="g", xin=4, yout=None, parsed=True)
        elif has(beat, "exactly one output") or has(beat, "assigns each input"):
            spec.update(kind="generic", label="f", yout=None, parsed=True)
        elif has(beat, "f(x) means", "not f times", "f of"):
            spec.update(kind="generic", label="f", yout=None, parsed=True)
        if has(beat, "f(0) is the start", "extra cost per"):
            spec.update(kind="linear", m=8.0, b=12.0, label="8n + 12", fn_name="C", var="n",
                        xin=0, yout=12, parsed=True, marks=[(0, 12)])
        if has(beat, "club fee", "8 per person") and not spec["parsed"]:
            spec.update(kind="linear", m=8.0, b=12.0, label="8n + 12", fn_name="C", var="n",
                        xin=5, yout=52, parsed=True)
        if spec["parsed"] and spec["kind"] == "linear" and spec.get("yout") is not None:
            spec["yout"] = spec["m"] * spec["xin"] + spec["b"] if not spec["marks"] else spec["yout"]
            if spec["marks"]:
                spec["xin"], spec["yout"] = spec["marks"][0]
        return spec

    def _fn_axes(self, spec):
        kind = spec["kind"]

        def stepped(xr, yr):
            def step(span):
                if span <= 8:
                    return 1
                if span <= 16:
                    return 2
                if span <= 40:
                    return 5
                if span <= 80:
                    return 10
                return 20
            x0, x1 = xr
            y0, y1 = yr
            return Axes((x0, x1, step(x1 - x0)), (y0, y1, step(y1 - y0)), height=3.0, width=3.5)

        if kind == "quad":
            return stepped((-2.5, 3), (-1, 9))
        if kind == "exp":
            return stepped((-1, 3.5), (0, 10))
        if kind == "abs":
            return stepped((-3, 3), (0, 4))
        if kind == "const":
            return stepped((-1, 5), (-1, max(5, spec["b"] + 2)))
        m, b = spec["m"], spec["b"]
        ymax = max(6, min(40, abs(m) * 4 + abs(b) + 2))
        ymin = min(-1, b - 2)
        xmax = 5 if abs(m) >= 6 else 5
        if abs(b) >= 8:
            xmax = 4
            ymax = max(abs(b) + abs(m) * 3 + 2, 16)
        return stepped((-1, xmax), (ymin, ymax))

    def _fn_curve(self, axes, spec, stroke=5, color=GOLD):
        kind = spec["kind"]
        if kind == "quad":
            return axes.get_graph(lambda x: x * x).set_stroke(PINK if color == GOLD else color, stroke)
        if kind == "exp":
            return axes.get_graph(lambda x: 2 ** x).set_stroke(PINK if color == GOLD else color, stroke)
        if kind == "abs":
            return axes.get_graph(lambda x: abs(x)).set_stroke(PINK if color == GOLD else color, stroke)
        if kind == "const":
            b = spec["b"]
            return axes.get_graph(lambda x, b=b: b).set_stroke(color, stroke)
        m, b = spec["m"], spec["b"]
        return axes.get_graph(lambda x, m=m, b=b: m * x + b).set_stroke(color, stroke)

    def _fn_caption(self, spec, extra=""):
        if spec["kind"] == "quad":
            lab = VGroup(formula(spec["fn_name"] + "(" + spec["var"] + ") = ", 20, PINK, 14),
                         power_mob(spec["var"], "2", 22, 12, PINK, GOLD)).arrange(RIGHT, buff=0.05)
        elif spec["kind"] == "exp":
            lab = VGroup(formula("f(x) = ", 20, PINK, 10),
                         power_mob("2", "x", 22, 12, PINK, GOLD)).arrange(RIGHT, buff=0.05)
        elif spec["kind"] == "abs":
            lab = formula("|x|  V shape", 20, PINK, 18)
        elif spec["kind"] == "generic":
            lab = formula(spec["fn_name"] + "(" + spec["var"] + ")", 20, GOLD, 14)
        else:
            lab = formula(spec["fn_name"] + "(" + spec["var"] + ") = " + spec["label"], 20, GOLD, 22)
        if extra:
            lab = VGroup(lab, T(extra, 18, TEAL, 28, FONT_MATH)).arrange(DOWN, buff=0.08)
        return lab

    def _rule_card(self, spec, color=GOLD, w=2.05, h=1.05):
        r = RoundedRectangle(w, h, corner_radius=0.12)
        r.set_stroke(color, 3).set_fill(color, 0.14)
        if spec["kind"] == "quad":
            t = power_mob(spec["var"], "2", 30, 16, CREAM, GOLD)
        elif spec["kind"] == "exp":
            t = power_mob("2", spec["var"], 30, 16, CREAM, GOLD)
        elif spec["kind"] == "abs":
            t = formula("|x|", 30, CREAM, 8)
        elif spec["kind"] == "generic":
            t = formula(spec["fn_name"], 34, CREAM, 6)
        else:
            t = formula(spec["label"], 28, CREAM, max(0.9, w * 0.86))
        if t.get_width() > w * 0.84:
            t.set_width(w * 0.84)
        if t.get_height() > h * 0.72:
            t.set_height(h * 0.72)
        t.move_to(r)
        return VGroup(r, t)

    def anim_function(self, beat_i, beat):
        if has(beat, "v-shape", "|x|", "each piece is a line"):
            return self.demo_curve(beat)
        if has(beat, "closed circle", "open circle"):
            return self.demo_function_graph(beat)
        if has(beat, "vertical line", "hits a graph twice", "fail the test"):
            return self.demo_vlt(beat)
        if has(beat, "count of people") or has(beat, "-3.5"):
            return self.demo_function_graph(beat)
        if has(beat, "units of the output"):
            return self.demo_table(beat)
        if has(beat, "all three") or (has(beat, "machine") and has(beat, "table") and has(beat, "graph")):
            return self.demo_machine(beat)
        if has(beat, "v-shape", "|x|", "each piece is a line"):
            return self.demo_curve(beat)
        if has(beat, "2^x", "grows by multiplying"):
            return self.demo_curve(beat)
        if has(beat, "table", "first differences", "y-jumps", "plot the pairs") or (
            has(beat, "nonlinear") and has(beat, "jump", "bend", "curve")
        ):
            return self.demo_table(beat)
        if has(beat, "nonlinear", "parabola", "x^2", "bends", "not a line", "square"):
            return self.demo_curve(beat)
        if has(beat, "domain", "range"):
            return self.demo_curve(beat)
        if has(beat, "solve") or has(beat, "set 2x"):
            return self.demo_function_graph(beat)
        if has(beat, "linear", "mx + b", "equal x-steps", "straight", "constant rate",
               "horizontal", "slope 0"):
            return self.demo_function_graph(beat)
        if has(beat, "machine", "f(x) means", "not f times", "g(t)", "f of", "input"):
            return self.demo_machine(beat)
        if "=" in beat or "f(" in beat or "C(" in beat:
            return self.demo_function_graph(beat)
        return self.demo_machine(beat)

    def demo_function_graph(self, beat):
        if has(beat, "closed circle", "open circle"):
            axes = Axes((-1, 5), (-1, 5), height=3.1, width=3.6)
            axes.set_stroke(MUTED, 2)
            start, end = axes.c2p(0, 1), axes.c2p(4, 3.4)
            line = Line(start, end).set_stroke(GOLD, 5)
            closed = Dot(start, fill_color=GOLD).scale(1.25)
            opened = Dot(end, fill_color="#111111").scale(1.2).set_stroke(PINK, 4)
            cap = T("closed on  open off", 20, TEAL, 28)
            pack = VGroup(VGroup(axes, line, closed, opened), cap).arrange(DOWN, buff=0.12).move_to(0.25 * DOWN)
            self.play(ShowCreation(axes), ShowCreation(line), run_time=0.45)
            self.play(GrowFromCenter(closed), GrowFromCenter(opened), FadeIn(cap), run_time=0.4)
            return pack
        if has(beat, "count of people") or has(beat, "-3.5"):
            line = NumberLine((-4, 6), width=7.2).set_stroke(MUTED, 4)
            dots = VGroup(*[Dot(line.n2p(n), fill_color=TEAL).scale(1.1) for n in range(0, 5)])
            bad = Dot(line.n2p(-3.5), fill_color=PINK).scale(1.25)
            no = T("not a count", 18, PINK, 16).next_to(bad, UP, buff=0.12)
            cap = T("n = 0, 1, 2, 3, ...", 20, GOLD, 28)
            g = VGroup(line, dots, bad, no, cap)
            cap.next_to(line, DOWN, buff=0.28)
            g.move_to(0.2 * DOWN)
            self.play(ShowCreation(line), run_time=0.35)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), run_time=0.55)
            self.play(GrowFromCenter(bad), FadeIn(no), FadeIn(cap), run_time=0.35)
            return g
        spec = self._parse_fn(beat)
        axes = self._fn_axes(spec)
        axes.set_stroke(MUTED, 2)
        curve = self._fn_curve(axes, spec)
        extra = ""
        if has(beat, "equal x-steps", "equal y-steps", "constant rate"):
            extra = "equal steps"
        if spec["kind"] == "const" or has(beat, "horizontal", "slope 0"):
            extra = "horizontal  slope 0"
        cap = self._fn_caption(spec, extra)
        pack = VGroup(VGroup(axes, curve), cap).arrange(DOWN, buff=0.12).move_to(0.25 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(curve), FadeIn(cap), run_time=0.5)
        extras = []
        if spec["kind"] == "linear" and has(beat, "equal x-steps", "equal y-steps", "constant rate"):
            pts = VGroup()
            for i in range(4):
                pts.add(Dot(axes.c2p(i, spec["m"] * i + spec["b"]), fill_color=TEAL).scale(1.05))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in pts], lag_ratio=0.12), run_time=0.5)
            extras.append(pts)
        if spec.get("solve") is not None and spec["kind"] == "linear" and spec["m"]:
            yv = spec["solve"]
            xv = (yv - spec["b"]) / spec["m"]
            hline = axes.get_graph(lambda x, yv=yv: yv).set_stroke(TEAL, 3)
            dot = Dot(axes.c2p(xv, yv), fill_color=GOLD).scale(1.25)
            sl = formula("x = " + self._fn_num(xv), 20, GOLD, 12).next_to(dot, UR, buff=0.08)
            self.play(ShowCreation(hline), run_time=0.3)
            self.play(GrowFromCenter(dot), FadeIn(sl), run_time=0.3)
            extras.extend([hline, dot, sl])
        elif spec["marks"]:
            dots = VGroup()
            for xi, yi in spec["marks"][:3]:
                dots.add(Dot(axes.c2p(xi, yi), fill_color=TEAL).scale(1.15))
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.12), run_time=0.4)
            extras.append(dots)
        elif spec["kind"] in ("linear", "const") and spec.get("yout") is not None:
            try:
                dot = Dot(axes.c2p(spec["xin"], spec["yout"]), fill_color=TEAL)
                self.play(GrowFromCenter(dot), run_time=0.25)
                extras.append(dot)
            except Exception:
                pass
        return VGroup(pack, *extras)

    def demo_machine(self, beat=""):
        spec = self._parse_fn(beat)
        combo = has(beat, "all three") or (has(beat, "machine") and has(beat, "table") and has(beat, "graph"))
        if has(beat, "f of") and not spec["parsed"]:
            spec.update(kind="linear", m=2.0, b=-1.0, label="2x - 1", xin=3, yout=5,
                        fn_name="f", var="x", parsed=True)
        if combo and not spec["parsed"]:
            spec.update(kind="linear", m=2.0, b=-1.0, label="2x - 1", xin=2, yout=3,
                        fn_name="f", var="x", parsed=True)
        var = spec["var"]
        xin = spec["xin"]
        inn = self._card(var + " = " + self._fn_num(xin), BLUE, 1.65, 0.75)
        box = self._rule_card(spec)
        if spec.get("yout") is None:
            out_txt = spec["fn_name"] + "(" + self._fn_num(xin) + ")"
        else:
            out_txt = self._fn_num(spec["yout"])
        out = self._card(out_txt, TEAL, 1.45, 0.75)
        row = VGroup(inn, box, out).arrange(RIGHT, buff=0.62)
        a1 = Arrow(inn.get_right(), box.get_left(), buff=0.06, fill_color=GOLD)
        a2 = Arrow(box.get_right(), out.get_left(), buff=0.06, fill_color=TEAL)
        if spec["kind"] in ("quad", "exp", "abs"):
            row.move_to(0.55 * UP)
            axes = self._fn_axes(spec)
            axes.set_stroke(MUTED, 2)
            curve = self._fn_curve(axes, spec, stroke=4)
            graph = VGroup(axes, curve).scale(0.72).move_to(1.2 * DOWN)
            self.play(GrowFromCenter(box), run_time=0.28)
            self.sfx("whoosh", -12)
            self.play(FadeIn(inn, RIGHT), ShowCreation(a1), run_time=0.28)
            self.pop_flash(box.get_center(), GOLD, 0.4)
            self.play(ShowCreation(a2), GrowFromCenter(out), run_time=0.32)
            self.play(ShowCreation(axes), ShowCreation(curve), run_time=0.45)
            return VGroup(row, a1, a2, graph)
        if combo:
            row.move_to(1.15 * UP)
            pairs = [(0, spec["m"] * 0 + spec["b"]), (1, spec["m"] * 1 + spec["b"]),
                     (2, spec["m"] * 2 + spec["b"])]
            headers = VGroup(T(var, 18, GOLD, 6), T("out", 18, TEAL, 8)).arrange(RIGHT, buff=0.9)
            trows = VGroup()
            for x, y in pairs:
                trows.add(VGroup(T(self._fn_num(x), 18, CREAM, 6),
                                 T(self._fn_num(y), 18, CREAM, 6)).arrange(RIGHT, buff=1.0))
            table = VGroup(headers, *trows).arrange(DOWN, buff=0.12).move_to(1.15 * DOWN + 3.1 * LEFT)
            axes = Axes((-1, 4), (min(-2, spec["b"] - 1), max(6, spec["m"] * 3 + spec["b"] + 1)),
                        height=2.15, width=2.5)
            axes.set_stroke(MUTED, 2)
            curve = self._fn_curve(axes, spec, stroke=4)
            dot = Dot(axes.c2p(xin, spec["m"] * xin + spec["b"]), fill_color=TEAL)
            graph = VGroup(axes, curve, dot).move_to(1.15 * DOWN + 2.4 * RIGHT)
            self.play(GrowFromCenter(box), run_time=0.25)
            self.sfx("whoosh", -12)
            self.play(FadeIn(inn, RIGHT), ShowCreation(a1), run_time=0.25)
            self.pop_flash(box.get_center(), GOLD, 0.35)
            self.play(ShowCreation(a2), GrowFromCenter(out), run_time=0.28)
            self.play(LaggedStart(*[FadeIn(r, UP) for r in table], lag_ratio=0.12), run_time=0.45)
            self.play(ShowCreation(axes), ShowCreation(curve), GrowFromCenter(dot), run_time=0.4)
            return VGroup(row, a1, a2, table, graph)
        row.move_to(0.55 * UP)
        axes = self._fn_axes(spec)
        axes.set_stroke(MUTED, 2)
        curve = self._fn_curve(axes, spec, stroke=4)
        graph = VGroup(axes, curve)
        extras = []
        if spec.get("yout") is not None and spec["kind"] in ("linear", "const"):
            try:
                extras.append(Dot(axes.c2p(xin, spec["yout"]), fill_color=TEAL))
            except Exception:
                pass
        graph = VGroup(axes, curve, *extras).scale(0.78).move_to(1.2 * DOWN)
        self.play(GrowFromCenter(box), run_time=0.28)
        self.sfx("whoosh", -12)
        self.play(FadeIn(inn, RIGHT), ShowCreation(a1), run_time=0.28)
        self.pop_flash(box.get_center(), GOLD, 0.4)
        self.play(ShowCreation(a2), GrowFromCenter(out), run_time=0.32)
        self.play(ShowCreation(axes), ShowCreation(curve), run_time=0.4)
        if extras:
            self.play(*[GrowFromCenter(d) for d in extras], run_time=0.25)
        return VGroup(row, a1, a2, graph)

    def demo_table(self, beat=""):
        spec = self._parse_fn(beat)
        var = spec["var"] if spec["parsed"] else "x"
        caption = ""
        show_jumps = False
        plot_after = False
        plot_first = False
        if has(beat, "two different y", "x shows two"):
            pairs = [(1, 2), (1, 5), (3, 4)]
            caption = "x = 1 twice  not a function"
            var = "x"
        elif (
            has(beat, "keep changing")
            or has(beat, "not constant")
            or (has(beat, "nonlinear") and has(beat, "jump", "bend", "curve", "table", "y-jumps"))
            or (has(beat, "not linear") and has(beat, "table", "first differences", "jump"))
            or (
                has(beat, "parabola", "x^2", "square")
                and has(beat, "first differences", "table", "jump")
            )
        ):
            pairs = [(1, 1), (2, 4), (3, 9)]
            caption = "not linear"
            show_jumps = True
        elif has(beat, "first differences") or (has(beat, "table") and has(beat, "constant")):
            pairs = [(0, 4), (1, 7), (2, 10)]
            caption = "constant"
            show_jumps = True
        elif has(beat, "sit on the curve", "graph to a table"):
            pairs = [(0, -1), (1, 1), (2, 3)]
            caption = "read off the line"
            plot_first = True
            spec.update(kind="linear", m=2.0, b=-1.0, label="2x - 1", parsed=True)
        elif has(beat, "plot the pairs", "table to a graph"):
            pairs = [(0, 1), (1, 3), (2, 5)]
            caption = "plot the pairs"
            plot_after = True
            spec.update(kind="linear", m=2.0, b=1.0, label="2x + 1", parsed=True)
        elif has(beat, "units of the output"):
            pairs = [(0, 12), (1, 20), (2, 28)]
            caption = "output in dollars"
            var = "n"
        elif spec["parsed"] and spec["kind"] == "linear":
            pairs = [(i, spec["m"] * i + spec["b"]) for i in range(3)]
            caption = spec["label"]
        elif spec["parsed"] and spec["kind"] == "quad":
            pairs = [(1, 1), (2, 4), (3, 9)]
            caption = "squares"
            show_jumps = True
        else:
            pairs = [(0, 1), (1, 3), (2, 5)]
        headers = VGroup(T(var, 22, GOLD, 6), T("out", 22, TEAL, 8)).arrange(RIGHT, buff=1.35)
        rows = VGroup()
        for x, y in pairs:
            rows.add(VGroup(T(self._fn_num(x), 22, CREAM, 6),
                            T(self._fn_num(y), 22, CREAM, 6)).arrange(RIGHT, buff=1.55))
        table = VGroup(headers, *rows).arrange(DOWN, buff=0.16)
        cap = T(caption, 20, GOLD if "not" not in caption else PINK, 28) if caption else None
        if plot_first or plot_after:
            axes = Axes((-1, 4), (-2, 7), height=2.6, width=3.0)
            axes.set_stroke(MUTED, 2)
            curve = self._fn_curve(axes, spec, stroke=4)
            dots = VGroup(*[Dot(axes.c2p(x, y), fill_color=TEAL).scale(1.1) for x, y in pairs])
            graph = VGroup(axes, curve, dots)
            if plot_first:
                graph.move_to(2.6 * LEFT + 0.15 * DOWN)
                table.move_to(2.7 * RIGHT + 0.15 * DOWN)
                self.play(ShowCreation(axes), ShowCreation(curve), run_time=0.45)
                self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.12), run_time=0.4)
                self.play(LaggedStart(*[FadeIn(r, UP) for r in table], lag_ratio=0.12), run_time=0.5)
            else:
                table.move_to(2.7 * LEFT + 0.15 * DOWN)
                graph.move_to(2.6 * RIGHT + 0.15 * DOWN)
                self.play(LaggedStart(*[FadeIn(r, UP) for r in table], lag_ratio=0.12), run_time=0.5)
                self.play(ShowCreation(axes), run_time=0.25)
                self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.12), run_time=0.4)
                self.play(ShowCreation(curve), run_time=0.35)
            extras = [graph]
            if cap:
                cap.next_to(VGroup(table, graph), DOWN, buff=0.18)
                self.play(FadeIn(cap), run_time=0.2)
                extras.append(cap)
            return VGroup(table, *extras)
        bits = [table]
        jlab = None
        if show_jumps and len(pairs) >= 3:
            diffs = [pairs[i][1] - pairs[i - 1][1] for i in range(1, len(pairs))]
            jtxt = ", ".join(("+" if d >= 0 else "") + self._fn_num(d) for d in diffs)
            jlab = T("jumps  " + jtxt, 20, TEAL, 18)
            out_col = VGroup(*[row[1] for row in rows])
            jlab.next_to(out_col, DOWN, buff=0.14)
            jlab.align_to(out_col, RIGHT)
            bits.append(jlab)
        if cap:
            bits.append(cap)
        pack = VGroup(*bits)
        if jlab is not None:
            pack = VGroup(table, jlab, *([cap] if cap else [])).move_to(0.2 * DOWN)
            # Keep jump labels under the out column, not under x.
            jlab.next_to(out_col, DOWN, buff=0.14)
            jlab.align_to(out_col, RIGHT)
            if cap:
                cap.next_to(jlab, DOWN, buff=0.12)
        else:
            pack = VGroup(*bits).arrange(DOWN, buff=0.16).move_to(0.2 * DOWN)
        self.play(LaggedStart(*[FadeIn(r, UP) for r in table], lag_ratio=0.15), run_time=0.7)
        extra = [m for m in (jlab, cap) if m is not None]
        if extra:
            self.play(*[FadeIn(b) for b in extra], run_time=0.25)
        return pack

    def demo_curve(self, beat=""):
        spec = self._parse_fn(beat)
        if has(beat, "domain", "range") and spec["kind"] == "linear" and not spec["parsed"]:
            spec.update(kind="quad", label="x^2", parsed=True)
        if spec["kind"] == "linear" and not spec["parsed"]:
            spec.update(kind="quad", label="x^2")
        axes = self._fn_axes(spec)
        axes.set_stroke(MUTED, 2)
        curve = self._fn_curve(axes, spec)
        if spec["kind"] == "abs":
            extra = "nonlinear  V shape"
        elif spec["kind"] == "exp":
            extra = "grows by multiplying"
        elif has(beat, "domain", "range"):
            extra = "domain on x   range on y"
        else:
            extra = "not a line"
        cap = self._fn_caption(spec, extra)
        pack = VGroup(VGroup(axes, curve), cap).arrange(DOWN, buff=0.12).move_to(0.25 * DOWN)
        self.play(ShowCreation(axes), run_time=0.3)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(curve), FadeIn(cap), run_time=0.55)
        extras = []
        if has(beat, "domain", "range"):
            dx = Line(axes.c2p(-2, 0), axes.c2p(2, 0)).set_stroke(TEAL, 8, 0.55)
            dy = Line(axes.c2p(0, 0), axes.c2p(0, 4)).set_stroke(GOLD, 8, 0.55)
            self.play(ShowCreation(dx), ShowCreation(dy), run_time=0.4)
            extras.extend([dx, dy])
        return VGroup(pack, *extras)

    def demo_vlt(self, beat=""):
        both = has(beat, "fail the test") or has(beat, "machines")
        if both:
            a1 = Axes((-1, 3), (-1, 3), height=2.5, width=2.6)
            a1.set_stroke(MUTED, 2)
            line = a1.get_graph(lambda x: 0.7 * x + 0.6).set_stroke(GOLD, 4)
            p1 = Line(a1.c2p(1.2, -1), a1.c2p(1.2, 3)).set_stroke(TEAL, 3)
            hit = Dot(a1.c2p(1.2, 0.7 * 1.2 + 0.6), fill_color=TEAL)
            ok = T("one hit", 18, TEAL, 12)
            left = VGroup(VGroup(a1, line, p1, hit), ok).arrange(DOWN, buff=0.1)
            a2 = Axes((-2.2, 2.2), (-2.2, 2.2), height=2.5, width=2.6)
            a2.set_stroke(MUTED, 2)
            origin = a2.c2p(0, 0)
            r = ((a2.c2p(1.4, 0)[0] - origin[0]) ** 2 + (a2.c2p(1.4, 0)[1] - origin[1]) ** 2) ** 0.5
            circ = Circle(radius=r).move_to(origin).set_stroke(PINK, 4).set_fill(PINK, 0)
            px = 0.6
            py = (1.4 ** 2 - px ** 2) ** 0.5
            p2 = Line(a2.c2p(px, -2.1), a2.c2p(px, 2.1)).set_stroke(TEAL, 3)
            d1 = Dot(a2.c2p(px, py), fill_color=PINK)
            d2 = Dot(a2.c2p(px, -py), fill_color=PINK)
            no = T("two hits", 18, PINK, 12)
            right = VGroup(VGroup(a2, circ, p2, d1, d2), no).arrange(DOWN, buff=0.1)
            pack = VGroup(left, right).arrange(RIGHT, buff=0.55).move_to(0.2 * DOWN)
            self.play(ShowCreation(a1), ShowCreation(line), run_time=0.35)
            self.play(ShowCreation(p1), GrowFromCenter(hit), FadeIn(ok), run_time=0.3)
            self.play(ShowCreation(a2), ShowCreation(circ), run_time=0.35)
            self.play(ShowCreation(p2), GrowFromCenter(d1), GrowFromCenter(d2), FadeIn(no), run_time=0.35)
            return pack
        axes = Axes((-2.4, 2.4), (-2.4, 2.4), height=3.2, width=3.5)
        axes.set_stroke(MUTED, 2)
        origin = axes.c2p(0, 0)
        rad = 1.55
        r = ((axes.c2p(rad, 0)[0] - origin[0]) ** 2 + (axes.c2p(rad, 0)[1] - origin[1]) ** 2) ** 0.5
        circ = Circle(radius=r).move_to(origin).set_stroke(GOLD, 5).set_fill(GOLD, 0)
        probe = Line(axes.c2p(-2.1, -2.2), axes.c2p(-2.1, 2.2)).set_stroke(TEAL, 4)
        cap = T("two hits  not a function", 20, PINK, 28)
        pack = VGroup(VGroup(axes, circ), cap).arrange(DOWN, buff=0.12).move_to(0.2 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(circ), run_time=0.5)
        self.play(ShowCreation(probe), run_time=0.25)
        px = 0.7
        py = (rad ** 2 - px ** 2) ** 0.5
        moved = Line(axes.c2p(px, -2.2), axes.c2p(px, 2.2)).set_stroke(TEAL, 4)
        self.sfx("whoosh", -12)
        self.play(Transform(probe, moved), run_time=0.7)
        d1 = Dot(axes.c2p(px, py), fill_color=PINK).scale(1.2)
        d2 = Dot(axes.c2p(px, -py), fill_color=PINK).scale(1.2)
        self.play(GrowFromCenter(d1), GrowFromCenter(d2), FadeIn(cap), run_time=0.35)
        self.pop_flash(d1.get_center(), PINK, 0.4)
        return VGroup(pack, probe, d1, d2)

    # ----- systems: different intersections / methods -----

    def _wants_eliminate(self, beat):
        t = caretify(beat).lower()
        if has(beat, "substitut") and has(beat, "eliminat") and not has(beat, "add", "cancel", "oppose"):
            return False
        if has(beat, "cancel", "oppose"):
            return True
        if has(beat, "add or subtract", "when you add", "then subtract", "then add"):
            return True
        if re.search(r"\badd:", t):
            return True
        stripped = t.rstrip(" .")
        if stripped.endswith(" add") or stripped.endswith(", add"):
            return True
        if has(beat, "adding"):
            return True
        if has(beat, "multiply") and has(beat, "subtract", "both equations"):
            return True
        if re.search(r"[×x]\s*\d+", t) and has(beat, "subtract", "add"):
            return True
        if re.search(r"\bsubtract:", t) or re.search(r"\badd:", t):
            return True
        if has(beat, "eliminat") and not has(beat, "substitut"):
            return True
        return False

    def anim_system(self, beat_i, beat):
        t = caretify(beat).lower()
        stacked = has(beat, "stacked")
        rails = has(beat, "rails", "never meet")
        no_sol = has(beat, "parallel", "no solution", "never meet", "rails") or bool(
            re.search(r"\bnone\b", t)
        )
        inf = has(beat, "same line", "infinitely")
        if (stacked and rails) or (no_sol and inf):
            return self.demo_stacked_vs_rails()
        if no_sol:
            return self.demo_sys_parallel(beat)
        if inf:
            return self.demo_sys_same_line(beat)
        wants_elim = self._wants_eliminate(beat)
        wants_sub = (
            has(beat, "plug", " into ")
            or has(beat, "set the y")
            or (has(beat, "substitut") and "=" in caretify(beat))
        )
        if getattr(self, "unit_num", 0) == 5:
            wants_elim = False
        eqs = parse_lin_system(beat)
        pair = pair_from_text(beat)
        if getattr(self, "unit_num", 0) == 6:
            if wants_sub and not wants_elim:
                return self.demo_substitute(beat)
            if len(eqs) >= 2 or wants_elim:
                return self.demo_eliminate(beat)
            if has(beat, "isolated") or has(beat, "coefficients match") or has(beat, "either way"):
                return self.demo_choose_method()
            if pair and len(eqs) >= 2:
                return self.demo_cross(pair[0], pair[1], eqs=eqs)
            if len(eqs) == 1:
                kind, xy = ("one", pair)
                return self._elim_graph(eqs[0], None, kind, xy)
            if pair:
                lab = formula(f"({_fmt_n(pair[0])}, {_fmt_n(pair[1])})", 40, GOLD, 12)
                self.play(GrowFromCenter(lab), run_time=0.4)
                return lab
            return self.demo_choose_method()
        both = wants_sub and wants_elim
        if both and not has(beat, " into ", "plug"):
            if len(eqs) >= 2:
                kind, xy = solve_lin_system(eqs[0], eqs[1])
                if kind == "one" and xy:
                    return self.demo_cross(xy[0], xy[1], eqs=eqs)
            pair = pair or self._unique_xy(beat_i, beat)
            return self.demo_cross(pair[0], pair[1], eqs=eqs)
        if wants_sub:
            return self.demo_substitute(beat)
        if wants_elim:
            return self.demo_eliminate(beat)
        if len(eqs) >= 2:
            kind, xy = solve_lin_system(eqs[0], eqs[1])
            if kind == "one" and xy:
                return self.demo_cross(xy[0], xy[1], eqs=eqs)
            if kind == "none":
                return self.demo_sys_parallel(beat)
            return self.demo_sys_same_line(beat)
        if pair:
            return self.demo_cross(pair[0], pair[1], eqs=eqs)
        return self.demo_cross(*self._unique_xy(beat_i, beat))

    def _unique_xy(self, beat_i, beat=""):
        pts = (
            (2, 3), (1, 4), (4, 2), (5, 1), (0, 2),
            (3, 1), (1, 2), (4, 5), (2, 1), (5, 3),
            (6, 2), (2, 5), (1, 1), (4, 4), (3, 6),
        )
        s = caretify(beat) + "#" + str(beat_i)
        h = sum((i + 3) * ord(c) for i, c in enumerate(s))
        return pts[h % len(pts)]

    def _slope_of(self, fn):
        if fn is None:
            return None
        try:
            return float(fn(1.0) - fn(0.0))
        except Exception:
            return None

    def _cross_at(self, x, y, m1, m2, where=0.35 * DOWN, width=3.6, height=3.2):
        x, y = float(x), float(y)
        m1 = 0.7 if m1 is None else float(m1)
        m2 = -0.9 if m2 is None else float(m2)
        if abs(m1 - m2) < 0.04:
            m2 = m1 - 1.3 if m1 > 0 else m1 + 1.3
        xmax = max(5.0, x + 2.2)
        ymax = max(6.0, y + 2.2)
        xmin = min(-1.0, x - 1.6)
        ymin = min(-1.0, y - 1.6)
        axes = Axes((xmin, xmax, 1), (ymin, ymax, 1), height=height, width=width)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(lambda t, m1=m1, x=x, y=y: y + m1 * (t - x)).set_stroke(BLUE, 5)
        l2 = axes.get_graph(lambda t, m2=m2, x=x, y=y: y + m2 * (t - x)).set_stroke(PINK, 5)
        dot = Dot(axes.c2p(x, y), fill_color=GOLD).scale(1.3)
        lab = formula(f"({_fmt_n(x)}, {_fmt_n(y)})", 20, GOLD, 12)
        lab.next_to(dot, UR, buff=0.08)
        pack = VGroup(axes, l1, l2, dot, lab).move_to(where)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(ShowCreation(l1), run_time=0.4)
        self.play(ShowCreation(l2), run_time=0.4)
        self.sfx("sparkle", -9)
        self.play(GrowFromCenter(dot), FadeIn(lab), run_time=0.3)
        return pack

    def demo_cross(self, x, y, eqs=None):
        x, y = float(x), float(y)
        m1, m2 = 0.7, -0.9
        if eqs:
            s1 = self._slope_of(self._sys_fn(eqs[0]))
            if s1 is not None:
                m1 = s1
        if eqs and len(eqs) >= 2:
            kind, xy = solve_lin_system(eqs[0], eqs[1])
            if kind == "inf":
                return self.demo_sys_same_line("")
            if kind == "none":
                return self.demo_sys_parallel("")
            s2 = self._slope_of(self._sys_fn(eqs[1]))
            if s2 is not None:
                m2 = s2
        return self._cross_at(x, y, m1, m2)

    def demo_choose_method(self):
        def card(txt, color):
            t = T(txt, 28, CREAM, 34)
            r = RoundedRectangle(t.get_width() + 0.7, t.get_height() + 0.45, corner_radius=0.14)
            r.set_stroke(color, 4).set_fill(color, 0.28)
            t.move_to(r)
            return VGroup(r, t)

        a = card("y already isolated: substitute", TEAL)
        b = card("matching coefficients: eliminate", GOLD)
        pack = VGroup(a, b).arrange(DOWN, buff=0.4).move_to(0.1 * DOWN)
        self.play(FadeIn(a, LEFT), run_time=0.4)
        self.play(FadeIn(b, RIGHT), run_time=0.4)
        return pack

    def demo_same_line(self, beat=""):
        return self.demo_sys_same_line(beat)

    def _sys_fn(self, e):
        a, b, c = float(e["a"]), float(e["b"]), float(e["c"])
        if abs(b) < 1e-8:
            return None
        return lambda t, a=a, b=b, c=c: (c - a * t) / b

    def demo_sys_parallel(self, beat=""):
        eqs = parse_lin_system(beat)
        if len(eqs) >= 2:
            e1, e2 = eqs[0], eqs[1]
            f1, f2 = self._sys_fn(e1), self._sys_fn(e2)
        else:
            f1 = lambda t: 0.55 * t + 0.45
            f2 = lambda t: 0.55 * t + 2.35
        if not f1:
            f1 = lambda t: 0.55 * t + 0.45
        if not f2:
            f2 = lambda t: 0.55 * t + 2.35
        axes = Axes((-1, 6), (-1, 6), height=3.0, width=3.4)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(f1).set_stroke(BLUE, 5)
        l2 = axes.get_graph(f2).set_stroke(PINK, 5)
        lab = formula("no solution  parallel", 22, RED, 28)
        g = VGroup(axes, l1, l2)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.12).move_to(0.25 * DOWN)
        p1, p2 = l1.get_center(), l2.get_center()
        gap = p2 - p1
        if np.linalg.norm(gap) < 0.35:
            p2 = p2 + 0.45 * UP
        mid = (p1 + p2) / 2
        xa = Line(mid + 0.28 * UL, mid + 0.28 * DR).set_stroke(RED, 6)
        xb = Line(mid + 0.28 * UR, mid + 0.28 * DL).set_stroke(RED, 6)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(ShowCreation(l1), ShowCreation(l2), run_time=0.55)
        self.sfx("wrong", -10)
        self.play(ShowCreation(xa), ShowCreation(xb), FadeIn(lab), run_time=0.4)
        return VGroup(pack, xa, xb)

    def demo_sys_same_line(self, beat=""):
        eqs = parse_lin_system(beat)
        fn = None
        if eqs:
            fn = self._sys_fn(eqs[0])
        if fn is None:
            fn = lambda t: 0.5 * t + 1.1
        axes = Axes((-1, 6), (-1, 6), height=3.0, width=3.4)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(fn).set_stroke(BLUE, 9, 0.45)
        l2 = axes.get_graph(fn).set_stroke(GOLD, 4)
        dots = VGroup()
        for t in (0.2, 1.6, 3.0, 4.4):
            dots.add(Dot(axes.c2p(t, fn(t)), fill_color=GOLD).scale(0.95))
        lab = formula("same line  infinitely many", 22, GOLD, 32)
        g = VGroup(axes, l1, l2, dots)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.12).move_to(0.25 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(l1), ShowCreation(l2), run_time=0.55)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.14),
            FadeIn(lab),
            run_time=0.55,
        )
        return pack

    def demo_stacked_vs_rails(self):
        def mini(same):
            axes = Axes((-1, 4), (-1, 4), height=2.35, width=2.55)
            axes.set_stroke(MUTED, 2)
            if same:
                l1 = axes.get_graph(lambda x: 0.45 * x + 1.15).set_stroke(BLUE, 8, 0.5)
                l2 = axes.get_graph(lambda x: 0.45 * x + 1.15).set_stroke(GOLD, 3)
                cap = formula("same line", 18, GOLD, 14)
                extra = VGroup(
                    *[Dot(axes.c2p(t, 0.45 * t + 1.15), fill_color=GOLD).scale(0.7) for t in (0.3, 1.6, 2.9)]
                )
                pic = VGroup(axes, l1, l2, extra)
            else:
                l1 = axes.get_graph(lambda x: 0.45 * x + 0.35).set_stroke(BLUE, 4)
                l2 = axes.get_graph(lambda x: 0.45 * x + 2.15).set_stroke(PINK, 4)
                cap = formula("never meet", 18, RED, 14)
                mid = (l1.get_center() + l2.get_center()) / 2
                xa = Line(mid + 0.22 * UL, mid + 0.22 * DR).set_stroke(RED, 4)
                xb = Line(mid + 0.22 * UR, mid + 0.22 * DL).set_stroke(RED, 4)
                pic = VGroup(axes, l1, l2, xa, xb)
            return VGroup(pic, cap).arrange(DOWN, buff=0.1)

        left = mini(True)
        right = mini(False)
        pack = VGroup(left, right).arrange(RIGHT, buff=0.65).move_to(0.2 * DOWN)
        self.play(FadeIn(left), FadeIn(right), run_time=0.75)
        return pack

    def _y_fn_from_eq(self, eq):
        if not eq:
            return None
        t = caretify(eq).replace(" ", "").rstrip(".")
        m = re.fullmatch(r"y=([+-]?)(\d+(?:\.\d+)?)?x([+-]\d+(?:\.\d+)?)?", t)
        if m:
            sign, coef, b = m.group(1), m.group(2), m.group(3)
            mv = 1.0 if not coef else float(coef)
            if sign == "-":
                mv = -mv
            bv = float(b) if b else 0.0
            return lambda x, mv=mv, bv=bv: mv * x + bv
        m = re.fullmatch(r"y=([+-]?\d+(?:\.\d+)?)-x/(\d+(?:\.\d+)?)", t)
        if m:
            b, k = float(m.group(1)), float(m.group(2))
            return lambda x, b=b, k=k: b - x / k
        m = re.fullmatch(r"y=x/(\d+(?:\.\d+)?)", t)
        if m:
            k = float(m.group(1))
            return lambda x, k=k: x / k
        if t == "y=x":
            return lambda x: x
        m = re.fullmatch(
            r"(\d+(?:\.\d+)?)\((\d+(?:\.\d+)?)?x([+-])(\d+(?:\.\d+)?)?y\)=([+-]?\d+(?:\.\d+)?)",
            t,
        )
        if m:
            n = float(m.group(1))
            a = float(m.group(2) or 1)
            b = float(m.group(4) or 1) * (1.0 if m.group(3) == "+" else -1.0)
            c = float(m.group(5))
            A, B = n * a, n * b
            if abs(B) > 1e-9:
                return lambda x, A=A, B=B, c=c: (c - A * x) / B
        m = re.fullmatch(
            r"(\d+(?:\.\d+)?)\(([+-]?)(\d+(?:\.\d+)?)?x([+-]\d+(?:\.\d+)?)\)([+-]\d+(?:\.\d+)?)y=([+-]?\d+(?:\.\d+)?)",
            t,
        )
        if m:
            n = float(m.group(1))
            xs = -1.0 if m.group(2) == "-" else 1.0
            xc = float(m.group(3) or 1) * xs
            inside_b = float(m.group(4))
            yc = float(m.group(5))
            rhs = float(m.group(6))
            A = n * xc
            B = yc
            C = rhs - n * inside_b
            if abs(B) > 1e-9:
                return lambda x, A=A, B=B, C=C: (C - A * x) / B
        m = re.fullmatch(r"x=([+-]?\d+(?:\.\d+)?)([+-])(\d+(?:\.\d+)?)?y", t)
        if m:
            p = float(m.group(1))
            q = float(m.group(3) or "1")
            if m.group(2) == "-":
                q = -q
            if abs(q) < 1e-9:
                return None
            return lambda x, p=p, q=q: (x - p) / q
        eqs = parse_lin_system(eq)
        if len(eqs) == 1:
            return self._sys_fn(eqs[0])
        return None

    def _clip_eq(self, chunk):
        s = caretify(chunk).strip().rstrip(".")
        if not s:
            return ""
        s = re.split(r"\s+Which\b", s, maxsplit=1, flags=re.I)[0]
        s = re.split(r"\.\s+(?=[A-Z])", s, maxsplit=1)[0]
        cut = re.split(r"\s+(?:set|gives|then|so|from|into)\b", s, maxsplit=1, flags=re.I)
        s = cut[0].strip().rstrip(".,")
        if "," in s and not re.search(r"\([^)]*$", s):
            head, tail = s.split(",", 1)
            if "=" in head and not re.match(r"^\s*[xy]\s*=", tail):
                s = head.strip().rstrip(".,")
        return s

    def _make_plug(self, isolated, other):
        iso = caretify(isolated).strip()
        oth = caretify(other).strip()
        my = re.match(r"y\s*=\s*(.+)$", iso)
        oy = re.match(r"y\s*=\s*(.+)$", oth)
        if my and oy:
            return f"{my.group(1).strip()} = {oy.group(1).strip()}"
        if my:
            expr = my.group(1).strip()
            return re.sub(r"(?<![A-Za-z])y(?![A-Za-z])", "(" + expr + ")", oth)
        mx = re.match(r"x\s*=\s*(.+)$", iso)
        if mx:
            expr = mx.group(1).strip()
            return re.sub(r"(?<![A-Za-z])x(?![A-Za-z])", "(" + expr + ")", oth)
        return ""

    def _sub_from_beat(self, beat):
        t = caretify(beat)
        pair = pair_from_text(t)
        isolated = other = plug = ""
        m = re.search(r"(?i)((?:[xy])\s*=\s*.+?)\s+into\s+(.+)", t)
        if not m:
            m = re.search(r"(?i)((?:[xy])\s*=\s*.+?)\s+and\s+(.+)", t)
        if m:
            isolated = self._clip_eq(m.group(1))
            rest = m.group(2).strip()
            bits = [b.strip().rstrip(".") for b in re.split(r"\s*->\s*", rest) if b.strip()]
            if bits:
                other = self._clip_eq(bits[0])
            for chunk in bits[1:]:
                if pair_from_text(chunk):
                    if pair is None:
                        pair = pair_from_text(chunk)
                    continue
                if re.search(r"[xy]\s*=\s*-?\d", chunk) and re.search(r"[xy]\s*=", chunk[1:]):
                    continue
                if "=" in chunk and not plug:
                    plug = self._clip_eq(chunk)
        if isolated and other:
            made = self._make_plug(isolated, other)
            if made and made != caretify(other).strip():
                plug = made
            elif not plug:
                plug = made
        return isolated, other, plug, pair

    def demo_substitute(self, beat=""):
        isolated, other, plug, pair = self._sub_from_beat(beat)
        if not isolated or not other:
            isolated, other, plug, pair = "y = 2x", "x + y = 9", "x + (2x) = 9", (3.0, 6.0)
        if pair is None:
            pair = self._unique_xy(0, beat or isolated + other)
        x0, y0 = float(pair[0]), float(pair[1])
        a = formula(isolated, 24, BLUE, 6.2).move_to(3.15 * LEFT + 0.95 * UP)
        b = formula(other, 24, PINK, 6.2).move_to(3.15 * LEFT + 0.35 * UP)
        self.play(FadeIn(a, LEFT), FadeIn(b, LEFT), run_time=0.35)
        plug_m = formula(plug or isolated, 22, GOLD, 6.4).move_to(3.15 * LEFT + 0.35 * DOWN)
        out = formula(f"({_fmt_n(x0)}, {_fmt_n(y0)})", 32, GREEN, 12).move_to(3.15 * LEFT + 1.15 * DOWN)
        self.sfx("whoosh", -11)
        self.play(FadeIn(plug_m, RIGHT), run_time=0.3)
        self.play(GrowFromCenter(out), run_time=0.3)
        f1 = self._y_fn_from_eq(isolated)
        f2 = self._y_fn_from_eq(other)
        graph = self._cross_at(
            x0,
            y0,
            self._slope_of(f1),
            self._slope_of(f2),
            where=2.65 * RIGHT + 0.15 * DOWN,
            width=3.0,
            height=2.8,
        )
        self.pop_flash(graph[3].get_center())
        return VGroup(a, b, plug_m, out, graph)

    def demo_eliminate(self, beat=""):
        eqs = parse_lin_system(beat)
        pair = pair_from_text(beat)
        if len(eqs) >= 2:
            e1, e2 = eqs[0], eqs[1]
        elif pair:
            lab = formula(f"({_fmt_n(pair[0])}, {_fmt_n(pair[1])})", 40, GOLD, 12)
            self.play(GrowFromCenter(lab), run_time=0.4)
            return lab
        else:
            return self.demo_choose_method()
        kind, xy = solve_lin_system(e1, e2)
        add_cancel = abs(e1["a"] + e2["a"]) < 1e-8 or abs(e1["b"] + e2["b"]) < 1e-8
        sub_cancel = abs(e1["a"] - e2["a"]) < 1e-8 or abs(e1["b"] - e2["b"]) < 1e-8
        vx, vy = e1.get("x", "x"), e1.get("y", "y")
        tbeat = caretify(beat)
        mscale = re.search(r"[×x]\s*(\d+)", tbeat, re.I)
        if add_cancel:
            op, k1, k2, sign = "ADD", 1.0, 1.0, 1.0
        elif sub_cancel:
            op, k1, k2, sign = "SUBTRACT", 1.0, 1.0, -1.0
        else:
            op, k1, k2, sign = "SCALE then SUBTRACT", 1.0, 1.0, -1.0
            picked = False
            if mscale:
                k = float(mscale.group(1))
                t2a, t2b = k * e2["a"], k * e2["b"]
                if abs(e1["a"] - t2a) < 1e-8 or abs(e1["b"] - t2b) < 1e-8:
                    k1, k2, sign, op, picked = 1.0, k, -1.0, "SUBTRACT", True
                elif abs(e1["a"] + t2a) < 1e-8 or abs(e1["b"] + t2b) < 1e-8:
                    k1, k2, sign, op, picked = 1.0, k, 1.0, "ADD", True
            if not picked:
                for var in ("a", "b"):
                    a1, a2 = e1[var], e2[var]
                    if abs(a2) < 1e-8:
                        continue
                    ratio = a1 / a2
                    if abs(ratio) >= 0.99 and abs(ratio - round(ratio)) < 1e-6:
                        k1, k2 = 1.0, float(abs(round(ratio)))
                        sign = -1.0 if (a1 * a2) > 0 else 1.0
                        op = "SUBTRACT" if sign < 0 else "ADD"
                        picked = True
                        break
            if not picked:
                op = "SCALE then SUBTRACT"
                if abs(e1["b"]) > 1e-8 and abs(e2["b"]) > 1e-8:
                    k1, k2 = abs(e2["b"]), abs(e1["b"])
                elif abs(e1["a"]) > 1e-8 and abs(e2["a"]) > 1e-8:
                    k1, k2 = abs(e2["a"]), abs(e1["a"])
                sign = -1.0
        combined = {
            "a": k1 * e1["a"] + sign * k2 * e2["a"],
            "b": k1 * e1["b"] + sign * k2 * e2["b"],
            "c": k1 * e1["c"] + sign * k2 * e2["c"],
            "x": vx,
            "y": vy,
            "src": "",
        }
        lead = combined["a"] if abs(combined["a"]) > 1e-8 else combined["b"]
        if lead < 0:
            combined["a"] *= -1
            combined["b"] *= -1
            combined["c"] *= -1
        s1 = {
            "a": k1 * e1["a"], "b": k1 * e1["b"], "c": k1 * e1["c"],
            "x": vx, "y": vy, "src": "",
        }
        s2 = {
            "a": k2 * e2["a"], "b": k2 * e2["b"], "c": k2 * e2["c"],
            "x": vx, "y": vy, "src": "",
        }
        eq1 = formula(fmt_lin_eq(s1), 24, BLUE, 8)
        eq2 = formula(fmt_lin_eq(s2), 24, PINK, 8)
        stack = VGroup(eq1, eq2).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        mark = formula("+" if sign > 0 else "-", 34, GOLD, 4)
        mark.next_to(eq2, LEFT, buff=0.14)
        bar = Line(stack.get_left() + 0.08 * LEFT, stack.get_right() + 0.08 * RIGHT)
        bar.set_stroke(GOLD, 3)
        bar.next_to(stack, DOWN, buff=0.1)
        op_lab = formula(op, 20, GOLD, 22)
        op_lab.next_to(bar, DOWN, buff=0.1)
        if kind == "one":
            sum_txt = fmt_lin_eq(combined)
            result = f"({_fmt_n(xy[0])}, {_fmt_n(xy[1])})"
        elif kind == "none":
            if abs(combined["a"]) < 1e-8 and abs(combined["b"]) < 1e-8:
                sum_txt = f"0 = {_fmt_n(combined['c'])}"
            else:
                sum_txt = fmt_lin_eq(combined)
            result = "no solution"
        else:
            sum_txt = "0 = 0"
            result = "infinitely many"
        sum_m = formula(sum_txt, 24, TEAL, 10)
        sum_m.next_to(op_lab, DOWN, buff=0.1)
        out = formula(result, 26, GREEN if kind == "one" else (RED if kind == "none" else GOLD), 14)
        out.next_to(sum_m, DOWN, buff=0.16)
        left = VGroup(stack, mark, bar, op_lab, sum_m, out)
        left.move_to(3.15 * LEFT + 0.05 * DOWN)
        if left.get_height() > 4.6:
            left.scale(4.6 / left.get_height())
            left.move_to(3.15 * LEFT + 0.05 * DOWN)
        self.play(FadeIn(eq1), FadeIn(eq2), run_time=0.3)
        self.sfx("thud", -11)
        self.play(FadeIn(mark), FadeIn(bar), run_time=0.28)
        self.play(FadeIn(op_lab), FadeIn(sum_m), run_time=0.32)
        self.play(GrowFromCenter(out), run_time=0.28)
        graph = self._elim_graph(e1, e2, kind, xy)
        return VGroup(left, graph)

    def _elim_graph(self, e1, e2, kind, xy):
        x0, y0 = (2.0, 2.0) if not xy else (float(xy[0]), float(xy[1]))
        x_lo = min(-1.0, x0 - 1.5)
        y_lo = min(-1.0, y0 - 1.5)
        x_hi = min(10.0, max(6.0, abs(x0) + 2.5))
        y_hi = min(10.0, max(6.0, abs(y0) + 2.5))
        axes = Axes((x_lo, x_hi), (y_lo, y_hi), height=2.85, width=3.05)
        axes.set_stroke(MUTED, 2)
        f1 = self._sys_fn(e1)
        f2 = self._sys_fn(e2) if e2 else None
        if f1:
            l1 = axes.get_graph(f1).set_stroke(BLUE, 8 if kind == "inf" else 4, 0.5 if kind == "inf" else 1)
        else:
            xv = e1["c"] / e1["a"] if abs(e1["a"]) > 1e-8 else 0
            l1 = Line(axes.c2p(xv, y_lo), axes.c2p(xv, y_hi)).set_stroke(BLUE, 4)
        l2 = None
        if e2 is None:
            pass
        elif kind == "inf":
            l2 = axes.get_graph(f1 or (lambda t: 0.5 * t + 1)).set_stroke(GOLD, 4)
        elif f2:
            l2 = axes.get_graph(f2).set_stroke(PINK, 4)
        else:
            xv = e2["c"] / e2["a"] if abs(e2["a"]) > 1e-8 else 0
            l2 = Line(axes.c2p(xv, y_lo), axes.c2p(xv, y_hi)).set_stroke(PINK, 4)
        bits = [axes, l1] + ([l2] if l2 is not None else [])
        extra = []
        if kind == "one" and xy:
            dot = Dot(axes.c2p(x0, y0), fill_color=GOLD).scale(1.2)
            lab = formula(f"({_fmt_n(x0)}, {_fmt_n(y0)})", 18, GOLD, 12)
            lab.next_to(dot, UR, buff=0.08)
            bits.extend([dot, lab])
            extra.extend([dot, lab])
        elif kind == "inf":
            fn = f1 or f2 or (lambda t: 0.5 * t + 1)
            for t in (0.4, 2.0, 3.6):
                extra.append(Dot(axes.c2p(t, fn(t)), fill_color=GOLD).scale(0.85))
            bits.extend(extra)
        g = VGroup(*bits).move_to(2.65 * RIGHT + 0.08 * DOWN)
        self.play(ShowCreation(axes), run_time=0.25)
        if l2 is None:
            self.play(ShowCreation(l1), run_time=0.48)
        else:
            self.play(ShowCreation(l1), ShowCreation(l2), run_time=0.48)
        if kind == "one" and extra:
            self.play(GrowFromCenter(extra[0]), FadeIn(extra[1]), run_time=0.28)
            self.pop_flash(extra[0].get_center(), GOLD, 0.5)
        elif kind == "inf":
            self.play(LaggedStart(*[GrowFromCenter(d) for d in extra], lag_ratio=0.12), run_time=0.4)
        elif l2 is not None:
            mid = (l1.get_center() + l2.get_center()) / 2
            xa = Line(mid + 0.28 * UL, mid + 0.28 * DR).set_stroke(RED, 5)
            xb = Line(mid + 0.28 * UR, mid + 0.28 * DL).set_stroke(RED, 5)
            self.play(ShowCreation(xa), ShowCreation(xb), run_time=0.28)
            g.add(xa, xb)
        return g

    # ----- pythagoras: NEVER loop the same 3-4-5 -----

    def _side_lab(self, n):
        if abs(float(n) - round(float(n))) < 0.05:
            return str(int(round(float(n))))
        shown = f"{float(n):.2f}".rstrip("0").rstrip(".")
        return shown

    def _tri_points(self, a, b, scale):
        return ORIGIN, a * scale * RIGHT, a * scale * RIGHT + b * scale * UP

    def _scalene_points(self, bc, ac, ab, scale):
        A = ORIGIN
        B = ab * scale * RIGHT
        cos_a = (ac * ac + ab * ab - bc * bc) / (2.0 * ac * ab)
        cos_a = max(-1.0, min(1.0, cos_a))
        sin_a = (1.0 - cos_a * cos_a) ** 0.5
        C = ac * scale * cos_a * RIGHT + ac * scale * sin_a * UP
        return A, B, C

    def _pts_in(self, beat):
        return [(int(x), int(y)) for x, y in re.findall(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", beat)]

    def _parse_cyl(self, beat):
        t = caretify(beat).lower()
        r = h = d = None
        m = re.search(r"diameter\s+(\d+(?:\.\d+)?)", t)
        if m:
            d = float(m.group(1))
            r = d / 2.0
        m = re.search(r"\br\s*=\s*(\d+(?:\.\d+)?)", t)
        if m:
            r = float(m.group(1))
        m = re.search(r"radius\s+(\d+(?:\.\d+)?)", t)
        if m:
            r = float(m.group(1))
        m = re.search(r"\bh\s*=\s*(\d+(?:\.\d+)?)", t)
        if m:
            h = float(m.group(1))
        m = re.search(r"height\s+(\d+(?:\.\d+)?)", t)
        if m:
            h = float(m.group(1))
        vol = None
        if r is not None and h is not None:
            vol = round(3.14 * r * r * h, 2)
            if abs(vol - round(vol)) < 1e-9:
                vol = int(round(vol))
        return r, h, vol, d

    def anim_pythag(self, beat_i, beat):
        t = caretify(beat)
        pts = self._pts_in(beat)
        if has(beat, "2, 3, 4", "2, 3 and 4") or (has(beat, "not right", "not equal") and not has(beat, "might not")):
            return self.demo_triangle(2, 3, "NOT right", right=False, c=4)
        if has(beat, "ladder") or (has(beat, "13 ft") and has(beat, "wall")):
            return self.demo_ladder()
        if has(beat, "share an x", "vertical"):
            return self.demo_distance((2, 1), (2, 6))
        if has(beat, "signs square", "(-3)", "never negative"):
            return self.demo_signed_run()
        if len(pts) >= 4:
            return self.demo_two_distances(pts[1], pts[3])
        if len(pts) >= 2:
            return self.demo_distance(pts[0], pts[1])
        if has(beat, "5-12-13") and has(beat, "8-15-17"):
            return self.demo_two_triples((5, 12, "5-12-13"), (8, 15, "8-15-17"))
        if has(beat, "6-8-10") and has(beat, "9-12-15"):
            return self.demo_two_triples((6, 8, "6-8-10"), (9, 12, "9-12-15"))
        if has(beat, "8-15-17"):
            return self.demo_triangle(8, 15, "8-15-17")
        if has(beat, "9-12-15"):
            return self.demo_triangle(9, 12, "9-12-15")
        if has(beat, "6-8-10", "6, 8, and 10", "6, 8 and 10", "6, 8, 10", "sides 6, 8", "legs 6 and 8"):
            return self.demo_triangle(6, 8, "6-8-10  (double 3-4-5)")
        if has(beat, "5-12-13", "5 and 12", "legs 5 and 12"):
            return self.demo_triangle(5, 12, "5-12-13")
        if has(beat, "formula", "x2 - x1", "coordinate clothes"):
            return self.demo_distance_formula()
        if has(beat, "bird", "diagonally", "street grid"):
            return self.demo_grid_vs_diag()
        if has(beat, "silo", "grain") or (has(beat, "cylinder") and has(beat, "3.14", "units", "curved", "cans")):
            return self.demo_cylinder(r=2, h=5, vol=62.8)
        if has(beat, "name the shape", "triangle or cylinder"):
            return self.demo_shape_choice()
        if has(beat, "cones", "spheres", "curved solid"):
            return self.demo_cylinder()
        if has(beat, "little square", "corner marks"):
            return self.demo_corner_square()
        if has(beat, "subtract", "square root", "know c", "one leg"):
            return self.demo_missing_leg(5, 13)
        if has(beat, "9 + 16", "legs 3 and 4", "3, 4, 5", "already satisfy"):
            return self.demo_squares_on_sides(3, 4)
        if has(beat, "longest", "two shorter"):
            return self.demo_triangle(2, 3, "test the longest", right=False, c=4)
        if has(beat, "90", "right angle", "legs a and b"):
            return self.demo_right_intro()
        if has(beat, "distance", "coordinate"):
            return self.demo_distance()
        if has(beat, "hypotenuse") and not has(beat, "bird"):
            return self.demo_right_intro()
        return self.demo_right_intro()

    def _make_triangle_group(self, a, b, caption, right=True, c=None, max_side=2.4):
        if c is None:
            c = (a * a + b * b) ** 0.5
        scale = max_side / max(a, b, c, 1)
        if right:
            A, B, Cpt = self._tri_points(a, b, scale)
            la = T(self._side_lab(a), 20, BLUE, 6).next_to(Line(A, B), DOWN, buff=0.08)
            lb = T(self._side_lab(b), 20, TEAL, 6).next_to(Line(B, Cpt), RIGHT, buff=0.08)
            lc = T(self._side_lab(c), 20, GOLD, 8)
            lc.move_to((A + Cpt) / 2 + 0.22 * LEFT + 0.12 * UP)
        else:
            A, B, Cpt = self._scalene_points(b, a, c, scale)
            la = T(self._side_lab(c), 20, BLUE, 6).next_to(Line(A, B), DOWN, buff=0.08)
            lb = T(self._side_lab(a), 20, TEAL, 6).next_to(Line(A, Cpt), LEFT, buff=0.08)
            lc = T(self._side_lab(b), 20, GOLD, 8).next_to(Line(B, Cpt), RIGHT, buff=0.08)
        tri = Polygon(A, B, Cpt).set_stroke(CREAM, 4).set_fill(GOLD if right else RED, 0.12)
        cap = T(caption, 18, GREEN if right else RED, 22)
        g = VGroup(tri, la, lb, lc)
        return VGroup(g, cap).arrange(DOWN, buff=0.16)

    def demo_right_intro(self):
        A, B, C = self._tri_points(4, 3, 0.55)
        tri = Polygon(A, B, C).set_stroke(CREAM, 4).set_fill(BLUE, 0.12)
        sq = Square(0.28).set_stroke(GOLD, 3).move_to(B + 0.14 * LEFT + 0.14 * UP)
        la = T("a", 20, BLUE, 6).next_to(Line(A, B), DOWN, buff=0.08)
        lb = T("b", 20, TEAL, 6).next_to(Line(B, C), RIGHT, buff=0.08)
        hyp = T("hypotenuse c", 20, GOLD, 18).move_to((A + C) / 2 + 0.35 * LEFT + 0.2 * UP)
        g = VGroup(tri, sq, la, lb).move_to(0.35 * DOWN)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(tri), run_time=0.55)
        self.play(FadeIn(sq), FadeIn(la), FadeIn(lb), FadeIn(hyp), run_time=0.3)
        self.play(WiggleOutThenIn(sq, run_time=0.4, n_wiggles=4))
        return VGroup(g, hyp)

    def demo_triangle(self, a, b, caption, right=True, c=None):
        pack = self._make_triangle_group(a, b, caption, right=right, c=c, max_side=2.6)
        pack.move_to(0.3 * DOWN)
        self.play(FadeIn(pack, UP), run_time=0.5)
        if not right:
            self.sfx("wrong", -9)
            cross = Line(pack.get_corner(UL), pack.get_corner(DR)).set_stroke(RED, 5)
            self.play(ShowCreation(cross), run_time=0.25)
            return VGroup(pack, cross)
        self.pop_flash(pack.get_center(), GOLD, 0.6)
        return pack

    def demo_two_triples(self, left, right):
        g1 = self._make_triangle_group(*left, max_side=1.7)
        g2 = self._make_triangle_group(*right, max_side=1.7)
        pack = VGroup(g1, g2).arrange(RIGHT, buff=0.85).move_to(0.2 * DOWN)
        self.play(FadeIn(g1, LEFT), FadeIn(g2, RIGHT), run_time=0.55)
        return pack

    def _outward_square(self, P, Q, inside):
        v = Q - P
        n = np.array([-v[1], v[0], 0.0])
        mid = (P + Q) / 2
        if np.dot(n[:2], (mid - inside)[:2]) < 0:
            n = -n
        nlen = np.linalg.norm(n)
        vlen = np.linalg.norm(v)
        if nlen < 1e-9 or vlen < 1e-9:
            return Polygon(P, Q, Q, P)
        n = n * (vlen / nlen)
        return Polygon(P, Q, Q + n, P + n)

    def demo_squares_on_sides(self, a, b):
        c2 = a * a + b * b
        c = c2 ** 0.5
        scale = 0.38
        A, B, C = self._tri_points(a, b, scale)
        tri = Polygon(A, B, C).set_stroke(CREAM, 3).set_fill(GOLD, 0.08)
        inside = (A + B + C) / 3
        s_a = self._outward_square(A, B, inside).set_stroke(BLUE, 3).set_fill(BLUE, 0.15)
        s_b = self._outward_square(B, C, inside).set_stroke(TEAL, 3).set_fill(TEAL, 0.15)
        s_c = self._outward_square(C, A, inside).set_stroke(GOLD, 3).set_fill(GOLD, 0.12)
        ta = T(str(a * a), 18, BLUE, 8).move_to(s_a.get_center())
        tb = T(str(b * b), 18, TEAL, 8).move_to(s_b.get_center())
        tc = T(str(int(c2)), 18, GOLD, 8).move_to(s_c.get_center())
        eq = T(f"{a * a} + {b * b} = {int(c2)}", 24, GOLD, 24)
        g = VGroup(s_a, s_b, s_c, tri, ta, tb, tc)
        pack = VGroup(g, eq).arrange(DOWN, buff=0.28).move_to(0.1 * DOWN)
        self.play(ShowCreation(tri), run_time=0.35)
        self.sfx("pop", -12)
        self.play(FadeIn(s_a), FadeIn(ta), run_time=0.3)
        self.play(FadeIn(s_b), FadeIn(tb), run_time=0.3)
        self.play(FadeIn(s_c), FadeIn(tc), run_time=0.3)
        self.sfx("ding", -10)
        self.play(FadeIn(eq), run_time=0.35)
        return pack

    def demo_missing_leg(self, a, c):
        b = int(round((c * c - a * a) ** 0.5))
        pic = self._make_triangle_group(a, b, f"leg {b}", c=c, max_side=2.0)
        pic.to_edge(RIGHT, buff=0.45).shift(0.2 * DOWN)
        src = T(f"c = {c},  leg = {a}", 26, CREAM, 24).move_to(2.2 * LEFT + 0.9 * UP)
        self.play(FadeIn(src), FadeIn(pic), run_time=0.35)
        step = T(f"{c * c} - {a * a} = {c * c - a * a}", 26, TEAL, 28)
        step.next_to(src, DOWN, buff=0.28, aligned_edge=LEFT)
        self.play(FadeIn(step, UP), run_time=0.3)
        out = T(f"other leg = {b}", 32, GOLD, 20)
        out.next_to(step, DOWN, buff=0.28, aligned_edge=LEFT)
        self.sfx("ding", -10)
        self.play(GrowFromCenter(out), run_time=0.35)
        return VGroup(src, step, out, pic)

    def demo_ladder(self):
        wall = Line(ORIGIN, 2.6 * UP).set_stroke("#c8c8c8", 10)
        ground = Line(ORIGIN, 1.35 * LEFT).set_stroke("#a0d0a0", 10)
        lad = Line(1.35 * LEFT, 2.6 * UP).set_stroke(GOLD, 7)
        a = T("5  ground", 18, BLUE, 12).next_to(ground, DOWN, buff=0.08)
        b = T("12  wall", 18, TEAL, 12).next_to(wall, RIGHT, buff=0.08)
        c = T("13  ladder", 20, GOLD, 14).move_to(0.35 * LEFT + 1.45 * UP)
        g = VGroup(wall, ground, lad, a, b, c).move_to(0.25 * DOWN)
        self.play(ShowCreation(wall), ShowCreation(ground), run_time=0.35)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(lad), FadeIn(a), FadeIn(b), FadeIn(c), run_time=0.5)
        return g

    def demo_distance(self, p=(1, 2), q=(4, 6)):
        dx = q[0] - p[0]
        dy = q[1] - p[1]
        dist = (dx * dx + dy * dy) ** 0.5
        xs = [p[0], q[0], 0]
        ys = [p[1], q[1], 0]
        x0, x1 = min(xs) - 1, max(xs) + 1
        y0, y1 = min(ys) - 1, max(ys) + 1
        if x1 - x0 < 4:
            x1 = x0 + 4
        if y1 - y0 < 4:
            y1 = y0 + 4
        axes = Axes((x0, x1), (y0, y1), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        pdot = Dot(axes.c2p(*p), fill_color=TEAL)
        qdot = Dot(axes.c2p(*q), fill_color=GOLD)
        hyp = Line(pdot.get_center(), qdot.get_center()).set_stroke(PINK, 4)
        extras = []
        if dx and dy:
            elbow = axes.c2p(q[0], p[1])
            run = Line(pdot.get_center(), elbow).set_stroke(BLUE, 3)
            rise = Line(elbow, qdot.get_center()).set_stroke(TEAL, 3)
            extras.extend([run, rise])
            rlab = T("run " + self._side_lab(abs(dx)), 16, BLUE, 12)
            ulab = T("rise " + self._side_lab(abs(dy)), 16, TEAL, 12)
            rlab.next_to(run, DOWN, buff=0.06)
            ulab.next_to(rise, RIGHT, buff=0.06)
            extras.extend([rlab, ulab])
        lab = T("distance " + self._side_lab(dist), 20, GOLD, 18)
        pack = VGroup(axes, pdot, qdot, hyp, *extras)
        g = VGroup(pack, lab).arrange(DOWN, buff=0.12).move_to(0.25 * DOWN)
        self.play(ShowCreation(axes), GrowFromCenter(pdot), GrowFromCenter(qdot), run_time=0.4)
        if dx and dy:
            self.play(ShowCreation(extras[0]), ShowCreation(extras[1]), run_time=0.3)
        self.play(ShowCreation(hyp), FadeIn(lab), run_time=0.35)
        return g

    def demo_distance_formula(self):
        def sub(name, ix, size=36, color=WHITE):
            n = Text(name, font=FONT_MATH, font_size=size).set_color(color)
            s = Text(ix, font=FONT_MATH, font_size=int(size * 0.52)).set_color(TEAL)
            s.next_to(n, DR, buff=0.02)
            s.shift(0.10 * LEFT + 0.04 * UP)
            return VGroup(n, s)

        def minus_bar(sz=36):
            half = max(0.055, min(0.09, sz * 0.0020))
            return Line(LEFT * half, RIGHT * half).set_stroke(WHITE, max(2.0, sz / 26.0))

        def pair_sq(xn, xi, yn, yi):
            inner = VGroup(
                Text("(", font=FONT_MATH, font_size=34).set_color(WHITE),
                sub(xn, xi),
                minus_bar(),
                sub(yn, yi),
                Text(")", font=FONT_MATH, font_size=34).set_color(WHITE),
            ).arrange(RIGHT, buff=0.06, aligned_edge=ORIGIN)
            exp = Text("2", font=FONT_MATH, font_size=20).set_color(GOLD)
            exp.next_to(inner, UR, buff=0.04)
            return VGroup(inner, exp)

        body = VGroup(
            pair_sq("x", "2", "x", "1"),
            Text("+", font=FONT_MATH, font_size=34).set_color(GOLD),
            pair_sq("y", "2", "y", "1"),
        ).arrange(RIGHT, buff=0.14, aligned_edge=ORIGIN)
        rad = radical_mob(" ", 40, WHITE)
        # Drop the dummy inner letter; keep the drawn radical, then park body under the bar.
        hook = VGroup(*rad.submobjects[:3])
        body.next_to(hook, RIGHT, buff=0.08)
        body.shift(0.08 * DOWN)
        # Stretch the vinculum over the whole inner formula.
        bar = hook[2]
        bar.put_start_and_end_on(
            bar.get_start(),
            np.array([body.get_right()[0] + 0.12, bar.get_start()[1], 0]),
        )
        expr = VGroup(hook, body)
        tag = T("same theorem, coordinate clothes", 20, GOLD, 32)
        pack = VGroup(expr, tag).arrange(DOWN, buff=0.4).move_to(0.15 * DOWN)
        self.play(FadeIn(expr), run_time=0.55)
        self.play(FadeIn(tag), run_time=0.25)
        return pack

    def demo_two_distances(self, q1, q2):
        span = max(q1[0], q2[0], q1[1], q2[1], 6) + 2
        axes = Axes((-1, span, 1), (-1, span, 1), height=3.5, width=3.5)
        axes.set_stroke(MUTED, 2)
        o = Dot(axes.c2p(0, 0), fill_color=CREAM)
        d1 = Dot(axes.c2p(*q1), fill_color=TEAL).scale(1.2)
        d2 = Dot(axes.c2p(*q2), fill_color=GOLD).scale(1.2)
        s1 = Line(o.get_center(), d1.get_center()).set_stroke(TEAL, 4)
        s2 = Line(o.get_center(), d2.get_center()).set_stroke(GOLD, 4)
        n1 = (q1[0] * q1[0] + q1[1] * q1[1]) ** 0.5
        n2 = (q2[0] * q2[0] + q2[1] * q2[1]) ** 0.5
        p1 = T(f"({q1[0]}, {q1[1]})", 16, TEAL, 16).next_to(d1, UR, buff=0.08)
        p2 = T(f"({q2[0]}, {q2[1]})", 16, GOLD, 16).next_to(d2, LEFT, buff=0.10)
        l1 = T(f"distance {self._side_lab(n1)}", 16, TEAL, 18)
        l2 = T(f"distance {self._side_lab(n2)}", 16, GOLD, 18)
        labs = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        pack = VGroup(axes, o, d1, d2, s1, s2, p1, p2)
        g = VGroup(pack, labs).arrange(DOWN, buff=0.12).move_to(0.2 * DOWN)
        self.play(ShowCreation(axes), GrowFromCenter(o), run_time=0.3)
        self.play(ShowCreation(s1), GrowFromCenter(d1), FadeIn(p1), FadeIn(l1), run_time=0.35)
        self.play(ShowCreation(s2), GrowFromCenter(d2), FadeIn(p2), FadeIn(l2), run_time=0.35)
        return g

    def demo_signed_run(self):
        eq = T("(-3)^2 = 9", 44, GOLD, 16).move_to(0.35 * UP)
        tag = T("distance is never negative", 22, TEAL, 28).next_to(eq, DOWN, buff=0.28)
        self.play(FadeIn(eq), run_time=0.35)
        self.play(FadeIn(tag), run_time=0.25)
        return VGroup(eq, tag)

    def demo_grid_vs_diag(self):
        A = ORIGIN
        B = 2.2 * RIGHT
        C = 2.2 * RIGHT + 2.9 * UP
        street = VGroup(Line(A, B), Line(B, C)).set_stroke(MUTED, 6)
        diag = Line(A, C).set_stroke(GOLD, 5)
        g = T("grid  3 + 4 = 7", 20, MUTED, 22)
        f = T("fly  hypotenuse 5", 20, GOLD, 22)
        labs = VGroup(g, f).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        pic = VGroup(street, diag).move_to(1.6 * LEFT + 0.15 * DOWN)
        labs.next_to(pic, RIGHT, buff=0.45)
        self.play(ShowCreation(street), run_time=0.4)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(diag), FadeIn(labs), run_time=0.45)
        return VGroup(pic, labs)

    def demo_shape_choice(self):
        tri = self._make_triangle_group(3, 4, "right triangle", max_side=1.6)
        cyl = self._cylinder_mobject()
        cap = T("or a cylinder", 18, BLUE, 16)
        right = VGroup(cyl, cap).arrange(DOWN, buff=0.16)
        pack = VGroup(tri, right).arrange(RIGHT, buff=1.1).move_to(0.2 * DOWN)
        self.play(FadeIn(tri, LEFT), FadeIn(right, RIGHT), run_time=0.5)
        return pack

    def demo_corner_square(self):
        return self.demo_right_intro()

    # ----- cylinder -----

    def anim_cylinder(self, beat_i, beat):
        r, h, vol, d = self._parse_cyl(beat)
        if has(beat, "would be wrong", "square r alone", "(pi r)"):
            return self.demo_wrong_pi_square()
        if has(beat, "height doubles"):
            return self.demo_stack_height(doubled=True)
        if has(beat, "r doubles", "quadruples"):
            return self.demo_double_radius()
        if has(beat, "square r first"):
            return self.demo_square_r_order(r or 2, h or 5)
        if d is not None and has(beat, "diameter 6", "141.3", "r = 3"):
            return self.demo_cylinder(r=r or 3, h=h or 5, vol=vol or 141.3, diameter=d)
        if has(beat, "twice the radius", "never plug", "diameter is"):
            return self.demo_diameter_warning()
        if r is not None and h is not None:
            return self.demo_cylinder(r=r, h=h, vol=vol, diameter=d)
        if has(beat, "3.14") and has(beat, "pi", "unless"):
            return self.demo_pi_approx()
        if has(beat, "base area", "base is a circle"):
            return self.demo_base_area()
        if has(beat, "stack"):
            return self.demo_stack_height()
        return self.demo_cylinder()

    def _cylinder_mobject(self, r=1.15, h=2.5, r_lab="r", h_lab="h"):
        rw = max(0.9, min(2.3, 0.7 + 0.28 * float(r if isinstance(r, (int, float)) else 2)))
        hh = max(1.2, min(2.8, 0.7 + 0.28 * float(h if isinstance(h, (int, float)) else 5)))
        top = Ellipse(width=2 * rw, height=0.62 * rw).set_stroke(BLUE, 4).set_fill(BLUE, 0.18)
        bot = Ellipse(width=2 * rw, height=0.62 * rw).set_stroke(BLUE, 4).set_fill("#1e3a8a", 0.45)
        top.shift((hh / 2) * UP)
        bot.shift((hh / 2) * DOWN)
        left = Line(top.get_left(), bot.get_left()).set_stroke(BLUE, 4)
        right = Line(top.get_right(), bot.get_right()).set_stroke(BLUE, 4)
        hl = T(str(h_lab), 20, GOLD, 10).next_to(right, RIGHT, buff=0.1)
        rl = T(str(r_lab), 20, TEAL, 10).next_to(top, UP, buff=0.06)
        return VGroup(bot, left, right, top, hl, rl)

    def demo_cylinder(self, r=None, h=None, vol=None, diameter=None):
        r_lab = f"r = {self._side_lab(r)}" if r is not None else "r"
        h_lab = f"h = {self._side_lab(h)}" if h is not None else "h"
        g = self._cylinder_mobject(r if r is not None else 2, h if h is not None else 5, r_lab, h_lab)
        extras = []
        if diameter is not None:
            top = g[3]
            dline = Line(top.get_left(), top.get_right()).set_stroke(GOLD, 3)
            dlab = T(f"d = {self._side_lab(diameter)}", 18, GOLD, 12).next_to(top, DOWN, buff=0.05)
            extras.extend([dline, dlab])
        if vol is not None:
            eq = T(f"V = {vol}", 28, GOLD, 16)
        else:
            eq = VGroup(T("V = pi", 24, GOLD, 14), power_mob("r", "2", 28, 16, GOLD, TEAL), T("h", 24, GOLD, 6))
            eq.arrange(RIGHT, buff=0.1)
        body = VGroup(g, *extras)
        body.move_to(0.35 * DOWN + 1.55 * LEFT)
        eq.next_to(body, RIGHT, buff=0.4)
        self.play(ShowCreation(g[0]), run_time=0.2)
        self.play(ShowCreation(g[1]), ShowCreation(g[2]), run_time=0.25)
        self.play(ShowCreation(g[3]), FadeIn(g[4]), FadeIn(g[5]), run_time=0.28)
        if extras:
            self.play(*[FadeIn(x) if not isinstance(x, Line) else ShowCreation(x) for x in extras], run_time=0.25)
        self.play(body.animate.shift(0.1 * UP), run_time=0.15)
        self.play(body.animate.shift(0.1 * DOWN), run_time=0.15)
        self.sfx("pop", -11)
        self.play(GrowFromCenter(eq), run_time=0.28)
        return VGroup(body, eq)

    def demo_base_area(self, r=None):
        rad = 1.15
        circ = Circle(radius=rad).set_stroke(TEAL, 4).set_fill(TEAL, 0.15)
        rlab = T(f"r = {self._side_lab(r)}" if r is not None else "r", 22, GOLD, 10).next_to(circ, RIGHT, buff=0.1)
        eq = VGroup(T("base = pi", 24, GOLD, 16), power_mob("r", "2", 28, 16, GOLD, TEAL)).arrange(RIGHT, buff=0.1)
        g = VGroup(circ, rlab)
        pack = VGroup(g, eq).arrange(DOWN, buff=0.3).move_to(0.25 * DOWN)
        self.play(GrowFromCenter(circ), FadeIn(rlab), run_time=0.4)
        self.play(FadeIn(eq), run_time=0.35)
        return pack

    def demo_stack_height(self, doubled=False):
        def stack(n, color=BLUE):
            discs = VGroup()
            for _ in range(n):
                e = Ellipse(width=1.7, height=0.38).set_stroke(color, 2).set_fill(color, 0.18)
                discs.add(e)
            discs.arrange(UP, buff=0.02)
            return discs
        if doubled:
            a = stack(4, BLUE)
            b = stack(8, GOLD)
            la = T("h   ->  V", 18, BLUE, 14)
            lb = T("2h  ->  2V", 18, GOLD, 16)
            left = VGroup(a, la).arrange(DOWN, buff=0.16)
            right = VGroup(b, lb).arrange(DOWN, buff=0.16)
            pack = VGroup(left, right).arrange(RIGHT, buff=0.9).move_to(0.15 * DOWN)
            self.play(LaggedStart(*[FadeIn(d, UP) for d in a], lag_ratio=0.08), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(d, UP) for d in b], lag_ratio=0.06), FadeIn(la), FadeIn(lb), run_time=0.55)
            return pack
        discs = stack(5)
        h = T("stack the bases  x h", 22, GOLD, 28).next_to(discs, DOWN, buff=0.25)
        discs.move_to(0.25 * UP)
        self.play(LaggedStart(*[FadeIn(d, UP) for d in discs], lag_ratio=0.12), run_time=0.8)
        self.play(FadeIn(h), run_time=0.25)
        return VGroup(discs, h)

    def demo_square_r_order(self, r=2, h=5):
        r2 = int(r * r) if float(r) == int(r) else r * r
        pir2 = round(3.14 * float(r2), 2)
        vol = round(pir2 * float(h), 2)
        cards = VGroup(
            self._card(self._side_lab(r), TEAL, 1.15),
            self._card(self._side_lab(r2), BLUE, 1.25),
            self._card(self._side_lab(pir2), GOLD, 1.45),
            self._card(self._side_lab(vol), GREEN, 1.45),
        )
        cards.arrange(RIGHT, buff=0.22).move_to(0.2 * UP)
        labs = VGroup(
            T("r", 16, MUTED, 6),
            T("r^2", 16, MUTED, 8),
            T("pi r^2", 16, MUTED, 10),
            T("pi r^2 h", 16, MUTED, 12),
        )
        for lab, card in zip(labs, cards):
            lab.next_to(card, DOWN, buff=0.12)
        self.sfx("pop", -12)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cards], lag_ratio=0.18), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.12), run_time=0.4)
        return VGroup(cards, labs)

    def demo_wrong_pi_square(self):
        bad = T("(pi r)^2 h", 30, RED, 20).move_to(0.55 * UP)
        mark = T("WRONG", 22, RED, 12).next_to(bad, RIGHT, buff=0.2)
        good = VGroup(T("pi", 30, GREEN, 8), power_mob("r", "2", 34, 18, GREEN, GOLD), T("h", 30, GREEN, 8))
        good.arrange(RIGHT, buff=0.1).move_to(0.7 * DOWN)
        ok = T("square r alone", 20, GREEN, 20).next_to(good, DOWN, buff=0.18)
        self.play(FadeIn(bad), FadeIn(mark), run_time=0.35)
        self.sfx("wrong", -9)
        cross = Line(bad.get_left() + 0.1 * LEFT, bad.get_right() + 0.1 * RIGHT).set_stroke(RED, 4)
        self.play(ShowCreation(cross), run_time=0.25)
        self.play(FadeIn(good, UP), FadeIn(ok), run_time=0.35)
        return VGroup(bad, mark, cross, good, ok)

    def demo_diameter_warning(self):
        circ = Circle(radius=1.2).set_stroke(TEAL, 4).set_fill(TEAL, 0.12)
        dline = Line(circ.get_left(), circ.get_right()).set_stroke(GOLD, 4)
        rline = Line(circ.get_center(), circ.get_right()).set_stroke(BLUE, 4)
        dlab = T("d = 2r", 20, GOLD, 12).next_to(circ, UP, buff=0.12)
        rlab = T("r", 20, BLUE, 6).next_to(rline, DOWN, buff=0.08)
        warn = T("never plug d into r^2", 22, RED, 24).next_to(circ, DOWN, buff=0.35)
        g = VGroup(circ, dline, rline, dlab, rlab, warn).move_to(0.2 * DOWN)
        self.play(GrowFromCenter(circ), ShowCreation(dline), FadeIn(dlab), run_time=0.45)
        self.play(ShowCreation(rline), FadeIn(rlab), FadeIn(warn), run_time=0.35)
        return g

    def demo_double_radius(self):
        a = self._cylinder_mobject(1, 4, "r", "h")
        b = self._cylinder_mobject(2, 4, "2r", "h")
        la = T("V", 20, BLUE, 8)
        lb = T("4V", 22, GOLD, 8)
        left = VGroup(a, la).arrange(DOWN, buff=0.14)
        right = VGroup(b, lb).arrange(DOWN, buff=0.14)
        pack = VGroup(left, right).arrange(RIGHT, buff=1.0).move_to(0.15 * DOWN)
        self.play(FadeIn(left, LEFT), run_time=0.35)
        self.play(FadeIn(right, RIGHT), run_time=0.4)
        return pack

    def demo_pi_approx(self):
        eq = T("pi ~ 3.14", 44, GOLD, 16).move_to(0.7 * UP)
        g = self._cylinder_mobject(2, 4)
        g.next_to(eq, DOWN, buff=0.35)
        self.play(FadeIn(eq), run_time=0.3)
        self.play(FadeIn(g, UP), run_time=0.4)
        return VGroup(eq, g)

    # ----- scatter -----

    def _lsq(self, pts):
        n = float(len(pts))
        mx = sum(p[0] for p in pts) / n
        my = sum(p[1] for p in pts) / n
        den = sum((p[0] - mx) ** 2 for p in pts)
        if den < 1e-9:
            return 0.0, my
        slope = sum((p[0] - mx) * (p[1] - my) for p in pts) / den
        return slope, my - slope * mx

    def anim_scatter(self, beat_i, beat):
        if has(beat, "outlier") or has(beat, "pull the fitted", "far from the rest"):
            return self.demo_outlier(pull=has(beat, "pull"))
        if has(beat, "cluster"):
            return self.demo_cluster()
        if has(beat, "two-way", "categorical", "joint count", "relative frequency",
               "rows might", "among soccer", "12 of 40", "15 of 50", "15/50",
               "band vs sport", "band / no"):
            return self.demo_two_way(beat)
        if has(beat, "box plot", "median", "iqr", "longer box", "group a",
               "overlap is normal", "two sentences", "two classes", "side-by-side"):
            return self.demo_two_boxplots(beat)
        if has(beat, "match the data", "finish with a sentence") or (
            has(beat, "hours vs score") and has(beat, "two-way", "band vs")
        ):
            return self.demo_display_choice()
        if has(beat, "hours vs score"):
            return self.demo_scatter_pts(self._pts_pos(), "hours vs score", fit=True)
        if has(beat, "names vs", "wrong picture"):
            return self.demo_wrong_scatter()
        if has(beat, "negative", "falls"):
            return self.demo_scatter_pts(self._pts_neg(), "negative association", fit=True)
        if has(beat, "no association", "shapeless", "blob"):
            return self.demo_scatter_pts(self._pts_blob(), "no association", fit=False)
        if has(beat, "tight", "cigar") and has(beat, "weak", "spray"):
            return self.demo_strong_weak()
        if has(beat, "tight", "strong", "cigar"):
            return self.demo_scatter_pts(self._pts_tight(), "strong association", fit=True)
        if has(beat, "wide spray", "weak"):
            return self.demo_scatter_pts(self._pts_wide(), "weak association", fit=True)
        if has(beat, "interpolat"):
            return self.demo_interp_extra("in")
        if has(beat, "extrapolat"):
            return self.demo_interp_extra("out")
        if has(beat, "slope 2"):
            return self.demo_slope2_fit()
        if has(beat, "floats far", "question the line"):
            return self.demo_bad_fit()
        if has(beat, "exact y", "one person"):
            return self.demo_scatter_pts(self._pts_pos(), "typical path, not exact", fit=True)
        if has(beat, "best fit", "follows the trend", "not need to hit", "hit every"):
            return self.demo_scatter_pts(self._pts_pos(), "line of best fit", fit=True)
        if has(beat, "positive", "climbs"):
            return self.demo_scatter_pts(self._pts_pos(), "positive association", fit=True)
        return self.demo_scatter_pts(self._pts_cloud(), "scatter plot", fit=False)

    def _pts_cloud(self):
        return [
            (1.1, 2.6), (1.5, 4.2), (1.9, 1.7), (2.3, 3.5), (2.7, 5.1),
            (3.0, 2.2), (3.4, 4.0), (3.8, 1.5), (4.2, 3.2), (4.6, 5.4),
            (5.0, 2.8), (5.4, 4.6), (5.8, 1.9), (6.2, 3.7),
        ]

    def _pts_pos(self):
        return [
            (0.8, 1.2), (1.2, 1.7), (1.6, 1.5), (2.0, 2.3), (2.4, 2.0),
            (2.8, 3.0), (3.2, 3.4), (3.6, 3.1), (4.0, 4.1), (4.4, 4.5),
            (4.8, 4.2), (5.2, 5.2), (5.6, 5.5), (6.0, 5.8),
        ]

    def _pts_neg(self):
        return [
            (0.8, 5.9), (1.2, 5.5), (1.6, 5.2), (2.0, 4.7), (2.4, 4.4),
            (2.8, 4.0), (3.2, 3.5), (3.6, 3.2), (4.0, 2.8), (4.4, 2.4),
            (4.8, 2.1), (5.2, 1.7), (5.6, 1.5), (6.0, 1.1),
        ]

    def _pts_blob(self):
        return [
            (1.0, 3.4), (1.4, 1.3), (1.7, 5.2), (2.1, 2.7), (2.5, 4.8),
            (2.9, 1.6), (3.2, 5.5), (3.6, 3.0), (4.0, 2.1), (4.3, 4.9),
            (4.7, 1.5), (5.1, 3.7), (5.5, 5.3), (5.9, 2.4),
        ]

    def _pts_tight(self):
        return [
            (0.9, 1.3), (1.5, 1.8), (2.1, 2.4), (2.7, 2.9), (3.3, 3.4),
            (3.9, 4.0), (4.5, 4.5), (5.1, 5.1), (5.7, 5.6),
        ]

    def _pts_wide(self):
        return [
            (0.9, 2.6), (1.5, 1.1), (2.1, 3.8), (2.7, 2.0), (3.3, 4.6),
            (3.9, 2.8), (4.5, 5.4), (5.1, 3.5), (5.7, 5.9),
        ]

    def demo_scatter_pts(self, pts, caption, fit=False, color=TEAL):
        axes = Axes((0, 7), (0, 7), height=3.1, width=3.5)
        axes.set_stroke(MUTED, 2)
        dots = VGroup(*[Dot(axes.c2p(x, y), fill_color=color).scale(1.15) for x, y in pts])
        lab = T(caption, 20, GOLD, 28).next_to(axes, DOWN, buff=0.18)
        extras = [dots]
        line = None
        if fit and len(pts) >= 2:
            slope, intercept = self._lsq(pts)
            line = axes.get_graph(lambda x, m=slope, b=intercept: m * x + b).set_stroke(GOLD, 4)
            extras.append(line)
        pack = VGroup(axes, *extras, lab).move_to(0.1 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.sfx("pop", -12)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), run_time=0.65)
        if line is not None:
            self.play(ShowCreation(line), run_time=0.4)
        self.play(FadeIn(lab), run_time=0.2)
        return pack

    def demo_outlier(self, pull=False):
        cloud = [
            (1.0, 1.4), (1.6, 1.8), (2.2, 2.2), (2.8, 2.6),
            (3.4, 3.1), (4.0, 3.5), (4.6, 4.0),
        ]
        ox, oy = 5.5, 6.3
        axes = Axes((0, 7), (0, 7), height=3.1, width=3.5)
        axes.set_stroke(MUTED, 2)
        dots = VGroup(*[Dot(axes.c2p(x, y), fill_color=TEAL).scale(1.15) for x, y in cloud])
        slope, intercept = self._lsq(cloud)
        line = axes.get_graph(lambda x, m=slope, b=intercept: m * x + b).set_stroke(GOLD, 4)
        outlier = Dot(axes.c2p(ox, oy), fill_color=RED).scale(1.5)
        ring = Circle(radius=0.24).move_to(outlier.get_center()).set_stroke(RED, 3).set_fill(opacity=0)
        lab = T("outlier", 20, RED, 14).next_to(outlier, RIGHT, buff=0.12)
        cap = T("spot the outlier", 20, GOLD, 24).next_to(axes, DOWN, buff=0.2)
        pack = VGroup(axes, dots, line, outlier, ring, lab, cap).move_to(0.1 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.sfx("pop", -12)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), run_time=0.55)
        self.play(ShowCreation(line), run_time=0.32)
        self.play(GrowFromCenter(outlier), ShowCreation(ring), FadeIn(lab), FadeIn(cap), run_time=0.45)
        self.pop_flash(outlier.get_center(), RED, 0.5)
        extras = []
        if pull:
            s2, b2 = self._lsq(cloud + [(ox, oy)])
            pulled = axes.get_graph(lambda x, m=s2, b=b2: m * x + b).set_stroke(RED, 4)
            note = T("the line leans toward it", 18, RED, 28).next_to(cap, DOWN, buff=0.12)
            self.play(ShowCreation(pulled), FadeIn(note), run_time=0.45)
            extras.extend([pulled, note])
        return VGroup(pack, *extras)

    def demo_cluster(self):
        left = [(1.1, 1.2), (1.4, 1.6), (1.7, 1.1), (1.5, 1.8), (1.9, 1.4)]
        right = [(5.0, 4.9), (5.3, 5.4), (5.6, 4.8), (5.4, 5.2), (5.8, 5.0)]
        axes = Axes((0, 7), (0, 7), height=3.1, width=3.5)
        axes.set_stroke(MUTED, 2)
        d1 = VGroup(*[Dot(axes.c2p(x, y), fill_color=TEAL).scale(1.15) for x, y in left])
        d2 = VGroup(*[Dot(axes.c2p(x, y), fill_color=PINK).scale(1.15) for x, y in right])
        e1 = Ellipse(width=1.35, height=1.15).move_to(axes.c2p(1.5, 1.42))
        e1.set_stroke(TEAL, 2).set_fill(TEAL, 0.08)
        e2 = Ellipse(width=1.35, height=1.15).move_to(axes.c2p(5.4, 5.06))
        e2.set_stroke(PINK, 2).set_fill(PINK, 0.08)
        lab = T("two clusters", 20, GOLD, 20).next_to(axes, DOWN, buff=0.18)
        pack = VGroup(axes, e1, e2, d1, d2, lab).move_to(0.1 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.sfx("pop", -12)
        self.play(FadeIn(e1), FadeIn(e2), run_time=0.25)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in list(d1) + list(d2)], lag_ratio=0.08),
            run_time=0.7,
        )
        self.play(FadeIn(lab), run_time=0.2)
        return pack

    def demo_strong_weak(self):
        def mini(pts, caption, color):
            axes = Axes((0, 7), (0, 7), height=2.35, width=2.55)
            axes.set_stroke(MUTED, 2)
            dots = VGroup(*[Dot(axes.c2p(x, y), fill_color=color).scale(0.95) for x, y in pts])
            slope, intercept = self._lsq(pts)
            line = axes.get_graph(lambda x, m=slope, b=intercept: m * x + b).set_stroke(GOLD, 3)
            lab = T(caption, 18, GOLD, 16).next_to(axes, DOWN, buff=0.12)
            return VGroup(axes, dots, line, lab)

        left = mini(self._pts_tight(), "strong", TEAL)
        right = mini(self._pts_wide(), "weak", PINK)
        row = VGroup(left, right).arrange(RIGHT, buff=0.7).move_to(0.1 * DOWN)
        self.play(ShowCreation(left[0]), ShowCreation(right[0]), run_time=0.3)
        self.sfx("pop", -12)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in list(left[1]) + list(right[1])], lag_ratio=0.06),
            run_time=0.7,
        )
        self.play(ShowCreation(left[2]), ShowCreation(right[2]), FadeIn(left[3]), FadeIn(right[3]), run_time=0.4)
        return row

    def demo_interp_extra(self, kind="in"):
        pts = self._pts_pos()[:10]
        axes = Axes((0, 7), (0, 7), height=3.1, width=3.5)
        axes.set_stroke(MUTED, 2)
        dots = VGroup(*[Dot(axes.c2p(x, y), fill_color=TEAL).scale(1.1) for x, y in pts])
        slope, intercept = self._lsq(pts)
        x0 = min(p[0] for p in pts)
        x1 = max(p[0] for p in pts)
        y = lambda x: slope * x + intercept
        core = Line(axes.c2p(x0, y(x0)), axes.c2p(x1, y(x1))).set_stroke(GOLD, 4)
        extras = []
        if kind == "in":
            mark = Dot(axes.c2p(3.2, y(3.2)), fill_color=TEAL).scale(1.4)
            lab = T("interpolation", 20, TEAL, 20)
        else:
            tail = Line(axes.c2p(x1, y(x1)), axes.c2p(6.6, y(6.6))).set_stroke(RED, 4)
            mark = Dot(axes.c2p(6.4, y(6.4)), fill_color=RED).scale(1.4)
            lab = T("extrapolation", 20, RED, 20)
            extras.append(tail)
        lab.next_to(axes, DOWN, buff=0.18)
        pack = VGroup(axes, dots, core, mark, lab, *extras).move_to(0.1 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), run_time=0.5)
        self.play(ShowCreation(core), run_time=0.3)
        if extras:
            self.play(ShowCreation(extras[0]), run_time=0.28)
        self.play(GrowFromCenter(mark), FadeIn(lab), run_time=0.35)
        self.pop_flash(mark.get_center(), RED if kind == "out" else TEAL, 0.4)
        return pack

    def demo_slope2_fit(self):
        pts = [(1.0, 1.1), (2.0, 3.2), (3.0, 4.8), (4.0, 7.2)]
        axes = Axes((0, 5), (0, 9), height=3.1, width=3.5)
        axes.set_stroke(MUTED, 2)
        dots = VGroup(*[Dot(axes.c2p(x, y), fill_color=TEAL).scale(1.15) for x, y in pts])
        line = axes.get_graph(lambda x: 2 * x - 0.8).set_stroke(GOLD, 4)
        run = Line(axes.c2p(2, 3.2), axes.c2p(3, 3.2)).set_stroke(TEAL, 3)
        rise = Line(axes.c2p(3, 3.2), axes.c2p(3, 5.2)).set_stroke(PINK, 3)
        lab = T("rise 2 for run 1", 20, GOLD, 22).next_to(axes, DOWN, buff=0.18)
        pack = VGroup(axes, dots, line, run, rise, lab).move_to(0.1 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), run_time=0.5)
        self.play(ShowCreation(line), run_time=0.32)
        self.play(ShowCreation(run), ShowCreation(rise), FadeIn(lab), run_time=0.4)
        return pack

    def demo_bad_fit(self):
        pts = self._pts_pos()
        axes = Axes((0, 7), (0, 7), height=3.1, width=3.5)
        axes.set_stroke(MUTED, 2)
        dots = VGroup(*[Dot(axes.c2p(x, y), fill_color=TEAL).scale(1.1) for x, y in pts])
        bad = axes.get_graph(lambda x: 0.35 * x + 4.4).set_stroke(RED, 4)
        lab = T("line floats above the cloud", 18, RED, 32).next_to(axes, DOWN, buff=0.18)
        pack = VGroup(axes, dots, bad, lab).move_to(0.1 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.08), run_time=0.55)
        self.play(ShowCreation(bad), FadeIn(lab), run_time=0.45)
        return pack

    def demo_wrong_scatter(self):
        names = ["Ada", "Ben", "Cam", "Dee"]
        scores = [4.2, 2.1, 5.5, 3.0]
        axes = Axes((0, 5), (0, 7), height=3.0, width=3.4)
        axes.set_stroke(MUTED, 2)
        dots = VGroup()
        labels = VGroup()
        for i, (nm, sc) in enumerate(zip(names, scores), 1):
            d = Dot(axes.c2p(i, sc), fill_color=GREY).scale(1.1)
            dots.add(d)
            labels.add(T(nm, 16, GREY, 8).next_to(d, DOWN, buff=0.08))
        cross = VGroup(
            Line(axes.c2p(0.4, 0.4), axes.c2p(4.6, 6.4)).set_stroke(RED, 4),
            Line(axes.c2p(0.4, 6.4), axes.c2p(4.6, 0.4)).set_stroke(RED, 4),
        )
        lab = T("names are not a numeric x", 18, RED, 30).next_to(axes, DOWN, buff=0.22)
        pack = VGroup(axes, dots, labels, cross, lab).move_to(0.1 * DOWN)
        self.play(ShowCreation(axes), run_time=0.25)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), FadeIn(labels), run_time=0.5)
        self.play(ShowCreation(cross), FadeIn(lab), run_time=0.4)
        return pack

    def demo_two_way(self, beat=""):
        def cell(txt, color=CREAM, fill=None, w=1.85, h=0.68):
            r = RoundedRectangle(w, h, corner_radius=0.08)
            r.set_stroke(MUTED, 2)
            r.set_fill(fill if fill else GREY, 0.18 if fill else 0.04)
            t = T(txt, 20, color, 16)
            if t.get_width() > w * 0.86:
                t.set_width(w * 0.86)
            t.move_to(r)
            return VGroup(r, t)

        soccer = has(beat, "among soccer", "soccer")
        fifteen = has(beat, "15 of 50", "15/50")
        highlight = has(beat, "relative", "12 of 40") and not soccer and not fifteen
        if soccer:
            head = VGroup(cell(" ", MUTED), cell("basketball", GOLD), cell("no bball", GOLD)).arrange(RIGHT, buff=0.08)
            r1 = VGroup(
                cell("soccer", TEAL),
                cell("10", WHITE, TEAL),
                cell("8", WHITE),
            ).arrange(RIGHT, buff=0.08)
            r2 = VGroup(cell("no soccer", TEAL), cell("4", WHITE), cell("18", WHITE)).arrange(RIGHT, buff=0.08)
            note = T("among soccer is not among all", 20, GOLD, 32)
        elif fifteen:
            head = VGroup(cell(" ", MUTED), cell("band", GOLD), cell("no band", GOLD)).arrange(RIGHT, buff=0.08)
            r1 = VGroup(cell("sport", TEAL), cell("15", WHITE, TEAL), cell("10", WHITE)).arrange(RIGHT, buff=0.08)
            r2 = VGroup(cell("no sport", TEAL), cell("12", WHITE), cell("13", WHITE)).arrange(RIGHT, buff=0.08)
            note = T("15 of 50 = 0.3", 22, GOLD, 24)
        else:
            head = VGroup(cell(" ", MUTED), cell("band", GOLD), cell("no band", GOLD)).arrange(RIGHT, buff=0.08)
            r1 = VGroup(
                cell("sport", TEAL),
                cell("12", WHITE, TEAL if highlight else None),
                cell("8", WHITE),
            ).arrange(RIGHT, buff=0.08)
            r2 = VGroup(cell("no sport", TEAL), cell("10", WHITE), cell("10", WHITE)).arrange(RIGHT, buff=0.08)
            if highlight:
                note = T("12 of 40 = 30%", 22, GOLD, 24)
            else:
                note = T("two-way table", 22, GOLD, 20)
        grid = VGroup(head, r1, r2).arrange(DOWN, buff=0.08)
        pack = VGroup(grid, note).arrange(DOWN, buff=0.22).move_to(0.1 * DOWN)
        self.play(LaggedStart(*[FadeIn(row, UP) for row in (head, r1, r2)], lag_ratio=0.16), run_time=0.8)
        self.play(FadeIn(note), run_time=0.25)
        return pack

    def demo_two_boxplots(self, beat=""):
        long_b = has(beat, "longer box", "more spread")
        show_iqr = has(beat, "iqr", "q1", "q3")
        axes = Axes((0, 3), (0, 13), height=3.3, width=4.0)
        axes.set_stroke(MUTED, 2)
        a = (4, 6, 8, 10, 12)
        b = (2, 3, 7, 11, 12) if long_b else (3, 5, 7, 9, 11)

        def box(gx, stats, color):
            lo, q1, med, q3, hi = stats
            whisk = Line(axes.c2p(gx, lo), axes.c2p(gx, hi)).set_stroke(color, 3)
            cap_lo = Line(axes.c2p(gx - 0.18, lo), axes.c2p(gx + 0.18, lo)).set_stroke(color, 3)
            cap_hi = Line(axes.c2p(gx - 0.18, hi), axes.c2p(gx + 0.18, hi)).set_stroke(color, 3)
            h = abs(axes.c2p(gx, q3)[1] - axes.c2p(gx, q1)[1])
            body = Rectangle(width=0.7, height=max(h, 0.08))
            body.set_stroke(color, 3).set_fill(color, 0.16)
            body.move_to(axes.c2p(gx, (q1 + q3) / 2))
            mid = Line(axes.c2p(gx - 0.35, med), axes.c2p(gx + 0.35, med)).set_stroke(GOLD, 4)
            return VGroup(whisk, cap_lo, cap_hi, body, mid)

        ba = box(1.0, a, TEAL)
        bb = box(2.0, b, PINK)
        la = T("A", 20, TEAL, 6).next_to(ba, DOWN, buff=0.12)
        lb = T("B", 20, PINK, 6).next_to(bb, DOWN, buff=0.12)
        if show_iqr:
            cap = T("IQR = Q3 - Q1", 20, GOLD, 22)
        elif long_b:
            cap = T("longer box, more spread", 18, GOLD, 28)
        else:
            cap = T("A median 8, B median 7", 18, GOLD, 28)
        cap.next_to(axes, DOWN, buff=0.28)
        pack = VGroup(axes, ba, bb, la, lb, cap).move_to(0.05 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(FadeIn(ba), FadeIn(bb), FadeIn(la), FadeIn(lb), run_time=0.5)
        self.play(FadeIn(cap), run_time=0.25)
        return pack

    def demo_display_choice(self):
        sc = self._card("scatter", TEAL, 2.2, 1.0)
        tb = self._card("two-way", GOLD, 2.2, 1.0)
        bx = self._card("box plots", PINK, 2.2, 1.0)
        row = VGroup(sc, tb, bx).arrange(RIGHT, buff=0.45).move_to(0.2 * DOWN)
        lab = T("match the picture to the data", 20, GOLD, 32).next_to(row, DOWN, buff=0.3)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in row], lag_ratio=0.18), run_time=0.7)
        self.play(FadeIn(lab), run_time=0.25)
        return VGroup(row, lab)

    # ----- roots on a number line -----

    def anim_roots(self, beat_i, beat):
        m = re.search(r"sqrt\s*(\d+)", caretify(beat).lower())
        if m:
            n = int(m.group(1))
            root = int(round(n ** 0.5))
            if root * root == n:
                return self.demo_root_line(n, root, root)
            lo = int(n ** 0.5)
            return self.demo_root_line(n, lo, lo + 1)
        return self.demo_show_math(beat)

    def demo_root_line(self, n, lo, hi):
        span = max(10, hi + 2)
        line = NumberLine((-1, span), width=6.2).set_stroke(MUTED, 4)
        val = n ** 0.5
        star = Dot(line.n2p(val), fill_color=GOLD).scale(1.35)
        lab = radical_mob(str(n), 22, GOLD)
        lab.next_to(star, UP, buff=0.14)
        extras = []
        if lo == hi:
            cap = T("exactly " + str(lo), 22, GOLD, 18)
            g = VGroup(line, star, lab).move_to(0.45 * UP)
        else:
            d0 = Dot(line.n2p(lo), fill_color=TEAL).scale(1.15)
            d1 = Dot(line.n2p(hi), fill_color=TEAL).scale(1.15)
            l0 = T(str(lo), 18, MUTED, 6).next_to(d0, DOWN, buff=0.1)
            l1 = T(str(hi), 18, MUTED, 6).next_to(d1, DOWN, buff=0.1)
            cap = T("between " + str(lo) + " and " + str(hi), 20, GOLD, 28)
            g = VGroup(line, d0, d1, star, lab, l0, l1).move_to(0.45 * UP)
            extras = [d0, d1, l0, l1]
        cap.next_to(g, DOWN, buff=0.35)
        self.play(ShowCreation(line), run_time=0.35)
        if extras:
            self.play(GrowFromCenter(extras[0]), GrowFromCenter(extras[1]), FadeIn(extras[2]), FadeIn(extras[3]), run_time=0.3)
        self.sfx("sparkle", -10)
        self.play(GrowFromCenter(star), FadeIn(lab), FadeIn(cap), run_time=0.35)
        return VGroup(g, cap)
