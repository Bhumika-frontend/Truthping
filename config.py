import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Twilio (optional – for real WhatsApp webhook)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

    # Supported Indian languages
    SUPPORTED_LANGUAGES = {
        'hi': 'Hindi',
        'ta': 'Tamil',
        'bn': 'Bengali',
        'mr': 'Marathi',
        'te': 'Telugu',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'ur': 'Urdu'
    }