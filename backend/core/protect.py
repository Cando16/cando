import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Regions:
    body: str
    excluded: List[Tuple[str, str]]
    
    def reassemble(self, rewritten_body: str) -> str:
        res = rewritten_body
        for ph, content in self.excluded:
            res = res.replace(ph, content)
        return res

def split_no_rewrite_regions(text: str) -> Regions:
    excluded = []
    
    # 1. Extract References section
    # Matches "\nReferences" or "\n# References" followed by everything to the end
    ref_match = re.search(r'(?i)\n(?:#+\s+)?(?:References|Bibliography|Works Cited)\s*\n.*', text, flags=re.DOTALL)
    if ref_match:
        ref_text = ref_match.group(0)
        ph = f"<<EXCL_REF>>"
        excluded.append((ph, ref_text))
        text = text.replace(ref_text, ph)
        
    return Regions(body=text, excluded=excluded)

# Ordered list of regexes. 
REGEXES = [
    ("url", r'(https?://\S+|10\.\d{4,9}/[-._;()/:A-Z0-9]+)', re.IGNORECASE),
    ("citation", r'(\([A-Za-z\s&.,]+,\s*\d{4}\)|\[\d+(?:[–-]\d+)?\])', 0),
    ("date", r'(\d{1,2}\s+[A-Za-z]{3,}\s+\d{4}|\d{4}-\d{2}-\d{2})', 0),
    # For equations, we match LaTeX $...$ or specific demo patterns for now
    ("equation", r'(\$.*?\$|η\s*=\s*[0-9.]+)', 0),
    # Chemical formulas (case sensitive)
    ("chemical", r'(\b(?:[A-Z][a-z]?\d*){2,}\b)', 0), 
    ("noun_quotes", r'("[^"]+")', 0),
    # Numbers with units
    ("number_unit", r'(\d+(?:,\d+)*(?:\.\d+)?\s*(?:°C|bar|kg/day|m³/h|kg m⁻³|kg))', 0),
    # Bare numbers & percentages
    ("bare_number", r'(\b\d+(?:,\d+)*(?:\.\d+)?(?:%)?\b)', 0),
]

class SentinelError(Exception):
    pass

def mask(text: str) -> Tuple[str, Dict[str, str]]:
    spans = {}
    counter = 1
    
    # Simple placeholder format
    def get_ph(i): return f"<<P{i}>>"
    
    # We tokenize to avoid replacing inside already masked spans or breaking things
    # But for a quick implementation, we can just replace and rely on the fact that
    # our regexes shouldn't match <<Px>>.
    
    current_text = text
    for name, pattern, flags in REGEXES:
        
        def repl(match):
            nonlocal counter
            # All our regexes should have exactly one outer capture group
            val = match.group(1)
            if val.startswith("<<P") and val.endswith(">>"):
                return val
                
            ph = get_ph(counter)
            spans[ph] = val
            counter += 1
            return ph
            
        current_text = re.sub(pattern, repl, current_text, flags=flags)
        
    return current_text, spans

def unmask(text: str, spans: Dict[str, str]) -> str:
    for ph, content in spans.items():
        count = text.count(ph)
        if count != 1:
            raise SentinelError(f"Sentinel {ph} appeared {count} times (expected 1).")
        text = text.replace(ph, content)
        
    return text
