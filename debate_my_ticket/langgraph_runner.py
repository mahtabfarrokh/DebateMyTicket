from typing import Dict, Any, List
from debate_my_ticket.agents.pro_payment import ProPaymentAgent
from debate_my_ticket.agents.anti_payment import AntiPaymentAgent
from debate_my_ticket.backend.info_scraper import InfoScraper
from debate_my_ticket.backend.ticket_validator import TicketValidator


class DebateRunner:
    def __init__(self):
        self.pro_agent = ProPaymentAgent()
        self.anti_agent = AntiPaymentAgent()
        self.info_scraper = InfoScraper()
        self.validator = TicketValidator()
        self.max_rounds = 3
        self.debate_history = []
    
    def _initialize_context(self, ticket_info: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize context with default values and gather information."""
        try:
            # Initialize with default values
            context = {
                'local_laws': 'No specific local laws found.',
                'social_context': 'No social context available.'
            }
            
            # Gather additional context
            gathered_context = self.info_scraper.gather_context(ticket_info)
            
            # Update context with gathered information
            if gathered_context.get('local_laws'):
                context['local_laws'] = gathered_context['local_laws']
            if gathered_context.get('social_context'):
                context['social_context'] = gathered_context['social_context']
            
            return context
        except Exception as e:
            print(f"Warning: Error gathering context: {str(e)}")
            return {
                'local_laws': 'No specific local laws found.',
                'social_context': 'No social context available.'
            }
    
    def run_debate(self, ticket_info: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, str]]:
        """Run the debate between agents."""
        try:
            # Validate ticket first
            issues = self.validator.validate_ticket(ticket_info)
            if issues:
                self.debate_history.append({
                    'role': 'system',
                    'content': f"Ticket validation issues found: {', '.join(issues)}"
                })
            
            # Get initial arguments
            pro_argument = self.pro_agent.generate_argument(ticket_info, context)
            anti_argument = self.anti_agent.generate_argument(ticket_info, context)
            
            # Add initial arguments to history
            self.debate_history.extend([
                {'role': 'pro_payment', 'content': pro_argument},
                {'role': 'anti_payment', 'content': anti_argument}
            ])
            
            # Run debate rounds
            for _ in range(self.max_rounds - 1):
                # Get responses to previous arguments
                pro_response = self.pro_agent.respond_to_counterargument(
                    self.debate_history[-1]['content'],
                    ticket_info,
                    context
                )
                anti_response = self.anti_agent.respond_to_counterargument(
                    self.debate_history[-2]['content'],
                    ticket_info,
                    context
                )
                
                # Add responses to history
                self.debate_history.extend([
                    {'role': 'pro_payment', 'content': pro_response},
                    {'role': 'anti_payment', 'content': anti_response}
                ])
            
            return self.debate_history
        except Exception as e:
            print(f"Error in debate: {str(e)}")
            return [{'role': 'error', 'content': f"Error running debate: {str(e)}"}]
    
    def get_debate_summary(self) -> str:
        """Get a summary of the debate using LLM."""
        if not self.debate_history:
            return "No debate history available."
        
        # Prepare debate content for summarization
        debate_content = ""
        for entry in self.debate_history:
            if entry['role'] == 'pro_payment':
                debate_content += f"Pro-Payment Argument: {entry['content']}\n\n"
            elif entry['role'] == 'anti_payment':
                debate_content += f"Anti-Payment Argument: {entry['content']}\n\n"
        
        # Use LLM to generate summary
        summary_prompt = f"""Please analyze the following debate about a ticket and provide a concise summary with:
1. Key points from both sides
2. The strength of each argument
3. A clear recommendation on whether to pay or challenge the ticket

Debate content:
{debate_content}

Please provide a well-structured summary that helps the user make an informed decision."""

        try:
            # Use the pro_agent to generate summary
            summary = self.pro_agent.generate_argument(summary_prompt, {})
            return summary
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return "Error generating summary. Please review the debate points above." 