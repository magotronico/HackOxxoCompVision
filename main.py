import os
import base64
from dotenv import load_dotenv
from csv2json import csv_to_json
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it in your .env file.")
client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
        
# Function to make a request to the LMM
def request_LMM(planograma_json, image_64):
    """
    Function to send a request to the LMM (Language Model Model) with the provided planograma JSON.
    """
    # Path to your image
    if image_64 == None:
        image_path = "path_to_your_image.jpg"

    # Getting the Base64 string
    base64_image = encode_image(image_path)


    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    { "type": "input_text", "text": "what's in this image?" },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )
    
    return response

def main():
    file_path = r'..\files\HackOxxo.csv'
    planograma = csv_to_json(file_path, 'HackOxxo.json')

    errors = request_LMM(planograma)

    if errors:
        print("Errors found in the planograma:")
        for error in errors:
            print(error)
    else:
        print("No errors found in the planograma.")


if __name__ == "__main__":
    main()
