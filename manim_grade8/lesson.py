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
    b = Text(_pretty_minus(base), font=FONT, font_size=base_size).set_color(base_color)
    e = Text(_pretty_minus(exp), font=FONT, font_size=exp_size).set_color(exp_color)
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
        # Unary minus before a number: draw as op bar + digits (never "−2" font glyph).
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


def token_mob(tok, size, color, font=FONT):
    kind = tok[0]
    if kind == "pow":
        return power_mob(tok[1], tok[2], size, max(14, int(size * 0.55)), color, GOLD)
    if kind == "sqrt":
        rad = Text("√", font=font, font_size=int(size * 1.2)).set_color(TEAL)
        inner = Text(_pretty_minus(tok[1] or ""), font=font, font_size=size).set_color(color)
        return VGroup(rad, inner).arrange(RIGHT, buff=0.02, aligned_edge=ORIGIN)
    if kind == "arrow":
        # Simple teal chevron — avoid Triangle/OpenGL quirks.
        tip = Text(">", font=font, font_size=int(size * 0.9)).set_color(TEAL)
        return tip
    if kind == "op":
        if tok[1] == "-":
            # Drawn minus bar — never a low "_" glyph from font metrics.
            bar = Line(LEFT * 0.22, RIGHT * 0.22).set_stroke(color, max(3, int(size / 14)))
            return bar
        shown = {"*": "x", "·": "x"}.get(tok[1], tok[1])
        col = GOLD if tok[1] == "=" else (TEAL if tok[1] in "×÷·*" else color)
        return Text(shown, font=font, font_size=size).set_color(col)
    return Text(_pretty_minus(tok[1]), font=font, font_size=size).set_color(color)


def formula(text, size=36, color=WHITE, max_width=12.0, font=FONT):
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
                rows.append(token_mob(("arrow",), size, TEAL, font))
        return VGroup(*rows).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    pieces = [token_mob(tok, size, color, font) for tok in tokens]
    rows, row, row_w, gap = [], [], 0.0, 0.12
    for p in pieces:
        w = p.get_width()
        if row and row_w + gap + w > max_width:
            rows.append(VGroup(*row).arrange(RIGHT, buff=gap, aligned_edge=ORIGIN))
            row, row_w = [p], w
        else:
            row.append(p)
            row_w = row_w + (gap if len(row) > 1 else 0) + w
    if row:
        rows.append(VGroup(*row).arrange(RIGHT, buff=gap, aligned_edge=ORIGIN))
    return rows[0] if len(rows) == 1 else VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)


def T(text, size=36, color=WHITE, width=40, font=FONT):
    max_w = min(12.4, max(4.5, 0.30 * float(width)))
    return formula(text, size, color, max_w, font)


