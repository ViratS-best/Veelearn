#!/usr/bin/env python3
"""Script to convert Unicode characters to LaTeX in massive_course_injection.py"""

# Mapping of Unicode characters to LaTeX equivalents
unicode_to_latex = {
    # Superscripts
    '⁰': '^0',
    '¹': '^1',
    '²': '^2',
    '³': '^3',
    '⁴': '^4',
    '⁵': '^5',
    '⁶': '^6',
    '⁷': '^7',
    '⁸': '^8',
    '⁹': '^9',
    'ⁿ': '^n',
    # Subscripts
    '₀': '_0',
    '₁': '_1',
    '₂': '_2',
    '₃': '_3',
    '₄': '_4',
    '₅': '_5',
    '₆': '_6',
    '₇': '_7',
    '₈': '_8',
    '₉': '_9',
    # Greek letters (lowercase)
    'α': '\\alpha',
    'β': '\\beta',
    'γ': '\\gamma',
    'δ': '\\delta',
    'ε': '\\epsilon',
    'ζ': '\\zeta',
    'η': '\\eta',
    'θ': '\\theta',
    'ι': '\\iota',
    'κ': '\\kappa',
    'λ': '\\lambda',
    'μ': '\\mu',
    'ν': '\\nu',
    'ξ': '\\xi',
    'π': '\\pi',
    'ρ': '\\rho',
    'σ': '\\sigma',
    'τ': '\\tau',
    'υ': '\\upsilon',
    'φ': '\\phi',
    'χ': '\\chi',
    'ψ': '\\psi',
    'ω': '\\omega',
    # Greek letters (uppercase)
    'Γ': '\\Gamma',
    'Δ': '\\Delta',
    'Θ': '\\Theta',
    'Λ': '\\Lambda',
    'Ξ': '\\Xi',
    'Π': '\\Pi',
    'Σ': '\\Sigma',
    'Φ': '\\Phi',
    'Ψ': '\\Psi',
    'Ω': '\\Omega',
    # Math symbols
    '×': '\\times',
    '÷': '\\div',
    '±': '\\pm',
    '∓': '\\mp',
    '≤': '\\leq',
    '≥': '\\geq',
    '≠': '\\neq',
    '≈': '\\approx',
    '∼': '\\sim',
    '∞': '\\infty',
    '√': '\\sqrt',
    '∫': '\\int',
    '∂': '\\partial',
    '∇': '\\nabla',
    '∑': '\\sum',
    '∏': '\\prod',
    '∈': '\\in',
    '∉': '\\notin',
    '⊂': '\\subset',
    '⊃': '\\supset',
    '∩': '\\cap',
    '∪': '\\cup',
    '∅': '\\emptyset',
    '∀': '\\forall',
    '∃': '\\exists',
    '∧': '\\wedge',
    '∨': '\\vee',
    '¬': '\\neg',
    '→': '\\rightarrow',
    '←': '\\leftarrow',
    '⇒': '\\Rightarrow',
    '⇐': '\\Leftarrow',
    '↔': '\\leftrightarrow',
    '↑': '\\uparrow',
    '↓': '\\downarrow',
    '…': '...',
    '•': '*',
    '·': '\\cdot',
    '⋅': '\\cdot',
    '′': "'",
    '″': "''",
    '‴': "'''",
    '°': '\\degree',
    'Ω': '\\Omega',
    'ℓ': '\\ell',
    '←': '\\leftarrow',
    '→': '\\rightarrow',
    '↔': '\\leftrightarrow',
    '⇐': '\\Leftarrow',
    '⇒': '\\Rightarrow',
    '⇔': '\\Leftrightarrow',
}

# Special handling for arrows with text
arrow_replacements = [
    ('→', '->'),  # Simple arrow replacement for non-LaTeX contexts
]

def main():
    filepath = r'c:\Users\virat\OneDrive\Documents\Veelearn\Veelearn\massive_course_injection.py'
    
    print("Reading file...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Converting Unicode characters to LaTeX...")
    count = 0
    for char, latex in unicode_to_latex.items():
        if char in content:
            occurrences = content.count(char)
            content = content.replace(char, latex)
            count += occurrences
            print(f"  Replaced {occurrences} occurrences of '{char}' with '{latex}'")
    
    print(f"\nTotal replacements: {count}")
    
    print("Writing file...")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Done!")
    
    # Verify by trying to compile
    print("\nVerifying Python syntax...")
    import py_compile
    try:
        py_compile.compile(filepath, doraise=True)
        print("Syntax check passed!")
    except py_compile.PyCompileError as e:
        print(f"Syntax error: {e}")

if __name__ == '__main__':
    main()
