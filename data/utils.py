from typing import Iterable
import os


def files_in_path(path: str, extension: str) -> Iterable[str]:
    return (os.path.join(path, x) for x in os.listdir(path) if x.endswith(extension))
