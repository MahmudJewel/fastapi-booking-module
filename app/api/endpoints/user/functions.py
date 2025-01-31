from fastapi import HTTPException, status, Depends
from typing import Annotated
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import JWTError, jwt

# # import 
from app.models import user as UserModel
from app.schemas.user import UserCreate, UserUpdate, User
from app.core.settings import SECRET_KEY, REFRESH_SECRET_KEY, ALGORITHM
from app.core.dependencies import oauth2_scheme
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.user import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# get user by email 
async def get_user_by_email(email: str):
    return await UserModel.User.find_one(UserModel.User.email == email)

# get user by id
async def get_user_by_id(user_id: str):
    db_user = await UserModel.User.find_one(UserModel.User.id == user_id)
    # print('==========================>', db_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# crete new user 
async def create_new_user(user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    new_user = UserModel.User(email=user.email, password=hashed_password, first_name=user.first_name, last_name=user.last_name)
    # new_user = UserModel.User(**user.model_dump())
    await new_user.insert()
    return new_user
    


# get all user 
async def read_all_user(skip:int, limit:int):
    users = await UserModel.User.all().skip(skip).limit(limit).to_list()
    return users

# update user
async def update_user(user_id: str, user: UserUpdate):
    db_user = await get_user_by_id(user_id)
    updated_data = user.model_dump(exclude_unset=True) # partial update
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    await db_user.save()
    return db_user

# delete user
async def delete_user(user_id: str):
    db_user = await get_user_by_id( user_id)
    await db_user.delete()
    return {"msg": f"{db_user.email} deleted successfully"}

# # =====================> login/logout <============================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(user: UserCreate):
    member = await get_user_by_email(email=user.email)
    # print("authenticate_user ======>", member, member.email)
    if not member:
        return False
    if not verify_password(user.password, member.password):
        return False
    return member

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        # member = await User.get(user_id)
        member = await get_user_by_id(user_id)
        if member is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(
            data={"id": member.id, "email": member.email, "role": member.role},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
# get current users info 
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f"Payload =====> {payload}")
        current_email: str = payload.get("email")
        if current_email is None:
            raise credentials_exception
        user = await get_user_by_email( current_email)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

