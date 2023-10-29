from multiprocessing import Process

def crawl_python():
    from crawler104jobs import Crawler104Jobs
    Crawler104Jobs("python", "crawler_python", "Chrome")

def crawl_java():
    from crawler104jobs import Crawler104Jobs
    Crawler104Jobs("java", "crawler_java", "Edge")

if __name__ == "__main__":
    # 創建兩個進程，分別執行 crawl_python 和 crawl_java 函式
    process_python = Process(target=crawl_python)
    process_java = Process(target=crawl_java)

    # 啟動進程
    process_python.start()
    process_java.start()

    # 等待兩個進程完成
    process_python.join()
    process_java.join()
