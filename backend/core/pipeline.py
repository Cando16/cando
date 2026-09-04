from pydantic import BaseModel
from typing import List, Dict, Any, AsyncGenerator
import json
from backend.core import protect, artifacts, humanizer, no_ai_slop, validator

class CandoResult(BaseModel):
    original: str
    result: str
    validation: Dict[str, Any]
    artifacts: List[Dict[str, Any]]

async def run_cando_sse(content: str, options: humanizer.CandoOptions) -> AsyncGenerator[str, None]:
    # Yield progress messages
    yield json.dumps({"step": "Sanitizing"}) + "\n"
    sanitized, in_report = artifacts.clean_text(content)
    
    yield json.dumps({"step": "Protecting content"}) + "\n"
    regions = protect.split_no_rewrite_regions(sanitized)
    masked, spans = protect.mask(regions.body)
    
    # Auto-engage logic (rough approximation for citation and unit detection)
    citation_count = sum(1 for name in spans.values() if "(" in name or "[" in name)
    unit_count = sum(1 for name in spans.values() if any(u in name for u in ["°C", "bar", "kg", "m³"]))
    
    if citation_count >= 3:
        options.academic_mode = True
    if unit_count >= 5:
        options.technical_preservation = True
        
    yield json.dumps({"step": "Humanizing"}) + "\n"
    stage1 = await humanizer.process(masked, options)
    
    yield json.dumps({"step": "Removing AI-slop patterns"}) + "\n"
    stage2 = no_ai_slop.process(stage1, options)
    
    yield json.dumps({"step": "Validating"}) + "\n"
    body = protect.unmask(stage2, spans)
    rebuilt, out_report = artifacts.clean_text(regions.reassemble(body))
    val = validator.compare(content, rebuilt, spans)
    
    result = CandoResult(
        original=content,
        result=rebuilt,
        validation=val,
        artifacts=in_report + out_report
    )
    yield json.dumps({"step": "Done", "result": result.model_dump()}) + "\n"

async def run_cando(content: str, options: humanizer.CandoOptions) -> CandoResult:
    async for event in run_cando_sse(content, options):
        data = json.loads(event.strip())
        if data.get("step") == "Done":
            return CandoResult(**data["result"])
    raise RuntimeError("Pipeline did not yield a Done event")
