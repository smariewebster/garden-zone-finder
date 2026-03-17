# Garden Zone Finder

A Python CLI tool that helps gardeners find what grows in their USDA hardiness zone, with tips scraped live from gardening websites.

Built for zone 6b (Santa Fe, NM) but works for any US zip code.

## Features

- Zip code → USDA growing zone lookup
- Last spring frost / first fall frost dates
- Plant database with native Southwest species flagged
- Water needs, days to maturity, direct sow vs. transplant info
- Live web scraping of gardening sites for zone-specific tips
- Optional report saved to .txt file

## Installation

**Requirements:** Python 3.9+
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/garden-zone-finder.git
cd garden-zone-finder

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
python3 main.py
```

You will be prompted to:
1. Enter your zip code
2. Choose whether to scrape live tips (takes ~2 min)
3. Optionally save the report to a .txt file

## Plant Database

Currently includes plants suited for zones 5a-9b across three categories:

| Category | Count |
|----------|-------|
| Vegetables | 8 |
| Fruits | 3 |
| Flowers | 5 |

Native Southwest species are flagged with `[NATIVE]` in the output.

## Data Sources

- USDA Plant Hardiness Zone Map via [phzmapi.org](https://phzmapi.org)
- Location data via pgeocode
- Growing tips scraped from:
  - Old Farmer's Almanac
  - NMSU Extension (nmsu.edu)
  - High Country Gardens
  - Gardening Know How
  - Planet Natural

## Project Structure
```
garden-zone-finder/
├── main.py           # CLI entry point
├── zone_lookup.py    # Zip → zone + frost dates
├── plants.py         # Plant database
├── scraper.py        # Web scraping logic
├── organizer.py      # Tip organization + formatting
├── requirements.txt  # Dependencies
└── README.md
```

## Contributing

Plant database contributions welcome - especially additional native Southwest species. Open a PR or file an issue.

## License

MIT
