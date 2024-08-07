import schedule
import time


class Scheduler:
    """_summary_
    指定間隔で実行する。
    もしexec処理に5分以上かかった場合、終了後すぐに次の処理が開始される。
    
        Usage:
            def main():
                # スクレイパーのインスタンスを作成
                scraper1 = MyScraper1()
                scraper2 = MyScraper2()

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
    
    """

    def __init__(self, interval, scraper):
        self.interval = interval
        self.scraper = scraper

    def start(self):
        self.scraper.exec()
        schedule.every(self.interval).minutes.do(self.scraper.exec)

        while True:
            schedule.run_pending()
            time.sleep(1)
            
    # def start(self):
    #     while True:
    #         self.scraper.exec()
    #         time.sleep(self.interval * 60)  # intervalは分単位なので秒単位に変換
