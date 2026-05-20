import os
import tempfile


def get_upload_dir(*parts):
    if os.getenv("VERCEL"):
        return os.path.join(tempfile.gettempdir(), *parts)
    return None
