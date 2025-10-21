from io import BytesIO
from PIL import Image
import hashlib
import time

def prepare_image_download_bytes(image_bytes: bytes, prompt: str):
    try:
        im = Image.open(BytesIO(image_bytes)).convert("RGBA")
    except Exception:
        filename = _make_filename(prompt)
        return image_bytes, filename

    buf = BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    filename = _make_filename(prompt)
    return buf.getvalue(), filename

def _make_filename(prompt: str) -> str:
    safe_hash = hashlib.sha1((prompt or str(time.time())).encode("utf-8")).hexdigest()[:8]
    stub = "_".join((prompt or "").strip().split())[:40]
    filename = f"imagine_{stub}_{safe_hash}.png"
    return "".join([c if c.isalnum() or c in ("_", "-", ".") else "_" for c in filename])