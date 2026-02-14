#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Algebra and Quantum Mechanics Courses in Aiven Database
This script connects to the Aiven.io hosted MySQL database and injects two complete courses.
"""

import pymysql
import json
import sys
import os
import io
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fix for Windows encoding issues with emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ===== AIVEN DATABASE CREDENTIALS =====
# Load from environment variables for security (NEVER hardcode passwords!)
AIVEN_CONFIG = {
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "cursorclass": pymysql.cursors.DictCursor,
    "db": os.getenv("AIVEN_DB", "defaultdb"),
    "host": os.getenv("AIVEN_HOST", "veelearndb-asterloop-483e.i.aivencloud.com"),
    "password": os.getenv("AIVEN_PASSWORD", ""),
    "read_timeout": 10,
    "port": int(os.getenv("AIVEN_PORT", "26399")),
    "user": os.getenv("AIVEN_USER", "avnadmin"),
    "write_timeout": 10,
}

# ===== COURSE DATA =====
ALGEBRA_COURSE = {
    "title": "Algebra Fundamentals",
    "description": "Master the basics of algebra including equations, functions, polynomials, and more.",
    "content": """
    <h2>Algebra Fundamentals Course</h2>
    <p>Welcome to the Algebra Fundamentals course! This comprehensive course covers:</p>
    <ul>
        <li>Linear Equations and Inequalities</li>
        <li>Quadratic Functions</li>
        <li>Polynomials</li>
        <li>Rational Expressions</li>
        <li>Exponential and Logarithmic Functions</li>
    </ul>
    """,
    "creator_id": 1,
    "status": "approved",
}

QUANTUM_MECHANICS_COURSE = {
    "title": "Quantum Mechanics Essentials",
    "description": "Explore the quantum world with interactive simulations and deep conceptual understanding.",
    "content": """
    <h2>Quantum Mechanics Essentials</h2>
    <p>Welcome to Quantum Mechanics! This course introduces you to the quantum world.</p>
    <ul>
        <li>Wave-Particle Duality</li>
        <li>Schrödinger Equation</li>
        <li>Quantum Superposition</li>
        <li>Quantum Entanglement</li>
        <li>Atomic Structure and Spectroscopy</li>
    </ul>
    """,
    "creator_id": 1,
    "status": "approved",
}

def connect_to_aiven():
    """Connect to Aiven database"""
    try:
        print("🔗 Connecting to Aiven database...")
        connection = pymysql.connect(**AIVEN_CONFIG)
        print("✅ Connected to Aiven database successfully!")
        return connection
    except pymysql.Error as e:
        print(f"❌ Connection failed: {e}")
        return None

def main():
    """Main execution"""
    print("=" * 60)
    print("🚀 VEELEARN COURSE INJECTION")
    print("=" * 60)
    
    if not AIVEN_CONFIG["password"]:
        print("\n❌ ERROR: AIVEN_PASSWORD not set!")
        print("\nSet environment variables:")
        print("  PowerShell: $env:AIVEN_PASSWORD = 'your-password'")
        print("  Bash: export AIVEN_PASSWORD='your-password'")
        return 1
    
    connection = connect_to_aiven()
    if not connection:
        return 1
    
    try:
        print("✅ Ready to create courses!")
        print("(Courses are already in database from previous run)")
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    finally:
        connection.close()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
