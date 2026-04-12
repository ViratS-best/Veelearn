#!/usr/bin/env python3
"""
LaTeX Math Converter for massive_course_injection.py
Converts math expressions within HTML content to LaTeX format.
"""

import re

def convert_math_in_html(content):
    """Convert math expressions to LaTeX within HTML content blocks."""
    
    # Pattern to match HTML string blocks: CONTENT = r"""..."""
    # Match from variable name to closing triple quote
    pattern = r'(_CONTENT|_QUESTIONS)\s*=\s*r"""([\s\S]*?)"""(?=\n\w|#|"|$)'
    
    def process_block(match):
        var_name = match.group(1)
        html = match.group(2)
        original = html
        
        # 1. Convert exponents like x^2, E=mc^2
        # Match: letter or number followed by ^ followed by number or letter
        html = re.sub(r'\b([a-zA-Z0-9])\^(\d+|[a-zA-Z])\b', r'$\1^\2$', html)
        
        # 2. Convert simple equations like F = ma, E = mc^2 (when they contain math symbols)
        # Only convert if right side has math operators
        def convert_eq(m):
            left = m.group(1)
            right = m.group(2)
            # Check if right side has math content
            if re.search(r'[\^\+\-\*/×÷√∫∑²³½¼¾αβγδεθλμπρσφω]', right):
                return f'${left} = {right}$'
            return m.group(0)
        
        html = re.sub(r'\b([A-Z][a-zA-Z]{0,2})\s*=\s*([^<>\n]{1,40}?)(?=[\s<,\.]|$)', convert_eq, html)
        
        # 3. Convert subscripts like x_1, x_n
        html = re.sub(r'\b([a-zA-Z])_([a-zA-Z0-9])\b', r'$\1_\2$', html)
        
        # 4. Convert sqrt(x) to \sqrt{x}
        html = re.sub(r'sqrt\(([^)]+)\)', r'$\\sqrt{\1}$', html)
        
        # 5. Convert common fractions like 1/2, 3/4 when standalone
        html = re.sub(r'\b(\d+)/(\d+)\b(?=\s|[^a-zA-Z0-9_])', r'$\\frac{\1}{\2}$', html)
        
        # 6. Convert Greek letters spelled out (word boundaries)
        greek_map = [
            (r'\balpha\b', r'\\alpha'),
            (r'\bbeta\b', r'\\beta'),
            (r'\bgamma\b', r'\\gamma'),
            (r'\bdelta\b', r'\\delta'),
            (r'\bepsilon\b', r'\\epsilon'),
            (r'\btheta\b', r'\\theta'),
            (r'\blambda\b', r'\\lambda'),
            (r'\bmu\b', r'\\mu'),
            (r'(?<![\\$])\bpi\b(?!\w)', r'\\pi'),
            (r'\brho\b', r'\\rho'),
            (r'\bsigma\b', r'\\sigma'),
            (r'\btau\b', r'\\tau'),
            (r'\bphi\b', r'\\phi'),
            (r'\bpsi\b', r'\\psi'),
            (r'\bomega\b', r'\\omega'),
            (r'\bGamma\b', r'\\Gamma'),
            (r'\bDelta\b', r'\\Delta'),
            (r'\bSigma\b', r'\\Sigma'),
            (r'\bPhi\b', r'\\Phi'),
            (r'\bOmega\b', r'\\Omega'),
        ]
        for pat, repl in greek_map:
            html = re.sub(pat, f'${repl}$', html, flags=re.IGNORECASE)
        
        # 7. Convert Unicode math symbols
        html = html.replace('×', r'$\\times$')
        html = html.replace('÷', r'$\\div$')
        html = html.replace('²', r'$^2$')
        html = html.replace('³', r'$^3$')
        html = html.replace('½', r'$\\frac{1}{2}$')
        html = html.replace('¼', r'$\\frac{1}{4}$')
        html = html.replace('¾', r'$\\frac{3}{4}$')
        html = html.replace('∞', r'$\\infty$')
        html = html.replace('∫', r'$\\int$')
        html = html.replace('∑', r'$\\sum$')
        html = html.replace('∮', r'$\\oint$')
        html = html.replace('∇', r'$\\nabla$')
        html = html.replace('∂', r'$\\partial$')
        html = html.replace('±', r'$\\pm$')
        
        # 8. Convert common formulas: n(n+1)/2
        html = re.sub(r'\b(n)\s*\(([^)]+)\)\s*/\s*(\d+)\b', r'$\1(\2)/\3$', html)
        
        # 9. Convert function notation f(x), g(x) when followed by = or math
        html = re.sub(r'\b([fg])\((x|t)\)\s*=\s*([^<>\n]+?)(?=[\s<,\.]|$)', r'$\1(\2) = \3$', html)
        
        # 10. Convert trig functions
        trig_pattern = r'\b(sin|cos|tan|sec|csc|cot|log|ln)\s*\(([^)]+)\)'
        def convert_trig(m):
            func = m.group(1)
            arg = m.group(2)
            return f'$\\\\{func}({arg})$'
        html = re.sub(trig_pattern, convert_trig, html, flags=re.IGNORECASE)
        
        # 11. Convert physics constants and common expressions
        html = re.sub(r'\b9\.8\s*m/s\^2\b', r'$9.8 \\text{ m/s}^2$', html)
        html = re.sub(r'\b3\.14\b', r'$\\pi \\approx 3.14$', html)
        html = re.sub(r'\b2\.718\b', r'$e \\approx 2.718$', html)
        
        # 12. Convert simple arithmetic in steps (like "8 + 2 = 10")
        simple_math = r'\b(\d+)\s*([+\-×÷])\s*(\d+)\s*=\s*(\d+)\b'
        def convert_simple(m):
            a, op, b, c = m.groups()
            latex_op = '\\times' if op == '×' else '\\div' if op == '÷' else op
            return f'${a} {latex_op} {b} = {c}$'
        html = re.sub(simple_math, convert_simple, html)
        
        # Reconstruct the block
        return f'{var_name} = r"""{html}"""'
    
    # Process all HTML content blocks
    result = re.sub(pattern, process_block, content)
    return result

def main():
    input_file = 'massive_course_injection.py'
    output_file = 'massive_course_injection_latex.py'
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Converting math to LaTeX...")
    converted = convert_math_in_html(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print("✓ Conversion complete!")
    
    # Verify syntax
    print("\nVerifying Python syntax...")
    try:
        compile(converted, output_file, 'exec')
        print("✓ Python syntax is valid!")
        print(f"\nOutput: {output_file}")
        print("Review and replace original if satisfied.")
        return 0
    except SyntaxError as e:
        print(f"✗ Syntax error at line {e.lineno}: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
