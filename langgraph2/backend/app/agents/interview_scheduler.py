import datetime
from typing import Dict, TypedDict, List

class HiringState(TypedDict):
    """Represents the state of our hiring workflow."""
    candidate: Dict
    screening_result: Dict
    emails_sent: List[Dict]
    final_decision: str
    next_step: str
    history: List

def schedule_interview(state: HiringState) -> HiringState:
    """Schedule interview for qualified candidates."""
    candidate = state["candidate"]
    candidate_name = candidate.get("name", "Candidate")
    candidate_email = candidate.get("email", "candidate@example.com")

    # Calculate next business day
    today = datetime.datetime.now()
    next_day = today + datetime.timedelta(days=1)
    if next_day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        days_to_add = 7 - next_day.weekday()
        next_day = today + datetime.timedelta(days=days_to_add)

    interview_date = next_day.strftime("%A, %B %d, %Y")
    interview_time = "10:00 AM"
    interviewer = candidate.get("interviewer", "HR Manager")
    interviewer_email = candidate.get("interviewer_email", "hr@company.com")

    # Generate email to candidate
    candidate_email_content = f"""
    Subject: Interview Invitation - {candidate.get("position", "Position")}

    Dear {candidate_name},

    We're pleased to inform you that your resume has been selected for the next round of our hiring process for the {candidate.get("position", "Position")} role.

    Your interview has been scheduled for:
    Date: {interview_date}
    Time: {interview_time}
    Location: {candidate.get("interview_location", "Online via Zoom")}

    Please confirm your availability for this time by replying to this email.

    We look forward to speaking with you!

    Best regards,
    {candidate.get("company_name", "Company")} Hiring Team
    """

    # Generate email to interviewer
    interviewer_email_content = f"""
    Subject: Interview Scheduled - {candidate_name} for {candidate.get("position", "Position")}

    Dear {interviewer},

    An interview has been scheduled with {candidate_name} for the {candidate.get("position", "Position")} position.

    Interview details:
    Date: {interview_date}
    Time: {interview_time}
    Candidate Email: {candidate_email}

    The candidate's resume and screening results are attached for your review.

    Thank you,
    Automated Hiring System
    """

    emails = [
        {
            "recipient": candidate_email,
            "subject": f"Interview Invitation - {candidate.get('position', 'Position')}",
            "content": candidate_email_content
        },
        {
            "recipient": interviewer_email,
            "subject": f"Interview Scheduled - {candidate_name}",
            "content": interviewer_email_content
        }
    ]

    new_state = state.copy()
    new_state["emails_sent"] = emails
    new_state["history"].append({
        "agent": "Interview Scheduler",
        "action": "Scheduled interview",
        "result": {
            "interview_date": interview_date,
            "interview_time": interview_time,
            "emails_sent": emails
        }
    })
    new_state["next_step"] = "end"
    
    return new_state 