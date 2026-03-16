import streamlit as st
import plotly.express as px
from pipeline.data_maneger import TradeDataManager

# --- 1. ページ全体の基本設定 ---
st.set_page_config(page_title="貿易統計分析", layout="wide")

# --- 2. データの読み込み (一度だけ実行されるようキャッシュを検討しても良い) ---
data_manager = TradeDataManager()
df = data_manager.df

# --- 3. メインタイトル（ここを一番上に持ってくる） ---
st.title("📈 貿易統計：品目別単価分析")
st.caption("経産省のサイトから取得した最新の貿易データを可視化します。")

# --- 4. サイドバーでの設定 ---
st.sidebar.header("表示設定")

# 「合計」行をリストから除外し、ソートして表示
unique_countries = sorted(df[~df["国名"].str.contains("合計", na=False)]["国名"].unique())

selected_countries = st.sidebar.multiselect(
    "分析対象の国を選択してください", 
    unique_countries
)

# --- 5. データの表示・グラフ作成 ---
if selected_countries:
    # フィルタリング
    filtered_df = df[df["国名"].isin(selected_countries)].sort_values("年月", ascending=False)

    # A. グラフの作成
    fig = px.line(
        filtered_df, 
        x="年月", 
        y="単価", 
        color="国名", 
        markers=True,
        title="単価の推移（円/単位）",
        hover_data={"年月": "|%Y/%m", "単価": ":.2f"}
    )

    fig.update_layout(hovermode="x unified")
    # x軸のフォーマットを年月表示に変更
    fig.update_xaxes(tickformat="%Y/%m")
    st.plotly_chart(fig, use_container_width=True)

    # B. 詳細表の表示（改善版）
    st.subheader("📋 詳細データ一覧")
    st.dataframe(
        filtered_df,
        column_config={
            "年月": st.column_config.DateColumn("年月", format="YYYY/MM"),
            "単価": st.column_config.NumberColumn("単価", format="¥%d"),
            "累計_金額": st.column_config.NumberColumn("累計金額", format="%d"),
            "累計_第2数量": st.column_config.NumberColumn("累計数量", format="%d"),
        },
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("👈 左側のサイドバーから分析したい国を選択してください。")