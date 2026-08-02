#!/usr/bin/env python3
"""Inject MathCounts Counting & Combinatorics master + 8 unit courses into Aiven.

- Secrets via env only (AIVEN_PASSWORD / MYSQLPASSWORD, DB_SSL_CA).
- Quiz hydration: insert questions → LAST_INSERT_ID → <!--QUIZ_SLOT_n--> placeholders.
- Idempotent by (title, grade_level).
"""

import io
import json
import math
import os
import random
import re
import ssl
import sys
from collections import Counter

import pymysql

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRADE = 8
MASTER_TITLE = "MathCounts Counting & Combinatorics"
RNG_SEED = 20260802


def getenv_int(name, default):
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


AIVEN_CONFIG = {
    "charset": "utf8mb4",
    "connect_timeout": getenv_int("MYSQL_CONNECT_TIMEOUT", 60),
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("MYSQL_DATABASE") or os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("MYSQLHOST") or os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("MYSQLPASSWORD") or os.getenv("AIVEN_PASSWORD", ""),
    "port": getenv_int("MYSQLPORT", getenv_int("AIVEN_PORT", 26399)),
    "user": os.getenv("MYSQLUSER") or os.getenv("AIVEN_USER", "avnadmin"),
    "read_timeout": getenv_int("MYSQL_READ_TIMEOUT", 180),
    "write_timeout": getenv_int("MYSQL_WRITE_TIMEOUT", 180),
}

_ca_path = None
ssl_ca = os.getenv("DB_SSL_CA")
if ssl_ca:
    _ca_path = os.path.join(os.getcwd(), "ca.pem")
    with open(_ca_path, "w", encoding="utf-8") as f:
        f.write(ssl_ca.replace("\\n", "\n"))
    AIVEN_CONFIG["ssl"] = {"ca": _ca_path}
else:
    _ssl_ctx = ssl.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE
    AIVEN_CONFIG["ssl"] = _ssl_ctx


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def page_break():
    return '<hr class="page-break" />'


def solved(num, problem, steps, answer, note="", level="Easy"):
    badge_colors = {
        "Easy": "#dcfce7",
        "Medium": "#dbeafe",
        "Hard": "#fef3c7",
        "Challenge": "#fce7f3",
    }
    bg = badge_colors.get(level, "#f4f8ff")
    steps_html = "".join(f"<li>{s}</li>" for s in steps)
    note_html = f"<p><em>{note}</em></p>" if note else ""
    return (
        f'<div style="background:#f4f8ff;border:1px solid #c9def4;border-radius:10px;'
        f'padding:16px;margin:14px 0;">'
        f'<p><span style="background:{bg};padding:2px 10px;border-radius:4px;font-weight:bold;">'
        f'{level}</span></p>'
        f"<h4>Solved Example {num}</h4>"
        f"<p><strong>Problem:</strong> {problem}</p>"
        f"<ol>{steps_html}</ol>"
        f'<p><strong>Answer:</strong> <span style="background:#dcfce7;padding:2px 8px;'
        f'border-radius:4px;">{answer}</span></p>{note_html}</div>'
    )


def watch_out(title, body):
    return (
        f'<div style="background:#fffbeb;border:1px solid #fcd34d;border-radius:10px;'
        f'padding:14px;margin:12px 0;">'
        f"<h4>Watch out! {title}</h4><p>{body}</p></div>"
    )


def strategy_tip(text):
    return (
        f'<div style="background:#ecfdf5;border:1px solid #6ee7b7;border-radius:10px;'
        f'padding:14px;margin:12px 0;">'
        f"<h4>Mini strategy tip</h4><p>{text}</p></div>"
    )


def concept(title, body):
    return f"<h3>{title}</h3>{body}"


def before_practice(items):
    lis = "".join(f"<li>{p}</li>" for p in items)
    return f"<h3>Before you practice</h3><ul>{lis}</ul>"


def practice_section():
    slots = "\n".join(quiz_slot(i) for i in range(1, 51))
    return (
        "<h2>Practice Problem Set (50 Problems)</h2>"
        "<p>Try each problem on paper first. Then pick an answer and read the explanation.</p>\n"
        f"{slots}"
    )


def quiz_slot(n):
    return f"<!--QUIZ_SLOT_{n}-->"


def make_question(text, correct, distractors, explanation, idx, points=1):
    opts = [str(correct)] + [str(d) for d in distractors[:3]]
    unique = []
    for opt in opts:
        if opt not in unique:
            unique.append(opt)
    while len(unique) < 4:
        unique.append(str(int(unique[0]) + len(unique) + 1) if unique[0].isdigit() else f"Option {len(unique) + 1}")
    return {
        "question_text": text,
        "question_type": "multiple_choice",
        "options": unique,
        "correct_answer": str(correct),
        "explanation": explanation,
        "points": points,
        "order_index": idx,
    }


def shuffle_options(question, rng):
    q = dict(question)
    options = list(q["options"])
    rng.shuffle(options)
    if q["correct_answer"] not in options:
        options[0] = q["correct_answer"]
        rng.shuffle(options)
    q["options"] = options
    return q


def placeholder_html(question_id, idx):
    return (
        f'<div class="quiz-question-placeholder" data-question-id="{question_id}" '
        f'style="background:#e0e7ff;border:2px solid #667eea;padding:1.5em;margin:1.5em 0;'
        f'border-radius:8px;user-select:none;"><strong>Quiz Question {idx}</strong></div>'
    )


def fill_quiz_slots(content, placeholders):
    """Replace <!--QUIZ_SLOT_n--> with placeholders in order; append leftovers."""
    slots = sorted(int(m) for m in re.findall(r"<!--QUIZ_SLOT_(\d+)-->", content))
    used = 0
    for slot_n in slots:
        if used >= len(placeholders):
            content = content.replace(f"<!--QUIZ_SLOT_{slot_n}-->", "", 1)
            continue
        content = content.replace(f"<!--QUIZ_SLOT_{slot_n}-->", placeholders[used], 1)
        used += 1
    leftover = "".join(placeholders[used:])
    if leftover:
        content += "<h2>End-of-Unit Check</h2>" + leftover
    return content


# ---------------------------------------------------------------------------
# Question-generation helpers (answers computed in Python)
# ---------------------------------------------------------------------------

