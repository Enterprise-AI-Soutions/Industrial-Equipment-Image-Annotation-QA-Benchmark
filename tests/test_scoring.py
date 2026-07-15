from src.quality_scoring import calculate_quality_score


def test_perfect_score():

    score = calculate_quality_score(
        iou=1.0,
        duplicate=False,
        valid_schema=True
    )

    assert score == 100


def test_duplicate_penalty():

    score = calculate_quality_score(
        iou=0.95,
        duplicate=True,
        valid_schema=True
    )

    assert score < 100
