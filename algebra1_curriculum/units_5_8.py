"""Deep Algebra 1 curriculum builders (units 5–8)."""
from __future__ import annotations

from curriculum_kit import (
    lesson_figure, svg_plane, svg_circle, svg_triangle, svg_rect, svg_balance,
    svg_number_line, svg_scatter, svg_parabola,
)
from hs_curriculum import (
    concept_block, solved, practice_slots, unit_shell, page_break, mq,
    xy_graph, sample_curve, number_line,
)
from .common import AUDIENCE, STRETCH_LABEL


def _seg(m, b, x0, x1):
    return [(x0, m * x0 + b), (x1, m * x1 + b)]


def _area_model(tl, tr, bl, br, top="x + 3", left="x + 2"):
    return (
        '<svg viewBox="0 0 280 180" width="100%" style="max-width:280px" role="img">'
        '<rect x="50" y="30" width="110" height="70" fill="#bfdbfe" stroke="#1e3a8a" stroke-width="2"/>'
        '<rect x="160" y="30" width="70" height="70" fill="#ddd6fe" stroke="#5b21b6" stroke-width="2"/>'
        '<rect x="50" y="100" width="110" height="50" fill="#bbf7d0" stroke="#166534" stroke-width="2"/>'
        '<rect x="160" y="100" width="70" height="50" fill="#fde68a" stroke="#92400e" stroke-width="2"/>'
        f'<text x="105" y="72" text-anchor="middle" font-size="13">{tl}</text>'
        f'<text x="195" y="72" text-anchor="middle" font-size="13">{tr}</text>'
        f'<text x="105" y="130" text-anchor="middle" font-size="13">{bl}</text>'
        f'<text x="195" y="130" text-anchor="middle" font-size="13">{br}</text>'
        f'<text x="140" y="20" text-anchor="middle" font-size="12">{top}</text>'
        f'<text x="14" y="90" font-size="12">{left}</text>'
        "</svg>"
    )


# ===========================================================================
# UNIT 5: Exponents & Exponential Intro
# ===========================================================================

