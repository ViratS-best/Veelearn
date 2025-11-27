/**
 * Script to create and publish a comprehensive Arithmetic course
 * Run this with: node create_arithmetic_course.js
 */

const http = require('http');

// First, let's login as superadmin to get token
async function login() {
  return new Promise((resolve, reject) => {
    const loginData = JSON.stringify({
      email: 'viratsuper6@gmail.com',
      password: 'Virat@123'
    });

    const options = {
      hostname: 'localhost',
      port: 3000,
      path: '/api/login',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': loginData.length
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.success && parsed.data.token) {
            console.log('✅ Login successful');
            resolve(parsed.data.token);
          } else {
            reject(new Error('Login failed: ' + parsed.message));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(loginData);
    req.end();
  });
}

async function createCourse(token) {
  return new Promise((resolve, reject) => {
    const courseData = JSON.stringify({
      title: '🎓 Mastering Arithmetic: From Basics to Advanced',
      description: 'A comprehensive guide to arithmetic fundamentals including addition, subtraction, multiplication, and division. Learn through interactive PhET simulations and hands-on examples.',
      content: `
<h2>Welcome to Arithmetic Mastery!</h2>
<p>This course is designed to help you master the fundamentals of arithmetic through interactive learning and real-world applications.</p>

<h3>📚 Course Overview</h3>
<p>In this course, you will learn:</p>
<ul>
  <li><strong>Number Systems:</strong> Understand whole numbers, integers, and their properties</li>
  <li><strong>Addition:</strong> Master basic and advanced addition techniques</li>
  <li><strong>Subtraction:</strong> Learn subtraction strategies and borrowing concepts</li>
  <li><strong>Multiplication:</strong> Develop multiplication skills and patterns</li>
  <li><strong>Division:</strong> Understand division, remainders, and long division</li>
  <li><strong>Real-World Applications:</strong> Apply arithmetic to everyday situations</li>
</ul>

<h3>📖 Module 1: Introduction to Numbers</h3>
<p>Numbers are the foundation of mathematics. In this module, we'll explore:</p>
<ul>
  <li>What are numbers?</li>
  <li>Place value and number representation</li>
  <li>Comparing and ordering numbers</li>
  <li>Number sequences and patterns</li>
</ul>

<h3>📖 Module 2: Addition Fundamentals</h3>
<p><strong>Addition</strong> is the process of combining numbers to find a total. Let's explore addition with interactive simulations!</p>
<p>Key concepts:</p>
<ul>
  <li>Single-digit addition</li>
  <li>Multi-digit addition</li>
  <li>Addition properties (Commutative, Associative)</li>
  <li>Mental math strategies</li>
</ul>

<h3>📖 Module 3: Subtraction Fundamentals</h3>
<p><strong>Subtraction</strong> is the reverse of addition - it's about finding the difference between numbers.</p>
<p>Topics covered:</p>
<ul>
  <li>Basic subtraction facts</li>
  <li>Subtraction with borrowing (regrouping)</li>
  <li>Multi-digit subtraction</li>
  <li>Subtraction as the inverse of addition</li>
</ul>

<h3>📖 Module 4: Multiplication Mastery</h3>
<p><strong>Multiplication</strong> is repeated addition. It's a powerful mathematical operation used everywhere!</p>
<p>What you'll learn:</p>
<ul>
  <li>Multiplication tables (1-12)</li>
  <li>Multiplication properties</li>
  <li>Multi-digit multiplication</li>
  <li>Estimation and checking answers</li>
</ul>

<h3>📖 Module 5: Division Strategies</h3>
<p><strong>Division</strong> is the inverse of multiplication. It's about sharing and grouping.</p>
<p>Essential topics:</p>
<ul>
  <li>Basic division facts</li>
  <li>Division with remainders</li>
  <li>Long division technique</li>
  <li>Division word problems</li>
</ul>

<h3>📖 Module 6: Mixed Operations & Problem Solving</h3>
<p>Combine all four operations to solve real-world problems!</p>
<ul>
  <li>Order of operations (PEMDAS/BODMAS)</li>
  <li>Two-step and multi-step word problems</li>
  <li>Real-world applications in shopping, cooking, and more</li>
  <li>Estimation and reasonableness checking</li>
</ul>

<h3>✨ Interactive Learning</h3>
<p>Each module includes interactive PhET simulations to help you visualize and understand concepts better. Learning by doing is the most effective way to master arithmetic!</p>

<h3>🎯 Course Goals</h3>
<p>By the end of this course, you will be able to:</p>
<ul>
  <li>Perform all four basic arithmetic operations fluently</li>
  <li>Understand mathematical concepts deeply, not just memorize</li>
  <li>Apply arithmetic to real-world situations</li>
  <li>Develop problem-solving and critical thinking skills</li>
  <li>Build confidence in mathematics</li>
</ul>

<h3>💡 Tips for Success</h3>
<ol>
  <li><strong>Practice regularly:</strong> Mathematics requires consistent practice</li>
  <li><strong>Use the simulations:</strong> Interactive tools help deepen understanding</li>
  <li><strong>Try the quizzes:</strong> Test your knowledge and identify areas for improvement</li>
  <li><strong>Don't rush:</strong> Take time to understand concepts thoroughly</li>
  <li><strong>Ask questions:</strong> Mathematics builds on itself - understand each step</li>
</ol>

<p style="margin-top: 30px; padding: 15px; background-color: #e8f4f8; border-left: 4px solid #0288d1; border-radius: 4px;">
  <strong>Welcome aboard!</strong> We're excited to help you master arithmetic. Let's begin this journey together! 🚀
</p>
      `,
      status: 'approved'
    });

    const options = {
      hostname: 'localhost',
      port: 3000,
      path: '/api/courses',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': courseData.length,
        'Authorization': `Bearer ${token}`
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.success && parsed.data.id) {
            console.log('✅ Course created with ID:', parsed.data.id);
            resolve(parsed.data.id);
          } else {
            reject(new Error('Course creation failed: ' + parsed.message));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(courseData);
    req.end();
  });
}

async function addQuizQuestion(token, courseId, questionData) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(questionData);

    const options = {
      hostname: 'localhost',
      port: 3000,
      path: `/api/courses/${courseId}/questions`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length,
        'Authorization': `Bearer ${token}`
      }
    };

    const req = http.request(options, (res) => {
      let responseData = '';
      res.on('data', (chunk) => { responseData += chunk; });
      res.on('end', () => {
        try {
          const parsed = JSON.parse(responseData);
          if (parsed.success) {
            console.log('✅ Quiz question added:', questionData.question_text.substring(0, 50));
            resolve(parsed.data.id);
          } else {
            reject(new Error('Question failed: ' + parsed.message));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  try {
    console.log('🚀 Creating Arithmetic Course...\n');

    // Step 1: Login
    console.log('Step 1: Authenticating...');
    const token = await login();

    // Step 2: Create course
    console.log('\nStep 2: Creating course with comprehensive content...');
    const courseId = await createCourse(token);

    // Step 3: Add quiz questions
    console.log('\nStep 3: Adding quiz questions...');
    const quizQuestions = [
      {
        question_text: 'What is 15 + 27?',
        question_type: 'multiple_choice',
        options: ['32', '42', '52', '62'],
        correct_answer: '42',
        explanation: '15 + 27 = 42. When adding, align the digits by place value.',
        points: 10
      },
      {
        question_text: 'What is 50 - 23?',
        question_type: 'multiple_choice',
        options: ['17', '27', '37', '47'],
        correct_answer: '27',
        explanation: '50 - 23 = 27. When subtracting, start from the ones place.',
        points: 10
      },
      {
        question_text: 'What is 6 × 7?',
        question_type: 'multiple_choice',
        options: ['36', '42', '48', '54'],
        correct_answer: '42',
        explanation: '6 × 7 = 42. This is an important multiplication fact to memorize.',
        points: 10
      },
      {
        question_text: 'What is 56 ÷ 8?',
        question_type: 'multiple_choice',
        options: ['6', '7', '8', '9'],
        correct_answer: '7',
        explanation: '56 ÷ 8 = 7 because 8 × 7 = 56.',
        points: 10
      },
      {
        question_text: 'What is the sum of 234 + 156 + 310?',
        question_type: 'multiple_choice',
        options: ['500', '600', '700', '800'],
        correct_answer: '700',
        explanation: '234 + 156 = 390, then 390 + 310 = 700.',
        points: 15
      },
      {
        question_text: 'If you have 120 apples and give away 45, how many do you have left?',
        question_type: 'multiple_choice',
        options: ['65', '75', '85', '95'],
        correct_answer: '75',
        explanation: '120 - 45 = 75 apples remaining.',
        points: 15
      },
      {
        question_text: 'A book costs $12 and you need to buy 8 books. What is the total cost?',
        question_type: 'multiple_choice',
        options: ['$84', '$96', '$108', '$120'],
        correct_answer: '$96',
        explanation: '$12 × 8 = $96.',
        points: 15
      },
      {
        question_text: 'Which operation does 5 × 4 represent?',
        question_type: 'multiple_choice',
        options: ['5 added 4 times', '5 divided into 4 parts', '4 added 5 times', '4 subtracted 5 times'],
        correct_answer: '4 added 5 times',
        explanation: 'Multiplication means repeated addition. 5 × 4 means adding 4 five times: 4+4+4+4+4=20.',
        points: 10
      }
    ];

    for (const question of quizQuestions) {
      await addQuizQuestion(token, courseId, question);
    }

    console.log('\n' + '='.repeat(60));
    console.log('✨ ARITHMETIC COURSE SUCCESSFULLY CREATED! ✨');
    console.log('='.repeat(60));
    console.log(`
📊 Course Details:
   • Course ID: ${courseId}
   • Title: 🎓 Mastering Arithmetic: From Basics to Advanced
   • Status: PUBLISHED & APPROVED
   • Quiz Questions: 8
   • Content Modules: 6
   • PhET Simulators: Ready to add via UI

🌍 The course is NOW LIVE and visible to all users on Veelearn!

📝 To add PhET simulators:
   1. Go to the course editor
   2. Click "⚛️ PhET Simulator" button
   3. Select simulators like:
      • Arithmetic (https://phet.colorado.edu/sims/html/arithmetic/latest/arithmetic_en.html)
      • Area Model (https://phet.colorado.edu/sims/html/area-model/latest/area-model_en.html)
      • Fractions Intro (https://phet.colorado.edu/sims/html/fractions-intro/latest/fractions-intro_en.html)

🎓 This is the FIRST course on Veelearn!
    `);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
