from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader, APIKeyQuery, APIKeyCookie, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import check_api_key,check_expiry

db = SessionLocal()

API_KEY_NAME = "api_key"
COOKIE_DOMAIN = "localhost"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header)
):
    
    if check_api_key(db, api_key_query):
        api_key = api_key_query
    elif check_api_key(db, api_key_header):
        api_key = api_key_header
    
    else:
        print("***********************************")

        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="User not Found"
        )
    if check_expiry(db, api_key):
        return api_key
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="API key has expired"
        )
