import json
import configparser
from typing import Dict, Any, Optional
import os

def load_config() -> Dict[str, str]:
    """Load configuration from api.cfg file."""
    config = configparser.ConfigParser()
    config_path = os.path.join('./api.cfg')
    config.read(config_path)
    return dict(config['openai'])

def parse_agent_response(response: str) -> tuple[bool, str]:
    """Parse agent response to check for concession and extract message."""
    if response.startswith("CONCEDE:"):
        return True, response[8:].strip()
    return False, response.strip()

def format_debate_history(messages: list[Dict[str, str]]) -> str:
    """Format debate history for prompt context."""
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

def validate_ticket_info(ticket_info: Dict[str, Any]) -> list[str]:
    """Validate ticket information for required fields."""
    required_fields = [
        'ticket_number',
        'city',
        'address',
        'violation_code',
        'date',
        'officer_info',
        'fine_amount'
    ]
    
    missing_fields = [field for field in required_fields if field not in ticket_info]
    return missing_fields

def save_debate_history(ticket_number: str, debate_history: list[Dict[str, str]]):
    """Save debate history to a JSON file."""
    history_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'history')
    os.makedirs(history_dir, exist_ok=True)
    
    file_path = os.path.join(history_dir, f"{ticket_number}.json")
    with open(file_path, 'w') as f:
        json.dump(debate_history, f, indent=2)

def load_debate_history(ticket_number: str) -> Optional[list[Dict[str, str]]]:
    """Load debate history from a JSON file."""
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'history',
        f"{ticket_number}.json"
    )
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None 