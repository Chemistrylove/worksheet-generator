import pytest

from app.generators.linear import generate_linear_equation, verify_linear_equation


DIFFICULTIES = ["easy", "medium", "hard"]


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_generated_problem_has_expected_shape(difficulty):
    problem = generate_linear_equation(difficulty)
    assert problem["type"] == "linear_equation"
    assert problem["difficulty"] == difficulty
    assert isinstance(problem["a"], int)
    assert isinstance(problem["b"], int)
    assert isinstance(problem["c"], int)
    assert isinstance(problem["answer"], int)
    assert "problem_text" in problem


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_generated_problems_are_self_consistent(difficulty):
    """
    Loop many times since generation is random. Each generated problem
    must satisfy its own equation when we plug the answer back in.
    """
    for _ in range(200):
        problem = generate_linear_equation(difficulty)
        a, b, c, answer = problem["a"], problem["b"], problem["c"], problem["answer"]
        assert a * answer + b == c


def test_invalid_difficulty_raises():
    with pytest.raises(ValueError):
        generate_linear_equation("impossible")


def test_verify_accepts_correct_answer():
    # 3x + 5 = 20  ->  x = 5
    assert verify_linear_equation(a=3, b=5, c=20, claimed_answer=5) is True


def test_verify_rejects_incorrect_answer():
    assert verify_linear_equation(a=3, b=5, c=20, claimed_answer=4) is False


def test_verify_rejects_a_equal_zero():
    # a=0 means it's not a valid linear equation (no x term)
    assert verify_linear_equation(a=0, b=5, c=20, claimed_answer=5) is False