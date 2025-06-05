from fastapi import APIRouter
from pydantic import BaseModel
from app.services.mail_service import send_email

router = APIRouter()

class MailRequest(BaseModel):
    receiver_email: str
    subject: str
    body: str
    pdf_path: str  # full path of the PDF to attach

@router.post("/send-mail")
async def send_mail_endpoint(mail: MailRequest):
    try:
        send_email(
            receiver_email=mail.receiver_email,
            subject=mail.subject,
            body=mail.body,
            pdf_path=mail.pdf_path
        )
        return {"message": "Email sent successfully"}
    except Exception as e:
        return {"error": str(e)}