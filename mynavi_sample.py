import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time
import pandas as pd
import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
import csv

LOG_FILE_PATH = "./log/log_{datetime}.log"
EXP_CSV_PATH="./exp_list_{search_keyword}_{datetime}.csv"
log_file_path=LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))

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
         return Chrome(ChromeDriverManager().install(), options=options) 
    else:
        return Firefox(executable_path=os.getcwd() + "/" + driver_path, options=options)

### ログファイルおよびコンソール出力
def log(txt):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now , txt)
    # ログ出力
    with open(log_file_path, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

# main処理


def main():
    log('処理開始')
    search_keyword = input("検索するワードを入力してください：")
    # driverを起動
    if os.name == 'nt':  # Windows
        driver = set_driver("chromedriver.exe", False)
    # elif os.name == 'posix': #Mac
    #     driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/list/kw"+search_keyword+"/?jobsearchType=14&searchType=18")
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')

    # 検索窓に入力
    # driver.find_element_by_class_name(
    #     "topSearch__text").send_keys(search_keyword)
    # # 検索ボタンクリック
    # driver.find_element_by_class_name("topSearch__button").click()
    
    title_xpath = "/html/body/div[1]/div[3]/div[1]/form/h1"
    title = driver.find_element_by_xpath(title_xpath)
    log(title.text)

    page_count = 1
    next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
    exp_name_list = []
    exp_annual_income_list = []
    exp_place_list = []
    while True:
        # ページ終了まで繰り返し取得
        # 検索結果の一番上の会社名とテーブルの値を取得
        name_list = driver.find_elements_by_class_name(
            "cassetteRecruit__name")
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")
        count = 0
        # 1ページ分繰り返し
        for name, table in zip(name_list, table_list):
            try:
                place =  find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "勤務地")
                annual_income = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "初年度年収")
                print(name.text)
                exp_name_list.append(name.text)
                exp_annual_income_list.append(annual_income)
                exp_place_list.append(place)
                log(str(count)+'件目成功')
            except Exception as e:
                log(str(count)+'件目失敗')
                pass
            finally:
                count += 1
        # 最終ページであるかの確認
        if len(next_page) >= page_count:
            log('--------------------'+str(page_count)+'ページ目終了--------------------')
            page_count +=1
            # 次ページボタン(>)クリック  
            driver.find_element_by_class_name("iconFont--arrowLeft").click()     
        else:
            log('--------------------'+str(page_count)+'ページ目終了--------------------')
            break

    #CSV出力
    # DataFrameに対して辞書形式でデータを追加する
    try:

        df = pd.DataFrame(
            {
            "会社名": exp_name_list,
            "初年度年収": exp_annual_income_list,
            "勤務地": exp_place_list})
        df.to_csv("stock.csv",encoding="UTF_8_sig")
    except Exception as e:
        log('CSVの出力に失敗しました')
    #処理終了
    log('処理終了')

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
