def calculate_metrics(data, offer_price, additional_inputs=None):
    """
    Calculate financial metrics such as NOI, Cap Rate, Cash on Cash Return, DSCR, and others.
    
    Args:
        data: DataFrame containing financial data (Income, Expenses, etc.).
        offer_price: Purchase price of the property.
        additional_inputs: Dictionary containing additional data like equity, debt service, and other parameters.
    
    Returns:
        dict: A dictionary containing calculated financial metrics.
    """
    try:
        # Extract basic data
        income = data.get('Income', []).sum()
        expenses = data.get('Expenses', []).sum()
        noi = income - expenses

        # Basic metrics
        cap_rate = (noi / offer_price) * 100 if offer_price > 0 else 0

        # Additional metrics
        equity = additional_inputs.get("Equity", 0) if additional_inputs else 0
        debt_service = additional_inputs.get("Debt Service", 0) if additional_inputs else 0
        market_rent = additional_inputs.get("Market Rent", 0)
        num_units = additional_inputs.get("Number of Units", 0)
        cash_on_cash_return = (noi / equity) * 100 if equity > 0 else 0
        dscr = noi / debt_service if debt_service > 0 else 0
        breakeven_occupancy = (expenses / income) * 100 if income > 0 else 0
        projected_cap_rate_at_sale = additional_inputs.get("Projected Cap Rate at Sale", 0)
        market_growth_rate = additional_inputs.get("Market Growth Rate", 0)

        # Tenant and Income Analysis
        parking_income = additional_inputs.get("Parking Income", 0)
        laundry_income = additional_inputs.get("Laundry Income", 0)
        other_income = parking_income + laundry_income

        # Per Unit Metrics
        rent_per_unit = (income / num_units) if num_units > 0 else 0
        expense_per_unit = (expenses / num_units) if num_units > 0 else 0

        # Market Comparison (if Market Rent is provided)
        rent_gap = (market_rent - rent_per_unit) if market_rent > 0 and rent_per_unit > 0 else 0
        rent_gap_percentage = (rent_gap / market_rent) * 100 if market_rent > 0 else 0

        # Sensitivity Analysis
        rent_variation = additional_inputs.get("Rent Variation", 0)
        expense_variation = additional_inputs.get("Expense Variation", 0)
        adjusted_income = income * (1 + rent_variation / 100)
        adjusted_expenses = expenses * (1 + expense_variation / 100)
        adjusted_noi = adjusted_income - adjusted_expenses

        # Compile metrics into a dictionary
        metrics = {
            "NOI": noi,
            "Cap Rate (%)": cap_rate,
            "Cash on Cash Return (%)": cash_on_cash_return,
            "DSCR": dscr,
            "Breakeven Occupancy (%)": breakeven_occupancy,
            "Rent Per Unit ($)": rent_per_unit,
            "Expense Per Unit ($)": expense_per_unit,
            "Rent Gap ($)": rent_gap,
            "Rent Gap (%)": rent_gap_percentage,
            "Projected Cap Rate at Sale (%)": projected_cap_rate_at_sale,
            "Market Growth Rate (%)": market_growth_rate,
            "Parking Income ($)": parking_income,
            "Laundry Income ($)": laundry_income,
            "Other Income ($)": other_income,
            "Adjusted NOI ($)": adjusted_noi,
            "Adjusted Income ($)": adjusted_income,
            "Adjusted Expenses ($)": adjusted_expenses,
        }

        # Filter out metrics with invalid values (e.g., negative or infinite)
        metrics = {key: round(value, 2) if value >= 0 else 0 for key, value in metrics.items()}
        
        return metrics
    except KeyError as e:
        raise ValueError(f"Missing required column in the data: {e}")
    except Exception as e:
        raise ValueError(f"Error calculating metrics: {e}")
