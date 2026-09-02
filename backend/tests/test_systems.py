import pytest

from app.generators.systems import generate_system_of_equations, verify_system


DIFFICULTIES = ["easy", "medium", "hard"]


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_generated_problem_has_expected_shape(difficulty):
    problem = generate_system_of_equations(difficulty)
    assert problem["type"] == "system_of_linear_equations"
    assert "x" in problem["answer"]
    assert "y" in problem["answer"]


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_generated_problems_are_self_consistent(difficulty):
    for _ in range(200):
        problem = generate_system_of_equations(difficulty)
        x, y = problem["answer"]["x"], problem["answer"]["y"]
        a1, b1, c1 = problem["a1"], problem["b1"], problem["c1"]
        a2, b2, c2 = problem["a2"], problem["b2"], problem["c2"]
        assert a1 * x + b1 * y == c1
        assert a2 * x + b2 * y == c2


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_equations_are_always_independent(difficulty):
    """
    The two equations must never be parallel/identical, or there'd be
    no single unique solution — that would make a broken worksheet question.
    """
    for _ in range(200):
        problem = generate_system_of_equations(difficulty)
        a1, b1 = problem["a1"], problem["b1"]
        a2, b2 = problem["a2"], problem["b2"]
        determinant = a1 * b2 - a2 * b1
        assert determinant != 0


def test_invalid_difficulty_raises():
    with pytest.raises(ValueError):
        generate_system_of_equations("impossible")


def test_verify_accepts_correct_solution():
    # x + y = 3, 3x + 2y = 8  ->  x=2, y=1
    # check: 2+1=3 ✓, 3(2)+2(1)=8 ✓
    assert verify_system(a1=1, b1=1, c1=3, a2=3, b2=2, c2=8, claimed_x=2, claimed_y=1) is True


def test_verify_rejects_incorrect_solution():
    assert verify_system(a1=3, b1=2, c1=8, a2=5, b2=-1, c2=3, claimed_x=1, claimed_y=1) is False


def test_verify_rejects_parallel_equations():
    # 2x + 4y = 6 and 1x + 2y = 3 are the same line scaled -> no unique solution
    assert verify_system(a1=2, b1=4, c1=6, a2=1, b2=2, c2=3, claimed_x=1, claimed_y=1) is False