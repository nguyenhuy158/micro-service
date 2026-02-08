import uuid
from sqlalchemy import Column, Integer, String, UUID, ForeignKey
from app.db.base import Base


class Inventory(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    quantity = Column(Integer, default=0)
    reserved_quantity = Column(Integer, default=0)
    location = Column(String, nullable=True)

    @property
    def available_quantity(self) -> int:
        return self.quantity - self.reserved_quantity
