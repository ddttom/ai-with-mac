import openai
import math
import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("Error: OPENAI_API_KEY environment variable not found.")
    exit(1)

print("OpenAI version:", openai.__version__)

# Create a clean httpx client with no proxy settings
http_client = httpx.Client()

# Try to create the OpenAI client with an explicit http_client
try:
    client = openai.OpenAI(
        api_key=api_key,
        http_client=http_client
    )
    print("Client created successfully")
except Exception as e:
    print(f"Error creating client: {e}")
    print(f"Error type: {type(e)}")
    exit(1)


query = "Explain why water boils at a lower temperature when heated more intensely at the same altitude?"

# More comprehensive set of stop words
stop_words = {
    "of", "the", "and", "a", "is", "in", "it", "to", ",", ".", "at", "when",
    "as", "for", "with", "on", "be", "that", "by", "this", "have", "do",
    "so", "than", "then", "however", "but", "can", "from", "into", "will",
    "was", "were", "been", "being", "had", "has", "could", "would",
    "should", "may", "might", "must", "am", "are", "shall", "ought", "did",
    "does", "having", "here", "there", "where", "which", "who", "whom",
    "whose", "what", "why", "how", "all", "any", "both", "each", "few",
    "many", "some", "these", "those", "other", "one", "two", "three",
    "first", "second", "third", "up", "down", "out", "off", "over", "under",
    "again", "further", "thence", "once", "its", "they"
}
punctuation = {".", "!", "?", ",",":","-","_","(",")","[","]","{","}","'","\"","*","+","=","/","\\","|","@","#","$","%","^","&","~","`","<",">"}

# Combine stop words and punctuation into a single set
filtered_words = stop_words.union(punctuation)

# Confidence threshold
low_confidence_threshold = 0.6

# Number of top alternatives to display
top_n_alternatives = 3

# Make the API call
try:
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

    answer = response.choices[0].message.content
    logprobs_data = response.choices[0].logprobs

    print(f"Question: {query}\n")
    print(f"Answer: {answer}\n")
    print(f"Potentially Less Confident Key Concepts (Confidence < {low_confidence_threshold:.2f}):\n")

    if logprobs_data and logprobs_data.content:
        low_confidence_keywords = []
        total_prob_low_confidence = 0
        count_low_confidence = 0

        for token_info in logprobs_data.content:
            token = token_info.token.strip().lower()
            token_prob = math.exp(token_info.logprob)

            if token and token not in filtered_words and token_prob < low_confidence_threshold:
                count_low_confidence += 1
                total_prob_low_confidence += token_prob
                alternatives = {
                    t.token.strip(): math.exp(t.logprob)
                    for t in token_info.top_logprobs
                    if t.token.strip().lower() != token and t.token.strip().lower() not in filtered_words
                }
                sorted_alternatives = sorted(alternatives.items(), key=lambda x: x[1], reverse=True)[:top_n_alternatives]

                low_confidence_keywords.append({
                    "token": token_info.token.strip(),
                    "confidence": token_prob,
                    "alternatives": sorted_alternatives
                })

        if low_confidence_keywords:
            for item in low_confidence_keywords:
                print(f"Token: '{item['token']}' (Confidence: {item['confidence']:.4f})")
                if item["alternatives"]:
                    alt_str = ", ".join(f"'{alt}': {prob:.4f}" for alt, prob in item["alternatives"])
                    print(f"  Alternatives: {alt_str}")
                print("-" * 30)

            if count_low_confidence > 0:
                average_prob_low_confidence = total_prob_low_confidence / count_low_confidence
                if average_prob_low_confidence > 0.9:
                    confidence_level = "Very high"
                elif average_prob_low_confidence > 0.7:
                    confidence_level = "High"
                elif average_prob_low_confidence > 0.5:
                    confidence_level = "Moderate"
                else:
                    confidence_level = "Low"
                print(f"\nConfidence Level (based on potentially less confident key concepts): {confidence_level}")
            else:
                print("\nNo potentially low-confidence key concepts found to determine overall confidence level.")

        else:
            print("No potentially low-confidence key concepts found.")

    else:
        print("No log probabilities data in response.")

except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")

print(f"\nFinal Answer: {answer}")

# Generate final answer with stop words removed
answer_without_stopwords = " ".join([word for word in answer.lower().split() if word not in stop_words])
print(f"\nFinal Answer (Stop words removed): {answer_without_stopwords}")