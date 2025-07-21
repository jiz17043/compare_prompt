def is_valid_python(code: str) -> bool:
    try:
        compile(code, "<string>", "exec")
        return True
    except Exception:
        return False
