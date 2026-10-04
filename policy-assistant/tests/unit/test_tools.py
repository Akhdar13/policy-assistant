"""Unit tests for policy-assistant tools."""

from app.tools import check_expense_limit


def test_check_expense_limit_meals_zurich() -> None:
    result = check_expense_limit("meals", "Zurich")
    assert result == "Maximum daily allowance is $120."


def test_check_expense_limit_meals_other_city() -> None:
    result = check_expense_limit("meals", "Paris")
    assert result == "Standard daily allowance is $75."


def test_check_expense_limit_other_category() -> None:
    result = check_expense_limit("lodging", "Zurich")
    assert result == "Receipt required; approval needed for expenses over $500."
