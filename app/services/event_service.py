from sqlalchemy.orm import Session
from app.models import ClaimEvent

def is_duplicate_event(db: Session, event_id: str):
    return db.query(ClaimEvent).filter_by(event_id=event_id).first()
