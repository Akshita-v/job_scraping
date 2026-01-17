def company_career_links(keywords):
    """
    Returns a list of job links for multiple companies in one go
    """
    companies = {
        "Google": "https://www.google.com/about/careers/applications/jobs/results/?q={query}",
        "Microsoft": "https://jobs.careers.microsoft.com/global/en/search?q={query}",
        "Deloitte": "https://apply.deloitte.com/careers/SearchJobs/{query}",
        "Accenture": "https://www.accenture.com/in-en/careers/jobsearch?keywords={query}",
        "Infosys": "https://career.infosys.com/joblist?search={query}"
    }

    jobs = []

    for company_name, url_template in companies.items():
        for k in keywords:
            query = k.replace(" ", "%20")
            url = url_template.format(query=query)

            jobs.append({
                "title": f"{company_name} jobs for {k}",
                "type": "Job",
                "company": company_name,
                "location": "India / Global",
                "domain": k,
                "sent": "NO",
                "link": url,
                "source": "company_careers"
            })

    print(f"company careers scraped: {len(jobs)}")
    return jobs
