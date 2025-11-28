# --- Database Connection Setup ---
# 1. Import SQLAlchemy tools
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 2. Define the Database URL
# Format: postgresql://<username>:<password>@<host>/<database_name>
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/ai_knowledge_hub"

# 3. Create the Engine
# The "engine" is the actual connection to the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. Create the SessionLocal
# This is a "factory" that creates new database sessions.
# We use this session to talk to the database (add, delete, query).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Create the Base Class
# All our database models (tables) will inherit from this class.
Base = declarative_base()

# 6. Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
