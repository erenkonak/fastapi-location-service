from fastapi import APIRouter
from pydantic import BaseModel
from app.services.mail_receiver_service import read_unseen_emails, mark_email_as_seen_by_subject

router = APIRouter()

class MarkSeenRequest(BaseModel):
    subject: str

@router.get("/read-emails")
async def get_unseen_emails():
    try:
        emails = read_unseen_emails()
        return {"emails": emails}
    except Exception as e:
        return {"error": str(e)}
    


@router.post("/mark-email-seen")
async def mark_email_seen(data: MarkSeenRequest):
    try:
        result = mark_email_as_seen_by_subject(data.subject)
        return {"message": result}
    except Exception as e:
        return {"error": str(e)}