import re

class CodePreprocessor:
    @staticmethod
    def preprocess(code: str) -> str:
        """
        1. Remove comments (#)
        2. Remove docstrings (''' ... ''' or \"\"\" ... \"\"\")
        3. Standardize indent (not implemented here, but can be)
        4. Trim leading/trailing whitespace
        """
        # Remove docstrings
        code = re.sub(r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')', '', code)
        
        # Remove line comments
        lines = code.split('\n')
        cleaned_lines = []
        for line in lines:
            # Simple comment removal (might be improved to avoid removing # inside strings)
            comment_idx = line.find('#')
            if comment_idx != -1:
                line = line[:comment_idx]
            cleaned_lines.append(line.rstrip())
        
        # Filter out empty lines
        cleaned_code = '\n'.join([l for l in cleaned_lines if l.strip()])
        return cleaned_code.strip()
