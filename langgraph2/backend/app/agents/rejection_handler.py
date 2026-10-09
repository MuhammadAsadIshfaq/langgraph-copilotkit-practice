from typing import Dict, TypedDict, List

class HiringState(TypedDict):
    """Represents the state of our hiring workflow."""
    candidate: Dict
    screening_result: Dict
    emails_sent: List[Dict]
    final_decision: str
    next_step: str
    history: List

def send_rejection(state: HiringState) -> HiringState:
    """Send rejection email to unqualified candidates."""
    candidate = state["candidate"]
    candidate_name = candidate.get("name", "Candidate")
    candidate_email = candidate.get("email", "candidate@example.com")
    screening_result = state["screening_result"]

    # Generate rejection email
    rejection_email_content = f"""
    Subject: Application Status - {candidate.get("position", "Position")}

    Dear {candidate_name},

    Thank you for your interest in the {candidate.get("position", "Position")} position at {candidate.get("company_name", "our company")}.

    After careful review of your application, we regret to inform you that we have decided to move forward with other candidates whose qualifications more closely match our current needs.

    We appreciate your interest in joining our team and wish you success in your job search.

    Best regards,
    {candidate.get("company_name", "Company")} Hiring Team
    """

    emails = [
        {
            "recipient": candidate_email,
            "subject": f"Application Status - {candidate.get('position', 'Position')}",
            "content": rejection_email_content
        }
    ]

    new_state = state.copy()
    new_state["emails_sent"] = emails
    new_state["history"].append({
        "agent": "Rejection Handler",
        "action": "Sent rejection email",
        "result": {
            "email_sent": emails[0]
        }
    })
    new_state["next_step"] = "end"
    
    return new_state 