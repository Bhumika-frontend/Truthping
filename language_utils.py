from deep_translator import GoogleTranslator
from langdetect import detect
import re

class LanguageProcessor:
    @staticmethod
    def detect_language(text):
        try:
            lang = detect(text)
            return lang if lang in ['hi', 'ta', 'bn', 'mr', 'te', 'gu', 'kn', 'ml', 'pa', 'ur'] else 'en'
        except:
            return 'en'

    @staticmethod
    def translate_to_english(text, source_lang='auto'):
        try:
            if source_lang == 'auto':
                source_lang = LanguageProcessor.detect_language(text)
            if source_lang != 'en':
                return GoogleTranslator(source=source_lang, target='en').translate(text)
            return text
        except:
            return text

    @staticmethod
    def translate_response(text, target_lang):
        if target_lang == 'en':
            return text
        try:
            return GoogleTranslator(source='en', target=target_lang).translate(text)
        except:
            return text

    @staticmethod
    def extract_claim(text):
        # Remove common prefixes
        prefixes = ['check this', 'is this true', 'verify', 'सच', 'झूठ', 'सत्यापित', 'fact check']
        for p in prefixes:
            if text.lower().startswith(p):
                text = text[len(p):]
        # Extract URL if present
        url_match = re.search(r'https?://[^\s]+', text)
        if url_match:
            return {'type': 'url', 'content': url_match.group(0)}
        return {'type': 'claim', 'content': text.strip()[:500]}