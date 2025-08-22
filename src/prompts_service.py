import json
import os
import random
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

NOCODB_BASE_URL = os.getenv("NOCODB_BASE_URL")  
NOCODB_API_TOKEN = os.getenv("NOCODB_API_TOKEN")
NOCODB_TABLE_ID = os.getenv("NOCODB_TABLE_ID") 

LOCAL_PROMPTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "prompts.json")


def _get_prompt_from_local(character: str) -> Optional[Dict[str, Any]]:
	try:
		with open(LOCAL_PROMPTS_PATH, "r", encoding="utf-8") as f:
			data = json.load(f)
			prompts = data.get("prompts", [])
			candidates = [p for p in prompts if p.get("character") == character] or prompts
			return random.choice(candidates) if candidates else None
	except Exception:
		return None


def get_prompt(character: str) -> Optional[Dict[str, Any]]:
	"""Return a prompt object for a character. Tries NocoDB first (if configured), then local JSON."""
	if NOCODB_BASE_URL and NOCODB_API_TOKEN and NOCODB_TABLE_ID:
		api_url = f"{NOCODB_BASE_URL}/api/v2/tables/{NOCODB_TABLE_ID}/records"
		headers = {"xc-token": NOCODB_API_TOKEN}
		try:
			resp = requests.get(api_url, headers=headers, timeout=20)
			resp.raise_for_status()
			data = resp.json()
			records = data.get("list", [])
			if records:
				# Try to find by character if exists; else pick random
				filtered = []
				for rec in records:
					payload = rec.get("Prompts") or rec
					if not isinstance(payload, dict):
						continue
					if payload.get("character") == character:
						filtered.append(payload)
				selected = random.choice(filtered or [r.get("Prompts") or r for r in records])
				return {
					"character": selected.get("character", character),
					"prompt": selected.get("prompt") or selected.get("Prompt", ""),
					"negative_prompt": selected.get("negative_prompt", ""),
					"width": int(selected.get("width", 768)),
					"height": int(selected.get("height", 768)),
					"num_inference_steps": int(selected.get("num_inference_steps", 25)),
					"guidance_scale": float(selected.get("guidance_scale", 6.5)),
					"sampler": selected.get("sampler", ""),
					"upscaler": selected.get("upscaler", ""),
				}
		except Exception:
			pass
	# Fallback to local
	return _get_prompt_from_local(character)