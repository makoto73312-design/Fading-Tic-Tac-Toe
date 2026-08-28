import streamlit as st

st.set_page_config(page_title="會消失的井字棋", page_icon="❌", layout="centered")

# 安全版 CSS：確保手機版保持橫向，且調大按鈕字體
st.markdown("""
    <style>
    [data-testid="stHorizontalBlock"] {
        flex-direction: row !important;
    }
    div.stButton > button {
        height: 70px !important;
        font-size: 22px !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. 初始化狀態
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.o_queue = []
    st.session_state.x_queue = []
    st.session_state.turn = "O"
    st.session_state.winner = None

# 2. 獲勝判定
def check_win(board, player):
    win_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
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

# 6. 棋盤繪製
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
