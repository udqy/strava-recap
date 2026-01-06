# Strava Recap

Generate your Strava year recap with transparent PNG visualizations.

A common way to share these stats is by overlaying them on top of other pictures. Here's my recap as an example - [Link](https://drive.google.com/file/d/19MAeFGYMrJnxXaDKTvALZAnY1SdCscqK/view?usp=sharing).

## Setup

1. **Install**
   ```bash
   git clone https://github.com/udqy/strava-recap.git
   cd strava-recap
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Get Strava API credentials**
   - Go to https://www.strava.com/settings/api
   - Create an app to get your Client ID and Client Secret

3. **Configure environment**
   - Copy `.env.example` to `.env`
   - Add your Strava credentials:
     ```
     CLIENT_ID=your_client_id
     CLIENT_SECRET=your_client_secret
     ```

4. **Get OAuth tokens**
   - Follow Strava OAuth flow to get access and refresh tokens
   - Copy `tokens.json.template` to `tokens.json`
   - Add your tokens:
     ```json
     {
       "token_type": "Bearer",
       "expires_at": 0,
       "expires_in": 0,
       "access_token": "your_access_token",
       "refresh_token": "your_refresh_token"
     }
     ```

## Usage

**Basic usage:**
```bash
python main.py
```

**With AI analysis:**
```bash
python main.py --ai
```

**With roast mode:**
```bash
python main.py --roast
```

### What it does:
- Fetches all your activities from the current year
- Analyzes your stats across all activity types
- Generates PNG visualizations in the `data/` folder
- Optionally generates AI-powered analysis (with `--ai` or `--roast`)

### AI Features (Optional)

To use AI features, add ONE of these to your `.env`:

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

The app auto-detects which provider to use based on which key is set.

**Flags:**
- `--ai` - Generates thoughtful year review with insights
- `--roast` - Generates sarcastic roast of your year
