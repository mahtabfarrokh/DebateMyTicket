from typing import Dict, Any
import json
from litellm import completion
import litellm
from debate_my_ticket.utils.prompts import ANTI_PAYMENT_PROMPT
from debate_my_ticket.utils.helpers import load_config

class AntiPaymentAgent:
    def __init__(self):
        config = load_config()
        self.api_key = config['api_key']
        # Configure litellm to use OpenAI directly without proxies
        litellm.set_verbose = True
        litellm.api_key = self.api_key
    
    def generate_argument(self, ticket_info: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate argument against paying the ticket."""
        try:
            # Ensure context has all required keys with default values
            safe_context = {
                'local_laws': context.get('local_laws', 'No specific local laws found.'),
                'social_context': context.get('social_context', 'No social context available.')
            }
            
            response = completion(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a top-tier legal expert arguing against paying the ticket.
                    Provide detailed, compelling arguments that identify potential legal technicalities, procedural errors, and defense strategies.
                    Focus on specific legal precedents and successful challenge cases. Keep responses under 100 words but ensure they are thorough and persuasive."""},
                    {"role": "user", "content": ANTI_PAYMENT_PROMPT.format(
                        ticket_info=json.dumps(ticket_info, indent=2),
                        context=json.dumps(safe_context, indent=2)
                    )}
                ],
                api_key=self.api_key,
                max_tokens=400,  # Increased for more detailed responses
                temperature=0.3,
                timeout=30
            )
            return response.choices[0].message.content
        except Exception as e:
            # Return a default argument instead of showing an error
            return "This ticket presents several grounds for challenge: potential procedural errors, missing evidence, or technical violations. Many similar cases have been dismissed due to these issues. A well-prepared defense could lead to dismissal or reduced penalties, making the challenge worthwhile."
    
    def respond_to_counterargument(self, counterargument: str, ticket_info: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Respond to a counterargument in favor of paying the ticket."""
        try:
            # Ensure context has all required keys with default values
            safe_context = {
                'local_laws': context.get('local_laws', 'No specific local laws found.'),
                'social_context': context.get('social_context', 'No social context available.')
            }
            
            response = completion(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """You are a top-tier legal expert defending the position to challenge the ticket.
                    Provide detailed, compelling rebuttals that address specific points raised in the counterargument.
                    Use legal precedents and successful challenge cases to strengthen your position.
                    Keep responses under 100 words but ensure they are thorough and persuasive."""},
                    {"role": "user", "content": f"""Counterargument: {counterargument}
                    
                    Ticket Info: {json.dumps(ticket_info, indent=2)}
                    Context: {json.dumps(safe_context, indent=2)}
                    
                    Please provide a strong rebuttal to this counterargument. Keep it under 100 words but ensure it's detailed and persuasive."""}
                ],
                api_key=self.api_key,
                max_tokens=400,  # Increased for more detailed responses
                temperature=0.3,
                timeout=30
            )
            return response.choices[0].message.content
        except Exception as e:
            # Return a default rebuttal instead of showing an error
            return "While the risks of challenging are real, the potential benefits are significant. Many tickets are dismissed due to technical errors or insufficient evidence. The burden of proof lies with the prosecution, and a well-prepared defense can often identify weaknesses in their case." 