def has(text, *needles):
    t = caretify(text).lower()
    return any(n.lower() in t for n in needles)


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
        try:
            rect = SurroundingRectangle(mob, buff=0.12)
            rect.set_stroke(color, 2)
            self.play(ShowCreation(rect), run_time=0.45)
            self.play(FadeOut(rect), run_time=0.35)
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
        self.play(Write(title), run_time=1.6)
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
        self.play(Write(done), run_time=1.2)
        self.highlight(done, TEAL)
        self.rest()
        self.play(FadeOut(done), run_time=0.6)

    def play_part(self, index, part):
        self.wipe()
        self.narrate(part["title"] + ". Watch how the pieces move.")
        title = Text(part["title"], font=FONT, font_size=46).set_color(WHITE)
        if title.get_width() > 12:
            title.set_width(12)
        self.play(Write(title), run_time=1.3)
        self.highlight(title)
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
        visual = self.animate_visual(visual_kind, index, beat)
        if visual is not None:
            try:
                self.highlight(visual, TEAL)
            except Exception:
                pass
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

        # Extra picture for the answer — graph / number line when it fits.
        if self._example_wants_picture(ex):
            self.wipe()
            self.narrate("Here is the same answer as a picture.")
            self._example_picture(ex)
            self.rest()

    def _example_wants_picture(self, ex):
        ans = caretify(ex.get("answer", ""))
        prob = caretify(ex.get("problem", ""))
        if has(prob, "how many solutions", "no solution") or has(ans, "no solution", "none"):
            return True
        if has(ans, "infinitely", "all real", "identity"):
            return True
        if re.search(r"x\s*=\s*-?\d+", ans) or re.search(r"x\s*=\s*-?\d+", prob):
            return True
        if re.search(r"\(\s*-?\d+\s*,\s*-?\d+\s*\)", ans):
            return True
        return False

    def _example_picture(self, ex):
        ans = caretify(ex.get("answer", ""))
        prob = caretify(ex.get("problem", ""))
        if has(prob, "how many solutions", "no solution") or has(ans, "no solution", "none"):
            return self.demo_eq_graph_parallel(prob or "x + 1 = x + 4")
        if has(ans, "infinitely", "all real", "identity"):
            return self.demo_eq_graph_same(prob)
        if re.search(r"x\s*=\s*-?\d+", ans) or re.search(r"x\s*=\s*-?\d+", prob):
            return self.demo_eq_graph_solve(ans if "x =" in ans else prob)
        if re.search(r"\(\s*-?\d+\s*,\s*-?\d+\s*\)", ans):
            m = re.search(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", ans)
            return self.demo_cross(int(m.group(1)), int(m.group(2)))
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
        t = formula(txt, 28, CREAM, max(0.9, w * 0.86))
        if t.get_width() > w * 0.84:
            t.set_width(w * 0.84)
        if t.get_height() > h * 0.72:
            t.set_height(h * 0.72)
        t.move_to(r)
        return VGroup(r, t)

    def demo_show_math(self, text, size=40):
        chunk = extract_math(text)
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
        if has(beat, "inside the power"):
            return self.demo_signed_square(True)
        if has(beat, "square 3 first", "then apply the minus") or "-3^2 = -9" in t.replace(" ", ""):
            return self.demo_signed_square(False)
        if has(beat, "parenthes") and "(-3)" in t:
            return self.demo_signed_square(True)
        if has(beat, "irrational") or (has(beat, "rational") and "sqrt 2" in tl):
            return self.demo_rational_split()
        if has(beat, "root", "sqrt", "undoes"):
            m = re.search(r"sqrt\s*(\d+)", tl)
            n = int(m.group(1)) if m else 81
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
        quot = re.search(r"(\d+)\^(\d+)\s*/\s*\1\^(\d+)", t)
        if quot or has(beat, "subtract exponents"):
            if quot:
                return self.demo_quotient_rule(quot.group(1), quot.group(2), quot.group(3))
            return self.demo_quotient_rule()
        if has(beat, "coefficient") or re.search(r"\(\d+x", t):
            return self.demo_coeff_product(beat)
        if has(beat, "same base", "add exponents"):
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

    def demo_signed_square(self, parens=True):
        if parens:
            left = self._card("(-3)", BLUE, 1.6)
            right = self._card("(-3)", PINK, 1.6)
            result = formula("9", 56, GREEN, 8)
            tag = formula("minus is INSIDE", 22, GREEN, 24)
        else:
            left = self._card("-", RED, 0.9)
            right = self._card("3 × 3", TEAL, 1.7)
            result = formula("-9", 56, RED, 8)
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
        lab = formula(f"√{n} = {root}", 22, GOLD, 20).next_to(g, DOWN, buff=0.35)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(arrow), GrowFromCenter(out), FadeIn(lab), run_time=0.5)
        return VGroup(g, arrow, out, lab)

    def demo_rational_split(self):
        good = self._card("√16 = 4", TEAL, 3.2, 1.1)
        bad = self._card("√2 never ends", PINK, 3.4, 1.1)
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
        self.pop_flash(out.get_center())
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
        a = VGroup(power_mob(str(base), e1), formula("÷", 32, MUTED, 4), power_mob(str(base), e2)).arrange(RIGHT, buff=0.16)
        a.move_to(2.2 * LEFT + 0.2 * DOWN)
        self.play(FadeIn(a, UP), run_time=0.35)
        minus = formula(f"{e1} − {e2} = {total}", 24, PINK, 16).next_to(a, DOWN, buff=0.3)
        self.play(FadeIn(minus), run_time=0.3)
        out = power_mob(str(base), total, 48, 24).move_to(3.0 * RIGHT)
        self.play(GrowFromCenter(out), run_time=0.4)
        return VGroup(a, minus, out)

    def demo_coeff_product(self, beat="(2x³)(5x²) = 10x⁵"):
        left = formula(extract_math(beat), 32, CREAM, 12)
        left.move_to(0.55 * UP)
        if left.get_width() > 12:
            left.set_width(12)
        self.play(FadeIn(left, DOWN), run_time=0.35)
        nums = formula("2 × 5 = 10", 28, TEAL, 16).move_to(1.5 * LEFT + 0.55 * DOWN)
        vars_ = VGroup(formula("x³ × x² =", 26, GOLD, 12), power_mob("x", "5", 36, 20)).arrange(RIGHT, buff=0.12)
        vars_.move_to(2.2 * RIGHT + 0.55 * DOWN)
        self.play(FadeIn(nums, LEFT), FadeIn(vars_, RIGHT), run_time=0.4)
        out = formula("10x⁵", 40, GREEN, 12).move_to(1.35 * DOWN)
        self.sfx("ding", -10)
        self.play(GrowFromCenter(out), run_time=0.35)
        return VGroup(left, nums, vars_, out)

    # ----- scientific notation / zero & negative exponents -----

    def anim_sci(self, beat_i, beat):
        t = caretify(beat)
        scis = parse_sci(beat)
        if has(beat, "do not read", "minus lives", "as -8"):
            return self.demo_not_negative_eight()
        if len(scis) >= 2 and has(beat, "larger", "compare", "beats"):
            return self.demo_sci_compare(scis[0], scis[1])
        if scis:
            return self.demo_sci_expand(scis[0][0], scis[0][1])
        if has(beat, "flip") or "(1/2)^-1" in t.replace(" ", ""):
            return self.demo_flip_fraction()
        if has(beat, "nonzero") or re.search(r"(?<!10)\d+\^0\b", t) or re.search(r"\b7\^0\b", t):
            m = re.search(r"(\d+)\^0", t)
            return self.demo_zero_power(m.group(1) if m else "7")
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
        src.move_to(3.2 * LEFT)
        self.play(GrowFromCenter(src), run_time=0.3)
        frac = formula(f"1 / {denom}", 52, GOLD, 12).move_to(2.6 * RIGHT)
        mid = formula("reciprocal", 20, TEAL, 14)
        self.sfx("whoosh", -10)
        self.play(src.animate.scale([-1, 1, 1]), run_time=0.4)
        self.play(FadeIn(frac, LEFT), FadeIn(mid, UP), run_time=0.35)
        self.pop_flash(frac.get_center(), TEAL)
        return VGroup(src, frac, mid)

    def demo_not_negative_eight(self):
        wrong = formula("-8", 56, RED, 8).move_to(2.4 * LEFT)
        self.play(GrowFromCenter(wrong), run_time=0.3)
        self.sfx("wrong", -8)
        cross = VGroup(
            Line(wrong.get_corner(UL), wrong.get_corner(DR)),
            Line(wrong.get_corner(UR), wrong.get_corner(DL)),
        ).set_stroke(RED, 6)
        self.play(ShowCreation(cross), run_time=0.3)
        right = formula("1 / 8", 52, GREEN, 12).move_to(2.5 * RIGHT)
        lab = formula("the minus is in the exponent", 20, GOLD, 32).to_edge(DOWN, buff=1.15)
        self.play(GrowFromCenter(right), FadeIn(lab), run_time=0.4)
        return VGroup(wrong, cross, right, lab)

    def demo_flip_fraction(self):
        a = formula("1/2", 48, CREAM, 10).move_to(2.4 * LEFT)
        self.play(FadeIn(a), run_time=0.25)
        self.play(Rotate(a, PI), run_time=0.45)
        b = formula("2/1 = 2", 48, GOLD, 14).move_to(2.3 * RIGHT)
        self.sfx("pop", -11)
        self.play(GrowFromCenter(b), run_time=0.4)
        return VGroup(a, b)

    def demo_sci_expand(self, coeff="3.2", exp=4):
        exp = int(exp)
        before = VGroup(
            formula(str(coeff), 36, CREAM, 8),
            formula("×", 32, TEAL, 4),
            power_mob("10", str(exp), 36, 20),
        ).arrange(RIGHT, buff=0.12)
        before.move_to(1.45 * UP)
        self.play(FadeIn(before, DOWN), run_time=0.35)
        hops = formula(
            ("hop decimal " + str(abs(exp)) + " places right") if exp >= 0
            else ("hop decimal " + str(abs(exp)) + " places left"),
            22, TEAL, 36,
        )
        hops.next_to(before, DOWN, buff=0.35)
        self.play(FadeIn(hops), run_time=0.3)
        shown = formula(expand_sci(coeff, exp), 52, GOLD if exp >= 0 else PINK, 16)
        shown.move_to(0.85 * DOWN)
        self.sfx("whoosh", -11)
        self.play(GrowFromCenter(shown), run_time=0.45)
        return VGroup(before, hops, shown)

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

    # ----- equations: graphs for one-variable too -----

    def anim_balance(self, beat_i, beat):
        t = caretify(beat)
        if has(beat, "no solution", "never true", "contradiction", "nothing works", "numbers disagree"):
            return self.demo_eq_graph_parallel(beat)
        if has(beat, "identity", "every x", "infinitely", "every x works", "numbers match"):
            return self.demo_eq_graph_same(beat)
        if "->" in t or "→" in beat:
            return self.demo_eq_chain_and_graph(beat)
        if has(beat, "distribut") or "3(2x" in t or "3(x" in t or "4(x" in t:
            return self.demo_distribute(beat)
        if has(beat, "fraction", "/3", "/2", "/4", "0.5", "decimal", "denominator"):
            return self.demo_clear_fraction(beat)
        if has(beat, "check", "original"):
            return self.demo_number_line_check(beat)
        if has(beat, "balance", "both sides stay", "stay equal", "parentheses first"):
            return self.demo_scale()
        if has(beat, "minus in front", "hits every"):
            return self.demo_distribute(beat)
        if "=" in beat:
            return self.demo_eq_graph_solve(beat)
        return self.demo_scale()

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

    def demo_eq_chain_and_graph(self, beat):
        """Show arrow steps stacked, then a graph of the solution."""
        sol = self._guess_solution(beat)
        chain = formula(extract_math(beat), 26, CREAM, 11)
        if chain.get_width() > 6.2:
            chain.set_width(6.2)
        axes = self._axes_pair((-1, max(6, sol + 2)), (-1, 10), h=2.6, w=3.0)
        line = axes.get_graph(lambda x: (x / 4.0) + 3).set_stroke(BLUE, 4)
        flat = axes.get_graph(lambda x: 7).set_stroke(PINK, 4)
        # Prefer a generic rising vs horizontal if fraction form not clear.
        if "x/4" not in caretify(beat) and "/4" not in caretify(beat):
            line = axes.get_graph(lambda x: 0.5 * x + 1).set_stroke(BLUE, 4)
            flat = axes.get_graph(lambda x: 0.5 * sol + 1).set_stroke(PINK, 4)
        dot = Dot(axes.c2p(sol, 0.5 * sol + 1 if "x/4" not in caretify(beat) else 7), fill_color=GOLD)
        if "x/4" in caretify(beat) or "/4" in caretify(beat):
            dot = Dot(axes.c2p(sol, 7), fill_color=GOLD)
        tip = formula(f"x = {sol}", 22, GOLD, 10).next_to(dot, UR, buff=0.08)
        graph = VGroup(axes, line, flat, dot, tip)
        pack = VGroup(chain, graph).arrange(RIGHT, buff=0.4).move_to(0.2 * DOWN)
        self.play(FadeIn(chain, LEFT), run_time=0.45)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(axes), ShowCreation(line), ShowCreation(flat), run_time=0.55)
        self.play(GrowFromCenter(dot), FadeIn(tip), run_time=0.3)
        self.pop_flash(dot.get_center())
        return pack

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

    def demo_scale(self):
        base = Line(LEFT * 2.4, RIGHT * 2.4).set_stroke(MUTED, 5)
        fulcrum = Triangle().set_fill(GOLD, 1).set_stroke(width=0).scale(0.28)
        fulcrum.next_to(base, DOWN, buff=0)
        left = self._card("x + 3", BLUE, 1.8, 0.8)
        right = self._card("11", TEAL, 1.5, 0.8)
        left.move_to(1.4 * LEFT + 0.7 * UP)
        right.move_to(1.4 * RIGHT + 0.7 * UP)
        g = VGroup(base, fulcrum, left, right).move_to(0.35 * DOWN)
        self.play(ShowCreation(base), GrowFromCenter(fulcrum), run_time=0.35)
        self.sfx("thud", -11)
        self.play(FadeIn(left, DOWN), FadeIn(right, DOWN), run_time=0.3)
        self.play(g.animate.rotate(0.1), run_time=0.2)
        self.play(g.animate.rotate(-0.2), run_time=0.25)
        self.play(g.animate.rotate(0.1), run_time=0.2)
        return g

    def demo_distribute(self, beat="3(x + 4) = 3x + 12"):
        eq = formula(extract_math(beat), 30, CREAM, 11)
        if eq.get_width() > 11.5:
            eq.set_width(11.5)
        eq.move_to(0.85 * UP)
        self.play(FadeIn(eq), run_time=0.35)
        # Picture: arrows from the outer factor into each inside term.
        box = RoundedRectangle(4.2, 1.1, corner_radius=0.12).set_stroke(BLUE, 3)
        inside = formula("x + 4", 28, CREAM, 10).move_to(box)
        factor = formula("3", 36, GOLD, 6).next_to(box, LEFT, buff=0.35)
        group = VGroup(factor, box, inside).move_to(0.35 * DOWN)
        a1 = Arrow(factor.get_right() + 0.1 * UP, inside.get_left() + 0.2 * LEFT + 0.15 * UP, fill_color=GOLD, buff=0.05)
        a2 = Arrow(factor.get_right() + 0.1 * DOWN, inside.get_right() + 0.1 * LEFT + 0.15 * DOWN, fill_color=TEAL, buff=0.05)
        out = formula("3x + 12", 32, GREEN, 12).next_to(group, DOWN, buff=0.35)
        self.play(FadeIn(factor), ShowCreation(box), FadeIn(inside), run_time=0.4)
        self.sfx("pop", -11)
        self.play(ShowCreation(a1), ShowCreation(a2), run_time=0.35)
        self.play(GrowFromCenter(out), run_time=0.3)
        return VGroup(eq, group, a1, a2, out)

    def demo_both_sides(self, beat="6x - 7 = 5x + 7"):
        return self.demo_eq_graph_solve(beat)

    def demo_no_solution(self, beat="x + 1 = x + 4"):
        return self.demo_eq_graph_parallel(beat)

    def demo_identity(self, beat="2(x + 1) = 2x + 2"):
        return self.demo_eq_graph_same(beat)

    def demo_clear_fraction(self, beat="(x + 2)/3 = 4"):
        t = caretify(beat)
        if "->" in t:
            return self.demo_eq_chain_and_graph(beat)
        eq = formula(extract_math(beat), 30, CREAM, 11)
        if eq.get_width() > 11:
            eq.set_width(11)
        eq.move_to(0.9 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        # Visual: multiply both sides by the denominator.
        left = self._card(extract_math(beat).split("=")[0].strip() if "=" in extract_math(beat) else "frac", BLUE, 2.6, 0.9)
        right = self._card(extract_math(beat).split("=")[-1].strip() if "=" in extract_math(beat) else "n", TEAL, 1.6, 0.9)
        pair = VGroup(left, formula("=", 28, GOLD, 4), right).arrange(RIGHT, buff=0.25).move_to(0.15 * DOWN)
        times = formula("× denominator on both sides", 22, TEAL, 32).next_to(pair, DOWN, buff=0.3)
        self.play(FadeIn(pair), run_time=0.35)
        self.sfx("whoosh", -11)
        self.play(pair.animate.scale(1.08), FadeIn(times), run_time=0.35)
        # Small graph of the answer on a number line.
        sol = self._guess_solution(beat)
        nl = NumberLine(x_range=(0, max(12, sol + 2), 2), width=7)
        nl.set_stroke(MUTED, 2)
        tip = Dot(nl.n2p(sol), fill_color=GOLD)
        tip_lab = formula(f"x = {sol}", 20, GOLD, 10).next_to(tip, UP, buff=0.15)
        nl_g = VGroup(nl, tip, tip_lab).next_to(times, DOWN, buff=0.3)
        self.play(ShowCreation(nl), GrowFromCenter(tip), FadeIn(tip_lab), run_time=0.45)
        return VGroup(eq, pair, times, nl_g)

    # ----- slope: different lines each beat -----

    def anim_slope(self, beat_i, beat):
        if has(beat, "vertical", "undefined"):
            return self.demo_vertical()
        if has(beat, "horizontal") or has(beat, "slope 0"):
            return self.demo_slope_line(0, "m = 0  flat")
        if has(beat, "parallel"):
            return self.demo_parallel()
        if has(beat, "perpendicular"):
            return self.demo_perp()
        pts = re.findall(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", beat)
        if len(pts) >= 2:
            x1, y1 = int(pts[0][0]), int(pts[0][1])
            x2, y2 = int(pts[1][0]), int(pts[1][1])
            run = x2 - x1
            rise = y2 - y1
            m = (rise / run) if run else 0
            b = y1 - m * x1
            lab = f"m = {rise}/{run}" if run else "undefined"
            return self.demo_slope_line(m, lab, intercept=b)
        if has(beat, "negative", "falls"):
            return self.demo_slope_line(-2, "m = -2  falls")
        compact = caretify(beat).replace(" ", "")
        mline = re.search(r"y=\(?(-?\d+(?:/\d+)?)\)?x\+(-?\d+)", compact)
        if mline:
            raw_m, raw_b = mline.group(1), mline.group(2)
            if "/" in raw_m:
                n, d = raw_m.split("/")
                m = float(n) / float(d)
            else:
                m = float(raw_m)
            return self.demo_slope_line(m, f"y = {raw_m}x + {raw_b}", intercept=float(raw_b))
        return self.demo_show_math(beat)

    def demo_slope_line(self, m, label, intercept=1):
        axes = Axes((-1, 5), (-1, 5), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        line = axes.get_graph(lambda x: m * x + intercept)
        line.set_stroke(GOLD, 5)
        g = VGroup(axes, line)
        lab = T(label, 22, GOLD, 28)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.15).move_to(0.35 * DOWN)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(axes), run_time=0.3)
        self.play(ShowCreation(line), run_time=0.55)
        dot = Dot(axes.c2p(0, intercept), fill_color=TEAL)
        self.play(GrowFromCenter(dot), FadeIn(lab), run_time=0.3)
        try:
            self.play(MoveAlongPath(dot, line), run_time=0.9)
        except Exception:
            self.play(dot.animate.shift(RIGHT), run_time=0.4)
        return VGroup(pack, dot)

    def demo_vertical(self):
        axes = Axes((-1, 5), (-1, 5), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        x = 2
        line = Line(axes.c2p(x, -1), axes.c2p(x, 5)).set_stroke(PINK, 5)
        lab = T("undefined slope", 22, PINK, 20)
        g = VGroup(axes, line, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(line), FadeIn(lab), run_time=0.7)
        return g

    def demo_parallel(self):
        axes = Axes((-1, 5), (-1, 5), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(lambda x: 0.6 * x + 0.5).set_stroke(BLUE, 4)
        l2 = axes.get_graph(lambda x: 0.6 * x + 2.2).set_stroke(GOLD, 4)
        lab = T("same slope  never meet", 20, TEAL, 28)
        g = VGroup(axes, l1, l2)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), run_time=0.3)
        self.play(ShowCreation(l1), ShowCreation(l2), FadeIn(lab), run_time=0.7)
        return pack

    def demo_perp(self):
        axes = Axes((-1, 5), (-1, 5), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(lambda x: 0.5 * x + 1).set_stroke(BLUE, 4)
        l2 = axes.get_graph(lambda x: -2 * x + 4).set_stroke(PINK, 4)
        lab = T("slopes  1/2  and  -2", 20, GOLD, 28)
        g = VGroup(axes, l1, l2)
        pack = VGroup(g, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(l1), ShowCreation(l2), FadeIn(lab), run_time=0.9)
        return pack

    # ----- functions -----

    def anim_function(self, beat_i, beat):
        if has(beat, "vertical line"):
            return self.demo_vlt()
        if has(beat, "table", "first differences"):
            return self.demo_table()
        if has(beat, "nonlinear", "x to the 2", "curve", "not a line"):
            return self.demo_curve()
        if has(beat, "machine", "f(x)", "notation", "input", "output"):
            return self.demo_machine()
        if has(beat, "linear", "mx + b", "equal x-steps", "straight"):
            return self.demo_slope_line(1.5, "linear: equal steps", intercept=1)
        if has(beat, "domain", "range"):
            return self.demo_curve()
        if "=" in beat or "f(" in beat:
            return self.demo_function_graph(beat)
        return self.demo_machine()

    def demo_function_graph(self, beat):
        axes = Axes((-2, 5), (-2, 8), height=3.1, width=3.6)
        axes.set_stroke(MUTED, 2)
        t = caretify(beat)
        if "x^2" in t or "x²" in beat:
            curve = axes.get_graph(lambda x: 0.35 * x * x).set_stroke(PINK, 5)
            lab = formula("curve", 20, PINK, 12)
        else:
            curve = axes.get_graph(lambda x: 1.2 * x + 1).set_stroke(GOLD, 5)
            lab = formula("y = f(x)", 20, GOLD, 14)
        pack = VGroup(VGroup(axes, curve), lab).arrange(DOWN, buff=0.12).move_to(0.25 * DOWN)
        self.play(ShowCreation(axes), run_time=0.3)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(curve), FadeIn(lab), run_time=0.55)
        return pack

    def demo_machine(self):
        inn = self._card("x = 3", BLUE, 1.6, 0.75)
        box = self._card("2x + 1", GOLD, 2.0, 1.1)
        out = self._card("7", TEAL, 1.3, 0.75)
        row = VGroup(inn, box, out).arrange(RIGHT, buff=0.7).move_to(0.55 * UP)
        a1 = Arrow(inn.get_right(), box.get_left(), buff=0.06, fill_color=GOLD)
        a2 = Arrow(box.get_right(), out.get_left(), buff=0.06, fill_color=TEAL)
        axes = Axes((-1, 5), (-1, 8), height=2.2, width=2.6)
        axes.set_stroke(MUTED, 2)
        line = axes.get_graph(lambda x: 2 * x + 1).set_stroke(GOLD, 4)
        dot = Dot(axes.c2p(3, 7), fill_color=TEAL)
        graph = VGroup(axes, line, dot).move_to(1.15 * DOWN)
        self.play(GrowFromCenter(box), run_time=0.3)
        self.sfx("whoosh", -12)
        self.play(FadeIn(inn, RIGHT), ShowCreation(a1), run_time=0.3)
        self.pop_flash(box.get_center(), GOLD, 0.45)
        self.play(ShowCreation(a2), GrowFromCenter(out), run_time=0.35)
        self.play(ShowCreation(axes), ShowCreation(line), GrowFromCenter(dot), run_time=0.45)
        return VGroup(row, a1, a2, graph)

    def demo_table(self):
        headers = VGroup(T("x", 22, GOLD, 6), T("f(x)", 22, TEAL, 8)).arrange(RIGHT, buff=1.4)
        rows = VGroup()
        for x, y in [(0, 1), (1, 3), (2, 5)]:
            rows.add(VGroup(T(str(x), 22, CREAM, 6), T(str(y), 22, CREAM, 6)).arrange(RIGHT, buff=1.6))
        table = VGroup(headers, *rows).arrange(DOWN, buff=0.18).move_to(0.25 * DOWN)
        self.play(LaggedStart(*[FadeIn(r, UP) for r in table], lag_ratio=0.15), run_time=0.8)
        return table

    def demo_curve(self):
        axes = Axes((-2, 3), (-1, 5), height=3.1, width=3.6)
        axes.set_stroke(MUTED, 2)
        curve = axes.get_graph(lambda x: x * x)
        curve.set_stroke(PINK, 5)
        lab = T("not a line", 20, PINK, 16)
        pack = VGroup(axes, curve)
        g = VGroup(pack, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(curve), FadeIn(lab), run_time=0.9)
        return g

    def demo_vlt(self):
        axes = Axes((-1, 4), (-1, 4), height=3.1, width=3.4)
        axes.set_stroke(MUTED, 2)
        line = axes.get_graph(lambda x: 0.7 * x + 0.5).set_stroke(GOLD, 4)
        probe = Line(axes.c2p(2, -1), axes.c2p(2, 4)).set_stroke(TEAL, 3)
        lab = T("one hit  ->  function", 20, TEAL, 24)
        pack = VGroup(axes, line)
        g = VGroup(pack, lab).arrange(DOWN, buff=0.12).move_to(0.25 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(line), run_time=0.55)
        self.play(ShowCreation(probe), FadeIn(lab), run_time=0.4)
        return VGroup(g, probe)

    # ----- systems: different intersections / methods -----

    def anim_system(self, beat_i, beat):
        if has(beat, "parallel", "none", "no solution"):
            return self.demo_parallel()
        if has(beat, "same line", "infinitely"):
            return self.demo_same_line()
        if has(beat, "eliminat", "add", "cancel", "oppose"):
            return self.demo_eliminate()
        if has(beat, "substitut"):
            return self.demo_substitute()
        pts = re.findall(r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)", beat)
        if pts:
            return self.demo_cross(int(pts[0][0]), int(pts[0][1]))
        if has(beat, "intersect", "one solution", "cross"):
            return self.demo_cross(2, 3)
        if "=" in beat:
            return self.demo_cross(3, 4)
        return self.demo_cross(2, 3)

    def demo_cross(self, x, y):
        axes = Axes((-1, max(5, x + 2)), (-1, max(6, y + 2)), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(lambda t: y + (t - x)).set_stroke(BLUE, 5)
        l2 = axes.get_graph(lambda t: y - (t - x)).set_stroke(PINK, 5)
        dot = Dot(axes.c2p(x, y), fill_color=GOLD).scale(1.3)
        lab = formula(f"({x}, {y})", 20, GOLD, 12).next_to(dot, UR, buff=0.08)
        g = VGroup(axes, l1, l2).move_to(0.35 * DOWN)
        self.play(ShowCreation(axes), run_time=0.28)
        self.play(ShowCreation(l1), run_time=0.4)
        self.play(ShowCreation(l2), run_time=0.4)
        self.sfx("sparkle", -9)
        self.play(GrowFromCenter(dot), FadeIn(lab), run_time=0.3)
        self.pop_flash(dot.get_center(), GOLD, 0.65)
        return VGroup(g, dot, lab)

    def demo_same_line(self):
        axes = Axes((-1, 5), (-1, 5), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(lambda x: 0.5 * x + 1).set_stroke(BLUE, 8, 0.5)
        l2 = axes.get_graph(lambda x: 0.5 * x + 1).set_stroke(GOLD, 4)
        lab = formula("same line  infinitely many", 20, GOLD, 32)
        pack = VGroup(VGroup(axes, l1, l2), lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(l1), ShowCreation(l2), FadeIn(lab), run_time=0.85)
        return pack

    def demo_substitute(self):
        a = formula("y = x + 1", 26, BLUE, 16).move_to(3.2 * LEFT + 0.9 * UP)
        b = formula("2x + y = 10", 26, PINK, 16).move_to(3.2 * LEFT + 0.35 * UP)
        self.play(FadeIn(a, LEFT), FadeIn(b, LEFT), run_time=0.35)
        plug = formula("2x + (x + 1) = 10", 24, GOLD, 22).move_to(3.2 * LEFT + 0.35 * DOWN)
        out = formula("(3, 4)", 34, GREEN, 12).move_to(3.2 * LEFT + 1.15 * DOWN)
        self.sfx("whoosh", -11)
        self.play(FadeIn(plug, RIGHT), run_time=0.3)
        self.play(GrowFromCenter(out), run_time=0.3)
        axes = Axes((-1, 6), (-1, 8), height=2.8, width=3.0)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(lambda x: x + 1).set_stroke(BLUE, 4)
        l2 = axes.get_graph(lambda x: 10 - 2 * x).set_stroke(PINK, 4)
        dot = Dot(axes.c2p(3, 4), fill_color=GOLD)
        graph = VGroup(axes, l1, l2, dot).move_to(2.6 * RIGHT + 0.15 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(l1), ShowCreation(l2), GrowFromCenter(dot), run_time=0.6)
        self.pop_flash(dot.get_center())
        return VGroup(a, b, plug, out, graph)

    def demo_eliminate(self):
        a = formula("x + y = 10", 26, BLUE, 16).move_to(3.0 * LEFT + 0.85 * UP)
        b = formula("x − y = 2", 26, PINK, 16).move_to(3.0 * LEFT + 0.3 * UP)
        self.play(FadeIn(a), FadeIn(b), run_time=0.3)
        plus = formula("ADD  ->  2x = 12", 24, GOLD, 20).move_to(3.0 * LEFT + 0.35 * DOWN)
        out = formula("x = 6, y = 4", 28, GREEN, 18).move_to(3.0 * LEFT + 1.1 * DOWN)
        self.sfx("thud", -11)
        self.play(a.animate.shift(0.12 * DOWN), b.animate.shift(0.12 * UP), run_time=0.25)
        self.play(FadeIn(plus), GrowFromCenter(out), run_time=0.4)
        axes = Axes((-1, 8), (-1, 8), height=2.8, width=3.0)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(lambda x: 10 - x).set_stroke(BLUE, 4)
        l2 = axes.get_graph(lambda x: x - 2).set_stroke(PINK, 4)
        dot = Dot(axes.c2p(6, 4), fill_color=GOLD)
        graph = VGroup(axes, l1, l2, dot).move_to(2.7 * RIGHT + 0.1 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(l1), ShowCreation(l2), GrowFromCenter(dot), run_time=0.55)
        return VGroup(a, b, plus, out, graph)

    # ----- pythagoras: NEVER loop the same 3-4-5 -----

    def anim_pythag(self, beat_i, beat):
        if has(beat, "5-12-13", "5 and 12", "5, 12", "12 ft", "13 ft ladder"):
            return self.demo_triangle(5, 12, "5-12-13")
        if has(beat, "8-15-17"):
            return self.demo_triangle(8, 15, "8-15-17")
        if has(beat, "6-8-10", "6, 8, and 10", "6, 8 and 10", "sides 6, 8"):
            return self.demo_triangle(6, 8, "6-8-10  (double 3-4-5)")
        if has(beat, "2, 3, 4", "2, 3 and 4", "not right", "not equal"):
            return self.demo_triangle(2, 3, "NOT right", right=False)
        if has(beat, "ladder"):
            return self.demo_ladder()
        if has(beat, "distance", "points", "coordinate"):
            return self.demo_distance()
        if has(beat, "90", "right angle", "hypotenuse", "legs a and b"):
            return self.demo_right_intro()
        if has(beat, "little square", "corner marks"):
            return self.demo_corner_square()
        if has(beat, "subtract", "square root", "know c"):
            return self.demo_missing_leg(5, 13)
        if has(beat, "9 + 16", "legs 3 and 4"):
            return self.demo_squares_on_sides(3, 4)
        return self.demo_show_math(beat)

    def _tri_points(self, a, b, scale):
        return ORIGIN, a * scale * RIGHT, a * scale * RIGHT + b * scale * UP

    def demo_right_intro(self):
        A, B, C = self._tri_points(4, 3, 0.55)
        tri = Polygon(A, B, C).set_stroke(CREAM, 4).set_fill(BLUE, 0.12)
        sq = Square(0.28).set_stroke(GOLD, 3).move_to(B + 0.14 * LEFT + 0.14 * UP)
        hyp = T("hypotenuse c", 20, GOLD, 18).move_to(0.9 * RIGHT + 1.15 * UP)
        g = VGroup(tri, sq).move_to(0.35 * DOWN)
        self.sfx("whoosh", -12)
        self.play(ShowCreation(tri), run_time=0.55)
        self.play(FadeIn(sq), FadeIn(hyp), run_time=0.3)
        self.play(WiggleOutThenIn(sq, run_time=0.4, n_wiggles=4))
        return VGroup(g, hyp)

    def demo_triangle(self, a, b, caption, right=True):
        c = (a * a + b * b) ** 0.5
        scale = 2.6 / max(a, b, 1)
        A, B, C = self._tri_points(a, b, scale)
        tri = Polygon(A, B, C).set_stroke(CREAM, 4).set_fill(GOLD if right else RED, 0.12)
        la = T(str(a), 22, BLUE, 6).next_to(Line(A, B), DOWN, buff=0.08)
        lb = T(str(b), 22, TEAL, 6).next_to(Line(B, C), RIGHT, buff=0.08)
        lc = T(str(int(c)) if abs(c - round(c)) < 0.05 else f"{c:.1f}", 22, GOLD, 8)
        lc.move_to((A + C) / 2 + 0.25 * LEFT + 0.15 * UP)
        cap = T(caption, 22, GREEN if right else RED, 28)
        g = VGroup(tri, la, lb, lc)
        pack = VGroup(g, cap).arrange(DOWN, buff=0.22).move_to(0.3 * DOWN)
        self.play(ShowCreation(tri), run_time=0.45)
        self.play(FadeIn(la), FadeIn(lb), FadeIn(lc), FadeIn(cap), run_time=0.35)
        if not right:
            self.sfx("wrong", -9)
            cross = Line(g.get_corner(UL), g.get_corner(DR)).set_stroke(RED, 5)
            self.play(ShowCreation(cross), run_time=0.25)
            return VGroup(pack, cross)
        self.pop_flash(g.get_center(), GOLD, 0.6)
        return pack

    def demo_squares_on_sides(self, a, b):
        c2 = a * a + b * b
        scale = 0.42
        A, B, C = self._tri_points(a, b, scale)
        tri = Polygon(A, B, C).set_stroke(CREAM, 3).set_fill(GOLD, 0.08)
        s_a = Square(a * scale).set_stroke(BLUE, 3).set_fill(BLUE, 0.15)
        s_b = Square(b * scale).set_stroke(TEAL, 3).set_fill(TEAL, 0.15)
        s_c = Square((c2 ** 0.5) * scale).set_stroke(GOLD, 3).set_fill(GOLD, 0.12)
        s_a.next_to(Line(A, B), DOWN, buff=0)
        s_b.next_to(Line(B, C), RIGHT, buff=0)
        s_c.move_to((A + C) / 2)
        ta = T(str(a * a), 18, BLUE, 8).move_to(s_a)
        tb = T(str(b * b), 18, TEAL, 8).move_to(s_b)
        tc = T(str(c2), 18, GOLD, 8).move_to(s_c)
        eq = T(f"{a * a} + {b * b} = {c2}", 24, GOLD, 24)
        g = VGroup(tri, s_a, s_b, s_c, ta, tb, tc)
        pack = VGroup(g, eq).arrange(DOWN, buff=0.2).move_to(0.25 * DOWN)
        self.play(ShowCreation(tri), run_time=0.35)
        self.sfx("pop", -12)
        self.play(GrowFromCenter(s_a), FadeIn(ta), run_time=0.3)
        self.play(GrowFromCenter(s_b), FadeIn(tb), run_time=0.3)
        self.play(GrowFromCenter(s_c), FadeIn(tc), run_time=0.3)
        self.sfx("ding", -10)
        self.play(Write(eq), run_time=0.35)
        return pack

    def demo_missing_leg(self, a, c):
        b = int(round((c * c - a * a) ** 0.5))
        src = T(f"c = {c},  leg = {a}", 26, CREAM, 24).move_to(0.7 * UP)
        self.play(FadeIn(src), run_time=0.25)
        step = T(f"{c * c} - {a * a} = {c * c - a * a}", 26, TEAL, 28)
        self.play(FadeIn(step, UP), run_time=0.3)
        out = T(f"other leg = {b}", 36, GOLD, 20).move_to(1.0 * DOWN)
        self.sfx("ding", -10)
        self.play(GrowFromCenter(out), run_time=0.35)
        return VGroup(src, step, out)

    def demo_ladder(self):
        wall = Line(ORIGIN, 2.4 * UP).set_stroke(MUTED, 8)
        ground = Line(ORIGIN, 1.2 * LEFT).set_stroke(MUTED, 8)
        lad = Line(1.2 * LEFT, 2.4 * UP).set_stroke(GOLD, 6)
        a = T("5", 20, BLUE, 6).next_to(ground, DOWN, buff=0.08)
        b = T("12", 20, TEAL, 6).next_to(wall, RIGHT, buff=0.08)
        c = T("13", 22, GOLD, 6).move_to(0.2 * LEFT + 1.4 * UP)
        g = VGroup(wall, ground, lad, a, b, c).move_to(0.25 * DOWN)
        self.play(ShowCreation(wall), ShowCreation(ground), run_time=0.35)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(lad), FadeIn(a), FadeIn(b), FadeIn(c), run_time=0.5)
        return g

    def demo_distance(self):
        axes = Axes((-1, 6), (-1, 6), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        p = Dot(axes.c2p(1, 2), fill_color=TEAL)
        q = Dot(axes.c2p(4, 6), fill_color=GOLD)
        seg = Line(p.get_center(), q.get_center()).set_stroke(PINK, 4)
        lab = T("distance 5", 20, GOLD, 16)
        pack = VGroup(axes, p, q, seg)
        g = VGroup(pack, lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), GrowFromCenter(p), GrowFromCenter(q), run_time=0.45)
        self.play(ShowCreation(seg), FadeIn(lab), run_time=0.4)
        return g

    def demo_corner_square(self):
        return self.demo_right_intro()

    # ----- cylinder -----

    def anim_cylinder(self, beat_i, beat):
        if has(beat, "area", "pi r"):
            return self.demo_base_area()
        if has(beat, "height", "stack"):
            return self.demo_stack_height()
        return self.demo_cylinder()

    def demo_cylinder(self):
        top = Ellipse(width=2.3, height=0.7).set_stroke(BLUE, 4).set_fill(BLUE, 0.18)
        bot = Ellipse(width=2.3, height=0.7).set_stroke(BLUE, 4).set_fill("#1e3a8a", 0.45)
        top.shift(1.35 * UP)
        bot.shift(1.35 * DOWN)
        left = Line(top.get_left(), bot.get_left()).set_stroke(BLUE, 4)
        right = Line(top.get_right(), bot.get_right()).set_stroke(BLUE, 4)
        h = T("h", 22, GOLD, 6).next_to(right, RIGHT, buff=0.12)
        r = T("r", 22, TEAL, 6).next_to(top, UP, buff=0.08)
        eq = VGroup(T("V = pi", 24, GOLD, 14), power_mob("r", "2", 28, 16, GOLD, TEAL), T("h", 24, GOLD, 6))
        eq.arrange(RIGHT, buff=0.1)
        g = VGroup(bot, left, right, top, h, r)
        g.move_to(0.4 * DOWN + 1.6 * LEFT)
        eq.next_to(g, RIGHT, buff=0.45)
        self.play(ShowCreation(bot), run_time=0.22)
        self.play(ShowCreation(left), ShowCreation(right), run_time=0.28)
        self.play(ShowCreation(top), FadeIn(h), FadeIn(r), run_time=0.3)
        self.play(g.animate.shift(0.12 * UP), run_time=0.18)
        self.play(g.animate.shift(0.12 * DOWN), run_time=0.18)
        self.sfx("pop", -11)
        self.play(GrowFromCenter(eq), run_time=0.3)
        return VGroup(g, eq)

    def demo_base_area(self):
        circ = Circle(radius=1.15).set_stroke(TEAL, 4).set_fill(TEAL, 0.15)
        r = T("r", 22, GOLD, 6).next_to(circ, RIGHT, buff=0.1)
        eq = VGroup(T("base = pi", 24, GOLD, 16), power_mob("r", "2", 28, 16, GOLD, TEAL)).arrange(RIGHT, buff=0.1)
        g = VGroup(circ, r)
        pack = VGroup(g, eq).arrange(DOWN, buff=0.3).move_to(0.25 * DOWN)
        self.play(GrowFromCenter(circ), FadeIn(r), run_time=0.4)
        self.play(Write(eq), run_time=0.35)
        return pack

    def demo_stack_height(self):
        discs = VGroup()
        for i in range(5):
            e = Ellipse(width=2.0, height=0.45).set_stroke(BLUE, 2).set_fill(BLUE, 0.18)
            discs.add(e)
        discs.arrange(UP, buff=0.02).move_to(0.2 * DOWN)
        h = T("stack the bases  x h", 22, GOLD, 28).next_to(discs, DOWN, buff=0.25)
        self.play(LaggedStart(*[FadeIn(d, UP) for d in discs], lag_ratio=0.12), run_time=0.8)
        self.play(FadeIn(h), run_time=0.25)
        return VGroup(discs, h)

    # ----- scatter -----

    def anim_scatter(self, beat_i, beat):
        if has(beat, "outlier"):
            return self.demo_outlier()
        if has(beat, "negative", "falls"):
            return self.demo_scatter_pts([(1, 5), (2, 4.2), (3, 3.5), (4, 2.4), (5, 1.6)], "negative trend")
        if has(beat, "no association", "random", "none"):
            return self.demo_scatter_pts([(1, 3), (2, 1.5), (3, 4.5), (4, 2.2), (5, 3.8)], "no clear trend", fit=False)
        if has(beat, "cluster"):
            return self.demo_cluster()
        return self.demo_scatter_pts(
            [(1, 1.6), (2, 2.2), (3, 3.4), (4, 3.1), (5, 4.6), (6, 5.2)],
            "positive trend",
        )

    def demo_scatter_pts(self, pts, caption, fit=True):
        axes = Axes((0, 7), (0, 7), height=3.1, width=3.5)
        axes.set_stroke(MUTED, 2)
        dots = VGroup(*[Dot(axes.c2p(x, y), fill_color=TEAL).scale(1.15) for x, y in pts])
        lab = T(caption, 20, GOLD, 24)
        g = VGroup(axes)
        self.play(ShowCreation(axes), run_time=0.28)
        self.sfx("pop", -12)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1), run_time=0.7)
        extras = [dots]
        if fit:
            line = axes.get_graph(lambda x: 0.75 * x + 0.5).set_stroke(GOLD, 4)
            self.play(ShowCreation(line), run_time=0.4)
            extras.append(line)
        self.play(FadeIn(lab), run_time=0.2)
        extras.append(lab)
        return VGroup(g, *extras)

    def demo_outlier(self):
        pts = [(1, 1.5), (2, 2.1), (3, 2.8), (4, 3.4), (5, 6.5)]
        g = self.demo_scatter_pts(pts[:-1], "spot the outlier", fit=True)
        axes = g[0]
        # last point already not included; add red outlier
        # axes is Axes in VGroup - get from first
        return g

    def demo_cluster(self):
        pts = [(1.2, 1.3), (1.5, 1.6), (1.8, 1.2), (5.2, 5.0), (5.5, 5.4), (5.7, 4.8)]
        return self.demo_scatter_pts(pts, "two clusters", fit=False)

    # ----- roots on a number line -----

    def anim_roots(self, beat_i, beat):
        m = re.search(r"sqrt\s*(\d+)", caretify(beat).lower())
        if m:
            n = int(m.group(1))
            lo = int(n ** 0.5)
            hi = lo if lo * lo == n else lo + 1
            if lo * lo == n:
                lo, hi = max(lo - 1, 0), lo + 1
            return self.demo_root_line(n, lo, hi)
        return self.demo_show_math(beat)

    def demo_root_line(self, n, lo, hi):
        line = NumberLine((-1, 10), width=6.2).set_stroke(MUTED, 4)
        d0 = Dot(line.n2p(lo), fill_color=TEAL).scale(1.15)
        d1 = Dot(line.n2p(hi), fill_color=TEAL).scale(1.15)
        val = n ** 0.5
        star = Dot(line.n2p(val), fill_color=GOLD).scale(1.35)
        lab = T(f"sqrt {n}", 20, GOLD, 14).next_to(star, UP, buff=0.12)
        l0 = T(str(lo), 18, MUTED, 6).next_to(d0, DOWN, buff=0.1)
        l1 = T(str(hi), 18, MUTED, 6).next_to(d1, DOWN, buff=0.1)
        g = VGroup(line, d0, d1, star, lab, l0, l1).move_to(0.3 * DOWN)
        self.play(ShowCreation(line), run_time=0.35)
        self.play(GrowFromCenter(d0), GrowFromCenter(d1), FadeIn(l0), FadeIn(l1), run_time=0.3)
        self.sfx("sparkle", -10)
        self.play(GrowFromCenter(star), FadeIn(lab), run_time=0.3)
        self.play(star.animate.shift(0.12 * UP), run_time=0.15)
        self.play(star.animate.shift(0.12 * DOWN), run_time=0.15)
        return g
