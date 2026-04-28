import sys
import os
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.vibefinder import run_vibefinder

# Predefined test cases
TEST_CASES = [
    {
        "name": "Happy Pop Test",
        "mood": "happy",
        "genre": "pop",
        "energy": 0.8,
        "expected_mood": "happy",
        "expected_genre": "pop"
    },
    {
        "name": "Chill Jazz Test",
        "mood": "chill",
        "genre": "jazz",
        "energy": 0.3,
        "expected_mood": "chill",
        "expected_genre": "jazz"
    },
    {
        "name": "Energetic Rock Test",
        "mood": "energetic",
        "genre": "rock",
        "energy": 0.9,
        "expected_mood": "energetic",
        "expected_genre": "rock"
    },
    {
        "name": "Sad R&B Test",
        "mood": "sad",
        "genre": "r&b",
        "energy": 0.4,
        "expected_mood": "sad",
        "expected_genre": "r&b"
    },
    {
        "name": "Focused Classical Test",
        "mood": "focused",
        "genre": "classical",
        "energy": 0.5,
        "expected_mood": "focused",
        "expected_genre": "classical"
    }
]

def run_eval():
    print("=" * 60)
    print("VibeFinder 2.0 — Evaluation Harness")
    print("=" * 60)

    passed = 0
    failed = 0
    results = []

    for i, test in enumerate(TEST_CASES, 1):
        print(f"\nTest {i}: {test['name']}")
        try:
            result = run_vibefinder(test["mood"], test["genre"], test["energy"])

            # Check 1: recommendations returned
            has_recommendations = len(result["recommendations"]) > 0

            # Check 2: explanation generated
            has_explanation = len(result["explanation"]) > 0

            # Check 3: wiki context retrieved
            has_wiki = len(result["wiki_context"]) > 0

            # Check 4: rag context retrieved
            has_rag = len(result["rag_context"]) > 0

            # Confidence score (0-1 based on how many checks passed)
            checks = [has_recommendations, has_explanation, has_wiki, has_rag]
            confidence = round(sum(checks) / len(checks), 2)

            status = "PASS" if all(checks) else "FAIL"
            if status == "PASS":
                passed += 1
            else:
                failed += 1

            results.append({
                "test": test["name"],
                "status": status,
                "confidence": confidence,
                "songs_found": len(result["recommendations"])
            })

            print(f"  Status: {status}")
            print(f"  Confidence: {confidence}")
            print(f"  Songs found: {len(result['recommendations'])}")
            print(f"  Explanation: {'✓' if has_explanation else '✗'}")
            print(f"  Wiki context: {'✓' if has_wiki else '✗'}")
            print(f"  RAG context: {'✓' if has_rag else '✗'}")

        except Exception as e:
            failed += 1
            results.append({
                "test": test["name"],
                "status": "FAIL",
                "confidence": 0.0,
                "error": str(e)
            })
            print(f"  Status: FAIL")
            print(f"  Error: {str(e)}")

    # Summary
    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(TEST_CASES)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    avg_confidence = round(sum(r["confidence"] for r in results) / len(results), 2)
    print(f"Average confidence: {avg_confidence}")
    print("=" * 60)

if __name__ == "__main__":
    run_eval()

