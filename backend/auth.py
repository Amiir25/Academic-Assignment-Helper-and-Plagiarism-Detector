from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Configuration - In a real app, move these to a .env file
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# pwd_context = CryptContext(
#     schemes=["bcrypt"], 
#     deprecated="auto",
#     bcrypt__truncate_error=False  # This stops the 72-byte error
# )
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def hash_password(password: str):
    # Manually encode and truncate to 72 bytes to satisfy modern bcrypt
    # truncated_password = password.encode('utf-8')[:72]
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    # truncated_password = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)