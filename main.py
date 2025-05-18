from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
import base64
import aiohttp
import os
from dotenv import load_dotenv
import json

from openai import OpenAI

app = FastAPI()

# Load environment variables
load_dotenv()
gpt4v_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Encode image content to base64
def encode_image_bytes(content: bytes) -> str:
    return base64.b64encode(content).decode("utf-8")


# Call GPT-4 Vision to find planogram errors
# async def analyze_planogram(image_content: bytes, planograma_data: dict):
#     base64_image = encode_image_bytes(image_content)

#     headers = {
#         "Authorization": f"Bearer {gpt4v_key}",
#         "Content-Type": "application/json"
#     }

#     system_message = """
#         You are an expert in detecting product placement errors on retail shelves.
#         Respond in a clear, structured, and professional manner. Prioritize accuracy and brevity.
#         Return only the relevant data or analysis requested, without additional commentary.
#         If you complete the task successfully you will receive a reward, if you fail to complete the task you will be penalized.
#     """

#     user_message = """
#         Your task is to analyze the list of products below and identify errors in shelf organization. There are two types of possible errors:
#         1. **Empty Spot** - A position on the shelf that should be occupied but is currently empty.
#         2. **Product Misplaced** - A product is found in a location where it should not be.

#         Please analyze the shelf layout using the following guidelines:
#         - Each "Charola" represents a shelf level (starting from the bottom as Charola 1).
#         - Each "Posicion en Charola" represents the horizontal position on that shelf, from left to right.
#         - Each "Cantidad de Frentes" represents the number of the same product that should be displayed starting from the left on the "Posicion en Charola".
#         - Treat the shelf as a 2D Cartesian grid where the bottom-left corner is coordinate **(1, 1)**.
#         - Coordinates are defined as **(x, y)**, where:
#         - **x** is the position from left to right (Posicion en Charola),
#         - **y** is the vertical level (Charola).

#         Return the identified issues in the following JSON format:
#         ```json
#         [
#             {
#                 "error_type": "empty_spot",
#                 "coordinates": "(x, y)"
#             },
#             {
#                 "error_type": "product_misplaced",
#                 "coordinates": "(x, y)",
#                 "CB": "product_code"
#             }
#         ]
#         ```
#     """

#     payload = {
#         "model": "gpt-4o",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {"role": "system", "content": system_message},
#                     {"type": "text", "text": user_message},
#                     {"type": "text", "text": f"List of Products:\n{json.dumps(planograma_data, indent=2)}"},
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}"
#                         }
#                     }
#                 ]
#             }
#         ],
#         "max_tokens": 1000
#     }

#     async with aiohttp.ClientSession() as session:
#         async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload) as response:
#             try:
#                 response_json = await response.json()
#                 print("GPT response:", response_json)  # Debugging line
#                 result_text = response_json["choices"][0]["message"]["content"]

#                 return json.loads(result_text)  # Ensure GPT returns valid JSON
#             except Exception as e:
#                 print("Error processing GPT response:", e)
#                 return {"error": "Failed to process image or invalid response format"}
async def analyze_planogram(image_content: bytes, planograma_data: dict):
    base64_image = encode_image_bytes(image_content)

    system_message = {
        "role": "system",
        "content": [
            {
                "type": "input_text",
                "text": 
                    "You are an expert in detecting product placement errors on retail shelves.\nRespond in a clear, structured, and professional manner. Prioritize accuracy and brevity.\nReturn only the relevant data or analysis requested, without additional commentary.\nIf you complete the task successfully you will receive a reward, if you fail to complete the task you will be penalized."
            }
        ]
    }

    user_message = {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": (
                    "Your task is to analyze the list of products below and identify errors in shelf organization. "
                    "There are two types of possible errors:\n"
                    "1. **empty_spot** – A position on the shelf that should be occupied but is currently empty.\n"
                    "2. **product_misplaced** – A product is found in a location where it should not be.\n\n"

                    "Use the following shelf layout rules:\n"
                    "- Each \"Charola\" represents a vertical level (starting from the bottom as Charola 1).\n"
                    "- Each \"Posicion en Charola\" represents the horizontal position on that shelf (left to right).\n"
                    "- \"Cantidad de Frentes\" tells how many units of the same product should appear in sequence starting at the given position.\n"
                    "- The shelf is a 2D Cartesian grid with coordinates **(x, y)** where:\n"
                    "    - x = horizontal position (Posicion en Charola)\n"
                    "    - y = vertical shelf level (Charola)\n"
                    "- The bottom-left position is (1, 1).\n\n"

                    "**Example:**\n"
                    "If the planogram indicates that at (3, 2) there should be CB: \"7501045403014\", and the image shows it missing, then this is an `empty_spot`.\n"
                    "If the image shows CB: \"7506339394719\" at position (1, 1), but this product is not expected there, then it's a `product_misplaced`.\n\n"

                    "**Important:**\n"
                    "- Be strict and systematic.\n"
                    "- Cross-verify each coordinate against the product list.\n"
                    "- Only return valid errors that can be confirmed from the visual input.\n\n"

                    "Return the identified issues in the following JSON format:\n"
                    "```json\n"
                    "[\n"
                    "  {\n"
                    "    \"error_type\": \"empty_spot\",\n"
                    "    \"coordinates\": \"(x, y)\"\n"
                    "  },\n"
                    "  {\n"
                    "    \"error_type\": \"product_misplaced\",\n"
                    "    \"coordinates\": \"(x, y)\",\n"
                    "    \"CB\": \"product_code\"\n"
                    "  }\n"
                    "]\n"
                    "```\n\n"
                    f"List of Products:\n{json.dumps(planograma_data, indent=2)}"
                )
            },
            {
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{base64_image}"
                
            }
        ]
    }

    try:
        response = client.responses.create(
            model="gpt-4o",
            input=[system_message, user_message],
            reasoning={},
            tools=[],
            temperature=0.7,
            max_output_tokens=2048,
            top_p=1,
            text={"format": {
                "type": "json_object"
                }
            }
        )
        content = response.output[0]
        print(content)
        content_json = content.content[0].text
        print(content, type(content))
        return json.loads(content_json)
        
    except Exception as e:
        print("Error processing GPT response:", e)
        return {"error": "Failed to process image or invalid response format"}

@app.post("/analyze-shelf/")
async def analyze_shelf(
    store_id: str = Form(...),
    planograma: str = Form(...),  # Planogram as JSON string
    image: UploadFile = File(...)
):
    try:
        print("Received request with store_id:", store_id)  # Debugging line
        content = await image.read()
        planograma_data = json.loads(planograma)

        result = await analyze_planogram(content, planograma_data)
        print("Analysis result:", result)  # Debugging line

        return JSONResponse(content={"store_id": store_id, "analysis_result": result})

    except Exception as e:
        print("Unexpected error:", e)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})
