"""
Test Azure OpenAI deployments one by one
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
print("Testing Azure OpenAI Deployments")
print("=" * 70)
print(f"Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"API Version: {os.getenv('AZURE_OPENAI_API_VERSION')}")
print("=" * 70)

# Test 1: Chat deployment
print("\n🧪 Test 1: Testing GPT-4.1 deployment...")
try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": "Say 'Hello, I am working!'"}],
        max_tokens=50
    )
    print(f"✅ GPT-4.1 deployment works!")
    print(f"   Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ GPT-4.1 deployment failed: {str(e)}")

# Test 2: Test with alternative API versions
print("\n🧪 Test 2: Trying different API versions...")
api_versions = ["2024-10-21", "2024-08-01-preview", "2024-02-15-preview", "2023-12-01-preview"]

for api_ver in api_versions:
    try:
        test_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=api_ver,
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        response = test_client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=10
        )
        print(f"✅ API version {api_ver} works!")
        print(f"   Update your .env with: AZURE_OPENAI_API_VERSION={api_ver}")
        break
    except Exception as e:
        print(f"❌ API version {api_ver} failed: {str(e)[:100]}")

print("\n" + "=" * 70)
