import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class StravaAuth:
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.tokens_file = 'tokens.json'
        
    def load_tokens(self):
        try:
            with open(self.tokens_file, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def save_tokens(self, tokens):
        with open(self.tokens_file, 'w') as f:
            json.dump(tokens, f, indent=2)
    
    def refresh_token(self):
        tokens = self.load_tokens()
        if not tokens:
            raise Exception("No tokens found. Please authenticate first.")
        
        # Check if token is expired
        if tokens['expires_at'] > time.time():
            return tokens['access_token']
        
        # Refresh token
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': tokens['refresh_token']
        }
        
        response = requests.post('https://www.strava.com/oauth/token', data=data)
        if response.status_code != 200:
            raise Exception(f"Token refresh failed: {response.text}")
        
        new_tokens = response.json()
        self.save_tokens(new_tokens)
        return new_tokens['access_token']