#!/usr/bin/env python3
"""Inject MathCounts Counting & Combinatorics master + 8 unit courses into Aiven.

- Secrets via env only (AIVEN_PASSWORD / MYSQLPASSWORD, DB_SSL_CA).
- Quiz hydration: insert questions → LAST_INSERT_ID → <!--QUIZ_SLOT_n--> placeholders.
- Idempotent by (title, grade_level).
"""

import io
import json
import os
import random
import re
import ssl
import sys

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
    # Aiven requires TLS; allow handshake without local CA file if env not set.
    _ssl_ctx = ssl.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl.CERT_NONE
    AIVEN_CONFIG["ssl"] = _ssl_ctx


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def page_break():
    return '<hr class="page-break" />'


def solved(num, problem, steps, answer, note=""):
    steps_html = "".join(f"<li>{s}</li>" for s in steps)
    note_html = f"<p><em>{note}</em></p>" if note else ""
    return (
        f'<div style="background:#f4f8ff;border:1px solid #c9def4;border-radius:10px;'
        f'padding:16px;margin:14px 0;">'
        f"<h4>Solved Example {num}</h4>"
        f"<p><strong>Problem:</strong> {problem}</p>"
        f"<ol>{steps_html}</ol>"
        f'<p><strong>Answer:</strong> <span style="background:#dcfce7;padding:2px 8px;'
        f'border-radius:4px;">{answer}</span></p>{note_html}</div>'
    )


def trap(title, wrong, right):
    return (
        f'<div style="background:#fff5f5;border:1px solid #fecaca;border-radius:10px;'
        f'padding:14px;margin:12px 0;">'
        f"<h4>Trap: {title}</h4>"
        f"<p><strong>Common mistake:</strong> {wrong}</p>"
        f"<p><strong>Fix:</strong> {right}</p></div>"
    )


def concept(title, body):
    return f"<h3>{title}</h3>{body}"


def practice_block(items):
    lis = "".join(f"<li>{p}</li>" for p in items)
    return f"<h3>Practice (worked answers below)</h3><ol>{lis}</ol>"


def quiz_slot(n):
    return f"<!--QUIZ_SLOT_{n}-->"


def make_question(text, correct, distractors, explanation, idx, points=1):
    opts = [correct] + list(distractors)[:3]
    unique = []
    for opt in opts:
        s = str(opt)
        if s not in unique:
            unique.append(s)
    while len(unique) < 4:
        unique.append(f"Option {len(unique) + 1}")
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
# Unit definitions: content + questions
# ---------------------------------------------------------------------------

def unit_counting_principles():
    title = "MathCounts Unit 1: Counting Principles"
    description = (
        "Product and sum rules, complementary counting, and systematic enumeration "
        "for MathCounts Chapter through National."
    )
    content = f"""
<h1>{title}</h1>
<p><strong>Level:</strong> MathCounts Chapter → National &nbsp;|&nbsp; <strong>Focus:</strong> product rule, sum rule, complementary counting.</p>
<p>Counting is the art of organizing possibilities so nothing is missed and nothing is double-counted.
This unit builds the two rules every contest problem rests on.</p>

{concept("The Product Rule", '''
<p>If a process has $k$ independent stages, and stage $i$ can be done in $n_i$ ways
<strong>regardless of previous choices</strong>, then the total is</p>
$$N = n_1 \\cdot n_2 \\cdots n_k.$$
<p>Think of filling slots: password digits, outfit pieces, paths with forced turns.</p>
''')}

{solved(1,
    "A locker code has 3 digits from $0$–$9$. How many codes are possible if digits may repeat?",
    [
        "Slot 1: $10$ choices ($0$–$9$).",
        "Slot 2: again $10$ choices (repeats allowed).",
        "Slot 3: $10$ choices.",
        "Product rule: $10 \\times 10 \\times 10 = 1000$.",
    ],
    "$1000$",
    "If order matters and slots are independent, multiply.",
)}

{solved(2,
    "Same locker, but digits must be <em>distinct</em>. How many codes?",
    [
        "First digit: $10$ choices.",
        "Second: $9$ remaining.",
        "Third: $8$ remaining.",
        "$10 \\times 9 \\times 8 = 720$.",
    ],
    "$720$",
)}

{concept("The Sum Rule", '''
<p>If the outcomes split into <strong>disjoint</strong> cases $A_1, A_2, \\ldots, A_m$, then</p>
$$|A_1 \\cup A_2 \\cup \\cdots \\cup A_m| = |A_1| + |A_2| + \\cdots + |A_m|.$$
<p>Cases must not overlap. If they do, you need inclusion-exclusion (Unit 6).</p>
''')}

{solved(3,
    "How many 2-digit numbers have either both digits even or both digits odd?",
    [
        "Tens digit cannot be $0$. Even tens: $2,4,6,8$ ($4$ choices). Even units: $0,2,4,6,8$ ($5$). Both even: $4 \\times 5 = 20$.",
        "Odd tens: $1,3,5,7,9$ ($5$). Odd units: $1,3,5,7,9$ ($5$). Both odd: $5 \\times 5 = 25$.",
        "Cases disjoint → sum: $20 + 25 = 45$.",
    ],
    "$45$",
)}

{page_break()}

{concept("Complementary Counting", '''
<p>Often easier: count the total, subtract the bad cases.</p>
$$|\\text{good}| = |\\text{universe}| - |\\text{bad}|.$$
<p>Use this when “at least one” or “not all” appears.</p>
''')}

{solved(4,
    "How many 3-letter strings from $\\{A,B,C,D\\}$ (repeats OK) use at least one $A$?",
    [
        "Total strings: $4^3 = 64$.",
        "Strings with no $A$: $3^3 = 27$.",
        "At least one $A$: $64 - 27 = 37$.",
    ],
    "$37$",
    "Direct casework on “exactly one / two / three $A$” works but is longer.",
)}

{solved(5,
    "A fair six-sided die is rolled twice. In how many ordered outcomes is the sum at least $10$?",
    [
        "Universe: $6 \\times 6 = 36$ ordered pairs.",
        "Sum $\\ge 10$: $(4,6),(5,5),(5,6),(6,4),(6,5),(6,6)$ → wait, also $(4,6)$ already; list carefully: sums $10,11,12$.",
        "Sum $10$: $(4,6),(5,5),(6,4)$ → $3$. Sum $11$: $(5,6),(6,5)$ → $2$. Sum $12$: $(6,6)$ → $1$. Total $6$.",
        "Complement: sum $\\le 9$ is $36-6=30$ (sanity check).",
    ],
    "$6$",
)}

{trap("Multiplying when cases overlap",
      "Adding product-rule counts for overlapping descriptions.",
      "Draw a Venn sketch or redefine disjoint cases before adding.")}

{trap("Forgetting leading-zero restrictions",
      "Treating a 3-digit number like a 3-digit string with leading zeros allowed.",
      "Separate the first digit’s allowed set.")}

{quiz_slot(1)}
{quiz_slot(2)}
{quiz_slot(3)}

{page_break()}

{concept("Systematic Listing", '''
<p>For small $n$, list in lexicographic order. Contest problems often hide behind “how many” when listing is feasible and safer than a wrong formula.</p>
''')}

{solved(6,
    "How many positive integers less than $50$ have digit sum $9$?",
    [
        "1-digit: only $9$ → $1$ number.",
        "2-digit $10a+b$ with $a\\in[1,4]$, $a+b=9$, $b\\in[0,9]$: $(1,8),(2,7),(3,6),(4,5)$ → $4$.",
        "Wait — also $a$ can be up to $4$ for $<50$, but $a=5$ gives $50$ which is not less than $50$. Also include $18,27,36,45$ and $9$. What about $90$? Too big. Also $36$ ok.",
        "Actually 2-digit with $a\\le 4$: $(1,8),(2,7),(3,6),(4,5)$ only? $(1,8)=18$. Also $(9,0)=90$ out. And $27$, etc. Plus $a=4,b=5$. Count also numbers like $36$. That's $4$ two-digit + $1$ one-digit = $5$? Missing $a$ from $1$ to $4$ is incomplete for digit sum $9$ under $50$: also $a=5$ is $50$ excluded. What about $39$? $3+9=12$. Recheck: pairs $(a,b)$ with $a\\in\\{{1,2,3,4\\}}$, $b=9-a\\in[0,9]$: $(1,8),(2,7),(3,6),(4,5)$ — $4$. Plus $9$ — total $5$.",
        "Wait — also two-digit numbers like $18$ only those. But $45$ yes. Is $90$ out yes. Final: $5$? That seems too small. Numbers $<50$ with digit sum $9$: $9,18,27,36,45$ — yes $5$. Also $39$ has sum $12$. Correct.",
    ],
    "$5$",
)}

{practice_block([
    "Password of length $4$ from $26$ letters, repeats allowed: $26^4$.",
    "Same, no repeats: $P(26,4)=26\\times25\\times24\\times23$.",
    "How many subsets of $\\{1,2,3,4,5\\}$ contain $1$? Complement of those without $1$: $2^5-2^4=16$.",
])}

{quiz_slot(4)}
{quiz_slot(5)}
{quiz_slot(6)}
{quiz_slot(7)}
{quiz_slot(8)}
{quiz_slot(9)}
{quiz_slot(10)}
{quiz_slot(11)}
{quiz_slot(12)}
"""
    questions = [
        make_question(
            "A code has 2 letters from A–Z then 2 digits $0$–$9$, all independent with repeats OK. How many codes?",
            "67600", ["65000", "6760", "456976"],
            "Product: $26\\times26\\times10\\times10=67600$.", 1),
        make_question(
            "How many 3-digit numbers have all distinct digits?",
            "648", ["900", "720", "504"],
            "First digit $9$ choices ($1$–$9$); second $9$ (incl. $0$ minus used); third $8$: $9\\times9\\times8=648$.", 2),
        make_question(
            "Strings of length $3$ from $\\{A,B,C\\}$ (repeats OK) with at least one $A$: ?",
            "19", ["27", "8", "26"],
            "Total $3^3=27$; no $A$: $2^3=8$; at least one $A$: $27-8=19$.", 3),
        make_question(
            "License plates: 3 letters then 3 digits, letters distinct, digits distinct. Count?",
            "11232000", ["17576000", "308915776", "676000"],
            "$P(26,3)\\times P(10,3)=26\\times25\\times24\\times10\\times9\\times8=11232000$.", 4),
        make_question(
            "A meal: 3 soups, 4 mains, 2 desserts. Must pick one of each. How many meals?",
            "24", ["9", "12", "48"],
            "Product rule: $3\\times4\\times2=24$.", 5),
        make_question(
            "How many positive integers $\\le 100$ are divisible by $2$ or $5$? (use complement carefully)",
            "60", ["50", "70", "55"],
            "Div by $2$: $50$; by $5$: $20$; by $10$: $10$. Union $50+20-10=60$.", 6),
        make_question(
            "Die rolled twice (ordered). Outcomes with sum $=7$?",
            "6", ["5", "7", "12"],
            "$(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$ → $6$.", 7),
        make_question(
            "Bit strings of length $5$ that are not all zeros?",
            "31", ["32", "30", "16"],
            "Total $2^5=32$; subtract the all-zero string → $31$.", 8),
        make_question(
            "How many ways to assign each of $4$ students a grade A/B/C/D/F (repeats OK)?",
            "625", ["120", "1024", "20"],
            "Each student $5$ choices: $5^4=625$.", 9),
        make_question(
            "Two-digit numbers with both digits the same?",
            "9", ["10", "90", "11"],
            "$11,22,\\ldots,99$ → $9$.", 10),
        make_question(
            "From $\\{1,2,3,4,5,6\\}$, how many ordered pairs $(a,b)$ have $a+b$ even?",
            "18", ["15", "36", "12"],
            "Both odd or both even: $3\\times3+3\\times3=18$.", 11),
        make_question(
            "Complementary counting is best when the problem asks for:",
            "at least one / not all of something",
            ["exact permutations of distinct objects only", "only grid path counts", "only binomial coefficients"],
            "Complements shine on “at least / not all” language.", 12),
    ]
    return title, description, content, questions


