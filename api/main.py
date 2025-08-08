from dotenv import load_dotenv
load_dotenv()
import os

import firebase_admin
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoints.v1.users import router as user_router
from endpoints.v1.feeds import router as feed_router
from endpoints.v1.follows import router as follow_router
from endpoints.v1.posts import router as post_router
from graphql_api.graphql import graphql_router


app = FastAPI()


app.include_router(user_router)
app.include_router(feed_router)
app.include_router(follow_router)
app.include_router(post_router)
app.include_router(graphql_router, prefix="/graphql")


origins = [
    f"{os.getenv('CLIENT_ORIGIN')}",
]


# Initialize FastAPI CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Initialize Firebase SDK
cred = firebase_admin.credentials.Certificate(f"secrets/{os.getenv('FIREBASE_CREDENTIALS_PATH')}")
firebase_admin.initialize_app(cred)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=os.getenv("APP_PORT"))