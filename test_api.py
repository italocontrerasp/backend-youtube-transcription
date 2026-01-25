import requests
import json

url = "http://127.0.0.1:8000/transcribe"

# Test case 1: Spanish (default)
payload_es = {
    "url": "https://www.youtube.com/watch?v=5MgBikgcWnY", # "Hello World" in Python
    "language": "en" # actually let's test english explicitly first as the video is likely english
}

try:
    print("Testing English Video...")
    response = requests.post(url, json=payload_es)
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        print(f"Video ID: {data['video_id']}")
        print(f"Transcript preview: {data['transcript'][:100]}...")
    else:
        print(f"Failed: {response.text}")

except Exception as e:
    print(f"Error: {e}")

# Test case 2: Default param (es) - using a likely spanish video or just verifying logic
# Let's try a clearly spanish video if possible, but for now let's just re-test with 'es' and see if it falls back or errors if video is EN
payload_default = {
    "url": "https://www.youtube.com/watch?v=5MgBikgcWnY"
    # language defaults to 'es'
}

print("\nTesting Default (Spanish) request on English video (checking fallback or error)...")
try:
    response = requests.post(url, json=payload_default)
    if response.status_code == 200:
        data = response.json()
        print("Success (likely fallback or found track)!")
        print(f"Transcript preview: {data['transcript'][:100]}...")
    else:
        print(f"Failed (Expected if no ES track and no fallback logic for strict): {response.text}")
except Exception as e:
    print(f"Error: {e}")
