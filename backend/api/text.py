from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from backend.core import pipeline, humanizer, no_ai_slop, artifacts

router = APIRouter()

class TextRequest(BaseModel):
    content: str
    options: humanizer.CandoOptions = humanizer.CandoOptions()

@router.post("/inspect")
async def inspect_text(req: TextRequest):
    _, in_report = artifacts.clean_text(req.content)
    detected_slop = []
    for rule in no_ai_slop.RULES:
        if rule.detect(req.content):
            detected_slop.append(rule.name)
            
    return {
        "artifacts": in_report,
        "patterns": detected_slop
    }

@router.post("/clean")
async def clean_text(req: TextRequest):
    sanitized, report = artifacts.clean_text(req.content)
    return {"result": sanitized, "artifacts": report}

@router.post("/humanize")
async def humanize_text(req: TextRequest):
    revised = await humanizer.process(req.content, req.options)
    return {"result": revised}

@router.post("/no-ai-slop")
async def remove_slop(req: TextRequest):
    cleaned = no_ai_slop.process(req.content, req.options)
    return {"result": cleaned}

@router.post("/cando")
async def full_cando(req: TextRequest):
    return StreamingResponse(
        pipeline.run_cando_sse(req.content, req.options), 
        media_type="text/event-stream"
    )
