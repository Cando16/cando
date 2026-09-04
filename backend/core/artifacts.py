import re
from typing import Tuple, List, Dict, Any

# Detect invisible unicode characters (zero-width space, zero-width non-joiner, etc.)
INVISIBLE_CHARS = [
    r'\u200B', # Zero-width space
    r'\u200C', # Zero-width non-joiner
    r'\u200D', # Zero-width joiner
    r'\uFEFF', # Zero-width no-break space
]

INVISIBLE_PATTERN = re.compile('|'.join(INVISIBLE_CHARS))

def clean_text(text: str) -> Tuple[str, List[Dict[str, Any]]]:
    # Returns cleaned text and a list of artifacts removed
    artifacts = []
    
    matches = INVISIBLE_PATTERN.findall(text)
    if matches:
        artifacts.append({
            "type": "invisible_unicode",
            "count": len(matches)
        })
        
    cleaned = INVISIBLE_PATTERN.sub('', text)
    
    return cleaned, artifacts
