# FastAPI Concepts for Beginners

I realized I jumped into the deep end with Authentication. Let's pause and understand the **FastAPI specific tools** we just used in `auth.py`.

## 1. `APIRouter` (The "Mini-App")
Imagine you are building a house.
-   `app = FastAPI()` is the whole house.
-   You don't want to put the kitchen, bedroom, and bathroom all in one big room (`main.py`).
-   **`APIRouter`** lets you build the "Kitchen" (`auth.py`) and "Bedroom" (`users.py`) separately.
-   Then in `main.py`, you just say: `app.include_router(auth.router)`.

## 2. `Depends` (The "Helper")
This is one of the most important concepts in FastAPI.
Imagine you go to a restaurant. You order food. You don't need to know *how* the chef got the ingredients or turned on the stove. You just want the food.

In code:
```python
def login(db: Session = Depends(get_db)):
```
-   **You (the function)**: "I need a database connection to do my job."
-   **FastAPI**: "Okay, I see you need `get_db`. I will run that function, get the connection, and hand it to you."

**Why?** It makes your code clean. You don't have to write "connect to db" in every single function.

## 3. `HTTPException` (The "Error Reporter")
When something goes wrong, you can't just `print("Error")`. You need to tell the *browser* or *app* what happened using standard Web Codes.

-   **200 OK**: Success.
-   **400 Bad Request**: User made a mistake (e.g., email already exists).
-   **401 Unauthorized**: User isn't logged in.
-   **403 Forbidden**: User is logged in but not allowed to do this.
-   **404 Not Found**: It's gone.

Code:
```python
raise HTTPException(status_code=400, detail="Email already registered")
```
This stops the function immediately and sends a "400" error back to the user with your message.

## 4. `OAuth2PasswordRequestForm`
This is just a fancy way FastAPI helps you handle login forms.
-   It expects the user to send a `username` and `password`.
-   It saves you from writing code to parse the JSON body yourself.

## Summary
-   **Router**: Organize code into files.
-   **Depends**: Ask FastAPI to give you things (like DB connections).
-   **HTTPException**: Stop and send an error.
