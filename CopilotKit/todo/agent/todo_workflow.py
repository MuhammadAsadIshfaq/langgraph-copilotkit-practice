from typing import Dict, List, Any
import groq
import os

class TodoWorkflow:
    def __init__(self):
        self.client = groq.Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.model = "mixtral-8x7b-32768"

    def _get_completion(self, prompt: str) -> str:
        """Get completion from Groq API."""
        completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0.7,
        )
        return completion.choices[0].message.content

    def process_todo(self, todo_text: str) -> Dict[str, Any]:
        """Process a todo through the workflow."""
        # Step 1: Enhance the todo
        enhanced_todo = self._get_completion(
            f"Please enhance this todo description to be more specific and actionable: {todo_text}"
        )

        # Step 2: Suggest priority
        priority = self._get_completion(
            f"Based on this todo description, suggest a priority level (High/Medium/Low): {enhanced_todo}"
        )

        # Step 3: Estimate time
        estimated_time = self._get_completion(
            f"Estimate how long this todo might take to complete (in hours): {enhanced_todo}"
        )

        # Step 4: Suggest subtasks
        subtasks = self._get_completion(
            f"Break down this todo into 2-3 subtasks if it's complex enough: {enhanced_todo}"
        )

        return {
            "enhanced_todo": enhanced_todo,
            "priority": priority,
            "estimated_time": estimated_time,
            "subtasks": subtasks
        } 