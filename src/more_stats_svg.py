import json
from datetime import datetime
from collections import Counter

class MoreStatsSVG:
    def __init__(self):
        with open('data/stats.json', 'r') as f:
            self.stats = json.load(f)
        with open('data/2025_activities.json', 'r') as f:
            self.activities = json.load(f)

    def create_calories_svg(self):
        """Show calories burned"""
        runs = [a for a in self.activities if a['type'] == 'Run']

        total_calories = sum(a.get('calories', 0) for a in runs)
        avg_calories = total_calories / len(runs) if runs else 0

        # Fun comparisons
        pizza_slices = total_calories / 285  # ~285 cal per slice
        burgers = total_calories / 540  # ~540 cal per burger

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="150" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    CALORIES BURNED
  </text>

  <text x="540" y="280" font-family="JetBrains Mono" font-size="48" fill="#FC4C02" text-anchor="middle">
    {total_calories:,.0f} calories
  </text>

  <text x="540" y="380" font-family="JetBrains Mono" font-size="36" fill="#FC4C02" text-anchor="middle">
    = {pizza_slices:.0f} pizza slices
  </text>

  <text x="540" y="480" font-family="JetBrains Mono" font-size="36" fill="#FC4C02" text-anchor="middle">
    = {burgers:.0f} burgers
  </text>

  <text x="540" y="600" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    Avg: {avg_calories:.0f} cal/run
  </text>

</svg>'''

        with open('data/calories_burned.svg', 'w') as f:
            f.write(svg)

        return svg

    def create_time_of_day_svg(self):
        """Show preferred running times"""
        runs = [a for a in self.activities if a['type'] == 'Run']

        # Categorize by time of day
        morning = 0  # 5-11am
        afternoon = 0  # 11am-5pm
        evening = 0  # 5pm-9pm
        night = 0  # 9pm-5am

        for run in runs:
            date = datetime.fromisoformat(run['start_date_local'].replace('Z', '+00:00'))
            hour = date.hour

            if 5 <= hour < 11:
                morning += 1
            elif 11 <= hour < 17:
                afternoon += 1
            elif 17 <= hour < 21:
                evening += 1
            else:
                night += 1

        times = [
            ("Morning (5-11am)", morning),
            ("Afternoon (11am-5pm)", afternoon),
            ("Evening (5-9pm)", evening),
            ("Night (9pm-5am)", night)
        ]

        times.sort(key=lambda x: x[1], reverse=True)
        favorite = times[0]

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="150" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    TIME OF DAY
  </text>

  <text x="540" y="280" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    You're a {favorite[0].split()[0]} runner
  </text>

  <text x="540" y="360" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    {favorite[1]} runs in {favorite[0].lower()}
  </text>

'''

        y_pos = 480
        for time_label, count in times[1:]:
            if count > 0:
                svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="28" fill="#FC4C02" text-anchor="middle">
    {time_label}: {count} runs
  </text>

'''
                y_pos += 70

        svg += '''</svg>'''

        with open('data/time_of_day.svg', 'w') as f:
            f.write(svg)

        return svg

    def create_achievements_svg(self):
        """Show fastest times for key distances"""
        runs = [a for a in self.activities if a['type'] == 'Run']

        # Find fastest 5k
        runs_5k = [r for r in runs if 4500 <= r.get('distance', 0) <= 5500]
        if runs_5k:
            fastest_5k = min(runs_5k, key=lambda x: x.get('moving_time', float('inf')))
            fastest_5k_time = fastest_5k['moving_time'] / 60  # minutes
        else:
            fastest_5k_time = None

        # Find fastest 10k
        runs_10k = [r for r in runs if 9500 <= r.get('distance', 0) <= 10500]
        if runs_10k:
            fastest_10k = min(runs_10k, key=lambda x: x.get('moving_time', float('inf')))
            fastest_10k_time = fastest_10k['moving_time'] / 60  # minutes
        else:
            fastest_10k_time = None

        # Find fastest 21k (half marathon)
        runs_21k = [r for r in runs if 20000 <= r.get('distance', 0) <= 22000]
        if runs_21k:
            fastest_21k = min(runs_21k, key=lambda x: x.get('moving_time', float('inf')))
            fastest_21k_time = fastest_21k['moving_time'] / 60  # minutes
        else:
            fastest_21k_time = None

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="150" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    BEST TIMES
  </text>

'''

        y_pos = 300
        if fastest_5k_time:
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    Fastest 5K: {int(fastest_5k_time)}:{int((fastest_5k_time % 1) * 60):02d}
  </text>

'''
            y_pos += 120

        if fastest_10k_time:
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    Fastest 10K: {int(fastest_10k_time)}:{int((fastest_10k_time % 1) * 60):02d}
  </text>

'''
            y_pos += 120

        if fastest_21k_time:
            hours = int(fastest_21k_time / 60)
            mins = int(fastest_21k_time % 60)
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    Fastest 21K: {hours}:{mins:02d}:{int(((fastest_21k_time % 1) * 60)):02d}
  </text>

'''

        svg += '''</svg>'''

        with open('data/achievements.svg', 'w') as f:
            f.write(svg)

        return svg

    def create_weekly_average_svg(self):
        """Show weekly and monthly running stats"""
        runs = [a for a in self.activities if a['type'] == 'Run']

        total_distance_km = sum(a['distance'] / 1000 for a in runs)
        total_weeks = 52  # Full year
        total_months = 12

        avg_km_per_week = total_distance_km / total_weeks
        avg_runs_per_week = len(runs) / total_weeks
        avg_km_per_month = total_distance_km / total_months
        avg_runs_per_month = len(runs) / total_months

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="150" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    AVERAGES
  </text>

  <text x="540" y="280" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    Weekly: {avg_km_per_week:.1f} km
  </text>

  <text x="540" y="360" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    {avg_runs_per_week:.1f} runs/week
  </text>

  <text x="540" y="500" font-family="JetBrains Mono" font-size="42" fill="#FC4C02" text-anchor="middle">
    Monthly: {avg_km_per_month:.1f} km
  </text>

  <text x="540" y="580" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    {avg_runs_per_month:.1f} runs/month
  </text>

</svg>'''

        with open('data/averages.svg', 'w') as f:
            f.write(svg)

        return svg

if __name__ == "__main__":
    more_stats = MoreStatsSVG()
    more_stats.create_time_of_day_svg()
    print("Generated time of day SVG!")
    more_stats.create_achievements_svg()
    print("Generated achievements SVG!")
    more_stats.create_weekly_average_svg()
    print("Generated averages SVG!")
