import json
from datetime import datetime, timedelta
from collections import defaultdict

class ExtraVisualizations:
    def __init__(self):
        with open('data/2025_activities.json', 'r') as f:
            self.activities = json.load(f)

    def create_distance_distribution_svg(self):
        """Show distribution of run distances"""
        runs = [a for a in self.activities if a['type'] == 'Run']

        # Categorize runs by distance
        buckets = {
            "0-3km": 0,
            "3-5km": 0,
            "5-7km": 0,
            "7-10km": 0,
            "10-15km": 0,
            "15-21km": 0,
            "21km+": 0
        }

        for run in runs:
            dist_km = run['distance'] / 1000
            if dist_km < 3:
                buckets["0-3km"] += 1
            elif dist_km < 5:
                buckets["3-5km"] += 1
            elif dist_km < 7:
                buckets["5-7km"] += 1
            elif dist_km < 10:
                buckets["7-10km"] += 1
            elif dist_km < 15:
                buckets["10-15km"] += 1
            elif dist_km < 21:
                buckets["15-21km"] += 1
            else:
                buckets["21km+"] += 1

        # Find max for scaling
        max_count = max(buckets.values())

        # Generate roast based on distribution
        most_common = max(buckets.items(), key=lambda x: x[1])
        roast = ""
        if most_common[0] == "0-3km":
            roast = "Mostly running to the corner store?"
        elif most_common[0] in ["3-5km", "5-7km"]:
            roast = "Playing it safe in the comfort zone"
        elif most_common[0] == "7-10km":
            roast = "The sweet spot of mediocrity"
        else:
            roast = "Actually trying for once"

        svg = f'''<svg width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">
  <text x="540" y="100" font-family="JetBrains Mono" font-size="56" font-weight="bold" fill="#FC4C02" text-anchor="middle">
    RUN DISTRIBUTION
  </text>

  <text x="540" y="170" font-family="JetBrains Mono" font-size="24" fill="#FC4C02" text-anchor="middle">
    {roast}
  </text>

'''

        # Draw bars
        y_pos = 250
        bar_height = 60
        max_bar_width = 700

        for label, count in buckets.items():
            bar_width = (count / max_count * max_bar_width) if max_count > 0 else 0

            svg += f'''  <text x="100" y="{y_pos + bar_height/2 + 8}" font-family="JetBrains Mono" font-size="28" fill="#FC4C02" text-anchor="start">
    {label}
  </text>

  <rect x="300" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="#FC4C02" opacity="0.8" rx="8"/>

  <text x="{310 + bar_width}" y="{y_pos + bar_height/2 + 8}" font-family="JetBrains Mono" font-size="28" fill="#FC4C02" text-anchor="start">
    {count}
  </text>

'''
            y_pos += bar_height + 30

        svg += f'''
  <text x="540" y="{y_pos + 50}" font-family="JetBrains Mono" font-size="24" fill="#FC4C02" text-anchor="middle">
    Total: {len(runs)} runs
  </text>

</svg>'''

        with open('data/distribution.svg', 'w') as f:
            f.write(svg)

        return svg

    def create_calendar_heatmap_svg(self):
        """Create a GitHub-style calendar heatmap"""
        runs = [a for a in self.activities if a['type'] == 'Run']

        # Create dict of date -> distance
        run_dates = {}
        for run in runs:
            date = datetime.fromisoformat(run['start_date_local'].replace('Z', '+00:00')).date()
            dist_km = run['distance'] / 1000
            if date in run_dates:
                run_dates[date] += dist_km
            else:
                run_dates[date] = dist_km

        # Get date range for 2025
        start_date = datetime(2025, 1, 1).date()
        end_date = datetime(2025, 12, 31).date()

        # Find max distance for color scaling
        max_distance = max(run_dates.values()) if run_dates else 1

        # SVG settings
        cell_size = 12
        cell_gap = 3
        weeks_in_year = 53
        days_in_week = 7

        svg_width = weeks_in_year * (cell_size + cell_gap) + 200
        svg_height = days_in_week * (cell_size + cell_gap) + 200

        svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&amp;display=swap');
    </style>
  </defs>

  <!-- Background -->
  <rect width="{svg_width}" height="{svg_height}" fill="#000000" opacity="0.5"/>

  <text x="{svg_width/2}" y="50" font-family="'JetBrains Mono', monospace" font-size="42" font-weight="bold" fill="#FC4C02" text-anchor="middle" stroke="#FC4C02" stroke-width="0.5">
    2025 RUNNING CALENDAR
  </text>

  <!-- Month labels -->
