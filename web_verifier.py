
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

# Load Tavily API key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is missing from your .env file"
    )

tavily = TavilyClient(api_key=TAVILY_API_KEY)


# ==========================================
# 1. SOURCE CREDIBILITY CLASSIFICATION
# ==========================================

def classify_source(url):
    """
    Classify sources using validated domain names.

    These are preliminary domain-based credibility signals.
    They do not guarantee that an individual article is accurate.
    """

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            raise ValueError("Invalid URL scheme")

        hostname = parsed.hostname

        if not hostname:
            raise ValueError("Invalid hostname")

        hostname = hostname.lower().rstrip(".")

    except (ValueError, TypeError, AttributeError):
        return {
            "source_type": "Other",
            "credibility_level": "Unverified"
        }

    def matches_domain(domains):
        return any(
            hostname == domain or
            hostname.endswith("." + domain)
            for domain in domains
        )

    # Official documentation and first-party sources
    official_domains = (
        "gov",
        "gov.in",
        "gov.uk",
        "edu",
        "ac.uk",
        "python.org",
        "who.int",
        "un.org",
        "europa.eu",
        "microsoft.com",
        "developers.google.com",
        "docs.github.com"
    )

    # Research and academic publishers
    research_domains = (
        "arxiv.org",
        "nature.com",
        "sciencedirect.com",
        "springer.com",
        "ieee.org",
        "computer.org",
        "acm.org",
        "pubmed.ncbi.nlm.nih.gov",
        "cwi.nl"
    )

    # Established news publishers
    news_domains = (
        "reuters.com",
        "apnews.com",
        "bbc.com",
        "bbc.co.uk",
        "theguardian.com",
        "nytimes.com"
    )

    # Educational and technical publications
    educational_domains = (
        "pythoninstitute.org",
        "realpython.com",
        "geeksforgeeks.org",
        "udacity.com",
        "builtin.com",
        "stackoverflow.com",
        "nedbatchelder.com",
        "inventwithpython.com"
    )

    # Specific first-party biography host
    first_party_hosts = (
        "gvanrossum.github.io",
    )

    if hostname in first_party_hosts:
        return {
            "source_type": "Other",
            "credibility_level": "Medium-High"
        }

    if matches_domain(official_domains):
        return {
            "source_type": "Official",
            "credibility_level": "High"
        }

    if matches_domain(research_domains):
        return {
            "source_type": "Research",
            "credibility_level": "High"
        }

    if matches_domain(news_domains):
        return {
            "source_type": "News",
            "credibility_level": "Medium-High"
        }

    if matches_domain(educational_domains):
        return {
            "source_type": "Other",
            "credibility_level": "Medium-High"
        }

    return {
        "source_type": "Other",
        "credibility_level": "Unverified"
    }


# ==========================================
# 2. EVIDENCE RANKING
# ==========================================

def rank_evidence(evidence):
    """
    Rank evidence by source credibility first,
    followed by Tavily relevance score.
    """

    credibility_priority = {
        "High": 3,
        "Medium-High": 2,
        "Unverified": 1
    }

    def ranking_score(item):

        credibility = credibility_priority.get(
            item.get("credibility_level", "Unverified"),
            1
        )

        try:
            relevance = float(item.get("score", 0) or 0)
        except (ValueError, TypeError):
            relevance = 0.0

        return credibility, relevance

    return sorted(
        evidence,
        key=ranking_score,
        reverse=True
    )


# ==========================================
# 3. LIVE WEB SEARCH
# ==========================================

def search_claim(claim):
    """
    Search the web for evidence related to a factual claim.
    Uses Tavily advanced search and ranks the results.
    """

    print(f"\nSearching web for: {claim}")

    response = tavily.search(
        query=claim,
        search_depth="advanced",
        max_results=10
    )

    evidence = []

    for result in response.get("results", []):

        source_url = result.get("url", "")

        source_info = classify_source(source_url)

        evidence.append({
            "title": result.get("title", ""),
            "url": source_url,
            "content": result.get("content", ""),
            "score": result.get("score", 0),
            "source_type": source_info["source_type"],
            "credibility_level": source_info["credibility_level"]
        })

    # Rank the retrieved evidence
    evidence = rank_evidence(evidence)

    print("\nRanked evidence:")

    for index, item in enumerate(evidence, start=1):

        print(
            f"{index}. {item['title']} | "
            f"{item['source_type']} | "
            f"{item['credibility_level']} | "
            f"Relevance: {item['score']}"
        )

    return evidence


# ==========================================
# 4. TEST THE WEB VERIFIER
# ==========================================

if __name__ == "__main__":

    test_claim = (
        "Python 3.12 was released in October 2023."
    )

    results = search_claim(test_claim)

    print("\n========== LIVE WEB EVIDENCE ==========")

    for index, item in enumerate(results, start=1):

        print(f"\n{index}. {item['title']}")
        print("URL:", item["url"])
        print("Source Type:", item["source_type"])
        print("Credibility:", item["credibility_level"])
        print("Relevance:", item["score"])
        print("Evidence:", item["content"][:400])
