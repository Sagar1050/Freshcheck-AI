
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    print("ERROR: Tavily API key not loaded from .env")
else:
    try:
        tavily = TavilyClient(api_key=api_key)

        response = tavily.search(
            query="Latest artificial intelligence news",
            max_results=3
        )

        print("SUCCESS! Tavily is connected.")
        for result in response["results"]:
            print("\nTitle:", result["title"])
            print("URL:", result["url"])

    except Exception as error:
        print("Tavily connection failed:", error)
