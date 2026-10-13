import logging
import smtplib
from email.message import EmailMessage

from ExchangeListGenerator import Participant

GMAIL_EMAIL: str = 'quique2.0.1@gmail.com'
GMAIL_PASSWORD: str = 'owrq eykw zmde rvlm'  # Gmail App Password, not the account password
EMAIL_SUBJECT: str = 'Intercambio'
EMAIL_FROM: str = 'Héctor Díaz <quique2.0.1@gmail.com>'

SMTP_HOST: str = 'smtp.gmail.com'
SMTP_PORT: int = 465

logger = logging.getLogger(__name__)


def send_email(participant: Participant) -> bool:
    message = EmailMessage()
    message['Subject'] = EMAIL_SUBJECT
    message['From'] = EMAIL_FROM or GMAIL_EMAIL
    message['To'] = participant.email
    message.set_content(f'Hola {participant.name}, te toca regalarle a: '
                        f'{participant.matched_participant and participant.matched_participant.name}')

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.login(GMAIL_EMAIL, GMAIL_PASSWORD)
            smtp.send_message(message)
    except (smtplib.SMTPException, OSError) as e:
        logger.error(f'Failed to send email to {participant.name} | {participant.email}: {e}')
        return False

    logger.info(f'Email sent successfully to {participant.name} | {participant.email}')
    return True
