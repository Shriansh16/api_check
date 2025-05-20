import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)



from langchain_groq import ChatGroq
api_key1=st.secrets["GROQ_API_KEY"]
#api_key1=""
# Streamlit setup  

st.image("meera11.jpg",caption="Meet Meera, your friendly cooking enthusiast!",width=300)

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Hi there! I'm Meera. I'm here as a compassionate companion who truly cares about your emotional well-being. Whether you’re feeling a little low or just want someone to talk to, I’m here to listen and support you. We can chat about mindfulness, self-care, or simply share thoughts that bring comfort and calm. Let’s take a moment for you—because your mental health matters."]
if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# Initialize the language model
llm=ChatGroq(groq_api_key=api_key1,model_name="llama-3.3-70b-versatile",temperature=0.6)

# Initialize conversation memory
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=2, return_messages=True)

# Define prompt templates
system_msg_template = SystemMessagePromptTemplate.from_template(template="""You are Meera, a warm and friendly mental health companion who genuinely cares about the emotional well-being of others. Your goal is to engage in thoughtful, empathetic conversations with elderly individuals to help manage loneliness by discussing topics related to mental health. Focus on emotional support, mindfulness, self-care routines, positive affirmations, and coping strategies. Stay positive, patient, and compassionate. Avoid discussing topics outside of mental health and emotional well-being.""")                                                                        
human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
link='meera11.jpg'
# Create conversation chain
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# Container for chat history
response_container = st.container()
# Container for text box
text_container = st.container()



with text_container:
    user_query =st.chat_input("Let’s chat! Type your message here...")

    if user_query:
        with st.spinner("typing..."):
            response = conversation.predict(input=f"Query:\n{user_query}")


        
        # Append the new query and response to the session state  
        st.session_state.requests.append(user_query)
        st.session_state.responses.append(response)
st.markdown(
    """
    <style>
    [data-testid="stChatMessageContent"] p{
        font-size: 1rem;
    }
    </style>
    """, unsafe_allow_html=True
)


# Display chat history
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            with st.chat_message('Momos', avatar=link):
                st.write(st.session_state['responses'][i])
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
