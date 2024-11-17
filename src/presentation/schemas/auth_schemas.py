from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: int | None = None
    
class TokenData(BaseModel):
    email: str | None = None

class Login(BaseModel):
    email: EmailStr
    password: str