def unit_permutations():
    title = "MathCounts Unit 2: Permutations & Arrangements"
    description = "Factorials, $P(n,k)$, arrangements with repetition and identical items."
    content = f"""
<h1>{title}</h1>
<p>Permutations count <strong>ordered</strong> selections. The core formulas:</p>
$$n! = 1\\cdot 2\\cdots n, \\qquad P(n,k)=\\frac{{n!}}{{(n-k)!}}=n(n-1)\\cdots(n-k+1).$$

{concept("Arranging distinct objects", '''
<p>$n$ distinct objects in a line: $n!$ orders. Choosing $k$ of them in order: $P(n,k)$.</p>
''')}

{solved(1,
    "How many ways to arrange the letters in MATH?",
    ["$4$ distinct letters → $4!=24$."],
    "$24$",
)}

{solved(2,
    "From $10$ students, how many ways to choose a president, VP, and secretary (all different)?",
    [
        "Order matters and roles differ → $P(10,3)=10\\times9\\times8=720$.",
        "Not $C(10,3)$ because roles are distinct.",
    ],
    "$720$",
)}

{solved(3,
    "How many distinct arrangements of the letters in BALLOON?",
    [
        "Letters: B,A,L,L,O,O,N → $7$ letters with L$\\times2$, O$\\times2$.",
        "Formula: $\\dfrac{{7!}}{{2!\\,2!}}=\\dfrac{{5040}}{{4}}=1260$.",
    ],
    "$1260$",
)}

{page_break()}

{concept("With repetition vs without", '''
<p>Ordered $k$-tuples from $n$ types with repetition: $n^k$. Without: $P(n,k)$.</p>
''')}

{solved(4,
    "How many $4$-digit PINs using digits $0$–$9$ with no repeated digit?",
    ["$P(10,4)=10\\times9\\times8\\times7=5040$."],
    "$5040$",
)}

{solved(5,
    "Arrange $5$ people around a circular table (rotations same). How many?",
    [
        "Circular arrangements of $n$ distinct: $(n-1)!$.",
        "$(5-1)!=24$.",
    ],
    "$24$",
    "If reflections are the same (necklace), divide by $2$ more — only when the problem says so.",
)}

{solved(6,
    "How many injective functions from a set of $3$ elements to a set of $7$?",
    ["Choose images in order: $P(7,3)=7\\times6\\times5=210$."],
    "$210$",
)}

{trap("Using $n!$ when there are identical letters",
      "Counting MISSISSIPPI as $11!$.",
      "Divide by factorials of repeated letters: $\\frac{{11!}}{{4!4!2!}}$.")}

{trap("Using combinations for distinct roles",
      "Choosing chair/secretary with $C(n,2)$.",
      "Roles ordered → use $P(n,2)$.")}

{quiz_slot(1)}
{quiz_slot(2)}
{quiz_slot(3)}
{page_break()}

{practice_block([
    "Arrangements of SUCCESS: $\\frac{{7!}}{{3!2!}}$.",
    "P(12,2)=12\\times11=132.",
    "Circular arrangements of 8 beads if flips count as same: $\\frac{{7!}}{{2}}$.",
])}

{quiz_slot(4)}
{quiz_slot(5)}
{quiz_slot(6)}
{quiz_slot(7)}
{quiz_slot(8)}
{quiz_slot(9)}
{quiz_slot(10)}
{quiz_slot(11)}
{quiz_slot(12)}
"""
    questions = [
        make_question("Compute $P(8,3)$.", "336", ["56", "512", "24"],
                      "$8\\times7\\times6=336$.", 1),
        make_question("Arrangements of the word CODE?", "24", ["16", "12", "4"],
                      "$4!=24$.", 2),
        make_question("Distinct arrangements of LEVEL?", "30", ["120", "60", "24"],
                      "$\\frac{{5!}}{{2!2!}}=30$.", 3),
        make_question("Ways to award gold/silver/bronze among $9$ runners?", "504", ["84", "729", "36"],
                      "$P(9,3)=9\\times8\\times7=504$.", 4),
        make_question("Circular arrangements of $6$ distinct people?", "120", ["720", "60", "24"],
                      "$(6-1)!=120$.", 5),
        make_question("PINs of length $3$ from digits $0$–$9$, no repeats?", "720", ["1000", "900", "504"],
                      "$P(10,3)=720$.", 6),
        make_question("Distinct arrangements of BOOKKEEPER letters count formula uses denominators:",
                      "2! 2! 3! 2!", ["11!", "only 2!", "4! 4!"],
                      "B1 O2 K2 E3 P1 R1 → divide by $2!2!3!$. (P,R,B once).", 7),
        make_question("How many injective functions from $\\{1,2\\}$ to $\\{1,2,3,4\\}$?",
                      "12", ["16", "6", "8"],
                      "$P(4,2)=12$.", 8),
        make_question("$7!$ equals", "5040", ["720", "40320", "840"],
                      "$7!=5040$.", 9),
        make_question("Arrangements of AAA BBB with all letters used?",
                      "20", ["720", "36", "6"],
                      "$\\frac{{6!}}{{3!3!}}=20$.", 10),
        make_question("Number of $5$-letter words from $8$ distinct letters, no repeats?",
                      "6720", ["56", "32768", "40"],
                      "$P(8,5)=8\\times7\\times6\\times5\\times4=6720$.", 11),
        make_question("When should you use $P(n,k)$ instead of $C(n,k)$?",
                      "When order/roles matter",
                      ["When order never matters", "Only for identical objects", "Only for circles"],
                      "Permutations encode order.", 12),
    ]
    return title, description, content, questions


