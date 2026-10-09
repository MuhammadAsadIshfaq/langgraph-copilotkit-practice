from typing import Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

class EmailCommunicationAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

    async def send_email(self, to_email: str, subject: str, content: str) -> Dict[str, Any]:
        """
        Send an email to a candidate.
        
        Args:
            to_email: Candidate's email address
            subject: Email subject
            content: Email content
            
        Returns:
            Dict containing email sending status
        """
        try:
            # Create email message
            msg = MIMEMultipart()
            msg["From"] = "hiring@company.com"
            msg["To"] = to_email
            msg["Subject"] = subject
            
            # Add content
            msg.attach(MIMEText(content, "plain"))
            
            # Send email (Note: In production, you'd want to use proper email server configuration)
            with smtplib.SMTP('localhost', 25) as server:
                server.send_message(msg)
            
            return {"status": "success", "message": "Email sent successfully"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def generate_email_content(self, template_type: str, candidate_info: Dict[str, Any]) -> str:
        """
        Generate email content based on template type and candidate information.
        
        Args:
            template_type: Type of email template (e.g., "initial_contact", "interview_scheduled")
            candidate_info: Dictionary containing candidate information
            
        Returns:
            Generated email content
        """
        prompt = f"""
        Generate a professional email for a hiring workflow.
        Template Type: {template_type}
        Candidate Information: {candidate_info}
        
        Please create a warm and professional email that follows best practices for hiring communications.
        """
        
        response = await self.llm.agenerate([HumanMessage(content=prompt)])
        return response.generations[0][0].text
