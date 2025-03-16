#!/usr/bin/env python3

"""
Simple web server for AI with Mac demonstration.
"""

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for
from summarize import Summarizer
from caption import ImageCaptioner

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Initialize models
summarizer = Summarizer()
captioner = ImageCaptioner()

# Create upload directories
os.makedirs("../uploads", exist_ok=True)

@app.route("/")
def index():
    """Render main page."""
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize_text():
    """Summarize text input using MLX."""
    text = request.form.get("text", "")
    
    if not text:
        return render_template("index.html", error="Please enter some text to summarize.")
    
    summary = summarizer.summarize(text)
    
    return render_template("result.html", 
                          result_type="summary",
                          original=text,
                          result=summary,
                          framework="MLX")

@app.route("/caption", methods=["POST"])
def caption_image():
    """Caption uploaded image using PyTorch with Metal."""
    if "image" not in request.files:
        return render_template("index.html", error="No image uploaded.")
    
    file = request.files["image"]
    if file.filename == "":
        return render_template("index.html", error="No image selected.")
    
    # Save uploaded image
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    filepath = os.path.join("../uploads", filename)
    file.save(filepath)
    
    # Generate caption
    caption = captioner.generate_caption(filepath)
    
    return render_template("result.html",
                          result_type="caption",
                          image_path="../uploads/" + filename,
                          result=caption,
                          framework="PyTorch with Metal")

if __name__ == "__main__":
    app.run(debug=True)
