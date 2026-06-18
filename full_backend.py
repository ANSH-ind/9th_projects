import os
import io
import time
import asyncio
import sys
import logging
from PIL import Image,UnidentifiedImageError
from fastapi.staticfiles import StaticFiles
from pathlib import Path 
import shutil
from fastapi import FastAPI, HTTPException,Depends, status, File, UploadFile, Request, BackgroundTasks,WebSocket, WebSocketDisconnect
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import create_engine,Column, Integer, String,Text, or_

from jose import JWTError, jwt
import yagmail
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.decorator import cache

from sqlalchemy.orm import sessionmaker, declarative_base,Session
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from passlib.context import CryptContext

from datetime import datetime, timedelta, timezone

from fastapi.responses import JSONResponse,HTMLResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(InMemoryBackend(), prefix="ansh-cache")
    yield



REFRESH_TOKEN_EXP_TIME = 60*24*7

limiter = Limiter(key_func = get_remote_address)

email_pass = "nbaq wbbc lrgw htft"

async def send_email(email: str, name: str):
    yag = yagmail.SMTP(
    user = "anshraj0000000001@gmail.com",
    password = email_pass)
    
    yag.send(
    to = email,
    subject = "thanks for visiting our site",
    contents = f"hii {name} I am ansh raj from Bihar if you want to see more project of ai & ml now you can join or suscribe our youtube channel ansh_py and also if you want to me as a friend you can mail me.")
    
    
logger = logging.getLogger("Fast API logs")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s -%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
file_handler = logging.FileHandler("server.log")
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
uploaded_img = "/storage/emulated/0/uploaded_images"
os.makedirs(uploaded_img, exist_ok = True)


SECRET_CODE = "this_is_long_password"
ALGRITHOM = "HS256"
PASS_EXP_TIME = 30

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes = REFRESH_TOKEN_EXP_TIME)
    to_encode.update({"exp": expire,"token_type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_CODE, algorithm = ALGRITHOM)
    return encoded_jwt
    
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated= "auto")

def hash_pass(password: str):
    return pwd_context.hash(password)
    
def verify_pass(plane_pass, hashed_pass):
    return pwd_context.verify(plane_pass, hashed_pass)
    
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)+timedelta(minutes= PASS_EXP_TIME)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_CODE, algorithm = ALGRITHOM)
    return encode_jwt

auth_scheme = OAuth2PasswordBearer(tokenUrl = "login")


#set sqlite url for communicate with databse
db_url = "sqlite:///./databases_v2.db"

#create database engine 
engine = create_engine(
db_url,
connect_args = {"check_same_thread": False}) #if we change check same thread False to True then we need to create more threads for every request

local_session = sessionmaker(autocommit = False, autoflush = False ,bind = engine)

base = declarative_base()

class user_table(base):
    __tablename__ = "users"
    user_name = Column(String, unique = True, index = True)
    email = Column(String, unique = True)
    password = Column(String)
    name = Column(String, nullable = False)
    post_massage = Column(Text)
    ID = Column(Integer, primary_key = True, index = True, autoincrement = True)
    profile_pic_url = Column(String, default="")
    role = Column(String, default = "user")
    
    
    
