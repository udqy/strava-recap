"""
Replace web font with reliable system monospace fonts
"""
import os
import re

SVG_DIR = 'data'

# Universal monospace font stack that works on all platforms
FONT_STACK = "'Courier New', 'Monaco', 'Menlo', 'Consolas', 'Courier', monospace"

def fix_fonts(svg_content):
    """Replace JetBrains Mono with universal monospace fonts"""

    # Remove web font import
    svg_content = re.sub(r'<defs>\s*<style>\s*@import url\([^)]+\);\s*</style>\s*</defs>', '', svg_content)

    # Replace font-family declarations
    svg_content = re.sub(
        r'font-family="[^"]*"',
        f'font-family="{FONT_STACK}"',
        svg_content
    )

    return svg_content

def process_all_svgs():
    """Fix fonts in all SVG files"""
    svg_files = [f for f in os.listdir(SVG_DIR) if f.endswith('.svg')]

    print(f"Fixing fonts in {len(svg_files)} SVG files...\n")

    for svg_file in svg_files:
        filepath = os.path.join(SVG_DIR, svg_file)

        with open(filepath, 'r') as f:
            content = f.read()

        fixed = fix_fonts(content)

        with open(filepath, 'w') as f:
            f.write(fixed)

        print(f"✓ Fixed {svg_file}")

    print(f"\n✅ All fonts fixed to universal monospace!")

if __name__ == "__main__":
    process_all_svgs()
