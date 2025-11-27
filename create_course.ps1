# PowerShell script to create Arithmetic course

$baseUrl = "http://localhost:3000/api"
$email = "viratsuper6@gmail.com"
$password = "Virat@123"

Write-Host "Creating Arithmetic Course..." -ForegroundColor Cyan

# Step 1: Login
Write-Host "Step 1: Authenticating..." -ForegroundColor Yellow
$loginBody = @{
    email = $email
    password = $password
} | ConvertTo-Json

$loginResponse = Invoke-WebRequest -Uri "$baseUrl/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body $loginBody `
    -ErrorAction Stop

$loginData = $loginResponse.Content | ConvertFrom-Json
$token = $loginData.data.token

Write-Host "Login successful" -ForegroundColor Green

# Step 2: Create course
Write-Host "Step 2: Creating course..." -ForegroundColor Yellow

$courseContent = @"
<h2>Welcome to Arithmetic Mastery!</h2>
<p>Master the fundamentals of arithmetic through interactive learning.</p>

<h3>Course Overview</h3>
<p>Learn:</p>
<ul>
  <li>Number Systems and place value</li>
  <li>Addition and subtraction</li>
  <li>Multiplication and division</li>
  <li>Real-world applications</li>
</ul>

<h3>Module 1: Introduction to Numbers</h3>
<p>Numbers are the foundation. Key topics:</p>
<ul>
  <li>What are numbers and place value</li>
  <li>Comparing and ordering numbers</li>
  <li>Number sequences</li>
</ul>

<h3>Module 2: Addition Fundamentals</h3>
<p>Learn addition:</p>
<ul>
  <li>Single and multi-digit addition</li>
  <li>Addition properties</li>
  <li>Mental math strategies</li>
</ul>

<h3>Module 3: Subtraction Fundamentals</h3>
<p>Master subtraction:</p>
<ul>
  <li>Basic subtraction facts</li>
  <li>Subtraction with borrowing</li>
  <li>Multi-digit subtraction</li>
</ul>

<h3>Module 4: Multiplication Mastery</h3>
<p>Develop multiplication skills:</p>
<ul>
  <li>Multiplication tables</li>
  <li>Multiplication properties</li>
  <li>Multi-digit multiplication</li>
</ul>

<h3>Module 5: Division Strategies</h3>
<p>Understand division:</p>
<ul>
  <li>Basic division facts</li>
  <li>Division with remainders</li>
  <li>Long division</li>
</ul>

<h3>Module 6: Mixed Operations</h3>
<p>Solve real-world problems with multiple operations.</p>

<h3>By the end you will:</h3>
<ul>
  <li>Perform arithmetic fluently</li>
  <li>Understand concepts deeply</li>
  <li>Apply to real situations</li>
  <li>Build confidence</li>
</ul>
"@

$courseBody = @{
    title = "Mastering Arithmetic"
    description = "Comprehensive guide to arithmetic fundamentals through interactive simulations."
    content = $courseContent
    status = "approved"
} | ConvertTo-Json -Depth 10

$courseResponse = Invoke-WebRequest -Uri "$baseUrl/courses" `
    -Method POST `
    -ContentType "application/json" `
    -Headers @{"Authorization" = "Bearer $token"} `
    -Body $courseBody `
    -ErrorAction Stop

$courseData = $courseResponse.Content | ConvertFrom-Json
$courseId = $courseData.data.id

Write-Host "Course created with ID: $courseId" -ForegroundColor Green

# Step 3: Add quiz questions
Write-Host "Step 3: Adding quiz questions..." -ForegroundColor Yellow

$questions = @(
    @{
        question_text = "What is 15 + 27?"
        question_type = "multiple_choice"
        options = @("32", "42", "52", "62")
        correct_answer = "42"
        explanation = "15 plus 27 equals 42."
        points = 10
    },
    @{
        question_text = "What is 50 - 23?"
        question_type = "multiple_choice"
        options = @("17", "27", "37", "47")
        correct_answer = "27"
        explanation = "50 minus 23 equals 27."
        points = 10
    },
    @{
        question_text = "What is 6 times 7?"
        question_type = "multiple_choice"
        options = @("36", "42", "48", "54")
        correct_answer = "42"
        explanation = "6 times 7 equals 42."
        points = 10
    },
    @{
        question_text = "What is 56 divided by 8?"
        question_type = "multiple_choice"
        options = @("6", "7", "8", "9")
        correct_answer = "7"
        explanation = "56 divided by 8 equals 7."
        points = 10
    },
    @{
        question_text = "What is 234 + 156 + 310?"
        question_type = "multiple_choice"
        options = @("500", "600", "700", "800")
        correct_answer = "700"
        explanation = "234 plus 156 plus 310 equals 700."
        points = 15
    },
    @{
        question_text = "If you have 120 apples and give away 45, how many remain?"
        question_type = "multiple_choice"
        options = @("65", "75", "85", "95")
        correct_answer = "75"
        explanation = "120 minus 45 equals 75 apples."
        points = 15
    },
    @{
        question_text = "A book costs 12 dollars and you buy 8 books. What is the total?"
        question_type = "multiple_choice"
        options = @("84", "96", "108", "120")
        correct_answer = "96"
        explanation = "12 times 8 equals 96 dollars."
        points = 15
    },
    @{
        question_text = "What does 5 times 4 mean?"
        question_type = "multiple_choice"
        options = @("5 groups of 4", "5 divided by 4", "4 groups of 5", "4 minus 5")
        correct_answer = "4 groups of 5"
        explanation = "5 times 4 means 4 repeated 5 times."
        points = 10
    }
)

foreach ($q in $questions) {
    $qBody = $q | ConvertTo-Json
    $qResponse = Invoke-WebRequest -Uri "$baseUrl/courses/$courseId/questions" `
        -Method POST `
        -ContentType "application/json" `
        -Headers @{"Authorization" = "Bearer $token"} `
        -Body $qBody `
        -ErrorAction Stop
    
    Write-Host "Added: $($q.question_text)" -ForegroundColor Green
}

Write-Host "`nCourse successfully created!" -ForegroundColor Magenta
Write-Host "Course ID: $courseId" -ForegroundColor Cyan
Write-Host "Status: Published and Approved" -ForegroundColor Green
Write-Host "Questions: 8" -ForegroundColor Green
Write-Host "`nThis is the FIRST course on Veelearn!" -ForegroundColor Yellow
