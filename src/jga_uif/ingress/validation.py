from pathlib import PurePosixPath


def validate_safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    if path.is_absolute():
        return False
    if ".." in path.parts:
        return False
    return True
