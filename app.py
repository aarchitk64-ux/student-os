import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Aarchit OS",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# LOAD ENV
# -----------------------------
load_dotenv()

# -----------------------------
# AI CLIENT
# -----------------------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# -----------------------------
# FILE SETUP
# -----------------------------
GOALS_FILE = "data/goals.txt"

if not os.path.exists(GOALS_FILE):
    with open(GOALS_FILE, "w", encoding="utf-8"):
        pass

# -----------------------------
# LOAD GOALS
# -----------------------------
with open(GOALS_FILE, "r", encoding="utf-8") as f:
    goals = [line.strip() for line in f.readlines() if line.strip()]

# -----------------------------
# TITLE
# -----------------------------
st.title("🎓 Aarchit OS")

# -----------------------------
# DASHBOARD
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Goals", len(goals))

with col2:
    st.metric("Projects", 0)

with col3:
    st.metric("Study Hours", 0)

# -----------------------------
# GOAL TRACKER
# -----------------------------
st.divider()

st.header("🎯 Goal Tracker")

new_goal = st.text_input("Add a Goal")

if st.button("Add Goal"):

    if new_goal.strip():

        with open(
            GOALS_FILE,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(new_goal + "\n")

        st.success("Goal Saved!")
        st.rerun()

# -----------------------------
# DISPLAY GOALS
# -----------------------------
st.subheader("My Goals")

if goals:

    for goal in goals:
        st.write(f"✅ {goal}")

else:
    st.info("No goals added yet.")

# -----------------------------
# ROADMAP GENERATOR
# -----------------------------
st.divider()

st.header("📚 AI Roadmap Generator")

name = st.text_input("Name")

education = st.selectbox(
    "Education Level",
    [
        "School",
        "Class 12",
        "College",
        "Graduate"
    ]
)

interests = st.text_area(
    "Interests",
    placeholder="AI, Python, Startups, Web Development..."
)

if st.button("Generate Roadmap"):

    if not name.strip():
        st.warning("Please enter your name.")
        st.stop()

    if not interests.strip():
        st.warning("Please enter your interests.")
        st.stop()

    prompt = f"""
Student Name: {name}
Education Level: {education}
Interests: {interests}

Generate:

1. Personalized 6-month roadmap
2. Skills to learn
3. Five practical project ideas

Format nicely in markdown.
"""

    with st.spinner("Generating roadmap..."):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert mentor helping students learn skills and build projects."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        roadmap = response.choices[0].message.content

    st.success("Roadmap Generated!")
    st.markdown(roadmap)

# -----------------------------
# AI MENTOR
# -----------------------------
st.divider()

st.header("🤖 AI Mentor")

question = st.text_input(
    "Ask anything about careers, coding, AI, internships..."
)

if st.button("Ask AI Mentor"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Thinking..."):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI mentor for students."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )

        answer = response.choices[0].message.content

    st.markdown(answer)