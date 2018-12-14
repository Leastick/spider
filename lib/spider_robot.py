from lib.parsed_page import Page
import lib.url_parser as url_parser
import asyncio
import urllib
import ssl
import os

LOGS_PATH = os.path.join(os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'logs'), 'logs.txt')


class Spider:
    def __init__(self, start_url, storage, max_depth):
        self.start_url = start_url
        self.max_depth = max_depth
        self.storage = storage
        self.__visited_urls = set()

    def __get_page_html(self, url):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            request = urllib.request.Request(url,
                                             None,
                                             headers={'User-Agent': 'Mozilla/5.0'})
            return urllib.request.urlopen(request).read().decode()
        except urllib.error.HTTPError as error:
            with open(LOGS_PATH, 'a') as f:
                f.write('{0} fails with code {1}\n'.format(url, error.code))
            return None
        except ValueError:
            url = url_parser.iri_to_uri(url)
            request = urllib.request.Request(url,
                                             None,
                                             headers={'User-Agent': 'Mozilla/5.0'})
            return urllib.request.urlopen(request).read().decode()

    def __dfs(self, url, current_depth):
        self.__visited_urls.add(url)
        if current_depth > self.max_depth:
            return
        if url not in self.storage.parsed_page:
            html = self.__get_page_html(url)
            if html is None:
                return
            page = Page(url, self.__get_page_html(url))
        else:
            page = self.storage.parsed_page[url]
        yield page
        for link in page.get_hyperlinks_iter():
            if link not in self.__visited_urls:
                yield from self.__dfs(link, current_depth + 1)

    def traverse(self):
        for page in self.__dfs(self.start_url, 0):
            yield page
