from pydantic import BaseModel
from datetime import date
from typing import Optional


class ContactBase(BaseModel):
    name: str
    last_name: str
    email: str
    phone: str
    birthday: Optional[date] = None
    additional_data: Optional[str] = None


class ContactResponse(ContactBase):
    id: int


class ContactUpdate(ContactBase):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class ContactSearchParams(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    last_name: Optional[str] = None


class Contact(ContactBase):
    id: int

    class Config:
        from_attributes = True
