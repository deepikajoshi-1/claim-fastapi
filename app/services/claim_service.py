from sqlalchemy.orm import Session
from app.models.claims import Claim
import uuid
from app.kafka.producer import publish_event

def create_claim(db: Session, policy_number: str, amount: float):
    claim = Claim(
        policy_number=policy_number,
        amount=amount,
        status="CREATED"
    )
    db.add(claim)
    db.commit()
    db.refresh(claim)

    event = {
        "event_id": str(uuid.uuid4()),
        "claim_id": claim.id,
        "event_type": "CLAIM_CREATED"
    }

    publish_event(topic="claim.created", event=event)
    return claim

def update_claim_status(db: Session, claim_id: int, new_status: str):
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        return None

    claim.status = new_status
    db.commit()
    return claim
