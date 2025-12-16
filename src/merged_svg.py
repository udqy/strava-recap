import json

class MergedSVG:
    def __init__(self):
        with open('data/stats.json', 'r') as f:
            self.stats = json.load(f)

    def create_recap_perspective_svg(self):
        """Merge 2025 Recap and Perspective into one SVG"""
        # Recap data
        distance = self.stats['run_stats']['distance_km']
        time = self.stats['run_stats']['time_hours']
        elevation = self.stats['run_stats']['elevation_m']
        runs = self.stats['run_stats']['count']
        avg_pace = self.stats['run_stats']['avg_pace']

        # Distance comparisons
        cities = {
            "Mumbai to Pune": 150,
            "Half Marathon": 21.1,
            "Full Marathon": 42.2
        }

        dist_comparisons = []
        for city, city_distance in cities.items():
            if distance >= city_distance:
                times = distance / city_distance
                dist_comparisons.append((city, times))

        # Elevation comparisons
        landmarks = {
            "Burj Khalifa": 828,
            "Eiffel Tower": 330
        }

        elev_comparisons = []
        for landmark, height in landmarks.items():
            if elevation >= height:
                times = elevation / height
                elev_comparisons.append((landmark, times))

        svg = f'''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="540" y="150" font-family="JetBrains Mono" font-size="64" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    2025 STRAVA RECAP
  </text>

  <!-- Main Stats -->
  <text x="540" y="280" font-family="JetBrains Mono" font-size="48" fill="#FC4C02" text-anchor="middle">
    {distance:.1f} km
  </text>

  <text x="540" y="350" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    {time:.1f} hours · {runs} runs
  </text>

  <text x="540" y="420" font-family="JetBrains Mono" font-size="32" fill="#FC4C02" text-anchor="middle">
    {elevation:.0f}m elevation
  </text>

  <text x="540" y="480" font-family="JetBrains Mono" font-size="28" fill="#FC4C02" text-anchor="middle">
    Avg pace: {avg_pace:.1f} min/km
  </text>

  <!-- Divider -->
  <line x1="200" y1="560" x2="880" y2="560" stroke="#FC4C02" stroke-width="2" opacity="0.3"/>

  <!-- Perspective Title -->
  <text x="540" y="640" font-family="JetBrains Mono" font-size="48" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    PERSPECTIVE
  </text>

  <!-- Distance Perspective -->
  <text x="540" y="730" font-family="JetBrains Mono" font-size="36" fill="#FC4C02" text-anchor="middle">
    Distance:
  </text>

'''

        y_pos = 800
        for city, times in dist_comparisons[:2]:
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="28" fill="#FC4C02" text-anchor="middle">
    = {times:.1f}x {city}
  </text>

'''
            y_pos += 60

        svg += f'''
  <!-- Elevation Perspective -->
  <text x="540" y="{y_pos + 60}" font-family="JetBrains Mono" font-size="36" fill="#FC4C02" text-anchor="middle">
    Elevation:
  </text>

'''

        y_pos += 130
        for landmark, times in elev_comparisons[:2]:
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="28" fill="#FC4C02" text-anchor="middle">
    = {times:.1f}x {landmark}
  </text>

'''
            y_pos += 60

        svg += '''</svg>'''

        with open('data/recap.svg', 'w') as f:
            f.write(svg)

        return svg

    def create_stats_performance_svg(self):
        """Merge Averages and Best Times into one SVG"""
        runs = []
        with open('data/2025_activities.json', 'r') as f:
            import json
            activities = json.load(f)
            runs = [a for a in activities if a['type'] == 'Run']

        # Averages
        total_distance_km = sum(a['distance'] / 1000 for a in runs)
        total_weeks = 52
        total_months = 12

        avg_km_per_week = total_distance_km / total_weeks
        avg_runs_per_week = len(runs) / total_weeks
        avg_km_per_month = total_distance_km / total_months
        avg_runs_per_month = len(runs) / total_months

        # Best times
        runs_5k = [r for r in runs if 4500 <= r.get('distance', 0) <= 5500]
        fastest_5k_time = None
        if runs_5k:
            fastest_5k = min(runs_5k, key=lambda x: x.get('moving_time', float('inf')))
            fastest_5k_time = fastest_5k['moving_time'] / 60

        runs_10k = [r for r in runs if 9500 <= r.get('distance', 0) <= 10500]
        fastest_10k_time = None
        if runs_10k:
            fastest_10k = min(runs_10k, key=lambda x: x.get('moving_time', float('inf')))
            fastest_10k_time = fastest_10k['moving_time'] / 60

        runs_21k = [r for r in runs if 20000 <= r.get('distance', 0) <= 22000]
        fastest_21k_time = None
        if runs_21k:
            fastest_21k = min(runs_21k, key=lambda x: x.get('moving_time', float('inf')))
            fastest_21k_time = fastest_21k['moving_time'] / 60

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="120" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    AVERAGES
  </text>

  <text x="540" y="230" font-family="JetBrains Mono" font-size="38" fill="#FC4C02" text-anchor="middle">
    Weekly: {avg_km_per_week:.1f} km
  </text>

  <text x="540" y="290" font-family="JetBrains Mono" font-size="28" fill="#FC4C02" text-anchor="middle">
    {avg_runs_per_week:.1f} runs/week
  </text>

  <text x="540" y="390" font-family="JetBrains Mono" font-size="38" fill="#FC4C02" text-anchor="middle">
    Monthly: {avg_km_per_month:.1f} km
  </text>

  <text x="540" y="450" font-family="JetBrains Mono" font-size="28" fill="#FC4C02" text-anchor="middle">
    {avg_runs_per_month:.1f} runs/month
  </text>

  <!-- Divider -->
  <line x1="200" y1="530" x2="880" y2="530" stroke="#FC4C02" stroke-width="2" opacity="0.3"/>

  <text x="540" y="620" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    BEST TIMES
  </text>

'''

        y_pos = 720
        if fastest_5k_time:
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="38" fill="#FC4C02" text-anchor="middle">
    5K: {int(fastest_5k_time)}:{int((fastest_5k_time % 1) * 60):02d}
  </text>

'''
            y_pos += 90

        if fastest_10k_time:
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="38" fill="#FC4C02" text-anchor="middle">
    10K: {int(fastest_10k_time)}:{int((fastest_10k_time % 1) * 60):02d}
  </text>

'''
            y_pos += 90

        if fastest_21k_time:
            hours = int(fastest_21k_time / 60)
            mins = int(fastest_21k_time % 60)
            svg += f'''  <text x="540" y="{y_pos}" font-family="JetBrains Mono" font-size="38" fill="#FC4C02" text-anchor="middle">
    21K: {hours}:{mins:02d}:{int(((fastest_21k_time % 1) * 60)):02d}
  </text>

'''

        svg += '''</svg>'''

        with open('data/performance.svg', 'w') as f:
            f.write(svg)

        return svg

if __name__ == "__main__":
    merged = MergedSVG()
    merged.create_recap_perspective_svg()
    print("Generated merged recap + perspective SVG!")
    merged.create_stats_performance_svg()
    print("Generated merged averages + best times SVG!")
