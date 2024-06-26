import json
import os
import uuid
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Union
from urllib.parse import unquote

from fastapi import FastAPI, File, Form, UploadFile, status, Depends, HTTPException, Request, Header, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError

from celery_worker import process_files_task
import jwt
from llmMessenger import predict

# FastAPI app initialization
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 这里的 "token" 应该是你的登录端点
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database setup
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:czt1717@localhost/opentutor"  # 替换为你的实际连接字符串
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Upload folder setup
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# JWT setup
SECRET_KEY = "~r2Xgk~.2uW,mKZ=t"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7200  # 5 days

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Database models
class UserInDB(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True, index=True)
    courseName = Column(String, index=True, nullable=False)
    school = Column(String)
    professor = Column(String)
    year = Column(String)
    info = Column(Text)
    skip = Column(Boolean, default=False)


class UserCourse(Base):
    __tablename__ = "user_courses"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    # user_id = Column(Integer, primary_key=True)
    course_code = Column(String, ForeignKey("courses.id"), primary_key=True)


class FileMetadata(Base):
    __tablename__ = "file_metadata"
    file_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    # user_id = Column(Integer)
    course_id = Column(String, ForeignKey("courses.id"))
    file_path = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# Pydantic models

class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
    username: str


class CourseCreate(BaseModel):
    courseName: str
    school: str = None
    professor: str = None
    year: str = None
    info: str = None
    skip: bool = False


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JWT functions
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: str = payload.get("id")
        if user_id is None:
            raise credentials_exception
        return {"id": user_id}
    except JWTError:
        raise credentials_exception


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Routes
'''
@app.post("/api/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = UserInDB(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@app.post("/api/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserInDB).filter(UserInDB.username == user.username).first()
    if db_user and pwd_context.verify(user.password, db_user.password):
        access_token = create_access_token(
            data={"id": db_user.id, "username": db_user.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
'''


@app.get("/generate-token")
def generate_token(db: Session = Depends(get_db)):
    user_id = str(uuid.uuid4())
    print("Token generated.")
    token = create_access_token(data={"id": user_id})
    db_user = UserInDB(id=user_id, username="test" + user_id[:6], password="123456")
    db.add(db_user)
    db.commit()
    return {"access_token": token, "token_type": "bearer"}


'''
@app.post("/token")
def login_for_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
) -> Token:
    user_id = str(uuid.uuid4())
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user_id}, expires_delta=access_token_expires
    )
    db_user = UserInDB(id=user_id, username="test"+user_id[:6], password="123456")
    db.add(db_user)
    db.commit()

    print("Token generated.")
    return {"access_token": access_token, "token_type": "bearer"}
'''


@app.post("/api/register-course")
def create_course(course: CourseCreate = Body(...), current_user: dict = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    course_id = str(uuid.uuid4())
    cur_user_id = current_user["id"]
    print(cur_user_id)

    # Check values of course.
    if not course.skip and course.courseName == "":
        raise HTTPException(status_code=400, detail="Course name required.")

    try:
        db_course = Course(id=course_id, **course.dict())
        db.add(db_course)
        db.commit()
        # db.refresh(db_course)  # 刷新会话以确保数据同步

        user_course = UserCourse(user_id=cur_user_id, course_code=course_id)
        db.add(user_course)
        db.commit()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Course created successfully", "course_id": course_id}


class FileStorage:
    def __init__(self):
        self.data = defaultdict(list)
        self.user_id = None

    def set_files(self, user_id, coursePath, saved_files):
        self.user_id = user_id
        self.data[user_id].append(coursePath)
        self.data[user_id].append(saved_files)

    def get_files(self, user_id):
        if user_id != self.user_id:
            print(user_id)
            print(self.user_id)
            raise ValueError("Invalid path for this user")
        return self.data[user_id][0], self.data[user_id][1]

    def clear(self, user_id):
        self.data[user_id].clear()



file_storage = FileStorage()


@app.post("/api/submit")
async def submit(
        request: Request,
        course_id: str = Form(...),
        textbook: list[UploadFile] = File(None),
        homework: list[UploadFile] = File(None),
        mockTests: list[UploadFile] = File(None),
        others: list[UploadFile] = File(None),
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user_id = current_user["id"]
    user_path = os.path.join(UPLOAD_FOLDER, str(user_id))
    course_path = os.path.join(user_path, course_id)
    os.makedirs(course_path, exist_ok=True)

    files = {
        'textbook': textbook,
        'homework': homework,
        'mockTests': mockTests,
        'others': others
    }

    # 检查是否有文件上传
    if not any(files.values()):
        raise HTTPException(status_code=400, detail='No file uploaded')

    saved_files = []
    for category, file_list in files.items():
        if file_list:
            category_path = os.path.join(course_path, category)
            os.makedirs(category_path, exist_ok=True)
            for file in file_list:
                file_path = os.path.join(category_path, file.filename)
                with open(file_path, "wb") as buffer:
                    buffer.write(await file.read())
                saved_files.append(file_path)

    file_storage.set_files(user_id, course_path, saved_files)

    return {"message": "Files received", "courseID": course_id}



@app.get("/api/processed-files")
def get_processed_files(course_id: str, current_user: dict = Depends(get_current_user)):
    try:
        user_id = current_user["id"]
        cPath, sFiles = file_storage.get_files(user_id)
        if not cPath or not sFiles:
            raise ValueError("Invalid file storage data")

        task = process_files_task.delay(cPath, sFiles)
        return {"status": "processing", "task_id": str(task.id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/task-status")
def get_task_status(task_id: str, course_id:str, current_user: dict = Depends(get_current_user)):
    task = process_files_task.AsyncResult(task_id)
    print("I found the task!~~~~~~~~~~~~~~~~~~~~~~")
    if task.ready():
        result = task.result
        print("Its ready!~~~~~~~~~~~~~~~~~~~~~~")
        if isinstance(result, str) and result.startswith("Error"):
            return {"status": "error", "message": result}

        user_id = current_user["id"]

        user_path = os.path.join(UPLOAD_FOLDER, str(user_id), str(course_id), "to_download")
        download_path = os.path.join(str(user_id), str(course_id), "to_download")

        if os.path.exists(user_path):
            processed_files = [os.path.join(download_path, file) for file in os.listdir(user_path)]
            file_storage.clear(user_id)
            return {"status": "completed", "processed_files": processed_files}
        else:
            return {"status": "error", "message": "to_download directory not found"}
    else:
        return {"status": "processing"}


@app.get("/download/{path:path}")
async def download_file(path: str):
    # print(f"Requested path: {path}")
    decoded_path = unquote(path)
    # print(f"Decoded path: {decoded_path}")
    file_path = os.path.join(UPLOAD_FOLDER, decoded_path)

    # 安全检查：确保文件路径不会超出 UPLOAD_FOLDER
    if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_FOLDER)):
        raise HTTPException(status_code=403, detail="Access to this file is forbidden")

    if os.path.isfile(file_path):
        return FileResponse(file_path, filename=os.path.basename(file_path))
    else:
        raise HTTPException(status_code=404, detail="File not found")


# Warning! Must be disabled in real deployment.
@app.post("/clear-database/")
def clear_db_route(db: Session = Depends(get_db)):
    try:
        Base.metadata.drop_all(bind=engine)
        return {"message": "Database cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing database: {str(e)}")


def clear_database(db: Session):
    meta = MetaData(bind=engine)
    meta.reflect()
    for table in reversed(meta.sorted_tables):
        db.execute(table.delete())
    db.commit()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8010, reload=True)
