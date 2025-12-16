# Strava Recap

Generate your Strava year recap with PNG visualizations.

## Setup

1. **Install dependencies**
   ```bash
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

**Both AI features:**
```bash
python main.py --ai --roast
```

### What it does:
- Fetches all your activities from the current year
- Analyzes your stats across all activity types
- Generates PNG visualizations in the `data/` folder
- Optionally generates AI-powered analysis (with `--ai` or `--roast`)

### AI Features (Optional)

To use AI features, add ONE of these to your `.env`:

**OpenAI:**
```
OPENAI_API_KEY=sk-...
```

**Anthropic Claude:**
```
ANTHROPIC_API_KEY=sk-ant-...
```

**Google Gemini:**
```
GOOGLE_API_KEY=...
```

The app auto-detects which provider to use based on which key is set.

**Flags:**
- `--ai` - Generates thoughtful year review with insights
- `--roast` - Generates funny, sarcastic roast of your year

**Models used:**
- OpenAI: GPT-4
- Anthropic: Claude 3.5 Sonnet
- Google: Gemini Pro

## Output

**Standard visualizations** (always generated):
- `recap.png` - Overall stats summary and records
- `by_type.png` - Detailed breakdown by activity type
- `monthly.png` - Monthly progress chart
- `time_analysis.png` - Hour of day and day of week patterns
- `detailed_stats.png` - Distance breakdown and performance metrics

**AI visualizations** (with `--ai` or `--roast`):
- `ai_review.png` - AI-generated year review
- `ai_roast.png` - AI-generated funny roast
