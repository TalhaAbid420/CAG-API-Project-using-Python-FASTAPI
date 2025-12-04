from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Query
)
import uuid as uuid_pkg
import os

from src.data_store import data_store
from ..utils.llm_client import get_llm_response
from ..utils.pdf_processor import extract_text_from_pdf


# Create router
router = APIRouter()

# Temporary folder for storing uploaded PDFs
UPLOAD_DIR = "/tmp/cag_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
#   POST: Upload a new PDF
# -----------------------------
@router.post("/upload/{uuid}", status_code=201)
def upload_pdf(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Upload a PDF for a specific UUID.
    Extract PDF text and store it.
    Fails if UUID already exists.
    """

    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are accepted."
        )

    uuid_str = str(uuid)

    # If UUID already exists, user should use PUT instead
    if uuid_str in data_store:
        raise HTTPException(
            status_code=400,
            detail=f"UUID {uuid_str} already exists. Use PUT /api/v1/update/{uuid_str} to update."
        )

    # Create a temporary path
    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_{file.filename}")

    try:
        # Save uploaded PDF
        with open(file_path, "wb") as temp_file:
            temp_file.write(file.file.read())

        # Extract text
        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text:
            raise HTTPException(
                status_code=500,
                detail="Failed to extract text from the PDF."
            )

        # Store in centralized memory
        data_store[uuid_str] = extracted_text

        return {
            "message": "File uploaded and text extracted successfully.",
            "uuid": uuid_str
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while processing PDF: {str(e)}"
        )

    finally:
        # Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)


# -----------------------------
#   PUT: Append more PDF data
# -----------------------------
@router.put("/update/{uuid}")
def update_pdf_data(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Append new PDF text to an existing UUID.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF files are accepted."
        )

    uuid_str = str(uuid)

    # UUID must exist
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404,
            detail=f"UUID {uuid_str} not found. Use POST to create it first."
        )

    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_update_{file.filename}")

    try:
        # Save uploaded PDF
        with open(file_path, "wb") as temp_file:
            temp_file.write(file.file.read())

        # Extract new text
        new_text = extract_text_from_pdf(file_path)

        if not new_text:
            raise HTTPException(
                status_code=500,
                detail="Failed to extract text from the PDF."
            )

        # Append text
        data_store[uuid_str] += "\n\n" + new_text

        return {"message": "Data appended successfully.", "uuid": uuid_str}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while processing PDF: {str(e)}"
        )

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# -----------------------------
#   GET: Query LLM with PDF text
# -----------------------------
@router.get("/query/{uuid}")
def query_data(uuid: uuid_pkg.UUID, query: str = Query(..., min_length=1)):
    """
    Query an LLM using stored PDF text as context.
    """

    uuid_str = str(uuid)

    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404,
            detail=f"UUID {uuid_str} not found."
        )

    stored_text = data_store[uuid_str]

    llm_response = get_llm_response(
        context=stored_text,
        query=query
    )

    return {
        "uuid": uuid_str,
        "query": query,
        "llm_response": llm_response
    }


# -----------------------------
#   DELETE: Remove UUID data
# -----------------------------
@router.delete("/data/{uuid}", status_code=200)
def delete_data(uuid: uuid_pkg.UUID):
    """
    Delete stored text for a UUID.
    """

    uuid_str = str(uuid)

    if uuid_str not in data_store:
        raise HTTPException(
            status_code=404,
            detail=f"UUID {uuid_str} not found."
        )

    del data_store[uuid_str]

    return {"message": f"Data for UUID {uuid_str} deleted successfully."}


# -----------------------------
#   GET: List all UUIDs
# -----------------------------
@router.get("/list_uuids")
def list_all_uuids():
    """
    Return list of all UUIDs in memory.
    """
    return {"uuids": list(data_store.keys())}
