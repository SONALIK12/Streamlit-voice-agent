"""
Check available models in your Azure OpenAI resource
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

print("=" * 70)
print("Checking your Azure OpenAI Resource...")
print("=" * 70)

# Try to list models/deployments
url = f"{endpoint}openai/deployments?api-version={api_version}"

headers = {
    "api-key": api_key
}

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        deployments = data.get("data", [])
        
        if deployments:
            print(f"\n✅ Found {len(deployments)} deployment(s):\n")
            for dep in deployments:
                print(f"  📦 Deployment Name: {dep.get('id')}")
                print(f"     Model: {dep.get('model')}")
                print(f"     Status: {dep.get('status')}")
                print()
            
            print("=" * 70)
            print("\n✏️  Update your .env file with these deployment names:")
            for dep in deployments:
                model = dep.get('model', '').lower()
                dep_name = dep.get('id')
                if 'gpt' in model:
                    print(f"AZURE_OPENAI_CHAT_DEPLOYMENT={dep_name}")
                elif 'whisper' in model:
                    print(f"AZURE_OPENAI_WHISPER_DEPLOYMENT={dep_name}")
                elif 'tts' in model:
                    print(f"AZURE_OPENAI_TTS_DEPLOYMENT={dep_name}")
        else:
            print("\n⚠️  No deployments found!")
            print("\n📝 You need to create deployments first:")
            print("   1. Go to Azure Portal: https://portal.azure.com/")
            print("   2. Search for 'sonaliopenai'")
            print("   3. Click on your Azure OpenAI resource")
            print("   4. Look for 'Model deployments' in the left menu")
            print("   5. Click 'Create' or 'Manage Deployments'")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")

print("\n" + "=" * 70)
print("📖 INSTRUCTIONS:")
print("=" * 70)
print("To create deployments:")
print("  1. Go to: https://portal.azure.com/")
print("  2. Find your 'sonaliopenai' resource")
print("  3. Click 'Model deployments' (or 'Go to Azure OpenAI Studio')")
print("  4. Create these deployments:")
print("     • GPT-4 or GPT-3.5-Turbo")
print("     • Whisper")
print("     • TTS")
print("=" * 70)
