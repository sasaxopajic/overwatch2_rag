import streamlit as st

from llama_index.core import (
    Settings,
    VectorStoreIndex,
    load_index_from_storage,
    StorageContext
    )

#Using SimpleWebPageReader to scrape data from a website
from llama_index.readers.web import SimpleWebPageReader

import os

from llama_index.llms.openai import OpenAI

#Load environmental variables
from dotenv import load_dotenv

load_dotenv()

#Changing the version of ChatGPT
Settings.llm = OpenAI(model="gpt-4o-mini", system_prompt="You have access to detailed data from the Overwatch Fandom wiki pages for Sombra, Moira, and Symmetra. Your job is to answer questions specifically about these characters. Make sure your responses are based only on facts from these pages, and never mix up the information about the characters. Always reference only the character relevant to the question, and if the user asks a general question, make it clear which character's information you're referencing. Strictly follow these instructions and ensure accuracy.")

#URL for data retrieving
URL=["https://overwatch.fandom.com/wiki/Sombra", "https://overwatch.fandom.com/wiki/Moira", "https://overwatch.fandom.com/wiki/Symmetra"]

#Streamlit Application
st.header("Overwatch 2 Chatbot")

# Path to the persistent storage directory
PERSIST_DIR = "./storage"

# Initialize the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question!"}
    ]

# Function to either load or create the index
def load_or_create_index():
    if os.path.exists(PERSIST_DIR):  # Check if persistent directory exists
        # Load the index from the storage directory
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        st.info("Index loaded from persisted storage.")
    else:
        # If not, create a new index and persist it
        reader = SimpleWebPageReader(html_to_text=True)
        docs = reader.load_data(URL)
        index = VectorStoreIndex.from_documents(docs)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        st.info("New index created and persisted.")
    return index

# Load the index (either from disk or by creating a new one)
index = load_or_create_index()

#Create the chat engine
chat_engine = index.as_chat_engine(chat_mode="openai", verbose=True)

#Prompt for user input and display message history
if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

#Pass query to chat engine and display response
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            #Expander for showing the information about the source nodes used to synthesize the response
            for node in response.source_nodes:
                with st.expander(f"{str(round(node.score*100, 2))} {"%"}"):
                    st.markdown(node.text)
                    #Check if metadata exists
                    if len(node.metadata) == 0:
                        st.info("\nMetadata for this node doesn't exist.")
                    else:
                        st.markdown(f"{"Metadata"}\n {node.text}")
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history