from manimlib import *


class SmokeCheck(Scene):
    def construct(self):
        title = Text("Veelearn  ·  Grade 8", font="Arial", font_size=48)
        title.set_color("#fbbf24")
        sub = Text("Manim lesson engine is ready", font="Arial", font_size=28)
        sub.set_color("#e2e8f0")
        sub.next_to(title, DOWN, buff=0.45)
        ring = Circle(radius=1.4)
        ring.set_stroke("#2dd4bf", width=6)
        ring.set_fill("#2dd4bf", opacity=0.12)
        ring.next_to(sub, DOWN, buff=0.7)
        self.play(FadeIn(title, DOWN), run_time=0.8)
        self.play(Write(sub), run_time=0.8)
        self.play(ShowCreation(ring), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(VGroup(title, sub, ring)))
