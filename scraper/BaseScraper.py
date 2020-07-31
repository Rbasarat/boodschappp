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

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def __del__(self):
        self.finish_scrape_history()
        self.cursor.close()
        self.cnx.close()

    def increment_scrape_error(self):
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
        price_in_cents = int(str(price).ljust(4, "0"))
        if self.is_price_changed(product_id, price_in_cents):
            query = ("INSERT INTO Product (Id, store_id, name, image, price, bonus) "
                     "VALUES (%s, %s, %s, %s, %s, %s)")
            product = (product_id, self.store_id, name, image, price_in_cents, bonus)
            self.write_to_db(query, product)

    def get_user_agents(self):
        self.cursor.execute("SELECT agent FROM UserAgents")
        self.user_agents = self.cursor.fetchall()

    def get_store_id(self, store_name):
        query = "SELECT Id FROM GroceryStore WHERE store_name = %s"
        self.cursor.execute(query, (store_name,))
        self.store_id = self.cursor.fetchone()

    # TODO: error/logging do we want it here or not?
    def write_to_db(self, query, data):
        try:
            self.cursor.execute(query, data)
            self.cnx.commit()
            return True
        except mysql.connector.Error as e:
            try:
                print("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                return False
            except IndexError:
                print("MySQL Error: %s" % str(e))
                return False
        except TypeError as e:
            print(e)
            return False
        except ValueError as e:
            print(e)
            return False

    def safe_request(self, url):
        time.sleep(random.randint(1000, 2500) / 1000)
        try:
            response = requests.get(url, headers={"User-Agent": random.choice(self.user_agents["agent"])})
            return response
        # TODO: catch different errors
        except requests.exceptions.RequestException:
            print("Error retrieving url: " + url)


p = BaseScraper("Albert Heijn", ScrapeType.FULL)
p.add_product(100105, "test", "https:nivero.io", 523555, 0)
del p
