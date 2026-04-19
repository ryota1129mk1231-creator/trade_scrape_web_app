
from database.supabase_client import get_admin_client
# dfを受け取り、supabaseのテーブルに保存する関数
def save_to_supabase(df):
    supabase = get_admin_client()
    records = df.to_dict(orient="records")

    for i in range(0, len(records), 1000):
        batch = records[i:i+1000]

        supabase.table("trade_data").upsert(
            batch,
            on_conflict="year,month,hs_code,country_name"
        ).execute()