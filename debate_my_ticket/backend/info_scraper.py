import requests
from typing import Dict, Any
import json
from litellm import completion
import litellm
from debate_my_ticket.utils.helpers import load_config

class InfoScraper:
    def __init__(self):
        config = load_config()
        self.api_key = config['api_key']
        # Configure litellm to use OpenAI directly without proxies
        litellm.set_verbose = True
        litellm.api_key = self.api_key
    
    def gather_context(self, ticket_info: Dict[str, Any]) -> Dict[str, Any]:
        """Gather legal and social context for the ticket."""
        context = {
            'local_laws': self._get_local_laws(ticket_info),
            'social_context': self._get_social_context(ticket_info)
        }
        return context
    
    def _get_local_laws(self, ticket_info: Dict[str, Any]) -> str:
        """Get relevant local laws for the ticket."""
        city = ticket_info.get('city', '').lower()
        violation_code = ticket_info.get('violation_code', '')
        
        # This is a placeholder. In a real implementation, you would:
        # 1. Query a legal database API
        # 2. Scrape city/municipal websites
        # 3. Use GPT to summarize relevant laws
        
        prompt = f"""Find relevant laws for {city} regarding violation code {violation_code}.
        Focus on:
        1. Specific municipal codes
        2. Required elements for a valid ticket
        3. Common defenses
        4. Appeal process"""
        
        try:
            response = completion(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a legal research assistant."},
                    {"role": "user", "content": prompt}
                ],
                api_key=self.api_key,
                max_tokens=1000,
                temperature=0.3,
                timeout=30
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error gathering local laws: {str(e)}"
    
    def _get_social_context(self, ticket_info: Dict[str, Any]) -> str:
        """Get social context from various sources."""
        city = ticket_info.get('city', '')
        violation_type = ticket_info.get('violation_code', '')
        
        # This is a placeholder. In a real implementation, you would:
        # 1. Query Reddit API for relevant posts
        # 2. Search Twitter for related tweets
        # 3. Scrape legal forums
        
        prompt = f"""Find social context about {violation_type} tickets in {city}.
        Include:
        1. Common experiences
        2. Success/failure rates of challenges
        3. Notable cases or precedents
        4. Public sentiment"""
        
        try:
            response = completion(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a social media analyst."},
                    {"role": "user", "content": prompt}
                ],
                api_key=self.api_key,
                max_tokens=1000,
                temperature=0.3,
                timeout=30
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error gathering social context: {str(e)}" 