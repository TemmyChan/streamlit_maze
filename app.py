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
player_pos = st.session_state.get("player_pos", start_pos)

# キーボード入力
keys = st.session_state.get("keys", {})

def update_position():
    global player_pos
    x, y = player_pos
    if keys.get("left", False) and (x-1, y) in maze.nodes and ((x, y), (x-1, y)) in maze.edges:
        player_pos = (x-1, y)
    if keys.get("right", False) and (x+1, y) in maze.nodes and ((x, y), (x+1, y)) in maze.edges:
        player_pos = (x+1, y)
    if keys.get("up", False) and (x, y-1) in maze.nodes and ((x, y), (x, y-1)) in maze.edges:
        player_pos = (x, y-1)
    if keys.get("down", False) and (x, y+1) in maze.nodes and ((x, y), (x, y+1)) in maze.edges:
        player_pos = (x, y+1)
    
    st.session_state["player_pos"] = player_pos

# キーボード入力のキャプチャ
st.text("矢印キーで移動")

keys["left"] = st.button("←")
keys["right"] = st.button("→")
keys["up"] = st.button("↑")
keys["down"] = st.button("↓")

st.session_state["keys"] = keys

update_position()

# 迷路を描画して表示
maze_image = draw_maze(maze, SIZE, player_pos, goal_pos)
st.image(maze_image)

# ゴール判定
if player_pos == goal_pos:
    st.success("ゴール！おめでとう！")
