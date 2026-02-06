from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import models, auth
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import requests
import ai_services

app = FastAPI(title="Academic Assignment Helper")

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
    access_token = auth.create_access_token(data={"sub": user.email, "role": "student"})
    return {"access_token": access_token, "token_type": "bearer"}


# --- JWT ---

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_student(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 'auth.SECRET_KEY' and 'auth.ALGORITHM' should be in your auth.py
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    student = db.query(models.Student).filter(models.Student.email == email).first()
    if student is None:
        raise credentials_exception
    return student

# --- ASSIGNMENT ---

N8N_WEBHOOK_URL = "http://n8n:5678/webhook/assignment" # [cite: 480]

@app.post("/assignments/upload")
async def upload_assignment(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_student: models.Student = Depends(get_current_student)
):
    # 1. Save file locally
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # 2. Create initial database record
    new_assignment = models.Assignment(
        filename=file.filename,
        student_id=current_student.id,
        original_text=None
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)

    # 3. Trigger n8n Webhook 
    payload = {
        "assignment_id": new_assignment.id,
        "student_email": current_student.email,
        "file_path": file_location
    }
    
    try:
        requests.post(N8N_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"n8n Trigger Failed: {e}")

    # 4. Return the ID for tracking 
    return {"status": "Analysis started", "job_id": new_assignment.id}


@app.get("/assignments/{assignment_id}/analysis")
def get_analysis(
    assignment_id: int, 
    db: Session = Depends(get_db),
    current_student: models.Student = Depends(get_current_student) # Authenticate
):
    # Check if the assignment exists AND belongs to this student
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id,
        models.Assignment.student_id == current_student.id
    ).first()
    
    if not assignment:
        # Return 404 even if it exists but belongs to someone else to prevent "ID fishing" (security best practice)
        raise HTTPException(status_code=404, detail="Assignment not found or unauthorized")

    # 2. Get the analysis linked to that assignment
    result = db.query(models.AnalysisResult).filter(
        models.AnalysisResult.assignment_id == assignment_id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Analysis still processing or not found")
        
    return {
        "assignment_id": result.assignment_id,
        "filename": assignment.filename, # Nice to include for the UI
        "plagiarism_score": result.plagiarism_score,
        "feedback": result.research_suggestions
    }