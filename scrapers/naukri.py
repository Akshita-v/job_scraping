def naukri_links(keywords):
    jobs = []

    for k in keywords:
        query = k.replace(" ", "-")
        url = f"https://www.naukri.com/{query}-jobs"

        jobs.append({
            "title": f"Naukri jobs for {k}",
            "type": "Job",
            "company": "Multiple (via Naukri)",
            "location": "India",
            "domain": k,
            "sent": "NO",
            "link": url,
            "source": "naukri"
        })
    print(f"naukri scraped: {len(jobs)}")
    return jobs
