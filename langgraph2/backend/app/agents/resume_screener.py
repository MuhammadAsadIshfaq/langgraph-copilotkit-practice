import json
from typing import Dict, TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import os

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY", "")
)

THRESHOLD_SCORE = 75

class HiringState(TypedDict):
    """Represents the state of our hiring workflow."""
    candidate: Dict
    screening_result: Dict
    emails_sent: List[Dict]
    final_decision: str
    next_step: str
    history: List

def screen_resume(state: HiringState) -> HiringState:
    """Screen a candidate's resume for job fit."""
    candidate = state["candidate"]
    job = candidate.get("job_description", "")
    resume = candidate.get("resume_text", "")

    prompt = f"""
    You are a Resume Screening Agent. Your task is to evaluate if a candidate is suitable for a job based on their resume.

    JOB DESCRIPTION:
    {job}

    CANDIDATE RESUME:
    {resume}

    Please analyze the resume against the job requirements and provide a detailed assessment.
    Return your analysis as JSON with the following fields:
    - qualified: Boolean (true/false) indicating if the candidate meets basic qualifications
    - overall_score: Integer from 0-100 indicating overall fit
    - strengths: List of the candidate's strengths relevant to the position
    - gaps: List of areas where the candidate falls short
    - recommendation: String with a brief recommendation of why the candidate should or should not proceed
    """

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)

    try:
        result_text = response.content
        start_idx = result_text.find('{')
        end_idx = result_text.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = result_text[start_idx:end_idx]
            result = json.loads(json_str)
        else:
            raise ValueError("No valid JSON found in response")
    except Exception as e:
        print(f"Error parsing JSON response: {e}")
        result = {
            "qualified": False,
            "overall_score": 0,
            "strengths": [],
            "gaps": ["Failed to properly analyze resume"],
            "recommendation": "Unable to analyze resume properly"
        }

    new_state = state.copy()
    new_state["screening_result"] = result
    new_state["history"].append({"agent": "Resume Screener", "action": "Screened resume", "result": result})

    if result.get("overall_score", 0) >= THRESHOLD_SCORE:
        new_state["next_step"] = "schedule_interview"
        new_state["final_decision"] = "Proceed to interview"
    else:
        new_state["next_step"] = "send_rejection"
        new_state["final_decision"] = "Rejected based on resume screening"

    return new_state 