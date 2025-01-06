import streamlit as st
import pandas as pd
from utils.data_processing import parse_file
from utils.calculations import calculate_metrics
from utils.llm_analysis import generate_insights
from utils.visualization import plot_metrics
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="H:\\Property UnderWriting\\.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize session state for inputs
basic_inputs = ["offer_price", "total_income", "total_expenses", "equity", "debt_service"]
additional_inputs = [
    "market_rent", "cash_on_cash_return", "projected_cap_rate_at_sale",
    "breakeven_occupancy", "year_built", "num_units", "unit_mix",
    "occupancy_rate_trends", "market_growth_rate", "price_per_unit",
    "average_in_place_rent", "submarket_trends", "employment_growth_rate",
    "crime_rate", "school_ratings", "renovation_cost", "capex",
    "holding_period", "rent_variation", "expense_variation",
    "parking_income", "laundry_income", "tenant_type"
]

# Initialize session states
for input_name in basic_inputs + additional_inputs:
    if input_name not in st.session_state:
        st.session_state[input_name] = 0.0 if input_name not in ["unit_mix", "submarket_trends", "tenant_type"] else ""

if "data" not in st.session_state:
    st.session_state["data"] = None

if "metrics" not in st.session_state:
    st.session_state["metrics"] = None

# Streamlit app starts here
st.title("UnderwritePro")
st.write("Provide detailed inputs for a comprehensive analysis and actionable insights.")

# File Upload
uploaded_file = st.file_uploader("Upload a file (Excel or CSV) (Optional)", type=["xlsx", "csv"])

# Inputs - Basic Metrics
st.header("Basic Metrics")
st.session_state["offer_price"] = st.number_input(
    "Enter Offer Price ($)", min_value=0.0, value=st.session_state["offer_price"], step=1000.0
)
st.session_state["total_income"] = st.number_input(
    "Enter Total Income ($)", min_value=0.0, value=st.session_state["total_income"], step=1000.0
)
st.session_state["total_expenses"] = st.number_input(
    "Enter Total Expenses ($)", min_value=0.0, value=st.session_state["total_expenses"], step=1000.0
)
st.session_state["equity"] = st.number_input(
    "Enter Equity ($) (Optional)", min_value=0.0, value=st.session_state["equity"], step=1000.0
)
st.session_state["debt_service"] = st.number_input(
    "Enter Debt Service ($) (Optional)", min_value=0.0, value=st.session_state["debt_service"], step=1000.0
)

# Inputs - Property Overview
with st.expander("Property Overview (Optional)"):
    st.session_state["year_built"] = st.slider(
        "Year Built (Optional)", min_value=1800, max_value=2100, value=int(st.session_state["year_built"])
    )
    st.session_state["num_units"] = st.slider(
        "Number of Units (Optional)", min_value=0, max_value=1000, value=int(st.session_state["num_units"])
    )
    st.session_state["unit_mix"] = st.text_input(
        "Unit Mix (Optional)", value=st.session_state["unit_mix"], help="e.g., 1B1B: 10 units, 2B2B: 5 units"
    )
    st.session_state["price_per_unit"] = st.number_input(
        "Price Per Unit ($) (Optional)", min_value=0.0, value=st.session_state["price_per_unit"], step=100.0
    )
    st.session_state["average_in_place_rent"] = st.number_input(
        "Average In-Place Rent ($) (Optional)", min_value=0.0, value=st.session_state["average_in_place_rent"], step=50.0
    )

# Inputs - Market Analysis
with st.expander("Market Analysis (Optional)"):
    st.session_state["submarket_trends"] = st.text_area(
        "Submarket Trends (Optional)", value=st.session_state["submarket_trends"], 
        help="Provide details on local market conditions and comparable properties."
    )
    st.session_state["employment_growth_rate"] = st.slider(
        "Employment Growth Rate (%) (Optional)", min_value=-100, max_value=100, value=int(st.session_state["employment_growth_rate"])
    )
    st.session_state["crime_rate"] = st.slider(
        "Crime Rate (%) (Optional)", min_value=0, max_value=100, value=int(st.session_state["crime_rate"])
    )
    st.session_state["school_ratings"] = st.slider(
        "School Ratings (1-10) (Optional)", min_value=1, max_value=10, value=int(st.session_state["school_ratings"])
    )

