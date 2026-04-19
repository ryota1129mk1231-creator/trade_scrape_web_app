
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from tqdm import tqdm

# 指定された年月、HSコードからデータをスクレイピングする関数
def single_scraper(driver,year,month,hs_code):
    try:
        base_url = "https://www.customs.go.jp/toukei/srch/index.htm?M=01&P=1,2,,,,,,,,1,0,{param_year},0,{param_month},0,2,{param_HS_CODE},,,,,,,,,,1,,,,,,,,,,,,,,,,,,,,,,200"
        url = base_url.format(param_year=year, param_month=month, param_HS_CODE=hs_code)
        driver.get(url)

        # FR_M_INFOフレームが表示されるまで最大5秒待ち、表示されたらそのフレームに切り替える
        WebDriverWait(driver, 5).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, "FR_M_INFO"))
        )

        # maincolumnを取得し、テキストが「検索結果なし。」で始まるか確認
        maincolumn = driver.find_element(By.ID, "maincolumn")
        if maincolumn.text.startswith("検索結果なし。"):
            # データがない場合はURLと条件をログに出力して空のリストを返す
            tqdm.write(f"--- データなし ---")
            tqdm.write(f"条件: {year}-{month} (HS: {hs_code})")
            tqdm.write(f"URL: {url}")
            return []
        
        # テーブルが表示されるまで最大3秒待つ
        target_table = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "value"))
        )

        unit_table = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "normal"))
        )

        unit_rows = unit_table.find_elements(By.TAG_NAME, "tr")
        unit_cols = unit_rows[0].find_elements(By.TAG_NAME, "td")
        unit = unit_cols[0].text.strip()  

         # 単位から数字を抽出し、数字型に変換
        match = re.search(r"\((\d+)円\)", unit)
        if match:
            unit_value = int(match.group(1))
        else:
            unit_value = None  # 数字が見つからない場合はNoneを設定


        # ヘッダーを除いたデータ行を取得
        target_table = driver.find_element(By.CLASS_NAME, "value")
        rows = target_table.find_elements(By.TAG_NAME, "tr")

        all_rows = []
        # データをリストに格納
        for row in rows[2:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            row_data = [col.text.strip() for col in cols]

            # 年、月、HSコードを追加
            row_data.insert(0, year)
            row_data.insert(1, month)
            row_data.insert(2, hs_code)

            # 末尾に単位値を追加
            row_data.append(unit_value)

            all_rows.append(row_data)
        return all_rows
    except Exception as e:

        tqdm.write(f"--- エラー発生 ---")
        tqdm.write(f"条件: {year}-{month} (HS: {hs_code})")
        tqdm.write(f"URL: {url}")
        tqdm.write(f"エラー内容: {e}")

        # エラーが発生した場合は空のリストを返す
        return []
    finally:        # フレームから元のコンテキストに戻る
        driver.switch_to.default_content()


