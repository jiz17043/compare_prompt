import tempfile
import subprocess

def run_test_code(function_code, test_code):
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w+", delete=False) as f:
        f.write(function_code + "\n\n" + test_code)
        f.flush()
        result = subprocess.run(["python", f.name], capture_output=True, text=True)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
