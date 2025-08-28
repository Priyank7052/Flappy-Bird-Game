import streamlit as st
import random
import time

# Game constants
HEIGHT = 20
WIDTH = 20
PIPE_GAP = 6
BIRD_X = 3

if "bird_y" not in st.session_state:
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.pipes = [(WIDTH, random.randint(4, HEIGHT - PIPE_GAP - 4))]
    st.session_state.score = 0
    st.session_state.game_over = False

def reset():
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.pipes = [(WIDTH, random.randint(4, HEIGHT - PIPE_GAP - 4))]
    st.session_state.score = 0
    st.session_state.game_over = False

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
            new_pipes.append((WIDTH, random.randint(4, HEIGHT - PIPE_GAP - 4)))
    st.session_state.pipes = new_pipes

    # Collision check
    for x, h in st.session_state.pipes:
        if x == BIRD_X:
            if not (h < st.session_state.bird_y < h + PIPE_GAP):
                st.session_state.game_over = True

def draw():
    grid = []
    for y in range(HEIGHT):
        row = ""
        for x in range(WIDTH):
            if x == BIRD_X and y == st.session_state.bird_y:
                row += "🐤"
            elif any(px == x and (y < ph or y > ph + PIPE_GAP) for px, ph in st.session_state.pipes):
                row += "🟩"
            else:
                row += "⬜"
        grid.append(row)
    return "\n".join(grid)

st.title("🐦 Flappy Bird - Simple Streamlit Edition")

col1, col2 = st.columns(2)
if col1.button("⬆️ Flap"):
    st.session_state.bird_y = max(0, st.session_state.bird_y - 2)
if col2.button("🔄 Restart"):
    reset()

update()
st.text(draw())
st.write(f"Score: {st.session_state.score}")

if st.session_state.game_over:
    st.error("💀 Game Over! Press Restart.")
else:
    time.sleep(0.2)
    st.experimental_rerun()
