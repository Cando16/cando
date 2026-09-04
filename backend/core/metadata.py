import datetime

def scrub_docx_metadata(doc):
    props = doc.core_properties
    props.author = ""
    props.comments = ""
    props.keywords = ""
    props.last_modified_by = ""
    props.subject = ""
    props.title = ""
    props.category = ""
    
    epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
    try:
        props.created = epoch
        props.modified = epoch
    except Exception:
        pass # Fallback if python-docx version balks at setting dates
