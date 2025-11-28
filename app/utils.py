from passlib.context import CryptContext

# Setup the password hashing context
# "bcrypt" is the hashing algorithm we use.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """
    Takes a plain password (e.g., "secret") and returns a hashed string.
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    Checks if the plain password matches the hashed password.
    Returns True if they match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

