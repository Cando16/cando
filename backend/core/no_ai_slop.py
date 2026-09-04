import re
from backend.core.humanizer import CandoOptions
from typing import List

class SlopRule:
    name: str = "Unknown"
    confidence: float = 1.0

    def detect(self, text: str) -> bool:
        return False
        
    def fix(self, text: str) -> str:
        return text

class ThroatClearing(SlopRule):
    name = "Throat Clearing"
    confidence = 0.9
    def detect(self, text: str) -> bool: return bool(re.search(r'(?i)\b(?:it is important to note that|it should be noted that|it is worth noting that)\b', text))
    def fix(self, text: str) -> str: return re.sub(r'(?i)\b(?:It is important to note that|It should be noted that|It is worth noting that)\s*', '', text)

class FauxInsightRule(SlopRule):
    name = "Faux Insight"
    confidence = 0.95
    def detect(self, text: str) -> bool: return bool(re.search(r'(?i)\bThis highlights the significance of\b', text))
    def fix(self, text: str) -> str: return re.sub(r'(?i)\bThis highlights the significance of\b', 'This shows the importance of', text)

class ImportancePufferyRule(SlopRule):
    name = "Importance Puffery"
    confidence = 0.85
    def detect(self, text: str) -> bool:
        if re.search(r'(?i)\brobust process control\b', text):
            return False # Context guard
        return bool(re.search(r'(?i)\bin today\'s rapidly evolving world\b', text))
    def fix(self, text: str) -> str: return re.sub(r'(?i)\bIn today\'s rapidly evolving world,?\s*', '', text)

class UnsupportedAttribution(SlopRule):
    name = "Unsupported Attribution"
    confidence = 0.8
    def detect(self, text: str) -> bool: return bool(re.search(r'(?i)\bexperts agree that\b', text))
    def fix(self, text: str) -> str: return re.sub(r'(?i)\bexperts agree that\s*', '', text)

class MechanicalTransitions(SlopRule):
    name = "Mechanical Transitions"
    confidence = 0.95
    def detect(self, text: str) -> bool: return bool(re.search(r'(?i)\b(?:Moreover|Furthermore|Additionally)[\s,]+(?:it is important to note that|it should be noted that)\b', text))
    def fix(self, text: str) -> str: return re.sub(r'(?i)\b(?:Moreover|Furthermore|Additionally)[\s,]+(?:it is important to note that|it should be noted that)\s*', 'Additionally, ', text)

class NotOnlyButAlso(SlopRule):
    name = "Not Only But Also"
    confidence = 0.8
    def detect(self, text: str) -> bool: return bool(re.search(r'(?i)not only.*?but also', text))
    # Too complex for simple regex replace reliably, low confidence so might not auto apply.
    def fix(self, text: str) -> str: return text 

RULES: List[SlopRule] = [
    MechanicalTransitions(),
    ThroatClearing(),
    FauxInsightRule(),
    ImportancePufferyRule(),
    UnsupportedAttribution(),
    NotOnlyButAlso()
]

def process(text: str, options: CandoOptions) -> str:
    threshold = 0.85
    for rule in RULES:
        if rule.confidence >= threshold and rule.detect(text):
            text = rule.fix(text)
    return text
