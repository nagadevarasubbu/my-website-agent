import os
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from typing import List, Optional

from agent_logic import generate_website_package

app = FastAPI(title="Website Generator Agent API")

# CORS for agent↔agent / n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    website_type: str
    business_name: Optional[str] = None
    sections_required: List[str]
    callback_url_for_assets: Optional[str] = None

    @field_validator("sections_required")
    @classmethod
    def _clean_sections(cls, v: List[str]):
        # Trim whitespace-only items
        return [s for s in (v or []) if isinstance(s, str) and s.strip()]

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate-website")
async def generate_website(payload: GenerateRequest = Body(...)):
    result = generate_website_package(payload.model_dump())
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)
