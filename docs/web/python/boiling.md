# Why Confidence Scores Alone Aren't Enough for AI Truth

In Artificial Intelligence, large language models (LLMs) are becoming increasingly adept at generating human-like text. From answering complex questions to drafting creative content, their capabilities seem limitless. However, as we integrate these powerful tools into our applications, a question arises: how much can we trust their output?

One common metric used to gauge this trust is the "confidence score" provided by the model. Often presented as a probability, this score seemingly indicates how certain the AI is about the words it has generated. A high confidence score might lead us to believe the information is accurate, while a low score could raise a red flag.

But as we've explored in a recent investigation, relying solely on overall confidence scores can be misleading. Consider a scenario where we asked an LLM a question with a flawed premise: "Explain why water boils at a lower temperature when heated more intensely at the same altitude?", the code and the run are listed at the end of the blog.

Intuitively, as anyone with a basic understanding of physics knows, this premise is incorrect. The boiling point of water at a given altitude is determined by atmospheric pressure, not the intensity of the heat source. More intense heating will simply cause the water to reach its boiling point faster.

When we posed this question to GPT-3.5 (version 1.30.1) and analyzed its token-by-token confidence, we initially saw a seemingly reassuring overall confidence level. This might lead someone to believe the explanation provided was sound. However, digging deeper, we employed a technique to identify the confidence levels associated with the *meaning-bearing words* within the model's response, by filtering out high-confidence but less informative elements: both "stop words" (common link words and phrases) and punctuation marks.

## Low Confidence Where Meaning Resides

By focusing on the confidence scores of the meaning-bearing words, achieved by filtering out common, less informative phrases, link words (often called 'stop words'), and all punctuation, a different picture emerged. Our analysis identified **14 key tokens** with confidence scores below our threshold of 0.6, with an average confidence of just **0.47** across these important terms.

The most uncertain tokens were particularly telling:

- "eventually" (confidence: 0.21)
- "overcome" (confidence: 0.44)
- "energy" (confidence: 0.44)

Terms directly related to the physical processes described revealed significantly lower confidence levels compared to the more common grammatical elements and structural tokens. For instance, when the model wrote that water "absorbs more energy," its confidence in the word "absorbs" was only 0.50, with competing alternatives like "means" (0.10), "reaches" (0.10), and "gains" (0.09).

Even more revealing were cases where strongly competing alternatives existed. For the word "energy" (confidence: 0.44), the model almost equally considered "heat" (0.31) and "thermal" (0.25) as alternatives. This suggests the model was genuinely uncertain about the correct physical terminology to use.

This filtering approach is crucial because both stop words and punctuation typically receive very high confidence scores, yet contribute little to the factual substance of the response. In fact, our analysis showed that 43.6% of the total words in the response were stop words or punctuation—reducing from 133 words to just 75 meaning-bearing terms. By removing these elements from our confidence analysis, we can better isolate and assess the model's certainty about the actual concepts being discussed.

Ultimately, when we calculated the overall confidence *based solely on these potentially less certain key concepts*, the assessment shifted dramatically to **"Low"**.

## The Illusion of Certainty

This experiment highlights a critical limitation of relying on simple, overall confidence scores. An LLM can be highly confident in its grammatical structure, punctuation usage, and common connecting words, leading to a seemingly trustworthy output, even when the underlying reasoning or factual basis is weak or incorrect.

What makes this particularly concerning is that our analysis showed that nearly half (43.6%) of the words in the response were stop words or punctuation. These high-confidence structural elements can mask the uncertainty in the remaining 56.4% of words that actually carry the meaningful content.

For example, when examining the model's explanation of water molecules "breaking free" during boiling, we found multiple instances where the model wavered between key physical concepts:

- For "reach" (confidence: 0.51), it also considered "break" (0.39) and "overcome" (0.06)
- For "kinetic" energy (confidence: 0.46), it nearly equally considered "average" (0.35)
- For "transition" into vapor (confidence: 0.48), it also considered "reach" (0.19) and "turn" (0.10)

For professionals tasked with designing and implementing AI-driven solutions, this distinction is paramount. Inaccurate information, presented with a veneer of high confidence, can lead to flawed decisions and potentially harmful outcomes—especially in domains requiring technical precision.

## A More Nuanced Approach

Our exploration demonstrates the need for more sophisticated methods of evaluating the reliability of LLM outputs. By focusing on the confidence levels of key concepts, achieved through techniques like stop word and punctuation removal, we can gain a more granular understanding of where the model's certainty truly lies. This approach allows for:

