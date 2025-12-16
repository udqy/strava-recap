import json
from datetime import datetime

class ProgressionNarrative:
    def __init__(self):
        with open('data/stats.json', 'r') as f:
            self.stats = json.load(f)
        with open('data/2025_activities.json', 'r') as f:
            self.activities = json.load(f)

    def generate_narrative(self):
        """Generate a paragraph about progression with savage roasts"""
        runs = [a for a in self.activities if a['type'] == 'Run']

        # Get monthly data
        monthly = self.stats['monthly_stats']
        months_with_data = sorted(monthly.keys())

        # Find best and worst months
        best_month = max(monthly.items(), key=lambda x: x[1]['distance'])
        worst_month = min(monthly.items(), key=lambda x: x[1]['distance'])

        # Calculate progression
        first_half = sum(monthly[m]['distance'] for m in months_with_data[:len(months_with_data)//2])
        second_half = sum(monthly[m]['distance'] for m in months_with_data[len(months_with_data)//2:])

        improvement = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0

        # Get pace improvement
        runs_sorted = sorted(runs, key=lambda x: datetime.fromisoformat(x['start_date_local'].replace('Z', '+00:00')))
        early_runs = runs_sorted[:len(runs_sorted)//3]
        late_runs = runs_sorted[-len(runs_sorted)//3:]

        early_avg_pace = sum((r['moving_time']/60) / (r['distance']/1000) for r in early_runs if r['distance'] > 0) / len(early_runs)
        late_avg_pace = sum((r['moving_time']/60) / (r['distance']/1000) for r in late_runs if r['distance'] > 0) / len(late_runs)

        pace_improvement = early_avg_pace - late_avg_pace

        # Generate narrative with harsh roasts
        narrative = f"""September was your peak at {best_month[1]['distance']:.1f}km. Then you got injured and gave your body the perfect excuse to quit. """

        narrative += f"The second half actually saw a {improvement:.0f}% improvement, but let's be real - that's mostly September carrying the entire year. "

        narrative += f"\n\n{worst_month[0]} was your rock bottom at {worst_month[1]['distance']:.1f}km. Even your Uber driver probably logged more distance that month. "

        if pace_improvement > 0:
            narrative += f"\n\nYour pace improved by {pace_improvement:.1f} min/km through the year. Congrats on finally figuring out that legs can move faster than a leisurely stroll. "
        elif pace_improvement < -0.5:
            narrative += f"\n\nYour pace got {abs(pace_improvement):.1f} min/km slower by year end. That injury really exposed how you were barely holding it together. "
        else:
            narrative += f"\n\nYour pace stayed consistent. Consistently mediocre, that is. "

        narrative += f"\n\n416km across {len(runs)} runs. That's {416/len(runs):.1f}km per run - basically a neighborhood jog. Your Strava wrapped looks like someone who runs to the grocery store, not someone training for anything serious."

        return narrative

    def create_narrative_svg(self):
        """Create an SVG with the narrative"""
        narrative = self.generate_narrative()

        # Split narrative into lines for SVG (wrap text)
        words = narrative.split()
        lines = []
        current_line = []
        max_chars = 45

        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) > max_chars:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
            else:
                current_line.append(word)

        if current_line:
            lines.append(' '.join(current_line))

        svg = f'''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="100" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    YOUR YEAR
  </text>

'''

        y_pos = 200
        for line in lines:
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="22" fill="#FC4C02" text-anchor="middle">
    {line}
  </text>

'''
            y_pos += 40

        svg += '''</svg>'''

        with open('data/progression.svg', 'w') as f:
            f.write(svg)

        return svg

if __name__ == "__main__":
    prog = ProgressionNarrative()
    prog.create_narrative_svg()
    print("Generated progression narrative!")
    print("\n" + prog.generate_narrative())
