from typing import Dict, Any, List
import json
from litellm import completion
import litellm
from debate_my_ticket.utils.prompts import TICKET_VALIDATION_PROMPT
from debate_my_ticket.utils.helpers import load_config

class TicketValidator:
    def __init__(self):
        config = load_config()
        self.api_key = config['api_key']
        # Configure litellm to use OpenAI directly without proxies
        litellm.set_verbose = True
        litellm.api_key = self.api_key
    
    def validate_ticket(self, ticket_info: Dict[str, Any]) -> List[str]:
        """Validate ticket for legal issues."""
        try:
            response = completion(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a legal expert specializing in ticket validation."},
                    {"role": "user", "content": TICKET_VALIDATION_PROMPT.format(ticket_info=json.dumps(ticket_info, indent=2))}
                ],
                api_key=self.api_key,
                max_tokens=1000,
                temperature=0.3,
                timeout=30
            )
            
            # Parse the response to get list of issues
            issues = response.choices[0].message.content.split('\n')
            return [issue.strip() for issue in issues if issue.strip()]
        except Exception as e:
            return [f"Error validating ticket: {str(e)}"]
    
    def is_ticket_valid(self, ticket_info: Dict[str, Any]) -> bool:
        """Check if ticket is legally valid."""
        issues = self.validate_ticket(ticket_info)
        return len(issues) == 0
    
    def get_validation_summary(self, ticket_info: Dict[str, Any]) -> str:
        """Get a summary of ticket validation results."""
        issues = self.validate_ticket(ticket_info)
        
        if not issues:
            return "The ticket appears to be legally valid."
        
        summary = "The following issues were found:\n"
        for i, issue in enumerate(issues, 1):
            summary += f"{i}. {issue}\n"
        
        return summary 