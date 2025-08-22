import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

NOCODB_BASE_URL = os.getenv("NOCODB_BASE_URL")
NOCODB_API_TOKEN = os.getenv("NOCODB_API_TOKEN")


def is_configured() -> bool:
	return bool(NOCODB_BASE_URL and NOCODB_API_TOKEN)


def upload_bytes(filename: str, content: bytes) -> Optional[Dict[str, Any]]:
	"""Upload in-memory bytes to NocoDB storage if configured."""
	if not is_configured():
		return None
	try:
		url = f"{NOCODB_BASE_URL}/api/v2/storage/upload"
		headers = {"xc-token": NOCODB_API_TOKEN}
		files = {"file": (filename, content, "image/png")}
		resp = requests.post(url, headers=headers, files=files, timeout=30)
		resp.raise_for_status()
		return resp.json()
	except Exception:
		return None