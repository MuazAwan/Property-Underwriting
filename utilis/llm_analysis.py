import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_insights(metrics, model="gpt-4", insight_type="general"):
    """
    Generate insights using OpenAI Chat API.

    Args:
        metrics: Dictionary of financial metrics.
        model: OpenAI model to use (default: "gpt-4").
        insight_type: Type of insights to generate (e.g., "general", "improvement", "risk analysis", "investment potential").
    
    Returns:
        str: Generated insights.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is not set. Please check your .env file.")
    
    openai.api_key = OPENAI_API_KEY

    # Construct prompt dynamically
    prompt = f"Analyze the following financial metrics and property details:\n{metrics}\n\n"

    # Add dynamic insight type handling
    if insight_type == "general":
        prompt += "Provide a general analysis of the financial health and performance of the property."
    elif insight_type == "improvement":
        prompt += "Suggest ways to improve these metrics and optimize property performance."
    elif insight_type == "risk analysis":
        prompt += "Identify potential risks associated with these metrics and propose mitigation strategies."
    elif insight_type == "investment potential":
        prompt += "Evaluate the investment potential of this property based on these metrics."
    else:
        prompt += "Provide useful insights related to these metrics."

    # Include detailed context for OpenAI analysis
    prompt += (
        "\nConsider factors such as Net Operating Income (NOI), Cap Rate, "
        "Cash-on-Cash Return, Debt Service Coverage Ratio (DSCR), Breakeven Occupancy, "
        "Year Built, Number of Units, Market Rent, and market trends in your analysis. "
        "Additionally, evaluate sensitivity to rent variations, expense changes, and "
        "amenities such as parking and laundry income."
    )

    try:
        # Generate the response from OpenAI
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a financial analysis assistant specializing in real estate underwriting."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=700,  # Increased to allow for more detailed insights
            temperature=0.5,  # Balanced creativity
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.InvalidRequestError as e:
        raise ValueError(f"OpenAI API request error: {e}")
    except openai.error.AuthenticationError:
        raise ValueError("Invalid OpenAI API key. Please check your configuration.")
    except openai.error.APIError as e:
        raise ValueError(f"OpenAI API error: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error: {e}")
