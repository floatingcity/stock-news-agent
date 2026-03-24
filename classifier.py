import json
from pathlib import Path
from typing import Iterable


RULES_PATH = Path(__file__).with_name("sentiment_rules.json")


def load_rules() -> dict:
    with RULES_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def match_priority_pattern(headline: str, rules: dict) -> str | None:
    normalized = normalize_text(headline)
    for item in rules.get("priority_patterns", []):
        pattern = normalize_text(str(item.get("pattern", "")))
        sentiment = str(item.get("sentiment", "")).strip().title()
        if pattern and pattern in normalized and sentiment in {"Positive", "Negative", "Neutral"}:
            return sentiment
    return None


def count_keyword_matches(headline: str, keywords: Iterable[str]) -> int:
    normalized = normalize_text(headline)
    return sum(1 for kw in keywords if normalize_text(str(kw)) in normalized)


def classify_headline(headline: str, rules: dict) -> str:
    priority_sentiment = match_priority_pattern(headline, rules)
    if priority_sentiment:
        return priority_sentiment

    positive_score = count_keyword_matches(headline, rules.get("positive", []))
    negative_score = count_keyword_matches(headline, rules.get("negative", []))
    neutral_score = count_keyword_matches(headline, rules.get("neutral", []))

    if positive_score > negative_score:
        return "Positive"
    if negative_score > positive_score:
        return "Negative"

    if neutral_score > 0:
        return "Neutral"

    tie_break = rules.get("tie_break_rules", {})
    if tie_break.get("prefer_negative_on_risk_words", True):
        risk_words = {"risk", "risks", "lawsuit", "investigation", "probe", "warning"}
        if count_keyword_matches(headline, risk_words) > 0:
            return "Negative"

    return "Neutral"


def classify_headlines(headlines: list[str]) -> list[dict[str, str]]:
    rules = load_rules()
    results: list[dict[str, str]] = []

    for headline in headlines:
        if not headline or not headline.strip():
            continue

        sentiment = classify_headline(headline, rules)
        results.append({
            "headline": headline.strip(),
            "sentiment": sentiment,
        })

    return results
