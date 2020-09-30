import random
import time

from alive_progress import alive_bar
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options

from BaseScraper import BaseScraper
from BaseScraper import ScrapeType

options = Options()
options.headless = False
driver_path = "./driver/chromedriver"
base_scraper = BaseScraper("Deen", ScrapeType.FULL)
driver = webdriver.Chrome(options=options, executable_path=driver_path)
base_url = "https://www.deen.nl"


# homepage = open("./testHtml/deen_boodschappen.html", "rb")


def safe_request(url):
    retry_count = 0

    try:
        time.sleep(random.randint(1000, 2500) / 1000)
        if retry_count > 3:
            return
        driver.get(url)
        # Make sure the element is clickable. In case of ah site react needs to load in
        time.sleep(2)

        return driver.page_source
        # TODO: catch different errors
    except TimeoutException:
        retry_count += 1
        safe_request(url)
    except Exception as err:
        base_scraper.add_scrape_error("Generic error on safe request" + err.args[1])
    except ElementNotInteractableException as err:
        base_scraper.add_scrape_error("Generic error on safe request" + err.args[1])
    finally:
        if retry_count > 3:
            base_scraper.add_scrape_error("TimeoutException: Failed to retrieve url:" + url)
            return


def get_urls():
    urls = []
    try:
        homepage = safe_request(base_url + "/boodschappen")
        soup = BeautifulSoup(homepage, "lxml")
        scrape_urls = soup.find("div", {"id": "categories"}).find_all("a", {"class", "c-categorylist__link"})
        with alive_bar(len(scrape_urls), title="Retrieving urls...", spinner="classic") as bar:
            for url in scrape_urls:
                urls.append(base_url + url["href"] + "?items=600")
                bar()
        return urls
    except Exception as err:
        base_scraper.add_scrape_error(str(err))
        return urls


def scrape_product(product_page):
    soup = BeautifulSoup(product_page, "lxml")
    products = soup.find_all("li", {"class": "c-productgrid__item"})
    for product in products:
        if len(product.contents) > 0 and "c-productgrid__item--banner" not in product["class"]:
            name = product.find("h3").text
            image = product.find("img")["src"]
            product_id = int(product.find("div", {"class", "c-product-thumbnail"})["data-product-itemcode"])
            price = int(product.find("span", {"class": "c-price"}).text.replace(",", ""))
            base_scraper.add_product(product_id, name, image, price, None)


def parse_all(urls=None):
    if urls:
        product_urls = urls
    else:
        product_urls = get_urls()
    if len(product_urls) > 0:
        random.shuffle(product_urls)
        current_url = None
        try:
            with alive_bar(len(product_urls), title="Scraping products", spinner="classic") as bar:
                while len(product_urls) > 0:
                    current_url = product_urls.pop()
                    product_page = safe_request(current_url)
                    scrape_product(product_page)
                    bar()
        except Exception as err:
            print(err)
            base_scraper.add_scrape_error("Error scraping url:" + current_url)
            parse_all(product_urls)

    else:
        base_scraper.add_scrape_error("No urls retrieved.")


if __name__ == '__main__':
    parse_all()

    # This keeps reference alive so we can call finish scrape history.
    del base_scraper
    driver.quit()
