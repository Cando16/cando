# CANDO Implementation Plan

This document outlines the implementation plan for the CANDO project, following the strict constraints and phased approach provided in the specification.

## Phase List

*   **Phase 0:** Repo, backend skeleton, config, provider abstraction, CI (Required)
*   **Phase 1:** Protected-content engine + deterministic text cleanup (Required)
*   **Phase 2:** Humanizer + No-AI-Slop + full text API + web UI (Required)
*   **Phase 3:** DOCX/PDF read, process, export (Required)
*   **Phase 4:** Word add-in (Required)
*   **Phase 5:** File metadata hygiene (Optional)
*   **Phase 6:** Media reading (Optional, gated)
*   **Phase 7:** Image/video visible-watermark studio (Optional, gated)

## Phase 0 Files to Create

*   `pyproject.toml`, `requirements.txt`, `package.json`
*   `backend/main.py`: FastAPI application entry point.
*   `backend/config.py`: Pydantic Settings for configuration.
*   `backend/api/status.py`: Router for `/api/status`.
*   `backend/providers/base.py`: `AIProvider` abstract base class.
*   `backend/providers/openrouter.py`, `backend/providers/ollama.py`, `backend/providers/null_provider.py`: Provider implementations.
*   `backend/tests/test_status.py`, `backend/tests/test_providers.py`: Phase 0 tests.
*   `.env.example`, `.gitignore`
*   `NOT_IMPLEMENTED.md`, `THIRD_PARTY_NOTICES.md`, `README.md`

## Phase 1 Files to Create

*   `backend/core/protect.py`: Protected-span extraction, masking, and unmasking.
*   `backend/core/artifacts.py`: Invisible Unicode inspection and cleaning.
*   `backend/core/validator.py`: Post-hoc validation of protected spans.
*   `backend/core/humanizer.py`: Stub for model-based rewriting.
*   `backend/core/no_ai_slop.py`: Stub for deterministic context-aware rules.
*   `backend/core/pipeline.py`: The canonical `run_cando` function.
*   `backend/tests/test_protect.py`, `backend/tests/test_artifacts.py`, `backend/tests/test_validator.py`, `backend/tests/test_pipeline.py`: Phase 1 tests.
*   `backend/tests/fixtures/demo.txt`: The required demo fixture.

## Disagreements / Points of Clarification

I have read the document fully and agree with the technical decisions and constraints, including the input-side sanitization and the masking approach. I have no disagreements. I am ready to proceed with Phase 0 upon approval.
