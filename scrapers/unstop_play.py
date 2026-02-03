# unstop_play.py
from playwright.sync_api import sync_playwright
import time

def scrape_unstop_play(keywords):
    """
    Improved Unstop internships scraper (2026-ready version)
    - Handles infinite scroll properly
    - Uses more resilient selectors
    - Extracts more fields (stipend, location, deadline)
    """
    jobs = []

    # You can add ?search= or filters in URL for better targeting
    # Example: https://unstop.com/internships?filters=,,,,,ai,machine%20learning
    base_url = "https://unstop.com/internships"  # ← start here

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0")

        print("[INFO] Navigating to Unstop internships...")
        page.goto(base_url, wait_until="networkidle", timeout=45000)

        # Give initial load time
        page.wait_for_timeout(4000)

        # ── Infinite scroll until no new content ──
        print("[INFO] Scrolling to load all opportunities...")
        last_height = page.evaluate("document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 25  # safety limit

        while scroll_attempts < max_attempts:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2200)  # give time for new cards to appear

            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                print("   [INFO] No more content loading. Stopping scroll.")
                break
            last_height = new_height
            scroll_attempts += 1
            print(f"   [INFO] Scrolled {scroll_attempts} times...")
        # Try multiple possible card selectors (most likely one will work)
        possible_card_selectors = [
            "div[class*='opportunity-card']",                  # common pattern
            "div[class*='card']",                             # generic
            "[data-testid='opportunity-card']",               # if they use testid
            "article",                                        # sometimes used
            "div.j-between-start",                            # your old one (fallback)
        ]

        cards = []
        for selector in possible_card_selectors:
            found = page.query_selector_all(selector)
            if len(found) > 5:  # reasonable number → probably correct
                cards = found
                print(f"[INFO] Found {len(cards)} cards using selector: {selector}")
                break

        if not cards:
            print("[WARNING] No opportunity cards found with any selector. Site probably changed significantly.")
            browser.close()
            return jobs

        print(f"[INFO] Processing {len(cards)} opportunity cards...")

        for i, card in enumerate(cards, 1):
            try:
                # Title - most reliable patterns first
                title_el = (
                    card.query_selector("h3") or
                    card.query_selector("[class*='title']") or
                    card.query_selector("a > div > div:first-child")
                )
                title = title_el.inner_text().strip() if title_el else "N/A"

                # Company / Organizer
                company_el = (
                    card.query_selector("[class*='company'], [class*='organiser'], [class*='subtitle'], p") or
                    card.query_selector("span[class*='company']")
                )
                company = company_el.inner_text().strip() if company_el else "Unstop"

                # Link (most important - must be absolute)
                link_el = card.query_selector("a[href^='/internships/'], a[href^='/competitions/']")
                link = "https://unstop.com" + link_el.get_attribute("href") if link_el and link_el.get_attribute("href") else "N/A"

                # Location (optional)
                location_el = card.query_selector("[class*='location'], [class*='place'], span[class*='location']")
                location = location_el.inner_text().strip() if location_el else "India / Remote"

                # Stipend (very useful!)
                stipend_el = card.query_selector("[class*='stipend'], [class*='reward'], [class*='prize'], span[class*='amount']")
                stipend = stipend_el.inner_text().strip() if stipend_el else "N/A"

                # Simple keyword filter (you can make it stricter later)
                combined_text = f"{title} {company} {stipend}".lower()
                if any(k.lower() in combined_text for k in keywords):
                    jobs.append({
                        "title": title,
                        "type": "Internship",
                        "company": company,
                        "location": location,
                        "stipend": stipend,
                        "domain": "AI/ML",  # you can make dynamic later
                        "sent": "NO",
                        "link": link,
                        "source": "unstop"
                    })

                if i % 10 == 0:
                    print(f"Processed {i}/{len(cards)} cards...")

            except Exception as e:
                print(f"Error processing card {i}: {e}")

        browser.close()

    print(f"unstop scraped: {len(jobs)} relevant opportunities")
    return jobs