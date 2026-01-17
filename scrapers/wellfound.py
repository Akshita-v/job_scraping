def wellfound_links(keywords):
    base_url = "https://wellfound.com/jobs?role="
    jobs = []

    for keyword in keywords:
        role = keyword.replace(" ", "-").lower()
        link = base_url + role

        jobs.append({
            "title": f"Wellfound search for {keyword}",
            "type": "Job",
            "company": "Wellfound",
            "location": "Remote",
            "domain": "AI/ML",
            "sent": "NO",
            "link": link,
            "source": "wellfound"
        })

    print(f"wellfound scraped: {len(jobs)}")
    return jobs
