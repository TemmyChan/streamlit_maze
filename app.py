import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

# 迷路の生成
def generate_maze(size=10):
    G = nx.grid_2d_graph(size, size)  # グリッドグラフを作成
    maze = nx.minimum_spanning_tree(G)  # 最小全域木で迷路を生成
    return maze

# 迷路を画像として描画
def draw_maze(maze, size, player_pos, goal_pos):
    cell_size = 40
    img_size = size * cell_size
    img = Image.new("RGB", (img_size, img_size), "white")
    draw = ImageDraw.Draw(img)

    # グリッドを描画
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

# プレイヤーの初期位置をセッションに保存
if "player_pos" not in st.session_state:
    st.session_state["player_pos"] = start_pos

# キーボード入力を受け取る
key = st.text_input("矢印キーを入力（←, →, ↑, ↓）して Enter を押してください:")

# プレイヤーの位置を更新
def update_position():
    x, y = st.session_state["player_pos"]
    if key == "←" and (x-1, y) in maze.nodes and ((x, y), (x-1, y)) in maze.edges:
        st.session_state["player_pos"] = (x-1, y)
    if key == "→" and (x+1, y) in maze.nodes and ((x, y), (x+1, y)) in maze.edges:
        st.session_state["player_pos"] = (x+1, y)
    if key == "↑" and (x, y-1) in maze.nodes and ((x, y), (x, y-1)) in maze.edges:
        st.session_state["player_pos"] = (x, y-1)
    if key == "↓" and (x, y+1) in maze.nodes and ((x, y), (x, y+1)) in maze.edges:
        st.session_state["player_pos"] = (x, y+1)

update_position()

# 迷路を描画して表示
maze_image = draw_maze(maze, SIZE, st.session_state["player_pos"], goal_pos)
st.image(maze_image)

# ゴール判定
if st.session_state["player_pos"] == goal_pos:
    st.success("ゴール！おめでとう！")
