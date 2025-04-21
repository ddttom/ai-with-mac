import openai
import math
import os
from pprint import pprint
from dotenv import load_dotenv  # Import the function

# Load environment variables from .env file
load_dotenv()

# Set your API key from environment variable (safer than hardcoding)
# This will now find the key loaded from .env
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Example query with a factual question
query = "What is the capital of Canada?"

# Make the API call with logprobs enabled
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ],
    logprobs=True,
    top_logprobs=3,
    max_tokens=25,
    temperature=0  # Use deterministic sampling for consistency
)

# Extract answer and log probabilities
answer = response.choices[0].message.content
logprobs_data = response.choices[0].logprobs

print(f"Question: {query}")
print(f"Answer: {answer}")
print("\nToken-by-token analysis:")

# Calculate average confidence
total_logprob = 0
token_count = 0

# Process each token
for token_info in logprobs_data.content:
    token = token_info.token
    token_logprob = token_info.logprob
    token_prob = math.exp(token_logprob)  # Convert log probability to probability

    # Get alternative tokens
    alternatives = {t.token: math.exp(t.logprob) for t in token_info.top_logprobs}

    # Only process non-whitespace tokens for better analysis
    if token.strip():
        total_logprob += token_logprob
        token_count += 1

        print(f"\nToken: '{token}'")
        print(f"Confidence: {token_prob:.4f} (logprob: {token_logprob:.4f})")

        # Print top alternatives
        print("Top alternatives:")
        for alt_token, alt_prob in sorted(alternatives.items(), key=lambda x: x[1], reverse=True):
            if alt_token != token:  # Skip the selected token
                print(f"  '{alt_token}': {alt_prob:.4f}")

# Calculate overall confidence metrics
if token_count > 0:
    avg_logprob = total_logprob / token_count
    avg_prob = math.exp(avg_logprob)

    print("\nOverall confidence metrics:")
    print(f"Average token logprob: {avg_logprob:.4f}")
    print(f"Average token probability: {avg_prob:.4f}")

    # Interpret confidence
    if avg_prob > 0.9:
        confidence_level = "Very high confidence"
    elif avg_prob > 0.7:
        confidence_level = "High confidence"
    elif avg_prob > 0.5:
        confidence_level = "Moderate confidence"
    else:
        confidence_level = "Low confidence"

    print(f"Confidence assessment: {confidence_level}")