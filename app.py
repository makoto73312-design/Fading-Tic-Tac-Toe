import streamlit as st

# 頁面基本設定
st.set_page_config(page_title="會消失的井字棋", page_icon="❌", layout="centered")

# 🛠️ 強制蓋過 Streamlit 的手機版防折行 CSS
st.markdown("""
    <style>
    /* 1. 強制橫向容器在所有螢幕尺寸下都保持橫向排列 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 6px !important;
    }
    
    /* 2. 強制三個欄位平分寬度（各 33.33%），防止手機版被改成 100% 垂直堆疊 */
    div[data-testid="stColumn"], div[data-testid="column"] {
        width: 33.33% !important;
        min-width: 0px !important;
        flex: 1 1 33.33% !important;
    }

    /* 3. 按鈕外觀微調：適應手機螢幕寬度，文字不折行 */
    div.stButton > button {
        width: 100% !important;
        height: 70px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 0px !important;
        white-space: nowrap !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. 初始化遊戲狀態
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.o_queue = []
    st.session_state.x_queue = []
    st.session_state.turn = "O"
    st.session_state.winner = None

# 2. 獲勝判定
def check_win(board, player):
    win_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 橫線
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 直線
        [0, 4, 8], [2, 4, 6]              # 對角線
    ]
    return any(all(board[i] == player for i in line) for line in win_lines)

# 3. 點擊邏輯
def handle_click(index):
    if st.session_state.board[index] != "" or st.session_state.winner:
        return

    current = st.session_state.turn
    queue = st.session_state.o_queue if current == "O" else st.session_state.x_queue

    queue.append(index)
    st.session_state.board[index] = current

    if len(queue) > 3:
        oldest_index = queue.pop(0)
        st.session_state.board[oldest_index] = ""

    if check_win(st.session_state.board, current):
        st.session_state.winner = current
    else:
        st.session_state.turn = "X" if current == "O" else "O"

# 4. 重置邏輯
def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.o_queue = []
    st.session_state.x_queue = []
    st.session_state.turn = "O"
    st.session_state.winner = None

# 5. UI 渲染
st.title("👻 會消失的井字棋")

if st.session_state.winner:
    st.balloons()
    st.success(f"🎉 玩家 **{st.session_state.winner}** 獲勝！")
else:
    st.info(f"輪到玩家：**{st.session_state.turn}**")

# 6. 繪製 3x3 九宮格
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        val = st.session_state.board[idx]
        
        # 標記即將消失的棋子
        display_label = val
        if val == "O" and len(st.session_state.o_queue) == 3 and st.session_state.o_queue[0] == idx:
            display_label = "O ⚠️"
        elif val == "X" and len(st.session_state.x_queue) == 3 and st.session_state.x_queue[0] == idx:
            display_label = "X ⚠️"
        elif val == "":
            display_label = " "

        cols[col].button(
            display_label, 
            key=f"btn_{idx}", 
            on_click=handle_click, 
            args=(idx,), 
            use_container_width=True
        )

st.write("")
st.button("🔄 重新開始", on_click=reset_game, use_container_width=True)
