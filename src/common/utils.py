from pathlib import Path
from uuid import uuid4


def get_project_path(project_path: str) -> str:
    return str((Path(__file__).parent / "../" / project_path).resolve())

def str_uuid4() -> str:
    return str(uuid4())