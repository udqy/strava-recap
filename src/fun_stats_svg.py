import json
from datetime import datetime

class FunStatsSVG:
    def __init__(self):
        with open('data/stats.json', 'r') as f:
            self.stats = json.load(f)
        with open('data/2025_activities.json', 'r') as f:
            self.activities = json.load(f)

    def create_pace_evolution_svg(self):
        """Show how pace improved over time"""
        runs = [a for a in self.activities if a['type'] == 'Run' and a.get('moving_time', 0) > 0]

        # Calculate pace for each run
        paces = []
        for run in runs:
            distance_km = run['distance'] / 1000
            time_min = run['moving_time'] / 60
            if distance_km > 0:
                pace = time_min / distance_km
                date = datetime.fromisoformat(run['start_date_local'].replace('Z', '+00:00'))
                paces.append((date.strftime('%b'), pace))

        if not paces:
            return "No pace data"

        # Get monthly averages
        from collections import defaultdict
        monthly_paces = defaultdict(list)
        for month, pace in paces:
            monthly_paces[month].append(pace)

        avg_paces = [(month, sum(paces)/len(paces)) for month, paces in monthly_paces.items()]

        best_pace = min(p[1] for p in paces)
        worst_pace = max(p[1] for p in paces)

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="150" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    PACE EVOLUTION
  </text>

  <text x="540" y="280" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    Best: {best_pace:.1f} min/km
  </text>

  <text x="540" y="350" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    Average: {self.stats['run_stats']['avg_pace']:.1f} min/km
  </text>

  <text x="540" y="480" font-family="JetBrains Mono" font-size="36" fill="#FC4C02" text-anchor="middle">
    You got {worst_pace - best_pace:.1f} min/km faster!
  </text>

</svg>'''

        with open('data/pace_evolution.svg', 'w') as f:
            f.write(svg)

        return svg

    def create_streaks_svg(self):
        """Show running streaks and consistency"""
        runs = [a for a in self.activities if a['type'] == 'Run']

        # Sort by date
        runs.sort(key=lambda x: x['start_date_local'])

        # Calculate longest streak
        from datetime import datetime, timedelta
        dates = [datetime.fromisoformat(r['start_date_local'].replace('Z', '+00:00')).date() for r in runs]

        longest_streak = 1
        current_streak = 1

        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days <= 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1

        # Count weekend runs
        weekend_runs = sum(1 for d in dates if d.weekday() >= 5)

        # Most active month
        monthly = self.stats['monthly_stats']
        most_active = max(monthly.items(), key=lambda x: x[1]['count'])

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="150" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    CONSISTENCY
  </text>

  <text x="540" y="300" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    Longest streak: {longest_streak} days
  </text>

  <text x="540" y="420" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    Weekend warrior: {weekend_runs} runs
  </text>

  <text x="540" y="540" font-family="JetBrains Mono" font-size="36" fill="#FC4C02" text-anchor="middle">
    Most active: {most_active[0]}
  </text>

  <text x="540" y="600" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    ({most_active[1]['count']} runs, {most_active[1]['distance']:.1f} km)
  </text>

</svg>'''

        with open('data/consistency.svg', 'w') as f:
            f.write(svg)

        return svg

    def create_elevation_svg(self):
        """Fun elevation comparisons"""
        elevation_m = self.stats['run_stats']['elevation_m']

        # Famous mountains/buildings in meters
        comparisons = {
            "Burj Khalifa (Dubai)": 828,
            "Empire State Building": 443,
            "Eiffel Tower": 330,
            "Mt. Everest": 8849
        }

        matches = []
        for landmark, height in comparisons.items():
            if elevation_m >= height:
                times = elevation_m / height
                matches.append((landmark, times))

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="150" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    ELEVATION CLIMBED
  </text>

  <text x="540" y="250" font-family="JetBrains Mono" font-size="48" fill="#FC4C02" text-anchor="middle">
    {elevation_m:.0f} meters
  </text>

'''

        y_pos = 380
        for landmark, times in matches[:3]:
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    = {times:.1f}x {landmark}
  </text>

'''
            y_pos += 100

        svg += '''
</svg>'''

        with open('data/elevation_climb.svg', 'w') as f:
            f.write(svg)

        return svg

if __name__ == "__main__":
    # This file is deprecated - stats moved to other generators
    print("Fun stats generation skipped - using other generators")
