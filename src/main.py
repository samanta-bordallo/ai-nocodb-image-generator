import argparse
import os
from datetime import datetime

from dotenv import load_dotenv

from .prompts_service import get_prompt
from .ai_service import generate_image
from .nocodb_client import upload_bytes, is_configured as nocodb_enabled

load_dotenv()


def ensure_out_dir() -> str:
	out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "out")
	os.makedirs(out_dir, exist_ok=True)
	return out_dir


def main():
	parser = argparse.ArgumentParser(description="Minimal AI + API + NocoDB demo")
	parser.add_argument("--character", default="demo_character")
	args = parser.parse_args()

	character = args.character
	prompt_data = get_prompt(character)
	if not prompt_data:
		print(f"No prompt found for character '{character}'. Configure NocoDB or data/prompts.json")
		return

	print(f"Using prompt: {prompt_data.get('prompt', '')[:80]}...")
	image_bytes = generate_image({
		"character": character,
		"prompt": prompt_data.get("prompt", ""),
		"negative_prompt": prompt_data.get("negative_prompt", ""),
		"width": int(prompt_data.get("width", 768)),
		"height": int(prompt_data.get("height", 768)),
		"num_inference_steps": int(prompt_data.get("num_inference_steps", 25)),
		"guidance_scale": float(prompt_data.get("guidance_scale", 6.5)),
		"sampler": prompt_data.get("sampler", ""),
		"upscaler": prompt_data.get("upscaler", ""),
	})
	if not image_bytes:
		print("Image generation failed")
		return

	out_dir = ensure_out_dir()
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	filename = f"{character}_{timestamp}.png"
	out_path = os.path.join(out_dir, filename)
	with open(out_path, "wb") as f:
		f.write(image_bytes)
	print(f"Saved: {out_path}")

	if nocodb_enabled():
		upload_resp = upload_bytes(filename, image_bytes)
		if upload_resp:
			print("Uploaded to NocoDB storage:", upload_resp)
		else:
			print("Failed to upload to NocoDB (optional)")


if __name__ == "__main__":
	main()