from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
import base64
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

# Analyze the planogram using OpenAI's GPT-4
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
                "Analyze the provided product list and shelf image to identify organizational errors.\n\n"

                "**Types of Errors:**\n"
                "1. `empty_spot` - A location expected to have a product but is visibly empty.\n"
                "2. `product_misplaced` - A product appears where it does not belong.\n\n"

                "**Shelf Layout Rules:**\n"
                "- A 'Charola' represents the vertical shelf level (bottom = Charola 1).\n"
                "- 'Posicion en Charola' is the horizontal position (left to right).\n"
                "- 'Cantidad de Frentes' = number of identical product units in a row starting at the given position.\n"
                "- Coordinates follow a 2D format: **(x, y)**, where:\n"
                "  - x = horizontal position\n"
                "  - y = vertical level\n"
                "  - (1, 1) is the bottom-left of the shelf\n\n"

                "**Examples:**\n"
                "- If product CB `7501045403014` is expected at (3, 2) but missing: `{ \"error_type\": \"empty_spot\", \"coordinates\": \"(3, 2)\" }`\n"
                "- If product CB `7506339394719` appears at (1, 1) but shouldn't: `{ \"error_type\": \"product_misplaced\", \"coordinates\": \"(1, 1)\", \"CB\": \"7506339394719\" }`\n\n"

                "**Instructions:**\n"
                "- Be strict and systematic.\n"
                "- Cross-check each product's expected vs. actual position.\n"
                "- Only report errors that can be visually confirmed.\n\n"

                "**Output Format (JSON):**\n"
                "```json\n"
                "[\n"
                "  { \"error_type\": \"empty_spot\", \"coordinates\": \"(x, y)\" },\n"
                "  { \"error_type\": \"product_misplaced\", \"coordinates\": \"(x, y)\", \"CB\": \"product_code\" }\n"
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
