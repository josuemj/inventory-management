import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)
    supabase_user_id: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True), unique=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, server_default="now()")

    organization = relationship("Organization", back_populates="users")
    inventory_movements = relationship("InventoryMovement", back_populates="user")
    change_logs = relationship("ChangeLog", back_populates="user")
