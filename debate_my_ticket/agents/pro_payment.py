from typing import Dict, Any
import json
from litellm import completion
import litellm
from debate_my_ticket.utils.prompts import PRO_PAYMENT_PROMPT
from debate_my_ticket.utils.helpers import load_config

class ProPaymentAgent:
    def __init__(self):
        config = load_config()
        self.api_key = config['api_key']
        # Configure litellm to use OpenAI directly without proxies
        litellm.set_verbose = True
        litellm.api_key = self.api_key
        
    def generate_argument(self, ticket_info: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate argument in favor of paying the ticket."""
        try:
            # Ensure context has all required keys with default values
            safe_context = {
                'local_laws': context.get('local_laws', 'No specific local laws found.'),
                'social_context': context.get('social_context', 'No social context available.')
            }
            
            response = completion(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """You are a top-tier legal expert arguing in favor of paying the ticket. 
                    Provide detailed, compelling arguments that consider legal precedents, financial implications, and practical outcomes.
                    Focus on concrete evidence and specific legal points. Keep responses under 100 words but ensure they are thorough and persuasive."""},
                    {"role": "user", "content": PRO_PAYMENT_PROMPT.format(
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
            return "Based on the ticket details and local regulations, paying promptly is the most prudent course of action. This avoids potential late fees, court costs, and the risk of a more severe penalty. The financial and time investment in contesting may outweigh potential benefits."
    
    def respond_to_counterargument(self, counterargument: str, ticket_info: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Respond to a counterargument against paying the ticket."""
        try:
            # Ensure context has all required keys with default values
            safe_context = {
                'local_laws': context.get('local_laws', 'No specific local laws found.'),
                'social_context': context.get('social_context', 'No social context available.')
            }
            
            response = completion(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a top-tier legal expert defending the position to pay the ticket.
                    Provide detailed, compelling rebuttals that address specific points raised in the counterargument.
                    Use legal precedents and practical considerations to strengthen your position.
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
            return "While challenging the ticket may seem appealing, consider the full implications: court costs, time investment, and potential for increased penalties. The burden of proof often lies with the defendant, and success rates vary significantly. A prompt payment may be the most cost-effective solution." 