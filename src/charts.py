import json
from datetime import datetime

class ChartGenerator:
    def __init__(self):
        with open('data/stats.json', 'r') as f:
            self.stats = json.load(f)
    
    def create_monthly_chart(self):
        monthly_stats = self.stats['monthly_stats']
        
        # Get max distance for scaling
        max_distance = max([month['distance'] for month in monthly_stats.values()] + [1])
        
        # Chart dimensions
        width, height = 1080, 800
        margin = 100
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Bar width
        months = sorted(monthly_stats.keys())
        bar_width = chart_width / len(months) * 0.8
        bar_spacing = chart_width / len(months)
        
        # Generate bars
        bars = []
        for i, month in enumerate(months):
            distance = monthly_stats[month]['distance']
            bar_height = (distance / max_distance) * chart_height
            x = margin + i * bar_spacing + (bar_spacing - bar_width) / 2
            y = margin + chart_height - bar_height
            
            bars.append(f'''
  <rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="#FC4C02" opacity="0.9" rx="8"/>
  <text x="{x + bar_width/2}" y="{y - 10}" font-family="JetBrains Mono" font-size="24" fill="#FC4C02" text-anchor="middle">
    {distance:.1f}km
  </text>
  <text x="{x + bar_width/2}" y="{margin + chart_height + 40}" font-family="JetBrains Mono" font-size="20" fill="#FC4C02" text-anchor="middle">
    {datetime.strptime(month, '%Y-%m').strftime('%b')}
  </text>''')

        svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="{width//2}" y="60" font-family="JetBrains Mono" font-size="48" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    MONTHLY DISTANCE
  </text>

  <!-- Chart area -->
  <rect x="{margin}" y="{margin}" width="{chart_width}" height="{chart_height}" fill="none" stroke="#FC4C02" stroke-width="2" opacity="0.3"/>

  <!-- Bars -->
  {''.join(bars)}

  <!-- Y-axis labels -->
  <text x="{margin - 20}" y="{margin}" font-family="JetBrains Mono" font-size="20" fill="#FC4C02" text-anchor="end">
    {max_distance:.0f}km
  </text>
  <text x="{margin - 20}" y="{margin + chart_height}" font-family="JetBrains Mono" font-size="20" fill="#FC4C02" text-anchor="end">
    0km
  </text>

</svg>'''
        
        with open('data/monthly_chart.svg', 'w') as f:
            f.write(svg)
        return svg

if __name__ == "__main__":
    chart = ChartGenerator()
    chart.create_monthly_chart()
    print("Generated monthly distance chart!")