# Why Confidence Scores Alone Aren't Enough for AI Truth**

In Artificial Intelligence, large language models (LLMs) are becoming increasingly adept at generating human-like text. From answering complex questions to drafting creative content, their capabilities seem limitless. However, as we integrate these powerful tools into our applications, a question arises: how much can we trust their output?

One common metric used to gauge this trust is the "confidence score" provided by the model. Often presented as a probability, this score seemingly indicates how certain the AI is about the words it has generated. A high confidence score might lead us to believe the information is accurate, while a low score could raise a red flag.

But as we've explored in a recent investigation, relying solely on overall confidence scores can be misleading. Consider a scenario where we asked an LLM a question with a flawed premise: "Explain why water boils at a lower temperature when heated more intensely at the same altitude?"

Intuitively, as anyone with a basic understanding of physics knows, this premise is incorrect. The boiling point of water at a given altitude is determined by atmospheric pressure, not the intensity of the heat source. More intense heating will simply cause the water to reach its boiling point faster.

When we posed this question to an LLM and analyzed its token-by-token confidence, we initially saw a seemingly reassuring "High" overall confidence level. This might lead someone to believe the explanation provided was sound. However, digging deeper, we employed a technique to identify the confidence levels associated with the *meaning-bearing words* within the model's response, by filtering out high-confidence but less informative "stop words" (common link words and phrases).

**Low Confidence Where Meaning Resides

By focusing on the confidence scores of the meaning-bearing words, achieved by filtering out common, less informative phrases and link words (often called 'stop words'), a different picture emerged. Terms directly related to the physical processes described – such as "absorbs," "energy," "increase," "boiling," and "pressure" – revealed significantly lower confidence levels compared to the more common grammatical elements.

Ultimately, when we calculated the overall confidence *based solely on these potentially less certain key concepts*, the assessment shifted dramatically from "High" to **"Low"**.

**The Illusion of Certainty

This experiment highlights a limitation of relying on simple, overall confidence scores. An LLM can be highly confident in its grammatical structure and common connecting words, leading to a seemingly trustworthy output, even when the underlying reasoning or factual basis is weak or incorrect.

For professionals, who are tasked with designing and implementing AI-driven solutions, this distinction is paramount. Inaccurate information, presented with a veneer of high confidence, can lead to flawed decisions and potentially harmful outcomes.

**A More Nuanced Approach

Our exploration demonstrates the need for more sophisticated methods of evaluating the reliability of LLM outputs. By focusing on the confidence levels of key concepts, achieved through techniques like stop word removal, we can gain a more granular understanding of where the model's certainty truly lies. This approach allows for:

* **More targeted human review:** Identifying specific areas of low confidence helps prioritize where expert scrutiny is most needed.  
* **Improved system design:** Incorporating concept-level confidence analysis can lead to more robust error detection and mitigation strategies.  
* **More informed trust:** Understanding the nuances of AI confidence allows for a more realistic assessment of the reliability of the generated information.

In conclusion, while confidence scores offer a starting point for evaluating LLM outputs, they are far from the complete picture. By moving beyond surface-level metrics and focusing on the confidence associated with the core meaning, we can develop a more discerning and ultimately more trustworthy relationship with these powerful AI tools. The key lies in understanding *what* the AI is confident about, not just *how* confident it sounds.

**The Python Program

Python

import openai  
import math  
import os  
import httpx  
from dotenv import load\_dotenv

\# Load environment variables  
load\_dotenv()

\# Get API key  
api\_key \= os.environ.get("OPENAI\_API\_KEY")  
if not api\_key:  
    print("Error: OPENAI\_API\_KEY environment variable not found.")  
    exit(1)

print("OpenAI version:", openai.\_\_version\_\_)

\# Create a clean httpx client with no proxy settings  
http\_client \= httpx.Client()

\# Try to create the OpenAI client with an explicit http\_client  
try:  
    client \= openai.OpenAI(  
        api\_key=api\_key,  
        http\_client=http\_client  
    )  
    print("Client created successfully")  
except Exception as e:  
    print(f"Error creating client: {e}")  
    print(f"Error type: {type(e)}")  
    exit(1)

query \= "Explain why water boils at a lower temperature when heated more intensely at the same altitude?"

\# More comprehensive set of stop words  
stop\_words \= {  
    "of", "the", "and", "a", "is", "in", "it", "to", ",", ".", "at", "when",  
    "as", "for", "with", "on", "be", "that", "by", "this", "have", "do",  
    "so", "than", "then", "however", "but", "can", "from", "into", "will",  
    "are", "was", "were", "been", "being", "had", "has", "could", "would",  
    "should", "may", "might", "must", "am", "are", "shall", "ought", "did",  
    "does", "having", "here", "there", "where", "which", "who", "whom",  
    "whose", "what", "why", "how", "all", "any", "both", "each", "few",  
    "many", "some", "these", "those", "other", "one", "two", "three",  
    "first", "second", "third", "up", "down", "out", "off", "over", "under",  
    "again", "further", "thence", "once", "its", "they"  
}

\# Confidence threshold  
low\_confidence\_threshold \= 0.6

\# Number of top alternatives to display  
top\_n\_alternatives \= 3

\# Make the API call  
try:  
    response \= client.chat.completions.create(  
        model="gpt-3.5-turbo",  
        messages=\[  
            {"role": "system", "content": "You are a helpful assistant."},  
            {"role": "user", "content": query}  
        \],  
        logprobs=True,  
        top\_logprobs=top\_n\_alternatives \+ 1,  \# Get one extra to filter the current token  
        max\_tokens=150,  
        temperature=0  
    )

    answer \= response.choices\[0\].message.content  
    logprobs\_data \= response.choices\[0\].logprobs

    print(f"Question: {query}\\n")  
    print(f"Answer: {answer}\\n")  
    print(f"Potentially Less Confident Key Concepts (Confidence \< {low\_confidence\_threshold:.2f}):\\n")

    if logprobs\_data and logprobs\_data.content:  
        low\_confidence\_keywords \= \[\]  
        total\_prob\_low\_confidence \= 0  
        count\_low\_confidence \= 0

        for token\_info in logprobs\_data.content:  
            token \= token\_info.token.strip().lower()  
            token\_prob \= math.exp(token\_info.logprob)

            if token and token not in stop\_words and token\_prob \< low\_confidence\_threshold:  
                count\_low\_confidence \+= 1  
                total\_prob\_low\_confidence \+= token\_prob  
                alternatives \= {  
                    t.token.strip(): math.exp(t.logprob)  
                    for t in token\_info.top\_logprobs  
                    if t.token.strip().lower() \!= token and t.token.strip().lower() not in stop\_words  
                }  
                sorted\_alternatives \= sorted(alternatives.items(), key=lambda x: x\[1\], reverse=True)\[:top\_n\_alternatives\]

                low\_confidence\_keywords.append({  
                    "token": token\_info.token.strip(),  
                    "confidence": token\_prob,  
                    "alternatives": sorted\_alternatives  
                })

        if low\_confidence\_keywords:  
            for item in low\_confidence\_keywords:  
                print(f"Token: '{item\['token'\]}' (Confidence: {item\['confidence'\]:.4f})")  
                if item\["alternatives"\]:  
                    alt\_str \= ", ".join(f"'{alt}': {prob:.4f}" for alt, prob in item\["alternatives"\])  
                    print(f"  Alternatives
 