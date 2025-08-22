import io
import os
import random
from datetime import datetime
from typing import Any, Dict, Optional
try:
	import torch
	_HAS_TORCH = True
except Exception:
	_HAS_TORCH = False
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

try:
	from diffusers import DiffusionPipeline
	_HAS_DIFFUSERS = True
except Exception:
	_HAS_DIFFUSERS = False

load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
def _draw_gradient_background(img, draw, width, height):
	for y in range(height):
		ratio = y / height
		r = int(20 + (60 - 20) * ratio)
		g = int(25 + (45 - 25) * ratio)
		b = int(35 + (85 - 35) * ratio)
		draw.line([(0, y), (width, y)], fill=(r, g, b))


def _draw_geometric_elements(img, draw, width, height):
	colors = [(100, 180, 255, 60), (255, 100, 150, 40), (150, 255, 150, 50)]
	for i in range(3):
		x = random.randint(width // 4, 3 * width // 4)
		y = random.randint(height // 6, height // 3)
		radius = random.randint(50, 120)
		color = colors[i]
		circle_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
		circle_draw = ImageDraw.Draw(circle_img)
		circle_draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
		img_rgba = img.convert('RGBA')
		img_rgba = Image.alpha_composite(img_rgba, circle_img)
		img = img_rgba.convert('RGB')
	return img


def _wrap_text(text, font, max_width):
	words = text.split()
	lines = []
	current_line = ""
	for word in words:
		test_line = current_line + (" " if current_line else "") + word
		bbox = font.getbbox(test_line)
		text_width = bbox[2] - bbox[0]
		if text_width <= max_width:
			current_line = test_line
		else:
			if current_line:
				lines.append(current_line)
			current_line = word
	if current_line:
		lines.append(current_line)
	return lines[:4]


def _get_font(size=24):
	font_paths = [
		"C:/Windows/Fonts/arial.ttf",
		"C:/Windows/Fonts/calibri.ttf",
		"C:/Windows/Fonts/segoeui.ttf",
		"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
		"/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
		"/System/Library/Fonts/Helvetica.ttc",
		"/Library/Fonts/Arial.ttf",
	]
	for font_path in font_paths:
		try:
			if os.path.exists(font_path):
				return ImageFont.truetype(font_path, size)
		except Exception:
			continue
	return ImageFont.load_default()


def _generate_synthetic_image(prompt: str, width: int, height: int) -> bytes:
	img = Image.new("RGB", (width, height), color=(20, 25, 35))
	draw = ImageDraw.Draw(img)
	for _ in range(1):
		_draw_gradient_background(img, draw, width, height)
	img = _draw_geometric_elements(img, draw, width, height)
	overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
	overlay_draw = ImageDraw.Draw(overlay)
	text_area_height = height // 3
	overlay_draw.rectangle([0, height - text_area_height, width, height], fill=(10, 15, 25, 180))
	img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
	subtitle_font = _get_font(size=min(width // 30, 24))
	small_font = _get_font(size=min(width // 40, 16))
	text = (prompt or "AI Demo")[0:100]
	draw = ImageDraw.Draw(img)
	draw.text((30, 20), "AI PORTFOLIO PROJECT", fill=(200, 210, 230), font=subtitle_font)
	wrapped = _wrap_text(text, subtitle_font, width - 60)
	y = height - text_area_height + 40
	for line in wrapped:
		draw.text((30, y), line, fill=(240, 245, 255), font=subtitle_font)
		y += 35
	draw.text((30, height - 30), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fill=(160, 170, 190), font=small_font)
	draw.text((width - 200, height - 30), "Python • PIL • AI", fill=(100, 180, 255), font=small_font)
	buf = io.BytesIO()
	img.save(buf, format="PNG", quality=95)
	return buf.getvalue()


def generate_image(params: Dict[str, Any]) -> Optional[bytes]:
	prompt = params.get("prompt", "demo")
	width = int(params.get("width", 768))
	height = int(params.get("height", 768))

	if _HAS_DIFFUSERS and _HAS_TORCH and HUGGINGFACE_TOKEN:
		try:
			device = "cuda" if torch.cuda.is_available() else "cpu"
			print(f"🚀 Using device: {device}")
			if device == "cuda":
				print(f"🎮 GPU: {torch.cuda.get_device_name()}")
			pipe = DiffusionPipeline.from_pretrained(
				"runwayml/stable-diffusion-v1-5",
				use_safetensors=True,
				token=HUGGINGFACE_TOKEN,
			)
			pipe = pipe.to(device)
			image = pipe(prompt).images[0]
			buf = io.BytesIO()
			image.save(buf, format="PNG")
			return buf.getvalue()
		except Exception:
			pass

	# fallback to local synthetic image when external generation isn't available
	return _generate_synthetic_image(prompt, width, height)