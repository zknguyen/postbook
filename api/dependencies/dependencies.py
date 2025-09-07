# dependencies.py
from fastapi import HTTPException, Request
from firebase_admin import auth
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        # return decoded_token  # This contains uid, email, etc.
        print(f"Token verified: {decoded_token}")
        return token
    except (InvalidIdTokenError, ExpiredIdTokenError) as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")
