import requests
from typing import Dict, Optional
from config.settings import settings

class CanvaService:
    def __init__(self):
        self.client_id = settings.CANVA_CLIENT_ID
        self.client_secret = settings.CANVA_CLIENT_SECRET
        self.base_url = 'https://api.canva.com/v1'
        self.token = None
    
    async def create_design(self, prompt: str, design_type: str = 'social-media') -> Dict:
        try:
            # Template selection based on design type
            templates = {
                'social-media': 'linkedIn-post',
                'banner': 'linkedIn-banner',
                'profile': 'linkedIn-profile'
            }
            
            template = templates.get(design_type, 'social-media')
            
            # Create design from template
            headers = {
                'Authorization': f'Bearer {self.client_secret}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'template': template,
                'prompt': prompt
            }
            
            response = requests.post(
                f'{self.base_url}/designs',
                headers=headers,
                json=data
            )
            
            return response.json()
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }
    
    async def generate_image(self, topic: str, industry: str) -> Dict:
        prompt = f"Create a professional LinkedIn post image about {topic} for {industry} industry. Style: modern, professional, engaging"
        
        try:
            result = await self.create_design(prompt)
            return result
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed'
            }