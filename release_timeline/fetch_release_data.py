#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""
Fetch EEST Release Data from GitHub

This script fetches the latest release data from GitHub and saves it locally
for use by the visualization script. This separation allows you to fetch data
once and generate plots multiple times without hitting GitHub API rate limits.

Usage:
    ./fetch_releases.py

Requirements:
    - gh CLI tool installed and authenticated

Output:
    - releases.txt: Raw release data
    - releases_chronological.md: Human-readable chronological list
"""

import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime

def fetch_release_data():
    """Fetch release data from GitHub API using gh CLI."""
    print("Fetching release data from GitHub...")
    
    try:
        # Fetch releases using gh CLI
        result = subprocess.run([
            "gh", "api", "repos/ethereum/execution-spec-tests/releases", "--paginate"
        ], capture_output=True, text=True, check=True)
        
        releases = json.loads(result.stdout)
        print(f"Fetched {len(releases)} releases from GitHub")
        
        # Convert to our format: tag|date|name
        release_lines = []
        for release in releases:
            tag = release['tag_name']
            date = release['published_at']
            name = release['name'] or tag
            release_lines.append(f"{tag}|{date}|{name}")
        
        return release_lines
        
    except subprocess.CalledProcessError as e:
        print(f"Error fetching releases: {e}")
        print("Make sure 'gh' CLI is installed and authenticated")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing GitHub API response: {e}")
        sys.exit(1)

def save_release_data(release_lines):
    """Save release data to file."""
    # Create build directory if it doesn't exist
    script_dir = Path(__file__).parent
    build_dir = script_dir / "build"
    build_dir.mkdir(exist_ok=True)
    
    releases_file = build_dir / "releases.txt"
    with open(releases_file, "w") as f:
        for line in release_lines:
            f.write(line + "\n")
    
    print(f"Saved {len(release_lines)} releases to {releases_file}")
    return releases_file

def generate_chronological_markdown(release_lines):
    """Generate chronological markdown file for human review."""
    print("Generating chronological markdown file...")
    
    # Parse and sort releases chronologically
    releases = []
    for line in release_lines:
        parts = line.strip().split("|")
        if len(parts) >= 3:
            tag = parts[0]
            date_str = parts[1]
            name = parts[2]
            # Parse date for sorting
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            releases.append((date, tag, name))
    
    # Sort by date
    releases.sort(key=lambda x: x[0])
    
    # Generate markdown
    md_content = ["# EEST Releases - Chronological Order", ""]
    md_content.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_content.append(f"Total releases: {len(releases)}")
    md_content.append("")
    
    for date, tag, name in releases:
        date_str = date.strftime("%Y-%m-%d")
        md_content.append(f"- **{tag}** - {date_str}")
    
    # Write to file
    script_dir = Path(__file__).parent
    build_dir = script_dir / "build"
    build_dir.mkdir(exist_ok=True)
    md_file = build_dir / "releases_chronological.md"
    with open(md_file, "w") as f:
        f.write("\n".join(md_content))
    
    print(f"Saved chronological release list to {md_file}")
    return md_file

def main():
    """Main execution function."""
    print("=== EEST Release Data Fetcher ===")
    print()
    
    # Step 1: Fetch release data from GitHub
    release_lines = fetch_release_data()
    
    # Step 2: Save raw release data
    releases_file = save_release_data(release_lines)
    
    # Step 3: Generate chronological markdown for human review
    md_file = generate_chronological_markdown(release_lines)
    
    # Summary
    print()
    print("=== Fetch Complete ===")
    print(f"Files created:")
    print(f"  - {releases_file}")
    print(f"  - {md_file}")
    print()
    print(f"Total releases fetched: {len(release_lines)}")
    print("Data ready for visualization generation!")
    print()
    print("Next step: uv run release_timeline/generate_plots.py")

if __name__ == "__main__":
    main()