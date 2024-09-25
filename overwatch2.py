import streamlit as st
import os
import json

from llama_index.core import (
    Settings,
    VectorStoreIndex,
    load_index_from_storage,
    StorageContext
    )

#Import HeroNameExtractor class from a .py file
from hero_name_extractor import HeroNameExtractor

hero_name_extractor = HeroNameExtractor()

#Using SimpleWebPageReader to scrape data from a website
from llama_index.readers.web import SimpleWebPageReader

#Semantic chunking (TextSplitter)
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding

embed_model = OpenAIEmbedding()
splitter = SemanticSplitterNodeParser(
    buffer_size=1, breakpoint_percentile_threshold=95, embed_model=embed_model
)

#Title extractor
from llama_index.core.extractors import TitleExtractor

title_extractor = TitleExtractor(nodes=5)

#Import LLM
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
    try:
        if os.path.exists(PERSIST_DIR):  # Check if persistent directory exists
            # Load the index from the storage directory
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context)
            st.info("Index loaded from persisted storage.")
        else:
            # If not, create a new index and persist it
            reader = SimpleWebPageReader(html_to_text=True)
            docs = reader.load_data(URL)
            # Extracting the metadata with transformations
            index = VectorStoreIndex.from_documents(docs, transformations=[splitter, title_extractor, hero_name_extractor])
            index.storage_context.persist(persist_dir=PERSIST_DIR)
            st.info("New index created and persisted.")
        return index
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse JSON: {e}")
        return None

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
            st.header("Nodes retrieved")
            for node in response.source_nodes:
                with st.expander(f"{str(round(node.score*100, 2))} {"%"}"):
                    st.markdown(node.text)
                    #Check if metadata exists
                    if len(node.metadata) == 0:
                        st.info("Metadata for this node doesn't exist.")
                    else:
                        st.header("Metadata")
                        st.markdown(f"{node.metadata}")
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history