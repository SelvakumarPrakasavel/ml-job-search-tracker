import smtplib
import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime

def search_jobs():
    keywords = [
        "machine learning engineer 1 year",
        "machine learning engineer 2 years experience",
        "junior machine learning engineer",
        "ml engineer entry level",
        "remote junior ml engineer startup"
    ]
    search_sites = {
        "Wellfound": "https://www.google.com/search?q={}+site:wellfound.com",
        "LinkedIn": "https://www.google.com/search?q={}+site:linkedin.com/jobs",
        "Naukri": "https://www.google.com/search?q={}+site:naukri.com"
    }
    results = []

    headers = {"User-Agent": "Mozilla/5.0"}
    for keyword in keywords:
        for site_name, base_url in search_sites.items():
            url = base_url.format("+".join(keyword.split()))
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.select('a'):
                href = link.get('href')
                if href and "http" in href and any(s in href for s in ["wellfound.com", "linkedin.com/jobs", "naukri.com"]):
                    cleaned = href.split("&")[0].replace("/url?q=", "")
                    results.append(cleaned)

    return list(set(results))[:15]

def send_email(jobs):
    sender = os.environ.get("EMAIL_USER")
    receiver = sender
    password = os.environ.get("EMAIL_PASS")
    subject = f"🧠 ML Job Digest - {datetime.now().strftime('%Y-%m-%d')}"
    body = "Here are today's ML job results:

" + "\n".join(jobs)

    message = f"Subject: {subject}\n\n{body}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, message)
    server.quit()

if __name__ == "__main__":
    jobs = search_jobs()
    if jobs:
        with open("latest_jobs.txt", "w") as f:
            f.write("\n".join(jobs))
        send_email(jobs)
