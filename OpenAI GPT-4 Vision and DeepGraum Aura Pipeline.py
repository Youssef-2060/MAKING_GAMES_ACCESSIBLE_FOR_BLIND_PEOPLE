from openai import OpenAI
import base64  # Convert Image to Base64 with error handling
import requests  # Ensures the file exists before reading
from dotenv import load_dotenv  # Load environment variables from .env file
import os  # Prevents crashes due to missing or unreadable files
import cv2  # For image processing (Extracting frames from video)
from pathlib import Path

# Load environment variables from .env file and Initialize OpenAI client
# load_dotenv()
dotenv_path = Path('/Users/youssefibrahim/Documents/GMU Research/Research_with_Dr_Yotam_Gingold 2/.env')
load_dotenv(dotenv_path=dotenv_path)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Error: API key not found. Please check your .env file.")
    exit(1)
client = OpenAI(api_key=api_key)

# Send image to OpenAI GPT-4 Vision API for processing
# Includes error handling for API failures

def encode_image(image_path):
    # This function reads an image from the specified image_path, 
    # converts it to binary, and then encodes it in Base64 format.
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
    "descriptive": "Describe the main elements of the game scene, including characters, objects, and the environment. How do they interact or affect each other?",
    "feature_identification": "Identify the key characters or elements in the game scene. Describe their actions, emotions, or roles in the current gameplay.",
    "contextual_analysis": "Analyze the game scene as if it were part of a specific genre or game style, such as a retro RPG, a futuristic sci-fi, or a medieval fantasy.",
    "technical_analysis": "Extract and list all text visible in this game scene, including user interface elements, dialogue, and any text-based instructions or cues.",
    "creative_interpretation": "Create a short narrative or dialogue based on the game scene. What could the characters be thinking or saying at this moment?"
}

# Send to OpenAI GPT-4 Vision for Image-to-Text Processing
def get_description(image_path, prompt_type="descriptive", custom_prompt=None):
    # This function sends the image data to the OpenAI GPT-4 Vision API for analysis.
    if prompt_type not in PROMPTS:
        raise ValueError(f"Invalid prompt_type: '{prompt_type}'. Choose from: {', '.join(PROMPTS.keys())}")
    prompt = custom_prompt if custom_prompt else PROMPTS.get(prompt_type, PROMPTS["descriptive"])
    image_data = encode_image(image_path)
    if not image_data:
        return "Error: No image data"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPTS.get(prompt_type, PROMPTS["descriptive"])},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI GPT-4 Vision API Error: {e}")
        return "Error processing image"



# Extracting frames from the video
def extract_frame(video_path, frame_number=0, output_path="frame.jpg"):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = cap.read()
    if success:
        cv2.imwrite(output_path, frame)
        return output_path
    else:
        print("Error: Could not extract frame.")
        return None


video_path = "Frames.mp4"
image_path = extract_frame(video_path, frame_number=0)  # Extract the first frame

if image_path is None:
    print("Frame extraction failed. Exiting.")
    exit(1)

if image_path:
    description = get_description(image_path, prompt_type="feature_identification")
    print("OpenAI GPT-4 Vision Output:", description)

# """
# DeepGram Aura Pipeline 
# (I commented it out because the API has only $200 free credit)
# So, let's use the OpenAI GPT-4 Vision API for now and make sure it's working fine first.
# """
# Load environment variables from .env file
# load_dotenv()
# deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")  # Set this in your .env file

# def text_to_speech(text):
#     # This function converts text into speech using the DeepGram API.
#     if not text or text.startswith("Error"):
#         print("Skipping TTS: No valid input text.")
#         return None

#     api_url = "wss://api.deepgram.com/v1/listen"
#     headers = {
#         "Authorization": f"Token {deepgram_api_key}",
#         "Content-Type": "application/json"
#     }
#     payload = {"text": text, "voice": "aura"}

#     try:
#         response = requests.post(api_url, json=payload, headers=headers)
#         response.raise_for_status()

#         audio_path = "output_audio.wav"
#         with open(audio_path, "wb") as audio_file:
#             audio_file.write(response.content)

#         print(f"Audio saved as {audio_path}")
#         return audio_path
#     except requests.exceptions.RequestException as e:
#         print(f"DeepGram API Error: {e}")
#         return None

# # Example Usage for text-to-speech (TTS)
# audio_file = text_to_speech(description)

# # Ensures audio file exists before playing
# if audio_file and os.path.exists(audio_file):
#     try:
#         from playsound import playsound
#         playsound(audio_file)
#     except Exception as e:
#         print(f"Error playing audio: {e}")

'''
Note: Playing Audio in Unity or Godot:
Unity: Use AudioSource.
Godot: Use AudioStreamPlayer.
'''

'''
1) Improved Error Handling: Now prints API errors and avoids crashes.
2) Handles Missing Image Files: Checks if the file exists before attempting to read it.
3) Prevents TTS on Errors: If get_description() fails, TTS won't run.
4) Ensures Audio File Exists Before Playing: Avoids attempting to play non-existent files.
5) Uses `requests.raise_for_status()`: Properly handles HTTP errors.
6) Enhanced Debugging: Now includes specific error messages.
'''


'''
::::Things to Add After Protoyping::::
1. Use logging instead of print() (as you already hinted)

This will help if you're running this in a production or debugging environment later:

import logging
logging.basicConfig(level=logging.INFO)

# Example
logging.info("API key loaded")
logging.error("Error: Could not extract frame.")
2. Support different image formats

You hardcoded .jpg in:

"url": f"data:image/jpeg;base64,{image_data}"
Make it dynamic:

import mimetypes

def get_mime_type(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    return mime_type or "image/jpeg"
Then use:

"image_url": {
    "url": f"data:{get_mime_type(image_path)};base64,{image_data}"
}
3. Return structured results

If the get_description function might eventually be used for multiple purposes (e.g., saving logs, routing audio playback), returning a dict could be more helpful:

return {
    "success": True,
    "content": response.choices[0].message.content
}
Then:

result = get_description(image_path, prompt_type="feature_identification")
if isinstance(result, dict) and result.get("success"):
    print("OpenAI GPT-4 Vision Output:", result["content"])
else:
    print("Failed to get image description.")
4. Modularize config loading

Encapsulate environment loading for reuse:

def load_api_key(env_path, key_name="OPENAI_API_KEY"):
    load_dotenv(dotenv_path=env_path)
    key = os.getenv(key_name)
    if not key:
        logging.error(f"{key_name} not found in .env")
        exit(1)
    return key
'''