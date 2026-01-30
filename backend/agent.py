
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool # Import the tool decorator
from schemas import ResumeAnalysis
from prompts import RESUME_PROMPT


load_dotenv()

# 1. Initialize LLM
llm = ChatGroq(temperature=0, model="llama-3.1-8b-instant")

# 2. CREATE A WRAPPER TOOL
# This hides the complex schema from the LLM and forces correct types
@tool
def get_market_trends(query: str):
    """
    Searches the internet for current high-demand skills, 
    job market trends, and industry requirements.
    """
    search = TavilySearch(max_results=2)
    # We hard-code the boolean parameters here so the LLM never sees them
    return search.run(query)

tools = [get_market_trends]

# 3. Agent Instructions - Updated to mention the new tool name
system_message = (
    "You are a professional Career Coach Agent. Analyze the resume and provide feedback. "
    "Use the 'get_market_trends' tool to find high-demand skills for the job titles mentioned. "
    "Then, compare the resume against those trends."
)

# 4. Create Agent
agent_executor = create_react_agent(llm, tools, prompt=system_message)

async def run_agent(resume_text: str):
    try:
        # Step A: Execute Agentic Search and Reasoning
        response = await agent_executor.ainvoke({
            "messages": [HumanMessage(content=f"Analyze this resume: {resume_text}")]
        })
        
        agent_final_thought = response["messages"][-1].content

        # Step B: Force into Pydantic Schema
        structured_llm = llm.with_structured_output(ResumeAnalysis)
        
        # return await structured_llm.ainvoke(
        #     f"Based on these findings, provide structured JSON feedback: {agent_final_thought}"
        # )
        return await structured_llm.ainvoke(
           RESUME_PROMPT.format(resume_text=agent_final_thought)
        )
    except Exception as e:
        print(f"AGENT-LEVEL ERROR: {e}")
        raise e
