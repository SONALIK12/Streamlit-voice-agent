# 🎙️ Streamlit Voice Chat Agent (Azure OpenAI)

A fully functional voice-enabled AI assistant built with Streamlit that listens to your voice, processes it with Azure OpenAI's models, and responds back in voice.

![Voice Chat Agent](https://via.placeholder.com/800x400.png?text=Voice+Chat+Agent)

## ✨ Features

- 🎤 **Voice Input**: Record audio directly from your browser
- 🗣️ **Speech-to-Text**: Converts your voice to text using Azure OpenAI Whisper
- 🤖 **AI Processing**: Intelligent responses powered by Azure OpenAI GPT-4
- 🔊 **Text-to-Speech**: AI responses converted to natural-sounding voice
- ☁️ **Azure Integration**: Enterprise-ready with Azure OpenAI Service
- 🎨 **Clean UI**: Simple and intuitive Streamlit interface

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or later
- Azure OpenAI Service resource ([Create one here](https://portal.azure.com))
- Deployed models in Azure OpenAI Studio:
  - **Whisper** deployment for speech-to-text
  - **GPT-4** (or GPT-3.5) deployment for chat
  - **TTS** deployment for text-to-speech

### Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Azure OpenAI credentials:**

   Create a `.env` file in the project directory (see `.env.example` for template):
   ```bash
   AZURE_OPENAI_API_KEY=your_azure_openai_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   
   # Your deployment names from Azure OpenAI Studio
   AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4
   AZURE_OPENAI_WHISPER_DEPLOYMENT=whisper
   AZURE_OPENAI_TTS_DEPLOYMENT=tts
   ```

4. **Get your Azure OpenAI credentials:**

   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to your Azure OpenAI resource
   - Find **Keys and Endpoint** in the left menu
   - Copy your **Key** and **Endpoint**
   - Note your **deployment names** from Azure OpenAI Studio

### Running the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🎯 How to Use

1. **Click** the "🎤 Start Recording" button
2. **Speak** your question or message clearly
3. **Click** "⏹️ Stop Recording" when done
4. **Wait** for the AI to transcribe, process, and respond
5. **Listen** to the AI's voice response

## 🛠️ Technologies Used

- **Streamlit**: Web interface framework
- **Azure OpenAI Service**: Enterprise-grade AI models
- **Azure OpenAI Whisper**: Speech-to-text conversion
- **Azure OpenAI GPT-4**: Language model for intelligent responses
- **Azure OpenAI TTS**: Text-to-speech conversion
- **streamlit-mic-recorder**: Audio recording component

## ⚙️ Configuration

### Setting Up Azure OpenAI Deployments

1. Go to [Azure OpenAI Studio](https://oai.azure.com/)
2. Navigate to **Deployments**
3. Create the following deployments:
   - **Whisper**: Use model `whisper`
   - **GPT-4**: Use model `gpt-4` or `gpt-35-turbo`
   - **TTS**: Use model `tts` or `tts-hd`
4. Note the deployment names and add them to your `.env` file

### Available Voice Options

You can change the voice in `app.py` by modifying the `voice` parameter:
- `alloy` - Neutral and balanced
- `echo` - Warm and expressive
- `fable` - British accent
- `onyx` - Deep and authoritative
- `nova` - Energetic and friendly (default)
- `shimmer` - Soft and gentle

### Azure OpenAI Models

- **Speech-to-Text**: Whisper deployment
- **Language Model**: GPT-4 or GPT-3.5-Turbo deployment
- **Text-to-Speech**: TTS or TTS-HD deployment

## 📋 Project Structure

```
voice-agent/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .env.example       # Example environment file
└── README.md          # This file
```

## 🐛 Troubleshooting

### Import Errors
The import error for `streamlit_mic_recorder` is normal before installation. Run:
```bash
pip install -r requirements.txt
```

### Microphone Not Working
- Ensure your browser has microphone permissions
- Check that your microphone is properly connected
- Try using Chrome or Edge (best compatibility)

### Azure OpenAI Errors

**"Missing Azure OpenAI configuration"**
- Make sure you created a `.env` file (not just `.env.example`)
- Verify all required variables are set: `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`

**"Deployment not found"**
- Check your deployment names in Azure OpenAI Studio
- Make sure they match the names in your `.env` file
- Deployments must be active and not deleted

**"Authentication failed"**
- Verify your API key is correct (check Azure Portal → Keys and Endpoint)
- Ensure your endpoint URL is correct (should include `https://` and end with `/`)

**"Model not available"**
- Confirm your Azure OpenAI resource has access to the required models
- Some models require special access approval from Microsoft
- You may need to request quota increase for certain models

## 💡 Future Enhancements

- [ ] Conversation history
- [ ] Multiple voice options selector
- [ ] Language translation
- [ ] Continuous conversation mode
- [ ] Background music/effects
- [ ] Avatar with lip-sync
- [ ] MCP tool calling integration
- [ ] Export conversation transcripts

## 📝 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## ⚠️ Important Notes

- This app requires an active internet connection
- Azure OpenAI Service usage will incur costs based on your usage and pricing tier
- Make sure to keep your API key secure and never commit `.env` to version control
- Azure OpenAI offers enterprise features like private endpoints, managed identities, and compliance certifications
- Check [Azure OpenAI Pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) for cost details

## 🔗 Useful Links

- [Azure OpenAI Service Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Azure OpenAI Studio](https://oai.azure.com/)
- [Azure Portal](https://portal.azure.com)
- [Model Availability by Region](https://learn.microsoft.com/azure/ai-services/openai/concepts/models)
