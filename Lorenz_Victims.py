import httpx
from bs4 import BeautifulSoup
import re
import csv

proxies = {
    "http://": "socks5://127.0.0.1:9050",
    "https://": "socks5://127.0.0.1:9050"
}

url = 'http://lorenzmlwpzgxq736jzseuterytjueszsvznuibanxomlpkyxk6ksoyd.onion/'


def load_existing_entries(file):
    existing_entries = set()
    try:
        with open(file, mode='r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                existing_entries.add(tuple(row))
    except FileNotFoundError:
        pass
    return existing_entries


def pageScrape(response):
    # Open to check for duplicates
    try:
        with open("Lorenz_Victims.csv", "r") as file:
            existing_data = file.read().splitlines()
    except FileNotFoundError:
        existing_data = []

    existing_entries = load_existing_entries('Lorenz_Victims.csv')

    soup = BeautifulSoup(response.text, features="html.parser")
    companies = soup.find_all('div', attrs={"id": re.compile("comp")})

    with open('Lorenz_Victims.csv', mode="a", newline='') as file:
        csv_writer = csv.writer(file)

        for eachCompany in companies:
            name = eachCompany.find('h3')
            if name is None:
                date = eachCompany.find('h6').text
                new_entry = ("Paid", date)
                if new_entry not in existing_entries:
                    csv_writer.writerow(new_entry)
                    existing_entries.add(new_entry)
            else:
                nameText = name.get_text().strip()
                possibleDates = eachCompany.find_all(string=re.compile("Posted"))
                for possibleDay in possibleDates:
                    new_entry = (nameText, possibleDay)
                    if new_entry not in existing_entries:
                        csv_writer.writerow(new_entry)
                        existing_entries.add(new_entry)


with httpx.Client(proxies=proxies) as client:
    response = client.get(url)
    if response.status_code == 200:
        pageScrape(response)
    else:
        print('**End**')
