"""
AI client for generating responses
"""

import logging
import asyncio
from typing import Dict, Any, Optional
import json
import os

from ..config import settings


logger = logging.getLogger(__name__)


class AIClient:
    """Client for AI service integration"""
    
    def __init__(self):
        self.openai_api_key = settings.openai_api_key
        self.anthropic_api_key = settings.anthropic_api_key
        self.minimax_api_key = settings.minimax_api_key
        self.minimax_base_url = settings.minimax_base_url
        self._openai_client = None
        self._anthropic_client = None
        self._minimax_client = None
        
    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a response using available AI service
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            AI response dictionary
        """
        logger.info("Generating AI response")
        
        # Try different AI services in order of preference
        if self.anthropic_api_key:
            try:
                return await self._generate_anthropic_response(prompt)
            except Exception as e:
                logger.warning(f"Anthropic API failed: {e}")
                
        if self.minimax_api_key:
            try:
                return await self._generate_minimax_response(prompt)
            except Exception as e:
                logger.warning(f"MiniMax API failed: {e}")
                
        if self.openai_api_key:
            try:
                return await self._generate_openai_response(prompt)
            except Exception as e:
                logger.warning(f"OpenAI API failed: {e}")
                
        # Fallback to a simple template-based response
        logger.info("No AI APIs available, using fallback response")
        return self._generate_fallback_response(prompt)
        
    async def _generate_anthropic_response(self, prompt: str) -> Dict[str, Any]:
        """Generate response using Anthropic Claude"""
        
        try:
            import anthropic
            
            # Create client
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            
            # Send request
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return {
                "content": response.content[0].text,
                "model": "anthropic-claude",
                "usage": getattr(response, 'usage', {})
            }
            
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
            
    async def _generate_minimax_response(self, prompt: str) -> Dict[str, Any]:
        """Generate response using MiniMax via OpenAI SDK"""
        
        try:
            from openai import OpenAI
            
            # Create client if not exists
            if not self._minimax_client:
                self._minimax_client = OpenAI(
                    base_url=self.minimax_base_url,
                    api_key=self.minimax_api_key
                )
            
            # Send request
            response = self._minimax_client.chat.completions.create(
                model="MiniMax-M2",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful AI coding assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                extra_body={"reasoning_split": True},
                temperature=1.0
            )
            
            # Get thinking process and response content
            thinking = response.choices[0].message.reasoning_details[0]['text'] if response.choices[0].message.reasoning_details else ""
            content = response.choices[0].message.content
            
            return {
                "content": content,
                "thinking": thinking,
                "model": "minimax-m2",
                "usage": getattr(response, 'usage', {})
            }
            
        except Exception as e:
            logger.error(f"MiniMax API error: {e}")
            raise
            
    async def _generate_openai_response(self, prompt: str) -> Dict[str, Any]:
        """Generate response using OpenAI"""
        
        try:
            from openai import OpenAI
            
            # Create client
            client = OpenAI(api_key=self.openai_api_key)
            
            # Send request
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful programming assistant that provides clear, actionable solutions to coding problems."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return {
                "content": response.choices[0].message.content,
                "model": "openai-gpt-3.5",
                "usage": response.usage.dict() if response.usage else {}
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
            
    def _generate_fallback_response(self, prompt: str) -> Dict[str, Any]:
        """Generate a fallback response when AI APIs are unavailable"""
        
        # Simple template-based response
        response_templates = {
            "bug": """
## Bug Analysis

Based on your description, here's my analysis of the bug:

**Problem:** The issue appears to be related to [specific area mentioned in the prompt]

**Solution approach:**
1. Check error messages and stack traces for clues
2. Identify the root cause by examining the failing code
3. Implement a targeted fix
4. Test the solution thoroughly

**Next steps:**
- Please share the exact error message and relevant code
- I can provide more specific guidance once I see the actual error
- Consider adding error handling and logging to prevent similar issues

Let me know if you'd like me to help with any specific part of the debugging process.
""",
            "feature": """
## Feature Implementation

I'll help you implement this feature step by step:

**Planning:**
1. **Requirements analysis** - Understand exactly what the feature should do
2. **Design phase** - Plan the implementation approach
3. **Development** - Write the code for the new feature
4. **Testing** - Ensure the feature works correctly
5. **Integration** - Make sure it fits well with existing code

**Getting started:**
- Could you share more details about the specific requirements?
- Do you have any existing code or examples to work from?
- What programming language are you using?

I'm ready to help you build this feature! Please provide more details so I can give you a specific implementation plan.
""",
            "debug": """
## Debugging Assistance

Let's debug this issue systematically:

**Debugging approach:**
1. **Reproduce the problem** - Make sure you can consistently trigger the issue
2. **Gather information** - Collect error messages, logs, and relevant code
3. **Isolate the issue** - Identify which part of the code is causing the problem
4. **Implement fix** - Address the root cause
5. **Verify solution** - Test that the fix works and doesn't break other functionality

**Information I need:**
- What exactly is happening vs. what you expect to happen?
- Any error messages or stack traces?
- Relevant code snippets
- Steps to reproduce the issue

Share these details and I'll help you find and fix the problem!
"""
        }
        
        # Try to match prompt to a template
        prompt_lower = prompt.lower()
        
        if any(keyword in prompt_lower for keyword in ['bug', 'error', 'exception', 'broken']):
            response = response_templates["bug"]
        elif any(keyword in prompt_lower for keyword in ['feature', 'add', 'implement', 'create']):
            response = response_templates["feature"]
        elif any(keyword in prompt_lower for keyword in ['debug', 'troubleshoot', 'find issue']):
            response = response_templates["debug"]
        else:
            response = """
## Coding Assistance

I'm here to help with your coding problem! 

**What I can help with:**
- 🐛 Bug fixes and error resolution
- ⚡ Feature development and implementation
- 🔍 Code analysis and optimization
- 🛠️ Debugging and troubleshooting
- 📚 General programming questions

**To get started:**
Please describe your specific coding challenge, including:
- What you're trying to accomplish
- Any error messages you're seeing
- Relevant code snippets
- What programming language you're using

I'll analyze your request and provide a detailed solution approach!
"""
            
        return {
            "content": response,
            "model": "fallback-template",
            "usage": {}
        }