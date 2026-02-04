import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

base_endpoint = os.getenv('AZURE_OPENAI_TTS_ENDPOINT')
base_key = os.getenv('AZURE_OPENAI_TTS_API_KEY') or os.getenv('AZURE_OPENAI_API_KEY')
current_dep = os.getenv('AZURE_OPENAI_TTS_DEPLOYMENT') or 'tts'

names = []
for cand in [current_dep, 'tts', 'tts-001', 'tts-hd', 'tts-hd-001']:
    if cand and cand not in names:
        names.append(cand)

versions = []
for cand in [os.getenv('AZURE_OPENAI_TTS_API_VERSION') or '', '2025-03-01-preview', '2024-10-21', '2024-08-01-preview', '2024-06-01', '2023-12-01-preview']:
    if cand and cand not in versions:
        versions.append(cand)

print('Endpoint:', base_endpoint)
print('Trying deployment names:', names)
print('Trying API versions:', versions)

for ver in versions:
    client = AzureOpenAI(api_key=base_key, api_version=ver, azure_endpoint=base_endpoint)
    for name in names:
        try:
            print(f"\nTesting name='{name}' with api_version='{ver}'...")
            resp = client.audio.speech.create(model=name, voice='nova', input='Hello from TTS test')
            data = resp.read()
            print(f"SUCCESS: name={name} version={ver} bytes={len(data)}")
            print('\nSUGGESTED .env updates:')
            print('AZURE_OPENAI_TTS_DEPLOYMENT=' + name)
            print('AZURE_OPENAI_TTS_API_VERSION=' + ver)
            raise SystemExit(0)
        except Exception as e:
            msg = str(e)
            print('FAIL:', msg[:300])

print('\nNo working combination found. Please verify the TTS deployment name in Azure OpenAI Studio (Model deployments → Deployment name).')
