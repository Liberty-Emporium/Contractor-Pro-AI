"""
AI CEO for Contractor Pro
"""

import os
import requests

GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
Qwen_API_KEY = os.environ.get('QWEN_API_KEY', '')

class AICEO:
    def __init__(self):
        self.name = "Contractor AI"
    
    def think(self, prompt):
        system_prompt = """You are the CEO of Contractor Pro - an app for contractors.
Your job is to help with:
- Writing bids
- Finding best prices
- Answering contractor questions
- Business advice

Be specific, helpful, and professional."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        # Try Groq first
        if GROQ_API_KEY:
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                    json={"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": 500}
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
            except:
                pass
        
        # Fallback to Qwen
        if Qwen_API_KEY:
            try:
                response = requests.post(
                    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                    headers={"Authorization": f"Bearer {Qwen_API_KEY}"},
                    json={"model": "qwen-plus", "messages": messages, "max_tokens": 500}
                )
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
            except:
                pass
        
        return "AI unavailable - configure API keys in Railway"

ceo = AICEO()
