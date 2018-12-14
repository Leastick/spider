import unittest
import lib.url_parser as url_parser
from lib.parsed_page import Page


class UrlParserTest(unittest.TestCase):

    def test_remove_beginning(self):
        self.assertEqual(('http://', 'www.example.ru'), url_parser.remove_beginning('http://www.example.ru'))
        self.assertEqual(('http://', 'example.ru'), url_parser.remove_beginning('http://example.ru'))
        self.assertEqual(('https://', 'example.ru'), url_parser.remove_beginning('https://example.ru'))
        self.assertEqual(('', 'www.example.ru'), url_parser.remove_beginning('www.example.ru'))

    def test_updir(self):
        self.assertEqual('www.example.ru/level1/level2/level3/',
                         url_parser.get_updir('www.example.ru/level1/level2/level3/index.html', 0))
        self.assertEqual('www.example.ru/level1/level2/',
                         url_parser.get_updir('www.example.ru/level1/level2/level3/index.html', 1))
        self.assertEqual('www.example.ru/level1/',
                         url_parser.get_updir('www.example.ru/level1/level2/level3/index.html', 2))
        self.assertEqual('www.example.ru/',
                         url_parser.get_updir('www.example.ru/level1/level2/level3/index.html', 4))
        self.assertEqual('www.example.ru/',
                         url_parser.get_updir('www.example.ru/level1/level2/level3/index.html', 1000))

    def test_make_absolute_path(self):
        self.assertEqual('https://www.example.ru/dir1/page1.html',
                         url_parser.make_absolute_path('https://www.example.ru/dir1/page.html',
                                                       'page1.html')
                         )
        self.assertEqual('https://www.example.ru/dir1/page.html',
                         url_parser.make_absolute_path('https://www.example.ru/dir1/dir2/dir3/page.html',
                                                       '../../page.html')
                         )
        self.assertEqual('https://www.example.com.tr/dir0/page.html',
                         url_parser.make_absolute_path('https://www.example.com.tr/dir1/dir2/dir3/page.html',
                                                       '/dir0/page.html')
                         )

    def test_is_relative_link(self):
        self.assertFalse(url_parser.is_relative_link('http://www.example.com'))
        self.assertFalse(url_parser.is_relative_link('https://www.example.com'))
        self.assertTrue(url_parser.is_relative_link('/index.html'))
        self.assertTrue(url_parser.is_relative_link('../../../index.html'))
        self.assertTrue(url_parser.is_relative_link('../index.html'))

    def test_iri_to_uri(self):
        self.assertEqual('http://xn--j1ail.xn--p1ai/#reg',
                         url_parser.iri_to_uri('http://кто.рф/#reg'))
        self.assertEqual('https://www.example.com',
                         url_parser.iri_to_uri('https://www.example.com'))
        self.assertEqual('https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8',
                         url_parser.iri_to_uri('https://ru.wikipedia.org/wiki/Вики'))


class PageTest(unittest.TestCase):
    def setUp(self):
        with open('tests/test_data/grammy.html', 'r') as f:
            grammy_html = f.read()
        self.grammy_page = Page('https://tass.ru/kultura/5885752?utm_source=yxnews&utm_medium=desktop',
                                grammy_html)
        with open('tests/test_data/test.html', 'rb') as f:
            test_html = f.read().decode('windows-1251')
        self.test_page = Page('https://www.test-site.com.tr/dir1/dir2/dir3/index.html',
                              test_html)

    def test_get_title(self):
        self.assertEqual('Объявлены номинанты на Grammy-2019 -  Культура - ТАСС',
                         self.grammy_page.get_title())
        self.assertEqual('Тестовый html-файл',
                         self.test_page.get_title())

    def test_get_hyperlinks(self):
        self.assertEqual(
            {
                'https://www.youtube.com/watch?v=k3UmYLE0F5k',
                'https://www.billboard.com/articles/news/grammys/8489045/2019-grammy-nominees-full-list',
                'https://www.liveinternet.ru/click;TASS_total'
             },
            set(self.grammy_page.get_hyperlinks_list())
        )
        # https://www.test-site.com.tr/dir1/dir2/dir3/index.html
        self.assertEqual(
            {
                'https://www.test-site.com.tr/dir1/subdir/index.html',  # href="../../subdir/index.html"
                'https://www.test-site.com.tr/dir1/dir2/dir3/index1.html',  # href="index1.html"
                'https://www.example.com',  # href="https://www.example.com"
                'https://www.test-site.com.tr/bbb/aaa.html',  # href="/bbb/aaa.html"
            },
            set(self.test_page.get_hyperlinks_list()))


if __name__ == '__main__':
    unittest.main()