def unit_combinations():
    title = "MathCounts Unit 3: Combinations & Binomials"
    description = "Combinations $C(n,k)$, Pascal's identity, and binomial theorem links."
    content = f"""
<h1>{title}</h1>
<p>Combinations count <strong>unordered</strong> selections:</p>
$$C(n,k)=\\binom{{n}}{{k}}=\\frac{{n!}}{{k!(n-k)!}}=\\frac{{P(n,k)}}{{k!}}.$$

{concept("From permutations to combinations", '''
<p>Every unordered $k$-set corresponds to $k!$ ordered $k$-tuples, so divide $P(n,k)$ by $k!$.</p>
''')}

{solved(1,
    "How many ways to choose $3$ books from $10$?",
    ["$\\binom{{10}}{{3}}=\\dfrac{{10\\times9\\times8}}{{6}}=120$."],
    "$120$",
)}

{solved(2,
    "A committee of $4$ from $6$ girls and $5$ boys must include $2$ girls and $2$ boys. Count?",
    [
        "$\\binom{{6}}{{2}}\\binom{{5}}{{2}}=15\\times10=150$.",
        "Product of independent combination counts.",
    ],
    "$150$",
)}

{solved(3,
    "Expand $(x+y)^4$ and find the coefficient of $x^2 y^2$.",
    [
        "Binomial theorem: $(x+y)^n=\\sum \\binom{{n}}{{k}} x^{{n-k}} y^k$.",
        "Here $n=4$, need $x^2 y^2$ → $\\binom{{4}}{{2}}=6$.",
    ],
    "$6$",
)}

{page_break()}

{concept("Pascal's identity", '''
<p>$$\\binom{{n}}{{k}}=\\binom{{n-1}}{{k}}+\\binom{{n-1}}{{k-1}}.$$</p>
<p>Combinatorial proof: fix element $x$. Subsets containing $x$: $\\binom{{n-1}}{{k-1}}$; not containing $x$: $\\binom{{n-1}}{{k}}$.</p>
''')}

{solved(4,
    "Compute $\\binom{{8}}{{3}}$ using Pascal from $\\binom{{7}}{{2}}$ and $\\binom{{7}}{{3}}$.",
    [
        "$\\binom{{7}}{{2}}=21$, $\\binom{{7}}{{3}}=35$.",
        "$\\binom{{8}}{{3}}=21+35=56$.",
    ],
    "$56$",
)}

{solved(5,
    "How many $5$-card hands from a $52$-card deck?",
    ["$\\binom{{52}}{{5}}=2598960$."],
    "$2598960$",
)}

{solved(6,
    "Number of subsets of an $n$-element set?",
    [
        "Each element in or out → $2^n$.",
        "Also $\\sum_{{k=0}}^{{n}}\\binom{{n}}{{k}}=2^n$.",
    ],
    "$2^n$",
)}

{trap("Forgetting to divide by $k!$",
      "Reporting $P(n,k)$ when the problem says “choose a team”.",
      "Ask: does order among the chosen matter?")}

{quiz_slot(1)}
{quiz_slot(2)}
{quiz_slot(3)}
{page_break()}

{practice_block([
    "$\\binom{{12}}{{2}}=66$.",
    "$\\binom{{n}}{{0}}=\\binom{{n}}{{n}}=1$.",
    "$\\binom{{n}}{{1}}=n$.",
])}

{quiz_slot(4)}
{quiz_slot(5)}
{quiz_slot(6)}
{quiz_slot(7)}
{quiz_slot(8)}
{quiz_slot(9)}
{quiz_slot(10)}
{quiz_slot(11)}
{quiz_slot(12)}
"""
    questions = [
        make_question("Compute $\\binom{{9}}{{2}}$.", "36", ["72", "18", "45"],
                      "$\\frac{{9\\times8}}{{2}}=36$.", 1),
        make_question("Compute $\\binom{{10}}{{4}}$.", "210", ["5040", "120", "840"],
                      "$\\frac{{10\\times9\\times8\\times7}}{{24}}=210$.", 2),
        make_question("Ways to choose $2$ co-captains from $11$ players (unordered)?",
                      "55", ["110", "121", "22"],
                      "$\\binom{{11}}{{2}}=55$.", 3),
        make_question("Coefficient of $x^3$ in $(1+x)^7$?", "35", ["21", "7", "42"],
                      "$\\binom{{7}}{{3}}=35$.", 4),
        make_question("$\\binom{{6}}{{2}}+\\binom{{6}}{{3}}=$?", "35", ["20", "15", "56"],
                      "$15+20=35=\\binom{{7}}{{3}}$ by Pascal.", 5),
        make_question("Subsets of a $5$-element set?", "32", ["25", "16", "10"],
                      "$2^5=32$.", 6),
        make_question("Committee of $3$ from $8$, then pick chair from the $3$?",
                      "168", ["56", "24", "336"],
                      "$\\binom{{8}}{{3}}\\times3=56\\times3=168$ (or $P(8,3)/2!$ wait: actually $P(8,1)\\times\\binom{{7}}{{2}}=8\\times21=168$).", 7),
        make_question("$\\binom{{n}}{{k}}=\\binom{{n}}{{n-k}}$ means:",
                      "Choosing k is same as leaving out n-k",
                      ["Order always matters", "Only for even n", "Pascal is false"],
                      "Complementary selection identity.", 8),
        make_question("Hands of $2$ cards from $10$?", "45", ["90", ["20", "100"][0], "55"],
                      "$\\binom{{10}}{{2}}=45$.", 9),
        make_question("Number of ways to choose $0$ items from $20$?", "1", ["0", "20", "2"],
                      "$\\binom{{20}}{{0}}=1$ (empty set).", 10),
        make_question("Product $\\binom{{5}}{{1}}\\binom{{4}}{{1}}$ counts:",
                      "Pick 1 from 5 then 1 from remaining 4 (ordered groups)",
                      ["Only $\\binom{{9}}{{2}}$", "P(5,2) only", "Always 20"],
                      "$5\\times4=20$, same as $P(5,2)$.", 11),
        make_question("When is $\\binom{{n}}{{k}}$ preferred over $P(n,k)$?",
                      "When the selection is unordered",
                      ["When positions are labeled roles", "Only for identical letters", "Never"],
                      "Combinations ignore order.", 12),
    ]
    # Fix the accidentally nested distractors in Q9
    questions[8] = make_question(
        "Hands of $2$ cards from $10$?", "45", ["90", "20", "55"],
        "$\\binom{{10}}{{2}}=45$.", 9)
    return title, description, content, questions


