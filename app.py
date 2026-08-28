import streamlit as st

st.set_page_config(page_title="會消失的井字棋", page_icon="❌", layout="centered")

# 🛠️ 強制手機版保持橫向 3×3 九宮格排版
st.markdown("""
    <style>
    /* 1. 強制欄位區塊（stHorizontalBlock）在手機上也維持單行橫排 */
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        gap: 0.5rem !important;
    }
    
    /* 2. 解除欄位最小寬度限制，避免手機版自動折行 */
    [data-testid="column"] {
        min-width: 0px !important;
        flex: 1 1 0% !important;
    }

    /* 3. 優化按鈕外觀：將按鈕做成正方形且放大字體 */
    div.stButton > button {
        width: 100% !important;
        height: 75px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)
