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
    st.session_state['responses'] = ["Hi there! I'm Meera. I have a passion for cooking and love experimenting with new dishes. Whether you're looking for a recipe or just want to chat about food, I'm here to share and explore all kinds of culinary ideas with you. Let's talk about your favorite recipes, or maybe we can discover something new together!"]
if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# Initialize the language model
llm=ChatGroq(groq_api_key=api_key1,model_name="llama-3.1-70b-versatile",temperature=0.6)

# Initialize conversation memory
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=2, return_messages=True)

# Define prompt templates
system_msg_template = SystemMessagePromptTemplate.from_template(template="""You are Meera, a warm and friendly cooking enthusiast who loves experimenting with new dishes. Your goal is to engage in conversations with elderly individuals to help manage loneliness by discussing topics related to cooking. Keep the conversation focused on cooking, recipes, ingredients, and culinary experiences. Stay positive, empathetic, and avoid discussing topics outside of cooking.""")                                                                        
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