import os
import logging
from typing import Annotated, Sequence, TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from ..models.hiring_state import HiringState

logger = logging.getLogger(__name__)

THRESHOLD_SCORE = 75

class ScreeningResult(BaseModel):
    qualified: bool = Field(description="Whether the candidate is qualified for the position")
    overall_score: float = Field(description="Overall score from 0 to 100")
    strengths: list[str] = Field(description="List of candidate's strengths")
    gaps: list[str] = Field(description="List of candidate's gaps or areas for improvement")
    recommendation: str = Field(description="Detailed recommendation for next steps")

def create_screener_agent(groq_api_key: str):
    logger.info("Creating resume screener agent")
    
    # Initialize the LLM
    llm = ChatGroq(
        api_key=os.environ.get("GROQ_API_KEY"),
        model_name="mixtral-8x7b-32768",
        temperature=0.1
    )
    logger.info("LLM initialized")

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert HR professional and technical recruiter. Your task is to screen resumes and provide detailed analysis.
        
        Analyze the candidate's resume and the job description to determine if they are qualified for the position.
        Consider the following aspects:
        1. Technical skills and experience
        2. Education and certifications
        3. Relevant projects and achievements
        4. Years of experience
        5. Industry knowledge
        
        Provide a detailed analysis with:
        - Overall qualification decision (qualified/not qualified)
        - Score from 0-100
        - Key strengths
        - Areas of concern or gaps
        - Detailed recommendation for next steps
        
        Be specific and provide evidence from the resume to support your analysis."""),
        MessagesPlaceholder(variable_name="history"),
        ("human", """Candidate Information:
        Name: {name}
        Position: {position}
        Company: {company_name}
        
        Job Description:
        {job_description}
        
        Resume:
        {resume_text}
        
        Please analyze this candidate's qualifications for the position.""")
    ])
    logger.info("Prompt template created")

    # Create the output parser
    parser = JsonOutputParser(pydantic_object=ScreeningResult)
    logger.info("Output parser created")

    def screen_resume(state):
        logger.info("Starting resume screening")
        try:
            # Get candidate info from state
            candidate = state["candidate"]
            logger.info(f"Screening resume for {candidate['name']}")
            
            # Format the prompt
            messages = prompt.format_messages(
                name=candidate["name"],
                position=candidate["position"],
                company_name=candidate["company_name"],
                job_description=candidate["job_description"],
                resume_text=candidate["resume_text"],
                history=state.get("history", [])
            )
            logger.info("Prompt formatted")

            # Get response from LLM
            logger.info("Sending request to LLM")
            response = llm.invoke(messages)
            logger.info("Received response from LLM")

            # Parse the response
            logger.info("Parsing LLM response")
            result = parser.parse(response.content)
            logger.info(f"Screening result: {result}")

            # Update state
            state["screening_result"] = result.dict()
            state["history"].extend([
                HumanMessage(content=f"Please analyze this candidate's qualifications for the {candidate['position']} position at {candidate['company_name']}."),
                AIMessage(content=response.content)
            ])
            
            # Determine next step
            if result.qualified:
                state["next_step"] = "schedule_interview"
                state["final_decision"] = "Candidate is qualified. Proceeding with interview scheduling."
            else:
                state["next_step"] = "send_rejection"
                state["final_decision"] = "Candidate is not qualified. Sending rejection email."
            
            logger.info(f"Next step determined: {state['next_step']}")
            return state
            
        except Exception as e:
            logger.error(f"Error in resume screening: {str(e)}", exc_info=True)
            raise

    return screen_resume 