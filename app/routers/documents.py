from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from .. import database, models, schemas
from ..routers.users import get_current_user
from ..services import file_processor

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# ==========================================
# FILE UPLOAD - POST /documents/upload
# ==========================================
@router.post("/upload", response_model=schemas.Document, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    category: str = None,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Upload a file (PDF, DOCX, TXT) and create a document from it.
    Text will be automatically extracted from the file.
    """
    # Validate file size (10MB limit)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 10MB limit"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    try:
        # Extract text from file
        content = await file_processor.process_file(file)
        
        # Use filename as title if not provided
        if not title:
            title = file.filename.rsplit('.', 1)[0]  # Remove extension
        
        # Create document
        new_document = models.Document(
            title=title,
            content=content,
            category=category,
            is_public=False,
            owner_id=current_user.id
        )
        
        db.add(new_document)
        db.commit()
        db.refresh(new_document)
        
        return new_document
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )


# ==========================================
# CREATE - POST /documents/
# ==========================================
@router.post("/", response_model=schemas.Document, status_code=status.HTTP_201_CREATED)
def create_document(
    doc: schemas.DocumentCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Create a new document for the authenticated user.
    """
    new_document = models.Document(
        title=doc.title,
        content=doc.content,
        category=doc.category,
        is_public=doc.is_public,
        owner_id=current_user.id
    )
    
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    return new_document


# ==========================================
# READ ALL - GET /documents/
# ==========================================
@router.get("/", response_model=List[schemas.Document])
def get_all_documents(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get all documents owned by the authenticated user.
    """
    documents = db.query(models.Document).filter(
        models.Document.owner_id == current_user.id
    ).all()
    
    return documents


# ==========================================
# READ ONE - GET /documents/{id}
# ==========================================
@router.get("/{id}", response_model=schemas.Document)
def get_document(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get a specific document by ID.
    """
    document = db.query(models.Document).filter(
        models.Document.id == id,
        models.Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {id} not found"
        )
    
    return document


# ==========================================
# UPDATE - PUT /documents/{id}
# ==========================================
@router.put("/{id}", response_model=schemas.Document)
def update_document(
    id: int,
    doc: schemas.DocumentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Update a document.
    """
    document_query = db.query(models.Document).filter(
        models.Document.id == id,
        models.Document.owner_id == current_user.id
    )
    
    document = document_query.first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {id} not found"
        )
    
    document_query.update({
        "title": doc.title,
        "content": doc.content,
        "category": doc.category,
        "is_public": doc.is_public
    }, synchronize_session=False)
    
    db.commit()
    db.refresh(document)
    
    return document


# ==========================================
# DELETE - DELETE /documents/{id}
# ==========================================
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Delete a document.
    """
    document = db.query(models.Document).filter(
        models.Document.id == id,
        models.Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with id {id} not found"
        )
    
    db.delete(document)
    db.commit()
    
    return None
