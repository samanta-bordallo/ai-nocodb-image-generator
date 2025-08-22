# 🎨 AI Image Generator

A modern web application that generates AI-powered images using Stable Diffusion v1.5. Features a beautiful frontend interface with real-time image generation, prompt management via NocoDB, and GPU acceleration support.

## ✨ Features

- **🤖 Real AI Generation**: Uses Hugging Face's Stable Diffusion v1.5 for authentic AI-generated images
- **🎯 Custom Prompts**: Write your own descriptions or use the "Surprise Me!" feature
- **📊 NocoDB Integration**: Fetch random prompts from your NocoDB database
- **⚡ GPU Acceleration**: Automatically detects and uses CUDA GPU for faster generation
- **📱 Responsive Design**: Modern, mobile-friendly interface
- **💾 Download & Share**: Save generated images or share them easily
- **🔄 Fallback System**: Graceful degradation with synthetic images if AI generation fails

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- CUDA-compatible GPU (optional, but recommended for speed)
- Hugging Face account and API token

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ai-nocodb-image-generator.git
   cd ai-nocodb-image-generator
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   ```bash
   cp env.example .env
   # Edit .env with your tokens
   ```

5. **Start the application**

   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Required: Hugging Face Token

1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens)
2. Create a new token with **Read** permissions
3. Add it to your `.env` file:
   ```
   HUGGINGFACE_TOKEN=your_token_here
   ```

### Optional: NocoDB Setup

For the "Surprise Me!" feature, configure NocoDB:

1. Create a NocoDB project
2. Create a table with columns: `prompt`, `character` (optional)
3. Add your credentials to `.env`:
   ```
   NOCODB_BASE_URL=https://your-project.nocodb.com
   NOCODB_API_TOKEN=your_token_here
   NOCODB_TABLE_ID=your_table_id_here
   ```

## 🏗️ Project Structure

```
ai-nocodb-image-generator/
├── src/
│   ├── ai_service.py      # Core AI image generation logic
│   ├── prompts_service.py # NocoDB and local prompt management
│   ├── nocodb_client.py   # NocoDB API integration
│   └── main.py           # CLI interface for testing
├── app.py                # Flask web server
├── index.html            # Frontend interface
├── styles.css            # Modern styling
├── script.js             # Frontend JavaScript
├── requirements.txt      # Python dependencies
├── env.example           # Environment template
└── README.md            # This file
```

## 🎮 Usage

### Web Interface

1. **Custom Generation**: Type your prompt and click "Generate Image"
2. **Surprise Me**: Click to get a random prompt from NocoDB or local fallback
3. **Download**: Save your generated image
4. **Share**: Share the image link

### Command Line

```bash
# Generate with custom prompt
python -m src.main --character "my_prompt"

# Generate with default prompt
python -m src.main
```

## 🔍 Technical Details

### AI Model

- **Model**: Stable Diffusion v1.5 (runwayml/stable-diffusion-v1-5)
- **Framework**: Hugging Face Diffusers
- **Device**: Automatic CUDA/CPU detection
- **Resolution**: Configurable (256x256 to 1024x1024)

### Performance

- **GPU**: ~43 seconds for 768x768 (RTX 3060)
- **CPU**: ~2-3 minutes for 768x768
- **Memory**: ~4GB VRAM required for GPU mode

### Security

- Tokens stored in `.env` file (not committed to Git)
- Frontend communicates via secure API endpoints
- No sensitive data exposed in client-side code

## 🛠️ Development

### Running in Development Mode

```bash
python app.py
```

The Flask server runs with debug mode enabled for development.

### Testing the Backend

```bash
cd src
python main.py
```

### Adding New Features

1. Backend logic goes in `src/` modules
2. Frontend updates in `index.html`, `styles.css`, `script.js`
3. API endpoints in `app.py`

## 📝 Learning Journey

This project demonstrates my journey into AI engineering and web development. As someone new to the field, I built this to learn:

- **AI Integration**: Working with Hugging Face APIs and Stable Diffusion
- **Full-Stack Development**: Flask backend with modern frontend
- **API Design**: RESTful endpoints and error handling
- **Database Integration**: NocoDB for prompt management
- **Performance Optimization**: GPU acceleration and fallback systems

The project shows practical application of these concepts in a real, working application rather than just theoretical knowledge.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the Stable Diffusion model
- [NocoDB](https://nocodb.com/) for the database platform
- [Flask](https://flask.palletsprojects.com/) for the web framework

---

**Built with ❤️ by Samanta Bordallo**
