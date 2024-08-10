import httpx
from bs4 import BeautifulSoup
import re

proxies = {
    "http://": "socks5://127.0.0.1:9050",
    "https://": "socks5://127.0.0.1:9050"
}

url = 'http://rnsm777cdsjrsdlbs4v5qoeppu3px6sb2igmh53jzrx7ipcrbjz5b2ad.onion/'

def pageScrape(response):
    # Open to check for duplicates
    try:
        with open("RansomEXX_Victims.csv", "r") as file:
            existing_data = file.read().splitlines()
    except FileNotFoundError:
        existing_data = []

    soup = BeautifulSoup(response.text, features="html.parser")
    companies = soup.find_all('h2')
    publishDates = soup.find_all('time', attrs={"class": re.compile("entry-date published")})

    with open('RansomEXX_Victims.csv', "a") as file:
        for count, company in enumerate(companies):
            entry = f'{company.text},"{publishDates[count].text}"'

            # Check if entry is already in existing data
            if entry.strip() not in existing_data:
                # Write the new entry to the file
                file.write(entry + "\n")
            else:
                print(f"Skipping existing entry: {company.text}")

    print("/Scraped Page/")


with httpx.Client(proxies=proxies) as client:
    response = client.get(url)
    if response.status_code == 200:
        print(f'------Page 1------')
        pageScrape(response)

    for i in range(2, 500):
        url = f'http://rnsm777cdsjrsdlbs4v5qoeppu3px6sb2igmh53jzrx7ipcrbjz5b2ad.onion/page/{i}/index.html'
        response = client.get(url)
        print(f'------Page {i}------')
        if response.status_code == 200:
            pageScrape(response)
        else:
            print('**End**')
            break
