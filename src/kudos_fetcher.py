import json
import requests
import time
from collections import Counter
from auth import StravaAuth

class KudosFetcher:
    def __init__(self):
        self.auth = StravaAuth()
        self.access_token = self.auth.refresh_token()
        self.base_url = "https://www.strava.com/api/v3"

        with open('data/2025_activities.json', 'r') as f:
            self.activities = json.load(f)

    def fetch_activity_kudos(self, activity_id):
        """Fetch kudos for a specific activity"""
        url = f"{self.base_url}/activities/{activity_id}/kudos"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limited, waiting...")
            time.sleep(60)
            return self.fetch_activity_kudos(activity_id)
        else:
            print(f"Failed to fetch kudos for activity {activity_id}: {response.status_code}")
            return []

    def get_top_kudos_givers(self, limit=10):
        """Get the people who gave the most kudos"""
        kudos_counter = Counter()

        # Only process activities with kudos
        activities_with_kudos = [a for a in self.activities if a.get('kudos_count', 0) > 0]

        print(f"Fetching kudos from {len(activities_with_kudos)} activities...")

        for idx, activity in enumerate(activities_with_kudos):
            activity_id = activity['id']
            kudos_count = activity.get('kudos_count', 0)

            if kudos_count > 0:
                print(f"Fetching kudos for activity {idx+1}/{len(activities_with_kudos)}...")
                kudos_list = self.fetch_activity_kudos(activity_id)

                for kudo in kudos_list:
                    name = f"{kudo.get('firstname', '')} {kudo.get('lastname', '')}"
                    kudos_counter[name] += 1

                # Be nice to the API
                time.sleep(0.5)

        # Get top givers
        top_givers = kudos_counter.most_common(limit)

        # Save to file
        kudos_data = {
            'top_givers': [{'name': name, 'count': count} for name, count in top_givers],
            'total_kudos': sum(kudos_counter.values()),
            'unique_people': len(kudos_counter)
        }

        with open('data/kudos_data.json', 'w') as f:
            json.dump(kudos_data, f, indent=2)

        return kudos_data

if __name__ == "__main__":
    fetcher = KudosFetcher()
    data = fetcher.get_top_kudos_givers(limit=10)
    print(f"\nTop kudos givers:")
    for giver in data['top_givers'][:4]:
        print(f"  {giver['name']}: {giver['count']} kudos")
    print(f"\nTotal kudos: {data['total_kudos']}")
    print(f"Unique people: {data['unique_people']}")
