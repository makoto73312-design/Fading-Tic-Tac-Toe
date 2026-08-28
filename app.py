import streamlit as st

st.set_page_config(page_title="會消失的井字棋", page_icon="❌", layout="centered")

# 初始化遊戲狀態
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.o_queue = []  # 記錄 O 的下棋位置順序
    st.session_state.x_queue = []  # 記錄 X 的下棋位置順序
    st.session_state.turn = "O"
    st.session_state.winner = None

def check_win(board, player):
    win_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # 橫線
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # 直線
        [0, 4, 8], [2, 4, 6]             # 對角線
    ]
    return any(all(board[i] == player for i in line) for line in win_lines)

def handle_click(index):
    # 若已被佔用或已有贏家則不動作
    if st.session_state.board[index] != "" or st.session_state.winner:
        return

    current = st.session_state.turn
    queue = st.session_state.o_queue if current == "O" else st.session_state.x_queue

    # 1. 放置新棋子
    queue.append(index)
    st.session_state.board[index] = current

    # 2. 超過 3 顆時，移除最舊的一顆（FIFO）
    if len(queue) > 3:
        oldest_index = queue.pop(0)
        st.session_state.board[oldest_index] = ""

    # 3. 判定勝負或換人
    if check_win(st.session_state.board, current):
        st.session_state.winner = current
    else:
        st.session_state.turn = "X" if current == "O" else "O"

def reset_game():
    st.session_state.board = [""] * 9
    st.session_state.o_queue = []
    st.session_state.x_queue = []
    st.session_state.turn = "O"
    st.session_state.winner = None

# UI 視覺渲染
st.title("👻 會消失的井字棋")
st.caption("每人最多保留 3 顆棋子，下第 4 顆時最早下的棋子會自動消失！")

if st.session_state.winner:
    st.balloons()
    st.success(f"🎉 玩家 **{st.session_state.winner}** 獲勝！")
else:
    st.info(f"當前輪到玩家：**{st.session_state.turn}**")

# 繪製 3x3 九宮格按鈕
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        val = st.session_state.board[idx]
        
        # 提示即將消失的棋子 (當佇列滿 3 顆且為最早的那顆)
        display_label = val
        if val == "O" and len(st.session_state.o_queue) == 3 and st.session_state.o_queue[0] == idx:
            display_label = "O (⚠️)"
        elif val == "X" and len(st.session_state.x_queue) == 3 and st.session_state.x_queue[0] == idx:
            display_label = "X (⚠️)"
        elif val == "":
            display_label = " "

        cols[col].button(
            display_label, 
            key=f"btn_{idx}", 
            on_click=handle_click, 
            args=(idx,), 
            use_container_width=True
        )

st.button("🔄 重新開始遊戲", on_click=reset_game)
