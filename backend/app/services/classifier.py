import re
from typing import Tuple, Optional

KEYMAP = {
    "Transporte": [r"\buber\b", r"\b99\b", r"\bcabify\b"],
    "Mercado": [r"\b(supermercado|market|carrefour|extra|bompre[cç]o)\b"],
    "Lazer": [r"\b(spotify|netflix|prime\s?video|cinema)\b"],
    "Alimentação": [r"\b(restaurante|ifood|mcdonald'?s?|burg(er)?\s?king)\b"],
    "Saúde": [r"\b(farm[aá]cia|drogasil|drogaria|wellhub|gympass)\b"],
    "Serviços": [r"\b(icloud|google\s?drive|github|aws|render|vercel)\b"],
}

class Classifier:
    def predict_one(self, description: Optional[str]) -> Tuple[Optional[str], float]:
        if not description:
            return (None, 0.0)
        desc = description.lower()
        best_cat, best_score = None, 0
        for cat, patterns in KEYMAP.items():
            score = sum(1 for p in patterns in re.search(p, desc))
            if score > best_score:
                best_cat, best_score = cat, score
            if best_score == 0:
                return (None, 0.0)
            conf = min(1.0, best_score / 3.0)
            return (best_cat, conf)
