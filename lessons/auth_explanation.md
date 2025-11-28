# Understanding Authentication (`app/routers/auth.py`)

Here is the line-by-line breakdown of how our authentication works.

## 1. Imports & Setup (Lines 1-16)
```python
router = APIRouter(prefix="/auth", tags=["Authentication"])
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
```
-   **`APIRouter`**: We use this to group our auth routes together.
-   **`SECRET_KEY`**: This is used to sign the JWT tokens. If someone knows this, they can forge tokens. **In production, this comes from an environment variable.**
-   **`ALGORITHM`**: The math used to sign the token.

## 2. Creating Tokens (Lines 18-23)
```python
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```
-   **`data`**: The info we want to put inside the token (like the user's email).
-   **`expire`**: Tokens must expire (e.g., after 30 mins) for security.
-   **`jwt.encode`**: This creates the long string `eyJhbGci...` that is the actual token.

## 3. Registration (Lines 25-38)
```python
@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(...)):
```
-   **Step 1**: Check if email exists (`db.query(...).first()`). If yes, error.
-   **Step 2**: **Hash the password**. `utils.hash_password(user.password)`.
    -   *Crucial*: We never save `user.password` directly.
-   **Step 3**: Save to DB and return the user info (without the password).

## 4. Login (Lines 40-53)
```python
@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), ...):
```
-   **`OAuth2PasswordRequestForm`**: A FastAPI helper that expects `username` and `password` form fields.
-   **Step 1**: Find user by email (`user_credentials.username`).
-   **Step 2**: **Verify Password**. `utils.verify_password(...)`.
    -   This checks if the password they sent matches the hash in the DB.
-   **Step 3**: If valid, **Create Token** (`create_access_token`) and return it.