'''

        # Add month labels
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_month = -1
        week_num = 0
        current_date = start_date

        while current_date <= end_date:
            if current_date.month != current_month:
                current_month = current_date.month
                x = 100 + week_num * (cell_size + cell_gap)
                svg += f'''  <text x="{x}" y="100" font-family="JetBrains Mono" font-size="12" fill="#FC4C02" text-anchor="start">
    {months[current_month - 1]}
  </text>

'''
            current_date += timedelta(days=7)
            week_num += 1

        # Day labels
        days = ['M', 'W', 'F']
        for i, day in enumerate([0, 2, 4]):  # Mon, Wed, Fri
            y = 120 + day * (cell_size + cell_gap)
            svg += f'''  <text x="80" y="{y + cell_size}" font-family="JetBrains Mono" font-size="10" fill="#FC4C02" text-anchor="end">
    {days[i]}
  </text>

'''

        # Draw calendar cells
        current_date = start_date
        # Start on the first Monday of the year or before
        while current_date.weekday() != 0:  # 0 = Monday
            current_date -= timedelta(days=1)

        week = 0
        while current_date <= end_date or current_date.weekday() != 0:
            if current_date <= end_date:
                day_of_week = current_date.weekday()
                x = 100 + week * (cell_size + cell_gap)
                y = 120 + day_of_week * (cell_size + cell_gap)

                # Determine color intensity
                if current_date in run_dates:
                    distance = run_dates[current_date]
                    intensity = min(distance / max_distance, 1.0)
                    opacity = 0.3 + (intensity * 0.7)  # Range from 0.3 to 1.0
                    color = "#FC4C02"
                else:
                    color = "#FC4C02"
                    opacity = 0.05

                svg += f'''  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" fill="{color}" opacity="{opacity}" rx="2"/>
'''

            current_date += timedelta(days=1)
            if current_date.weekday() == 0:  # New week
                week += 1

        # Add legend
        legend_y = svg_height - 80
        svg += f'''
  <text x="100" y="{legend_y}" font-family="JetBrains Mono" font-size="14" fill="#FC4C02" text-anchor="start">
    Less
  </text>
'''

        for i in range(5):
            opacity = 0.2 + (i * 0.2)
            x = 150 + i * (cell_size + cell_gap)
            svg += f'''  <rect x="{x}" y="{legend_y - cell_size}" width="{cell_size}" height="{cell_size}" fill="#FC4C02" opacity="{opacity}" rx="2"/>
'''

        svg += f'''  <text x="{150 + 5 * (cell_size + cell_gap) + 10}" y="{legend_y}" font-family="JetBrains Mono" font-size="14" fill="#FC4C02" text-anchor="start">
    More
  </text>

  <!-- Stats -->
  <text x="{svg_width/2}" y="{svg_height - 30}" font-family="JetBrains Mono" font-size="18" fill="#FC4C02" text-anchor="middle">
    {len(run_dates)} days active · {365 - len(run_dates)} days skipped
  </text>

</svg>'''

        with open('data/heatmap.svg', 'w') as f:
            f.write(svg)

        return svg

if __name__ == "__main__":
    viz = ExtraVisualizations()
    viz.create_distance_distribution_svg()
    print("Generated distance distribution SVG!")
    viz.create_calendar_heatmap_svg()
    print("Generated calendar heatmap SVG!")
