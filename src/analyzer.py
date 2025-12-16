import json
from datetime import datetime
from collections import defaultdict

class StravaAnalyzer:
    def __init__(self):
        current_year = datetime.now().year
        with open(f'data/{current_year}_activities.json', 'r') as f:
            self.activities = json.load(f)

    def calculate_stats(self):
        stats = {
            'total_distance_km': 0,
            'total_time_hours': 0,
            'total_elevation_m': 0,
            'activity_count': len(self.activities),
            'monthly_stats': defaultdict(lambda: {'distance': 0, 'count': 0}),
            'by_type': defaultdict(lambda: {
                'distance_km': 0,
                'time_hours': 0,
                'elevation_m': 0,
                'count': 0
            }),
            'longest_activity': None,
            'most_elevation': None
        }

        for activity in self.activities:
            distance_m = activity.get('distance', 0)
            time_s = activity.get('moving_time', 0)
            elevation_m = activity.get('total_elevation_gain', 0)
            activity_type = activity.get('type', 'Unknown')

            # Convert to km and hours
            distance_km = distance_m / 1000
            time_hours = time_s / 3600

            stats['total_distance_km'] += distance_km
            stats['total_time_hours'] += time_hours
            stats['total_elevation_m'] += elevation_m

            # Dynamic stats by activity type
            stats['by_type'][activity_type]['distance_km'] += distance_km
            stats['by_type'][activity_type]['time_hours'] += time_hours
            stats['by_type'][activity_type]['elevation_m'] += elevation_m
            stats['by_type'][activity_type]['count'] += 1

            # Track longest activity overall
            if stats['longest_activity'] is None or distance_km > stats['longest_activity']['distance']:
                stats['longest_activity'] = {
                    'name': activity['name'],
                    'distance': distance_km,
                    'date': activity['start_date_local'],
                    'type': activity_type
                }

            # Track most elevation gain
            if stats['most_elevation'] is None or elevation_m > stats['most_elevation']['elevation']:
                stats['most_elevation'] = {
                    'name': activity['name'],
                    'elevation': elevation_m,
                    'date': activity['start_date_local'],
                    'type': activity_type
                }

            # Monthly stats
            month = datetime.fromisoformat(activity['start_date_local'].replace('Z', '+00:00')).strftime('%Y-%m')
            stats['monthly_stats'][month]['distance'] += distance_km
            stats['monthly_stats'][month]['count'] += 1

        return stats
    
    def save_stats(self):
        stats = self.calculate_stats()
        with open('data/stats.json', 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        return stats

if __name__ == "__main__":
    analyzer = StravaAnalyzer()
    stats = analyzer.save_stats()
    print(f"Total Distance: {stats['total_distance_km']:.1f} km")
    print(f"Total Time: {stats['total_time_hours']:.1f} hours")
    print(f"Total Elevation: {stats['total_elevation_m']:.0f} m")
    print(f"Total Activities: {stats['activity_count']}")
    print("\nBy Activity Type:")
    for activity_type, type_stats in stats['by_type'].items():
        print(f"  {activity_type}: {type_stats['count']} activities, {type_stats['distance_km']:.1f} km")