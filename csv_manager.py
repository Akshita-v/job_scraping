import pandas as pd
import os
from datetime import datetime, timedelta

CSV_FILE = "opportunities.csv"
MAX_JOB_AGE_WEEKS = 4

COLUMNS = [
    "title",
    "type",
    "company",
    "location",
    "domain",
    "sent",
    "link",
    "source",
    "date_sent"
]

def save_jobs(new_jobs):
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        # Add date_sent column if it doesn't exist (but leave empty)
        if "date_sent" not in df.columns:
            df["date_sent"] = ""
    else:
        df = pd.DataFrame(columns=COLUMNS)
    
    for job in new_jobs:
        # Check if link already exists
        if job["link"] not in df["link"].astype(str).values:
            # Also check if title and company already exist and sent
            existing = df[(df["title"] == job["title"]) & (df["company"] == job["company"]) & (df["sent"] == "YES")]
            if existing.empty:
                # Don't set date_sent yet - it's set when email is sent
                if "date_sent" not in job:
                    job["date_sent"] = ""
                df = pd.concat([df, pd.DataFrame([job])], ignore_index=True)
    
    # Remove jobs older than MAX_JOB_AGE_WEEKS
    df = cleanup_old_jobs(df)
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
    # Ensure date_sent column is string type to avoid dtype warnings
    df["date_sent"] = df["date_sent"].astype(str).replace("nan", "")
    
    today = datetime.now().strftime("%Y-%m-%d")
    for job in jobs:
        df.loc[df["link"] == job["link"], "sent"] = "YES"
        # Set date_sent to today when email is sent
        df.loc[df["link"] == job["link"], "date_sent"] = today

    df.to_csv(CSV_FILE, index=False)


def cleanup_old_jobs(df):
    """Remove SENT jobs older than MAX_JOB_AGE_WEEKS weeks"""
    if "date_sent" not in df.columns or df.empty:
        return df
    
    cutoff_date = datetime.now() - timedelta(weeks=MAX_JOB_AGE_WEEKS)
    
    # Convert date_sent to datetime, keeping NaN for empty values
    df["date_sent"] = pd.to_datetime(df["date_sent"], errors="coerce")
    
    # Keep: 1) Unsent jobs (date_sent is NaN), 2) Sent jobs within time window
    df_filtered = df[(df["date_sent"].isna()) | (df["date_sent"] >= cutoff_date)].copy()
    
    removed_count = len(df) - len(df_filtered)
    if removed_count > 0:
        print(f"[CLEANUP] Removed {removed_count} sent jobs older than {MAX_JOB_AGE_WEEKS} weeks")
    
    # Convert back to string format for CSV (NaN becomes empty string)
    df_filtered["date_sent"] = df_filtered["date_sent"].dt.strftime("%Y-%m-%d")
    df_filtered["date_sent"] = df_filtered["date_sent"].fillna("")
    return df_filtered
