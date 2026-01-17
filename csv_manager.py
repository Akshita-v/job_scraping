import pandas as pd
import os

CSV_FILE = "opportunities.csv"

COLUMNS = [
    "title",
    "type",
    "company",
    "location",
    "domain",
    "sent",
    "link",
    "source"
]

def save_jobs(new_jobs):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    for job in new_jobs:
        # Check if link already exists
        if job["link"] not in df["link"].astype(str).values:
            # Also check if title and company already exist and sent
            existing = df[(df["title"] == job["title"]) & (df["company"] == job["company"]) & (df["sent"] == "YES")]
            if existing.empty:
                df = pd.concat([df, pd.DataFrame([job])], ignore_index=True)

    df.to_csv(CSV_FILE, index=False)


def get_unsent_jobs():
    if not os.path.exists(CSV_FILE):
        return []

    df = pd.read_csv(CSV_FILE)
    return df[df["sent"] == "NO"].to_dict("records")


def mark_sent(jobs):
    if not jobs:
        return

    df = pd.read_csv(CSV_FILE)
    for job in jobs:
        df.loc[df["link"] == job["link"], "sent"] = "YES"

    df.to_csv(CSV_FILE, index=False)
