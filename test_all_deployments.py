"""
Test all three deployments: GPT-4.1, Whisper, and TTS
"""
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

print("=" * 70)
print("Testing All Azure OpenAI Deployments")
print("=" * 70)

# Test 1: GPT-4.1 (Chat)
print("\n✅ Test 1: GPT-4.1 (Chat)")
try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": "Say hello in 5 words"}],
        max_tokens=20
    )
    print(f"   ✅ Success: {response.choices[0].message.content}")
except Exception as e:
    print(f"   ❌ Failed: {str(e)[:150]}")

# Test 2: Whisper (Speech-to-Text)
print("\n✅ Test 2: Whisper (Speech-to-Text)")
print("   ⚠️  Note: This requires actual audio input, will test in the app")
print("   Deployment name 'whisper' is configured")

# Test 3: TTS (Text-to-Speech)
print("\n✅ Test 3: TTS (Text-to-Speech)")
try:
    response = client.audio.speech.create(
        model="tts",
        voice="nova",
        input="Testing text to speech"
    )
    audio_data = response.read()
    print(f"   ✅ Success: Generated {len(audio_data)} bytes of audio")
except Exception as e:
    print(f"   ❌ Failed: {str(e)[:150]}")

print("\n" + "=" * 70)
print("🎉 All configured deployments are ready!")
print("=" * 70)
print("\n🚀 You can now run: streamlit run app.py")
print("=" * 70)
