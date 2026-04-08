import docker
import os
import tempfile
import uuid
import time
import subprocess
from app.config import settings

class CodeSandbox:
    def __init__(self, image=settings.SANDBOX_IMAGE):
        self.image = image
        self.enabled = False
        self.client = None
        # Allow turning sandbox off via env (e.g., SANDBOX_ENABLED=0 for local dev)
        env_flag = os.getenv("SANDBOX_ENABLED", "0").lower() in ("1", "true", "yes")
        if env_flag:
            try:
                self.client = docker.from_env()
                # probe client to ensure it connects correctly
                _ = self.client.version()
                self.enabled = True
            except Exception:
                self.enabled = False

    def execute(self, code: str, test_code: str = "") -> dict:
        """
        Executes code + optional pytest in a temporary Docker container.
        Returns: { 'success': bool, 'output': str, 'error': str, 'exit_code': int }
        """
        job_id = str(uuid.uuid4())
        # Use absolute path for temp_dir to ensure it works on Windows
        temp_dir = tempfile.mkdtemp(prefix=f"sandbox_{job_id}_")
        
        # Write code to a file
        code_file = os.path.join(temp_dir, "solution.py")
        with open(code_file, "w", encoding="utf-8") as f:
            f.write(code)
            
        # Write test code if provided
        test_file = None
        if test_code:
            test_file = os.path.join(temp_dir, "test_solution.py")
            with open(test_file, "w", encoding="utf-8") as f:
                # Import solution to test it
                f.write("from solution import *\n\n" + test_code)

        try:
            # If Docker sandbox is available and enabled, use it
            if self.enabled and self.client is not None:
                # Docker volume mount needs absolute path
                abs_temp_dir = os.path.abspath(temp_dir)
                command = "pytest test_solution.py" if test_file else "python solution.py"
                container = self.client.containers.run(
                    self.image,
                    command=command,
                    volumes={abs_temp_dir: {'bind': '/app', 'mode': 'rw'}},
                    working_dir='/app',
                    detach=True,
                    mem_limit='64m',
                    cpu_quota=50000,  # 50% CPU
                    network_disabled=True
                )
                # Wait with timeout
                start_time = time.time()
                timeout = 10
                status = container.status
                while status != 'exited' and (time.time() - start_time) < timeout:
                    time.sleep(0.5)
                    container.reload()
                    status = container.status
                if status != 'exited':
                    container.kill()
                    return {"success": False, "output": "", "error": "Timeout", "exit_code": -1}
                logs = container.logs().decode('utf-8')
                exit_code = container.attrs['State']['ExitCode']
                container.remove()
                return {
                    "success": exit_code == 0,
                    "output": logs if exit_code == 0 else "",
                    "error": logs if exit_code != 0 else "",
                    "exit_code": exit_code
                }
            else:
                # Fallback local execution (dev only). Enforce timeout.
                # Run in temp dir to avoid touching project files.
                cmd = ["python", "solution.py"] if not test_file else ["python", "-m", "pytest", "test_solution.py"]
                proc = subprocess.run(
                    cmd,
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                success = proc.returncode == 0
                return {
                    "success": success,
                    "output": proc.stdout if success else "",
                    "error": proc.stderr if not success else "",
                    "exit_code": proc.returncode
                }
        except subprocess.TimeoutExpired:
            return {"success": False, "output": "", "error": "Timeout", "exit_code": -1}
        except Exception as e:
            return {"success": False, "output": "", "error": str(e), "exit_code": -1}
        finally:
            # Clean up files
            try:
                if os.path.exists(code_file): os.remove(code_file)
                if test_file and os.path.exists(test_file): os.remove(test_file)
                os.rmdir(temp_dir)
            except:
                pass
