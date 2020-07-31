import requests
import random
import time
import mysql.connector
from mysql.connector import errorcode


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
    query_get_user_agents = "SELECT agent FROM UserAgents"

    def __init__(self):
        try:
            self.cnx = mysql.connector.connect(**self.config)
            self.cursor = self.cnx.self.cursor()
            print("Retrieving user agents..")
            self.cursor.execute(self.query_get_user_agents)
            self.user_agents = [row[0] for row in self.cursor.fetchall()]

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor.close()
            self.cnx.close()

    def write_to_db(self, query, data):
        try:
            self.cursor.execute(query, data)
            self.cnx = self.cursor.commit()
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
            response = requests.get(url, headers={"User-Agent": random.choice(self.user_agents)})
            return response
        # TODO: catch different errors
        except requests.exceptions.RequestException:
            print("Error retrieving url: " + url)


p = BaseScraper()
