import uuid
from sqlalchemy import Column, Float, String, UUID, Enum as SQLEnum
from app.db.base import Base
from shared.enums.status import PaymentStatus


class Payment(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    amount = Column(Float, nullable=False)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    transaction_id = Column(String, nullable=True)
    provider = Column(String, default="mock")
