# OpenAI Confidence Score Analyzer

This tool extracts and analyzes token-level confidence scores from OpenAI's language models. By examining the logprobs (log probabilities) returned by the API, you can gain insights into how confident the model is about each part of its response.

## Problem Solved

When working with AI models, understanding their confidence is crucial for:

1. **Reliability assessment**: Identifying when a model might be guessing vs. when it's confident
2. **Uncertainty detection**: Finding parts of responses that may need human verification
3. **Model behavior analysis**: Understanding how the model decides between different options
4. **Quality control**: Setting thresholds for acceptable confidence levels in production systems

## How It Works

The script:

1. Sends a query to OpenAI's API with logprobs enabled
2. Extracts token-by-token confidence scores
3. Calculates overall confidence metrics
4. Provides a human-readable confidence assessment

## Requirements

- Python 3.7+
- OpenAI Python client v1.x
- dotenv
- httpx

## Installation

```bash
pip install openai python-dotenv httpx
```

## Usage

Create a `.env` file with your OpenAI API key:

```bash
OPENAI_API_KEY=your-api-key-here
```

Run the script:

```bash
python confidence.py
```

## Code Explanation

The core of the script creates an OpenAI client with a clean HTTP client configuration:

```python
import openai
import math
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.environ.get("OPENAI_API_KEY")

# Create a clean httpx client with no proxy settings
http_client = httpx.Client()

# Create the OpenAI client with an explicit http_client
client = openai.OpenAI(
    api_key=api_key,
    http_client=http_client
)
```

Then it makes an API call with logprobs enabled:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ],
    logprobs=True,
    top_logprobs=3,
    max_tokens=25,
    temperature=0
)
```

The script processes each token's confidence:

```python
for token_info in logprobs_data.content:
    token = token_info.token
    token_logprob = token_info.logprob
    token_prob = math.exp(token_logprob)
    
    alternatives = {t.token: math.exp(t.logprob) for t in token_info.top_logprobs}
    
    # Analysis code...
```

And calculates overall confidence metrics:

```python
avg_logprob = total_logprob / token_count
avg_prob = math.exp(avg_logprob)
```

## Troubleshooting

### "Unexpected keyword argument 'proxies'" Error

This error occurs when the OpenAI client receives proxy configuration it doesn't support. The solution is to:

1. Create a clean httpx client with no proxy settings
2. Pass this client explicitly to the OpenAI client
3. This bypasses any global proxy settings that might be causing issues

## Example Output

```terminal
Question: What is the capital of Canada?
Answer: The capital of Canada is Ottawa.

Token-by-token analysis:

Token: 'The'
Confidence: 0.8634 (logprob: -0.1469)
Top alternatives:
  'Ottawa': 0.0721
  'Canada': 0.0245

Token: 'capital'
Confidence: 0.9856 (logprob: -0.0146)
Top alternatives:
  ' capital': 0.0112
  ' Capital': 0.0021

...

Overall confidence metrics:
Average token logprob: -0.0285
Average token probability: 0.9719
Confidence assessment: Very high confidence
```

## Future Enhancements

- Visualization of confidence scores
- Database storage for tracking confidence over time
- Threshold filtering for low-confidence tokens
- Support for analyzing different types of queries
- Comparative analysis between different OpenAI models

## License

MIT
