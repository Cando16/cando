from pydantic import BaseModel
from backend.providers import get_provider
from backend.providers.base import ProviderUnavailable

class CandoOptions(BaseModel):
    temperature: float = 0.3
    level: str = "standard" # "light", "standard", "strong"
    academic_mode: bool = False
    technical_preservation: bool = False

SYSTEM_PROMPT = """You are the Humanizer stage of the CANDO editing pipeline.

Rewrite wording and sentence flow only. Improve awkward sentences, vary
sentence length naturally, use direct wording, and remove unnecessary
repetition.

Tokens of the form <<P1>>, <<P2>> etc. are protected placeholders. Reproduce
each one exactly as written, exactly once. Do not alter, translate, split,
renumber, or explain them.

Do not add factual information. Do not fabricate citations. Do not change
conclusions or claims. Do not weaken technical precision. Do not introduce
deliberate errors or slang.

Return only the revised text, with no preamble or commentary."""

async def process(text: str, options: CandoOptions) -> str:
    if options.level == "light":
        return text
        
    provider = get_provider()
    
    prompt = SYSTEM_PROMPT
    if options.academic_mode:
        prompt += "\n\nACADEMIC MODE IS ON: Disable all factual expansion. Preserve cautious hedging language. Never simplify discipline terminology."
    if options.technical_preservation:
        prompt += "\n\nTECHNICAL PRESERVATION IS ON: Forbid stylistic rewriting of technical expressions."
        
    try:
        revised = await provider.complete(prompt, text, temperature=options.temperature)
        return revised
    except ProviderUnavailable:
        return text
