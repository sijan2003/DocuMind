from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models
from ..services import ai as ai_service
from ..routers.users import get_current_user

router = APIRouter(
    prefix="/ai",
    tags=["AI Features"]
)


# -------------------------------------------------------
# 1. SUMMARIZE DOCUMENT
# -------------------------------------------------------
@router.post("/summarize/{document_id}")
def summarize_document(
    document_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Generate a summary for a specific document using Google Gemini.
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {document_id} not found"
        )
    
    summary = ai_service.generate_summary(document.content)
    
    if summary.startswith("Error"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=summary
        )
        
    return {"summary": summary}


# -------------------------------------------------------
# 2. GET KEY POINTS
# -------------------------------------------------------
@router.post("/keypoints/{document_id}")
def extract_key_points(
    document_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Extract key bullet points from the document.
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    result = ai_service.extract_key_points(document.content)

    if result.startswith("Error"):
        raise HTTPException(status_code=500, detail=result)

    return {"key_points": result}


# -------------------------------------------------------
# 3. PARAPHRASE DOCUMENT
# -------------------------------------------------------
@router.post("/paraphrase/{document_id}")
def paraphrase_document(
    document_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Paraphrase or rewrite the document more clearly.
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    result = ai_service.paraphrase(document.content)

    if result.startswith("Error"):
        raise HTTPException(status_code=500, detail=result)

    return {"paraphrased": result}


# -------------------------------------------------------
# 4. ANSWER A QUESTION ABOUT DOCUMENT
# -------------------------------------------------------
@router.post("/ask/{document_id}")
def ask_question(
    document_id: int,
    question: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Ask a question based on the contents of the document.
    """
    document = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.owner_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    result = ai_service.answer_question(document.content, question)

    if result.startswith("Error"):
        raise HTTPException(status_code=500, detail=result)

    return {"answer": result}
