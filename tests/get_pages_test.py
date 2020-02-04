import json
import unittest

from hachinai_scraping import get_pages


class TestGetPage(unittest.TestCase):
    def test_url(self):
        url = ''
        actual = get_pages(url)
        print(json.dumps(actual, indent='\t', ensure_ascii=False))
        self.assertIsNotNone(actual)


if __name__ == '__main__':
    unittest.main()
