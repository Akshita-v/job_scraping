import requests
from bs4 import BeautifulSoup

def linkedin_links(keywords):
    jobs = []

    for k in keywords:
        url = f"https://www.linkedin.com/jobs/search/?keywords={k.replace(' ', '%20')}&location=India"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")

            # Find job cards
            cards = soup.select("div.job-search-card")

            for card in cards[:5]:  # Limit to 5 per keyword to avoid too many
                title_tag = card.select_one("h3")
                company_tag = card.select_one("h4")
                link_tag = card.select_one("a")

                link = link_tag["href"] if link_tag else url

                # Parse title and company from URL if masked
                if link and '/jobs/view/' in link:
                    url_parts = link.split('/jobs/view/')[1].split('-at-')
                    if len(url_parts) == 2:
                        title_slug = url_parts[0].replace('-', ' ').title()
                        company_slug = url_parts[1].split('-')[0].replace('-', ' ').title()
                        title = title_slug
                        company = company_slug
                    else:
                        title = f"LinkedIn job for {k}"
                        company = "Various Companies"
                else:
                    title = title_tag.text.strip() if title_tag else f"LinkedIn job for {k}"
                    company = company_tag.text.strip() if company_tag else "LinkedIn"
                    if '*' in title:
                        title = f"LinkedIn Job Opportunity ({k})"
                    if '*' in company:
                        company = "Various Companies"

                jobs.append({
                    "title": title,
                    "type": "Job",
                    "company": company,
                    "location": "India",
                    "domain": k,
                    "sent": "NO",
                    "link": link,
                    "source": "linkedin"
                })
        except Exception as e:
            print(f"❌ LinkedIn error for {k}: {e}")

    print(f"linkedin scraped: {len(jobs)}")
    return jobs

