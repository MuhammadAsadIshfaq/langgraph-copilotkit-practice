from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
import PyPDF2
import docx
import mammoth
import io

class ResumeScreeningAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

    async def process_resume(self, file_path: str, job_description: str, threshold_score: int) -> Dict[str, Any]:
        """
        Process a resume file and screen it against the job description.
        
        Args:
            file_path: Path to the resume file
            job_description: Job description text
            threshold_score: Minimum score threshold
            
        Returns:
            Dict containing screening results
        """
        # Extract text from resume based on file type
        resume_text = await self._extract_text_from_file(file_path)
        
        # Create prompt for resume screening
        prompt = f"""
        You are a resume screening assistant. Please analyze the following resume and job description:
        
        Job Description:
        {job_description}
        
        Resume:
        {resume_text}
        
        Please provide a score (0-100) indicating how well the candidate matches the job requirements.
        Also provide a detailed analysis of their qualifications and any relevant experience.
        """
        
        # Get LLM response
        response = await self.llm.agenerate([HumanMessage(content=prompt)])
        
        # Parse response
        screening_result = self._parse_screening_response(response)
        
        # Add threshold check
        screening_result["meets_threshold"] = screening_result["score"] >= threshold_score
        
        return screening_result

    async def _extract_text_from_file(self, file_path: str) -> str:
        """Extract text from different file types (PDF, DOCX, etc.)"""
        _, ext = os.path.splitext(file_path)
        
        if ext.lower() == ".pdf":
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = " ".join(page.extract_text() for page in reader.pages)
                return text
        
        elif ext.lower() == ".docx":
            doc = docx.Document(file_path)
            return " ".join(paragraph.text for paragraph in doc.paragraphs)
        
        elif ext.lower() == ".doc":
            with open(file_path, 'rb') as file:
                result = mammoth.convert_to_text(file)
                return result.value
        
        raise ValueError(f"Unsupported file type: {ext}")

    def _parse_screening_response(self, response) -> Dict[str, Any]:
        """Parse the LLM response into a structured format"""
        # This is a simplified parser - in production you'd want a more robust implementation
        content = response.generations[0][0].text
        
        # Extract score
        score = 0
        for line in content.split('\n'):
            if "score" in line.lower():
                try:
                    score = int(line.split()[0])
                    break
                except:
                    continue
        
        return {
            "score": score,
            "analysis": content,
            "meets_threshold": False
        }
