import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Gen-e",page_icon="🤖")
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

area_list = areas_of_interest = [
    "Artificial Intelligence (AI)",
    "Machine Learning (ML)",
    "Deep Learning",
    "Natural Language Processing (NLP)",
    "Computer Vision",
    "Data Science",
    "Web Development",
    "Mobile App Development",
    "Software Engineering",
    "Cloud Computing",
    "Cybersecurity",
    "Blockchain",
    "Internet of Things (IoT)",
    "Augmented Reality (AR)",
    "Virtual Reality (VR)",
    "Game Development",
    "UI/UX Design",
    "Data Analytics",
    "Robotics",
    "Biotechnology",
    "Space Exploration",
    "Renewable Energy",
    "Sports",
    "Music",
    "Art and Design",
    "Finance and Economics",
    "Healthcare",
    "Education",
    "Environmental Science",
    "Philosophy",
    "History",
    "Travel",
    "Cuisine",
    "Fitness and Wellness",
    "Photography",
    "Film and Cinema",
    "Literature",
    "Philanthropy",
    "Social Impact",
    "Fashion",
    "Gaming",
    "Astrophysics",
    "Psychology",
    "Political Science",
    "Languages and Linguistics",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Geology",
    "Astronomy",
    "Medicine",
    "Automotive Technology",
    "Electrical Engineering",
    "Civil Engineering",
    "Mechanical Engineering",
    "Aerospace Engineering",
    "Telecommunications",
    "Cryptocurrencies",
    "Digital Marketing",
    "E-commerce",
    "Human-Computer Interaction",
    "Ethical Hacking",
    "Quantum Computing"
]

area_of_interest = st.multiselect("Enter your area of interest :",area_list)

submit_button = st.button('Submit')

# Load environment variables from the .env file
load_dotenv()
# Access the environment variable
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')

prompt = f"""
Based on user area of interest Do fetch the most related recent blogs, hackathons, conferences, and updates and youtube video and news in these areas. Provide links along with a brief description for each recommendation

MY AREA OF INTEREST ARE :
{" * ".join(area_list)}
"""

if submit_button:
    with st.spinner('In progress...'):
        response = model.generate_content(prompt)
        st.write(response.text)
        
    
