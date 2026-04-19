from supabase import create_client
from config.settings import *

def get_public_client():
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def get_admin_client():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)