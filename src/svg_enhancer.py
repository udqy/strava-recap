"""
Enhance all SVG files with:
1. JetBrains Mono web font
2. Text stroke for better visibility
3. Convert to PNG
"""
import os
import re
import subprocess

SVG_DIR = 'data'

def add_web_font_and_stroke(svg_content):
    """Add web font import and stroke to text elements"""

    # Check if font is already imported
    if '@import url' not in svg_content:
        # Add font import after opening svg tag
        font_style = '''<defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&amp;display=swap');
    </style>
  </defs>

  '''
        # Ensure xmlns is present
        if 'xmlns="http://www.w3.org/2000/svg"' not in svg_content:
            svg_content = svg_content.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" ', 1)

        # Add font style after opening svg tag
        svg_content = re.sub(r'(<svg[^>]*>)', r'\1\n  ' + font_style, svg_content, count=1)

    # Update font-family to include fallback and add stroke
    svg_content = re.sub(
        r'font-family="JetBrains Mono"',
        r'font-family="\'JetBrains Mono\', monospace"',
        svg_content
    )

    # Add stroke to text elements that don't have it
    def add_stroke_to_text(match):
        text_tag = match.group(0)
        # Only add stroke if not already present
        if 'stroke=' not in text_tag and 'fill="#FC4C02"' in text_tag:
            # Add before the closing >
            text_tag = text_tag.replace('>', ' stroke="#FC4C02" stroke-width="0.5">', 1)
        return text_tag

    svg_content = re.sub(r'<text [^>]+>', add_stroke_to_text, svg_content)

    return svg_content

def convert_svg_to_png(svg_file):
    """Convert SVG to PNG using cairosvg or inkscape"""
    png_file = svg_file.replace('.svg', '.png')

    try:
        # Try using cairosvg first (needs to be installed)
        import cairosvg
        cairosvg.svg2png(url=svg_file, write_to=png_file, dpi=300)
        print(f"✓ Converted {os.path.basename(svg_file)} to PNG (cairosvg)")
        return True
    except ImportError:
        # Fallback to inkscape if available
        try:
            result = subprocess.run(
                ['inkscape', svg_file, '--export-type=png', f'--export-filename={png_file}', '--export-dpi=300'],
                capture_output=True,
                check=True
            )
            print(f"✓ Converted {os.path.basename(svg_file)} to PNG (inkscape)")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"✗ Could not convert {os.path.basename(svg_file)} - install cairosvg or inkscape")
            return False

def process_all_svgs():
    """Process all SVG files in data directory"""
    svg_files = [f for f in os.listdir(SVG_DIR) if f.endswith('.svg')]

    print(f"Processing {len(svg_files)} SVG files...\n")

    for svg_file in svg_files:
        filepath = os.path.join(SVG_DIR, svg_file)

        # Read SVG
        with open(filepath, 'r') as f:
            content = f.read()

        # Enhance SVG
        enhanced = add_web_font_and_stroke(content)

        # Write back
        with open(filepath, 'w') as f:
            f.write(enhanced)

        print(f"✓ Enhanced {svg_file}")

        # Convert to PNG
        convert_svg_to_png(filepath)

    print(f"\n✅ All SVGs enhanced and converted!")

if __name__ == "__main__":
    process_all_svgs()
