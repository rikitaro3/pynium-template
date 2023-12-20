from lib.case import Case
from lib.scraper import Scraper


class MyScraper(Scraper):
    """_summary_
        サンプル自身のプロジェクト共通のScraperクラス。サイト共通の処理をここに記載

    Args:
        Scraper (_type_): _description_
    """

    def exec(self):
        raise NotImplementedError

    def exec_selenium(self):
        raise NotImplementedError

    def extract(self, html):
        raise NotImplementedError

    def format(self, scraped_data):
        raise NotImplementedError

    def output(self, data_list):
        raise NotImplementedError
