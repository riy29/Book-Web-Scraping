import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
import time
import random
import re

class BookScraper:
    def __init__(self):
        # Headers to mimic a browser request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # List to store all scraped books
        self.books_data = []
        
    def fetch_page(self, url):
        # Fetches a webpage and returns the BeautifulSoup object. Includes error handling and rate limiting.
        try:
            # Add delay to be respectful to the server
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def scrape_book_list(self, url):
        # Scrapes book information from a Goodreads list page
        soup = self.fetch_page(url)
        if not soup:
            return
        
        # Find all book entries on the page
        bookEntries = soup.findAll('tr', {'itemtype': 'http://schema.org/Book'})
        
        for entry in bookEntries:
            bookData = {}
            
            # Extract title
            titleElement = entry.find('a', {'class': 'bookTitle'})
            bookData['title'] = titleElement.text.strip() if titleElement else 'Unknown Title'
            
            # Extract author
            authorElement = entry.find('a', {'class': 'authorName'})
            bookData['author'] = authorElement.text.strip() if authorElement else 'Unknown Author'

            self.books_data.append(bookData)
            
    def save_to_txt(self, filename="scraped_books.txt"):
        # Saves the scraped data to a text file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Scraped Book Data - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            for book in self.books_data:
                f.write(f"Title: {book['title']}\n")
                f.write(f"Author: {book['author']}\n")
                f.write("-" * 30 + "\n")
    
    def save_to_csv(self, filename="scraped_books.csv"):
        # Saves the scraped data to a CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'author']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.books_data)
    
    def save_to_json(self, filename="scraped_books.json"):
        # Saves the scraped data to a JSON file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.books_data, f, indent=4, ensure_ascii=False)

def main():
    # Initialize the scraper
    scraper = BookScraper()
    
    # List of Goodreads list URLs to scrape (you can add more)
    urls = [
        'https://www.goodreads.com/list/show/1.Best_Books_Ever',
        'https://www.librarything.com/',
    ]
    
    # Scrape each URL
    for url in urls:
        print(f"Scraping: {url}")
        scraper.scrape_book_list(url)
    
    # Save the data in different formats
    scraper.save_to_txt()
    scraper.save_to_csv()
    scraper.save_to_json()
    
    print(f"Scraping completed! Found {len(scraper.books_data)} books.")

if __name__ == "__main__":
    main()