import requests
import base64
import json
from prompt import system_prompt
# Read and encode the image as base64
system_prompt = system_prompt()

image_dir = "file/test.jpg"
with open(image_dir, "rb") as f:
    image_bytes = f.read()
image_base64 = base64.b64encode(image_bytes).decode("utf-8")

# API request payload
payload = {
    "model": "gemma3:12b",   # ⚠ gemma3 is text-only; use llava:7b for image captioning
    "prompt": system_prompt,
    "images": [image_base64]
}

# Send request to local Ollama server with streaming enabled
response = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)

# # Print each line of the streamed response as it arrives

# Print only the 'response' value from each line (parsed as dict)

for line in response.iter_lines():
    if line:
        try:
            data = json.loads(line.decode("utf-8"))
            print(data.get("response", ""), end="")
        except Exception:
            pass
