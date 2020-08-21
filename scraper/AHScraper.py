from BaseScraper import ScrapeType
from BaseScraper import BaseScraper
from bs4 import BeautifulSoup
from sys import argv

base_scraper = None
ah_base_url = "https://www.ah.nl"


def parse_all():
    base_scraper = BaseScraper("Albert Heijn", ScrapeType.FULL)
    # TODO: switch this after testing
    # homepage = base_scraper.safe_request("https://www.google.com/search/about/").content
    homepage = open("./testHtml/ah_producten.html", "rb")
    soup = BeautifulSoup(homepage, "lxml")
    scrape_urls = soup.find_all("div", {"class": "product-category-overview_category__1H99m"})
    categories = []
    for url in scrape_urls:
        # TODO: switch this after testing
        # category = base_scraper.safe_request(ah_base_url + url.find("a")["href"]).content
        homepage = open("./testHtml/ah_producten.html", "rb")
        soup = BeautifulSoup(homepage, "lxml")
        soorten = soup.find_all()


def update_product():
    base_scraper = BaseScraper("Albert Heijn", ScrapeType.SINGLE)
    print("test2")


if __name__ == '__main__':
    print("Init basescraper")
    if int(argv[1]) == 1:
        parse_all()
    elif int(argv[1]) == 2:
        update_product()
