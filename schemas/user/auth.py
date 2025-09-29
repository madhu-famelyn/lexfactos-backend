from pydantic import BaseModel, EmailStr

# ----------- Login Schema -----------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ----------- Token Response -----------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
