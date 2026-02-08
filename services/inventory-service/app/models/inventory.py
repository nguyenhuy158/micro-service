import uuid

from app.db.base import Base
from sqlalchemy import UUID, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True
    )
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    reserved_quantity: Mapped[int] = mapped_column(Integer, default=0)
    location: Mapped[str | None] = mapped_column(String, nullable=True)

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.reserved_quantity
