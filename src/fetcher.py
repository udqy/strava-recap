import json
import time
import requests
from datetime import datetime
from auth import StravaAuth

class StravaFetcher:
    def __init__(self):
        self.auth = StravaAuth()
        self.access_token = self.auth.refresh_token()
        self.base_url = "https://www.strava.com/api/v3"
    
    def fetch_year_activities(self):
        activities = []
        page = 1
        current_year = datetime.now().year
        jan_1 = int(datetime(current_year, 1, 1).timestamp())

        while True:
            params = {
                'per_page': 200,
                'page': page,
                'after': jan_1
            }

            headers = {'Authorization': f'Bearer {self.access_token}'}
            response = requests.get(f'{self.base_url}/athlete/activities', params=params, headers=headers)

            if response.status_code == 429:
                print("Rate limit hit. Waiting 15 minutes...")
                time.sleep(900)
                continue

            data = response.json()
            if not data:
                break

            # Include ALL activity types
            activities.extend(data)
            page += 1

            print(f"Fetched {len(data)} activities (page {page})")

        # Save to data/
        filename = f'data/{current_year}_activities.json'
        with open(filename, 'w') as f:
            json.dump(activities, f, indent=2)

        print(f"Saved {len(activities)} activities to {filename}")
        return activities

if __name__ == "__main__":
    fetcher = StravaFetcher()
    fetcher.fetch_year_activities()