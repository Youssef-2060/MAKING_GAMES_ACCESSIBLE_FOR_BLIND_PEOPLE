"""
Groq Pipeline
"""

import base64  # Convert Image to Base64 with error handling
import requests  # Ensures the file exists before reading
import os  # Prevents crashes due to missing or unreadable files
from groq import Groq  # Import Groq API client

# Initialize Groq Client
client = Groq(api_key="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")

# Send image to Groq API for processing
# Includes error handling for API failures

def encode_image(image_path):
    """
    This function reads an image from the specified image_path, 
    converts it to binary, and then encodes it in Base64 format.
    """
    if not os.path.exists(image_path):
        print("Error: Image file not found.")
        return None
    try:
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode('utf-8')
    except Exception as e:
        print(f"Error reading image file: {e}")
        return None

# Predefined prompts for different types of analysis
PROMPTS = {
    "descriptive": "Describe the objects and their relationships in this image.",
    "feature_identification": "Identify all people in this image and describe their emotions.",
    "contextual_analysis": "Analyze this image in the style of Renaissance paintings.",
    "technical_analysis": "Extract and list all text from this image in JSON format.",
    "creative_interpretation": "Generate a short story based on this image."
}

# Send to Groq for Image-to-Text Processing
def get_description(image_path, prompt_type="descriptive"):
    """
    This function sends the image data to the Groq API for analysis.
    """
    image_data = encode_image(image_path)
    if not image_data:
        return "Error: No image data"

    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": "Bearer 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"}
    payload = {
        "image": image_data,
        "prompt": PROMPTS.get(prompt_type, PROMPTS["descriptive"])  # Default to descriptive
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("description", "No description found")
    except requests.exceptions.RequestException as e:
        print(f"Groq API Error: {e}")
        return "Error processing image"

# Example Usage
image_path = "/Users/youssefibrahim/Documents/Research with Dr.Yotam Gingold/frame.png"
description = get_description(image_path, prompt_type="feature_identification")
print("Groq Output:", description)

# Groq LLM Call
def groq_chat():
    """
    This function uses the Groq API client to analyze an image.
    """
    image_data = encode_image(image_path)
    if not image_data:
        print("Error: No image data")
        return "Error: No image data"
    else:
        print("Image data encoded successfully.")
    
    messages = [
        {"role": "system", "content": "Analyse the image and provide a description."},
        {"role": "user", "content": f"Here is the image data: {image_data}"}
    ]
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")

# Call the function
groq_chat()

"""
DeepGram Aura Pipeline 
(I commented it out because the API has only $200 free credit)
So, let's use the Groq API for now and make sure it's working fine first.
"""

def text_to_speech(text):
    """
    This function converts text into speech using the DeepGram API.
    """
    if not text or text.startswith("Error"):
        print("Skipping TTS: No valid input text.")
        return None

    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Token Daa45e434c8d61f47801f3b4050325b258539cad7",
        "Content-Type": "application/json"
    }
    payload = {"text": text, "voice": "aura"}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        
        audio_path = "output_audio.wav"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)
        
        print(f"Audio saved as {audio_path}")
        return audio_path
    except requests.exceptions.RequestException as e:
        print(f"DeepGram API Error: {e}")
        return None

# Example Usage
audio_file = text_to_speech(description)

# Ensures audio file exists before playing
if audio_file and os.path.exists(audio_file):
    try:
        from playsound import playsound
        playsound(audio_file)
    except Exception as e:
        print(f"Error playing audio: {e}")

'''
Note: Playing Audio in Unity or Godot:
Unity: Use AudioSource.
Godot: Use AudioStreamPlayer.
'''
'''
1)Improved Error Handling: Now prints API errors and avoids crashes.
2)Handles Missing Image Files: Checks if the file exists before attempting to read it.
3)Prevents TTS on Errors: If get_description() fails, TTS won't run.
4)Ensures Audio File Exists Before Playing: Avoids attempting to play non-existent files.
5)Uses `requests.raise_for_status()`: Properly handles HTTP errors.
6)Enhanced Debugging: Now includes specific error messages.
'''
