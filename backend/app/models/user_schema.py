from pydantic import BaseModel, EmailStr, Field

class UserSignup(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=120)

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        # allows to show from ORM
        from_attributes = True