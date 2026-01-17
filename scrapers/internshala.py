import requests
from bs4 import BeautifulSoup
import time
import re

def scrape_internshala(keywords):
    url = "https://internshala.com/internships"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        print("❌ Internshala request failed:", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Find all internship links
    internship_links = soup.select("h3 a[href*='internship/detail']")

    if not internship_links:
        print("⚠️ Internshala: No internship links found")
        return []

    for link_tag in internship_links:
        title = link_tag.text.strip()
        link = "https://internshala.com" + link_tag["href"]

        # Find the company: the next text after the h3
        h3 = link_tag.find_parent("h3")
        company = h3.next_sibling.strip() if h3 and h3.next_sibling else "Internshala"

        combined_text = f"{title} {company}".lower()

        # RELAXED keyword match
        if any(re.search(r'\b' + re.escape(k.lower()) + r'\b', combined_text) for k in keywords):
            jobs.append({
                "title": title,
                "type": "Internship",
                "company": company,
                "location": "India / Remote",
                "domain": "AI/ML",
                "sent": "NO",
                "link": link,
                "source": "internshala"
            })

    print(f"internshala scraped: {len(jobs)}")
    return jobs
