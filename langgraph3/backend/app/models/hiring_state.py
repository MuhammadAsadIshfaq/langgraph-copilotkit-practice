from typing import Dict, List, TypedDict

class HiringState(TypedDict):
    """Represents the state of our hiring workflow."""
    candidate: Dict
    screening_result: Dict
    emails_sent: List[Dict]
    final_decision: str
    next_step: str
    history: List 