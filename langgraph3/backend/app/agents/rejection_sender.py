from ..models.hiring_state import HiringState

def send_rejection(state: HiringState) -> HiringState:
    """Send rejection email to candidate."""
    candidate = state["candidate"]
    candidate_name = candidate.get("name", "Candidate")
    candidate_email = candidate.get("email", "candidate@example.com")

    rejection_email_content = f"""
    Subject: Regarding Your Application for {candidate.get("position", "Position")}

    Dear {candidate_name},

    Thank you for your interest in the {candidate.get("position", "Position")} role at {candidate.get("company_name", "Company")}.

    After careful consideration of your application, we regret to inform you that we will not be moving forward with your candidacy at this time.

    We appreciate the time you took to apply and wish you the best in your job search.

    Sincerely,
    {candidate.get("company_name", "Company")} Hiring Team
    """

    emails = [
        {
            "recipient": candidate_email,
            "subject": f"Regarding Your Application for {candidate.get('position', 'Position')}",
            "content": rejection_email_content
        }
    ]

    new_state = state.copy()
    new_state["emails_sent"] = emails
    new_state["history"].append({
        "agent": "Rejection Notifier",
        "action": "Sent rejection email"
    })
    new_state["next_step"] = "end"

    return new_state 