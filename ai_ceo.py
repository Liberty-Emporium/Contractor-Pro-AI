"""
AI CEO for Contractor Pro
"""

import os
import requests

class AICEO:
    def __init__(self, api_keys=None, active_provider='qwen'):
        self.name = "Contractor AI"
        self.api_keys = api_keys or {}
        self.active_provider = active_provider
    
    def think(self, prompt):
        system_prompt = """You are the CEO of Contractor Pro - an app for contractors.
Your job is to help with:
- Writing bids
- Finding best prices
- Answering contractor questions
- Business advice

Be specific, helpful, and professional."""
        
        # Try providers in order
        providers = ['anthropic', 'groq', 'qwen', 'openai', 'xai', 'mistral']
        
        for prov in providers:
            key = self.api_keys.get(f'{prov}_key', '')
            if not key or len(key) < 10:
                continue
            
            try:
                if prov == 'anthropic':
                    # Anthropic v1 message format
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": key,
                            "anthropic-version": "2023-06-01"
                        },
                        json={
                            "model": "claude-3-haiku-20240307",
                            "max_tokens": 500,
                            "system": system_prompt,
                            "messages": [{"role": "user", "content": prompt}]
                        },
                        timeout=30
                    )
                    if response.status_code == 200:
                        return response.json()['content'][0]['text']
                    print(f"Anthropic error: {response.status_code} - {response.text[:200]}")
                        
                elif prov == 'groq':
                    response = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {key}"},
                        json={
                            "model": "llama-3.1-70b-versatile",
                            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                            "max_tokens": 500
                        },
                        timeout=30
                    )
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
                    print(f"Groq error: {response.status_code}")
                        
                elif prov == 'qwen':
                    response = requests.post(
                        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                        headers={"Authorization": f"Bearer {key}"},
                        json={
                            "model": "qwen-plus",
                            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                            "max_tokens": 500
                        },
                        timeout=30
                    )
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
                    print(f"Qwen error: {response.status_code} - {response.text[:200]}")
                    
            except Exception as e:
                print(f"Exception for {prov}: {e}")
                continue
        
        return "AI unavailable - all API calls failed"

ceo = AICEO()
