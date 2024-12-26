import streamlit as st
from openai import OpenAI
import plotly.graph_objects as go
import os

# Use the secret
XAI_API_KEY = st.secrets["XAI_API_KEY"]

# Then initialize your client or use the key as needed
client = OpenAI(
    api_key=XAI_API_KEY,
    base_url="https://api.x.ai/v1",
)

# Define questions and options
questions = [
    "1. Does procrastination come naturally to you? (e.g., putting off tasks even when they are simple)",
    "2. Do you have responsibilities that you're not doing? (e.g., work assignments or household chores)",
    "3. Do you have plans that stay on the drawing board? (e.g., unfinished personal projects)",
    "4. Do you sidestep uncomfortable priorities? (e.g., avoiding difficult conversations or tasks)",
    "5. Do you tell yourself that later is the time to begin? (e.g., saying 'I'll start tomorrow' repeatedly)",
    "6. Do you start things that you don't finish? (e.g., leaving projects half-done)",
    "7. Do you have a habit of showing up late? (e.g., being consistently late to meetings or events)",
    "8. Do you delay acting to meet a deadline? (e.g., waiting until the last minute to begin tasks)",
    "9. Do you find ways to extend deadlines? (e.g., asking for extensions unnecessarily)",
    "10. Do you come up with excuses to explain delays? (e.g., blaming circumstances instead of taking responsibility)",
]
options = ["Not at all", "Several times", "Nearly every day"]

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "responses" not in st.session_state:
    st.session_state.responses = []

# Navigation functions
def next_question(selected_option):
    st.session_state.responses.append(selected_option)
    st.session_state.question_index += 1
    st.rerun()

def restart():
    st.session_state.current_page = "Home"
    st.session_state.question_index = 0
    st.session_state.responses = []
    st.experimental_rerun()  # This will rerun the entire app

def send_to_grok(score):
    try:
        completion = client.chat.completions.create(
            model="grok-2-1212",
            messages=[
                {"role": "system", "content": "You are an AI that interprets procrastination scores. Higher scores indicate more severe procrastination. Your response should first congratulate the user for taking the test, then interpret the score, explain what procrastination is, suggest some coping mechanisms, and encourage seeking a therapist if necessary."},
                {"role": "user", "content": f"My procrastination score is {score} out of 20. Please provide an analysis."}
            ]
        )
        interpretation = completion.choices[0].message.content
        
        # Style the interpretation in a card-like structure
        styled_interpretation = f"""
        <div style="background-color: #f8f9fa; 
                    border-radius: 20px; 
                    padding: 20px; 
                    box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
                    font-family: Arial, sans-serif;
                    color: #333;
                    margin-bottom: 20px;">
            <h3 style="color: #D2691E; text-align: center;">Grok's Insight</h3>
            <p>{interpretation}</p>
        </div>
        """
        return styled_interpretation
    except Exception as e:
        return f"<div style='color: red;'>Error communicating with Grok API: {e}</div>"

