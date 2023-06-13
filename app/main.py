import uvicorn
from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from fastapi.security.api_key import APIKey
from auth import get_api_key
import model
import schemas
from database import engine, SessionLocal
from crud import user_register, check_user, key_details
from auth import get_api_key
from starlette.responses import Response

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register/")
async def create_user(user_input: schemas.UserCreate, db: Session = Depends(get_db)):

    username = user_input.username
    email = user_input.email
    
    if check_user(db, username):
        raise HTTPException(status_code=400, detail="User already registered")
    
    else:
        key = user_register(db, username, email)    
        return {"message": "User created", "username": username, "api_key": key}

@app.post("/user/authenticate")
async def authenticate_user(
    db: Session = Depends(get_db), 
    key: APIKey = Depends(get_api_key),response: Response = Response()
):

    user = key_details(db, key)
    response.set_cookie(
        key="key",
        value=key,
        
    )
    response.set_cookie(
        key="username",
        value=user.username,
        
    )
    response.set_cookie(
        key="email",
        value=user.email,
    )
    response.set_cookie(
        key="api_key_expiry",
        value=user.expire_date,
  
    )
    return {"message": "User authenticated", "username": user.username, "email": user.email}

@app.get("/getUserData", dependencies=[Depends(get_api_key)])
async def get_user_data(request: Request, api_key: APIKey = Depends(get_api_key), db: Session = Depends(get_db)):
    print(request.cookies)
    if "username" not in request.cookies:
        print("No cookies")
        users = key_details(db,api_key)
        return {"username": users.username, "email": users.email, "api_key_expiry": users.expire_date}

    print("Cookies Found")
    username = request.cookies.get("username")
    email = request.cookies.get("email")
    api_key_expiry = request.cookies.get("api_key_expiry")
    return {"username": username, "email": email, "api_key_expiry": api_key_expiry}
    
   
if __name__ == "__main__":
    uvicorn.run(app, port=8000)