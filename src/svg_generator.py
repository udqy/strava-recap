import json
from datetime import datetime
from collections import defaultdict

class RecapSVG:
    def __init__(self):
        with open('data/stats.json', 'r') as f:
            self.stats = json.load(f)
        current_year = datetime.now().year
        with open(f'data/{current_year}_activities.json', 'r') as f:
            self.activities = json.load(f)
        self.year = current_year
        self.font = '"monospace"'
        self.orange = "#FC4C02"

    def create_main_recap(self):
        """Create main recap SVG with overall stats"""
        distance = self.stats['total_distance_km']
        time = self.stats['total_time_hours']
        elevation = self.stats['total_elevation_m']
        count = self.stats['activity_count']

        longest = self.stats.get('longest_activity', {})
        most_elev = self.stats.get('most_elevation', {})

        svg = f'''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="540" y="100" font-family={self.font} font-size="64" font-weight="bold" fill="{self.orange}" text-anchor="middle">
    {self.year} STRAVA RECAP
  </text>

  <!-- Main Stats -->
  <text x="100" y="200" font-family={self.font} font-size="36" fill="{self.orange}">
    Total Distance:     {distance:>10.2f} km
  </text>
  <text x="100" y="250" font-family={self.font} font-size="36" fill="{self.orange}">
    Total Activities:   {count:>10}
  </text>
  <text x="100" y="300" font-family={self.font} font-size="36" fill="{self.orange}">
    Total Time:         {time:>10.1f} hrs
  </text>
  <text x="100" y="350" font-family={self.font} font-size="36" fill="{self.orange}">
    Total Elevation:    {elevation:>10.0f} m
  </text>

  <!-- Calculated Stats -->
  <text x="100" y="450" font-family={self.font} font-size="36" fill="#FC8C52">
    Avg per activity:   {distance/count:>10.2f} km
  </text>
  <text x="100" y="500" font-family={self.font} font-size="36" fill="#FC8C52">
    Avg time:           {time/count:>10.1f} hrs
  </text>
  <text x="100" y="550" font-family={self.font} font-size="36" fill="#FC8C52">
    Avg elevation:      {elevation/count:>10.0f} m
  </text>

  <!-- Records -->
  <text x="540" y="700" font-family={self.font} font-size="48" font-weight="bold" fill="{self.orange}" text-anchor="middle">
    RECORDS
  </text>
  <text x="100" y="800" font-family={self.font} font-size="32" fill="{self.orange}">
    Longest: {longest.get('distance', 0):.2f} km - {longest.get('name', 'N/A')[:40]}
  </text>
  <text x="100" y="850" font-family={self.font} font-size="32" fill="{self.orange}">
    Most elevation: {most_elev.get('elevation', 0):.0f} m - {most_elev.get('name', 'N/A')[:40]}
  </text>
</svg>'''

        with open('data/recap.svg', 'w') as f:
            f.write(svg)
        return svg

    def create_by_type_breakdown(self):
        """Create detailed breakdown by activity type"""
        by_type = self.stats.get('by_type', {})

        y_pos = 200
        type_texts = []

        for activity_type, type_stats in sorted(by_type.items(), key=lambda x: x[1]['distance_km'], reverse=True):
            count = type_stats['count']
            dist = type_stats['distance_km']
            time = type_stats['time_hours']
            elev = type_stats['elevation_m']

            type_texts.append(f'''
  <text x="100" y="{y_pos}" font-family={self.font} font-size="40" font-weight="bold" fill="{self.orange}">
    {activity_type}
  </text>
  <text x="150" y="{y_pos + 50}" font-family={self.font} font-size="28" fill="{self.orange}">
    Count:      {count:>6}  |  Distance: {dist:>8.1f} km
  </text>
  <text x="150" y="{y_pos + 90}" font-family={self.font} font-size="28" fill="{self.orange}">
    Time:       {time:>6.1f}h |  Elevation: {elev:>7.0f} m
  </text>
  <text x="150" y="{y_pos + 130}" font-family={self.font} font-size="28" fill="#FC8C52">
    Avg dist:   {dist/count if count > 0 else 0:>6.2f} km  |  Avg time: {time/count if count > 0 else 0:>5.2f}h
  </text>''')
            y_pos += 220

        svg = f'''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="540" y="100" font-family={self.font} font-size="56" font-weight="bold" fill="{self.orange}" text-anchor="middle">
    BY ACTIVITY TYPE
  </text>

  <!-- Activity breakdown -->
  {''.join(type_texts)}
</svg>'''

        with open('data/by_type.svg', 'w') as f:
            f.write(svg)
        return svg

    def create_monthly_chart(self):
        """Create detailed monthly breakdown"""
        monthly = self.stats.get('monthly_stats', {})
        months = sorted(monthly.keys())

        if not months:
            return ""

        max_distance = max(monthly[m]['distance'] for m in months) if months else 1

        bars = []
        x_pos = 80
        bar_width = 70

        for month in months:
            month_name = datetime.fromisoformat(month + "-01").strftime("%b")
            distance = monthly[month]['distance']
            count = monthly[month]['count']
            bar_height = (distance / max_distance) * 600 if max_distance > 0 else 0
            y_pos = 1100 - bar_height

            bars.append(f'''
  <rect x="{x_pos}" y="{y_pos}" width="{bar_width}" height="{bar_height}" fill="{self.orange}" stroke="#000"/>
  <text x="{x_pos + bar_width/2}" y="{y_pos - 30}" font-family={self.font} font-size="22" fill="{self.orange}" text-anchor="middle">
    {distance:.0f}km
  </text>
  <text x="{x_pos + bar_width/2}" y="{y_pos - 5}" font-family={self.font} font-size="18" fill="#FC8C52" text-anchor="middle">
    {count}
  </text>
  <text x="{x_pos + bar_width/2}" y="1150" font-family={self.font} font-size="28" fill="{self.orange}" text-anchor="middle">
    {month_name}
  </text>''')
            x_pos += 85

        svg = f'''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="540" y="100" font-family={self.font} font-size="56" font-weight="bold" fill="{self.orange}" text-anchor="middle">
    MONTHLY PROGRESS
  </text>

  <!-- Bars -->
  {''.join(bars)}

  <!-- Legend -->
  <text x="540" y="1250" font-family={self.font} font-size="24" fill="#FC8C52" text-anchor="middle">
    Top: Distance (km) | Middle: Activity count | Bottom: Month
  </text>
</svg>'''

        with open('data/monthly.svg', 'w') as f:
            f.write(svg)
        return svg

    def create_time_analysis(self):
        """Create time of day and day of week analysis"""
        hour_counts = defaultdict(int)
        dow_counts = defaultdict(int)
        dow_distance = defaultdict(float)

        for activity in self.activities:
            dt = datetime.fromisoformat(activity['start_date_local'].replace('Z', '+00:00'))
            hour = dt.hour
            dow = dt.strftime('%a')

            hour_counts[hour] += 1
            dow_counts[dow] += 1
            dow_distance[dow] += activity.get('distance', 0) / 1000

        # Hour bars
        max_hour_count = max(hour_counts.values()) if hour_counts else 1
        hour_bars = []
        for hour in range(24):
            count = hour_counts.get(hour, 0)
            x = 100 + hour * 40
            height = (count / max_hour_count) * 300 if max_hour_count > 0 else 0
            y = 500 - height
            hour_bars.append(f'''
  <rect x="{x}" y="{y}" width="35" height="{height}" fill="{self.orange}"/>
  <text x="{x + 17.5}" y="520" font-family={self.font} font-size="16" fill="{self.orange}" text-anchor="middle">{hour}</text>''')

        # Day of week
        days_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        dow_bars = []
        y_pos = 700
        for day in days_order:
            count = dow_counts.get(day, 0)
            dist = dow_distance.get(day, 0)
            dow_bars.append(f'''
  <text x="100" y="{y_pos}" font-family={self.font} font-size="32" fill="{self.orange}">
    {day}: {count:>3} activities  {dist:>8.1f} km
  </text>''')
            y_pos += 50

        svg = f'''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="540" y="100" font-family={self.font} font-size="56" font-weight="bold" fill="{self.orange}" text-anchor="middle">
    TIME ANALYSIS
  </text>

  <!-- Hour of day -->
  <text x="540" y="200" font-family={self.font} font-size="40" fill="{self.orange}" text-anchor="middle">
    Hour of Day Distribution
  </text>
  {''.join(hour_bars)}

  <!-- Day of week -->
  <text x="540" y="650" font-family={self.font} font-size="40" fill="{self.orange}" text-anchor="middle">
    Day of Week
  </text>
  {''.join(dow_bars)}
</svg>'''

        with open('data/time_analysis.svg', 'w') as f:
            f.write(svg)
        return svg

    def create_detailed_stats(self):
        """Create detailed statistics page"""
        by_type = self.stats.get('by_type', {})

        # Calculate totals
        total_km = self.stats['total_distance_km']
        total_time = self.stats['total_time_hours']
        total_elev = self.stats['total_elevation_m']

        # Speed stats
        avg_speed = total_km / total_time if total_time > 0 else 0

        # Activity type percentages
        type_lines = []
        y_pos = 250
        for activity_type, type_stats in sorted(by_type.items(), key=lambda x: x[1]['distance_km'], reverse=True):
            pct = (type_stats['distance_km'] / total_km * 100) if total_km > 0 else 0
            bar_width = pct * 8  # Scale for visual
            type_lines.append(f'''
  <rect x="400" y="{y_pos - 25}" width="{bar_width}" height="30" fill="{self.orange}"/>
  <text x="100" y="{y_pos}" font-family={self.font} font-size="28" fill="{self.orange}">
    {activity_type:.<20} {pct:>5.1f}%
  </text>''')
            y_pos += 50

        svg = f'''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="540" y="100" font-family={self.font} font-size="56" font-weight="bold" fill="{self.orange}" text-anchor="middle">
    DETAILED STATISTICS
  </text>

  <!-- Overall metrics -->
  <text x="100" y="200" font-family={self.font} font-size="32" font-weight="bold" fill="{self.orange}">
    Distance Breakdown
  </text>
  {''.join(type_lines)}

  <!-- Performance metrics -->
  <text x="100" y="{y_pos + 100}" font-family={self.font} font-size="32" font-weight="bold" fill="{self.orange}">
    Performance
  </text>
  <text x="100" y="{y_pos + 150}" font-family={self.font} font-size="28" fill="{self.orange}">
    Average speed:      {avg_speed:>8.2f} km/h
  </text>
  <text x="100" y="{y_pos + 190}" font-family={self.font} font-size="28" fill="{self.orange}">
    Elevation gain/km:  {total_elev/total_km if total_km > 0 else 0:>8.1f} m
  </text>
  <text x="100" y="{y_pos + 230}" font-family={self.font} font-size="28" fill="{self.orange}">
    Activities/month:   {self.stats['activity_count']/12:>8.1f}
  </text>
</svg>'''

        with open('data/detailed_stats.svg', 'w') as f:
            f.write(svg)
        return svg

if __name__ == "__main__":
    generator = RecapSVG()
    generator.create_main_recap()
    generator.create_by_type_breakdown()
    generator.create_monthly_chart()
    generator.create_time_analysis()
    generator.create_detailed_stats()
    print("Generated recap SVGs")
