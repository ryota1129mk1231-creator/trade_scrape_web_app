import pandas as pd
import numpy as np

def list_to_df(data):
    # all_dataをDataFrameに変換
    df = pd.DataFrame(data,columns=["year","month","hs_code","country_name","unit_1","unit_2","monthly_qty_1","monthly_qty_2","monthly_amount","cumulative_qty_1","cumulative_qty_2","cumulative_amount","unit_value"] )
    
    # "-"をNaNに変換
    df = df.replace("-", np.nan)

    # DataFrameの空文字をNaNに変換
    df = df.replace(r'^\s*$', np.nan, regex=True).infer_objects(copy=False)
    
    # NaNをNoneに変換
    df = df.replace({np.nan: None})

    return df