def near_int(correct, count=3):
    """Plausible integer distractors near a numeric correct answer."""
    c = int(correct)
    pool = []
    for delta in (1, 2, -1, -2, 5, -5, 10, c // 2, c * 2, c + 3, max(1, c - 3)):
        if isinstance(delta, int) and delta > 0 and delta != c:
            pool.append(str(delta))
    unique = []
    for p in pool:
        if p not in unique and p != str(c):
            unique.append(p)
        if len(unique) >= count:
            break
    while len(unique) < count:
        filler = str(c + len(unique) + 7)
        if filler != str(c) and filler not in unique:
            unique.append(filler)
    return unique[:count]


def perm_repeated(word):
    c = Counter(word)
    n = len(word)
    denom = 1
    for v in c.values():
        denom *= math.factorial(v)
    return math.factorial(n) // denom


def stars_bars_nonneg(n, k):
    return math.comb(n + k - 1, k - 1)


def stars_bars_positive(n, k):
    return stars_bars_nonneg(n - k, k)


def pie_divisible(limit, primes):
    """Count integers 1..limit divisible by at least one prime in list."""
    from itertools import combinations
    total = 0
    for r in range(1, len(primes) + 1):
        for combo in combinations(primes, r):
            prod = 1
            for p in combo:
                prod *= p
            term = limit // prod
            total += term if r % 2 == 1 else -term
    return total


def lattice_paths(a, b):
    return math.comb(a + b, a)


def domino_tilings_2xn(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 1, 2
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def no_consecutive_ones(n):
    if n == 0:
        return 1
    a, b = 1, 2
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def catalan(n):
    return math.comb(2 * n, n) // (n + 1)


# ---------------------------------------------------------------------------
# Unit definitions: content + 50 questions each
# ---------------------------------------------------------------------------

def _gen_unit1_questions():
    qs = []
    idx = 1

    for k in (2, 3, 4, 5):
        ans = 10 ** k
        qs.append(make_question(
            f"A PIN has {k} digits from $0$–$9$ with repeats allowed. How many PINs?",
            str(ans), near_int(ans),
            f"Each of {k} slots has $10$ choices. Product rule: $10^{{{k}}}={ans}$.", idx))
        idx += 1

    for k in (2, 3, 4):
        ans = math.perm(10, k)
        qs.append(make_question(
            f"A code uses {k} distinct digits from $0$–$9$ in order. How many codes?",
            str(ans), near_int(ans),
            f"Order matters and digits are distinct: $P(10,{k})={ans}$.", idx))
        idx += 1

    for letters in (2, 3):
        ans = 26 ** letters
        qs.append(make_question(
            f"How many {letters}-letter strings from A–Z if letters may repeat?",
            str(ans), near_int(ans),
            f"$26^{{{letters}}}={ans}$ by the product rule.", idx))
        idx += 1

    for n in (3, 4, 5):
        total = 2 ** n
        bad = 1
        ans = total - bad
        qs.append(make_question(
            f"Bit strings of length ${n}$ that are not all zeros?",
            str(ans), near_int(ans),
            f"Total $2^{{{n}}}={total}$; subtract the all-zero string: ${total}-1={ans}$.", idx))
        idx += 1

    for alphabet in (3, 4):
        total = alphabet ** 3
        bad = (alphabet - 1) ** 3
        ans = total - bad
        qs.append(make_question(
            f"Strings of length $3$ from a {alphabet}-letter alphabet with at least one of the first letter?",
            str(ans), near_int(ans),
            f"Total ${alphabet}^3={total}$; none of that letter: ${alphabet-1}^3={bad}$; complement ${total}-{bad}={ans}$.", idx))
        idx += 1

    qs.append(make_question(
        "A meal: pick 1 of 4 soups, 1 of 5 mains, 1 of 3 desserts. How many meals?",
        "60", ["12", "15", "45"],
        "Independent choices multiply: $4\\times5\\times3=60$.", idx)); idx += 1

    qs.append(make_question(
        "How many two-digit numbers have both digits even?",
        "20", ["25", "45", "10"],
        "Tens digit from $\\{2,4,6,8\\}$ ($4$ choices); units from $\\{0,2,4,6,8\\}$ ($5$): $4\\times5=20$.", idx)); idx += 1

    qs.append(make_question(
        "How many two-digit numbers have both digits odd?",
        "25", ["20", "45", "5"],
        "Tens from $\\{1,3,5,7,9\\}$ ($5$); units from $\\{1,3,5,7,9\\}$ ($5$): $5\\times5=25$.", idx)); idx += 1

    qs.append(make_question(
        "Two-digit numbers with either both digits even OR both digits odd?",
        "45", ["20", "25", "90"],
        "Disjoint cases: $20+25=45$ (sum rule).", idx)); idx += 1

    qs.append(make_question(
        "Ordered outcomes when a fair die is rolled twice?",
        "36", ["12", "21", "6"],
        "Two independent stages with $6$ choices each: $6\\times6=36$.", idx)); idx += 1

    qs.append(make_question(
        "Ordered die pairs with sum $7$?",
        "6", ["5", "7", "12"],
        "List: $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$ — six ordered pairs.", idx)); idx += 1

    qs.append(make_question(
        "Ordered die pairs with sum at least $10$?",
        "6", ["30", "3", "10"],
        "Sum $10$: $3$ pairs; sum $11$: $2$; sum $12$: $1$; total $6$.", idx)); idx += 1

    qs.append(make_question(
        "How many 3-digit numbers (no leading zero) have all distinct digits?",
        "648", ["900", "720", "504"],
        "Hundreds: $9$; tens: $9$; units: $8$ → $9\\times9\\times8=648$.", idx)); idx += 1

    qs.append(make_question(
        "License plate: 2 letters then 3 digits, all independent with repeats OK. Count?",
        "676000", ["650000", "67600", "260000"],
        "$26\\times26\\times10\\times10\\times10=676000$.", idx)); idx += 1

    qs.append(make_question(
        "Complementary counting is especially helpful when the problem says:",
        "at least one / not all",
        ["only circular arrangements", "only lattice paths", "only binomial rows"],
        "Phrases like “at least one” often mean: total minus “none.”", idx)); idx += 1

    qs.append(make_question(
        "The product rule applies when choices in different stages are:",
        "independent",
        ["always identical", "always overlapping", "never ordered"],
        "Each stage’s count must not depend on earlier picks (unless you adjust the count on purpose).", idx)); idx += 1

    qs.append(make_question(
        "The sum rule applies when your cases are:",
        "disjoint (no overlap)",
        ["always the same size", "always overlapping", "never complete"],
        "If cases overlap, add carefully or switch to inclusion-exclusion.", idx)); idx += 1

    while len(qs) < 50:
        n = len(qs) + 1
        ans = 9 * 10 ** (n % 3)
        qs.append(make_question(
            f"How many {2 + n % 3}-digit numbers if the first digit is 1–9 and others are 0–9?",
            str(ans), near_int(ans),
            f"First digit $9$ choices; each other digit $10$: computed as ${ans}$.", len(qs) + 1))

    return qs[:50]


def unit_counting_principles():
    title = "MathCounts Unit 1: Counting Principles"
    description = (
        "Product rule, sum rule, and complementary counting for MathCounts and AMC 8."
    )
    content = f"""
<h1>{title}</h1>
<p><strong>Who this is for:</strong> 6th–8th graders preparing for MathCounts and AMC 8.</p>
<p>Almost every counting problem on a contest comes down to three ideas: multiply when stages are independent,
add when cases do not overlap, and subtract when “at least one” is easier than listing everything.</p>

{concept("The product rule (multiply)", '''
<p><strong>In plain English:</strong> If you make several choices one after another, and each choice does not
change how many options you have in the other stages, multiply the counts.</p>
$$N = n_1 \\cdot n_2 \\cdots n_k$$
<p>Example: outfit with $3$ shirts and $4$ pants → $3\\times4=12$ outfits.</p>
''')}

{solved(1,
    "A bike lock uses 3 digits from $0$–$9$ and digits may repeat. How many locks?",
    [
        "Think of three slots: hundreds, tens, units (leading zeros are allowed on a lock).",
        "Each slot has $10$ choices.",
        "Multiply: $10\\times10\\times10=1000$.",
    ],
    "$1000$",
    "When repeats are allowed, every slot usually keeps the full $10$ choices.",
    "Easy",
)}

{solved(2,
    "Lunch: $4$ sandwiches, $3$ drinks, $2$ cookies. You pick one of each. How many lunches?",
    [
        "Sandwich: $4$ ways.",
        "Drink: $3$ ways (independent of sandwich).",
        "Cookie: $2$ ways.",
        "Product rule: $4\\times3\\times2=24$ lunches.",
    ],
    "$24$",
    "",
    "Easy",
)}

{page_break()}

{concept("The sum rule (add disjoint cases)", '''
<p><strong>In plain English:</strong> Split the problem into cases that cover everything and do not overlap.
Add the case counts.</p>
$$|A\\cup B| = |A|+|B| \\quad\\text{(when }A\\cap B=\\emptyset\\text{)}$$
''')}

{solved(3,
    "How many two-digit numbers have both digits even OR both digits odd?",
    [
        "<strong>Case 1 — both even:</strong> tens from $\\{2,4,6,8\\}$ ($4$); units from $\\{0,2,4,6,8\\}$ ($5$). Count $4\\times5=20$.",
        "<strong>Case 2 — both odd:</strong> tens from $\\{1,3,5,7,9\\}$ ($5$); units from $\\{1,3,5,7,9\\}$ ($5$). Count $5\\times5=25$.",
        "A number cannot be both all-even and all-odd, so add: $20+25=45$.",
    ],
    "$45$",
    "",
    "Medium",
)}

{solved(4,
    "A 3-digit PIN uses digits $0$–$9$ with no repeated digit. How many PINs?",
    [
        "Slot 1: $10$ choices.",
        "Slot 2: $9$ remaining digits.",
        "Slot 3: $8$ remaining digits.",
        "$10\\times9\\times8=720$.",
    ],
    "$720$",
    "This is still the product rule, but later counts shrink because digits must differ.",
    "Medium",
)}

{watch_out("Leading zeros",
    "A <em>3-digit number</em> cannot start with $0$, but a <em>3-digit lock code</em> often can. "
    "Read whether the first slot is restricted before you multiply.")}

{page_break()}

{concept("Complementary counting (total minus bad)", '''
<p><strong>In plain English:</strong> Count everything allowed, then subtract what you do <em>not</em> want.</p>
$$|\\text{good}| = |\\text{total}| - |\\text{bad}|$$
<p>Look for words like “at least one,” “not all,” or “not every.”</p>
''')}

{solved(5,
    "How many 3-letter strings from $\\{A,B,C,D\\}$ (repeats OK) contain at least one $A$?",
    [
        "Total strings: $4^3=64$.",
        "Bad strings (no $A$): use only $\\{B,C,D\\}$ → $3^3=27$.",
        "Good strings: $64-27=37$.",
    ],
    "$37$",
    "Listing “exactly one $A$,” “exactly two $A$’s,” etc. also works but takes longer.",
    "Medium",
)}

{solved(6,
    "How many 3-digit numbers contain at least one digit $7$?",
    [
        "Total 3-digit numbers: $900$ (from $100$ to $999$).",
        "Bad numbers (no $7$): each digit chosen from $\\{0,1,2,3,4,5,6,8,9\\}$ — $9$ choices per digit, but hundreds digit cannot be $0$.",
        "Hundreds: $8$ choices (1–9 except 7); tens and units: $9$ each → $8\\times9\\times9=648$.",
        "At least one $7$: $900-648=252$.",
    ],
    "$252$",
    "",
    "Hard",
)}

{solved(7,
    "A fair die is rolled twice (order matters). How many outcomes have a sum of at least $10$?",
    [
        "Total ordered outcomes: $6\\times6=36$.",
        "List sums $\\ge10$: sum $10$ → $(4,6),(5,5),(6,4)$ ($3$); sum $11$ → $(5,6),(6,5)$ ($2$); sum $12$ → $(6,6)$ ($1$).",
        "Total favorable: $3+2+1=6$.",
    ],
    "$6$",
    "You could also count sums $\\le9$ and subtract from $36$, but the favorable list is small here.",
    "Hard",
)}

{watch_out("Multiplying when cases overlap",
    "Do not multiply counts from overlapping descriptions. If two “stages” share information, "
    "either redefine disjoint cases or use inclusion-exclusion later.")}

{strategy_tip(
    "Before multiplying, ask: <em>Does this choice change how many options I have next?</em> "
    "If yes, adjust the next count (like $10\\to9\\to8$ for distinct digits)."
)}

{page_break()}

{solved(8,
    "How many positive integers less than $1000$ have digit sum exactly $9$?",
    [
        "Use casework by number of digits.",
        "<strong>1-digit:</strong> only $9$ → $1$ number.",
        "<strong>2-digit $10a+b$:</strong> need $a+b=9$ with $a\\ge1$. Pairs $(1,8),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),(8,1),(9,0)$ → $9$ numbers.",
        "<strong>3-digit $100a+10b+c$:</strong> $a+b+c=9$, $a\\ge1$. Let $a'=a-1\\ge0$. Then $a'+b+c=8$. Stars and bars: $\\binom{8+3-1}{3-1}=\\binom{10}{2}=45$.",
        "Total: $1+9+45=55$.",
    ],
    "$55$",
    "This preview connects to Unit 5 (stars and bars).",
    "Challenge",
)}

{before_practice([
    "Can I fill independent slots and multiply?",
    "Should I split into disjoint cases and add?",
    "Does “at least one” suggest complement (total minus none)?",
    "Did I treat numbers vs. codes differently for leading zeros?",
])}

{practice_section()}
"""
    return title, description, content, _gen_unit1_questions()


def _gen_unit2_questions():
    qs = []
    idx = 1

    for n in (4, 5, 6, 7):
        ans = math.factorial(n)
        qs.append(make_question(
            f"How many ways to arrange {n} distinct books in a row?",
            str(ans), near_int(ans),
            f"${n}!={ans}$.", idx)); idx += 1

    for n, k in ((8, 3), (10, 3), (12, 2), (9, 4), (7, 2)):
        ans = math.perm(n, k)
        qs.append(make_question(
            f"Compute $P({n},{k})$.",
            str(ans), near_int(ans),
            f"$P({n},{k})={n}\\times\\cdots\\times({n}-{k}+1)={ans}$.", idx)); idx += 1

    for word in ("MATH", "CODE", "LEVEL", "BANANA", "MISSISSIPPI"):
        ans = perm_repeated(word)
        qs.append(make_question(
            f"Distinct arrangements of the letters in {word}?",
            str(ans), near_int(ans),
            f"Divide by repeated letter factorials: ${ans}$.", idx)); idx += 1

    for n in (5, 6, 8):
        ans = math.factorial(n - 1)
        qs.append(make_question(
            f"Distinct people seated around a round table ({n} people, rotations equivalent)?",
            str(ans), near_int(ans),
            f"Circular arrangements: $({n}-1)!={ans}$.", idx)); idx += 1

    qs.append(make_question(
        "Gold, silver, bronze medals among $9$ runners (distinct people)?",
        "504", ["84", "729", "36"],
        "Three different medals → order matters: $P(9,3)=9\\times8\\times7=504$.", idx)); idx += 1

    qs.append(make_question(
        "Injective functions from a $3$-element set to a $7$-element set?",
        "210", ["35", "343", "21"],
        "Pick images in order without repetition: $P(7,3)=210$.", idx)); idx += 1

    qs.append(make_question(
        "4-digit PINs from digits $0$–$9$ with no repeated digit?",
        "5040", ["10000", "9000", "720"],
        "$P(10,4)=10\\times9\\times8\\times7=5040$.", idx)); idx += 1

    qs.append(make_question(
        "Use $P(n,k)$ instead of $C(n,k)$ when:",
        "order or distinct roles matter",
        ["order never matters", "objects are identical", "only complements are needed"],
        "Permutations count ordered selections.", idx)); idx += 1

    qs.append(make_question(
        "Arrangements of AABBC (all letters used)?",
        "30", ["120", "60", "12"],
        "$\\frac{{5!}}{{2!2!1!}}=30$.", idx)); idx += 1

    while len(qs) < 50:
        n = 5 + len(qs) % 4
        k = 2 + len(qs) % 3
        ans = math.perm(n, k)
        qs.append(make_question(
            f"$P({n},{k})$ equals?",
            str(ans), near_int(ans),
            f"Computed: $P({n},{k})={ans}$.", len(qs) + 1))

    return qs[:50]


def unit_permutations():
    title = "MathCounts Unit 2: Permutations & Arrangements"
    description = "Factorials, ordered selections, repeated letters, and circular seating."
    content = f"""
<h1>{title}</h1>
<p><strong>Why this matters:</strong> MathCounts loves questions where order matters — medals, passwords with
different slots, or lining up people.</p>
<p>A <strong>permutation</strong> means an <em>ordered</em> arrangement. If swapping two people creates a new
outcome, you are in permutation territory.</p>

{concept("Factorials and $P(n,k)$", '''
<p>$n! = 1\\cdot2\\cdots n$ counts arrangements of $n$ distinct objects.</p>
<p>To choose and order $k$ of $n$ distinct objects:</p>
$$P(n,k)=\\frac{{n!}}{{(n-k)!}}=n(n-1)\\cdots(n-k+1)$$
''')}

{solved(1,
    "How many ways can the letters in MATH be arranged?",
    [
        "All four letters are different.",
        "Arrange $4$ distinct objects: $4!=24$.",
    ],
    "$24$",
    "",
    "Easy",
)}

{solved(2,
    "From $10$ students, choose a president, vice-president, and treasurer (all different jobs). How many ways?",
    [
        "Jobs are distinct, so order matters.",
        "President: $10$ choices; VP: $9$; treasurer: $8$.",
        "$P(10,3)=10\\times9\\times8=720$.",
    ],
    "$720$",
    "Choosing a committee of $3$ would be $\\binom{{10}}{{3}}=120$ — different problem.",
    "Easy",
)}

{page_break()}

{concept("Repeated letters", '''
<p>When some letters match, divide by factorials of the repeat counts:</p>
$$\\frac{{n!}}{{r_1!\\,r_2!\\cdots}}$$
''')}

{solved(3,
    "Distinct arrangements of the letters in BALLOON?",
    [
        "Seven letters with two L's and two O's.",
        "$\\dfrac{{7!}}{{2!\\,2!}}=\\dfrac{{5040}}{{4}}=1260$.",
    ],
    "$1260$",
    "",
    "Medium",
)}

{solved(4,
    "Distinct arrangements of MISSISSIPPI?",
    [
        "Eleven letters: M×1, I×4, S×4, P×2.",
        "$\\dfrac{{11!}}{{4!\\,4!\\,2!}}=34650$.",
    ],
    "$34650$",
    "",
    "Medium",
)}

{solved(5,
    "How many 4-digit PINs use digits $0$–$9$ with all digits different?",
    [
        "Four ordered slots, no repeats.",
        "$P(10,4)=10\\times9\\times8\\times7=5040$.",
    ],
    "$5040$",
    "",
    "Medium",
)}

{watch_out("Using $n!$ when letters repeat",
    "BOOK is $4!$, but BOBO is $\\frac{{4!}}{{2!}}$ because the two O's match. "
    "Identical objects cannot be told apart by swapping.")}

{page_break()}

{concept("Circular arrangements", '''
<p>When rotations of a circle look the same, fix one person’s seat and arrange the rest:</p>
$$(n-1)! \\quad\\text{for }n\\text{ distinct people}$$
<p>Only divide by $2$ for reflections (necklace style) if the problem says so.</p>
''')}

{solved(6,
    "Five distinct friends sit around a round table (rotations equivalent). How many seatings?",
    [
        "Fix one person to break rotation symmetry.",
        "Arrange the other $4$: $4!=24$.",
    ],
    "$24$",
    "",
    "Hard",
)}

{solved(7,
    "Injective functions from $\\{1,2,3\\}$ to $\\{1,2,\\ldots,7\\}$?",
    [
        "Each input needs a different output; order of outputs matters by label.",
        "Choose values in order: $P(7,3)=7\\times6\\times5=210$.",
    ],
    "$210$",
    "",
    "Hard",
)}

{solved(8,
    "Arrange the multiset $\\{A,A,B,B,C\\}$ (all five letters used). How many distinct strings?",
    [
        "Five positions with two A's and two B's repeated.",
        "$\\dfrac{{5!}}{{2!\\,2!}}=\\dfrac{{120}}{{4}}=30$.",
    ],
    "$30$",
    "",
    "Challenge",
)}

{strategy_tip(
    "Ask: <em>If I swap two chosen objects, is that a new outcome?</em> Yes → permutation. "
    "No → combination (Unit 3)."
)}

{watch_out("Combinations for distinct roles",
    "Do not use $\\binom{{n}}{{2}}$ for president and secretary. Those jobs are different — use $P(n,2)$.")}

{before_practice([
    "Does order matter or do roles differ?",
    "Are any letters or objects identical (divide by factorials)?",
    "Is the table circular (use $(n-1)!$)?",
    "For PINs: are repeats allowed?",
])}

{practice_section()}
"""
    return title, description, content, _gen_unit2_questions()


def _gen_unit3_questions():
    qs = []
    idx = 1

    for n, k in ((9, 2), (10, 3), (10, 4), (12, 5), (8, 3), (11, 2), (7, 4)):
        ans = math.comb(n, k)
        qs.append(make_question(
            f"Compute $\\binom{{{n}}}{{{k}}}$.",
            str(ans), near_int(ans),
            f"$\\binom{{{n}}}{{{k}}}={ans}$.", idx)); idx += 1

    for n in (5, 6, 7, 8, 10):
        ans = 2 ** n
        qs.append(make_question(
            f"How many subsets of an {n}-element set?",
            str(ans), near_int(ans),
            f"Each element in or out: $2^{{{n}}}={ans}$.", idx)); idx += 1

    for n, k in ((7, 3), (8, 2), (9, 4)):
        ans = math.comb(n, k)
        qs.append(make_question(
            f"Coefficient of $x^{{{k}}}$ in $(1+x)^{{{n}}}$?",
            str(ans), near_int(ans),
            f"Binomial coefficient $\\binom{{{n}}}{{{k}}}={ans}$.", idx)); idx += 1

    qs.append(make_question(
        "Choose a committee of $3$ from $10$ people (unordered)?",
        "120", ["720", "1000", "30"],
        "$\\binom{{10}}{{3}}=120$.", idx)); idx += 1

    qs.append(make_question(
        "Committee of $2$ girls from $6$ and $2$ boys from $5$?",
        "150", ["30", "300", "11"],
        "$\\binom{{6}}{{2}}\\binom{{5}}{{2}}=15\\times10=150$.", idx)); idx += 1

    qs.append(make_question(
        "$\\binom{{6}}{{2}}+\\binom{{6}}{{3}}$ equals $\\binom{{7}}{{3}}$ because:",
        "Pascal's identity",
        ["order matters", "stars and bars", "PIE always"],
        "$\\binom{{n}}{{k}}=\\binom{{n-1}}{{k}}+\\binom{{n-1}}{{k-1}}$.", idx)); idx += 1

    qs.append(make_question(
        "$\\binom{{n}}{{k}}=\\binom{{n}}{{n-k}}$ means:",
        "choosing k to keep equals choosing n-k to leave out",
        ["order matters", "k must be 0", "only for even n"],
        "Complementary selection within a set.", idx)); idx += 1

    qs.append(make_question(
        "Choose $4$ from $10$, then elect a chair from those $4$?",
        "840", ["210", "5040", "120"],
        "$\\binom{{10}}{{4}}\\times4=210\\times4=840$.", idx)); idx += 1

    qs.append(make_question(
        "5-card hands from a 52-card deck?",
        "2598960", ["259896", "311875200", "52"],
        "$\\binom{{52}}{{5}}=2598960$.", idx)); idx += 1

    qs.append(make_question(
        "Use $\\binom{{n}}{{k}}$ instead of $P(n,k)$ when:",
        "the selection is unordered",
        ["roles are labeled", "letters repeat", "paths on a grid"],
        "Teams and committees usually ignore order.", idx)); idx += 1

    while len(qs) < 50:
        n = 6 + len(qs) % 5
        k = 1 + len(qs) % 3
        ans = math.comb(n, k)
        qs.append(make_question(
            f"$\\binom{{{n}}}{{{k}}}$ equals?",
            str(ans), near_int(ans),
            f"Computed $\\binom{{{n}}}{{{k}}}={ans}$.", len(qs) + 1))

    return qs[:50]


def unit_combinations():
    title = "MathCounts Unit 3: Combinations & Binomials"
    description = "Unordered selections, binomial coefficients, and Pascal's triangle."
    content = f"""
<h1>{title}</h1>
<p>A <strong>combination</strong> is a way to choose a group where order does <em>not</em> matter.
Picking Alice then Bob is the same committee as Bob then Alice.</p>

{concept("The combination formula", '''
$$\\binom{{n}}{{k}}=C(n,k)=\\frac{{n!}}{{k!(n-k)!}}=\\frac{{P(n,k)}}{{k!}}$$
<p>Every unordered $k$-set corresponds to $k!$ different orderings, so divide.</p>
''')}

{solved(1,
    "How many ways to choose $3$ books from $10$ (order irrelevant)?",
    [
        "Unordered selection of $3$ from $10$.",
        "$\\binom{{10}}{{3}}=\\dfrac{{10\\times9\\times8}}{{3\\times2\\times1}}=120$.",
    ],
    "$120$",
    "",
    "Easy",
)}

{solved(2,
    "Expand $(x+y)^4$. What is the coefficient of $x^2y^2$?",
    [
        "In $(x+y)^4$, the $x^2y^2$ term comes from choosing $y$ twice in four factors.",
        "Coefficient $=\\binom{{4}}{{2}}=6$.",
    ],
    "$6$",
    "",
    "Easy",
)}

{page_break()}

{solved(3,
    "Committee of $4$ with exactly $2$ girls from $6$ girls and $2$ boys from $5$ boys?",
    [
        "Choose girls: $\\binom{{6}}{{2}}=15$.",
        "Choose boys: $\\binom{{5}}{{2}}=10$.",
        "Independent choices multiply: $15\\times10=150$.",
    ],
    "$150$",
    "",
    "Medium",
)}

{solved(4,
    "How many subsets does a $5$-element set have?",
    [
        "Each element is either in or out: $2$ choices per element.",
        "$2^5=32$ subsets (including the empty set).",
    ],
    "$32$",
    "",
    "Medium",
)}

{concept("Pascal's identity", '''
$$\\binom{{n}}{{k}}=\\binom{{n-1}}{{k}}+\\binom{{n-1}}{{k-1}}$$
<p>Fix one special element: either it is chosen or it is not.</p>
''')}

{solved(5,
    "Compute $\\binom{{8}}{{3}}$ using $\\binom{{7}}{{2}}$ and $\\binom{{7}}{{3}}$.",
    [
        "$\\binom{{7}}{{2}}=21$, $\\binom{{7}}{{3}}=35$.",
        "Pascal: $\\binom{{8}}{{3}}=21+35=56$.",
    ],
    "$56$",
    "",
    "Medium",
)}

{watch_out("Forgetting to divide by $k!$",
    "If the problem says “choose a team,” do not leave the answer as $P(n,k)$. "
    "Divide by $k!$ unless roles differ.")}

{page_break()}

{solved(6,
    "How many $5$-card poker hands from a $52$-card deck?",
    [
        "Order of cards in a hand does not matter.",
        "$\\binom{{52}}{{5}}=2598960$.",
    ],
    "$2598960$",
    "",
    "Hard",
)}

{solved(7,
    "Choose a committee of $4$ from $10$, then elect a chair from the committee?",
    [
        "Choose members: $\\binom{{10}}{{4}}=210$.",
        "Elect chair from those $4$: $4$ ways.",
        "$210\\times4=840$.",
    ],
    "$840$",
    "",
    "Hard",
)}

{solved(8,
    "How many ways to choose $0$ objects from $20$?",
    [
        "The empty selection is allowed.",
        "$\\binom{{20}}{{0}}=1$.",
    ],
    "$1$",
    "This matches the one way to choose nothing.",
    "Challenge",
)}

{strategy_tip(
    "Before computing, say out loud: <em>Does order matter?</em> No → combination. "
    "Yes → permutation from Unit 2."
)}

{before_practice([
    "Is the group unordered (team/committee/hand)?",
    "Did I divide by $k!$ after $P(n,k)$ if needed?",
    "For binomial coefficients: which power of $y$ am I choosing?",
    "Does the problem have two independent choices to multiply?",
])}

{practice_section()}
"""
    return title, description, content, _gen_unit3_questions()


def _gen_unit4_questions():
    qs = []
    idx = 1

    for n in (5, 6, 7, 8):
        ans = n * (n - 3) // 2
        qs.append(make_question(
            f"Diagonals in a convex {n}-gon?",
            str(ans), near_int(ans),
            f"$\\binom{{{n}}}{{2}}-{n}=\\frac{{{n}({n}-3)}}{{2}}={ans}$.", idx)); idx += 1

    for a, b in ((3, 2), (4, 3), (5, 2), (6, 1), (5, 5)):
        ans = lattice_paths(a, b)
        qs.append(make_question(
            f"Lattice paths from $(0,0)$ to $({a},{b})$ using only right and up steps?",
            str(ans), near_int(ans),
            f"$\\binom{{{a+b}}}{{{a}}}={ans}$.", idx)); idx += 1

    qs.append(make_question(
        "Split $6$ people into two unlabeled teams of $3$?",
        "10", ["20", "40", "6"],
        "Labeled rooms: $\\binom{{6}}{{3}}=20$; unlabeled divide by $2$ → $10$.", idx)); idx += 1

    qs.append(make_question(
        "Split $6$ people into Red team and Blue team of $3$ each (rooms labeled)?",
        "20", ["10", "40", "6"],
        "Choose Red’s $3$: $\\binom{{6}}{{3}}=20$; Blue gets the rest.", idx)); idx += 1

    qs.append(make_question(
        "Two-digit numbers with distinct digits?",
        "81", ["90", "72", "80"],
        "Tens: $9$ choices (1–9); units: $9$ (0–9 except used tens digit): $9\\times9=81$.", idx)); idx += 1

    qs.append(make_question(
        "3-digit numbers with exactly two digits equal (not all three equal)?",
        "243", ["648", "900", "234"],
        "Total $900$ minus all distinct $648$ minus all same $9$ → $900-648-9=243$.", idx)); idx += 1

    qs.append(make_question(
        "Seat $3$ distinct people in $5$ labeled chairs (no empty chair restriction beyond 3 filled)?",
        "60", ["10", "125", "120"],
        "Injective assignment: $P(5,3)=60$.", idx)); idx += 1

    qs.append(make_question(
        "Integers $1$–$20$ divisible by $2$ or $3$?",
        "13", ["10", "6", "8"],
        "Div by 2: $10$; by 3: $6$; by 6: $3$; union $10+6-3=13$.", idx)); idx += 1

    qs.append(make_question(
        "Positive integers $<50$ with digit sum $9$?",
        "5", ["9", "4", "6"],
        "Numbers: $9,18,27,36,45$ → five numbers.", idx)); idx += 1

    qs.append(make_question(
        "Casework works best when cases are:",
        "disjoint and cover all possibilities",
        ["always overlapping", "never complete", "only size 1"],
        "Good cases partition the problem.", idx)); idx += 1

    qs.append(make_question(
        "If each valid object was counted exactly twice, fix overcount by:",
        "dividing by 2",
        ["multiplying by 2", "adding 2", "using n! always"],
        "Uniform double-count → divide.", idx)); idx += 1

    while len(qs) < 50:
        n = 4 + len(qs) % 4
        ans = math.comb(n, 2)
        qs.append(make_question(
            f"Segments joining {n} labeled points (no three collinear)?",
            str(ans), near_int(ans),
            f"$\\binom{{{n}}}{{2}}={ans}$.", len(qs) + 1))

    return qs[:50]


def unit_casework():
    title = "MathCounts Unit 4: Casework & Overcounting"
    description = "Split into clean cases, avoid double-counting, and repair symmetry."
    content = f"""
<h1>{title}</h1>
<p>When a problem has several “types” of outcomes, <strong>casework</strong> means listing neat cases,
counting each case, then adding — but only if cases do not overlap.</p>

{concept("Designing good cases", '''
<ul>
<li><strong>Exhaustive:</strong> every outcome fits some case.</li>
<li><strong>Disjoint:</strong> no outcome fits two cases.</li>
<li>Common splits: by size, by whether a special item is included, by parity, by first digit.</li>
</ul>
''')}

{solved(1,
    "How many positive integers less than $50$ have digit sum $9$?",
    [
        "List systematically: $9$ (1-digit).",
        "2-digit: $18,27,36,45$ — tens digit at most $4$ because $<50$.",
        "That is $1+4=5$ numbers total.",
    ],
    "$5$",
    "",
    "Easy",
)}

{solved(2,
    "How many two-digit numbers have distinct digits?",
    [
        "Tens digit: $9$ choices ($1$–$9$).",
        "Units digit: $9$ choices ($0$–$9$ except the tens digit).",
        "$9\\times9=81$.",
    ],
    "$81$",
    "",
    "Easy",
)}

{page_break()}

{solved(3,
    "Seat $4$ people in $6$ labeled chairs in a row (exactly 4 chairs used)?",
    [
        "Choose which $4$ chairs: $\\binom{{6}}{{4}}=15$.",
        "Arrange $4$ people in those chairs: $4!=24$.",
        "Multiply: $15\\times24=360$ (same as $P(6,4)$).",
    ],
    "$360$",
    "",
    "Medium",
)}

{solved(4,
    "How many 3-digit numbers have exactly two digits the same (and the third different)?",
    [
        "Total 3-digit numbers: $900$.",
        "All digits distinct: $9\\times9\\times8=648$.",
        "All three digits the same: $111,222,\\ldots,999$ → $9$.",
        "Exactly two equal: $900-648-9=243$.",
    ],
    "$243$",
    "",
    "Medium",
)}

{watch_out("Dividing by 2 too quickly",
    "Only divide when every unordered pair was counted exactly twice. "
    "Labeled teams do not get divided.")}

{page_break()}

{concept("Overcounting repair", '''
<p>If every valid object was counted $m$ times the same way, divide by $m$.</p>
<p>Example: splitting into two unlabeled teams of $3$ from $6$ people: $\\binom{{6}}{{3}}/2=10$.</p>
''')}

{solved(5,
    "Split $6$ people into two unlabeled teams of $3$?",
    [
        "If teams were labeled Red/Blue: $\\binom{{6}}{{3}}=20$.",
        "Teams are identical → each split counted twice → $20/2=10$.",
    ],
    "$10$",
    "",
    "Hard",
)}

{solved(6,
    "Paths from $(0,0)$ to $(2,2)$ that pass through $(1,1)$?",
    [
        "$(0,0)\\to(1,1)$: $\\binom{{2}}{{1}}=2$ paths.",
        "$(1,1)\\to(2,2)$: $\\binom{{2}}{{1}}=2$ paths.",
        "Multiply independent segments: $2\\times2=4$.",
    ],
    "$4$",
    "",
    "Hard",
)}

{solved(7,
    "Diagonals in a convex octagon?",
    [
        "Every pair of vertices gives a segment: $\\binom{{8}}{{2}}=28$.",
        "Subtract the $8$ sides: $28-8=20$ diagonals.",
    ],
    "$20$",
    "",
    "Hard",
)}

{solved(8,
    "Integers from $1$ to $100$ with digit sum divisible by $3$?",
    [
        "Among $1$–$99$, digit sums mod $3$ are balanced: exactly $33$ each residue.",
        "$100$ has digit sum $1$, not divisible by $3$.",
        "Answer: $33$.",
    ],
    "$33$",
    "",
    "Challenge",
)}

{strategy_tip(
    "Write your case labels first. If two cases share an outcome, merge them before adding."
)}

{before_practice([
    "Are my cases disjoint and complete?",
    "Did I multiply independent stages within a case?",
    "Should I subtract from a total instead of listing many cases?",
    "If teams are unlabeled, do I need to divide?",
])}

{practice_section()}
"""
    return title, description, content, _gen_unit4_questions()


def _gen_unit5_questions():
    qs = []
    idx = 1

    for n, k in ((5, 3), (4, 3), (6, 4), (7, 3), (8, 5), (10, 4)):
        ans = stars_bars_nonneg(n, k)
        qs.append(make_question(
            f"Non-negative integer solutions to $x_1+\\cdots+x_{k}={n}$?",
            str(ans), near_int(ans),
            f"Stars and bars: $\\binom{{{n+k-1}}}{{{k-1}}}={ans}$.", idx)); idx += 1

    for n, k in ((6, 3), (8, 4), (10, 3), (7, 5), (9, 4)):
        ans = stars_bars_positive(n, k)
        qs.append(make_question(
            f"Positive integer solutions to $x_1+\\cdots+x_{k}={n}$?",
            str(ans), near_int(ans),
            f"Subtract $1$ from each variable: $\\binom{{{n-k+k-1}}}{{{k-1}}}={ans}$.", idx)); idx += 1

    qs.append(make_question(
        "Non-negative solutions to $x+y=7$?",
        "8", ["7", "6", "9"],
        "Values $0$ through $7$ for $x$ → $8$ pairs.", idx)); idx += 1

    qs.append(make_question(
        "Non-negative solutions to $x+y+z=4$?",
        "15", ["12", "64", "10"],
        "$\\binom{{6}}{{2}}=15$.", idx)); idx += 1

    qs.append(make_question(
        "Positive solutions to $x+y+z=6$?",
        "10", ["28", "15", "20"],
        "$\\binom{{5}}{{2}}=10$.", idx)); idx += 1

    qs.append(make_question(
        "Distribute $7$ identical stickers to $3$ distinct kids (each may get zero)?",
        "36", ["21", "2187", "28"],
        "$\\binom{{7+3-1}}{{3-1}}=\\binom{{9}}{{2}}=36$.", idx)); idx += 1

    qs.append(make_question(
        "Non-negative solutions to $x+y+z=10$ with $x\\le4$?",
        "45", ["66", "21", "51"],
        "Total $\\binom{{12}}{{2}}=66$; bad $x\\ge5$ gives $\\binom{{7}}{{2}}=21$; $66-21=45$.", idx)); idx += 1

    qs.append(make_question(
        "Positive solutions to $w+x+y+z=8$?",
        "35", ["70", "56", "20"],
        "$\\binom{{7}}{{3}}=35$.", idx)); idx += 1

    qs.append(make_question(
        "Stars and bars applies when objects are:",
        "identical and bins are distinct",
        ["all distinct and ordered", "always circular", "never integers"],
        "Classic: identical items into labeled boxes.", idx)); idx += 1

    qs.append(make_question(
        "If each $x_i\\ge2$ in $x+y+z=9$, substitute $x_i'=x_i-2$ to get sum:",
        "3", ["9", "6", "1"],
        "Minimum $2$ each uses $6$; remaining sum $3$.", idx)); idx += 1

    while len(qs) < 50:
        n = 3 + len(qs) % 6
        k = 2 + len(qs) % 4
        ans = stars_bars_nonneg(n, k)
        qs.append(make_question(
            f"Non-negative solutions to {k} variables summing to {n}?",
            str(ans), near_int(ans),
            f"$\\binom{{{n+k-1}}}{{{k-1}}}={ans}$.", len(qs) + 1))

    return qs[:50]


def unit_stars_bars():
    title = "MathCounts Unit 5: Stars and Bars"
    description = "Count integer solutions and identical-item distributions."
    content = f"""
<h1>{title}</h1>
<p>Stars and bars answers questions like: “How many ways can I split identical items among labeled groups?”
The answer uses a binomial coefficient.</p>

{concept("Non-negative solutions", '''
<p>Count solutions to $x_1+x_2+\\cdots+x_k=n$ with each $x_i\\ge0$:</p>
$$\\binom{{n+k-1}}{{k-1}}$$
<p>Picture $n$ stars and $k-1$ bars separating $k$ bins.</p>
''')}

{solved(1,
    "Non-negative solutions to $x+y+z=5$?",
    [
        "$n=5$, $k=3$ variables.",
        "$\\binom{{5+3-1}}{{3-1}}=\\binom{{7}}{{2}}=21$.",
    ],
    "$21$",
    "",
    "Easy",
)}

{solved(2,
    "Positive solutions to $x+y+z=5$ (each at least $1$)?",
    [
        "Give each variable $1$ first — uses $3$ from the sum.",
        "Remaining: $x'+y'+z'=2$ with $x',y',z'\\ge0$.",
        "$\\binom{{2+3-1}}{{2}}=\\binom{{4}}{{2}}=6$.",
    ],
    "$6$",
    "",
    "Easy",
)}

{page_break()}

{solved(3,
    "How many ways to buy $7$ bagels of $3$ types if order does not matter and you can buy zero of a type?",
    [
        "Identical bagels → stars and bars with $n=7$, $k=3$ types.",
        "$\\binom{{7+3-1}}{{3-1}}=\\binom{{9}}{{2}}=36$.",
    ],
    "$36$",
    "",
    "Medium",
)}

{solved(4,
    "Non-negative solutions to $x+y=7$?",
    [
        "List idea: $x=0,1,\\ldots,7$ each gives one $y$ → $8$ solutions.",
        "Formula: $\\binom{{7+2-1}}{{1}}=8$.",
    ],
    "$8$",
    "",
    "Medium",
)}

{concept("Upper bounds (complement)", '''
<p>If $x_1\\le m$, count all non-negative solutions, then subtract those with $x_1\\ge m+1$.</p>
''')}

{solved(5,
    "Non-negative solutions to $x+y+z=10$ with $x\\le4$?",
    [
        "Total: $\\binom{{12}}{{2}}=66$.",
        "Bad ($x\\ge5$): let $x'=x-5\\ge0$, then $x'+y+z=5$ → $\\binom{{7}}{{2}}=21$.",
        "Valid: $66-21=45$.",
    ],
    "$45$",
    "",
    "Hard",
)}

{solved(6,
    "Positive solutions to $a+b+c+d=8$?",
    [
        "Each at least $1$ → subtract $4$ from sum.",
        "Non-negative solutions to $a'+b'+c'+d'=4$: $\\binom{{7}}{{3}}=35$.",
    ],
    "$35$",
    "",
    "Hard",
)}

{watch_out("Using stars and bars on distinct objects",
    "If books are different titles, you cannot treat them as identical stars. "
    "Use combinations or product rules instead.")}

{page_break()}

{solved(7,
    "Non-negative solutions to $w+x+y+z=3$?",
    [
        "$\\binom{{3+4-1}}{{4-1}}=\\binom{{6}}{{3}}=20$.",
    ],
    "$20$",
    "",
    "Hard",
)}

{solved(8,
    "Positive solutions to $x_1+x_2+x_3+x_4+x_5=12$?",
    [
        "Minimum $1$ each uses $5$; remaining sum $7$.",
        "$\\binom{{7+5-1}}{{5-1}}=\\binom{{11}}{{4}}=330$.",
    ],
    "$330$",
    "",
    "Challenge",
)}

{strategy_tip(
    "Translate the story: identical items → stars; distinct recipients → bars between bins."
)}

{before_practice([
    "Are items identical and boxes distinct?",
    "Non-negative or strictly positive (subtract 1 each)?",
    "Any upper caps (use complement)?",
    "Check $\\binom{{n+k-1}}{{k-1}}$ with your $n$ and $k$.",
])}

{practice_section()}
"""
    return title, description, content, _gen_unit5_questions()


def _gen_unit6_questions():
    qs = []
    idx = 1

    pairs = [
        (12, 9, 4, 17),
        (20, 15, 5, 30),
        (25, 20, 10, 35),
        (30, 18, 8, 40),
    ]
    for a, b, ab, ans in pairs:
        qs.append(make_question(
            f"$|A|={a}$, $|B|={b}$, $|A\\cap B|={ab}$. Find $|A\\cup B|$.",
            str(ans), near_int(ans),
            f"${a}+{b}-{ab}={ans}$.", idx)); idx += 1

    for limit, p in ((100, 2), (100, 5), (100, 4), (60, 6), (30, 2)):
        if p == 2:
            ans = limit // 2
        elif p == 5:
            ans = limit // 5
        elif p == 4:
            ans = limit // 4 + limit // 6 - limit // 12
        elif p == 6:
            ans = limit // 6
        qs.append(make_question(
            f"Integers $1$–${limit}$ divisible by ${p if p!=4 else 4}$"
            + (" or $6$" if p == 4 else "") + "?",
            str(ans), near_int(ans),
            f"Computed with inclusion-exclusion / floor division: ${ans}$.", idx)); idx += 1

    qs.append(make_question(
        "Integers $1$–$100$ divisible by $2$ or $5$?",
        "60", ["50", "70", "55"],
        "$50+20-10=60$.", idx)); idx += 1

    qs.append(make_question(
        "Integers $1$–$60$ divisible by $2$, $3$, or $5$?",
        "44", ["30", "50", "38"],
        "$30+20+12-10-6-4+2=44$.", idx)); idx += 1

    qs.append(make_question(
        "Onto functions from a $3$-set to a $2$-set?",
        "6", ["8", "4", "2"],
        "Total $2^3=8$ minus $2$ constant functions → $6$.", idx)); idx += 1

    qs.append(make_question(
        "Onto functions from a $4$-set to a $2$-set?",
        "14", ["16", "8", "12"],
        "$2^4-2=14$.", idx)); idx += 1

    qs.append(make_question(
        "Class: 40 students; 25 math, 20 science, 10 both. Take math or science?",
        "35", ["45", "15", "55"],
        "$25+20-10=35$.", idx)); idx += 1

    qs.append(make_question(
        "Survey of 100: 50 tea, 40 coffee, 20 both. Like neither?",
        "30", ["10", "20", "60"],
        "Union $70$; neither $100-70=30$.", idx)); idx += 1

    qs.append(make_question(
        "Three-set PIE adds back $|A\\cap B\\cap C|$ because:",
        "those elements were subtracted too many times",
        ["they were never counted", "sets must be equal", "only for even n"],
        "Triple overlap correction.", idx)); idx += 1

    qs.append(make_question(
        "Derangements of $3$ objects (!$3$)?",
        "2", ["6", "3", "0"],
        "Only $(2,3,1)$ and $(3,1,2)$ leave no fixed point → $2$.", idx)); idx += 1

    qs.append(make_question(
        "PIE is often better than listing when:",
        "overlap patterns are structured (divisibility, set membership)",
        ["only one object exists", "order always matters", "never on contests"],
        "Structured overlaps suit PIE.", idx)); idx += 1

    while len(qs) < 50:
        limit = 30 + len(qs) * 2
        ans = pie_divisible(limit, [2, 3])
        qs.append(make_question(
            f"Integers $1$–${limit}$ divisible by $2$ or $3$?",
            str(ans), near_int(ans),
            f"$\\lfloor {limit}/2\\rfloor+\\lfloor {limit}/3\\rfloor-\\lfloor {limit}/6\\rfloor={ans}$.", len(qs) + 1))

    return qs[:50]


def unit_inclusion():
    title = "MathCounts Unit 6: Inclusion-Exclusion"
    description = "Count unions without double-counting overlaps."
    content = f"""
<h1>{title}</h1>
<p>When sets overlap, you cannot just add sizes. <strong>Inclusion-exclusion</strong> (PIE) fixes the overlap.</p>

{concept("Two sets", '''
$$|A\\cup B| = |A| + |B| - |A\\cap B|$$
<p>Subtract the overlap because it was counted twice.</p>
''')}

{solved(1,
    "In a class of $40$, $25$ take Math, $20$ take Science, $10$ take both. How many take Math or Science?",
    [
        "$|M\\cup S|=25+20-10=35$.",
    ],
    "$35$",
    "",
    "Easy",
)}

{solved(2,
    "How many integers from $1$ to $100$ are divisible by $2$ or $5$?",
    [
        "Div by $2$: $\\lfloor100/2\\rfloor=50$.",
        "Div by $5$: $\\lfloor100/5\\rfloor=20$.",
        "Div by $10$: $\\lfloor100/10\\rfloor=10$.",
        "Union: $50+20-10=60$.",
    ],
    "$60$",
    "",
    "Easy",
)}

{page_break()}

{concept("Three sets", '''
$$|A\\cup B\\cup C| = |A|+|B|+|C| - |A\\cap B| - |A\\cap C| - |B\\cap C| + |A\\cap B\\cap C|$$
''')}

{solved(3,
    "How many integers from $1$ to $60$ are divisible by $2$, $3$, or $5$?",
    [
        "$30+20+12-10-6-4+2=44$.",
    ],
    "$44$",
    "",
    "Medium",
)}

{solved(4,
    "Onto functions from a $3$-element set to a $2$-element set?",
    [
        "All functions: $2^3=8$.",
        "Not onto: constant functions ($2$ of them).",
        "Onto: $8-2=6$.",
    ],
    "$6$",
    "",
    "Medium",
)}

{watch_out("Forgetting the triple intersection",
    "After subtracting pairwise overlaps, add back $|A\\cap B\\cap C|$ once."
)}

{page_break()}

{solved(5,
    "Band $18$, choir $15$, drama $12$; overlaps $7$, $6$, $5$; all three $3$. How many in at least one?",
    [
        "$18+15+12-7-6-5+3=30$.",
    ],
    "$30$",
    "",
    "Hard",
)}

{solved(6,
    "Survey: $100$ people; $50$ like tea, $40$ coffee, $20$ both. How many like neither?",
    [
        "Union: $50+40-20=70$.",
        "Neither: $100-70=30$.",
    ],
    "$30$",
    "",
    "Hard",
)}

{solved(7,
    "Derangements of $3$ letters A,B,C (no letter in its original position)?",
    [
        "List: BCA and CAB only.",
        "Answer: $2$.",
    ],
    "$2$",
    "",
    "Hard",
)}

{solved(8,
    "Integers $1$–$100$ divisible by $4$ or $6$?",
    [
        "Div by $4$: $25$; by $6$: $16$; by $12$: $8$.",
        "$25+16-8=33$.",
    ],
    "$33$",
    "",
    "Challenge",
)}

{strategy_tip(
    "For divisibility, write $\\lfloor N/p\\rfloor$ for each prime power and combine with PIE signs alternating by set size."
)}

{before_practice([
    "Did I subtract every pairwise intersection?",
    "For three sets, did I add the triple intersection back?",
    "Can I use complement (neither) instead?",
    "For onto functions: total minus those missing a value.",
])}

{practice_section()}
"""
    return title, description, content, _gen_unit6_questions()


def _gen_unit7_questions():
    qs = []
    idx = 1

    for a, b in ((3, 3), (4, 3), (5, 2), (6, 1), (5, 5), (4, 4), (7, 2)):
        ans = lattice_paths(a, b)
        qs.append(make_question(
            f"Lattice paths from $(0,0)$ to $({a},{b})$ (right/up only)?",
            str(ans), near_int(ans),
            f"$\\binom{{{a+b}}}{{{a}}}={ans}$.", idx)); idx += 1

    for n in (1, 2, 3, 4, 5, 6):
        ans = domino_tilings_2xn(n)
        qs.append(make_question(
            f"Domino tilings of a $2\\times{n}$ board?",
            str(ans), near_int(ans),
            f"Fibonacci recurrence gives ${ans}$.", idx)); idx += 1

    for n in (3, 4, 5, 6):
        ans = no_consecutive_ones(n)
        qs.append(make_question(
            f"Binary strings of length ${n}$ with no two consecutive $1$s?",
            str(ans), near_int(ans),
            f"Recurrence count: ${ans}$.", idx)); idx += 1

    for n in (2, 3, 4, 5):
        ans = catalan(n)
        qs.append(make_question(
            f"Catalan number $C_{n}$?",
            str(ans), near_int(ans),
            f"$C_{n}=\\frac{{1}}{{n+1}}\\binom{{2n}}{{n}}={ans}$.", idx)); idx += 1

    qs.append(make_question(
        "Paths $(0,0)$ to $(2,2)$ passing through $(1,1)$?",
        "4", ["6", "2", "8"],
        "$\\binom{{2}}{{1}}\\times\\binom{{2}}{{1}}=2\\times2=4$.", idx)); idx += 1

    qs.append(make_question(
        "Paths $(0,0)$ to $(5,5)$ passing through $(2,3)$?",
        "100", ["252", "20", "50"],
        "$\\binom{{5}}{{2}}\\times\\binom{{5}}{{2}}=10\\times10=100$.", idx)); idx += 1

    qs.append(make_question(
        "Standard grid path count uses steps:",
        "only right and up",
        ["any diagonal", "only down", "teleporting"],
        "Classic lattice path model.", idx)); idx += 1

    qs.append(make_question(
        "Sequential path segments combine by:",
        "multiplication",
        ["addition always", "subtraction", "division by 2"],
        "Independent segments multiply.", idx)); idx += 1

    qs.append(make_question(
        "Fibonacci $F_1=1,F_2=1,F_6=$?",
        "8", ["5", "13", "6"],
        "Sequence $1,1,2,3,5,8$.", idx)); idx += 1

    while len(qs) < 50:
        a = 2 + len(qs) % 5
        b = 1 + len(qs) % 4
        ans = lattice_paths(a, b)
        qs.append(make_question(
            f"Paths to $({a},{b})$ on a grid?",
            str(ans), near_int(ans),
            f"$\\binom{{{a+b}}}{{{a}}}={ans}$.", len(qs) + 1))

    return qs[:50]


def unit_paths():
    title = "MathCounts Unit 7: Paths, Recursion & Counting Sequences"
    description = "Grid paths, domino tilings, Fibonacci-style recurrences, and Catalan preview."
    content = f"""
<h1>{title}</h1>
<p>Many counting problems become easy once you see a <strong>pattern</strong> or a <strong>recurrence</strong>:
each new size is built from smaller sizes.</p>

{concept("Lattice paths", '''
<p>From $(0,0)$ to $(a,b)$ using only right and up unit steps:</p>
$$\\binom{{a+b}}{{a}}$$
<p>You arrange $a$ right steps among $a+b$ total steps.</p>
''')}

{solved(1,
    "Paths from $(0,0)$ to $(4,3)$ using only right and up?",
    [
        "$7$ steps total: choose which $4$ are right (or which $3$ are up).",
        "$\\binom{{7}}{{3}}=35$.",
    ],
    "$35$",
    "",
    "Easy",
)}

{solved(2,
    "Paths from $(0,0)$ to $(6,1)$?",
    [
        "$7$ steps: $6$ right and $1$ up.",
        "$\\binom{{7}}{{1}}=7$.",
    ],
    "$7$",
    "",
    "Easy",
)}

{page_break()}

{solved(3,
    "Paths from $(0,0)$ to $(2,2)$ that pass through $(1,1)$?",
    [
        "$(0,0)\\to(1,1)$: $\\binom{{2}}{{1}}=2$.",
        "$(1,1)\\to(2,2)$: $\\binom{{2}}{{1}}=2$.",
        "Multiply: $2\\times2=4$.",
    ],
    "$4$",
    "",
    "Medium",
)}

{solved(4,
    "How many ways to tile a $2\\times4$ board with $1\\times2$ dominoes?",
    [
        "Let $a_n$ = tilings of $2\\times n$.",
        "$a_1=1$, $a_2=2$, recurrence $a_n=a_{{n-1}}+a_{{n-2}}$.",
        "$a_4=a_3+a_2=3+2=5$.",
    ],
    "$5$",
    "",
    "Medium",
)}

{concept("Catalan numbers (preview)", '''
$$C_n=\\frac{{1}}{{n+1}}\\binom{{2n}}{{n}}$$
<p>Count Dyck paths, balanced parentheses, and many “never go below the diagonal” problems.</p>
''')}

{solved(5,
    "Compute $C_3$.",
    [
        "$C_3=\\dfrac{{1}}{{4}}\\binom{{6}}{{3}}=\\dfrac{{20}}{{4}}=5$.",
    ],
    "$5$",
    "",
    "Hard",
)}

{solved(6,
    "Binary strings of length $5$ with no two consecutive $1$s?",
    [
        "Let $b_n$ count valid length-$n$ strings.",
        "$b_1=2$, $b_2=3$, recurrence $b_n=b_{{n-1}}+b_{{n-2}}$.",
        "$b_5=8$.",
    ],
    "$8$",
    "",
    "Hard",
)}

{watch_out("Adding path segments",
    "If you must pass through a point, multiply counts for each leg — do not add them."
)}

{page_break()}

{solved(7,
    "Paths from $(0,0)$ to $(5,5)$ through $(2,3)$?",
    [
        "$(0,0)\\to(2,3)$: $\\binom{{5}}{{2}}=10$.",
        "$(2,3)\\to(5,5)$: $\\binom{{5}}{{2}}=10$.",
        "Product: $100$.",
    ],
    "$100$",
    "",
    "Hard",
)}

{solved(8,
    "Compute $C_4$.",
    [
        "$C_4=\\dfrac{{1}}{{5}}\\binom{{8}}{{4}}=\\dfrac{{70}}{{5}}=14$.",
    ],
    "$14$",
    "",
    "Challenge",
)}

{strategy_tip(
    "When a problem looks like “build from smaller pieces,” try a recurrence: "
    "count how the first move or first tile splits the problem."
)}

{before_practice([
    "Is this a right/up path (binomial)?",
    "Must the path pass through a point (multiply legs)?",
    "Does a tiling or string problem repeat a Fibonacci pattern?",
    "For Catalan: is there a diagonal or balance constraint?",
])}

{practice_section()}
"""
    return title, description, content, _gen_unit7_questions()


def _gen_unit8_questions():
    qs = []
    idx = 1

    # Mixed numeric from prior units
    mixed = [
        ("Odd 3-digit numbers with distinct digits?", 5 * 9 * 8, "Units odd (5); hundreds 9; tens 8 → 360."),
        ("Rectangles in a $3\\times3$ unit grid?", math.comb(4, 2) ** 2, "Choose 2 horizontal and 2 vertical lines: $6^2=36$."),
        ("$P(10,6)-P(9,6)$ (6-digit strings using 0–9, all digits distinct, at least one 0)?",
         math.perm(10, 6) - math.perm(9, 6), "$151200-60480=90720$."),
        ("Non-neg solutions $x+y+z+w=5$?", stars_bars_nonneg(5, 4), "$\\binom{{8}}{{3}}=56$."),
        ("Paths $(0,0)$ to $(5,3)$?", lattice_paths(5, 3), "$\\binom{{8}}{{3}}=56$."),
        ("Arrangements of MISSISSIPPI?", perm_repeated("MISSISSIPPI"), "$34650$."),
        ("Split 8 people into two unlabeled teams of 4?", math.comb(8, 4) // 2, "$70/2=35$."),
        ("Onto functions $[5]\\to[3]$?",
         3 ** 5 - 3 * 2 ** 5 + 3 * 1 ** 5, "$243-96+3=150$."),
        ("Positive solutions $x+y+z=8$?", stars_bars_positive(8, 3), "$\\binom{{7}}{{2}}=21$."),
        ("Integers $1$–$50$ divisible by $2$ or $3$?", pie_divisible(50, [2, 3]), "$25+16-8=33$."),
    ]
    for text, ans, expl in mixed:
        qs.append(make_question(text, str(ans), near_int(ans), expl, idx)); idx += 1

    qs.append(make_question(
        "Rooks on a $4\\times4$ board: choose 3 non-attacking rooks (one per row and column)?",
        "96", ["64", "24", "256"],
        "$\\binom{{4}}{{3}}^2\\times3!=16\\times6=96$.", idx)); idx += 1

    qs.append(make_question(
        "Committee of $4$ from $10$, then elect chair from committee?",
        "840", ["210", "5040", "120"],
        "$\\binom{{10}}{{4}}\\times4=840$.", idx)); idx += 1

    qs.append(make_question(
        "When stuck on a hard counting problem, a good first move is:",
        "try small cases or complement",
        ["always guess n!", "skip immediately", "only use one formula"],
        "Small cases reveal structure; complement simplifies “at least one.”", idx)); idx += 1

    qs.append(make_question(
        "MathCounts Sprint tip: if you see “at least one,” often try:",
        "complement counting",
        ["always stars and bars", "always Catalan", "never subtract"],
        "Total minus “none” is fast on Sprint.", idx)); idx += 1

    qs.append(make_question(
        "Target round tip: before calculating, you should:",
        "write a one-line plan",
        ["memorize pi", "avoid diagrams", "never check answer form"],
        "A plan prevents mixing permutations and combinations.", idx)); idx += 1

    qs.append(make_question(
        "Team round tip:",
        "split problems by topic and verify key counts two ways",
        ["one person does all work silently", "never discuss", "skip checking"],
        "Cross-check catches order vs unordered mistakes.", idx)); idx += 1

    qs.append(make_question(
        "AMC 8 answers are always:",
        "non-negative integers",
        ["fractions", "always multiples of 10", "sometimes pi"],
        "If you get a fraction, re-read the problem.", idx)); idx += 1

    qs.append(make_question(
        "Order matters for medals but not for choosing a team. This distinction is:",
        "essential on every contest",
        ["rarely tested", "only for geometry", "never on AMC 8"],
        "Core permutations vs combinations check.", idx)); idx += 1

    qs.append(make_question(
        "Plugging in small $n$ helps when:",
        "a recurrence or pattern is suspected",
        ["only on geometry", "never on counting", "only on team round"],
        "Small cases expose the recurrence.", idx)); idx += 1

    while len(qs) < 50:
        a = 2 + len(qs) % 4
        b = 2 + len(qs) % 3
        ans = lattice_paths(a, b)
        qs.append(make_question(
            f"Mixed review: paths $(0,0)$ to $({a},{b})$?",
            str(ans), near_int(ans),
            f"$\\binom{{{a+b}}}{{{a}}}={ans}$.", len(qs) + 1))

    return qs[:50]


def unit_contest_mixed():
    title = "MathCounts Unit 8: Contest Mixed Sets & Strategy"
    description = "Mixed AMC 8 / MathCounts problems plus Sprint, Target, and Team strategy."
    content = f"""
<h1>{title}</h1>
<p>This unit mixes ideas from Units 1–7 the way real contests do — and teaches how to <em>manage time</em>
and pick the right tool quickly.</p>

{concept("Round-by-round strategy", '''
<ul>
<li><strong>Sprint (MathCounts):</strong> 40 problems in 30 minutes. Recognize the tool in under 30 seconds.
If you see “at least one,” think complement first.</li>
<li><strong>Target:</strong> Pairs of harder problems with calculators allowed. Write a one-line plan before computing.</li>
<li><strong>Team:</strong> Divide by strength (counting vs geometry vs algebra). Verify important counts two ways.</li>
<li><strong>AMC 8:</strong> Answers are integers from $0$ to $999$. A fraction usually means a misread.</li>
</ul>
''')}

{solved(1,
    "How many odd 3-digit numbers have all distinct digits?",
    [
        "Units must be odd: $1,3,5,7,9$ → $5$ choices.",
        "Hundreds: any of $1$–$9$ except the units digit if needed — $9$ choices (units is never $0$).",
        "Tens: $8$ remaining digits (including $0$).",
        "$5\\times9\\times8=360$.",
    ],
    "$360$",
    "",
    "Easy",
)}

{solved(2,
    "How many rectangles in a $3\\times3$ grid of unit squares?",
    [
        "Choose $2$ horizontal grid lines from $4$: $\\binom{{4}}{{2}}=6$.",
        "Choose $2$ vertical lines from $4$: $\\binom{{4}}{{2}}=6$.",
        "Multiply: $6\\times6=36$.",
    ],
    "$36$",
    "",
    "Easy",
)}

{page_break()}

{solved(3,
    "6-character codes from digits $0$–$9$, all digits distinct, at least one $0$?",
    [
        "Total distinct 6-digit strings from 10 digits: $P(10,6)=151200$.",
        "No zero: $P(9,6)=60480$.",
        "At least one zero: $151200-60480=90720$.",
    ],
    "$90720$",
    "",
    "Medium",
)}

{solved(4,
    "Place $3$ non-attacking rooks on a $4\\times4$ board (one per row and column)?",
    [
        "Choose $3$ rows: $\\binom{{4}}{{3}}$; choose $3$ columns: $\\binom{{4}}{{3}}$.",
        "Assign columns to rows: $3!$.",
        "$\\binom{{4}}{{3}}^2\\times6=16\\times6=96$.",
    ],
    "$96$",
    "",
    "Medium",
)}

{watch_out("Forcing one formula",
    "If a problem mentions distinct objects, do not use stars and bars. "
    "Label what is identical before choosing a method."
)}

{page_break()}

{solved(5,
    "Split $8$ people into two unlabeled teams of $4$?",
    [
        "Labeled teams: $\\binom{{8}}{{4}}=70$.",
        "Unlabeled: divide by $2$ → $35$.",
    ],
    "$35$",
    "",
    "Hard",
)}

{solved(6,
    "Onto functions from a $5$-element set to a $3$-element set?",
    [
        "PIE: $3^5-\\binom{{3}}{{1}}2^5+\\binom{{3}}{{0}}1^5=243-96+3=150$.",
    ],
    "$150$",
    "",
    "Hard",
)}

{solved(7,
    "Positive integers $n\\le200$ with digit sum $5$?",
    [
        "1-digit: $\\{5\\}$ → $1$.",
        "2-digit $10a+b$: $a+b=5$, $a\\ge1$ → $(1,4),(2,3),(3,2),(4,1),(5,0)$ → $5$.",
        "3-digit $100a+10b+c$ with $a\\ge1$: $a+b+c=5$ → non-neg solutions to $a'+b+c=4$ with $a'\\ge0$: $\\binom{{6}}{{2}}=15$.",
        "Total: $1+5+15=21$.",
    ],
    "$21$",
    "",
    "Hard",
)}

{solved(8,
    "How many subsets of $\\{1,2,3,4,5,6\\}$ have even size?",
    [
        "Half of all subsets (pairs empty with full set): $2^6/2=32$.",
    ],
    "$32$",
    "",
    "Challenge",
)}

{strategy_tip(
    "<strong>Answer-form check:</strong> MathCounts wants a positive integer. "
    "If you have $\\binom{{10}}{{3}}$, compute $120$ before bubbling."
)}

{before_practice([
    "Which unit’s tool fits in 30 seconds?",
    "Can complement or small cases simplify this?",
    "Did I check order vs unordered?",
    "Is my final answer a contest integer?",
])}

{practice_section()}
"""
    return title, description, content, _gen_unit8_questions()


def master_content():
    return f"""
<h1>{MASTER_TITLE}</h1>
<p><strong>For:</strong> 6th–8th graders preparing for <strong>MathCounts</strong> and <strong>AMC 8</strong>.</p>
<p>Counting questions show up on every contest — from locker codes to path walking to committee picks.
This master course walks you through eight units in a sensible order. Each unit has long explanations,
solved examples from Easy through Challenge, and <strong>50</strong> multiple-choice practice problems.</p>

{page_break()}

<h2>Your roadmap</h2>
<ol>
<li><strong>Unit 1 — Counting Principles:</strong> multiply independent choices, add disjoint cases, subtract complements.</li>
<li><strong>Unit 2 — Permutations:</strong> order matters; factorials; repeated letters; circular tables.</li>
<li><strong>Unit 3 — Combinations:</strong> order does not matter; binomial coefficients; Pascal’s triangle.</li>
<li><strong>Unit 4 — Casework &amp; Overcounting:</strong> clean splits; divide when you double-count.</li>
<li><strong>Unit 5 — Stars and Bars:</strong> identical items into distinct bins; integer solutions.</li>
<li><strong>Unit 6 — Inclusion-Exclusion:</strong> overlapping sets and divisibility.</li>
<li><strong>Unit 7 — Paths &amp; Recursion:</strong> grid walks, tilings, Fibonacci patterns, Catalan preview.</li>
<li><strong>Unit 8 — Contest Mixed Sets:</strong> Sprint/Target/Team strategy and mixed review.</li>
</ol>

<p><strong>Suggested pace:</strong> about one unit per week. Revisit Unit 8 for timed practice before a meet.</p>
<p><strong>How to study:</strong> read the examples slowly, cover the answer, then try the practice set on paper.
Use the quiz explanations to learn from mistakes — not just to score points.</p>
"""


def all_units():
    return [
        unit_counting_principles(),
        unit_permutations(),
        unit_combinations(),
        unit_casework(),
        unit_stars_bars(),
        unit_inclusion(),
        unit_paths(),
        unit_contest_mixed(),
    ]


# ---------------------------------------------------------------------------
# DB operations
# ---------------------------------------------------------------------------

def resolve_creator_id(cursor):
    preferred = os.getenv("COURSE_CREATOR_ID")
    if preferred and preferred.isdigit():
        cursor.execute("SELECT id FROM users WHERE id=%s LIMIT 1", (int(preferred),))
        row = cursor.fetchone()
        if row:
            return row["id"]
    cursor.execute(
        "SELECT id FROM users WHERE role IN ('superadmin','admin') ORDER BY id ASC LIMIT 1"
    )
    row = cursor.fetchone()
    if row:
        return row["id"]
    cursor.execute("SELECT id FROM users ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    return row["id"] if row else None


def upsert_unit(cursor, title, description, content, questions, creator_id, rng):
    cursor.execute(
        "SELECT id FROM courses WHERE title=%s AND grade_level=%s ORDER BY id ASC LIMIT 1",
        (title, GRADE),
    )
    row = cursor.fetchone()
    if row:
        course_id = row["id"]
        cursor.execute(
            "UPDATE courses SET description=%s, content=%s, status='approved', course_type='single' WHERE id=%s",
            (description, content, course_id),
        )
        action = "updated"
    else:
        cursor.execute(
            """
            INSERT INTO courses (title, description, content, creator_id, status, grade_level, course_type)
            VALUES (%s, %s, %s, %s, 'approved', %s, 'single')
            """,
            (title, description, content, creator_id, GRADE),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        course_id = cursor.fetchone()["id"]
        action = "inserted"

    cursor.execute("DELETE FROM course_questions WHERE course_id=%s", (course_id,))
    qids = []
    for raw_q in questions:
        q = shuffle_options(raw_q, rng)
        cursor.execute(
            """
            INSERT INTO course_questions
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                course_id,
                q["question_text"],
                q["question_type"],
                json.dumps(q["options"]),
                q["correct_answer"],
                q["explanation"],
                q["points"],
                q["order_index"],
            ),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        qids.append(cursor.fetchone()["id"])

    placeholders = [placeholder_html(qid, idx) for idx, qid in enumerate(qids, 1)]
    hydrated = fill_quiz_slots(content, placeholders)
    cursor.execute(
        "UPDATE courses SET content=%s, status='approved' WHERE id=%s",
        (hydrated, course_id),
    )
    return {"id": course_id, "title": title, "questions": len(qids), "action": action}


def upsert_master(cursor, creator_id):
    desc = (
        "Master course: MathCounts Counting & Combinatorics for AMC 8 and MathCounts — "
        "eight units with LaTeX lessons, solved examples, and 50 quizzes per unit."
    )
    content = master_content()
    cursor.execute(
        "SELECT id FROM courses WHERE title=%s AND grade_level=%s ORDER BY id ASC LIMIT 1",
        (MASTER_TITLE, GRADE),
    )
    row = cursor.fetchone()
    if row:
        master_id = row["id"]
        cursor.execute(
            """
            UPDATE courses SET description=%s, content=%s, status='approved', course_type='master'
            WHERE id=%s
            """,
            (desc, content, master_id),
        )
        action = "updated"
    else:
        cursor.execute(
            """
            INSERT INTO courses (title, description, content, creator_id, status, grade_level, course_type)
            VALUES (%s, %s, %s, %s, 'approved', %s, 'master')
            """,
            (MASTER_TITLE, desc, content, creator_id, GRADE),
        )
        cursor.execute("SELECT LAST_INSERT_ID() AS id")
        master_id = cursor.fetchone()["id"]
        action = "inserted"
    return master_id, action


def link_units(cursor, master_id, unit_ids):
    cursor.execute("DELETE FROM course_units WHERE parent_course_id=%s", (master_id,))
    for order, child_id in enumerate(unit_ids):
        cursor.execute(
            """
            INSERT INTO course_units
            (parent_course_id, child_course_id, order_index, is_draft, prerequisite_unit_id, linked_course_id)
            VALUES (%s, %s, %s, FALSE, NULL, %s)
            """,
            (master_id, child_id, order, child_id),
        )


def verify(cursor, ids):
    if not ids:
        return []
    placeholders = ",".join(["%s"] * len(ids))
    cursor.execute(
        f"""
        SELECT c.id, c.title, c.course_type, c.status,
               COUNT(q.id) AS q_count,
               (LENGTH(c.content)-LENGTH(REPLACE(c.content, 'quiz-question-placeholder', ''))) /
               LENGTH('quiz-question-placeholder') AS p_count
        FROM courses c
        LEFT JOIN course_questions q ON q.course_id = c.id
        WHERE c.id IN ({placeholders})
        GROUP BY c.id, c.title, c.course_type, c.status, c.content
        ORDER BY c.id
        """,
        ids,
    )
    return cursor.fetchall()


def dry_check():
    """Validate structure and answer integrity without touching the database."""
    bad_expl = re.compile(r"\b(wait|recalculate)\b", re.I)
    bad_content = re.compile(r"\bwait[,\s—-]|actually recalculate\b", re.I)
    units = all_units()
    assert len(units) == 8, f"Expected 8 units, got {len(units)}"
    for title, _desc, content, questions in units:
        assert len(questions) == 50, f"{title}: expected 50 questions, got {len(questions)}"
        slot_count = len(re.findall(r"<!--QUIZ_SLOT_\d+-->", content))
        assert slot_count == 50, f"{title}: expected 50 quiz slots, got {slot_count}"
        if bad_content.search(content):
            raise AssertionError(f"{title}: content contains self-correction phrasing")
        for q in questions:
            assert q["correct_answer"] in q["options"], (
                f"{title} Q{q['order_index']}: correct answer not in options"
            )
            if bad_expl.search(q["explanation"]):
                raise AssertionError(
                    f"{title} Q{q['order_index']}: explanation contains banned phrasing"
                )
    print("DRY_CHECK OK: 8 units, 50 questions each, all answers verified.")


def main():
    if not AIVEN_CONFIG["password"]:
        print("ERROR: Set AIVEN_PASSWORD (or MYSQLPASSWORD) env var before running.")
        return 1

    rng = random.Random(RNG_SEED)
    print("Connecting to Aiven/MySQL...")
    try:
        conn = pymysql.connect(**AIVEN_CONFIG)
    except Exception as exc:
        print(f"Connection failed: {exc}")
        return 1

    try:
        cursor = conn.cursor()
        creator_id = resolve_creator_id(cursor)
        if not creator_id:
            print("ERROR: No users found to use as creator_id.")
            return 1
        print(f"Using creator_id: {creator_id}")

        unit_results = []
        for i, (title, desc, content, questions) in enumerate(all_units(), 1):
            result = upsert_unit(cursor, title, desc, content, questions, creator_id, rng)
            unit_results.append(result)
            print(
                f"[Unit {i}/8] {result['action'].upper()} | ID {result['id']} | "
                f"Q {result['questions']} | {result['title']}"
            )

        master_id, master_action = upsert_master(cursor, creator_id)
        link_units(cursor, master_id, [u["id"] for u in unit_results])
        print(f"[Master] {master_action.upper()} | ID {master_id} | {MASTER_TITLE}")
        print(f"Linked {len(unit_results)} units to master {master_id}")

        conn.commit()

        rows = verify(cursor, [u["id"] for u in unit_results] + [master_id])
        ok = True
        for row in rows:
            q, p = int(row["q_count"]), int(row["p_count"] or 0)
            ctype = row.get("course_type") or "single"
            match = "OK" if (ctype == "master" and q == 0) or (q == p and q > 0) else "MISMATCH"
            if match != "OK":
                ok = False
            print(
                f"  verify id={row['id']} type={ctype} status={row['status']} "
                f"q={q} placeholders={p} → {match}"
            )

        cursor.execute(
            "SELECT COUNT(*) AS n FROM course_units WHERE parent_course_id=%s", (master_id,)
        )
        linked = cursor.fetchone()["n"]
        print(f"  course_units linked: {linked}")
        if linked != 8:
            ok = False

        if ok:
            print("SUCCESS: MathCounts Counting & Combinatorics injected.")
            return 0
        print("WARNING: Verification found mismatches.")
        return 2
    except Exception as exc:
        conn.rollback()
        print(f"ERROR: {exc}")
        raise
    finally:
        conn.close()
        if _ca_path and os.path.isfile(_ca_path):
            try:
                os.remove(_ca_path)
            except OSError:
                pass


if __name__ == "__main__":
    if os.getenv("DRY_CHECK") == "1":
        dry_check()
        sys.exit(0)
    sys.exit(main())

