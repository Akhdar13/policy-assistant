"""Tools for policy-assistant agent."""


def check_expense_limit(category: str, location: str) -> str:
    """Checks the expense policy limit for a given category and location.

    Args:
        category: The expense category (e.g., 'meals', 'lodging', 'travel').
        location: The city or location where the expense occurred.

    Returns:
        A string describing the expense allowance or requirement.
    """
    if category.strip().lower() == "meals":
        if location.strip().lower() == "zurich":
            return "Maximum daily allowance is $120."
        return "Standard daily allowance is $75."
    return "Receipt required; approval needed for expenses over $500."
