from joblib import dump, load
from pathlib import Path

def save_artifact(artifact, path: Path):
    dump(artifact, path)

def load_artifact(path: Path):
    return load(path)
