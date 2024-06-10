# -*- coding: utf-8 -*-
"""Untitled

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jZRLa9BnYLrk83oF62A_SIoVRwaQsMAt
"""

pip install pymupdf pytesseract nltk pillow

!apt-get update
!apt-get install -y tesseract-ocr
!apt-get install -y libtesseract-dev

from google.colab import files
uploaded = files.upload()

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import re

nltk.download('punkt')

# Function to convert PDF to text
def pdf_to_text(pdf_path, txt_output_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text += page.get_text()

    with open(txt_output_path, 'w') as f:
        f.write(text)

# Function to extract images from PDF
def extract_images_from_pdf(pdf_path):
    images = []
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image)
    return images

# Function to perform OCR on extracted images
def perform_ocr_on_images(images):
    ocr_results = []
    for img_index, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        ocr_results.append((img_index, text))
    return ocr_results

# Function to clean and preprocess text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return text

def preprocess_text(text):
    cleaned_text = clean_text(text)
    sentences = sent_tokenize(cleaned_text)
    tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
    return tokenized_sentences

# Example usage
pdf_path = list(uploaded.keys())[0]
txt_output_path = "output.txt"

# Convert PDF to text
pdf_to_text(pdf_path, txt_output_path)

# Extract images and perform OCR
images = extract_images_from_pdf(pdf_path)
ocr_results = perform_ocr_on_images(images)

# Preprocess text
with open(txt_output_path, 'r') as file:
    text = file.read()

preprocessed_text = preprocess_text(text)

# Output results
print("OCR Results:", ocr_results)
print("Preprocessed Text:", preprocessed_text)

pip install openai

import openai

api_key = 'asst_Q0seTqpzz8flyGiSyKdv8x6J'

def initialize_openai(api_key):
    openai.api_key = api_key

def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="davinci",  # Use "davinci" for GPT-3
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Example usage
initialize_openai(api_key)
response = get_gpt3_response("Extract key information from this document: ...")
print(response)