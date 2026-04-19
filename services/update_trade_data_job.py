
from database.hs_master_repository import get_level4_hscodes
from datetime import datetime
from services.job_service import scrape_trade_data
from database.trade_data_repository import save_to_supabase
from services.trade_data_transform import list_to_df



def run_job():
    #レベル4のHSコードを取得
    hs_codes = get_level4_hscodes()

    # 10年前から現在までの年月を生成
    current_year = datetime.now().year
    current_month = datetime.now().month
    year_month_list = []

    for year in range(current_year - 10, current_year + 1):
        for month in range(1, 13):

            if year == current_year and month > current_month:
                continue

            year_month_list.append((year, month))

    # スクレイピング処理を実行
    all_data = scrape_trade_data(year_month_list, hs_codes)

    
    