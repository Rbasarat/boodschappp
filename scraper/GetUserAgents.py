from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import os


# We need to redo this in the future. Find a better way to retrieve up to date user agents.
class GetUserAgents:
    # There are lots of browsers that are too old in here.
    user_agents_source_base = "https://developers.whatismybrowser.com"
    config = {
        "user": "root",
        "password": "admin",
        "host": "192.168.0.123",
        "database": "boodschappp",
        "raise_on_warnings": True
    }
    add_user_agent = ("INSERT INTO UserAgents "
                      "(agent, software, os) "
                      "VALUES (%s, %s, %s)")

    def __init__(self):
        try:
            cnx = mysql.connector.connect(**self.config)
            cursor = cnx.cursor()
            self.scrape_user_agent_from_html(cnx, cursor)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cursor.close()
            cnx.close()

    # Make sure we dont use browsers that are too old.
    @staticmethod
    def check_agent_version(agent):
        split = agent.split(" ")
        if "safari" in split[0].lower():
            return float(split[1]) > 12
        if "edge" in split[0].lower():
            return float(split[1]) > 17
        if "opera" in split[0].lower():
            return float(split[1]) > 60
        if "internet" in split[0].lower():
            return False

        try:
            float(split[1].lower())
            return float(split[1]) > 70
        except ValueError:
            return False

    def scrape_user_agent_from_html(self, cnx, cursor):
        for filename in os.listdir("./userAgents"):
            if filename.endswith(".html"):
                f = open("./userAgents/" + filename, "r")
                soup = BeautifulSoup(f, "lxml")
                rows = soup.find("tbody").find_all("tr")
                for row in rows:
                    columns = row.find_all("td")
                    if self.check_agent_version(columns[1].text):
                        data_user_agent = (columns[0].text, columns[1].text, columns[2].text)
                        cursor.execute(self.add_user_agent, data_user_agent)
                        cnx.commit()


p = GetUserAgents()