# Inputs - Financial Metrics
with st.expander("Financial Metrics (Optional)"):
    st.session_state["cash_on_cash_return"] = st.slider(
        "Cash-on-Cash Return (%) (Optional)", min_value=-100, max_value=100, value=int(st.session_state["cash_on_cash_return"])
    )
    st.session_state["projected_cap_rate_at_sale"] = st.slider(
        "Projected Cap Rate at Sale (%) (Optional)", min_value=0.0, max_value=100.0, value=st.session_state["projected_cap_rate_at_sale"], step=0.1
    )
    st.session_state["breakeven_occupancy"] = st.slider(
        "Breakeven Occupancy Rate (%) (Optional)", min_value=0, max_value=100, value=int(st.session_state["breakeven_occupancy"])
    )
    st.session_state["renovation_cost"] = st.number_input(
        "Total Renovation Costs ($) (Optional)", min_value=0.0, value=st.session_state["renovation_cost"], step=1000.0
    )
    st.session_state["capex"] = st.number_input(
        "Capital Expenditures (CapEx) ($) (Optional)", min_value=0.0, value=st.session_state["capex"], step=1000.0
    )

# Inputs - Tenant and Revenue Analysis
with st.expander("Tenant and Revenue Analysis (Optional)"):
    st.session_state["tenant_type"] = st.selectbox(
        "Primary Tenant Type (Optional)", 
        ["Family-Oriented", "Students", "Working Professionals", "Retirees"], index=0
    )
    st.session_state["parking_income"] = st.number_input(
        "Parking Income ($) (Optional)", min_value=0.0, value=st.session_state["parking_income"], step=100.0
    )
    st.session_state["laundry_income"] = st.number_input(
        "Laundry Income ($) (Optional)", min_value=0.0, value=st.session_state["laundry_income"], step=50.0
    )

# Sensitivity Analysis
with st.expander("Sensitivity Analysis (Optional)"):
    st.session_state["rent_variation"] = st.slider(
        "Rent Variation (%)", min_value=-50, max_value=50, value=0, step=5, help="Simulate changes in rent levels."
    )
    st.session_state["expense_variation"] = st.slider(
        "Expense Variation (%)", min_value=-50, max_value=50, value=0, step=5, help="Simulate changes in expense levels."
    )

# Button to Analyze
st.divider()
if st.button("Analyze"):
    try:
        # Parse file if uploaded
        if uploaded_file:
            required_columns = ["Income", "Expenses"]
            optional_columns = [
                "Equity", "Debt Service", "Occupancy Rate", "Market Rent", 
                "CapEx", "Year Built", "Units", "Market Growth Rate", "Price Per Unit"
            ]
            result = parse_file(uploaded_file, required_columns, optional_columns)
            st.session_state["data"] = result["data"]
            st.write("Uploaded Data Preview:")
            st.dataframe(st.session_state["data"].head())
        else:
            # Manual input fallback
            st.session_state["data"] = pd.DataFrame({
                "Income": [st.session_state["total_income"]],
                "Expenses": [st.session_state["total_expenses"]]
            })

        # Calculate metrics
        additional_inputs = {key: st.session_state[key] for key in additional_inputs}
        st.session_state["metrics"] = calculate_metrics(st.session_state["data"], st.session_state["offer_price"], additional_inputs)

        # Display results
        st.write("Calculated Metrics:")
        st.json(st.session_state["metrics"])

        # Insights
        if OPENAI_API_KEY:
            insight_type = st.selectbox(
                "Select Insight Type",
                ["general", "improvement", "risk analysis", "investment potential"],
                key="insight_type"
            )
            insights = generate_insights(st.session_state["metrics"], model="gpt-4", insight_type=insight_type)
            st.write("LLM-Generated Insights:")
            st.text(insights)
        else:
            st.error("OpenAI API key not set. Please check your configuration.")

        # Visualization
        chart_type = st.selectbox("Select Chart Type", ["bar", "pie", "line"], key="chart_type")
        plot_metrics(st.session_state["metrics"], chart_type=chart_type)

    except Exception as e:
        st.error(f"Error during analysis: {e}")
