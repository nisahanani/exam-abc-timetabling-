import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Exam Timetabling using ABC",
    layout="wide"
)

st.title("🐝 Exam Timetabling Optimization using Artificial Bee Colony (ABC)")
st.markdown("""
This system applies the Artificial Bee Colony (ABC) algorithm to optimize
exam timetabling by minimizing conflicts and improving room utilization.
""")

# =========================
# Load datasets
# =========================
@st.cache_data
def load_data():
    classrooms = pd.read_csv("data/classrooms.csv")
    timeslots = pd.read_csv("data/exam_timeslot.csv")
    return classrooms, timeslots

classrooms, timeslots = load_data()

# =========================
# Sidebar - Parameters
# =========================
st.sidebar.header("⚙️ ABC Parameters")

num_bees = st.sidebar.slider("Number of Bees", 10, 100, 30)
limit = st.sidebar.slider("Abandonment Limit", 5, 50, 20)
max_iter = st.sidebar.slider("Maximum Iterations", 50, 500, 200)

st.sidebar.markdown("---")
run_button = st.sidebar.button("🚀 Run ABC Optimization")

# =========================
# Dataset Preview
# =========================
st.subheader("📊 Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Classrooms Dataset**")
    st.dataframe(classrooms)

with col2:
    st.markdown("**Exam Timeslot Dataset**")
    st.dataframe(timeslots)

# =========================
# Placeholder for Results
# =========================
st.subheader("📈 Optimization Results")

if run_button:
    st.info("ABC algorithm will be executed here (logic will be integrated next).")

    # Dummy convergence curve (placeholder)
    fitness_history = [100 - i*0.3 for i in range(max_iter)]

    fig, ax = plt.subplots()
    ax.plot(fitness_history)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Fitness Value")
    ax.set_title("ABC Convergence Curve")

    st.pyplot(fig)

    st.success("Optimization completed successfully!")

else:
    st.warning("Click **Run ABC Optimization** to start.")