def _u5_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("When multiplying powers with the same base, $x^3\\cdot x^5$ equals:", "$x^8$",
         "Product rule: add the exponents, $3+5=8$. The base stays $x$.",
         ["$x^{15}$", "$x^2$", "$8x$"]),
        ("The quotient $a^7\\div a^2$ simplifies to:", "$a^5$",
         "Quotient rule: subtract exponents, $7-2=5$.",
         ["$a^9$", "$a^{14}$", "$a^{7/2}$"]),
        ("Which rule justifies $2^4\\cdot 2^3=2^7$?", "product of powers (add exponents)",
         "Same base, multiplication: add the exponents. You do not add the bases.",
         ["power of a power (multiply exponents)", "quotient of powers", "zero-exponent rule"]),
        ("$b^6\\cdot b$ is equivalent to:", "$b^7$",
         "The second factor is $b^1$, so $6+1=7$.",
         ["$b^6$", "$b^5$", "$6b$"]),
        ("$\\dfrac{5^{10}}{5^{10}}$ equals:", "$1$",
         "Quotient rule gives $5^0$, and a nonzero number to the $0$ power is $1$. Also any nonzero over itself is $1$.",
         ["$0$", "$5$", "$10$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("$(x^3)^4$ simplifies to:", "$x^{12}$",
         "Power of a power: multiply exponents, $3\\cdot 4=12$.",
         ["$x^7$", "$x^{81}$", "$4x^3$"]),
        ("For a nonzero number $c$, $c^0$ equals:", "1",
         "The zero-exponent rule: $c^0=1$ whenever $c\\neq 0$. $0^0$ is left undefined in Algebra 1.",
         ["0", "c", "undefined for every c"]),
        ("$2^{-3}$ is equal to:", "$\\dfrac{1}{8}$",
         "Negative exponent: $2^{-3}=\\dfrac{1}{2^3}=\\dfrac{1}{8}$, not $-8$.",
         ["$-8$", "$8$", "$-\\dfrac{1}{8}$"]),
        ("$(3x)^0$ for $x\\neq 0$ equals:", "1",
         "The entire product $3x$ is the base. Any nonzero quantity to the $0$ power is $1$.",
         ["0", "3", "x"]),
        ("$5^{-2}$ equals:", "$\\dfrac{1}{25}$",
         "$5^{-2}=\\dfrac{1}{5^2}=\\dfrac{1}{25}$.",
         ["$-25$", "$25$", "$-\\dfrac{1}{25}$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("$4500$ in scientific notation is:", "$4.5\\times 10^{3}$",
         "Move the point three places: $4.5$ times $10^3$.",
         ["$4.5\\times 10^{-3}$", "$45\\times 10^{2}$", "$4.5\\times 10^{4}$"]),
        ("$0.0032$ in scientific notation is:", "$3.2\\times 10^{-3}$",
         "The coefficient must be at least $1$ and less than $10$. Three places right means exponent $-3$.",
         ["$3.2\\times 10^{3}$", "$32\\times 10^{-4}$", "$0.32\\times 10^{-2}$"]),
        ("$(3\\times 10^{4})(2\\times 10^{3})$ equals:", "$6\\times 10^{7}$",
         "Multiply coefficients $3\\cdot 2=6$ and add exponents $4+3=7$.",
         ["$5\\times 10^{7}$", "$6\\times 10^{12}$", "$6\\times 10^{1}$"]),
        ("Which is larger, $4.1\\times 10^{3}$ or $3.9\\times 10^{4}$?", "$3.9\\times 10^{4}$",
         "Compare exponents first: $10^4$ beats $10^3$. $39000>4100$.",
         ["$4.1\\times 10^{3}$", "they are equal", "cannot tell without a calculator"]),
        ("Standard form of $6.02\\times 10^{2}$ is:", "602",
         "Move the point two places right: $602$.",
         ["60.2", "0.0602", "6020"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("If $f(x)=2^{x}$, then $f(3)$ equals:", "8",
         "$2^{3}=8$. The graph of $y=2^{x}$ passes through $(3,8)$.",
         ["6", "9", "5"]),
        ("Every exponential $y=a^{x}$ with $a>0$, $a\\neq 1$ passes through:", "$(0,1)$",
         "$a^{0}=1$ for $a\\neq 0$. The $y$-intercept is $1$.",
         ["$(1,0)$", "$(0,0)$", "$(1,1)$"]),
        ("A quantity that doubles every year from $5$ is modeled by:", "$5\\cdot 2^{t}$",
         "Initial $5$, growth factor $2$ each year: $5\\cdot 2^{t}$.",
         ["$5+2t$", "$2^{5t}$", "$5t^{2}$"]),
        ("On $y=2^{x}$, as $x$ increases the $y$-values:", "grow faster and faster",
         "Each step multiplies by $2$, so the rises themselves get larger.",
         ["stay constant", "decrease toward 0", "form a straight line"]),
        ("The value of $3^{x}$ at $x=0$ is:", "1",
         "Any nonzero base to the $0$ power is $1$. That is the intercept of the growth graph.",
         ["0", "3", "undefined"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("If $g(x)=\\left(\\dfrac{1}{2}\\right)^{x}$, then $g(3)$ equals:", "$\\dfrac{1}{8}$",
         "$\\left(\\dfrac{1}{2}\\right)^{3}=\\dfrac{1}{8}$. Decay graphs fall toward $0$ as $x$ grows.",
         ["$8$", "$\\dfrac{3}{2}$", "$-\\dfrac{1}{8}$"]),
        ("A decay factor of $0.8$ each year starting at $100$ is:", "$100(0.8)^{t}$",
         "Multiply by $0.8$ once per year. Subtracting $0.8$ would be linear, not exponential.",
         ["$100-0.8t$", "$100^{0.8t}$", "$0.8t+100$"]),
        ("As $x\\to\\infty$, $\\left(\\dfrac{1}{2}\\right)^{x}$ approaches:", "0",
         "Repeatedly taking half heads toward $0$ but never reaches a negative.",
         ["$\\infty$", "$-1$", "$\\dfrac{1}{2}$"]),
        ("The graph of $y=\\left(\\dfrac{1}{2}\\right)^{x}$ is the graph of $y=2^{x}$:", "reflected over the $y$-axis",
         "$\\left(\\dfrac{1}{2}\\right)^{x}=2^{-x}$, which is $2^{x}$ with $x$ replaced by $-x$.",
         ["reflected over the $x$-axis", "shifted up 1", "a straight line"]),
        ("After two half-lives, a sample of $80$ g has:", "20 g remaining",
         "Each half-life multiplies by $\\dfrac{1}{2}$: $80\\to 40\\to 20$.",
         ["40 g", "10 g", "0 g"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("A table with constant first differences is best modeled as:", "linear",
         "Constant add-on each step is a line. Constant ratio each step is exponential.",
         ["exponential", "a circle", "undefined"]),
        ("A table $1,2,4,8,16$ is:", "exponential with ratio $2$",
         "Each term is twice the previous. A linear model would add a constant, not multiply.",
         ["linear with slope $2$", "quadratic", "arithmetic with difference $2$"]),
        ("At $x=1$, $y=2x$ equals $2$ and $y=2^{x}$ equals $2$. At $x=5$, $2^{x}$ is:", "32, which is larger than $10$",
         "$2(5)=10$ while $2^{5}=32$. Exponential eventually overtakes a line with the same early match.",
         ["10, the same", "5", "25"]),
        ("Which function grows faster for large positive $x$: $y=100x$ or $y=2^{x}$?", "$y=2^{x}$",
         "Exponential growth outruns any line in the long run, even if the line starts steeper.",
         ["$y=100x$", "they stay equal", "neither grows"]),
        ("If each year a population adds $40$ people, the model is:", "linear",
         "A constant amount added is slope. A constant percent would be exponential.",
         ["exponential", "absolute value", "a hyperbola"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("$\\dfrac{x^{9}}{x^{3}}$ equals:", "$x^{6}$",
         "Subtract exponents: $9-3=6$.",
         ["$x^{12}$", "$x^{3}$", "$x^{27}$"]),
        ("$(2^{3})^{2}$ equals:", "64",
         "Power of a power: $2^{6}=64$. Or $(8)^{2}=64$.",
         ["32", "12", "16"]),
        ("$10^{-2}$ in decimal form is:", "0.01",
         "$\\dfrac{1}{100}=0.01$.",
         ["-100", "100", "0.1"]),
        ("$3.1\\times 10^{-1}$ equals:", "0.31",
         "One place left from $3.1$.",
         ["31", "3.1", "0.031"]),
        ("$f(x)=3^{x}$ at $x=2$ is:", "9",
         "$3^{2}=9$.",
         ["6", "8", "5"]),
        ("A decay graph $y=(0.5)^{x}$ at $x=0$ is at height:", "1",
         "$(0.5)^{0}=1$.",
         ["0.5", "0", "2"]),
        ("$\\dfrac{2^{5}}{2^{-1}}$ equals:", "$2^{6}$",
         "Subtract: $5-(-1)=6$.",
         ["$2^{4}$", "$2^{-6}$", "$2^{5}$"]),
        ("Which expression is not equal to $16$?", "$2^{-4}$",
         "$2^{4}=16$, $4^{2}=16$, $16^{1}=16$, but $2^{-4}=\\dfrac{1}{16}$.",
         ["$2^{4}$", "$4^{2}$", "$16^{1}$"]),
        ("$(5\\times 10^{2})\\div(2\\times 10^{-1})$ equals:", "$2.5\\times 10^{3}$",
         "Coefficients $5/2=2.5$; exponents $2-(-1)=3$.",
         ["$2.5\\times 10^{1}$", "$10\\times 10^{3}$", "$2.5\\times 10^{-3}$"]),
        ("The $y$-intercept of $y=4\\cdot 2^{x}$ is:", "4",
         "$4\\cdot 2^{0}=4\\cdot 1=4$.",
         ["2", "0", "8"]),
        ("Linear $y=3x$ versus exponential $y=3^{x}$ at $x=0$:", "the exponential is $1$, the line is $0$",
         "$3^{0}=1$ while $3(0)=0$. They do not share the origin.",
         ["both $0$", "both $1$", "both $3$"]),
        ("$x^{4}\\cdot x^{-4}$ for $x\\neq 0$ equals:", "1",
         "Add exponents: $4+(-4)=0$, so $x^{0}=1$.",
         ["0", "$x^{8}$", "$x^{-16}$"]),
        ("A culture triples each hour from $2$ cells. After $4$ hours:", "162",
         "$2\\cdot 3^{4}=2\\cdot 81=162$.",
         ["24", "81", "8"]),
        ("Which table is linear? Inputs $0,1,2,3$ with outputs:", "$5,8,11,14$",
         "Common difference $+3$. The list $3,6,12,24$ is exponential (ratio $2$).",
         ["$3,6,12,24$", "$1,4,9,16$", "$2,4,8,16$"]),
        ("$\\left(\\dfrac{2}{3}\\right)^{-1}$ equals:", "$\\dfrac{3}{2}$",
         "A negative exponent takes the reciprocal: $\\dfrac{3}{2}$.",
         ["$-\\dfrac{2}{3}$", "$\\dfrac{2}{3}$", "$-\\dfrac{3}{2}$"]),
        ("Moving from $y=2^{x}$ to $y=2^{x}-1$ shifts the graph:", "down $1$",
         "Subtracting $1$ outside is a vertical shift down. The intercept becomes $0$.",
         ["left $1$", "right $1$", "up $1$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("SAT Stretch: Simplify $\\dfrac{(2^{3})^{4}\\cdot 2^{-5}}{2^{2}}$.", "$2^{5}$",
         "Numerator: $2^{12}\\cdot 2^{-5}=2^{7}$. Then $2^{7}/2^{2}=2^{5}$.",
         ["$2^{7}$", "$2^{9}$", "$2^{-1}$"]),
        ("SAT Stretch: $(4.0\\times 10^{-3})\\div(8.0\\times 10^{2})$ equals:", "$5.0\\times 10^{-6}$",
         "Coefficients $4/8=0.5$, rewrite $0.5\\times 10^{-5}=5.0\\times 10^{-6}$. Exponents $-3-2=-5$, then adjust.",
         ["$5.0\\times 10^{-5}$", "$2.0\\times 10^{-1}$", "$5.0\\times 10^{6}$"]),
        ("SAT Stretch: A bank balance is $B(t)=800(1.05)^{t}$. The factor $1.05$ means:",
         "the balance is multiplied by $1.05$ each year (5% growth)",
         "Exponential $a(1+r)^{t}$ uses growth factor $1+r$. Here $r=0.05$. Adding $1.05$ each year would be linear.",
         ["add $\\$1.05$ each year", "the interest is $105\\%$ per year", "the balance halves every year"]),
        ("SAT Stretch: Compare $f(x)=2x+16$ and $g(x)=2^{x}$ at $x=6$. Which is larger, and by how much?",
         "$g$ is larger by $36$",
         "$f(6)=12+16=28$ and $g(6)=64$. The exponential is larger by $64-28=36$.",
         ["$g$ is larger by $4$", "$f$ is larger by $36$", "they are equal"]),
        ("SAT Stretch: A medicine decays by $50\\%$ every $4$ hours from $64$ mg. Amount after $12$ hours:",
         "8 mg",
         "Twelve hours is three half-lives: $64\\to 32\\to 16\\to 8$.",
         ["16 mg", "32 mg", "4 mg"]),
        ("SAT Stretch: Which expression equals $\\left(\\dfrac{x^{3}}{x^{-2}}\\right)^{2}$ for $x\\neq 0$?", "$x^{10}$",
         "Inside: $x^{3-(-2)}=x^{5}$. Then $(x^{5})^{2}=x^{10}$.",
         ["$x^{6}$", "$x^{2}$", "$x^{-2}$"]),
        ("SAT Stretch: $y=5(0.5)^{x}$ and $y=5-0.5x$ agree at $x=0$. At $x=4$ the exponential value is:",
         "0.3125",
         "$5(0.5)^{4}=5\\cdot\\dfrac{1}{16}=\\dfrac{5}{16}=0.3125$. The line is $5-2=3$, much larger.",
         ["3", "2.5", "1"]),
        ("SAT Stretch: Scientific comparison: $7.2\\times 10^{5}$ is how many times $1.8\\times 10^{3}$?", "400",
         "$\\dfrac{7.2}{1.8}\\times 10^{5-3}=4\\times 10^{2}=400$.",
         ["4", "40", "0.4"]),
        ("SAT Stretch: First simplify $\\dfrac{(3^{2})^{3}\\cdot 3^{-4}}{3}$. A culture $C(t)=5\\cdot 3^{t}$ and a linear "
         "count $L(t)=15t+5$ are then compared at $t$ equal to that simplified exponent. Which is larger, and by how much?",
         "$C$ is larger by $85$",
         "Power of a power: $(3^{2})^{3}=3^{6}$. Product: $3^{6}\\cdot 3^{-4}=3^{2}$. Quotient: $3^{2}/3=3^{1}$, so $t=3$. "
         "Then $C(3)=5\\cdot 27=135$ and $L(3)=45+5=50$. The exponential is larger by $135-50=85$.",
         ["$L$ is larger by $85$", "$C$ is larger by $50$", "they are equal at $t=3$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    return qs


def build_unit5():
    title = "Algebra 1 Unit 5: Exponents & Exponential Intro"
    description = (
        "Product, quotient, and power rules, zero and negative exponents, scientific notation, exponential "
        "growth and decay graphs, and comparing linear versus exponential change."
    )
    concepts = [
        "Product and quotient rules",
        "Power rules and zero/negative",
        "Scientific notation",
        "Exponential growth graphs",
        "Exponential decay graphs",
        "Compare linear vs exponential",
    ]

    c1 = concept_block(
        "1. Product and quotient rules",
        [
            "A power $a^{n}$ means $n$ factors of the base $a$ when $n$ is a positive integer. Exponential notation "
            "is a compression of repeated multiplication, not a new operation from nowhere.",
            "The product rule: $a^{m}\\cdot a^{n}=a^{m+n}$ when the bases match. You add the counts of factors, you "
            "do not add the bases and you do not multiply the exponents.",
            "The quotient rule: $\\dfrac{a^{m}}{a^{n}}=a^{m-n}$ for $a\\neq 0$. Subtracting exponents is removing "
            "$n$ factors from the numerator.",
            "If the bases differ, these rules do not apply: $2^{3}\\cdot 3^{2}$ is $8\\cdot 9=72$, not $6^{5}$. "
            "Only identical bases combine this way.",
            "A bare $x$ is $x^{1}$. That is why $x^{4}\\cdot x=x^{5}$. Forgetting the invisible $1$ is the usual "
            "product-rule miss.",
            "These two rules are the algebra behind scientific notation products and quotients later in this unit, "
            "and behind exponential growth factors $a\\cdot a\\cdot a$.",
        ],
        "Polynomial multiplication in Unit 6 still uses $x^{m}x^{n}=x^{m+n}$ on every pair of variable factors. If "
        "the product rule is shaky, factoring later feels like a foreign language.",
        "Same base? Add on a product, subtract on a quotient. Different bases? Compute or leave as a product. Write "
        "the invisible exponent $1$ before you add.",
        lesson_figure(
            svg_rect("2^3", "2^2"),
            "An area of $2^{3}\\times 2^{2}$ unit squares",
            "Eight by four is thirty-two, which is $2^{5}$. Adding exponents $3+2=5$ matches the area count.",
        )
        + solved(1, "Simplify $x^{4}\\cdot x^{7}$.",
                 ["Write the invisible exponents: $x^{4}\\cdot x^{7}=x^{4+7}$.",
                  "Add: $4+7=11$.",
                  "The product is $x^{11}$.",
                  "Check with a small base: $2^{4}\\cdot 2^{7}=16\\cdot 128=2048=2^{11}$."],
                 "$x^{11}$", "", "Easy")
        + solved(2, "Simplify $\\dfrac{y^{9}}{y^{3}}$.",
                 ["Same base $y\\neq 0$, so subtract exponents: $9-3=6$.",
                  "The quotient is $y^{6}$.",
                  "Think of cancelling three $y$ factors from nine, leaving six.",
                  "Check: $y^{6}\\cdot y^{3}=y^{9}$, which returns the original numerator."],
                 "$y^{6}$", "", "Medium")
        + solved(3, "Simplify $\\dfrac{a^{5}\\cdot a^{2}}{a^{4}}$.",
                 ["Numerator first, product rule: $a^{5}\\cdot a^{2}=a^{7}$.",
                  "Now divide: $\\dfrac{a^{7}}{a^{4}}=a^{7-4}=a^{3}$ for $a\\neq 0$.",
                  "All at once: $5+2-4=3$.",
                  "Check: $a^{3}\\cdot a^{4}=a^{7}=a^{5}\\cdot a^{2}$."],
                 "$a^{3}$", "", "Hard"),
        ("Multiplying the exponents on a product of the same base",
         "$x^{2}\\cdot x^{5}$ is $x^{7}$, not $x^{10}$. Multiply exponents only for $(x^{2})^{5}$."),
        ("Write every factor with an exponent",
         "Replace $x$ with $x^{1}$ and $x^{3}x^{3}$ with two visible threes before you add. Hidden $1$s are how "
         "counts go missing."),
        [
            "I can add exponents on a product of like bases.",
            "I can subtract exponents on a quotient of like bases.",
            "I can treat a bare variable as exponent $1$.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Power rules and zero/negative",
        [
            "A power of a power multiplies exponents: $(a^{m})^{n}=a^{mn}$. Raising a product to a power distributes: "
            "$(ab)^{n}=a^{n}b^{n}$. A quotient works the same: $\\left(\\dfrac{a}{b}\\right)^{n}=\\dfrac{a^{n}}{b^{n}}$.",
            "The zero exponent: $a^{0}=1$ for $a\\neq 0$. One reason: $\\dfrac{a^{n}}{a^{n}}=a^{0}$ and also equals $1$. "
            "$0^{0}$ is not defined in this course.",
            "A negative exponent means a reciprocal, not a negative number: $a^{-n}=\\dfrac{1}{a^{n}}$ for $a\\neq 0$. "
            "So $2^{-3}=\\dfrac{1}{8}$, not $-8$ and not $-\\dfrac{1}{8}$.",
            "You can move a factor across a fraction bar by changing the sign of its exponent: "
            "$\\dfrac{1}{x^{-2}}=x^{2}$. That is the same reciprocal idea.",
            "The sign of the exponent and the sign of the value are different jobs. $(-2)^{4}=16$ while $-2^{4}=-16$ "
            "and $2^{-4}=\\dfrac{1}{16}$. Parentheses decide the base.",
            "Together with lesson 1, you can now simplify mixed monomials such as $\\dfrac{(2x^{3})^{2}}{x^{-1}}$.",
        ],
        "Scientific notation is almost entirely zero, negative, and product/quotient rules applied to $10$. Growth "
        "and decay graphs use $a^{x}$ for non-integer $x$ later; the integer laws you learn here still govern the "
        "lattice points on those graphs.",
        "Apply power-of-a-power first (multiply), then product/quotient (add/subtract), then rewrite negatives as "
        "fractions. Keep the base in parentheses until the exponent is simplified.",
        lesson_figure(
            number_line(-4, 4, closed=[(-3, "2^{-3}=1/8"), (0, "2^0=1"), (3, "2^3=8")]),
            "Integer powers of $2$ as a story, not as $x$-coordinates of $2$",
            "Negative exponents are small positive values, not left-side negatives of $2$. The output $2^{n}$ is always positive.",
        )
        + solved(4, "Simplify $(x^{2})^{5}$.",
                 ["Multiply exponents: $2\\cdot 5=10$.",
                  "$x^{10}$."],
                 "$x^{10}$", "", "Easy")
        + solved(5, "Rewrite $3^{-4}$ as a positive-exponent fraction.",
                 ["$3^{-4}=\\dfrac{1}{3^{4}}=\\dfrac{1}{81}$."],
                 "$\\dfrac{1}{81}$", "", "Medium")
        + solved(6, "Simplify $\\left(\\dfrac{2x^{-1}}{y^{2}}\\right)^{3}$.",
                 ["Cube each factor: $\\dfrac{8 x^{-3}}{y^{6}}$.",
                  "Rewrite $x^{-3}$ as $\\dfrac{1}{x^{3}}$: $\\dfrac{8}{x^{3}y^{6}}$."],
                 "$\\dfrac{8}{x^{3}y^{6}}$", "", "SAT"),
        ("Reading $a^{-n}$ as $-a^{n}$",
         "The minus in the exponent is an instruction to take a reciprocal. The value $2^{-3}$ is positive $\\dfrac{1}{8}$."),
        ("Parentheses around a negative base",
         "$(-3)^{2}=9$ includes the minus in the base. $-3^{2}=-9$ squares $3$ first. Write the parentheses if the "
         "minus belongs to the base."),
        [
            "I can multiply exponents for a power of a power.",
            "I know $a^{0}=1$ for $a\\neq 0$.",
            "I can rewrite negative exponents as reciprocals.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Scientific notation",
        [
            "Scientific notation writes a number as $c\\times 10^{k}$ where $1\\leq |c|<10$ and $k$ is an integer. "
            "It is built for very large and very small measurements.",
            "To convert from standard form, move the decimal until the coefficient is in $[1,10)$ and count the "
            "moves: rightward moves make $k$ negative; leftward moves make $k$ positive.",
            "Products: multiply the coefficients and add the exponents of $10$. Then adjust if the new coefficient "
            "is not yet in $[1,10)$. Example: $(4\\times 10^{5})(6\\times 10^{2})=24\\times 10^{7}=2.4\\times 10^{8}$.",
            "Quotients: divide coefficients and subtract exponents. Adjust the coefficient the same way.",
            "Comparing two scientific numbers: look at the exponents of $10$ first. The larger exponent wins unless "
            "the coefficients and signs complicate a negative case.",
            "On a calculator, $3.2\\text{E}4$ means $3.2\\times 10^{4}$. Knowing the laws lets you estimate without "
            "the device and catch a dropped sign on $k$.",
        ],
        "Science classes report masses, wavelengths, and populations in this form. The exponent laws of lessons 1–2 "
        "are exactly the arithmetic of those reports.",
        "Write each factor as $c\\times 10^{k}$. Multiply/divide the $c$’s; add/subtract the $k$’s. Then slide the "
        "decimal so $c$ is between $1$ and $10$ and fix $k$.",
        lesson_figure(
            svg_number_line(-4, 4, marks=[(-3, "10^{-3}"), (0, "1"), (3, "10^{3}")]),
            "Powers of ten on a log-style number line of exponents",
            "Each integer step in the exponent is a factor of $10$ in the actual size. $10^{3}=1000$ and $10^{-3}=0.001$.",
        )
        + solved(7, "Write $72000$ in scientific notation.",
                 ["$7.2$ with the point moved $4$ places: $7.2\\times 10^{4}$."],
                 "$7.2\\times 10^{4}$", "", "Easy")
        + solved(8, "Write $0.00056$ in scientific notation.",
                 ["$5.6$ with four moves right: $5.6\\times 10^{-4}$."],
                 "$5.6\\times 10^{-4}$", "", "Medium")
        + solved(9, "Compute $\\dfrac{6.0\\times 10^{5}}{2.0\\times 10^{-2}}$.",
                 ["Coefficients $6/2=3$. Exponents $5-(-2)=7$.",
                  "$3.0\\times 10^{7}$."],
                 "$3.0\\times 10^{7}$", "", "Hard"),
        ("Leaving the coefficient outside $[1,10)$",
         "$23\\times 10^{4}$ is not yet scientific notation. Rewrite as $2.3\\times 10^{5}$."),
        ("Count the hops, then check magnitude",
         "After converting, ask: is this thousands, millionths, …? A wrong sign on $k$ is usually an off-by-a-world "
         "error you can catch by size."),
        [
            "I can convert to and from scientific notation.",
            "I can multiply and divide scientific numbers.",
            "I can compare two numbers by their powers of ten.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Exponential growth graphs",
        [
            "An exponential growth model has the form $y=a\\cdot b^{x}$ with $a>0$ and $b>1$. The graph is an "
            "increasing curve, not a line. It passes through $(0,a)$ because $b^{0}=1$.",
            "The parent $y=2^{x}$ goes through $(0,1)$, $(1,2)$, $(2,4)$, $(3,8)$. Each step to the right multiplies "
            "$y$ by $2$. The rises themselves get larger: $1$, then $2$, then $4$.",
            "Domain of $y=b^{x}$ for $b>0$ is all reals (in Algebra 1 you mainly plot integer $x$, then sketch a "
            "smooth curve). Range is $y>0$ when $a>0$. The $x$-axis is a horizontal asymptote.",
            "A discrete growth story — “doubles every year” — is $a\\cdot 2^{t}$ at whole-number $t$. Connecting the "
            "dots is a model, not a claim that the quantity is defined at $t=1.37$ unless the context allows it.",
            "Vertical stretches $y=a\\cdot 2^{x}$ change the intercept to $a$ but keep the same multiplicative "
            "pattern. Horizontal shifts $y=2^{x-h}$ slide the curve, equivalent to a different intercept.",
            "Reading a growth graph: look for the intercept, then check one doubling step to confirm the base.",
        ],
        "Populations, compound interest, and later logarithms all sit on this curve family. Distinguishing it from "
        "a steep line is the point of lesson 6.",
        "Plot $(0,a)$ and two more points by multiplying by $b$ each time $x$ increases by $1$. Sketch a smooth "
        "increasing curve that never crosses the $x$-axis.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: 2 ** x, -2, 4))],
                points=[(0, 1, "(0,1)"), (1, 2, "(1,2)"), (3, 8, "(3,8)")],
                xlim=(-2, 4), ylim=(-1, 10),
            ),
            "Growth curve $y=2^{x}$",
            "Lattice points $(0,1)$, $(1,2)$, $(2,4)$, $(3,8)$ sit on a curve that steepens as $x$ increases.",
        )
        + solved(10, "List $f(x)=2^{x}$ for $x=0,1,2,3$.",
                 ["$1,2,4,8$."],
                 "$1,2,4,8$", "", "Easy")
        + solved(11, "A population $P(t)=50\\cdot 2^{t}$ starts at what size, and what is $P(3)$?",
                 ["$P(0)=50$.",
                  "$P(3)=50\\cdot 8=400$."],
                 "starts at $50$; $P(3)=400$", "", "Medium")
        + solved(12, "Why does $y=2^{x}$ never meet the $x$-axis?",
                 ["$2^{x}$ is always positive.",
                  "As $x\\to-\\infty$, $2^{x}\\to 0$ but never reaches $0$. The $x$-axis is an asymptote."],
                 "horizontal asymptote $y=0$", "", "SAT"),
        ("Plotting $(1,0)$ as if it were a line intercept",
         "Exponential $a^{x}$ hits $(0,1)$, not $(1,0)$. The point $(1,0)$ would be an $x$-intercept, which this "
         "family does not have when $a>0$."),
        ("Multiply, do not add, to find the next point",
         "From $(2,4)$ on $y=2^{x}$, the next integer point is $(3,8)$, not $(3,6)$. Adding the slope of a chord "
         "is a linear habit."),
        [
            "I can plot $y=b^{x}$ from a table of integer inputs.",
            "I can read the intercept $(0,a)$.",
            "I can describe the $x$-axis as an asymptote.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Exponential decay graphs",
        [
            "Exponential decay has $y=a\\cdot b^{x}$ with $a>0$ and $0<b<1$. Each step multiplies by a fraction, so "
            "the graph falls toward the $x$-axis from the intercept $(0,a)$.",
            "The parent $y=\\left(\\dfrac{1}{2}\\right)^{x}=2^{-x}$ goes through $(0,1)$, $(1,0.5)$, $(2,0.25)$. It "
            "is the growth curve $2^{x}$ reflected across the $y$-axis.",
            "Half-life language: if a quantity halves every $h$ years, $y=a\\left(\\dfrac{1}{2}\\right)^{t/h}$. In "
            "Algebra 1 you often take $h=1$ in the chosen time unit so the base is simply $\\dfrac{1}{2}$.",
            "Decay never goes negative in these models. A line with negative slope will cross the axis; a decay "
            "exponential will not (for $a>0$).",
            "Percent decay uses $b=1-r$. Losing $20\\%$ per year is multiplying by $0.80$, not subtracting $0.20$ "
            "from the formula each year as a linear term.",
            "Reading a decay graph: intercept first, then one multiplicative step down, then the long-run approach "
            "to $0$.",
        ],
        "Medicine, cooling (as a first model), and depreciation stories are decay. Mixing them up with a line that "
        "hits zero in finite time gives a wrong “gone by Tuesday” prediction.",
        "Plot $(0,a)$, multiply by $b$ as $x$ increases by $1$, and sketch a falling curve that flattens toward "
        "$y=0$ from above.",
        lesson_figure(
            xy_graph(
                curves=[("#dc2626", sample_curve(lambda x: 0.5 ** x, -1, 5))],
                points=[(0, 1, "(0,1)"), (1, 0.5, "(1,1/2)"), (2, 0.25, "(2,1/4)")],
                xlim=(-1, 5), ylim=(-0.2, 2.2),
            ),
            "Decay curve $y=\\left(\\dfrac{1}{2}\\right)^{x}$",
            "Each step to the right halves the height. The curve approaches the $x$-axis but does not cross it.",
        )
        + solved(13, "Compute $\\left(\\dfrac{1}{2}\\right)^{4}$.",
                 ["$\\left(\\dfrac{1}{2}\\right)^{4}$ means four factors of $\\dfrac{1}{2}$.",
                  "$\\dfrac{1}{2}\\cdot\\dfrac{1}{2}=\\dfrac{1}{4}$, then $\\dfrac{1}{4}\\cdot\\dfrac{1}{2}=\\dfrac{1}{8}$.",
                  "One more factor: $\\dfrac{1}{8}\\cdot\\dfrac{1}{2}=\\dfrac{1}{16}$.",
                  "Same as $2^{-4}=\\dfrac{1}{16}$."],
                 "$\\dfrac{1}{16}$", "", "Easy")
        + solved(14, "A $200$ mg dose halves every hour. How much remains after $3$ hours?",
                 ["Each hour multiplies by $\\dfrac{1}{2}$, so three hours is three factors.",
                  "Model: $200\\cdot\\left(\\dfrac{1}{2}\\right)^{3}$.",
                  "$\\left(\\dfrac{1}{2}\\right)^{3}=\\dfrac{1}{8}$, then $200\\cdot\\dfrac{1}{8}=25$.",
                  "Check the chain: $200\\to 100\\to 50\\to 25$ mg."],
                 "$25$ mg", "", "Medium")
        + solved(15, "A sample starts at $80$ g and is multiplied by $0.9$ each year. Write $m(t)$.",
                 ["Start $a=80$. The yearly factor is $b=0.9$ (keep nine-tenths of what remains).",
                  "Exponential form: $m(t)=80(0.9)^{t}$.",
                  "After $1$ year: $80\\cdot 0.9=72$ g, not $80-10=70$.",
                  "The curve stays positive and approaches $0$, matching the decay graph in this lesson."],
                 "$80(0.9)^{t}$", "", "Hard"),
        ("Subtracting the percent instead of multiplying",
         "$20\\%$ decay is $\\times 0.8$, not $y=a-0.20t$ unless the context truly loses a constant amount."),
        ("Keep the curve toward the axis, not through it",
         "If your decay graph crosses $y=0$, you drew a line. Exponential decay with $a>0$ stays positive."),
        [
            "I can evaluate $b^{x}$ for $0<b<1$.",
            "I can write a half-life or percent-decay model.",
            "I can describe the asymptote $y=0$.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Compare linear vs exponential",
        [
            "A linear model adds a constant amount each equal time step (common difference). An exponential model "
            "multiplies by a constant each equal time step (common ratio).",
            "Tables tell the difference quickly: look at first differences versus ratios. $4,7,10,13$ is linear "
            "(difference $3$). $4,8,16,32$ is exponential (ratio $2$).",
            "Graphs: a line has constant slope. An exponential growth curve starts flatter or steeper depending on "
            "parameters, then steepens; a decay curve flattens toward $0$.",
            "A line can overtake an exponential for a while (a large slope versus a small base), but growth "
            "exponential $b^{x}$ with $b>1$ eventually exceeds any given line as $x$ grows.",
            "Stories: “gains $30$ per week” is linear. “grows $30\\%$ per week” is exponential. The words amount "
            "versus percent are the tell.",
            "Choosing a model is Unit 8’s job in more generality. Here you only need to pick line versus exponential "
            "from a table, graph, or sentence.",
        ],
        "Misclassifying a percent-growth story as a line is how people underestimate long-run change. That warning "
        "is the Algebra 1 version of choosing a model carefully.",
        "Ask: add or multiply each step? Constant difference $\\to$ line. Constant ratio $\\to$ exponential. Then "
        "write $y=mx+b$ or $y=ab^{x}$ accordingly.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#64748b", _seg(2, 0, -1, 4)),
                    ("#4f46e5", sample_curve(lambda x: 2 ** x, -1, 4)),
                ],
                points=[(1, 2, "both 2 at x=1"), (3, 8, "2^3=8")],
                xlim=(-1, 4), ylim=(-1, 10),
            ),
            "Gray line $y=2x$ versus purple curve $y=2^{x}$",
            "They meet at $(1,2)$, but the exponential pulls away for larger $x$.",
        )
        + solved(16, "Classify the table $x=0,1,2,3$ with $y=5,9,13,17$.",
                 ["First differences $4,4,4$. Linear, slope $4$, intercept $5$: $y=4x+5$."],
                 "linear $y=4x+5$", "", "Easy")
        + solved(17, "Classify $y=3,6,12,24$ for $x=0,1,2,3$.",
                 ["Ratios $2,2,2$. Exponential $y=3\\cdot 2^{x}$."],
                 "exponential $3\\cdot 2^{x}$", "", "Medium")
        + solved(18, "A plan pays $\\$20$ plus $\\$4$ per week. Another doubles from $\\$5$. Which is larger after $6$ weeks?",
                 ["Linear: $20+4\\cdot 6=44$.",
                  "Exponential: $5\\cdot 2^{6}=5\\cdot 64=320$.",
                  "The doubling plan is larger after $6$ weeks."],
                 "doubling plan, $\\$320$ vs $\\$44$", "", "SAT"),
        ("Calling any increasing curve linear",
         "Increasing is not the test. Constant slope is the test for a line. Exponential growth increases with "
         "changing slope."),
        ("Differences and ratios on the table",
         "Write a differences row and a ratios row. One of those rows will be nearly constant if a simple Algebra 1 "
         "model fits."),
        [
            "I can tell common difference from common ratio.",
            "I can match a story to $mx+b$ or $ab^{x}$.",
            "I can compare a line and an exponential at a given $x$.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u5_questions()


# ===========================================================================
# UNIT 6: Polynomials & Factoring
# ===========================================================================

def _u6_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("$(3x^{2}+5x)-(x^{2}-2x)$ equals:", "$2x^{2}+7x$",
         "Distribute the minus: $3x^{2}+5x-x^{2}+2x=2x^{2}+7x$.",
         ["$2x^{2}+3x$", "$4x^{2}+7x$", "$2x^{2}+5x-2x$"]),
        ("The sum $(4x-1)+(2x+9)$ is:", "$6x+8$",
         "Add like terms: $4x+2x=6x$ and $-1+9=8$.",
         ["$6x+10$", "$8x-10$", "$2x+8$"]),
        ("Degree of $7x^{3}-x+4$ is:", "3",
         "Degree is the highest power with a nonzero coefficient.",
         ["1", "4", "7"]),
        ("$5x^{2}+3x^{2}$ combines to:", "$8x^{2}$",
         "Like terms: add coefficients, keep $x^{2}$.",
         ["$8x^{4}$", "$15x^{2}$", "$8x$"]),
        ("$(2x^{2}-x+6)+(-2x^{2}+4x)$ equals:", "$3x+6$",
         "The $x^{2}$ terms cancel. $-x+4x=3x$, constant $6$.",
         ["$6x+6$", "$3x$", "$8$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("$3x(2x-5)$ expands to:", "$6x^{2}-15x$",
         "Distribute: $6x^{2}-15x$.",
         ["$6x-15$", "$6x^{2}-5$", "$5x^{2}-15x$"]),
        ("$(x+4)(x+2)$ equals:", "$x^{2}+6x+8$",
         "FOIL: $x^{2}+2x+4x+8=x^{2}+6x+8$.",
         ["$x^{2}+8$", "$x^{2}+6x$", "$x^{2}+8x+8$"]),
        ("$(x+3)(x-3)$ is:", "$x^{2}-9$",
         "Difference of squares: $x^{2}-3^{2}$. The middle terms cancel.",
         ["$x^{2}-6x-9$", "$x^{2}+9$", "$x^{2}-6$"]),
        ("$(2x+1)(x+5)$ expands to:", "$2x^{2}+11x+5$",
         "$2x^{2}+10x+x+5=2x^{2}+11x+5$.",
         ["$2x^{2}+5$", "$2x^{2}+10x+5$", "$2x^{2}+11x+1$"]),
        ("$x(x+2)(x+3)$ first grouping $(x^{2}+2x)(x+3)$ equals:", "$x^{3}+5x^{2}+6x$",
         "$x^{2}(x+3)+2x(x+3)=x^{3}+3x^{2}+2x^{2}+6x=x^{3}+5x^{2}+6x$.",
         ["$x^{3}+6x$", "$x^{3}+5x+6$", "$x^{2}+5x+6$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The GCF of $12x^{3}$ and $18x$ is:", "$6x$",
         "GCF of $12$ and $18$ is $6$; smallest power of $x$ is $x^{1}$.",
         ["$12x$", "$6x^{3}$", "$36x^{3}$"]),
        ("Factor $8x+12$ by pulling out the GCF:", "$4(2x+3)$",
         "GCF is $4$. Check by distributing.",
         ["$8(x+12)$", "$2(4x+6)$", "$4(2x+12)$"]),
        ("Factor $x^{3}+2x^{2}+3x+6$ by grouping:", "$(x^{2}+3)(x+2)$",
         "$x^{2}(x+2)+3(x+2)=(x^{2}+3)(x+2)$.",
         ["$(x^{3}+3)(x+2)$", "$(x^{2}+2)(x+3)$", "$x(x^{2}+2x+3)+6$"]),
        ("The GCF of $15x^{2}y$ and $10xy^{2}$ is:", "$5xy$",
         "GCF of $15$ and $10$ is $5$; take $x^{1}$ and $y^{1}$.",
         ["$150x^{2}y^{2}$", "$5x^{2}y^{2}$", "$xy$"]),
        ("Factor $6x^{2}-9x$ completely (GCF only at this step):", "$3x(2x-3)$",
         "GCF $3x$. The leftover $2x-3$ has no common factor.",
         ["$6x(x-9)$", "$3(2x^{2}-3x)$", "$x(6x-9)$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Factor $x^{2}+5x+6$.", "$(x+2)(x+3)$",
         "Numbers that multiply to $6$ and add to $5$: $2$ and $3$.",
         ["$(x+1)(x+6)$", "$(x-2)(x-3)$", "$(x+6)(x-1)$"]),
        ("Factor $x^{2}-7x+10$.", "$(x-2)(x-5)$",
         "Multiply to $+10$, add to $-7$: $-2$ and $-5$.",
         ["$(x+2)(x+5)$", "$(x-10)(x-1)$", "$(x+2)(x-5)$"]),
        ("Factor $x^{2}+x-12$.", "$(x+4)(x-3)$",
         "Multiply to $-12$, add to $+1$: $4$ and $-3$.",
         ["$(x+6)(x-2)$", "$(x-4)(x+3)$", "$(x+12)(x-1)$"]),
        ("Which pair of numbers works for $x^{2}+9x+14$?", "$2$ and $7$",
         "$2\\cdot 7=14$ and $2+7=9$.",
         ["$1$ and $14$", "$-2$ and $-7$", "$4$ and $5$"]),
        ("$x^{2}-9x+18$ factors as:", "$(x-3)(x-6)$",
         "$-3$ and $-6$ multiply to $18$ and add to $-9$.",
         ["$(x+3)(x+6)$", "$(x-2)(x-9)$", "$(x-18)(x-1)$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Factor $2x^{2}+7x+3$.", "$(2x+1)(x+3)$",
         "Check: $2x^{2}+6x+x+3=2x^{2}+7x+3$.",
         ["$(2x+3)(x+1)$", "$(2x+7)(x+3)$", "$(x+1)(x+3)$"]),
        ("$4x^{2}-9$ is:", "$(2x-3)(2x+3)$",
         "Difference of squares: $(2x)^{2}-3^{2}$.",
         ["$(4x-9)(x+1)$", "$(2x-9)(2x+1)$", "$(4x-3)^{2}$"]),
        ("$(x+5)^{2}$ expands to:", "$x^{2}+10x+25$",
         "Square of a binomial: $x^{2}+2\\cdot x\\cdot 5+25$.",
         ["$x^{2}+25$", "$x^{2}+5x+25$", "$x^{2}+10x+10$"]),
        ("Factor $3x^{2}-11x-4$.", "$(3x+1)(x-4)$",
         "$3x^{2}-12x+x-4=3x^{2}-11x-4$.",
         ["$(3x-1)(x+4)$", "$(3x-4)(x+1)$", "$(x-4)(x+3)$"]),
        ("$x^{2}-16$ factors as:", "$(x-4)(x+4)$",
         "Difference of squares with $4^{2}=16$.",
         ["$(x-8)^{2}$", "$(x-16)(x+1)$", "$(x-4)^{2}$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Factor $2x^{2}-8$ completely.", "$2(x-2)(x+2)$",
         "GCF $2$ first: $2(x^{2}-4)$, then difference of squares.",
         ["$2(x^{2}-8)$", "$(2x-8)(x+1)$", "$2(x-4)(x+1)$"]),
        ("Factor $x^{3}-4x$ completely.", "$x(x-2)(x+2)$",
         "GCF $x$: $x(x^{2}-4)$, then $x(x-2)(x+2)$.",
         ["$x(x^{2}-4x)$", "$(x-4)(x^{2})$", "$x(x-4)$"]),
        ("$3x^{2}+6x+3$ factors completely as:", "$3(x+1)^{2}$",
         "GCF $3$: $3(x^{2}+2x+1)=3(x+1)^{2}$.",
         ["$(3x+1)(x+3)$", "$3(x^{2}+2x+1)$ only, unfactored", "$(x+1)(3x+3)$"]),
        ("A polynomial is factored completely when:", "it is a product of polynomials that cannot be factored further over the integers",
         "Always take GCF first, then binomial/trinomial patterns, then stop at primes over the integers.",
         ["the degree is 1", "all coefficients are 1", "there are no plus signs"]),
        ("Factor $4x^{2}+12x+8$ completely.", "$4(x+1)(x+2)$",
         "GCF $4$: $4(x^{2}+3x+2)=4(x+1)(x+2)$.",
         ["$(2x+2)(2x+4)$", "$4(x^{2}+3x+2)$", "$(4x+8)(x+1)$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("$(5x^{2}-x+2)-(3x^{2}+4x-1)$ equals:", "$2x^{2}-5x+3$",
         "$5x^{2}-x+2-3x^{2}-4x+1=2x^{2}-5x+3$.",
         ["$2x^{2}+3x+1$", "$8x^{2}+3x+1$", "$2x^{2}-5x+1$"]),
        ("The product $(x-1)(x-1)$ is:", "$x^{2}-2x+1$",
         "A square: $(x-1)^{2}$.",
         ["$x^{2}-1$", "$x^{2}+1$", "$x^{2}-x+1$"]),
        ("GCF of $9x^{4}$ and $6x^{2}$ is:", "$3x^{2}$",
         "GCF of $9$ and $6$ is $3$; lowest power $x^{2}$.",
         ["$9x^{2}$", "$3x^{4}$", "$54x^{6}$"]),
        ("$x^{2}+8x+15$ factors as:", "$(x+3)(x+5)$",
         "$3$ and $5$ multiply to $15$ and add to $8$.",
         ["$(x+1)(x+15)$", "$(x-3)(x-5)$", "$(x+8)(x+7)$"]),
        ("Expanding $(3x-2)^{2}$ gives:", "$9x^{2}-12x+4$",
         "$9x^{2}-2\\cdot 3x\\cdot 2+4=9x^{2}-12x+4$.",
         ["$9x^{2}+4$", "$9x^{2}-4$", "$9x^{2}-6x+4$"]),
        ("Factor $x^{2}-x-20$.", "$(x-5)(x+4)$",
         "$-5$ and $4$ multiply to $-20$ and add to $-1$.",
         ["$(x-4)(x+5)$", "$(x-10)(x+2)$", "$(x+5)(x+4)$"]),
        ("$5(x-2)+x(x-2)$ factors by grouping as:", "$(x-2)(5+x)$",
         "Common binomial $(x-2)$.",
         ["$5x(x-2)$", "$(5+x)(x+2)$", "$x^{2}+3x-10$ unfactored"]),
        ("$(2x-1)(2x+1)$ equals:", "$4x^{2}-1$",
         "Difference of squares.",
         ["$4x^{2}+1$", "$4x^{2}-2$", "$2x^{2}-1$"]),
        ("Add $x^{2}+4x$ and $x^{2}-4x+3$.", "$2x^{2}+3$",
         "$x^{2}$ terms: $2x^{2}$. The $4x$ and $-4x$ cancel. Constant $3$.",
         ["$2x^{2}+8x+3$", "$3$", "$2x^{2}+4x+3$"]),
        ("Factor $x^{2}+6x+9$.", "$(x+3)^{2}$",
         "Perfect square trinomial.",
         ["$(x+9)(x+1)$", "$(x+3)(x+6)$", "$(x-3)^{2}$"]),
        ("$6x^{2}+11x+3$ factors as:", "$(3x+1)(2x+3)$",
         "Check: $6x^{2}+9x+2x+3=6x^{2}+11x+3$.",
         ["$(6x+1)(x+3)$", "$(3x+3)(2x+1)$", "$(6x+3)(x+1)$"]),
        ("Completely factor $18x^{2}-8$.", "$2(3x-2)(3x+2)$",
         "GCF $2$: $2(9x^{2}-4)=2(3x-2)(3x+2)$.",
         ["$2(9x^{2}-4)$", "$(18x-8)$", "$8(x^{2}-1)$"]),
        ("The missing middle term in $(x+4)(x+\\_\\_)=x^{2}+9x+20$ is:", "5",
         "$4+5=9$ and $4\\cdot 5=20$.",
         ["9", "20", "4"]),
        ("$(x+y)^{2}$ is not equal to:", "$x^{2}+y^{2}$",
         "The middle $2xy$ is required. $x^{2}+2xy+y^{2}$ is the square.",
         ["$x^{2}+2xy+y^{2}$", "$(x+y)(x+y)$", "$x(x+y)+y(x+y)$"]),
        ("Factor $x^{3}+5x^{2}-x-5$ by grouping.", "$(x^{2}-1)(x+5)$",
         "$x^{2}(x+5)-1(x+5)=(x^{2}-1)(x+5)$, then further $(x-1)(x+1)(x+5)$ if asked completely. "
         "The grouping binomial is $(x^{2}-1)(x+5)$.",
         ["$(x^{3}-5)(x+1)$", "$(x+5)(x^{2}+1)$", "$(x^{2}+5)(x-1)$"]),
        ("Subtract $2x-7$ from $5x+1$.", "$3x+8$",
         "$(5x+1)-(2x-7)=5x+1-2x+7=3x+8$.",
         ["$3x-6$", "$7x-6$", "$3x-8$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("SAT Stretch: Factor $6x^{3}-15x^{2}-9x$ completely.", "$3x(2x+1)(x-3)$",
         "GCF $3x$: $3x(2x^{2}-5x-3)$. Then $2x^{2}-5x-3=(2x+1)(x-3)$ because $2x^{2}-6x+x-3$.",
         ["$3x(2x-3)(x+1)$", "$3x(2x^{2}-5x-3)$", "$x(6x-9)(x+1)$"]),
        ("SAT Stretch: For $2x^{2}+kx-21$ to have $(x-3)$ as a factor, $k$ equals:", "1",
         "If $x-3$ is a factor, $x=3$ is a root: $2(9)+3k-21=0$, so $18+3k-21=0$, $3k=3$, $k=1$. "
         "Check: $2x^{2}+x-21=(2x+7)(x-3)$.",
         ["-1", "7", "3"]),
        ("SAT Stretch: The area of a rectangle is $x^{2}+7x+10$ and one side is $x+2$. The other side is:",
         "$x+5$",
         "Divide by $x+2$, or factor $x^{2}+7x+10=(x+2)(x+5)$.",
         ["$x+7$", "$x+10$", "$x+3$"]),
        ("SAT Stretch: Expand and simplify $(x+4)^{2}-(x-1)^{2}$.", "$10x+15$",
         "$x^{2}+8x+16-(x^{2}-2x+1)=x^{2}+8x+16-x^{2}+2x-1=10x+15$. Difference of squares: "
         "$(x+4-(x-1))(x+4+x-1)=(5)(2x+3)=10x+15$.",
         ["$8x+15$", "$2x+15$", "$10x+17$"]),
        ("SAT Stretch: Factor $x^{4}-16$ completely over the integers.", "$(x^{2}-4)(x^{2}+4)=(x-2)(x+2)(x^{2}+4)$",
         "Difference of squares twice: $x^{4}-16=(x^{2}-4)(x^{2}+4)=(x-2)(x+2)(x^{2}+4)$. "
         "$x^{2}+4$ does not factor over the reals with real linear factors.",
         ["$(x-2)^{4}$", "$(x^{2}-4)^{2}$", "$(x-4)(x+4)$"]),
        ("SAT Stretch: If $(3x+k)(x-2)=3x^{2}-x-10$, then $k$ equals:", "5",
         "Expand: $3x^{2}-6x+kx-2k=3x^{2}+(k-6)x-2k$. Then $-2k=-10$ so $k=5$, and $k-6=-1$ checks.",
         ["-5", "2", "6"]),
        ("SAT Stretch: Completely factor $12x^{2}-27$.", "$3(2x-3)(2x+3)$",
         "GCF $3$: $3(4x^{2}-9)=3(2x-3)(2x+3)$.",
         ["$(6x-9)(2x+3)$", "$12(x^{2}-27)$", "$3(4x-9)$"]),
        ("SAT Stretch: The polynomial $x^{3}+3x^{2}-4x-12$ factors by grouping as:", "$(x+3)(x+2)(x-2)$",
         "$x^{2}(x+3)-4(x+3)=(x^{2}-4)(x+3)=(x-2)(x+2)(x+3)$.",
         ["$(x+3)(x^{2}-4x-4)$", "$(x-3)(x+2)(x-2)$", "$(x+6)(x-2)(x+1)$"]),
        ("SAT Stretch: A square has side $x+6$. A rectangle $2$ by $x$ is removed. The remaining area is:",
         "$x^{2}+10x+36$",
         "$(x+6)^{2}-2x=x^{2}+12x+36-2x=x^{2}+10x+36$.",
         ["$x^{2}+12x+36$", "$(x+6)(x+4)$", "$x^{2}+36$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    return qs


def build_unit6():
    title = "Algebra 1 Unit 6: Polynomials & Factoring"
    description = (
        "Adding and subtracting polynomials, multiplying with area models, GCF and grouping, trinomials with "
        "$a=1$ and $a>1$, special products, and factoring completely."
    )
    concepts = [
        "Add and subtract polynomials",
        "Multiply polynomials",
        "GCF and grouping",
        "Trinomials a=1",
        "Trinomials a>1 and special products",
        "Factor completely",
    ]

    c1 = concept_block(
        "1. Add and subtract polynomials",
        [
            "A polynomial is a sum of terms $ax^{n}$ with nonnegative integer powers. Monomials have one term, "
            "binomials two, trinomials three. The degree is the highest power present.",
            "Like terms have the same variable powers. $3x^{2}$ and $-x^{2}$ combine; $3x^{2}$ and $3x$ do not. "
            "Addition is combining like terms after you write both polynomials without extra parentheses.",
            "Subtraction means adding the opposite: distribute a minus through the second polynomial, flipping every "
            "sign, then combine. $ (5x-1)-(2x+4)=5x-1-2x-4=3x-5 $.",
            "Aligning like terms in columns (degree by degree) reduces dropped signs, especially with several "
            "subtractions in a row.",
            "The sum of two polynomials is a polynomial. Degree of a sum is at most the larger of the two degrees, "
            "and can drop if leading terms cancel.",
            "Addition and subtraction here are bookkeeping. The next concept multiplies; factoring later undoes that "
            "multiplication. Clean addition is how you check a factoring by expanding and comparing.",
        ],
        "Every factoring check in this unit is “expand, then add like terms.” If subtraction signs are sloppy, you "
        "will think a correct factoring is wrong.",
        "Write both polynomials, distribute every minus, then add coefficients of matching powers. Look specifically "
        "for cancelled leading terms.",
        lesson_figure(
            svg_balance("3x^2+5x", "x^2+2x + ?"),
            "Adding like tiles: $x^{2}$ with $x^{2}$, $x$ with $x$",
            "Only matching shades combine. A constant tile does not merge with an $x$ tile.",
        )
        + solved(1, "Add $(2x+3)+(5x-1)$.",
                 ["Drop the parentheses: $2x+3+5x-1$.",
                  "Combine like $x$-terms: $2x+5x=7x$.",
                  "Combine constants: $3-1=2$.",
                  "Check: $(2+5)x+(3-1)=7x+2$."],
                 "$7x+2$", "", "Easy")
        + solved(2, "Subtract $(x^{2}+4x-2)-(3x^{2}-x+5)$.",
                 ["Distribute the minus through the second polynomial: $x^{2}+4x-2-3x^{2}+x-5$.",
                  "Combine $x^{2}$ terms: $1-3=-2$. Combine $x$ terms: $4+1=5$.",
                  "Combine constants: $-2-5=-7$. The difference is $-2x^{2}+5x-7$.",
                  "Check by adding the answer to $3x^{2}-x+5$: $(-2x^{2}+5x-7)+(3x^{2}-x+5)=x^{2}+4x-2$."],
                 "$-2x^{2}+5x-7$", "", "Medium")
        + solved(3, "Find $(4x^{3}-x+1)+(-4x^{3}+x+8)$ and state the degree of the result.",
                 ["Add $x^{3}$ coefficients: $4+(-4)=0$, so those terms cancel.",
                  "Add $x$ coefficients: $-1+1=0$, so those cancel too.",
                  "Add constants: $1+8=9$. The sum is the nonzero constant $9$.",
                  "A nonzero constant has degree $0$."],
                 "$9$; degree $0$", "", "Hard"),
        ("Forgetting to flip every sign when subtracting",
         "The minus applies to the entire second polynomial. $-(2x-5)$ is $-2x+5$, not $-2x-5$."),
        ("Stack powers in columns",
         "Write $x^{2}$, $x$, and constant columns before you add. Gaps in a column are zeros, not missing work."),
        [
            "I can add polynomials by combining like terms.",
            "I can subtract by distributing a minus.",
            "I can find the degree of a sum.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Multiply polynomials",
        [
            "Multiplication of polynomials uses the distributive property repeatedly. A monomial times a polynomial "
            "is one pass: $3x(x^{2}-2)=3x^{3}-6x$.",
            "A binomial times a binomial is four products (FOIL: first, outer, inner, last). An area model makes the "
            "same four products into a rectangle of tiles.",
            "After distributing, combine like terms. $(x+3)(x+4)=x^{2}+4x+3x+12=x^{2}+7x+12$. The middle two tiles "
            "are both $x$-tiles.",
            "Special products worth memorizing: $(a+b)^{2}=a^{2}+2ab+b^{2}$, $(a-b)^{2}=a^{2}-2ab+b^{2}$, and "
            "$(a+b)(a-b)=a^{2}-b^{2}$. They are shortcuts, not new laws.",
            "A trinomial times a binomial is six products. Organize them; do not rely on holding six numbers in "
            "working memory.",
            "Multiplication is how you check factoring. If the product is not the original polynomial, the factors "
            "are wrong.",
        ],
        "Area models here are the same rectangles you will factor in reverse for the rest of the unit. Seeing "
        "$x^{2}+5x+6$ as a rectangle with sides $x+2$ and $x+3$ is the whole game.",
        "Draw the rectangle, fill each cell with a product, then add the cells. For special products, still expand "
        "once to confirm until the pattern is automatic.",
        lesson_figure(
            _area_model("x^2", "3x", "2x", "6", top="x + 3", left="x + 2"),
            "Area model for $(x+3)(x+2)$",
            "Tiles $x^{2}$, $3x$, $2x$, and $6$ combine to $x^{2}+5x+6$. Factoring later splits this rectangle back into sides.",
        )
        + solved(4, "Expand $x(x+7)$.",
                 ["Distribute $x$ to the first term: $x\\cdot x=x^{2}$.",
                  "Distribute $x$ to $7$: $x\\cdot 7=7x$.",
                  "There are no like terms to combine, so the product is $x^{2}+7x$.",
                  "Check: an area $x$ by $x+7$ is an $x^{2}$ square plus a $7x$ rectangle."],
                 "$x^{2}+7x$", "", "Easy")
        + solved(5, "Expand $(x+5)(x-2)$.",
                 ["First: $x\\cdot x=x^{2}$. Outer: $x\\cdot(-2)=-2x$.",
                  "Inner: $5\\cdot x=5x$. Last: $5\\cdot(-2)=-10$.",
                  "Combine the $x$ terms: $-2x+5x=3x$. The product is $x^{2}+3x-10$.",
                  "Check: $(x+5)(x-2)=x(x-2)+5(x-2)=x^{2}-2x+5x-10=x^{2}+3x-10$."],
                 "$x^{2}+3x-10$", "", "Medium")
        + solved(6, "Expand $(2x-3)(x+4)$.",
                 ["Four products: $2x\\cdot x=2x^{2}$, $2x\\cdot 4=8x$, $-3\\cdot x=-3x$, $-3\\cdot 4=-12$.",
                  "Combine like $x$ terms: $8x-3x=5x$.",
                  "The expanded form is $2x^{2}+5x-12$.",
                  "Check by grouping: $2x(x+4)-3(x+4)=2x^{2}+8x-3x-12=2x^{2}+5x-12$."],
                 "$2x^{2}+5x-12$", "", "SAT"),
        ("Writing $(x+3)^{2}=x^{2}+9$",
         "The middle term $6x$ is missing. Square of a sum always has $2ab$."),
        ("Fill four cells, then combine",
         "Even when you FOIL in your head, jot the four products. Combining too early drops an inner or outer term."),
        [
            "I can multiply a monomial by a polynomial.",
            "I can expand two binomials with an area model.",
            "I can use the three special-product patterns.",
        ],
        6,
    )

    c3 = concept_block(
        "3. GCF and grouping",
        [
            "The greatest common factor of monomials is the largest integer that divides the coefficients, times the "
            "smallest power of each shared variable. GCF of $12x^{3}$ and $18x^{2}$ is $6x^{2}$.",
            "Factoring out a GCF is reverse distribution: $6x^{2}+9x=3x(2x+3)$. Always check by multiplying back.",
            "Four-term polynomials often factor by grouping: split into two pairs, factor each pair, then factor the "
            "common binomial. $x^{3}+2x^{2}+3x+6=x^{2}(x+2)+3(x+2)=(x^{2}+3)(x+2)$.",
            "If the pairs do not share a binomial, regroup or look for a hidden GCF first. Sometimes you factor $-1$ "
            "from the second pair to force a match: $x^{3}+x^{2}-x-1=x^{2}(x+1)-1(x+1)$.",
            "Taking out a GCF first can change grouping from messy to obvious. Never skip the GCF step; it is also "
            "required for “factor completely” later.",
            "Grouping is the path to $a>1$ trinomials when you rewrite $2x^{2}+7x+3$ as $2x^{2}+6x+x+3$ and group.",
        ],
        "Forgetting the GCF leaves a polynomial “factored” that still has a common factor — incomplete, and often "
        "the difference between full credit and not on a test.",
        "GCF first. Then, for four terms, factor each pair and look for a shared binomial. Multiply back as a check.",
        lesson_figure(
            svg_rect("3x", "2x+3"),
            "GCF picture: $3x(2x+3)=6x^{2}+9x$",
            "The common height $3x$ is pulled out of both tiles. Factoring is reading the side lengths of the rectangle.",
        )
        + solved(7, "Factor $10x+15$.",
                 ["The GCF of $10$ and $15$ is $5$; both terms also share no extra $x$ beyond the first.",
                  "Divide each term by $5$: $10x\\div 5=2x$ and $15\\div 5=3$.",
                  "Write $5(2x+3)$.",
                  "Check by distributing: $5\\cdot 2x+5\\cdot 3=10x+15$."],
                 "$5(2x+3)$", "", "Easy")
        + solved(8, "Factor $x^{3}+4x^{2}+2x+8$ by grouping.",
                 ["Split into $(x^{3}+4x^{2})+(2x+8)$.",
                  "Factor each pair: $x^{2}(x+4)+2(x+4)$.",
                  "The shared binomial is $x+4$, so $(x^{2}+2)(x+4)$.",
                  "Check: $x^{2}(x+4)+2(x+4)=x^{3}+4x^{2}+2x+8$."],
                 "$(x^{2}+2)(x+4)$", "", "Medium")
        + solved(9, "Factor $6x^{3}-9x^{2}-4x+6$ by grouping.",
                 ["Group $(6x^{3}-9x^{2})+(-4x+6)$.",
                  "Factor $3x^{2}$ from the first pair and $-2$ from the second: $3x^{2}(2x-3)-2(2x-3)$.",
                  "Shared binomial $2x-3$ gives $(3x^{2}-2)(2x-3)$.",
                  "Check: $3x^{2}(2x-3)-2(2x-3)=6x^{3}-9x^{2}-4x+6$."],
                 "$(3x^{2}-2)(2x-3)$", "", "Hard"),
        ("Stopping after a partial GCF",
         "$2(6x+9)$ still has a $3$ inside. Pull $6$: $6(2x+3)$, or pull $3$ from the leftover."),
        ("Force a matching binomial with $-1$",
         "If the second pair is $-x-1$, write $-1(x+1)$ so it matches an $(x+1)$ from the first pair."),
        [
            "I can find a monomial GCF.",
            "I can factor four terms by grouping.",
            "I check by distributing.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Trinomials $a=1$",
        [
            "To factor $x^{2}+bx+c$ you want integers $p$ and $q$ with $p+q=b$ and $pq=c$. Then "
            "$x^{2}+bx+c=(x+p)(x+q)$.",
            "List factor pairs of $c$ and keep the pair that adds to $b$. Signs matter: if $c>0$ and $b>0$, both "
            "factors are positive. If $c>0$ and $b<0$, both are negative. If $c<0$, the factors have opposite signs.",
            "The area model is the reverse of last lesson: you know the total rectangle $x^{2}+5x+6$ and you hunt "
            "side lengths $x+2$ and $x+3$.",
            "Not every trinomial factors over the integers. $x^{2}+x+1$ has no integer pair. Later, the quadratic "
            "formula still solves $x^{2}+x+1=0$.",
            "Always multiply back. $(x+2)(x+3)=x^{2}+5x+6$ confirms the pair. A sign error is obvious on that check.",
            "When $c=0$, $x^{2}+bx=x(x+b)$ is a GCF, not a two-binomial hunt. Recognize that shortcut.",
        ],
        "Solving quadratics by factoring in Unit 7 depends on this hunt being fast and accurate. The pair-of-factors "
        "habit is the entire method.",
        "Write factor pairs of $c$, circle the pair that sums to $b$, write $(x+p)(x+q)$, multiply to check.",
        lesson_figure(
            _area_model("x^2", "3x", "2x", "6", top="x + 3", left="x + 2"),
            "Factoring $x^{2}+5x+6$ as side lengths",
            "The $x$-tiles split as $2x$ and $3x$, matching $2+3=5$ and $2\\cdot 3=6$.",
        )
        + solved(10, "Factor $x^{2}+8x+15$.",
                 ["Need integers $p,q$ with $pq=15$ and $p+q=8$. Pairs of $15$: $1$ and $15$, $3$ and $5$.",
                  "The pair $3$ and $5$ adds to $8$.",
                  "Write $(x+3)(x+5)$.",
                  "Check by expanding: $x^{2}+5x+3x+15=x^{2}+8x+15$."],
                 "$(x+3)(x+5)$", "", "Easy")
        + solved(11, "Factor $x^{2}-5x-14$.",
                 ["Need $pq=-14$ and $p+q=-5$. Signed pairs of $-14$ include $-7$ and $2$.",
                  "$-7+2=-5$, which matches the middle term.",
                  "Write $(x-7)(x+2)$.",
                  "Check: $x^{2}+2x-7x-14=x^{2}-5x-14$."],
                 "$(x-7)(x+2)$", "", "Medium")
        + solved(12, "Factor $x^{2}+4x-21$.",
                 ["Need $pq=-21$ and $p+q=4$. Signed pairs of $-21$ include $7$ and $-3$.",
                  "$7+(-3)=4$.",
                  "Write $(x+7)(x-3)$.",
                  "Check: $x^{2}-3x+7x-21=x^{2}+4x-21$."],
                 "$(x+7)(x-3)$", "", "SAT"),
        ("Using pairs that multiply to $b$ instead of $c$",
         "The product $pq$ must equal the constant $c$, not the middle coefficient. The sum $p+q$ is the middle."),
        ("List signed pairs, not just positives",
         "For $c<0$, one factor is negative. Writing only $1,21$ and $3,7$ will miss $7$ and $-3$."),
        [
            "I can find integer pairs $p,q$ with $p+q=b$ and $pq=c$.",
            "I can handle mixed signs.",
            "I multiply to verify.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Trinomials $a>1$ and special products",
        [
            "For $ax^{2}+bx+c$ with $a>1$, one method is grouping: find numbers that multiply to $ac$ and add to $b$, "
            "split the middle, then group. For $2x^{2}+7x+3$, $ac=6$, and $6+1=7$, so $2x^{2}+6x+x+3$.",
            "Trial binomials also work: guess $(2x+\\_)(x+\\_)$ and adjust constants until the outer+inner match $b$. "
            "Checking by expansion is required either way.",
            "Difference of squares: $a^{2}-b^{2}=(a-b)(a+b)$. Perfect square trinomials: $a^{2}\\pm 2ab+b^{2}=(a\\pm b)^{2}$. "
            "Spotting these saves the $ac$ hunt.",
            "A common miss is treating $4x^{2}-9$ as not factorable because it is not a trinomial. It is a binomial "
            "that is a difference of squares.",
            "Leading coefficient $4$ in $4x^{2}+4x+1$ is $(2x+1)^{2}$. Recognizing squares of binomials is faster "
            "than grouping.",
            "If nothing works over the integers, say so. Do not invent fractions inside factors unless the problem "
            "allows rational coefficients.",
        ],
        "Unit 7 will solve $2x^{2}+7x+3=0$ by this factoring. Special products also generate the identities you "
        "use when completing the square.",
        "Compute $ac$, split $b$, group. Or guess-and-check binomials. Then look once more: is it a square or a "
        "difference of squares?",
        lesson_figure(
            _area_model("2x^2", "6x", "x", "3", top="x + 3", left="2x + 1"),
            "Area model for $(2x+1)(x+3)=2x^{2}+7x+3$",
            "The middle $7x$ is the sum of the off-diagonal tiles $6x$ and $x$.",
        )
        + solved(13, "Factor $x^{2}-25$.",
                 ["This is a difference of squares: $a=x$ and $b=5$ because $5^{2}=25$.",
                  "Use $a^{2}-b^{2}=(a-b)(a+b)$ to write $(x-5)(x+5)$.",
                  "Expand to check: $x^{2}+5x-5x-25=x^{2}-25$.",
                  "The middle terms cancel, which is the signature of $a^{2}-b^{2}$."],
                 "$(x-5)(x+5)$", "", "Easy")
        + solved(14, "Factor $3x^{2}+11x+6$.",
                 ["Here $a=3$, so $ac=18$. Find a pair that multiplies to $18$ and adds to $11$: $9$ and $2$.",
                  "Split the middle: $3x^{2}+9x+2x+6$.",
                  "Group: $3x(x+3)+2(x+3)=(3x+2)(x+3)$.",
                  "Check: $(3x+2)(x+3)=3x^{2}+9x+2x+6=3x^{2}+11x+6$."],
                 "$(3x+2)(x+3)$", "", "Medium")
        + solved(15, "Factor $4x^{2}-12x+9$.",
                 ["Look for a perfect square: $4x^{2}=(2x)^{2}$ and $9=3^{2}$.",
                  "The middle of $(2x-3)^{2}$ is $2\\cdot 2x\\cdot 3=12x$, matching the given $12x$ with a minus.",
                  "So $4x^{2}-12x+9=(2x-3)^{2}$.",
                  "Check: $(2x-3)(2x-3)=4x^{2}-6x-6x+9=4x^{2}-12x+9$."],
                 "$(2x-3)^{2}$", "", "Hard"),
        ("Stopping at $a^{2}-b^{2}$ still written as a single binomial",
         "$x^{2}-16$ is not finished until $(x-4)(x+4)$. A difference of squares is a factoring, not a simplified "
         "trinomial."),
        ("Split the middle so grouping is obvious",
         "After you find the $ac$ pair, rewrite four terms and factor by grouping. Do not try to jump straight to "
         "binomials without a check."),
        [
            "I can factor $ax^{2}+bx+c$ with $a>1$.",
            "I can factor a difference of squares.",
            "I can recognize a perfect square trinomial.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Factor completely",
        [
            "Factoring completely over the integers means: take out the GCF, then factor every remaining polynomial "
            "until each factor is linear or a prime quadratic (no further integer-coefficient factors).",
            "A standard order: GCF, then four-term grouping if needed, then trinomial or difference of squares, then "
            "look again — $x^{2}-4$ inside still factors.",
            "Example: $2x^{3}-8x=2x(x^{2}-4)=2x(x-2)(x+2)$. Stopping at $2x(x^{2}-4)$ is incomplete.",
            "Constants can stay as integer GCFs. $12x^{2}-27=3(4x^{2}-9)=3(2x-3)(2x+3)$. Pulling $3$ is part of "
            "completely.",
            "Prime over the integers, such as $x^{2}+1$ or $x^{2}+x+1$, is an acceptable stopping point. Completely "
            "does not mean “use complex numbers” in Algebra 1.",
            "The check is still expansion. If you used three factors, multiply them in any order and compare to the "
            "original polynomial.",
        ],
        "Unit 7’s “solve by factoring” uses the zero product property on a complete factorization. A leftover "
        "$x^{2}-4$ hides two roots.",
        "GCF, then patterns, then look inside each factor once more. Expand all the way back as the last line.",
        lesson_figure(
            _area_model("x^2", "2x", "-2x", "-4", top="x - 2", left="x + 2"),
            "After GCF, $x^{2}-4$ still splits",
            "The remaining rectangle is a difference of squares. Completely factored form includes both $(x-2)$ and $(x+2)$.",
        )
        + solved(16, "Factor $x^{2}-4x$ completely.",
                 ["Every term has an $x$, so the GCF is $x$.",
                  "Factor: $x(x-4)$.",
                  "The leftover $x-4$ is already linear, so stop.",
                  "Check: $x\\cdot x-x\\cdot 4=x^{2}-4x$."],
                 "$x(x-4)$", "", "Easy")
        + solved(17, "Factor $3x^{2}-12$ completely.",
                 ["GCF of the coefficients is $3$: $3(x^{2}-4)$.",
                  "The leftover $x^{2}-4$ is a difference of squares.",
                  "Continue: $3(x-2)(x+2)$.",
                  "Check: $(x-2)(x+2)=x^{2}-4$, then $3(x^{2}-4)=3x^{2}-12$."],
                 "$3(x-2)(x+2)$", "", "Medium")
        + solved(18, "Factor $x^{3}+x^{2}-4x-4$ completely.",
                 ["Group: $(x^{3}+x^{2})+(-4x-4)=x^{2}(x+1)-4(x+1)$.",
                  "Shared binomial: $(x^{2}-4)(x+1)$.",
                  "Then $x^{2}-4=(x-2)(x+2)$, so completely $(x-2)(x+2)(x+1)$.",
                  "Check: $(x-2)(x+2)=x^{2}-4$, times $(x+1)$ is $x^{3}+x^{2}-4x-4$."],
                 "$(x-2)(x+2)(x+1)$", "", "SAT"),
        ("Calling $2(x^{2}-9)$ complete",
         "$x^{2}-9$ still factors. Completely requires $(x-3)(x+3)$ as well: $2(x-3)(x+3)$."),
        ("One extra pass on each factor",
         "After you write a product, stare at each piece: GCF? squares? trinomial? Only then stop."),
        [
            "I always pull a GCF first.",
            "I continue until factors are linear or prime quadratics.",
            "I expand to verify a complete factorization.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u6_questions()


# ===========================================================================
# UNIT 7: Quadratic Functions & Equations
# ===========================================================================

def _u7_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("The parent parabola $y=x^{2}$ has vertex:", "$(0,0)$",
         "The lowest point of $y=x^{2}$ is the origin.",
         ["$(1,0)$", "$(0,1)$", "$(1,1)$"]),
        ("If $a>0$ in $y=ax^{2}+bx+c$, the parabola:", "opens upward",
         "Positive $a$ means a U shape (minimum at the vertex). Negative $a$ opens downward.",
         ["opens downward", "is a line", "has no vertex"]),
        ("The vertex of $y=(x-3)^{2}+2$ is:", "$(3,2)$",
         "Vertex form $y=(x-h)^{2}+k$ has vertex $(h,k)$. Here $h=3$, $k=2$.",
         ["$(-3,2)$", "$(3,-2)$", "$(2,3)$"]),
        ("The axis of symmetry of $y=x^{2}-6x+1$ is:", "$x=3$",
         "$x=-\\dfrac{b}{2a}=-\\dfrac{-6}{2}=3$.",
         ["$x=-3$", "$x=6$", "$y=3$"]),
        ("Compared with $y=x^{2}$, the graph $y=-x^{2}$ is:", "reflected over the $x$-axis",
         "The leading negative flips the U upside down.",
         ["shifted left 1", "shifted up 1", "a wider line"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Solve $x^{2}-5x+6=0$ by factoring.", "$x=2$ or $x=3$",
         "$(x-2)(x-3)=0$, so $x=2$ or $x=3$.",
         ["$x=-2$ or $x=-3$", "$x=6$", "$x=5$"]),
        ("If $(x-4)(x+1)=0$, then $x$ is:", "$4$ or $-1$",
         "Zero product: a factor is $0$.",
         ["$4$ or $1$", "$-4$ or $1$", "$0$"]),
        ("Solve $x^{2}=9$ using factoring $x^{2}-9=0$.", "$x=3$ or $x=-3$",
         "$(x-3)(x+3)=0$.",
         ["$x=9$", "$x=3$ only", "$x=0$"]),
        ("The solutions of $x(x-8)=0$ are:", "$0$ and $8$",
         "Zero product on $x=0$ or $x=8$.",
         ["$8$ only", "$-8$ and $8$", "$1$ and $8$"]),
        ("Solve $x^{2}+6x+8=0$.", "$x=-2$ or $x=-4$",
         "$(x+2)(x+4)=0$.",
         ["$x=2$ or $x=4$", "$x=-8$", "$x=6$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The quadratic formula for $ax^{2}+bx+c=0$ is $x=$:",
         "$\\dfrac{-b\\pm\\sqrt{b^{2}-4ac}}{2a}$",
         "That formula comes from completing the square on the general trinomial.",
         ["$\\dfrac{b\\pm\\sqrt{b^{2}-4ac}}{2a}$", "$-b\\pm 2a$", "$\\dfrac{-b}{2a}$ only"]),
        ("Discriminant of $x^{2}-4x+1=0$ is:", "12",
         "$b^{2}-4ac=16-4=12$. Two real roots.",
         ["4", "0", "-12"]),
        ("If the discriminant is $0$, the equation has:", "one real solution (a double root)",
         "The parabola is tangent to the $x$-axis.",
         ["two distinct real solutions", "no real solution", "infinitely many"]),
        ("Solve $x^{2}-2x-1=0$ using the formula. The roots are:", "$1\\pm\\sqrt{2}$",
         "$x=\\dfrac{2\\pm\\sqrt{4+4}}{2}=\\dfrac{2\\pm\\sqrt{8}}{2}=\\dfrac{2\\pm 2\\sqrt{2}}{2}=1\\pm\\sqrt{2}$.",
         ["$2\\pm\\sqrt{2}$", "$\\pm 1$", "$1\\pm 2$"]),
        ("For $2x^{2}+3x-2=0$, one root from the formula is:", "$\\dfrac{1}{2}$",
         "Discriminant $9+16=25$. $x=\\dfrac{-3\\pm 5}{4}$. Then $\\dfrac{2}{4}=\\dfrac{1}{2}$ and $\\dfrac{-8}{4}=-2$.",
         ["$3$", "$-\\dfrac{3}{2}$", "$2$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Complete the square: $x^{2}+6x$ becomes:", "$(x+3)^{2}-9$",
         "Half of $6$ is $3$, square is $9$. So $x^{2}+6x+9-9=(x+3)^{2}-9$.",
         ["$(x+6)^{2}$", "$(x+3)^{2}+9$", "$(x+3)^{2}$"]),
        ("Vertex form of $y=x^{2}+4x+1$ after completing the square is:", "$y=(x+2)^{2}-3$",
         "$x^{2}+4x+1=(x+2)^{2}-4+1=(x+2)^{2}-3$. Vertex $(-2,-3)$.",
         ["$y=(x+2)^{2}+1$", "$y=(x+4)^{2}-15$", "$y=(x-2)^{2}-3$"]),
        ("To complete the square on $x^{2}+10x$, you add and subtract:", "25",
         "$(10/2)^{2}=25$.",
         ["10", "5", "100"]),
        ("$x^{2}-8x+c$ is a perfect square when $c=$:", "16",
         "Half of $-8$ is $-4$, square $16$. $(x-4)^{2}=x^{2}-8x+16$.",
         ["8", "4", "-16"]),
        ("Completing the square on $x^{2}+2x-5=0$ yields:", "$(x+1)^{2}=6$",
         "$x^{2}+2x=5$, add $1$: $(x+1)^{2}=6$.",
         ["$(x+1)^{2}=5$", "$(x+2)^{2}=5$", "$(x+1)^{2}=-5$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("If a parabola crosses the $x$-axis at $-1$ and $4$, a possible equation is:", "$y=(x+1)(x-4)$",
         "Roots $r,s$ give $y=a(x-r)(x-s)$. Here $a=1$.",
         ["$y=(x-1)(x+4)$", "$y=x^{2}+4$", "$y=(x+1)^{2}$"]),
        ("A graph that touches the $x$-axis at one point has discriminant:", "0",
         "Tangent to the axis: one real root (double).",
         ["positive", "negative", "undefined"]),
        ("If $y=x^{2}+1$, the number of real roots of $y=0$ is:", "0",
         "$x^{2}=-1$ has no real $x$. The graph sits entirely above the $x$-axis.",
         ["1", "2", "infinitely many"]),
        ("The $x$-intercepts of $y=(x-2)^{2}-9$ are:", "$x=5$ and $x=-1$",
         "$(x-2)^{2}=9$, $x-2=\\pm 3$, so $x=5$ or $x=-1$.",
         ["$x=2$ only", "$x=3$ and $x=-3$", "$x=9$"]),
        ("A parabola with no $x$-intercepts and $a>0$ has range:", "$y\\geq k$ with $k>0$",
         "Minimum $k$ is above the axis, so the graph never crosses $y=0$.",
         ["all real $y$", "$y\\leq 0$", "$y=0$ only"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("A ball’s height $h(t)=-16t^{2}+64t$ (feet, seconds) is $0$ at $t=0$ and at:", "$t=4$",
         "$-16t(t-4)=0$. The positive intercept is the landing time $4$ s.",
         ["$t=2$", "$t=16$", "$t=64$"]),
        ("For $h(t)=-16t^{2}+64t$, the time of maximum height is:", "2 s",
         "Vertex $t=-\\dfrac{b}{2a}=-\\dfrac{64}{-32}=2$.",
         ["4 s", "1 s", "8 s"]),
        ("The maximum height of $h(t)=-16t^{2}+64t$ is:", "64 ft",
         "$h(2)=-16(4)+128=-64+128=64$.",
         ["32 ft", "128 ft", "16 ft"]),
        ("A projectile $h(t)=-5t^{2}+20t+2$ has initial height:", "2",
         "$h(0)=2$, the constant term.",
         ["20", "-5", "0"]),
        ("If $h(t)=-16t^{2}+48t$ models a jump, the ball is in the air for:", "3 s",
         "$-16t(t-3)=0$, so it lands at $t=3$.",
         ["48 s", "1.5 s", "16 s"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The vertex of $y=-(x+1)^{2}+5$ is:", "$(-1,5)$",
         "$h=-1$, $k=5$. It opens down, so $5$ is a maximum.",
         ["$(1,5)$", "$(-1,-5)$", "$(0,5)$"]),
        ("Solve $x^{2}-x-6=0$ by factoring.", "$x=3$ or $x=-2$",
         "$(x-3)(x+2)=0$.",
         ["$x=6$", "$x=1$", "$x=-3$ or $x=2$"]),
        ("Discriminant of $x^{2}+2x+5=0$ is:", "-16",
         "$4-20=-16$. No real roots.",
         ["16", "4", "0"]),
        ("$y=x^{2}-4x+4$ touches the $x$-axis at:", "$(2,0)$",
         "$(x-2)^{2}=0$, double root $x=2$.",
         ["$(4,0)$", "$(0,4)$", "$(-2,0)$"]),
        ("Completing the square: $x^{2}-2x-3=0$ becomes:", "$(x-1)^{2}=4$",
         "$x^{2}-2x=3$, add $1$: $(x-1)^{2}=4$. Then $x-1=\\pm 2$.",
         ["$(x-1)^{2}=3$", "$(x-2)^{2}=3$", "$(x-1)^{2}=-3$"]),
        ("The axis of $y=2(x-4)^{2}+1$ is the vertical line:", "$x=4$",
         "Axis of symmetry is $x=h$.",
         ["$x=2$", "$y=1$", "$x=1$"]),
        ("Quadratic formula on $x^{2}=5$ gives:", "$x=\\pm\\sqrt{5}$",
         "$x^{2}-5=0$, $x=\\dfrac{\\pm\\sqrt{20}}{2}$? $a=1,b=0,c=-5$, $x=\\pm\\sqrt{5}$.",
         ["$x=5$", "$x=\\pm 5$", "$x=\\sqrt{5}$ only"]),
        ("A graph with $x$-intercepts $2$ and $6$ and vertex at $x=4$ is consistent because:",
         "the axis is the midpoint of the roots",
         "Axis $x=\\dfrac{2+6}{2}=4$.",
         ["the vertex must be on the $y$-axis", "roots must be opposites", "a must be 1"]),
        ("$h(t)=-16t^{2}+80t$ reaches max at $t=$:", "2.5 s",
         "$t=80/32=2.5$.",
         ["5 s", "16 s", "80 s"]),
        ("If $y=(x-1)(x-5)$, the $y$-intercept is:", "5",
         "$y=(0-1)(0-5)=5$. Point $(0,5)$.",
         ["-5", "0", "1"]),
        ("Solve $2x^{2}-8=0$ by factoring.", "$x=2$ or $x=-2$",
         "$2(x^{2}-4)=0$, $(x-2)(x+2)=0$.",
         ["$x=8$", "$x=4$", "$x=0$"]),
        ("Vertex of $y=x^{2}+8x+7$ is at $x=$:", "-4",
         "$x=-8/2=-4$. Then $y=16-32+7=-9$, vertex $(-4,-9)$.",
         ["4", "8", "-8"]),
        ("No real solution of $x^{2}+4=0$ because:", "the graph $y=x^{2}+4$ never meets $y=0$",
         "Minimum is $4>0$. Discriminant $-16<0$.",
         ["the formula is undefined for all quadratics", "degree is even", "c is positive always fails"]),
        ("A projectile $h=-4.9t^{2}+14.7t$ (meters) lands when $t=$:", "3 s",
         "$-4.9t(t-3)=0$, $t=3$.",
         ["4.9 s", "14.7 s", "1.5 s"]),
        ("Factored $y=-(x+2)(x-6)$ opens:", "downward",
         "Leading coefficient: $-x^{2}$ after expansion, so $a<0$.",
         ["upward", "to the right", "horizontally"]),
        ("The formula $t=-\\dfrac{b}{2a}$ finds:", "the vertex time (axis of symmetry)",
         "It is the $x$-coordinate of the vertex, hence the max/min time for a projectile.",
         ["the landing time only", "the initial height", "the discriminant"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("SAT Stretch: A parabola $y=x^{2}-6x+c$ has a double root. Then $c$ equals:", "9",
         "Discriminant $36-4c=0$, so $c=9$. Equivalently $(x-3)^{2}=x^{2}-6x+9$.",
         ["6", "0", "36"]),
        ("SAT Stretch: Solve $2x^{2}-3x-2=0$. The positive root is:", "2",
         "Discriminant $9+16=25$. $x=\\dfrac{3\\pm 5}{4}$. Positive: $\\dfrac{8}{4}=2$. The other is $-\\dfrac{1}{2}$.",
         ["$\\dfrac{3}{2}$", "3", "$\\dfrac{1}{2}$"]),
        ("SAT Stretch: Complete the square to find the minimum of $y=x^{2}-10x+21$. The minimum value is:", "-4",
         "$y=(x-5)^{2}-25+21=(x-5)^{2}-4$. Minimum $-4$ at $x=5$.",
         ["21", "5", "-25"]),
        ("SAT Stretch: A ball is thrown so $h(t)=-16t^{2}+48t+4$. Its maximum height is:", "40 ft",
         "Vertex $t=48/32=1.5$. $h(1.5)=-16(2.25)+48(1.5)+4=-36+72+4=40$.",
         ["4 ft", "48 ft", "36 ft"]),
        ("SAT Stretch: The graph of $y=2(x-1)^{2}-8$ has $x$-intercepts:", "$x=3$ and $x=-1$",
         "$2(x-1)^{2}=8$, $(x-1)^{2}=4$, $x-1=\\pm 2$, so $x=3$ or $x=-1$.",
         ["$x=1$ only", "$x=4$ and $x=0$", "$x=2$ and $x=0$"]),
        ("SAT Stretch: For $ax^{2}+bx+c=0$ to have two distinct real roots, which must hold?", "$b^{2}-4ac>0$ and $a\\neq 0$",
         "A quadratic needs $a\\neq 0$ and a positive discriminant for two distinct real roots.",
         ["$c>0$", "$b=0$", "$a>0$ only"]),
        ("SAT Stretch: Rewrite $y=2x^{2}+12x+10$ in vertex form.", "$y=2(x+3)^{2}-8$",
         "$y=2(x^{2}+6x)+10=2((x+3)^{2}-9)+10=2(x+3)^{2}-18+10=2(x+3)^{2}-8$.",
         ["$y=2(x+3)^{2}+10$", "$y=(x+3)^{2}-8$", "$y=2(x+6)^{2}-8$"]),
        ("SAT Stretch: A rectangle has width $x$ and length $x+3$. Area $40$. The positive width is:", "5",
         "$x(x+3)=40$, $x^{2}+3x-40=0$, $(x+8)(x-5)=0$, so $x=5$.",
         ["8", "40", "3"]),
        ("SAT Stretch: A ball follows $h(t)=-16t^{2}+64t+5$. The time of maximum height, the maximum height, and "
         "the number of real times $h=53$ are:",
         "$2$ s; $69$ ft; two times",
         "Vertex time $t=-b/(2a)=64/32=2$. Then $h(2)=-16(4)+64(2)+5=-64+128+5=69$. "
         "Set $h=53$: $-16t^{2}+64t+5=53$, so $-16t^{2}+64t-48=0$. Divide by $-16$: $t^{2}-4t+3=0=(t-1)(t-3)$. "
         "Discriminant $16-12=4>0$ with two positive roots, so two times.",
         ["$2$ s; $69$ ft; one time", "$4$ s; $5$ ft; two times", "$2$ s; $53$ ft; none"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    return qs


def build_unit7():
    title = "Algebra 1 Unit 7: Quadratic Functions & Equations"
    description = (
        "Parabolas and vertices, solving by factoring, the quadratic formula, completing the square, "
        "connecting graphs to roots, and projectile models."
    )
    concepts = [
        "Parabolas and vertex",
        "Factoring to solve",
        "Quadratic formula",
        "Completing the square (intro)",
        "Graphs vs roots",
        "Projectile stories",
    ]

    c1 = concept_block(
        "1. Parabolas and vertex",
        [
            "A quadratic function has the form $f(x)=ax^{2}+bx+c$ with $a\\neq 0$. Its graph is a parabola — a U "
            "shape if $a>0$, an upside-down U if $a<0$.",
            "The vertex is the turning point: a minimum when $a>0$ and a maximum when $a<0$. The axis of symmetry "
            "is the vertical line $x=-\\dfrac{b}{2a}$ through the vertex.",
            "Vertex form $y=a(x-h)^{2}+k$ makes the vertex $(h,k)$ obvious. Standard form hides it until you compute "
            "$-b/(2a)$ or complete the square.",
            "The parent $y=x^{2}$ has vertex $(0,0)$. $y=(x-h)^{2}+k$ shifts that parent by $h$ right and $k$ up. "
            "The factor $a$ stretches or reflects.",
            "A table of a quadratic has constant second differences. That is a quick check that a scatter is "
            "parabolic rather than linear or exponential.",
            "Graphing from vertex form: plot $(h,k)$, then use $a$ to step equal distances left and right (symmetry).",
        ],
        "Every quadratic story in this unit — roots, projectiles, area — is easier once you can name the vertex. "
        "The vertex is the max/min the application cares about.",
        "Identify $a$ for open up/down. Find $h$ from vertex form or $-b/(2a)$. Plot the vertex, then two symmetric "
        "points.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: (x - 2) ** 2 - 1, -1, 5))],
                points=[(2, -1, "vertex (2,−1)"), (0, 3, "(0,3)"), (4, 3, "(4,3)")],
                xlim=(-2, 6), ylim=(-3, 8),
            ),
            "The parabola $y=(x-2)^{2}-1$",
            "Vertex $(2,-1)$ is the minimum. Symmetric points on either side share the same height.",
        )
        + solved(1, "State the vertex of $y=(x+4)^{2}-3$.",
                 ["$h=-4$, $k=-3$, vertex $(-4,-3)$."],
                 "$(-4,-3)$", "", "Easy")
        + solved(2, "Find the axis of symmetry of $y=2x^{2}-8x+1$.",
                 ["$x=-\\dfrac{-8}{4}=2$."],
                 "$x=2$", "", "Medium")
        + solved(3, "Convert $y=x^{2}-6x+5$ to vertex form by completing the square, and name the vertex.",
                 ["$y=(x^{2}-6x+9)+5-9=(x-3)^{2}-4$.",
                  "Vertex $(3,-4)$."],
                 "$y=(x-3)^{2}-4$; vertex $(3,-4)$", "", "SAT"),
        ("Reading $y=(x+4)^{2}$ as vertex $(4,0)$",
         "The form is $(x-h)^{2}$, so $x+4=x-(-4)$ and $h=-4$. The vertex is to the left."),
        ("Plot the vertex first",
         "Do not start at the $y$-intercept and guess the bottom. Compute $(h,k)$, then use symmetry."),
        [
            "I can tell open up versus open down from $a$.",
            "I can find the vertex from vertex form or $-b/(2a)$.",
            "I can use symmetry to plot points.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Factoring to solve",
        [
            "The zero product property: if $AB=0$, then $A=0$ or $B=0$ (or both). That is why factoring solves "
            "quadratic equations. First write the equation as $=0$.",
            "Example: $x^{2}-5x+6=0$ becomes $(x-2)(x-3)=0$, so $x=2$ or $x=3$. Each factor gives a root, which is "
            "an $x$-intercept of $y=x^{2}-5x+6$.",
            "If a GCF is present, factor it too: $2x^{2}-8x=0$ is $2x(x-4)=0$, so $x=0$ or $x=4$. Dropping the $2x$ "
            "loses the root $0$.",
            "Not every quadratic factors over the integers. When factoring stalls, use the quadratic formula or "
            "complete the square — next lessons, not a reason to invent factors.",
            "Checking means substituting each root into the original equation, not into a half-factored middle line "
            "only.",
            "The graph meets the $x$-axis at the real roots. Two factors, two intercepts (unless a double root).",
        ],
        "Factoring is the fastest exact method when it works. Unit 6’s complete factorization is the skill; solving "
        "here is the reason that skill exists.",
        "Set equal to zero, factor completely, apply zero product, check each root in the original.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: (x - 2) * (x - 5), 0, 7))],
                points=[(2, 0, "x=2"), (5, 0, "x=5"), (3.5, -2.25, "vertex")],
                xlim=(-1, 8), ylim=(-5, 6),
            ),
            "Graph of $y=(x-2)(x-5)$",
            "The roots $2$ and $5$ are the $x$-intercepts. The parabola crosses the axis there because the product is $0$.",
        )
        + solved(4, "Solve $(x-7)(x+2)=0$.",
                 ["$x=7$ or $x=-2$."],
                 "$x=7$ or $x=-2$", "", "Easy")
        + solved(5, "Solve $x^{2}+x-12=0$ by factoring.",
                 ["$(x+4)(x-3)=0$.",
                  "$x=-4$ or $x=3$."],
                 "$x=-4$ or $x=3$", "", "Medium")
        + solved(6, "Solve $3x^{2}-3x-6=0$ by factoring completely.",
                 ["GCF $3$: $3(x^{2}-x-2)=0$.",
                  "$(x-2)(x+1)=0$.",
                  "$x=2$ or $x=-1$."],
                 "$x=2$ or $x=-1$", "", "Hard"),
        ("Dividing both sides by $x$",
         "From $x^{2}=4x$, do not divide by $x$ and lose $x=0$. Bring to $x^{2}-4x=0$ and factor $x(x-4)=0$."),
        ("Zero on one side first",
         "Never apply zero product to $(x-1)(x+2)=3$. Expand, subtract $3$, then factor the new trinomial."),
        [
            "I can use the zero product property.",
            "I can solve a factored quadratic.",
            "I do not drop a GCF root.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Quadratic formula",
        [
            "The quadratic formula $x=\\dfrac{-b\\pm\\sqrt{b^{2}-4ac}}{2a}$ solves $ax^{2}+bx+c=0$ for any $a\\neq 0$. "
            "It is completing the square done once and for all on the general trinomial.",
            "The discriminant $D=b^{2}-4ac$ decides the real-root story: $D>0$ two distinct real roots, $D=0$ one "
            "real root (double), $D<0$ no real roots.",
            "Substitute $a,b,c$ carefully, including signs. For $x^{2}-4x-1=0$, $a=1$, $b=-4$, $c=-1$, so "
            "$-b=4$ and $D=16+4=20$.",
            "Simplify radicals when you can: $\\sqrt{20}=2\\sqrt{5}$, then cancel a common $2$ with the denominator "
            "if it divides the entire numerator.",
            "The formula still works when factoring would have been faster. Use factoring when the numbers are "
            "friendly; use the formula when they are not.",
            "Each real root is still an $x$-intercept of $y=ax^{2}+bx+c$. No real roots means the graph misses the "
            "axis.",
        ],
        "This is the general solving tool of the unit. Completing the square explains where it comes from; the "
        "formula is what you actually run on messy coefficients.",
        "Write $a,b,c$ with signs. Compute $D$. If $D<0$, stop (no real $x$). If $D\\geq 0$, plug into the formula "
        "and simplify.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: x * x - 4 * x - 1, -1, 6))],
                points=[(2 - 2.236, 0, ""), (2 + 2.236, 0, ""), (2, -5, "vertex")],
                xlim=(-2, 6), ylim=(-7, 6),
            ),
            "$y=x^{2}-4x-1$ with two irrational intercepts",
            "The formula gives $2\\pm\\sqrt{5}$. The graph crosses twice even though the roots are not integers.",
        )
        + solved(7, "Find the discriminant of $x^{2}+3x-4=0$.",
                 ["$9+16=25$."],
                 "$25$", "", "Easy")
        + solved(8, "Solve $x^{2}-2x-4=0$ using the formula.",
                 ["$D=4+16=20$.",
                  "$x=\\dfrac{2\\pm\\sqrt{20}}{2}=\\dfrac{2\\pm 2\\sqrt{5}}{2}=1\\pm\\sqrt{5}$."],
                 "$1\\pm\\sqrt{5}$", "", "Medium")
        + solved(9, "How many real solutions does $2x^{2}+x+5=0$ have?",
                 ["$D=1-40=-39<0$.",
                  "No real solutions."],
                 "none", "", "SAT"),
        ("Dropping the sign of $b$",
         "If $b=-6$, then $-b=6$. Writing $-6$ in the numerator is the most common formula error."),
        ("Compute $D$ on its own line",
         "A wrong discriminant poisons both roots. Box $D$ before you touch the $\\pm$."),
        [
            "I can identify $a,b,c$ with signs.",
            "I can use the discriminant to count real roots.",
            "I can simplify answers from the formula.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Completing the square (intro)",
        [
            "Completing the square rewrites $x^{2}+bx$ as $\\left(x+\\dfrac{b}{2}\\right)^{2}-\\left(\\dfrac{b}{2}\\right)^{2}$. "
            "You add and subtract the square of half the linear coefficient.",
            "On an equation: $x^{2}+6x-1=0$ becomes $x^{2}+6x=1$, then add $9$: $(x+3)^{2}=10$. Then $x+3=\\pm\\sqrt{10}$.",
            "On a function: $y=x^{2}+6x+2=(x+3)^{2}-9+2=(x+3)^{2}-7$. Now the vertex is $(-3,-7)$ without the "
            "$-b/(2a)$ formula.",
            "If $a\\neq 1$, factor $a$ out of the $x^{2}$ and $x$ terms first: $y=2x^{2}+8x+3=2(x^{2}+4x)+3$, then "
            "complete the square inside.",
            "This method is the origin of the quadratic formula and the path to vertex form. Algebra 2 will use it "
            "again for circles.",
            "The geometric picture is a literal square of side $x+\\dfrac{b}{2}$ plus a leftover constant — an area "
            "model with a missing corner filled in.",
        ],
        "Vertex form, max/min without calculus, and the quadratic formula all sit on this one algebraic move. "
        "Learning it as “add the square of half of $b$” is enough for Algebra 1.",
        "Move the constant, take half of $b$, square it, add to both sides (equation) or add and subtract (expression). "
        "Then write the squared binomial.",
        lesson_figure(
            _area_model("x^2", "3x", "3x", "9", top="x + 3", left="x + 3"),
            "Completing $x^{2}+6x$ into $(x+3)^{2}$",
            "The missing $9$ tile turns the L-shape $x^{2}+6x$ into a square of side $x+3$. You then subtract $9$ to stay equal.",
        )
        + solved(10, "What must you add to $x^{2}+8x$ to make a square?",
                 ["Half of $8$ is $4$, square $16$."],
                 "$16$", "", "Easy")
        + solved(11, "Complete the square: $x^{2}+10x+3$.",
                 ["$x^{2}+10x+25+3-25=(x+5)^{2}-22$."],
                 "$(x+5)^{2}-22$", "", "Medium")
        + solved(12, "Solve $x^{2}-4x-7=0$ by completing the square.",
                 ["$x^{2}-4x=7$. Add $4$: $(x-2)^{2}=11$.",
                  "$x-2=\\pm\\sqrt{11}$, so $x=2\\pm\\sqrt{11}$."],
                 "$x=2\\pm\\sqrt{11}$", "", "Hard"),
        ("Adding the square on only one side of an equation",
         "An equation is a balance. If you add $16$ to the left, add $16$ to the right."),
        ("Half, then square — not square, then half",
         "For $x^{2}+10x$, half of $10$ is $5$, then $25$. Halving $100$ would be the wrong order."),
        [
            "I can find the number that completes the square.",
            "I can rewrite a monic quadratic in vertex form.",
            "I can solve by completing the square.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Graphs vs roots",
        [
            "Roots of $ax^{2}+bx+c=0$ are $x$-intercepts of $y=ax^{2}+bx+c$. Seeing the graph is seeing the "
            "solutions (when they are real).",
            "Two crossings: two real roots, $D>0$. One touch point: double root, $D=0$. No crossing: no real roots, "
            "$D<0$. The vertex’s $y$-coordinate tells you which side of the axis the graph lives on.",
            "If you know the roots $r$ and $s$, you can write $y=a(x-r)(x-s)$. The stretch $a$ is then fixed by one "
            "more point, often the $y$-intercept.",
            "The axis of symmetry is the midpoint of the roots: $x=\\dfrac{r+s}{2}$. That is the same $x$ as $-b/(2a)$.",
            "A double root means the vertex sits on the $x$-axis. The graph kisses the axis and turns back.",
            "Matching a graph to an equation: read intercepts and the vertex, then choose among factored, vertex, "
            "or standard form.",
        ],
        "This lesson stitches the three algebraic methods to a picture so you can catch an extra or missing root "
        "before you submit an answer.",
        "Sketch intercepts and vertex. Count crossings. That count must match the discriminant and the factors you "
        "wrote.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda x: (x + 1) * (x - 4), -2, 6))],
                points=[(-1, 0, "root −1"), (4, 0, "root 4"), (1.5, -6.25, "vertex")],
                xlim=(-3, 7), ylim=(-8, 8),
            ),
            "$y=(x+1)(x-4)$ and its two intercepts",
            "The axis $x=1.5$ is halfway between $-1$ and $4$. Two crossings match two linear factors.",
        )
        + solved(13, "How many $x$-intercepts does $y=x^{2}+4$ have?",
                 ["$x^{2}=-4$ has no real $x$. Zero intercepts."],
                 "0", "", "Easy")
        + solved(14, "A parabola has intercepts $1$ and $5$ and passes through $(0,-5)$. Find $y=a(x-1)(x-5)$.",
                 ["$-5=a(0-1)(0-5)=5a$, so $a=-1$.",
                  "$y=-(x-1)(x-5)$."],
                 "$y=-(x-1)(x-5)$", "", "Medium")
        + solved(15, "Explain why $y=(x-3)^{2}$ has a double root and sketch the intercepts.",
                 ["$(x-3)^{2}=0$ only at $x=3$.",
                  "The vertex $(3,0)$ is on the axis; the graph touches once."],
                 "double root $x=3$; vertex on the $x$-axis", "", "SAT"),
        ("Counting the $y$-intercept as a root",
         "A root is where $y=0$. The $y$-intercept is where $x=0$. They coincide only if the graph through the "
         "origin."),
        ("Midpoint of the roots is the axis",
         "If your vertex $x$ is not halfway between the intercepts, one of those numbers is wrong."),
        [
            "I can match discriminant to number of intercepts.",
            "I can write $y=a(x-r)(x-s)$ from a graph.",
            "I can use the midpoint of the roots as the axis.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Projectile stories",
        [
            "A simple projectile height is $h(t)=at^{2}+bt+c$ with $a<0$ (gravity pulls down). In feet and seconds, "
            "$a$ is often $-16$; in meters, about $-4.9$.",
            "The constant $c=h(0)$ is the launch height. The coefficient $b$ relates to initial upward speed. The "
            "vertex time $t=-b/(2a)$ is when the object is highest.",
            "Landing (back at a stated height, often $0$) is a quadratic equation $h(t)=0$ or $h(t)=h_{\\text{ground}}$. "
            "Discard a negative time unless the model started before $t=0$.",
            "Maximum height is $h$ at the vertex, not the $y$-intercept and not the landing height.",
            "Units matter in the sentence you report: seconds for time, feet or meters for height. An answer of "
            "$t=2$ without “seconds” is incomplete in a story problem.",
            "The same algebra works for area and revenue quadratics: vertex for max, roots for break-even or a "
            "required area.",
        ],
        "This is the standard Algebra 1 application of everything in the unit: vertex for max height, factoring or "
        "formula for landing, graph for a sanity check that the motion goes up then down.",
        "Identify $a,b,c$. Vertex for max. Solve $h(t)=0$ for flight time, keep $t\\geq 0$. Substitute to report "
        "height with units.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", sample_curve(lambda t: -16 * t * t + 64 * t, 0, 4))],
                points=[(0, 0, "launch"), (2, 64, "max 64 ft"), (4, 0, "land")],
                xlim=(-0.5, 5), ylim=(-10, 80), xlab="t", ylab="h",
            ),
            "Height $h(t)=-16t^{2}+64t$",
            "Launch and landing at $h=0$. The vertex at $t=2$ s is the maximum $64$ ft.",
        )
        + solved(16, "For $h(t)=-16t^{2}+48t$, when does the ball land?",
                 ["$-16t(t-3)=0$, so $t=0$ or $t=3$. Landing at $3$ s."],
                 "$3$ s", "", "Easy")
        + solved(17, "Find the maximum height of $h(t)=-16t^{2}+48t$.",
                 ["$t=48/32=1.5$.",
                  "$h(1.5)=-16(2.25)+72=-36+72=36$ ft."],
                 "$36$ ft", "", "Medium")
        + solved(18, "A toy rocket is $h(t)=-16t^{2}+80t+6$. How long until it returns to $6$ ft (besides $t=0$)?",
                 ["Set $h=6$: $-16t^{2}+80t+6=6$, so $-16t^{2}+80t=0$.",
                  "$-16t(t-5)=0$, $t=5$ s."],
                 "$5$ s", "", "SAT"),
        ("Reporting the vertex time as the landing time",
         "The vertex is the top. Landing is a root of $h(t)=0$ (or the later time back at launch height)."),
        ("Keep $t\\geq 0$",
         "Quadratic equations often give a negative time. In a flight that starts at $t=0$, discard the negative."),
        [
            "I can find flight time from $h(t)=0$.",
            "I can find max height from the vertex.",
            "I can interpret $h(0)$ as launch height.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u7_questions()


# ===========================================================================
# UNIT 8: Data, Sequences & Modeling
# ===========================================================================

def _u8_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("A scatter plot of study hours versus test scores that rises left to right shows:",
         "a positive association",
         "Larger $x$ tends to go with larger $y$. That is a positive trend.",
         ["a negative association", "no association", "a vertical line only"]),
        ("A trend line is used to:", "summarize the overall linear pattern in a scatter",
         "It is a model through the cloud, not a requirement that every point sit on the line.",
         ["connect the first point to the last only", "replace the $y$-axis", "force every residual to 0"]),
        ("If the cloud of points slopes down, the association is:", "negative",
         "As $x$ increases, $y$ tends to decrease.",
         ["positive", "zero slope always", "exponential by default"]),
        ("Three points $(1,2)$, $(2,4)$, $(3,5)$ suggest a trend with slope about:", "1.5",
         "From first to last: $\\dfrac{5-2}{3-1}=1.5$. A trend line near slope $1.5$ fits the rise.",
         ["5", "0", "-1"]),
        ("A tight cloud around a line means:", "a stronger linear association",
         "Less scatter about the trend means the line describes the data more closely.",
         ["no association", "the slope must be 1", "an outlier is required"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("A residual is:", "actual $y$ minus predicted $y$",
         "Residual $= y-\\hat{y}$. Positive means the point sits above the trend line.",
         ["predicted minus actual", "the slope", "the $y$-intercept"]),
        ("If a point is at $(3,10)$ and the trend predicts $8$, the residual is:", "2",
         "$10-8=2$. The point is $2$ units above the line.",
         ["-2", "8", "3"]),
        ("An outlier in a scatter plot is:", "a point far from the overall cloud or trend",
         "It can pull a trend line toward itself. It is not merely the largest $x$.",
         ["any point on the $y$-axis", "the first data point", "a residual of 0"]),
        ("A residual of $-4$ means the actual $y$ is:", "4 below the predicted value",
         "Negative residual: the point is under the line.",
         ["4 above the line", "the slope is -4", "x is -4"]),
        ("Removing a high-leverage outlier far to the right often:", "changes the slope of the trend line",
         "Points with unusual $x$ can tilt the fitted line. Residuals of nearby points then change too.",
         ["must make the slope 0", "deletes the $y$-intercept forever", "has no possible effect"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("An arithmetic sequence has a constant:", "common difference",
         "You add $d$ each term. $3,7,11,15$ has $d=4$.",
         ["common ratio", "vertex", "discriminant"]),
        ("The next term of $5,8,11,14$ is:", "17",
         "Common difference $3$: $14+3=17$.",
         ["16", "20", "11"]),
        ("The $n$th term of an arithmetic sequence with first term $a_1$ and difference $d$ is:",
         "$a_n=a_1+(n-1)d$",
         "You add $d$ once for each step after the first term, so $n-1$ times.",
         ["$a_n=a_1\\cdot d^{n-1}$", "$a_n=a_1+nd$", "$a_n=n+d$"]),
        ("For $2,6,10,14$, the 10th term is:", "38",
         "$a_{10}=2+(10-1)\\cdot 4=2+36=38$.",
         ["40", "20", "14"]),
        ("Which list is arithmetic?", "$4,1,-2,-5$",
         "Common difference $-3$. The list $2,4,8,16$ is geometric.",
         ["$2,4,8,16$", "$1,4,9,16$", "$3,3,6,12$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("A geometric sequence has a constant:", "common ratio",
         "You multiply by $r$ each term. $3,6,12,24$ has $r=2$.",
         ["common difference", "slope", "residual"]),
        ("The next term of $5,10,20,40$ is:", "80",
         "Ratio $2$: $40\\times 2=80$.",
         ["45", "60", "50"]),
        ("The $n$th geometric term with first term $a_1$ and ratio $r$ is:", "$a_n=a_1 r^{n-1}$",
         "You multiply by $r$ once per step after the first term.",
         ["$a_n=a_1+(n-1)r$", "$a_n=a_1^{n}$", "$a_n=nr$"]),
        ("For $81,27,9,3$, the common ratio is:", "$\\dfrac{1}{3}$",
         "$27/81=1/3$. Decay geometric sequences have $0<|r|<1$.",
         ["$3$", "$-3$", "$54$"]),
        ("Which list is geometric?", "$2,6,18,54$",
         "Ratio $3$. The list $2,5,8,11$ is arithmetic.",
         ["$2,5,8,11$", "$1,2,4,7$", "$10,20,30,40$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("For $f(x)=\\begin{cases}x+1 & x\\leq 2\\\\ 2x-1 & x>2\\end{cases}$, $f(2)$ equals:", "3",
         "The first piece includes $x=2$: $2+1=3$. Do not use the second piece at the closed endpoint of the first.",
         ["5", "1", "4"]),
        ("Using the same $f$, $f(5)$ equals:", "9",
         "$5>2$, so $2(5)-1=9$.",
         ["6", "4", "10"]),
        ("A piecewise linear graph is made of:", "line segments (or rays) joined at breakpoints",
         "Each piece is linear on its interval. The whole graph need not be a single line.",
         ["a single parabola", "only vertical lines", "a scatter with no rule"]),
        ("If $g(x)=3$ for $x<0$ and $g(x)=x$ for $x\\geq 0$, then $g(-4)$ is:", "3",
         "$-4<0$, so the constant piece applies.",
         ["-4", "0", "4"]),
        ("A closed dot at a breakpoint means:", "that piece includes the endpoint",
         "Match $\\leq$ or $\\geq$ to a filled (closed) dot. A strict inequality uses an open dot.",
         ["the function is undefined there", "the slope is 0", "there is an outlier"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("A table with constant first differences is best fit by:", "a linear model",
         "Constant add-on $\\leftrightarrow$ line. Constant second differences suggest quadratic. Constant ratios suggest exponential.",
         ["an exponential model", "a circle", "no model"]),
        ("A table $2,4,8,16$ should be modeled as:", "exponential",
         "Common ratio $2$, not a common difference.",
         ["linear", "a residual of 2", "arithmetic with $d=2$"]),
        ("Constant second differences in $y$ (for equally spaced $x$) point to:", "a quadratic model",
         "Linear: constant first differences. Quadratic: constant second differences. Exponential: constant ratios.",
         ["a linear model", "no pattern", "a geometric sequence with $r=0$"]),
        ("“Grows by $6\\%$ each year” is:", "exponential",
         "Percent growth is a common ratio $1.06$. Adding $6$ each year would be linear.",
         ["linear with slope 6", "arithmetic with $d=0.06$", "a piecewise constant"]),
        ("If residuals for a line show a clear U-shape, you should consider:", "a quadratic (or other curved) model",
         "A patterned residual plot means the linear model missed curvature.",
         ["that the line is perfect", "deleting the $x$-axis", "an arithmetic sequence with $d=0$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The trend through $(0,1)$ and $(4,9)$ has slope:", "2",
         "$m=\\dfrac{9-1}{4-0}=2$, so $\\hat{y}=2x+1$.",
         ["8", "4", "1"]),
        ("Using $\\hat{y}=2x+1$, the residual at $(3,8)$ is:", "1",
         "Predicted $7$; actual $8$; residual $1$.",
         ["-1", "8", "3"]),
        ("The 7th term of $9,6,3,0,\\ldots$ is:", "-9",
         "$d=-3$, $a_7=9+6(-3)=9-18=-9$.",
         ["-6", "0", "7"]),
        ("Geometric $7,14,28$ has 5th term:", "112",
         "$7\\cdot 2^{4}=7\\cdot 16=112$.",
         ["56", "35", "21"]),
        ("For $h(x)=\\begin{cases} -x & x<0 \\\\ x & x\\geq 0 \\end{cases}$, $h(-3)$ is:", "3",
         "This is $|x|$. For $x<0$, $-(-3)=3$.",
         ["-3", "0", "9"]),
        ("Association that is neither clearly up nor down is called:", "little or no linear association",
         "The cloud may be random, vertical, or curved without a linear trend.",
         ["always exponential", "a common difference of 1", "undefined slope of data"]),
        ("$a_n=4n-1$ is:", "arithmetic with $d=4$",
         "Each increase of $n$ by $1$ adds $4$. First term $a_1=3$.",
         ["geometric with $r=4$", "quadratic", "a residual sequence"]),
        ("A residual plot randomly scattered about $0$ supports:", "that a linear model is reasonable",
         "No leftover pattern means the line captured the trend.",
         ["that you must switch to exponential", "that every residual is exactly 0", "that $x$ is time"]),
        ("The 1st term of a geometric sequence with $a_4=24$ and $r=2$ is:", "3",
         "$a_4=a_1 r^{3}=24$, so $a_1\\cdot 8=24$, $a_1=3$.",
         ["6", "12", "48"]),
        ("Evaluate $p(x)=\\begin{cases} 5 & x\\leq 1 \\\\ 2x+1 & x>1 \\end{cases}$ at $x=1$ and $x=4$.",
         "$5$ and $9$",
         "$p(1)=5$ (closed first piece). $p(4)=8+1=9$.",
         ["$3$ and $9$", "$5$ and $5$", "$2$ and $9$"]),
        ("Points $(1,1),(2,2),(3,8)$ are poorly fit by a line because:", "the third point breaks the constant difference",
         "Differences $1$ then $6$. A line expected another $+1$. An exponential $2^{x-1}$ fits $1,2,4$ better than $8$, still off. "
         "The jump to $8$ suggests a different model or an outlier at $(3,8)$.",
         ["slope is undefined", "x is not integer", "residuals cannot be computed"]),
        ("Common ratio of $16,8,4,2$ is:", "$\\dfrac{1}{2}$",
         "Each term is half the previous.",
         ["$2$", "$-8$", "$4$"]),
        ("A trend $\\hat{y}=-3x+20$ predicts that when $x$ increases by $1$, $y$ tends to:", "decrease by 3",
         "Slope is the predicted change in $y$ per unit $x$.",
         ["increase by 20", "decrease by 20", "stay 3"]),
        ("Arithmetic mean of terms $a_2$ and $a_4$ in $a_n=n+3$ equals $a_3$ because:",
         "in an arithmetic sequence, the middle of three equally spaced terms is the average",
         "$a_2=5$, $a_3=6$, $a_4=7$, and $(5+7)/2=6$.",
         ["it is geometric", "the residual is 3", "n must be even"]),
        ("Choosing $y=ab^{x}$ over $y=mx+b$ is reasonable when:", "ratios of consecutive $y$-values (equal $x$-steps) are nearly constant",
         "That is the exponential fingerprint. Constant differences would pick a line.",
         ["the scatter is a single point", "all residuals are 100", "x is negative only"]),
        ("An outlier at $(8,1)$ among points near the line $y=x$ will likely have residual about:", "-7",
         "Predicted $\\hat{y}\\approx 8$, actual $1$, residual $1-8=-7$.",
         ["8", "1", "0"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("SAT Stretch: Data $(1,3),(2,5),(3,7),(4,20)$. A line through the first three is $y=2x+1$. The residual at $x=4$ is:",
         "11",
         "The line predicts $9$ at $x=4$. Actual $20$, residual $11$. The point $(4,20)$ is an outlier relative to the first three.",
         ["20", "9", "-11"]),
        ("SAT Stretch: An arithmetic sequence has $a_3=11$ and $a_7=23$. Then $a_1$ equals:", "5",
         "Four steps from $a_3$ to $a_7$: $4d=12$, $d=3$. Then $a_1=a_3-2d=11-6=5$.",
         ["8", "11", "2"]),
        ("SAT Stretch: Geometric $a_1=5$, $a_n=5(1.2)^{n-1}$. After $4$ steps from $a_1$ (that is, at $n=5$), "
         "the term and the percent growth per step are:",
         "$a_5=10.368$; $20\\%$ per step",
         "Four multiplications by $1.2$: $5(1.2)^{4}=5\\cdot 2.0736=10.368$. The factor $1.2=1+0.20$ is $20\\%$ growth each term, "
         "not $1.2\\%$ and not $120\\%$.",
         ["$a_5=6$; $20\\%$ per step", "$a_5=10.368$; $1.2\\%$ per step", "$a_5=24$; $120\\%$ per step"]),
        ("SAT Stretch: $f(x)=\\begin{cases} 2x+1 & x<3 \\\\ 10-x & x\\geq 3 \\end{cases}$. The function is continuous at $3$ because:",
         "both pieces equal $7$ at $x=3$",
         "Left: $2(3)+1=7$. Right: $10-3=7$. The closed piece also equals $7$.",
         ["the slope is the same on both pieces", "f(3) is undefined", "2x+1 equals 10-x for all x"]),
        ("SAT Stretch: Equally spaced $x=0,1,2,3$ with $y=1,4,9,16$. The second differences are:", "2,2",
         "Four outputs give three first differences $3,5,7$, then two second differences $2,2$. "
         "A quadratic $y=(x+1)^{2}$ fits exactly. Four points never produce three second differences.",
         ["2,2,2", "3,5,7", "4,4,4"]),
        ("SAT Stretch: A linear fit $\\hat{y}=0.5x+2$ and an exponential $\\hat{y}=2(1.5)^{x}$ are compared at $x=6$. "
         "The exponential prediction is:", "22.78125",
         "$2(1.5)^{6}=2\\cdot(11.390625)=22.78125$. The line predicts $0.5(6)+2=5$. Context of rapid growth favors exponential.",
         ["5", "12", "9"]),
        ("SAT Stretch: Sequence $a_n=3n+2$ and $b_n=2\\cdot 3^{n-1}$. Which is larger at $n=5$?", "$b_5$",
         "$a_5=17$ and $b_5=2\\cdot 81=162$. The geometric term is larger.",
         ["$a_5$", "they are equal", "neither is defined"]),
        ("SAT Stretch: Points $(2,3),(4,7),(6,11)$ lie on a line. The residual of $(8,10)$ from that line is:", "-5",
         "Slope $\\dfrac{7-3}{4-2}=2$, so $y-3=2(x-2)$, $y=2x-1$. At $x=8$, predict $15$. Residual $10-15=-5$.",
         ["10", "15", "2"]),
        ("SAT Stretch: A piecewise parking fee is $\\$3$ for $0<t\\leq 2$ hours and $\\$3+2(t-2)$ after that. "
         "The smallest $t>2$ for which the fee is at least $\\$9$ is:", "5",
         "The two-hour fee is $\\$3$. For $t>2$ solve $3+2(t-2)\\geq 9$: $2(t-2)\\geq 6$, so $t-2\\geq 3$ and $t\\geq 5$. "
         "Check: at $t=5$, $3+2(3)=9$. At $t=4$, $3+2(2)=7<9$.",
         ["3", "2", "6"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    return qs


def build_unit8():
    title = "Algebra 1 Unit 8: Data, Sequences & Modeling"
    description = (
        "Scatter plots and trend lines, residuals and outliers, arithmetic sequences, an introduction to "
        "geometric sequences, piecewise linear models, and choosing linear versus exponential versus quadratic models."
    )
    concepts = [
        "Scatter plots and trend lines",
        "Residuals and fit",
        "Arithmetic sequences",
        "Geometric sequences intro",
        "Piecewise linear models",
        "Choose a model",
    ]

    c1 = concept_block(
        "1. Scatter plots and trend lines",
        [
            "A scatter plot displays paired numerical data as points $(x,y)$. It is a cloud, not a function you "
            "must already know. The cloud may rise, fall, curve, or look like noise.",
            "A positive association means larger $x$ tends to come with larger $y$. A negative association means "
            "larger $x$ tends to come with smaller $y$. No linear association looks like a formless blob or a "
            "vertical stripe.",
            "A trend line (line of best fit, in Algebra 1 often sketched by eye or fit to two representative points) "
            "summarizes a linear pattern. Most points will not sit exactly on it.",
            "Slope of the trend is the predicted change in $y$ per unit $x$, with units: points per hour of study, "
            "dollars per year, and so on.",
            "The intercept of a trend is the predicted $y$ when $x=0$. It may or may not make sense in context "
            "(negative height is a warning that $x=0$ is outside the data).",
            "Do not connect the dots like a broken polyline unless the context is a time series you are graphing as "
            "a path. A scatter of unrelated pairs should stay a cloud plus one trend.",
        ],
        "Later statistics courses formalize least-squares. Algebra 1 asks you to see direction, strength, and a "
        "reasonable line — the same skills used to choose linear models in lesson 6.",
        "Look at the cloud: up, down, or none? Fit a line through the middle of the band. Read slope with units. "
        "Ask whether $x=0$ is a meaningful intercept.",
        lesson_figure(
            svg_scatter(
                points=[(1, 2), (2, 2.6), (3, 3.8), (4, 4.1), (5, 5.3), (6, 5.9)],
                trend=(1, 1.9, 6, 6.0),
                xlabel="hours",
                ylabel="score",
            ),
            "Scatter of hours versus score with a dashed trend",
            "The cloud rises: a positive association. The dashed line summarizes the trend; individual points miss it by small residuals.",
        )
        + solved(1, "The points $(1,2)$, $(2,3)$, $(3,5)$ show which association?",
                 ["As $x$ increases, $y$ increases: positive association."],
                 "positive", "", "Easy")
        + solved(2, "A rising cloud includes $(1,2)$ and $(5,10)$. Using those two points as a trend, what slope do you get?",
                 [
                  svg_scatter(
                      points=[(1, 2), (2, 2.6), (3, 3.8), (4, 4.1), (5, 10), (6, 5.9)],
                      trend=(1, 2, 5, 10),
                      xlabel="x",
                      ylabel="y",
                  )
                  + " Cloud with a dashed trend through $(1,2)$ and $(5,10)$; other points miss the line.",
                  "Rise $10-2=8$ and run $5-1=4$.",
                  "Slope $m=\\dfrac{8}{4}=2$.",
                  "Those two points lie on $y=2x$; other cloud points will have nonzero residuals from that trend.",
                 ],
                 "slope $2$", "", "Medium")
        + solved(3, "Why might a trend intercept of $-4$ hours of sleep predicted at age $0$ be meaningless?",
                 ["Age $0$ may be outside the measured ages, and negative sleep is not a real amount.",
                  "The line can still be useful inside the data range even if the intercept is not a story value."],
                 "extrapolation / context", "", "SAT"),
        ("Connecting every point like a path",
         "A scatter of pairs is not automatically a time sequence. A trend line is one summary, not a polyline "
         "through every dot."),
        ("Read direction before slope",
         "Decide positive versus negative from the cloud first. Then estimate rise over run from two points in the "
         "middle of the band, not from the most extreme pair."),
        [
            "I can describe positive, negative, or no linear association.",
            "I can fit a reasonable trend line.",
            "I can interpret slope with units.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Residuals and fit",
        [
            "A residual is actual $y$ minus predicted $\\hat{y}$ from the trend: $y-\\hat{y}$. A point above the line "
            "has a positive residual; a point below has a negative residual.",
            "Residuals measure leftover error after the linear model has done its job. A good linear fit has residuals "
            "that look randomly scattered around $0$, with no obvious curve.",
            "An outlier is a point far from the cloud or far from the trend. It can have a huge residual and, if its "
            "$x$ is also unusual, it can tilt the entire fitted line (leverage).",
            "Always look at the scatter with the outlier marked, not a blank pair of axes. The picture is the "
            "definition: far from the pattern, not merely “the biggest number in the table.”",
            "Removing or keeping an outlier is a context decision (typo versus a real extreme). Algebra 1 asks you "
            "to see the effect, not to run a formal test.",
            "A residual plot (residuals versus $x$) that shows a U-shape is a warning that a line is the wrong "
            "family — lesson 6’s cue to consider quadratic or exponential.",
        ],
        "Without residuals, a trend line is just decoration. Residuals are how you argue that a line is good enough, "
        "or that a curved model is needed instead.",
        "Compute $\\hat{y}$ from the trend, subtract from $y$, and interpret the sign. Circle any point whose residual "
        "is far larger than the others — that is your outlier candidate.",
        lesson_figure(
            svg_scatter(
                points=[(1, 2.1), (2, 2.8), (3, 4.0), (4, 4.4), (6, 6.1)],
                trend=(1, 2.0, 6, 6.2),
                outlier=(5, 1.2),
                xlabel="x",
                ylabel="y",
            ),
            "A linear cloud with one marked outlier",
            "The orange point sits far below the dashed trend. Its residual is large and negative; it should not be mistaken for a typical point on a blank plane.",
        )
        + solved(4, "Trend $\\hat{y}=3x+1$. Residual at $(2,8)$?",
                 ["Predicted $7$. Residual $8-7=1$."],
                 "$1$", "", "Easy")
        + solved(5, "Trend $\\hat{y}=-x+10$. Residual at $(4,3)$?",
                 ["Predicted $6$. Residual $3-6=-3$. The point is below the line."],
                 "$-3$", "", "Medium")
        + solved(6, "Points follow $y=x$ closely except $(10,2)$. Describe the residual and the modeling risk.",
                 ["Predicted $10$, residual $2-10=-8$.",
                  "The point is an outlier. If included in a fit, it can flatten the slope."],
                 "residual $-8$; possible slope pull", "", "SAT"),
        ("Calling the largest $y$ an outlier automatically",
         "An outlier is far from the pattern. A large $y$ that sits on a steep trend may be perfectly typical."),
        ("Write actual minus predicted",
         "Mixing the order flips the sign and then “above/below” is backwards. Box $y-\\hat{y}$ every time."),
        [
            "I can compute a residual.",
            "I can interpret positive versus negative residuals.",
            "I can identify an outlier on a scatter with a trend.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Arithmetic sequences",
        [
            "An arithmetic sequence adds a constant $d$ (the common difference) each term. $7,10,13,16$ has $d=3$. "
            "The graph of term number versus term value is a set of collinear points — a discrete line.",
            "The explicit formula is $a_n=a_1+(n-1)d$. You add $d$ once for every step after the first term.",
            "A recursive view is $a_{n+1}=a_n+d$ with a given start. Both describe the same list.",
            "Finding $d$ from two terms: $d=\\dfrac{a_k-a_j}{k-j}$. Then walk backward to $a_1$ if needed.",
            "Arithmetic sequences are linear functions sampled at positive integers. Slope $d$ plays the role of "
            "the common difference.",
            "Word problems: “saves $\\$20$ more each month” is arithmetic. “earns $5\\%$ more of the current balance” "
            "is not — that is geometric.",
        ],
        "Recognizing add-versus-multiply is the same distinction as linear versus exponential in Unit 5 and in "
        "lesson 6 of this unit. Sequences are that idea with a discrete index $n$.",
        "Check differences between consecutive terms. If they match, write $a_n=a_1+(n-1)d$ and plug in $n$.",
        lesson_figure(
            number_line(0, 16, closed=[(3, "a1=3"), (7, "a2"), (11, "a3"), (15, "a4")]),
            "Arithmetic $3,7,11,15$ on a number line",
            "Equal steps of $+4$. The dots are equally spaced, which is the geometric meaning of a common difference.",
        )
        + solved(7, "Find the next two terms of $4,9,14,19$.",
                 ["$d=5$, so $24$ and $29$."],
                 "$24,29$", "", "Easy")
        + solved(8, "Find $a_{12}$ if $a_1=5$ and $d=-3$.",
                 ["$a_{12}=5+11(-3)=5-33=-28$."],
                 "$-28$", "", "Medium")
        + solved(9, "$a_4=20$ and $a_10=38$. Find $a_1$ and $d$.",
                 ["Six steps: $6d=18$, $d=3$.",
                  "$a_4=a_1+3d=20$, so $a_1+9=20$, $a_1=11$."],
                 "$a_1=11$, $d=3$", "", "Hard"),
        ("Using $a_n=a_1+nd$",
         "That extra $+d$ off-by-one is common. There are $n-1$ steps from $a_1$ to $a_n$."),
        ("Write $d$ with its sign",
         "A decreasing sequence has negative $d$. Dropping the minus turns $17,14,11$ into growth."),
        [
            "I can find a common difference.",
            "I can use $a_n=a_1+(n-1)d$.",
            "I can recover $a_1$ from two later terms.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Geometric sequences intro",
        [
            "A geometric sequence multiplies by a constant $r$ (the common ratio) each term. $3,6,12,24$ has $r=2$. "
            "The discrete graph sits on an exponential curve $y=a_1 r^{n-1}$.",
            "The explicit formula is $a_n=a_1 r^{n-1}$. The recursive form is $a_{n+1}=r a_n$.",
            "Find $r$ by dividing a term by the previous term (when that previous term is not $0$). Signs: $r$ may "
            "be negative, which produces an alternating sequence.",
            "Percent growth is geometric: $r=1+p$ for growth, $r=1-p$ for decay. That is Unit 5’s $a(1\\pm p)^{t}$ "
            "with integer $t=n-1$.",
            "A sequence can be arithmetic or geometric, but not both (except in trivial constant cases). Checking "
            "both differences and ratios prevents a wrong family.",
            "This is an introduction: Algebra 2 will add finite geometric sums. Here you only need terms, $r$, and "
            "the contrast with arithmetic.",
        ],
        "Exponential models in the last lesson are continuous cousins of geometric sequences. Mixing $r$ with $d$ "
        "is mixing multiply with add — the same error as treating percent growth as a line.",
        "Divide consecutive terms to get $r$. Write $a_n=a_1 r^{n-1}$. Compare with an arithmetic alternative before "
        "you commit.",
        lesson_figure(
            xy_graph(
                curves=[("#94a3b8", sample_curve(lambda n: 3 * (2 ** (n - 1)), 1, 5))],
                points=[(1, 3, "a1=3"), (2, 6, "6"), (3, 12, "12"), (4, 24, "24")],
                xlim=(0, 5.5), ylim=(-1, 28), xlab="n", ylab="a_n",
            ),
            "Geometric $3,6,12,24$ as points on $y=3\\cdot 2^{n-1}$",
            "Equal ratios, not equal gaps. The heights double; the points ride an exponential curve.",
        )
        + solved(10, "The sequence $80,40,20$ continues with a constant ratio. Find that ratio and the next term.",
                 [
                  xy_graph(
                      curves=[("#94a3b8", sample_curve(lambda n: 80 * (0.5 ** (n - 1)), 1, 4.2))],
                      points=[(1, 80, "80"), (2, 40, "40"), (3, 20, "20"), (4, 10, "next")],
                      xlim=(0, 5), ylim=(-5, 90), xlab="n", ylab="a_n",
                  )
                  + " Discrete terms $80,40,20,10$ on an exponential curve, not a shaded pie.",
                  "Common ratio $r=40/80=20/40=1/2$.",
                  "Next term: $20\\cdot\\dfrac{1}{2}=10$.",
                  "Check the fourth term from the explicit formula: $80\\cdot\\left(\\dfrac{1}{2}\\right)^{3}=10$.",
                 ],
                 "$r=1/2$; next $10$", "", "Easy")
        + solved(11, "Find $a_6$ if $a_1=2$ and $r=3$.",
                 ["$a_6=2\\cdot 3^{5}=2\\cdot 243=486$."],
                 "$486$", "", "Medium")
        + solved(12, "A salary of $\\$40{,}000$ grows $5\\%$ per year. Write $a_n$ for year $n$ (year 1 is the start).",
                 ["$r=1.05$.",
                  "$a_n=40000(1.05)^{n-1}$."],
                 "$40000(1.05)^{n-1}$", "", "SAT"),
        ("Subtracting to find a “ratio”",
         "$24-12=12$ is a difference, not a ratio. Geometric uses division: $24/12=2$."),
        ("Count $n-1$ multiplications",
         "From $a_1$ to $a_6$ there are five multiplications by $r$, not six. The exponent is $n-1$."),
        [
            "I can find a common ratio.",
            "I can use $a_n=a_1 r^{n-1}$.",
            "I can connect percent growth to $r=1+p$.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Piecewise linear models",
        [
            "A piecewise linear function uses different linear rules on different intervals of $x$. Parking fees, "
            "tax brackets, and “$y=|x|$” are built this way.",
            "To evaluate, first decide which piece owns the input. The inequality on the piece — especially whether "
            "the breakpoint is $\\leq$ or $<$ — decides $f$ at the joint.",
            "Graph each piece only on its interval. At a breakpoint, use a closed dot for the included piece and an "
            "open dot for the excluded one. If both pieces agree, the graph is continuous there.",
            "Absolute value $y=|x|$ is piecewise: $y=-x$ for $x<0$ and $y=x$ for $x\\geq 0$. Two rays meeting at "
            "the origin.",
            "A story with a change of rate — “$\\$20$ plus $\\$3$ per mile after the first $5$ miles” — is piecewise. "
            "Write the two formulas and the mile cutover carefully.",
            "Piecewise models are still linear on each piece, so slope and intercept skills from Unit 3 apply locally.",
        ],
        "Real fee schedules are almost never a single line. Piecewise linear is the Algebra 1 way to be honest about "
        "a change in rate without jumping to a curve.",
        "Circle the interval that contains $x$, evaluate only that formula, and graph with open/closed dots at "
        "breakpoints.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", [(-2, 1), (1, 1)]),
                    ("#4f46e5", [(1, 1), (4, 7)]),
                ],
                points=[(1, 1, "(1,1)")],
                xlim=(-3, 5), ylim=(-1, 8),
            ),
            "Piecewise $y=1$ for $x\\leq 1$ and $y=2x-1$ for $x>1$",
            "A horizontal segment meets a slope-$2$ ray at $(1,1)$. Each piece is linear; the whole graph is not one line.",
        )
        + solved(13, "For $f(x)=2x$ when $x\\leq 0$ and $f(x)=x+1$ when $x>0$, find $f(-3)$.",
                 ["$-3\\leq 0$, so $f(-3)=-6$."],
                 "$-6$", "", "Easy")
        + solved(14, "Using the same $f$, find $f(0)$ and $f(4)$.",
                 ["$f(0)=0$ from the first piece.",
                  "$f(4)=5$ from the second."],
                 "$0$ and $5$", "", "Medium")
        + solved(15, "A taxi charges $\\$3$ for the first mile and $\\$2$ per additional mile. Write $C(m)$ for $m\\geq 1$.",
                 ["For $1\\leq m\\leq 1$ the cost is $3$. For $m>1$, $C=3+2(m-1)=2m+1$.",
                  "As a single expression for $m\\geq 1$: $C(m)=3+2(m-1)$ which simplifies to $2m+1$.",
                  "If the first mile is special, piecewise: $3$ at $m=1$, and $2m+1$ for $m>1$ (which also equals $3$ at $m=1$)."],
                 "$C(m)=3+2(m-1)=2m+1$ for $m\\geq 1$", "", "SAT"),
        ("Evaluating both pieces and averaging",
         "Exactly one rule applies. At a closed endpoint, use the piece whose inequality includes that $x$."),
        ("Draw open and closed dots",
         "A graph without endpoint dots hides whether $f(3)$ is $7$ or $8$. Match the inequality."),
        [
            "I can choose the correct piece for an input.",
            "I can graph segments with open/closed endpoints.",
            "I can write a two-rate fee as piecewise linear.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Choose a model",
        [
            "Algebra 1’s modeling menu is short: linear (constant difference / constant slope), exponential "
            "(constant ratio / percent), quadratic (constant second differences / a vertex), or piecewise linear "
            "(a change of rate).",
            "From a table with equally spaced $x$: compute first differences, second differences, and ratios. One of "
            "those rows being nearly constant picks the family.",
            "From a story: “adds $30$” is linear, “grows $30\\%$” is exponential, “area of a square with side $x$” "
            "is quadratic, “rate changes after $2$ hours” is piecewise.",
            "From a residual picture: random leftovers support the model you tried. A U-shape after a linear fit "
            "suggests quadratic. A fan that grows suggests exponential.",
            "Goodness of fit in Algebra 1 is informal: smaller residuals, no leftover pattern, and a context that "
            "matches. Do not overfit four points with a degree-$10$ story.",
            "After you choose, write the formula, name the units, and say where the model should not be used "
            "(outside the data, after a policy change, below $t=0$).",
        ],
        "Choosing a model is the capstone of Algebra 1 modeling: every previous unit supplies a family, and you pick "
        "which family the new situation actually is.",
        "Story first, then table diagnostics (differences versus ratios), then a residual check. Write the formula "
        "only after the family is chosen.",
        lesson_figure(
            svg_scatter(
                points=[(1, 1.1), (2, 2.0), (3, 4.1), (4, 8.2), (5, 15.8)],
                trend=(1, 0.5, 5, 12),
                xlabel="t",
                ylabel="P",
            ),
            "A cloud that a line (dashed) underfits",
            "Heights roughly double: an exponential model beats the straight trend. Choosing a line here would leave a curved residual pattern.",
        )
        + solved(16, "Table $x=1,2,3,4$ with $y=10,13,16,19$. Which family?",
                 ["First differences $3,3,3$. Linear, $y=3x+7$."],
                 "linear", "", "Easy")
        + solved(17, "Table $y=5,10,20,40$. Which family?",
                 ["Ratios $2,2,2$. Exponential."],
                 "exponential", "", "Medium")
        + solved(18, "A ball’s height versus time looks like an arch. First differences of equally spaced times are "
                 "not constant, but second differences are. Which model?",
                 ["Constant second differences: quadratic (projectile parabola).",
                  "A line would have constant first differences; exponential would have constant ratios."],
                 "quadratic", "", "SAT"),
        ("Picking exponential because the graph “goes up”",
         "Lines go up too. The diagnostic is how they go up: add versus multiply, or first versus second differences."),
        ("Run all three checks on a table",
         "Write a differences row, a second-differences row, and a ratios row. The nearly constant row names the "
         "model."),
        [
            "I can use differences and ratios to choose a family.",
            "I can match a story to linear, exponential, quadratic, or piecewise.",
            "I can use residual shape as a warning.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u8_questions()


def build_master():
    units = [('Expressions, Properties & Real Numbers', ['The real number line and subsets', 'Properties of operations', 'Simplify expressions', 'Absolute value as distance', 'Order of operations with grouping', 'Translate words to algebra']), ('Linear Equations & Inequalities', ['One-step and two-step equations', 'Multi-step with distribute', 'Variables on both sides', 'Inequalities and number-line graphs', 'Compound inequalities', 'Absolute-value equations']), ('Linear Functions & Graphs', ['Slope as rate of change', 'Slope-intercept form', 'Point-slope and standard form', 'Parallel and perpendicular', 'Intercepts and graphing', 'Function notation for lines']), ('Systems of Linear Equations', ['Graphical solutions', 'Substitution', 'Elimination', 'No solution and infinitely many', 'Systems of inequalities', 'Word-problem systems']), ('Exponents & Exponential Intro', ['Product and quotient rules', 'Power rules and zero/negative', 'Scientific notation', 'Exponential growth graphs', 'Exponential decay graphs', 'Compare linear vs exponential']), ('Polynomials & Factoring', ['Add and subtract polynomials', 'Multiply polynomials', 'GCF and grouping', 'Trinomials a=1', 'Trinomials a>1 and special products', 'Factor completely']), ('Quadratic Functions & Equations', ['Parabolas and vertex', 'Factoring to solve', 'Quadratic formula', 'Completing the square (intro)', 'Graphs vs roots', 'Projectile stories']), ('Data, Sequences & Modeling', ['Scatter plots and trend lines', 'Residuals and fit', 'Arithmetic sequences', 'Geometric sequences intro', 'Piecewise linear models', 'Choose a model'])]
    items = "".join(f"<li>Unit {i} — {u[0]}</li>" for i, u in enumerate(units, 1))
    return (
        f"<h1>Algebra 1 Complete</h1>"
        f"<p><strong>For:</strong> <strong>Grade 9 Algebra 1</strong>. Eight deep units, each with six concepts, "
        "worked examples with matching diagrams, 5 quizzes per concept, and a 25-problem stretch finale.</p>"
        f"{page_break()}"
        "<h2>The eight units</h2>"
        f"<ol>{items}</ol>"
    )
