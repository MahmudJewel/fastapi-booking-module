# fastapi 
from fastapi import APIRouter, HTTPException
from datetime import timedelta

# auth google 
from starlette.requests import Request
from starlette.responses import JSONResponse
from authlib.integrations.starlette_client import OAuth

# import 
from app.models import user as UserModel
from app.api.endpoints.user import functions as user_functions
from app.core.settings import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    REDIRECT_URI,
    )
from app.core.settings import (
    REDIRECT_URI, 
    GOOGLE_CLIENT_ID, 
    GOOGLE_CLIENT_SECRET, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    )
from app.schemas.user import Token

social_auth_module = APIRouter()

# google ========================
oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri=REDIRECT_URI,
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
)

# ============================> signin using google <========================
@social_auth_module.get('/auth/google/')
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    print(f"Redirect URI=========================>: {redirect_uri}")
    response = await oauth.google.authorize_redirect(request, redirect_uri)
    return response

@social_auth_module.get('/social/auth/google/callback')
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    # google = oauth.create_client('google')
    # token = await google.authorize_access_token(request)
    if 'id_token' not in token:
        raise HTTPException(status_code=400, detail="Missing id_token in response")
    # user = await oauth.google.parse_id_token(request, token)
    # user_info = await oauth.google.parse_id_token(request, token)
    # ===> no need to parse_id_token. starlet will do parse_id_token automatically. 
    user_info = token['userinfo']
    # Extract user information
    email = user_info['email']
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')
    is_verified = user_info.get('email_verified', False)
    print(f"user info ===================> {user_info}")
    # Check if user already exists
    user = await user_functions.get_user_by_email(email)
    # user = db.query(UserModel.User).filter(UserModel.User.email == email).first()
    if user is None:
        # Create a new user
        user = UserModel.User(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        await user.insert()
    else:
        # Update existing user
        user.first_name = first_name
        user.last_name = last_name
        await user.save()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await user_functions.create_access_token(
    data={"id": user.id, "email": user.email, "role": user.role}, expires_delta=access_token_expires
        )
    
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = await user_functions.create_refresh_token(
        data={"id": user.id, "email": user.email, "role": user.role}, 
        expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

# @auth_module.get('/protected')
# async def protected(user: dict = Depends(oauth.google.authorize_user)):
#     return {'message': 'This is a protected route', 'user': user}