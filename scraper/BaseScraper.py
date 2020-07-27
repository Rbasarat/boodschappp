import datetime

import requests
from bs4 import BeautifulSoup
import random
import time

from requests.exceptions import ProxyError


class BaseScraper:
    user_agents_source_base = 'https://developers.whatismybrowser.com'
    proxy_sources = ['https://www.sslproxies.org/', 'https://free-proxy-list.net/']
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246']
    proxies = ['107.148.232.113:8888',
               '144.217.101.245:3129',
               '144.76.174.21:33973',
               '34.217.82.196:8888',
               '185.21.217.20:3128',
               '188.165.16.230:3129',
               '209.222.10.120:31965',
               '185.34.22.225:37879',
               '45.76.166.148:30323',
               '46.191.226.105:3128',
               '94.30.97.245:80',
               '81.201.60.130:80',
               '45.76.129.163:30481',
               '52.31.193.74:8118',
               '45.77.110.15:32001',
               '149.34.32.77:8082',
               '206.205.114.235:8888',
               '82.200.233.4:3128',
               '78.141.201.90:33723',
               '95.38.14.16:8080',
               '95.179.229.35:31843',

               ]
    proxy_error = 0
    succes = 0

    def __init__(self):
        # print('initializing proxies...')
        # self.get_proxies()
        # print('Done..')
        for x in range(100):
            start = datetime.datetime.now()
            self.safe_request('https://www.kongregate.com/')
            time = (datetime.datetime.now() - start)
            print('duration of request: ' + str(time))

        print('success count: ' + self.succes)

    # TODO: get the user agent list from api and parse to db

    # TODO: we want a report about how many proxies we have used.
    # TODO: we need to know how many proxies failed and how many we used
    # TODO: When do we renew a <b>user agent</b>
    def safe_request(self, url):
        timeout = random.randint(1000, 1001)
        if len(self.proxies) < 1:
            print('No more proxies left refreshing')
            self.get_proxies()

        proxy_url = random.choice(self.proxies)
        proxy = {'http': proxy_url, 'https': proxy_url}
        # Because sleep is in seconds
        time.sleep(timeout / 1000)
        try:
            response = requests.get(url, headers={'User-Agent': random.choice(self.user_agents)}, proxies=proxy)
            self.succes += 1
            return response
        except ProxyError:
            if self.proxy_error > 100:
                print('too many proxy errors aborting...')
            else:
                print('Request failed due to proxy, retrying...')
                self.proxies.remove(proxy_url)
                self.proxy_error += 1
                self.safe_request(url)

    def get_proxies(self):
        for source in self.proxy_sources:
            response = requests.get(source)
            soup = BeautifulSoup(response.content, 'lxml')
            proxies_table = soup.find(id='proxylisttable')
            # Save proxies in the array
            for row in proxies_table.tbody.find_all('tr'):
                self.proxies.append(':'.join([row.find_all('td')[0].string, row.find_all('td')[1].string]))
        print('proxy count: ', len(self.proxies))

    def scrape_user_agent_from_html(self, request):
        soup = BeautifulSoup(request.content, 'lxml')
        # Save user agents in the array
        for row in soup.find_all('td', {'class': 'useragent'}):
            self.user_agents.append(row.find('a').text)

    # def get_user_agents(self):
    #     # Scrape first page and then the others
    #     first_page = self.user_agents_source_base + '/useragents/explore/software_type_specific/web-browser/1'
    #     # We have only one user agent in our list yet.
    #     response = self.safe_request(first_page)
    #     self.scrape_user_agent_from_html(response)
    #     for a in BeautifulSoup(response, 'lxml').find(id='pagination').find_all('a', href=True):
    #         url = self.user_agents_source_base + a
    #         self.scrape_user_agent_from_html(self.safe_request(url))
    #     print('user agent count: ', len(self.user_agents))


p = BaseScraper()
