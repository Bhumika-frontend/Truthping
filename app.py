import streamlit as st
import re
from deep_translator import GoogleTranslator
from langdetect import detect

# ------------------ Language Processor ------------------
def detect_language(text):
    try:
        lang = detect(text)
        return lang if lang in ['hi', 'ta', 'bn', 'mr', 'te', 'gu', 'kn', 'ml', 'pa', 'ur'] else 'en'
    except:
        return 'en'

def translate_to_english(text, source_lang='auto'):
    try:
        if source_lang == 'auto':
            source_lang = detect_language(text)
        if source_lang != 'en':
            return GoogleTranslator(source=source_lang, target='en').translate(text)
        return text
    except:
        return text

def translate_response(text, target_lang):
    if target_lang == 'en':
        return text
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except:
        return text

# ------------------ Fact Checker ------------------
common_myths = {
    "corona vaccine causes infertility": {
        "verdict": "False",
        "explanation": "This is false. WHO confirms COVID-19 vaccines are safe and do not affect fertility.",
        "source": "World Health Organization"
    },
    "free government smartphone scheme": {
        "verdict": "False",
        "explanation": "No such nationwide scheme exists. Verify only on official government websites (gov.in).",
        "source": "PIB Fact Check"
    },
    "kbc lottery winner 25 lakhs": {
        "verdict": "Scam",
        "explanation": "This is a well-known scam. KBC never asks for money or personal details via WhatsApp.",
        "source": "Cyber Crime Cell"
    },
    "work from home job earn 50000 per month": {
        "verdict": "Suspicious",
        "explanation": "Legitimate companies do not offer high salaries without interview/background check. Be careful.",
        "source": "Local Database"
    }
}

fake_patterns = [
    "earn money from home without investment",
    "government giving free smartphones",
    "lottery winner in your area",
    "kbc lucky winner number",
    "part time job no experience",
    "आधार कार्ड से पैसे",
    "free recharges"
]

def check_local_db(claim):
    claim_lower = claim.lower()
    for myth, result in common_myths.items():
        if myth.lower() in claim_lower or claim_lower in myth.lower():
            return result
    for pattern in fake_patterns:
        if pattern.lower() in claim_lower:
            return {
                "verdict": "Suspicious",
                "explanation": f"This matches a known scam/fake pattern: '{pattern}'. Be very cautious.",
                "source": "Local Database"
            }
    return None

def verify_claim(claim, source_lang='hi'):
    local_result = check_local_db(claim)
    if local_result:
        return {
            'verified': local_result['verdict'],
            'explanation': local_result['explanation'],
            'source': local_result.get('source', 'Local Database'),
            'confidence': 'high'
        }

    scam_words = ['free', 'lottery', 'winner', 'urgent', 'click', 'register', 'फ्री', 'लॉटरी', 'जीत', 'तुरंत']
    score = sum(1 for w in scam_words if w in claim.lower())
    if score >= 2:
        return {
            'verified': 'Suspicious',
            'explanation': 'This message contains multiple indicators typical of scams or misinformation. Verify through official channels.',
            'source': 'AI Heuristics',
            'confidence': 'medium'
        }

    return {
        'verified': 'Unknown',
        'explanation': 'No immediate match found in our database. Please cross-check with trusted sources like PIB Fact Check or official government websites.',
        'source': 'System',
        'confidence': 'low'
    }

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="TruthPing - WhatsApp Fact Checker", page_icon="🔍", layout="centered")

st.title("📱 TruthPing")
st.caption("Verify suspicious WhatsApp messages in your own language")

lang_options = {
    'hi': 'हिन्दी (Hindi)',
    'ta': 'தமிழ் (Tamil)',
    'bn': 'বাংলা (Bengali)',
    'mr': 'मराठी (Marathi)',
    'te': 'తెలుగు (Telugu)',
    'en': 'English'
}
selected_lang = st.selectbox("Select your language", options=list(lang_options.keys()), format_func=lambda x: lang_options[x])

user_message = st.text_area("Paste or type the suspicious message here:", height=150)

if st.button("🔍 Verify Now", type="primary"):
    if user_message.strip():
        with st.spinner("Checking..."):
            english_claim = translate_to_english(user_message, selected_lang)
            result = verify_claim(english_claim, selected_lang)
            
            if selected_lang != 'en':
                result['explanation'] = translate_response(result['explanation'], selected_lang)
            
            if result['verified'] == 'False':
                emoji = "❌"
            elif result['verified'] in ['Suspicious', 'Scam']:
                emoji = "⚠️"
            elif result['verified'] == 'Unknown':
                emoji = "❓"
            else:
                emoji = "✅"
            
            st.markdown(f"### {emoji} Verdict: {result['verified']}")
            st.markdown(f"**📝 Explanation:** {result['explanation']}")
            st.markdown(f"**📌 Source:** {result['source']}")
            st.markdown(f"**🎯 Confidence:** {result['confidence']}")
    else:
        st.warning("Please enter a message to verify.")

with st.expander("📋 Try these examples"):
    st.markdown("- *Free government smartphone scheme! Click here to claim your phone*")
    st.markdown("- *KBC lottery winner 2024 – You won 25 lakhs! Send 500 INR for processing*")
    st.markdown("- *Work from home job, earn 50,000 per month without investment*")
    st.markdown("- *Corona vaccine causes infertility – don’t take it*")

st.caption("🔒 Works in Hindi, Tamil, Bengali, Marathi, Telugu, and more. No app switching required.")