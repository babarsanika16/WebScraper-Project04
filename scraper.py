import requests
import json
import time
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin

# Website details
BASE_URL = "https://quotes.toscrape.com"
HEADERS = {
    "User-Agent": "StudentLearningProject/1.0"
}

# Function to scrape quotes
def scrape_quotes():

    url = BASE_URL
    all_quotes = []

    while url:

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            response.raise_for_status()

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            quote_boxes = soup.select("div.quote")

            for box in quote_boxes:

                quote_text = box.select_one("span.text")
                author_name = box.select_one("small.author")

                if quote_text and author_name:

                    tags = [
                        tag.get_text(strip=True)
                        for tag in box.select("a.tag")
                    ]

                    quote_data = {
                        "quote": quote_text.get_text(strip=True),
                        "author": author_name.get_text(strip=True),
                        "tags": tags
                    }

                    all_quotes.append(quote_data)

            # Find next page
            next_page = soup.select_one("li.next a")

            if next_page:
                url = urljoin(BASE_URL, next_page["href"])
                time.sleep(1)
            else:
                url = None

        except requests.RequestException as error:
            print("Website request failed:", error)
            break

    return all_quotes


# Function to save data
def save_data(data):

    # Save JSON file
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    # Save readable text file
    with open("quotes.txt", "w", encoding="utf-8") as file:

        for index, item in enumerate(data, start=1):

            file.write(f"Quote {index}\n")
            file.write(f"Text: {item['quote']}\n")
            file.write(f"Author: {item['author']}\n")
            file.write(f"Tags: {', '.join(item['tags'])}\n")
            file.write("-" * 50 + "\n")


# Function to display summary
def show_summary(data):

    print("\n----- SCRAPING SUMMARY -----")

    print("Total quotes collected:", len(data))

    if data:

        authors = Counter(
            item["author"] for item in data
        )

        all_tags = [
            tag
            for item in data
            for tag in item["tags"]
        ]

        common_author = authors.most_common(1)[0]
        print("Most quoted author:", common_author[0])

        if all_tags:
            common_tag = Counter(all_tags).most_common(1)[0]
            print("Most common tag:", common_tag[0])

    print("\nFiles saved successfully!")


# Main program
if __name__ == "__main__":

    print("Starting Web Scraper...")

    quotes = scrape_quotes()

    save_data(quotes)

    show_summary(quotes)