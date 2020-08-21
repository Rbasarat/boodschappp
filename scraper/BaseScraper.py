import requests
import random
import time
import mysql.connector
from mysql.connector import errorcode
import enum
from datetime import datetime


class ScrapeType(enum.Enum):
    FULL = 1
    SINGLE = 2


class BaseScraper:
    config = {
        "user": "root",
        "password": "admin",
        "host": "192.168.0.123",
        "database": "boodschappp",
        "raise_on_warnings": True
    }
    user_agents = []
    cnx = None
    cursor = None
    store_id = None
    scrape_history_id = None
    scrape_error = 0
    retry_count = 0

    def __init__(self, store, scrape_type):
        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cursor = self.cnx.cursor(dictionary=True)
            print("Setting store Id.")
            self.get_store_id(store)
            if self.store_id is None or len(self.store_id) == 0:
                raise ValueError("Store not found")
            else:
                self.store_id = self.store_id["Id"]

            self.init_scrape_history(scrape_type)
            print("Retrieving user agents.")
            self.get_user_agents()
            if len(self.user_agents) < 0:
                raise Exception("No user agents found!")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.add_scrape_error("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.add_scrape_error("Database does not exist")
            else:
                self.add_scrape_error(err)

    def __del__(self):
        self.finish_scrape_history()
        self.cursor.close()
        self.cnx.close()

    def add_scrape_error(self, message, product_id=None, ):
        query = ("INSERT INTO ScrapeErrors"
                 "(scrape_id, product_id, date, message)"
                 "VALUES ('%s', '%s', '%s')")
        self.write_to_db(query, (self.scrape_history_id, product_id, message,))
        self.scrape_error += 1

    def init_scrape_history(self, scrape_type):
        self.cursor.execute('SELECT UUID()')
        self.scrape_history_id = self.cursor.fetchone()["UUID()"]
        query = ("INSERT INTO ScrapeHistory "
                 "(Id, store_id, scrape_type) "
                 "VALUES (%s, %s, %s)")
        self.write_to_db(query, (self.scrape_history_id, self.store_id, scrape_type.value,))

    def finish_scrape_history(self):
        query = "UPDATE ScrapeHistory SET end_date= %s, error_count= %s WHERE Id = %s"
        self.write_to_db(query, (datetime.now(), self.scrape_error, self.scrape_history_id,))

    def is_price_changed(self, product_id, price):
        self.cursor.execute("SELECT price FROM Product WHERE Id = %s AND store_id = %s ORDER BY last_updated DESC ",
                            (product_id, self.store_id,))
        result = self.cursor.fetchall()
        if len(result) > 0:
            return result[0]["price"] != price
        else:
            return True

    # We already checked for null when calling this.
    def add_product(self, product_id, name, image, price, bonus):
        # Price is in cents.
        price_in_cents = int(str(price).ljust(4, "0"))
        # Only write new record if price has changed. Safes db space.
        if self.is_price_changed(product_id, price_in_cents):
            query = ("INSERT INTO Product (Id, store_id, name, image, price, bonus) "
                     "VALUES (%s, %s, %s, %s, %s, %s)")
            product = (product_id, self.store_id, name, image, price_in_cents, bonus)
            self.write_to_db(query, product)

    def get_user_agents(self):
        self.cursor.execute("SELECT agent FROM UserAgents")
        self.user_agents = self.cursor.fetchall()

    def get_store_id(self, store_name):
        self.cursor.execute("SELECT Id FROM GroceryStore WHERE store_name = %s", (store_name,))
        self.store_id = self.cursor.fetchone()

    # TODO: error/logging do we want it here or not?
    def write_to_db(self, query, data):
        try:
            self.cursor.execute(query, data)
            self.cnx.commit()
        except mysql.connector.Error as e:
            try:
                # self.add_scrape_error("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                print(e.args[1])
            except IndexError:
                self.add_scrape_error("MySQL Error: %s" % str(e))

    def safe_request(self, url):
        time.sleep(random.randint(1000, 2500) / 1000)
        try:
            if self.retry_count > 3:
                raise requests.exceptions.RequestException
            response = requests.get(url, headers={"User-Agent": random.choice(self.user_agents)["agent"]})
            return response
        # TODO: catch different errors
        except requests.exceptions.RequestException:
            self.safe_request(url)
            self.retry_count += 1
        finally:
            if self.retry_count > 3:
                self.retry_count = 0
                self.add_scrape_error("Failed to retrieve url:" + url)
