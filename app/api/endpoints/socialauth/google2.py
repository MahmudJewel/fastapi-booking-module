
# ............................................
# ............................................
# No need for this project
#..............................................
# .............................................

# fastapi 
from fastapi import APIRouter, Depends, HTTPException, status, Request as FastAPIRequest
from typing import Annotated
from datetime import timedelta

from fastapi.security import OAuth2AuthorizationCodeBearer
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
# from app.core.dependencies import get_db, oauth2_scheme 
from app.core.settings import REDIRECT_URI, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES
from app.api.endpoints.user import functions as user_functions
from app.schemas.user import Token
import os

social_auth_module = APIRouter()

@social_auth_module.get("/google")
async def google_login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
    )
    authorization_url, state = flow.authorization_url()
    return {"authorization_url": authorization_url}

@social_auth_module.get("/google/callback/")
async def google_callback(request: FastAPIRequest):
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [REDIRECT_URI],
                }
            },
            scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        )
        flow.fetch_token(authorization_response=str(request.url))
        
        credentials = flow.credentials
        id_info = id_token.verify_oauth2_token(credentials.id_token, GoogleRequest(), GOOGLE_CLIENT_ID)
        
        email = id_info.get("email")
        first_name = id_info.get("given_name")
        last_name = id_info.get("family_name")
        
        user = await user_functions.get_user_by_email(email)
        if not user:
            user = await user_functions.create_new_oauth_user(email, first_name, last_name)
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await user_functions.create_access_token(
        data={"id": user.id, "email": user.email, "role": user.role}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
