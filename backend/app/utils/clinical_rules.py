from datetime import datetime
import re

def calculate_recency_score(source: dict) -> float:
    date_str = source.get("last_updated") or source.get("last_filled")
    if not date_str:
        return 0.3
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        days_old = (datetime.now() - dt).days
        return max(0.1, 1.0 - (days_old / 365))
    except:
        return 0.5

def is_plausible_bp(bp: str) -> bool:
    if not bp:
        return True
    match = re.match(r"(\d+)/(\d+)", bp)
    if not match:
        return False
    sys, dia = int(match.group(1)), int(match.group(2))
    return 70 <= sys <= 220 and 40 <= dia <= 140

def adjust_for_egfr(med: str, egfr: float) -> str:
    if "metformin" in med.lower() and egfr < 60:
        return med.replace("1000mg", "500mg").replace("twice daily", "twice daily")  # example rule
    return med