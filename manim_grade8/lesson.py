"""Kid-friendly no-voiceover lessons. Unique moving demo per beat — never the same 3-4-5 on loop."""
import os
import re
from pathlib import Path

from manimlib import *

GOLD = "#fbbf24"
TEAL = "#2dd4bf"
BLUE = "#7dd3fc"
CREAM = "#e8eef9"
MUTED = "#94a3b8"
PINK = "#f9a8d4"
GREEN = "#86efac"
RED = "#f87171"
PANEL = "#151b2e"
FONT = "Comic Sans MS"
TITLE_FONT = "Segoe Script"
SOUND_DIR = Path(__file__).resolve().parent / "sounds"
SLOW = 1.7

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


def clean(text) -> str:
    s = str(text)
    s = re.sub(
        r"[⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁻]+",
        lambda m: " to the " + "".join(SUP_MAP.get(c, c) for c in m.group(0)),
        s,
    )
    s = re.sub(r"\^(\{)?(-?[0-9n]+|\w)(\})?", r" to the \2", s)
    for src, dst in PLAIN.items():
        s = s.replace(src, dst)
    return " ".join(s.split())


def wrap(text, width=28):
    words = clean(text).split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if len(trial) > width:
            if cur:
                lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return "\n".join(lines) if lines else clean(text)


def T(text, size=40, color=CREAM, width=26, font=TITLE_FONT):
    raw = str(text)
    body = wrap(raw, width) if "\n" not in raw else clean(raw)
    mob = Text(body, font=font, font_size=size)
    try:
        mob.set_color(color)
    except Exception:
        pass
    return mob


def power_mob(base, exp, base_size=52, exp_size=28, base_color=CREAM, exp_color=GOLD):
    b = Text(str(base), font=FONT, font_size=base_size).set_color(base_color)
    e = Text(str(exp), font=FONT, font_size=exp_size).set_color(exp_color)
    e.next_to(b.get_corner(UR), RIGHT, buff=0.04)
    e.shift(0.08 * UP)
    return VGroup(b, e)


def chip(label, fill=GOLD):
    txt = T(label, 26, fill, 40, font=TITLE_FONT)
    box = RoundedRectangle(
        width=max(txt.get_width() + 0.85, 3.4),
        height=max(txt.get_height() + 0.32, 0.64),
        corner_radius=0.18,
    )
    box.set_fill(fill, 0.22).set_stroke(fill, 3)
    txt.move_to(box)
    return VGroup(box, txt)


def has(text, *needles):
    t = clean(text).lower()
    return any(n.lower() in t for n in needles)


