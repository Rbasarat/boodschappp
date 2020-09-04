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
driver_path = "./driver/chromedriver.exe"
base_scraper = BaseScraper("Albert Heijn", ScrapeType.SINGLE)
driver = webdriver.Chrome(options=options, executable_path=driver_path)
ah_base_url = "https://www.ah.nl"


# homepage = open("./testHtml/ah_producten.html", "rb")

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


def get_urls():
    urls = []
    try:
        homepage = safe_request(ah_base_url + "/producten")
        soup = BeautifulSoup(homepage, "lxml")
        scrape_urls = soup.find_all("div", {"class": "product-category-overview_category__1H99m"})
        with alive_bar(len(scrape_urls), title="Retrieving urls...", spinner="classic") as bar:
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
                        urls.append(ah_base_url + category_url + soort_url + "&page=68")
                bar()

        return urls
    except Exception as err:
        base_scraper.add_scrape_error(str(err))
        return urls


def scrape_product(product_page):
    soup = BeautifulSoup(product_page, "lxml")
    products = soup.find("div", {"class": "search-lane-wrapper"}).find_all("article")
    for product in products:
        gall_gall = product.find("svg", {"class": "svg--gall"})
        etos = product.find("svg", {"class": "svg--etos"})
        
        if not gall_gall or etos:
            name = product.find("span", {"class": "line-clamp line-clamp--active title_lineclamp__10wki"}).text
            image = product.find("img")["src"]
            product_id = re.findall(r"\/wi([a-zA-Z0-9]+)\/", product.find("a")["href"], re.MULTILINE)[0]
            price = (int(product.find("span", {"class": "price-amount_integer__N3JDd"}).text) * 100) + int(
                product.find("span", {"class": "price-amount_fractional__3sfJy"}).text)
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

    else:
        base_scraper.add_scrape_error("No urls retrieved.")


if __name__ == '__main__':
    if int(argv[1]) == 1:
        parse_all()

    # This keeps reference alive so we can call finish scrape history.
    del base_scraper
    driver.quit()
