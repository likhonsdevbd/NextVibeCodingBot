"""
Code analyzer for understanding and analyzing coding tasks
"""

import logging
from typing import Dict, Any, Optional, List
import json
import asyncio
from datetime import datetime

from ..config import settings
from ..utils.ai_client import AIClient


logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Analyze and understand coding tasks"""
    
    def __init__(self):
        self.ai_client = AIClient()
        
    async def analyze_task(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a task and provide insights and solutions
        
        Args:
            task_info: Parsed task information
            
        Returns:
            Analysis results including solution approach
        """
        logger.info(f"Analyzing task: {task_info['task_type']}")
        
        analysis = {
            "task_id": task_info["id"],
            "task_type": task_info["task_type"],
            "language": task_info["language"],
            "timestamp": datetime.utcnow().isoformat(),
            "status": "analyzing"
        }
        
        try:
            # Generate solution approach
            solution = await self._generate_solution(task_info)
            analysis["solution"] = solution
            
            # Analyze code if provided
            if task_info.get("code_blocks"):
                code_analysis = await self._analyze_code(task_info)
                analysis["code_analysis"] = code_analysis
                
            # Determine if task is executable
            analysis["executable"] = self._is_executable(task_info)
            
            # Generate implementation plan
            analysis["implementation_plan"] = await self._create_implementation_plan(task_info, solution)
            
            analysis["status"] = "completed"
            analysis["confidence"] = self._calculate_analysis_confidence(task_info, solution)
            
        except Exception as e:
            logger.error(f"Error in code analysis: {e}")
            analysis["status"] = "error"
            analysis["error"] = str(e)
            analysis["executable"] = False
            
        return analysis
        
    async def _generate_solution(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a solution approach for the task"""
        
        # Prepare prompt for AI
        prompt = self._build_solution_prompt(task_info)
        
        # Get AI response
        try:
            response = await self.ai_client.generate_response(prompt)
            solution = {
                "approach": response.get("content", ""),
                "ai_model": "minimax" if hasattr(self.ai_client, '_minimax_client') else "fallback",
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.warning(f"AI service unavailable, using fallback solution: {e}")
            solution = self._get_fallback_solution(task_info)
            
        return solution
        
    def _build_solution_prompt(self, task_info: Dict[str, Any]) -> str:
        """Build a detailed prompt for the AI service"""
        
        base_prompt = f"""
You are a senior software engineer and coding expert. Analyze the following task and provide a comprehensive solution.

Task Type: {task_info['task_type']}
Programming Language: {task_info.get('language', 'Not specified')}
Urgency: {task_info['details']['urgency']}
Complexity: {task_info['details']['complexity']}

Original Message:
{task_info['original_message']}

"""
        
        if task_info.get('code_blocks'):
            base_prompt += "\nCode Blocks Provided:\n"
            for i, block in enumerate(task_info['code_blocks']):
                if block['type'] == 'fenced':
                    base_prompt += f"``` {block.get('language', '')}\n{block['code']}\n```\n"
                else:
                    base_prompt += f"Inline code: `{block['code']}`\n"
                    
        if task_info['details'].get('error_messages'):
            base_prompt += "\nError Messages:\n"
            for error in task_info['details']['error_messages']:
                base_prompt += f"- {error}\n"
                
        base_prompt += """
Please provide:
1. A clear explanation of the problem
2. Step-by-step solution approach
3. Any code improvements or fixes needed
4. Best practices to follow
5. Potential issues to watch for

Format your response in a clear, structured way using markdown.
"""
        
        return base_prompt
        
    async def _analyze_code(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze provided code blocks"""
        
        code_analysis = {
            "blocks_analyzed": 0,
            "issues_found": [],
            "suggestions": [],
            "quality_score": 0
        }
        
        for block in task_info.get('code_blocks', []):
            if block['type'] == 'fenced' and block.get('code'):
                code_analysis["blocks_analyzed"] += 1
                
                # Basic code analysis
                issues = self._find_code_issues(block['code'], block.get('language'))
                code_analysis["issues_found"].extend(issues)
                
        # Calculate quality score
        code_analysis["quality_score"] = max(0, 100 - len(code_analysis["issues_found"]) * 10)
        
        return code_analysis
        
    def _find_code_issues(self, code: str, language: Optional[str]) -> List[str]:
        """Find common issues in code"""
        issues = []
        
        if not language:
            return issues
            
        # Common issues by language
        if language == "python":
            # Check for common Python issues
            if "print(" in code and "import logging" not in code:
                issues.append("Consider using logging instead of print statements")
            if "except:" in code:
                issues.append("Consider specifying exception types in except clauses")
                
        elif language in ["javascript", "typescript"]:
            # Check for common JS/TS issues
            if "var " in code:
                issues.append("Consider using let/const instead of var")
            if "==" in code and "!" not in code:
                issues.append("Consider using strict equality (===) instead of loose equality (==)")
                
        return issues
        
    def _is_executable(self, task_info: Dict[str, Any]) -> bool:
        """Determine if the task can be executed"""
        
        # If it's a code analysis or debugging task, it's executable
        if task_info['task_type'] in ['bug', 'debug', 'code_review']:
            return True
            
        # If we have complete code blocks, it might be executable
        if task_info.get('code_blocks'):
            for block in task_info['code_blocks']:
                if block['type'] == 'fenced' and len(block['code'].strip()) > 10:
                    return True
                    
        # If it's a simple feature request with clear requirements
        if task_info['task_type'] == 'feature' and task_info['details']['complexity'] == 'low':
            return True
            
        return False
        
    async def _create_implementation_plan(self, task_info: Dict[str, Any], solution: Dict[str, Any]) -> List[str]:
        """Create a step-by-step implementation plan"""
        
        plan = []
        
        if task_info['task_type'] == 'bug':
            plan = [
                "1. Identify the root cause of the bug",
                "2. Create a minimal test case to reproduce the issue",
                "3. Implement the fix",
                "4. Test the fix with the provided code",
                "5. Verify the solution works correctly"
            ]
        elif task_info['task_type'] == 'feature':
            plan = [
                "1. Understand the feature requirements",
                "2. Design the implementation approach", 
                "3. Write the code implementation",
                "4. Add error handling and edge cases",
                "5. Test the new functionality"
            ]
        elif task_info['task_type'] == 'debug':
            plan = [
                "1. Analyze the problem symptoms",
                "2. Add logging/print statements to trace execution",
                "3. Identify the problematic code section",
                "4. Implement debugging solution",
                "5. Verify the fix resolves the issue"
            ]
        else:
            plan = [
                "1. Analyze the requirements",
                "2. Develop a solution approach",
                "3. Implement the solution",
                "4. Test and validate the result"
            ]
            
        return plan
        
    def _get_fallback_solution(self, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Provide a basic solution when AI service is unavailable"""
        
        task_type = task_info['task_type']
        
        if task_type == 'bug':
            approach = "To fix this bug: 1) Check error messages and stack traces, 2) Identify the root cause, 3) Implement a targeted fix, 4) Test the solution."
        elif task_type == 'feature':
            approach = "To implement this feature: 1) Understand the requirements, 2) Design the implementation, 3) Write the code, 4) Test thoroughly."
        elif task_type == 'debug':
            approach = "To debug this issue: 1) Reproduce the problem, 2) Add logging/prints to trace execution, 3) Identify the problematic code, 4) Fix the underlying issue."
        else:
            approach = "I'll help you solve this coding problem step by step. Please provide more specific details about what you need."
            
        return {
            "approach": approach,
            "ai_model": "fallback",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    def _calculate_analysis_confidence(self, task_info: Dict[str, Any], solution: Dict[str, Any]) -> float:
        """Calculate confidence in the analysis"""
        
        confidence = task_info.get('confidence', 0.5)
        
        # Boost confidence if we have code blocks
        if task_info.get('code_blocks'):
            confidence += 0.2
            
        # Boost confidence if solution was generated by AI
        if solution.get('ai_model') != 'fallback':
            confidence += 0.2
            
        # Reduce confidence for very complex tasks
        if task_info['details']['complexity'] == 'high':
            confidence -= 0.1
            
        return max(0.0, min(confidence, 1.0))