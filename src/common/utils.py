from pathlib import Path


def get_project_path(project_path: str) -> str:
    return str((Path(__file__).parent / "../" / project_path).resolve())
