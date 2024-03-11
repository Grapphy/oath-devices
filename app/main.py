import uvicorn
from fastapi import FastAPI

from routers import users, auth


app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    print("Navigate the url: http://localhost:8000/docs for Swagger docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)