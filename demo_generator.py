import streamlit as st
import time
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Death to the Form - AI Chat Demo",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for WhatsApp-like styling
st.markdown("""
    <style>
        /* Main container */
        .main {
            background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%);
        }

        /* Chat container */
        .chat-container {
            background: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            height: 600px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        /* Message bubbles */
        .message {
            display: flex;
            margin-bottom: 8px;
            animation: slideIn 0.3s ease-out;
        }

        .message.ai {
            justify-content: flex-start;
        }

        .message.worker {
            justify-content: flex-end;
        }

        .bubble {
            max-width: 70%;
            padding: 10px 14px;
            border-radius: 12px;
            font-size: 14px;
            line-height: 1.4;
            word-wrap: break-word;
        }

        .bubble.ai {
            background: #e8e8e8;
            color: #000;
            border-bottom-left-radius: 4px;
        }

        .bubble.worker {
            background: #007AFF;
            color: #fff;
            border-bottom-right-radius: 4px;
        }

        .timestamp {
            font-size: 12px;
            color: #999;
            text-align: center;
            margin: 8px 0;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Scene title */
        .scene-title {
            text-align: center;
            color: #007AFF;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        /* Controls */
        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "current_scene" not in st.session_state:
    st.session_state.current_scene = 1
if "messages" not in st.session_state:
    st.session_state.messages = []
if "animating" not in st.session_state:
    st.session_state.animating = False

# Define scenes with conversations
SCENES = {
    1: {
        "title": "Scene 1: The Hook (0-15s)",
        "description": "Proactive AI outreach vs. worker engagement",
        "messages": [
            ("ai", "Hey, saw you clocked out at 9:15pm today. That's rough—you doing okay at the site?"),
        ]
    },
    2: {
        "title": "Scene 2: The Retention Check-in (15-25s)",
        "description": "Real conversation vs. generic satisfaction survey",
        "messages": [
            ("ai", "Hey, saw you clocked out at 9:15pm today. That's rough—you doing okay at the site?"),
            ("worker", "Honestly, my feet are killing me."),
            ("ai", "Got it. Anything else I should know?"),
            ("worker", "Yeah, no break today."),
        ]
    },
    3: {
        "title": "Scene 3: The Resolution (25-35s)",
        "description": "Action-driven AI vs. dead-end form response",
        "messages": [
            ("ai", "Hey, saw you clocked out at 9:15pm today. That's rough—you doing okay at the site?"),
            ("worker", "Honestly, my feet are killing me."),
            ("ai", "Got it. Anything else I should know?"),
            ("worker", "Yeah, no break today."),
            ("ai", "I've flagged this with your manager. Help's on the way."),
        ]
    }
}

# Sidebar navigation
st.sidebar.title("Demo Scenes")
st.sidebar.markdown("---")
for scene_num in [1, 2, 3]:
    if st.sidebar.button(f"Scene {scene_num}", key=f"scene_{scene_num}"):
        st.session_state.current_scene = scene_num
        st.session_state.messages = []
        st.rerun()

# Main content
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 💬 Death to the Form")
    st.markdown("**AI Agent Demo for Staffing Agencies**")
    st.markdown("---")

# Get current scene
scene = SCENES[st.session_state.current_scene]

# Display scene title and description
st.markdown(f"<div class='scene-title'>{scene['title']}</div>", unsafe_allow_html=True)
st.markdown(f"*{scene['description']}*", unsafe_allow_html=True)
st.markdown("---")

# Chat container
with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    # Initialize chat with auto-play
    if len(st.session_state.messages) < len(scene["messages"]):
        # Auto-play messages with delay
        for i in range(len(st.session_state.messages), len(scene["messages"])):
            time.sleep(0.8)  # Delay between messages for screen recording
            st.session_state.messages.append(scene["messages"][i])
            st.rerun()

    # Display all messages
    for sender, text in st.session_state.messages:
        message_class = "ai" if sender == "ai" else "worker"
        sender_label = "AI Agent" if sender == "ai" else "Worker"

        st.markdown(f"""
            <div class="message {message_class}">
                <div class="bubble {message_class}">
                    {text}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Controls
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("← Prev Scene", disabled=(st.session_state.current_scene == 1)):
        st.session_state.current_scene -= 1
        st.session_state.messages = []
        st.rerun()

with col2:
    if st.button("🔄 Reset", key="reset_btn"):
        st.session_state.messages = []
        st.rerun()

with col3:
    if st.button("Next Scene →", disabled=(st.session_state.current_scene == 3)):
        st.session_state.current_scene += 1
        st.session_state.messages = []
        st.rerun()

# Footer info
st.markdown("---")
st.markdown("""
**Recording Tips:**
- Use the "Reset" button to start fresh before recording
- Auto-play shows messages with 0.8s delay for smooth screen recording
- Works best in a fixed window size for consistent video editing
""")
