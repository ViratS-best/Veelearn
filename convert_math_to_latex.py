#!/usr/bin/env python3
"""
Convert mathematical expressions in massive_course_injection.py to LaTeX format.
This script performs regex-based conversions to wrap math expressions in $...$ delimiters.
"""

import re
import sys

def convert_math_to_latex(content):
    """Convert mathematical patterns to LaTeX format."""
    
    # Track changes
    changes = []
    
    # Pattern 1: Simple equations like E = mc^2, F = ma, etc.
    # Match: Word/letter = expression with numbers/operators
    def convert_simple_equations(text):
        # Pattern: Capital letter or word = expression with math operators
        pattern = r'([A-Z][a-zA-Z]*)\s*=\s*([^<>"\']+?)(?=[\s<,\.]|$)'
        
        def replace_eq(match):
            left = match.group(1)
            right = match.group(2).strip()
            # Check if right side has math content
            if any(c in right for c in '^*/+-×÷√∫∑∏αβγδεθλμπρσφω'):
                return f'${left} = {right}$'
            return match.group(0)
        
        return re.sub(pattern, replace_eq, text)
    
    # Pattern 2: Variable names with subscripts like x_1, x_{n+1}
    def convert_subscripts(text):
        # Pattern: letter_letter or letter_{...}
        pattern = r'\b([a-zA-Z])_([a-zA-Z0-9]|\{[^}]+\})'
        return re.sub(pattern, r'$\1_\2$', text)
    
    # Pattern 3: Exponents like x^2, x^{n+1}
    def convert_exponents(text):
        # Pattern: base ^ exponent
        pattern = r'\b([a-zA-Z0-9])\^(\d+|\{[^}]+\})'
        return re.sub(pattern, r'$\1^\2$', text)
    
    # Pattern 4: Greek letters spelled out
    def convert_greek(text):
        greek_map = {
            r'\balpha\b': r'\\alpha',
            r'\bbeta\b': r'\\beta',
            r'\bgamma\b': r'\\gamma',
            r'\bdelta\b': r'\\delta',
            r'\bepsilon\b': r'\\epsilon',
            r'\bzeta\b': r'\\zeta',
            r'\btheta\b': r'\\theta',
            r'\blambda\b': r'\\lambda',
            r'\bmu\b': r'\\mu',
            r'\bpi\b(?=\s|[^a-zA-Z]|$)': r'\\pi',
            r'\brho\b': r'\\rho',
            r'\bsigma\b': r'\\sigma',
            r'\btau\b': r'\\tau',
            r'\bphi\b': r'\\phi',
            r'\bchi\b': r'\\chi',
            r'\bpsi\b': r'\\psi',
            r'\bomega\b': r'\\omega',
            r'\bGamma\b': r'\\Gamma',
            r'\bDelta\b': r'\\Delta',
            r'\bTheta\b': r'\\Theta',
            r'\bLambda\b': r'\\Lambda',
            r'\bSigma\b': r'\\Sigma',
            r'\bPhi\b': r'\\Phi',
            r'\bPsi\b': r'\\Psi',
            r'\bOmega\b': r'\\Omega',
        }
        for pattern, replacement in greek_map.items():
            text = re.sub(pattern, f'${replacement}$', text, flags=re.IGNORECASE)
        return text
    
    # Pattern 5: Common math operations and symbols
    def convert_symbols(text):
        # sqrt(x) -> $\sqrt{x}$
        text = re.sub(r'sqrt\(([^)]+)\)', r'$\\sqrt{\1}$', text)
        # Sum notation: sum(...) -> $\sum ...$
        text = re.sub(r'\bsum\b', r'$\\sum$', text)
        # Integral notation: integral -> $\int$
        text = re.sub(r'\bintegral\b|\bint\b', r'$\\int$', text, flags=re.IGNORECASE)
        # Product notation
        text = re.sub(r'\bprod\b', r'$\\prod$', text)
        # Infinity
        text = re.sub(r'\binfty\b|\binfinity\b', r'$\\infty$', text, flags=re.IGNORECASE)
        # Common fractions like 1/2, 3/4 when standalone
        text = re.sub(r'\b(\d+)/(\d+)\b(?=\s|[^a-zA-Z0-9_])', r'$\\frac{\1}{\2}$', text)
        return text
    
    # Pattern 6: Math expressions in parentheses with operators
    def convert_parenthetical_math(text):
        # Pattern: (...math expression...)  
        # Look for expressions with multiple math operators inside parens
        pattern = r'\(([^)]*[\^\+\-\*/×÷√∫∑][^)]*)\)'
        
        def replace_paren_math(match):
            inner = match.group(1)
            # Check if it looks like math
            if re.search(r'[0-9a-zA-Z_^\+\-\*/×÷√∫∑]{3,}', inner):
                return f'$({inner})$'
            return match.group(0)
        
        return re.sub(pattern, replace_paren_math, text)
    
    # Pattern 7: Complex expressions like n(n+1)/2
    def convert_complex_expressions(text):
        # Pattern: n(n+1)/2, n^2, etc.
        pattern = r'\b(n|x|y|z|a|b|c|m)\s*\(([^)]+)\)\s*/\s*(\d+)\b'
        return re.sub(pattern, r'$\1(\2)/\3$', text)
    
    # Apply all conversions
    content = convert_simple_equations(content)
    content = convert_subscripts(content)
    content = convert_exponents(content)
    content = convert_greek(content)
    content = convert_symbols(content)
    content = convert_parenthetical_math(content)
    content = convert_complex_expressions(content)
    
    return content

def main():
    input_file = 'massive_course_injection.py'
    output_file = 'massive_course_injection_latex.py'
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Converting math expressions to LaTeX...")
    converted = convert_math_to_latex(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print("✓ Conversion complete!")
    print(f"  Original file: {input_file}")
    print(f"  LaTeX version: {output_file}")
    print("\nPlease review the output and replace the original if satisfied.")

if __name__ == '__main__':
    main()
