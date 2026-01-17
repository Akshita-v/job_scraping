import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from scrapers.internshala import scrape_internshala
from scrapers.wellfound import wellfound_links
from scrapers.linkedin_links import linkedin_links
from scrapers.unstop_play import scrape_unstop_play
from scrapers.naukri import naukri_links
from scrapers.company_careers import company_career_links

from csv_manager import save_jobs, get_unsent_jobs, mark_sent
from email_sender import send_email

KEYWORDS = ["ai", "machine learning", "data science"]

def main():
    print("\n🚀 JOB SCRAPER STARTED\n")

    all_jobs = []

    try:
        all_jobs.extend(scrape_internshala(KEYWORDS))
    except Exception as e:
        print("❌ Internshala failed:", e)

    try:
        all_jobs.extend(wellfound_links(KEYWORDS))
    except Exception as e:
        print("❌ Wellfound failed:", e)

    try:
        all_jobs.extend(linkedin_links(KEYWORDS))
    except Exception as e:
        print("❌ LinkedIn failed:", e)

    try:
        all_jobs.extend(scrape_unstop_play(KEYWORDS))
    except ImportError:
        print("❌ Unstop skipped: Playwright not installed")
    except Exception as e:
        print("❌ Unstop failed:", e)

    try:
        all_jobs.extend(naukri_links(KEYWORDS))
    except Exception as e:
        print("❌ Naukri failed:", e)

    try:
        all_jobs.extend(company_career_links(KEYWORDS))
    except Exception as e:
        print("❌ Company Careers failed:", e)

    print(f"\n🔎 Total jobs found: {len(all_jobs)}")

    save_jobs(all_jobs)

    new_jobs = get_unsent_jobs()
    print(f"📬 New jobs to email: {len(new_jobs)}")

    send_email(new_jobs)
    mark_sent(new_jobs)

    print("\n✅ ALL DONE\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
