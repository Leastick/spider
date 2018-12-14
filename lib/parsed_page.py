import re
import lib.url_parser as url_parser


class Page:
    def __init__(self, url, html):
        self.__re_get_title = re.compile(r'<title>(.*?)</title>')
        self.__re_get_hyperlinks = re.compile(r'<a href="(?!javascript)(.+?)"')  # smth wrong here or maybe not here
        title, hyperlinks = self.__parse(html)
        self.__url = url
        self.__title = title
        self.__hyperlinks = hyperlinks
        self.__html = html

    def __parse(self, html):
        title = self.__re_get_title.search(html).group(1)
        hyperlinks = [link.group(1) for link in self.__re_get_hyperlinks.finditer(html)]
        return title, hyperlinks

    def get_hyperlinks_iter(self):
        for link in self.__hyperlinks:
            if not url_parser.is_relative_link(link):
                yield link
            else:
                yield url_parser.make_absolute_path(self.__url, link)

    def get_hyperlinks_list(self):
        return list(self.get_hyperlinks_iter())

    def get_title(self):
        return self.__title

    def get_url(self):
        return self.__url

    def get_html(self):
        return self.__html


