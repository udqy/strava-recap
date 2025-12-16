#!/usr/bin/env python3
"""
Strava Year Recap Generator
Fetches your Strava activities and generates PNG visualizations
"""

import sys
import os
import argparse
from datetime import datetime
import cairosvg

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fetcher import StravaFetcher
from analyzer import StravaAnalyzer
from svg_generator import RecapSVG
from ai_analyzer import AIAnalyzer

def convert_svg_to_png(svg_path, png_path):
    """Convert SVG file to PNG"""
    try:
        cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1080, output_height=1920)
        print(f"✓ Created {png_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to convert {svg_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Generate Strava year recap visualizations')
    parser.add_argument('--ai', action='store_true', help='Generate AI-powered year review')
    parser.add_argument('--roast', action='store_true', help='Generate funny roast-style review (implies --ai)')
    args = parser.parse_args()

    year = datetime.now().year
    print(f"🏃 Strava {year} Recap Generator\n")

    # Step 1: Fetch activities
    print("📡 Fetching activities from Strava...")
    try:
        fetcher = StravaFetcher()
        activities = fetcher.fetch_year_activities()
        print(f"✓ Fetched {len(activities)} activities\n")
    except Exception as e:
        print(f"✗ Error fetching activities: {e}")
        return

    # Step 2: Analyze data
    print("📊 Analyzing data...")
    try:
        analyzer = StravaAnalyzer()
        stats = analyzer.save_stats()
        print(f"✓ Total: {stats['total_distance_km']:.1f} km across {stats['activity_count']} activities\n")
    except Exception as e:
        print(f"✗ Error analyzing data: {e}")
        return

    # Step 3: Generate SVGs
    print("🎨 Generating visualizations...")
    try:
        generator = RecapSVG()
        generator.create_main_recap()
        generator.create_by_type_breakdown()
        generator.create_monthly_chart()
        generator.create_time_analysis()
        generator.create_detailed_stats()
        print("✓ Generated SVGs\n")
    except Exception as e:
        print(f"✗ Error generating SVGs: {e}")
        return

    # Step 4: Generate AI analysis (if requested)
    ai_review_created = False
    ai_roast_created = False

    if args.ai or args.roast:
        print("🤖 Generating AI analysis...")
        try:
            ai_analyzer = AIAnalyzer()
            if args.roast:
                ai_analyzer.create_ai_recap_svg(roast_mode=True)
                ai_roast_created = True
                print("✓ Generated AI roast\n")
            if args.ai:
                ai_analyzer.create_ai_recap_svg(roast_mode=False)
                ai_review_created = True
                print("✓ Generated AI review\n")
        except Exception as e:
            print(f"✗ AI analysis failed: {e}")
            print("  Skipping AI generation. Configure LLM API key in .env to use this feature.\n")

    # Step 5: Convert SVGs to PNGs
    print("🖼️  Converting to PNG...")
    svg_files = [
        ('data/recap.svg', 'data/recap.png'),
        ('data/by_type.svg', 'data/by_type.png'),
        ('data/monthly.svg', 'data/monthly.png'),
        ('data/time_analysis.svg', 'data/time_analysis.png'),
        ('data/detailed_stats.svg', 'data/detailed_stats.png')
    ]

    # Add AI files only if they were successfully generated
    if ai_review_created:
        svg_files.append(('data/ai_review.svg', 'data/ai_review.png'))
    if ai_roast_created:
        svg_files.append(('data/ai_roast.svg', 'data/ai_roast.png'))

    success_count = 0
    for svg_path, png_path in svg_files:
        if os.path.exists(svg_path):
            if convert_svg_to_png(svg_path, png_path):
                success_count += 1

    print(f"\n🎉 Done! Generated {success_count} PNG files in data/")
    print("\nOutput files:")
    print("  - recap.png - Overall stats and records")
    print("  - by_type.png - Detailed breakdown by activity type")
    print("  - monthly.png - Monthly progress chart")
    print("  - time_analysis.png - Hour of day and day of week analysis")
    print("  - detailed_stats.png - Distance breakdown and performance metrics")
    if ai_review_created:
        print("  - ai_review.png - AI-generated year review")
    if ai_roast_created:
        print("  - ai_roast.png - AI-generated funny roast")

if __name__ == "__main__":
    main()