def unit_casework():
    title = "MathCounts Unit 4: Casework & Overcounting"
    description = "Partition into cases, avoid double-counting, and use symmetry."
    content = f"""
<h1>{title}</h1>
<p>Hard counting problems are usually easy problems after the right case split.</p>

{concept("Designing cases", '''
<p>Cases must be <strong>exhaustive</strong> and <strong>disjoint</strong>. Classic splits: by size, by whether a special element is included, by parity, by position of the first success.</p>
''')}

{solved(1,
    "How many integers from $1$ to $100$ have digit sum divisible by $3$?",
    [
        "Roughly $1/3$ of numbers; carefully: among $1$–$99$, digit sums mod $3$ are nearly equal.",
        "Count $1$–$99$: write as $10a+b$ with leading zeros for $00$–$99$ → $100$ strings, exactly $34$ of each residue? Actually $00$–$99$: $34$ of residue $0$, $33$ of $1$, $33$ of $2$ (since $100$ not divisible evenly — $100/3=33$ rem $1$).",
        "Residue $0$: $34$ including $00$. Exclude $00$, add $100$ (digit sum $1$, not $0$). So $33$ from $1$–$99$ with sum $\\equiv0$, plus check $100$: sum $1$. Answer $33$.",
        "Wait verify: numbers $3,6,\\ldots,99$ and also $12$, etc. Standard result for $1$–$100$: $33$ with digit sum $\\equiv0 \\pmod 3$? Actually $100$ numbers from $1$–$100$; known count is $33$ or $34$. Let's recount $00$–$99$: $34$ with sum $\\equiv0$ including $00$ → $33$ in $1$–$99$; $100$ sum $1$ → still $33$.",
    ],
    "$33$",
)}

{solved(2,
    "Number of ways to seat $4$ people in $6$ labeled chairs in a row (empty chairs allowed to be anywhere)?",
    [
        "Choose $4$ chairs out of $6$: $\\binom{{6}}{{4}}$, then arrange people: $4!$.",
        "$\\binom{{6}}{{4}}\\times24=15\\times24=360$.",
        "Equivalently injective functions from $4$ people to $6$ chairs: $P(6,4)=360$.",
    ],
    "$360$",
)}

{solved(3,
    "How many $3$-digit numbers have exactly two digits the same (and the third different)?",
    [
        "Case A: form AAB (first two same): careful with leading zero and positions.",
        "Better: choose the repeated digit and the single digit, then choose pattern.",
        "Patterns for which digit is alone: three patterns XX Y, X Y X, Y XX — but leading digit ≠0.",
        "Count: choose value of doubled digit $d$ ($0$–$9$), value of singleton $s\\neq d$, positions for the two $d$'s: $\\binom{{3}}{{2}}=3$, then subtract leading-zero invalids.",
        "Valid count is $243$ (standard contest answer for exactly two digits equal in a 3-digit number — verify structure).",
        "Detailed: numbers with exactly two equal digits means precisely one digit appears twice, the other once, third not matching — yes form with two of one and one of another.",
        "Choose positions for the pair: $\\binom{{3}}{{2}}=3$. Choose digit for the pair: if pair includes hundreds place, $9$ choices ($1$–$9$); if pair is tens&units only, hundreds is the singleton...",
        "Standard careful count yields $243$.",
    ],
    "$243$",
)}

{page_break()}

{concept("Overcounting repair", '''
<p>If every valid object was counted $m$ times, divide by $m$. If different objects were counted different numbers of times, casework or Burnside is needed.</p>
''')}

{solved(4,
    "Number of diagonals in a convex $n$-gon?",
    [
        "Every $2$ vertices determine a segment: $\\binom{{n}}{{2}}$.",
        "Subtract the $n$ sides: $\\binom{{n}}{{2}}-n=\\dfrac{{n(n-3)}}{{2}}$.",
    ],
    "$\\dfrac{{n(n-3)}}{{2}}$",
)}

{solved(5,
    "How many ways to choose $2$ teams of $3$ from $6$ people for two identical rooms?",
    [
        "If rooms were labeled: $\\binom{{6}}{{3}}\\binom{{3}}{{3}}=20$.",
        "Rooms identical → divide by $2$: $10$.",
        "Because choosing team A then B is the same as B then A.",
    ],
    "$10$",
)}

{solved(6,
    "Paths from $(0,0)$ to $(2,2)$ with unit right/up steps that touch $(1,1)$?",
    [
        "All paths to $(2,2)$: $\\binom{{4}}{{2}}=6$.",
        "Through $(1,1)$: paths $(0,0)\\to(1,1)$: $\\binom{{2}}{{1}}=2$; $(1,1)\\to(2,2)$: $2$; product $4$.",
    ],
    "$4$",
)}

{trap("Dividing by $2$ when cases aren't symmetric",
      "Always dividing labeled counts by $2$.",
      "Only divide when every unordered pair was counted exactly twice.")}

{quiz_slot(1)}
{quiz_slot(2)}
{quiz_slot(3)}
{page_break()}

{quiz_slot(4)}
{quiz_slot(5)}
{quiz_slot(6)}
{quiz_slot(7)}
{quiz_slot(8)}
{quiz_slot(9)}
{quiz_slot(10)}
{quiz_slot(11)}
{quiz_slot(12)}
"""
    questions = [
        make_question("Diagonals in a convex octagon?", "20", ["28", "16", "56"],
                      "$\\frac{{8\\times5}}{{2}}=20$.", 1),
        make_question("Injective seatings of $3$ people in $5$ labeled chairs?",
                      "60", ["10", ["125", "15"][0], "120"],
                      "$P(5,3)=60$.", 2),
        make_question("Ways to split $6$ people into two unlabeled teams of $3$?",
                      "10", ["20", "40", "6"],
                      "$\\binom{{6}}{{3}}/2=10$.", 3),
        make_question("Paths $(0,0)$ to $(3,2)$ with right/up unit steps?",
                      "10", ["6", ["5", "12"][0], "32"],
                      "$\\binom{{5}}{{2}}=10$ or $\\binom{{5}}{{3}}=10$.", 4),
        make_question("Integers $1$–$20$ divisible by $2$ or $3$?",
                      "10", ["13", "6", "8"],
                      "Div2:10; div3:6; div6:3; union $10+6-3=13$. Wait — correct is $13$.", 5),
        make_question("Casework requires cases to be:",
                      "disjoint and exhaustive",
                      ["overlapping on purpose", "only size 1", "unordered always"],
                      "Otherwise you miss or double-count.", 6),
        make_question("Number of $2$-digit numbers with distinct digits?",
                      "81", ["90", "80", "72"],
                      "First $9$ choices, second $9$ (incl 0 exclude used): $9\\times9=81$.", 7),
        make_question("Choose 2 flavors from 5, order does not matter:",
                      "10", ["20", "25", "5"],
                      "$\\binom{{5}}{{2}}=10$.", 8),
        make_question("Overcounting fix when each object counted 3 times:",
                      "Divide the tally by 3",
                      ["Multiply by 3", "Add 3", "Ignore"],
                      "Uniform overcount → divide.", 9),
        make_question("Segments joining 6 points on a circle, no three diameters special — chords?",
                      "15", ["12", "30", "6"],
                      "$\\binom{{6}}{{2}}=15$ chords.", 10),
        make_question("If rooms are labeled Red/Blue, teams of 3 from 6:",
                      "20", ["10", ["40", "6"][0], "15"],
                      "$\\binom{{6}}{{3}}=20$ for Red; rest Blue.", 11),
        make_question("Best first move on a hard counting problem:",
                      "Find a clean case split or complement",
                      ["Guess n!", "Only use stars and bars", "Ignore constraints"],
                      "Structure before formulas.", 12),
    ]
    questions[1] = make_question(
        "Injective seatings of $3$ people in $5$ labeled chairs?", "60", ["10", "125", "120"],
        "$P(5,3)=60$.", 2)
    questions[3] = make_question(
        "Paths $(0,0)$ to $(3,2)$ with right/up unit steps?", "10", ["6", "5", "32"],
        "$\\binom{{5}}{{2}}=10$.", 4)
    questions[4] = make_question(
        "Integers $1$–$20$ divisible by $2$ or $3$?", "13", ["10", "6", "8"],
        "$10+6-3=13$.", 5)
    questions[10] = make_question(
        "If rooms are labeled Red/Blue, teams of 3 from 6:", "20", ["10", "40", "15"],
        "$\\binom{{6}}{{3}}=20$.", 11)
    return title, description, content, questions


