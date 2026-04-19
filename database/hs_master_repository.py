
from database.supabase_client import get_public_client

# SupabaseからHSコードのレベル4のデータを取得し、リストとして返す
def get_level4_hscodes():
    supabase = get_public_client()
    
    response = supabase.table("hs_master").select("*").eq("level", 4).execute()
    
    if response.data:
        hs_codes = [r["hs_code"] for r in response.data]
    return hs_codes