- **More targeted human review:** Identifying specific areas of low confidence helps prioritize where expert scrutiny is most needed. In our example, a physicist would immediately want to examine the model's uncertain assertions about energy absorption and molecular transitions.
- **Improved system design:** Incorporating concept-level confidence analysis can lead to more robust error detection and mitigation strategies. For instance, a system could be programmed to flag responses where key scientific terms show confidence below 0.5.
- **More informed trust:** Understanding the nuances of AI confidence allows for a more realistic assessment of the reliability of the generated information. When 14 crucial terms in a physics explanation show an average confidence of only 0.47, users should approach the entire explanation with appropriate skepticism.

In conclusion, while confidence scores offer a starting point for evaluating LLM outputs, they are far from the complete picture. By moving beyond surface-level metrics and focusing on the confidence associated with the core meaning—filtering out both stop words and punctuation—we can develop a more discerning and ultimately more trustworthy relationship with these powerful AI tools. The key lies in understanding *what* the AI is confident about, not just *how* confident it sounds.

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

```

Now the run

```terminal
python scripts/confidence.py
OpenAI version: 1.30.1
Client created successfully
Question: Explain why water boils at a lower temperature when heated more intensely at the same altitude?

Answer: When water is heated more intensely, it absorbs more energy, which increases the kinetic energy of the water molecules. This causes the water molecules to move faster and eventually reach a point where they have enough energy to overcome the intermolecular forces holding them together in the liquid state. This is when the water starts to boil and turn into vapor.

At higher altitudes, the atmospheric pressure is lower compared to sea level. This lower pressure means there are fewer air molecules pressing down on the surface of the water. As a result, it requires less energy for the water molecules to overcome the reduced pressure and transition into the vapor phase. This is why water boils at a lower temperature at higher altitudes.

In summary, when water is heated more intensely, it

Potentially Less Confident Key Concepts (Confidence < 0.60):

Token: 'absorbs' (Confidence: 0.5003)
  Alternatives: 'means': 0.0988, 'reaches': 0.0983, 'gains': 0.0921
------------------------------
Token: 'more' (Confidence: 0.4959)
  Alternatives: 'heat': 0.2626, 'energy': 0.2117, 'thermal': 0.0191
------------------------------
Token: 'energy' (Confidence: 0.4422)
  Alternatives: 'heat': 0.3087, 'thermal': 0.2488, 'kinetic': 0.0002
------------------------------
Token: 'kinetic' (Confidence: 0.4611)
  Alternatives: 'average': 0.3528, 'temperature': 0.0832, 'speed': 0.0377
------------------------------
Token: 'eventually' (Confidence: 0.2143)
  Alternatives: 'collide': 0.1350, 'break': 0.1136
------------------------------
Token: 'reach' (Confidence: 0.5073)
  Alternatives: 'break': 0.3879, 'overcome': 0.0578, 'escape': 0.0381
------------------------------
Token: 'starts' (Confidence: 0.4914)
  Alternatives: 'transitions': 0.2474, 'begins': 0.0972, 'boils': 0.0726
------------------------------
Token: 'turn' (Confidence: 0.4842)
  Alternatives: 'turns': 0.3325, 'transition': 0.0683, 'transitions': 0.0407
------------------------------
Token: 'higher' (Confidence: 0.4857)
  Alternatives: 'normal': 0.0021
------------------------------
Token: 'lower' (Confidence: 0.5148)
  Alternatives: 'reduced': 0.1720, 'means': 0.1479, 'decrease': 0.1279
------------------------------
Token: 'pressing' (Confidence: 0.5219)
  Alternatives: 'pushing': 0.3624, 'above': 0.1040, 'exert': 0.0107
------------------------------
Token: 'requires' (Confidence: 0.5891)
  Alternatives: 'becomes': 0.0299, 'takes': 0.0296
------------------------------
Token: 'overcome' (Confidence: 0.4385)
  Alternatives: 'escape': 0.2844, 'break': 0.2622, 'reach': 0.0139
------------------------------
Token: 'transition' (Confidence: 0.4824)
  Alternatives: 'reach': 0.1937, 'turn': 0.0987, 'start': 0.0692
------------------------------

Confidence Level (based on potentially less confident key concepts): Low

Final Answer (Stop words removed): water heated more intensely, absorbs more energy, increases kinetic energy water molecules. causes water molecules move faster eventually reach point enough energy overcome intermolecular forces holding them together liquid state. water starts boil turn vapor. higher altitudes, atmospheric pressure lower compared sea level. lower pressure means fewer air molecules pressing surface water. result, requires less energy water molecules overcome reduced pressure transition vapor phase. water boils lower temperature higher altitudes. summary, water heated more intensely,
 
```
