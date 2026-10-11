from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session 
from db_connection import sessionLocal, engine
from db_models.register_model import Register as register_db , Base
from models.register_model import Register as register_schema
from passwordHash import hash_password , verify_password
from jwtService import generate_token , current_user
from fastapi.security import OAuth2PasswordRequestForm
from redis_client import redis_client
from rate_limiter import rate_limit
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware ,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greet():
    return {"message": "Hello there"}


@app.get("/redis-test")
def redis_test():
    redis_client.set("test_key", "hello")
    value = redis_client.get("test_key")

    return {
        "redis": value
    }

# regsiter api
@app.post("/register")
def register_user(register:register_schema , db :Session = Depends(get_db)):
    # hash password 
    hashPassword = hash_password(register.password)
    newUser = register_db(
        username=register.username,
        password = hashPassword
    )
    db.add(newUser)
    db.commit()
    return {"User added successfully"}


# for login 
@app.post("/login")
def login_user(
    # form_data: OAuth2PasswordRequestForm = Depends(),
    user:register_schema,
    db: Session = Depends(get_db),
    _: None = Depends(rate_limit)
):
    # OAuth2 calls this field "username"
    # We use it to find our user
    register_user = db.query(register_db).filter(
        register_db.username == user.username
    ).first()

    if not register_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        register_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = generate_token({
        "sub": register_user.username
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# protected route 

@app.get("/get")
def get_users(db:Session=Depends(get_db) ,user:str= Depends(current_user)):
    return db.query(register_db).all()

    