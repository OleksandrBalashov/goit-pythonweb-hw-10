from typing import List, Literal, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.contacts import ContactService
from src.database.db import get_db
from src.schemas.schemas import ContactBase, ContactResponse, ContactUpdate
from src.schemas.auth import User
from src.services.auth import get_current_user


router = APIRouter(prefix="/contacts", tags=["contacts"])

SearchField = Literal["email", "name", "last_name"]


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(limit, offset, user)
    return contacts


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    db: AsyncSession = Depends(get_db),
    email: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    user: User = Depends(get_current_user)
):
    filters = {"email": email, "name": name, "last_name": last_name}
    if not any(filters.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one search filter must be provided",
        )

    contact_service = ContactService(db)
    contacts = await contact_service.search_contacts(filters, user)
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: AsyncSession = Depends(get_db),  user: User = Depends(get_current_user)):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body, user)


@router.get("/birthdays", response_model=List[ContactResponse])
async def get_upcoming_birthdays(limit: int = 100, db: AsyncSession = Depends(get_db),  user: User = Depends(get_current_user)):
    contact_service = ContactService(db)
    contacts = await contact_service.get_upcoming_birthdays(user, limit)
    return contacts


@router.get("/{id}", response_model=ContactResponse)
async def get_contact(id: int, db: AsyncSession = Depends(get_db),  user: User = Depends(get_current_user)):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact_by_id(id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.put("/{id}", response_model=ContactResponse)
async def update_contact(
    body: ContactUpdate, id: int, db: AsyncSession = Depends(get_db),  user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(id, body, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return contact


@router.delete("/{id}", response_model=ContactResponse)
async def delete_contact(id: int, db: AsyncSession = Depends(get_db),  user: User = Depends(get_current_user)):
    contact_service = ContactService(db)
    contact = await contact_service.delete_contact(id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact
