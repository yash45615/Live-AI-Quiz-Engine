from app.services.session_service import generate_session_code
from app.services.scoring_service import calculate_score


def test_session_code_length():

    code = generate_session_code()

    assert len(code) == 6


def test_session_code_is_uppercase():

    code = generate_session_code()

    assert code == code.upper()


def test_correct_fast_answer():

    score = calculate_score(
        "A",
        "A",
        5
    )

    assert score == 1000


def test_correct_slow_answer():

    score = calculate_score(
        "A",
        "A",
        40
    )

    assert score == 600


def test_wrong_answer():

    score = calculate_score(
        "B",
        "A",
        5
    )

    assert score == 0