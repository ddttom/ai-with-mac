# OpenAI Confidence Score Analyzer

This tool extracts and analyzes token-level confidence scores from OpenAI's language models. By examining the logprobs (log probabilities) returned by the API, you can gain insights into how confident the model is about each part of its response, with a special focus on meaning-bearing words.

## Problem Solved

When working with AI models, understanding their confidence is crucial for:

1. **Reliability assessment**: Identifying when a model might be guessing vs. when it's confident
2. **Uncertainty detection**: Finding parts of responses that may need human verification
3. **Model behavior analysis**: Understanding how the model decides between different options
4. **Quality control**: Setting thresholds for acceptable confidence levels in production systems
5. **Meaning-focused evaluation**: Distinguishing between confidence in structural elements (stop words, punctuation) and confidence in key concepts

## The Challenge - Misleading Overall Confidence

Overall confidence scores can be misleading. LLMs often show high confidence in grammatical structure, common words, and punctuation, which can mask uncertainty in the meaningful, content-bearing terms that actually convey information.

Our tool addresses this by:

- Filtering out stop words and punctuation to focus on meaning-bearing tokens
- Identifying tokens with confidence below a customizable threshold
- Showing alternative tokens the model considered
- Providing both the original response and a version with stop words removed

## How It Works

The script:

1. Sends a query to OpenAI's API with logprobs and top alternatives enabled
2. Extracts token-by-token confidence scores
3. Filters out common stop words and punctuation to focus on meaningful content
4. Identifies low-confidence key concepts (below customizable threshold)
5. Shows alternative tokens the model considered for each low-confidence token
6. Calculates overall confidence based on these key concepts
7. Provides the final answer both with and without stop words

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
import os
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

We define stop words and punctuation to filter out non-meaningful tokens:

```python
# More comprehensive set of stop words
stop_words = {
    "of", "the", "and", "a", "is", "in", "it", "to", ",", ".", "at", "when",
    # ... (more stop words)
}
punctuation = {".", "!", "?", ",",":","-","_","(",")","[","]","{","}","'","\"","*","+","=","/","\\","|","@","#","$","%","^","&","~","`","<",">"}

# Combine stop words and punctuation into a single set
filtered_words = stop_words.union(punctuation)
```

Then it makes an API call with logprobs and top alternatives enabled:

```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ],
    logprobs=True,
    top_logprobs=top_n_alternatives + 1,  # Get one extra to filter the current token
    max_tokens=150,
    temperature=0
)
```

The script processes each token's confidence, focusing on meaningful words:

```python
for token_info in logprobs_data.content:
    token = token_info.token.strip().lower()
    token_prob = math.exp(token_info.logprob)

    if token and token not in filtered_words and token_prob < low_confidence_threshold:
        # Process low confidence tokens that aren't stop words or punctuation
        alternatives = {
            t.token.strip(): math.exp(t.logprob)
            for t in token_info.top_logprobs
            if t.token.strip().lower() != token and t.token.strip().lower() not in filtered_words
        }
        # Analysis code...
```

And finally provides the answer with stop words removed:

```python
# Generate final answer with stop words removed
answer_without_stopwords = " ".join([word for word in answer.lower().split() if word not in stop_words])
print(f"\nFinal Answer (Stop words removed): {answer_without_stopwords}")
```

## Troubleshooting

### "Unexpected keyword argument 'proxies'" Error

This error occurs when the OpenAI client receives proxy configuration it doesn't support. The solution is to:

1. Create a clean httpx client with no proxy settings
2. Pass this client explicitly to the OpenAI client
3. This bypasses any global proxy settings that might be causing issues

## Example Output

```terminal
Question: Explain why water boils at a lower temperature when heated more intensely at the same altitude?

Answer: When water is heated more intensely, it absorbs more energy, which increases the kinetic energy of the water molecules. This causes the water molecules to move faster and eventually reach a point where they have enough energy to overcome the intermolecular forces holding them together in the liquid state. This is when the water starts to boil and turn into vapor.

At higher altitudes, the atmospheric pressure is lower compared to sea level. This lower pressure means there are fewer air molecules pressing down on the surface of the water. As a result, it requires less energy for the water molecules to overcome the reduced pressure and transition into the vapor phase. This is why water boils at a lower temperature at higher altitudes.

Potentially Less Confident Key Concepts (Confidence < 0.60):

Token: 'absorbs' (Confidence: 0.5003)
  Alternatives: 'means': 0.0988, 'reaches': 0.0983, 'gains': 0.0921
------------------------------
Token: 'energy' (Confidence: 0.4422)
  Alternatives: 'heat': 0.3087, 'thermal': 0.2488, 'kinetic': 0.0002
------------------------------
Token: 'eventually' (Confidence: 0.2143)
  Alternatives: 'collide': 0.1350, 'break': 0.1136
------------------------------
[... more tokens ...]

Confidence Level (based on potentially less confident key concepts): Low

Final Answer (Stop words removed): water heated more intensely, absorbs more energy, increases kinetic energy water molecules. causes water molecules move faster eventually reach point enough energy overcome intermolecular forces holding them together liquid state. water starts boil turn vapor. higher altitudes, atmospheric pressure lower compared sea level. lower pressure means fewer air molecules pressing surface water. result, requires less energy water molecules overcome reduced pressure transition vapor phase. water boils lower temperature higher altitudes.
```

## Key Insights

Analysis of this output reveals:

- 14 key tokens had confidence below our threshold of 0.6
- The average confidence of these key tokens was only 0.47
- 43.6% of the words in the response were stop words or punctuation
- Despite the flawed premise of the question, the model produced a seemingly coherent answer
- The lowest confidence tokens were in core physical concepts like "eventually" (0.21) and "energy" (0.44)

## Future Enhancements

- Visualization of confidence scores across different token types
- Database storage for tracking confidence over time and across domains
- Customizable stopword lists for domain-specific analysis
- Comparative analysis between different OpenAI models
- Integration with fact-checking systems to correlate confidence with factual accuracy
- Automatic detection of topics where models show systematic uncertainty

## License

MIT
