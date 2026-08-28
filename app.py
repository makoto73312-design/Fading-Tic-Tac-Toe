import streamlit as st

# 頁面基本設定
st.set_page_config(page_title="會消失的井字棋", page_icon="❌", layout="centered")

# 注入 CSS 確保手機版保持 3x3 九宮格排版
st.markdown("""
    <style>
    /* 1. 強制欄位區塊在手機上維持橫向排列 */
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
        gap: 0.5rem !important;
    }
    
    /* 2. 解除欄位最小寬度限制，避免手機版自動垂直堆疊 */
    [data-testid="column"] {
        min-width: 0px !important;
        flex: 1 1 0% !important;
    }

    /* 3. 優化按鈕外觀：做成正方形且放大字體 */
    div.stButton > button {
        width: 100% !important;
        height: 80px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. 初始化 Session State
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.o_queue = []  # 記錄 O 下棋的位置與順序 (FIFO)
    st.session_state.x_queue = []  # 記錄 X 下棋的位置與順序 (FIFO)
    st.session_state.turn = "O"
    st.session_state.winner = None

# 2. 勝利條件判定
def check_win(board, player):
    win_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 橫線
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 直線
        [0, 4, 8], [2, 4, 6]              # 對角線
    ]
    return any(all(board[i] == player for i in line) for line in win_lines)

# 3. 落子邏輯處理
def handle_click(index):
    # 若已被佔用或已有贏家，不執行任何動作
    if st.session_state.board[index] != "" or st.session_state.winner:
        return

    current = st.session_state.turn
    queue = st.session_state.o_queue if current == "O" else st.session_state.x_queue

    # 放
