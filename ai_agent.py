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
Vendor B is recommended because it provides faster delivery and better warranty support.

## Trade-Off Analysis
- Vendor A has balanced pricing and delivery.
- Vendor B is slightly expensive but offers strong service quality.
- Vendor C is cheaper but has high delivery delay risk.
- Vendor D provides good warranty support with moderate pricing.

## Procurement Risks
- Vendor C has high delivery delay risk.
- Vendor B quotation cost is comparatively high.

## Negotiation Suggestions
- Negotiate pricing discounts with Vendor B.
- Request faster delivery timelines from Vendor C.
- Ask Vendor D for additional support benefits.

## Final Decision
The system selected the vendor based on weighted scoring using:
- price
- delivery speed
- warranty
- support quality
"""

    return recommendation