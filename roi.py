"""Utility functions for ROI calculations."""


def calculate_roi(purchase_price: float, renovation_cost: float, annual_rent: float, annual_expenses: float) -> float:
    """Return ROI percentage given investment details."""
    total_investment = purchase_price + renovation_cost
    annual_return = annual_rent - annual_expenses
    if total_investment == 0:
        return 0
    return (annual_return / total_investment) * 100
