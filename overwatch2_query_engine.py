# Define the metadata filters
from llama_index.legacy.vector_stores.types import MetadataFilter, MetadataFilters

from llama_index.core.tools import RetrieverTool
from llama_index.agent.openai import OpenAIAgent

HEROES = ["Sombra", "Moira", "Symmetra"]

# Function to create the hero-specific retriever
def create_hero_retriever_tool(index, hero_name):
    hero_name_filter = MetadataFilter(key='hero_name', value=hero_name)
    retrieve_filters = MetadataFilters(filters=[hero_name_filter])
    retriever = index.as_retriever(filters=retrieve_filters)
    return RetrieverTool.from_defaults(retriever, name=f"{hero_name}_retriever" ,description=f"Useful for getting information about specific Overwatch 2 hero: {hero_name}")

# Function to create the general retriever
def create_general_retriever_tool(index):
    retriever = index.as_retriever()
    return RetrieverTool.from_defaults(retriever, name="general_retriever", description="Useful for general information about Overwatch 2")

# Function to create chat engine by combining general and all hero specific retrievers
def create_chat_engine(index):
    tools = [create_hero_retriever_tool(index, hero) for hero in HEROES]
    tools.append(create_general_retriever_tool(index))
    return OpenAIAgent.from_tools(
        tools=tools,
        streaming=True,
        verbose=True
    )
