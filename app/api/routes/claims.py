from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schema.claim import ClaimCreate
from app.services.claim_service import create_claim, update_claim_status
from app.api.dependencies import require_role

router = APIRouter(prefix="/claims", tags=["Claims"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", dependencies=[Depends(require_role(["ADJUSTER"]))])
def create(claim: ClaimCreate,db: Session = Depends(get_db)):
    return create_claim(db, claim.policy_number, claim.amount)

@router.put(
    "/{claim_id}/validate",
    dependencies=[Depends(require_role(["ADJUSTER"]))]
)
def validate_claim(claim_id: int, db: Session = Depends(get_db)):
    updated = update_claim_status(db, claim_id, "VALIDATED")
    if not updated:
        raise HTTPException(404)
    return updated

@router.put(
    "/{claim_id}/approve",
    dependencies=[Depends(require_role(["ADMIN"]))]
)
def approve_claim(claim_id: int, db: Session = Depends(get_db)):
    return update_claim_status(db, claim_id, "APPROVED")

@router.get("/")
def list_claims(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    claims = (
        db.query(claims.Claim)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return claims
