import logging


class Scraper:
    """_summary_
    
        * インターフェースです。スクレイプするサイトごとにこのクラスを実装すること
        e.g.)
            Scraper <- MyScraper <- GoogleScraper
            Scraper <- MyScraper <- YahooScraper
            
        * サイトごとに変わる処理・パラメータを継承先のクラスで定義すること
        * SchedulerクラスのメンバにこのScraperクラスが存在し、Schedulerがexecを叩く
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

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
