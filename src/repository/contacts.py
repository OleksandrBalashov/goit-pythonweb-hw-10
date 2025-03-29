from datetime import datetime, timedelta
from typing import Dict, Literal, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas.auth import User


from src.database.models import Contact
from src.schemas.schemas import ContactBase, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contact_by_id(self, id: int, user: User) -> Contact | None:
        stmt = select(Contact).filter_by(id=id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def search_contacts(
        self,
        filters: Optional[Dict[str, str]],
        user: User,
    ) -> Sequence[Contact]:
        stmt = select(Contact)

        for field, value in filters.items():
            if value:
                stmt = stmt.where(getattr(Contact, field).ilike(f"%{value}%"))

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_contacts(
        self, limit: int, offset: int, user: User
    ) -> Sequence[Contact]:
        stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
        contacts = await self.db.execute(stmt)
        return list(contacts.scalars().all())

    async def create_contact(self, contact: ContactBase, user: User) -> Contact:
        new_contact = Contact(**contact.model_dump(exclude_unset=True), user=user)
        self.db.add(new_contact)
        await self.db.commit()
        await self.db.refresh(new_contact)
        return new_contact

    async def update_contact(
        self, id: int, body: ContactUpdate, user: User
    ) -> Contact | None:
        contact = await self.get_contact_by_id(id, user)
        if contact:
            contact.name = body.name
            contact.last_name = body.last_name
            contact.email = body.email
            contact.phone = body.phone
            contact.birthday = body.birthday
            contact.additional_data = body.additional_data

            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def delete_contact(self, id: int, user: User) -> Contact:
        contact = await self.get_contact_by_id(id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthdays(self, user: User, limit: int = 100):
        today = datetime.today().date()
        seven_days_later = today + timedelta(days=7)

        stmt = (
            select(Contact)
            .filter_by(user=user)
            .filter(Contact.birthday >= today)
            .filter(Contact.birthday <= seven_days_later)
            .order_by(Contact.birthday)
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()
