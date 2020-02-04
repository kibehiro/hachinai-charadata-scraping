import unittest

from hachinai_scraping import get_pages


class TestGetPage(unittest.TestCase):
    def test_url(self):
        url = ''
        actual = get_pages(url)
        self.assertIsNotNone(actual)


if __name__ == '__main__':
    unittest.main()
