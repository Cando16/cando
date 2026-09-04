import pytest
from backend.core.pipeline import run_cando
from backend.core.humanizer import CandoOptions
from pathlib import Path

@pytest.mark.asyncio
async def test_run_cando_demo():
    # Load demo text
    demo_path = Path(__file__).parent / "fixtures" / "demo.txt"
    with open(demo_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    options = CandoOptions()
    
    result = await run_cando(content, options)
    
    assert result.original == content
    assert result.validation["severity"] == "ok"
    
    # Assert protected values are intact
    assert "520 °C" in result.result
    assert "4,420 kg/day" in result.result
    assert "η = 0.87" in result.result
    assert "H2SO4" in result.result
    assert "2.5 bar" in result.result
    assert "(Smith, 2025)" in result.result
    
    # Test slop removal rules ran (since we didn't mock the provider, it just passes through, but slop rules apply)
    # The fixture has: "Furthermore, it is important to note that"
    # Our rule replaces with "Additionally, "
    assert "Additionally, " in result.result
    assert "Furthermore, it is important to note that" not in result.result
    
    assert "This shows the importance of" in result.result
    assert "This highlights the significance of" not in result.result
