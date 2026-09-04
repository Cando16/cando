import pytest
import docx
import io
import datetime
from backend.core.metadata import scrub_docx_metadata

def test_scrub_docx_metadata():
    doc = docx.Document()
    props = doc.core_properties
    props.author = "John Doe"
    props.last_modified_by = "Jane Doe"
    props.comments = "Secret project details"
    
    # Save and reload just to prove they exist initially
    stream = io.BytesIO()
    doc.save(stream)
    stream.seek(0)
    
    reloaded_doc = docx.Document(stream)
    assert reloaded_doc.core_properties.author == "John Doe"
    
    # Scrub
    scrub_docx_metadata(reloaded_doc)
    
    assert reloaded_doc.core_properties.author == ""
    assert reloaded_doc.core_properties.last_modified_by == ""
    assert reloaded_doc.core_properties.comments == ""
    assert reloaded_doc.core_properties.created.year == 1970
