"""Deep Algebra 1 curriculum builders (units 1–4)."""
from __future__ import annotations

from curriculum_kit import (
    lesson_figure, svg_plane, svg_circle, svg_triangle, svg_rect, svg_balance,
    svg_number_line, svg_scatter, svg_parabola,
)
from hs_curriculum import (
    concept_block, solved, practice_slots, unit_shell, mq,
    xy_graph, sample_curve, number_line,
)
from .common import AUDIENCE, STRETCH_LABEL


def _seg(m, b, x0, x1):
    return [(x0, m * x0 + b), (x1, m * x1 + b)]


def _nest_ops():
    return (
        '<svg viewBox="0 0 340 90" width="100%" style="max-width:340px" role="img">'
        '<rect x="8" y="18" width="70" height="40" rx="8" fill="#dbeafe" stroke="#1e3a8a"/>'
        '<text x="43" y="44" text-anchor="middle" font-size="13">2+3</text>'
        '<text x="88" y="44" font-size="16">→</text>'
        '<rect x="108" y="18" width="80" height="40" rx="8" fill="#fde68a" stroke="#92400e"/>'
        '<text x="148" y="44" text-anchor="middle" font-size="13">× 4</text>'
        '<text x="198" y="44" font-size="16">→</text>'
        '<rect x="218" y="18" width="50" height="40" rx="8" fill="#dbeafe" stroke="#1e3a8a"/>'
        '<text x="243" y="44" text-anchor="middle" font-size="13">20</text>'
        '<text x="276" y="44" font-size="16">→</text>'
        '<rect x="294" y="18" width="38" height="40" rx="8" fill="#dcfce7" stroke="#166534"/>'
        '<text x="313" y="44" text-anchor="middle" font-size="13">−1</text>'
        "</svg>"
    )


# ===========================================================================
# UNIT 1: Expressions, Properties & Real Numbers
# ===========================================================================

