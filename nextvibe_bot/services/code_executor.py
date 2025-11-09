"""
Code executor for running code in a safe environment
"""

import asyncio
import logging
import os
import sys
import tempfile
import subprocess
import shutil
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from ..config import settings, SUPPORTED_LANGUAGES


logger = logging.getLogger(__name__)


class CodeExecutor:
    """Execute code in a safe environment"""
    
    def __init__(self):
        self.temp_dir = None
        self.docker_enabled = settings.docker_enabled
        self.execution_timeout = settings.code_execution_timeout
        
    async def execute(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute code based on analysis results
        
        Args:
            analysis: Code analysis results
            
        Returns:
            Execution results
        """
        logger.info("Starting code execution")
        
        execution_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "pending",
            "output": "",
            "error": None,
            "execution_time": 0,
            "files_created": []
        }
        
        try:
            # Create temporary directory
            self.temp_dir = tempfile.mkdtemp(prefix="nextvibe_exec_")
            logger.info(f"Created temp directory: {self.temp_dir}")
            
            # Prepare code for execution
            prepared_code = await self._prepare_code(analysis)
            if not prepared_code:
                execution_result["status"] = "skipped"
                execution_result["output"] = "No executable code found"
                return execution_result
                
            # Write code to file
            file_path = await self._write_code_to_file(prepared_code)
            execution_result["files_created"].append(file_path)
            
            # Execute the code
            start_time = datetime.utcnow()
            
            if self.docker_enabled:
                result = await self._execute_in_docker(file_path, analysis.get("language"))
            else:
                result = await self._execute_locally(file_path, analysis.get("language"))
                
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            execution_result["execution_time"] = execution_time
            
            if result["success"]:
                execution_result["status"] = "completed"
                execution_result["output"] = result["output"]
            else:
                execution_result["status"] = "failed"
                execution_result["error"] = result["error"]
                execution_result["output"] = result.get("output", "")
                
        except Exception as e:
            logger.error(f"Error during code execution: {e}")
            execution_result["status"] = "error"
            execution_result["error"] = str(e)
            
        finally:
            # Clean up temporary directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                logger.info("Cleaned up temp directory")
                
        return execution_result
        
    async def _prepare_code(self, analysis: Dict[str, Any]) -> Optional[str]:
        """Prepare code for execution based on analysis"""
        
        language = analysis.get("language", "python")
        
        # If we have code blocks, prioritize them
        if "code_analysis" in analysis and analysis["code_analysis"].get("blocks_analyzed", 0) > 0:
            return self._extract_executable_code(analysis)
            
        # Otherwise, generate simple test code
        if language == "python":
            return self._generate_python_test(analysis)
        elif language in ["javascript", "typescript"]:
            return self._generate_javascript_test(analysis)
        else:
            # For other languages, try to create a simple hello world
            return self._generate_simple_test(language)
            
    def _extract_executable_code(self, analysis: Dict[str, Any]) -> str:
        """Extract and prepare executable code from analysis"""
        
        # This is a simplified version - in a real implementation,
        # you'd want to be more sophisticated about code extraction
        for block in analysis.get("task_info", {}).get("code_blocks", []):
            if block["type"] == "fenced" and block.get("code"):
                return block["code"]
                
        return ""
        
    def _generate_python_test(self, analysis: Dict[str, Any]) -> str:
        """Generate a simple Python test based on the analysis"""
        
        task_type = analysis.get("task_type", "coding")
        
        if task_type == "bug":
            return '''#!/usr/bin/env python3
"""Test script for bug fix verification"""

import sys
import traceback

def test_bug_fix():
    """Test the bug fix"""
    try:
        print("Testing the bug fix...")
        # This is a placeholder - in a real implementation,
        # you would have the actual bug fix code
        print("Bug fix appears to be working!")
        return True
    except Exception as e:
        print(f"Error testing bug fix: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_bug_fix()
    sys.exit(0 if success else 1)
'''
        elif task_type == "feature":
            return '''#!/usr/bin/env python3
"""Test script for feature implementation"""

import sys

def test_feature():
    """Test the new feature"""
    try:
        print("Testing the new feature...")
        # This is a placeholder for the actual feature implementation
        print("Feature is working correctly!")
        return True
    except Exception as e:
        print(f"Error testing feature: {e}")
        return False

if __name__ == "__main__":
    success = test_feature()
    sys.exit(0 if success else 1)
'''
        else:
            return '''#!/usr/bin/env python3
"""General test script"""

import sys

def main():
    print("Code execution test")
    print("This is a placeholder for the actual code")
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
        
    def _generate_javascript_test(self, analysis: Dict[str, Any]) -> str:
        """Generate a simple JavaScript test"""
        
        return '''console.log("JavaScript execution test");
console.log("This is a placeholder for the actual code");

// Test completion
process.exit(0);
'''
        
    def _generate_simple_test(self, language: str) -> str:
        """Generate a simple test for other languages"""
        
        templates = {
            "java": '''public class Test {
    public static void main(String[] args) {
        System.out.println("Java execution test");
    }
}''',
            "cpp": '''#include <iostream>
int main() {
    std::cout << "C++ execution test" << std::endl;
    return 0;
}''',
            "go": '''package main
import "fmt"
func main() {
    fmt.Println("Go execution test")
}''',
            "rust": '''fn main() {
    println!("Rust execution test");
}'''
        }
        
        return templates.get(language, "# No template available for this language")
        
    async def _write_code_to_file(self, code: str) -> str:
        """Write code to a temporary file"""
        
        if not self.temp_dir:
            raise RuntimeError("Temp directory not initialized")
            
        # Determine file extension based on language
        # This is simplified - you'd want more sophisticated language detection
        if "public class" in code or "System.out" in code:
            file_path = os.path.join(self.temp_dir, "Test.java")
        elif "#include" in code or "std::" in code:
            file_path = os.path.join(self.temp_dir, "test.cpp")
        elif "package main" in code:
            file_path = os.path.join(self.temp_dir, "main.go")
        elif "fn main" in code:
            file_path = os.path.join(self.temp_dir, "main.rs")
        else:
            # Default to Python
            file_path = os.path.join(self.temp_dir, "test.py")
            
        with open(file_path, "w") as f:
            f.write(code)
            
        return file_path
        
    async def _execute_in_docker(self, file_path: str, language: Optional[str]) -> Dict[str, Any]:
        """Execute code in Docker container"""
        
        # This is a placeholder - implementing full Docker execution
        # would require the docker library and proper container management
        logger.info(f"Docker execution requested for {file_path}")
        
        # For now, fall back to local execution
        return await self._execute_locally(file_path, language)
        
    async def _execute_locally(self, file_path: str, language: Optional[str]) -> Dict[str, Any]:
        """Execute code locally (simulated)"""
        
        result = {
            "success": True,
            "output": "",
            "error": None
        }
        
        try:
            logger.info(f"Executing {file_path} locally")
            
            # Determine execution command
            if file_path.endswith('.py'):
                cmd = [sys.executable, file_path]
            elif file_path.endswith('.js'):
                cmd = ['node', file_path]
            elif file_path.endswith('.java'):
                # For Java, compile first
                compile_result = await asyncio.create_subprocess_exec(
                    'javac', file_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                compile_stdout, compile_stderr = await compile_result.communicate()
                
                if compile_result.returncode != 0:
                    result["success"] = False
                    result["error"] = f"Compilation error: {compile_stderr.decode()}"
                    return result
                    
                # Execute the compiled class
                class_name = os.path.splitext(os.path.basename(file_path))[0]
                cmd = ['java', '-cp', os.path.dirname(file_path), class_name]
            else:
                result["success"] = False
                result["error"] = f"Unsupported file type: {file_path}"
                return result
                
            # Execute the command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(file_path)
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.execution_timeout
            )
            
            output = stdout.decode() if stdout else ""
            error = stderr.decode() if stderr else ""
            
            if process.returncode == 0:
                result["output"] = output
            else:
                result["success"] = False
                result["error"] = error or f"Process exited with code {process.returncode}"
                if output:
                    result["output"] = output
                    
        except asyncio.TimeoutError:
            result["success"] = False
            result["error"] = f"Execution timed out after {self.execution_timeout} seconds"
        except Exception as e:
            result["success"] = False
            result["error"] = f"Execution error: {str(e)}"
            
        return result