from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class ClaimEvent(Base):
    __tablename__ = "claim_events"

    event_id = Column(String, primary_key=True)
    claim_id = Column(String, nullable=False)
    event_type = Column(String, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    