import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PIL.Image
from langdetect import detect

st.set_page_config(page_title="Gen-e",page_icon="🤖")
hide_st_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Load environment variables from the .env file
load_dotenv()
# Access the environment variable
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')
model_vision = genai.GenerativeModel('gemini-pro-vision')

if "chat_model" not in st.session_state:
    chat = model.start_chat(history=[])
    st.session_state.chat_model = chat

if "chat_model_vision" not in st.session_state:
    chat = genai.GenerativeModel('gemini-pro-vision')
    st.session_state.chat_model_vision = chat

from googletrans import Translator

def language_translation(input_string,source_lan,target_lag):
    language = {'afrikaans': 'af', 'albanian': 'sq', 'amharic': 'am', 'arabic': 'ar', 'armenian': 'hy', 'azerbaijani': 'az', 'basque': 'eu', 'belarusian': 'be', 'bengali': 'bn', 'bosnian': 'bs', 'bulgarian': 'bg', 'catalan': 'ca', 'cebuano': 'ceb', 'chichewa': 'ny', 'chinese (simplified)': 'zh-cn', 'chinese (traditional)': 'zh-tw', 'corsican': 'co', 'croatian': 'hr', 'czech': 'cs', 'danish': 'da', 'dutch': 'nl', 'english': 'en', 'esperanto': 'eo', 'estonian': 'et', 'filipino': 'tl', 'finnish': 'fi', 'french': 'fr', 'frisian': 'fy', 'galician': 'gl', 'georgian': 'ka', 'german': 'de', 'greek': 'el', 'gujarati': 'gu', 'haitian creole': 'ht', 'hausa': 'ha', 'hawaiian': 'haw', 'hebrew': 'he', 'hindi': 'hi', 'hmong': 'hmn', 'hungarian': 'hu', 'icelandic': 'is', 'igbo': 'ig', 'indonesian': 'id', 'irish': 'ga', 'italian': 'it', 'japanese': 'ja', 'javanese': 'jw', 'kannada': 'kn', 'kazakh': 'kk', 'khmer': 'km', 'korean': 'ko', 'kurdish (kurmanji)': 'ku', 'kyrgyz': 'ky', 'lao': 'lo', 'latin': 'la', 'latvian': 'lv', 'lithuanian': 'lt', 'luxembourgish': 'lb', 'macedonian': 'mk', 'malagasy': 'mg', 'malay': 'ms', 'malayalam': 'ml', 'maltese': 'mt', 'maori': 'mi', 'marathi': 'mr', 'mongolian': 'mn', 'myanmar (burmese)': 'my', 'nepali': 'ne', 'norwegian': 'no', 'odia': 'or', 'pashto': 'ps', 'persian': 'fa', 'polish': 'pl', 'portuguese': 'pt', 'punjabi': 'pa', 'romanian': 'ro', 'russian': 'ru', 'samoan': 'sm', 'scots gaelic': 'gd', 'serbian': 'sr', 'sesotho': 'st', 'shona': 'sn', 'sindhi': 'sd', 'sinhala': 'si', 'slovak': 'sk', 'slovenian': 'sl', 'somali': 'so', 'spanish': 'es', 'sundanese': 'su', 'swahili': 'sw', 'swedish': 'sv', 'tajik': 'tg', 'tamil': 'ta', 'telugu': 'te', 'thai': 'th', 'turkish': 'tr', 'ukrainian': 'uk', 'urdu': 'ur', 'uyghur': 'ug', 'uzbek': 'uz', 'vietnamese': 'vi', 'welsh': 'cy', 'xhosa': 'xh', 'yiddish': 'yi', 'yoruba': 'yo', 'zulu': 'zu'}
    googletrans_translator = Translator()
    googletrans_result = googletrans_translator.translate(input_string,src= "auto", dest= target_lag)
    return googletrans_result.text


# import speech_recognition as sr

# def speech_to_text():
#     # Initialize the recognizer
#     recognizer = sr.Recognizer()
    
