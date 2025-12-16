import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        current_year = datetime.now().year
        with open('data/stats.json', 'r') as f:
            self.stats = json.load(f)
        with open(f'data/{current_year}_activities.json', 'r') as f:
            self.activities = json.load(f)[:50]  # Limit to first 50 for context
        self.year = current_year
        self.font = '"monospace"'
        self.orange = "#FC4C02"
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LLM based on available API keys"""
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        google_key = os.getenv('GOOGLE_API_KEY')

        if openai_key:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-4", temperature=0.7)
        elif anthropic_key:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)
        elif google_key:
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        else:
            raise Exception(
                "No LLM API key found. Please set one of:\n"
                "  - OPENAI_API_KEY\n"
                "  - ANTHROPIC_API_KEY\n"
                "  - GOOGLE_API_KEY"
            )

    def prepare_data_summary(self):
        """Prepare a summary of stats for the LLM"""
        by_type = self.stats.get('by_type', {})

        summary = f"""Year: {self.year}
Total Activities: {self.stats['activity_count']}
Total Distance: {self.stats['total_distance_km']:.1f} km
Total Time: {self.stats['total_time_hours']:.1f} hours
Total Elevation: {self.stats['total_elevation_m']:.0f} m

By Activity Type:
"""
        for activity_type, type_stats in sorted(by_type.items(), key=lambda x: x[1]['distance_km'], reverse=True):
            summary += f"  {activity_type}: {type_stats['count']} activities, {type_stats['distance_km']:.1f} km\n"

        if self.stats.get('longest_activity'):
            longest = self.stats['longest_activity']
            summary += f"\nLongest Activity: {longest['distance']:.2f} km - {longest['name']}\n"

        if self.stats.get('most_elevation'):
            most_elev = self.stats['most_elevation']
            summary += f"Most Elevation: {most_elev['elevation']:.0f} m - {most_elev['name']}\n"

        # Monthly breakdown
        monthly = self.stats.get('monthly_stats', {})
        if monthly:
            summary += "\nMonthly Distance:\n"
            for month in sorted(monthly.keys()):
                summary += f"  {month}: {monthly[month]['distance']:.1f} km ({monthly[month]['count']} activities)\n"

        return summary

    def generate_analysis(self, roast_mode=False):
        """Generate AI analysis of the year"""
        data_summary = self.prepare_data_summary()

        if roast_mode:
            prompt = f"""You are a brutally honest, sarcastic fitness coach analyzing someone's Strava year recap.
Be funny, use roasts and jokes, but keep it light-hearted. Don't be mean, just playfully sarcastic.

Analyze this data and write 3-5 paragraphs roasting their year in review. Focus on:
- Inconsistent training patterns
- Funny observations about their activity types or timing
- Playful jabs at their performance
- End with an encouraging but sarcastic note

Data:
{data_summary}

Write a funny, roast-style year review in 3-5 paragraphs. Keep each paragraph to 2-3 sentences max for readability."""
        else:
            prompt = f"""You are an insightful fitness analyst reviewing someone's Strava year.

Analyze this data and write 3-5 paragraphs about their year in review. Focus on:
- Key achievements and milestones
- Patterns and consistency
- Areas of strength
- Growth opportunities
- Overall year summary

Data:
{data_summary}

Write a thoughtful, encouraging year review in 3-5 paragraphs. Keep each paragraph to 2-3 sentences max for readability."""

        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            raise Exception(f"LLM generation failed: {e}")

    def create_ai_recap_svg(self, roast_mode=False):
        """Create SVG with AI-generated analysis"""
        try:
            analysis = self.generate_analysis(roast_mode)
        except Exception as e:
            print(f"Warning: AI analysis failed: {e}")
            analysis = "AI analysis unavailable. Please check your LLM configuration."

        # Split into paragraphs and wrap text
        paragraphs = [p.strip() for p in analysis.split('\n\n') if p.strip()]

        # Wrap text to fit width
        wrapped_lines = []
        max_chars = 55  # Characters per line

        for para in paragraphs:
            words = para.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= max_chars:
                    current_line += (word + " ")
                else:
                    wrapped_lines.append(current_line.strip())
                    current_line = word + " "
            if current_line:
                wrapped_lines.append(current_line.strip())
            wrapped_lines.append("")  # Empty line between paragraphs

        # Create SVG
        y_pos = 250
        text_elements = []
        for line in wrapped_lines:
            if line:  # Skip empty lines for spacing
                text_elements.append(f'''
  <text x="100" y="{y_pos}" font-family={self.font} font-size="24" fill="{self.orange}">
    {line}
  </text>''')
            y_pos += 40

        title = "AI ROAST" if roast_mode else "AI YEAR REVIEW"

        svg = f'''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
  <!-- Title -->
  <text x="540" y="100" font-family={self.font} font-size="56" font-weight="bold" fill="{self.orange}" text-anchor="middle">
    {title}
  </text>

  <!-- Stats Summary -->
  <text x="540" y="170" font-family={self.font} font-size="24" fill="#FC8C52" text-anchor="middle">
    {self.stats['activity_count']} activities | {self.stats['total_distance_km']:.0f} km | {self.stats['total_time_hours']:.0f} hours
  </text>

  <!-- AI Analysis -->
  {''.join(text_elements)}
</svg>'''

        filename = 'data/ai_roast.svg' if roast_mode else 'data/ai_review.svg'
        with open(filename, 'w') as f:
            f.write(svg)
        return svg

if __name__ == "__main__":
    analyzer = AIAnalyzer()
    analyzer.create_ai_recap_svg(roast_mode=False)
    print("Generated AI recap")
