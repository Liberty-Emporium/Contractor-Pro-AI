"""
AI CEO for Contractor Pro - with debug logging
"""

import os
import requests
import json

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
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        providers = ['anthropic', 'qwen', 'groq', 'openai', 'xai', 'mistral']
        
        for prov in providers:
            key = self.api_keys.get(f'{prov}_key', '')
            if not key or len(key) < 10:
                continue
            
            print(f"Trying {prov} with key: {key[:10]}...")
            
            try:
                if prov == 'anthropic':
                    response = requests.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": key, 
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json"
                        },
                        json={
                            "model": "claude-3-haiku-20240307", 
                            "max_tokens": 500, 
                            "messages": messages
                        },
                        timeout=30
                    )
                    print(f"Anthropic response: {response.status_code}")
                    if response.status_code == 200:
                        return response.json()['content'][0]['text']
                        
                elif prov == 'qwen':
                    response = requests.post(
                        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "qwen-plus", 
                            "messages": messages, 
                            "max_tokens": 500
                        },
                        timeout=30
                    )
                    print(f"Qwen response: {response.status_code}")
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
                        
                elif prov == 'groq':
                    response = requests.post(
                        "https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {key}"},
                        json={"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": 500},
                        timeout=30
                    )
                    print(f"Groq response: {response.status_code}")
                    if response.status_code == 200:
                        return response.json()['choices'][0]['message']['content']
                        
            except Exception as e:
                print(f"Exception for {prov}: {e}")
                continue
        
        return "AI unavailable - no valid API keys found"

ceo = AICEO()