# Apply custom CSS for dark orange navigation bar and button styling with mobile responsiveness
st.markdown(
    """
    <style>
    div[data-testid="stToolbar"] {
        visibility: hidden;
    }
    div.block-container {
        
        
        padding-top: 1rem; /* Remove top padding to move navbar up */
    }
    /* Full-width dark orange banner at the top */
    div[data-testid="stAppViewContainer"] > div:first-child {
        background-color: #D2691E; /* Dark Orange */
        padding: 10px 0;
    }
    /* Dark orange background for navbar buttons with black and white text */
    .stButton>button {
        background-color: #D2691E; /* Dark Orange */
        color: white; /* Default text color */
        border: none;
        padding: 10px 20px;
        margin: 0 5px;
        transition: background-color 0.3s, color 0.3s;
    }
    .stButton>button:hover {
        background-color: white; /* Changes background to white on hover */
        color: black; /* Text color changes to black on hover for contrast */
    }
    
    /* Media query for mobile devices */
    @media (max-width: 600px) {
        .stButton>button {
            display: block;
            margin: 0 auto 10px; /* Center and add some space below each button */
            width: 80%; /* Make buttons wider to fill most of the screen width */
        }
        .stButton {
            text-align: center; /* Align the container to center */
        }
    }
    
    /* Add some space below the question card */
    .stMarkdown>div {
        margin-bottom: 30px; /* Adjust this value to increase or decrease spacing */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navigation bar
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Home"):
        st.session_state.current_page = "Home"

with col2:
    if st.button("Assessment"):
        st.session_state.current_page = "Assessment"

with col3:
    if st.button("Resources/Articles"):
        st.session_state.current_page = "Resources/Articles"

# Render pages
if st.session_state.current_page == "Home":
    st.markdown(
    """
    <h1 style="text-align: center; 
               font-family: 'Arial Black', Gadget, sans-serif; 
               font-size: 2.5em; 
               color: #D2691E; /* Dark Orange text color */
               background-color: #000; /* Black background */
               padding: 10px; /* Add some padding for a better look */
               border-radius: 10px; /* Rounded edges */
               margin-bottom: 20px;">
        Welcome to Our Procrastination Analysis App
    </h1>
    """,
    unsafe_allow_html=True
)
    st.markdown(
        """
        <div style="
            background-color: #f8f9fa; 
            border-radius: 40px; 
            padding: 20px; 
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
        ">
           <h3 style="color: #333; font-family: 'Comic Sans MS', cursive; font-size: 20px; text-align: center;">Hey There, Procrastination Pal! 😄👋</h3>
<p style="font-size: 16px; line-height: 1.6; color: #555; font-family: Arial, sans-serif;">
    Welcome to the magical land where we don't judge your love for 'snooze' buttons or your art of postponing everything! This app is here to gently nudge you towards discovering your procrastination superpowers. Dive into our fun quiz, and we'll show you some tricks to turn your time-wasting into time-mastery. 
</p>
<p style="font-size: 16px; line-height: 1.6; color: #555; font-family: Arial, sans-serif;">
    <b>Disclaimer:</b> Before we get too excited, let's keep it real: this app is just for giggles and a bit of self-awareness, not for any medical or professional advice. If your procrastination has you living in a world where tomorrow never comes, maybe it's time to chat with someone who can help you with more than just a digital nudge. And hey, relax! We're not here to spy on you. We don't care to know your name, where you come from
    or even what you do for a living. Privacy assured.
</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif st.session_state.current_page == "Assessment":
    st.title("Procrastination Assessment")

    # Display progress bar
    progress_percentage = (st.session_state.question_index / len(questions)) * 100
    st.progress(progress_percentage / 100)

    if st.session_state.question_index < len(questions):
        question = questions[st.session_state.question_index]

        # Display question in a rounded card
        st.markdown(
            f"""
            <div style="
                background-color: #ffffff;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
                font-family: Arial, sans-serif;
                color: #333;
            ">
                <h4>{question}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Add space before the buttons
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

        # Display options as buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(options[0]):
                next_question(options[0])

        with col2:
            if st.button(options[1]):
                next_question(options[1])

        with col3:
            if st.button(options[2]):
                next_question(options[2])

    else:
        # Display the results
        total_score = sum([options.index(response) for response in st.session_state.responses])
        st.write(f"Your total score is: {total_score} out of {len(questions) * 2}.")

        # Gauge Chart for Scores
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=total_score,
            title={"text": "Procrastination Score"},
            gauge={
                "axis": {"range": [0, len(questions) * 2]},
                "bar": {"color": "red" if total_score > 10 else "yellow" if total_score > 5 else "green"},
                "steps": [
                    {"range": [0, 5], "color": "#8BC34A"},
                    {"range": [5, 10], "color": "#FFEB3B"},
                    {"range": [10, len(questions) * 2], "color": "black"}
                ]
            }
        ))
        st.plotly_chart(fig)

        # Send the score to Grok for interpretation
        interpretation = send_to_grok(total_score)
        st.markdown(interpretation, unsafe_allow_html=True)  # Use markdown to render HTML

        # Back to Top Button
        if st.button("Back to Top"):
            st.session_state.current_page = "Home"
            st.rerun()  # Rerun the app to reset view to the top

elif st.session_state.current_page == "Resources/Articles":
    st.title("Resources/Articles")

    st.markdown(
        """
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <p>These resources can help you manage procrastination. Please find time to read them:</p>
            <ul style="list-style-type: square; padding-left: 20px;">
                <li><a href="https://tanaamen.com/7-ways-to-beat-procrastination-and-get-stuff-done-now/" target="_blank">7 Ways to Beat Procrastination and Get Stuff Done</a></li>
                <li><a href="https://mcgraw.princeton.edu/undergraduates/resources/resource-library/understanding-and-overcoming-procrastination" target="_blank">Understanding and Overcoming Procrastination (Princeton)</a></li>
                <li><a href="https://www.nytimes.com/2019/03/25/smarter-living/why-you-procrastinate-it-has-nothing-to-do-with-self-control.html" target="_blank">Why You Procrastinate - NY Times</a></li>
                <li><a href="https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.783570/full" target="_blank">Procrastination - Insights from Psychology</a></li>
                <li><a href="https://www.researchgate.net/publication/374642425_The_Dangers_of_Procrastination_for_Learners" target="_blank">The Dangers of Procrastination for Learners</a></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
