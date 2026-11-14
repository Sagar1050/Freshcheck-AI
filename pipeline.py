
import json

from ai_engine import extract_claims
from web_verifier import search_claim
from claim_verifier import verify_claim


def clean_json(content):
    """Remove Markdown code fences and parse JSON."""

    content = content.strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0].strip()

    return json.loads(content)


def run_freshcheck(answer):

    print("\n========== FRESHCHECK AI ==========")

    # STEP 1: Extract claims
    print("\n[1/3] Extracting factual claims...")

    extracted = extract_claims(answer)
    data = clean_json(extracted)
    print("\nDEBUG - Original answer:")
    print(repr(answer))

    print("\nDEBUG - Gemini extraction response:")
    print(repr(extracted))

    print("\nDEBUG - Parsed JSON:")
    print(data)
    
     
    claims = data.get("claims", [])

    if not claims:
        print("No factual claims found.")
        return {
            "project": "FreshCheck AI",
            "summary": {
                "total_claims": 0,
                "verified_claims": 0,
                "average_freshness_score": None,
                "supported": 0,
                "contradicted": 0,
                "potentially_outdated": 0,
                "insufficient_evidence": 0,
                "verification_errors": 0
            },
            "claim_reports": []
        }

    print(f"Successfully extracted {len(claims)} claims.")


    # STEP 2: Search and verify every claim
    print("\n[2/3] Searching and verifying claims...")

    reports = []

    for index, claim in enumerate(claims, start=1):

        print(f"\n--- Claim {index}/{len(claims)} ---")
        print("Claim:", claim)

        try:
            evidence = search_claim(claim)

            if not evidence:
                reports.append({
                    "claim": claim,
                    "verdict": "Insufficient Evidence",
                    "freshness_score": None,
                    "explanation": "No web evidence was retrieved.",
                    "suggested_correction": "",
                    "evidence_used": []
                })
                continue

            result = verify_claim(claim, evidence)

            report = {
                "claim": claim,
                **result
            }

            reports.append(report)

            print("Verdict:", result["verdict"])
            print("Freshness Score:", result["freshness_score"])

        except Exception as error:

            print("Verification error:", error)

            reports.append({
                "claim": claim,
                "verdict": "Verification Error",
                "freshness_score": None,
                "explanation": str(error),
                "suggested_correction": "",
                "evidence_used": []
            })

    # STEP 3: Generate combined report
    print("\n[3/3] Generating final report...")

    scored_reports = [
        item for item in reports
        if isinstance(item.get("freshness_score"), (int, float))
    ]

    average_score = (
        round(
            sum(item["freshness_score"] for item in scored_reports)
            / len(scored_reports),
            2
        )
        if scored_reports else None
    )

    summary = {
        "total_claims": len(claims),
        "verified_claims": len(scored_reports),
        "average_freshness_score": average_score,
        "supported": sum(
            item["verdict"] == "Supported" for item in reports
        ),
        "contradicted": sum(
            item["verdict"] == "Contradicted" for item in reports
        ),
        "potentially_outdated": sum(
            item["verdict"] == "Potentially Outdated" for item in reports
        ),
        "insufficient_evidence": sum(
            item["verdict"] == "Insufficient Evidence" for item in reports
        ),
        "verification_errors": sum(
            item["verdict"] == "Verification Error" for item in reports
        )
    }

    final_report = {
        "project": "FreshCheck AI",
        "summary": summary,
        "claim_reports": reports
    }

    print("\n========== FINAL FRESHCHECK REPORT ==========")
    print(json.dumps(final_report, indent=4, ensure_ascii=False))

    # Save report to a JSON file
    with open("freshcheck_report.json", "w", encoding="utf-8") as file:
        json.dump(final_report, file, indent=4, ensure_ascii=False)

    print("\nReport saved as freshcheck_report.json")
    return final_report


if __name__ == "__main__":

    sample_answer = """
    Python 3.12 was released on October 2, 2023.
    Python 3.13 was released on October 7, 2024.
    Python 3.14 was released on October 7, 2025.
    """

    run_freshcheck(sample_answer)