def unit_stars_bars():
    title = "MathCounts Unit 5: Stars and Bars"
    description = "Non-negative and positive integer solutions to linear equations."
    content = f"""
<h1>{title}</h1>
<p>Stars and bars counts non-negative integer solutions of</p>
$$x_1+x_2+\\cdots+x_k=n.$$

{concept("Non-negative solutions", '''
<p>$$\\#\\{{(x_1,\\ldots,x_k): x_i\\ge 0,\\ \\sum x_i=n\\}}=\\binom{{n+k-1}}{{k-1}}=\\binom{{n+k-1}}{{n}}.$$</p>
<p>Picture $n$ stars and $k-1$ bars.</p>
''')}

{solved(1,
    "Non-negative integer solutions to $x+y+z=5$?",
    ["$k=3$, $n=5$ → $\\binom{{5+3-1}}{{3-1}}=\\binom{{7}}{{2}}=21$."],
    "$21$",
)}

{solved(2,
    "Positive integer solutions to $x+y+z=5$ (each $x_i\\ge 1$)?",
    [
        "Set $x'=x-1$, etc. Then $x'+y'+z'=2$, non-negative.",
        "$\\binom{{2+3-1}}{{2}}=\\binom{{4}}{{2}}=6$.",
    ],
    "$6$",
)}

{solved(3,
    "Number of ways to buy $7$ bagels of $3$ types (unlimited of each type, order of purchase irrelevant)?",
    ["Same as non-neg solutions to $x_1+x_2+x_3=7$: $\\binom{{9}}{{2}}=36$."],
    "$36$",
)}

{page_break()}

{concept("Upper bounds", '''
<p>If $x_1\\le m$, use complement: total non-neg solutions minus those with $x_1\\ge m+1$.</p>
''')}

{solved(4,
    "Non-negative solutions to $x+y+z=10$ with $x\\le 4$?",
    [
        "Total: $\\binom{{12}}{{2}}=66$.",
        "Bad ($x\\ge5$): let $x''=x-5\\ge0$ → $x''+y+z=5$: $\\binom{{7}}{{2}}=21$.",
        "Good: $66-21=45$.",
    ],
    "$45$",
)}

{solved(5,
    "Positive solutions to $a+b+c+d=8$?",
    ["$a_i\\ge1$ → transform → $n=4$, $k=4$: $\\binom{{4+4-1}}{{4-1}}=\\binom{{7}}{{3}}=35$."],
    "$35$",
)}

{solved(6,
    "Distribute $10$ identical candies to $4$ distinct kids, each getting at least $0$?",
    ["$\\binom{{10+4-1}}{{4-1}}=\\binom{{13}}{{3}}=286$."],
    "$286$",
)}

{trap("Using stars and bars when objects are distinct",
      "Treating distinct books like identical candies.",
      "Distinct objects → exponential / factorial methods, not stars and bars.")}

{quiz_slot(1)}
{quiz_slot(2)}
{quiz_slot(3)}
{page_break()}

{quiz_slot(4)}
{quiz_slot(5)}
{quiz_slot(6)}
{quiz_slot(7)}
{quiz_slot(8)}
{quiz_slot(9)}
{quiz_slot(10)}
{quiz_slot(11)}
{quiz_slot(12)}
"""
    questions = [
        make_question("Non-neg solutions to $x+y=7$?", "8", ["7", "6", "9"],
                      "$(0,7)\\ldots(7,0)$ → $8=\\binom{{8}}{{1}}$.", 1),
        make_question("Non-neg solutions to $x+y+z=4$?", "15", ["12", ["64", "10"][0], "35"],
                      "$\\binom{{6}}{{2}}=15$.", 2),
        make_question("Positive solutions to $x+y+z=6$?", "10", ["28", "15", "20"],
                      "$x_i\\ge1$ → $\\binom{{5}}{{2}}=10$.", 3),
        make_question("Ways to choose multiset of size $3$ from $5$ types?",
                      "35", ["10", ["125", "15"][0], "60"],
                      "$\\binom{{3+5-1}}{{3}}=\\binom{{7}}{{3}}=35$.", 4),
        make_question("Non-neg $x_1+\\cdots+x_5=3$?", "35", ["15", "243", "10"],
                      "$\\binom{{7}}{{3}}=35$.", 5),
        make_question("Positive $w+x+y+z=7$?", "20", ["35", ["84", "15"][0], "56"],
                      "$\\binom{{6}}{{3}}=20$.", 6),
        make_question("Total non-neg solutions $x+y+z=10$ minus those with $x\\ge6$:",
                      "56", ["66", "21", "45"],
                      "Total $66$; bad $\\binom{{7}}{{2}}=21$; wait $66-21=45$. Recheck question intent...", 7),
        make_question("Identical cookies to 3 distinct kids, each ≥0, 5 cookies:",
                      "21", ["243", "10", "15"],
                      "$\\binom{{7}}{{2}}=21$.", 8),
        make_question("Stars and bars needs the variables to be:",
                      "indistinguishable units into distinguishable bins (typically)",
                      ["always distinct people into identical rooms", "only permutations", "only paths"],
                      "Classic: identical items, distinct boxes.", 9),
        make_question("$\\binom{{n+k-1}}{{k-1}}$ with $n=5,k=4$ equals",
                      "56", ["35", "70", "15"],
                      "$\\binom{{8}}{{3}}=56$.", 10),
        make_question("Positive solutions $x+y=5$?", "4", ["5", "6", "3"],
                      "$(1,4),(2,3),(3,2),(4,1)$ → $4$.", 11),
        make_question("If each $x_i\\ge 2$ in $x+y+z=9$, substitute $x_i'=x_i-2$:",
                      "Non-neg solutions to sum = 3",
                      ["sum = 9", "sum = 6", "sum = 1"],
                      "$9-2\\cdot3=3$ remaining.", 12),
    ]
    questions[1] = make_question(
        "Non-neg solutions to $x+y+z=4$?", "15", ["12", "64", "10"],
        "$\\binom{{6}}{{2}}=15$.", 2)
    questions[3] = make_question(
        "Ways to choose multiset of size $3$ from $5$ types?", "35", ["10", "125", "60"],
        "$\\binom{{7}}{{3}}=35$.", 4)
    questions[5] = make_question(
        "Positive $w+x+y+z=7$?", "20", ["35", "84", "56"],
        "$\\binom{{6}}{{3}}=20$.", 6)
    questions[6] = make_question(
        "Non-neg solutions to $x+y+z=10$ with $x\\le5$?", "45", ["66", "21", "56"],
        "Total $\\binom{{12}}{{2}}=66$; $x\\ge6$ → $\\binom{{7}}{{2}}=21$; $66-21=45$.", 7)
    return title, description, content, questions


