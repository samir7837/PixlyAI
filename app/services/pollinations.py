import os
import urllib.parse
import requests

POLLINATIONS_BASE_URL = os.getenv("POLLINATIONS_BASE_URL", "https://image.pollinations.ai/prompt/")

def generate_image_bytes(prompt: str, timeout: int = 60) -> bytes:
    if not prompt:
        raise ValueError("Prompt is empty")

    encoded = urllib.parse.quote(prompt, safe="")
    url = POLLINATIONS_BASE_URL.rstrip("/") + "/" + encoded

    resp = requests.get(url, timeout=timeout)
    if resp.status_code != 200:
        raise RuntimeError(f"Pollinations request failed: {resp.status_code} {resp.text[:200]}")

    content_type = resp.headers.get("Content-Type", "")
    if content_type and content_type.startswith("image/"):
        return resp.content

    
    text = resp.text or ""
    import re
    m = re.search(r'<img[^>]+src="([^"]+)"', text)
    if m:
        img_url = m.group(1)
        r2 = requests.get(img_url, timeout=timeout)
        if r2.status_code == 200 and r2.headers.get("Content-Type", "").startswith("image/"):
            return r2.content
        raise RuntimeError("Image URL fetched but failed to fetch image bytes.")
    raise RuntimeError("Pollinations returned non-image content and no image could be extracted.")