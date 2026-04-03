#!/usr/bin/env python3
"""Inject Math Curriculum Batch 1 (Grades 1-4) into Veelearn database."""

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

# SSL Configuration for Aiven
ssl_ca = os.getenv("DB_SSL_CA")
if ssl_ca:
    if "\\n" in ssl_ca:
        ssl_ca = ssl_ca.replace("\\n", "\n")
    ca_path = os.path.join(os.getcwd(), "ca.pem")
    with open(ca_path, "w") as f:
        f.write(ssl_ca)
    AIVEN_CONFIG["ssl"] = {"ca": ca_path}
elif os.getenv("MYSQLHOST") or os.getenv("AIVEN_HOST"):
    # If no CA provided but on Aiven, use default SSL
    AIVEN_CONFIG["ssl"] = {}

# =====================================================================
# GRADE 1: Magic of Numbers
# =====================================================================
G1_CONTENT = r"""
<h1>Grade 1 Math: The Magic of Numbers</h1>
<p>In this course, we'll discover how numbers work, explore counting, and learn the basics of addition and subtraction!</p>

<hr>

<h2>Module 1: Counting & Groups</h2>
<p>Numbers tell us "how many." Counting is the foundation of all math. We count objects one by one to find the total.</p>
<ul>
  <li>Counting up to 20</li>
  <li>Groups of 5 and 10</li>
  <li>Comparing numbers (More vs. Less)</li>
</ul>

<hr>

<h2>Module 2: Basic Addition</h2>
<p>Addition is putting two groups together to make a larger group. The "+" sign is the addition symbol.</p>
<p><strong>Example:</strong> $2 + 3 = 5$</p>

<h3>Interactive Arithmetic Simulator</h3>
<iframe src="https://phet.colorado.edu/sims/html/arithmetic/latest/arithmetic_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Use the "Multiply" or "Add" tabs to practice your number skills!</em></p>

<hr>

<h2>Module 3: Basic Subtraction</h2>
<p>Subtraction is taking part of a group away. The "−" sign is the subtraction symbol.</p>
<p><strong>Example:</strong> $5 - 2 = 3$</p>
<p>Think of it as the opposite of addition!</p>
"""

