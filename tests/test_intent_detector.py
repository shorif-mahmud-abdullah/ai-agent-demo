import pytest

from src.ai.intent_detector import IntentDetector


@pytest.fixture
def detector():
    return IntentDetector()


@pytest.mark.parametrize(
    "query, expected",
    [
        ("What is my account balance?", "balance_check"),
        ("I want to withdraw my winnings", "withdrawal"),
        ("I want to recharge", "deposit"),
        ("Is my KYC approved yet?", "kyc_status"),
        ("Show my previous transactions", "transaction_history"),
        ("Do you have any bonus for new players?", "bonus"),
        ("The game is not working", "technical_issue"),
        ("Let me talk to a human", "human_request"),
        ("Tell me about the weather", "general_query"),
    ],
)
def test_detect_intent(detector, query, expected):
    assert detector.detect_intent(query) == expected


def test_detection_is_case_insensitive(detector):
    assert detector.detect_intent("WITHDRAW") == "withdrawal"


def test_general_query_has_neutral_confidence(detector):
    assert detector.get_intent_confidence("hello there", "general_query") == 0.5


def test_confidence_grows_with_more_keyword_matches(detector):
    one = detector.get_intent_confidence("kyc", "kyc_status")
    two = detector.get_intent_confidence("kyc verification", "kyc_status")
    assert two > one


def test_confidence_is_capped(detector):
    query = "kyc verification documents verify approved"
    assert detector.get_intent_confidence(query, "kyc_status") <= 0.9
