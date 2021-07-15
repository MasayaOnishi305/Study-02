import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    if "chrome" in driver_path:
        options = ChromeOptions()
    else:
        options = Options()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    if "chrome" in driver_path:
        return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)
    else:
        return Firefox(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt':  # Windows
        driver = set_driver("chromedriver.exe", False)
    # elif os.name == 'posix': #Mac
    #     driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/list/kw%E9%AB%98%E5%8F%8E%E5%85%A5/pg2/?jobsearchType=14&searchType=18")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()
    # 次ページボタン(>)の有無で最終ページであるか確認
    while True:
        next_gage = driver.find_elements_by_class_name("pager__next")
        if len(next_gage) > 0:
    # ページ終了まで繰り返し取得
    # 検索結果の一番上の会社名とテーブルの値を取得
            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
            table_list = driver.find_elements_by_class_name("tableCondition__body")
    # 空のDataFrame作成
            df = pd.DataFrame()
            i = 2
            j = 4

    # 1ページ分繰り返し
            print(len(name_list))
            for name in name_list:
                place = table_list[i]
                annual_income = table_list[j]
                print(name.text)
                print(annual_income.text)
                print(place.text)
                # DataFrameに対して辞書形式でデータを追加する
                df = df.append(
                    {"会社名": name.text,
                    "初年度年収": annual_income.text,
                    "勤務地": place.text},
                    ignore_index=True)
                i += 5
                j += 5
                print(i)
            # 次ページボタン(>)クリック
            driver.find_element_by_class_name("pager__next").click()
        else:
            break


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
