#!/usr/bin/env python3
"""Inject Math Curriculum Batch 2 (Grades 5-8) into Veelearn database."""

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
# GRADE 5: Decimal Operations
# =====================================================================
G5_CONTENT = r"""
<h1>Grade 5 Math: Master of Decimals</h1>
<p>In this course, we dive deep into the world of decimals—learning how to add, subtract, multiply, and divide them with precision!</p>

<hr>

<h2>Module 1: Adding and Subtracting Decimals</h2>
<p>The most important rule? <strong>Align the decimal points!</strong> Just like you align columns for large whole numbers, you must keep the tenths with tenths and hundredths with hundredths.</p>

<hr>

<h2>Module 2: Multiplying Decimals</h2>
<p>When multiplying, ignore the decimals first. Multiply like whole numbers, then count the total decimal places in the factors to place the point in the product.</p>

<h3>Interactive Area Model Decimals</h3>
<iframe src="https://phet.colorado.edu/sims/html/area-model-decimals/latest/area-model-decimals_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Use the "Multiply" tab to see how decimals are broken into parts!</em></p>

<hr>

<h2>Module 3: Dividing Decimals</h2>
<p>Dividing a decimal by a whole number is simple—just place the decimal directly above in the quotient. For decimal-by-decimal, move the point to make the divisor a whole number first!</p>
"""

