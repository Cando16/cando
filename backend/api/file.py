from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from backend.core import document, humanizer
import io

router = APIRouter()

@router.post("/process")
async def process_file(
    file: UploadFile = File(...),
    level: str = Form("standard"),
    academic_mode: bool = Form(False),
    technical_preservation: bool = Form(False)
):
    options = humanizer.CandoOptions(
        level=level,
        academic_mode=academic_mode,
        technical_preservation=technical_preservation
    )
    
    content = await file.read()
    filename = file.filename or "document.docx"
    
    if filename.lower().endswith(".docx"):
        out_bytes = await document.process_docx(content, options)
        out_filename = filename.replace(".docx", "_cando.docx")
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif filename.lower().endswith(".pdf"):
        out_bytes = await document.process_pdf(content, options)
        out_filename = filename.replace(".pdf", "_cando.docx")
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")
        
    return StreamingResponse(
        io.BytesIO(out_bytes),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{out_filename}"'}
    )
