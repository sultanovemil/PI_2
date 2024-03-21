from youtube_transcript_api import YouTubeTranscriptApi as yt
from deeppavlov import build_model
import streamlit as st
import re

if "model" not in st.session_state:
    st.session_state.model = build_model('squad_ru_bert', download=True, install=True)


# Check if ru
def check_ru(video_id):
    transcript_list = yt.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['ru'])
    if transcript.language_code == "ru":
        return 1
    else:
        return 0


# Get subtitles
@st.cache_data
def get_sub(video_id, lg_code="ru"):
    full_text = ""
    try:
        transcript = yt.get_transcript(video_id, languages=[lg_code])
        for line in transcript:
            text = line['text'] + " "
            full_text += text
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return 0
    return full_text


# Get answers
def get_answers(model, context, question):
    try:
        answer = model([context], [question])
    except Exception as e:
        print(f'Произошла ошибка: {e}')
        return "Не знаю!"
    if answer[0][0] == "":
        return "Не знаю!"
    return answer[0][0]


# Web interface
st.title("ChatBot")

if "check_lan_ok" not in st.session_state:
    st.session_state.check_lan_ok = False
if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

# Get YouTube video ID
pattern = r"(?<=v=)[\w-]+(?=&|\b)"
url = st.text_input('URL YouTube')
match = re.search(pattern, url)
if match:
    vidID = match.group()
    st.success('URL is OK', icon="✅")
    if st.button(label="Check language"):
        st.session_state.check_lan_ok = True
else:
    st.warning('Enter correct URL', icon="⚠️")

if st.session_state.check_lan_ok:
    if check_ru(vidID):
        st.success('The video has russian subtitles', icon="✅")       
        st.session_state.start_chat = True
    else:
        st.warning('There is no russian subtitles', icon="⚠️")    
        chat_container = st.empty()

if st.session_state.start_chat:
    with st.spinner('Getting content...'):
        context = get_sub(vidID)       
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if question := st.chat_input("Enter your question"):
        
        # Display user message in chat message container
        st.chat_message("user").markdown(question)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        with st.spinner('I am thinking ...'):
            answer = get_answers(st.session_state.model, context, question)        
        
        # Display assistant response in chat message container
        response = f"Echo: {answer}"
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
