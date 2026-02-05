from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import models, auth

app = FastAPI(title="Academic Assignment Helper")

# Database Connection (Remember we used port 5433 for host access!)
SQLALCHEMY_DATABASE_URL = "postgresql://student:secure_password@localhost:5433/academic_helper"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a DB connection for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Server is running!"}

# --- AUTHENTICATION ENDPOINTS ---

@app.post("/auth/register")
def register(email: str, password: str, full_name: str, db: Session = Depends(get_db)):
    # 1. Check if user exists
    user_exists = db.query(models.Student).filter(models.Student.email == email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Hash password and save
    hashed_pwd = auth.hash_password(password)
    new_student = models.Student(email=email, password_hash=hashed_pwd, full_name=full_name)
    db.add(new_student)
    db.commit()
    return {"message": "Student registered successfully"}

@app.post("/auth/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.Student).filter(models.Student.email == email).first()
    if not user or not auth.verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Issue the "Badge" (Token)
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- ASSIGNMENT UPLOAD ---

@app.post("/assignments/upload")
async def upload_assignment(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    # 1. Read the file content
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return {"error": "Only .txt files are supported for now."}
    
    # 2. Save to database (Linking to the student we just created)
    # For now, we'll hardcode student_id=1. Tomorrow we'll use the Token!
    new_assignment = models.Assignment(
        filename=file.filename,
        original_text=text,
        student_id=1 
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return {
        "assignment_id": new_assignment.id,
        "filename": file.filename,
        "status": "Stored in Database"
    }