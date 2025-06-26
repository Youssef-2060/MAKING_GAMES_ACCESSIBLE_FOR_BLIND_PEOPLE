"""
Groq Pipeline
"""

import base64
import requests

# Convert Image to Base64
def encode_image(image_path):
    try:
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode('utf-8')
    except FileNotFoundError:
        print("Error: Image file not found.")
        return None

# Send to Groq for Image-to-Text Processing
def get_description(image_path):
    image_data = encode_image(image_path)
    if not image_data:
        return "No image data"

    api_url = "https://api.groq.com/v1/image-to-text"
    headers = {"Authorization": "Bearer YOUR_GROQ_API_KEY"}
    payload = {"image": image_data}

    response = requests.post(api_url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("description", "No description found")
    else:
        print(f"Groq API Error: {response.status_code} - {response.text}")
        return "Error processing image"

# Example Usage
image_path = "frame.png"
description = get_description(image_path)
print("Groq Output:", description)


"""
DeepGram Aura Pipeline
"""

def text_to_speech(text):
    if not text or text.startswith("Error"):
        print("Skipping TTS: No valid input text.")
        return None

    api_url = "https://api.deepgram.com/v1/speak"
    headers = {
        "Authorization": "Token YOUR_DEEPGRAM_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {"text": text, "voice": "aura"}
    
    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        with open("output_audio.wav", "wb") as audio_file:
            audio_file.write(response.content)
        print("Audio saved as output_audio.wav")
        return "output_audio.wav"
    else:
        print(f"DeepGram API Error: {response.status_code} - {response.text}")
        return None

# Example Usage
audio_file = text_to_speech(description)

# Optional: Play the audio
if audio_file:
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
✅ Error Handling: Now prints API errors for debugging.
✅ Handles Missing Image File: Avoids crashing if frame.png is missing.
✅ Prevents TTS on Errors: If get_description() fails, TTS won't run.
✅ Audio Playback (Optional): Plays audio if playsound is installed.
'''