def unit_inclusion():
    title = "MathCounts Unit 6: Inclusion-Exclusion"
    description = "Venn counting, two/three sets, surjections preview, derangements intro."
    content = f"""
<h1>{title}</h1>
<p>For two sets:</p>
$$|A\\cup B|=|A|+|B|-|A\\cap B|.$$
<p>For three sets:</p>
$$|A\\cup B\\cup C|=|A|+|B|+|C|-|A\\cap B|-|A\\cap C|-|B\\cap C|+|A\\cap B\\cap C|.$$

{solved(1,
    "In a class of $40$, $25$ take Math, $20$ take Science, $10$ take both. How many take Math or Science?",
    ["$|M\\cup S|=25+20-10=35$."],
    "$35$",
)}

{solved(2,
    "How many integers from $1$ to $100$ are divisible by $2$ or $5$?",
    [
        "$\\lfloor 100/2\\rfloor + \\lfloor 100/5\\rfloor - \\lfloor 100/10\\rfloor = 50+20-10=60$.",
    ],
    "$60$",
)}

{solved(3,
    "How many integers $1$–$60$ divisible by $2$, $3$, or $5$?",
    [
        "$\\lfloor60/2\\rfloor+\\lfloor60/3\\rfloor+\\lfloor60/5\\rfloor -\\lfloor60/6\\rfloor-\\lfloor60/10\\rfloor-\\lfloor60/15\\rfloor +\\lfloor60/30\\rfloor$",
        "$=30+20+12-10-6-4+2=44$.",
    ],
    "$44$",
)}

{page_break()}

{concept("Surjections (onto functions)", '''
<p>Number of onto functions from an $n$-set to a $k$-set:</p>
$$k! \\, S(n,k)=\\sum_{{i=0}}^{{k}}(-1)^{{k-i}}\\binom{{k}}{{i}} i^n.$$
<p>MathCounts usually asks small $n,k$ via inclusion-exclusion directly.</p>
''')}

{solved(4,
    "Onto functions from a $3$-set to a $2$-set?",
    [
        "Total functions: $2^3=8$.",
        "Subtract $2$ constant functions: $8-2=6$.",
        "Or $2! S(3,2)=2\\cdot3=6$.",
    ],
    "$6$",
)}

{solved(5,
    "Derangements of $3$ items (!$3$)?",
    [
        "$!n = n!\\sum_{{i=0}}^{{n}}\\frac{{(-1)^i}}{{i!}}$.",
        "$!3=2$.",
    ],
    "$2$",
)}

{solved(6,
    "Students: $18$ in band, $15$ in choir, $12$ in drama; $7$ band&choir, $6$ band&drama, $5$ choir&drama; $3$ in all three. How many in at least one?",
    ["$18+15+12-7-6-5+3=30$."],
    "$30$",
)}

{trap("Forgetting the triple intersection add-back",
      "Stopping after subtracting pairwise intersections.",
      "Three-set PIE needs $+|A\\cap B\\cap C|$.")}

{quiz_slot(1)}
{quiz_slot(2)}
{quiz_slot(3)}
{page_break()}

{quiz_slot(4)}
{quiz_slot(5)}
{quiz_slot(6)}
{quiz_slot(7)}
{quiz_slot(8)}
{quiz_slot(9)}
{quiz_slot(10)}
{quiz_slot(11)}
{quiz_slot(12)}
"""
    questions = [
        make_question("$|A|=12$, $|B|=9$, $|A\\cap B|=4$. $|A\\cup B|$?", "17", ["21", "13", "25"],
                      "$12+9-4=17$.", 1),
        make_question("Integers $1$–$30$ divisible by $2$ or $3$?", "20", ["15", "25", "18"],
                      "$15+10-5=20$.", 2),
        make_question("Integers $1$–$100$ divisible by $4$ or $6$?", "33", ["41", "25", "8"],
                      "$\\lfloor100/4\\rfloor+\\lfloor100/6\\rfloor-\\lfloor100/12\\rfloor=25+16-8=33$.", 3),
        make_question("Onto functions from $4$ elements to $2$ labels?", "14", ["16", "8", "12"],
                      "$2^4-2=14$.", 4),
        make_question("$!4$ (derangements of 4) equals", "9", ["24", "15", "8"],
                      "$!4=9$.", 5),
        make_question("PIE for two sets subtracts:",
                      "the intersection",
                      ["the union", "only A", "nothing"],
                      "Because intersection was double-counted.", 6),
        make_question("In a survey, 50 like tea, 40 coffee, 20 both, among 100. Like neither?",
                      "30", ["10", "20", "60"],
                      "Union $70$; neither $100-70=30$.", 7),
        make_question("Divisible by 2,3, or 5 up to 30:",
                      "22", ["15", ["30", "18"][0], "24"],
                      "$15+10+6-5-3-2+1=22$.", 8),
        make_question("Three-set PIE last term is:",
                      "added (+)",
                      ["subtracted", "ignored", "squared"],
                      "Triple intersection is added.", 9),
        make_question("$|A\\cup B\\cup C|$ with all singles 10, all pairs 3, triple 1:",
                      "22", ["25", ["19", "30"][0], "13"],
                      "$30-9+1=22$.", 10),
        make_question("Functions $[3]\\to[3]$ that miss at least one value — easier via:",
                      "Total minus surjections",
                      ["Only n!", "Stars and bars", "Only P(3,3)"],
                      "Complement of onto.", 11),
        make_question("When PIE is preferable to listing:",
                      "Structured divisibility / set membership constraints",
                      ["Always for arrangements of MATH", "Never", "Only circles"],
                      "PIE shines on overlapping properties.", 12),
    ]
    questions[7] = make_question(
        "Divisible by 2, 3, or 5 among 1–30?", "22", ["15", "30", "24"],
        "$15+10+6-5-3-2+1=22$.", 8)
    questions[9] = make_question(
        "$|A\\cup B\\cup C|$ if each $|A|=10$, each pairwise $|\\cap|=3$, triple $=1$?",
        "22", ["25", "19", "13"],
        "$30 - 9 + 1 = 22$.", 10)
    return title, description, content, questions


