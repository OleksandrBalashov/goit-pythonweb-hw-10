from pydantic import BaseModel, Field, ConfigDict, EmailStr


class User(BaseModel):
    id: int
    username: str = Field(min_length=2, max_length=50, description="Username")
    email: EmailStr
    avatar: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(User):
    password: str = Field(min_length=6, max_length=12, description="Password")
