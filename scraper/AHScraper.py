from BaseScraper import ScrapeType
from BaseScraper import BaseScraper
from bs4 import BeautifulSoup
from sys import argv
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
# options.headless = True
driver_path = "./driver/chromedriver.exe"
base_scraper = BaseScraper("Albert Heijn", ScrapeType.SINGLE)
driver = webdriver.Chrome(options=options, executable_path=driver_path)
ah_base_url = "https://www.ah.nl"


def safe_request(url, element=None):
    retry_count = 0

    try:
        time.sleep(random.randint(1000, 2500) / 1000)
        if retry_count > 3:
            return
        driver.get(url)
        if element:
            driver.find_elements_by_class_name(element)[1].click()

        return driver.page_source
        # TODO: catch different errors
    except TimeoutException:
        retry_count += 1
        safe_request(url)
    except NoSuchElementException:
        base_scraper.add_scrape_error("Element not found on: " + url + "with element:" + element)
    finally:
        driver.close()
        if retry_count > 3:
            base_scraper.add_scrape_error("TimeoutException: Failed to retrieve url:" + url)


def parse_all():
    # TODO: switch this after testing
    # homepage = safe_request(ah_base_url + "producten")
    homepage = open("./testHtml/ah_producten.html", "rb")
    soup = BeautifulSoup(homepage, "lxml")
    scrape_urls = soup.find_all("div", {"class": "product-category-overview_category__1H99m"})

    # for url in scrape_urls:
    # TODO: switch this after testing
    # category_url = url.find("a")["href"]
    category_url = "/aardappel-groente-fruit"
    # category = safe_request(ah_base_url + category_url, "filter-group_showMore__3nXJH")
    category = open("./testHtml/ah_producten_category.html", "rb")
    soup = BeautifulSoup(category, "lxml")
    product_soorten = soup.find("span", string="Soorten", attrs={'class': 'filter-group_titleText__2ErIs'}) \
        .find_parent("div", {"class": "collapsible-block-element_root__2MU-5"}) \
        .find_all("a", {"class": "filter-group_filter__2kWhF"})
    # for url in product_soorten:
    #     soort_url = url.find("a")["href"]
    #     productPage  = safe_request(ah_base_url + category_url + soort_url + "&page=100")
    productPage = open("./testHtml/ah_producten_category_soort.html", "rb")
    soup = BeautifulSoup(productPage, "lxml")

    #
    # soup = BeautifulSoup(category, "lxml")
    print(productPage)


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
