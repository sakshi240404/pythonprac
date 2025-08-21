from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

# Basic Auth Scheme
security = HTTPBasic()

# Hardcoded credetials (for demo)
USERNAME = "sakshi"
PASSWORD = "mypassword"

@app.get("/")
def public():
    return {"message":"This is a public endpoint"}

@app.get("/secure")
def secure(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == USERNAME and credentials.password == PASSWORD:
        return{"message":f"Welcome {credentials.username}!"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Username or Password",
        headers={"WWW_Authenticate":"Basic"},
    )
