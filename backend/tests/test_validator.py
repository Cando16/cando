from backend.core.validator import compare

def test_compare():
    original = "The kiln operates at 520 °C and handles 4,420 kg/day."
    rebuilt = "Running at 520 °C, the kiln processes 4,420 kg/day."
    spans = {"<<P1>>": "520 °C", "<<P2>>": "4,420 kg/day"}
    
    val = compare(original, rebuilt, spans)
    
    assert val["sentinels_intact"] is True
    assert val["severity"] == "ok"
    assert val["length_delta_ratio"] > 0
