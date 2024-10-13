from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class UserCreate(BaseModel):
    name_empresa: Annotated[str, Field(description="Nome da Empresa", example="Dom Dino", min_length=3)]  
    email: Annotated[EmailStr, Field(description="Email da Empresa", example="Example@example.com")]  
    password: Annotated[str, Field(description="Senha da Empresa", example="123456",min_length=6)]  

class UserResponse(BaseModel):
    name_empresa: Annotated[str, Field(description="Nome da Empresa", example="Dom Dino", min_length=3)] 
    email: Annotated[EmailStr, Field(description="Email da Empresa", example="Example@example.com")]  

class UserLogin(BaseModel):
    email: Annotated[EmailStr, Field(description="Email da Empresa", example="Example@example.com")]
    password: Annotated[str, Field(description="Senha da Empresa", example="123456",min_length=6)]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    exp: str

