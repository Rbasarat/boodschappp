from BaseScraper import ScrapeType
from BaseScraper import BaseScraper
from bs4 import BeautifulSoup
from sys import argv
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import traceback

options = Options()
options.headless = True
driver_path = "./driver/chromedriver.exe"
base_scraper = BaseScraper("Albert Heijn", ScrapeType.SINGLE)
driver = webdriver.Chrome(options=options, executable_path=driver_path)
ah_base_url = "https://www.ah.nl"


def safe_request(url, element=None):
    retry_count = 0

    try:
        time.sleep(random.randint(1000, 10000) / 1000)
        if retry_count > 3:
            return
        driver.get(url)
        if element:
            driver.find_elements_by_class_name(element)[1].click()
        time.sleep(2)
        return driver.page_source
        # TODO: catch different errors
    except TimeoutException:
        retry_count += 1
        safe_request(url)
    except NoSuchElementException:
        base_scraper.add_scrape_error("Element not found on: " + url + "with element:" + element)
    except Exception as err:
        base_scraper.add_scrape_error("Generic error on safe request" + err.args[1])
    finally:
        if retry_count > 3:
            base_scraper.add_scrape_error("TimeoutException: Failed to retrieve url:" + url)


def calculate_bonus(product):
    bonus_block = product.find("div", {"class": "shield_root__YmXCB"})
    if bonus_block:
        bonus_type = base_scraper.get_bonus_types(bonus_block.span.text)
        if bonus_type:
            return bonus_type["Id"]
        else:
            base_scraper.add_bonus_type(bonus_block.span.text)
            return calculate_bonus(product)
    else:
        return None


def scrape_product(product_page):
    soup = BeautifulSoup(product_page, "lxml")
    products = soup.find("div", {"class": "search-lane-wrapper"}).find_all("article")
    for product in products:
        name = product.find("span", {"class": "line-clamp line-clamp--active title_lineclamp__10wki"}).text
        image = product.find("img")["src"]
        product_id = re.findall(r"\/wi([a-zA-Z0-9]+)\/", product.find("a")["href"], re.MULTILINE)[0]
        price = (int(product.find("span", {"class": "price-amount_integer__N3JDd"}).text) * 100) + int(
            product.find("span", {"class": "price-amount_fractional__3sfJy"}).text)
        bonus = calculate_bonus(product)
        base_scraper.add_product(product_id, name, image, price, bonus)


def parse_all():
    try:
        homepage = safe_request(ah_base_url + "/producten")
        soup = BeautifulSoup(homepage, "lxml")
        scrape_urls = soup.find_all("div", {"class": "product-category-overview_category__1H99m"})

        for url in scrape_urls:
            category_url = url.find("a")["href"]
            # Wijn page is different.
            if "wijn" in category_url:
                category = safe_request(ah_base_url + category_url)
                soup = BeautifulSoup(category, "lxml")
                product_soorten = soup.find("span", string="Wijnsoort",
                                            attrs={'class': 'filter-group_titleText__2ErIs'}) \
                    .find_parent("div", {"class": "collapsible-block-element_root__2MU-5"}) \
                    .find_all("a", {"class": "filter-group_filter__2kWhF"})
            else:
                category = safe_request(ah_base_url + category_url, "filter-group_showMore__3nXJH")
                soup = BeautifulSoup(category, "lxml")
                product_soorten = soup.find("span", string="Soorten", attrs={'class': 'filter-group_titleText__2ErIs'}) \
                    .find_parent("div", {"class": "collapsible-block-element_root__2MU-5"}) \
                    .find_all("a", {"class": "filter-group_filter__2kWhF"})

            for soort in product_soorten:
                soort_url = soort["href"]
                # skip this specific one since it has over 2k products
                if soort_url != "?soort=6407":
                    product_page = safe_request(ah_base_url + category_url + soort_url + "&page=100")
                    scrape_product(product_page)
    except Exception as err:
        base_scraper.add_scrape_error( traceback.print_exception(type(err), err, err.__traceback__))


def update_product():
    print("test2")


if __name__ == '__main__':
    if int(argv[1]) == 1:
        parse_all()
    elif int(argv[1]) == 2:
        update_product()

    # This keeps reference alive so we can call finish scrape history.
    del base_scraper
    driver.quit()
