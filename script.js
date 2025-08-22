// Configuration
const CONFIG = {
    API_URL: '/api/generate',
    NOCODB_BASE_URL: 'https://wsj7jcm3.nocodb.com',
    NOCODB_API_TOKEN: 'sAaRgcxQ1XH09weQxV4rtcDMV6HH2g87yAWXx3wA',
    NOCODB_TABLE_ID: 'mz68xazzeuhwshg'
};

// DOM elements
const promptInput = document.getElementById('prompt');
const widthInput = document.getElementById('width');
const heightInput = document.getElementById('height');
const generateBtn = document.getElementById('generateBtn');
const surpriseBtn = document.getElementById('surpriseBtn');
const resultSection = document.getElementById('resultSection');
const generatedImage = document.getElementById('generatedImage');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const downloadBtn = document.getElementById('downloadBtn');
const shareBtn = document.getElementById('shareBtn');

// Event listeners
generateBtn.addEventListener('click', generateImage);
surpriseBtn.addEventListener('click', surpriseMe);
downloadBtn.addEventListener('click', downloadImage);
shareBtn.addEventListener('click', shareImage);

// Generate image function
async function generateImage() {
    const prompt = promptInput.value.trim();
    const width = parseInt(widthInput.value);
    const height = parseInt(heightInput.value);

    if (!prompt) {
        showError('Please enter a prompt to generate an image.');
        return;
    }

    setLoading(true);
    hideError();

    try {
        const response = await fetch(CONFIG.API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                width: width,
                height: height
            })
        });

        const data = await response.json();

        if (data.success) {
            generatedImage.src = data.image;
            resultSection.style.display = 'block';
            hideError();
        } else {
            showError(data.error || 'Failed to generate image');
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        setLoading(false);
    }
}

// Surprise Me function
async function surpriseMe() {
    try {
        const prompt = await getRandomPromptFromNocoDB();
        if (prompt) {
            promptInput.value = prompt;
            generateImage();
        } else {
            showError('Could not fetch a random prompt. Please try again.');
        }
    } catch (error) {
        showError('Error getting random prompt: ' + error.message);
    }
}

// Get random prompt from NocoDB
async function getRandomPromptFromNocoDB() {
    const apiUrl = `${CONFIG.NOCODB_BASE_URL}/api/v2/tables/${CONFIG.NOCODB_TABLE_ID}/records`;
    const headers = { 'xc-token': CONFIG.NOCODB_API_TOKEN };

    try {
        const response = await fetch(apiUrl, { headers });
        const data = await response.json();
        
        if (data.list && data.list.length > 0) {
            const randomRecord = data.list[Math.floor(Math.random() * data.list.length)];
            const prompt = randomRecord.Prompts || randomRecord;
            return prompt.prompt || prompt.Prompt || 'A beautiful AI-generated image';
        }
    } catch (error) {
        console.log('NocoDB fallback to local prompts');
        // Fallback to local prompts
        return getRandomLocalPrompt();
    }
}

// Fallback to local prompts
function getRandomLocalPrompt() {
    const localPrompts = [
        'A serene mountain landscape at sunset',
        'A futuristic city with flying cars',
        'A magical forest with glowing mushrooms',
        'A cozy coffee shop on a rainy day',
        'A space station orbiting Earth',
        'A steampunk airship in the clouds',
        'A peaceful beach at dawn',
        'A cyberpunk street scene at night'
    ];
    return localPrompts[Math.floor(Math.random() * localPrompts.length)];
}

// Download image
function downloadImage() {
    const link = document.createElement('a');
    link.download = 'ai-generated-image.png';
    link.href = generatedImage.src;
    link.click();
}

// Share image
function shareImage() {
    if (navigator.share) {
        navigator.share({
            title: 'AI Generated Image',
            text: 'Check out this AI-generated image!',
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            alert('Link copied to clipboard!');
        });
    }
}

// Utility functions
function setLoading(loading) {
    const btnText = generateBtn.querySelector('.btn-text');
    const btnLoading = generateBtn.querySelector('.btn-loading');
    
    if (loading) {
        btnText.style.display = 'none';
        btnLoading.style.display = 'inline';
        generateBtn.disabled = true;
    } else {
        btnText.style.display = 'inline';
        btnLoading.style.display = 'none';
        generateBtn.disabled = false;
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    resultSection.style.display = 'none';
}

function hideError() {
    errorSection.style.display = 'none';
}