#     # Use the default microphone as the audio source
#     with sr.Microphone() as source:
#         print("Say something:")
#         audio = recognizer.listen(source, timeout=5)

#     try:
#         # Use Google Web Speech API to convert speech to text
#         text = recognizer.recognize_google(audio)
#         print("You said:", text)
#         return text

#     except sr.UnknownValueError:
#         print("Sorry, could not understand audio.")
#         return None

#     except sr.RequestError as e:
#         print(f"Error connecting to Google Web Speech API: {e}")
#         return None


st.title("My Buddy")

if "instruction" not in st.session_state:
    genai_prompt = st.text_area("Drop Yourself :")
    instruction_button = st.button("Submit")
    if instruction_button:
        st.session_state.instruction = genai_prompt

with st.sidebar:
    img_upload = st.file_uploader(label='Upload image')
    # speech_button = st.button('Speech')


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "messages_vision" not in st.session_state:
    st.session_state.messages_vision = []
    

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

for message in st.session_state.messages_vision:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# if speech_button:
#     prompt = speech_to_text()



if prompt := st.chat_input("What is up?"):
    
    # if prompt == True:
    #     from gtts import gTTS
    #     tts = gTTS('Say Something')
        
    #     try:os.remove('Say_Something.mp3') 
    #     except:pass
        
    #     tts.save('Say_Something.mp3')
        
    #     from playsound import playsound
    #     playsound('Say_Something.mp3')
        
    #     prompt = speech_to_text()
    # else:
    #     prompt = prompt
    
    if img_upload == None :
        
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        safety_ratings = {
        'HARM_CATEGORY_SEXUALLY_EXPLICIT':'block_none',
        'HARM_CATEGORY_HATE_SPEECH': 'block_none',
        'HARM_CATEGORY_HARASSMENT': 'block_none',
        'HARM_CATEGORY_DANGEROUS_CONTENT' : 'block_none'
        }
        
        chat = st.session_state.chat_model
        
        with st.spinner('Wait for it...........'):    

            response = chat.send_message(st.session_state.instruction + '\n' + " now my Question is " + prompt ,stream=True,safety_settings=safety_ratings)
        
            store_data = ""
            try:
                with st.chat_message("assistant"):
                    for chunk in response:
                        result = chunk.text
                        store_data += result 
                        response = result
                        # Display assistant response in chat message container
                        st.markdown(response)
            except:
                with st.chat_message("assistant"):
                    last_send, last_received = chat.rewind()
                    des_lang = detect(prompt)
                    prompt =  language_translation(prompt,'source_lan','english')
                    response = chat.send_message(st.session_state.instruction + '\n' + " now my Question is " + prompt ,stream=True,safety_settings=safety_ratings)
                    
                    for chunk in response:
                        result = chunk.text
                        result = language_translation(result,'english',des_lang)
                        store_data += result 
                        response = result
                        # Display assistant response in chat message container
                        st.markdown(response)
                    
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": store_data})
    
    else:
        
        st.chat_message("user").markdown(prompt)
        st.session_state.messages_vision.append({"role": "user", "content": prompt})
        
        img = PIL.Image.open(img_upload)
        chat = st.session_state.chat_model_vision
     
        st.image(img)
        with st.spinner('Wait for it...'):    

            # if len(chat.history) < 2:
            #     st.balloons()
            #     response = chat.send_message([prompt, img],stream=True)
            # else:
            #     response = chat.send_message([prompt, img],stream=True)

            response = model_vision.generate_content([prompt, img], stream=True)
            
            response.resolve()
            
            store_data = ""
            try:
                with st.chat_message("assistant"):
                    for chunk in response:
                        result = chunk.text
                        store_data += result 
                        response = result
                        # Display assistant response in chat message container
                        st.markdown(response)
            except:
                with st.chat_message("assistant"):
                    last_send, last_received = chat.rewind()    
                    st.markdown("Do not use Tanglish words")
                    
            # Add assistant response to chat history
            st.session_state.messages_vision.append({"role": "assistant", "content": store_data})
    
        
