import streamlit as st
import pandas as pd
from utils.data_processing import parse_file
from utils.calculations import calculate_metrics
from utils.llm_analysis import generate_insights
from utils.visualization import plot_metrics
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from fpdf import FPDF
from PIL import Image
import openai
import streamlit as st

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
'''
# Load environment variables
load_dotenv(dotenv_path="H:\\Property UnderWriting\\.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
'''
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

if "insight_type" not in st.session_state:
    st.session_state["insight_type"] = "general"

if "chart_type" not in st.session_state:
    st.session_state["chart_type"] = "bar"

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

# Insights Type
insight_type = st.selectbox(
    "Select Insight Type",
    ["general", "improvement", "risk analysis", "investment potential"],
    index=["general", "improvement", "risk analysis", "investment potential"].index(st.session_state["insight_type"]),
    key="insight_type"
)

# Chart Type
chart_type = st.selectbox(
    "Select Chart Type", ["bar", "pie", "line"], key="chart_type"
)

# Function to plot metrics and save the graph
def plot_metrics(metrics, chart_type="bar", save_path="chart.png"):
    if not metrics or all(value == 0 for value in metrics.values()):
        st.warning("No meaningful data to plot.")
        return

    try:
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size for better readability

        if chart_type == "bar":
            ax.bar(metrics.keys(), metrics.values(), color='skyblue', edgecolor='black')
            ax.set_title("Financial Metrics", fontsize=16, fontweight='bold')
            ax.set_ylabel("Value ($)", fontsize=12)
            ax.set_xlabel("Metrics", fontsize=12)
            ax.set_xticks(range(len(metrics.keys())))
            ax.set_xticklabels(metrics.keys(), rotation=45, ha="right", fontsize=10)
            ax.grid(axis='y', linestyle='--', alpha=0.7)

        elif chart_type == "pie":
            if len(metrics) > 10:
                st.warning("Too many metrics for a pie chart. Consider using a bar or line chart.")
                return
            ax.pie(metrics.values(), labels=metrics.keys(), autopct='%1.1f%%', startangle=90)
            ax.set_title("Financial Metrics Distribution", fontsize=16, fontweight='bold')

        elif chart_type == "line":
            ax.plot(list(metrics.keys()), list(metrics.values()), marker='o', linestyle='-', linewidth=2)
            ax.set_title("Financial Metrics Over Time", fontsize=16, fontweight='bold')
            ax.set_ylabel("Value ($)", fontsize=12)
            ax.set_xlabel("Metrics", fontsize=12)
            ax.set_xticks(range(len(metrics.keys())))
            ax.set_xticklabels(metrics.keys(), rotation=45, ha="right", fontsize=10)
            ax.grid(axis='both', linestyle='--', alpha=0.7)

        fig.tight_layout()  # Adjust layout to prevent label clipping
        fig.savefig(save_path, format="png", dpi=300, bbox_inches="tight")
        plt.close(fig)
        st.image(save_path, caption="Generated Chart")
    except Exception as e:
        st.error(f"Error generating chart: {e}")

# Function to generate PDF with graph
def save_to_pdf_with_graph(metrics, insights, chart_image_path, file_name="UnderwritePro_Output.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="UnderwritePro Output Report", ln=True, align="C")
    pdf.ln(10)  # Add space

    # Metrics Section
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Calculated Metrics:", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in metrics.items():
        pdf.cell(0, 10, txt=f"{key}: {value}", ln=True)

    # Insights Section
    if insights:
        pdf.ln(10)
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="Generated Insights:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=insights)

    # Add Graph
    if chart_image_path:
        with Image.open(chart_image_path) as img:
            width, height = img.size
            aspect_ratio = height / width

        max_width = 180
        img_width = max_width
        img_height = max_width * aspect_ratio

        max_height = 200
        if img_height > max_height:
            img_height = max_height
            img_width = max_height / aspect_ratio

        pdf.ln(10)
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="Visualization:", ln=True)
        pdf.image(chart_image_path, x=10, y=None, w=img_width, h=img_height)

    pdf.output(file_name)
    return file_name

# Analyze button
if st.button("Analyze"):
    try:
        if uploaded_file:
            required_columns = ["Income", "Expenses"]
            optional_columns = ["Equity", "Debt Service", "Occupancy Rate", "Market Rent", "CapEx", "Year Built", "Units"]
            result = parse_file(uploaded_file, required_columns, optional_columns)
            st.session_state["data"] = result["data"]
            st.write("Uploaded Data Preview:")
            st.dataframe(st.session_state["data"].head())
        else:
            st.session_state["data"] = pd.DataFrame({
                "Income": [st.session_state["total_income"]],
                "Expenses": [st.session_state["total_expenses"]]
            })

        additional_inputs_dict = {key: st.session_state[key] for key in additional_inputs}
        st.session_state["metrics"] = calculate_metrics(st.session_state["data"], st.session_state["offer_price"], additional_inputs_dict)

        st.write("Calculated Metrics:")
        st.json(st.session_state["metrics"])

        if OPENAI_API_KEY:
            insights = generate_insights(st.session_state["metrics"], model="gpt-4", insight_type=insight_type)
            st.write("LLM-Generated Insights:")
            st.text(insights)
        else:
            st.error("OpenAI API key not set. Please check your configuration.")

        plot_metrics(st.session_state["metrics"], chart_type=chart_type)

    except Exception as e:
        st.error(f"Error during analysis: {e}")

# Export to PDF
if st.button("Export to PDF"):
    try:
        if st.session_state["metrics"]:
            chart_path = "chart.png"
            plot_metrics(st.session_state["metrics"], chart_type=st.session_state["chart_type"], save_path=chart_path)

            insights_text = generate_insights(st.session_state["metrics"], model="gpt-4", insight_type=insight_type) if OPENAI_API_KEY else "Insights require a valid OpenAI API key."
            pdf_file = save_to_pdf_with_graph(st.session_state["metrics"], insights_text, chart_path)

            st.success(f"PDF generated successfully: {pdf_file}")
            with open(pdf_file, "rb") as f:
                st.download_button("Download PDF", f, file_name=pdf_file)
        else:
            st.error("No metrics to export. Perform analysis first.")
    except Exception as e:
        st.error(f"Failed to generate PDF: {e}")
