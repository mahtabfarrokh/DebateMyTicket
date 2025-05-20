import pytesseract
from PIL import Image
import io
from typing import Dict, Any
import json
from debate_my_ticket.utils.prompts import INFO_EXTRACTION_PROMPT
from litellm import completion
import litellm
from debate_my_ticket.utils.helpers import load_config

class OCRProcessor:
    def __init__(self):
        config = load_config()
        self.api_key = config['api_key']
        # Configure litellm to use OpenAI directly without proxies
        litellm.set_verbose = True
        litellm.api_key = self.api_key
    
    def process_image(self, image_data: bytes) -> Dict[str, Any]:
        """Process image and extract text using OCR."""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            # Extract structured information using GPT
            extracted_info = self._extract_structured_info(text)
            
            return extracted_info
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
    
    def _extract_structured_info(self, text: str) -> Dict[str, Any]:
        """Extract structured information from OCR text using GPT."""
        try:
            response = completion(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts information from ticket text."},
                    {"role": "user", "content": INFO_EXTRACTION_PROMPT.format(ticket_text=text)}
                ],
                api_key=self.api_key,
                max_tokens=1000,
                temperature=0.3,
                timeout=30
            )
            
            # Parse the response as JSON
            extracted_info = json.loads(response.choices[0].message.content)
            return extracted_info
        except Exception as e:
            raise Exception(f"Error extracting structured information: {str(e)}") 