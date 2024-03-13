import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.agents import load_tools, create_react_agent, AgentExecutor
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain import hub
from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache

# Set up API keys
# Set up API keys

OPENAI_API = open('open_api_key') 
OPENAI_API_KEY = OPENAI_API.read()

SERPAPI = open("SERPAPI_API_KEY")
SERPAPI_API_KEY = SERPAPI.read()

os.environ['OPENAI_API_KEY']= OPENAI_API_KEY
os.environ['SERPAPI_API_KEY'] = SERPAPI_API_KEY


# Pull necessary components
llm = ChatOpenAI(temperature=0)
prompt = hub.pull('hwchase17/react')
tools = load_tools(["serpapi"], llm=llm)

# Initialize agent and executor
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True)

# Initialize cache
set_llm_cache(InMemoryCache())

# Initialize output parser
output_parser = CommaSeparatedListOutputParser()

# Function to fetch activities based on interest, destination, and city
def searching_country(interest, destination, city):
    
    system_template = "You are an AI assistant that specializes in recommending exciting,funlife time memories events for                            tourists based on thier highlighted interest and the exact location where they can be found.keep it concise                       and short with not more than 12 suggestions"
                     
                        
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    human_template = "{request}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    msg = f"Kindly give details of activities that can be done in {city} {destination} based on my {interest})"

    request = chat_prompt.format_prompt(request=msg).to_messages()
    result = agent_executor.invoke({'input': request})
    result = result['output']

    return result

# Streamlit app
if __name__ == "__main__":
    st.title("Discover the World! 🌍")
    st.subheader('Holiday Plan 🧳')

    Language = ["English"]
    option = st.sidebar.selectbox("Language", Language, index=0)

    if option:
        st.subheader('Holiday Planner 🤖')
        destination = st.text_input("Embark on your next journey! Please share the country you're eager to explore. ✈️ 🌍")
        city = st.text_input("What city or state would you like to explore?")

        if destination and city:
            st.write(f"You're eager to explore {city} in {destination}")
            st.divider()

        interest = ["Sightseeing", "Cultural experiences", "Outdoor adventures", "Shopping", "Culinary experiences",                                 "Relaxation", "Meeting new people", 'Learning']

        x = st.multiselect(label="Events", options=interest)
        st.write("Let's plan your adventure 🏖️🏝️🍹🌞")
        st.divider()

        if st.button("Discover"):
            activities = searching_country(interest, city, destination)
            st.text_area(label=f"Activities suited to your interest in {city}", value=activities, height=1000)
