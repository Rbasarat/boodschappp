import random
import re
import time
from sys import argv

from alive_progress import alive_bar
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from BaseScraper import BaseScraper
from BaseScraper import ScrapeType

options = Options()
options.headless = False
driver_path = "./driver/chromedriver"
base_scraper = BaseScraper("Dirk van den Broek", ScrapeType.FULL)
driver = webdriver.Chrome(options=options, executable_path=driver_path)
base_url = "https://www.dirk.nl"


#         homepage = open("testHtml/dirk_producten.html", "rb")

def safe_request(url, element=None):
    retry_count = 0

    try:
        time.sleep(random.randint(1000, 2500) / 1000)
        if retry_count > 3:
            return
        driver.get(url)
        # Make sure the element is clickable. In case of ah site react needs to load in
        time.sleep(2)
        if element:
            # I don't know if this solves the problem that the element is no clickable when executing the click.
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, element)))
            driver.find_elements_by_class_name(element)[1].click()

        return driver.page_source
        # TODO: catch different errors
    except TimeoutException:
        retry_count += 1
        safe_request(url)
    except NoSuchElementException:
        base_scraper.add_scrape_error("Element not found on: " + url + "with element:" + element)
    except Exception as err:
        base_scraper.add_scrape_error("Generic error on safe request" + err.args[1])
    except ElementNotInteractableException as err:
        base_scraper.add_scrape_error("Generic error on safe request" + err.args[1])
    finally:
        if retry_count > 3:
            base_scraper.add_scrape_error("TimeoutException: Failed to retrieve url:" + url)
            return


def calculate_bonus(product):
    bonus_block = product.find("div", {"class": "product-card__discount"})
    if bonus_block:
        bonus_text = ' '.join([x.text for x in bonus_block.find_all("span")])
        bonus_type = base_scraper.get_bonus_types(bonus_text)
        if bonus_type:
            return bonus_type["Id"]
        else:
            base_scraper.add_bonus_type(bonus_text)
            return calculate_bonus(product)
    else:
        return None


def get_urls():
    urls = []
    try:
        homepage = safe_request(base_url)
        soup = BeautifulSoup(homepage, "lxml")
        scrape_urls = soup.find_all("a", {"class": "site-header__product-categories__category"}, href=True)
        with alive_bar(len(scrape_urls), title="Retrieving urls...", spinner="classic") as bar:
            for url in scrape_urls:
                if url["href"]:
                    category = safe_request(base_url + url["href"])
                    soup = BeautifulSoup(category, "lxml")
                    product_soorten = soup.find("nav", {"class": "product-category-header__nav"}).find_all("a")
                    for soort in product_soorten:
                        urls.append(base_url + soort["href"])
                bar()

        return urls
    except Exception as err:
        base_scraper.add_scrape_error(str(err))
        return urls


def scrape_product(product_page):
    soup = BeautifulSoup(product_page, "lxml")
    products = soup.find_all("div", {"class": "product-card"})
    for product in products:
        name = product.find("div", {"class": "product-card__name"}).text
        amount = product.find("div", {"class": "product-card__description"}).text
        name = " ".join([name, amount])
        image = product.find("img")["src"]
        product_id = int(product.find("a", {"class", "product-card__image"})["href"].split("/")[-1])
        price = (int(product.find("span", {"class": "product-card__price__euros"}).text.replace(".", "")) * 100) + int(
            product.find("span", {"class": "product-card__price__cents"}).text)
        bonus = calculate_bonus(product)
        base_scraper.add_product(product_id, name, image, price, bonus)


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
    #
    else:
        base_scraper.add_scrape_error("No urls retrieved.")


if __name__ == '__main__':
    parse_all()

    # This keeps reference alive so we can call finish scrape history.
    del base_scraper
    driver.quit()
