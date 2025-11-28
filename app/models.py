from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# --- User Table ---
class User(Base):
    # The name of the table in the database
    __tablename__ = "users"

    # Columns (Fields)
    id = Column(Integer, primary_key=True, index=True)  # Unique ID (1, 2, 3...)
    email = Column(String, unique=True, index=True)     # User's email (must be unique)
    hashed_password = Column(String)                    # We store the HASH, not the real password
    is_active = Column(Boolean, default=True)           # Is the account active?

    # Relationships
    # This allows us to get all documents for a user: user.documents
    documents = relationship("Document", back_populates="owner")

# --- Document Table ---
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(String, nullable=True)  # Optional category for organization
    is_public = Column(Boolean, default=False)  # Whether the document is public (for future sharing feature)
    
    # Foreign Key: Links this document to a specific User ID
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relationship: Allows us to get the user who owns this doc: document.owner
    owner = relationship("User", back_populates="documents")


