import urllib.request, urllib.error                         # urlアクセス
import requests                                             # urlアクセス
from bs4 import BeautifulSoup                               # web scraping用
from selenium import webdriver                              # 動的ページに対するscraping用
from selenium.webdriver.chrome.options import Options       # webdriverの設定用
import time                                                 # scrapingの時間制御用

def main():
    # 駅情報格納用
    stationInfo = {}    #{'駅名-路線':'ページurl'}
    text = ""
    reUrl = ""
    reUrlCnt = 0

    # ブラウザのオプションを格納する変数をもらってくる。
    options = Options()
    # Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がる）
    options.set_headless(True)
    # ブラウザを起動
    driver = webdriver.Chrome(chrome_options=options, executable_path='C:\\chromedriver.exe')
    # ブラウザでアクセスする
    driver.get(f"https://transit.goo.ne.jp/station/train/confirm.php?st_name=渋谷駅&input=検索")
    # HTMLを文字コードをUTF-8に変換してから取得します。
    html = driver.page_source.encode('utf-8')
    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    # 出口情報整理
    stationName_tag = soup.select('ul.stationname > li > a')    # 例：<a href="/station/train/kantou/山手線/山手線-130265/">渋谷-山手線</a>
    for sn_tag in stationName_tag:
        stationName = sn_tag.string
        stationInfo[stationName] = sn_tag.get('href')

    # 出口案内情報を取得
    for stationName in stationInfo:
        # urlの作り直し
        exitUrl = stationInfo[stationName].split('/')
        for exitUrlOne in exitUrl:
            print(exitUrlOne)
            if reUrlCnt == 4:
                reUrlCnt += 1
                continue
            else:
                reUrlCnt += 1
                reUrl = reUrl + exitUrlOne + '/'
        print("******************************:")
        print(reUrl)
        driver.get(f"https://transit.goo.ne.jp{reUrl}exit.html")        # 出口案内ページアクセス
        html = driver.page_source.encode('utf-8')       # HTMLを文字コードをUTF-8に変換してから取得します。
        soup = BeautifulSoup(html, "html.parser")       # htmlをBeautifulSoupで扱う

        # 出口と施設をリストexitInfoへ格納
        print(soup)
        facility_tag = soup.find_all(id='facility')
        print(facility_tag)
        break

    return



if __name__ == "__main__":
    # メイン関数
    main()
