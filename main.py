import threading

from lib.scheduler import Scheduler
from site.my_scraper import MyScraper


def main():
    # スクレイパーのインスタンスを作成
    scraper1 = MyScraper() # ※自身のプロジェクトではMyScraperを継承したクラスをインスタンス化する
    scraper2 = MyScraper()

    # スケジューラーのインスタンスを作成
    scheduler1 = Scheduler(5, scraper1)
    scheduler2 = Scheduler(10, scraper2)

    # スケジューラーを別々のスレッドで開始
    thread1 = threading.Thread(target=scheduler1.start)
    thread2 = threading.Thread(target=scheduler2.start)

    thread1.start()
    thread2.start()

    # 全てのスレッドが終了するまで待つ
    thread1.join()
    thread2.join()


if __name__ == "__main__":
    main()
