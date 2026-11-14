
import requests

url = "http://localhost:8080/v1/chat/completions"

payload = {
    "model": "gemini/gemini-3.5-flash-lite",
    "messages": [
        {
            "role": "user",
            "content": "Say hello to FreshCheck AI and explain your role in one sentence."
        }
    ],
    "max_tokens": 150
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=60
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()

    result = response.json()
    print("\nSUCCESS! Bifrost and Gemini are connected.")

except requests.exceptions.RequestException as error:
    print("\nConnection failed:", error)
