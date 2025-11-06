import os
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# ✅ Import the real logic from agent_logic.py
from agent_logic import generate_website_package

app = FastAPI(title="Website Generator Agent API")

# Allow requests from anywhere (important for agent → agent communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request format expected from my friend's agent
class GenerateRequest(BaseModel):
    website_type: str
    business_name: Optional[str] = None
    sections_required: List[str]

# ✅ Health check (for testing server is running)
@app.get("/health")
async def health():
    return {"status": "ok"}

# ✅ Main website generation endpoint
@app.post("/generate-website")
async def generate_website(payload: GenerateRequest = Body(...)):
    result = generate_website_package(payload.model_dump())
    return result

# ✅ Local development entry point (ignored in deployment)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
