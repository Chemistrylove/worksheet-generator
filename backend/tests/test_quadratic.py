import pytest

from app.generators.quadratic import (
    generate_quadratic_equation,
    verify_quadratic_equation,
)


DIFFICULTIES = ["easy", "medium", "hard"]


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_generated_problem_has_expected_shape(difficulty):
    problem = generate_quadratic_equation(difficulty)
    assert problem["type"] == "quadratic_equation"
    assert isinstance(problem["answer"], list)
    assert len(problem["answer"]) == 2


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_generated_problems_are_self_consistent(difficulty):
    for _ in range(200):
        problem = generate_quadratic_equation(difficulty)
        a, b, c = problem["a"], problem["b"], problem["c"]
        for root in problem["answer"]:
            result = a * (root ** 2) + b * root + c
            assert abs(result) < 1e-6, f"Root {root} did not satisfy equation"


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_leading_coefficient_never_zero(difficulty):
    """a=0 would make it linear, not quadratic — must never happen."""
    for _ in range(200):
        problem = generate_quadratic_equation(difficulty)
        assert problem["a"] != 0


def test_invalid_difficulty_raises():
    with pytest.raises(ValueError):
        generate_quadratic_equation("impossible")


def test_verify_accepts_correct_roots():
    # x^2 - 5x + 6 = 0  ->  roots 2 and 3
    assert verify_quadratic_equation(a=1, b=-5, c=6, claimed_roots=[2, 3]) is True


def test_verify_accepts_roots_in_either_order():
    assert verify_quadratic_equation(a=1, b=-5, c=6, claimed_roots=[3, 2]) is True


def test_verify_rejects_incorrect_roots():
    assert verify_quadratic_equation(a=1, b=-5, c=6, claimed_roots=[1, 4]) is False


def test_verify_rejects_a_equal_zero():
    assert verify_quadratic_equation(a=0, b=-5, c=6, claimed_roots=[2, 3]) is False


def test_verify_rejects_negative_discriminant():
    # x^2 + 1 = 0 has no real roots
    assert verify_quadratic_equation(a=1, b=0, c=1, claimed_roots=[0, 0]) is False