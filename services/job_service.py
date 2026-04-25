from selenium import webdriver
from scraper.trade_data_scraper import single_scraper
from tqdm import tqdm
from database.trade_data_repository import save_to_supabase
from services.trade_data_transform import list_to_df
from database.trade_data_repository import get_unique_hsCodeList


# 年月とHSコードのリストを受け取り、スクレイピング処理を実行する関数
def scrape_trade_data(year_month_list, hs_code_list):
    # Chromeドライバーのパスを指定してブラウザを起動
    driver = webdriver.Chrome()

    completed_hs_codes = get_unique_hsCodeList()



    for hs_code in tqdm(hs_code_list,desc = "Processing HSコード"):
        # すでに完了しているHSコードはスキップ
        if hs_code in completed_hs_codes:
            tqdm.write(f"Skipping HSコード: {hs_code} (already completed)")
            continue
        
        all_data = []
        for year, month in tqdm(year_month_list,desc = f"Processing 月別 for HSコード: {hs_code}", leave=False):
            tqdm.write(f"Processing HSコード: {hs_code}, Year: {year}, Month: {month}")
            all_data.extend(single_scraper(driver, year, month, hs_code))

        # all_dataをDataFrameに変換
        df = list_to_df(all_data)

        # dfをsupabaseに保存
        save_to_supabase(df)
    driver.quit()
    return all_data