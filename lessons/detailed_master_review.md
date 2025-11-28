# Detailed Master Review: Code & Concepts

This document goes deep into every file we have created. It explains the **Syntax** (what the code says) and the **Logic** (what it does).

---

## 1. `app/database.py` (The Connection)
**Purpose**: Connect Python to PostgreSQL.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/ai_knowledge_hub"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### Breakdown
1.  **`create_engine`**: This is the actual "cable" plugging into the database. It holds the connection pool.
2.  **`SessionLocal`**: Think of this as a "Factory". When a user sends a request, we ask this factory: "Give me a session."
    -   *Session*: A temporary workspace where we add/delete data. When done, we close it.
3.  **`Base`**: This is a special Python class. Any class we create that inherits from `Base` will automatically become a SQL table.

---

## 2. `app/models.py` (The Tables)
**Purpose**: Define what our data looks like in the database.

```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    documents = relationship("Document", back_populates="owner")
```

### Breakdown
1.  **`class User(Base)`**: "Hey SQLAlchemy, this class represents a table."
2.  **`__tablename__`**: The actual name of the table in Postgres.
3.  **`Column(...)`**: Defines a column.
    -   `primary_key=True`: This is the unique ID (1, 2, 3...).
    -   `unique=True`: No two users can have the same email.
    -   `index=True`: Makes searching by this column faster.
4.  **`relationship(...)`**: This is **Magic**. It's not a real column. It tells Python: "If I have a User object, find all their Documents for me."

---

## 3. `app/schemas.py` (The Validator)
**Purpose**: Define what data the API accepts and returns.

```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    
    class Config:
        from_attributes = True
```

### Breakdown
1.  **`UserCreate`**: Used for **Input** (Registration).
    -   It has `password`. We need the user to send us a password.
2.  **`User`**: Used for **Output** (Response).
    -   It has `id` and `is_active`.
    -   **Crucially, it does NOT have `password`**. This ensures we never accidentally send the password back to the frontend.
3.  **`from_attributes = True`**: This tells Pydantic: "Hey, the data coming from the database is an Object (SQLAlchemy model), not a Dictionary. Please read it anyway."

---

## 4. `app/utils.py` (The Tools)
**Purpose**: Helper functions for security.

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)
```

### Breakdown
1.  **`bcrypt`**: A hashing algorithm designed to be slow and secure.
2.  **`hash_password`**:
    -   Input: `secret123`
    -   Output: `$2b$12$wK...` (Random-looking characters).
    -   **Why?** If a hacker steals our database, they only see the random characters, not the real password.

---

## 5. `app/routers/auth.py` (The Logic)
**Purpose**: Handle Login and Registration.

### Registration Logic
```python
@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Check if email exists
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(...)
    
    # 2. Hash the password
    hashed_pw = utils.hash_password(user.password)
    
    # 3. Save to DB
    new_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
```
-   **`db.add`**: "Put this in the temporary workspace."
-   **`db.commit`**: "Save it to the permanent database now."

### Login Logic
```python
@router.post("/login")
def login(...):
    # 1. Find user
    user = db.query(models.User).filter(...).first()
    
    # 2. Verify password
    if not utils.verify_password(input_password, user.hashed_password):
        raise HTTPException(...)
        
    # 3. Create Token
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token}
```
-   **Token**: A digital string signed with our `SECRET_KEY`. The user keeps this.

---

## 6. `app/main.py` (The Boss)
**Purpose**: Tie everything together.

```python
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
```

### Breakdown
1.  **`create_all`**: This checks the database. If the tables (`users`, `documents`) don't exist, it creates them. This is why you didn't have to write SQL `CREATE TABLE` commands manually.
2.  **`include_router`**: Adds the "Authentication Department" (`auth.py`) to the main application.
