from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import status, text, file

app = FastAPI(title="CANDO API", version="0.1.0")

# CORS allowlist: only Vite dev origin and Office add-in origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status.router, prefix="/api", tags=["status"])
app.include_router(text.router, prefix="/api/text", tags=["text"])
app.include_router(file.router, prefix="/api/file", tags=["file"])

if __name__ == "__main__":
    import uvicorn
    from backend.config import settings
    uvicorn.run("backend.main:app", host=settings.CANDO_HOST, port=settings.CANDO_PORT, reload=True)
