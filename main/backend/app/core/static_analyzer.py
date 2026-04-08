import subprocess
import tempfile
import os
import json

class StaticAnalyzer:
    @staticmethod
    def analyze(code: str) -> list:
        """
        Run pylint on the provided code and return a list of issues.
        Returns: list of dicts with keys: line, column, type, symbol, message
        """
        issues = []
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as f:
            f.write(code.encode('utf-8'))
            temp_file_path = f.name
        
        try:
            # Run pylint with JSON output
            result = subprocess.run(
                ["pylint", "--output-format=json", temp_file_path],
                capture_output=True, text=True
            )
            
            if result.stdout:
                try:
                    pylint_issues = json.loads(result.stdout)
                    for issue in pylint_issues:
                        issues.append({
                            "line": issue.get("line", 1),
                            "column": issue.get("column", 0),
                            "type": issue.get("type", "unknown"),
                            "symbol": issue.get("symbol", ""),
                            "message": issue.get("message", "")
                        })
                except json.JSONDecodeError:
                    pass # Or handle error
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        
        return issues
