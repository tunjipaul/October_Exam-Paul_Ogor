from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
import bcrypt
import uvicorn
from database import get_db

app = FastAPI(title="NIGERIAN STATES API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class User(BaseModel):
    full_name: str = Field(..., example="sam")
    email: str = Field(..., example="sam@gmail.com")
    password: str = Field(..., example="sam123")

class UserLogin(BaseModel):
    email: str = Field(..., example="sam@gmail.com")
    password: str = Field(..., example="sam123")

@app.get("/")
def home():
    return "Welcome to my API"

@app.post("/signup")
def sign_up(input: User, db=Depends(get_db)):
    duplicate_query = text("SELECT * FROM users WHERE email = :email")
    existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = bcrypt.hashpw(input.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query = text(
        "INSERT INTO users (full_name, email, password_hash) VALUES (:full_name, :email, :password_hash)"
    )
    db.execute(query, {"full_name": input.full_name, "email": input.email, "password_hash": hashed_password})
    db.commit()
    return {"message": "User created successfully", "data": {"name": input.full_name, "email": input.email}}

@app.post("/login")
def login(input: UserLogin, db=Depends(get_db)):
    query = text("SELECT * FROM users WHERE email = :email")
    user = db.execute(query, {"email": input.email}).fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not bcrypt.checkpw(input.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login Successful!", "user": {"email": user.email, "full_name": user.full_name}}

@app.get("/states")
def states(db=Depends(get_db)):
    get_states = text("SELECT * FROM states")
    result = db.execute(get_states).mappings().all()
    if not result:
        return {"message": "No states yet. Try again later!"}
    return {"states": result}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
