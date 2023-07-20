import uuid
from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    tenant_name: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    email_verified: bool
    tenant_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
