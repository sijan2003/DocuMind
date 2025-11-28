from app import database
from sqlalchemy import text

engine = database.engine

with engine.connect() as conn:
    # Add category column
    conn.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS category VARCHAR"))
    # Add is_public column
    conn.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS is_public BOOLEAN DEFAULT FALSE"))
    conn.commit()

print("Columns added successfully!")
