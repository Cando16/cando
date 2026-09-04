from backend.core.artifacts import clean_text

def test_clean_text():
    # Insert some zero-width spaces
    text = "Hello\u200B World\u200D!"
    cleaned, report = clean_text(text)
    
    assert cleaned == "Hello World!"
    assert len(report) == 1
    assert report[0]["type"] == "invisible_unicode"
    assert report[0]["count"] == 2

def test_clean_text_clean():
    text = "Hello World!"
    cleaned, report = clean_text(text)
    assert cleaned == "Hello World!"
    assert len(report) == 0
