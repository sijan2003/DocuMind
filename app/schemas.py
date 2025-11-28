from pydantic import BaseModel, EmailStr
from typing import Optional

# =======================
# Pydantic Schemas
# =======================
# These are used to validate data coming IN (Request) and going OUT (Response).

# --- User Schemas ---

# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr

# Schema for REGISTRATION (Input)
# We need the password here.
class UserCreate(UserBase):
    password: str

# Schema for READING User data (Output)
# We DO NOT include the password here for security.
class User(UserBase):
    id: int
    is_active: bool

    # This config tells Pydantic to read data from SQLAlchemy models
    class Config:
        from_attributes = True

# --- Token Schemas ---
# Used when returning the JWT token to the user
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Document Schemas ---
class DocumentBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    is_public: bool = False

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

