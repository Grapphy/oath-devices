import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import users, auth


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    print("Navigate the url: http://localhost:8000/docs for Swagger docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)