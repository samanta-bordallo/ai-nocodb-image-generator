from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import base64
import os
import sys

# Add src to path so we can import ai_service
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from ai_service import generate_image
from prompts_service import get_prompt

app = Flask(__name__)
CORS(app)

# Serve static files
@app.route('/')
def index():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading index.html: {str(e)}"

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# API endpoint for image generation
@app.route('/api/generate', methods=['POST'])
def api_generate():
    try:
        data = request.json
        prompt = data.get('prompt', 'A beautiful AI-generated image')
        width = int(data.get('width', 768))
        height = int(data.get('height', 768))

        print(f"🎨 Generating image: {prompt} ({width}x{height})")

        # Use the working ai_service
        image_bytes = generate_image({
            'prompt': prompt,
            'width': width,
            'height': height
        })

        # Convert to base64 for frontend
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        print("✅ Image generated successfully!")

        return jsonify({
            'success': True,
            'image': f'data:image/png;base64,{image_base64}',
            'prompt': prompt
        })

    except Exception as e:
        print(f"❌ Error generating image: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# API endpoint for random prompt
@app.route('/api/surprise', methods=['GET'])
def api_surprise():
    try:
        # Get a random prompt from NocoDB or local fallback
        prompt_data = get_prompt("random")
        
        if prompt_data and prompt_data.get('prompt'):
            return jsonify({
                'success': True,
                'prompt': prompt_data.get('prompt'),
                'character': prompt_data.get('character', 'random')
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No prompts available'
            }), 404
            
    except Exception as e:
        print(f"❌ Error getting random prompt: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting AI Image Generator Server...")
    print("📱 Frontend available at: http://localhost:5000")
    print("🔧 API endpoint: http://localhost:5000/api/generate")
    app.run(debug=True, host='0.0.0.0', port=5000)