def _u1_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("Which of these numbers is irrational?", "$\\sqrt{2}$",
         "An irrational number cannot be written as a ratio of integers. $\\sqrt{2}$ does not terminate or repeat, "
         "while $0.25=\\dfrac{1}{4}$, $\\sqrt{16}=4$, and $-7$ are all rational.",
         ["$0.25$", "$\\sqrt{16}$", "$-7$"]),
        ("On the real number line, the point halfway between $-4$ and $2$ is located at:", "$-1$",
         "The midpoint of two numbers is their average: $\\dfrac{-4+2}{2}=\\dfrac{-2}{2}=-1$.",
         ["$1$", "$-3$", "$0$"]),
        ("Every whole number is also which of the following?", "an integer",
         "The whole numbers $\\{0,1,2,\\ldots\\}$ sit inside the integers $\\{\\ldots,-2,-1,0,1,2,\\ldots\\}$. "
         "They are not all natural if you take naturals as starting at $1$, and they are not all irrational.",
         ["an irrational number", "a negative integer", "a natural number starting at 1"]),
        ("$\\sqrt{36}$ belongs on which of these lists?", "rational and integer",
         "$\\sqrt{36}=6$, which is an integer and therefore also rational. It is not irrational.",
         ["irrational only", "natural but not integer", "not a real number"]),
        ("A number that is an integer but not a whole number is:", "$-5$",
         "Whole numbers are $0,1,2,\\ldots$. Negative integers such as $-5$ are integers but not whole numbers. "
         "$0$ and $8$ are whole, and $2.5$ is not an integer.",
         ["$0$", "$8$", "$2.5$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The equation $a+b=b+a$ is an example of the:", "commutative property of addition",
         "Commutative means order can swap. Addition of real numbers may be reordered without changing the sum.",
         ["associative property of addition", "distributive property", "identity property of addition"]),
        ("Rewriting $3(x+4)$ as $3x+12$ uses the:", "distributive property",
         "The distributive property says $a(b+c)=ab+ac$. Here $3$ multiplies both $x$ and $4$.",
         ["commutative property of multiplication", "associative property of multiplication", "zero property"]),
        ("Which rewrite is justified by the associative property of addition?", "$(7+2)+x=7+(2+x)$",
         "Associative lets you regroup with the same order: $(a+b)+c=a+(b+c)$. The numbers themselves do not swap places.",
         ["$7+x=x+7$", "$7(2+x)=14+7x$", "$7+0=7$"]),
        ("Because $5\\cdot 1=5$ for every real $5$, the number $1$ is the:", "multiplicative identity",
         "The multiplicative identity is $1$, since multiplying by $1$ leaves a number unchanged. "
         "The additive identity is $0$.",
         ["additive identity", "multiplicative inverse of 5", "additive inverse of 5"]),
        ("Which equation shows a multiplicative inverse pair?", "$\\dfrac{3}{4}\\cdot\\dfrac{4}{3}=1$",
         "Two numbers are multiplicative inverses when their product is $1$. $\\dfrac{3}{4}$ and $\\dfrac{4}{3}$ multiply to $1$.",
         ["$\\dfrac{3}{4}+\\dfrac{4}{3}=1$", "$\\dfrac{3}{4}\\cdot 0=0$", "$\\dfrac{3}{4}-\\dfrac{4}{3}=0$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Combine like terms: $7x-2x+5$.", "$5x+5$",
         "The $x$-terms combine: $7x-2x=5x$. The constant $5$ has no like partner, so the simplified form is $5x+5$.",
         ["$5x$", "$9x+5$", "$7x-7$"]),
        ("Which expression is equivalent to $4(2y-3)+y$?", "$9y-12$",
         "Distribute first: $8y-12+y$. Then combine like terms: $9y-12$.",
         ["$8y-3+y$", "$8y-12$", "$9y-3$"]),
        ("Simplify $3a-5(a-2)$.", "$-2a+10$",
         "Distribute the $-5$: $3a-5a+10$. Combine: $-2a+10$. The minus in front of $5$ flips the sign of both terms inside.",
         ["$-2a-10$", "$8a-10$", "$3a-5a-2$"]),
        ("The expression $2(x+4)+3(x-1)$ simplifies to:", "$5x+5$",
         "$2x+8+3x-3=5x+5$. Add the $x$-terms and the constants separately.",
         ["$5x+7$", "$6x+3$", "$5x-5$"]),
        ("After combining like terms, $x^2+4x-x^2+1$ equals:", "$4x+1$",
         "The $x^2$ terms cancel: $x^2-x^2=0$. Left behind are $4x+1$.",
         ["$2x^2+4x+1$", "$4x$", "$x^2+4x+1$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("$| -8 |$ equals:", "8",
         "Absolute value is distance from $0$ on the number line, which is never negative. $|-8|=8$.",
         ["-8", "0", "16"]),
        ("The distance between $-3$ and $5$ on the number line is:", "8",
         "Distance is $|5-(-3)|=|8|=8$. Subtracting without the absolute value would incorrectly suggest $-8$.",
         ["2", "-8", "15"]),
        ("If $|x|=7$, then $x$ is:", "$7$ or $-7$",
         "Distance $7$ from $0$ means the point can sit at $7$ or at $-7$.",
         ["$7$ only", "$-7$ only", "$0$"]),
        ("$|4-9|$ is equal to:", "5",
         "First subtract: $4-9=-5$. Then take absolute value: $|-5|=5$.",
         ["-5", "13", "4"]),
        ("The equation $|x-2|=0$ has solution:", "$x=2$",
         "Distance from $2$ is $0$ only when you are standing at $2$ itself.",
         ["$x=0$", "$x=-2$", "no real solution"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Evaluate $3+4\\times 2$.", "11",
         "Multiplication happens before addition: $4\\times 2=8$, then $3+8=11$. Adding first would wrongly give $14$.",
         ["14", "10", "24"]),
        ("What is $2(5+3)^2$?", "128",
         "Parentheses first: $5+3=8$. Then the exponent: $8^2=64$. Then multiply: $2\\times 64=128$.",
         ["64", "32", "100"]),
        ("Evaluate $18\\div 3\\times 2$.", "12",
         "Division and multiplication share a rank, so work left to right: $18\\div 3=6$, then $6\\times 2=12$.",
         ["3", "27", "8"]),
        ("Simplify $8-2(3+1)$.", "0",
         "Parentheses: $3+1=4$. Multiply: $2\\times 4=8$. Subtract: $8-8=0$.",
         ["6", "24", "4"]),
        ("The value of $-3^2$ is:", "-9",
         "The exponent binds to $3$ first: $3^2=9$, then the unary minus gives $-9$. Contrast $(-3)^2=9$.",
         ["9", "6", "-6"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("“Five less than twice a number $n$” translates to:", "$2n-5$",
         "Twice a number is $2n$. Five less than that quantity subtracts $5$ afterward: $2n-5$, not $5-2n$.",
         ["$5-2n$", "$2n+5$", "$5n-2$"]),
        ("The phrase “the product of $x$ and $7$, increased by $3$” is:", "$7x+3$",
         "Product means multiply: $7x$. Increased by $3$ adds $3$ after the product.",
         ["$7(x+3)$", "$x+7+3$", "$7x-3$"]),
        ("“The quotient of a number $k$ and $4$” is written:", "$\\dfrac{k}{4}$",
         "Quotient of $k$ and $4$ means $k$ divided by $4$. The order in the English phrase matches the order of division.",
         ["$\\dfrac{4}{k}$", "$k-4$", "$4k$"]),
        ("Which equation matches “three more than a number is $11$”?", "$n+3=11$",
         "Three more than a number is $n+3$, and “is $11$” sets that equal to $11$.",
         ["$3n=11$", "$n-3=11$", "$3-n=11$"]),
        ("“Twice the sum of $x$ and $6$” is:", "$2(x+6)$",
         "The word sum groups $x$ and $6$ first. Twice that sum multiplies the grouped quantity, so $2(x+6)$, not $2x+6$.",
         ["$2x+6$", "$2x+12$", "$x+12$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Which number is rational but not an integer?", "$\\dfrac{2}{3}$",
         "$\\dfrac{2}{3}$ is a ratio of integers, so it is rational, but it is not a whole integer. "
         "$\\sqrt{4}=2$ is an integer, $\\pi$ is irrational, and $-8$ is an integer.",
         ["$\\sqrt{4}$", "$\\pi$", "$-8$"]),
        ("Simplify $6-4(2-5)$.", "18",
         "Parentheses: $2-5=-3$. Then $-4(-3)=+12$. Then $6+12=18$. A sign error on the distributed negative is common.",
         ["-6", "2", "30"]),
        ("Which property allows $2(5x)$ to be rewritten as $(2\\cdot 5)x$?", "associative property of multiplication",
         "Associative regroups factors: $a(bc)=(ab)c$. Here the $2$ and $5$ may be multiplied first.",
         ["commutative property of addition", "distributive property", "identity property of multiplication"]),
        ("The distance from $-6$ to $1$ equals the distance from $1$ to what other number?", "8",
         "Distance is $|1-(-6)|=7$. The other point $7$ units from $1$, on the opposite side from $-6$, is $1+7=8$.",
         ["-5", "7", "-8"]),
        ("Which expression matches “four times the difference of a number and $9$”?", "$4(n-9)$",
         "Difference of a number and $9$ is $n-9$. Four times that grouped difference is $4(n-9)$.",
         ["$4n-9$", "$9-4n$", "$4(9-n)$"]),
        ("Evaluate $5^2-3\\times 4+1$.", "14",
         "Exponent first: $25$. Then multiply: $12$. Then left to right: $25-12+1=14$.",
         ["17", "8", "26"]),
        ("Which factored expression equals $3x+3x+3x$?", "$9x$",
         "Three copies of $3x$ add to $9x$. The power $3x^3$ would multiply, not add, and $x+x+x$ is only $3x$.",
         ["$3x^3$", "$x+x+x$", "$3+x+3+x+3+x$"]),
        ("If a number is $4$ units from $-1$ on the number line, which pair of values is possible?", "$-5$ and $3$",
         "Solve $|x-(-1)|=4$, so $|x+1|=4$. Then $x+1=4$ or $x+1=-4$, giving $x=3$ or $x=-5$.",
         ["$-4$ and $4$", "$0$ and $4$", "$-1$ and $4$"]),
        ("Which statement is always true for real numbers $a$ and $b$?", "$a+(-a)=0$",
         "Every real has an additive inverse: $a+(-a)=0$. The other claims fail in general ($a-b$ need not equal $b-a$).",
         ["$a-b=b-a$", "$a\\div b=b\\div a$", "$a^2=a$"]),
        ("Translate and simplify: “a number $x$, plus twice that number, minus $4$.”", "$3x-4$",
         "The phrase is $x+2x-4$, which combines to $3x-4$.",
         ["$x+2-4$", "$2x-4$", "$x^2-4$"]),
        ("Which of $-\\sqrt{9}$, $\\sqrt{-9}$, and $\\sqrt{9}$ is not a real number?", "$\\sqrt{-9}$",
         "Square roots of negative numbers are not real. $-\\sqrt{9}=-3$ and $\\sqrt{9}=3$ are real.",
         ["$-\\sqrt{9}$", "$\\sqrt{9}$", "both $-\\sqrt{9}$ and $\\sqrt{9}$"]),
        ("Using distribution, $-(2x-7)$ equals:", "$-2x+7$",
         "The leading minus distributes to both terms: $-2x-(-7)=-2x+7$.",
         ["$-2x-7$", "$2x-7$", "$-2x+7x$"]),
        ("$|3|-|-10|$ equals:", "-7",
         "$|3|=3$ and $|-10|=10$, so $3-10=-7$. Absolute values are taken first, then subtracted.",
         ["13", "7", "-13"]),
        ("The expression $2+3\\times(4-1)^2$ evaluates to:", "29",
         "Parentheses: $3$. Square: $9$. Multiply: $27$. Add: $29$.",
         ["45", "11", "50"]),
        ("“The square of the sum of $n$ and $5$” is:", "$(n+5)^2$",
         "Sum first, then square the grouped result. $n^2+5$ would square only $n$, and $n^2+25$ drops the middle term.",
         ["$n^2+5$", "$n^2+25$", "$n+5^2$"]),
        ("Which subset relationship is correct?", "naturals $\\subset$ integers $\\subset$ rationals $\\subset$ reals",
         "Each listed set sits inside the next. Irrationals are real but not rational, so they do not belong in that chain as a middle set.",
         ["reals $\\subset$ rationals", "integers $\\subset$ naturals", "irrationals $\\subset$ rationals"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("SAT Stretch: Which expression is equivalent to $3(2x-5)-(x-4)+2(x+1)$?", "$7x-9$",
         "Distribute: $6x-15-x+4+2x+2$. Combine $x$-terms: $6x-x+2x=7x$. Combine constants: $-15+4+2=-9$. Result $7x-9$. "
         "A frequent trap is flipping only one sign after the minus in front of $(x-4)$.",
         ["$7x-17$", "$5x-9$", "$7x-11$"]),
        ("SAT Stretch: Points $A=-7$ and $B=5$ lie on the real line. Point $C$ lies between them and is twice as far "
         "from $A$ as from $B$. The coordinate of $C$ is:", "1",
         "Let $C=x$ with $-7<x<5$ and $|x+7|=2|x-5|$. Between the points this is $x+7=2(5-x)$, so $x+7=10-2x$, hence $3x=3$ "
         "and $x=1$. Distances: $1-(-7)=8$ and $5-1=4$, and $8=2\\cdot 4$.",
         ["-3", "-1", "0"]),
        ("SAT Stretch: For which real $t$ is $|t-4|+|t+2|$ equal to $6$?", "every $t$ with $-2\\leq t\\leq 4$",
         "On the number line the sum of distances to $4$ and to $-2$ is the distance between those points, which is $6$, "
         "exactly when $t$ lies on the segment joining them. Outside that segment the sum is strictly larger than $6$.",
         ["only $t=1$", "only $t=4$ and $t=-2$", "no real $t$"]),
        ("SAT Stretch: Which property sequence correctly justifies "
         "$4(x+3)+2x=4x+12+2x=6x+12=6(x+2)$?",
         "distribute, combine like terms, then factor",
         "First $4$ is distributed. Then $4x$ and $2x$ combine. Then $6$ is factored from $6x+12$. "
         "The commutative property is not the main move here.",
         ["commutative, then inverse, then identity", "associative only", "zero product, then inverse"]),
        ("SAT Stretch: An expression is “three less than the product of $5$ and the quantity two more than $n$.” "
         "Which simplified form is correct?", "$5n+7$",
         "Two more than $n$ is $n+2$. Product with $5$ is $5(n+2)=5n+10$. Three less: $5n+10-3=5n+7$. "
         "Writing $5n+2-3$ drops the distribution on the $2$.",
         ["$5n-3$", "$5(n+2-3)$", "$3-5(n+2)$"]),
        ("SAT Stretch: Evaluate $\\left(2-7\\right)^2-4\\cdot 3^2\\div 6$.", "19",
         "Parentheses first: $2-7=-5$, and $(-5)^2=25$. Then $3^2=9$, so $4\\cdot 9=36$, then $36\\div 6=6$. "
         "Finish with $25-6=19$.",
         ["13", "7", "-11"]),
        ("SAT Stretch: A number $x$ satisfies $x^{2}=12$ and $x<0$. Which statement is complete and correct?",
         "$x=-2\\sqrt{3}$, irrational and real, not an integer",
         "$x=-\\sqrt{12}=-2\\sqrt{3}$. That is a negative irrational real. It is not an integer or a ratio of integers. "
         "$-\\sqrt{16}=-4$ would have been an integer; $\\sqrt{12}$ itself is positive, so it is not this $x$.",
         ["$x=2\\sqrt{3}$, a positive integer", "$x=-\\sqrt{12}$ is not real", "$x=-4$ because $12$ is near $16$"]),
        ("SAT Stretch: Let $p$ be the additive inverse of $3x-8$. Then $2p+(6x-16)$ equals:", "0",
         "$6x-16=2(3x-8)$, so $2p+(6x-16)=2\\bigl(p+(3x-8)\\bigr)$. By definition $p+(3x-8)=0$, hence the whole expression is $0$. "
         "The multiplicative inverse would instead satisfy $p(3x-8)=1$.",
         ["$6x-16$", "$2$", "$3x-8$"]),
        ("SAT Stretch: Compare $A=|2-5|^{2}-|1-8|+(-3)^{2}$ with $B=3\\bigl(4-1\\bigr)$. Which is larger, and by how much?",
         "$A$ is larger by $2$",
         "$|2-5|=3$ so $3^{2}=9$; $|1-8|=7$; $(-3)^{2}=9$. Then $A=9-7+9=11$. $B=3\\cdot 3=9$. $A-B=2$. "
         "A sign error on $(-3)^{2}$ would make $A$ too small.",
         ["$B$ is larger by $2$", "they are equal", "$A$ is larger by $16$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    return qs


def build_unit1():
    title = "Algebra 1 Unit 1: Expressions, Properties & Real Numbers"
    description = (
        "A deep Grade 9 introduction to the real number line, subsets, properties of operations, "
        "simplifying expressions, absolute value as distance, order of operations, and translating words "
        "into algebra — with matching diagrams and a hard stretch set."
    )
    concepts = [
        "The real number line and subsets",
        "Properties of operations",
        "Simplify expressions",
        "Absolute value as distance",
        "Order of operations with grouping",
        "Translate words to algebra",
    ]

    c1 = concept_block(
        "1. The real number line and subsets",
        [
            "Every real number sits at exactly one point on a horizontal line. Moving right increases the value; "
            "moving left decreases it. Zero is the origin of that line, and every other real is a directed distance from zero.",
            "Useful nested subsets are: natural numbers (counting numbers), whole numbers (naturals together with $0$), "
            "integers (whole numbers and their negatives), rational numbers (ratios of integers with nonzero denominator), "
            "and irrational numbers (reals that are not rational, such as $\\sqrt{2}$ and $\\pi$).",
            "A rational number can be written $\\dfrac{p}{q}$ with $p,q$ integers and $q\\neq 0$. Terminating and repeating "
            "decimals are rational. Non-repeating, non-terminating decimals are irrational.",
            "Square roots of perfect squares are integers, hence rational: $\\sqrt{49}=7$. Square roots of non-squares, "
            "when they are real, are irrational: $\\sqrt{2}$ cannot be written as a fraction of integers.",
            "The real numbers are the union of the rationals and the irrationals. There is no real square root of a "
            "negative number; $\\sqrt{-9}$ is not real, while $-\\sqrt{9}=-3$ is real.",
            "Classifying a number means checking these nested boxes in order: is it an integer? a rational? a real? "
            "That classification later decides which operations and which graphs are even defined.",
        ],
        "Later Algebra 1 work with square roots, rational expressions, and the coordinate plane all assume you can "
        "tell which numbers are allowed. Mixing up $\\sqrt{9}$ with $\\sqrt{-9}$, or calling $\\pi$ rational, quietly "
        "breaks domain work in later units.",
        "Place the number on a mental number line first. Then ask: integer? ratio of integers? If not a ratio and still "
        "real, it is irrational. Keep the nested picture naturals $\\subset$ wholes $\\subset$ integers $\\subset$ "
        "rationals $\\subset$ reals in view.",
        lesson_figure(
            number_line(-4, 5, closed=[(-3, "−3"), (0, "0"), (2, "√4"), (4, "4")]),
            "A piece of the real number line",
            "Integers are marked. $\\sqrt{4}=2$ lands on an integer; irrationals such as $\\sqrt{2}$ would sit between $1$ and $2$.",
        )
        + solved(1, "Classify $-6$, $0$, $\\dfrac{3}{5}$, and $\\sqrt{2}$.",
                 ["$-6$ is an integer, hence also rational and real, but it is not a whole number.",
                  "$0$ is a whole number, integer, rational, and real.",
                  "$\\dfrac{3}{5}$ is rational and real, but not an integer.",
                  "$\\sqrt{2}$ is irrational and real, not rational."],
                 "integer; whole; rational non-integer; irrational", "", "Easy")
        + solved(2, "Which of $\\sqrt{81}$, $\\sqrt{8}$, and $-\\sqrt{16}$ is irrational?",
                 ["$\\sqrt{81}=9$, an integer, so rational.",
                  "$-\\sqrt{16}=-4$, an integer, so rational.",
                  "$\\sqrt{8}=\\sqrt{4\\cdot 2}=2\\sqrt{2}$, which is a nonzero rational times the irrational $\\sqrt{2}$, hence irrational."],
                 "$\\sqrt{8}$", "", "Medium")
        + solved(3, "A number $x$ satisfies $x^2=7$. Where does $x$ live among the subsets of the reals?",
                 ["Then $x=\\sqrt{7}$ or $x=-\\sqrt{7}$.",
                  "$7$ is not a perfect square, so $\\sqrt{7}$ is irrational.",
                  "Both values are therefore irrational reals (and not integers or rationals)."],
                 "irrational reals $\\pm\\sqrt{7}$", "The equation $x^2=-7$ would have no real solution at all.", "SAT"),
        ("Calling every radical irrational",
         "Perfect-square roots such as $\\sqrt{36}=6$ are integers. Only roots that cannot be simplified to a rational "
         "are irrational. Always simplify first, then classify."),
        ("Sketch a nested Venn of the sets",
         "Before choosing a multiple-choice classification, jot naturals $\\subset$ wholes $\\subset$ integers "
         "$\\subset$ rationals $\\subset$ reals and drop the given number into the smallest box that fits."),
        [
            "I can place integers and simple rationals on a number line.",
            "I can tell rational from irrational among common Algebra 1 numbers.",
            "I can name the nested subsets of the real numbers.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Properties of operations",
        [
            "The commutative property says order can swap: $a+b=b+a$ and $ab=ba$. Subtraction and division are not "
            "commutative: $7-2\\neq 2-7$.",
            "The associative property says grouping can change when the operation stays the same: $(a+b)+c=a+(b+c)$ "
            "and $(ab)c=a(bc)$. You regroup; you do not reorder yet unless you also use commutative.",
            "The distributive property links multiplication to addition: $a(b+c)=ab+ac$. This is the engine behind "
            "combining like terms, factoring, and later multiplying polynomials.",
            "Identities leave a number unchanged: $a+0=a$ (additive identity) and $a\\cdot 1=a$ (multiplicative identity). "
            "Inverses undo an operation: $a+(-a)=0$ and, for $a\\neq 0$, $a\\cdot\\dfrac{1}{a}=1$.",
            "The zero product idea is not a property of rearranging, but it is related: $a\\cdot 0=0$ for every real $a$. "
            "You cannot divide by zero, so $0$ has no multiplicative inverse.",
            "Naming the property that justifies a rewrite is a standard Algebra 1 skill. The name is not decoration — "
            "it tells you which moves are legal when you solve equations in Unit 2.",
        ],
        "Every later equation-solving step is one of these properties in disguise. If you cannot say why $3(x+4)=3x+12$ "
        "is allowed, distributing with a negative later will feel like a magic trick instead of a rule.",
        "Ask: did I swap order (commutative), change grouping (associative), multiply through a sum (distributive), "
        "or use $0$ or $1$ (identity/inverse)? Match the rewrite to exactly one of those.",
        lesson_figure(
            svg_balance("a(b+c)", "ab+ac"),
            "Distributive property as a balance",
            "Both pans stay equal: multiplying a sum is the same as multiplying each addend and then adding.",
        )
        + solved(4, "Name the property: $9+x=x+9$.",
                 ["The two addends swapped places and the sum is unchanged.",
                  "That is the commutative property of addition."],
                 "commutative property of addition", "", "Easy")
        + solved(5, "Name the property: $4(y+7)=4y+28$.",
                 ["$4$ multiplies both terms inside the parentheses.",
                  "That is the distributive property.",
                  "Check: $4\\cdot y+4\\cdot 7=4y+28$."],
                 "distributive property", "", "Medium")
        + solved(6, "Which property justifies $5\\cdot\\dfrac{1}{5}=1$, and what is the name of $\\dfrac{1}{5}$ relative to $5$?",
                 ["The product of a nonzero number and its reciprocal is $1$.",
                  "That is the multiplicative inverse property.",
                  "$\\dfrac{1}{5}$ is the multiplicative inverse (reciprocal) of $5$."],
                 "multiplicative inverse; $\\dfrac{1}{5}$ is the reciprocal of $5$", "", "Hard"),
        ("Treating subtraction as commutative",
         "$a-b$ is $a+(-b)$. You may commute addition after you rewrite subtraction as adding a negative, "
         "but $a-b$ itself is not equal to $b-a$ in general."),
        ("Rewrite first, then name",
         "If a step looks messy, rewrite subtraction as adding the opposite and division as multiplying by the "
         "reciprocal. The usual properties then apply cleanly to $+$ and $\\times$ only."),
        [
            "I can name commutative, associative, and distributive moves.",
            "I can identify identities and inverses.",
            "I can reject illegal swaps of subtraction or division.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Simplify expressions",
        [
            "An algebraic expression is a combination of numbers, variables, and operations with no equal sign. "
            "To simplify means to rewrite it with as few terms as possible, following the properties of Unit 1 lesson 2.",
            "Like terms have the same variable part raised to the same power. $7x$ and $-2x$ are like; $7x$ and $7x^2$ "
            "are not. Constants are like each other: $5$ and $-1$ combine to $4$.",
            "Always distribute (including a lonely minus sign) before you combine. $3(x-4)+x$ becomes $3x-12+x$, "
            "then $4x-12$. Skipping distribution is the main source of dropped terms.",
            "A minus in front of parentheses distributes as multiplication by $-1$: $-(2x-5)=-2x+5$. Both signs inside "
            "flip. Forgetting the second flip is a classic error.",
            "After distribution, add coefficients of like terms: $4x+9x=(4+9)x=13x$. The variable part stays; only the "
            "counts in front change.",
            "Simplified form is the version you will later set equal to something, substitute into, or compare. Clean "
            "expressions make Unit 2 equations far shorter.",
        ],
        "Every multi-step equation in the next unit begins with simplifying each side. If like terms are not combined "
        "correctly, you will solve a different equation than the one that was asked.",
        "Circle like terms in the same color. Distribute every nearby factor, including hidden $-1$. Then add "
        "coefficients. Stop when no like pair remains.",
        lesson_figure(
            svg_rect("3x", "x+2"),
            "Area picture for $3x(x+2)$ after you multiply later",
            "For now, think of combining $3x+3x$ as stacking identical tiles. Different-shaped tiles ($x$ versus constant) do not merge.",
        )
        + solved(7, "Simplify $8x-3x+6$.",
                 ["$8x$ and $-3x$ are like: $5x$.",
                  "The constant $6$ stays.",
                  "Result $5x+6$."],
                 "$5x+6$", "", "Easy")
        + solved(8, "Simplify $2(3n-4)-5n$.",
                 ["Distribute $2$: $6n-8-5n$.",
                  "Combine $6n-5n=n$.",
                  "Result $n-8$."],
                 "$n-8$", "", "Medium")
        + solved(9, "Simplify $4-3(2x-1)+x$.",
                 ["Distribute $-3$: $4-6x+3+x$.",
                  "Constants: $4+3=7$. $x$-terms: $-6x+x=-5x$.",
                  "Result $-5x+7$."],
                 "$-5x+7$", "The $-3$ times $-1$ becomes $+3$. Missing that plus is the usual trap.", "Hard"),
        ("Combining unlike terms",
         "$3x+3$ is already simple. You cannot write $6x$ or $6$. Only matching variable parts combine."),
        ("Distribute the sign, then combine",
         "Underline the factor in front of each parenthesis, including a lone minus. Multiply it through, rewrite "
         "the line with no parentheses, then combine."),
        [
            "I can identify like terms.",
            "I can distribute, including a leading minus.",
            "I can combine coefficients correctly.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Absolute value as distance",
        [
            "The absolute value $|a|$ is the distance from $a$ to $0$ on the real number line. Distances are never "
            "negative, so $|a|\\geq 0$ for every real $a$.",
            "Algebraically, $|a|=a$ when $a\\geq 0$, and $|a|=-a$ when $a<0$. The second piece looks odd until you test "
            "it: if $a=-8$, then $-a=8$, which matches $|-8|$.",
            "Distance between two numbers $p$ and $q$ is $|p-q|$. Order does not matter because $|p-q|=|q-p|$.",
            "The equation $|x|=k$ with $k>0$ has two solutions, $x=k$ and $x=-k$. If $k=0$, there is one solution, $x=0$. "
            "If $k<0$, there is no real solution, because distance cannot be negative.",
            "More generally, $|x-h|=k$ means $x$ is $k$ units from $h$. The two candidates are $x=h+k$ and $x=h-k$. "
            "This geometric reading is faster than blindly dropping bars.",
            "Unit 2 will solve absolute-value equations after you isolate the bars. The distance picture you learn here "
            "is what tells you why two (or zero) solutions appear.",
        ],
        "Absolute value shows up in error, tolerance, piecewise graphs, and later inequalities. Treating $|x|$ as "
        "“erase the minus” without thinking about distance causes dropped solutions.",
        "Draw a number line, mark the center point, and walk $k$ units both directions. Those two landings are the "
        "solutions of $|x-h|=k$ when $k>0$.",
        lesson_figure(
            number_line(-5, 7, closed=[(-2, "x=−2"), (4, "x=4")]),
            "Solutions of $|x-1|=3$",
            "Center at $1$ (unmarked tick). Walk $3$ left to $-2$ and $3$ right to $4$. Both are distance $3$ from $1$.",
        )
        + solved(10, "Evaluate $|-11|$ and $|4-4|$.",
                 ["$|-11|$ is the distance from $-11$ to $0$, which is $11$.",
                  "$|4-4|=|0|=0$."],
                 "$11$ and $0$", "", "Easy")
        + solved(11, "Find the distance between $-9$ and $2$.",
                 ["Distance $=|-9-2|=|-11|=11$, or equivalently $|2-(-9)|=|11|=11$."],
                 "$11$", "", "Medium")
        + solved(12, "Solve $|x+4|=6$ using a number line.",
                 ["Rewrite as $|x-(-4)|=6$: center at $-4$, distance $6$.",
                  "Right landing: $-4+6=2$. Left landing: $-4-6=-10$.",
                  "Check: $|2+4|=6$ and $|-10+4|=6$."],
                 "$x=2$ or $x=-10$", "", "SAT"),
        ("Writing $|a|=-a$ as the only rule",
         "That identity holds only when $a$ is already negative or zero. For positive $a$, $|a|=a$, not $-a$."),
        ("Mark the center, then walk",
         "For $|x-h|=k$, plot $h$ first. If $k>0$, mark $h+k$ and $h-k$. If $k=0$, only $h$. If $k<0$, stop: no real $x$."),
        [
            "I can evaluate absolute values of numbers.",
            "I can compute distance between two points on a line.",
            "I can solve $|x-h|=k$ with a number-line picture.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Order of operations with grouping",
        [
            "A single expression can mix parentheses, exponents, multiplication, division, addition, and subtraction. "
            "The agreed order is grouping first, then exponents, then multiplication and division left to right, then "
            "addition and subtraction left to right.",
            "Grouping includes parentheses, brackets, fraction bars, and absolute-value bars. Anything inside a group "
            "is finished before the outside operations touch it.",
            "Multiplication and division are partners at the same rank. $18\\div 3\\times 2$ is $6\\times 2=12$, not "
            "$18\\div 6$. Left-to-right is the tie-breaker, not “multiply always before divide.”",
            "Exponents bind tightly to the object they sit on. $-3^2$ is $-(3^2)=-9$, while $(-3)^2=9$. The parentheses "
            "are what include the minus in the base.",
            "When a problem mixes a fraction bar with other operations, treat the entire numerator as grouped and the "
            "entire denominator as grouped: $\\dfrac{2+6}{2}$ is $8/2=4$, not $2+3$.",
            "Order of operations is how you evaluate; the properties from lesson 2 are how you rewrite. You often need "
            "both on the same line.",
        ],
        "Translating words, substituting into formulas, and checking solutions all require a correct evaluation order. "
        "A single left-to-right error changes the number you report.",
        "Rewrite the expression with an extra pair of parentheses around every group you intend. Then evaluate from "
        "the inside out, one rank at a time, and show each rank on its own line.",
        lesson_figure(
            _nest_ops(),
            "Inside-out evaluation of $4(2+3)-1$",
            "Add inside: $5$. Multiply: $20$. Subtract: $19$. The arrow chain is the order, not left-to-right of every symbol.",
        )
        + solved(13, "Evaluate $7+2\\times 5$.",
                 ["Multiply first: $2\\times 5=10$.",
                  "Add: $7+10=17$."],
                 "$17$", "", "Easy")
        + solved(14, "Evaluate $3(6-1)^2-4$.",
                 ["Parentheses: $5$.",
                  "Exponent: $25$.",
                  "Multiply: $75$. Subtract: $71$."],
                 "$71$", "", "Medium")
        + solved(15, "Evaluate $\\dfrac{8-2^3}{4\\div 2}-(-1)^2$.",
                 ["Numerator: $2^3=8$, so $8-8=0$.",
                  "Denominator: $4\\div 2=2$. Fraction: $0$.",
                  "Then $0-1=-1$, because $(-1)^2=1$."],
                 "$-1$", "", "Hard"),
        ("Always multiplying before dividing",
         "They share a rank. Scan left to right among $\\times$ and $\\div$ only. The same is true of $+$ and $-$."),
        ("One rank per line",
         "Write a new copy of the expression after finishing grouping, then after exponents, then after $\\times\\div$, "
         "then after $+\\, -$. That paper trail catches rank mistakes before you lock an answer."),
        [
            "I can evaluate mixed operations in the correct order.",
            "I can treat fraction bars and absolute values as grouping.",
            "I can distinguish $-a^2$ from $(-a)^2$.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Translate words to algebra",
        [
            "English hides operations in ordinary words. Sum, difference, product, and quotient map to $+$, $-$, "
            "$\\times$, and $\\div$. “Less than” and “more than” are not symmetric: $5$ less than $n$ is $n-5$.",
            "The word quantity, the phrase the sum of, and commas often mark grouping. “Twice the sum of $x$ and $3$” "
            "is $2(x+3)$, not $2x+3$.",
            "“Is,” “equals,” and “results in” become $=$. Until you see one of those, you are building an expression, "
            "not an equation. Unit 2 will set these expressions equal to numbers and solve.",
            "Consecutive integer problems use $n$, $n+1$, $n+2$. Even consecutives use $n$, $n+2$. Naming the first "
            "unknown clearly is more important than which letter you pick.",
            "Units and labels belong in a dictionary on scratch paper: let $t$ be the number of tickets, not “tickets $t$ "
            "dollars.” A clean definition prevents mixing a count with a cost later.",
            "After you write the expression, read it back in English. If the reverse translation does not match the "
            "original sentence, the grouping is probably wrong.",
        ],
        "Word problems in every later unit are translation plus algebra. If the translation is wrong, perfect "
        "simplifying still solves the wrong story.",
        "Underline operations, box grouping phrases, and replace each box with parentheses. Then attach coefficients. "
        "Read the result aloud as a check.",
        lesson_figure(
            svg_balance("2n+5", "17"),
            "“Five more than twice a number is 17”",
            "Twice a number is $2n$; five more adds $5$; “is $17$” balances the two pans. Solving comes in Unit 2.",
        )
        + solved(16, "Translate “nine more than a number $m$.”",
                 ["More than means add after the number: $m+9$."],
                 "$m+9$", "", "Easy")
        + solved(17, "Translate “seven less than three times a number $k$.”",
                 ["Three times a number: $3k$.",
                  "Seven less than that: $3k-7$, not $7-3k$."],
                 "$3k-7$", "", "Medium")
        + solved(18, "Translate “twice the quantity of a number $n$ decreased by $4$, plus $1$.”",
                 ["“A number decreased by $4$” is $n-4$.",
                  "Twice that quantity: $2(n-4)$.",
                  "Plus $1$: $2(n-4)+1$, which simplifies to $2n-7$ if asked."],
                 "$2(n-4)+1$", "If the comma is ignored, students write $2n-4+1$, which is a different expression.", "SAT"),
        ("Reversing “less than”",
         "$5$ less than $n$ subtracts $5$ from $n$. Writing $5-n$ is the translation of “$n$ less than $5$.”"),
        ("Parentheses for every ‘quantity’",
         "Whenever the sentence says quantity, sum, difference, or the result of, wrap that inner phrase in "
         "parentheses before you multiply or add anything else."),
        [
            "I can map sum, difference, product, and quotient to symbols.",
            "I can handle “less than” and “more than” in the correct order.",
            "I can group “twice the sum” with parentheses.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u1_questions()


# ===========================================================================
# UNIT 2: Linear Equations & Inequalities
# ===========================================================================

def _u2_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("Solve $x+9=14$.", "$x=5$",
         "Subtract $9$ from both sides: $x=5$. Check: $5+9=14$.",
         ["$x=23$", "$x=-5$", "$x=9$"]),
        ("Solve $4y=20$.", "$y=5$",
         "Divide both sides by $4$: $y=5$.",
         ["$y=16$", "$y=24$", "$y=4$"]),
        ("Solve $\\dfrac{n}{3}=7$.", "$n=21$",
         "Multiply both sides by $3$: $n=21$.",
         ["$n=\\dfrac{7}{3}$", "$n=10$", "$n=4$"]),
        ("Solve $2x-5=9$.", "$x=7$",
         "Add $5$: $2x=14$. Divide by $2$: $x=7$.",
         ["$x=2$", "$x=7/2$", "$x=-2$"]),
        ("Solve $-x=8$.", "$x=-8$",
         "Multiply (or divide) both sides by $-1$: $x=-8$. The equation says the opposite of $x$ is $8$.",
         ["$x=8$", "$x=0$", "$x=-1$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Solve $3(x+2)=18$.", "$x=4$",
         "Distribute: $3x+6=18$. Subtract $6$: $3x=12$. Divide: $x=4$. Or divide by $3$ first: $x+2=6$, so $x=4$.",
         ["$x=6$", "$x=5$", "$x=16$"]),
        ("Solve $2(3x-1)+4=14$.", "$x=2$",
         "Distribute: $6x-2+4=14$, so $6x+2=14$. Subtract $2$: $6x=12$. $x=2$.",
         ["$x=3$", "$x=1$", "$x=5$"]),
        ("Solve $5-2(x-3)=1$.", "$x=5$",
         "Distribute $-2$: $5-2x+6=1$, so $11-2x=1$. Subtract $11$: $-2x=-10$. Divide: $x=5$.",
         ["$x=3$", "$x=-5$", "$x=4$"]),
        ("Solve $\\dfrac{1}{2}(4x+8)=10$.", "$x=3$",
         "Multiply both sides by $2$: $4x+8=20$. Subtract $8$: $4x=12$. $x=3$.",
         ["$x=4$", "$x=6$", "$x=2$"]),
        ("Solve $4(x-1)-x=8$.", "$x=4$",
         "$4x-4-x=8$, so $3x-4=8$. Add $4$: $3x=12$. $x=4$.",
         ["$x=3$", "$x=9/4$", "$x=2$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Solve $5x+1=2x+10$.", "$x=3$",
         "Subtract $2x$: $3x+1=10$. Subtract $1$: $3x=9$. $x=3$.",
         ["$x=11/7$", "$x=9$", "$x=-3$"]),
        ("Solve $4x-7=4x+2$.", "no solution",
         "Subtract $4x$: $-7=2$, which is false. The variable cancelled and a false number sentence remains.",
         ["infinitely many solutions", "$x=0$", "$x=9/8$"]),
        ("Solve $2(x+3)=2x+6$.", "infinitely many solutions",
         "Distribute: $2x+6=2x+6$, which is always true. Every real $x$ works (an identity).",
         ["no solution", "$x=0$", "$x=3$"]),
        ("Solve $7-x=2x-8$.", "$x=5$",
         "Add $x$: $7=3x-8$. Add $8$: $15=3x$. $x=5$.",
         ["$x=1$", "$x=-5$", "$x=15$"]),
        ("The equation $3x+4=3(x+1)+2$ has which solution set?", "the empty set",
         "Right side: $3x+3+2=3x+5$. Then $3x+4=3x+5$ becomes $4=5$, which is false, so no real $x$ works.",
         ["all real numbers", "$\\{0\\}$", "$\\{-1\\}$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The inequality $x>3$ is graphed with:", "an open dot at $3$ and shading to the right",
         "$>$ does not include the endpoint, so the dot is open. Greater than means the right side of $3$.",
         ["a closed dot at $3$ and shading to the right", "an open dot at $3$ and shading to the left",
          "closed dots at $3$ and at $0$"]),
        ("Solve $x+4\\leq 1$.", "$x\\leq -3$",
         "Subtract $4$: $x\\leq -3$. The inequality direction stays the same when adding or subtracting.",
         ["$x\\leq 5$", "$x\\geq -3$", "$x<-3$"]),
        ("Solve $-2x>8$.", "$x<-4$",
         "Divide by $-2$ and reverse the inequality: $x<-4$. Forgetting to reverse is the standard error.",
         ["$x>-4$", "$x<-6$", "$x>4$"]),
        ("Which number is a solution of $3x-1\\geq 8$?", "$4$",
         "Solve: $3x\\geq 9$, so $x\\geq 3$. Among typical choices, $4$ works; $2$ does not.",
         ["$2$", "$0$", "$-1$"]),
        ("The graph of $x\\leq -1$ uses:", "a closed dot at $-1$ and shading to the left",
         "$\\leq$ includes the endpoint. Less than means the left side of $-1$.",
         ["an open dot at $-1$ and shading to the left", "a closed dot at $-1$ and shading to the right",
          "an open dot at $1$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Solve $-2<x\\leq 3$. Which integer is not a solution?", "$-2$",
         "The left end is strict, so $-2$ is excluded. Integers $-1,0,1,2,3$ work; $3$ is included.",
         ["$3$", "$0$", "$-1$"]),
        ("The compound $x<-1$ or $x\\geq 4$ is graphed as:", "two rays, open at $-1$ and closed at $4$",
         "“Or” is the union: shade left of $-1$ (open) and right of $4$ (closed).",
         ["the segment between $-1$ and $4$", "only the point $4$", "the entire number line"]),
        ("Solve $1\\leq 2x+3<9$.", "$-1\\leq x<3$",
         "Subtract $3$: $-2\\leq 2x<6$. Divide by $2$: $-1\\leq x<3$.",
         ["$1\\leq x<9$", "$-2\\leq x<6$", "$x\\leq -1$ or $x>3$"]),
        ("Which compound means “$x$ is at least $2$ and at most $5$”?", "$2\\leq x\\leq 5$",
         "At least $2$ is $x\\geq 2$; at most $5$ is $x\\leq 5$. Together they are the closed interval from $2$ to $5$.",
         ["$x\\leq 2$ or $x\\geq 5$", "$2<x<5$", "$x\\geq 5$"]),
        ("Solve $x+1<4$ and $x-2>-1$.", "$1<x<3$",
         "The first inequality gives $x<3$. The second gives $x>1$. Their intersection is $1<x<3$.",
         ["$-1<x<3$", "$x<3$", "$x>1$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Solve $|x|=5$.", "$x=5$ or $x=-5$",
         "Distance $5$ from $0$ gives the two points $5$ and $-5$.",
         ["$x=5$ only", "$x=0$", "no solution"]),
        ("Solve $|x-3|=4$.", "$x=7$ or $x=-1$",
         "$x-3=4$ or $x-3=-4$, so $x=7$ or $x=-1$.",
         ["$x=1$ or $x=-7$", "$x=3$", "$x=4$"]),
        ("Solve $|2x+1|=7$.", "$x=3$ or $x=-4$",
         "$2x+1=7$ or $2x+1=-7$. First: $2x=6$, $x=3$. Second: $2x=-8$, $x=-4$.",
         ["$x=4$ or $x=-3$", "$x=3$ only", "$x=\\pm 7$"]),
        ("Solve $|x|+3=1$.", "no real solution",
         "$|x|=-2$, but absolute value cannot be negative.",
         ["$x=-2$", "$x=2$", "$x=0$"]),
        ("Solve $|x+2|=0$.", "$x=-2$",
         "Distance $0$ from $-2$ means $x$ is exactly $-2$.",
         ["$x=2$", "$x=0$", "no solution"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Solve $6=2x-4$.", "$x=5$",
         "Add $4$: $10=2x$. Divide: $x=5$.",
         ["$x=1$", "$x=5/2$", "$x=-5$"]),
        ("After distributing, $3(2x-5)=x+4$ becomes which equivalent equation?", "$6x-15=x+4$",
         "Only the left side is distributed in this step. Combining like terms comes next.",
         ["$6x-5=x+4$", "$5x-15=4$", "$6x-15=x-4$"]),
        ("If $4x+9=4x+9$, the solution set is:", "all real numbers",
         "The two sides are identical for every $x$.",
         ["the empty set", "$\\{0\\}$", "$\\{9\\}$"]),
        ("Graphing $x>-2$ requires:", "open dot at $-2$, shade right",
         "Strict inequality excludes $-2$; greater than shades toward larger numbers.",
         ["closed dot at $-2$, shade right", "open dot at $-2$, shade left", "closed dot at $2$"]),
        ("Solve $-4<2x\\leq 6$.", "$-2<x\\leq 3$",
         "Divide all three parts by $2$ (positive, so direction stays): $-2<x\\leq 3$.",
         ["$-4<x\\leq 6$", "$-8<x\\leq 12$", "$x\\leq 3$"]),
        ("The solutions of $|3x|=9$ are:", "$x=3$ or $x=-3$",
         "$3x=9$ or $3x=-9$.",
         ["$x=9$ or $x=-9$", "$x=3$ only", "$x=1/3$"]),
        ("Solve $5x-2=3x+10$.", "$x=6$",
         "Subtract $3x$: $2x-2=10$. Add $2$: $2x=12$. $x=6$.",
         ["$x=4$", "$x=8$", "$x=-6$"]),
        ("Which value satisfies both $x\\geq 0$ and $x<2$?", "$1$",
         "The intersection is $0\\leq x<2$. $1$ lies inside; $2$ is excluded; $-1$ fails $x\\geq 0$.",
         ["$2$", "$-1$", "$3$"]),
        ("Solve $\\dfrac{x-4}{2}=5$.", "$x=14$",
         "Multiply by $2$: $x-4=10$. Add $4$: $x=14$.",
         ["$x=6$", "$x=1$", "$x=9$"]),
        ("If $|x-1|=x-1$, then $x$ must satisfy:", "$x\\geq 1$",
         "$|A|=A$ holds exactly when $A\\geq 0$. Here $A=x-1$, so $x-1\\geq 0$.",
         ["$x\\leq 1$", "$x=0$", "all real $x$"]),
        ("Solve $-(x-6)=2x$.", "$x=2$",
         "$-x+6=2x$. Add $x$: $6=3x$. $x=2$.",
         ["$x=6$", "$x=-2$", "$x=3$"]),
        ("The inequality $7\\geq x$ is equivalent to:", "$x\\leq 7$",
         "Reading “$7$ is at least $x$” the other way, $x$ is at most $7$.",
         ["$x\\geq 7$", "$x<7$", "$x>7$"]),
        ("Solve $2(x+5)=3(x+1)-1$.", "$x=8$",
         "Left $2x+10$. Right $3x+3-1=3x+2$. Then $2x+10=3x+2$, so $8=x$.",
         ["$x=4$", "$x=2$", "$x=10$"]),
        ("Which is the solution of $|x+5|=2$?", "$x=-3$ or $x=-7$",
         "$x+5=2$ or $x+5=-2$.",
         ["$x=3$ or $x=7$", "$x=-5$", "$x=2$"]),
        ("A student solves $-3x<12$ and writes $x<-4$. The error was:", "not reversing after dividing by a negative",
         "Dividing by $-3$ reverses to $x>-4$. The student kept the same direction.",
         ["adding 3 instead of dividing", "using an open dot", "combining unlike terms"]),
        ("Solve $4x+8=4(x+2)$.", "infinitely many solutions",
         "Right side $4x+8$. Both sides match for all $x$.",
         ["no solution", "$x=0$", "$x=2$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("SAT Stretch: Solve $\\dfrac{2x-1}{3}-\\dfrac{x+4}{6}=2$.", "$x=6$",
         "Multiply through by $6$: $2(2x-1)-(x+4)=12$, so $4x-2-x-4=12$, hence $3x-6=12$, $3x=18$, and $x=6$.",
         ["$x=11$", "$x=8$", "$x=4$"]),
        ("SAT Stretch: For which $k$ does $2(x-3)=2x+k$ have no solution?", "$k\\neq -6$",
         "Left: $2x-6$. Equation $2x-6=2x+k$ becomes $-6=k$. If $k=-6$ it is an identity; if $k\\neq -6$ there is no solution. "
         "The question asks for no solution, so $k\\neq -6$.",
         ["$k=-6$", "$k=0$", "$k=2$"]),
        ("SAT Stretch: Solve $|2x-3|=|x+5|$.", "$x=8$ or $x=-\\dfrac{2}{3}$",
         "Case A: $2x-3=x+5\\Rightarrow x=8$. Case B: $2x-3=-(x+5)\\Rightarrow 2x-3=-x-5\\Rightarrow 3x=-2\\Rightarrow x=-\\dfrac{2}{3}$. "
         "Both check because both sides are absolute values.",
         ["$x=8$ only", "$x=-5$ or $x=\\dfrac{3}{2}$", "no solution"]),
        ("SAT Stretch: The compound $-3\\leq 1-2x<5$ is equivalent to:", "$-2<x\\leq 2$",
         "Subtract $1$: $-4\\leq -2x<4$. Divide by $-2$ and reverse both: $2\\geq x>-2$, which is $-2<x\\leq 2$.",
         ["$-4\\leq x<4$", "$x\\leq 2$", "$-2\\leq x<2$"]),
        ("SAT Stretch: A number $n$ satisfies $3n-4>2n+1$ and $n\\leq 10$. The integer values of $n$ are:",
         "$6,7,8,9,10$",
         "First inequality: $n>5$. With $n\\leq 10$ and $n$ an integer: $6$ through $10$.",
         ["$5,6,7,8,9,10$", "$n>5$ only", "$1$ through $10$"]),
        ("SAT Stretch: Solve $5-3(2-x)=4x-1$.", "$x=0$",
         "$5-6+3x=4x-1$, so $-1+3x=4x-1$. Add $1$: $3x=4x$. Subtract $3x$: $0=x$.",
         ["$x=2$", "$x=1$", "$x=-1$"]),
        ("SAT Stretch: Solve $2|x+1|-3=7$. After isolating and splitting, the solutions are:",
         "$x=4$ or $x=-6$",
         "Add $3$: $2|x+1|=10$. Divide: $|x+1|=5$. Then $x+1=5$ or $x+1=-5$, so $x=4$ or $x=-6$. "
         "Check: $2|5|-3=7$ and $2|-5|-3=7$.",
         ["$x=5$ or $x=-5$", "$x=4$ only", "$x=2$ or $x=-4$"]),
        ("SAT Stretch: Which description matches the solution of $3(x-2)\\geq x+4$?",
         "closed dot at $5$, shade to the right",
         "$3x-6\\geq x+4$, $2x\\geq 10$, $x\\geq 5$. Include $5$ because of $\\geq$, then shade toward larger $x$.",
         ["open dot at $5$, shade right", "closed dot at $5$, shade left", "closed dot at $2$"]),
        ("SAT Stretch: The equation $|x+1|=2x$ has how many real solutions?", "one",
         "Cases: $x+1=2x\\Rightarrow x=1$, and $x+1=-2x\\Rightarrow 3x=-1\\Rightarrow x=-\\dfrac{1}{3}$. "
         "Check in the original: absolute value is $\\geq 0$, so the right side $2x$ must be $\\geq 0$, hence $x\\geq 0$. "
         "Only $x=1$ survives; $x=-1/3$ makes $2x$ negative.",
         ["two", "none", "infinitely many"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    return qs


def build_unit2():
    title = "Algebra 1 Unit 2: Linear Equations & Inequalities"
    description = (
        "One-step through multi-step linear equations, variables on both sides, identities and contradictions, "
        "inequalities with number-line graphs, compound inequalities, and absolute-value equations."
    )
    concepts = [
        "One-step and two-step equations",
        "Multi-step with distribute",
        "Variables on both sides",
        "Inequalities and number-line graphs",
        "Compound inequalities",
        "Absolute-value equations",
    ]

    c1 = concept_block(
        "1. One-step and two-step equations",
        [
            "An equation says two expressions name the same number. Solving means finding every value of the variable "
            "that makes the sentence true. Each legal move is an inverse operation applied to both sides.",
            "Addition and subtraction undo each other. If $x+7=10$, subtract $7$ from both sides to isolate $x$. "
            "The balance picture is literal: whatever you do to the left pan, do to the right pan.",
            "Multiplication and division undo each other (except division by zero). $5x=20$ becomes $x=4$ after "
            "dividing by $5$. A coefficient of $-1$, as in $-x=6$, is cleared by multiplying by $-1$.",
            "A two-step equation typically looks like $ax+b=c$. Undo addition or subtraction first (the outside layer), "
            "then undo multiplication or division. Think of peeling an onion from the outside in.",
            "Always substitute your answer back into the original equation. A true number sentence confirms both the "
            "arithmetic and the direction of each inverse.",
            "Fractions do not change the plan: $\\dfrac{x}{4}=3$ is one-step (multiply by $4$). "
            "$\\dfrac{x}{4}+1=3$ is two-step (subtract $1$, then multiply by $4$).",
        ],
        "Every later equation — systems, quadratics after factoring, formulas — uses these same inverse moves. "
        "Fluency here is what makes Unit 3 graphing and Unit 4 systems feel mechanical instead of mysterious.",
        "Name the outside operation, apply its inverse to both sides, and write a new, shorter equation. Repeat until "
        "the variable is alone. Then check.",
        lesson_figure(
            svg_balance("x+5", "12"),
            "The equation $x+5=12$ as a balance scale",
            "Removing $5$ from both pans leaves $x$ balanced with $7$. Inverse operations keep the scale level.",
        )
        + solved(1, "Solve $x-8=3$.",
                 ["Add $8$ to both sides.",
                  "$x=11$.",
                  "Check: $11-8=3$."],
                 "$x=11$", "", "Easy")
        + solved(2, "Solve $3x+4=19$.",
                 ["Subtract $4$: $3x=15$.",
                  "Divide by $3$: $x=5$.",
                  "Check: $3(5)+4=19$."],
                 "$x=5$", "", "Medium")
        + solved(3, "Solve $\\dfrac{2x-1}{5}=3$.",
                 ["Multiply both sides by $5$: $2x-1=15$.",
                  "Add $1$: $2x=16$.",
                  "Divide by $2$: $x=8$."],
                 "$x=8$", "", "Hard"),
        ("Undoing the inside first",
         "In $3x+4=19$, do not divide by $3$ first unless you divide every term, including the $4$. The cleaner habit "
         "is: undo $+$ or $-$ first, then undo the coefficient."),
        ("Write the inverse in words",
         "Before touching numbers, jot “subtract $4$, then divide by $3$.” That two-word plan prevents doing both "
         "moves at once and losing a term."),
        [
            "I can solve one-step equations with all four operations.",
            "I can solve two-step equations of the form $ax+b=c$.",
            "I can check by substituting.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Multi-step with distribute",
        [
            "When an equation contains parentheses, simplify each side before isolating the variable. Distribution "
            "and combining like terms are Unit 1 skills used in service of solving.",
            "The distributive property turns $3(x-4)$ into $3x-12$. A leading minus is distribution of $-1$: "
            "$-(x-6)=-x+6$. Both interior signs change.",
            "If several like terms live on the same side, combine them next. $2x+5x-1=20$ should become $7x-1=20$ "
            "before you start inverse operations.",
            "Sometimes it is smarter to divide a common factor first: $4(x+3)=20$ can become $x+3=5$ in one step. "
            "Either order is legal if you apply it to the entire equation.",
            "Fractions next to parentheses, such as $\\dfrac{1}{2}(6x-4)=5$, can be cleared by multiplying both sides "
            "by the denominator, or by distributing the fraction. Pick one plan and finish it.",
            "Show a simplified equation with no parentheses before you move terms across the equal sign. Mixing "
            "distribution with moving terms in the same line is how signs vanish.",
        ],
        "Most textbook “multi-step” items are distribution plus a two-step equation. If distribution is sloppy, "
        "the inverse steps that follow are solving the wrong line.",
        "Parentheses off, like terms combined, then peel inverse operations from the outside. Check in the original, "
        "not in a half-simplified middle line.",
        lesson_figure(
            svg_balance("2(x+3)", "14"),
            "$2(x+3)=14$",
            "You may divide both pans by $2$ first, getting $x+3=7$, or distribute first, getting $2x+6=14$. Both paths give $x=4$.",
        )
        + solved(4, "Solve $2(x+5)=16$.",
                 ["Divide by $2$: $x+5=8$.",
                  "Subtract $5$: $x=3$."],
                 "$x=3$", "", "Easy")
        + solved(5, "Solve $5(2x-1)-3x=16$.",
                 ["Distribute: $10x-5-3x=16$.",
                  "Combine like terms: $7x-5=16$.",
                  "Add $5$: $7x=21$. Divide by $7$: $x=3$.",
                  "Check: $5(6-1)-9=25-9=16$."],
                 "$x=3$", "", "Medium")
        + solved(6, "Solve $4-3(2-x)=x+10$.",
                 ["Distribute $-3$: $4-6+3x=x+10$.",
                  "Combine left: $-2+3x=x+10$.",
                  "Subtract $x$: $-2+2x=10$. Add $2$: $2x=12$. $x=6$."],
                 "$x=6$", "", "SAT"),
        ("Distributing only the first term",
         "$3(x+4)$ is $3x+12$, not $3x+4$. Every term inside is multiplied."),
        ("Get to a line with no parentheses",
         "Do not move a term across the equal sign while parentheses still exist. Finish Unit 1 simplifying on each "
         "side first."),
        [
            "I can distribute, including a leading minus.",
            "I can combine like terms on one side.",
            "I can then solve the resulting two-step equation.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Variables on both sides",
        [
            "When $x$ appears on both sides, collect variable terms on one side and constants on the other. Choose "
            "the side that keeps the coefficient of $x$ positive when you can; it is not required, only kinder.",
            "Subtract (or add) a variable term from both sides, just as you would a number. $5x+1=2x+10$ becomes "
            "$3x+1=10$ after subtracting $2x$.",
            "If the variable terms cancel and a true number sentence remains, such as $4=4$, every real number is a "
            "solution (an identity). The original expressions were equivalent.",
            "If the variable terms cancel and a false sentence remains, such as $4=7$, there is no solution (a "
            "contradiction). The graphs of the two sides are parallel distinct lines.",
            "Identities and contradictions are not failures. They are complete answers: $\\mathbb{R}$ or $\\emptyset$. "
            "Writing $x=0$ because “everything cancelled” is incorrect.",
            "After collecting, you are back in a two-step equation. Check by substituting into the original, especially "
            "when a negative coefficient was moved.",
        ],
        "Systems in Unit 4 are this lesson with two variables. Recognizing “all real” versus “empty” also prepares "
        "you for parallel and coincident lines on the coordinate plane.",
        "Move $x$-terms, then move constants, then divide. If $x$ disappears, judge the remaining number sentence "
        "true or false — that judgment is the solution set.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(2, 1, -2, 4)), ("#dc2626", _seg(2, 1, -2, 4))],
                points=[(0, 1, "(0,1)"), (2, 5, "(2,5)")],
                xlim=(-3, 5), ylim=(-2, 8),
            ),
            "An identity: both sides of $2x+1=2x+1$ are the same line",
            "Every $x$ is a solution. A contradiction would be two parallel lines that never meet.",
        )
        + solved(7, "Solve $6x-2=4x+8$.",
                 ["Subtract $4x$: $2x-2=8$.",
                  "Add $2$: $2x=10$.",
                  "$x=5$."],
                 "$x=5$", "", "Easy")
        + solved(8, "Solve $3x+7=3x-1$.",
                 ["Subtract $3x$: $7=-1$, which is false.",
                  "No real $x$ works."],
                 "no solution", "", "Medium")
        + solved(9, "Solve $2(3x-4)=3(2x-1)-5$.",
                 ["Left: $6x-8$. Right: $6x-3-5=6x-8$.",
                  "$6x-8=6x-8$ is always true.",
                  "Infinitely many solutions."],
                 "all real numbers", "", "Hard"),
        ("Reporting $x=0$ when both sides cancel",
         "Cancellation means the $x$ terms were identical. You must still look at the constants. True constants: all "
         "reals. False constants: none."),
        ("Keep a positive $x$ coefficient",
         "If the right side has the larger $x$ coefficient, subtract the left $x$-term instead. Fewer sign errors "
         "follow."),
        [
            "I can collect variable terms on one side.",
            "I can recognize identities and contradictions.",
            "I can check solutions in the original equation.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Inequalities and number-line graphs",
        [
            "A linear inequality uses $<$, $>$, $\\leq$, or $\\geq$ in place of $=$. Solutions are usually an infinite "
            "set of numbers, so we graph them on a number line rather than listing them.",
            "Adding or subtracting the same number on both sides preserves the inequality direction. $x+4>7$ becomes "
            "$x>3$ without any reversal.",
            "Multiplying or dividing by a positive number also preserves direction. Multiplying or dividing by a "
            "negative number reverses direction: $-2x>8$ becomes $x<-4$.",
            "A strict inequality $<$ or $>$ gets an open dot (the endpoint is not a solution). $\\leq$ or $\\geq$ "
            "gets a closed (filled) dot. Shade the ray of numbers that make the inequality true.",
            "Testing a point is the fastest graph check. For $x>-2$, test $0$: true, so shade toward $0$ (right). "
            "If a test point fails, shade the other way.",
            "Writing $7\\geq x$ is the same as $x\\leq 7$. Many students prefer the variable on the left so the arrow "
            "tip of $<$ or $>$ points toward the shaded direction on the number line.",
        ],
        "Inequalities model budgets, speed limits, and later systems of inequalities in Unit 4. The reverse-when-"
        "negative rule is the single most-tested mechanical skill in this unit.",
        "Solve as if it were an equation, reverse if you multiplied or divided by a negative, then graph with the "
        "correct endpoint mark and a test-point check.",
        lesson_figure(
            number_line(-4, 6, opened=[(2, "2")], shade=("right", 2)),
            "Graph of $x>2$",
            "Open dot at $2$ because $2$ itself is not included; purple shading runs to the right.",
        )
        + solved(10, "Solve and describe the graph of $x+5\\geq 2$.",
                 ["Subtract $5$: $x\\geq -3$.",
                  "Closed dot at $-3$, shade right."],
                 "$x\\geq -3$; closed, right", "", "Easy")
        + solved(11, "Solve $-3x<12$.",
                 ["Divide by $-3$ and reverse: $x>-4$.",
                  "Open dot at $-4$, shade right."],
                 "$x>-4$", "", "Medium")
        + solved(12, "Solve $5-2x\\leq 1$ and graph.",
                 ["Subtract $5$: $-2x\\leq -4$.",
                  "Divide by $-2$ and reverse: $x\\geq 2$.",
                  "Closed dot at $2$, shade right."],
                 "$x\\geq 2$", "", "SAT"),
        ("Forgetting to reverse",
         "The reversal happens only when multiplying or dividing by a negative. Adding $-5$ does not reverse. "
         "Dividing by $-5$ does."),
        ("Test one number after you graph",
         "Pick a convenient point in the shaded region and substitute into the original inequality. If it fails, "
         "the endpoint mark or the direction is wrong."),
        [
            "I can solve one-step and two-step inequalities.",
            "I reverse when multiplying or dividing by a negative.",
            "I can graph with open or closed dots.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Compound inequalities",
        [
            "A compound inequality joins two inequalities with and or or. And means intersection (both must be true). "
            "Or means union (at least one is true).",
            "The compact form $a<x<b$ is an and: $x$ is greater than $a$ and less than $b$. Graphically it is a "
            "segment (possibly missing endpoints if the inequalities are strict).",
            "To solve $a<2x+1<b$, perform the same operation on all three parts. Subtract $1$ from all three, then "
            "divide all three by $2$. Reverse all three if you divide by a negative.",
            "An or compound such as $x<-1$ or $x\\geq 4$ graphs as two rays. There is a gap in the middle that is "
            "not shaded.",
            "If an and compound cannot happen — for example $x>5$ and $x<2$ — the solution is empty. If an or "
            "compound covers everything, the solution is all reals.",
            "Interval notation is optional in Algebra 1 but useful: $2\\leq x<5$ is $[2,5)$. Matching the dot type "
            "to a bracket or parenthesis prevents endpoint errors.",
        ],
        "Compound inequalities appear in domain restrictions, absolute-value inequalities, and later piecewise "
        "functions. Reading and versus or incorrectly flips a segment into two rays.",
        "Split into two inequalities if the compact form feels crowded. Solve each, then intersect (and) or union "
        "(or). Graph last, with two endpoint dots when needed.",
        lesson_figure(
            number_line(-4, 6, closed=[(-1, "−1")], opened=[(4, "4")], shade=("between", -1, 4)),
            "Graph of $-1\\leq x<4$",
            "Closed at $-1$, open at $4$, shade between: an and compound.",
        )
        + solved(13, "Which integers satisfy $-1\\leq n<3$?",
                 ["Included: $-1,0,1,2$.",
                  "$3$ is excluded by the strict right end."],
                 "$-1,0,1,2$", "", "Easy")
        + solved(14, "Solve $-3<2x+1\\leq 7$.",
                 ["Subtract $1$: $-4<2x\\leq 6$.",
                  "Divide by $2$: $-2<x\\leq 3$."],
                 "$-2<x\\leq 3$", "", "Medium")
        + solved(15, "Solve $4-x\\geq 1$ or $2x+3>11$.",
                 ["First: $-x\\geq -3$, reverse: $x\\leq 3$.",
                  "Second: $2x>8$, $x>4$.",
                  "Union: $x\\leq 3$ or $x>4$."],
                 "$x\\leq 3$ or $x>4$", "", "Hard"),
        ("Treating or like and",
         "Or keeps both regions. And keeps only the overlap. If you shade a segment for an or statement, the graph "
         "is the opposite of what was asked."),
        ("Operate on all three parts",
         "For $a<x<b$, whatever you add or multiply must hit $a$, the middle, and $b$. Leaving one end unchanged "
         "breaks the compound."),
        [
            "I can graph and versus or.",
            "I can solve three-part inequalities.",
            "I can reverse all three parts when dividing by a negative.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Absolute-value equations",
        [
            "After Unit 1’s distance picture, an equation $|A|=k$ with $k>0$ splits into two ordinary equations: "
            "$A=k$ or $A=-k$. Solve each, then check both in the original.",
            "Always isolate the absolute value first. $|x|+3=10$ becomes $|x|=7$ before splitting. If isolation "
            "produces $|A|=$ a negative, stop: no real solution.",
            "When $A$ is linear, each case is a linear equation from earlier in this unit. $|2x-1|=7$ becomes "
            "$2x-1=7$ or $2x-1=-7$.",
            "Checking is not optional. If a later equation is $|A|=B$ with $B$ also containing $x$, a case solution "
            "can fail because the right side becomes negative.",
            "$|A|=0$ has one solution, the solution of $A=0$. $|A|=|B|$ splits as $A=B$ or $A=-B$, then check.",
            "Inequalities with absolute value are a natural next step (often honors): $|A|<k$ is an and compound, "
            "$|A|>k$ is an or compound. This lesson stays with equations.",
        ],
        "Absolute value is the first piecewise rule most Algebra 1 students solve. The isolate-then-split habit "
        "returns in quadratics when a substitution hides inside another function.",
        "Isolate the bars. If the right side is negative, conclude no solution. If zero, one case. If positive, two "
        "cases. Check each candidate in the original.",
        lesson_figure(
            number_line(-6, 8, closed=[(-1, "−1"), (5, "5")]),
            "Solutions of $|x-2|=3$",
            "Center $2$, distance $3$: landings at $-1$ and $5$.",
        )
        + solved(16, "Solve $|x|=9$.",
                 ["$x=9$ or $x=-9$."],
                 "$x=\\pm 9$", "", "Easy")
        + solved(17, "Solve $|x+5|=2$.",
                 ["$x+5=2$ or $x+5=-2$.",
                  "$x=-3$ or $x=-7$."],
                 "$x=-3$ or $x=-7$", "", "Medium")
        + solved(18, "Solve $|3x-6|=x$.",
                 ["Case 1: $3x-6=x\\Rightarrow 2x=6\\Rightarrow x=3$. Check: $|9-6|=3$, right side $3$. Good.",
                  "Case 2: $3x-6=-x\\Rightarrow 4x=6\\Rightarrow x=\\dfrac{3}{2}$. Check: $|4.5-6|=1.5$, right side $1.5$. Good.",
                  "Both survive because the right side $x$ is nonnegative for both candidates."],
                 "$x=3$ or $x=\\dfrac{3}{2}$", "If a case made the right side negative, it would be rejected.", "SAT"),
        ("Splitting before isolating",
         "From $|x|+4=10$, do not write $x+4=10$ or $x+4=-10$. Those extra $\\pm 4$ were never inside the bars.",
         ),
        ("Check when the other side has $x$",
         "Any solution of $|A|=B$ needs $B\\geq 0$. Substitute before you keep the answer."),
        [
            "I can isolate an absolute value.",
            "I can split $|A|=k$ into two linear equations.",
            "I can reject candidates that fail a check.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u2_questions()


# ===========================================================================
# UNIT 3: Linear Functions & Graphs
# ===========================================================================

def _u3_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("The slope of the line through $(1,2)$ and $(4,8)$ is:", "2",
         "$m=\\dfrac{8-2}{4-1}=\\dfrac{6}{3}=2$. Rise $6$, run $3$.",
         ["3", "1/2", "6"]),
        ("A line that falls from left to right has:", "negative slope",
         "Negative slope means $y$ decreases as $x$ increases, so the graph falls left to right.",
         ["positive slope", "zero slope", "undefined slope"]),
        ("The slope of a horizontal line is:", "0",
         "Rise is $0$ while run is nonzero, so $m=0$. A vertical line, by contrast, has undefined slope.",
         ["undefined", "1", "-1"]),
        ("From $(0,5)$ to $(10,0)$, the rate of change of $y$ with respect to $x$ is:", "$-\\dfrac{1}{2}$",
         "$m=\\dfrac{0-5}{10-0}=\\dfrac{-5}{10}=-\\dfrac{1}{2}$.",
         ["$\\dfrac{1}{2}$", "$-2$", "$5$"]),
        ("A vertical line through $x=4$ has slope that is:", "undefined",
         "Run is $0$, so the slope ratio is undefined. You cannot divide by zero.",
         ["0", "4", "1"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The $y$-intercept of $y=3x-7$ is:", "$(0,-7)$",
         "In $y=mx+b$, the constant $b$ is the $y$-intercept value, so the point is $(0,-7)$.",
         ["$(-7,0)$", "$(3,0)$", "$(0,3)$"]),
        ("Which equation has slope $4$ and $y$-intercept $1$?", "$y=4x+1$",
         "Slope-intercept form is $y=mx+b$ with $m=4$ and $b=1$.",
         ["$y=x+4$", "$y=4x-1$", "$4x+y=1$"]),
        ("If $y=-2x+6$, then when $x=3$ the output is:", "0",
         "Substitute: $y=-2(3)+6=-6+6=0$. The graph crosses the $x$-axis at $(3,0)$.",
         ["6", "12", "-6"]),
        ("A line with slope $\\dfrac{2}{3}$ that crosses the $y$-axis at $5$ is:", "$y=\\dfrac{2}{3}x+5$",
         "Plug $m=\\dfrac{2}{3}$ and $b=5$ into $y=mx+b$.",
         ["$y=\\dfrac{3}{2}x+5$", "$y=5x+\\dfrac{2}{3}$", "$y=\\dfrac{2}{3}x-5$"]),
        ("Rewriting $2x+y=8$ in slope-intercept form gives:", "$y=-2x+8$",
         "Subtract $2x$: $y=-2x+8$. Slope $-2$, intercept $8$.",
         ["$y=2x+8$", "$y=-2x-8$", "$y=8-x$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The point-slope form of a line through $(2,5)$ with slope $3$ is:", "$y-5=3(x-2)$",
         "Use $y-y_1=m(x-x_1)$ with $(x_1,y_1)=(2,5)$ and $m=3$.",
         ["$y-2=3(x-5)$", "$y+5=3(x+2)$", "$y=3x+2$"]),
        ("Standard form $Ax+By=C$ for $y=2x-4$ can be written:", "$2x-y=4$",
         "From $y=2x-4$, rearrange: $2x-y=4$. (Equivalently $-2x+y=-4$.)",
         ["$2x+y=4$", "$x-2y=4$", "$2x-y=-4$"]),
        ("A line through $(-1,4)$ with slope $-2$ has equation:", "$y-4=-2(x+1)$",
         "Point-slope: $y-4=-2\\bigl(x-(-1)\\bigr)= -2(x+1)$.",
         ["$y-4=-2(x-1)$", "$y+4=-2(x+1)$", "$y= -2x-1$"]),
        ("Which point lies on $3x-2y=12$?", "$(4,0)$",
         "Plug $(4,0)$: $12-0=12$, true. $(0,4)$ gives $-8=12$, false.",
         ["$(0,4)$", "$(3,2)$", "$(2,3)$"]),
        ("Converting $y+1=\\dfrac{1}{2}(x-6)$ to slope-intercept yields:", "$y=\\dfrac{1}{2}x-4$",
         "Distribute: $y+1=\\dfrac{1}{2}x-3$. Subtract $1$: $y=\\dfrac{1}{2}x-4$.",
         ["$y=\\dfrac{1}{2}x-3$", "$y=\\dfrac{1}{2}x+4$", "$y=2x-4$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Two distinct lines with the same slope are:", "parallel",
         "Equal slopes and different intercepts mean the lines never meet.",
         ["perpendicular", "the same line", "vertical"]),
        ("A line perpendicular to $y=3x-1$ has slope:", "$-\\dfrac{1}{3}$",
         "Negative reciprocal of $3$ is $-\\dfrac{1}{3}$.",
         ["$3$", "$-3$", "$\\dfrac{1}{3}$"]),
        ("The line through $(0,2)$ parallel to $y=-4x+7$ is:", "$y=-4x+2$",
         "Keep slope $-4$ and use $b=2$.",
         ["$y=\\dfrac{1}{4}x+2$", "$y=-4x+7$", "$y=4x+2$"]),
        ("Which pair of slopes is perpendicular?", "$\\dfrac{2}{5}$ and $-\\dfrac{5}{2}$",
         "The product is $\\dfrac{2}{5}\\cdot\\left(-\\dfrac{5}{2}\\right)=-1$.",
         ["$2$ and $5$", "$\\dfrac{2}{5}$ and $\\dfrac{5}{2}$", "$-2$ and $-\\dfrac{1}{2}$"]),
        ("A horizontal line and a vertical line are:", "perpendicular",
         "Slopes $0$ and undefined; geometrically they meet at a right angle.",
         ["parallel", "the same line", "neither parallel nor perpendicular"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The $x$-intercept of $2x+5y=10$ is:", "$(5,0)$",
         "Set $y=0$: $2x=10$, $x=5$. The point is $(5,0)$.",
         ["$(0,5)$", "$(0,2)$", "$(2,0)$"]),
        ("The $y$-intercept of $x-3y=6$ is:", "$(0,-2)$",
         "Set $x=0$: $-3y=6$, $y=-2$.",
         ["$(6,0)$", "$(0,2)$", "$(0,6)$"]),
        ("To graph $y=-\\dfrac{1}{2}x+3$ using intercepts, the $y$-intercept is:", "$(0,3)$",
         "When $x=0$, $y=3$. The $x$-intercept is found by setting $y=0$: $x=6$, so $(6,0)$.",
         ["$(3,0)$", "$(0,-1/2)$", "$(-2,0)$"]),
        ("A line with intercepts $(4,0)$ and $(0,-2)$ has slope:", "$\\dfrac{1}{2}$",
         "Rise over run from $(4,0)$ to $(0,-2)$ is $\\dfrac{-2-0}{0-4}=\\dfrac{-2}{-4}=\\dfrac{1}{2}$.",
         ["$-\\dfrac{1}{2}$", "$-2$", "$2$"]),
        ("If a line has $x$-intercept $a$ and $y$-intercept $b$, both nonzero, an intercept equation is:",
         "$\\dfrac{x}{a}+\\dfrac{y}{b}=1$",
         "The intercept form $\\dfrac{x}{a}+\\dfrac{y}{b}=1$ hits $(a,0)$ and $(0,b)$.",
         ["$ax+by=1$", "$x/b+y/a=1$", "$y=ax+b$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("If $f(x)=2x-5$, then $f(4)$ equals:", "3",
         "$f(4)=8-5=3$.",
         ["-3", "8", "4"]),
        ("The notation $f(0)$ for a linear $f$ is the:", "$y$-intercept of the graph",
         "$x=0$ is where the graph meets the $y$-axis, so $f(0)=b$.",
         ["$x$-intercept", "slope", "zero of the slope"]),
        ("If $g(x)=-x+8$ and $g(x)=2$, then $x$ is:", "6",
         "Solve $-x+8=2$: $-x=-6$, $x=6$.",
         ["10", "2", "-6"]),
        ("For $h(x)=\\dfrac{1}{2}x+1$, the point $(6,h(6))$ is:", "$(6,4)$",
         "$h(6)=3+1=4$.",
         ["$(6,7)$", "$(4,6)$", "$(6,3)$"]),
        ("Which statement is true for $f(x)=mx+b$ with $m\\neq 0$?", "$f$ is a function because each $x$ has one $y$",
         "A nonvertical line passes the vertical line test. Vertical lines are not functions of $x$.",
         ["it fails the vertical line test", "it is not linear", "it has undefined slope"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("A line rises $5$ units while $x$ increases by $2$. Its slope is:", "$\\dfrac{5}{2}$",
         "Slope is rise over run: $\\dfrac{5}{2}$.",
         ["$\\dfrac{2}{5}$", "$7$", "$-\\dfrac{5}{2}$"]),
        ("The graph of $y=x$ and the graph of $y=-x$ are:", "perpendicular",
         "Slopes $1$ and $-1$ multiply to $-1$.",
         ["parallel", "horizontal", "the same ray"]),
        ("Writing $4x-2y=10$ as $y=mx+b$ produces:", "$y=2x-5$",
         "$-2y=-4x+10$, so $y=2x-5$.",
         ["$y=2x+5$", "$y=-2x-5$", "$y=\\dfrac{1}{2}x-5$"]),
        ("A line through $(3,1)$ perpendicular to $y=\\dfrac{1}{2}x$ has slope:", "$-2$",
         "Negative reciprocal of $\\dfrac{1}{2}$ is $-2$.",
         ["$\\dfrac{1}{2}$", "$2$", "$-\\dfrac{1}{2}$"]),
        ("The $x$-intercept of $y=4x-12$ is the solution of:", "$4x-12=0$",
         "Set $y=0$. Then $x=3$, so the intercept is $(3,0)$.",
         ["$4x=0$", "$x-12=0$", "$y=4$"]),
        ("If $f(x)=5x+1$, then $f(-2)$ is:", "-9",
         "$5(-2)+1=-10+1=-9$.",
         ["11", "-10", "9"]),
        ("Two lines $y=3x+1$ and $y=3x-4$ never meet because they are:", "parallel and distinct",
         "Same slope $3$, different intercepts.",
         ["perpendicular", "the same line", "vertical"]),
        ("Point-slope with $m=-1$ through $(0,0)$ simplifies to:", "$y=-x$",
         "$y-0=-1(x-0)$, so $y=-x$.",
         ["$y=x$", "$y=-1$", "$x=-1$"]),
        ("On $y=\\dfrac{3}{4}x-2$, a run of $4$ produces a rise of:", "3",
         "Slope $\\dfrac{3}{4}$ means rise $3$ for run $4$.",
         ["4", "-2", "3/4"]),
        ("The graph of $x=5$ is:", "a vertical line",
         "Every point has $x$-coordinate $5$. Slope is undefined; it is not a function $y=f(x)$.",
         ["a horizontal line", "the line $y=5$", "a ray of slope 5"]),
        ("For $f(x)=x-9$, the zero of $f$ (where $f(x)=0$) is:", "$x=9$",
         "Solve $x-9=0$. That $x$-value is the $x$-intercept.",
         ["$x=-9$", "$x=0$", "$x=1$"]),
        ("A line with slope $0$ through $(2,-3)$ is:", "$y=-3$",
         "Horizontal line at height $-3$.",
         ["$x=2$", "$y=2$", "$y=0$"]),
        ("Which equation is in standard form with integer coefficients?", "$3x+4y=12$",
         "$Ax+By=C$ with $A,B,C$ integers. $y=\\dfrac{3}{4}x+1$ is slope-intercept, not standard as written.",
         ["$y=(3/4)x+1$", "$y-1=3(x-2)$", "$x=y$"]),
        ("The slope between $(a,b)$ and $(a,c)$ with $b\\neq c$ is:", "undefined",
         "The $x$-coordinates match, so run is $0$ (a vertical segment).",
         ["0", "$c-b$", "$1$"]),
        ("If $g(3)=10$ for $g(x)=mx+1$, then $m$ equals:", "3",
         "$3m+1=10$, so $3m=9$, $m=3$.",
         ["10", "11/3", "9"]),
        ("A line parallel to the $x$-axis through $(7,4)$ has equation:", "$y=4$",
         "Parallel to the $x$-axis means horizontal. Height is the given $y$-coordinate $4$.",
         ["$x=7$", "$y=7$", "$x=4$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("SAT Stretch: A line passes through $(2,5)$ and $(6,-3)$. The equation in slope-intercept form is:",
         "$y=-2x+9$",
         "$m=\\dfrac{-3-5}{6-2}=\\dfrac{-8}{4}=-2$. Then $5=-2(2)+b$ so $5=-4+b$ and $b=9$. Thus $y=-2x+9$.",
         ["$y=-2x+5$", "$y=2x+1$", "$y=-2x-3$"]),
        ("SAT Stretch: Line $k$ is perpendicular to $3x+4y=12$ and passes through $(0,-1)$. An equation of $k$ is:",
         "$y=\\dfrac{4}{3}x-1$",
         "From $4y=-3x+12$, $y=-\\dfrac{3}{4}x+3$, so the given slope is $-\\dfrac{3}{4}$. Perpendicular slope is "
         "$\\dfrac{4}{3}$. Through $(0,-1)$: $y=\\dfrac{4}{3}x-1$.",
         ["$y=-\\dfrac{3}{4}x-1$", "$y=\\dfrac{3}{4}x-1$", "$y=\\dfrac{4}{3}x+1$"]),
        ("SAT Stretch: If $f(x)=2x-3$ and $g(x)=-x+9$, the $x$-value where $f(x)=g(x)$ is:", "4",
         "$2x-3=-x+9$, so $3x=12$, $x=4$. Then $f(4)=5=g(4)$. This is the intersection of the two lines.",
         ["3", "6", "9"]),
        ("SAT Stretch: The intercepts of $ax+by=ab$ (with $a,b\\neq 0$) are:", "$(b,0)$ and $(0,a)$",
         "$y=0\\Rightarrow ax=ab\\Rightarrow x=b$. $x=0\\Rightarrow by=ab\\Rightarrow y=a$.",
         ["$(a,0)$ and $(0,b)$", "$(1,0)$ and $(0,1)$", "$(ab,0)$ and $(0,ab)$"]),
        ("SAT Stretch: A taxi charges $3$ plus $2$ per mile. If $f(m)$ is the cost after $m$ miles, $f(m)=2m+3$. "
         "How many miles make the cost $17$?", "7",
         "Solve $2m+3=17$: $2m=14$, $m=7$.",
         ["8", "10", "14"]),
        ("SAT Stretch: The line through $(1,4)$ parallel to $x-2y=6$ has which standard form?", "$x-2y=-7$",
         "From $x-2y=6$, $y=\\dfrac{1}{2}x-3$, slope $\\dfrac{1}{2}$. Parallel: $y-4=\\dfrac{1}{2}(x-1)$, so "
         "$2y-8=x-1$, hence $x-2y=-7$.",
         ["$x-2y=6$", "$2x+y=6$", "$x+2y=9$"]),
        ("SAT Stretch: For $f(x)=mx+b$, $f(2)=11$ and $f(5)=5$. The slope $m$ is:", "-2",
         "$m=\\dfrac{5-11}{5-2}=\\dfrac{-6}{3}=-2$. Then $11=-4+b$, $b=15$, so $f(x)=-2x+15$.",
         ["2", "-3", "6"]),
        ("SAT Stretch: Which line is neither parallel nor perpendicular to $y=-\\dfrac{2}{3}x+1$?", "$y=\\dfrac{2}{3}x-4$",
         "Parallel would match slope $-\\dfrac{2}{3}$. Perpendicular would be $\\dfrac{3}{2}$. Slope $\\dfrac{2}{3}$ is neither.",
         ["$y=-\\dfrac{2}{3}x$", "$y=\\dfrac{3}{2}x+8$", "$2x+3y=0$"]),
        ("SAT Stretch: Line $n$ passes through $(0,4)$ and is perpendicular to $2x+y=6$. The $x$-intercept of $n$ is:",
         "$-8$",
         "From $y=-2x+6$ the given slope is $-2$, so the perpendicular slope is $\\dfrac{1}{2}$. Then $n$ is "
         "$y=\\dfrac{1}{2}x+4$. Set $y=0$: $0=\\dfrac{1}{2}x+4$, so $x=-8$. The intercept point is $(-8,0)$.",
         ["$4$", "$8$", "$-4$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    return qs


def build_unit3():
    title = "Algebra 1 Unit 3: Linear Functions & Graphs"
    description = (
        "Slope as rate of change, slope-intercept and point-slope forms, standard form, parallel and "
        "perpendicular lines, intercepts, and function notation for lines."
    )
    concepts = [
        "Slope as rate of change",
        "Slope-intercept form",
        "Point-slope and standard form",
        "Parallel and perpendicular",
        "Intercepts and graphing",
        "Function notation for lines",
    ]

    c1 = concept_block(
        "1. Slope as rate of change",
        [
            "Slope measures how steep a line is: $m=\\dfrac{\\text{rise}}{\\text{run}}=\\dfrac{y_2-y_1}{x_2-x_1}$ for two "
            "distinct points on the line. The value does not depend on which point you call “first,” because both "
            "the numerator and the denominator change sign together.",
            "Positive slope means the line rises from left to right. Negative slope means it falls. Slope $0$ is a "
            "horizontal line: $y$ never changes. A vertical line has undefined slope because the run is $0$.",
            "Rate of change in a story is slope with units. If a tank loses $3$ gallons every $2$ minutes, the slope "
            "of gallons versus minutes is $-\\dfrac{3}{2}$ gallons per minute.",
            "Counting slope from a graph: pick a lattice point, then walk a convenient run along the grid and count "
            "the matching rise. Simplify the fraction. A run of $0$ means you accidentally picked a vertical step.",
            "Collinear points share one slope. If $A$, $B$, and $C$ are on a line, the slope $AB$ equals the slope $BC$. "
            "That test is how you later decide whether three given points are collinear without drawing.",
            "Slope is the $m$ in every form you will write this unit. Graphing, parallel tests, and function notation "
            "all start with a correct $m$.",
        ],
        "Linear models in science and business are “start plus rate times time.” If the rate (slope) is wrong, the "
        "entire prediction is wrong even when the intercept is perfect.",
        "Label the two points, subtract $y$’s on top and $x$’s on bottom in the same order, then simplify. Ask whether "
        "the sign matches “uphill or downhill left to right.”",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(2, 1, -1, 3))],
                points=[(0, 1, "(0,1)"), (1, 3, "(1,3)")],
                xlim=(-2, 4), ylim=(-1, 7),
            ),
            "The line $y=2x+1$ with slope $2$",
            "From $(0,1)$ to $(1,3)$ the rise is $2$ and the run is $1$, so $m=2$.",
        )
        + solved(1, "Find the slope through $(2,1)$ and $(6,9)$.",
                 ["$m=\\dfrac{9-1}{6-2}=\\dfrac{8}{4}=2$."],
                 "$2$", "", "Easy")
        + solved(2, "Find the slope through $(-3,4)$ and $(1,-2)$.",
                 ["$m=\\dfrac{-2-4}{1-(-3)}=\\dfrac{-6}{4}=-\\dfrac{3}{2}$.",
                  "The line falls left to right, matching the negative sign."],
                 "$-\\dfrac{3}{2}$", "", "Medium")
        + solved(3, "A car’s distance $d$ (miles) after $t$ hours satisfies the points $(1,40)$ and $(3,160)$. "
                 "Interpret the slope.",
                 ["$m=\\dfrac{160-40}{3-1}=\\dfrac{120}{2}=60$.",
                  "The car travels $60$ miles per hour on this interval (constant speed)."],
                 "$60$ miles per hour", "", "SAT"),
        ("Subtracting in opposite orders",
         "If you do $y_2-y_1$ on top but $x_1-x_2$ on bottom, the sign of the slope flips. Keep the same order."),
        ("Write rise over run as a fraction first",
         "Even when the numbers are integers, keeping $\\dfrac{\\Delta y}{\\Delta x}$ visible prevents swapping them."),
        [
            "I can compute slope from two points.",
            "I can identify positive, negative, zero, and undefined slope from a graph.",
            "I can interpret slope as a rate with units.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Slope-intercept form",
        [
            "The slope-intercept equation of a nonvertical line is $y=mx+b$. The number $m$ is the slope; the number "
            "$b$ is the $y$-intercept, the value of $y$ when $x=0$. The graph meets the $y$-axis at $(0,b)$.",
            "To graph, plot $(0,b)$, then use slope as a second point: from the intercept, move run in $x$ and rise "
            "in $y$. Draw the unique line through those two points.",
            "To write the equation from a graph, read $b$ off the $y$-axis and count $m$ from a second lattice point. "
            "Then write $y=mx+b$ immediately.",
            "Solving for $y$ converts other forms into slope-intercept. From $2x+4y=12$, subtract $2x$ and divide by "
            "$4$ to get $y=-\\dfrac{1}{2}x+3$. Now slope and intercept are visible.",
            "Changing $b$ slides the line up or down without changing steepness. Changing $m$ rotates the line around "
            "its $y$-intercept (except when you pass through vertical, which this form cannot represent).",
            "This form is the default for linear functions $f(x)=mx+b$ in the last lesson of the unit.",
        ],
        "Once a line is $y=mx+b$, you can evaluate, compare rates, and later decide parallel versus perpendicular "
        "by glancing at $m$ alone.",
        "Solve for $y$ first whenever the equation is not already $y=\\ldots$. Then read $m$ and $b$ and plot "
        "$(0,b)$ plus one slope step.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(-0.5, 3, -2, 6))],
                points=[(0, 3, "(0,3)"), (4, 1, "(4,1)")],
                xlim=(-3, 7), ylim=(-1, 6),
            ),
            "$y=-\\dfrac{1}{2}x+3$",
            "Intercept $(0,3)$. Slope $-\\dfrac{1}{2}$: from $(0,3)$ run $4$, rise $-2$, landing on $(4,1)$.",
        )
        + solved(4, "State slope and $y$-intercept of $y=5x-2$.",
                 ["$m=5$, $b=-2$, so the intercept point is $(0,-2)$."],
                 "$m=5$, $(0,-2)$", "", "Easy")
        + solved(5, "Write $6x+2y=10$ in slope-intercept form.",
                 ["$2y=-6x+10$.",
                  "$y=-3x+5$."],
                 "$y=-3x+5$", "", "Medium")
        + solved(6, "A line has slope $-4$ and passes through $(0,7)$. Write its equation and find $y$ when $x=3$.",
                 ["$y=-4x+7$.",
                  "$y=-12+7=-5$."],
                 "$y=-4x+7$; when $x=3$, $y=-5$", "", "Hard"),
        ("Calling the $x$-intercept $b$",
         "In $y=mx+b$, $b$ is the $y$-intercept. The $x$-intercept is found by setting $y=0$ and solving for $x$."),
        ("Plot $b$, then walk the slope",
         "Never start at the origin unless $b=0$. The first dot is $(0,b)$, not $(0,0)$."),
        [
            "I can read $m$ and $b$ from $y=mx+b$.",
            "I can convert a linear equation into slope-intercept form.",
            "I can graph from intercept plus slope.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Point-slope and standard form",
        [
            "Point-slope form is $y-y_1=m(x-x_1)$ for a nonvertical line through $(x_1,y_1)$ with slope $m$. It is "
            "the fastest form when you know a point that is not the $y$-intercept.",
            "Distributing and adding $y_1$ converts point-slope into slope-intercept. Both name the same line; they "
            "are different outfits, not different objects.",
            "Standard form $Ax+By=C$ is useful for intercepts and integer coefficients. A common classroom convention "
            "is $A$, $B$, $C$ integers, $A\\geq 0$, and $\\gcd(|A|,|B|,|C|)=1$.",
            "You may multiply an entire standard-form equation by a nonzero constant and still have the same line. "
            "$2x+y=5$ and $4x+2y=10$ are identical as graphs.",
            "Vertical lines $x=k$ cannot be written as $y=mx+b$ or in point-slope, but they are already simple in "
            "standard form (with $B=0$). Horizontal lines are $y=k$, or $By=C$.",
            "Choose the form that matches the given information: slope and intercept $\\to$ $y=mx+b$; slope and a "
            "point $\\to$ point-slope; intercepts or integer constraints $\\to$ standard.",
        ],
        "Later systems of equations are often given in standard form so elimination is clean. Point-slope is the "
        "bridge from two points (compute $m$, then write the line) to a graph.",
        "If you know $m$ and a point, write point-slope first, then convert only if the answer format demands "
        "$y=mx+b$ or $Ax+By=C$.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(3, -1, 0, 3))],
                points=[(2, 5, "(2,5)")],
                xlim=(-1, 4), ylim=(-2, 8),
            ),
            "The line $y-5=3(x-2)$",
            "It passes through $(2,5)$ with slope $3$. Equivalent: $y=3x-1$.",
        )
        + solved(7, "Write point-slope for slope $-1$ through $(4,2)$.",
                 ["$y-2=-1(x-4)$."],
                 "$y-2=-(x-4)$", "", "Easy")
        + solved(8, "Convert $y-1=2(x+3)$ to slope-intercept.",
                 ["$y-1=2x+6$.",
                  "$y=2x+7$."],
                 "$y=2x+7$", "", "Medium")
        + solved(9, "Write $y=\\dfrac{2}{3}x-4$ in standard form with integer coefficients.",
                 ["Multiply by $3$: $3y=2x-12$.",
                  "Rearrange: $-2x+3y=-12$, or multiply by $-1$: $2x-3y=12$."],
                 "$2x-3y=12$", "", "SAT"),
        ("Dropping the minus inside $(x-x_1)$",
         "Through $(-3,1)$ the factor is $(x-(-3))=(x+3)$, not $(x-3)$."),
        ("Convert only after the form is written",
         "Write point-slope with parentheses intact. Distribution is a second, separate line of work."),
        [
            "I can write point-slope from $m$ and a point.",
            "I can convert among point-slope, slope-intercept, and standard form.",
            "I can recognize vertical lines as $x=k$.",
        ],
        11,
    )

    c4 = concept_block(
        "4. Parallel and perpendicular",
        [
            "Parallel lines in the plane never meet. For nonvertical lines, that happens exactly when the slopes are "
            "equal and the lines are not the same line (different intercepts).",
            "Perpendicular lines meet at a right angle. For two nonvertical lines, the slopes $m_1$ and $m_2$ satisfy "
            "$m_1 m_2=-1$: each is the negative reciprocal of the other.",
            "A horizontal line (slope $0$) is perpendicular to a vertical line (undefined slope). Two vertical lines "
            "are parallel; two horizontal lines are parallel.",
            "To write the line through a given point parallel to a given line, copy the slope and use point-slope. "
            "For perpendicular, copy the negative reciprocal instead.",
            "Always put both equations in $y=mx+b$ (when they are nonvertical) before you compare slopes. Standard "
            "form hides $m$ until you solve for $y$.",
            "If the slopes match and a shared point exists, the “two” lines are actually the same line (infinitely "
            "many intersection points). That distinction returns in Unit 4 systems.",
        ],
        "Geometry and physics use right angles constantly. Algebra 1’s slope test is the coordinate version of a "
        "protractor. Systems later ask whether two lines meet once, never, or always.",
        "Solve both equations for $y$, compare $m$. Equal $\\to$ parallel (or identical). Product $-1$ $\\to$ "
        "perpendicular. Then use the given point to lock $b$.",
        lesson_figure(
            xy_graph(
                curves=[
                    ("#4f46e5", _seg(0.5, 1, -4, 4)),
                    ("#dc2626", _seg(-2, 2, -1, 3)),
                ],
                points=[(0, 1, "(0,1)"), (2, -2, "")],
                xlim=(-4, 5), ylim=(-4, 5),
            ),
            "Perpendicular lines with slopes $\\dfrac{1}{2}$ and $-2$",
            "The product of the slopes is $-1$. They meet at a right angle.",
        )
        + solved(10, "Are $y=4x-1$ and $y=4x+9$ parallel, perpendicular, or neither?",
                 ["Both slopes are $4$, intercepts differ, so they are parallel distinct lines."],
                 "parallel", "", "Easy")
        + solved(11, "Find the slope of a line perpendicular to $y=-\\dfrac{2}{5}x+3$.",
                 ["Negative reciprocal of $-\\dfrac{2}{5}$ is $\\dfrac{5}{2}$."],
                 "$\\dfrac{5}{2}$", "", "Medium")
        + solved(12, "Write the line through $(1,-2)$ perpendicular to $2x+y=7$.",
                 ["$y=-2x+7$, so given slope is $-2$. Perpendicular slope is $\\dfrac{1}{2}$.",
                  "$y+2=\\dfrac{1}{2}(x-1)$, so $y=\\dfrac{1}{2}x-\\dfrac{5}{2}$."],
                 "$y=\\dfrac{1}{2}x-\\dfrac{5}{2}$", "", "Hard"),
        ("Reciprocal without the negative",
         "Perpendicular to slope $3$ is $-\\dfrac{1}{3}$, not $\\dfrac{1}{3}$. Both the flip and the sign change."),
        ("Compare after solving for $y$",
         "Do not compare the $A$ and $B$ of standard form blindly. $2x+y=1$ and $4x+2y=7$ look different but have "
         "the same slope."),
        [
            "I can test parallel by equal slopes.",
            "I can test perpendicular by negative reciprocals.",
            "I can write a parallel or perpendicular line through a given point.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Intercepts and graphing",
        [
            "The $x$-intercept is where the graph meets the $x$-axis, so $y=0$. The $y$-intercept is where it meets "
            "the $y$-axis, so $x=0$. A nonvertical, nonhorizontal line has one of each (unless it passes through the "
            "origin, where they coincide at $(0,0)$).",
            "From $Ax+By=C$, the $x$-intercept is $\\left(\\dfrac{C}{A},0\\right)$ when $A\\neq 0$, and the "
            "$y$-intercept is $\\left(0,\\dfrac{C}{B}\\right)$ when $B\\neq 0$. This is why standard form is handy "
            "for a two-intercept sketch.",
            "To graph by intercepts: plot both intercepts and draw the line through them. If one intercept is missing "
            "(horizontal or vertical), you already know the picture.",
            "A third checkpoint — plug a third $x$ and confirm the $y$ — catches arithmetic errors in the intercepts. "
            "If the third point is off the line, one intercept is wrong.",
            "Covering $x$ with a finger to read the $y$-intercept, and covering $y$ to read the $x$-intercept, is a "
            "fast mental move for $Ax+By=C$.",
            "Intercepts are also the zeros of linear functions: $f(x)=0$ is the $x$-intercept of $y=f(x)$.",
        ],
        "Sketching by intercepts is faster than a full slope walk when the intercepts are integers. It is also the "
        "graph you need before discussing systems in Unit 4.",
        "Set $x=0$, then set $y=0$. Plot both points. Draw the line. Check with one extra point.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", [(-1, 8), (6, -6)])],
                points=[(3, 0, "(3,0)"), (0, 6, "(0,6)")],
                xlim=(-2, 7), ylim=(-4, 8),
            ),
            "Intercepts of $2x+y=6$",
            "$x$-intercept $(3,0)$ and $y$-intercept $(0,6)$. The line through them is the graph.",
        )
        + solved(13, "Find both intercepts of $x+2y=8$.",
                 ["$y=0\\Rightarrow x=8$, so $(8,0)$.",
                  "$x=0\\Rightarrow 2y=8$, $y=4$, so $(0,4)$."],
                 "$(8,0)$ and $(0,4)$", "", "Easy")
        + solved(14, "Find the intercepts of $y=\\dfrac{3}{2}x-6$.",
                 ["$y$-intercept: $(0,-6)$.",
                  "$x$-intercept: $0=\\dfrac{3}{2}x-6$, so $\\dfrac{3}{2}x=6$, $x=4$, hence $(4,0)$."],
                 "$(4,0)$ and $(0,-6)$", "", "Medium")
        + solved(15, "A line has intercepts $(a,0)$ and $(0,a)$ with $a\\neq 0$. Write its slope-intercept equation.",
                 ["Slope $m=\\dfrac{a-0}{0-a}=-1$.",
                  "$y$-intercept $a$, so $y=-x+a$."],
                 "$y=-x+a$", "", "SAT"),
        ("Swapping the two intercepts",
         "$(4,0)$ is on the $x$-axis. $(0,4)$ is on the $y$-axis. Listing them in the wrong order is a graphing "
         "error even when the numbers are right."),
        ("Cover $x$, then cover $y$",
         "On $Ax+By=C$, covering the $x$ term shows $By=C$; covering the $y$ term shows $Ax=C$. Write the two "
         "points before you draw."),
        [
            "I can find $x$- and $y$-intercepts from an equation.",
            "I can graph a line from two intercepts.",
            "I can check with a third point.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Function notation for lines",
        [
            "A linear function can be written $f(x)=mx+b$. The graph is the line $y=mx+b$. The notation $f(x)$ names "
            "the output when the input is $x$; it is not $f$ times $x$.",
            "Evaluating $f(3)$ means substituting $x=3$ into the rule. Solving $f(x)=k$ means finding the input that "
            "produces output $k$, which is the $x$-coordinate of the point where the line meets $y=k$.",
            "The $y$-intercept is $f(0)$. The zero of $f$ is the solution of $f(x)=0$, which is the $x$-intercept of "
            "the graph.",
            "Tables of values are just evaluations: pick $x$, compute $f(x)$, plot $(x,f(x))$. Three noncollinear "
            "points would mean you are not actually linear — a useful check.",
            "Average rate of change of $f$ between $x=a$ and $x=c$ is $\\dfrac{f(c)-f(a)}{c-a}$, which equals the "
            "constant slope $m$ for any linear $f$. That is what “constant rate” means.",
            "Function notation is the language of later units: quadratics $h(t)$, exponentials $P(t)$, and piecewise "
            "rules. Lines are the first family where $f(x)$ and a graph sit side by side.",
        ],
        "Tests will ask $f(2)$ and “solve $f(x)=2$” in the same item. Mixing those up — substituting versus solving — "
        "is the main notation error to kill now.",
        "Read $f(x)$ as “output at input $x$.” To evaluate, replace $x$. To solve $f(x)=k$, set the formula equal to "
        "$k$ and use Unit 2.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(2, -3, -1, 4))],
                points=[(0, -3, "f(0)=−3"), (3, 3, "f(3)=3")],
                xlim=(-2, 5), ylim=(-5, 6), ylab="f(x)",
            ),
            "The linear function $f(x)=2x-3$",
            "The labeled points are evaluations, not a second line. $f(3)=3$ sits at $(3,3)$.",
        )
        + solved(16, "If $f(x)=4x+1$, find $f(-2)$.",
                 ["$f(-2)=4(-2)+1=-8+1=-7$."],
                 "$-7$", "", "Easy")
        + solved(17, "If $g(x)=-3x+9$, solve $g(x)=0$.",
                 ["$-3x+9=0$, so $3x=9$, $x=3$.",
                  "The graph’s $x$-intercept is $(3,0)$."],
                 "$x=3$", "", "Medium")
        + solved(18, "A linear $f$ satisfies $f(1)=5$ and $f(4)=14$. Find $f(x)$ and then $f(10)$.",
                 ["$m=\\dfrac{14-5}{4-1}=3$. Then $5=3(1)+b$, so $b=2$.",
                  "$f(x)=3x+2$.",
                  "$f(10)=32$."],
                 "$f(x)=3x+2$; $f(10)=32$", "", "SAT"),
        ("Treating $f(x+1)$ as $f(x)+1$",
         "For $f(x)=2x$, $f(x+1)=2x+2$, while $f(x)+1=2x+1$. Substitute the entire input $x+1$ everywhere."),
        ("Decide: evaluate or solve?",
         "If the problem gives $x$ and wants $y$, substitute. If it gives $y$ (or $f(x)=k$) and wants $x$, solve."),
        [
            "I can evaluate $f(x)=mx+b$ at a number.",
            "I can solve $f(x)=k$.",
            "I can build $f$ from two points.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u3_questions()


# ===========================================================================
# UNIT 4: Systems of Linear Equations
# ===========================================================================

def _u4_questions():
    qs = []
    idx = 1

    for text, ans, expl, dist in [
        ("The graphical solution of a system is the point where:", "the two lines intersect",
         "A solution $(x,y)$ lies on both lines, so it is an intersection point.",
         ["the $y$-intercepts match", "the slopes match", "a line crosses the origin"]),
        ("The lines $y=x+1$ and $y=-x+5$ meet at:", "$(2,3)$",
         "Set $x+1=-x+5$: $2x=4$, $x=2$, then $y=3$.",
         ["$(1,2)$", "$(0,5)$", "$(5,0)$"]),
        ("If two graphed lines look parallel and distinct, the system has:", "no solution",
         "Parallel distinct lines never meet, so no ordered pair satisfies both.",
         ["one solution", "infinitely many solutions", "exactly two solutions"]),
        ("A solution of a system must make:", "both equations true",
         "One true equation is not enough; the pair $(x,y)$ has to sit on both graphs.",
         ["only the first equation true", "the slopes equal", "x=0"]),
        ("The system $y=2x$ and $x=3$ has solution:", "$(3,6)$",
         "The second equation is a vertical line. Plug $x=3$ into $y=2x$: $y=6$.",
         ["$(2,3)$", "$(3,2)$", "$(6,3)$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("To solve $y=x+4$ and $2x+y=10$ by substitution, replace $y$ in the second equation with:", "$x+4$",
         "The first equation already isolates $y$. Substitute that expression for $y$.",
         ["$10-2x$", "$2x$", "$x-4$"]),
        ("Solving $y=3x-1$ and $y=x+5$ by substitution yields $x$ equal to:", "3",
         "$3x-1=x+5$, $2x=6$, $x=3$, then $y=8$.",
         ["5", "1", "4"]),
        ("If $x=2y$ and $3x-y=10$, then $y$ equals:", "2",
         "Substitute: $3(2y)-y=10$, $6y-y=10$, $5y=10$, $y=2$, so $x=4$.",
         ["4", "10", "1"]),
        ("After substituting $y=5-x$ into $x+2y=7$, the equation in $x$ is:", "$x+2(5-x)=7$",
         "Replace every $y$ with $5-x$. Then simplify: $x+10-2x=7$, $-x=-3$, $x=3$.",
         ["$x+2y=5-x$", "$x=5-x$", "$2(5-x)=7$"]),
        ("The system $y=2x+1$ and $4x-2y=-2$ has how many solutions?", "infinitely many",
         "Substitute: $4x-2(2x+1)=-2$, $4x-4x-2=-2$, $-2=-2$, always true. The second equation is a multiple of the first.",
         ["none", "exactly one", "exactly two"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Adding $x+y=4$ and $x-y=2$ eliminates $y$ and gives:", "$2x=6$",
         "The $y$ terms cancel: $2x=6$, so $x=3$, then $y=1$.",
         ["$2y=6$", "$2x=2$", "$x=4$"]),
        ("To eliminate $y$ in $2x+3y=7$ and $4x-3y=5$, you should:", "add the equations",
         "The $y$ coefficients are already opposites $3$ and $-3$. Adding cancels $y$.",
         ["subtract the second from the first only after swapping", "multiply the first by 4", "divide by 3"]),
        ("For $3x+2y=8$ and $x+2y=4$, eliminating $y$ by subtraction gives:", "$2x=4$",
         "Subtract: $(3x+2y)-(x+2y)=8-4$, so $2x=4$, $x=2$, then $y=1$.",
         ["$4x=12$", "$2y=4$", "$3x=8$"]),
        ("If you multiply $x+2y=3$ by $2$ before adding to $3x-4y=1$, the goal is to:", "cancel the $y$ terms",
         "Twice the first has $4y$, opposite of $-4y$. Then add.",
         ["cancel the $x$ terms immediately", "make both intercepts 0", "graph faster"]),
        ("Elimination on $2x+y=10$ and $2x+y=7$ produces:", "a contradiction, so no solution",
         "Subtracting gives $0=3$, false. The lines are parallel.",
         ["$(0,0)$", "infinitely many solutions", "$x=2$"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("A system whose graphs are the same line has:", "infinitely many solutions",
         "Every point on the line satisfies both equations.",
         ["no solution", "exactly one solution", "exactly two solutions"]),
        ("The system $y=3x+1$ and $y=3x-4$ has:", "no solution",
         "Equal slopes, different intercepts: parallel distinct lines.",
         ["one solution", "infinitely many", "the solution $(0,1)$"]),
        ("If both variables vanish and you obtain $0=0$, the system has:", "infinitely many solutions",
         "$0=0$ is always true: the equations were dependent (the same line).",
         ["no solution", "only $x=0$", "only $y=0$"]),
        ("If both variables vanish and you obtain $0=5$, the system has:", "no solution",
         "$0=5$ is never true: inconsistent equations.",
         ["infinitely many solutions", "$(5,0)$", "$(0,5)$"]),
        ("$2x+4y=10$ and $x+2y=5$ represent:", "the same line",
         "The first is twice the second. Infinitely many solutions, not a unique pair.",
         ["parallel distinct lines", "perpendicular lines", "a single point only"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The solution of a system of linear inequalities is:", "a region (often a half-plane overlap)",
         "Each inequality shades a half-plane; the system is their intersection.",
         ["always a single point", "always a line", "the empty set only"]),
        ("For $y>x$ the boundary $y=x$ is drawn:", "dashed, because equality is not allowed",
         "Strict inequalities get dashed boundaries. $\\geq$ or $\\leq$ get solid boundaries.",
         ["solid", "not drawn at all", "as a single open dot"]),
        ("A test point of $(0,0)$ in $x+y>2$ shows that the origin is:", "not in the solution region",
         "$0+0>2$ is false, so shade the side that does not include the origin.",
         ["in the solution region", "on the boundary", "the only solution"]),
        ("The corner of $x\\geq 0$, $y\\geq 0$, $x+y\\leq 4$ at $(0,4)$ is:", "a vertex of the feasible region",
         "It is an intersection of $x=0$ and $x+y=4$ in the first quadrant, included because of $\\leq$ and $\\geq$.",
         ["excluded because $x=0$", "not on any boundary", "the only solution"]),
        ("$y\\leq 2$ and $y\\geq 5$ together have:", "no points in common",
         "No number is both $\\leq 2$ and $\\geq 5$. The shaded bands do not overlap.",
         ["the strip $2\\leq y\\leq 5$", "the line $y=3$", "the whole plane"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("Adult tickets cost $\\$8$ and child tickets $\\$5$. If $a+c=10$ and $8a+5c=68$, then $a$ equals:", "6",
         "From $a=10-c$, $8(10-c)+5c=68$, $80-8c+5c=68$, $-3c=-12$, $c=4$, so $a=6$.",
         ["4", "8", "10"]),
        ("Two numbers sum to $20$ and differ by $6$. The larger is:", "13",
         "$x+y=20$, $x-y=6$. Add: $2x=26$, $x=13$, $y=7$.",
         ["14", "10", "6"]),
        ("A boat goes $24$ miles downstream in $2$ hours and back upstream in $3$ hours. If $r$ is still-water speed "
         "and $c$ is current, then $r+c$ equals:", "12",
         "Downstream rate is $24/2=12=r+c$.",
         ["8", "10", "4"]),
        ("Mixture: $x$ liters of $10\\%$ acid plus $y$ liters of $40\\%$ acid make $20$ liters of $25\\%$ acid. Then $x$ is:",
         "10",
         "$x+y=20$ and $0.10x+0.40y=5$. Substitute $y=20-x$: $0.10x+0.40(20-x)=5$, $0.10x+8-0.40x=5$, $-0.30x=-3$, $x=10$.",
         ["5", "15", "8"]),
        ("Phone plan $A$ is $20+0.10m$ dollars and plan $B$ is $5+0.15m$. They cost the same when $m$ minutes equal:",
         "300",
         "$20+0.10m=5+0.15m$, $15=0.05m$, $m=300$.",
         ["200", "100", "250"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("The ordered pair $(1,4)$ is the intersection of $y=3x+1$ and:", "$y=-x+5$",
         "Check: $3(1)+1=4$ and $-1+5=4$. Other lines may miss $(1,4)$.",
         ["$y=x$", "$y=3x$", "$y=4x$"]),
        ("Substituting $x=y-3$ into $2x+y=12$ produces:", "$2(y-3)+y=12$",
         "Then $2y-6+y=12$, $3y=18$, $y=6$, $x=3$.",
         ["$2x+(x+3)=12$", "$x+y=12$", "$2(y+3)+y=12$"]),
        ("A good first elimination move for $5x+2y=11$ and $3x-2y=5$ is:", "add to cancel $y$",
         "The $y$ coefficients are already opposites.",
         ["subtract to cancel $x$", "divide the first by 5", "graph only"]),
        ("Dependent equations describe:", "the same line",
         "Infinitely many solutions; one equation is a scalar multiple of the other.",
         ["parallel distinct lines", "perpendicular lines", "a single point"]),
        ("Shading $y\\geq x$ includes the point:", "$(0,2)$",
         "$2\\geq 0$ is true. $(2,0)$ would fail $0\\geq 2$.",
         ["$(2,0)$", "$(1,-1)$", "$(3,1)$"]),
        ("The break-even of $C=4n+20$ and $R=6n$ (cost and revenue) occurs at $n=$:", "10",
         "$4n+20=6n$, $20=2n$, $n=10$.",
         ["5", "20", "24"]),
        ("The unique solution of $x-y=1$ and $x+y=7$ is:", "$(4,3)$",
         "Add: $2x=8$, $x=4$, then $y=3$.",
         ["$(3,4)$", "$(7,1)$", "$(1,7)$"]),
        ("Graphing $x+y<3$ uses a dashed line $x+y=3$ because:", "points on the line are not solutions",
         "Strict inequality excludes the boundary.",
         ["the slope is undefined", "there is no intercept", "the region is a single point"]),
        ("If $3x-y=4$ and $6x-2y=8$, the system is:", "dependent (infinite solutions)",
         "The second equation is twice the first.",
         ["inconsistent", "independent with one solution", "not linear"]),
        ("The solution of $y=5$ and $x=-2$ is:", "$(-2,5)$",
         "Horizontal meets vertical at that ordered pair.",
         ["$(5,-2)$", "$(0,5)$", "$(-2,0)$"]),
        ("After elimination, $0=0$ means you should:", "describe the line of solutions",
         "Infinitely many solutions: report the line (solve one equation for $y$).",
         ["write no solution", "write $(0,0)$ only", "divide by zero"]),
        ("Two numbers have sum $15$ and the larger is $4$ more than the smaller. The larger number is:",
         "9.5",
         "Let $s$ be the smaller. Then $s+(s+4)=15$, so $2s=11$ and $s=5.5$. The larger is $9.5$.",
         ["11", "7.5", "4"]),
        ("The feasible corner of $x\\geq 1$, $y\\geq 2$, $x+y\\leq 6$ that maximizes $x+2y$ among vertices "
         "$(1,2)$, $(1,5)$, $(4,2)$ is:", "$(1,5)$",
         "Values: $1+4=5$, $1+10=11$, $4+4=8$. The maximum is $11$ at $(1,5)$.",
         ["$(1,2)$", "$(4,2)$", "$(0,0)$"]),
        ("Solving $2x+3y=12$ and $x=y$ by substitution gives:", "$(\\dfrac{12}{5},\\dfrac{12}{5})$",
         "$2y+3y=12$, $5y=12$, $y=\\dfrac{12}{5}=x$.",
         ["$(3,3)$", "$(12,12)$", "$(2,3)$"]),
        ("Inconsistent systems correspond to:", "parallel distinct lines",
         "No intersection point exists.",
         ["coinciding lines", "perpendicular lines that meet", "a single intercept"]),
        ("A chemist mixes $x$ ml of $20\\%$ solution with $30$ ml of $50\\%$ to get $30\\%$. Then $x$ is:", "60",
         "$0.20x+15=0.30(x+30)$, $0.20x+15=0.30x+9$, $6=0.10x$, $x=60$.",
         ["30", "45", "20"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    for text, ans, expl, dist in [
        ("SAT Stretch: Solve $\\begin{cases}3x-2y=4\\\\ 5x+2y=20\\end{cases}$. The value of $x$ is:", "3",
         "Add: $8x=24$, $x=3$. Then $9-2y=4$, $-2y=-5$, $y=\\dfrac{5}{2}$. The pair is $\\left(3,\\dfrac{5}{2}\\right)$.",
         ["4", "2", "8"]),
        ("SAT Stretch: For which $k$ is $\\begin{cases}x+2y=5\\\\ 2x+4y=k\\end{cases}$ inconsistent?", "any $k\\neq 10$",
         "The second left side is twice the first. Consistency requires $k=10$. Any other $k$ is $0=$ nonzero.",
         ["$k=10$", "$k=5$", "$k=0$ only"]),
        ("SAT Stretch: The system $y=x+1$ and $2x-2y=8$ has how many solutions?", "none",
         "The second equation is $2x-2y=8$, or $x-y=4$, so $y=x-4$. The lines $y=x+1$ and $y=x-4$ are parallel and distinct.",
         ["one", "two", "infinitely many"]),
        ("SAT Stretch: Movie tickets: $2$ adult and $3$ child cost $\\$43$; $4$ adult and $1$ child cost $\\$51$. "
         "An adult ticket costs:", "11",
         "From $4a+c=51$, $c=51-4a$. Substitute into $2a+3c=43$: $2a+3(51-4a)=43$, $2a+153-12a=43$, $-10a=-110$, $a=11$. "
         "Then $c=7$. Check: $2(11)+3(7)=22+21=43$.",
         ["7", "8", "13"]),
        ("SAT Stretch: The feasible region $x\\geq 0$, $y\\geq 0$, $2x+y\\leq 8$, $x+2y\\leq 8$ has vertices at "
         "$(0,0)$, $(4,0)$, $(0,4)$, and:", "$(\\dfrac{8}{3},\\dfrac{8}{3})$",
         "Solve $2x+y=8$ and $x+2y=8$: multiply second by $2$: $2x+4y=16$. Subtract first: $3y=8$, $y=\\dfrac{8}{3}$, "
         "$x=8-\\dfrac{16}{3}=\\dfrac{8}{3}$.",
         ["$(2,2)$", "$(8,0)$", "$(4,4)$"]),
        ("SAT Stretch: Solve $\\begin{cases}y=2x-1\\\\ 3x-y=8\\end{cases}$. The $y$-coordinate of the solution is:", "13",
         "Substitute: $3x-(2x-1)=8$, so $3x-2x+1=8$, $x=7$, then $y=2(7)-1=13$. Check: $3(7)-13=8$.",
         ["9", "8", "7"]),
        ("SAT Stretch: A river current is $2$ mph. A boat travels $36$ miles downstream in $3$ hours. The boat’s "
         "still-water speed is:", "10",
         "Downstream speed is $36/3=12$ mph, which equals $r+2$, so $r=10$.",
         ["12", "8", "14"]),
        ("SAT Stretch: The lines $ax+2y=6$ and $3x-y=1$ are perpendicular. Then $a$ equals:", "$\\dfrac{2}{3}$",
         "First line: $y=-\\dfrac{a}{2}x+3$, slope $-\\dfrac{a}{2}$. Second: $y=3x-1$, slope $3$. "
         "Perpendicular to slope $3$ is $-\\dfrac{1}{3}$. Set $-\\dfrac{a}{2}=-\\dfrac{1}{3}$, so $a=\\dfrac{2}{3}$.",
         ["$6$", "$-6$", "$3$"]),
        ("SAT Stretch: A chemist mixes a $20\\%$ acid solution with a $50\\%$ solution to make $30$ L of $30\\%$ acid. "
         "How many liters of the $20\\%$ solution are used?", "20",
         "Let $x$ be liters of $20\\%$ and $30-x$ liters of $50\\%$. Acid: $0.20x+0.50(30-x)=0.30\\cdot 30$. "
         "Then $0.20x+15-0.50x=9$, so $-0.30x=-6$ and $x=20$. Check: $0.20(20)+0.50(10)=4+5=9$, and $30\\%$ of $30$ is $9$.",
         ["10", "15", "18"]),
    ]:
        qs.append(mq(text, ans, expl, idx, distractors=dist)); idx += 1

    return qs


def build_unit4():
    title = "Algebra 1 Unit 4: Systems of Linear Equations"
    description = (
        "Graphical solutions, substitution, elimination, no-solution and infinite-solution cases, systems of "
        "inequalities, and linear word-problem systems."
    )
    concepts = [
        "Graphical solutions",
        "Substitution",
        "Elimination",
        "No solution and infinitely many",
        "Systems of inequalities",
        "Word-problem systems",
    ]

    c1 = concept_block(
        "1. Graphical solutions",
        [
            "A system of two linear equations is two lines in the same plane. An ordered pair $(x,y)$ is a solution "
            "when it lies on both lines at once — their intersection.",
            "Three geometric pictures cover every case: the lines cross once (one solution), they are parallel and "
            "distinct (no solution), or they are the same line (infinitely many solutions).",
            "To solve graphically, graph each line carefully — intercepts plus a slope check — and read the "
            "intersection. Integer intersections are reliable; fractional ones are easier algebraically.",
            "A vertical line $x=a$ with a nonvertical $y=mx+b$ meets at $(a, ma+b)$. You can plot that without "
            "guessing.",
            "Graphing is also a check on algebra: after substitution or elimination, the pair you found should sit "
            "on both original lines.",
            "When the picture is messy, switch to algebra. The graph tells you which case you are in; the algebra "
            "gives exact coordinates.",
        ],
        "Seeing the three pictures now makes the “no solution / infinite” algebra in this unit obvious instead of "
        "mysterious. It is also how you later shade systems of inequalities.",
        "Graph both lines, then ask: one crossing, never, or always? If they cross, read $(x,y)$ and substitute "
        "back into both equations.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(1, 1, -2, 4)), ("#dc2626", _seg(-1, 5, -1, 5))],
                points=[(2, 3, "(2,3)")],
                xlim=(-3, 6), ylim=(-1, 7),
            ),
            "The system $y=x+1$ and $y=-x+5$",
            "The unique intersection is $(2,3)$. That ordered pair is the solution of the system.",
        )
        + solved(1, "Solve graphically: $y=x$ and $y=4-x$.",
                 ["Set $x=4-x$: $2x=4$, $x=2$, $y=2$.",
                  "The intersection is $(2,2)$."],
                 "$(2,2)$", "", "Easy")
        + solved(2, "Estimate the solution of $y=2x-1$ and $x=3$ from a graph, then confirm.",
                 ["The vertical line $x=3$ meets $y=2(3)-1=5$.",
                  "Solution $(3,5)$."],
                 "$(3,5)$", "", "Medium")
        + solved(3, "Explain why $y=\\dfrac{1}{2}x+1$ and $x-2y=-2$ have infinitely many solutions.",
                 ["Solve the second for $y$: $x-2y=-2$ becomes $-2y=-x-2$, so $y=\\dfrac{1}{2}x+1$.",
                  "That is the same equation as the first line.",
                  "The graphs coincide, so every point on the line is a solution."],
                 "they are the same line", "", "Hard"),
        ("Reading a nearby lattice point",
         "If the crossing is not on a grid intersection, do not round to the nearest integer and call it done. "
         "Switch to substitution for an exact pair."),
        ("Graph both, then check both",
         "A point on one line only is not a system solution. Plug into both equations every time."),
        [
            "I can identify one, none, or infinitely many from a graph.",
            "I can read an integer intersection.",
            "I can confirm a graphical solution by substitution.",
        ],
        1,
    )

    c2 = concept_block(
        "2. Substitution",
        [
            "Substitution solves a system by replacing one variable with an expression in the other. If a variable is "
            "already isolated, that equation is the one you substitute from.",
            "Typical start: from $y=3x-1$ and $2x+y=10$, replace $y$ in the second: $2x+(3x-1)=10$. Solve the resulting "
            "one-variable equation, then back-substitute.",
            "If neither variable is isolated, solve the easier equation for one variable first — look for a "
            "coefficient of $1$ or $-1$ — then substitute.",
            "Parentheses matter: substituting $x=y-4$ into $3x$ is $3(y-4)$, not $3y-4$. Distribution errors here "
            "create a wrong line.",
            "After you have both coordinates, check in the equation you did not substitute into. Checking in the "
            "source equation is almost automatic and hides mistakes.",
            "If substitution produces $0=0$, the system is dependent. If it produces $0=5$, it is inconsistent. Those "
            "are complete answers, not broken methods.",
        ],
        "Substitution is the default when one equation is already $y=mx+b$. Word problems that define one quantity "
        "in terms of another are substitution in disguise.",
        "Isolate the friendliest variable, wrap the expression in parentheses as you substitute, solve, then plug "
        "back. Check in the other original equation.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(3, -1, 0, 4)), ("#dc2626", _seg(1, 5, 0, 5))],
                points=[(3, 8, "(3,8)")],
                xlim=(-1, 6), ylim=(-2, 11),
            ),
            "$y=3x-1$ and $y=x+5$ meet at $(3,8)$",
            "Substitution sets $3x-1=x+5$. The intersection is the algebraic solution.",
        )
        + solved(4, "Solve $y=x+2$ and $x+y=10$.",
                 ["$x+(x+2)=10$, $2x=8$, $x=4$, $y=6$."],
                 "$(4,6)$", "", "Easy")
        + solved(5, "Solve $x=2y+1$ and $3x-4y=11$.",
                 ["Substitute $x$: $3(2y+1)-4y=11$.",
                  "$6y+3-4y=11$, so $2y=8$ and $y=4$.",
                  "Then $x=8+1=9$. Check: $3(9)-4(4)=27-16=11$."],
                 "$(9,4)$", "", "Medium")
        + solved(6, "Solve $y=4-2x$ and $4x+2y=8$.",
                 ["$4x+2(4-2x)=8$, $4x+8-4x=8$, $8=8$.",
                  "Identity: infinitely many solutions — all points on $y=4-2x$."],
                 "infinitely many; $y=4-2x$", "", "SAT"),
        ("Forgetting parentheses",
         "Replacing $x$ with $y-3$ in $2x+y$ is $2(y-3)+y$, not $2y-3+y$."),
        ("Check in the other equation",
         "The equation you substituted from will almost always “check.” The unused original is the real test."),
        [
            "I can substitute an isolated variable.",
            "I can back-substitute to find the second coordinate.",
            "I can recognize $0=0$ and $0=k$ outcomes.",
        ],
        6,
    )

    c3 = concept_block(
        "3. Elimination",
        [
            "Elimination (linear combination) adds a multiple of one equation to the other so that a variable "
            "cancels. It shines when both equations are in standard form $Ax+By=C$.",
            "If coefficients of $y$ are already opposites, add. If they are equal, subtract. Otherwise multiply one "
            "or both equations to manufacture opposites.",
            "Whatever you multiply, multiply every term, including the constant. Multiplying only the variable terms "
            "destroys equality.",
            "After one variable is gone, solve the remaining one-variable equation, then substitute into either "
            "original to get the other coordinate.",
            "The same $0=0$ / $0=k$ messages appear as in substitution. Elimination does not create extra solutions; "
            "it only reveals the case you are in.",
            "Choosing which variable to eliminate is strategy: pick the pair of coefficients with the smallest least "
            "common multiple so the arithmetic stays small.",
        ],
        "Larger systems (three variables) and later matrix methods are organized elimination. Getting comfortable "
        "with multiples now pays off in Algebra 2.",
        "Line up like terms. Make one pair of coefficients opposites. Add. Solve. Substitute. Check both originals.",
        lesson_figure(
            svg_balance("x+y=7", "x-y=1"),
            "Adding $x+y=7$ and $x-y=1$",
            "The $y$ terms cancel, leaving $2x=8$. Elimination is adding equal quantities to both sides of a story "
            "told in two sentences.",
        )
        + solved(7, "Solve $x+y=9$ and $x-y=3$ by elimination.",
                 ["Add: $2x=12$, $x=6$.",
                  "Then $6+y=9$, $y=3$."],
                 "$(6,3)$", "", "Easy")
        + solved(8, "Solve $2x+3y=5$ and $4x-3y=7$.",
                 ["Add: $6x=12$, $x=2$.",
                  "$4+3y=5$, $3y=1$, $y=\\dfrac{1}{3}$."],
                 "$\\left(2,\\dfrac{1}{3}\\right)$", "", "Medium")
        + solved(9, "Solve $3x+2y=4$ and $5x+3y=7$.",
                 ["Multiply first by $3$ and second by $2$: $9x+6y=12$, $10x+6y=14$.",
                  "Subtract: $x=2$. Then $6+2y=4$, $2y=-2$, $y=-1$.",
                  "Check: $5(2)+3(-1)=7$."],
                 "$(2,-1)$", "", "Hard"),
        ("Multiplying only one side",
         "An equation is a balance. If you triple the left, you must triple the right, including the constant."),
        ("Aim for opposites, not twins, unless you subtract",
         "If both $y$ coefficients become $+6$, subtract. If they become $+6$ and $-6$, add. Decide before you mix."),
        [
            "I can add or subtract to cancel a variable.",
            "I can multiply first to create opposite coefficients.",
            "I can interpret $0=0$ and $0=k$.",
        ],
        11,
    )

    c4 = concept_block(
        "4. No solution and infinitely many",
        [
            "When two linear equations describe the same line, every point on that line is a solution. The equations "
            "are dependent. Algebraically, one is a constant multiple of the other.",
            "When two linear equations describe parallel distinct lines, there is no solution. The equations are "
            "inconsistent. Algebraically, the variable parts match after scaling but the constants do not.",
            "You recognize the cases when $x$ and $y$ both cancel. True leftover ($0=0$): infinite. False leftover "
            "($0=4$): empty. Unique leftover ($x=3$): one solution.",
            "Graphically: coincident lines, parallel lines, or crossing lines. Matching this picture to the algebra "
            "is the whole lesson.",
            "Writing “undefined” or “$x=0$” for these cases is incorrect. The answer is a description of a set: "
            "empty, a single pair, or a line of pairs.",
            "In applications, infinite solutions mean the two constraints were actually the same constraint twice. "
            "No solution means the constraints cannot happen together (an impossible mixture, for example).",
        ],
        "Unit 2 identities and contradictions were the one-variable version of this lesson. Systems just add a "
        "second axis. You will meet the same three cases for linear systems in three variables later.",
        "Scale one equation to match the variable parts of the other. Then compare constants. Same constants: same "
        "line. Different constants: parallel. If you cannot match both variable parts, they cross once.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(1, 2, -3, 3)), ("#dc2626", _seg(1, -1, -2, 4))],
                xlim=(-4, 5), ylim=(-4, 6),
            ),
            "Parallel distinct lines $y=x+2$ and $y=x-1$",
            "Same slope $1$, different intercepts: no intersection, so the system has no solution.",
        )
        + solved(10, "Classify $y=2x+3$ and $2x-y=-3$.",
                 ["Second: $-y=-2x-3$, $y=2x+3$. Same line.",
                  "Infinitely many solutions."],
                 "infinitely many", "", "Easy")
        + solved(11, "Classify $3x+y=4$ and $6x+2y=5$.",
                 ["Twice the first is $6x+2y=8$, not $5$.",
                  "Parallel distinct: no solution."],
                 "no solution", "", "Medium")
        + solved(12, "For which $k$ does $x-y=2$ and $2x-2y=k$ have infinitely many solutions?",
                 ["The second is twice the first precisely when $k=4$.",
                  "If $k\\neq 4$ there is no solution. Never a unique solution, because the left sides are dependent."],
                 "$k=4$", "", "SAT"),
        ("Calling parallel lines “undefined”",
         "Slope of each line may be perfectly defined. What is empty is the solution set of the system, not the slope."),
        ("Compare after matching coefficients",
         "Do not decide from a glance at $C$ in standard form. Scale first, then look at the constants."),
        [
            "I can detect dependent equations.",
            "I can detect inconsistent equations.",
            "I can name the three geometric cases.",
        ],
        16,
    )

    c5 = concept_block(
        "5. Systems of inequalities",
        [
            "A linear inequality $y>mx+b$ describes a half-plane: all points on one side of the boundary line. The "
            "boundary is dashed for $>$ or $<$ and solid for $\\geq$ or $\\leq$.",
            "A system of inequalities is the overlap of the half-planes. The solution is usually a region, not a "
            "single point. Vertices of the region are where boundary lines meet.",
            "Test a point not on the boundary, often $(0,0)$ if it is available. If the inequality is true there, "
            "shade that side; if false, shade the other side.",
            "For $x\\geq 0$, $y\\geq 0$ you are in the first quadrant, including the axes. Many application regions "
            "(tickets, mixtures) live there.",
            "A point on a dashed boundary is not a solution. A point on a solid boundary is a solution of that "
            "inequality, and it is in the system only if it also satisfies the others.",
            "When two strict half-planes do not overlap, the system has no solution — the same idea as inconsistent "
            "equations, but now with regions.",
        ],
        "Linear programming in later courses optimizes a quantity on exactly this kind of feasible region. Algebra 1 "
        "asks you to shade and to test points, which is the geometric core of that topic.",
        "Graph each boundary with the correct dash/solid. Test a point for each inequality. The answer is the "
        "overlap. Label at least one true point in the shaded region.",
        lesson_figure(
            xy_graph(
                curves=[("#4f46e5", _seg(1, 0, -1, 5)), ("#dc2626", [(-1, 4), (5, 4)])],
                points=[(1, 2, "test (1,2)")],
                dashes=[("h", 4, "y=4")],
                xlim=(-2, 6), ylim=(-1, 6),
            ),
            "Boundaries $y=x$ and $y=4$ for a sample system $y\\geq x$ and $y\\leq 4$",
            "The feasible overlap is the wedge above $y=x$ and below the horizontal line $y=4$. The test point $(1,2)$ sits in that wedge.",
        )
        + solved(13, "Does $(0,0)$ satisfy $x+y\\geq 2$?",
                 ["$0+0\\geq 2$ is false, so the origin is not in that half-plane."],
                 "no", "", "Easy")
        + solved(14, "Describe the graph of $y<3$.",
                 ["Horizontal boundary $y=3$, dashed.",
                  "Shade below; $(0,0)$ works because $0<3$."],
                 "dashed $y=3$, shade below", "", "Medium")
        + solved(15, "Find a vertex of $x\\geq 0$, $y\\geq 0$, $x+2y\\leq 6$ other than the origin.",
                 ["Axis intercepts of $x+2y=6$: $(6,0)$ and $(0,3)$.",
                  "Both are vertices of the triangular feasible region, along with $(0,0)$."],
                 "$(6,0)$ or $(0,3)$", "", "Hard"),
        ("Solid versus dashed",
         "If the inequality includes equality, the boundary points count. Drawing the wrong style silently includes "
         "or excludes an entire line of points."),
        ("Test a point off the line",
         "Never test a boundary point to decide which side to shade. Use an interior point such as the origin when "
         "the origin is not on the boundary."),
        [
            "I can shade a half-plane with a test point.",
            "I can use dashed versus solid boundaries.",
            "I can find vertices of a simple feasible region.",
        ],
        21,
    )

    c6 = concept_block(
        "6. Word-problem systems",
        [
            "A word-problem system starts with a dictionary: let $a$ be the number of adult tickets, $c$ the number "
            "of child tickets. Write two equations from two independent facts — often a count and a value.",
            "Mixture problems pair a total-amount equation with a “pure stuff” equation (acid, cocoa, coins). Keep "
            "percents as decimals in the second equation.",
            "Motion problems with current or wind use $r+c$ and $r-c$ for downstream and upstream rates. Distance "
            "equals rate times time still holds on each leg.",
            "Break-even and plan-comparison problems set two linear cost functions equal. The solution $x$ is the "
            "input where the plans cost the same.",
            "After solving, interpret with units and check that both original sentences are true. A negative number "
            "of tickets means a modeling error, not a “valid algebraic extra solution.”",
            "If the story has only one constraint, you have an underdetermined system (a line of answers). If the "
            "story contradicts itself, you will get $0=k$.",
        ],
        "This is the reason systems exist in Algebra 1: two unknown quantities and two independent facts. Later "
        "science courses reuse the same two-equation pattern.",
        "Define variables in words, write the two facts as equations, choose substitution or elimination, then "
        "translate the ordered pair back into the story with units.",
        lesson_figure(
            svg_rect("8a", "5c"),
            "Value equation as an area of money",
            "If adults cost $\\$8$ and children $\\$5$, the total value $8a+5c$ is one equation; $a+c=$ the head-count is the other.",
        )
        + solved(16, "Two numbers sum to $18$ and the larger is $4$ more than the smaller. Find them.",
                 ["$x+y=18$, $x=y+4$.",
                  "$ (y+4)+y=18$, $2y=14$, $y=7$, $x=11$."],
                 "$11$ and $7$", "", "Easy")
        + solved(17, "Tickets: $3$ adult and $2$ child cost $\\$32$; $1$ adult and $4$ child cost $\\$24$. Find each price.",
                 ["From $a+4c=24$, $a=24-4c$.",
                  "Substitute: $3(24-4c)+2c=32$, so $72-12c+2c=32$, $-10c=-40$, $c=4$.",
                  "Then $a=24-16=8$. Check: $3(8)+2(4)=24+8=32$."],
                 "adult $\\$8$, child $\\$4$", "", "Medium")
        + solved(18, "A $20\\%$ acid solution is mixed with a $50\\%$ solution to make $30$ liters of $30\\%$ acid. "
                 "How many liters of each?",
                 ["$x+y=30$, $0.20x+0.50y=9$.",
                  "$0.20x+0.50(30-x)=9$, $0.20x+15-0.50x=9$, $-0.30x=-6$, $x=20$.",
                  "Then $y=10$. Check: $0.20(20)+0.50(10)=4+5=9$, and $9/30=30\\%$."],
                 "$20$ L of $20\\%$ and $10$ L of $50\\%$", "", "SAT"),
        ("Two variables, one sentence",
         "If you only write $a+c=10$, you have a line of answers. Hunt for the second independent fact (usually money, "
         "percent, or time)."),
        ("Units in the dictionary",
         "Write “$a=$ number of adult tickets” not “$a=$ adults.” Mixing a count with a price in one variable is how "
         "systems become nonsense."),
        [
            "I can define two variables from a story.",
            "I can write a count equation and a value equation.",
            "I can interpret the ordered pair with units.",
        ],
        26,
    )

    content = unit_shell(
        title, AUDIENCE, concepts, "".join([c1, c2, c3, c4, c5, c6]),
        practice_slots(31, 25, stretch_label=STRETCH_LABEL),
    )
    return title, description, content, _u4_questions()