G5_QUESTIONS = [
    {"question_text": "What is 1.5 + 2.7?", "question_type": "multiple_choice", "options": ["3.2", "4.2", "4.0", "3.8"], "correct_answer": "4.2", "explanation": "1.5 + 2.7 = 4.2.", "points": 1, "order_index": 1},
    {"question_text": "Solve: 0.5 x 0.5", "question_type": "multiple_choice", "options": ["2.5", "0.25", "5.0", "0.05"], "correct_answer": "0.25", "explanation": "5 x 5 = 25, then move point 2 places.", "points": 1, "order_index": 2},
    {"question_text": "What is 10.0 - 0.5?", "question_type": "multiple_choice", "options": ["9.5", "10.5", "9.0", "1.0"], "correct_answer": "9.5", "explanation": "Subtracting 0.5 from 10 leaves 9.5.", "points": 1, "order_index": 3},
    {"question_text": "How many decimal places in 1.2 x 3.45?", "question_type": "multiple_choice", "options": ["1", "2", "3", "4"], "correct_answer": "3", "explanation": "1 place in 1.2 + 2 places in 3.45 = 3 places.", "points": 1, "order_index": 4},
    {"question_text": "What is 4.8 / 2?", "question_type": "multiple_choice", "options": ["2.4", "2.2", "24", "4.2"], "correct_answer": "2.4", "explanation": "4.8 ÷ 2 = 2.4.", "points": 1, "order_index": 5},
    {"question_text": "Which is equivalent to 0.7?", "question_type": "multiple_choice", "options": ["7/10", "7/100", "0.07", "7.0"], "correct_answer": "7/10", "explanation": "0.7 is 7 tenths.", "points": 1, "order_index": 6},
    {"question_text": "What is 0.1 x 100?", "question_type": "multiple_choice", "options": ["1", "10", "0.1", "100"], "correct_answer": "10", "explanation": "0.1 x 100 = 10.", "points": 1, "order_index": 7},
    {"question_text": "Solve: 5.6 - 1.25", "question_type": "multiple_choice", "options": ["4.35", "4.45", "4.55", "3.35"], "correct_answer": "4.35", "explanation": "5.60 - 1.25 = 4.35.", "points": 1, "order_index": 8},
    {"question_text": "What is the tenths digit in 123.456?", "question_type": "multiple_choice", "options": ["4", "5", "6", "3"], "correct_answer": "4", "explanation": "The first digit after the point is tenths.", "points": 1, "order_index": 9},
    {"question_text": "Which is greater: 0.8 or 0.799?", "question_type": "multiple_choice", "options": ["0.8", "0.799", "Equal", "0.7"], "correct_answer": "0.8", "explanation": "0.8 is 0.800, which is larger than 0.799.", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 6: Ratios & Rates
# =====================================================================
G6_CONTENT = r"""
<h1>Grade 6 Math: Ratios & Rates</h1>
<p>Understand the relationship between numbers and learn how to scale quantities efficiently!</p>

<hr>

<h2>Module 1: Intro to Ratios</h2>
<p>A ratio is a comparison of two numbers. It can be written as $a:b$, $a$ to $b$, or $a/b$.</p>
<p><strong>Example:</strong> If there are 2 apples and 3 oranges, the ratio is $2:3$.</p>

<hr>

<h2>Module 2: Unit Rates</h2>
<p>A unit rate is a ratio where the second number is 1. Thinking in "per 1" (like miles per hour) helps us make comparisons easier.</p>

<h3>Interactive Ratio Lab</h3>
<iframe src="https://phet.colorado.edu/sims/html/ratio-lab/latest/ratio-lab_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Experiment with different proportions!</em></p>

<hr>

<h2>Module 3: Proportions</h2>
<p>A proportion is an equation stating that two ratios are equal. You can use cross-multiplication to solve for missing variables!</p>
"""

G6_QUESTIONS = [
    {"question_text": "If a box has 5 red balls and 10 blue balls, what is the ratio of red to blue?", "question_type": "multiple_choice", "options": ["1:2", "2:1", "5:1", "1:10"], "correct_answer": "1:2", "explanation": "5:10 simplifies to 1:2.", "points": 1, "order_index": 1},
    {"question_text": "A car travels 120 miles in 2 hours. What is its unit rate (mph)?", "question_type": "multiple_choice", "options": ["60 mph", "120 mph", "240 mph", "30 mph"], "correct_answer": "60 mph", "explanation": "120 / 2 = 60.", "points": 1, "order_index": 2},
    {"question_text": "Solve the proportion: 2/5 = x/10. What is x?", "question_type": "multiple_choice", "options": ["4", "5", "6", "2"], "correct_answer": "4", "explanation": "2 x 10 = 20; 20 / 5 = 4.", "points": 1, "order_index": 3},
    {"question_text": "What is the ratio of 3 boys to 12 girls simplified?", "question_type": "multiple_choice", "options": ["1:4", "1:3", "3:1", "4:1"], "correct_answer": "1:4", "explanation": "Divide both by 3.", "points": 1, "order_index": 4},
    {"question_text": "If 3 pizzas cost $30, how much does 1 pizza cost?", "question_type": "multiple_choice", "options": ["$10", "$5", "$15", "$3"], "correct_answer": "$10", "explanation": "$30 / 3 = $10.", "points": 1, "order_index": 5},
    {"question_text": "In the ratio 4:7, if the first quantity becomes 8, what does the second become?", "question_type": "multiple_choice", "options": ["14", "11", "7", "21"], "correct_answer": "14", "explanation": "Scaling by 2: 4x2=8, 7x2=14.", "points": 1, "order_index": 6},
    {"question_text": "Which is a better deal: 2 lbs for $4 or 5 lbs for $10?", "question_type": "multiple_choice", "options": ["They are the same", "2 lbs for $4", "5 lbs for $10", "None"], "correct_answer": "They are the same", "explanation": "Both are $2 per pound.", "points": 1, "order_index": 7},
    {"question_text": "Express 50% as a ratio.", "question_type": "multiple_choice", "options": ["1:2", "1:5", "5:1", "1:1"], "correct_answer": "1:2", "explanation": "50/100 = 1/2.", "points": 1, "order_index": 8},
    {"question_text": "If a recipe calls for 2 cups sugar to 5 cups flour, how much sugar for 10 cups flour?", "question_type": "multiple_choice", "options": ["4 cups", "5 cups", "10 cups", "2 cups"], "correct_answer": "4 cups", "explanation": "5x2=10, so 2x2=4.", "points": 1, "order_index": 9},
    {"question_text": "What does 'percent' mean?", "question_type": "multiple_choice", "options": ["Per 100", "Per 10", "Per 1", "Total"], "correct_answer": "Per 100", "explanation": "Percent comes from 'per centum' (hundred).", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 7: Geometry & Scale
# =====================================================================
G7_CONTENT = r"""
<h1>Grade 7 Math: Geometry & Reality</h1>
<p>Understand shapes, angles, and how the world scales up and down!</p>

<hr>

<h2>Module 1: Scale Factor</h2>
<p>Scale Factor tells us how many times larger or smaller a drawing is compared to the original object. $SF = \frac{\text{New}}{\text{Old}}$.</p>

<hr>

<h2>Module 2: Angles & Constructions</h2>
<p>Explore vertical, adjacent, and complementary angles. Mastering these is the foundation of building things!</p>

<h3>Interactive Geometric Construction</h3>
<iframe src="https://phet.colorado.edu/sims/html/geometric-construction/latest/geometric-construction_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Use this tool to draw and measure exactly!</em></p>

<hr>

<h2>Module 3: Area of Circles</h2>
<p>The area of a circle is calculated using $\pi$ ($3.14$). Formula: $A = \pi \times r^2$.</p>
"""

G7_QUESTIONS = [
    {"question_text": "What is the sum of angles in a triangle?", "question_type": "multiple_choice", "options": ["180°", "90°", "360°", "270°"], "correct_answer": "180°", "explanation": "All internal angles of a triangle add to 180 degrees.", "points": 1, "order_index": 1},
    {"question_text": "If a circle has a radius of 5, what is its diameter?", "question_type": "multiple_choice", "options": ["10", "25", "15", "5"], "correct_answer": "10", "explanation": "D = 2r.", "points": 1, "order_index": 2},
    {"question_text": "What is the approximate value of Pi ($\pi$)?", "question_type": "multiple_choice", "options": ["3.14", "2.14", "4.14", "1.14"], "correct_answer": "3.14", "explanation": "Pi is roughly 3.14.", "points": 1, "order_index": 3},
    {"question_text": "Two angles add to 90°. They are called:", "question_type": "multiple_choice", "options": ["Complementary", "Supplementary", "Vertical", "Right"], "correct_answer": "Complementary", "explanation": "Complementary sums to 90, Supplementary to 180.", "points": 1, "order_index": 4},
    {"question_text": "If a scale drawing is 1cm:10m, how long is 3cm in reality?", "question_type": "multiple_choice", "options": ["30m", "3m", "300m", "10m"], "correct_answer": "30m", "explanation": "3 x 10 = 30.", "points": 1, "order_index": 5},
    {"question_text": "Calculate the area of a circle with radius 2 (use $\pi = 3$ for estimation).", "question_type": "multiple_choice", "options": ["12", "6", "8", "4"], "correct_answer": "12", "explanation": "3 x 2^2 = 3 x 4 = 12.", "points": 1, "order_index": 6},
    {"question_text": "A rectangle with scale factor 2 will have how many times the area?", "question_type": "multiple_choice", "options": ["4", "2", "8", "1"], "correct_answer": "4", "explanation": "Area scales by scale factor squared (2^2 = 4).", "points": 1, "order_index": 7},
    {"question_text": "Vertical angles are always:", "question_type": "multiple_choice", "options": ["Equal", "Opposite", "90°", "Adding to 180°"], "correct_answer": "Equal", "explanation": "Vertical angles (opposite) are congruent.", "points": 1, "order_index": 8},
    {"question_text": "What is the perimeter of a 5x10 rectangle?", "question_type": "multiple_choice", "options": ["30", "50", "15", "20"], "correct_answer": "30", "explanation": "2(5) + 2(10) = 10 + 20 = 30.", "points": 1, "order_index": 9},
    {"question_text": "The ratio of circumference to diameter is always:", "question_type": "multiple_choice", "options": ["Pi", "2", "1", "10"], "correct_answer": "Pi", "explanation": "C / d = Pi.", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 8: Linear Functions
# =====================================================================
G8_CONTENT = r"""
<h1>Grade 8 Math: Linear Life</h1>
<p>Master the language of algebra, understand functions, and learn how to graph the future!</p>

<hr>

<h2>Module 1: Intro to Functions</h2>
<p>A function is like a machine: you put an "input" (x) in, and it gives you one "output" (y). Rule: Every input has exactly ONE output.</p>

<hr>

<h2>Module 2: Slope-Intercept Form</h2>
<p>The magic equation for straight lines is $y = mx + b$.</p>
<ul>
  <li><strong>m:</strong> The slope (rise over run).</li>
  <li><strong>b:</strong> The y-intercept (where it hits the zero line).</li>
</ul>

<h3>Interactive Graphing Lines</h3>
<iframe src="https://phet.colorado.edu/sims/html/graphing-lines/latest/graphing-lines_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Adjust the m and b sliders to see the line change!</em></p>

<hr>

<h2>Module 3: Systems of Equations</h2>
<p>A system of equations is two lines on a graph. The point where they cross $(x, y)$ is the solution that works for both!</p>
"""

G8_QUESTIONS = [
    {"question_text": "In y = 3x + 5, what is the slope?", "question_type": "multiple_choice", "options": ["3", "5", "x", "y"], "correct_answer": "3", "explanation": "The coefficient of x is the slope.", "points": 1, "order_index": 1},
    {"question_text": "What is the y-intercept of y = -2x + 8?", "question_type": "multiple_choice", "options": ["8", "-2", "0", "x"], "correct_answer": "8", "explanation": "The constant term is the y-intercept.", "points": 1, "order_index": 2},
    {"question_text": "If m = 1 and b = 0, what is the equation?", "question_type": "multiple_choice", "options": ["y = x", "y = 0", "y = 1", "y = x + 1"], "correct_answer": "y = x", "explanation": "y = 1x + 0 simplifies to y = x.", "points": 1, "order_index": 3},
    {"question_text": "A line going up from left to right has a ___ slope.", "question_type": "multiple_choice", "options": ["Positive", "Negative", "Zero", "Undefined"], "correct_answer": "Positive", "explanation": "Positive slope means y increases as x increases.", "points": 1, "order_index": 4},
    {"question_text": "What is the slope of a horizontal line?", "question_type": "multiple_choice", "options": ["0", "1", "Undefined", "10"], "correct_answer": "0", "explanation": "Horizontal lines have no 'rise'.", "points": 1, "order_index": 5},
    {"question_text": "Solve for y if x = 2 in y = 5x + 3.", "question_type": "multiple_choice", "options": ["13", "10", "15", "8"], "correct_answer": "13", "explanation": "y = 5(2) + 3 = 10 + 3 = 13.", "points": 1, "order_index": 6},
    {"question_text": "The point (0, 0) is also called the:", "question_type": "multiple_choice", "options": ["Origin", "Start", "Intersection", "Center"], "correct_answer": "Origin", "explanation": "The origin is (0,0).", "points": 1, "order_index": 7},
    {"question_text": "If two lines have the same slope, they are:", "question_type": "multiple_choice", "options": ["Parallel", "Perpendicular", "Intersecting", "Vertical"], "correct_answer": "Parallel", "explanation": "Parallel lines never meet and have equal slopes.", "points": 1, "order_index": 8},
    {"question_text": "What is the rise over run for a slope of 2/3?", "question_type": "multiple_choice", "options": ["Rise 2, Run 3", "Rise 3, Run 2", "Rise 6, Run 1", "Rise 1, Run 1"], "correct_answer": "Rise 2, Run 3", "explanation": "Numerator is rise, denominator is run.", "points": 1, "order_index": 9},
    {"question_text": "Is this a function: {(1,2), (2,3), (1,4)}?", "question_type": "multiple_choice", "options": ["No", "Yes", "Maybe", "Only on Tuesdays"], "correct_answer": "No", "explanation": "Input 1 has two different outputs (2 and 4).", "points": 1, "order_index": 10},
]

# =====================================================================
# Database injection logic
# =====================================================================

COURSES = [
    {"title": "Master of Decimals (Grade 5)", "desc": "Dive deep into decimal arithmetic and area models.", "content": G5_CONTENT, "questions": G5_QUESTIONS, "grade": 5},
    {"title": "Ratios & Rates (Grade 6)", "desc": "Understanding proportions and unit rates for Grade 6.", "content": G6_CONTENT, "questions": G6_QUESTIONS, "grade": 6},
    {"title": "Geometry & Reality (Grade 7)", "desc": "Shapes, angles, and scale factors for Grade 7.", "content": G7_CONTENT, "questions": G7_QUESTIONS, "grade": 7},
    {"title": "Linear Life (Grade 8)", "desc": "Mastering linear functions and graphing for Grade 8.", "content": G8_CONTENT, "questions": G8_QUESTIONS, "grade": 8},
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
        print("\nBatch 2 (Grades 5-8) Injected Successfully!")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        if 'conn' in locals():
            conn.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
