import streamlit as st
import numpy as np
import networkx as nx
from PIL import Image, ImageDraw
from streamlit_js_eval import streamlit_js_eval

# 迷路の生成
def generate_maze(size=10):
    G = nx.grid_2d_graph(size, size)
    maze = nx.minimum_spanning_tree(G)
    return maze

# 迷路を描画
def draw_maze(maze, size, player_pos, goal_pos):
    cell_size = 40
    img_size = size * cell_size
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    # グリッド描画
    for x in range(size):
        for y in range(size):
            if (x, y) in maze.nodes:
                if (x+1, y) in maze.nodes and ((x, y), (x+1, y)) not in maze.edges:
                    draw.line([(x*cell_size, y*cell_size), ((x+1)*cell_size, y*cell_size)], fill="black", width=3)
                if (x, y+1) in maze.nodes and ((x, y), (x, y+1)) not in maze.edges:
                    draw.line([(x*cell_size, y*cell_size), (x*cell_size, (y+1)*cell_size)], fill="black", width=3)

    # プレイヤーを描画
    px, py = player_pos
    draw.ellipse([(px*cell_size+10, py*cell_size+10), ((px+1)*cell_size-10, (py+1)*cell_size-10)], fill="blue")

    # ゴールを描画
    gx, gy = goal_pos
    draw.rectangle([(gx*cell_size+10, gy*cell_size+10), ((gx+1)*cell_size-10, (gy+1)*cell_size-10)], fill="red")

    return img

# 迷路のサイズ
SIZE = 10
maze = generate_maze(SIZE)
start_pos = (0, 0)
goal_pos = (SIZE-1, SIZE-1)

# プレイヤーの位置をセッションに保存
if "player_pos" not in st.session_state:
    st.session_state["player_pos"] = start_pos

# JavaScript で矢印キーをキャプチャ
key = streamlit_js_eval(js_expressions="window.keyEvent = ''; document.addEventListener('keydown', (e) => {window.keyEvent = e.key;}); window.keyEvent;", key="key_event")

# 位置を更新する関数
def update_position(key):
    x, y = st.session_state["player_pos"]
    if key == "ArrowLeft" and (x-1, y) in maze.nodes and ((x, y), (x-1, y)) in maze.edges:
        st.session_state["player_pos"] = (x-1, y)
    if key == "ArrowRight" and (x+1, y) in maze.nodes and ((x, y), (x+1, y)) in maze.edges:
        st.session_state["player_pos"] = (x+1, y)
    if key == "ArrowUp" and (x, y-1) in maze.nodes and ((x, y), (x, y-1)) in maze.edges:
        st.session_state["player_pos"] = (x, y-1)
    if key == "ArrowDown" and (x, y+1) in maze.nodes and ((x, y), (x, y+1)) in maze.edges:
        st.session_state["player_pos"] = (x, y+1)

# キーが取得できたら移動を実行
if key:
    update_position(key)

# 迷路を描画して表示
maze_image = draw_maze(maze, SIZE, st.session_state["player_pos"], goal_pos)
st.image(maze_image)

# ゴール判定
if st.session_state["player_pos"] == goal_pos:
    st.success("ゴール！おめでとう！")