G1_QUESTIONS = [
    {"question_text": "What is 2 + 3?", "question_type": "multiple_choice", "options": ["4", "5", "6", "7"], "correct_answer": "5", "explanation": "2 plus 3 equals 5.", "points": 1, "order_index": 1},
    {"question_text": "What is 7 - 4?", "question_type": "multiple_choice", "options": ["2", "3", "4", "5"], "correct_answer": "3", "explanation": "Taking 4 away from 7 leaves 3.", "points": 1, "order_index": 2},
    {"question_text": "Which number is MORE: 8 or 5?", "question_type": "multiple_choice", "options": ["8", "5", "They are equal", "0"], "correct_answer": "8", "explanation": "8 is a larger number than 5.", "points": 1, "order_index": 3},
    {"question_text": "Count the apples: 🍎🍎🍎. How many are there?", "question_type": "multiple_choice", "options": ["2", "3", "4", "5"], "correct_answer": "3", "explanation": "There are three apples.", "points": 1, "order_index": 4},
    {"question_text": "If I have 5 candies and eat 2, how many do I have left?", "question_type": "multiple_choice", "options": ["2", "3", "4", "5"], "correct_answer": "3", "explanation": "5 - 2 = 3.", "points": 1, "order_index": 5},
    {"question_text": "What is 10 + 0?", "question_type": "multiple_choice", "options": ["0", "1", "10", "11"], "correct_answer": "10", "explanation": "Adding zero doesn't change the number.", "points": 1, "order_index": 6},
    {"question_text": "What comes after 9?", "question_type": "multiple_choice", "options": ["8", "10", "11", "0"], "correct_answer": "10", "explanation": "The sequence is 8, 9, 10...", "points": 1, "order_index": 7},
    {"question_text": "What is 4 + 4?", "question_type": "multiple_choice", "options": ["6", "7", "8", "9"], "correct_answer": "8", "explanation": "Double 4 is 8.", "points": 1, "order_index": 8},
    {"question_text": "What is 9 - 9?", "question_type": "multiple_choice", "options": ["0", "1", "9", "18"], "correct_answer": "0", "explanation": "Subtracting a number from itself equals zero.", "points": 1, "order_index": 9},
    {"question_text": "If I have 1 ball and get 1 more, how many do I have?", "question_type": "multiple_choice", "options": ["1", "2", "3", "4"], "correct_answer": "2", "explanation": "1 + 1 = 2.", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 2: Place Value & Making Tens
# =====================================================================
G2_CONTENT = r"""
<h1>Grade 2 Math: Place Value & Making Tens</h1>
<p>Learn how digits create bigger numbers and master the "Make a Ten" strategy for faster math!</p>

<hr>

<h2>Module 1: Units and Tens</h2>
<p>Numbers like 15 are made of 1 Ten and 5 Ones. Understanding <strong>Place Value</strong> is the key to big numbers!</p>

<hr>

<h2>Module 2: Make a Ten Strategy</h2>
<p>When adding numbers like $8 + 5$, it's easier to think: "8 needs 2 more to make 10. Take 2 from the 5 (leaving 3). $10 + 3 = 13$!"</p>

<h3>Interactive "Make a Ten" Simulator</h3>
<iframe src="https://phet.colorado.edu/sims/html/make-a-ten/latest/make-a-ten_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Use this game to practice making groups of ten!</em></p>

<hr>

<h2>Module 3: 2-Digit Addition</h2>
<p>Add the ones first, then the tens. Remember to "carry over" if the ones add up to 10 or more.</p>
"""

G2_QUESTIONS = [
    {"question_text": "In the number 25, which digit is in the 'tens' place?", "question_type": "multiple_choice", "options": ["2", "5", "0", "None"], "correct_answer": "2", "explanation": "2 stands for twenty (2 tens).", "points": 1, "order_index": 1},
    {"question_text": "What is 8 + 7 using the 'Make a Ten' strategy?", "question_type": "multiple_choice", "options": ["13", "14", "15", "16"], "correct_answer": "15", "explanation": "8 + 2 = 10; 10 + 5 = 15.", "points": 1, "order_index": 2},
    {"question_text": "What is 30 + 40?", "question_type": "multiple_choice", "options": ["60", "70", "80", "43"], "correct_answer": "70", "explanation": "3 tens + 4 tens = 7 tens (70).", "points": 1, "order_index": 3},
    {"question_text": "Which is the same as 14 + 5?", "question_type": "multiple_choice", "options": ["10 + 9", "10 + 4", "10 + 5", "20 - 2"], "correct_answer": "10 + 9", "explanation": "14 + 5 = 19, which is 10 and 9.", "points": 1, "order_index": 4},
    {"question_text": "What is 10 less than 45?", "question_type": "multiple_choice", "options": ["35", "44", "55", "30"], "correct_answer": "35", "explanation": "4 tens - 1 ten = 3 tens (35).", "points": 1, "order_index": 5},
    {"question_text": "What is 9 + 1?", "question_type": "multiple_choice", "options": ["8", "10", "11", "0"], "correct_answer": "10", "explanation": "9 and 1 are partners to make 10.", "points": 1, "order_index": 6},
    {"question_text": "How many ones are in the number 38?", "question_type": "multiple_choice", "options": ["3", "8", "38", "0"], "correct_answer": "8", "explanation": "3 tens and 8 ones.", "points": 1, "order_index": 7},
    {"question_text": "What is 15 + 15?", "question_type": "multiple_choice", "options": ["20", "25", "30", "35"], "correct_answer": "30", "explanation": "15 + 15 = 30.", "points": 1, "order_index": 8},
    {"question_text": "Count by tens: 10, 20, 30, ... what's next?", "question_type": "multiple_choice", "options": ["31", "35", "40", "50"], "correct_answer": "40", "explanation": "Counting by tens: 10, 20, 30, 40.", "points": 1, "order_index": 9},
    {"question_text": "What is 20 - 5?", "question_type": "multiple_choice", "options": ["10", "15", "16", "25"], "correct_answer": "15", "explanation": "20 take away 5 is 15.", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 3: Exploring Fractions
# =====================================================================
G3_CONTENT = r"""
<h1>Grade 3 Math: Exploring Fractions</h1>
<p>Fractions represent parts of a whole. Let's learn about numerators, denominators, and how to see fractions in the real world!</p>

<hr>

<h2>Module 1: What is a Fraction?</h2>
<p>A fraction has two parts:</p>
<ul>
  <li><strong>Numerator (Top):</strong> How many parts you have.</li>
  <li><strong>Denominator (Bottom):</strong> How many equal parts the whole is divided into.</li>
</ul>
<p><strong>Example:</strong> $1/2$ means one out of two equal parts.</p>

<h3>Interactive Fractions Intro</h3>
<iframe src="https://phet.colorado.edu/sims/html/fractions-intro/latest/fractions-intro_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Build different fractions and see how they look!</em></p>

<hr>

<h2>Module 2: Fractions on a Number Line</h2>
<p>Fractions live between the whole numbers. $1/2$ is exactly halfway between 0 and 1.</p>

<hr>

<h2>Module 3: Comparing Unit Fractions</h2>
<p>A "Unit Fraction" has 1 as the numerator. <strong>Pro Tip:</strong> The bigger the denominator, the smaller the piece!</p>
<p>$1/2$ is bigger than $1/4$.</p>

"""

G3_QUESTIONS = [
    {"question_text": "What is the top number of a fraction called?", "question_type": "multiple_choice", "options": ["Numerator", "Denominator", "Whole", "Decimal"], "correct_answer": "Numerator", "explanation": "The numerator tells us how many parts are being counted.", "points": 1, "order_index": 1},
    {"question_text": "What does the denominator tell us?", "question_type": "multiple_choice", "options": ["Total parts in a whole", "Parts we have", "The answer", "The size"], "correct_answer": "Total parts in a whole", "explanation": "The denominator shows the total number of equal pieces.", "points": 1, "order_index": 2},
    {"question_text": "Which is larger: 1/2 or 1/4?", "question_type": "multiple_choice", "options": ["1/2", "1/4", "They are equal", "None"], "correct_answer": "1/2", "explanation": "Dividing a whole into 2 pieces makes much larger pieces than dividing into 4.", "points": 1, "order_index": 3},
    {"question_text": "If a pizza has 8 slices and you eat 3, what fraction did you eat?", "question_type": "multiple_choice", "options": ["3/8", "5/8", "8/3", "1/8"], "correct_answer": "3/8", "explanation": "3 parts out of 8 total slices.", "points": 1, "order_index": 4},
    {"question_text": "What is 1/3 + 1/3?", "question_type": "multiple_choice", "options": ["2/3", "2/6", "1/6", "1/3"], "correct_answer": "2/3", "explanation": "Combine the numerators when denominators are the same.", "points": 1, "order_index": 5},
    {"question_text": "Which fraction is equal to one whole?", "question_type": "multiple_choice", "options": ["4/4", "1/4", "0/4", "4/1"], "correct_answer": "4/4", "explanation": "When numerator and denominator are the same, it equals 1.", "points": 1, "order_index": 6},
    {"question_text": "On a number line, where is 1/2 located?", "question_type": "multiple_choice", "options": ["Between 0 and 1", "Between 1 and 2", "At 0", "At 1"], "correct_answer": "Between 0 and 1", "explanation": "Half is less than 1 but more than 0.", "points": 1, "order_index": 7},
    {"question_text": "What is 1/2 of 10?", "question_type": "multiple_choice", "options": ["2", "5", "10", "20"], "correct_answer": "5", "explanation": "Splitting 10 into two equal groups gives 5.", "points": 1, "order_index": 8},
    {"question_text": "How many halves make a whole?", "question_type": "multiple_choice", "options": ["1", "2", "3", "4"], "correct_answer": "2", "explanation": "1/2 + 1/2 = 1.", "points": 1, "order_index": 9},
    {"question_text": "Which is smaller: 1/10 or 1/5?", "question_type": "multiple_choice", "options": ["1/10", "1/5", "Equal", "1/2"], "correct_answer": "1/10", "explanation": "A larger denominator means more (and smaller) pieces.", "points": 1, "order_index": 10},
]

# =====================================================================
# GRADE 4: Advanced Fractions & Area Models
# =====================================================================
G4_CONTENT = r"""
<h1>Grade 4 Math: Equivalent Fractions & Area Models</h1>
<p>Master the art of fractions, learn about area models, and start your journey into decimals!</p>

<hr>

<h2>Module 1: Equivalent Fractions</h2>
<p>Some fractions look different but represent the same amount! For example, $1/2$ is the same as $2/4$ or $4/8$.</p>

<h3>Interactive Fraction Matcher</h3>
<iframe src="https://phet.colorado.edu/sims/html/fraction-matcher/latest/fraction-matcher_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Try to match the equivalent fractions!</em></p>

<hr>

<h2>Module 2: Area Models</h2>
<p>An **Area Model** is a visual way to solve multiplication problems by breaking them into smaller rectangles.</p>

<h3>Interactive Area Model Intro</h3>
<iframe src="https://phet.colorado.edu/sims/html/area-model-introduction/latest/area-model-introduction_all.html" 
  width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; margin: 20px 0;"></iframe>
<p><em>Build rectangles and see how their area relates to multiplication!</em></p>

<hr>

<h2>Module 3: Decimals Intro</h2>
<p>Decimals are another way to write fractions with denominators of 10 or 100.</p>
<p>$0.7 = 7/10$</p>
<p>$0.05 = 5/100$</p>

"""

G4_QUESTIONS = [
    {"question_text": "What is an equivalent fraction for 1/2?", "question_type": "multiple_choice", "options": ["2/4", "1/3", "2/3", "3/4"], "correct_answer": "2/4", "explanation": "1/2 and 2/4 both represent 50%.", "points": 1, "order_index": 1},
    {"question_text": "What is 2/10 written as a decimal?", "question_type": "multiple_choice", "options": ["0.2", "0.02", "2.0", "0.22"], "correct_answer": "0.2", "explanation": "2 tenths is 0.2.", "points": 1, "order_index": 2},
    {"question_text": "In an area model, what does the area represent?", "question_type": "multiple_choice", "options": ["The product", "The sum", "The difference", "The remainder"], "correct_answer": "The product", "explanation": "Area = Length x Width, which is multiplication.", "points": 1, "order_index": 3},
    {"question_text": "What is 3/4 + 1/4?", "question_type": "multiple_choice", "options": ["1", "4/8", "2/4", "1/2"], "correct_answer": "1", "explanation": "3/4 + 1/4 = 4/4, which is 1 whole.", "points": 1, "order_index": 4},
    {"question_text": "Which is greater: 0.5 or 0.05?", "question_type": "multiple_choice", "options": ["0.5", "0.05", "Equal", "0.005"], "correct_answer": "0.5", "explanation": "0.5 is 5 tenths, while 0.05 is only 5 hundredths.", "points": 1, "order_index": 5},
    {"question_text": "Solve: 5 x 4 using an area model.", "question_type": "multiple_choice", "options": ["20", "9", "25", "15"], "correct_answer": "20", "explanation": "A 5x4 grid has 20 squares.", "points": 1, "order_index": 6},
    {"question_text": "Which fraction is NOT equivalent to 1/3?", "question_type": "multiple_choice", "options": ["2/6", "3/9", "4/12", "5/10"], "correct_answer": "5/10", "explanation": "5/10 is equivalent to 1/2.", "points": 1, "order_index": 7},
    {"question_text": "What is 1/2 of 1/2?", "question_type": "multiple_choice", "options": ["1/4", "1", "1/2", "2/4"], "correct_answer": "1/4", "explanation": "Half of a half is a quarter.", "points": 1, "order_index": 8},
    {"question_text": "What is 0.75 as a fraction?", "question_type": "multiple_choice", "options": ["75/100", "7/5", "3/4", "Both A and C"], "correct_answer": "Both A and C", "explanation": "75/100 simplifies to 3/4.", "points": 1, "order_index": 9},
    {"question_text": "If you multiply the numerator and denominator by the same number, the fraction is:", "question_type": "multiple_choice", "options": ["Equivalent", "Larger", "Smaller", "Zero"], "correct_answer": "Equivalent", "explanation": "This is how we find equivalent fractions.", "points": 1, "order_index": 10},
]

# =====================================================================
# Database injection logic
# =====================================================================

COURSES = [
    {"title": "Magic of Numbers: Addition (Grade 1)", "desc": "Discovery of counting and basic arithmetic for Grade 1.", "content": G1_CONTENT, "questions": G1_QUESTIONS, "grade": 1},
    {"title": "Place Value & Making Ten (Grade 2)", "desc": "Mastering groups of ten and place value logic for Grade 2.", "content": G2_CONTENT, "questions": G2_QUESTIONS, "grade": 2},
    {"title": "Exploring Fractions (Grade 3)", "desc": "Introduction to parts of a whole and units for Grade 3.", "content": G3_CONTENT, "questions": G3_QUESTIONS, "grade": 3},
    {"title": "Equivalent Fractions & Area Models (Grade 4)", "desc": "Advanced fraction logic and area modeling for Grade 4.", "content": G4_CONTENT, "questions": G4_QUESTIONS, "grade": 4},
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
        print("\nBatch 1 (Grades 1-4) Injected Successfully!")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        if 'conn' in locals():
            conn.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
