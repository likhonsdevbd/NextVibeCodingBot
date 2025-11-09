"""
Task parser to analyze and classify coding tasks
"""

import re
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..config import settings, TASK_PATTERNS, SUPPORTED_LANGUAGES


logger = logging.getLogger(__name__)


class TaskParser:
    """Parse and classify incoming coding tasks"""
    
    def __init__(self):
        self.task_patterns = TASK_PATTERNS
        self.supported_languages = SUPPORTED_LANGUAGES
        
    async def parse_message(self, message: str) -> Dict[str, Any]:
        """
        Parse a message to identify the task type, language, and details
        
        Args:
            message: The raw message text from the user
            
        Returns:
            Dictionary containing task information
        """
        logger.info(f"Parsing message: {message[:100]}...")
        
        # Clean and prepare the message
        cleaned_message = self._clean_message(message)
        
        # Detect task type
        task_type = self._detect_task_type(cleaned_message)
        
        # Detect programming language
        language = self._detect_language(cleaned_message, message)
        
        # Extract code blocks
        code_blocks = self._extract_code_blocks(message)
        
        # Extract task details
        task_details = self._extract_task_details(cleaned_message)
        
        # Create task info
        task_info = {
            "id": self._generate_task_id(message),
            "original_message": message,
            "cleaned_message": cleaned_message,
            "task_type": task_type,
            "language": language,
            "code_blocks": code_blocks,
            "details": task_details,
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": self._calculate_confidence(task_type, task_details)
        }
        
        logger.info(f"Parsed task info: {task_info}")
        return task_info
        
    def _clean_message(self, message: str) -> str:
        """Clean and normalize the message text"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', message.strip())
        
        # Remove common Telegram formatting that doesn't affect meaning
        cleaned = re.sub(r'`{3}.*?`{3}', 'CODE_BLOCK', cleaned)  # Replace code blocks with placeholder
        cleaned = re.sub(r'`[^`]+`', 'CODE', cleaned)  # Replace inline code with placeholder
        
        return cleaned
        
    def _detect_task_type(self, message: str) -> str:
        """Detect the type of coding task"""
        message_lower = message.lower()
        
        # Score each task type
        scores = {}
        for task_type, patterns in self.task_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, message_lower)
                score += len(matches)
            scores[task_type] = score
            
        # Get the task type with highest score
        if scores:
            task_type = max(scores, key=scores.get)
            if scores[task_type] > 0:
                return task_type
                
        # Default to general coding if no clear match
        return "coding"
        
    def _detect_language(self, cleaned_message: str, original_message: str) -> Optional[str]:
        """Detect the programming language from the message"""
        # Check for explicit language mentions
        language_keywords = {
            "python": ["python", "py", "flask", "django", "pandas", "numpy"],
            "javascript": ["javascript", "js", "node", "react", "vue", "angular", "npm"],
            "typescript": ["typescript", "ts", "tsx", "jsx"],
            "java": ["java", "spring", "maven", "gradle"],
            "cpp": ["c++", "cpp", "qt"],
            "c": ["c language", "c programming"],
            "go": ["golang", "go language", "go programming"],
            "rust": ["rust", "cargo"],
            "php": ["php", "laravel", "symfony"],
            "ruby": ["ruby", "rails", "gem"]
        }
        
        message_lower = cleaned_message.lower()
        
        for language, keywords in language_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return language
                    
        # Check code blocks for language hints
        code_blocks = self._extract_code_blocks(original_message)
        for block in code_blocks:
            if block.get('language'):
                return block['language']
                
        return None
        
    def _extract_code_blocks(self, message: str) -> List[Dict[str, Any]]:
        """Extract code blocks from the message"""
        code_blocks = []
        
        # Match fenced code blocks
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.findall(pattern, message, re.DOTALL)
        
        for i, (lang, code) in enumerate(matches):
            code_blocks.append({
                "id": i,
                "language": lang or None,
                "code": code.strip(),
                "type": "fenced"
            })
            
        # Match inline code blocks
        inline_pattern = r'`([^`]+)`'
        inline_matches = re.findall(inline_pattern, message)
        
        for i, code in enumerate(inline_matches):
            code_blocks.append({
                "id": f"inline_{i}",
                "language": None,
                "code": code,
                "type": "inline"
            })
            
        return code_blocks
        
    def _extract_task_details(self, message: str) -> Dict[str, Any]:
        """Extract specific task details from the message"""
        details = {
            "urgency": self._detect_urgency(message),
            "complexity": self._detect_complexity(message),
            "specific_requirements": self._extract_requirements(message),
            "error_messages": self._extract_error_messages(message)
        }
        
        return details
        
    def _detect_urgency(self, message: str) -> str:
        """Detect urgency level of the task"""
        urgent_keywords = ["urgent", "asap", "immediately", "quick", "fast", "emergency"]
        medium_keywords = ["soon", "whenever", "no rush"]
        
        message_lower = message.lower()
        
        for keyword in urgent_keywords:
            if keyword in message_lower:
                return "high"
                
        for keyword in medium_keywords:
            if keyword in message_lower:
                return "low"
                
        return "medium"
        
    def _detect_complexity(self, message: str) -> str:
        """Detect the complexity level of the task"""
        simple_keywords = ["simple", "easy", "basic", "quick fix"]
        complex_keywords = ["complex", "advanced", "complicated", "full application", "system"]
        
        message_lower = message.lower()
        
        for keyword in simple_keywords:
            if keyword in message_lower:
                return "low"
                
        for keyword in complex_keywords:
            if keyword in message_lower:
                return "high"
                
        return "medium"
        
    def _extract_requirements(self, message: str) -> List[str]:
        """Extract specific requirements mentioned in the task"""
        requirements = []
        
        # Look for requirement patterns
        req_patterns = [
            r"need to (\w+)",
            r"should (\w+)",
            r"must (\w+)",
            r"has to (\w+)",
            r"requirements?[:\s]+(.*?)(?:\.|$)",
        ]
        
        for pattern in req_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            requirements.extend(matches)
            
        return requirements
        
    def _extract_error_messages(self, message: str) -> List[str]:
        """Extract error messages from the task description"""
        error_patterns = [
            r"error[:\s]+(.*?)(?:\.|$)",
            r"exception[:\s]+(.*?)(?:\.|$)",
            r"traceback[:\s]+(.*?)(?:\.|$)",
            r"(?i)getting (.*? error.*?)(?:\.|$)"
        ]
        
        errors = []
        for pattern in error_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE | re.DOTALL)
            errors.extend(matches)
            
        return errors
        
    def _generate_task_id(self, message: str) -> str:
        """Generate a unique task ID based on message content"""
        return hashlib.md5(message.encode()).hexdigest()[:8]
        
    def _calculate_confidence(self, task_type: str, details: Dict[str, Any]) -> float:
        """Calculate confidence score for the task classification"""
        confidence = 0.5  # Base confidence
        
        # Boost confidence if we found specific details
        if details.get('specific_requirements'):
            confidence += 0.2
        if details.get('error_messages'):
            confidence += 0.2
        if details.get('urgency') != 'medium':
            confidence += 0.1
            
        return min(confidence, 1.0)