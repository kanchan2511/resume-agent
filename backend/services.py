import json
from agent import run_agent
import asyncio

async def analyze_resume(text: str):
    if len(text.strip()) < 50:
        return {"error": "Resume text is too short to analyze."}
    
    try:
        # If you make run_agent async
        # analysis = await run_agent(text) 
        analysis = await asyncio.wait_for(run_agent(text), timeout=60)
        return analysis.model_dump()
    except asyncio.TimeoutError:
        return {"error": "AI took too long to respond. Please try again."}
    except Exception as e:
        print(f"CRITICAL AGENT ERROR: {e}") 
        return {"error": "The AI had trouble reading that. Please try again."}