# Job Scraper

A Python-based job scraper for AI/ML opportunities from various sources.

## Setup

1. Create a virtual environment: `python -m venv .venv`
2. Activate it: `.venv\Scripts\Activate` (Windows)
3. Install dependencies: `pip install beautifulsoup4 requests pandas playwright python-dotenv`
4. Install Playwright browsers: `playwright install`
5. Create a `.env` file with your email credentials:
   ```
   EMAIL=your_email@gmail.com
   PASSWORD=your_app_password
   ```

## Usage

Run `python main.py` to scrape and email new jobs.

## Sources

- Internshala
- Wellfound
- LinkedIn
- Unstop
- Naukri

## Notes

- Jobs are saved to `opportunities.csv`
- Only new jobs are emailed
- Duplicates are prevented by title/company and links.