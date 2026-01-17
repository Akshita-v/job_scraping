# unstop_play.py
from playwright.sync_api import sync_playwright

def scrape_unstop_play(keywords):
    """
    Scrape Unstop internships/events matching given keywords using Playwright.
    Handles JS-loaded content by scrolling and waiting for network idle.

    Args:
        keywords (list): List of keywords to filter opportunities.

    Returns:
        list: List of dictionaries containing opportunity details.
    """
    jobs = []

    with sync_playwright() as p:
        # Launch browser headless
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to Unstop internships page
        page.goto("https://unstop.com/internships")
        
        # Wait until network is idle (all JS loaded)
        page.wait_for_load_state("networkidle")
        
        # Scroll to bottom to trigger lazy loading
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(3000)  # wait 3 seconds for content to load

        # Select all opportunity cards
        cards = page.query_selector_all("div.opportunity-card")

        for card in cards:
            title_el = card.query_selector("h3")
            company_el = card.query_selector("p")
            link_el = card.query_selector("a")

            title = title_el.inner_text().strip() if title_el else "N/A"
            company = company_el.inner_text().strip() if company_el else "Unstop"
            link = "https://unstop.com" + link_el.get_attribute("href") if link_el else "N/A"

            # Filter by keywords
            if any(k.lower() in title.lower() for k in keywords):
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": "India",
                    "link": link,
                    "domain": "AI/ML",
                    "source": "unstop"
                })

        browser.close()

    print(f"unstop scraped: {len(jobs)}")
    return jobs
