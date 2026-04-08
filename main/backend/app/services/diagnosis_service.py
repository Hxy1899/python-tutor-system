from app.core.preprocessor import CodePreprocessor
from app.core.static_analyzer import StaticAnalyzer
from app.core.sandbox import CodeSandbox
from app.core.error_classifier import ErrorClassifier
from app.core.hint_generator import HintGenerator
from typing import Dict, Any

class DiagnosisService:
    def __init__(self):
        self.preprocessor = CodePreprocessor()
        self.static_analyzer = StaticAnalyzer()
        self.sandbox = CodeSandbox()
        self.error_classifier = ErrorClassifier()
        self.hint_generator = HintGenerator()

    def diagnose(self, code: str, test_code: str = "") -> Dict[str, Any]:
        """
        Runs the full diagnosis flow:
        Preprocess -> Static Analysis -> Dynamic Test -> ML Classification -> Hint Generation
        """
        # 1. Preprocess code
        processed_code = self.preprocessor.preprocess(code)
        
        # 2. Static Analysis
        static_issues = self.static_analyzer.analyze(code)
        
        # 3. Dynamic Testing
        dynamic_result = self.sandbox.execute(code, test_code)
        
        # 4. Error Classification (ML + Rules)
        error_type = "Correct"
        if not dynamic_result["success"]:
            # If dynamic test fails, predict error type
            error_type = self.error_classifier.predict(processed_code)
            # If ML says Unknown, use dynamic output for heuristic mapping
            if error_type == "Unknown" and dynamic_result["error"]:
                # Simple heuristic mapping from stderr
                if "SyntaxError" in dynamic_result["error"]:
                    error_type = "SyntaxError"
                elif "IndentationError" in dynamic_result["error"]:
                    error_type = "IndentationError"
                elif "NameError" in dynamic_result["error"]:
                    error_type = "NameError"
                elif "TypeError" in dynamic_result["error"]:
                    error_type = "TypeError"
                elif "ZeroDivisionError" in dynamic_result["error"]:
                    error_type = "ZeroDivisionError"
                elif "IndexError" in dynamic_result["error"]:
                    error_type = "IndexError"
                elif "KeyError" in dynamic_result["error"]:
                    error_type = "KeyError"
                else:
                    error_type = "LogicalError"
        elif static_issues:
            # If tests pass but static analysis finds major issues
            # We can treat some warnings as logical errors or code quality issues
            pass
            
        # 5. Hint Generation
        hint = ""
        if error_type != "Correct":
            hint = self.hint_generator.generate(error_type, code)
        
        return {
            "error_type": error_type,
            "hint": hint,
            "is_correct": dynamic_result["success"],
            "static_issues": static_issues,
            "dynamic_output": dynamic_result["output"],
            "dynamic_error": dynamic_result["error"]
        }
