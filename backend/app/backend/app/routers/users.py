from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database, auth

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pwd = auth.hash_password(user.password)
    return crud.create_user(db=db, user=user, hashed_password=hashed_pwd)

@router.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user.id}
