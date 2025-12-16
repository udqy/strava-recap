import json

class KudosSVG:
    def __init__(self):
        try:
            with open('data/kudos_data.json', 'r') as f:
                self.kudos_data = json.load(f)
        except FileNotFoundError:
            print("Kudos data not found. Run kudos_fetcher.py first.")
            self.kudos_data = None

    def create_top_supporters_svg(self):
        """Create SVG showing top kudos givers"""
        if not self.kudos_data:
            return "No kudos data available"

        top_givers = self.kudos_data['top_givers'][:4]  # Top 4
        total_kudos = self.kudos_data['total_kudos']

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#FC4C02;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF6B35;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="1080" height="1350" fill="url(#bg)"/>

  <!-- Title -->
  <text x="540" y="150" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="white" text-anchor="middle">
    TOP SUPPORTERS
  </text>

  <!-- Subtitle -->
  <text x="540" y="220" font-family="JetBrains Mono" font-size="28" fill="white" text-anchor="middle" opacity="0.9">
    These people gave you the most kudos
  </text>

  <!-- Total kudos -->
  <text x="540" y="280" font-family="JetBrains Mono" font-size="32" fill="white" text-anchor="middle" opacity="0.8">
    {total_kudos} total kudos received
  </text>

  <!-- Top supporters list -->
'''

        y_pos = 400
        for idx, giver in enumerate(top_givers):
            name = giver['name']
            count = giver['count']

            # Medal/Position circle
            svg += f'''  <circle cx="180" cy="{y_pos - 20}" r="40" fill="white" opacity="0.2"/>
  <text x="180" y="{y_pos - 10}" font-family="JetBrains Mono" font-size="32" font-weight="bold" fill="white" text-anchor="middle">
    {idx + 1}
  </text>

  <!-- Name -->
  <text x="270" y="{y_pos - 10}" font-family="JetBrains Mono" font-size="36" font-weight="bold" fill="white" text-anchor="start">
    {name}
  </text>

  <!-- Kudos count -->
  <text x="900" y="{y_pos - 10}" font-family="JetBrains Mono" font-size="36" fill="white" text-anchor="end" opacity="0.9">
    {count} kudos
  </text>

  <!-- Divider -->
  <line x1="180" y1="{y_pos + 40}" x2="900" y2="{y_pos + 40}" stroke="white" stroke-width="1" opacity="0.3"/>

'''
            y_pos += 180

        svg += '''  <!-- Decorative elements -->
  <circle cx="200" cy="200" r="60" fill="white" opacity="0.1"/>
  <circle cx="880" cy="300" r="80" fill="white" opacity="0.1"/>

</svg>'''

        with open('data/top_supporters.svg', 'w') as f:
            f.write(svg)

        return svg

if __name__ == "__main__":
    kudos_svg = KudosSVG()
    kudos_svg.create_top_supporters_svg()
    print("Generated top supporters SVG!")
