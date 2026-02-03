# SWE Job Scraper

A professional-grade Python-based job scraping and email notification system for AI/ML and Software Engineering opportunities from multiple job portals.

## Overview

This project automatically:
- 🔍 **Scrapes** job opportunities from 6+ job platforms
- 🎯 **Filters** jobs by 40+ relevant keywords (AI, ML, Data Science, etc.)
- 📧 **Emails** unsent jobs daily with detailed information
- 🗑️ **Auto-cleans** old jobs (>4 weeks old)
- 📊 **Tracks** when emails are sent with date stamps

## Features

### Smart Filtering
- **Keyword-based filtering**: Only jobs matching your interests (AI, Machine Learning, Data Science, Deep Learning, etc.)
- **4-week window**: Automatically removes sent jobs older than 4 weeks to keep data fresh
- **Duplicate prevention**: Prevents duplicate emails by tracking job links and company-title combinations

### Data Management
- **Centralized CSV storage**: All opportunities stored in `opportunities.csv`
- **Email tracking**: Records when jobs are emailed with `date_sent` column
- **Status tracking**: Marks jobs as sent/unsent to avoid resending

### Automation
- **Daily scheduling**: Set once, runs automatically at 8:00 AM via Windows Task Scheduler
- **Logging**: Tracks all executions in `scheduler.log`
- **Error handling**: Robust error management for failed scrapes

## Supported Job Platforms

1. **Internshala** - Indian internship platform
2. **LinkedIn** - Global professional network
3. **Naukri** - Indian job portal
4. **Wellfound** - Startup jobs
5. **Unstop** - Competitions & internships
6. **Company Career Pages** - Direct company portals (Google, Microsoft, Accenture, etc.)

## Installation

### Prerequisites
- Python 3.8+
- Windows (for Task Scheduler automation)
- Gmail account with app password

### Step 1: Clone/Setup
```bash
cd C:\Users\akshi\Downloads\swelist
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\Activate
```

### Step 3: Install Dependencies
```bash
pip install beautifulsoup4 requests pandas playwright python-dotenv
playwright install
```

### Step 4: Configure Email
Create `.env` file in the project root:
```
EMAIL=your_email@gmail.com
PASSWORD=your_app_password
```

**Note**: Use Gmail App Password, not your regular password. [How to create app password](https://support.google.com/accounts/answer/185833)

## Usage

### Manual Execution
```bash
python main.py
```

This will:
1. Scrape all job sources for keywords
2. Save new jobs to `opportunities.csv`
3. Send unsent jobs via email
4. Clean up old jobs (>4 weeks)
5. Update `date_sent` for emailed jobs

### Automated Daily Execution

#### Setup (One-time)

**See [SCHEDULER_SETUP_TEMPLATE.md](SCHEDULER_SETUP_TEMPLATE.md) for detailed step-by-step instructions with all paths and configurations.**

Quick summary:
1. Open Task Scheduler: `Win + R` → `taskschd.msc`
2. Create Basic Task named `SWE Job Scraper Daily`
3. Set trigger to Daily at 8:00 AM
4. Set action to run `schedule_runner.py` with Python
5. Configure settings and finish

#### Verify Setup
- Check `scheduler.log` for execution records
- Monitor `opportunities.csv` for new jobs

#### Disable/Edit Task
1. Open Task Scheduler
2. Find "SWE Job Scraper Daily"
3. Right-click to disable, edit, or delete

## Keywords List

The system automatically filters for these keywords:

**AI/ML Core**: AI, Machine Learning, Data Science, Deep Learning, Computer Vision, NLP, Robotics, Reinforcement Learning

**Data Skills**: Predictive Modeling, Big Data, Data Engineering, Data Analytics, Business Intelligence, Statistical Analysis

**Tools/Frameworks**: TensorFlow, PyTorch, Keras, Scikit-learn, R Programming

**Cloud**: Cloud Computing

**Internship Types**: Summer Internship, Winter Internship, Research Internship, Undergraduate Internship, Graduate Internship, AI Intern, ML Internship

Edit `KEYWORDS` in main.py to customize.

## Project Structure

```
swelist/
├── main.py                 # Main scraper orchestrator
├── csv_manager.py          # CSV handling & cleanup logic
├── email_sender.py         # Email notification system
├── schedule_runner.py      # Task Scheduler runner
├── run_daily.bat          # Batch file alternative
├── opportunities.csv       # Job database (auto-generated)
├── scheduler.log          # Execution logs (auto-generated)
├── .env                   # Email credentials (not in repo)
├── README.md              # This file
└── scrapers/              # Individual scraper modules
    ├── internshala.py
    ├── linkedin_links.py
    ├── naukri.py
    ├── wellfound.py
    ├── unstop_play.py
    └── company_careers.py
```

## CSV Columns

| Column | Type | Description |
|--------|------|-------------|
| title | String | Job title |
| type | String | Job/Internship |
| company | String | Company name |
| location | String | Job location |
| domain | String | Domain (AI/ML, etc) |
| sent | YES/NO | Email sent status |
| link | String | Job application link |
| source | String | Scraper source |
| stipend | String | Monthly stipend (if available) |
| date_sent | YYYY-MM-DD | Date when email was sent |

## Troubleshooting

### Emails not sending
1. Verify `.env` file has correct credentials
2. Check email is Gmail with app password enabled
3. Run manually: `python main.py`
4. Check for errors in console

### Task Scheduler not running
1. Verify Python path is correct: `where python`
2. Check `scheduler.log` for error messages
3. Test manually: `python schedule_runner.py`
4. Ensure computer doesn't go to sleep at 8:00 AM

### No jobs found
1. Check internet connection
2. Job portals may have changed structure
3. Update selectors in scraper files
4. Verify keywords are relevant

### View logs
- **Email logs**: `scheduler.log`
- **Job database**: `opportunities.csv`

## Advanced Configuration

### Change Max Job Age
Edit csv_manager.py:
```python
MAX_JOB_AGE_WEEKS = 4  # Change to desired number of weeks
```

### Change Email Schedule
In Task Scheduler, edit "SWE Job Scraper Daily" → Trigger Tab → Set new time

### Add/Remove Keywords
Edit `KEYWORDS` list in main.py

### Change Email Recipients
Edit email list in email_sender.py

## Performance

- **Scraping time**: 2-5 minutes (depends on internet speed)
- **CSV size**: Grows ~50-100 jobs per week (cleaned up after 4 weeks)
- **Email time**: <1 minute

## Requirements

- Python 3.8+
- Internet connection
- Gmail account
- Windows OS (for Task Scheduler)

## Maintenance

**Weekly**:
- Check `opportunities.csv` for data quality
- Monitor `scheduler.log` for errors

**Monthly**:
- Review and update keywords if needed
- Check job portal changes

## Support

For issues:
1. Check `scheduler.log` for error details
2. Run `python main.py` manually to test
3. Verify all dependencies installed: `pip list`
4. Check internet connectivity

## License

Private project for personal use.
