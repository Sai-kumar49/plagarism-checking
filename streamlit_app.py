import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login
import asyncio
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
from promptTemplate import prompt4conversation, prompt4conversationInternet
from HuggingChatAPI import HuggingChat
from langchain.embeddings import HuggingFaceHubEmbeddings
from duckduckgo_search import DDGS
from itertools import islice

hf = None
repo_id = "sentence-transformers/all-mpnet-base-v2"

if 'hf_token' in st.session_state:
    if 'hf' not in st.session_state:
        hf = HuggingFaceHubEmbeddings(
            repo_id=repo_id,
            task="feature-extraction",
            huggingfacehub_api_token=st.session_state['hf_token'],
        ) # type: ignore
        st.session_state['hf'] = hf

st.set_page_config(
    page_title="Plagiarism Checker💬", page_icon="🤗", layout="wide", initial_sidebar_state="expanded"
)

st.markdown('<style>.css-w770g5{\
            width: 100%;}\
            .css-b3z5c9{    \
            width: 100%;}\
            .stButton>button{\
            width: 100%;}\
            .stDownloadButton>button{\
            width: 100%;}\
            </style>', unsafe_allow_html=True)

# Sidebar contents for logIN, choose plugin, and export chat
with st.sidebar:
    st.title('🤗💬 Plagiarism Checker')
    
    if 'hf_email' not in st.session_state or 'hf_pass' not in st.session_state:
        with st.expander("ℹ️ Login in Hugging Face", expanded=True):
            st.write("⚠️ You need to login in Hugging Face to use this app. You can register [here](https://huggingface.co/join).")
            st.header('Hugging Face Login')
            hf_email = st.text_input('Enter E-mail:')
            hf_pass = st.text_input('Enter password:', type='password')
            hf_token = st.text_input('Enter API Token:', type='password')
            if st.button('Login 🚀') and hf_email and hf_pass and hf_token: 
                with st.spinner('🚀 Logging in...'):
                    st.session_state['hf_email'] = hf_email
                    st.session_state['hf_pass'] = hf_pass
                    st.session_state['hf_token'] = hf_token

                    try:
                    
                        sign = Login(st.session_state['hf_email'], st.session_state['hf_pass'])
                        cookies = sign.login()
                        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
                    except Exception as e:
                        st.error(e)
                        st.info("⚠️ Please check your credentials and try again.")
                        st.error("⚠️ dont abuse the API")
                        st.warning("⚠️ If you don't have an account, you can register [here](https://huggingface.co/join).")
                        from time import sleep
                        sleep(3)
                        del st.session_state['hf_email']
                        del st.session_state['hf_pass']
                        del st.session_state['hf_token']
                        st.experimental_rerun()

                    st.session_state['chatbot'] = chatbot

                    id = st.session_state['chatbot'].new_conversation()
                    st.session_state['chatbot'].change_conversation(id)

                    st.session_state['conversation'] = id
                    # Generate empty lists for generated and past.
                    ## generated stores AI generated responses
                    if 'generated' not in st.session_state:
                        st.session_state['generated'] = ["I'm **Plagiarism Checker**, Enter Text below for Plagiarism Detection ... "]
                    ## past stores User's questions
                    if 'past' not in st.session_state:
                        st.session_state['past'] = ['Hi!']

                    st.session_state['LLM'] =  HuggingChat(email=st.session_state['hf_email'], psw=st.session_state['hf_pass'])
                    
                    st.experimental_rerun()
                    

    else:

        temperature = 0.5
        top_p = 0.95
        repetition_penalty = 1.2
        top_k = 50
        max_new_tokens = 1024

        st.session_state['plugin'] = "🌐 Web Search"

# WEB SEARCH PLUGIN
        if st.session_state['plugin'] == "🌐 Web Search" and 'web_search' not in st.session_state:
            # web search settings
            
                    st.session_state['region'] = 'us-en'
                    st.session_state['safesearch'] = 'moderate'
                    st.session_state['timelimit'] = 'y'
                    st.session_state['max_results'] = 5
                    st.session_state['web_search'] = "True"
                    st.experimental_rerun()

# END OF PLUGIN
    add_vertical_space(4)
    if 'hf_email' in st.session_state:
        if st.button('🗑 Logout'):
            keys = list(st.session_state.keys())
            for key in keys:
                del st.session_state[key]
            st.experimental_rerun()
##### End of sidebar


# User input
# Layout of input/response containers
input_container = st.container()
response_container = st.container()
data_view_container = st.container()
loading_container = st.container()



## Applying the user input box
#with input_container:
input_text = st.chat_input("🧑‍💻 Write here 👇", key="input")

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    final_prompt =  ""
    make_better = True
    source = ""

    with loading_container:

        if st.session_state['plugin'] == "🌐 Web Search" and 'web_search' in st.session_state:
            #get last message if exists
            if len(st.session_state['past']) == 1:
                context = f"User: {st.session_state['past'][-1]}\nBot: {st.session_state['generated'][-1]}\n"
            else:
                context = f"User: {st.session_state['past'][-2]}\nBot: {st.session_state['generated'][-2]}\nUser: {st.session_state['past'][-1]}\nBot: {st.session_state['generated'][-1]}\n"
            
            if 'web_search' in st.session_state:
                if st.session_state['web_search'] == "True":
                    with st.spinner('🚀 Using internet to get information...'):
                        internet_result = ""
                        internet_answer = ""
                        with DDGS() as ddgs:
                            ddgs_gen = ddgs.text(prompt, region=st.session_state['region'], safesearch=st.session_state['safesearch'], timelimit=st.session_state['timelimit'])
                            for r in islice(ddgs_gen, st.session_state['max_results']):
                                internet_result += str(r) + "\n\n"
                            fast_answer = ddgs.answers(prompt)
                            for r in islice(fast_answer, 2):
                                internet_answer += str(r) + "\n\n"

                        final_prompt = prompt4conversationInternet(prompt, context, internet_result, internet_answer)
                else:
                    final_prompt = prompt4conversation(prompt, context)
            else:
                final_prompt = prompt4conversation(prompt, context)

        if make_better:
            with st.spinner('🚀 Generating response...'):
                print(final_prompt)
                response = st.session_state['chatbot'].chat(final_prompt, temperature=temperature, top_p=top_p, repetition_penalty=repetition_penalty, top_k=top_k, max_new_tokens=max_new_tokens)
                response += source
        else:
            print(final_prompt)
            response = final_prompt

    return response

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if input_text and 'hf_email' in st.session_state and 'hf_pass' in st.session_state:
        response = generate_response(input_text)
        st.session_state.past.append(input_text)
        st.session_state.generated.append(response)
    

    #print message in normal order, frist user then bot
    if 'generated' in st.session_state:
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])):
                with st.chat_message(name="user"):
                    st.markdown(st.session_state['past'][i])
                
                with st.chat_message(name="assistant"):
                    if len(st.session_state['generated'][i].split("✅Source:")) > 1:
                        source = st.session_state['generated'][i].split("✅Source:")[1]
                        mess = st.session_state['generated'][i].split("✅Source:")[0]

                        st.markdown(mess)
                        with st.expander("📚 Source of message number " + str(i+1)):
                            st.markdown(source)

                    else:
                        st.markdown(st.session_state['generated'][i])

            st.markdown('', unsafe_allow_html=True)