class user_basemodel(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    name: str
    post_massage: Optional[str]
    
class user_response_model(BaseModel):
    user_name: str
    post_massage: Optional[str]
    profile_pic_url: str
    
    class config:
        from_attributes = True

base.metadata.create_all(bind=engine)

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(auth_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
    status_code = 401,
    detail = "token are expired",
    headers = {"WWW-Authenticate": "Bearer"})
    try:
         payload = jwt.decode(token, SECRET_CODE, algorithms = [ALGRITHOM])
         user_id: str = payload.get("user_id")
         if user_id is None:
             raise credentials_exception
             
    except JWTError:
         raise credentials_exception
    user_details = db.query(user_table).filter(user_table.ID == user_id).first()
    if user_details is None:
         raise credentials_exception
    return user_details
 
def get_admin_user(current_user: user_table = Depends(get_current_user)):
    if current_user.role != "admin":
         raise HTTPException(
         status_code = 401,
         detail = "this route is not for general peoples")
    return current_user
         
                 
app = FastAPI(
lifespan=lifespan,
title="ansh api program",
description="this is only for testing fastapi api's speed...", 
version = "1.0.0", 
docs_url = "/docs",
contact={
"owner": "ansh raj",
"email": "anshraj0000000001@gmail.com",
"mobile number": 9508481289},
debug = True,
servers = [
{"url": "http://localhost:8000/"}])

app.mount("/static", StaticFiles(directory="/storage/emulated/0/uploaded_images"), name="static")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


origins = [
"http://localhost:3000",
"http://127.0.0.1:5500",   
"http://localhost:5173",
"https://anshstudios.pages.dev/"]
app.add_middleware(
CORSMiddleware,
allow_origins = origins,
allow_credentials = True,
allow_methods = ["*"],
allow_headers = ["*"])



def get_current_user(
    token: str = Depends(auth_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_CODE,
            algorithms=[ALGRITHOM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(user_table)\
             .filter(user_table.ID == user_id)\
             .first()

    if user is None:
        raise credentials_exception

    return user
    

    
@app.get("/admin_dash/", tags = ["admin route"], summary = "this route can be accessed only by admin", status_code = 201)
async def admin_route(admin_user: user_table = Depends(get_admin_user)):
    return {"massage: ": "welcome to admin pannel",
    "role: ": "main Admin",
    "server runs on": "ubuntu"}
    
        
              
@app.middleware("http")
async def process_t_haeader(request: Request, call_next):
    st_time = time.time()

    try:
        response = await call_next(request)

    except Exception as e:
        logger.error(
            f"CRITICAL CRASH -> Path: {request.url.path} | Error: {str(e)}"
        )

        response = JSONResponse(
            status_code=500,
            content={
                "error_type": "Internal Server Error",
                "message": "Sorry, we are trying to fix this website."
            }
        )

    end_time = time.time() - st_time
    process_time_ms = f"{end_time * 1000:.2f} ms"
    response.headers["X-Process-Time"] = process_time_ms

    return response
    

@app.post("/login", tags = ["login"], summary = "this is main login route", status_code = 200)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(user_table).filter(
        or_(
            user_table.user_name == form_data.username,
            user_table.email == form_data.username
        )
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username/email"
        )

    if not verify_pass(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    access_token = create_access_token(
        data={"user_id": user.ID}
    )
    refresh_token = create_refresh_token(
    data = {"user_id": user.ID})

    return {
        "refresh_token": refresh_token,
        "access_token": access_token,
        "token_type": "bearer"
    }
 
    
class TokenRefresh(BaseModel):
    refresh_token: str
    
   
@app.post("/refresh", tags = ["return refresh token"], summary = "this return refresh token and then frontend store in their local db")
async def refresh_access_token(token_data: TokenRefresh):
    credentials_exception = HTTPException(
    status_code = 401,
    detail = "refresh token has been expired",
    headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = jwt.decode(token_data.refresh_token, SECRET_CODE, algorithms=[ALGRITHOM])
        user_id: str = payload.get("user_id")
        token_type: str = payload.get("token_type")
        if user_id is None or token_type != "refresh":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    new_access_token =create_access_token(data= {"user_id":user_id})
    
    return {
    "access_token": new_access_token,
    "token_type": "bearer"}
    


@app.get("/", tags = ["home"], status_code = 200, summary = "this route is for home if you search our website and open it then you are in this route")
async def home(token: str = Depends(auth_scheme)):
    return {"massage": "welcome to our site and server apis"}
    

@app.post("/add_user", tags = ["add user"], summary = "this route is for adding new user to the database (sql database)", status_code = 201)
async def add_user(bg_task: BackgroundTasks,user_data: user_basemodel,db : Session = Depends(get_db)):
    is_user_exist = db.query(user_table).filter(or_(user_table.user_name == user_data.user_name,
    user_table.email == user_data.email)).first()    
    if is_user_exist is not None:
        if is_user_exist.user_name == user_data.user_name or is_user_exist.email == user_data.email:
            raise HTTPException(
            status_code = 401,
            detail = f"user with username {user_data.user_name} already exist and may be email is already exist please try with another email")
    hashed_pass = hash_pass(user_data.password)
    bg_task.add_task(send_email,user_data.email, user_data.user_name)
    new_user = user_table(user_name = user_data.user_name, email = user_data.email, password = hashed_pass, name = user_data.name, post_massage = user_data.post_massage)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"massage": f"new user added with name {user_data.name} and id {new_user.ID}"}
    
@app.get("/search_user/{user_id}", tags = ["search user"], summary = "this route is for search user by id", status_code = 200, response_model = user_response_model)
@cache(expire=30)
async def search_user(user_id: int, db: Session = Depends(get_db), current_user: user_table = Depends(get_current_user)):
    user_details = db.query(user_table).filter(user_table.ID == user_id).first()
    if user_details is None:
        raise HTTPException(
        status_code = 401,
        detail = "user not found")
    return user_details

@app.put("/edit/{user_id}", tags = ["edit profile"], summary = "this route for update data that are database", status_code = 201)
async def edit(user_id: int, update_user: user_basemodel, db: Session = Depends(get_db)):
    user_exist = db.query(user_table).filter(user_table.ID == user_id).first()
    if not user_exist:
        raise HTTPException(
        status_code = 401,
        detail = f"user's id that you entered {user_id} not found in our database")
    user_exist.user_name = update_user.user_name
    user_exist.email = update_user.email
    
    db.commit()
    db.refresh(user_exist)
    return {"massage: ": f"user username and email has been updated username: {user_exist.user_name} email: {user_exist.email}"}
    
@app.delete("/delete/{user_id}", tags = ["delete route"], summary = "this route is for deleting the use that are already exist", status_code = 201)
async def delete_data(user_id: int, db: Session = Depends(get_db)):
    user_data = db.query(user_table).filter(user_table.ID == user_id).first()
    if not user_data:
        raise HTTPException(
        status_code = 401,
        detail = "user you want to delete isn't found")
    db.delete(user_data)
    db.commit()
    return {"massage": "user deleted"}

@app.post("/upload_profile_pic/", tags = ["edit profile photo"], summary = "this route is for uploading your profile pic and we save it to our database", status_code = 200)

async def upload_pic(
request: Request,
file: UploadFile = File(...),
current_user: user_table = Depends(get_current_user), db: Session = Depends(get_db)):
    
    file_content = await file.read()
    try:
         img = Image.open(io.BytesIO(file_content))
         img.verify()
#        img = Image.open(io.BytesIO(file_content))
    except UnidentifiedImageError:
        raise HTTPException(
        status_code = 400,
        detail = "please upload image not video")
    logger.info("image verification complete\n")
    await file.seek(0)
    extension = Path(file.filename).suffix.lstrip(".")
    new_file = f"user_{current_user.ID}_profile.{extension}"
    file_location = f"{uploaded_img}/{new_file}"
    with open(file_location, "wb") as upload_file:
        shutil.copyfileobj(file.file, upload_file)
   
    base_url = str(request.base_url)
    file_url = f"{base_url}static/{new_file}"
    current_user.profile_pic_url = file_url
    db.commit()
    db.refresh(current_user)
    return current_user
 
@app.get("/test-crash")
async def test_crash():
    # ZeroDivisionError aayega yahan 100%
    calculation = 10 / 0 
    return {"result": calculation}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"critical crash -> path : {request.url.path} | error: {str(exc)}")
    
    return JSONResponse(
    status_code = 500,
    content = {
    "error type: ": "Internal server error",
    "massage": "we are fixing this error we are requested you to try again after some time \nthanks"})

          
if __name__ == "__main__":
    uvicorn.run(app, host ="0.0.0.0", port = 8000)
