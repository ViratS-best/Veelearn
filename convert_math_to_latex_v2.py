#!/usr/bin/env python3
"""
Convert mathematical expressions in massive_course_injection.py to LaTeX format.
This script only processes content within HTML strings, not Python code.
"""

import re
import sys

def convert_html_content_to_latex(content):
    """Convert math expressions within HTML content to LaTeX."""
    
    # Pattern to match HTML content blocks: CONTENT = r"""..."""
    pattern = r'((?:_CONTENT|_QUESTIONS)\s*=\s*r?"""[\s\S]*?""")'
    
    def process_html_block(match):
        html_content = match.group(1)
        
        # Convert superscripts in HTML like x^2, E=mc^2
        # Use word boundaries to avoid converting code
        html_content = re.sub(
            r'\b([a-zA-Z])\^(\d+|[a-zA-Z])\b',
            r'$\1^\2$',
            html_content
        )
        
        # Convert subscripts like x_1, x_n
        html_content = re.sub(
            r'\b([a-zA-Z])_([a-zA-Z0-9])\b',
            r'$\1_\2$',
            html_content
        )
        
        # Convert simple equations like E = mc^2 (when already partially converted)
        html_content = re.sub(
            r'\b([A-Z][a-zA-Z]{0,2})\s*=\s*([^<>\n$]{1,30})(?=[\s<,\.])',
            lambda m: f'${m.group(1)} = {m.group(2).strip()}$' 
            if any(c in m.group(2) for c in '^*/+-×÷√∫∑²³αβγδεθλμπρσφω') else m.group(0),
            html_content
        )
        
        # Convert sqrt(x) to \sqrt{x}
        html_content = re.sub(
            r'sqrt\(([^)]+)\)',
            r'$\\sqrt{\1}$',
            html_content
        )
        
        # Convert fractions like a/b when they look like math
        html_content = re.sub(
            r'\b(\d+)/(\d+)\b(?=\s*[\s<,\.])(?![^<]*</)',
            r'$\\frac{\1}{\2}$',
            html_content
        )
        
        # Convert Greek letters to LaTeX (spelled out)
        greek_patterns = [
            (r'\balpha\b', r'$\\alpha$'),
            (r'\bbeta\b', r'$\\beta$'),
            (r'\bgamma\b', r'$\\gamma$'),
            (r'\bdelta\b', r'$\\delta$'),
            (r'\bepsilon\b', r'$\\epsilon$'),
            (r'\btheta\b', r'$\\theta$'),
            (r'\blambda\b', r'$\\lambda$'),
            (r'\bmu\b', r'$\\mu$'),
            (r'(?<!\$)\bpi\b(?!\w)', r'$\\pi$'),
            (r'\bsigma\b', r'$\\sigma$'),
            (r'\btau\b', r'$\\tau$'),
            (r'\bphi\b', r'$\\phi$'),
            (r'\bomega\b', r'$\\omega$'),
            (r'\bGamma\b', r'$\\Gamma$'),
            (r'\bDelta\b', r'$\\Delta$'),
            (r'\bSigma\b', r'$\\Sigma$'),
        ]
        for pat, repl in greek_patterns:
            html_content = re.sub(pat, repl, html_content, flags=re.IGNORECASE)
        
        # Convert common math symbols
        html_content = html_content.replace('×', r'$\\times$')
        html_content = html_content.replace('÷', r'$\\div$')
        html_content = html_content.replace('√', r'$\\sqrt{}$')
        html_content = html_content.replace('²', r'$^2$')
        html_content = html_content.replace('³', r'$^3$')
        html_content = html_content.replace('∫', r'$\\int$')
        html_content = html_content.replace('∑', r'$\\sum$')
        html_content = html_content.replace('∏', r'$\\prod$')
        html_content = html_content.replace('∞', r'$\\infty$')
        
        # Convert common formulas: n(n+1)/2
        html_content = re.sub(
            r'\b(n)\s*\(([^)]+)\)\s*/\s*(\d+)\b',
            r'$\1(\2)/\3$',
            html_content
        )
        
        # Convert integrals notation
        html_content = re.sub(
            r'∮([^·]+)·([^=]+)=([^<\n]+)',
            r'$\\oint \1 \\cdot \2 = \3$',
            html_content
        )
        
        return html_content
    
    # Process each HTML content block
    converted = re.sub(pattern, process_html_block, content)
    return converted

def main():
    input_file = 'massive_course_injection.py'
    output_file = 'massive_course_injection_latex.py'
    
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Converting math expressions to LaTeX (HTML content only)...")
    converted = convert_html_content_to_latex(content)
    
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)
    
    print("✓ Conversion complete!")
    print(f"  Original file: {input_file}")
    print(f"  LaTeX version: {output_file}")
    print("\nVerifying Python syntax...")
    
    # Quick syntax check
    try:
        compile(converted, output_file, 'exec')
        print("✓ Python syntax is valid!")
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        return 1
    
    print("\nPlease review the output and replace the original if satisfied.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
