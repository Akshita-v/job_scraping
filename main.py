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

KEYWORDS = ["ai", "machine learning", "data science", "deep learning", "computer vision", "nlp", "robotics", "reinforcement learning", "predictive modeling", "big data", "data engineering", "data analytics", "business intelligence", "statistical analysis", "cloud computing", "tensorflow", "pytorch", "keras", "scikit-learn", "r programming",
            "summer internship", "winter internship", "research internship", "undergraduate internship", "graduate internship", "data science internship", "machine learning internship", "artificial intelligence internship", "deep learning internship"," computer vision internship", "nlp internship", "robotics internship","ai intern", " Ml internship"]

def main():
    print("\n[JOB SCRAPER STARTED]\n")

    all_jobs = []

    try:
        all_jobs.extend(scrape_internshala(KEYWORDS))
    except Exception as e:
        print("[ERROR] Internshala failed:", e)

    try:
        all_jobs.extend(wellfound_links(KEYWORDS))
    except Exception as e:
        print("[ERROR] Wellfound failed:", e)

    try:
        all_jobs.extend(linkedin_links(KEYWORDS))
    except Exception as e:
        print("[ERROR] LinkedIn failed:", e)

    try:
        all_jobs.extend(scrape_unstop_play(KEYWORDS))
    except ImportError:
        print("[ERROR] Unstop skipped: Playwright not installed")
    except Exception as e:
        print("[ERROR] Unstop failed:", e)

    try:
        all_jobs.extend(naukri_links(KEYWORDS))
    except Exception as e:
        print("[ERROR] Naukri failed:", e)

    try:
        all_jobs.extend(company_career_links(KEYWORDS))
    except Exception as e:
        print("[ERROR] Company Careers failed:", e)

    print(f"\n[TOTAL] Total jobs found: {len(all_jobs)}")

    save_jobs(all_jobs)

    new_jobs = get_unsent_jobs()
    print(f"[EMAIL] New jobs to email: {len(new_jobs)}")

    send_email(new_jobs)
    mark_sent(new_jobs)

    print("\n[SUCCESS] ALL DONE\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
