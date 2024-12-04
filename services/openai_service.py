from typing import Dict, Optional
from config.settings import settings
import openai

class OpenAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
    
    async def generate_content(self, 
        topic: str,
        industry: str,
        expertise: Optional[str] = None,
        story: Optional[str] = None
    ) -> Dict:
        prompt = self._build_prompt(topic, industry, expertise, story)
        
        try:
            response = await openai.chat.completions.create(
                model=settings.GPT_MODEL,
                messages=[
                    {"role": "system", "content": "You are a LinkedIn content expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
            return {
                "content": response.choices[0].message.content,
                "status": "success"
            }
        except Exception as e:
            return {
                "content": str(e),
                "status": "error"
            }
    
    def _build_prompt(self, topic: str, industry: str, expertise: Optional[str], story: Optional[str]) -> str:
        return f"""
        Create an engaging LinkedIn post about:
        Topic: {topic}
        Industry: {industry}
        Expertise: {expertise if expertise else 'General'}
        Personal Story: {story if story else 'None'}
        
        Include:
        1. Attention-grabbing hook
        2. Main insights backed by data
        3. Personal perspective
        4. Clear call-to-action
        5. 3-5 relevant hashtags
        
        Format the post with proper spacing and emojis for better readability.
        """
