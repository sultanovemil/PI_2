from deeppavlov import build_model
import streamlit as st


# Get answers 
def get_answers(context, question):
    try:
        dp_model = build_model('squad_ru_bert', download=True, install=True)
        answer = dp_model([context], [question])
    except Exception as e:
        return "Ошибка!"
    if answer[0][0] == "":
        return "Не знаю!"
    return answer[0][0]

# Web interface
st.title("ChatBot")

context = st.text_area(label="Enter your text")

if 'chat' not in st.session_state:
    st.session_state.chat = False

def chat_button():
    st.session_state.chat = True

st.button(label="Download content", on_click=chat_button)    


if st.session_state.chat:             
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
            answer = get_answers(context, question)
        
        response = f"Echo: {answer}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})