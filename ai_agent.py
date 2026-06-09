import google.generativeai as genai

# Your Gemini API Key
API_KEY = "YOUR_REAL_API_KEY"

# Configure API
genai.configure(api_key=API_KEY)

# Load Gemini model
model = genai.GenerativeModel(
    "gemini-pro"
)

def generate_recommendation(data):

    recommendation = """
# AI Procurement Insights

## Best Vendor Recommendation

The system recommends the highest-ranked vendor based on weighted procurement scoring.

Key factors considered:
- Pricing efficiency
- Delivery performance
- Warranty coverage
- Support quality

--------------------------------------------------

## Trade-Off Analysis

### Low-Cost Vendors

Advantages:
- Lower procurement spending
- Better cost efficiency

Disadvantages:
- Slower delivery timelines
- Limited support services

### Premium Vendors

Advantages:
- Faster delivery
- Better warranty support
- Strong customer service

Disadvantages:
- Higher procurement cost

--------------------------------------------------

## Procurement Risks

The system identifies:

- High delivery delay risks
- Expensive quotations
- Lower support ratings
- Reduced warranty coverage

These risks help procurement teams make informed decisions.

--------------------------------------------------

## Negotiation Suggestions

Recommended strategies:

- Request bulk-order discounts
- Negotiate delivery timelines
- Ask for extended warranty coverage
- Request additional support services

--------------------------------------------------

## Explainable AI Decision

Vendor ranking uses weighted procurement evaluation:

- Price → 40%
- Delivery Speed → 25%
- Warranty → 20%
- Support Quality → 15%

This ensures transparent and explainable procurement decision-making.

--------------------------------------------------

## Final Decision

The vendor with the highest score is selected as the most suitable procurement partner based on procurement efficiency, business value, and risk analysis.
"""

    return recommendation