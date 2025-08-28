import streamlit as st
import time
import random
import matplotlib.pyplot as plt

# ----- CONFIG -----
WIDTH, HEIGHT = 400, 600
GROUND_H = 80
PIPE_WIDTH = 70
PIPE_GAP = 200
BIRD_RADIUS = 15

GRAVITY = 2
JUMP_STRENGTH = -30
PIPE_SPEED = 5

# ----- INIT -----
if "bird_y" not in st.session_state:
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.velocity = 0
    st.session_state.pipes = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.last_update = time.time()


def reset_game():
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.velocity = 0
    st.session_state.pipes = [[WIDTH, random.randint(100, HEIGHT - PIPE_GAP - GROUND_H)]]
    st.session_state.score = 0
    st.session_state.game_over = False


def update_game():
    if st.session_state.game_over:
        return

    # Apply gravity
    st.session_state.velocity += GRAVITY
    st.session_state.bird_y += st.session_state.velocity

    # Move pipes
    for pipe in st.session_state.pipes:
        pipe[0] -= PIPE_SPEED

    # Remove offscreen pipes and add new ones
    if st.session_state.pipes and st.session_state.pipes[0][0] < -PIPE_WIDTH:
        st.session_state.pipes.pop(0)
        st.session_state.pipes.append([WIDTH, random.randint(100, HEIGHT - PIPE_GAP - GROUND_H)])
        st.session_state.score += 1

    # Collision detection
    bird_top = st.session_state.bird_y - BIRD_RADIUS
    bird_bottom = st.session_state.bird_y + BIRD_RADIUS
    if bird_bottom >= HEIGHT - GROUND_H:
        st.session_state.game_over = True

    for pipe_x, pipe_h in st.session_state.pipes:
        if pipe_x < 80 < pipe_x + PIPE_WIDTH:
            if bird_top < pipe_h or bird_bottom > pipe_h + PIPE_GAP:
                st.session_state.game_over = True


def draw_game():
    fig, ax = plt.subplots(figsize=(4, 6))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, HEIGHT)
    ax.axis("off")

    # Sky
    ax.set_facecolor("#87CEEB")

    # Pipes
    for pipe_x, pipe_h in st.session_state.pipes:
        ax.add_patch(plt.Rectangle((pipe_x, 0), PIPE_WIDTH, pipe_h, color="green"))
        ax.add_patch(plt.Rectangle((pipe_x, pipe_h + PIPE_GAP), PIPE_WIDTH, HEIGHT, color="green"))

    # Ground
    ax.add_patch(plt.Rectangle((0, 0), WIDTH, GROUND_H, color="#8B4513"))

    # Bird
    ax.add_patch(plt.Circle((80, st.session_state.bird_y), BIRD_RADIUS, color="yellow"))
    ax.add_patch(plt.Polygon([[95, st.session_state.bird_y],
                              [105, st.session_state.bird_y + 5],
                              [105, st.session_state.bird_y - 5]], color="orange"))

    st.pyplot(fig)


# ----- UI -----
st.title("🐦 Flappy Bird - Streamlit Edition")

col1, col2, col3 = st.columns(3)
if col1.button("⬆️ Flap"):
    st.session_state.velocity = JUMP_STRENGTH
if col2.button("🔄 Restart"):
    reset_game()
if col3.button("⏭️ Next Frame"):
    update_game()

# Auto update loop
if not st.session_state.game_over:
    update_game()
    time.sleep(0.05)
    st.experimental_rerun()

# Draw
draw_game()
st.subheader(f"Score: {st.session_state.score}")

if st.session_state.game_over:
    st.error("💀 Game Over! Press Restart to try again.")
