
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

# Import your local modules
from schemas import ResumeRequest
from services import analyze_resume


app = FastAPI()

# 1. Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://resume-agent-1-oc9t.onrender.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global list to hold log messages for the UI
logs = []

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/stream-logs")
async def stream_logs(request: Request):
    """
    Endpoint for Server-Sent Events (SSE). 
    React will connect here to see 'Backend Activity'.
    """
    async def log_generator():
        while True:
            if await request.is_disconnected():
                break
            if logs:
                # Pop the oldest log and send it
                yield f"data: {logs.pop(0)}\n\n"
            await asyncio.sleep(0.5)

    return StreamingResponse(log_generator(), media_type="text/event-stream")

@app.post("/analyze-resume")
async def analyze(req: ResumeRequest):
    """
    Main analysis endpoint that pushes logs and returns AI data.
    """
    try:
        # Step 1: Log progress
        logs.append("🚀 Received resume data...")
        logs.append("🔍 Searching for market trends via Tavily...")
        
        # Step 2: Run the Agent
        result = await analyze_resume(req.text)
        
        # Step 3: Log success
        logs.append("🤖 AI Reasoning complete.")
        logs.append("✅ Feedback generated successfully!")

        # Convert AI result to JSON-friendly format
        json_response = jsonable_encoder(result)
        
        # Print to terminal for your debugging
        print("--- ANALYSIS SUCCESSFUL ---")
        print(json_response)
        
        return json_response

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        logs.append(error_msg)
        print(error_msg)
        return {"error": str(e)}