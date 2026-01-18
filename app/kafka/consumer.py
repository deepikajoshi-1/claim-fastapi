from kafka import KafkaConsumer
import json
from sqlalchemy.orm import Session
from app.models.claim_event import ClaimEvent
from app.services.claim_service import update_claim_status
from app.db.session import SessionLocal
from app.services.event_service import handle_event

consumer = KafkaConsumer(
    "claim.created",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=False
)

for message in consumer:
    db = SessionLocal()
    try:
        handle_event(message.value, db)
        db.commit()
        consumer.commit()
    except Exception as e:
        db.rollback()
        # retry / DLQ later
        raise
    finally:
        db.close()