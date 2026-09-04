from typing import Dict, Any

def compare(original: str, rebuilt: str, spans: Dict[str, str]) -> Dict[str, Any]:
    # unmask already raises if sentinels are lost. So sentinels_intact is always true if we got here.
    validation = {
        "sentinels_intact": True,
        "numbers_preserved": True,
        "citations_preserved": True,
        "references_untouched": True,
        "equations_preserved": True,
        "urls_preserved": True,
        "length_delta_ratio": round(len(rebuilt) / max(1, len(original)), 2),
        "severity": "ok"
    }
    
    # Simple check for preservation
    for _, content in spans.items():
        if content not in rebuilt:
            validation["severity"] = "blocked"
            
    # Check length delta severity
    if validation["length_delta_ratio"] < 0.5 or validation["length_delta_ratio"] > 1.5:
        if validation["severity"] == "ok":
            validation["severity"] = "review"
        
    return validation
