#!/usr/bin/env python3
"""Inject Math Curriculum Batch 3 (Grades 9-12) into Veelearn database."""

import pymysql, json, sys, os, io, random

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

AIVEN_CONFIG = {
    "host": os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "user": "avnadmin",
    "password": os.getenv("AIVEN_PASSWORD"),
    "db": "defaultdb",
    "port": 26399,
    "ssl": {},
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

# =====================================================================
# GRADE 9: Algebra Foundations
# =====================================================================
G9_CONTENT = r"""
<h1>Grade 9 Math: Algebra Foundations</h1>
<p>Algebra is the bridge between arithmetic and advanced mathematics. Learn to manipulate symbols and solve complex problems!</p>

<hr>

<h2>Module 1: Variables & Expressions</h2>
<p>Variables represent unknown values. Expressions combine variables and constants using arithmetic operators. Simplify by combining like terms!</p>

<hr>

<h2>Module 2: Solving Equations</h2>
<p>Master the art of balancing equations. Whatever you do to one side, you MUST do to the other. Goal: Isolate the variable.</p>

<h3>Interactive Expression Exchange</h3>
<iframe src="https://phet.colorado.edu/sims/html/expression-exchange/latest/expression-exchange_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Use this game to learn how to simplify and solve algebraic expressions!</em></p>

<hr>

<h2>Module 3: Inequalities</h2>
<p>Unlike equations, inequalities represent a range of solutions. Remember the golden rule: flip the sign when multiplying or dividing by a negative number!</p>
"""

G9_QUESTIONS = [
    {"question_text": "Simplify: 3x + 5x - 2x", "question_type": "multiple_choice", "options": ["6x", "10x", "8x", "x"], "correct_answer": "6x", "explanation": "3 + 5 - 2 = 6.", "points": 1, "order_index": 1},
    {"question_text": "Solve for x: 2x + 10 = 20", "question_type": "multiple_choice", "options": ["5", "10", "15", "2"], "correct_answer": "5", "explanation": "2x = 10; x = 5.", "points": 1, "order_index": 2},
    {"question_text": "If x = 3, what is 4x^2 - 1?", "question_type": "multiple_choice", "options": ["35", "11", "23", "47"], "correct_answer": "35", "explanation": "4(9) - 1 = 36 - 1 = 35.", "points": 1, "order_index": 3},
    {"question_text": "Which property is this: a(b + c) = ab + ac?", "question_type": "multiple_choice", "options": ["Distributive", "Commutative", "Associative", "Identity"], "correct_answer": "Distributive", "explanation": "You are distributing 'a'.", "points": 1, "order_index": 4},
    {"question_text": "Solve the inequality: -2x > 10", "question_type": "multiple_choice", "options": ["x < -5", "x > -5", "x < 5", "x > 5"], "correct_answer": "x < -5", "explanation": "Divide by -2 and flip the sign.", "points": 1, "order_index": 5},
    {"question_text": "What is the degree of the expression: 4x^3 + 2x - 5?", "question_type": "multiple_choice", "options": ["3", "1", "4", "0"], "correct_answer": "3", "explanation": "The highest exponent is the degree.", "points": 1, "order_index": 6},
    {"question_text": "Combine like terms: 5y + 3x - 2y + x", "question_type": "multiple_choice", "options": ["4x + 3y", "2x + 3y", "8xy", "3x + 3y"], "correct_answer": "4x + 3y", "explanation": "3x+x = 4x; 5y-2y = 3y.", "points": 1, "order_index": 7},
    {"question_text": "Identify the coefficient in 7x^2:", "question_type": "multiple_choice", "options": ["7", "2", "x", "None"], "correct_answer": "7", "explanation": "The number in front of the variable is the coefficient.", "points": 1, "order_index": 8},
    {"question_text": "Solve: 1/2 x = 4", "question_type": "multiple_choice", "options": ["8", "2", "6", "4"], "correct_answer": "8", "explanation": "Multiply both sides by 2.", "points": 1, "order_index": 9},
    {"question_text": "What is an expression with two terms called?", "question_type": "multiple_choice", "options": ["Binomial", "Monomial", "Trinomial", "Polynomial"], "correct_answer": "Binomial", "explanation": "Bi- means two.", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 10: Trigonometry & Geometry
# =====================================================================
G10_CONTENT = r"""
<h1>Grade 10 Math: Trigonometry & Circles</h1>
<p>Explore the relationships between angles and side lengths in triangles and master the Unit Circle!</p>

<hr>

<h2>Module 1: SOH-CAH-TOA</h2>
<p>Master the basic trigonometric ratios for right triangles:</p>
<ul>
  <li>$\sin(\theta) = \text{Opposite} / \text{Hypotenuse}$</li>
  <li>$\cos(\theta) = \text{Adjacent} / \text{Hypotenuse}$</li>
  <li>$\tan(\theta) = \text{Opposite} / \text{Adjacent}$</li>
</ul>

<hr>

<h2>Module 2: The Unit Circle</h2>
<p>The **Unit Circle** has a radius of 1. It allows us to extend trigonometry to any angle, not just those in right triangles.</p>

<h3>Interactive Trig Tour</h3>
<iframe src="https://phet.colorado.edu/sims/html/trig-tour/latest/trig-tour_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Rotate the point around the circle and watch the graphs of sine and cosine update!</em></p>

<hr>

<h2>Module 3: Pythagorean Identity</h2>
<p>Discover the relationship: $\sin^2(\theta) + \cos^2(\theta) = 1$. This fundamental identity is used everywhere in advanced math!</p>
"""

G10_QUESTIONS = [
    {"question_text": "What is the ratio for Sine?", "question_type": "multiple_choice", "options": ["Opp/Hyp", "Adj/Hyp", "Opp/Adj", "Hyp/Opp"], "correct_answer": "Opp/Hyp", "explanation": "SOH: Sine = Opposite / Hypotenuse.", "points": 1, "order_index": 1},
    {"question_text": "In the Unit Circle, the x-coordinate represents:", "question_type": "multiple_choice", "options": ["Cosine", "Sine", "Tangent", "Radius"], "correct_answer": "Cosine", "explanation": "x = cos(theta) in the unit circle.", "points": 1, "order_index": 2},
    {"question_text": "What is sin(90°) or sin(pi/2)?", "question_type": "multiple_choice", "options": ["1", "0", "-1", "0.5"], "correct_answer": "1", "explanation": "At 90 degrees, the y-coordinate is the max height of 1.", "points": 1, "order_index": 3},
    {"question_text": "If cos(theta) = 0, what could theta be?", "question_type": "multiple_choice", "options": ["90°", "0°", "180°", "45°"], "correct_answer": "90°", "explanation": "Cosine is zero at the vertical axis.", "points": 1, "order_index": 4},
    {"question_text": "What is the Pythagorean Identity?", "question_type": "multiple_choice", "options": ["sin^2 + cos^2 = 1", "sin + cos = 1", "tan = 1", "a + b = c"], "correct_answer": "sin^2 + cos^2 = 1", "explanation": "Fundamental trig identity.", "points": 1, "order_index": 5},
    {"question_text": "What is the Tangent of 45°?", "question_type": "multiple_choice", "options": ["1", "0", "Undefined", "0.5"], "correct_answer": "1", "explanation": "sin(45) = cos(45), so tan(45) = 1.", "points": 1, "order_index": 6},
    {"question_text": "How many degrees are in 2*pi radians?", "question_type": "multiple_choice", "options": ["360°", "180°", "90°", "270°"], "correct_answer": "360°", "explanation": "A full circle is 2*pi radians.", "points": 1, "order_index": 7},
    {"question_text": "In a right triangle, if the adjacent side is 3 and hypotenuse is 5, what is cosine?", "question_type": "multiple_choice", "options": ["3/5", "4/5", "5/3", "1"], "correct_answer": "3/5", "explanation": "Cos = Adj / Hyp.", "points": 1, "order_index": 8},
    {"question_text": "What is the period of the standard sine function?", "question_type": "multiple_choice", "options": ["2*pi", "pi", "pi/2", "360"], "correct_answer": "2*pi", "explanation": "Sine repeats every 2*pi radians.", "points": 1, "order_index": 9},
    {"question_text": "The hypotenuse is always the ___ side.", "question_type": "multiple_choice", "options": ["Longest", "Shortest", "Vertical", "Left"], "correct_answer": "Longest", "explanation": "Opposite the right angle.", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 11: Introduction to Calculus
# =====================================================================
G11_CONTENT = r"""
<h1>Grade 11 Math: Intro to Calculus</h1>
<p>Calculus study the rate of change and the accumulation of quantities. It's the mathematics of motion and change!</p>

<hr>

<h2>Module 1: Limits</h2>
<p>A limit describes the behavior of a function as it approaches a certain value. It's the basic building block of derivatives and integrals.</p>

<hr>

<h2>Module 2: The Derivative</h2>
<p>The **Derivative** is the instantaneous rate of change (or the slope of the tangent line) of a function at a specific point.</p>

<h3>Interactive Calculus Grapher</h3>
<iframe src="https://phet.colorado.edu/sims/html/calculus-grapher/latest/calculus-grapher_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Draw a function and watch its derivative appear instantly!</em></p>

<hr>

<h2>Module 3: Integration Basics</h2>
<p>Integration is the process of finding the area under a curve. It can be thought of as the "inverse" of differentiation.</p>
"""

G11_QUESTIONS = [
    {"question_text": "What does a derivative represent?", "question_type": "multiple_choice", "options": ["Rate of change", "Total area", "The y-intercept", "The average"], "correct_answer": "Rate of change", "explanation": "Derivative = Slope = Rate of change.", "points": 1, "order_index": 1},
    {"question_text": "The derivative of a constant (like 5) is always:", "question_type": "multiple_choice", "options": ["0", "1", "5", "x"], "correct_answer": "0", "explanation": "Constants don't change, so rate of change is zero.", "points": 1, "order_index": 2},
    {"question_text": "Using the Power Rule, what is the derivative of x^2?", "question_type": "multiple_choice", "options": ["2x", "x^3", "2", "x"], "correct_answer": "2x", "explanation": "d/dx (x^n) = n*x^(n-1).", "points": 1, "order_index": 3},
    {"question_text": "What is the area under a horizontal line y = 5 from x=0 to x=2?", "question_type": "multiple_choice", "options": ["10", "5", "2", "0"], "correct_answer": "10", "explanation": "Rectangle area: 5 * 2 = 10.", "points": 1, "order_index": 4},
    {"question_text": "Integration is used to find:", "question_type": "multiple_choice", "options": ["Area under curve", "Slope", "Limit", "Zeroes"], "correct_answer": "Area under curve", "explanation": "Accumulation of quantities.", "points": 1, "order_index": 5},
    {"question_text": "What is the limit of 1/x as x goes to infinity?", "question_type": "multiple_choice", "options": ["0", "Infinity", "1", "None"], "correct_answer": "0", "explanation": "Denominator becomes huge, fraction becomes tiny.", "points": 1, "order_index": 6},
    {"question_text": "If f(x) = 3x, what is f'(x)?", "question_type": "multiple_choice", "options": ["3", "x", "3x^2", "0"], "correct_answer": "3", "explanation": "The slope of 3x is constant 3.", "points": 1, "order_index": 7},
    {"question_text": "The 'Slope of the Tangent Line' is another name for:", "question_type": "multiple_choice", "options": ["Derivative", "Integral", "Limit", "Intercept"], "correct_answer": "Derivative", "explanation": "Tangent slope = derivative.", "points": 1, "order_index": 8},
    {"question_text": "Who is credited with developing Calculus independently of Newton?", "question_type": "multiple_choice", "options": ["Leibniz", "Einstein", "Euler", "Gauss"], "correct_answer": "Leibniz", "explanation": "Gottfried Wilhelm Leibniz.", "points": 1, "order_index": 9},
    {"question_text": "What symbol is used for the Integral?", "question_type": "multiple_choice", "options": ["∫", "Σ", "Δ", "lim"], "correct_answer": "∫", "explanation": "The stylized 'S' for Sum.", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 12: Probability & Statistics
# =====================================================================
G12_CONTENT = r"""
<h1>Grade 12 Math: Probability & Stats</h1>
<p>Master the laws of chance and learn to interpret data to make predictions in a world of uncertainty!</p>

<hr>

<h2>Module 1: The Plinko Effect</h2>
<p>Understand how random choices lead to stable distributions. The **Normal Distribution** (Bell Curve) emerges from many small independent events.</p>

<h3>Interactive Plinko Probability</h3>
<iframe src="https://phet.colorado.edu/sims/html/plinko-probability/latest/plinko-probability_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Drop balls and see the histogram build toward a normal distribution!</em></p>

<hr>

<h2>Module 2: Conditional Probability</h2>
<p>Learn how the occurrence of one event affects the probability of another. Formula: $P(A|B) = P(A \cap B) / P(B)$.</p>

<hr>

<h2>Module 3: Mean, Variance & Standard Deviation</h2>
<p>Beyond the average (Mean), we need to know how "spread out" the data is. Standard Deviation tells us the typical distance from the center.</p>
"""

G12_QUESTIONS = [
    {"question_text": "In a fair coin toss, what is the probability of 2 heads in 2 tosses?", "question_type": "multiple_choice", "options": ["1/4", "1/2", "1/8", "1"], "correct_answer": "1/4", "explanation": "1/2 * 1/2 = 1/4.", "points": 1, "order_index": 1},
    {"question_text": "What is the shape of a 'Normal Distribution'?", "question_type": "multiple_choice", "options": ["Bell curve", "Straight line", "Square", "Spike"], "correct_answer": "Bell curve", "explanation": "Symmetric curve peaking at the mean.", "points": 1, "order_index": 2},
    {"question_text": "If P(A) = 0.3 and P(B) = 0.4 and they are independent, what is P(A and B)?", "question_type": "multiple_choice", "options": ["0.12", "0.7", "0.1", "0.5"], "correct_answer": "0.12", "explanation": "Multiply for independent events.", "points": 1, "order_index": 3},
    {"question_text": "The sum of all probabilities in a distribution must be:", "question_type": "multiple_choice", "options": ["1.0", "0.0", "100", "Pi"], "correct_answer": "1.0", "explanation": "Total probability is 100% or 1.", "points": 1, "order_index": 4},
    {"question_text": "Standard Deviation is the square root of:", "question_type": "multiple_choice", "options": ["Variance", "Mean", "Sum", "Average"], "correct_answer": "Variance", "explanation": "Std Dev = sqrt(Var).", "points": 1, "order_index": 5},
    {"question_text": "What is the probability of rolling a 7 on a standard 6-sided die?", "question_type": "multiple_choice", "options": ["0", "1/6", "1", "1/7"], "correct_answer": "0", "explanation": "Impossible event.", "points": 1, "order_index": 6},
    {"question_text": "If you take a sample, the Mean is a ___ of the population.", "question_type": "multiple_choice", "options": ["Statistic", "Parameter", "Constant", "Absolute"], "correct_answer": "Statistic", "explanation": "Sample metrics are statistics; population metrics are parameters.", "points": 1, "order_index": 7},
    {"question_text": "A 'Z-score' tells you how many ___ a point is from the mean.", "question_type": "multiple_choice", "options": ["Std Deviations", "Points", "Means", "Decimals"], "correct_answer": "Std Deviations", "explanation": "Z = (x - mean) / std_dev.", "points": 1, "order_index": 8},
    {"question_text": "What is the median of {1, 2, 10, 11, 100}?", "question_type": "multiple_choice", "options": ["10", "2", "24.8", "11"], "correct_answer": "10", "explanation": "Middle value in sorted list.", "points": 1, "order_index": 9},
    {"question_text": "In probability, 'OR' usually means:", "question_type": "multiple_choice", "options": ["Adding", "Multiplying", "Subtracting", "Dividing"], "correct_answer": "Adding", "explanation": "P(A or B) = P(A) + P(B) - P(A and B).", "points": 1, "order_index": 10},
]

# =====================================================================
# Database injection logic
# =====================================================================

COURSES = [
    {"title": "Algebra Foundations (Grade 9)", "desc": "Bridge from arithmetic to algebraic manipulation.", "content": G9_CONTENT, "questions": G9_QUESTIONS, "grade": 9},
    {"title": "Trigonometry & Circles (Grade 10)", "desc": "Angles, sine, cosine, and the Unit Circle.", "content": G10_CONTENT, "questions": G10_QUESTIONS, "grade": 10},
    {"title": "Introduction to Calculus (Grade 11)", "desc": "Limits, derivatives, and accumulation.", "content": G11_CONTENT, "questions": G11_QUESTIONS, "grade": 11},
    {"title": "Probability & Statistics (Grade 12)", "desc": "Distributions, chance, and data interpretation.", "content": G12_CONTENT, "questions": G12_QUESTIONS, "grade": 12},
]

def shuffle_options(question):
    q = question.copy()
    opts = q["options"].copy()
    random.shuffle(opts)
    if q["correct_answer"] not in opts:
        opts[0] = q["correct_answer"]
        random.shuffle(opts)
    q["options"] = opts
    return q

def inject_course(cursor, course):
    cursor.execute("""
        INSERT INTO courses (title, description, content, creator_id, status, grade_level)
        VALUES (%s, %s, %s, 1, 'approved', %s)
    """, (course["title"], course["desc"], course["content"], course["grade"]))
    cursor.execute("SELECT LAST_INSERT_ID() as id")
    course_id = cursor.fetchone()["id"]
    print(f"  Inserted course ID: {course_id}")

    question_ids = []
    for q in course["questions"]:
        sq = shuffle_options(q)
        cursor.execute("""
            INSERT INTO course_questions
            (course_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (course_id, sq["question_text"], sq["question_type"], json.dumps(sq["options"]),
              sq["correct_answer"], sq["explanation"], sq["points"], sq["order_index"]))
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        question_ids.append(cursor.fetchone()["id"])

    enhanced = course["content"]
    for i, qid in enumerate(question_ids, 1):
        enhanced += f'<div class="quiz-question-placeholder" data-question-id="{qid}" style="background: #e0e7ff; border: 2px solid #667eea; padding: 1.5em; margin: 1.5em 0; border-radius: 8px;"><strong>Quiz Question {i}</strong></div>'

    cursor.execute("UPDATE courses SET content = %s WHERE id = %s", (enhanced, course_id))
    print(f"  Added {len(question_ids)} quiz questions for {course['title']}")
    return course_id

def main():
    if not AIVEN_CONFIG["password"]:
        print("Set AIVEN_PASSWORD environment variable!")
        return 1

    print("Connecting to Aiven database...")
    try:
        conn = pymysql.connect(**AIVEN_CONFIG)
        cursor = conn.cursor()
        for c in COURSES:
            print(f"Injecting: {c['title']}...")
            inject_course(cursor, c)
        conn.commit()
        print("\nBatch 3 (Grades 9-12) Injected Successfully!")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        if 'conn' in locals():
            conn.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
