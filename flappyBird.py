import streamlit as st
import random
import plotly.graph_objects as go

# Game constants
WIDTH, HEIGHT = 400, 600
PIPE_WIDTH = 70
PIPE_GAP = 180
GROUND_H = 80
BIRD_X = 80
BIRD_SIZE = 20

GRAVITY = 3
JUMP = -40
SPEED = 5

# Initialize session state
if "bird_y" not in st.session_state:
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.velocity = 0
    st.session_state.pipes = [[WIDTH, random.randint(100, HEIGHT - PIPE_GAP - GROUND_H)]]
    st.session_state.score = 0
    st.session_state.game_over = False

# Reset function
def reset():
    st.session_state.bird_y = HEIGHT // 2
    st.session_state.velocity = 0
    st.session_state.pipes = [[WIDTH, random.randint(100, HEIGHT - PIPE_GAP - GROUND_H)]]
    st.session_state.score = 0
    st.session_state.game_over = False

# Game update
def update():
    if st.session_state.game_over:
        return

    # Bird physics
    st.session_state.velocity += GRAVITY
    st.session_state.bird_y += st.session_state.velocity

    # Pipe movement
    for pipe in st.session_state.pipes:
        pipe[0] -= SPEED

    # Add new pipe
    if st.session_state.pipes[-1][0] < WIDTH - 200:
        st.session_state.pipes.append([WIDTH, random.randint(100, HEIGHT - PIPE_GAP - GROUND_H)])

    # Remove offscreen pipes
    if st.session_state.pipes[0][0] < -PIPE_WIDTH:
        st.session_state.pipes.pop(0)
        st.session_state.score += 1

    # Collision detection
    bird_top = st.session_state.bird_y - BIRD_SIZE//2
    bird_bottom = st.session_state.bird_y + BIRD_SIZE//2
    if bird_bottom >= HEIGHT - GROUND_H or bird_top <= 0:
        st.session_state.game_over = True

    for pipe_x, pipe_h in st.session_state.pipes:
        if BIRD_X + BIRD_SIZE//2 > pipe_x and BIRD_X - BIRD_SIZE//2 < pipe_x + PIPE_WIDTH:
            if bird_top < pipe_h or bird_bottom > pipe_h + PIPE_GAP:
                st.session_state.game_over = True

# Draw game
def draw():
    fig = go.Figure()

    # Background
    fig.add_shape(type="rect", x0=0, y0=0, x1=WIDTH, y1=HEIGHT,
                  fillcolor="skyblue", line=dict(width=0))

    # Ground
    fig.add_shape(type="rect", x0=0, y0=0, x1=WIDTH, y1=GROUND_H,
                  fillcolor="saddlebrown", line=dict(width=0))

    # Pipes
    for pipe_x, pipe_h in st.session_state.pipes:
        fig.add_shape(type="rect", x0=pipe_x, y0=0, x1=pipe_x+PIPE_WIDTH, y1=pipe_h,
                      fillcolor="green", line=dict(width=0))
        fig.add_shape(type="rect", x0=pipe_x, y0=pipe_h+PIPE_GAP, x1=pipe_x+PIPE_WIDTH, y1=HEIGHT,
                      fillcolor="green", line=dict(width=0))

    # Bird
    fig.add_shape(type="circle", x0=BIRD_X-BIRD_SIZE//2, y0=st.session_state.bird_y-BIRD_SIZE//2,
                  x1=BIRD_X+BIRD_SIZE//2, y1=st.session_state.bird_y+BIRD_SIZE//2,
                  fillcolor="yellow", line=dict(width=2, color="orange"))

    # Layout
    fig.update_xaxes(visible=False, range=[0, WIDTH])
    fig.update_yaxes(visible=False, range=[0, HEIGHT])
    fig.update_layout(width=WIDTH, height=HEIGHT, margin=dict(l=0, r=0, t=0, b=0))
    return fig

# --- UI ---
st.title("🐦 Flappy Bird - Streamlit Edition")

col1, col2 = st.columns([1,1])
if col1.button("⬆️ Flap"):
    st.session_state.velocity = JUMP
if col2.button("🔄 Restart"):
    reset()

update()
st.plotly_chart(draw(), use_container_width=True)

st.subheader(f"Score: {st.session_state.score}")

if st.session_state.game_over:
    st.error("💀 Game Over! Press Restart to try again.")
else:
    # Auto refresh every 100ms
    st.experimental_rerun()
