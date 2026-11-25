from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.deps import CurrentUser, SessionDep
from app.models import User
from app.schemas import LoginIn, RegisterIn, TokenOut, UserOut
from app.security import create_access_token, hash_password, verify_password
from app.services.social import normalize_username, unique_username, valid_username

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, session: SessionDep):
    email = data.email.lower()
    if session.exec(select(User).where(User.email == email)).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    if data.username:
        username = normalize_username(data.username)
        if not valid_username(username):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Username: 3-20 letters, numbers, _ or .")
        if session.exec(select(User).where(User.username == username)).first():
            raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")
    else:
        username = unique_username(session, email.split("@")[0])
    user = User(email=email, name=data.name.strip(), hashed_password=hash_password(data.password), username=username)
    session.add(user)
    session.commit()
    session.refresh(user)
    return TokenOut(access_token=create_access_token(user.id))


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, session: SessionDep):
    user = session.exec(select(User).where(User.email == data.email.lower())).first()
    # Same error for unknown email and wrong password, so attackers can't probe accounts.
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    return TokenOut(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return UserOut(id=user.id, email=user.email, name=user.name, username=user.username, is_private=user.is_private)
