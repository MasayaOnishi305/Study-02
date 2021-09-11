from os import system
import eel
import desktop
import mynavi_sample

app_name="html"
end_point="index.html"
size=(700,700)

@ eel.expose
#index.html オーダー履歴表示処理
def search(search_word:str):
    '''
    検索結果を取得する
    '''
  
    # Orderが存在しなければOrderインスタンスを作成
    res = mynavi_sample.serch(search_word)
    if not res:
        eel.alertJs(f"『{search_word}』の検索結果は0件です")
    else:
        eel.return_log(res)

@eel.expose
def csv_output(csv_name):
    '''
    csvファイルの出力
    '''

    message = mynavi_sample.csv_rename(csv_name)
    eel.alertJs(message)


if __name__ == "__main__":
    desktop.start(app_name,end_point,size)
    