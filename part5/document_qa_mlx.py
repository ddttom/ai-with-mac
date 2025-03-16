#!/usr/bin/env python3

"""
Enhanced document Q&A system with vector search using MLX.
"""

import os
import re
import sys
import argparse
import numpy as np
import pypdf
from mlx_lm import generate, load
from mlx.core import array

class EnhancedDocumentQA:
    """Enhanced document Q&A system with vector search."""
    def __init__(self, model_path):
        """Initialize the system."""
        print(f"Loading model from {model_path}, please wait...")
        self.model, self.tokenizer = load(model_path)
        print("Model loaded successfully!")
        
        self.document_chunks = []
        self.chunk_embeddings = []
    
    def load_document(self, pdf_path):
        """Load and process a document."""
        print(f"Reading document: {pdf_path}")
        document_text = self._extract_text_from_pdf(pdf_path)
        
        if not document_text:
            print("Failed to extract text from the document.")
            return False
        
        # Split into semantically meaningful chunks
        self.document_chunks = self._split_into_semantic_chunks(document_text)
        print(f"Document split into {len(self.document_chunks)} chunks")
        
        # Create embeddings for each chunk
        self._create_embeddings()
        
        return True
    
    def answer_question(self, question):
        """Answer a question about the loaded document."""
        if not self.document_chunks:
            print("No document loaded. Please load a document first.")
            return None
        
        # Create embedding for the question
        question_embedding = self._embed_text(question)
        
        # Find most relevant chunks
        relevant_chunks = self._find_relevant_chunks(question_embedding, top_k=3)
        
        # Combine relevant chunks into context
        context = "\n\n".join([self.document_chunks[idx] for idx in relevant_chunks])
        
        # Create prompt for the model
        prompt = f"""Answer the question based ONLY on the following context:

Context:
{context}

Question: {question}

Answer:"""
        
        # Generate answer
        gen_config = {
            "max_tokens": 500,
            "temperature": 0.2,
            "top_p": 0.9
        }
        
        tokens = self.tokenizer.encode(prompt)
        generated_tokens = generate(self.model, self.tokenizer, tokens, gen_config)
        answer = self.tokenizer.decode(generated_tokens[len(tokens):])
        
        return answer.strip()
    
    def _extract_text_from_pdf(self, pdf_path):
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
    
    def _split_into_semantic_chunks(self, text, max_chunk_size=1500):
        """Split text into semantically meaningful chunks."""
        # Split by section headers or paragraphs
        sections = re.split(r'(?=\n\s*[A-Z][^a-z]*\n)|(?=\n\n)', text)
        
        chunks = []
        current_chunk = ""
        
        for section in sections:
            # Clean the section
            section = section.strip()
            if not section:
                continue
            
            # If adding this section exceeds max size, start a new chunk
            if len(current_chunk) + len(section) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = section
            else:
                if current_chunk:
                    current_chunk += "\n\n" + section
                else:
                    current_chunk = section
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _create_embeddings(self):
        """Create embeddings for all chunks."""
        print("Creating embeddings for document chunks...")
        self.chunk_embeddings = []
        
        for i, chunk in enumerate(self.document_chunks):
            embedding = self._embed_text(chunk)
            self.chunk_embeddings.append(embedding)
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(self.document_chunks)} chunks")
    
    def _embed_text(self, text):
        """Create an embedding for a piece of text using the model."""
        # For simplicity, we'll use a basic method:
        # 1. Tokenize the text
        # 2. Get the token IDs
        # 3. Create a normalized frequency vector
        
        tokens = self.tokenizer.encode(text)
        
        # Create a frequency vector of token IDs
        vocab_size = self.tokenizer.vocab_size
        embedding = np.zeros(vocab_size)
        
        unique_tokens, counts = np.unique(tokens, return_counts=True)
        for token, count in zip(unique_tokens, counts):
            if token < vocab_size:
                embedding[token] = count
        
        # Normalize the embedding
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def _find_relevant_chunks(self, query_embedding, top_k=3):
        """Find the most relevant chunks for a query embedding."""
        # Calculate cosine similarity
        similarities = []
        for chunk_embedding in self.chunk_embeddings:
            similarity = np.dot(query_embedding, chunk_embedding)
            similarities.append(similarity)
        
        # Get indices of top-k chunks
        return np.argsort(similarities)[-top_k:][::-1]

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Enhanced document Q&A system with vector search")
    parser.add_argument("--model", type=str, default="models/gemma-2b-it-4bit",
                        help="Path to the model directory")
    parser.add_argument("--pdf", type=str, required=True,
                        help="Path to the PDF document")
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf):
        print(f"Error: PDF file not found at {args.pdf}")
        sys.exit(1)
    
    qa_system = EnhancedDocumentQA(args.model)
    
    if not qa_system.load_document(args.pdf):
        print("Failed to load document.")
        sys.exit(1)
    
    print("\nEnhanced Document Q&A System (type 'exit' to quit)")
    
    while True:
        question = input("\nYour question: ")
        if question.lower() in ["exit", "quit"]:
            break
        
        print("\nSearching document and generating answer...")
        answer = qa_system.answer_question(question)
        
        print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()
