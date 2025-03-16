#!/usr/bin/env python3
"""
A simple document Q&A system using MLX language models.
"""
import os
import sys
import argparse
import pypdf
from mlx_lm import generate, load

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = pypdf.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def split_into_chunks(text, chunk_size=1500, overlap=200):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    
    return chunks

def document_qa(model_path, pdf_path):
    """Answer questions about a document using an MLX language model."""
    # Extract text from PDF
    print(f"Reading document: {pdf_path}")
    document_text = extract_text_from_pdf(pdf_path)
    
    if not document_text:
        print("Failed to extract text from the document.")
        return
    
    # Split into chunks
    chunks = split_into_chunks(document_text)
    print(f"Document split into {len(chunks)} chunks")
    
    # Load model
    print(f"Loading model from {model_path}, please wait...")
    model, tokenizer = load(model_path)
    print("Model loaded successfully!")
    
    print("\nDocument Q&A System (type 'exit' to quit)")
    
    while True:
        question = input("\nYour question: ")
        if question.lower() in ["exit", "quit"]:
            break
        
        # For each chunk, check if it contains relevant information
        print("Analyzing document...")
        best_answer = None
        best_relevance = 0
        
        for i, chunk in enumerate(chunks):
            # Create prompt to evaluate chunk relevance
            relevance_prompt = f"""Assess if this text contains information to answer the question.
Question: {question}
Text: {chunk[:1000]}...
Rate relevance from 0-10 (where 10 is highest):"""
            
            # Evaluate relevance
            gen_config = {
                "max_tokens": 10,
                "temperature": 0.1
            }
            tokens = tokenizer.encode(relevance_prompt)
            generated_tokens = generate(model, tokenizer, tokens, gen_config)
            response = tokenizer.decode(generated_tokens[len(tokens):])
            
            # Try to extract numeric rating
            try:
                relevance = int(''.join(filter(str.isdigit, response[:10])))
                if relevance > best_relevance:
                    # If relevant, use this chunk to answer the question
                    answer_prompt = f"""Answer the question based ONLY on the following text:
Text: {chunk}

Question: {question}

Answer:"""
                    
                    gen_config = {
                        "max_tokens": 500,
                        "temperature": 0.2
                    }
                    tokens = tokenizer.encode(answer_prompt)
                    generated_tokens = generate(model, tokenizer, tokens, gen_config)
                    answer = tokenizer.decode(generated_tokens[len(tokens):])
                    
                    best_answer = answer
                    best_relevance = relevance
                    
                    # If we get a very relevant chunk, stop looking
                    if relevance >= 8:
                        break
            except:
                continue
        
        # Print the best answer found
        if best_answer and best_relevance > 0:
            print(f"\nAnswer: {best_answer}")
        else:
            print("\nI couldn't find relevant information to answer that question.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Answer questions about a PDF document using an MLX language model")
    parser.add_argument("--model", type=str, default="models/gemma-2b-it-4bit",
                        help="Path to the model directory")
    parser.add_argument("--pdf", type=str, required=True,
                        help="Path to the PDF document")
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf):
        print(f"Error: PDF file not found at {args.pdf}")
        sys.exit(1)
        
    document_qa(args.model, args.pdf)
