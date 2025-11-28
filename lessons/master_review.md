# Master Review: The Journey So Far

You asked for a complete breakdown of everything we've done. Here is the story of our application.

## The Goal
We are building an **AI-Powered Research Hub**.
To do this, we need a backend that can:
1.  Talk to the internet (API).
2.  Store data (Database).
3.  Keep secrets (Authentication).

---

## Step 1: The Foundation (FastAPI)
### What did we do?
We installed `fastapi` and `uvicorn` and created an `app`.

### Why?
We need a program that listens for HTTP requests (like a browser visiting a page) and sends back answers.
-   **FastAPI**: The logic (the brain).
-   **Uvicorn**: The server (the mouth/ears).

### The Code (`app/main.py`)
```python
app = FastAPI()
```
This initializes our application. Everything starts here.

---

## Step 2: The Database (SQLAlchemy)
### What did we do?
We set up **PostgreSQL** and created `database.py` and `models.py`.

### Why?
If we just keep data in Python variables, it disappears when we restart the server. We need a permanent filing cabinet.
-   **SQLAlchemy**: The translator. It translates Python code (`user.email`) into SQL commands (`SELECT email FROM users`).

### The Code
**`app/database.py`**:
-   `create_engine`: Opens the connection line to Postgres.
-   `SessionLocal`: Creates a temporary workspace for each request.

**`app/models.py`**:
-   `class User(Base)`: Defines the "Users" table.
-   `class Document(Base)`: Defines the "Documents" table.
-   `relationship(...)`: Links them together (User owns Documents).

---

## Step 3: Data Validation (Pydantic)
### What did we do?
We created `app/schemas.py`.

### Why?
We don't trust the user. They might send "banana" instead of an email address. Pydantic stands at the door and checks everyone's ID.
-   **SQLAlchemy Models (`models.py`)**: For the *Database*.
-   **Pydantic Schemas (`schemas.py`)**: For the *API* (Input/Output).

### The Code (`app/schemas.py`)
```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str
```
If a user tries to register without a password, Pydantic throws an error before our code even runs.

---

## Step 4: Security (Authentication)
### What did we do?
We created `app/utils.py` and `app/routers/auth.py`.

### Why?
1.  **Password Hashing**: We can't save "password123" in the database. If we get hacked, everyone is doomed. We save a "hash" (scrambled version).
2.  **JWT Tokens**: When you log in, we give you a digital ID card (Token). You show this card for future requests so you don't have to type your password every time.

### The Code
**`app/utils.py`**:
-   `hash_password`: Turns "secret" into "$2b$12$..."
-   `verify_password`: Checks if a password matches the hash.

**`app/routers/auth.py`**:
-   `POST /login`: Takes email/password -> Checks DB -> Returns Token.

---

## Summary of Files
-   **`main.py`**: The boss. Connects everything.
-   **`database.py`**: The phone line to the database.
-   **`models.py`**: The blueprint for database tables.
-   **`schemas.py`**: The bouncer (validator).
-   **`routers/`**: The departments (Auth department, Users department).
-   **`utils.py`**: The toolbox (hashing functions).
