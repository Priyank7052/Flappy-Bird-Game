import streamlit as st
import random
import time

# Game constants
HEIGHT = 15   # rows
WIDTH = 20    # columns
PIPE_GAP = 5
BIRD_X = 3

# --- Initialize state ---
if "bird_y" not in st.session_state:
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.pipes = [(WIDTH, random.randint(3, HEIGHT - PIPE_GAP - 3))]
    st.session_state.score = 0
    st.session_state.game_over = False

def reset():
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.pipes = [(WIDTH, random.randint(3, HEIGHT - PIPE_GAP - 3))]
    st.session_state.score = 0
    st.session_state.game_over = False

def flap():
    st.session_state.bird_y = max(0, st.session_state.bird_y - 3)

def update():
    if st.session_state.game_over:
        return

    # Gravity
    st.session_state.bird_y += 1
    if st.session_state.bird_y >= HEIGHT:
        st.session_state.game_over = True

    # Move pipes
    new_pipes = []
    for x, h in st.session_state.pipes:
        if x > 0:
            new_pipes.append((x - 1, h))
        else:
            st.session_state.score += 1
            new_pipes.append((WIDTH, random.randint(3, HEIGHT - PIPE_GAP - 3)))
    st.session_state.pipes = new_pipes

    # Collision
    for x, h in st.session_state.pipes:
        if x == BIRD_X:
            if not (h < st.session_state.bird_y < h + PIPE_GAP):
                st.session_state.game_over = True

def draw():
    grid_html = "<div style='font-family: monospace;'>"
    for y in range(HEIGHT):
        row_html = ""
        for x in range(WIDTH):
            color = "skyblue"  # background
            if x == BIRD_X and y == st.session_state.bird_y:
                color = "yellow"  # bird
            elif any(px == x and (y < ph or y > ph + PIPE_GAP) for px, ph in st.session_state.pipes):
                color = "green"  # pipe
            row_html += f"<span style='display:inline-block;width:20px;height:20px;background:{color};border-radius:4px;'></span>"
        grid_html += row_html + "<br>"
    grid_html += "</div>"
    return grid_html

# --- UI ---
st.title("🐦 Flappy Bird - Streamlit Edition")

col1, col2 = st.columns(2)
if col1.button("⬆️ Jump"):
    flap()
if col2.button("🔄 Restart"):
    reset()

update()
st.markdown(draw(), unsafe_allow_html=True)
st.subheader(f"⭐ Score: {st.session_state.score}")

if st.session_state.game_over:
    st.error("💀 Game Over! Press Restart.")
else:
    time.sleep(0.3)
    st.experimental_rerun()