class LessonScene(Scene):
    unit_num = 1
    unit_title = "Grade 8"
    subtitle = "Pre-algebra"
    parts = []

    def construct(self):
        self.body = VGroup()
        parts = list(self.parts)
        if os.environ.get("G8_SMOKE"):
            first = dict(parts[0])
            first["beats"] = list(first.get("beats", []))[:2]
            first["examples"] = list(first.get("examples", []))[:1]
            parts = [first]
        self.build_stage()
        self.build_chrome()
        self.intro()
        for i, part in enumerate(parts, 1):
            self.play_part(i, part)
        self.outro()

    def play(self, *args, **kwargs):
        kwargs["run_time"] = float(kwargs.get("run_time", 1.0)) * SLOW
        return super().play(*args, **kwargs)

    def hold(self, text="", extra=1.0):
        n = len(clean(str(text)).split())
        self.wait(min(8.0, extra + max(3.2, n * 0.6)))

    def magic_in(self, mob, color=GOLD):
        self.sfx("sparkle", -13)
        self.play(GrowFromCenter(mob), run_time=0.7)
        self.play(mob.animate.scale(1.2), run_time=0.32)
        self.play(mob.animate.scale(1 / 1.2), run_time=0.28)
        try:
            self.play(FlashAround(mob, color=color, run_time=0.45))
        except Exception:
            pass

    def pulse(self, mob, amount=1.14):
        self.play(mob.animate.scale(amount), run_time=0.32)
        self.play(mob.animate.scale(1 / amount), run_time=0.28)
        self.play(mob.animate.scale(1.08), run_time=0.22)
        self.play(mob.animate.scale(1 / 1.08), run_time=0.22)

    def sfx(self, name, gain=-9):
        path = SOUND_DIR / f"{name}.wav"
        if path.exists():
            self.add_sound(str(path), gain=gain)

    def pop_flash(self, point, color=GOLD, radius=0.7):
        self.sfx("pop", -12)
        self.play(Flash(point, color=color, flash_radius=radius,
                        line_length=0.25, num_lines=14, run_time=0.4))

    def morph_number(self, mob, nxt_text, size=56, color=GOLD):
        nxt = T(nxt_text, size, color, 16).move_to(mob)
        self.play(Transform(mob, nxt), run_time=0.55)
        self.play(mob.animate.scale(1.18), run_time=0.18)
        self.play(mob.animate.scale(1 / 1.18), run_time=0.18)
        return mob

    def build_stage(self):
        panel = RoundedRectangle(FRAME_WIDTH - 0.35, FRAME_HEIGHT - 1.55, corner_radius=0.22)
        panel.set_fill("#101628", 1).set_stroke("#243049", 2)
        panel.shift(0.08 * DOWN)
        dots = VGroup()
        rng = np.random.default_rng(self.unit_num + 11)
        for _ in range(22):
            d = Dot(radius=0.03)
            d.set_fill([GOLD, TEAL, PINK][int(rng.integers(0, 3))], 0.2)
            d.move_to([rng.uniform(-6.2, 6.2), rng.uniform(-3.1, 2.4), 0])
            dots.add(d)
        self.stage = VGroup(panel, dots)
        self.add(self.stage)

    def build_chrome(self):
        bar = Rectangle(FRAME_WIDTH + 0.4, 0.72)
        bar.set_fill(PANEL, 1).set_stroke(width=0)
        bar.to_edge(UP, buff=0)
        brand = Text("VEELEARN", font=TITLE_FONT, font_size=26).set_color(GOLD)
        brand.to_edge(UL, buff=0.22).shift(0.04 * DOWN)
        unit = Text(f"Grade 8  ·  Unit {self.unit_num}", font=FONT, font_size=20)
        unit.set_color(MUTED).to_edge(UR, buff=0.22).shift(0.04 * DOWN)
        rule = Line(LEFT * (FRAME_WIDTH / 2 - 0.3), RIGHT * (FRAME_WIDTH / 2 - 0.3))
        rule.set_stroke(GOLD, 2.5, opacity=0.7).next_to(bar, DOWN, buff=0)
        self.chrome = VGroup(bar, brand, unit, rule)
        self.add(self.chrome)
        self.pips = self.make_pips(0)
        self.add(self.pips)

    def make_pips(self, active):
        n = max(len(self.parts), 1)
        dots = VGroup()
        for i in range(n):
            d = Dot(radius=0.085 if i + 1 == active else 0.07)
            if i + 1 == active:
                d.set_fill(GOLD, 1)
            elif i + 1 < active:
                d.set_fill(TEAL, 1)
            else:
                d.set_fill(MUTED, 0.35)
            dots.add(d)
        dots.arrange(RIGHT, buff=0.16).to_edge(DOWN, buff=0.2)
        return dots

    def set_pips(self, active):
        new = self.make_pips(active)
        self.remove(self.pips)
        self.add(new)
        self.pips = new

    def clear_body(self, run_time=0.28):
        if len(self.body):
            self.play(FadeOut(self.body, shift=0.18 * DOWN), run_time=run_time)
        self.body = VGroup()

    def keep(self, *mobs):
        group = VGroup(*mobs)
        self.body.add(group)
        return group

    def intro(self):
        self.sfx("whoosh", -8)
        kicker = T("Eighth Grade Math", 28, TEAL, 36, font=TITLE_FONT)
        title = Text(self.unit_title, font=TITLE_FONT, font_size=56).set_color(CREAM)
        if title.get_width() > 12.2:
            title.set_width(12.2)
        under = Line(LEFT * 2.8, RIGHT * 2.8).set_stroke(GOLD, 6)
        sub = T(self.subtitle, 30, MUTED, 36)
        note = T("Read each line. We go slow on purpose.", 26, MUTED, 34)
        stack = VGroup(kicker, title, under, sub, note).arrange(DOWN, buff=0.3)
        stack.move_to(0.1 * UP)
        self.keep(stack)
        self.play(FadeIn(kicker, DOWN), run_time=0.55)
        self.magic_in(title)
        self.play(ShowCreation(under), FadeIn(sub, UP), run_time=0.7)
        self.play(FadeIn(note), run_time=0.5)
        self.pulse(title)
        self.hold(self.unit_title, extra=1.6)

        self.clear_body(0.4)
        head = T("In this lesson", 42, GOLD, 24, font=TITLE_FONT)
        head.to_edge(UP, buff=1.12)
        self.keep(head)
        self.magic_in(head)
        rows = VGroup()
        for i, part in enumerate(self.parts, 1):
            num = Circle(radius=0.26).set_stroke(GOLD, 3).set_fill(GOLD, 0.18)
            ntxt = T(str(i), 22, GOLD, 8).move_to(num)
            label = T(part["title"], 30, CREAM, 32)
            rows.add(VGroup(VGroup(num, ntxt), label).arrange(RIGHT, buff=0.22))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.34)
        self.keep(rows)
        self.sfx("pop", -12)
        self.play(LaggedStart(*[GrowFromCenter(r) for r in rows], lag_ratio=0.18), run_time=2.2)
        self.hold("In this lesson we cover six parts", extra=1.8)

    def outro(self):
        self.set_pips(len(self.parts) + 1)
        self.clear_body()
        self.sfx("success", -7)
        mark = Text("YES!", font=TITLE_FONT, font_size=84).set_color(TEAL)
        done = T("You finished this unit", 44, CREAM, 28, font=TITLE_FONT)
        tip = T("Replay any part. Then try the quizzes.", 30, MUTED, 32)
        stack = VGroup(mark, done, tip).arrange(DOWN, buff=0.36)
        self.keep(stack)
        self.magic_in(mark, TEAL)
        self.play(FadeIn(done, UP), FadeIn(tip, UP), run_time=0.7)
        self.pop_flash(mark.get_center(), TEAL, 1.3)
        self.pulse(mark, 1.18)
        self.hold("You finished this unit", extra=2.2)
        self.play(FadeOut(self.body), FadeOut(self.chrome), FadeOut(self.pips), FadeOut(self.stage), run_time=0.8)

    def play_part(self, index, part):
        self.set_pips(index)
        self.clear_body()
        self.sfx("whoosh", -9)
        badge = chip(f"Part {index} of {len(self.parts)}")
        title = Text(part["title"], font=TITLE_FONT, font_size=52).set_color(CREAM)
        if title.get_width() > 12.2:
            title.set_width(12.2)
        stack = VGroup(badge, title).arrange(DOWN, buff=0.3).move_to(0.15 * UP)
        self.keep(stack)
        self.play(FadeIn(badge, DOWN), run_time=0.5)
        self.magic_in(title)
        self.pulse(title)
        self.hold(part["title"], extra=1.8)

        visual_kind = part.get("visual")
        beats = part.get("beats", [])
        for bi, beat in enumerate(beats):
            self.play_beat(beat, visual_kind, bi)
        examples = part.get("examples", [])[:1]
        if examples:
            self.play_example(examples[0], visual_kind)

    def play_beat(self, beat, visual_kind, index):
        self.clear_body(0.35)
        self.sfx("click", -12)
        cap = T(beat, 40, CREAM, 26)
        if cap.get_height() > 1.7:
            cap.set_height(1.7)
        if cap.get_width() > 12.3:
            cap.set_width(12.3)
        cap.to_edge(UP, buff=0.95)
        self.keep(cap)
        self.magic_in(cap)
        visual = self.animate_visual(visual_kind, index, beat)
        if visual is not None:
            self.keep(visual)
            self.pulse(visual)
        self.hold(beat, extra=1.6)

    def play_example(self, ex, visual_kind):
        self.clear_body(0.35)
        self.sfx("pop", -10)
        head_chip = chip("One example  ·  watch each step", TEAL)
        problem = T(ex["problem"], 42, GOLD, 24, font=TITLE_FONT)
        if problem.get_width() > 12.2:
            problem.set_width(12.2)
        head = VGroup(head_chip, problem).arrange(DOWN, buff=0.28)
        head.to_edge(UP, buff=0.9)
        self.keep(head)
        self.play(FadeIn(head_chip, DOWN), run_time=0.5)
        self.magic_in(problem)
        self.hold(ex["problem"], extra=2.0)

        stack = VGroup()
        self.keep(stack)
        for si, step in enumerate(ex.get("steps", []), 1):
            num = Circle(radius=0.3).set_stroke(GOLD, 3).set_fill(GOLD, 0.2)
            ntxt = T(str(si), 26, GOLD, 6).move_to(num)
            body = T(step, 36, CREAM, 22, font=TITLE_FONT)
            if body.get_width() > 10.2:
                body.set_width(10.2)
            row = VGroup(VGroup(num, ntxt), body).arrange(RIGHT, buff=0.24)
            if len(stack):
                row.next_to(stack, DOWN, buff=0.26, aligned_edge=LEFT)
            else:
                row.next_to(head, DOWN, buff=0.38)
                row.align_to(head, LEFT)
                row.shift(0.15 * RIGHT)
            stack.add(row)
            self.sfx("click", -14)
            self.magic_in(row, TEAL)
            self.hold(step, extra=1.8)

        if len(stack) and stack.get_bottom()[1] < -2.15:
            stack.scale(0.86)
            stack.next_to(head, DOWN, buff=0.28)

        ans_box = RoundedRectangle(width=12.0, height=1.15, corner_radius=0.22)
        ans_box.set_fill("#14532d", 0.62).set_stroke(GREEN, 4)
        ans_txt = T("Answer:  " + clean(ex["answer"]), 36, GREEN, 28, font=TITLE_FONT)
        if ans_txt.get_width() > 11.2:
            ans_txt.set_width(11.2)
        ans_txt.move_to(ans_box)
        ans = VGroup(ans_box, ans_txt).to_edge(DOWN, buff=0.58)
        self.keep(ans)
        self.sfx("ding", -7)
        ans.shift(1.4 * UP)
        self.play(ans.animate.shift(1.4 * DOWN), run_time=0.7, rate_func=rush_from)
        self.pulse(ans, 1.12)
        self.pop_flash(ans.get_center(), GREEN, 1.0)
        self.hold(ex["answer"], extra=2.6)

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
        t = T(txt, 32, CREAM, 12, font=FONT)
        t.move_to(r)
        return VGroup(r, t)

    # ----- exponents: a new multiply / sign / root story each beat -----

    def anim_exponent(self, beat_i, beat):
        if has(beat, "parenthes", "inside the power", "(-3)"):
            return self.demo_signed_square(True)
        if has(beat, "-3 to the 2 = -9", "square 3 first", "then apply the minus"):
            return self.demo_signed_square(False)
        if has(beat, "root", "sqrt", "undoes"):
            return self.demo_root_undo()
        if has(beat, "irrational", "rational"):
            return self.demo_rational_split()
        if has(beat, "power of a power", "multiply exponents", "(2"):
            return self.demo_power_of_power()
        if has(beat, "divide", "subtract exponents"):
            return self.demo_quotient_rule()
        if has(beat, "same base", "add exponents", "product"):
            return self.demo_product_rule()
        if has(beat, "coefficient"):
            return self.demo_coeff_product()
        variants = [self.demo_factor_stack, self.demo_signed_square, self.demo_root_undo,
                    self.demo_power_of_power, self.demo_product_rule]
        fn = variants[beat_i % len(variants)]
        return fn(True) if fn is self.demo_signed_square else fn()

    def demo_factor_stack(self, bases=(2, 4), exp=None):
        base = 4 if exp is None else bases[0]
        cards = VGroup(self._card(str(base), TEAL), self._card("x " + str(base), BLUE),
                       self._card("x " + str(base), PINK))
        cards.arrange(RIGHT, buff=0.2).move_to(0.55 * DOWN)
        prod = T(str(base), 48, GOLD, 10).next_to(cards, DOWN, buff=0.45)
        self.sfx("pop", -12)
        self.play(GrowFromCenter(cards[0]), run_time=0.25)
        self.play(FadeIn(prod, UP), run_time=0.2)
        self.play(FadeIn(cards[1], LEFT), run_time=0.25)
        self.morph_number(prod, str(base * base), 48, GOLD)
        self.play(FadeIn(cards[2], LEFT), run_time=0.25)
        self.sfx("ding", -10)
        self.morph_number(prod, str(base ** 3), 52, GOLD)
        eq = VGroup(power_mob(str(base), "3"), T("= " + str(base ** 3), 32, GOLD, 12)).arrange(RIGHT, buff=0.15)
        eq.next_to(prod, DOWN, buff=0.2)
        self.play(GrowFromCenter(eq), run_time=0.3)
        return VGroup(cards, prod, eq)

    def demo_signed_square(self, parens=True):
        if parens:
            left = self._card("(-3)", BLUE, 1.6)
            right = self._card("(-3)", PINK, 1.6)
            result = T("9", 56, GREEN, 8)
            tag = T("minus is INSIDE", 22, GREEN, 24)
        else:
            left = self._card("-", RED, 0.9)
            right = self._card("3 x 3", TEAL, 1.7)
            result = T("-9", 56, RED, 8)
            tag = T("minus is OUTSIDE", 22, RED, 24)
        pair = VGroup(left, right).arrange(RIGHT, buff=0.9).move_to(0.5 * UP + 0.4 * DOWN)
        self.play(FadeIn(left, LEFT), FadeIn(right, RIGHT), run_time=0.35)
        self.sfx("thud", -10)
        self.play(left.animate.shift(0.45 * RIGHT), right.animate.shift(0.45 * LEFT), run_time=0.3)
        result.move_to(0.85 * DOWN)
        tag.next_to(result, DOWN, buff=0.2)
        self.play(GrowFromCenter(result), FadeIn(tag), run_time=0.4)
        self.pop_flash(result.get_center(), GREEN if parens else RED)
        return VGroup(left, right, result, tag)

    def demo_root_undo(self):
        sq = Square(1.8).set_stroke(GOLD, 4).set_fill(GOLD, 0.1)
        nine = T("9 x 9", 26, CREAM, 12).move_to(sq)
        g = VGroup(sq, nine).move_to(0.2 * LEFT + 0.3 * DOWN)
        self.play(ShowCreation(sq), FadeIn(nine), run_time=0.4)
        arrow = Arrow(g.get_right(), g.get_right() + 2.2 * RIGHT, fill_color=TEAL, buff=0.1)
        out = T("9", 52, TEAL, 8).next_to(arrow, RIGHT, buff=0.2)
        lab = T("sqrt undoes a square", 20, GOLD, 28).next_to(g, DOWN, buff=0.35)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(arrow), GrowFromCenter(out), FadeIn(lab), run_time=0.5)
        return VGroup(g, arrow, out, lab)

    def demo_rational_split(self):
        good = self._card("sqrt 16 = 4", TEAL, 3.2, 1.1)
        bad = self._card("sqrt 2  never ends", PINK, 3.4, 1.1)
        a = T("rational", 20, TEAL, 16)
        b = T("irrational", 20, PINK, 16)
        good.move_to(3 * LEFT + 0.2 * DOWN)
        bad.move_to(3 * RIGHT + 0.2 * DOWN)
        a.next_to(good, DOWN, buff=0.2)
        b.next_to(bad, DOWN, buff=0.2)
        self.play(GrowFromCenter(good), FadeIn(a), run_time=0.35)
        self.play(GrowFromCenter(bad), FadeIn(b), run_time=0.35)
        self.play(good.animate.shift(0.12 * UP), bad.animate.shift(0.12 * UP), run_time=0.2)
        self.play(good.animate.shift(0.12 * DOWN), bad.animate.shift(0.12 * DOWN), run_time=0.2)
        return VGroup(good, bad, a, b)

    def demo_power_of_power(self):
        inner = power_mob("2", "3", 42, 22)
        wrapb = RoundedRectangle(2.4, 1.6, corner_radius=0.14).set_stroke(BLUE, 3)
        wrapb.move_to(inner)
        g = VGroup(wrapb, inner).move_to(2.2 * LEFT + 0.2 * DOWN)
        outer = T("to the 4", 26, GOLD, 16).next_to(g, UR, buff=0.1)
        self.play(GrowFromCenter(g), FadeIn(outer), run_time=0.4)
        arrow = Arrow(g.get_right() + 0.3 * RIGHT, 1.3 * RIGHT, fill_color=GOLD, buff=0.05)
        out = power_mob("2", "12", 48, 24)
        out.move_to(3.1 * RIGHT + 0.15 * DOWN)
        hint = T("3 x 4 = 12", 22, TEAL, 16).next_to(out, DOWN, buff=0.2)
        self.sfx("whoosh", -11)
        self.play(ShowCreation(arrow), run_time=0.25)
        self.play(GrowFromCenter(out), FadeIn(hint), run_time=0.4)
        self.pop_flash(out.get_center())
        return VGroup(g, outer, arrow, out, hint)

    def demo_product_rule(self):
        a = VGroup(power_mob("3", "2"), T("x", 28, MUTED, 4), power_mob("3", "4")).arrange(RIGHT, buff=0.18)
        a.move_to(2.3 * LEFT + 0.2 * DOWN)
        self.play(FadeIn(a, LEFT), run_time=0.35)
        plus = T("2 + 4 = 6", 24, TEAL, 16).next_to(a, DOWN, buff=0.3)
        self.play(Write(plus), run_time=0.35)
        arrow = Arrow(ORIGIN, 1.4 * RIGHT, fill_color=GOLD)
        out = power_mob("3", "6", 48, 24).move_to(3.0 * RIGHT + 0.15 * DOWN)
        self.sfx("ding", -10)
        self.play(ShowCreation(arrow), GrowFromCenter(out), run_time=0.45)
        return VGroup(a, plus, arrow, out)

    def demo_quotient_rule(self):
        a = VGroup(power_mob("5", "7"), T("/", 32, MUTED, 4), power_mob("5", "3")).arrange(RIGHT, buff=0.16)
        a.move_to(2.2 * LEFT + 0.2 * DOWN)
        self.play(FadeIn(a, UP), run_time=0.35)
        minus = T("7 - 3 = 4", 24, PINK, 16).next_to(a, DOWN, buff=0.3)
        self.play(Write(minus), run_time=0.3)
        out = power_mob("5", "4", 48, 24).move_to(3.0 * RIGHT)
        self.play(GrowFromCenter(out), run_time=0.4)
        return VGroup(a, minus, out)

    def demo_coeff_product(self):
        left = T("(2x to the 3)(5x to the 2)", 26, CREAM, 32)
        left.move_to(0.6 * UP)
        self.play(FadeIn(left, DOWN), run_time=0.3)
        nums = T("2 x 5 = 10", 28, TEAL, 20).move_to(1.3 * LEFT + 0.5 * DOWN)
        vars_ = T("x to the 5", 28, GOLD, 16).move_to(2.2 * RIGHT + 0.5 * DOWN)
        self.play(FadeIn(nums, LEFT), FadeIn(vars_, RIGHT), run_time=0.4)
        out = T("10 x to the 5", 36, GREEN, 24).move_to(1.3 * DOWN)
        self.sfx("ding", -10)
        self.play(GrowFromCenter(out), run_time=0.35)
        return VGroup(left, nums, vars_, out)

    # ----- scientific notation / zero & negative exponents -----

    def anim_sci(self, beat_i, beat):
        if has(beat, "0 power", "to the 0", "nonzero"):
            return self.demo_zero_power()
        if has(beat, "do not read", "minus lives", "as -8"):
            return self.demo_not_negative_eight()
        if has(beat, "negative exponent", "reciprocal", "1 /"):
            return self.demo_negative_exp()
        if has(beat, "flip", "1/2"):
            return self.demo_flip_fraction()
        if has(beat, "32,000", "3.2", "scientific", "10 to the"):
            return self.demo_sci_expand(4)
        if has(beat, "left", "tiny", "negative"):
            return self.demo_sci_expand(-3)
        variants = [self.demo_zero_power, self.demo_negative_exp, self.demo_not_negative_eight,
                    self.demo_sci_expand, self.demo_flip_fraction]
        fn = variants[beat_i % 5]
        return fn(4) if fn is self.demo_sci_expand else fn()

    def demo_zero_power(self):
        seven = power_mob("7", "0", 56, 28)
        seven.move_to(2.2 * LEFT)
        self.play(GrowFromCenter(seven), run_time=0.35)
        arrow = Arrow(LEFT * 0.2, RIGHT * 0.9, fill_color=GOLD)
        one = T("1", 64, GREEN, 6).move_to(2.4 * RIGHT)
        why = T("anything (not 0) to the 0 is 1", 20, MUTED, 36).to_edge(DOWN, buff=1.15)
        self.sfx("ding", -9)
        self.play(ShowCreation(arrow), GrowFromCenter(one), FadeIn(why), run_time=0.5)
        self.play(WiggleOutThenIn(one, run_time=0.4, n_wiggles=4))
        return VGroup(seven, arrow, one, why)

    def demo_negative_exp(self):
        src = power_mob("2", "-3", 48, 26)
        src.move_to(3.2 * LEFT)
        self.play(GrowFromCenter(src), run_time=0.3)
        frac = T("1 / 8", 52, GOLD, 12).move_to(2.6 * RIGHT)
        mid = T("flip me", 20, TEAL, 14)
        self.sfx("whoosh", -10)
        self.play(src.animate.scale([-1, 1, 1]), run_time=0.4)
        self.play(FadeIn(frac, LEFT), FadeIn(mid, UP), run_time=0.35)
        self.pop_flash(frac.get_center(), TEAL)
        return VGroup(src, frac, mid)

    def demo_not_negative_eight(self):
        wrong = T("-8", 56, RED, 8).move_to(2.4 * LEFT)
        self.play(GrowFromCenter(wrong), run_time=0.3)
        self.sfx("wrong", -8)
        cross = VGroup(
            Line(wrong.get_corner(UL), wrong.get_corner(DR)),
            Line(wrong.get_corner(UR), wrong.get_corner(DL)),
        ).set_stroke(RED, 6)
        self.play(ShowCreation(cross), run_time=0.3)
        right = T("1 / 8", 52, GREEN, 12).move_to(2.5 * RIGHT)
        lab = T("the minus is in the exponent", 20, GOLD, 32).to_edge(DOWN, buff=1.15)
        self.play(GrowFromCenter(right), FadeIn(lab), run_time=0.4)
        return VGroup(wrong, cross, right, lab)

    def demo_flip_fraction(self):
        a = T("1/2", 48, CREAM, 10).move_to(2.4 * LEFT)
        self.play(FadeIn(a), run_time=0.25)
        self.play(Rotate(a, PI), run_time=0.45)
        b = T("2/1 = 2", 48, GOLD, 14).move_to(2.3 * RIGHT)
        self.sfx("pop", -11)
        self.play(Transform(a.copy(), b), GrowFromCenter(b), run_time=0.4)
        return VGroup(a, b)

    def demo_sci_expand(self, exp=4):
        before = VGroup(T("3.2 x", 32, CREAM, 12), power_mob("10", str(exp), 32, 18)).arrange(RIGHT, buff=0.1)
        before.move_to(1.6 * UP)
        self.play(FadeIn(before, DOWN), run_time=0.3)
        if exp >= 0:
            digits = ["3", "2"] + ["0"] * exp
            digits.insert(1 + exp, "")  # 32000
            shown = T("32" + "0" * max(exp - 1, 0), 48, GOLD, 16)
            zeros = VGroup(*[T("0", 40, TEAL, 4) for _ in range(max(exp, 1))])
            zeros.arrange(RIGHT, buff=0.08).move_to(0.2 * DOWN)
            self.sfx("whoosh", -11)
            self.play(LaggedStart(*[FadeIn(z, UP) for z in zeros], lag_ratio=0.12), run_time=0.6)
            shown.move_to(1.15 * DOWN)
            self.play(GrowFromCenter(shown), run_time=0.3)
            return VGroup(before, zeros, shown)
        tiny = T("0.0032", 48, PINK, 16).move_to(0.2 * DOWN)
        self.play(GrowFromCenter(tiny), run_time=0.4)
        return VGroup(before, tiny)

    # ----- equations: a moving scale, not the same 6x-7 pan -----

    def anim_balance(self, beat_i, beat):
        if has(beat, "no solution", "never", "0 = 1", "0 = 5"):
            return self.demo_no_solution()
        if has(beat, "infinitely", "always", "identity", "0 = 0"):
            return self.demo_identity()
        if has(beat, "distribut", "parenthes"):
            return self.demo_distribute()
        if has(beat, "fraction", "divid"):
            return self.demo_clear_fraction()
        variants = [self.demo_scale, self.demo_distribute, self.demo_both_sides,
                    self.demo_no_solution, self.demo_identity]
        return variants[beat_i % 5]()

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

    def demo_distribute(self):
        before = T("3(x + 4)", 36, CREAM, 16).move_to(2.3 * LEFT)
        self.play(FadeIn(before), run_time=0.25)
        a = T("3x", 32, TEAL, 8).move_to(1.3 * RIGHT + 0.45 * UP)
        b = T("12", 32, GOLD, 8).move_to(1.3 * RIGHT + 0.45 * DOWN)
        self.play(FadeIn(a, LEFT), FadeIn(b, LEFT), run_time=0.35)
        out = T("3x + 12", 36, GREEN, 16).move_to(1.1 * DOWN)
        self.sfx("pop", -11)
        self.play(GrowFromCenter(out), run_time=0.3)
        return VGroup(before, a, b, out)

    def demo_both_sides(self):
        eq = T("6x - 7  =  5x + 7", 32, CREAM, 28).move_to(0.7 * UP)
        self.play(Write(eq), run_time=0.45)
        step = T("subtract 5x from both sides", 22, TEAL, 36).move_to(ORIGIN)
        self.play(FadeIn(step, UP), run_time=0.3)
        out = T("x = 14", 44, GOLD, 12).move_to(1.0 * DOWN)
        self.sfx("ding", -10)
        self.play(GrowFromCenter(out), run_time=0.35)
        self.play(WiggleOutThenIn(out, run_time=0.4, n_wiggles=4))
        return VGroup(eq, step, out)

    def demo_no_solution(self):
        eq = T("x + 1 = x + 4", 32, CREAM, 24).move_to(0.5 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        boom = T("0 = 3", 40, RED, 12)
        self.play(TransformFromCopy(eq, boom), run_time=0.45)
        no = T("no solution", 28, RED, 20).next_to(boom, DOWN, buff=0.3)
        self.sfx("wrong", -9)
        self.play(FadeIn(no), run_time=0.3)
        return VGroup(eq, boom, no)

    def demo_identity(self):
        eq = T("2(x + 1) = 2x + 2", 30, CREAM, 28).move_to(0.5 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        yes = T("0 = 0  always true", 32, GREEN, 28).move_to(0.6 * DOWN)
        self.sfx("success", -10)
        self.play(GrowFromCenter(yes), run_time=0.4)
        return VGroup(eq, yes)

    def demo_clear_fraction(self):
        eq = T("x / 4 + 3 = 7", 32, CREAM, 24).move_to(0.6 * UP)
        self.play(FadeIn(eq), run_time=0.3)
        times = T("x 4 on every term", 22, TEAL, 24)
        self.play(FadeIn(times), run_time=0.25)
        out = T("x = 16", 44, GOLD, 12).move_to(1.0 * DOWN)
        self.play(GrowFromCenter(out), run_time=0.35)
        return VGroup(eq, times, out)

    # ----- slope: different lines each beat -----

    def anim_slope(self, beat_i, beat):
        if has(beat, "horizontal", "slope 0"):
            return self.demo_slope_line(0, "m = 0  flat")
        if has(beat, "vertical", "undefined"):
            return self.demo_vertical()
        if has(beat, "negative", "falls"):
            return self.demo_slope_line(-2, "m = -2  falls")
        if has(beat, "parallel"):
            return self.demo_parallel()
        if has(beat, "perpendicular"):
            return self.demo_perp()
        if has(beat, "y = mx", "intercept", "b ="):
            return self.demo_slope_line(0.5, "y = (1/2)x + 1", intercept=1)
        slopes = [(0.5, "m = 1/2  climb"), (-1, "m = -1  fall"),
                  (0, "m = 0  flat"), (2, "m = 2  steep")]
        m, lab = slopes[beat_i % 4]
        return self.demo_slope_line(m, lab)

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
        if has(beat, "table"):
            return self.demo_table()
        if has(beat, "nonlinear", "x to the 2", "curve"):
            return self.demo_curve()
        if has(beat, "machine", "f(x)", "notation"):
            return self.demo_machine()
        variants = [self.demo_machine, self.demo_table, self.demo_curve, self.demo_vlt]
        return variants[beat_i % 4]()

    def demo_machine(self):
        inn = self._card("x = 3", BLUE, 1.6, 0.75)
        box = self._card("x 2 + 1", GOLD, 2.0, 1.1)
        out = self._card("7", TEAL, 1.3, 0.75)
        row = VGroup(inn, box, out).arrange(RIGHT, buff=0.7).move_to(0.2 * DOWN)
        a1 = Arrow(inn.get_right(), box.get_left(), buff=0.06, fill_color=GOLD)
        a2 = Arrow(box.get_right(), out.get_left(), buff=0.06, fill_color=TEAL)
        self.play(GrowFromCenter(box), run_time=0.3)
        self.sfx("whoosh", -12)
        self.play(FadeIn(inn, RIGHT), ShowCreation(a1), run_time=0.3)
        self.pop_flash(box.get_center(), GOLD, 0.45)
        self.play(ShowCreation(a2), GrowFromCenter(out), run_time=0.35)
        return VGroup(row, a1, a2)

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
        if has(beat, "eliminat", "add", "cancel"):
            return self.demo_eliminate()
        if has(beat, "substitut"):
            return self.demo_substitute()
        pts = [(2, 3), (1, 4), (3, 1), (0, 2)]
        x, y = pts[beat_i % 4]
        return self.demo_cross(x, y)

    def demo_cross(self, x, y):
        axes = Axes((-1, 5), (-1, 6), height=3.2, width=3.6)
        axes.set_stroke(MUTED, 2)
        l1 = axes.get_graph(lambda t: y + (t - x)).set_stroke(BLUE, 5)
        l2 = axes.get_graph(lambda t: y - (t - x)).set_stroke(PINK, 5)
        dot = Dot(axes.c2p(x, y), fill_color=GOLD).scale(1.3)
        lab = T(f"({x}, {y})", 20, GOLD, 12).next_to(dot, UR, buff=0.08)
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
        lab = T("same line  infinitely many", 20, GOLD, 32)
        pack = VGroup(VGroup(axes, l1, l2), lab).arrange(DOWN, buff=0.12).move_to(0.3 * DOWN)
        self.play(ShowCreation(axes), ShowCreation(l1), ShowCreation(l2), FadeIn(lab), run_time=0.85)
        return pack

    def demo_substitute(self):
        a = T("y = x + 1", 28, BLUE, 18).move_to(2.3 * LEFT + 0.5 * UP)
        b = T("2x + y = 10", 28, PINK, 18).move_to(2.3 * LEFT + 0.3 * DOWN)
        self.play(FadeIn(a, LEFT), FadeIn(b, LEFT), run_time=0.35)
        plug = T("2x + (x + 1) = 10", 26, GOLD, 24).move_to(2.4 * RIGHT + 0.4 * UP)
        out = T("(3, 4)", 40, GREEN, 12).move_to(2.4 * RIGHT + 0.7 * DOWN)
        self.sfx("whoosh", -11)
        self.play(FadeIn(plug, RIGHT), run_time=0.3)
        self.play(GrowFromCenter(out), run_time=0.35)
        return VGroup(a, b, plug, out)

    def demo_eliminate(self):
        a = T("x + y = 10", 26, BLUE, 18).move_to(2.2 * LEFT + 0.45 * UP)
        b = T("x - y = 2", 26, PINK, 18).move_to(2.2 * LEFT + 0.35 * DOWN)
        self.play(FadeIn(a), FadeIn(b), run_time=0.3)
        plus = T("ADD  ->  2x = 12", 26, GOLD, 22).move_to(2.3 * RIGHT + 0.35 * UP)
        out = T("x = 6, y = 4", 30, GREEN, 20).move_to(2.3 * RIGHT + 0.7 * DOWN)
        self.sfx("thud", -11)
        self.play(a.animate.shift(0.15 * DOWN), b.animate.shift(0.15 * UP), run_time=0.25)
        self.play(FadeIn(plus), GrowFromCenter(out), run_time=0.4)
        return VGroup(a, b, plus, out)

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
        cycle = [
            lambda: self.demo_right_intro(),
            lambda: self.demo_squares_on_sides(3, 4),
            lambda: self.demo_triangle(5, 12, "5-12-13"),
            lambda: self.demo_triangle(8, 15, "8-15-17"),
            lambda: self.demo_missing_leg(5, 13),
            lambda: self.demo_triangle(6, 8, "6-8-10"),
            lambda: self.demo_distance(),
            lambda: self.demo_ladder(),
        ]
        return cycle[beat_i % len(cycle)]()

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
        variants = [self.demo_cylinder, self.demo_base_area, self.demo_stack_height]
        return variants[beat_i % 3]()

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
        if has(beat, "50"):
            return self.demo_root_line(50, 7, 8)
        if has(beat, "2"):
            return self.demo_root_line(2, 1, 2)
        if has(beat, "10"):
            return self.demo_root_line(10, 3, 4)
        spots = [(50, 7, 8), (2, 1, 2), (10, 3, 4), (8, 2, 3)]
        n, a, b = spots[beat_i % 4]
        return self.demo_root_line(n, a, b)

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
