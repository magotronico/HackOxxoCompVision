import requests
import json

# File paths for your image and JSON
image_path = "../files/estante1.jpg"
json_path = "../files/HackOxxo.json"

# Load image file
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# Load JSON file
with open(json_path, "r") as json_file:
    planogram_data = json.load(json_file)

print("Loaded image and JSON data successfully.")

# API endpoint URL (adjust if your FastAPI server runs on a different host/port)
url = "http://localhost:8000/analyze-shelf/"

# Prepare data and files
store_id = "STORE123"
with open("../files/productos_estante_1.json", "r") as f:
    planogram_data = json.load(f)
files = {"image": ("estante1.jpg", image_data, "image/jpeg")}
data = {"store_id": store_id, "planograma": json.dumps(planogram_data)}

print("Prepared data for API call.")
# Make the API call
response = requests.post(url, files=files, data=data)

# Print the response
print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))