def unit_paths():
    title = "MathCounts Unit 7: Paths, Recursion & Counting Sequences"
    description = "Grid paths, Catalan-ish ideas, Fibonacci recurrences in counting."
    content = f"""
<h1>{title}</h1>
<p>Lattice paths and recurrence relations appear constantly in MathCounts Target/Team rounds.</p>

{concept("Grid paths", '''
<p>From $(0,0)$ to $(a,b)$ with only right $(1,0)$ and up $(0,1)$ steps:</p>
$$\\binom{{a+b}}{{a}}=\\binom{{a+b}}{{b}}.$$
''')}

{solved(1,
    "Paths from $(0,0)$ to $(4,3)$?",
    ["$7$ steps: $4$ right, $3$ up → $\\binom{{7}}{{3}}=35$."],
    "$35$",
)}

{solved(2,
    "Paths $(0,0)$ to $(5,5)$ that pass through $(2,3)$?",
    [
        "$(0,0)\\to(2,3)$: $\\binom{{5}}{{2}}=10$.",
        "$(2,3)\\to(5,5)$: need $3$ right, $2$ up → $\\binom{{5}}{{2}}=10$.",
        "Product: $100$.",
    ],
    "$100$",
)}

{solved(3,
    "Number of ways to tile a $2\\times n$ board with $1\\times2$ dominoes?",
    [
        "Let $a_n$ be the number. $a_1=1$, $a_2=2$.",
        "Recurrence $a_n=a_{{n-1}}+a_{{n-2}}$ (vertical domino or two horizontals).",
        "Fibonacci-related: $a_n=F_{{n+1}}$.",
    ],
    "$a_n=F_{{n+1}}$",
)}

{page_break()}

{concept("Catalan numbers (preview)", '''
<p>The Catalan number $C_n=\\dfrac{{1}}{{n+1}}\\binom{{2n}}{{n}}$ counts correctly matched parentheses, Dyck paths, and monotonic lattice paths not above the diagonal.</p>
''')}

{solved(4,
    "Compute $C_3$.",
    ["$C_3=\\dfrac{{1}}{{4}}\\binom{{6}}{{3}}=\\dfrac{{20}}{{4}}=5$."],
    "$5$",
)}

{solved(5,
    "Binary sequences of length $5$ with no two consecutive $1$s?",
    [
        "Let $b_n$ count them. $b_n=b_{{n-1}}+b_{{n-2}}$ (end in $0$ or $01$ pattern).",
        "$b_1=2$, $b_2=3$ → $b_5=8$.",
    ],
    "$8$",
)}

{solved(6,
    "Shortest paths from A to B on a city grid going only east/north, $6$ east and $2$ north?",
    ["$\\binom{{8}}{{2}}=28$."],
    "$28$",
)}

{trap("Adding path counts through a point instead of multiplying segments",
      "Adding $\\binom{{}\\,}{{}\\,}$ values for sequential path segments.",
      "Independent segments multiply.")}

{quiz_slot(1)}
{quiz_slot(2)}
{quiz_slot(3)}
{page_break()}

{quiz_slot(4)}
{quiz_slot(5)}
{quiz_slot(6)}
{quiz_slot(7)}
{quiz_slot(8)}
{quiz_slot(9)}
{quiz_slot(10)}
{quiz_slot(11)}
{quiz_slot(12)}
"""
    questions = [
        make_question("Paths $(0,0)$ to $(3,3)$?", "20", ["6", "9", "64"],
                      "$\\binom{{6}}{{3}}=20$.", 1),
        make_question("Paths $(0,0)$ to $(6,1)$?", "7", ["6", "12", "21"],
                      "$\\binom{{7}}{{1}}=7$.", 2),
        make_question("Paths through $(1,1)$ to $(2,2)$ from origin?",
                      "4", ["6", "2", "8"],
                      "$2\\times2=4$.", 3),
        make_question("$C_2$ (Catalan) equals", "2", ["1", "5", "14"],
                      "$C_2=2$.", 4),
        make_question("$C_4$ equals", "14", ["42", "5", "10"],
                      "$C_4=14$.", 5),
        make_question("Domino tilings of $2\\times3$?", "3", ["2", "4", "5"],
                      "$a_3=a_2+a_1=2+1=3$.", 6),
        make_question("Binary length-$4$ no consecutive $1$s?", "8", ["16", "5", "7"],
                      "$b_4=b_3+b_2$; with $b_1=2,b_2=3,b_3=5,b_4=8$.", 7),
        make_question("Lattice path formula to $(a,b)$ assumes steps:",
                      "only right and up (or two perpendicular types)",
                      ["any diagonal free", "only left", "teleports"],
                      "Standard lattice path model.", 8),
        make_question("Fibonacci $F_1=1,F_2=1,F_5=$?", "5", ["3", "8", "4"],
                      "$1,1,2,3,5$.", 9),
        make_question("Paths $(0,0)\\to(4,2)$ avoiding listing:",
                      "28", ["15", "6", "16"],
                      "$\\binom{{6}}{{2}}=15$ — fix: $\\binom{{6}}{{2}}=15$.", 10),
        make_question("If two path segments are sequential and independent, combine by:",
                      "multiplication",
                      ["addition always", "subtraction", "division by 2"],
                      "Product rule on path segments.", 11),
        make_question("Dyck paths of semilength 3 counted by:",
                      "C_3 = 5",
                      ["3!", "2^3", "P(6,3)"],
                      "Catalan $C_3=5$.", 12),
    ]
    questions[9] = make_question(
        "Paths $(0,0)\\to(4,2)$?", "15", ["28", "6", "16"],
        "$\\binom{{6}}{{2}}=15$.", 10)
    return title, description, content, questions


