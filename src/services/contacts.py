from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.auth import User


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def get_contacts(self, limit: int, offset: int, user: User):
        return await self.contact_repository.get_contacts(limit, offset, user)

    async def get_contact_by_id(self, id: int, user: User):
        return await self.contact_repository.get_contact_by_id(id, user)

    async def search_contacts(self, field: str, user: User):
        return await self.contact_repository.search_contacts(field, user)

    async def create_contact(self, contact, user: User):
        return await self.contact_repository.create_contact(contact, user)

    async def update_contact(self, id: int, body, user: User):
        return await self.contact_repository.update_contact(id, body, user)

    async def delete_contact(self, id: int, user: User):
        return await self.contact_repository.delete_contact(id, user)

    async def get_upcoming_birthdays(
        self,
        user: User,
        limit: int,
    ):
        return await self.contact_repository.get_upcoming_birthdays(user, limit)
