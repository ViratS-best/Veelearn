#!/usr/bin/env python3
"""
IndexNow URL Submission Script for Veelearn.org
Submits up to 100 URLs to IndexNow API for indexing
"""

import requests
import json

# Configuration
API_KEY = "9ed8a332259e4110bd7fc4705f539dc5"
HOST = "veelearn.org"
KEY_LOCATION = f"https://{HOST}/{API_KEY}.txt"
API_ENDPOINT = "https://api.indexnow.org/indexnow"

# All website URLs to index
URLS = [
    # Main pages
    f"https://{HOST}/",
    f"https://{HOST}/index.html",
    f"https://{HOST}/blog.html",
    f"https://{HOST}/chemistry.html",
    f"https://{HOST}/course-viewer.html",
    f"https://{HOST}/faq.html",
    f"https://{HOST}/faq-chemistry.html",
    f"https://{HOST}/faq-math.html",
    f"https://{HOST}/faq-physics.html",
    f"https://{HOST}/for-students.html",
    f"https://{HOST}/for-teachers.html",
    f"https://{HOST}/math.html",
    f"https://{HOST}/parent-dashboard.html",
    f"https://{HOST}/parent-signup.html",
    f"https://{HOST}/physics.html",
    f"https://{HOST}/school-admin-dashboard.html",
    f"https://{HOST}/school-admin-signup.html",
    f"https://{HOST}/simulator-creator.html",
    f"https://{HOST}/simulator-detail.html",
    f"https://{HOST}/simulator-execute.html",
    f"https://{HOST}/simulator-marketplace.html",
    f"https://{HOST}/simulator-studio.html",
    f"https://{HOST}/simulator-view.html",
    f"https://{HOST}/simulators.html",
    f"https://{HOST}/student-dashboard.html",
    f"https://{HOST}/student-signup.html",
    f"https://{HOST}/teacher-dashboard.html",
    f"https://{HOST}/teacher-signup.html",
    f"https://{HOST}/visual-simulator.html",
    f"https://{HOST}/block-simulator.html",
    
    # Blog pages (43 files)
    f"https://{HOST}/blog/best-of-chemistry-learning-resources.html",
    f"https://{HOST}/blog/best-of-math-learning-tools.html",
    f"https://{HOST}/blog/best-of-online-education-platforms.html",
    f"https://{HOST}/blog/best-of-physics-learning-platforms.html",
    f"https://{HOST}/blog/best-of-stem-simulations.html",
    f"https://{HOST}/blog/how-to-balance-chemical-equations.html",
    f"https://{HOST}/blog/how-to-calculate-gpa.html",
    f"https://{HOST}/blog/how-to-calculate-physics-problems.html",
    f"https://{HOST}/blog/how-to-solve-algebra-equations.html",
    f"https://{HOST}/blog/how-to-solve-calculus-problems.html",
    f"https://{HOST}/blog/how-to-study-for-science-exams.html",
    f"https://{HOST}/blog/stem-education-statistics-2026.html",
    f"https://{HOST}/blog/what-is-artificial-intelligence.html",
    f"https://{HOST}/blog/what-is-astronomy.html",
    f"https://{HOST}/blog/what-is-biochemistry.html",
    f"https://{HOST}/blog/what-is-cell-biology.html",
    f"https://{HOST}/blog/what-is-differential-equations.html",
    f"https://{HOST}/blog/what-is-dna.html",
    f"https://{HOST}/blog/what-is-ecology.html",
    f"https://{HOST}/blog/what-is-electricity.html",
    f"https://{HOST}/blog/what-is-geometry.html",
    f"https://{HOST}/blog/what-is-kinetic-energy.html",
    f"https://{HOST}/blog/what-is-light.html",
    f"https://{HOST}/blog/what-is-linear-algebra.html",
    f"https://{HOST}/blog/what-is-magnetism.html",
    f"https://{HOST}/blog/what-is-newtons-first-law.html",
    f"https://{HOST}/blog/what-is-newtons-second-law.html",
    f"https://{HOST}/blog/what-is-organic-chemistry.html",
    f"https://{HOST}/blog/what-is-ph.html",
    f"https://{HOST}/blog/what-is-photosynthesis.html",
    f"https://{HOST}/blog/what-is-probability.html",
    f"https://{HOST}/blog/what-is-quantum-mechanics.html",
    f"https://{HOST}/blog/what-is-robotics.html",
    f"https://{HOST}/blog/what-is-sound.html",
    f"https://{HOST}/blog/what-is-statistics.html",
    f"https://{HOST}/blog/what-is-the-best-way-to-learn-physics.html",
    f"https://{HOST}/blog/what-is-the-periodic-table.html",
    f"https://{HOST}/blog/what-is-the-pythagorean-theorem.html",
    f"https://{HOST}/blog/what-is-the-quadratic-formula.html",
    f"https://{HOST}/blog/what-is-the-scientific-method.html",
    f"https://{HOST}/blog/what-is-thermodynamics.html",
    f"https://{HOST}/blog/what-is-trigonometry.html",
    f"https://{HOST}/blog/what-is-waves.html",
    
    # Guide pages (10 files)
    f"https://{HOST}/guides/how-to-balance-chemical-equations.html",
    f"https://{HOST}/guides/how-to-calculate-ph.html",
    f"https://{HOST}/guides/how-to-learn-physics-effectively.html",
    f"https://{HOST}/guides/how-to-solve-algebra-equations.html",
    f"https://{HOST}/guides/how-to-solve-calculus-problems.html",
    f"https://{HOST}/guides/how-to-solve-physics-problems.html",
    f"https://{HOST}/guides/how-to-study-for-exams.html",
    f"https://{HOST}/guides/how-to-understand-newtons-laws.html",
    f"https://{HOST}/guides/how-to-use-periodic-table.html",
    f"https://{HOST}/guides/how-to-use-phet-simulations.html",
]

def submit_to_indexnow():
    """Submit URLs to IndexNow API"""
    
    # Limit to 100 URLs as requested
    urls_to_submit = URLS[:100]
    
    print(f"Submitting {len(urls_to_submit)} URLs to IndexNow...")
    print(f"Host: {HOST}")
    print(f"Key: {API_KEY}")
    print(f"Key Location: {KEY_LOCATION}")
    print("-" * 60)
    
    # Prepare payload
    payload = {
        "host": HOST,
        "key": API_KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls_to_submit
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    
    try:
        # Submit to IndexNow API
        response = requests.post(API_ENDPOINT, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ SUCCESS: URLs submitted successfully!")
            print(f"Total URLs submitted: {len(urls_to_submit)}")
        elif response.status_code == 202:
            print("\n⏳ ACCEPTED: URLs received. Key validation pending.")
        elif response.status_code == 400:
            print("\n❌ ERROR: Bad request - Invalid format")
        elif response.status_code == 403:
            print("\n❌ ERROR: Forbidden - Key not valid")
        elif response.status_code == 422:
            print("\n❌ ERROR: Unprocessable Entity - URLs don't belong to host or key mismatch")
        elif response.status_code == 429:
            print("\n❌ ERROR: Too Many Requests - Potential spam")
        else:
            print(f"\n❌ ERROR: Unexpected status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: Request failed: {e}")
    
    print("\n" + "=" * 60)
    print("URLs submitted:")
    for i, url in enumerate(urls_to_submit, 1):
        print(f"{i}. {url}")

if __name__ == "__main__":
    submit_to_indexnow()