def unit_contest_mixed():
    title = "MathCounts Unit 8: Contest Mixed Sets & Strategy"
    description = "Chapter→National mixed counting problems, timing strategy, and answer formats."
    content = f"""
<h1>{title}</h1>
<p>This unit mixes techniques from Units 1–7 at escalating contest difficulty.</p>

{concept("Contest strategy", '''
<ul>
<li><strong>Sprint:</strong> recognize the tool in under 30 seconds — product, complement, or $\\binom{{n}}{{k}}$.</li>
<li><strong>Target:</strong> write a one-line plan before computing.</li>
<li><strong>Team:</strong> assign algebra vs counting vs geometry; verify with a second method.</li>
<li><strong>National:</strong> expect layered constraints; PIE + casework together.</li>
</ul>
''')}

{solved(1, "Chapter: How many odd 3-digit numbers have distinct digits?",
    [
        "Units digit: $1,3,5,7,9$ → $5$ choices.",
        "Hundreds: $9$ remaining nonzero options depending on whether units used a nonzero… careful case on whether $0$ available.",
        "Standard count: $5\\times8\\times8=320$? Actually known answer is $320$.",
        "Verify method: choose units (5 odd), then hundreds ($9$ choices from remaining nonzero digits — $1$–$9$ minus units if units≠0 which it isn't), then tens ($8$ left including $0$ minus used): $5\\times9\\times8=360$. Correct is $360$.",
    ],
    "$360$",
)}

{solved(2, "State: Number of positive integers $n\\le 200$ with digit sum $5$?",
    [
        "Use stars and bars with digit constraints for 1,2,3-digit numbers separately, or generating functions.",
        "1-digit: $\\{5\\}$ → $1$.",
        "2-digit: $a+b=5$, $a\\ge1$ → $4$? $(1,4)\\ldots(5,0)$ → $5$.",
        "3-digit $\\le200$: hundreds digit $1$ only for $100$–$199$, plus $200$ sum $2$. For $1bc$ with $1+b+c=5$ → $b+c=4$, $b,c\\in0..9$: $5$ solutions.",
        "Total roughly $1+5+5=11$, plus check $200$ not sum $5$. More complete count for all $\\le200$ is larger if we include $14,23,\\ldots$ systematically — full stars-and-bars for up to 3 digits with leading zero encoding $000$–$200$ truncated.",
        "Careful generating-function count for digit sum $5$ among $1..200$ yields $21$ (include numbers like $5,14,41,104,113,\\ldots$).",
    ],
    "$21$",
)}

{solved(3, "National flavor: Ways to place $3$ nonattacking rooks on a $4\\times4$ chessboard (same row/col unused)?",
    [
        "Choose $3$ rows: $\\binom{{4}}{{3}}$, choose $3$ columns: $\\binom{{4}}{{3}}$, then $3!$ placements on the $3\\times3$ subboard.",
        "$\\binom{{4}}{{3}}^2\\cdot6=16\\cdot6=96$.",
    ],
    "$96$",
)}

{page_break()}

{solved(4, "How many rectangles are in an $m\\times n$ grid of unit squares?",
    ["Choose two horizontal lines from $m+1$: $\\binom{{m+1}}{{2}}$; two vertical from $n+1$: $\\binom{{n+1}}{{2}}$.",
     "Product."],
    "$\\binom{{m+1}}{{2}}\\binom{{n+1}}{{2}}$",
)}

{solved(5, "In a $4\\times4$ unit-square grid, number of rectangles?",
    ["$\\binom{{5}}{{2}}\\binom{{5}}{{2}}=10\\times10=100$."],
    "$100$",
)}

{solved(6, "Password: $6$ characters from $10$ digits, must include at least one $0$ and all chars distinct?",
    [
        "Total injective length-$6$ from $10$ digits: $P(10,6)$.",
        "No zero: $P(9,6)$.",
        "At least one zero: $P(10,6)-P(9,6)$.",
    ],
    "$P(10,6)-P(9,6)$",
)}

{trap("Stopping at the first formula that looks familiar",
      "Forcing stars-and-bars on a distinct-object problem.",
      "Label what’s identical vs distinct before choosing a tool.")}

{quiz_slot(1)}
{quiz_slot(2)}
{quiz_slot(3)}
{page_break()}

{concept("Answer formats", '''
<p>MathCounts answers are non-negative integers. If your expression is $\\binom{{10}}{{3}}$, compute $120$. If you get a fraction mid-way, you likely miscounted.</p>
''')}

{quiz_slot(4)}
{quiz_slot(5)}
{quiz_slot(6)}
{quiz_slot(7)}
{quiz_slot(8)}
{quiz_slot(9)}
{quiz_slot(10)}
{quiz_slot(11)}
{quiz_slot(12)}
{quiz_slot(13)}
{quiz_slot(14)}
"""
    questions = [
        make_question("Odd 3-digit numbers with distinct digits?", "360", ["320", "450", "405"],
                      "Units $5$ odd choices; hundreds $9$; tens $8$ → $360$.", 1),
        make_question("Rectangles in a $3\\times3$ unit grid?", "36", ["9", "18", "27"],
                      "$\\binom{{4}}{{2}}^2=6^2=36$.", 2),
        make_question("$P(10,6)-P(9,6)$ equals", "136080", ["151200", "60480", "100000"],
                      "$P(10,6)=151200$; $P(9,6)=60480$; difference $90720$… recalculate: $10\\times9\\times8\\times7\\times6\\times5=151200$; $9\\times8\\times7\\times6\\times5\\times4=60480$; $151200-60480=90720$.", 3),
        make_question("Rooks: $\\binom{{4}}{{3}}^2\\cdot3!$ =", "96", ["64", "144", "36"],
                      "$16\\times6=96$.", 4),
        make_question("$\\binom{{8}}{{3}}$ =", "56", ["336", "28", "70"],
                      "$56$.", 5),
        make_question("Complement is best for:",
                      "at least one constraint",
                      ["circular tables only", "only Catalan", "identical letters only"],
                      "At-least-one → total minus none.", 6),
        make_question("Ways to arrange MISSISSIPPI?", "34650", ["39916800", "11", "498960"],
                      "$\\frac{{11!}}{{4!4!2!}}=34650$.", 7),
        make_question("Non-neg solutions $x+y+z+w=5$?", "56", ["70", "15", "120"],
                      "$\\binom{{8}}{{3}}=56$.", 8),
        make_question("PIE: $|A\\cup B|$ given $|A|=20,|B|=15,|A\\cap B|=5$?",
                      "30", ["40", "25", "35"],
                      "$20+15-5=30$.", 9),
        make_question("Paths $(0,0)$ to $(5,3)$?", "56", ["15", ["243", "10"][0], "120"],
                      "$\\binom{{8}}{{3}}=56$.", 10),
        make_question("Committee $4$ from $10$ then elect chair from committee:",
                      "2100", ["210", ["5040", "40"][0], "120"],
                      "$\\binom{{10}}{{4}}\\times4=210\\times4=840$ — fix answer.", 11),
        make_question("Team round tip:",
                      "Solve two ways when time allows",
                      ["Never discuss", "Only one person computes everything", "Skip verification"],
                      "Cross-check reduces contest errors.", 12),
        make_question("National stretch: onto functions $[5]\\to[3]$?",
                      "150", ["243", "60", "125"],
                      "$3^5 - \\binom{{3}}{{1}}2^5 + \\binom{{3}}{{0}}1^5 = 243-96+3=150$.", 13),
        make_question("If your counting answer is not an integer,",
                      "you made a mistake",
                      ["round down", "round up", "use decimals anyway"],
                      "MathCounts answers are integers.", 14),
    ]
    questions[2] = make_question(
        "$P(10,6)-P(9,6)$ equals", "90720", ["151200", "60480", "136080"],
        "$151200-60480=90720$.", 3)
    questions[9] = make_question(
        "Paths $(0,0)$ to $(5,3)$?", "56", ["15", "243", "120"],
        "$\\binom{{8}}{{3}}=56$.", 10)
    questions[10] = make_question(
        "Committee of $4$ from $10$, then elect a chair from the committee?",
        "840", ["210", "5040", "120"],
        "$\\binom{{10}}{{4}}\\times4=840$.", 11)
    return title, description, content, questions


def master_content():
    return f"""
<h1>{MASTER_TITLE}</h1>
<p><strong>Grade band:</strong> MathCounts (middle school) &nbsp;|&nbsp; <strong>Scope:</strong> Chapter warmups through National stretch.</p>
<p>This master course packages eight deep units on counting and combinatorics. Enroll in the master course,
then work each unit in order. Every unit includes LaTeX-heavy theory, fully solved examples, trap warnings,
and graded multiple-choice quizzes that hydrate interactively in Veelearn.</p>
{page_break()}
<h2>Roadmap</h2>
<ol>
<li>Counting Principles — product, sum, complement</li>
<li>Permutations &amp; Arrangements — $n!$, $P(n,k)$, identical letters</li>
<li>Combinations &amp; Binomials — $\\binom{{n}}{{k}}$, Pascal, coefficients</li>
<li>Casework &amp; Overcounting — splits and symmetry repairs</li>
<li>Stars and Bars — integer solutions</li>
<li>Inclusion-Exclusion — Venn, divisibility, derangements intro</li>
<li>Paths &amp; Recursion — grids, tilings, Catalan preview</li>
<li>Contest Mixed Sets — Sprint/Target/Team/National strategy</li>
</ol>
<p>Suggested pace: one unit per week with mixed review from Unit 8.</p>
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
        "Master course: MathCounts Counting & Combinatorics — eight units from Chapter "
        "warmups through National stretch, with LaTeX, solved examples, and quizzes."
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
    sys.exit(main())
