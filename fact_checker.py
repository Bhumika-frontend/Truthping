import json
import re

class FactChecker:
    def __init__(self):
        self.common_myths = {
            "corona vaccine causes infertility": {
                "verdict": "False",
                "explanation": "False. WHO confirms COVID-19 vaccines are safe.",
                "source": "WHO"
            },
            "free government smartphone scheme": {
                "verdict": "False",
                "explanation": "No such scheme. Verify on gov.in.",
                "source": "PIB"
            },
            "kbc lottery winner": {
                "verdict": "Scam",
                "explanation": "Fake lottery scam. KBC never asks for money.",
                "source": "Cyber Cell"
            }
        }
        self.fake_patterns = [
            "earn money from home", "lottery winner", 
            "free smartphone", "kbc lucky winner"
        ]

    def check_local_db(self, claim):
        claim_lower = claim.lower()
        for myth, res in self.common_myths.items():
            if myth in claim_lower:
                return res
        for pat in self.fake_patterns:
            if pat in claim_lower:
                return {
                    "verdict": "Suspicious",
                    "explanation": f"Matches scam pattern: {pat}",
                    "source": "Database"
                }
        return None

    def verify_claim(self, claim, source_lang='hi', api_keys=None):
        local = self.check_local_db(claim)
        if local:
            return {**local, 'confidence': 'high'}
        
        scam_words = ['free','lottery','winner','urgent','click','register','discount','फ्री','लॉटरी']
        if sum(1 for w in scam_words if w in claim.lower()) >= 2:
            return {
                'verified': 'Suspicious',
                'explanation': 'Multiple scam indicators. Be careful.',
                'source': 'Heuristics',
                'confidence': 'medium'
            }
        return {
            'verified': 'Unknown',
            'explanation': 'Not in database. Check official sources.',
            'source': 'System',
            'confidence': 'low'
        }