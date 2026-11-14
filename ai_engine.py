
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BIFROST_URL = os.getenv(
    "BIFROST_BASE_URL",
    "http://localhost:8080"
)

BIFROST_MODEL = os.getenv(
    "BIFROST_MODEL",
    "gemini/gemini-3.5-flash-lite"
)


def extract_claims(answer):
    url = f"{BIFROST_URL}/v1/chat/completions"

    prompt = f"""
You are a factual claim extraction assistant.

Extract the individual verifiable factual claims
from the following AI-generated answer.

Rules:
1. Return only factual claims.
2. Separate independent claims.
3. Ignore opinions and greetings.
4. Do not verify or correct the claims yet.
5. Return valid JSON in this format:

{{
  "claims": [
    "First factual claim",
    "Second factual claim"
  ]
}}

AI-generated answer:
{answer}
"""

    payload = {
        "model": BIFROST_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.1,
        "max_tokens": 1000
    }

    response = requests.post(
        f"{url}",
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    sample_answer = """
    Python 3.12 was released in October 2023.
    Python 3.13 was released in October 2024.
    Python is currently the most popular programming language.
    """

    print("Extracting factual claims...\n")

    claims = extract_claims(sample_answer)

    print("Extracted Claims:")
    print(claims)
