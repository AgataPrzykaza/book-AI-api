import json
import re
from typing import Optional
from google import genai
from configure.config import GEMINI_API_KEY



class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = "gemini-2.5-flash"
    
    def _generate_content(self, prompt: str) -> Optional[str]:
        """Base method for API calls"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            return response.text if response.text else None
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return None
    
    def _extract_json_from_text(self, text: str, key: str) -> Optional[dict]:
        """Extract JSON containing specific key from text"""
        pattern = rf'\{{.*?"{key}"\s*:\s*.*?\}}'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        return None