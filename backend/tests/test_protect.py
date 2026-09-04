import pytest
from backend.core.protect import mask, unmask, split_no_rewrite_regions, SentinelError

def test_mask_and_unmask():
    text = "The kiln operates at 520 °C and handles 4,420 kg/day (Smith, 2025). The equation is η = 0.87. We also use H2SO4 at 2.5 bar."
    
    masked, spans = mask(text)
    
    assert "520 °C" not in masked
    assert "4,420 kg/day" not in masked
    assert "(Smith, 2025)" not in masked
    assert "η = 0.87" not in masked
    assert "H2SO4" not in masked
    assert "2.5 bar" not in masked
    
    # Assert sentinels are present
    assert "<<P1>>" in masked
    
    unmasked = unmask(masked, spans)
    assert unmasked == text

def test_unmask_fails_on_missing_sentinel():
    text = "Value is 520 °C."
    masked, spans = mask(text)
    
    # Simulate model dropping the sentinel
    bad_rewrite = "Value is 520 degrees."
    with pytest.raises(SentinelError):
        unmask(bad_rewrite, spans)

def test_unmask_fails_on_duplicated_sentinel():
    text = "Value is 520 °C."
    masked, spans = mask(text)
    
    # Simulate model duplicating the sentinel
    bad_rewrite = f"Value is {list(spans.keys())[0]} and {list(spans.keys())[0]}."
    with pytest.raises(SentinelError):
        unmask(bad_rewrite, spans)

def test_adversarial_reordering():
    text = "A 520 °C, B 2.5 bar, C H2SO4"
    masked, spans = mask(text)
    
    # We don't know the exact order of P1, P2, P3 without checking, but let's assume
    # P1=H2SO4 (chemical), P2=520 °C (number_unit), P3=2.5 bar (number_unit)
    # The actual order depends on regex evaluation order.
    # Chemical is evaluated before number_unit.
    
    # Let's dynamically find them for the test
    rev_spans = {v: k for k, v in spans.items()}
    p_h2so4 = rev_spans["H2SO4"]
    p_520 = rev_spans["520 °C"]
    p_25 = rev_spans["2.5 bar"]
    
    reordered = f"C {p_h2so4}, A {p_520}, B {p_25}"
    
    unmasked = unmask(reordered, spans)
    assert unmasked == "C H2SO4, A 520 °C, B 2.5 bar"

def test_split_no_rewrite_regions():
    text = "Body text here.\n\nReferences\nSmith, J. (2025)."
    regions = split_no_rewrite_regions(text)
    
    assert "Body text here." in regions.body
    assert "References" not in regions.body
    
    reassembled = regions.reassemble(regions.body)
    assert reassembled == text
