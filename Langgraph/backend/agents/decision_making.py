from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

class DecisionMakingAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

    async def make_decision(self, candidate_info: Dict[str, Any], 
                          screening_result: Dict[str, Any], 
                          emails_sent: list) -> Dict[str, Any]:
        """
        Make a hiring decision based on candidate information and workflow state.
        
        Args:
            candidate_info: Dictionary containing candidate information
            screening_result: Results from resume screening
            emails_sent: List of emails sent during the process
            
        Returns:
            Dict containing final decision and reasoning
        """
        # Create decision prompt
        prompt = f"""
        You are a hiring decision maker. Please make a final decision about the candidate based on the following information:
        
        Candidate Information:
        {candidate_info}
        
        Screening Results:
        {screening_result}
        
        Emails Sent:
        {emails_sent}
        
        Please provide a final decision (accept/reject) and detailed reasoning.
        """
        
        # Get LLM response
        response = await self.llm.agenerate([HumanMessage(content=prompt)])
        
        # Parse response
        decision = self._parse_decision_response(response)
        
        return decision

    def _parse_decision_response(self, response) -> Dict[str, Any]:
        """Parse the LLM response into a structured decision format"""
        content = response.generations[0][0].text
        
        # Extract decision
        decision = "reject"
        reasoning = ""
        
        for line in content.split('\n'):
            if "decision" in line.lower():
                decision = line.split()[0].lower()
            elif "reasoning" in line.lower():
                reasoning = line.split("reasoning:", 1)[1].strip()
        
        return {
            "decision": decision,
            "reasoning": reasoning,
            "timestamp": datetime.datetime.now().isoformat()
        }
