"""
Result formatting module for bot responses.
"""
from typing import Dict, Any, List
from rich.console import Console
from rich.syntax import Syntax

class ResponseFormatter:
    def __init__(self):
        self.console = Console()

    def format_code_execution_result(self, result: Dict[str, Any]) -> str:
        """
        Format code execution results.
        """
        if result["success"]:
            return (
                "✅ Code executed successfully!\n\n"
                "Output:\n"
                f"```\n{result['output']}```"
            )
        else:
            return (
                "❌ Code execution failed!\n\n"
                f"Error: {result['error']}"
            )

    def format_analysis_result(self, analysis: Dict[str, Any]) -> str:
        """
        Format code analysis results.
        """
        issues = self._format_list("Issues", analysis.get("issues", []))
        suggestions = self._format_list("Suggestions", analysis.get("suggestions", []))
        
        return (
            f"🔍 Code Analysis Results:\n\n"
            f"Complexity: {analysis.get('complexity', 'unknown')}\n\n"
            f"{issues}\n"
            f"{suggestions}"
        )

    def _format_list(self, title: str, items: List[str]) -> str:
        """
        Format a list of items with a title.
        """
        if not items:
            return f"{title}: None found"
            
        formatted = f"{title}:\n"
        for item in items:
            formatted += f"• {item}\n"
        return formatted

    def format_code_block(self, code: str, language: str = "python") -> str:
        """
        Format code with syntax highlighting.
        """
        syntax = Syntax(code, language, theme="monokai")
        return f"```{language}\n{code}\n```"